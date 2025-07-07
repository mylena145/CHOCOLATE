import customtkinter as ctk
from sidebar import SidebarFrame
from responsive_config import ResponsiveConfig
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import sqlite3
from responsive_utils import ThemeToggleButton

class PackagingFrame(ctk.CTkFrame):
    def __init__(self, master, user_info=None):
        super().__init__(master, fg_color="white")
        self.pack(fill="both", expand=True)
        if user_info is None:
            user_info = {
                'prenom': 'Utilisateur',
                'nom': 'Test',
                'role': 'Admin',
                'email': 'test@example.com',
                'matricule': '12345'
            }
        self.user_info = user_info
        self.sidebar = SidebarFrame(self, master)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.set_active_button("Emballages")
        
        # Charger les emballages depuis la base de données
        try:
            from database import get_all_emballages, add_emballage, update_emballage, delete_emballage, get_emballage_stats
            self.emballages = get_all_emballages()
            self._add_emballage_db = add_emballage
            self._update_emballage_db = update_emballage
            self._delete_emballage_db = delete_emballage
            self._get_stats_db = get_emballage_stats
        except Exception as e:
            print(f"Erreur lors du chargement des emballages depuis la base : {e}")
            self.emballages = []
            self._add_emballage_db = None
            self._update_emballage_db = None
            self._delete_emballage_db = None
            self._get_stats_db = None
        
        # Configuration responsive
        self.update_cards_data()
        
        self.create_widgets()
        
        # Lier le redimensionnement
        self.bind("<Configure>", self._on_frame_resize)
        
        # Rafraîchissement automatique toutes les 30 secondes
        self.after(30000, self.refresh_data)
    
    def update_cards_data(self):
        """Met à jour les données des cartes avec les vraies statistiques"""
        if self._get_stats_db:
            try:
                stats = self._get_stats_db()
                self.cards_data = [
                    {"title": "Emballages en cours", "value": str(stats["neuf"]), "icon": "📦", "color": "#00B8D4"},
                    {"title": "Emballages terminés", "value": str(stats["recupere"]), "icon": "✅", "color": "#43A047"},
                    {"title": "Emballages en attente", "value": "0", "icon": "⏳", "color": "#FFA000"},
                    {"title": "Emballages rejetés", "value": "0", "icon": "❌", "color": "#D32F2F"},
                    {"title": "Taux de réussite", "value": f"{stats['taux_reussite']}%", "icon": "📊", "color": "#6A1B9A"},
                    {"title": "Total emballages", "value": str(stats["total"]), "icon": "⏱️", "color": "#F4511E"}
                ]
            except Exception as e:
                print(f"Erreur lors du chargement des statistiques : {e}")
                self.cards_data = [
                    {"title": "Emballages en cours", "value": "0", "icon": "📦", "color": "#00B8D4"},
                    {"title": "Emballages terminés", "value": "0", "icon": "✅", "color": "#43A047"},
                    {"title": "Emballages en attente", "value": "0", "icon": "⏳", "color": "#FFA000"},
                    {"title": "Emballages rejetés", "value": "0", "icon": "❌", "color": "#D32F2F"},
                    {"title": "Taux de réussite", "value": "0%", "icon": "📊", "color": "#6A1B9A"},
                    {"title": "Total emballages", "value": "0", "icon": "⏱️", "color": "#F4511E"}
                ]
        else:
            self.cards_data = [
                {"title": "Emballages en cours", "value": "0", "icon": "📦", "color": "#00B8D4"},
                {"title": "Emballages terminés", "value": "0", "icon": "✅", "color": "#43A047"},
                {"title": "Emballages en attente", "value": "0", "icon": "⏳", "color": "#FFA000"},
                {"title": "Emballages rejetés", "value": "0", "icon": "❌", "color": "#D32F2F"},
                {"title": "Taux de réussite", "value": "0%", "icon": "📊", "color": "#6A1B9A"},
                {"title": "Total emballages", "value": "0", "icon": "⏱️", "color": "#F4511E"}
            ]
    
    def refresh_data(self):
        """Rafraîchit les données depuis la base"""
        try:
            from database import get_all_emballages, get_emballage_stats
            self.emballages = get_all_emballages()
            self.update_cards_data()
            self._create_cards()
            self.refresh_table()
        except Exception as e:
            print(f"Erreur lors du rafraîchissement : {e}")
        
        # Programmer le prochain rafraîchissement
        self.after(30000, self.refresh_data)
    
    def refresh_table(self):
        """Rafraîchit la table des emballages"""
        if hasattr(self, 'table_frame'):
            for widget in self.table_frame.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and widget != self.table_frame.winfo_children()[0]:
                    widget.destroy()
            self.create_table_data()
    
    def on_window_resize(self, width, height):
        """Méthode appelée quand la fenêtre est redimensionnée"""
        ResponsiveConfig.adapt_layout_to_size(self, width, height)
    
    def _on_frame_resize(self, event):
        """Gère le redimensionnement du frame"""
        if event.width > 100 and event.height > 100:
            self.on_window_resize(event.width, event.height)
    
    def create_widgets(self):
        # Contenu principal
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(side="right", fill="both", expand=True)
        
        # En-tête
        header = ctk.CTkFrame(self.main_content, fg_color="white", height=80)
        header.pack(fill="x", padx=20, pady=20)
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(header, text="📦 Gestion des Emballages", font=ctk.CTkFont(size=24, weight="bold"), text_color="#1f2937")
        title.pack(anchor="w", padx=20, pady=20)
        
        # Cartes statistiques
        cards_frame = ctk.CTkFrame(self.main_content, fg_color="white")
        cards_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.cards_frame = cards_frame
        
        # Créer les cartes avec ResponsiveConfig
        self._create_cards()
        
        # Filtres et recherche
        filters_frame = ctk.CTkFrame(self.main_content, fg_color="white", height=60)
        filters_frame.pack(fill="x", padx=20, pady=10)
        filters_frame.pack_propagate(False)
        
        # Barre de recherche
        search_frame = ctk.CTkFrame(filters_frame, fg_color="#f3f4f6", corner_radius=8)
        search_frame.pack(side="left", padx=20, pady=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Rechercher un emballage...", width=300, height=36, border_width=0, fg_color="transparent", font=ctk.CTkFont(size=14))
        self.search_entry.pack(side="left", padx=15, pady=8)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        # Filtres
        filter_frame = ctk.CTkFrame(filters_frame, fg_color="transparent")
        filter_frame.pack(side="right", padx=20, pady=10)
        
        ctk.CTkLabel(filter_frame, text="Filtrer par:", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(side="left", padx=(0, 10))
        
        self.status_filter = ctk.CTkOptionMenu(filter_frame, values=["Tous", "En cours", "Terminé", "En attente", "Rejeté"], width=120, height=36, fg_color="#ffffff", button_color="#00B8D4", button_hover_color="#0099CC", text_color="#374151", font=ctk.CTkFont(size=14), command=self.on_filter_change)
        self.status_filter.pack(side="left", padx=5)
        
        self.type_filter = ctk.CTkOptionMenu(filter_frame, values=["Tous", "Boite", "Adhesive", "Bourrage", "Autre"], width=120, height=36, fg_color="#ffffff", button_color="#00B8D4", button_hover_color="#0099CC", text_color="#374151", font=ctk.CTkFont(size=14), command=self.on_filter_change)
        self.type_filter.pack(side="left", padx=5)
        
        # Bouton d'ajout
        add_btn = ctk.CTkButton(filter_frame, text="+ Nouvel Emballage", width=140, height=36, fg_color="#00B8D4", hover_color="#0099CC", text_color="white", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, command=self.show_add_popup)
        add_btn.pack(side="left", padx=10)
        
        # Table des emballages
        table_frame = ctk.CTkFrame(self.main_content, fg_color="white", corner_radius=8)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.table_frame = table_frame
        
        # En-tête de la table
        table_header = ctk.CTkFrame(table_frame, fg_color="#f8fafc", corner_radius=8)
        table_header.pack(fill="x", padx=1, pady=1)
        
        headers = ["ID", "Type", "État", "Date création", "Responsable", "Actions"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(table_header, text=header, font=ctk.CTkFont(size=13, weight="bold"), text_color="#374151")
            label.grid(row=0, column=i, sticky="ew", padx=15, pady=12)
            table_header.grid_columnconfigure(i, weight=1)
        
        # Créer les données de la table
        self.create_table_data()
    
    def create_table_data(self):
        """Crée les données de la table depuis la base de données"""
        filtered_data = self.get_filtered_emballages()
        
        for row_idx, emballage in enumerate(filtered_data):
            row_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=1, pady=1)
            
            # ID
            ctk.CTkLabel(row_frame, text=f"EMB{emballage['id']:03d}", font=ctk.CTkFont(size=12), text_color="#6b7280").grid(row=0, column=0, sticky="ew", padx=15, pady=8)
            
            # Type
            ctk.CTkLabel(row_frame, text=emballage['type'], font=ctk.CTkFont(size=12), text_color="#6b7280").grid(row=0, column=1, sticky="ew", padx=15, pady=8)
            
            # Statut
            statut_text = "En cours" if emballage['etat'] == "Neuf" else "Terminé"
            statut_color = "#00B8D4" if emballage['etat'] == "Neuf" else "#43A047"
            ctk.CTkLabel(row_frame, text=statut_text, font=ctk.CTkFont(size=12), text_color=statut_color).grid(row=0, column=2, sticky="ew", padx=15, pady=8)
            
            # Date création
            ctk.CTkLabel(row_frame, text=emballage['date_creation'], font=ctk.CTkFont(size=12), text_color="#6b7280").grid(row=0, column=3, sticky="ew", padx=15, pady=8)
            
            # Responsable
            ctk.CTkLabel(row_frame, text=emballage['responsable'], font=ctk.CTkFont(size=12), text_color="#6b7280").grid(row=0, column=4, sticky="ew", padx=15, pady=8)
            
            # Actions
            btn_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            btn_frame.grid(row=0, column=5, sticky="ew", padx=15, pady=8)
            
            edit_btn = ctk.CTkButton(btn_frame, text="Modifier", width=60, height=28, fg_color="#00B8D4", hover_color="#0099CC", text_color="white", font=ctk.CTkFont(size=11), corner_radius=6, command=lambda e=emballage: self.edit_emballage(e))
            edit_btn.pack(side="left", padx=2)
            
            delete_btn = ctk.CTkButton(btn_frame, text="Supprimer", width=60, height=28, fg_color="#D32F2F", hover_color="#B71C1C", text_color="white", font=ctk.CTkFont(size=11), corner_radius=6, command=lambda e=emballage: self.delete_emballage(e))
            delete_btn.pack(side="left", padx=2)
            
            row_frame.grid_columnconfigure(0, weight=1)
            row_frame.grid_columnconfigure(1, weight=1)
            row_frame.grid_columnconfigure(2, weight=1)
            row_frame.grid_columnconfigure(3, weight=1)
            row_frame.grid_columnconfigure(4, weight=1)
            row_frame.grid_columnconfigure(5, weight=1)
    
    def get_filtered_emballages(self):
        """Filtre les emballages selon les critères"""
        filtered = self.emballages.copy()
        
        # Filtre par recherche
        search_term = self.search_entry.get().lower() if hasattr(self, 'search_entry') else ""
        if search_term:
            filtered = [e for e in filtered if search_term in str(e['id']).lower() or search_term in e['type'].lower() or search_term in e['etat'].lower()]
        
        # Filtre par statut
        status_filter = self.status_filter.get() if hasattr(self, 'status_filter') else "Tous"
        if status_filter != "Tous":
            if status_filter == "En cours":
                filtered = [e for e in filtered if e['etat'] == "Neuf"]
            elif status_filter == "Terminé":
                filtered = [e for e in filtered if e['etat'] == "Recupere"]
        
        # Filtre par type
        type_filter = self.type_filter.get() if hasattr(self, 'type_filter') else "Tous"
        if type_filter != "Tous":
            filtered = [e for e in filtered if e['type'] == type_filter]
        
        return filtered
    
    def on_search(self, event=None):
        """Gère la recherche"""
        self.refresh_table()
    
    def on_filter_change(self, value):
        """Gère le changement de filtre"""
        self.refresh_table()
    
    def _create_cards(self):
        """Crée les cartes avec ResponsiveConfig"""
        # Supprimer les cartes existantes
        for child in self.cards_frame.winfo_children():
            child.destroy()
        
        # Créer les nouvelles cartes
        for i, data in enumerate(self.cards_data):
            card = ResponsiveConfig._create_card(self.cards_frame, data)
            card.pack(side="left", expand=True, fill="x", padx=10)
    
    def show_add_popup(self):
        """Affiche la popup d'ajout d'emballage"""
        popup = ctk.CTkToplevel(self)
        popup.title("Nouvel Emballage")
        popup.geometry("400x350")
        popup.configure(fg_color='white')
        popup.grab_set()
        popup.resizable(False, False)
        
        ctk.CTkLabel(popup, text="Ajouter un nouvel emballage", font=ctk.CTkFont(size=18, weight="bold"), text_color="#333333").pack(pady=(20, 10))
        
        # Formulaire
        form_frame = ctk.CTkFrame(popup, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(form_frame, text="Type d'emballage:", font=ctk.CTkFont(size=14), text_color="#666666").pack(anchor="w", pady=(0, 5))
        type_menu = ctk.CTkOptionMenu(form_frame, values=["Boite", "Adhesive", "Bourrage", "Autre"], width=300, height=36, font=ctk.CTkFont(size=14))
        type_menu.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="État d'emballage:", font=ctk.CTkFont(size=14), text_color="#666666").pack(anchor="w", pady=(0, 5))
        etat_menu = ctk.CTkOptionMenu(form_frame, values=["Neuf", "Recupere"], width=300, height=36, font=ctk.CTkFont(size=14))
        etat_menu.pack(fill="x", pady=(0, 20))
        
        # Boutons
        btns = ctk.CTkFrame(popup, fg_color="transparent")
        btns.pack(pady=(0, 20))
        
        ctk.CTkButton(btns, text="Annuler", width=120, height=36, fg_color="#F3F4F6", text_color="#222", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, command=popup.destroy).pack(side="left", padx=8)
        ctk.CTkButton(btns, text="Ajouter", width=120, height=36, fg_color="#00B8D4", text_color="white", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, command=lambda: self.add_emballage_popup(type_menu.get(), etat_menu.get(), popup)).pack(side="left", padx=8)
    
    def add_emballage_popup(self, type_emballage, etat_emballage, popup):
        """Ajoute un emballage depuis la popup"""
        if self._add_emballage_db:
            try:
                new_id = self._add_emballage_db(type_emballage, etat_emballage)
                popup.destroy()
                self.refresh_data()
                # Afficher un message de succès
                self.show_notification(f"Emballage {type_emballage} ajouté avec succès!")
            except Exception as e:
                self.show_notification(f"Erreur lors de l'ajout : {e}", error=True)
        else:
            self.show_notification("Fonction d'ajout non disponible", error=True)
    
    def edit_emballage(self, emballage):
        """Édite un emballage"""
        popup = ctk.CTkToplevel(self)
        popup.title("Modifier Emballage")
        popup.geometry("400x350")
        popup.configure(fg_color='white')
        popup.grab_set()
        popup.resizable(False, False)
        
        ctk.CTkLabel(popup, text="Modifier l'emballage", font=ctk.CTkFont(size=18, weight="bold"), text_color="#333333").pack(pady=(20, 10))
        
        # Formulaire
        form_frame = ctk.CTkFrame(popup, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(form_frame, text="Type d'emballage:", font=ctk.CTkFont(size=14), text_color="#666666").pack(anchor="w", pady=(0, 5))
        type_menu = ctk.CTkOptionMenu(form_frame, values=["Boite", "Adhesive", "Bourrage", "Autre"], width=300, height=36, font=ctk.CTkFont(size=14))
        type_menu.set(emballage['type'])
        type_menu.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="État d'emballage:", font=ctk.CTkFont(size=14), text_color="#666666").pack(anchor="w", pady=(0, 5))
        etat_menu = ctk.CTkOptionMenu(form_frame, values=["Neuf", "Recupere"], width=300, height=36, font=ctk.CTkFont(size=14))
        etat_menu.set(emballage['etat'])
        etat_menu.pack(fill="x", pady=(0, 20))
        
        # Boutons
        btns = ctk.CTkFrame(popup, fg_color="transparent")
        btns.pack(pady=(0, 20))
        
        ctk.CTkButton(btns, text="Annuler", width=120, height=36, fg_color="#F3F4F6", text_color="#222", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, command=popup.destroy).pack(side="left", padx=8)
        ctk.CTkButton(btns, text="Enregistrer", width=120, height=36, fg_color="#00B8D4", text_color="white", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, command=lambda: self.update_emballage_popup(emballage['id'], type_menu.get(), etat_menu.get(), popup)).pack(side="left", padx=8)
    
    def update_emballage_popup(self, id_emballeur, type_emballage, etat_emballage, popup):
        """Met à jour un emballage depuis la popup"""
        if self._update_emballage_db:
            try:
                self._update_emballage_db(id_emballeur, type_emballage, etat_emballage)
                popup.destroy()
                self.refresh_data()
                self.show_notification(f"Emballage modifié avec succès!")
            except Exception as e:
                self.show_notification(f"Erreur lors de la modification : {e}", error=True)
        else:
            self.show_notification("Fonction de modification non disponible", error=True)
    
    def delete_emballage(self, emballage):
        """Supprime un emballage"""
        if self._delete_emballage_db:
            try:
                self._delete_emballage_db(emballage['id'])
                self.refresh_data()
                self.show_notification(f"Emballage supprimé avec succès!")
            except Exception as e:
                self.show_notification(f"Erreur lors de la suppression : {e}", error=True)
        else:
            self.show_notification("Fonction de suppression non disponible", error=True)
    
    def show_notification(self, message, error=False):
        """Affiche une notification"""
        # Créer une fenêtre de notification temporaire
        notif = ctk.CTkToplevel(self)
        notif.title("Notification")
        notif.geometry("300x100")
        notif.configure(fg_color='white')
        notif.grab_set()
        notif.resizable(False, False)
        
        color = "#D32F2F" if error else "#43A047"
        ctk.CTkLabel(notif, text=message, font=ctk.CTkFont(size=14), text_color=color).pack(expand=True)
        
        # Fermer automatiquement après 3 secondes
        notif.after(3000, notif.destroy)

    def apply_theme(self, theme):
        """Applique le thème à la page des emballages"""
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
            
            print(f"Thème appliqué à la page Emballages: {theme}")
            
        except Exception as e:
            print(f"Erreur lors de l'application du thème à la page Emballages: {e}")

    def _build_topbar(self):
        topbar = ctk.CTkFrame(self.main_content, fg_color="white", height=70)
        topbar.pack(fill="x", pady=(18, 0), padx=24)
        topbar.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(topbar, text="Gestion des Emballages", font=ctk.CTkFont(size=22, weight="bold"), text_color="#222")
        title.grid(row=0, column=0, sticky="w", pady=(8,0))
        
        subtitle = ctk.CTkLabel(topbar, text="Packaging et conditionnement", font=ctk.CTkFont(size=14), text_color="#666")
        subtitle.grid(row=1, column=0, sticky="w")
        
        # Bouton de thème
        self.theme_button = ThemeToggleButton(topbar, self.parent)
        self.theme_button.grid(row=0, column=1, rowspan=2, sticky="e", padx=(0,20))
        
        btn = ctk.CTkButton(topbar, text="📦 Nouvel Emballage", fg_color="#3b82f6", hover_color="#2563eb", text_color="white", corner_radius=8, font=ctk.CTkFont(size=14, weight="bold"), width=150, height=36, command=self._open_packaging_modal)
        btn.grid(row=0, column=2, rowspan=2, sticky="e", padx=(0,20)) 