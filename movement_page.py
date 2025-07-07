import customtkinter as ctk
import tkinter as tk
from sidebar import SidebarFrame
import datetime
from CTkToolTip import CTkToolTip
import psycopg2
from tkinter import messagebox
from responsive_utils import ThemeToggleButton

# Paramètres de connexion PostgreSQL
PG_CONN = dict(
    dbname="postgres",
    user="postgres",
    password="postgres123",
    host="localhost",
    port="5432",
    client_encoding="utf8",
    options="-c client_encoding=utf8",
    connect_timeout=10
)

class MovementsFrame(ctk.CTkFrame):
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
        self.parent = master
        
        # Variables
        self.current_filter = "Tous"
        self.current_page = 1
        self.items_per_page = 10
        
        # Sidebar
        self.sidebar = SidebarFrame(self, master)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.set_active_button("Mouvements")
        
        # Contenu principal
        self.main_content = ctk.CTkFrame(self, fg_color="white")
        self.main_content.pack(side="right", fill="both", expand=True)
        
        # Construire l'interface
        self._build_topbar()
        self.create_widgets()
        self.init_database()
        
    def _build_topbar(self):
        topbar = ctk.CTkFrame(self.main_content, fg_color="white", height=70)
        topbar.pack(fill="x", pady=(18, 0), padx=24)
        topbar.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(topbar, text="Mouvements de Stock", font=ctk.CTkFont(size=22, weight="bold"), text_color="#222")
        title.grid(row=0, column=0, sticky="w", pady=(8,0))
        
        subtitle = ctk.CTkLabel(topbar, text="Transferts et déplacements internes", font=ctk.CTkFont(size=14), text_color="#666")
        subtitle.grid(row=1, column=0, sticky="w")
        
        # Bouton de thème
        self.theme_button = ThemeToggleButton(topbar, self.parent)
        self.theme_button.grid(row=0, column=1, rowspan=2, sticky="e", padx=(0,20))
        
        btn = ctk.CTkButton(topbar, text="🔄 Nouveau Mouvement", fg_color="#3b82f6", hover_color="#2563eb", text_color="white", corner_radius=8, font=ctk.CTkFont(size=14, weight="bold"), width=160, height=36, command=self._open_movement_modal)
        btn.grid(row=0, column=2, rowspan=2, sticky="e", padx=(0,20))

    def init_database(self):
        """Initialise la table des mouvements si elle n'existe pas"""
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sge_cre.mouvements (
                id SERIAL PRIMARY KEY,
                type TEXT NOT NULL,
                produit_id INTEGER,
                produit_nom TEXT NOT NULL,
                quantite INTEGER NOT NULL,
                reference TEXT,
                origine TEXT,
                destination TEXT,
                responsable TEXT NOT NULL,
                date_mouvement TIMESTAMP NOT NULL,
                commentaire TEXT,
                statut TEXT DEFAULT 'Complété'
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_widgets(self):
        # Header
        self._create_header()
        
        # Cartes de statistiques
        self._create_stats_cards()
        
        # Barre de filtres
        self._create_filter_bar()
        
        # Tableau des mouvements
        self._create_movements_table()

    def _create_header(self):
        """Crée le header comme les autres pages"""
        header_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", anchor="w", padx=20)

        ctk.CTkLabel(
            title_frame, 
            text="Mouvements de Stock", 
            font=ctk.CTkFont(size=24, weight="bold"), 
            text_color="#212224"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame, 
            text="Traçabilité complète des entrées et sorties", 
            font=ctk.CTkFont(size=14), 
            text_color="#6B7280"
        ).pack(anchor="w")

        # Boutons d'action
        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=20)
        
        # Bouton Nouvelle Entrée
        entry_btn = ctk.CTkButton(
            buttons_frame, 
            text="📥 Nouvelle Entrée",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#10B981",
            hover_color="#059669",
            text_color="white",
            corner_radius=8,
            height=36,
            command=lambda: self._open_movement_modal("Entrée")
        )
        entry_btn.pack(side="left", padx=5)

        # Bouton Nouvelle Sortie
        exit_btn = ctk.CTkButton(
            buttons_frame, 
            text="📤 Nouvelle Sortie",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="white",
            corner_radius=8,
            height=36,
            command=lambda: self._open_movement_modal("Sortie")
        )
        exit_btn.pack(side="left", padx=5)

        # Bouton Export
        export_btn = ctk.CTkButton(
            buttons_frame, 
            text="⬇️ Exporter",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            text_color="white",
            corner_radius=8,
            height=36,
            command=self._export_movements
        )
        export_btn.pack(side="left", padx=5)

    def _create_stats_cards(self):
        """Crée les cartes de statistiques dans le style de l'app"""
        cards_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20), padx=20)

        cards_data = [
            {
                "icon": "📥", 
                "title": "Entrées du jour", 
                "value": str(self._get_today_movements("Entrée")), 
                "subtitle": "+12% vs hier", 
                "subtitle_color": "#059669", 
                "icon_bg": "#D1FAE5"
            },
            {
                "icon": "📤", 
                "title": "Sorties du jour", 
                "value": str(self._get_today_movements("Sortie")), 
                "subtitle": "-5% vs hier", 
                "subtitle_color": "#DC2626", 
                "icon_bg": "#FEE2E2"
            },
            {
                "icon": "📊", 
                "title": "Total Semaine", 
                "value": str(self._get_total_movements()), 
                "subtitle": "Tous mouvements", 
                "subtitle_color": "#6B7280", 
                "icon_bg": "#DBEAFE"
            },
            {
                "icon": "💰", 
                "title": "Valeur Déplacée", 
                "value": "2.4M", 
                "devise": "FCFA", 
                "subtitle": "+22% ce mois", 
                "subtitle_color": "#6B7280", 
                "icon_bg": "#FEF3C7"
            }
        ]

        for card_data in cards_data:
            card = ctk.CTkFrame(cards_frame, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
            card.pack(side="left", expand=True, fill="x", padx=10)
            
            card_content = ctk.CTkFrame(card, fg_color="transparent")
            card_content.pack(padx=15, pady=15, expand=True, fill="x")

            top_frame = ctk.CTkFrame(card_content, fg_color="transparent")
            top_frame.pack(fill="x")

            icon_frame = ctk.CTkFrame(top_frame, fg_color=card_data["icon_bg"], width=40, height=40, corner_radius=8)
            icon_frame.pack(side="left", padx=(0, 10))
            icon_frame.pack_propagate(False)

            ctk.CTkLabel(
                icon_frame, 
                text=card_data["icon"], 
                font=ctk.CTkFont(size=22),
                text_color="#212224"
            ).pack(expand=True)
            
            ctk.CTkLabel(
                top_frame, 
                text=card_data["title"], 
                font=ctk.CTkFont(size=15, weight="bold"), 
                text_color="#374151"
            ).pack(side="left", anchor="center")

            value_frame = ctk.CTkFrame(card_content, fg_color="transparent")
            value_frame.pack(anchor="w", pady=(10, 2))
            
            ctk.CTkLabel(
                value_frame, 
                text=card_data["value"], 
                font=ctk.CTkFont(size=32, weight="bold"), 
                text_color="#111827"
            ).pack(side="left")
            
            if "devise" in card_data:
                ctk.CTkLabel(
                    value_frame, 
                    text=card_data["devise"], 
                    font=ctk.CTkFont(size=20, weight="bold"), 
                    text_color="#16a34a"
                ).pack(side="left", padx=(8,0))
            
            ctk.CTkLabel(
                card_content, 
                text=card_data["subtitle"], 
                font=ctk.CTkFont(size=13), 
                text_color=card_data["subtitle_color"]
            ).pack(anchor="w")

    def _create_filter_bar(self):
        """Crée la barre de filtres dans le style de l'app"""
        filter_frame = ctk.CTkFrame(self.main_content, fg_color="white", height=60, corner_radius=10, border_width=1, border_color="#E5E7EB")
        filter_frame.pack(fill="x", padx=20, pady=(0, 20))
        filter_frame.pack_propagate(False)

        left_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=15, pady=15)

        # Recherche
        search_container = ctk.CTkFrame(left_frame, fg_color="#F3F4F6", corner_radius=8)
        search_container.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(search_container, text="🔍", font=ctk.CTkFont(size=16), text_color="#6B7280").pack(side="left", padx=(10, 5))

        self.search_entry = ctk.CTkEntry(
            search_container, 
            placeholder_text="Rechercher...",
            fg_color="transparent",
            border_width=0,
            width=250,
            text_color="#111827"
        )
        self.search_entry.pack(side="left", padx=(0, 10), pady=5)
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Filtres
        self.filter_btns = []
        filter_buttons = ["Tous", "Entrées", "Sorties", "Aujourd'hui"]
        
        for text in filter_buttons:
            is_active = (text == self.current_filter)
            btn = ctk.CTkButton(
                left_frame,
                text=text,
                fg_color="#9C27B0" if is_active else "transparent",
                text_color="white" if is_active else "#374151",
                border_color="#D1D5DB",
                border_width=0 if is_active else 1,
                hover_color="#7B1FA2" if is_active else "#F9FAFB",
                height=30,
                corner_radius=8,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda t=text: self._set_filter(t)
            )
            btn.pack(side="left", padx=5)
            self.filter_btns.append(btn)

        # Sélecteur de période
        right_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=15, pady=15)

        period_menu = ctk.CTkOptionMenu(
            right_frame, 
            values=["Cette semaine", "Ce mois", "Ce trimestre", "Cette année"],
            fg_color="#F3F4F6",
            text_color="#374151",
            button_color="#E5E7EB",
            button_hover_color="#D1D5DB",
            dropdown_fg_color="#F3F4F6",
            dropdown_text_color="#374151",
            corner_radius=8,
            height=30
        )
        period_menu.pack(side="left", padx=5)

    def _create_movements_table(self):
        """Crée le tableau des mouvements"""
        # Container principal
        table_frame = ctk.CTkFrame(self.main_content, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Header
        table_header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        table_header_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            table_header_frame, 
            text="Historique des Mouvements", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            text_color="#111827"
        ).pack(side="left")
        
        # Container scrollable
        self.table_scroll = ctk.CTkScrollableFrame(table_frame, fg_color="transparent")
        self.table_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self._refresh_movements_table()

    def _refresh_movements_table(self):
        """Rafraîchit le tableau des mouvements"""
        # Nettoyer le tableau
        for widget in self.table_scroll.winfo_children():
            widget.destroy()
        
        # En-tête du tableau
        header_frame = ctk.CTkFrame(self.table_scroll, fg_color="#F9FAFB", height=45)
        header_frame.pack(fill="x", pady=(0, 5))
        header_frame.grid_propagate(False)
        
        headers = ["TYPE", "DATE/HEURE", "PRODUIT", "QTÉ", "RÉFÉRENCE", "ORIG/DEST", "RESPONSABLE", "STATUT"]
        column_weights = [1, 2, 3, 1, 2, 2, 2, 1]
        
        for i, (header, weight) in enumerate(zip(headers, column_weights)):
            header_frame.grid_columnconfigure(i, weight=weight)
            cell = ctk.CTkFrame(header_frame, fg_color="transparent")
            cell.grid(row=0, column=i, sticky="nsew", padx=5)
            ctk.CTkLabel(
                cell, 
                text=header, 
                font=ctk.CTkFont(size=12, weight="bold"), 
                text_color="#6B7280"
            ).pack(side="left", padx=10)
        
        # Récupérer et afficher les mouvements
        movements = self._get_movements()
        
        if not movements:
            # Message si aucun mouvement
            empty_frame = ctk.CTkFrame(self.table_scroll, fg_color="#F9FAFB", corner_radius=8)
            empty_frame.pack(fill="x", pady=50)
            
            ctk.CTkLabel(
                empty_frame,
                text="📦",
                font=ctk.CTkFont(size=48),
                text_color="#CBD5E1"
            ).pack(pady=(20, 10))
            
            ctk.CTkLabel(
                empty_frame,
                text="Aucun mouvement enregistré",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#64748B"
            ).pack()
            
            ctk.CTkLabel(
                empty_frame,
                text="Commencez par créer une entrée ou une sortie",
                font=ctk.CTkFont(size=14),
                text_color="#94A3B8"
            ).pack(pady=(5, 20))
        else:
            # Afficher les mouvements
            for idx, movement in enumerate(movements):
                self._create_movement_row(idx, movement)
        
        # Pagination
        if movements:
            self._create_pagination_footer()

    def _create_movement_row(self, idx, movement):
        """Crée une ligne de mouvement"""
        row_frame = ctk.CTkFrame(
            self.table_scroll,
            fg_color="white" if idx % 2 == 0 else "#F9FAFB",
            height=60
        )
        row_frame.pack(fill="x", pady=1)
        row_frame.grid_propagate(False)
        
        # Configurer les colonnes
        column_weights = [1, 2, 3, 1, 2, 2, 2, 1]
        for i, weight in enumerate(column_weights):
            row_frame.grid_columnconfigure(i, weight=weight)
        
        # Type avec badge coloré
        type_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        type_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=10)
        
        type_color = "#10B981" if movement["type"] == "Entrée" else "#EF4444"
        type_bg = "#D1FAE5" if movement["type"] == "Entrée" else "#FEE2E2"
        type_icon = "📥" if movement["type"] == "Entrée" else "📤"
        
        type_badge = ctk.CTkLabel(
            type_frame,
            text=f"{type_icon} {movement['type']}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=type_color,
            fg_color=type_bg,
            corner_radius=6,
            padx=8,
            pady=4
        )
        type_badge.pack(anchor="w", padx=10)
        
        # Date/Heure
        date_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        date_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        ctk.CTkLabel(
            date_frame,
            text=movement["date"],
            font=ctk.CTkFont(size=12),
            text_color="#374151"
        ).pack(anchor="w", padx=10)
        
        # Produit
        product_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        product_frame.grid(row=0, column=2, sticky="nsew", padx=5)
        ctk.CTkLabel(
            product_frame,
            text=movement["produit"],
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#111827"
        ).pack(anchor="w", padx=10)
        
        # Quantité
        qty_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        qty_frame.grid(row=0, column=3, sticky="nsew", padx=5)
        ctk.CTkLabel(
            qty_frame,
            text=str(movement["quantite"]),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#111827"
        ).pack(padx=10)
        
        # Référence
        ref_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        ref_frame.grid(row=0, column=4, sticky="nsew", padx=5)
        ctk.CTkLabel(
            ref_frame,
            text=movement.get("reference", "-"),
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        ).pack(anchor="w", padx=10)
        
        # Origine/Destination
        loc_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        loc_frame.grid(row=0, column=5, sticky="nsew", padx=5)
        location = movement.get("origine" if movement["type"] == "Entrée" else "destination", "-")
        ctk.CTkLabel(
            loc_frame,
            text=location,
            font=ctk.CTkFont(size=12),
            text_color="#374151"
        ).pack(anchor="w", padx=10)
        
        # Responsable
        resp_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        resp_frame.grid(row=0, column=6, sticky="nsew", padx=5)
        ctk.CTkLabel(
            resp_frame,
            text=movement["responsable"],
            font=ctk.CTkFont(size=12),
            text_color="#374151"
        ).pack(anchor="w", padx=10)
        
        # Statut
        status_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        status_frame.grid(row=0, column=7, sticky="nsew", padx=5)
        
        status = movement.get("statut", "Complété")
        status_color = "#059669" if status == "Complété" else "#D97706"
        
        ctk.CTkLabel(
            status_frame,
            text=status,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=status_color
        ).pack(padx=10)

    def _create_pagination_footer(self):
        """Crée le footer de pagination"""
        footer_frame = ctk.CTkFrame(self.table_scroll, fg_color="transparent", height=50)
        footer_frame.pack(fill="x", pady=(10, 0))
        
        # Info pagination
        ctk.CTkLabel(
            footer_frame,
            text=f"Affichage de 1 à {self.items_per_page} sur {self._get_total_movements()} entrées",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        ).pack(side="left", padx=10)
        
        # Boutons pagination
        pagination_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        pagination_frame.pack(side="right", padx=10)
        
        ctk.CTkButton(
            pagination_frame,
            text="< Précédent",
            fg_color="white",
            hover_color="#F9FAFB",
            text_color="#374151",
            border_width=1,
            border_color="#D1D5DB",
            corner_radius=6,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold"),
            state="disabled" if self.current_page == 1 else "normal"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            pagination_frame,
            text="Suivant >",
            fg_color="white",
            hover_color="#F9FAFB",
            text_color="#374151",
            border_width=1,
            border_color="#D1D5DB",
            corner_radius=6,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=5)

    def _set_filter(self, filter_name):
        """Change le filtre actuel"""
        self.current_filter = filter_name
        for btn in self.filter_btns:
            is_active = (btn.cget("text") == filter_name)
            btn.configure(
                fg_color="#9C27B0" if is_active else "transparent",
                text_color="white" if is_active else "#374151",
                border_width=0 if is_active else 1,
                hover_color="#7B1FA2" if is_active else "#F9FAFB"
            )
        self._refresh_movements_table()

    def _on_search(self, event):
        """Gère la recherche"""
        self._refresh_movements_table()

    def _open_movement_modal(self, movement_type):
        """Ouvre la fenêtre de création de mouvement"""
        MovementModal(self, movement_type)

    def _export_movements(self):
        """Exporte les mouvements"""
        messagebox.showinfo("Export", "Fonctionnalité d'export en cours de développement")

    # Méthodes de données
    def _get_today_movements(self, movement_type):
        """Récupère le nombre de mouvements du jour"""
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "SELECT COUNT(*) FROM mouvements WHERE type = %s AND date(date_mouvement) = date(%s)",
            (movement_type, today)
        )
        count = cursor.fetchone()[0]
        
        conn.close()
        return count

    def _get_total_movements(self):
        """Récupère le nombre total de mouvements"""
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM sge_cre.mouvements")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count

    def _get_movements(self):
        """Récupère les mouvements selon les filtres"""
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        query = "SELECT * FROM mouvements WHERE 1=1"
        params = []
        
        # Appliquer les filtres
        if self.current_filter == "Entrées":
            query += " AND type = %s"
            params.append("Entrée")
        elif self.current_filter == "Sorties":
            query += " AND type = %s"
            params.append("Sortie")
        elif self.current_filter == "Aujourd'hui":
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            query += " AND date(date_mouvement) = date(%s)"
            params.append(today)
        
        # Recherche
        search_term = self.search_entry.get() if hasattr(self, 'search_entry') else ""
        if search_term:
            query += " AND (produit_nom LIKE %s OR reference LIKE %s OR responsable LIKE %s)"
            search_param = f"%{search_term}%"
            params.extend([search_param, search_param, search_param])
        
        query += " ORDER BY date_mouvement DESC LIMIT %s OFFSET %s"
        params.extend([self.items_per_page, (self.current_page - 1) * self.items_per_page])
        
        cursor.execute(query, params)
        columns = [description[0] for description in cursor.description]
        movements = []
        
        for row in cursor.fetchall():
            movement = dict(zip(columns, row))
            movement["produit"] = movement["produit_nom"]
            movement["quantite"] = movement["quantite"]
            
            # Formater la date
            try:
                dt = datetime.datetime.strptime(movement["date_mouvement"], "%Y-%m-%d %H:%M:%S")
                movement["date"] = dt.strftime("%d/%m/%Y %H:%M")
            except:
                movement["date"] = movement["date_mouvement"]
            
            movements.append(movement)
        
        conn.close()
        return movements

    def apply_theme(self, theme):
        """Applique le thème à la page des mouvements"""
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
            
            print(f"Thème appliqué à la page Mouvements: {theme}")
            
        except Exception as e:
            print(f"Erreur lors de l'application du thème à la page Mouvements: {e}")


