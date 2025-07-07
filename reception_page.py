import customtkinter as ctk
from stock_management_page import SidebarFrame
from responsive_utils import ThemeToggleButton
from tkinter import messagebox
import database
from tkcalendar import DateEntry
import datetime

class ReceptionFrame(ctk.CTkFrame):
    def __init__(self, master, user_info=None):
        try:
            super().__init__(master, fg_color="white")
            self.pack(fill="both", expand=True)
            self.master = master
            self.user_info = user_info if user_info is not None else {
                'prenom': 'Utilisateur',
                'nom': 'Test',
                'role': 'Admin',
                'email': 'test@example.com',
                'matricule': '12345'
            }
            self.previous_page = getattr(master, 'last_page', None) if hasattr(master, 'last_page') else None
            self.sidebar = SidebarFrame(self, master)
            self.sidebar.pack(side="left", fill="y")
            self.sidebar.set_active_button("Réception")
            self.bind("<Configure>", self._on_frame_resize)
            self.main_content = ctk.CTkFrame(self, fg_color="white")
            self.main_content.pack(side="right", fill="both", expand=True)
            self.active_filter = "Tous"
            self.current_page = 0
            self.items_per_page = 10
            self._build_topbar()
            self.create_widgets()
            self.bind("<Configure>", self._on_frame_resize)
            self._auto_refresh_interval = 5000  # 5 secondes
            self._auto_refresh()
        except Exception as e:
            self._show_error(str(e))

    def apply_theme(self, theme):
        """Applique le thème à la page de réception"""
        try:
            is_dark = theme == "dark"
            
            # Couleurs adaptatives
            bg_color = "#1a1a1a" if is_dark else "#f7fafd"
            card_bg = "#2d2d2d" if is_dark else "white"
            text_color = "#ffffff" if is_dark else "#222222"
            secondary_text = "#cccccc" if is_dark else "#666666"
            border_color = "#555555" if is_dark else "#e0e0e0"
            table_bg = "#3d3d3d" if is_dark else "#f9fafb"
            
            # Appliquer au frame principal
            self.configure(fg_color=bg_color)
            
            # Appliquer au contenu principal
            if hasattr(self, 'main_content'):
                self.main_content.configure(fg_color=bg_color)
            
            # Adapter tous les widgets enfants
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    widget.configure(fg_color=card_bg, border_color=border_color)
                    
                    # Adapter les labels dans les frames
                    for child in widget.winfo_children():
                        if isinstance(child, ctk.CTkLabel):
                            child.configure(text_color=text_color)
                        elif isinstance(child, ctk.CTkEntry):
                            child.configure(fg_color=table_bg, text_color=text_color, border_color=border_color)
                        elif isinstance(child, ctk.CTkButton):
                            # Garder les couleurs des boutons d'action
                            pass
                        elif isinstance(child, ctk.CTkFrame):
                            child.configure(fg_color=table_bg, border_color=border_color)
            
            print(f"Thème appliqué à la page Réception: {theme}")
            
        except Exception as e:
            print(f"Erreur lors de l'application du thème à la page Réception: {e}")

    def create_widgets(self):
        # Ajout du bouton retour intelligent en haut à gauche
        topbar = ctk.CTkFrame(self.main_content, fg_color="transparent")
        topbar.pack(fill="x", pady=(10, 0))
        btn_retour = ctk.CTkButton(
            topbar,
            text="← Retour",
            width=110,
            height=36,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            text_color="white",
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=8,
            command=self._go_back
        )
        btn_retour.pack(side="left", padx=18, pady=5)
        
        # HEADER (fixe)
        header = ctk.CTkFrame(self.main_content, fg_color="white")
        header.pack(fill="x", pady=(0, 10), padx=0)
        left = ctk.CTkFrame(header, fg_color="white")
        left.pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(left, text="Gestion des Réceptions", font=ctk.CTkFont(size=24, weight="bold"), text_color="#212224").pack(anchor="w")
        ctk.CTkLabel(left, text="Gérez les bons de réception et les arrivées de marchandises", font=ctk.CTkFont(size=14), text_color="#6B7280").pack(anchor="w")
        right = ctk.CTkFrame(header, fg_color="white")
        right.pack(side="right", padx=20, pady=10)
        ctk.CTkButton(right, text="+ Nouveau Bon", fg_color="#3B82F6", hover_color="#2563EB", text_color="white", font=ctk.CTkFont(size=13, weight="bold"), corner_radius=8, height=36, command=lambda: AddReceptionPopup(self)).pack(side="left", padx=5)
        ctk.CTkButton(right, text="Scanner", fg_color="#F59E0B", hover_color="#D97706", text_color="white", font=ctk.CTkFont(size=13, weight="bold"), corner_radius=8, height=36, command=lambda: ScannerPopup(self)).pack(side="left", padx=5)
        ctk.CTkButton(right, text="Exporter", fg_color="#10B981", hover_color="#059669", text_color="white", font=ctk.CTkFont(size=13, weight="bold"), corner_radius=8, height=36, command=lambda: ExportReceptionPopup(self)).pack(side="left", padx=5)

        # SCROLLABLE CONTENT
        scrollable = ctk.CTkScrollableFrame(self.main_content, fg_color="white")
        scrollable.pack(fill="both", expand=True)

        # SUMMARY CARDS
        cards_frame = ctk.CTkFrame(scrollable, fg_color="white")
        cards_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.summary_labels = {}
        card_data = [
            {"title": "En Attente", "key": "en_attente", "subtitle": "À réceptionner", "icon": "⏰", "color": "#F59E42", "subcolor": "#F59E42"},
            {"title": "Reçues Aujourd'hui", "key": "recues_aujourdhui", "subtitle": "Complétées", "icon": "✅", "color": "#10B981", "subcolor": "#10B981"},
            {"title": "Colis Totaux", "key": "colis_total", "subtitle": "Ce mois", "icon": "📦", "color": "#3B82F6", "subcolor": "#3B82F6"},
            {"title": "Anomalies", "key": "anomalies", "subtitle": "À traiter", "icon": "❗", "color": "#EF4444", "subcolor": "#EF4444"}
        ]
        for card in card_data:
            f = ctk.CTkFrame(cards_frame, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
            f.pack(side="left", expand=True, fill="x", padx=10)
            ctk.CTkLabel(f, text=card["title"], font=ctk.CTkFont(size=15, weight="bold"), text_color="#374151").pack(anchor="w", padx=15, pady=(12,0))
            row = ctk.CTkFrame(f, fg_color="white")
            row.pack(fill="x", padx=15, pady=(0,10))
            value_label = ctk.CTkLabel(row, text="-", font=ctk.CTkFont(size=32, weight="bold"), text_color="#111827")
            value_label.pack(side="left")
            self.summary_labels[card["key"]] = value_label
            iconf = ctk.CTkFrame(row, fg_color=card["color"], width=40, height=40, corner_radius=8)
            iconf.pack(side="left", padx=(10,0))
            iconf.pack_propagate(False)
            ctk.CTkLabel(iconf, text=card["icon"], font=ctk.CTkFont(size=22), text_color="white").pack(expand=True)
            ctk.CTkLabel(f, text=card["subtitle"], font=ctk.CTkFont(size=13), text_color=card["subcolor"]).pack(anchor="w", padx=15, pady=(0,8))

        # MIDDLE SECTION (Actions, Alertes, Prochaines arrivées)
        middle = ctk.CTkFrame(scrollable, fg_color="white")
        middle.pack(fill="x", padx=20, pady=(0, 10))
        # 1. Actions rapides
        actions = ctk.CTkFrame(middle, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        actions.pack(side="left", fill="both", expand=True, padx=(0, 12), pady=8)
        ctk.CTkLabel(actions, text="Actions Rapides", font=ctk.CTkFont(size=16, weight="bold"), text_color="#222").pack(anchor="w", padx=15, pady=(12,8))
        quicks = [
            ("🚚 Réceptionner", "Scanner et valider l'arrivée", "#3B82F6", "#2563EB", self.open_scanner_popup),
            ("🔍 Rechercher", "Par numéro ou fournisseur", "#F59E0B", "#D97706", self.open_search_popup),
            ("🛡️ Vérifier", "Traiter les écarts détectés", "#10B981", "#059669", self.open_anomalies_popup)
        ]
        for icon, desc, color, hover_color, command in quicks:
            btn = ctk.CTkButton(
                actions, 
                text=icon.split()[1], 
                fg_color=color, 
                hover_color=hover_color, 
                text_color="white", 
                font=ctk.CTkFont(size=14, weight="bold"), 
                corner_radius=8, 
                height=38,
                command=command
            )
            btn.pack(fill="x", padx=15, pady=(0,6))
            ctk.CTkLabel(actions, text=desc, font=ctk.CTkFont(size=12), text_color="#6B7280").pack(anchor="w", padx=25, pady=(0,8))
        # 2. Alertes urgentes
        alertes = ctk.CTkFrame(middle, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        alertes.pack(side="left", fill="both", expand=True, padx=(0, 12), pady=8)
        ctk.CTkLabel(alertes, text="Alertes Urgentes", font=ctk.CTkFont(size=16, weight="bold"), text_color="#222").pack(anchor="w", padx=15, pady=(12,8))
        urg = [
            ("❗ BR-2024-045", "Retard de 2 jours", "#FEE2E2", "#EF4444"),
            ("📦 Colis endommagé", "BR-2024-042", "#FEF3C7", "#F59E42"),
            ("⚖️ Poids incorrect", "BR-2024-041", "#FEF3C7", "#F59E42")
        ]
        for title, sub, bg, color in urg:
            card = ctk.CTkFrame(alertes, fg_color=bg, corner_radius=8, border_width=1, border_color=color)
            card.pack(fill="x", padx=15, pady=(0,8))
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14, weight="bold"), text_color=color).pack(anchor="w", padx=10, pady=(6,0))
            ctk.CTkLabel(card, text=sub, font=ctk.CTkFont(size=12), text_color=color).pack(anchor="w", padx=10, pady=(0,6))
        # 3. Prochaines arrivées
        nexts = ctk.CTkFrame(middle, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        nexts.pack(side="left", fill="both", expand=True, padx=(0, 0), pady=8)
        ctk.CTkLabel(nexts, text="Prochaines Arrivées", font=ctk.CTkFont(size=16, weight="bold"), text_color="#222").pack(anchor="w", padx=15, pady=(12,8))
        arr = [
            ("Dell Technologies", "Prévu: 15:30 - BR-2024-046", "En route", "#22c55e"),
            ("HP Enterprise", "Prévu: 17:00 - BR-2024-047", "Confirmé", "#3B82F6"),
            ("Lenovo Group", "Prévu: Demain 09:00", "Planifié", "#6B7280")
        ]
        for name, sub, status, color in arr:
            card = ctk.CTkFrame(nexts, fg_color="#F3F4F6", corner_radius=8)
            card.pack(fill="x", padx=15, pady=(0,8))
            ctk.CTkLabel(card, text=name, font=ctk.CTkFont(size=14, weight="bold"), text_color="#222").pack(anchor="w", padx=10, pady=(6,0))
            ctk.CTkLabel(card, text=sub, font=ctk.CTkFont(size=12), text_color="#6B7280").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=status, font=ctk.CTkFont(size=12), text_color=color).pack(anchor="w", padx=10, pady=(0,6))

        # BARRE DE FILTRE/RECHERCHE
        filterbar = ctk.CTkFrame(scrollable, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        filterbar.pack(fill="x", padx=20, pady=(0, 10))
        
        # Barre de recherche avec loupe
        search_frame = ctk.CTkFrame(filterbar, fg_color="transparent")
        search_frame.pack(side="left", padx=10, pady=10)
        
        # Conteneur pour la barre de recherche et la loupe
        search_container = ctk.CTkFrame(search_frame, fg_color="#F3F4F6", corner_radius=8, border_width=1, border_color="#D1D5DB")
        search_container.pack(fill="x")
        
        # Barre de recherche
        self.search_entry = ctk.CTkEntry(search_container, placeholder_text="Rechercher un bon de réception...", 
                                       fg_color="#F3F4F6", text_color="#222", border_color="#F3F4F6", 
                                       border_width=0, height=36, font=ctk.CTkFont(size=13))
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(12, 0))
        
        # Bouton loupe
        search_btn = ctk.CTkButton(search_container, text="🔍", width=36, height=36, 
                                 fg_color="transparent", hover_color="#E5E7EB", 
                                 text_color="#6B7280", font=ctk.CTkFont(size=16),
                                 corner_radius=0, command=self.perform_search)
        search_btn.pack(side="right")
        
        # Lier la touche Entrée à la recherche
        self.search_entry.bind("<Return>", lambda event: self.perform_search())
        self.filter_btns = []
        for text in ["Tous", "En Attente", "Reçues", "Partielles"]:
            btn = ctk.CTkButton(
                filterbar,
                text=text,
                fg_color="#ede9fe" if text==self.active_filter else "transparent",
                text_color="#6D28D9" if text==self.active_filter else "#374151",
                border_color="#D1D5DB",
                border_width=1,
                hover_color="#F3F4F6",
                height=30,
                corner_radius=8,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda t=text: self.set_table_filter(t)
            )
            btn.pack(side="left", padx=5)
            self.filter_btns.append(btn)
        ctk.CTkOptionMenu(filterbar, values=["Toutes dates", "Aujourd'hui", "Cette semaine", "Ce mois"], fg_color="#F3F4F6", text_color="#374151", button_color="#E5E7EB", button_hover_color="#D1D5DB", dropdown_fg_color="#F3F4F6", dropdown_text_color="#374151", corner_radius=8, height=30).pack(side="left", padx=5)
        ctk.CTkOptionMenu(filterbar, values=["Tous fournisseurs", "Dell", "HP", "Lenovo", "Samsung", "Logitech"], fg_color="#F3F4F6", text_color="#374151", button_color="#E5E7EB", button_hover_color="#D1D5DB", dropdown_fg_color="#F3F4F6", dropdown_text_color="#374151", corner_radius=8, height=30).pack(side="left", padx=5)
        ctk.CTkLabel(filterbar, text="Affichage:", font=ctk.CTkFont(size=12), text_color="#6B7280").pack(side="right", padx=(0,2))
        ctk.CTkOptionMenu(filterbar, values=["25", "50", "100"], fg_color="#F3F4F6", text_color="#374151", button_color="#E5E7EB", button_hover_color="#D1D5DB", dropdown_fg_color="#F3F4F6", dropdown_text_color="#374151", corner_radius=8, height=30, width=60).pack(side="right", padx=10)

        self.table_parent = table_parent = ctk.CTkFrame(scrollable, fg_color="white")
        table_parent.pack(fill="both", expand=True)
        self.render_table(table_parent)

    def open_scanner_popup(self):
        """Ouvre le popup de scanner pour réceptionner un colis"""
        ScannerPopup(self)

    def open_search_popup(self):
        """Ouvre le popup de recherche de bons de réception"""
        SearchReceptionPopup(self)

    def open_anomalies_popup(self):
        """Ouvre le popup de gestion des anomalies"""
        AnomaliesPopup(self)

    def perform_search(self):
        """Effectue la recherche dans les bons de réception"""
        search_term = self.search_entry.get().strip().lower()
        if search_term:
            self.show_search_results_popup(search_term)
        else:
            # Si la recherche est vide, rafraîchir le tableau
            for widget in self.table_parent.winfo_children():
                widget.destroy()
            self.render_table(self.table_parent)

    def show_search_results_popup(self, search_term):
        """Affiche les résultats de recherche dans un popup"""
        popup = ctk.CTkToplevel(self)
        popup.title("Résultats de Recherche")
        popup.geometry("600x400")
        popup.resizable(True, True)
        popup.configure(fg_color="white")
        popup.grab_set()
        
        # Header
        header = ctk.CTkFrame(popup, fg_color="white")
        header.pack(fill="x", pady=(16,0), padx=18)
        ctk.CTkLabel(header, text=f"Résultats pour '{search_term}'", font=ctk.CTkFont(size=18, weight="bold"), text_color="#222").pack(side="left", pady=6)
        
        # Contenu
        content = ctk.CTkFrame(popup, fg_color="white")
        content.pack(fill="both", expand=True, padx=18, pady=18)
        
        # Rechercher dans les données
        all_receptions = [
            ["BR-2024-045", "Dell Technologies", "15/03/2024 14:00", "-", "0/5", "25.5kg (prévu)", ("En Attente", "#F59E42")],
            ["BR-2024-044", "HP Enterprise", "14/03/2024 10:30", "14/03/2024 10:45", "3/3", "15.1kg", ("Reçue", "#10B981")],
            ["BR-2024-043", "Lenovo Group", "13/03/2024 16:00", "13/03/2024 16:15", "6/8", "34.2kg", ("Partielle", "#3B82F6")],
            ["BR-2024-042", "Samsung Electronics", "12/03/2024 09:00", "12/03/2024 09:30", "2/2", "8.3kg", ("Reçue", "#10B981")],
            ["BR-2024-041", "Logitech International", "11/03/2024 11:30", "-", "0/12", "18.6kg (prévu)", ("Annulée", "#EF4444")],
        ]
        
        # Filtrer les résultats
        results = []
        for reception in all_receptions:
            if (search_term in reception[0].lower() or  # Numéro de bon
                search_term in reception[1].lower() or  # Fournisseur
                search_term in reception[2].lower() or  # Date prévue
                search_term in reception[4].lower()):   # Colis
                results.append(reception)
        
        if results:
            # Afficher les résultats
            ctk.CTkLabel(content, text=f"{len(results)} résultat(s) trouvé(s)", font=ctk.CTkFont(size=14), text_color="#6B7280").pack(anchor="w", pady=(0, 15))
            
            # Tableau des résultats
            results_frame = ctk.CTkScrollableFrame(content, fg_color="white", height=250)
            results_frame.pack(fill="both", expand=True)
            
            # En-têtes du tableau
            headers = ["N° BON", "FOURNISSEUR", "DATE PRÉVUE", "DATE RÉCEPTION", "COLIS", "POIDS", "STATUT"]
            col_widths = [100, 160, 120, 120, 60, 80, 80]  # Largeurs fixes pour le popup
            
            # Frame pour les en-têtes
            header_frame = ctk.CTkFrame(results_frame, fg_color="#F9FAFB", height=40, corner_radius=6)
            header_frame.pack(fill="x", pady=(0, 2))
            header_frame.grid_propagate(False)
            
            # Création des en-têtes avec largeurs fixes
            for i, (header, width) in enumerate(zip(headers, col_widths)):
                header_cell = ctk.CTkFrame(header_frame, fg_color="transparent", width=width)
                header_cell.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
                header_cell.grid_propagate(False)
                ctk.CTkLabel(header_cell, text=header, font=ctk.CTkFont(size=11, weight="bold"), 
                            text_color="#6B7280").pack(expand=True, fill="both", padx=6, pady=8)
            
            # Corps du tableau
            body_frame = ctk.CTkFrame(results_frame, fg_color="white")
            body_frame.pack(fill="x")
            
            # Données du tableau
            for row_idx, row in enumerate(results):
                # Frame pour chaque ligne
                row_frame = ctk.CTkFrame(body_frame, fg_color="white" if row_idx % 2 == 0 else "#F9FAFB", height=40)
                row_frame.pack(fill="x", pady=1)
                row_frame.grid_propagate(False)
                
                # Création des cellules pour chaque colonne avec largeurs fixes
                for col_idx, (val, width) in enumerate(zip(row, col_widths)):
                    if col_idx == 6:  # Colonne STATUT (badge)
                        cell_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=width)
                        cell_frame.pack(side="left", fill="y", padx=1, pady=1)
                        cell_frame.pack_propagate(False)
                        
                        # Badge avec couleur
                        badge = ctk.CTkLabel(cell_frame, text=val[0], 
                                           font=ctk.CTkFont(size=10, weight="bold"), 
                                           text_color="white", fg_color=val[1], 
                                           corner_radius=4, padx=6, pady=2)
                        badge.pack(expand=True, fill="both", padx=3, pady=3)
                    else:
                        cell_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=width)
                        cell_frame.pack(side="left", fill="y", padx=1, pady=1)
                        cell_frame.pack_propagate(False)
                        
                        # Texte de la cellule
                        label = ctk.CTkLabel(cell_frame, text=val, 
                                           font=ctk.CTkFont(size=11), 
                                           text_color="#374151")
                        label.pack(expand=True, fill="both", padx=6, pady=6)
        else:
            # Aucun résultat
            ctk.CTkLabel(content, text="🔍", font=ctk.CTkFont(size=40), text_color="#6B7280").pack(pady=(40, 0))
            ctk.CTkLabel(content, text="Aucun résultat trouvé", font=ctk.CTkFont(size=16, weight="bold"), text_color="#374151").pack(pady=(10, 5))
            ctk.CTkLabel(content, text=f"Aucun bon de réception ne correspond à '{search_term}'", font=ctk.CTkFont(size=14), text_color="#6B7280").pack()
        
        # Boutons
        btn_frame = ctk.CTkFrame(content, fg_color="white")
        btn_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(btn_frame, text="Fermer", fg_color="#6B7280", hover_color="#4B5563", 
                     text_color="white", corner_radius=8, height=36, 
                     font=ctk.CTkFont(size=14, weight="bold"), 
                     command=popup.destroy).pack(side="right")

    def set_table_filter(self, filter_name):
        self.active_filter = filter_name
        # Réinitialiser la pagination lors du changement de filtre
        self.current_page = 0
        
        for btn in self.filter_btns:
            is_active = (btn.cget("text") == filter_name)
            btn.configure(
                fg_color="#ede9fe" if is_active else "transparent",
                text_color="#6D28D9" if is_active else "#374151"
            )
        for widget in self.table_parent.winfo_children():
            widget.destroy()
        self.render_table(self.table_parent)

    def get_filtered_receptions(self):
        """Récupère les données de la base et applique le filtre et la pagination."""
        all_rows = database.get_all_receptions()
        # Filtrage
        if self.active_filter == "Tous":
            filtered_rows = all_rows
        elif self.active_filter == "En Attente":
            filtered_rows = [r for r in all_rows if r['statut'] == "en_attente"]
        elif self.active_filter == "Reçues":
            filtered_rows = [r for r in all_rows if r['statut'] == "recu"]
        elif self.active_filter == "Partielles":
            filtered_rows = [r for r in all_rows if r['statut'] == "partielle"]
        else:
            filtered_rows = all_rows
        # Pagination
        items_per_page = getattr(self, 'items_per_page', 10)
        current_page = getattr(self, 'current_page', 0)
        start_idx = current_page * items_per_page
        end_idx = start_idx + items_per_page
        return filtered_rows[start_idx:end_idx], len(filtered_rows)

    def render_table(self, parent):
        table_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        ctk.CTkLabel(table_frame, text="Bons de Réception", font=ctk.CTkFont(size=18, weight="bold"), text_color="#111827").pack(anchor="w", padx=20, pady=(15,0))
        # Conteneur principal du tableau
        table_container = ctk.CTkFrame(table_frame, fg_color="white")
        table_container.pack(fill="both", expand=True, padx=20, pady=(0,10))
        # En-têtes du tableau améliorés
        headers = [
            "Référence",
            "Fournisseur",
            "Date prévue",
            "Date réception effective",
            "Observation",
            "Statut",
            "Magasinier",
            "Actions"  # Nouvelle colonne pour les boutons
        ]
        col_widths = [120, 140, 120, 140, 180, 100, 120, 80]
        header_frame = ctk.CTkFrame(table_container, fg_color="#F1F5F9", height=38, corner_radius=8, border_width=0, border_color="#E5E7EB")
        header_frame.pack(fill="x", pady=(0, 2))
        header_frame.grid_propagate(False)
        for i, (header, width) in enumerate(zip(headers, col_widths)):
            header_cell = ctk.CTkFrame(header_frame, fg_color="transparent", width=width)
            header_cell.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            header_cell.grid_propagate(False)
            ctk.CTkLabel(
                header_cell,
                text=header,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#1e293b"
            ).pack(expand=True, fill="both", padx=8, pady=8)
        
        # Corps du tableau avec scroll
        table_scroll = ctk.CTkScrollableFrame(table_container, fg_color="white", height=300)
        table_scroll.pack(fill="both", expand=True)
        
        # Frame pour le corps du tableau
        body_frame = ctk.CTkFrame(table_scroll, fg_color="white")
        body_frame.pack(fill="x")
        
        # Données du tableau avec pagination
        rows, total_count = self.get_filtered_receptions()
        for row_idx, row in enumerate(rows):
            # Frame pour chaque ligne (taille très réduite)
            row_frame = ctk.CTkFrame(body_frame, fg_color="white" if row_idx % 2 == 0 else "#F9FAFB", height=20)
            row_frame.pack(fill="x", pady=0.5)
            row_frame.grid_propagate(False)
            # Colonnes: référence, fournisseur, date prévue, date réception effective, observation, statut, magasinier
            values = [
                row['reference'],
                row['fournisseur'],
                str(row['date_prevue'])[:16] if row['date_prevue'] else '-',
                str(row['date_reception_effective'])[:16] if row['date_reception_effective'] else '-',
                row['observation'] or '-',
                row['statut'],
                row['magasinier']
            ]
            for col_idx, (val, width) in enumerate(zip(values, col_widths)):
                cell_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=width)
                cell_frame.pack(side="left", fill="y", padx=0.5, pady=0.5)
                cell_frame.pack_propagate(False)
                label = ctk.CTkLabel(cell_frame, text=val, font=ctk.CTkFont(size=12), text_color="#374151")
                label.pack(expand=True, fill="both", padx=8, pady=1)
            # Ajout colonne actions (éditer/supprimer/voir colis)
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=120)
            actions_frame.pack(side="left", fill="y", padx=0.5, pady=0.5)
            actions_frame.pack_propagate(False)
            edit_btn = ctk.CTkButton(actions_frame, text="✏️", width=30, height=30, fg_color="#F3F4F6", text_color="#6B7280", hover_color="#E0E7EF", command=lambda r=row: self.open_edit_reception_popup(r))
            edit_btn.pack(side="left", padx=2)
            delete_btn = ctk.CTkButton(actions_frame, text="🗑️", width=30, height=30, fg_color="#FEE2E2", text_color="#EF4444", hover_color="#FCA5A5", command=lambda r=row: self.confirm_delete_reception(r))
            delete_btn.pack(side="left", padx=2)
            colis_btn = ctk.CTkButton(actions_frame, text="📦 Colis", width=60, height=30, fg_color="#3B82F6", text_color="white", hover_color="#2563EB", command=lambda r=row: self.open_colis_popup(r))
            colis_btn.pack(side="left", padx=2)
        
        # Pagination
        self.render_pagination(table_container, total_count)
    
    def render_pagination(self, parent, total_count):
        """Affiche les contrôles de pagination"""
        items_per_page = getattr(self, 'items_per_page', 10)
        current_page = getattr(self, 'current_page', 0)
        total_pages = (total_count + items_per_page - 1) // items_per_page
        
        # Frame pour la pagination
        pagination_frame = ctk.CTkFrame(parent, fg_color="white")
        pagination_frame.pack(fill="x", pady=(10, 0))
        
        # Informations sur la pagination
        start_item = current_page * items_per_page + 1
        end_item = min((current_page + 1) * items_per_page, total_count)
        
        info_label = ctk.CTkLabel(pagination_frame, 
                                text=f"Affichage {start_item}-{end_item} sur {total_count} résultats", 
                                font=ctk.CTkFont(size=12), text_color="#6B7280")
        info_label.pack(side="left", padx=20)
        
        # Contrôles de pagination
        controls_frame = ctk.CTkFrame(pagination_frame, fg_color="white")
        controls_frame.pack(side="right", padx=20)
        
        # Bouton précédent
        prev_btn = ctk.CTkButton(controls_frame, text="◀ Précédent", 
                               fg_color="#6B7280" if current_page > 0 else "#D1D5DB",
                               hover_color="#4B5563" if current_page > 0 else "#D1D5DB",
                               text_color="white", corner_radius=6, height=28,
                               font=ctk.CTkFont(size=11), 
                               command=lambda: self.change_page(current_page - 1))
        prev_btn.pack(side="left", padx=2)
        
        # Numéros de page
        page_numbers_frame = ctk.CTkFrame(controls_frame, fg_color="white")
        page_numbers_frame.pack(side="left", padx=10)
        
        # Afficher les numéros de page (max 5 pages)
        start_page = max(0, current_page - 2)
        end_page = min(total_pages, start_page + 5)
        
        for page_num in range(start_page, end_page):
            page_btn = ctk.CTkButton(page_numbers_frame, text=str(page_num + 1),
                                   fg_color="#3B82F6" if page_num == current_page else "#F3F4F6",
                                   hover_color="#2563EB" if page_num == current_page else "#E5E7EB",
                                   text_color="white" if page_num == current_page else "#374151",
                                   corner_radius=6, width=32, height=28,
                                   font=ctk.CTkFont(size=11, weight="bold" if page_num == current_page else "normal"),
                                   command=lambda p=page_num: self.change_page(p))
            page_btn.pack(side="left", padx=1)
        
        # Bouton suivant
        next_btn = ctk.CTkButton(controls_frame, text="Suivant ▶", 
                               fg_color="#6B7280" if current_page < total_pages - 1 else "#D1D5DB",
                               hover_color="#4B5563" if current_page < total_pages - 1 else "#D1D5DB",
                               text_color="white", corner_radius=6, height=28,
                               font=ctk.CTkFont(size=11), 
                               command=lambda: self.change_page(current_page + 1))
        next_btn.pack(side="left", padx=2)
        
        # Sélecteur d'éléments par page
        items_frame = ctk.CTkFrame(pagination_frame, fg_color="white")
        items_frame.pack(side="right", padx=20)
        
        ctk.CTkLabel(items_frame, text="Par page:", font=ctk.CTkFont(size=11), text_color="#6B7280").pack(side="left", padx=(0, 5))
        
        items_menu = ctk.CTkOptionMenu(items_frame, values=["5", "10", "15", "20"], 
                                     fg_color="#F3F4F6", text_color="#374151",
                                     button_color="#E5E7EB", button_hover_color="#D1D5DB",
                                     dropdown_fg_color="#F3F4F6", dropdown_text_color="#374151",
                                     corner_radius=6, height=28, width=60,
                                     font=ctk.CTkFont(size=11),
                                     command=self.change_items_per_page)
        items_menu.pack(side="left")
        items_menu.set(str(items_per_page))
    
    def change_page(self, new_page):
        """Change la page actuelle"""
        # Vérifier les limites
        rows, total_count = self.get_filtered_receptions()
        total_pages = (total_count + self.items_per_page - 1) // self.items_per_page
        
        if 0 <= new_page < total_pages:
            self.current_page = new_page
            for widget in self.table_parent.winfo_children():
                widget.destroy()
            self.render_table(self.table_parent)
    
    def change_items_per_page(self, value):
        """Change le nombre d'éléments par page"""
        self.items_per_page = int(value)
        self.current_page = 0  # Retour à la première page
        for widget in self.table_parent.winfo_children():
            widget.destroy()
        self.render_table(self.table_parent)

    def on_window_resize(self, width, height):
        """Méthode appelée quand la fenêtre est redimensionnée"""
        # Adapter la mise en page selon la taille
        if width < 1200:
            # Mode compact
            pass
        else:
            # Mode normal
            pass
    
    def _on_frame_resize(self, event):
        """Gère le redimensionnement du frame"""
        if event.width > 100 and event.height > 100:
            self.on_window_resize(event.width, event.height)

    def _build_topbar(self):
        topbar = ctk.CTkFrame(self.main_content, fg_color="white", height=70)
        topbar.pack(fill="x", pady=(18, 0), padx=24)
        topbar.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(topbar, text="Réception de Marchandises", font=ctk.CTkFont(size=22, weight="bold"), text_color="#222")
        title.grid(row=0, column=0, sticky="w", pady=(8,0))
        
        subtitle = ctk.CTkLabel(topbar, text="Gestion des entrées et réceptions", font=ctk.CTkFont(size=14), text_color="#666")
        subtitle.grid(row=1, column=0, sticky="w")
        
        # Bouton de thème
        self.theme_button = ThemeToggleButton(topbar, self.master)
        self.theme_button.grid(row=0, column=1, rowspan=2, sticky="e", padx=(0,20))
        
        btn = ctk.CTkButton(topbar, text="📦 Nouvelle Réception", fg_color="#3b82f6", hover_color="#2563eb", text_color="white", corner_radius=8, font=ctk.CTkFont(size=14, weight="bold"), width=160, height=36, command=self._open_reception_modal)
        btn.grid(row=0, column=2, rowspan=2, sticky="e", padx=(0,20))

    def _go_back(self):
        """Retourne à la page précédente si possible, sinon dashboard"""
        if hasattr(self.master, 'show_dashboard') and self.previous_page is None:
            self.master.show_dashboard(self.user_info)
        elif hasattr(self.master, 'show_' + str(self.previous_page)):
            getattr(self.master, 'show_' + str(self.previous_page))()
        elif hasattr(self.master, 'show_dashboard'):
            self.master.show_dashboard(self.user_info)
        else:
            messagebox.showinfo("Retour", "Impossible de revenir en arrière. Redémarrez l'application.")

    def _show_error(self, message):
        for widget in self.winfo_children():
            widget.destroy()
        error_frame = ctk.CTkFrame(self, fg_color="#fee2e2", corner_radius=12)
        error_frame.pack(fill="both", expand=True, padx=60, pady=60)
        ctk.CTkLabel(error_frame, text="❌ Erreur lors de l'affichage de la page réception", font=ctk.CTkFont(size=20, weight="bold"), text_color="#b91c1c").pack(pady=(30, 10))
        ctk.CTkLabel(error_frame, text=message, font=ctk.CTkFont(size=15), text_color="#b91c1c").pack(pady=(0, 20))
        ctk.CTkButton(error_frame, text="🏠 Retour à l'accueil", fg_color="#2563eb", text_color="white", font=ctk.CTkFont(size=15, weight="bold"), command=self._go_back).pack(pady=10)

    def _open_reception_modal(self):
        """Ouvre la fenêtre modale pour créer une nouvelle réception."""
        AddReceptionPopup(self)

    def _auto_refresh(self):
        try:
            # Rafraîchir le tableau si visible
            if hasattr(self, 'table_parent') and self.table_parent:
                for widget in self.table_parent.winfo_children():
                    widget.destroy()
                self.render_table(self.table_parent)
            self.update_summary_cards()
            self.update_alertes_urgentes()
            self.update_prochaines_arrivees()
        except Exception:
            pass
        self.after(self._auto_refresh_interval, self._auto_refresh)

    def update_summary_cards(self):
        try:
            self.summary_labels["en_attente"].configure(text=str(database.count_receptions_en_attente()))
            self.summary_labels["recues_aujourdhui"].configure(text=str(database.count_receptions_recues_aujourdhui()))
            self.summary_labels["colis_total"].configure(text=str(database.count_colis_total()))
            self.summary_labels["anomalies"].configure(text=str(database.count_anomalies()))
        except Exception as e:
            pass

    def update_alertes_urgentes(self):
        pass

    def update_prochaines_arrivees(self):
        pass

    def open_edit_reception_popup(self, row):
        EditReceptionPopup(self, row)

    def confirm_delete_reception(self, row):
        def do_delete():
            import database
            success = database.delete_bon_reception(row['id'])
            if success:
                self.master.show_notification("Bon de réception supprimé avec succès !")
            else:
                self.master.show_notification("Erreur lors de la suppression !", duration=3000)
            self._auto_refresh()
        confirm = ctk.CTkToplevel(self)
        confirm.title("Confirmer la suppression")
        confirm.geometry("350x160")
        confirm.grab_set()
        ctk.CTkLabel(confirm, text="Voulez-vous supprimer ce bon de réception ?", font=ctk.CTkFont(size=15, weight="bold"), text_color="#EF4444").pack(pady=(30,10))
        btns = ctk.CTkFrame(confirm, fg_color="white")
        btns.pack(pady=10)
        ctk.CTkButton(btns, text="Oui, supprimer", fg_color="#EF4444", hover_color="#B91C1C", text_color="white", command=lambda: (do_delete(), confirm.destroy())).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="Annuler", fg_color="#6B7280", hover_color="#374151", text_color="white", command=confirm.destroy).pack(side="left", padx=10)

    def open_colis_popup(self, row):
        ColisPopup(self, row)

