import customtkinter as ctk
from datetime import datetime
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import StringVar
import importlib
from sidebar import SidebarFrame
from CTkToolTip import CTkToolTip
from responsive_utils import ThemeToggleButton
import database
import locale

# Thème clair moderne avec accents colorés
ctk.set_appearance_mode('Light')
ctk.set_default_color_theme('blue')

class DashboardFrame(ctk.CTkFrame):
    """
    Frame du tableau de bord moderne, intuitif et esthétique,
    conçu selon les 10 heuristiques de Nielsen.
    """
    def __init__(self, master, user_info, toplevel_window=None, standalone=True):
        super().__init__(master)
        self.master = master
        # Correction : toujours passer la fenêtre principale à la sidebar
        if toplevel_window is None:
            self.toplevel_window = master
        else:
            self.toplevel_window = toplevel_window
        
        # Données utilisateur
        self.user = user_info

        # Données pour les tableaux
        self.alert_products = [
            {'name': 'Souris optique Dell', 'stock': '3 / 10', 'loc': 'E0-A1-01'},
            {'name': 'Clavier USB HP', 'stock': '7 / 15', 'loc': 'E1-B2-03'},
            {'name': 'Disque Dur SSD 1To', 'stock': '9 / 10', 'loc': 'E4-A1-09'},
        ]
        self.alert_products_sort_key = 'name' # 'name' ou 'stock'

        # Données pour l'activité
        self.activity_data = [
            {'icon': '📥', 'user': 'A. Dupont', 'action': 'a reçu 50 unités de "Souris optique"', 'time': 'Il y a 2h', 'color': '#3B82F6', 'type': 'Réception'},
            {'icon': '✏️', 'user': 'B. Martin', 'action': 'a modifié l\'emplacement du produit "Clavier USB"', 'time': 'Il y a 5h', 'color': '#F59E0B', 'type': 'Modification'},
            {'icon': '🚚', 'user': 'C. Durand', 'action': 'a expédié la commande #CDE789', 'time': 'Il y a 8h', 'color': '#10B981', 'type': 'Expédition'},
            {'icon': '📥', 'user': 'E. Petit', 'action': 'a reçu 20 unités de "Moniteur Samsung"', 'time': 'Hier', 'color': '#3B82F6', 'type': 'Réception'},
            {'icon': '➕', 'user': 'F. Girard', 'action': 'a ajouté le produit "SSD 2To"', 'time': 'Hier', 'color': '#6D28D9', 'type': 'Modification'},
        ]
        self.activity_filter = 'Tous' # 'Tous', 'Réception', 'Expédition', 'Modification'

        # Configuration responsive
        self.responsive_config = self.master.get_responsive_config() if hasattr(self.master, 'get_responsive_config') else {}
        
        # Construction UI
        if standalone:
            self._build_topbar()
            self._build_sidebar()
            self._build_main()
        else:
            self.pack(fill="both", expand=True)
            self._build_main(add_padding=False)

        self._update_time()

        # Lier le redimensionnement
        self.bind("<Configure>", self._on_frame_resize)

        self.refresh_interval = 3000  # 3 secondes
        self.refresh_data()  # Démarre le rafraîchissement automatique

    def _set_alert_products_sort(self, key):
        """Définit la clé de tri pour les produits en alerte et met à jour l'affichage."""
        self.alert_products_sort_key = key
        self._update_alert_products_display()

    def _update_alert_products_display(self):
        """Efface et redessine la liste des produits en alerte en fonction du tri."""
        is_name_sort = self.alert_products_sort_key == 'name'
        is_stock_sort = self.alert_products_sort_key == 'stock'

        # Mettre à jour l'apparence des boutons de tri
        self.sort_name_button.configure(
            fg_color="#3B82F6" if is_name_sort else "transparent",
            text_color="white" if is_name_sort else "#374151",
            border_width=0 if is_name_sort else 1
        )
        self.sort_stock_button.configure(
            fg_color="#3B82F6" if is_stock_sort else "transparent",
            text_color="white" if is_stock_sort else "#374151",
            border_width=0 if is_stock_sort else 1
        )

        # Effacer le contenu actuel
        for widget in self.alert_products_container.winfo_children():
            widget.destroy()

        # Trier les données
        if self.alert_products_sort_key == 'name':
            sorted_products = sorted(self.alert_products, key=lambda p: p['name'])
        elif self.alert_products_sort_key == 'stock':
            # Extrait le premier nombre (le stock actuel) pour le tri
            sorted_products = sorted(self.alert_products, key=lambda p: int(p['stock'].split('/')[0].strip()))
        else:
            sorted_products = self.alert_products

        # Redessiner la liste
        for p in sorted_products:
            row = ctk.CTkFrame(self.alert_products_container, fg_color='transparent')
            row.pack(fill='x', pady=2)
            ctk.CTkLabel(row, text=f"📦 {p['name']}", font=ctk.CTkFont(size=13)).pack(side='left')
            ctk.CTkLabel(row, text=f"Stock: {p['stock']} | Loc: {p['loc']}", font=ctk.CTkFont(size=12), text_color='#666666').pack(side='right')

    def _set_activity_filter(self, filter_type):
        """Définit le filtre pour l'activité récente et met à jour l'affichage."""
        self.activity_filter = filter_type
        self._update_activity_display()

    def _update_activity_display(self):
        """Efface et redessine la liste d'activités en fonction du filtre."""
        # Mettre à jour l'apparence des boutons de filtre
        for f_type, button in self.activity_filter_buttons.items():
            is_active = self.activity_filter == f_type
            button.configure(
                fg_color="#3B82F6" if is_active else "transparent",
                text_color="white" if is_active else "#374151",
                border_width=0 if is_active else 1
            )

        # Effacer le contenu actuel
        for widget in self.activity_list_container.winfo_children():
            widget.destroy()

        # Adapter le filtre pour la correspondance
        def filtre_type(item_type):
            if item_type == 'Entrée':
                return 'Réception'
            elif item_type == 'Sortie':
                return 'Expédition'
            else:
                return 'Modification'

        # Filtrer les données
        if self.activity_filter == 'Tous':
            filtered_activity = self.activity_data
        else:
            filtered_activity = [item for item in self.activity_data if filtre_type(item['type']) == self.activity_filter]

        # Redessiner la liste
        if not filtered_activity:
            ctk.CTkLabel(self.activity_list_container, text="Aucune activité de ce type.", font=ctk.CTkFont(size=14), text_color="#6B7280").pack(pady=20)
            return

        for item in filtered_activity:
            item_frame = ctk.CTkFrame(self.activity_list_container, fg_color='#F8F9FA', corner_radius=8)
            item_frame.pack(fill='x', pady=5)
            content_frame = ctk.CTkFrame(item_frame, fg_color='transparent')
            content_frame.pack(fill='x', padx=15, pady=10)
            icon_label = ctk.CTkLabel(content_frame, text=item['icon'], font=ctk.CTkFont(size=20), text_color=item['color'])
            icon_label.pack(side='left')
            ctk.CTkLabel(content_frame, text=f'{item["user"]} {item["action"]}', font=ctk.CTkFont(size=14), text_color='#333333').pack(side='left', padx=(10,0))
            ctk.CTkLabel(content_frame, text=item['time'], font=ctk.CTkFont(size=13), text_color='#999999').pack(side='right')

    def _build_topbar(self):
        topbar = ctk.CTkFrame(self, height=80, fg_color='#F7F9FC', border_width=1, border_color='#E0E0E0')
        topbar.pack(side='top', fill='x')
        try:
            logo_img = Image.open('logo.png')
            logo = ctk.CTkImage(light_image=logo_img, size=(60, 60))
            ctk.CTkLabel(topbar, image=logo, text='').pack(side='left', padx=25, pady=10)
        except:
            ctk.CTkLabel(topbar, text='SGE', font=ctk.CTkFont(size=24, weight='bold'), text_color='#333333').pack(side='left', padx=25)
        ctk.CTkLabel(topbar, text='Tableau de bord', font=ctk.CTkFont(size=24, weight='bold'), text_color='#333333').pack(side='left', padx=(0,10))
        ctk.CTkLabel(topbar, text="Vue d'ensemble de votre entrepôt", font=ctk.CTkFont(size=16), text_color='#666666').pack(side='left')
        
        # Conteneur pour la barre de recherche avec loupe
        search_container = ctk.CTkFrame(topbar, fg_color='white', corner_radius=12, width=450, height=44)
        search_container.pack(side='right', padx=25, pady=10)
        search_container.pack_propagate(False)
        
        # Barre de recherche avec placeholder
        self.search_var = StringVar()
        self.search_entry = ctk.CTkEntry(
            search_container, 
            textvariable=self.search_var, 
            placeholder_text='Rechercher...', 
            width=350, 
            height=40, 
            corner_radius=12,
            border_width=0,
            fg_color='transparent',
            font=ctk.CTkFont(size=14),
            text_color='#1F2937'
        )
        self.search_entry.pack(side='left', padx=(15, 5), pady=2)
        
        # Bouton pour effacer la recherche (initialement caché)
        self.clear_search_button = ctk.CTkButton(
            search_container,
            text='✕',
            width=20,
            height=20,
            corner_radius=10,
            fg_color='transparent',
            hover_color='#E5E7EB',
            text_color='#9CA3AF',
            font=ctk.CTkFont(size=12, weight='bold'),
            command=self._clear_search
        )
        # La visibilité du bouton sera gérée par _update_clear_button
        
        # Bouton de recherche AMÉLIORÉ - Design moderne et attrayant
        search_button = ctk.CTkButton(
            search_container,
            text='🔍',
            width=60,
            height=40,
            corner_radius=10,
            fg_color='#3B82F6',
            hover_color='#1D4ED8',
            text_color='white',
            font=ctk.CTkFont(size=20, weight='bold'),
            command=self._perform_search,
            border_width=0,
            # Effet de gradient simulé avec une couleur plus riche
        )
        search_button.pack(side='right', padx=(5, 15), pady=2)
        
        # Ajouter un effet de survol personnalisé
        def on_search_hover_enter(event):
            search_button.configure(fg_color='#1D4ED8', text='🔍')
            
        def on_search_hover_leave(event):
            search_button.configure(fg_color='#3B82F6', text='🔍')
            
        search_button.bind('<Enter>', on_search_hover_enter)
        search_button.bind('<Leave>', on_search_hover_leave)
        
        # Bouton notifications
        self.notif_count = ctk.StringVar(value="0")
        self.nf_btn = ctk.CTkButton(topbar, textvariable=self.notif_count, width=100, height=40, corner_radius=12, fg_color='#FFE082', text_color='#333333', font=ctk.CTkFont(size=14, weight='bold'), command=self._show_notifications_popup)
        self.nf_btn.pack(side='right', padx=10, pady=10)
        CTkToolTip(self.nf_btn, message="Afficher les notifications et alertes les plus récentes.", corner_radius=8, border_width=1)
        
        # Bind pour la recherche avec Entrée
        self.search_entry.bind('<Return>', lambda event: self._perform_search())
        
        # Bind pour le focus (placeholder disparaît automatiquement avec CustomTkinter)
        self.search_entry.bind('<FocusIn>', self._on_search_focus_in)
        self.search_entry.bind('<FocusOut>', self._on_search_focus_out)
        
        # Mettre à jour l'état du bouton "effacer" à chaque changement
        self.search_var.trace_add('write', self._update_clear_button)
        self._update_clear_button() # Appel initial

        # Bouton de thème
        self.theme_button = ThemeToggleButton(topbar, self.toplevel_window)
        self.theme_button.pack(side='right', padx=(0, 20), pady=10)

        btn = ctk.CTkButton(topbar, text="📊 Voir Rapports", fg_color="#3b82f6", hover_color="#2563eb", text_color="white", corner_radius=8, font=ctk.CTkFont(size=14, weight="bold"), width=150, height=36, command=self._show_analytics)
        btn.pack(side='right', padx=(0, 20), pady=10)

    def _build_sidebar(self):
        self.sidebar = SidebarFrame(self, self.toplevel_window)
        self.sidebar.pack(side='left', fill='y')
        # Définir le bouton Dashboard comme actif
        self.sidebar.set_active_button("Dashboard")

    def _confirm_logout(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmation de déconnexion")
        dialog.geometry("370x180")
        dialog.configure(fg_color='white')
        dialog.grab_set()
        dialog.resizable(False, False)
        ctk.CTkLabel(dialog, text="Voulez-vous vraiment vous déconnecter ?", font=ctk.CTkFont(size=16, weight='bold'), text_color='#333333').pack(pady=(28,8), padx=20)
        ctk.CTkLabel(dialog, text="Vous serez redirigé vers la page de connexion.", font=ctk.CTkFont(size=13), text_color='#666666').pack(pady=(0,10), padx=20)
        btn_frame = ctk.CTkFrame(dialog, fg_color='transparent')
        btn_frame.pack(pady=(0,18))
        def logout_and_redirect():
            if self.toplevel_window:
                self.toplevel_window.show_auth_frame()
            else:
                self.destroy()
        ctk.CTkButton(btn_frame, text='Oui, me déconnecter', width=140, height=38, fg_color='#EF5350', hover_color='#E53935', text_color='white', corner_radius=8, font=ctk.CTkFont(size=14, weight='bold'), command=logout_and_redirect).pack(side='left', padx=12)
        ctk.CTkButton(btn_frame, text='Non, rester', width=120, height=38, fg_color='#90A4AE', hover_color='#78909C', text_color='white', corner_radius=8, font=ctk.CTkFont(size=14), command=dialog.destroy).pack(side='left', padx=12)

    def _build_main(self, add_padding=True):
        if add_padding:
            self.main = ctk.CTkScrollableFrame(self, fg_color='white')
            self.main.pack(side='right', fill='both', expand=True, padx=25, pady=25)
        else:
            self.main = ctk.CTkScrollableFrame(self, fg_color='white', corner_radius=0)
            self.main.pack(fill='both', expand=True)

        self._build_header()
        self._build_stats()

        # Conteneur pour le contenu principal (qui peut être remplacé par les résultats de recherche)
        self.main_content_container = ctk.CTkFrame(self.main, fg_color='transparent')
        self.main_content_container.pack(fill='both', expand=True)

        self._build_activity(self.main_content_container)
        self._build_charts(self.main_content_container)
        self._build_tables(self.main_content_container)

    def _build_header(self):
        hdr = ctk.CTkFrame(self.main, fg_color='white')
        hdr.pack(fill='x', pady=(0,25))
        ctk.CTkLabel(hdr, text=f"Bienvenue, {self.user['prenom']} {self.user['nom']} !", font=ctk.CTkFont(size=24, weight='bold'), text_color='#333333').pack(side='left', padx=15)
        self.time_lbl = ctk.CTkLabel(hdr, text='', font=ctk.CTkFont(size=14), text_color='#666666')
        self.time_lbl.pack(side='right', padx=15)

    def _build_stats(self):
        frame = ctk.CTkFrame(self.main, fg_color='white')
        frame.pack(fill='x', pady=(0,25))
        self.stats_labels = {}  # Ajouté pour stocker les labels dynamiques
        cards_data = [
            {
                'icon': '📦',
                'title': 'Produits',
                'key': 'produits',
                'subtitle': '+12% ce mois',
                'color': '#10B981',
                'bg_color': '#ECFDF5',
                'border_color': '#D1FAE5',
                'tooltip': "Nombre total de références de produits uniques dans l'entrepôt."
            },
            {
                'icon': '🏢',
                'title': 'Cellules',
                'key': 'cellules',
                'subtitle': '76% occupées',
                'color': '#F59E0B',
                'bg_color': '#FFFBEB',
                'border_color': '#FED7AA',
                'tooltip': 'Cellules de stockage utilisées par rapport au total disponible.'
            },
            {
                'icon': '📋',
                'title': 'Commandes',
                'key': 'commandes',
                'subtitle': 'En cours',
                'color': '#3B82F6',
                'bg_color': '#EFF6FF',
                'border_color': '#BFDBFE',
                'tooltip': 'Nombre de commandes clients en attente de préparation ou d\'expédition.'
            },
            {
                'icon': '🚨',
                'title': 'Alertes',
                'key': 'alertes',
                'subtitle': 'À traiter',
                'color': '#EF4444',
                'bg_color': '#FEF2F2',
                'border_color': '#FECACA',
                'tooltip': 'Produits nécessitant une attention immédiate (stock bas, etc.).'
            }
        ]
        for i, card in enumerate(cards_data):
            card_frame = ctk.CTkFrame(
                frame, 
                fg_color=card['bg_color'], 
                corner_radius=16, 
                width=300, 
                height=200,
                border_width=2,
                border_color=card['border_color']
            )
            card_frame.grid(row=0, column=i, padx=15, pady=10)
            card_frame.grid_propagate(False)
            CTkToolTip(card_frame, message=card['tooltip'], corner_radius=8, border_width=1)
            content_frame = ctk.CTkFrame(card_frame, fg_color='transparent')
            content_frame.pack(fill='both', expand=True, padx=20, pady=20)
            top_row = ctk.CTkFrame(content_frame, fg_color='transparent')
            top_row.pack(fill='x', pady=(0, 15))
            ctk.CTkLabel(
                top_row, 
                text=card['icon'], 
                font=ctk.CTkFont(size=32), 
                text_color=card['color']
            ).pack(side='left')
            ctk.CTkLabel(
                top_row, 
                text=card['title'], 
                font=ctk.CTkFont(size=18, weight='bold'), 
                text_color='#1F2937'
            ).pack(side='right', pady=10)
            # Label dynamique pour la valeur
            value_label = ctk.CTkLabel(
                content_frame, 
                text='...', 
                font=ctk.CTkFont(size=36, weight='bold'), 
                text_color=card['color']
            )
            value_label.pack(anchor='w', pady=(0, 8))
            self.stats_labels[card['key']] = value_label
            subtitle_frame = ctk.CTkFrame(content_frame, fg_color='transparent')
            subtitle_frame.pack(fill='x')
            ctk.CTkLabel(
                subtitle_frame, 
                text=card['subtitle'], 
                font=ctk.CTkFont(size=14), 
                text_color='#6B7280'
            ).pack(side='left')
            if i == 0:
                trend_frame = ctk.CTkFrame(subtitle_frame, fg_color='#10B981', corner_radius=8, width=60, height=20)
                trend_frame.pack(side='right')
                trend_frame.pack_propagate(False)
                ctk.CTkLabel(trend_frame, text='↗️ +12%', font=ctk.CTkFont(size=11, weight='bold'), text_color='white').pack(expand=True)
            elif i == 1:
                progress_frame = ctk.CTkFrame(subtitle_frame, fg_color='#E5E7EB', corner_radius=10, width=80, height=8)
                progress_frame.pack(side='right', pady=5)
                progress_bar = ctk.CTkFrame(progress_frame, fg_color='#F59E0B', corner_radius=10, width=60, height=8)
                progress_bar.pack(side='left', padx=2, pady=2)
            elif i == 2:
                status_frame = ctk.CTkFrame(subtitle_frame, fg_color='#3B82F6', corner_radius=8, width=70, height=20)
                status_frame.pack(side='right')
                status_frame.pack_propagate(False)
                ctk.CTkLabel(status_frame, text='⏳ En cours', font=ctk.CTkFont(size=11, weight='bold'), text_color='white').pack(expand=True)
            elif i == 3:
                priority_frame = ctk.CTkFrame(subtitle_frame, fg_color='#EF4444', corner_radius=8, width=70, height=20)
                priority_frame.pack(side='right')
                priority_frame.pack_propagate(False)
                ctk.CTkLabel(priority_frame, text='⚠️ Urgent', font=ctk.CTkFont(size=11, weight='bold'), text_color='white').pack(expand=True)

    def _build_activity(self, master):
        frame = ctk.CTkFrame(master, fg_color='white')
        frame.pack(fill='x', pady=(0,25))
        
        # Header avec titre et filtres
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(fill='x', padx=15, pady=(0,15))
        ctk.CTkLabel(header_frame, text='Activité Récente', font=ctk.CTkFont(size=18, weight='bold'), text_color='#333333').pack(side='left')

        # Filtres
        filters_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        filters_frame.pack(side='right')
        
        self.activity_filter_buttons = {}
        filters = ['Tous', 'Réception', 'Expédition', 'Modification']
        for f_type in filters:
            btn = ctk.CTkButton(
                filters_frame,
                text=f_type,
                height=28,
                font=ctk.CTkFont(size=12),
                command=lambda ft=f_type: self._set_activity_filter(ft),
                border_color="#D1D5DB",
                hover_color="#E5E7EB"
            )
            btn.pack(side='left', padx=4)
            self.activity_filter_buttons[f_type] = btn
        
        # Conteneur pour la liste des activités
        self.activity_list_container = ctk.CTkFrame(frame, fg_color="transparent")
        self.activity_list_container.pack(fill='x', expand=True, padx=15)
        
        # Appel initial pour afficher la liste
        self._update_activity_display()

    def _build_charts(self, master):
        frame = ctk.CTkFrame(master, fg_color='white')
        frame.pack(fill='x', expand=True, pady=(0,25))
        ctk.CTkLabel(frame, text='Statistiques Visuelles', font=ctk.CTkFont(size=18, weight='bold'), text_color='#333333').pack(side='top', anchor='w', padx=15, pady=(0,15))
        # Graphique 1 : activité 7 derniers jours
        ch1 = ctk.CTkFrame(frame, fg_color='#F5F5F5', corner_radius=12)
        ch1.pack(side='left', expand=True, fill='both', padx=12)
        self.fig1 = Figure(figsize=(9,4), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.plot([1,2,3,4,5,6,7],[50,60,55,70,65,75,80],marker='o')
        self.ax1.set_title('Activité 7 derniers jours')
        self.fig1.tight_layout()
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=ch1)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(expand=True, fill='both', padx=10, pady=10)
        ctk.CTkLabel(frame, text='Taux de Rotation des Stocks', font=ctk.CTkFont(size=14, weight='bold'), text_color='#666666').pack(pady=(0,10))
        # Graphique 2 : répartition par zone
        ch2 = ctk.CTkFrame(frame, fg_color='#F5F5F5', corner_radius=12)
        ch2.pack(side='left', expand=True, fill='both', padx=12)
        self.fig2 = Figure(figsize=(9,4), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.pie([30,40,30], labels=['Zone A','Zone B','Zone C'], autopct='%1.1f%%')
        self.ax2.axis('equal')
        self.ax2.set_title('Répartition par zone')
        self.fig2.tight_layout()
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=ch2)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(expand=True, fill='both', padx=10, pady=10)
        ctk.CTkLabel(frame, text='Utilisation des Cellules', font=ctk.CTkFont(size=14, weight='bold'), text_color='#666666').pack(pady=(0,10))
        # Pour compatibilité, garder une référence sur les données
        self.charts_data = {
            'activity': [50,60,55,70,65,75,80],
            'zones': [30,40,30],
            'zones_labels': ['Zone A','Zone B','Zone C']
        }

    def _update_charts_display(self):
        """Met à jour dynamiquement les graphiques en temps réel."""
        # Exemple : activité 7 derniers jours
        if hasattr(self, 'ax1') and hasattr(self, 'charts_data'):
            self.ax1.clear()
            y = self.charts_data.get('activity', [0]*7)
            self.ax1.plot(range(1,8), y, marker='o')
            self.ax1.set_title('Activité 7 derniers jours')
            self.fig1.tight_layout()
            self.canvas1.draw()
        # Exemple : répartition par zone
        if hasattr(self, 'ax2') and hasattr(self, 'charts_data'):
            self.ax2.clear()
            sizes = self.charts_data.get('zones', [1,1,1])
            labels = self.charts_data.get('zones_labels', ['Zone A','Zone B','Zone C'])
            self.ax2.pie(sizes, labels=labels, autopct='%1.1f%%')
            self.ax2.axis('equal')
            self.ax2.set_title('Répartition par zone')
            self.fig2.tight_layout()
            self.canvas2.draw()

    def _build_tables(self, master):
        frame = ctk.CTkFrame(master, fg_color='white')
        frame.pack(fill='x', pady=(0,25))
        ctk.CTkLabel(frame, text='Produits en Alerte et Commandes Récentes', font=ctk.CTkFont(size=18, weight='bold'), text_color='#333333').pack(side='top', anchor='w', padx=15, pady=(0,15))
        # --- Produits en Alerte ---
        subframe1 = ctk.CTkFrame(frame, fg_color='#FEF2F2', corner_radius=12, border_width=1, border_color='#FECACA')
        subframe1.pack(side='left', expand=True, fill='both', padx=12)
        header_frame = ctk.CTkFrame(subframe1, fg_color="transparent")
        header_frame.pack(fill='x', padx=15, pady=(5,0))
        ctk.CTkLabel(header_frame, text='Produits en Alerte de Stock', font=ctk.CTkFont(size=14, weight='bold'), text_color='#D32F2F').pack(side='left')
        sort_buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        sort_buttons_frame.pack(side='right')
        ctk.CTkLabel(sort_buttons_frame, text="Trier par:", font=ctk.CTkFont(size=12), text_color="#6B7280").pack(side='left', padx=(0,5))
        self.sort_name_button = ctk.CTkButton(sort_buttons_frame, text="Nom", height=24, font=ctk.CTkFont(size=12), command=lambda: self._set_alert_products_sort('name'), border_color="#D1D5DB", hover_color="#E5E7EB")
        self.sort_name_button.pack(side='left')
        CTkToolTip(self.sort_name_button, message="Trier les produits par ordre alphabétique.")
        self.sort_stock_button = ctk.CTkButton(sort_buttons_frame, text="Stock", height=24, font=ctk.CTkFont(size=12), command=lambda: self._set_alert_products_sort('stock'), border_color="#D1D5DB", hover_color="#E5E7EB")
        self.sort_stock_button.pack(side='left', padx=5)
        CTkToolTip(self.sort_stock_button, message="Trier les produits par stock disponible (du plus bas au plus élevé).")
        self.alert_products_container = ctk.CTkFrame(subframe1, fg_color="transparent")
        self.alert_products_container.pack(fill='both', expand=True, padx=15, pady=(5,10))
        self._update_alert_products_display()
        # --- Dernières Commandes ---
        subframe2 = ctk.CTkFrame(frame, fg_color='#EFF6FF', corner_radius=12, border_width=1, border_color='#BFDBFE')
        subframe2.pack(side='left', expand=True, fill='both', padx=12)
        ctk.CTkLabel(subframe2, text='Dernières Commandes', font=ctk.CTkFont(size=14, weight='bold'), text_color='#3B82F6').pack(pady=5)
        self.recent_orders_container = ctk.CTkFrame(subframe2, fg_color="transparent")
        self.recent_orders_container.pack(fill='both', expand=True)
        self._update_recent_orders_display()

    def _update_recent_orders_display(self):
        """Met à jour dynamiquement la liste des dernières commandes en temps réel."""
        for widget in self.recent_orders_container.winfo_children():
            widget.destroy()
        try:
            orders = database.get_all_expeditions()
        except Exception:
            orders = []
        # On prend les 3 plus récentes
        for o in orders[:3]:
            row = ctk.CTkFrame(self.recent_orders_container, fg_color='transparent')
            row.pack(fill='x', padx=15, pady=5)
            ctk.CTkLabel(row, text=f"📋 {o['number']} - {o['client']}", font=ctk.CTkFont(size=13)).pack(side='left')
            ctk.CTkLabel(row, text=o['status'], font=ctk.CTkFont(size=12), text_color='#666666').pack(side='right')

    def _update_time(self):
        try:
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_TIME, 'fr_FR')
            except:
                pass  # fallback si la locale n'est pas installée
        now = datetime.now()
        date_str = now.strftime("%A %d %B %Y - %H:%M:%S")
        # Mettre la première lettre en minuscule (pour les jours/mois)
        date_str = date_str[0].lower() + date_str[1:]
        self.time_lbl.configure(text=date_str)
        self.time_lbl.after(3000, self._update_time)

    def _clear_search(self):
        """Efface le contenu de la barre de recherche."""
        self.search_var.set('')

    def _update_clear_button(self, *args):
        """Affiche ou masque le bouton pour effacer la recherche."""
        if self.search_var.get():
            self.clear_search_button.place(relx=0.8, rely=0.5, anchor='center')
        else:
            self.clear_search_button.place_forget()

    def _perform_search(self):
        """
        Effectue une recherche sur tous les éléments du dashboard (produits, commandes, mouvements, alertes).
        """
        search_query = self.search_var.get().lower()
        # Effacer le contenu précédent
        for widget in self.main_content_container.winfo_children():
            widget.destroy()
        if not search_query:
            self._build_activity(self.main_content_container)
            self._build_charts(self.main_content_container)
            self._build_tables(self.main_content_container)
            return
        # Recherche dans les produits
        produits = database.get_all_products()
        produits_results = [p for p in produits if search_query in p['name'].lower() or search_query in p.get('description','').lower() or search_query in p.get('brand','').lower()]
        # Recherche dans les commandes
        try:
            commandes = database.get_all_expeditions()
        except Exception:
            commandes = []
        commandes_results = [c for c in commandes if search_query in c['number'].lower() or search_query in c['client'].lower() or (c.get('status') and search_query in c['status'].lower())]
        # Recherche dans les mouvements (activité)
        try:
            mouvements = database.get_recent_activity(20)
        except Exception:
            mouvements = []
        mouvements_results = [m for m in mouvements if search_query in m['action'].lower() or search_query in m['user'].lower() or search_query in m['type'].lower()]
        # Recherche dans les produits en alerte
        alertes_results = [p for p in self.alert_products if search_query in p['name'].lower() or search_query in p['stock'].lower() or search_query in p['loc'].lower()]
        # Affichage des résultats
        results_frame = ctk.CTkFrame(self.main_content_container, fg_color='transparent')
        results_frame.pack(fill='both', expand=True, padx=15, pady=10)
        total_results = len(produits_results) + len(commandes_results) + len(mouvements_results) + len(alertes_results)
        ctk.CTkLabel(results_frame, text=f"{total_results} résultat(s) pour \"{search_query}\"", font=ctk.CTkFont(size=18, weight='bold')).pack(anchor='w', pady=(0,15))
        if produits_results:
            ctk.CTkLabel(results_frame, text="Produits :", font=ctk.CTkFont(size=15, weight='bold')).pack(anchor='w', pady=(8,2))
            for p in produits_results:
                row = ctk.CTkFrame(results_frame, fg_color='#F8F9FA', corner_radius=8)
                row.pack(fill='x', pady=3)
                ctk.CTkLabel(row, text=f"📦 {p['name']} ({p['stock']})", font=ctk.CTkFont(size=14)).pack(side='left', padx=10, pady=6)
                ctk.CTkLabel(row, text=p.get('brand',''), font=ctk.CTkFont(size=12), text_color='#666').pack(side='left', padx=8)
        if commandes_results:
            ctk.CTkLabel(results_frame, text="Commandes :", font=ctk.CTkFont(size=15, weight='bold')).pack(anchor='w', pady=(12,2))
            for c in commandes_results:
                row = ctk.CTkFrame(results_frame, fg_color='#EFF6FF', corner_radius=8)
                row.pack(fill='x', pady=3)
                ctk.CTkLabel(row, text=f"📦 {c['number']} - {c['client']}", font=ctk.CTkFont(size=14)).pack(side='left', padx=10, pady=6)
                ctk.CTkLabel(row, text=c.get('status',''), font=ctk.CTkFont(size=12), text_color='#666').pack(side='left', padx=8)
        if mouvements_results:
            ctk.CTkLabel(results_frame, text="Activité récente :", font=ctk.CTkFont(size=15, weight='bold')).pack(anchor='w', pady=(12,2))
            for m in mouvements_results:
                row = ctk.CTkFrame(results_frame, fg_color='#F8F9FA', corner_radius=8)
                row.pack(fill='x', pady=3)
                ctk.CTkLabel(row, text=f"{m['icon']} {m['user']} {m['action']}", font=ctk.CTkFont(size=14)).pack(side='left', padx=10, pady=6)
                ctk.CTkLabel(row, text=m['time'], font=ctk.CTkFont(size=12), text_color='#999').pack(side='left', padx=8)
        if alertes_results:
            ctk.CTkLabel(results_frame, text="Produits en alerte :", font=ctk.CTkFont(size=15, weight='bold')).pack(anchor='w', pady=(12,2))
            for a in alertes_results:
                row = ctk.CTkFrame(results_frame, fg_color='#FEF2F2', corner_radius=8)
                row.pack(fill='x', pady=3)
                ctk.CTkLabel(row, text=f"🚨 {a['name']} ({a['stock']})", font=ctk.CTkFont(size=14), text_color='#D32F2F').pack(side='left', padx=10, pady=6)
                ctk.CTkLabel(row, text=a['loc'], font=ctk.CTkFont(size=12), text_color='#666').pack(side='left', padx=8)
        if total_results == 0:
            ctk.CTkLabel(results_frame, text="🤷‍♂️ Aucun résultat trouvé", font=ctk.CTkFont(size=24, weight='bold'), text_color='#333').pack(pady=(20,10))
            ctk.CTkLabel(results_frame, text=f"Nous n'avons rien trouvé pour \"{search_query}\".\nEssayez avec d'autres mots-clés ou vérifiez l'orthographe.", font=ctk.CTkFont(size=16), text_color='#666', justify='center').pack()

    def _on_search_focus_in(self, event):
        self.search_entry.configure(fg_color='#F8F9FA', border_width=1, border_color='#A5B4FC')

    def _on_search_focus_out(self, event):
        self.search_entry.configure(fg_color='transparent', border_width=0)
        
        # Mettre à jour l'état du bouton "effacer" à chaque changement
        self._update_clear_button()

    def on_window_resize(self, width, height):
        """Méthode appelée quand la fenêtre est redimensionnée"""
        if hasattr(self.parent, 'get_responsive_config'):
            self.responsive_config = self.parent.get_responsive_config()
        self._adapt_layout_to_size(width, height)

    def apply_theme(self, theme):
        """Applique le thème au dashboard"""
        try:
            is_dark = theme == "dark"
            
            # Couleurs adaptatives
            bg_color = "#1a1a1a" if is_dark else "#f7fafd"
            card_bg = "#2d2d2d" if is_dark else "white"
            text_color = "#ffffff" if is_dark else "#222222"
            secondary_text = "#cccccc" if is_dark else "#666666"
            border_color = "#555555" if is_dark else "#e0e0e0"
            
            # Appliquer au frame principal
            self.configure(fg_color=bg_color)
            
            # Appliquer au contenu principal
            if hasattr(self, 'main_content'):
                self.main_content.configure(fg_color=bg_color)
            
            # Adapter les cartes de statistiques
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    widget.configure(fg_color=card_bg, border_color=border_color)
                    
                    # Adapter les labels dans les cartes
                    for child in widget.winfo_children():
                        if isinstance(child, ctk.CTkLabel):
                            if "stat" in str(child).lower() or "value" in str(child).lower():
                                child.configure(text_color=text_color)
                            else:
                                child.configure(text_color=secondary_text)
            
            print(f"Thème appliqué au dashboard: {theme}")
            
        except Exception as e:
            print(f"Erreur lors de l'application du thème au dashboard: {e}")

    def _on_frame_resize(self, event):
        """Gère le redimensionnement du frame"""
        if event.width > 100 and event.height > 100:
            self._adapt_layout_to_size(event.width, event.height)
    
    def _adapt_layout_to_size(self, width, height):
        """Adapte la mise en page selon la taille"""
        # Adapter les colonnes des cartes selon la largeur
        if width < 1200:
            # Mode compact - 2 colonnes
            self._configure_cards_layout(2)
        elif width < 1600:
            # Mode normal - 3 colonnes
            self._configure_cards_layout(3)
        else:
            # Mode large - 4 colonnes
            self._configure_cards_layout(4)
    
    def _configure_cards_layout(self, columns):
        """Configure la disposition des cartes selon le nombre de colonnes"""
        # Cette méthode peut être implémentée pour réorganiser les cartes
        pass

    def _show_analytics(self):
        # Affiche un pop-up avec le RapportAnalyticsFrame
        popup = ctk.CTkToplevel(self)
        popup.title("Rapports et Analytics")
        popup.geometry("1200x800")
        popup.grab_set()
        popup.focus_force()
        popup.resizable(True, True)
        from rapport_analytics import RapportAnalyticsFrame
        RapportAnalyticsFrame(popup, user_info=self.user)

    def _show_notifications_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Notifications en temps réel")
        popup.geometry("420x600")
        popup.grab_set()
        popup.focus_force()
        popup.resizable(False, False)
        ctk.CTkLabel(popup, text="🔔 Notifications", font=ctk.CTkFont(size=20, weight="bold"), text_color="#333").pack(pady=(18, 8))
        notif_frame = ctk.CTkScrollableFrame(popup, fg_color="#f9fafb")
        notif_frame.pack(fill="both", expand=True, padx=18, pady=8)
        # Générer les notifications à partir des produits en alerte, commandes, mouvements
        notifications = []
        # Produits en alerte
        for p in self.alert_products:
            notifications.append({
                'icon': '🚨',
                'text': f"Stock critique pour {p['name']} ({p['stock']}) à {p['loc']}",
                'color': '#ef4444'
            })
        # Dernières commandes
        try:
            from database import get_all_expeditions
            commandes = get_all_expeditions()
            for c in commandes[:3]:
                notifications.append({
                    'icon': '📦',
                    'text': f"Commande {c['number']} - {c['client']} : {c['status']}",
                    'color': '#3B82F6'
                })
        except Exception:
            pass
        # Derniers mouvements
        for a in self.activity_data[:5]:
            notifications.append({
                'icon': a['icon'],
                'text': f"{a['user']} {a['action']}",
                'color': a['color']
            })
        if not notifications:
            ctk.CTkLabel(notif_frame, text="Aucune notification récente.", font=ctk.CTkFont(size=15), text_color="#666").pack(pady=30)
        else:
            for n in notifications:
                row = ctk.CTkFrame(notif_frame, fg_color="white", corner_radius=8)
                row.pack(fill='x', pady=6, padx=2)
                ctk.CTkLabel(row, text=n['icon'], font=ctk.CTkFont(size=18), text_color=n['color']).pack(side='left', padx=8)
                ctk.CTkLabel(row, text=n['text'], font=ctk.CTkFont(size=13), text_color="#222").pack(side='left', padx=4)

    def refresh_data(self):
        """Rafraîchit toutes les données du dashboard en temps réel depuis la base de données."""
        self.alert_products = self._get_alert_products_from_db()
        self.activity_data = self._get_activity_from_db()
        self.stats_data = self._get_stats_from_db()
        self.charts_data = self._get_charts_data_from_db()
        self._update_alert_products_display()
        self._update_activity_display()
        self._update_stats_display()
        self._update_charts_display()
        self._update_recent_orders_display()
        # Mettre à jour le nombre de notifications
        notif_count = len(self.alert_products)
        try:
            from database import get_all_expeditions
            notif_count += len(get_all_expeditions()[:3])
        except Exception:
            pass
        notif_count += min(5, len(self.activity_data))
        self.notif_count.set(f"🔔 {notif_count}")
        self.after(self.refresh_interval, self.refresh_data)

    def _get_alert_products_from_db(self):
        """Récupère les produits en alerte (stock bas) depuis la base de données."""
        produits = database.get_all_products()
        return [
            {'name': p['name'], 'stock': f"{p['stock']} / {p['alert']}", 'loc': p['loc']}
            for p in produits if p['stock'] <= p['alert']
        ]

    def _get_activity_from_db(self):
        """Récupère l'activité récente réelle depuis la base de données (mouvements)."""
        try:
            return database.get_recent_activity(10)
        except Exception:
            return []

    def _get_stats_from_db(self):
        """Récupère les statistiques globales pour les cartes du dashboard."""
        produits = database.get_all_products()
        nb_produits = len(produits)
        nb_alertes = len([p for p in produits if p['stock'] <= p['alert']])
        # Cellules temps réel
        try:
            nb_cellules_occupees, nb_cellules_total = database.get_cellules_stats()
        except Exception:
            nb_cellules_occupees, nb_cellules_total = 0, 0
        # Commandes temps réel
        try:
            nb_commandes = database.get_commandes_en_cours()
        except Exception:
            nb_commandes = 0
        return {
            'produits': nb_produits,
            'cellules': f"{nb_cellules_occupees}/{nb_cellules_total}",
            'commandes': nb_commandes,
            'alertes': nb_alertes
        }

    def _get_charts_data_from_db(self):
        """Récupère les données pour les graphiques depuis la base de données (vraies stats)."""
        # Activité 7 derniers jours : nombre de mouvements par jour
        try:
            activity = database.get_mouvements_7_jours()
        except Exception:
            activity = [0]*7
        # Répartition par zone : nombre de produits par zone
        try:
            zones_dict = database.get_repartition_zones()
            zones_labels = list(zones_dict.keys())
            zones = list(zones_dict.values())
        except Exception:
            zones_labels = ['Zone A','Zone B','Zone C']
            zones = [1,1,1]
        return {
            'activity': activity,
            'zones': zones,
            'zones_labels': zones_labels
        }

    def _update_stats_display(self):
        """Met à jour dynamiquement les valeurs des stats en temps réel."""
        if not hasattr(self, 'stats_labels') or not hasattr(self, 'stats_data'):
            return
        for key, label in self.stats_labels.items():
            if key in self.stats_data:
                label.configure(text=str(self.stats_data[key]))