class MovementModal(ctk.CTkToplevel):
    """Fenêtre modale pour créer un mouvement"""
    def __init__(self, parent, movement_type):
        super().__init__(parent)
        self.parent = parent
        self.movement_type = movement_type
        
        # Configuration de la fenêtre
        self.title(f"Nouveau Mouvement - {movement_type}")
        self.geometry("600x700")
        self.configure(fg_color="white")
        
        # Centrer la fenêtre
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"600x700+{x}+{y}")
        
        # Modal
        self.transient(parent)
        self.grab_set()
        
        self.create_content()
        
    def create_content(self):
        """Crée le contenu de la modale"""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        icon = "📥" if self.movement_type == "Entrée" else "📤"
        color = "#10B981" if self.movement_type == "Entrée" else "#EF4444"
        
        ctk.CTkLabel(
            header,
            text=f"{icon} Nouvelle {self.movement_type}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=color
        ).pack(side="left")
        
        # Formulaire
        form_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Sélection du produit
        ctk.CTkLabel(
            form_frame,
            text="Produit *",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        products = self._get_products_list()
        self.product_var = tk.StringVar()
        self.product_menu = ctk.CTkOptionMenu(
            form_frame,
            values=products,
            variable=self.product_var,
            fg_color="#F3F4F6",
            button_color="#E5E7EB",
            button_hover_color="#D1D5DB",
            dropdown_fg_color="#F3F4F6",
            dropdown_text_color="#111827",
            corner_radius=8,
            height=38,
            font=ctk.CTkFont(size=14),
            command=self._on_product_selected
        )
        self.product_menu.pack(fill="x", pady=(0, 15))
        
        # Stock actuel (info)
        self.stock_info_frame = ctk.CTkFrame(form_frame, fg_color="#F0FDF4", corner_radius=8)
        self.stock_info_frame.pack(fill="x", pady=(0, 15))
        
        stock_content = ctk.CTkFrame(self.stock_info_frame, fg_color="transparent")
        stock_content.pack(padx=15, pady=10)
        
        ctk.CTkLabel(
            stock_content,
            text="Stock actuel:",
            font=ctk.CTkFont(size=12),
            text_color="#166534"
        ).pack(side="left")
        
        self.stock_label = ctk.CTkLabel(
            stock_content,
            text="-- unités",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#166534"
        )
        self.stock_label.pack(side="left", padx=(10, 0))
        
        # Quantité
        ctk.CTkLabel(
            form_frame,
            text="Quantité *",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.quantity_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Entrez la quantité",
            fg_color="#F3F4F6",
            border_width=0,
            corner_radius=8,
            height=38,
            font=ctk.CTkFont(size=14)
        )
        self.quantity_entry.pack(fill="x", pady=(0, 15))
        
        # Référence
        ctk.CTkLabel(
            form_frame,
            text="Référence du bon",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.reference_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text=f"Ex: {'BE' if self.movement_type == 'Entrée' else 'BS'}-2024-001",
            fg_color="#F3F4F6",
            border_width=0,
            corner_radius=8,
            height=38,
            font=ctk.CTkFont(size=14)
        )
        self.reference_entry.pack(fill="x", pady=(0, 15))
        
        # Origine/Destination
        location_label = "Origine" if self.movement_type == "Entrée" else "Destination"
        ctk.CTkLabel(
            form_frame,
            text=f"{location_label} *",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.location_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text=f"{location_label} du mouvement",
            fg_color="#F3F4F6",
            border_width=0,
            corner_radius=8,
            height=38,
            font=ctk.CTkFont(size=14)
        )
        self.location_entry.pack(fill="x", pady=(0, 15))
        
        # Commentaire
        ctk.CTkLabel(
            form_frame,
            text="Commentaire",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#374151"
        ).pack(anchor="w", pady=(0, 5))
        
        self.comment_text = ctk.CTkTextbox(
            form_frame,
            fg_color="#F3F4F6",
            border_width=0,
            corner_radius=8,
            height=80,
            font=ctk.CTkFont(size=14)
        )
        self.comment_text.pack(fill="x", pady=(0, 20))
        
        # Responsable (info)
        resp_frame = ctk.CTkFrame(form_frame, fg_color="#F3F4F6", corner_radius=8)
        resp_frame.pack(fill="x", pady=(0, 20))
        
        resp_content = ctk.CTkFrame(resp_frame, fg_color="transparent")
        resp_content.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            resp_content,
            text="Responsable:",
            font=ctk.CTkFont(size=12),
            text_color="#6B7280"
        ).pack(side="left")
        
        user_name = f"{self.parent.user_info['prenom']} {self.parent.user_info['nom']}"
        ctk.CTkLabel(
            resp_content,
            text=user_name,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#111827"
        ).pack(side="left", padx=(10, 0))
        
        # Boutons d'action
        button_frame = ctk.CTkFrame(self, fg_color="white", height=70)
        button_frame.pack(fill="x", side="bottom")
        button_frame.pack_propagate(False)
        
        button_content = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_content.pack(expand=True)
        
        # Bouton Annuler
        cancel_btn = ctk.CTkButton(
            button_content,
            text="Annuler",
            fg_color="#E5E7EB",
            hover_color="#D1D5DB",
            text_color="#374151",
            corner_radius=8,
            height=38,
            width=120,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.destroy
        )
        cancel_btn.pack(side="left", padx=10)
        
        # Bouton Valider
        validate_color = "#10B981" if self.movement_type == "Entrée" else "#EF4444"
        validate_hover = "#059669" if self.movement_type == "Entrée" else "#DC2626"
        
        validate_btn = ctk.CTkButton(
            button_content,
            text=f"Valider la {self.movement_type}",
            fg_color=validate_color,
            hover_color=validate_hover,
            text_color="white",
            corner_radius=8,
            height=38,
            width=180,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._validate_movement
        )
        validate_btn.pack(side="left", padx=10)
        
    def _get_products_list(self):
        """Récupère la liste des produits depuis la base"""
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        cursor.execute("SELECT code, name FROM products ORDER BY name")
        products = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        
        conn.close()
        
        # Si pas de produits, utiliser une liste de test
        if not products:
            products = [
                "DELL-MS116-001 - Souris optique Dell",
                "HP-K120-001 - Clavier USB HP",
                "SAMSUNG-24-001 - Moniteur Full HD",
                "DELL-LAPTOP-001 - Dell Latitude 7420"
            ]
        
        return products
    
    def _on_product_selected(self, choice):
        """Gère la sélection d'un produit"""
        # Extraire le code produit
        product_code = choice.split(" - ")[0]
        
        # Récupérer le stock actuel
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        cursor.execute("SELECT stock FROM sge_cre.products WHERE code = %s", (product_code,))
        result = cursor.fetchone()
        
        if result:
            stock = result[0]
        else:
            stock = 100  # Valeur par défaut
        
        conn.close()
        
        self.stock_label.configure(text=f"{stock} unités")
        
    def _validate_movement(self):
        """Valide et enregistre le mouvement"""
        # Récupérer les valeurs
        product = self.product_var.get()
        quantity = self.quantity_entry.get()
        reference = self.reference_entry.get()
        location = self.location_entry.get()
        comment = self.comment_text.get("1.0", "end-1c")
        
        # Validation
        if not product or product == "":
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit")
            return
            
        if not quantity or not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Erreur", "Veuillez entrer une quantité valide")
            return
            
        if not location:
            messagebox.showerror("Erreur", f"Veuillez entrer {'l\'origine' if self.movement_type == 'Entrée' else 'la destination'}")
            return
        
        # Enregistrer le mouvement
        try:
            conn = psycopg2.connect(**PG_CONN)
            cursor = conn.cursor()
            
            # Extraire le nom du produit
            product_name = product.split(" - ")[1] if " - " in product else product
            
            cursor.execute("""
                INSERT INTO mouvements (
                    type, produit_nom, quantite, reference, 
                    origine, destination, responsable, 
                    date_mouvement, commentaire
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                self.movement_type,
                product_name,
                int(quantity),
                reference or f"AUTO-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                location if self.movement_type == "Entrée" else None,
                location if self.movement_type == "Sortie" else None,
                f"{self.parent.user_info['prenom']} {self.parent.user_info['nom']}",
                datetime.datetime.now(),
                comment
            ))
            
            # Mettre à jour le stock si table products existe
            try:
                product_code = product.split(" - ")[0]
                if self.movement_type == "Entrée":
                    cursor.execute("UPDATE sge_cre.products SET stock = stock + %s WHERE code = %s", (int(quantity), product_code))
                else:
                    cursor.execute("UPDATE sge_cre.products SET stock = stock - %s WHERE code = %s", (int(quantity), product_code))
            except:
                pass
            
            conn.commit()
            conn.close()
            
            # Afficher le succès
            self._show_success()
            
            # Rafraîchir le tableau parent
            self.parent._refresh_movements_table()
            
            # Fermer la modale après un délai
            self.after(1500, self.destroy)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement : {str(e)}")
    
    def _show_success(self):
        """Affiche un message de succès"""
        # Frame de succès
        success_frame = ctk.CTkFrame(self, fg_color="#10B981", corner_radius=0)
        success_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Contenu
        content = ctk.CTkFrame(success_frame, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Icône
        ctk.CTkLabel(
            content,
            text="✅",
            font=ctk.CTkFont(size=72),
            text_color="white"
        ).pack()
        
        # Message
        ctk.CTkLabel(
            content,
            text=f"{self.movement_type} enregistrée avec succès !",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=(20, 0))