class AddReceptionPopup(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Créer un Nouveau Bon de Réception")
        self.geometry("700x540")
        self.resizable(True, True)  # Permettre le redimensionnement
        self.minsize(600, 400)  # Taille minimale
        self.configure(fg_color="white")
        self.grab_set()
        self._drag_start_x = None
        self._drag_start_y = None
        self.protocol("WM_DELETE_WINDOW", self.destroy)  # Permettre la fermeture

        # Header
        header = ctk.CTkFrame(self, fg_color="white")
        header.pack(fill="x", pady=(14,0), padx=18)
        ctk.CTkLabel(header, text="Créer un Nouveau Bon de Réception", font=ctk.CTkFont(size=22, weight="bold"), text_color="#222").pack(side="left", pady=6)
        def start_move(event):
            self._drag_start_x = event.x
            self._drag_start_y = event.y
        def do_move(event):
            x = self.winfo_x() + event.x - self._drag_start_x
            y = self.winfo_y() + event.y - self._drag_start_y
            self.geometry(f"+{x}+{y}")
        header.bind("<Button-1>", start_move)
        header.bind("<B1-Motion>", do_move)

        # Main content (scrollable)
        content = ctk.CTkScrollableFrame(self, fg_color="white")
        content.pack(fill="both", expand=True, padx=18, pady=6)

        # Ligne 1 : Numéro de Bon & Fournisseur
        row1 = ctk.CTkFrame(content, fg_color="white")
        row1.pack(fill="x", pady=(0,12))
        # Numéro de Bon
        bon_frame = ctk.CTkFrame(row1, fg_color="white")
        bon_frame.pack(side="left", expand=True, fill="x", padx=(0,8))
        ctk.CTkLabel(bon_frame, text="Numéro de Bon *", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w")
        self.bon_entry = ctk.CTkEntry(bon_frame, fg_color="#f3f4f6", text_color="#222", border_color="#d1d5db", border_width=1, height=38, font=ctk.CTkFont(size=14))
        self.bon_entry.pack(fill="x", pady=(4,0))
        # Fournisseur
        fournisseur_frame = ctk.CTkFrame(row1, fg_color="white")
        fournisseur_frame.pack(side="left", expand=True, fill="x", padx=(8,0))
        ctk.CTkLabel(fournisseur_frame, text="Fournisseur *", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w")
        self.fournisseur_menu = ctk.CTkOptionMenu(fournisseur_frame, values=["Sélectionner un fournisseur", "Dell", "HP", "Lenovo", "Samsung", "Logitech"], fg_color="#f3f4f6", text_color="#222", button_color="#e5e7eb", button_hover_color="#d1d5db", dropdown_fg_color="#f3f4f6", dropdown_text_color="#222", font=ctk.CTkFont(size=14))
        self.fournisseur_menu.pack(fill="x", pady=(4,0))

        # Ligne 2 : Date prévue & Colis attendu
        row2 = ctk.CTkFrame(content, fg_color="white")
        row2.pack(fill="x", pady=(0,12))
        # Date prévue
        date_frame = ctk.CTkFrame(row2, fg_color="white")
        date_frame.pack(side="left", expand=True, fill="x", padx=(0,8))
        ctk.CTkLabel(date_frame, text="Date de Réception Prévue *", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w")
        self.date_entry = DateEntry(date_frame, date_pattern="yyyy-mm-dd", font=("Segoe UI", 13), background="#f3f4f6", foreground="#222", borderwidth=1, width=18)
        self.date_entry.pack(fill="x", pady=(4,0))
        # Colis attendu
        colis_frame = ctk.CTkFrame(row2, fg_color="white")
        colis_frame.pack(side="left", expand=True, fill="x", padx=(8,0))
        ctk.CTkLabel(colis_frame, text="Nombre de Colis Attendu *", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w")
        self.colis_entry = ctk.CTkEntry(colis_frame, fg_color="#f3f4f6", text_color="#222", border_color="#d1d5db", border_width=1, height=38, font=ctk.CTkFont(size=14))
        self.colis_entry.pack(fill="x", pady=(4,0))

        # Ligne 3 : Poids total & Bon d'expédition lié
        row3 = ctk.CTkFrame(content, fg_color="white")
        row3.pack(fill="x", pady=(0,12))
        # Poids total
        poids_frame = ctk.CTkFrame(row3, fg_color="white")
        poids_frame.pack(side="left", expand=True, fill="x", padx=(0,8))
        ctk.CTkLabel(poids_frame, text="Poids Total Attendu (kg) *", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w")
        self.poids_entry = ctk.CTkEntry(poids_frame, fg_color="#f3f4f6", text_color="#222", border_color="#d1d5db", border_width=1, height=38, font=ctk.CTkFont(size=14))
        self.poids_entry.pack(fill="x", pady=(4,0))
        # Bon d'expédition lié
        exp_frame = ctk.CTkFrame(row3, fg_color="white")
        exp_frame.pack(side="left", expand=True, fill="x", padx=(8,0))
        ctk.CTkLabel(exp_frame, text="Bon d'Expédition Lié", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w")
        self.exp_menu = ctk.CTkOptionMenu(exp_frame, values=["Sélectionner un bon d'expédition", "EXP-2024-001", "EXP-2024-002"], fg_color="#f3f4f6", text_color="#222", button_color="#e5e7eb", button_hover_color="#d1d5db", dropdown_fg_color="#f3f4f6", dropdown_text_color="#222", font=ctk.CTkFont(size=14))
        self.exp_menu.pack(fill="x", pady=(4,0))

        # Commentaires
        ctk.CTkLabel(content, text="Commentaires", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w", pady=(0,2))
        self.comment_text = ctk.CTkTextbox(content, fg_color="#f3f4f6", text_color="#222", border_color="#d1d5db", border_width=1, height=48, font=ctk.CTkFont(size=14))
        self.comment_text.insert("0.0", "Informations supplémentaires sur la réception...")
        self.comment_text.pack(fill="x", pady=(4,12))

        # Produits attendus
        ctk.CTkLabel(content, text="Produits Attendus", font=ctk.CTkFont(size=15, weight="bold"), text_color="#222").pack(anchor="w", pady=(8,6))
        self.products_frame = ctk.CTkFrame(content, fg_color="white")
        self.products_frame.pack(fill="x", pady=(0,8))
        self.product_rows = []
        self.add_product_row()
        add_btn = ctk.CTkButton(content, text="+ Ajouter un produit", fg_color="#3B82F6", hover_color="#2563EB", text_color="white", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, height=34, command=self.add_product_row)
        add_btn.pack(anchor="w", pady=(0,12))

        # Ligne 5 : Boutons d'action
        row5 = ctk.CTkFrame(content, fg_color="white")
        row5.pack(fill="x", pady=(20, 0))
        ctk.CTkButton(row5, text="Annuler", fg_color="#EF4444", hover_color="#DC2626", text_color="white", corner_radius=12, height=44, font=ctk.CTkFont(size=16, weight="bold"), command=self.destroy).pack(side="left", expand=True, fill="x", padx=(0, 12))
        ctk.CTkButton(row5, text="Terminer la Réception", fg_color="#10B981", hover_color="#059669", text_color="white", corner_radius=12, height=44, font=ctk.CTkFont(size=16, weight="bold"), command=self.validate_and_create).pack(side="left", expand=True, fill="x", padx=(12, 0))
        
        # Labels d'erreur (initialement cachés)
        self.error_labels = {}
        self.error_labels['bon'] = ctk.CTkLabel(bon_frame, text="", font=ctk.CTkFont(size=12), text_color="#EF4444")
        self.error_labels['fournisseur'] = ctk.CTkLabel(fournisseur_frame, text="", font=ctk.CTkFont(size=12), text_color="#EF4444")
        self.error_labels['date'] = ctk.CTkLabel(date_frame, text="", font=ctk.CTkFont(size=12), text_color="#EF4444")
        self.error_labels['colis'] = ctk.CTkLabel(colis_frame, text="", font=ctk.CTkFont(size=12), text_color="#EF4444")
        self.error_labels['poids'] = ctk.CTkLabel(poids_frame, text="", font=ctk.CTkFont(size=12), text_color="#EF4444")

    def add_product_row(self):
        row = ctk.CTkFrame(self.products_frame, fg_color="white", border_color="#e5e7eb", border_width=1, corner_radius=8)
        row.pack(fill="x", pady=4)
        # Produit
        prod_menu = ctk.CTkOptionMenu(row, values=["Sélectionner un", "Produit A", "Produit B"], fg_color="#f3f4f6", text_color="#222", button_color="#e5e7eb", button_hover_color="#d1d5db", dropdown_fg_color="#f3f4f6", dropdown_text_color="#222", width=160, font=ctk.CTkFont(size=14))
        prod_menu.pack(side="left", padx=(8,8), pady=6)
        # Quantité
        qty_entry = ctk.CTkEntry(row, fg_color="#f3f4f6", text_color="#222", border_color="#d1d5db", border_width=1, width=60, height=32, font=ctk.CTkFont(size=14))
        qty_entry.insert(0, "10")
        qty_entry.pack(side="left", padx=(0,8), pady=6)
        # Poids unitaire
        weight_entry = ctk.CTkEntry(row, fg_color="#f3f4f6", text_color="#222", border_color="#d1d5db", border_width=1, width=80, height=32, font=ctk.CTkFont(size=14))
        weight_entry.insert(0, "0.5")
        weight_entry.pack(side="left", padx=(0,8), pady=6)
        # Supprimer
        del_btn = ctk.CTkButton(row, text="🗑️", fg_color="white", hover_color="#EF4444", text_color="#EF4444", width=32, height=32, corner_radius=8, font=ctk.CTkFont(size=16), command=lambda: self.remove_product_row(row))
        del_btn.pack(side="left", padx=(0,8), pady=6)
        self.product_rows.append(row)

    def remove_product_row(self, row):
        row.destroy()
        self.product_rows.remove(row)

    def validate_and_create(self):
        """Valide les champs obligatoires avant de créer la réception"""
        # Réinitialiser tous les messages d'erreur
        for label in self.error_labels.values():
            label.configure(text="")
        # Réinitialiser les bordures
        self.bon_entry.configure(border_color="#d1d5db")
        self.fournisseur_menu.configure(button_color="#e5e7eb")
        # self.date_entry.configure(border_color="#d1d5db")  # LIGNE SUPPRIMÉE
        self.colis_entry.configure(border_color="#d1d5db")
        self.poids_entry.configure(border_color="#d1d5db")
        has_errors = False
        # Validation du numéro de bon
        if not self.bon_entry.get().strip():
            self.error_labels['bon'].configure(text="Le numéro de bon est obligatoire. Veuillez saisir un identifiant unique pour le bon de réception.")
            self.bon_entry.configure(border_color="#EF4444")
            has_errors = True
        # Validation du fournisseur
        if self.fournisseur_menu.get() == "Sélectionner un fournisseur":
            self.error_labels['fournisseur'].configure(text="Veuillez sélectionner un fournisseur dans la liste déroulante.")
            self.fournisseur_menu.configure(button_color="#EF4444")
            has_errors = True
        # Validation de la date
        if not self.date_entry.get().strip():
            self.error_labels['date'].configure(text="La date de réception est obligatoire. Veuillez choisir une date valide à l'aide du calendrier.")
            self.date_entry.configure(background="#ffe5e5")
            has_errors = True
        # Validation du nombre de colis
        colis_text = self.colis_entry.get().strip()
        if not colis_text:
            self.error_labels['colis'].configure(text="Le nombre de colis est obligatoire. Indiquez combien de colis sont attendus pour cette réception.")
            self.colis_entry.configure(border_color="#EF4444")
            has_errors = True
        elif not colis_text.isdigit() or int(colis_text) <= 0:
            self.error_labels['colis'].configure(text="Le nombre de colis doit être un nombre entier positif (ex: 5, 10, 20). Veuillez corriger la valeur saisie.")
            self.colis_entry.configure(border_color="#EF4444")
            has_errors = True
        # Validation du poids
        poids_text = self.poids_entry.get().strip()
        if not poids_text:
            self.error_labels['poids'].configure(text="Le poids total est obligatoire. Veuillez indiquer le poids total (en kg) de tous les colis.")
            self.poids_entry.configure(border_color="#EF4444")
            has_errors = True
        else:
            try:
                poids = float(poids_text)
                if poids <= 0:
                    self.error_labels['poids'].configure(text="Le poids doit être un nombre positif (ex: 12.5). Veuillez corriger la valeur saisie.")
                    self.poids_entry.configure(border_color="#EF4444")
                    has_errors = True
            except ValueError:
                self.error_labels['poids'].configure(text="Le poids doit être un nombre valide (ex: 10, 15.5). Veuillez corriger la valeur saisie.")
                self.poids_entry.configure(border_color="#EF4444")
                has_errors = True
        # Afficher les labels d'erreur
        for label in self.error_labels.values():
            if label.cget("text"):
                label.pack(anchor="w", pady=(2, 0))
        if not has_errors:
            # Ajout réel en base
            reference = self.bon_entry.get().strip()
            fournisseur = self.fournisseur_menu.get()
            date_reception = self.date_entry.get().strip()
            observation = self.comment_text.get("0.0", "end") if hasattr(self, 'comment_text') else ''
            nb_colis = int(self.colis_entry.get().strip())
            poids_total = float(self.poids_entry.get().strip())
            success = database.add_bon_reception(reference, fournisseur, date_reception, observation, nb_colis, poids_total)
            if success:
                self.master.master.show_notification("Bon de réception ajouté avec succès !")
            else:
                self.master.master.show_notification("Erreur lors de l'ajout !", duration=3000)
            self.master._auto_refresh()
            self.destroy()

    def show_success_popup(self, message="Bon de réception créé avec succès !"):
        popup = ctk.CTkToplevel(self)
        popup.title("Succès")
        popup.geometry("320x140")
        popup.resizable(False, False)
        popup.configure(fg_color="#f0fdf4")
        popup.grab_set()
        ctk.CTkLabel(popup, text="✅", font=ctk.CTkFont(size=40), text_color="#22c55e").pack(pady=(16,0))
        ctk.CTkLabel(popup, text=message, font=ctk.CTkFont(size=14, weight="bold"), text_color="#166534").pack(pady=(5,0))
        ctk.CTkButton(popup, text="OK", fg_color="#22c55e", hover_color="#16a34a", text_color="white", corner_radius=8, height=32, font=ctk.CTkFont(size=13, weight="bold"), command=lambda: (popup.destroy(), self.destroy())).pack(pady=12)

class ScannerPopup(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Scanner Code-Barres")
        self.geometry("400x420")
        self.resizable(True, True)  # Permettre le redimensionnement
        self.minsize(350, 350)  # Taille minimale
        self.configure(fg_color="white")
        self.grab_set()
        self._drag_start_x = None
        self._drag_start_y = None
        self.protocol("WM_DELETE_WINDOW", self.destroy)  # Permettre la fermeture

        # Header
        header = ctk.CTkFrame(self, fg_color="white")
        header.pack(fill="x", pady=(16,0), padx=18)
        ctk.CTkLabel(header, text="Scanner Code-Barres", font=ctk.CTkFont(size=20, weight="bold"), text_color="#222").pack(side="left", pady=6)
        def start_move(event):
            self._drag_start_x = event.x
            self._drag_start_y = event.y
        def do_move(event):
            x = self.winfo_x() + event.x - self._drag_start_x
            y = self.winfo_y() + event.y - self._drag_start_y
            self.geometry(f"+{x}+{y}")
        header.bind("<Button-1>", start_move)
        header.bind("<B1-Motion>", do_move)

        # QR Icon
        qr_frame = ctk.CTkFrame(self, fg_color="#f3f4f6", width=120, height=120, corner_radius=16)
        qr_frame.pack(pady=(24,8))
        qr_frame.pack_propagate(False)
        ctk.CTkLabel(qr_frame, text="\U0001F7E6\U0001F7E6\n\U0001F7E6\U0001F7E6", font=ctk.CTkFont(size=44), text_color="#9CA3AF").pack(expand=True)

        # Instruction
        ctk.CTkLabel(self, text="Pointez votre caméra vers le code-barres du colis", font=ctk.CTkFont(size=14), text_color="#6B7280").pack(pady=(0,10))

        # Champ d'entrée
        entry_frame = ctk.CTkFrame(self, fg_color="#f3f4f6", corner_radius=12)
        entry_frame.pack(fill="x", padx=18, pady=(0,18))
        self.entry = ctk.CTkEntry(entry_frame, fg_color="#f3f4f6", text_color="#222", border_color="#e5e7eb", border_width=1, font=ctk.CTkFont(size=14), placeholder_text="Ou saisissez le code manuellement")
        self.entry.pack(fill="x", padx=8, pady=8)
        
        # Label d'erreur
        self.error_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12), text_color="#EF4444")
        
        # Boutons
        btns = ctk.CTkFrame(self, fg_color="white")
        btns.pack(fill="x", padx=18, pady=(0,10))
        scan_btn = ctk.CTkButton(btns, text="\U0001F4F7  Démarrer Scan", fg_color="#3B82F6", hover_color="#2563EB", text_color="white", font=ctk.CTkFont(size=15, weight="bold"), corner_radius=8, height=38)
        scan_btn.pack(side="left", expand=True, fill="x", padx=(0,8))
        valider_btn = ctk.CTkButton(btns, text="✓  Valider", fg_color="#22c55e", hover_color="#16a34a", text_color="white", font=ctk.CTkFont(size=15, weight="bold"), corner_radius=8, height=38, command=self.validate_and_scan)
        valider_btn.pack(side="left", expand=True, fill="x", padx=(8,0))

    def validate_and_scan(self):
        """Valide le code-barres avant de procéder au scan"""
        code = self.entry.get().strip()
        
        # Masquer le message d'erreur précédent
        self.error_label.pack_forget()
        
        # Réinitialiser la bordure
        self.entry.configure(border_color="#e5e7eb")
        
        if not code:
            self.error_label.configure(text="Veuillez saisir ou scanner un code-barres")
            self.error_label.pack(pady=(0, 10))
            self.entry.configure(border_color="#EF4444")
            return
        
        # Validation basique du format (au moins 5 caractères)
        if len(code) < 5:
            self.error_label.configure(text="Le code-barres doit contenir au moins 5 caractères")
            self.error_label.pack(pady=(0, 10))
            self.entry.configure(border_color="#EF4444")
            return
        
        # Si la validation passe, procéder au scan
        self.show_success_popup()

    def show_success_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Succès")
        popup.geometry("320x140")
        popup.resizable(False, False)
        popup.configure(fg_color="#f0fdf4")
        popup.grab_set()
        ctk.CTkLabel(popup, text="✅", font=ctk.CTkFont(size=40), text_color="#22c55e").pack(pady=(16,0))
        ctk.CTkLabel(popup, text="Code-barres scanné avec succès !", font=ctk.CTkFont(size=14, weight="bold"), text_color="#166534").pack(pady=(5,0))
        ctk.CTkButton(popup, text="OK", fg_color="#22c55e", hover_color="#16a34a", text_color="white", corner_radius=8, height=32, font=ctk.CTkFont(size=13, weight="bold"), command=lambda: (popup.destroy(), self.destroy())).pack(pady=12)

class ExportReceptionPopup(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Exporter les Réceptions")
        self.geometry("600x500")
        self.resizable(True, True)
        self.minsize(550, 450)
        self.configure(fg_color="white")
        self.grab_set()
        self._drag_start_x = None
        self._drag_start_y = None
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.master = master

        # Header moderne avec icône
        header = ctk.CTkFrame(self, fg_color="white")
        header.pack(fill="x", pady=(20,0), padx=20)
        ctk.CTkLabel(header, text="📊", font=ctk.CTkFont(size=24)).pack(side="left", padx=(0,10))
        ctk.CTkLabel(header, text="Exporter les Réceptions", font=ctk.CTkFont(size=22, weight="bold"), text_color="#1F2937").pack(side="left")
        
        def start_move(event):
            self._drag_start_x = event.x
            self._drag_start_y = event.y
        def do_move(event):
            x = self.winfo_x() + event.x - self._drag_start_x
            y = self.winfo_y() + event.y - self._drag_start_y
            self.geometry(f"+{x}+{y}")
        header.bind("<Button-1>", start_move)
        header.bind("<B1-Motion>", do_move)

        # Main content avec design moderne
        content = ctk.CTkFrame(self, fg_color="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Section 1: Contenu à exporter avec design moderne
        section1 = ctk.CTkFrame(content, fg_color="#F8FAFC", corner_radius=12, border_width=1, border_color="#E2E8F0")
        section1.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(section1, text="📋 Contenu à exporter", font=ctk.CTkFont(size=16, weight="bold"), text_color="#1F2937").pack(anchor="w", padx=20, pady=(15,10))
        
        self.export_choice = ctk.StringVar(value="current")
        ctk.CTkRadioButton(section1, text="Vue actuelle (avec filtres appliqués)", variable=self.export_choice, value="current", 
                          font=ctk.CTkFont(size=14), text_color="#374151", fg_color="#3B82F6", hover_color="#2563EB").pack(anchor="w", padx=20, pady=2)
        ctk.CTkRadioButton(section1, text="Toutes les réceptions (données complètes)", variable=self.export_choice, value="all", 
                          font=ctk.CTkFont(size=14), text_color="#374151", fg_color="#3B82F6", hover_color="#2563EB").pack(anchor="w", padx=20, pady=(2,15))

        # Section 2: Format d'export avec design moderne
        section2 = ctk.CTkFrame(content, fg_color="#F8FAFC", corner_radius=12, border_width=1, border_color="#E2E8F0")
        section2.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(section2, text="📄 Format d'export", font=ctk.CTkFont(size=16, weight="bold"), text_color="#1F2937").pack(anchor="w", padx=20, pady=(15,15))
        
        format_frame = ctk.CTkFrame(section2, fg_color="transparent")
        format_frame.pack(fill="x", padx=20, pady=(0,15))
        
        # Boutons de format avec design moderne et icônes
        csv_btn = ctk.CTkButton(format_frame, text="📊 CSV", fg_color="#3B82F6", hover_color="#2563EB", 
                               text_color="white", font=ctk.CTkFont(size=14, weight="bold"), 
                               corner_radius=10, height=45, width=120,
                               command=lambda: self.export_data("CSV"))
        csv_btn.pack(side="left", padx=(0, 15))
        
        excel_btn = ctk.CTkButton(format_frame, text="📈 Excel", fg_color="#10B981", hover_color="#059669", 
                                 text_color="white", font=ctk.CTkFont(size=14, weight="bold"), 
                                 corner_radius=10, height=45, width=120,
                                 command=lambda: self.export_data("Excel"))
        excel_btn.pack(side="left", padx=(0, 15))
        
        pdf_btn = ctk.CTkButton(format_frame, text="📄 PDF", fg_color="#EF4444", hover_color="#DC2626", 
                               text_color="white", font=ctk.CTkFont(size=14, weight="bold"), 
                               corner_radius=10, height=45, width=120,
                               command=lambda: self.export_data("PDF"))
        pdf_btn.pack(side="left")

        # Section 3: Options d'export avec design moderne
        section3 = ctk.CTkFrame(content, fg_color="#F8FAFC", corner_radius=12, border_width=1, border_color="#E2E8F0")
        section3.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(section3, text="⚙️ Options d'export", font=ctk.CTkFont(size=16, weight="bold"), text_color="#1F2937").pack(anchor="w", padx=20, pady=(15,10))
        
        self.include_headers = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(section3, text="Inclure les en-têtes de colonnes", variable=self.include_headers, 
                       font=ctk.CTkFont(size=14), text_color="#374151", fg_color="#3B82F6", hover_color="#2563EB").pack(anchor="w", padx=20, pady=2)
        
        self.include_timestamps = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(section3, text="Inclure les horodatages", variable=self.include_timestamps, 
                       font=ctk.CTkFont(size=14), text_color="#374151", fg_color="#3B82F6", hover_color="#2563EB").pack(anchor="w", padx=20, pady=2)

        self.include_summary = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(section3, text="Inclure un résumé statistique", variable=self.include_summary, 
                       font=ctk.CTkFont(size=14), text_color="#374151", fg_color="#3B82F6", hover_color="#2563EB").pack(anchor="w", padx=20, pady=(2,15))

        # Boutons d'action avec design moderne
        btn_frame = ctk.CTkFrame(content, fg_color="white")
        btn_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(btn_frame, text="❌ Annuler", fg_color="#6B7280", hover_color="#4B5563", 
                     text_color="white", corner_radius=10, height=45, 
                     font=ctk.CTkFont(size=15, weight="bold"), 
                     command=self.destroy).pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        ctk.CTkButton(btn_frame, text="💾 Exporter", fg_color="#10B981", hover_color="#059669", 
                     text_color="white", corner_radius=10, height=45, 
                     font=ctk.CTkFont(size=15, weight="bold"), 
                     command=self.show_export_options).pack(side="left", expand=True, fill="x", padx=(10, 0))

    def export_data(self, format_type):
        """Exporte les données dans le format spécifié"""
        try:
            import os
            import datetime
            from tkinter import filedialog
            
            # Récupérer les données depuis la base
            import database
            if self.export_choice.get() == "current":
                # Utiliser les données filtrées actuelles
                receptions, total_count = self.master.get_filtered_receptions()
            else:
                # Utiliser toutes les données
                receptions = database.get_all_receptions()
            
            # Créer le nom de fichier avec timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"receptions_{timestamp}"
            
            # Obtenir le dossier Downloads
            downloads_path = os.path.expanduser("~/Downloads")
            if not os.path.exists(downloads_path):
                downloads_path = os.path.expanduser("~/Desktop")  # Fallback
            
            if format_type == "CSV":
                filepath = self.export_to_csv(receptions, downloads_path, filename)
            elif format_type == "Excel":
                filepath = self.export_to_excel(receptions, downloads_path, filename)
            elif format_type == "PDF":
                filepath = self.export_to_pdf(receptions, downloads_path, filename)
            
            # Afficher le message de succès avec le chemin
            self.show_export_success(format_type, filepath)
            
        except Exception as e:
            self.show_export_error(str(e))

    def export_to_csv(self, receptions, folder_path, filename):
        """Exporte les données en CSV"""
        import csv
        import os
        
        filepath = os.path.join(folder_path, f"{filename}.csv")
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # En-têtes
            if self.include_headers.get():
                headers = ["Référence", "Fournisseur", "Date prévue", "Date réception effective", "Observation", "Statut", "Magasinier"]
                if self.include_timestamps.get():
                    headers.append("Date d'export")
                writer.writerow(headers)
            
            # Données
            for reception in receptions:
                row = [
                    reception['reference'],
                    reception['fournisseur'],
                    str(reception['date_prevue'])[:16] if reception['date_prevue'] else '-',
                    str(reception['date_reception_effective'])[:16] if reception['date_reception_effective'] else '-',
                    reception['observation'] or '-',
                    reception['statut'],
                    reception['magasinier']
                ]
                if self.include_timestamps.get():
                    row.append(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
                writer.writerow(row)
            
            # Résumé si demandé
            if self.include_summary.get():
                writer.writerow([])
                writer.writerow(["RÉSUMÉ"])
                writer.writerow(["Total réceptions", len(receptions)])
                writer.writerow(["Réceptions en attente", len([r for r in receptions if r['statut'] == 'en_attente'])])
                writer.writerow(["Réceptions reçues", len([r for r in receptions if r['statut'] == 'recu'])])
        
        return filepath

    def export_to_excel(self, receptions, folder_path, filename):
        """Exporte les données en Excel"""
        try:
            import pandas as pd
            import os
            
            filepath = os.path.join(folder_path, f"{filename}.xlsx")
            
            # Préparer les données
            data = []
            for reception in receptions:
                row = {
                    "Référence": reception['reference'],
                    "Fournisseur": reception['fournisseur'],
                    "Date prévue": str(reception['date_prevue'])[:16] if reception['date_prevue'] else '-',
                    "Date réception effective": str(reception['date_reception_effective'])[:16] if reception['date_reception_effective'] else '-',
                    "Observation": reception['observation'] or '-',
                    "Statut": reception['statut'],
                    "Magasinier": reception['magasinier']
                }
                if self.include_timestamps.get():
                    row["Date d'export"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                data.append(row)
            
            # Créer le DataFrame
            df = pd.DataFrame(data)
            
            # Exporter avec formatage
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Réceptions', index=False)
                
                # Formatage de la feuille
                worksheet = writer.sheets['Réceptions']
                
                # Ajuster la largeur des colonnes
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                
                # Ajouter un résumé si demandé
                if self.include_summary.get():
                    summary_data = {
                        "Métrique": ["Total réceptions", "Réceptions en attente", "Réceptions reçues"],
                        "Valeur": [
                            len(receptions),
                            len([r for r in receptions if r['statut'] == 'en_attente']),
                            len([r for r in receptions if r['statut'] == 'recu'])
                        ]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Résumé', index=False)
            
            return filepath
            
        except ImportError:
            # Fallback si pandas n'est pas installé
            return self.export_to_csv(receptions, folder_path, filename)

    def export_to_pdf(self, receptions, folder_path, filename):
        """Exporte les données en PDF"""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            import os
            
            filepath = os.path.join(folder_path, f"{filename}.pdf")
            
            # Créer le document PDF
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1  # Centré
            )
            
            # Titre
            title = Paragraph("Rapport des Réceptions", title_style)
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Préparer les données pour le tableau
            if self.include_headers.get():
                headers = ["Référence", "Fournisseur", "Date prévue", "Statut", "Magasinier"]
                data = [headers]
            else:
                data = []
            
            for reception in receptions:
                row = [
                    reception['reference'],
                    reception['fournisseur'],
                    str(reception['date_prevue'])[:10] if reception['date_prevue'] else '-',
                    reception['statut'],
                    reception['magasinier']
                ]
                data.append(row)
            
            # Créer le tableau
            if data:
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(table)
            
            # Ajouter un résumé si demandé
            if self.include_summary.get():
                story.append(Spacer(1, 30))
                summary_title = Paragraph("Résumé", styles['Heading2'])
                story.append(summary_title)
                
                summary_data = [
                    ["Métrique", "Valeur"],
                    ["Total réceptions", str(len(receptions))],
                    ["Réceptions en attente", str(len([r for r in receptions if r['statut'] == 'en_attente']))],
                    ["Réceptions reçues", str(len([r for r in receptions if r['statut'] == 'recu']))]
                ]
                
                summary_table = Table(summary_data)
                summary_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(summary_table)
            
            # Horodatage si demandé
            if self.include_timestamps.get():
                story.append(Spacer(1, 20))
                timestamp = Paragraph(f"Exporté le : {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal'])
                story.append(timestamp)
            
            # Générer le PDF
            doc.build(story)
            return filepath
            
        except ImportError:
            # Fallback si reportlab n'est pas installé
            return self.export_to_csv(receptions, folder_path, filename)

    def show_export_options(self):
        """Affiche les options d'export"""
        # Pour l'instant, on utilise CSV par défaut
        self.export_data("CSV")

    def show_export_success(self, format_type, filepath):
        """Affiche le message de succès d'export avec le chemin du fichier"""
        popup = ctk.CTkToplevel(self)
        popup.title("Export Réussi")
        popup.geometry("450x200")
        popup.resizable(False, False)
        popup.configure(fg_color="#f0fdf4")
        popup.grab_set()
        
        ctk.CTkLabel(popup, text="✅", font=ctk.CTkFont(size=40), text_color="#22c55e").pack(pady=(20,0))
        ctk.CTkLabel(popup, text=f"Export {format_type} réussi !", font=ctk.CTkFont(size=16, weight="bold"), text_color="#166534").pack(pady=(5,10))
        ctk.CTkLabel(popup, text=f"Fichier sauvegardé dans :", font=ctk.CTkFont(size=12), text_color="#374151").pack()
        ctk.CTkLabel(popup, text=filepath, font=ctk.CTkFont(size=11), text_color="#6B7280").pack(pady=(0,15))
        
        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=(0,20))
        
        ctk.CTkButton(btn_frame, text="Ouvrir le dossier", fg_color="#3B82F6", hover_color="#2563EB", 
                     text_color="white", corner_radius=8, height=32, 
                     font=ctk.CTkFont(size=12, weight="bold"), 
                     command=lambda: self.open_folder(filepath)).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="OK", fg_color="#22c55e", hover_color="#16a34a", 
                     text_color="white", corner_radius=8, height=32, 
                     font=ctk.CTkFont(size=12, weight="bold"), 
                     command=lambda: (popup.destroy(), self.destroy())).pack(side="left", padx=5)

    def open_folder(self, filepath):
        """Ouvre le dossier contenant le fichier exporté"""
        import os
        import subprocess
        import platform
        
        folder_path = os.path.dirname(filepath)
        
        if platform.system() == "Windows":
            subprocess.run(["explorer", folder_path])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", folder_path])
        else:  # Linux
            subprocess.run(["xdg-open", folder_path])

    def show_export_error(self, error_message):
        """Affiche le message d'erreur d'export"""
        popup = ctk.CTkToplevel(self)
        popup.title("Erreur d'Export")
        popup.geometry("400x180")
        popup.resizable(False, False)
        popup.configure(fg_color="#fef2f2")
        popup.grab_set()
        
        ctk.CTkLabel(popup, text="❌", font=ctk.CTkFont(size=40), text_color="#EF4444").pack(pady=(20,0))
        ctk.CTkLabel(popup, text="Erreur lors de l'export", font=ctk.CTkFont(size=16, weight="bold"), text_color="#DC2626").pack(pady=(5,10))
        ctk.CTkLabel(popup, text=error_message, font=ctk.CTkFont(size=12), text_color="#6B7280").pack(pady=(0,15))
        ctk.CTkButton(popup, text="OK", fg_color="#EF4444", hover_color="#DC2626", 
                     text_color="white", corner_radius=8, height=32, 
                     font=ctk.CTkFont(size=12, weight="bold"), 
                     command=popup.destroy).pack(pady=10)

class SearchReceptionPopup(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Rechercher un Bon de Réception")
        self.geometry("500x400")
        self.resizable(True, True)
        self.minsize(450, 350)
        self.configure(fg_color="white")
        self.grab_set()
        self._drag_start_x = None
        self._drag_start_y = None
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Header
        header = ctk.CTkFrame(self, fg_color="white")
        header.pack(fill="x", pady=(16,0), padx=18)
        ctk.CTkLabel(header, text="Rechercher un Bon de Réception", font=ctk.CTkFont(size=20, weight="bold"), text_color="#222").pack(side="left", pady=6)
        def start_move(event):
            self._drag_start_x = event.x
            self._drag_start_y = event.y
        def do_move(event):
            x = self.winfo_x() + event.x - self._drag_start_x
            y = self.winfo_y() + event.y - self._drag_start_y
            self.geometry(f"+{x}+{y}")
        header.bind("<Button-1>", start_move)
        header.bind("<B1-Motion>", do_move)

        # Main content
        content = ctk.CTkFrame(self, fg_color="white")
        content.pack(fill="both", expand=True, padx=18, pady=18)

        # Section de recherche
        ctk.CTkLabel(content, text="Critères de recherche", font=ctk.CTkFont(size=16, weight="bold"), text_color="#222").pack(anchor="w", pady=(0, 15))
        
        # Numéro de bon
        bon_frame = ctk.CTkFrame(content, fg_color="white")
        bon_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(bon_frame, text="Numéro de Bon", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w")
        self.bon_search_entry = ctk.CTkEntry(bon_frame, fg_color="#f3f4f6", text_color="#222", border_color="#d1d5db", border_width=1, height=38, font=ctk.CTkFont(size=14), placeholder_text="Ex: BR-2024-045")
        self.bon_search_entry.pack(fill="x", pady=(4, 0))

        # Fournisseur
        fournisseur_frame = ctk.CTkFrame(content, fg_color="white")
        fournisseur_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(fournisseur_frame, text="Fournisseur", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w")
        self.fournisseur_search_menu = ctk.CTkOptionMenu(fournisseur_frame, values=["Tous les fournisseurs", "Dell", "HP", "Lenovo", "Samsung", "Logitech"], fg_color="#f3f4f6", text_color="#222", button_color="#e5e7eb", button_hover_color="#d1d5db", dropdown_fg_color="#f3f4f6", dropdown_text_color="#222", font=ctk.CTkFont(size=14))
        self.fournisseur_search_menu.pack(fill="x", pady=(4, 0))

        # Date
        date_frame = ctk.CTkFrame(content, fg_color="white")
        date_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(date_frame, text="Période", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w")
        self.date_search_menu = ctk.CTkOptionMenu(date_frame, values=["Toutes les dates", "Aujourd'hui", "Cette semaine", "Ce mois", "Dernier mois"], fg_color="#f3f4f6", text_color="#222", button_color="#e5e7eb", button_hover_color="#d1d5db", dropdown_fg_color="#f3f4f6", dropdown_text_color="#222", font=ctk.CTkFont(size=14))
        self.date_search_menu.pack(fill="x", pady=(4, 0))

        # Boutons d'action
        btn_frame = ctk.CTkFrame(content, fg_color="white")
        btn_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(btn_frame, text="Annuler", fg_color="#EF4444", hover_color="#DC2626", 
                     text_color="white", corner_radius=12, height=44, 
                     font=ctk.CTkFont(size=16, weight="bold"), 
                     command=self.destroy).pack(side="left", expand=True, fill="x", padx=(0, 12))
        
        ctk.CTkButton(btn_frame, text="Rechercher", fg_color="#F59E0B", hover_color="#D97706", 
                     text_color="white", corner_radius=12, height=44, 
                     font=ctk.CTkFont(size=16, weight="bold"), 
                     command=self.perform_search).pack(side="left", expand=True, fill="x", padx=(12, 0))

    def perform_search(self):
        """Effectue la recherche et affiche les résultats"""
        # Simuler une recherche
        self.show_search_results()

    def show_search_results(self):
        """Affiche les résultats de recherche"""
        popup = ctk.CTkToplevel(self)
        popup.title("Résultats de Recherche")
        popup.geometry("400x300")
        popup.resizable(True, True)
        popup.configure(fg_color="white")
        popup.grab_set()
        
        ctk.CTkLabel(popup, text="🔍", font=ctk.CTkFont(size=40), text_color="#F59E0B").pack(pady=(20, 0))
        ctk.CTkLabel(popup, text="Résultats trouvés", font=ctk.CTkFont(size=18, weight="bold"), text_color="#222").pack(pady=(10, 5))
        ctk.CTkLabel(popup, text="3 bons de réception trouvés", font=ctk.CTkFont(size=14), text_color="#6B7280").pack(pady=(0, 20))
        
        # Liste des résultats
        results_frame = ctk.CTkScrollableFrame(popup, fg_color="white", height=150)
        results_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        results = [
            ("BR-2024-045", "Dell Technologies", "En Attente"),
            ("BR-2024-044", "HP Enterprise", "Reçue"),
            ("BR-2024-043", "Lenovo Group", "Partielle")
        ]
        
        for bon, fournisseur, status in results:
            result_frame = ctk.CTkFrame(results_frame, fg_color="#f3f4f6", corner_radius=8)
            result_frame.pack(fill="x", pady=2)
            ctk.CTkLabel(result_frame, text=f"{bon} - {fournisseur}", font=ctk.CTkFont(size=12, weight="bold"), text_color="#222").pack(anchor="w", padx=10, pady=5)
            ctk.CTkLabel(result_frame, text=f"Statut: {status}", font=ctk.CTkFont(size=11), text_color="#6B7280").pack(anchor="w", padx=10, pady=(0, 5))
        
        ctk.CTkButton(popup, text="Fermer", fg_color="#F59E0B", hover_color="#D97706", 
                     text_color="white", corner_radius=8, height=32, 
                     font=ctk.CTkFont(size=13, weight="bold"), 
                     command=lambda: (popup.destroy(), self.destroy())).pack(pady=10)

class AnomaliesPopup(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestion des Anomalies")
        self.geometry("600x500")
        self.resizable(True, True)
        self.minsize(500, 400)
        self.configure(fg_color="white")
        self.grab_set()
        self._drag_start_x = None
        self._drag_start_y = None
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Header
        header = ctk.CTkFrame(self, fg_color="white")
        header.pack(fill="x", pady=(16,0), padx=18)
        ctk.CTkLabel(header, text="Gestion des Anomalies", font=ctk.CTkFont(size=20, weight="bold"), text_color="#222").pack(side="left", pady=6)
        def start_move(event):
            self._drag_start_x = event.x
            self._drag_start_y = event.y
        def do_move(event):
            x = self.winfo_x() + event.x - self._drag_start_x
            y = self.winfo_y() + event.y - self._drag_start_y
            self.geometry(f"+{x}+{y}")
        header.bind("<Button-1>", start_move)
        header.bind("<B1-Motion>", do_move)

        # Main content
        content = ctk.CTkFrame(self, fg_color="white")
        content.pack(fill="both", expand=True, padx=18, pady=18)

        # Titre
        ctk.CTkLabel(content, text="Anomalies détectées", font=ctk.CTkFont(size=16, weight="bold"), text_color="#222").pack(anchor="w", pady=(0, 15))
        
        # Liste des anomalies
        anomalies_frame = ctk.CTkScrollableFrame(content, fg_color="white", height=300)
        anomalies_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        anomalies = [
            ("❗ BR-2024-045", "Retard de 2 jours", "Critique", "#FEE2E2", "#EF4444"),
            ("📦 BR-2024-042", "Colis endommagé", "Moyen", "#FEF3C7", "#F59E42"),
            ("⚖️ BR-2024-041", "Poids incorrect", "Faible", "#FEF3C7", "#F59E42"),
            ("📋 BR-2024-040", "Documentation manquante", "Faible", "#FEF3C7", "#F59E42")
        ]
        
        for anomaly, description, severity, bg_color, text_color in anomalies:
            anomaly_frame = ctk.CTkFrame(anomalies_frame, fg_color=bg_color, corner_radius=8, border_width=1, border_color=text_color)
            anomaly_frame.pack(fill="x", pady=5)
            
            # En-tête de l'anomalie
            header_frame = ctk.CTkFrame(anomaly_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=10, pady=(8, 0))
            
            ctk.CTkLabel(header_frame, text=anomaly, font=ctk.CTkFont(size=14, weight="bold"), text_color=text_color).pack(side="left")
            
            severity_badge = ctk.CTkFrame(header_frame, fg_color=text_color, corner_radius=6)
            severity_badge.pack(side="right", padx=(0, 10))
            ctk.CTkLabel(severity_badge, text=severity, font=ctk.CTkFont(size=11, weight="bold"), text_color="white").pack(padx=8, pady=2)
            
            # Description
            ctk.CTkLabel(anomaly_frame, text=description, font=ctk.CTkFont(size=12), text_color=text_color).pack(anchor="w", padx=10, pady=(5, 8))
            
            # Boutons d'action
            action_frame = ctk.CTkFrame(anomaly_frame, fg_color="transparent")
            action_frame.pack(fill="x", padx=10, pady=(0, 8))
            
            ctk.CTkButton(action_frame, text="Traiter", fg_color=text_color, hover_color="#DC2626", 
                         text_color="white", corner_radius=6, height=28, 
                         font=ctk.CTkFont(size=11, weight="bold"), 
                         command=lambda a=anomaly: self.treat_anomaly(a)).pack(side="left", padx=(0, 8))
            
            ctk.CTkButton(action_frame, text="Ignorer", fg_color="#6B7280", hover_color="#4B5563", 
                         text_color="white", corner_radius=6, height=28, 
                         font=ctk.CTkFont(size=11), 
                         command=lambda a=anomaly: self.ignore_anomaly(a)).pack(side="left")

        # Boutons d'action principaux
        btn_frame = ctk.CTkFrame(content, fg_color="white")
        btn_frame.pack(fill="x", pady=(0, 0))
        
        ctk.CTkButton(btn_frame, text="Fermer", fg_color="#EF4444", hover_color="#DC2626", 
                     text_color="white", corner_radius=12, height=44, 
                     font=ctk.CTkFont(size=16, weight="bold"), 
                     command=self.destroy).pack(side="left", expand=True, fill="x", padx=(0, 12))
        
        ctk.CTkButton(btn_frame, text="Traiter Tout", fg_color="#10B981", hover_color="#059669", 
                     text_color="white", corner_radius=12, height=44, 
                     font=ctk.CTkFont(size=16, weight="bold"), 
                     command=self.treat_all_anomalies).pack(side="left", expand=True, fill="x", padx=(12, 0))

    def treat_anomaly(self, anomaly):
        """Traite une anomalie spécifique"""
        self.show_treatment_popup(anomaly, "traité")

    def ignore_anomaly(self, anomaly):
        """Ignore une anomalie spécifique"""
        self.show_treatment_popup(anomaly, "ignoré")

    def treat_all_anomalies(self):
        """Traite toutes les anomalies"""
        self.show_treatment_popup("toutes les anomalies", "traitées")

    def show_treatment_popup(self, anomaly, action):
        """Affiche un popup de confirmation de traitement"""
        popup = ctk.CTkToplevel(self)
        popup.title("Confirmation")
        popup.geometry("300x150")
        popup.resizable(False, False)
        popup.configure(fg_color="white")
        popup.grab_set()
        
        ctk.CTkLabel(popup, text="✅", font=ctk.CTkFont(size=40), text_color="#10B981").pack(pady=(20, 0))
        ctk.CTkLabel(popup, text=f"Anomalie {action}", font=ctk.CTkFont(size=14, weight="bold"), text_color="#166534").pack(pady=(5, 0))
        ctk.CTkLabel(popup, text=f"L'anomalie '{anomaly}' a été {action} avec succès.", font=ctk.CTkFont(size=12), text_color="#6B7280").pack(pady=(5, 0))
        
        ctk.CTkButton(popup, text="OK", fg_color="#10B981", hover_color="#059669", 
                     text_color="white", corner_radius=8, height=32, 
                     font=ctk.CTkFont(size=13, weight="bold"), 
                     command=popup.destroy).pack(pady=15)

# Popup d'édition
class EditReceptionPopup(ctk.CTkToplevel):
    def __init__(self, master, row):
        super().__init__(master)
        self.title("Modifier le bon de réception")
        self.geometry("420x420")
        self.grab_set()
        self.row = row
        self.master = master
        self.build_form()

    def build_form(self):
        import database
        ctk.CTkLabel(self, text="Modifier le bon de réception", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(18,10))
        self.ref_entry = ctk.CTkEntry(self, placeholder_text="Référence", width=320)
        self.ref_entry.pack(pady=6)
        self.ref_entry.insert(0, self.row['reference'])
        self.fourn_entry = ctk.CTkEntry(self, placeholder_text="Fournisseur", width=320)
        self.fourn_entry.pack(pady=6)
        self.fourn_entry.insert(0, self.row['fournisseur'])
        self.date_entry = DateEntry(self, width=18, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(pady=6)
        if self.row['date_prevue']:
            self.date_entry.set_date(self.row['date_prevue'])
        self.obs_entry = ctk.CTkEntry(self, placeholder_text="Observation", width=320)
        self.obs_entry.pack(pady=6)
        self.obs_entry.insert(0, self.row['observation'] or "")
        ctk.CTkButton(self, text="Enregistrer", fg_color="#3B82F6", hover_color="#2563EB", text_color="white", command=self.save).pack(pady=18)
        ctk.CTkButton(self, text="Annuler", fg_color="#6B7280", hover_color="#374151", text_color="white", command=self.destroy).pack()

    def save(self):
        import database
        ref = self.ref_entry.get()
        fourn = self.fourn_entry.get()
        date_prev = self.date_entry.get_date()
        obs = self.obs_entry.get()
        success = database.update_bon_reception(self.row['id'], ref, fourn, date_prev, obs, 0, 0)
        if success:
            self.master.master.show_notification("Bon de réception modifié avec succès !")
        else:
            self.master.master.show_notification("Erreur lors de la modification !", duration=3000)
        self.master._auto_refresh()
        self.destroy()

# Popup de gestion des colis
class ColisPopup(ctk.CTkToplevel):
    def __init__(self, master, row):
        super().__init__(master)
        self.title(f"Colis pour {row['reference']}")
        self.geometry("600x400")
        self.grab_set()
        self.row = row
        self.master = master
        self.build_ui()

    def build_ui(self):
        import database
        ctk.CTkLabel(self, text=f"Colis pour {self.row['reference']}", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(18,10))
        self.colis_frame = ctk.CTkFrame(self, fg_color="white")
        self.colis_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_colis()
        ctk.CTkButton(self, text="+ Ajouter un colis", fg_color="#10B981", hover_color="#059669", text_color="white", command=self.add_colis_popup).pack(pady=8)
        ctk.CTkButton(self, text="Fermer", fg_color="#6B7280", hover_color="#374151", text_color="white", command=self.destroy).pack(pady=4)

    def refresh_colis(self):
        import database
        for widget in self.colis_frame.winfo_children():
            widget.destroy()
        # Filtrer les colis de cette réception
        all_colis = database.get_all_colis()
        colis = [c for c in all_colis if c['reception'] == self.row['id']]
        for c in colis:
            f = ctk.CTkFrame(self.colis_frame, fg_color="#F3F4F6", corner_radius=8)
            f.pack(fill="x", pady=4, padx=2)
            ctk.CTkLabel(f, text=f"Colis {c['id']} - {c['poids']}kg - {c['emplacement']}", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=8)
            ctk.CTkButton(f, text="✏️", width=30, height=28, fg_color="#F3F4F6", text_color="#6B7280", hover_color="#E0E7EF", command=lambda col=c: self.edit_colis_popup(col)).pack(side="left", padx=2)
            ctk.CTkButton(f, text="🗑️", width=30, height=28, fg_color="#FEE2E2", text_color="#EF4444", hover_color="#FCA5A5", command=lambda col=c: self.delete_colis(col)).pack(side="left", padx=2)

    def add_colis_popup(self):
        AddEditColisPopup(self, self.row['id'], None, self.refresh_colis)

    def edit_colis_popup(self, colis):
        AddEditColisPopup(self, self.row['id'], colis, self.refresh_colis)

    def delete_colis(self, colis):
        import database
        success = database.delete_colis(colis['id'])
        if success:
            self.master.master.show_notification("Colis supprimé avec succès !")
        else:
            self.master.master.show_notification("Erreur lors de la suppression du colis !", duration=3000)
        self.refresh_colis()

# Popup d'ajout/édition de colis
class AddEditColisPopup(ctk.CTkToplevel):
    def __init__(self, master, id_reception, colis=None, on_save=None):
        super().__init__(master)
        self.title("Ajouter/Modifier un colis")
        self.geometry("350x320")
        self.grab_set()
        self.id_reception = id_reception
        self.colis = colis
        self.on_save = on_save
        self.build_form()

    def build_form(self):
        import database
        ctk.CTkLabel(self, text="Colis", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(18,10))
        self.dimension_entry = ctk.CTkEntry(self, placeholder_text="Dimension", width=220)
        self.dimension_entry.pack(pady=6)
        self.poids_entry = ctk.CTkEntry(self, placeholder_text="Poids (kg)", width=220)
        self.poids_entry.pack(pady=6)
        self.emplacement_entry = ctk.CTkEntry(self, placeholder_text="Emplacement", width=220)
        self.emplacement_entry.pack(pady=6)
        if self.colis:
            self.dimension_entry.insert(0, str(self.colis['dimension']))
            self.poids_entry.insert(0, str(self.colis['poids']))
            self.emplacement_entry.insert(0, self.colis['emplacement'])
        ctk.CTkButton(self, text="Enregistrer", fg_color="#3B82F6", hover_color="#2563EB", text_color="white", command=self.save).pack(pady=18)
        ctk.CTkButton(self, text="Annuler", fg_color="#6B7280", hover_color="#374151", text_color="white", command=self.destroy).pack()

    def save(self):
        import database
        dimension = self.dimension_entry.get()
        poids = self.poids_entry.get()
        emplacement = self.emplacement_entry.get()
        if self.colis:
            success = database.update_colis(self.colis['id'], dimension, poids, emplacement)
            if success:
                self.master.master.show_notification("Colis modifié avec succès !")
            else:
                self.master.master.show_notification("Erreur lors de la modification du colis !", duration=3000)
        else:
            success = database.add_colis(self.id_reception, dimension, poids, emplacement)
            if success:
                self.master.master.show_notification("Colis ajouté avec succès !")
            else:
                self.master.master.show_notification("Erreur lors de l'ajout du colis !", duration=3000)
        if self.on_save:
            self.on_save()
        self.destroy()

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Gestion des Réceptions")
    app.geometry("1400x900")
    ctk.set_appearance_mode("light")
    frame = ReceptionFrame(app)
    app.mainloop() 