# Classe pour compatibilité avec l'ancien code
class DashboardApp(ctk.CTk):
    def __init__(self, user_info=None):
        super().__init__()
        self.title('SGE – Tableau de bord')
        self.state('zoomed')
        self.configure(fg_color='white')
        
        if user_info is None:
            user_info = {
                'nom': 'Dupont',
                'prenom': 'Jean',
                'email': 'jean.dupont@sac.com',
                'role': 'Admin',
                'contact': '+33 6 12 34 56 78',
                'matricule': 'A12345'
            }
        
        self.dashboard_frame = DashboardFrame(self, user_info)
        self.dashboard_frame.pack(fill='both', expand=True)
        
        # Gestion de la fermeture de fenêtre avec pop-up de confirmation
        self.protocol("WM_DELETE_WINDOW", self._confirm_exit)

    def _confirm_exit(self):
        """Affiche un pop-up de confirmation avant de quitter l'application"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmation de fermeture")
        dialog.geometry("400x200")
        dialog.configure(fg_color='white')
        dialog.grab_set()  # Rend la fenêtre modale
        dialog.resizable(False, False)
        
        # Centrer la fenêtre
        dialog.transient(self)
        dialog.grab_set()
        
        # Contenu du pop-up
        ctk.CTkLabel(
            dialog, 
            text="🚪 Quitter l'application ?", 
            font=ctk.CTkFont(size=18, weight='bold'), 
            text_color='#333333'
        ).pack(pady=(30, 10), padx=20)
        
        ctk.CTkLabel(
            dialog, 
            text="Êtes-vous sûr de vouloir fermer l'application ?\nToutes les données non sauvegardées seront perdues.", 
            font=ctk.CTkFont(size=14), 
            text_color='#666666'
        ).pack(pady=(0, 20), padx=20)
        
        # Boutons d'action
        btn_frame = ctk.CTkFrame(dialog, fg_color='transparent')
        btn_frame.pack(pady=(0, 20))
        
        def confirm_quit():
            dialog.destroy()
            self.quit()
            self.destroy()
        
        def cancel_quit():
            dialog.destroy()
        
        ctk.CTkButton(
            btn_frame, 
            text='✅ Oui, quitter', 
            width=120, 
            height=38, 
            fg_color='#EF4444', 
            hover_color='#DC2626', 
            text_color='white', 
            corner_radius=8, 
            font=ctk.CTkFont(size=14, weight='bold'), 
            command=confirm_quit
        ).pack(side='left', padx=10)
        
        ctk.CTkButton(
            btn_frame, 
            text='❌ Non, rester', 
            width=120, 
            height=38, 
            fg_color='#6B7280', 
            hover_color='#4B5563', 
            text_color='white', 
            corner_radius=8, 
            font=ctk.CTkFont(size=14), 
            command=cancel_quit
        ).pack(side='left', padx=10)

if __name__ == '__main__':
    app = DashboardApp()
    app.mainloop()
