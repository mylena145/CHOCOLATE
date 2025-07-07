import customtkinter as ctk
from PIL import Image
from sidebar import SidebarFrame
from CTkToolTip import CTkToolTip
import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt
from responsive_utils import ThemeToggleButton

class StockManagementFrame(ctk.CTkFrame):
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
        self.sidebar = SidebarFrame(self, master)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.set_active_button("Stocks")
        
        # Lier le redimensionnement
        self.bind("<Configure>", self._on_frame_resize)
        
        self.main_content = ctk.CTkFrame(self, fg_color="white")
        self.main_content.pack(side="right", fill="both", expand=True)
        
        self.active_stock_filter = "Tous"
        self.search_term = ""

        # Pagination
        self.current_page = 1
        self.items_per_page = 10
        
        # Charger les produits depuis la base de données
        try:
            from database import get_all_products, add_product, update_product, delete_product as db_delete_product
            self.products = get_all_products()
            self._add_product_db = add_product
            self._update_product_db = update_product
            self._delete_product_db = db_delete_product
        except Exception as e:
            print(f"Erreur lors du chargement des produits depuis la base : {e}")
            self.products = []
            self._add_product_db = None
            self._update_product_db = None
            self._delete_product_db = None
        
        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self._build_topbar()
        self.create_summary_cards(main_frame)
        self.create_filter_bar(main_frame)
        self.product_list_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.product_list_container.pack(fill="both", expand=True)
        self.refresh_product_list()

    def _build_topbar(self):
        topbar = ctk.CTkFrame(self.main_content, fg_color="white", height=70)
        topbar.pack(fill="x", pady=(18, 0), padx=24)
        topbar.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(topbar, text="Gestion des Stocks", font=ctk.CTkFont(size=22, weight="bold"), text_color="#222")
        title.grid(row=0, column=0, sticky="w", pady=(8,0))
        
        subtitle = ctk.CTkLabel(topbar, text="Inventaire et gestion des produits", font=ctk.CTkFont(size=14), text_color="#666")
        subtitle.grid(row=1, column=0, sticky="w")
        
        # Bouton de thème
        self.theme_button = ThemeToggleButton(topbar, self.parent)
        self.theme_button.grid(row=0, column=1, rowspan=2, sticky="e", padx=(0,20))
        
        btn = ctk.CTkButton(topbar, text="➕ Ajouter Produit", fg_color="#3b82f6", hover_color="#2563eb", text_color="white", corner_radius=8, font=ctk.CTkFont(size=14, weight="bold"), width=150, height=36, command=self._open_add_product_modal)
        btn.grid(row=0, column=2, rowspan=2, sticky="e", padx=(0,20))

    def open_export_popup(self):
        ExportPopup(self)

    def create_summary_cards(self, parent):
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))

        cards_data = [
            {"icon": "📦", "title": "Total Produits", "value": "1,247", "subtitle": "+5% ce mois", "subtitle_color": "#059669", "icon_bg": "#D1FAE5"},
            {"icon": "🧊", "title": "Lots Actifs", "value": "342", "subtitle": "En stock", "subtitle_color": "#6B7280", "icon_bg": "#DBEAFE"},
            {"icon": "⚠️", "title": "Stock Critique", "value": "12", "subtitle": "À réapprovisionner", "subtitle_color": "#DC2626", "icon_bg": "#FEE2E2"},
            {"icon": "💶", "title": "Valeur Stock", "value": "2 400 000 FCFA", "subtitle": "Total estimé", "subtitle_color": "#6B7280", "icon_bg": "#FEF3C7"}
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
            
            ctk.CTkLabel(top_frame, text=card_data["title"], font=ctk.CTkFont(size=15, weight="bold"), text_color="#374151").pack(side="left", anchor="center")

            ctk.CTkLabel(card_content, text=card_data["value"], font=ctk.CTkFont(size=32, weight="bold"), text_color="#111827").pack(anchor="w", pady=(10, 2))
            
            ctk.CTkLabel(card_content, text=card_data["subtitle"], font=ctk.CTkFont(size=13), text_color=card_data["subtitle_color"]).pack(anchor="w")

    def create_filter_bar(self, parent):
        filter_frame = ctk.CTkFrame(parent, fg_color="white", height=80, corner_radius=10, border_width=1, border_color="#E5E7EB")
        filter_frame.pack(fill="x", pady=(0, 20))
        filter_frame.pack_propagate(False)

        left_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=15, pady=15)

        search_container = ctk.CTkFrame(left_frame, fg_color="#F3F4F6", corner_radius=8)
        search_container.pack(side="left")

        ctk.CTkLabel(search_container, text="🔍", font=ctk.CTkFont(size=16), text_color="#6B7280").pack(side="left", padx=(10, 5))

        self.search_entry = ctk.CTkEntry(
            search_container, 
            placeholder_text="Rechercher...",
            fg_color="transparent",
            border_width=0,
            width=200,
            text_color="#111827"
        )
        self.search_entry.pack(side="left", padx=(0, 10), pady=5)
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        filter_buttons = ["Tous", "Stock Critique", "Stock Faible", "En Stock"]
        self.filter_btns = []
        for i, text in enumerate(filter_buttons):
            is_active = (text == self.active_stock_filter)
            btn = ctk.CTkButton(
                left_frame,
                text=text,
                fg_color="#3B82F6" if is_active else "transparent",
                text_color="white" if is_active else "#374151",
                border_color="#D1D5DB",
                border_width=0 if is_active else 1,
                hover_color="#2563EB" if is_active else "#F9FAFB",
                height=30,
                corner_radius=8,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda t=text: self.set_stock_filter(t)
            )
            btn.pack(side="left", padx=5)
            self.filter_btns.append(btn)

        right_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=15, pady=15)

        categories = ["Toutes catégories", "Électronique", "Mobilier", "Fournitures"]
        category_menu = ctk.CTkOptionMenu(
            right_frame, 
            values=categories,
            fg_color="#F3F4F6",
            text_color="#374151",
            button_color="#E5E7EB",
            button_hover_color="#D1D5DB",
            dropdown_fg_color="#F3F4F6",
            dropdown_text_color="#374151",
            corner_radius=8,
            height=30
        )
        category_menu.pack(side="left", padx=5)

        marques = ["Toutes marques", "Dell", "HP", "Samsung", "Logitech"]
        marque_menu = ctk.CTkOptionMenu(
            right_frame, 
            values=marques,
            fg_color="#F3F4F6",
            text_color="#374151",
            button_color="#E5E7EB",
            button_hover_color="#D1D5DB",
            dropdown_fg_color="#F3F4F6",
            dropdown_text_color="#374151",
            corner_radius=8,
            height=30
        )
        marque_menu.pack(side="left", padx=5)

    def _on_search(self, event):
        self.search_term = self.search_entry.get()
        self.current_page = 1
        self.refresh_product_list()

    def set_stock_filter(self, filter_name):
        self.active_stock_filter = filter_name
        self.current_page = 1 
        for btn in self.filter_btns:
            is_active = (btn.cget("text") == filter_name)
            btn.configure(
                fg_color="#3B82F6" if is_active else "transparent",
                text_color="white" if is_active else "#374151",
                border_width=0 if is_active else 1,
                hover_color="#2563EB" if is_active else "#F9FAFB"
            )
        self.refresh_product_list()

    def get_filtered_products(self):
        products = self.products

        if self.active_stock_filter == "Stock Critique":
            products = [p for p in products if p["status"] == "Critique"]
        elif self.active_stock_filter == "Stock Faible":
            products = [p for p in products if p["status"] == "Faible"]
        elif self.active_stock_filter == "En Stock":
             products = [p for p in products if p["status"] == "Normal"]

        if self.search_term:
            term = self.search_term.lower()
            products = [
                p for p in products if
                term in p['name'].lower() or
                term in p['code'].lower() or
                term in p['brand'].lower() or
                term in p['sub'].lower()
            ]
        
        return products

    def refresh_product_list(self):
        for widget in self.product_list_container.winfo_children():
            widget.destroy()
        self.create_product_list(self.product_list_container)

    def create_product_list(self, parent):
        product_list_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        product_list_frame.pack(fill="both", expand=True, pady=(0, 20))

        list_header_frame = ctk.CTkFrame(product_list_frame, fg_color="transparent")
        list_header_frame.pack(fill="x", padx=20, pady=(15,10))
        ctk.CTkLabel(list_header_frame, text="Liste des Produits", font=ctk.CTkFont(size=18, weight="bold"), text_color="#111827").pack(side="left")
        
        table_container = ctk.CTkFrame(product_list_frame, fg_color="transparent")
        table_container.pack(fill="both", expand=True, padx=20)

        table_header = ctk.CTkFrame(table_container, fg_color="#F9FAFB", height=45)
        table_header.pack(fill="x")
        table_header.grid_propagate(False)

        headers = ["PRODUIT", "RÉFÉRENCE", "MARQUE", "STOCK", "EMPLACEMENT", "STATUT", "ACTIONS"]
        column_weights = [4, 3, 2, 1, 2, 2, 2] 

        for i, (header, weight) in enumerate(zip(headers, column_weights)):
            table_header.grid_columnconfigure(i, weight=weight)
            cell = ctk.CTkFrame(table_header, fg_color="transparent")
            cell.grid(row=0, column=i, sticky="nsew")
            ctk.CTkLabel(cell, text=header, font=ctk.CTkFont(size=12, weight="bold"), text_color="#6B7280").pack(side="left", padx=10)

        scrollable_body = ctk.CTkScrollableFrame(table_container, fg_color="white", corner_radius=0)
        scrollable_body.pack(fill="both", expand=True)

        for i, weight in enumerate(column_weights):
            scrollable_body.grid_columnconfigure(i, weight=weight)

        all_products = self.get_filtered_products()
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        products_to_display = all_products[start_index:end_index]
        
        status_colors = {
            "Critique": ("#FEE2E2", "#DC2626"),
            "Faible": ("#FEF3C7", "#D97706"),
            "Normal": ("#D1FAE5", "#059669")
        }

        for i, product in enumerate(products_to_display):
            
            if i > 0:
                ctk.CTkFrame(scrollable_body, height=1, fg_color="#E5E7EB").grid(row=i*2 - 1, column=0, columnspan=len(headers), sticky="ew")

            cell_product = ctk.CTkFrame(scrollable_body, fg_color="transparent")
            ctk.CTkLabel(cell_product, text=product["name"], font=ctk.CTkFont(size=14, weight="bold"), text_color="#111827").pack(anchor="w")
            ctk.CTkLabel(cell_product, text=product["code"], font=ctk.CTkFont(size=12), text_color="#6B7280").pack(anchor="w")
            cell_product.grid(row=i*2, column=0, sticky="w", padx=10, pady=15)
            
            ctk.CTkLabel(scrollable_body, text=product["sub"], font=ctk.CTkFont(size=13), text_color="#111827").grid(row=i*2, column=1, sticky="w", padx=10)
            ctk.CTkLabel(scrollable_body, text=product["brand"], font=ctk.CTkFont(size=13), text_color="#111827").grid(row=i*2, column=2, sticky="w", padx=10)

            cell_stock = ctk.CTkFrame(scrollable_body, fg_color="transparent")
            ctk.CTkLabel(cell_stock, text=str(product["stock"]), font=ctk.CTkFont(size=14, weight="bold"), text_color="#111827").pack(anchor="w")
            ctk.CTkLabel(cell_stock, text=f"Seuil: {product['alert']}", font=ctk.CTkFont(size=11), text_color="#6B7280").pack(anchor="w")
            cell_stock.grid(row=i*2, column=3, sticky="w", padx=10)

            ctk.CTkLabel(scrollable_body, text=product["loc"], font=ctk.CTkFont(size=13), text_color="#111827").grid(row=i*2, column=4, sticky="w", padx=10)

            status_color_bg, status_color_text = status_colors.get(product["status"], ("#E5E7EB", "#374151"))
            status_badge = ctk.CTkLabel(scrollable_body, text=product["status"], font=ctk.CTkFont(size=12, weight="bold"), fg_color=status_color_bg, text_color=status_color_text, corner_radius=10, width=80, height=24)
            status_badge.grid(row=i*2, column=5, sticky="w", padx=10)

            cell_actions = ctk.CTkFrame(scrollable_body, fg_color="transparent")
            edit_button = ctk.CTkButton(cell_actions, text="✏️", width=30, height=30, fg_color="transparent", text_color="#6B7280", hover_color="#F3F4F6", command=lambda p_id=product['id']: self.open_edit_product_popup(p_id))
            edit_button.pack(side="left")
            CTkToolTip(edit_button, "Modifier le produit")

            delete_button = ctk.CTkButton(cell_actions, text="🗑️", width=30, height=30, fg_color="transparent", text_color="#6B7280", hover_color="#FEE2E2", command=lambda p_id=product['id']: self.delete_product(p_id))
            delete_button.pack(side="left")
            CTkToolTip(delete_button, "Supprimer le produit")
            cell_actions.grid(row=i*2, column=6, sticky="w", padx=10)

        footer_frame = ctk.CTkFrame(product_list_frame, fg_color="transparent", height=50)
        footer_frame.pack(fill="x", padx=20, pady=(5,10), side="bottom")
        footer_frame.pack_propagate(False)
        
        self.pagination_label = ctk.CTkLabel(footer_frame, text="", font=ctk.CTkFont(size=12), text_color="#6B7280")
        self.pagination_label.pack(side="left")
        
        pagination_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        pagination_frame.pack(side="right")

        self.prev_button = ctk.CTkButton(pagination_frame, text="< Précédent", fg_color="white", hover_color="#F9FAFB", text_color="#374151", border_width=1, border_color="#D1D5DB", corner_radius=6, height=34, font=ctk.CTkFont(size=12, weight="bold"), command=self.prev_page)
        self.prev_button.pack(side="left")
        
        self.next_button = ctk.CTkButton(pagination_frame, text="Suivant >", fg_color="white", hover_color="#F9FAFB", text_color="#374151", border_width=1, border_color="#D1D5DB", corner_radius=6, height=34, font=ctk.CTkFont(size=12, weight="bold"), command=self.next_page)
        self.next_button.pack(side="left", padx=8)

        self._update_pagination_controls()

    def _update_pagination_controls(self):
        filtered_products = self.get_filtered_products()
        total_items = len(filtered_products)
        start_item = (self.current_page - 1) * self.items_per_page + 1
        end_item = min(self.current_page * self.items_per_page, total_items)
        
        if total_items == 0:
             self.pagination_label.configure(text="Aucun produit à afficher")
        else:
            self.pagination_label.configure(text=f"Affichage de {start_item} à {end_item} sur {total_items} entrées")

        self.prev_button.configure(state="normal" if self.current_page > 1 else "disabled")
        self.next_button.configure(state="normal" if end_item < total_items else "disabled")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_product_list()

    def next_page(self):
        filtered_products = self.get_filtered_products()
        total_items = len(filtered_products)
        if self.current_page * self.items_per_page < total_items:
            self.current_page += 1
            self.refresh_product_list()

    def delete_product(self, product_id):
        # Suppression en base
        if self._delete_product_db:
            self._delete_product_db(product_id)
        # Recharger la liste depuis la base
        self.products = self._reload_products()
        self.refresh_product_list()

    def _reload_products(self):
        try:
            from database import get_all_products
            return get_all_products()
        except Exception as e:
            print(f"Erreur lors du rechargement des produits : {e}")
            return []
            
    def open_edit_product_popup(self, product_id):
        product_data = next((p for p in self.products if p["id"] == product_id), None)
        if product_data:
            popup = EditProductPopup(self, product_data)
            self.wait_window(popup)
            self.refresh_product_list()

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
            self._adapt_layout_to_size(event.width, event.height)

    def apply_theme(self, theme):
        """Applique le thème à la page de gestion des stocks"""
        try:
            is_dark = theme == "dark"
            
            # Couleurs adaptatives
            bg_color = "#1a1a1a" if is_dark else "#f7fafd"
            card_bg = "#2d2d2d" if is_dark else "white"
            text_color = "#ffffff" if is_dark else "#222222"
            secondary_text = "#cccccc" if is_dark else "#666666"
            border_color = "#555555" if is_dark else "#e0e0e0"
            table_bg = "#3d3d3d" if is_dark else "#f9fafb"
            table_header_bg = "#4d4d4d" if is_dark else "#f3f4f6"
            
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
            
            print(f"Thème appliqué à la page Stocks: {theme}")
            
        except Exception as e:
            print(f"Erreur lors de l'application du thème à la page Stocks: {e}")

class EditProductPopup(ctk.CTkToplevel):
    def __init__(self, master, product_data):
        super().__init__(master)
        self.master = master
        self.product_data = product_data

        self.title("Modifier le Produit")
        self.geometry("600x600")
        self.resizable(False, False)
        self.configure(fg_color="white")
        self.grab_set()

        # ... (Le contenu du popup de modification)
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text=f"Modifier: {self.product_data['name']}", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w")

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20)

        ctk.CTkLabel(form_frame, text="Nom du produit *", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        self.nom_entry = ctk.CTkEntry(form_frame, height=38)
        self.nom_entry.pack(fill="x", pady=(0, 10))
        self.nom_entry.insert(0, self.product_data['name'])

        row_stock = ctk.CTkFrame(form_frame, fg_color="transparent")
        row_stock.pack(fill="x", expand=True)
        
        stock_frame = ctk.CTkFrame(row_stock, fg_color="transparent")
        stock_frame.pack(side="left", expand=True, fill="x", padx=(0,10))
        ctk.CTkLabel(stock_frame, text="Quantité en stock *").pack(anchor="w")
        self.stock_entry = ctk.CTkEntry(stock_frame, height=38)
        self.stock_entry.pack(fill="x")
        self.stock_entry.insert(0, str(self.product_data['stock']))
        
        seuil_frame = ctk.CTkFrame(row_stock, fg_color="transparent")
        seuil_frame.pack(side="left", expand=True, fill="x", padx=(10,0))
        ctk.CTkLabel(seuil_frame, text="Seuil d'alerte *").pack(anchor="w")
        self.seuil_entry = ctk.CTkEntry(seuil_frame, height=38)
        self.seuil_entry.pack(fill="x")
        self.seuil_entry.insert(0, str(self.product_data['alert']))
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(btn_frame, text="Enregistrer les modifications", command=self.save_changes, height=40, font=ctk.CTkFont(size=14, weight="bold")).pack(side="right")
        ctk.CTkButton(btn_frame, text="Annuler", command=self.destroy, height=40, fg_color="#E5E7EB", text_color="#374151", hover_color="#D1D5DB").pack(side="right", padx=10)

    def save_changes(self):
        new_nom = self.nom_entry.get()
        new_stock = self.stock_entry.get()
        new_seuil = self.seuil_entry.get()
        # Mise à jour en base
        if hasattr(self.master, '_update_product_db') and self.master._update_product_db:
            product_data = self.product_data.copy()
            product_data["name"] = new_nom
            product_data["stock"] = int(new_stock)
            product_data["alert"] = int(new_seuil)
            self.master._update_product_db(product_data["id"], product_data)
        # Recharger la liste depuis la base
        self.master.products = self.master._reload_products()
        self.master.refresh_product_list()
        self.destroy()

class BasePopup(ctk.CTkToplevel):
    """Une classe de base pour les popups."""
    def __init__(self, master, title, geometry):
        super().__init__(master)
        self.master = master
        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self.configure(fg_color="white")
        self.grab_set()

        self.content_frame = ctk.CTkFrame(self, fg_color="white")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=15)

    def show_success_popup(self, message):
        popup = ctk.CTkToplevel(self)
        popup.title("Succès")
        popup.geometry("340x160")
        popup.resizable(False, False)
        popup.configure(fg_color="#f0fdf4")
        popup.grab_set()
        ctk.CTkLabel(popup, text="✅", font=ctk.CTkFont(size=48), text_color="#22c55e").pack(pady=(20,0))
        ctk.CTkLabel(popup, text=message, font=ctk.CTkFont(size=16, weight="bold"), text_color="#166534").pack(pady=(5,0))
        ctk.CTkButton(popup, text="OK", fg_color="#22c55e", hover_color="#16a34a", text_color="white", corner_radius=8, height=36, font=ctk.CTkFont(size=14, weight="bold"), command=lambda: (popup.destroy(), self.destroy())).pack(pady=18)

class AddProductPopup(BasePopup):
    def __init__(self, master=None):
        super().__init__(master, title="Ajouter un Nouveau Produit", geometry="600x550")
        self.master = master
        self.create_form()

    def create_form(self):
        # Ligne 0 : ID Produit (optionnel)
        row0 = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        row0.pack(fill="x", pady=(0, 15))
        self.create_entry_group(row0, "id_entry", "ID Produit (optionnel)", "", side="left")

        # Ligne 1: Nom et Code Produit
        row1 = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 15))
        self.create_entry_group(row1, "nom_entry", "Nom du Produit *", "Souris Optique Dell", side="left")
        self.create_entry_group(row1, "code_entry", "Code Produit *", "DELL-MS116", side="right")

        # Ligne 2: Marque et Référence
        row2 = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 15))
        self.create_entry_group(row2, "brand_entry", "Marque *", "Dell", side="left")
        self.create_entry_group(row2, "sub_entry", "Référence/Modèle *", "MS116", side="right")

        # Ligne 3: Stock et Seuil d'alerte
        row3 = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        row3.pack(fill="x", pady=(0, 15))
        self.create_entry_group(row3, "stock_entry", "Stock Initial *", "50", side="left")
        self.create_entry_group(row3, "alert_entry", "Seuil d'Alerte *", "10", side="right")

        # Ligne 4: Emplacement et Fournisseur
        row4 = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        row4.pack(fill="x", pady=(0, 15))
        self.create_entry_group(row4, "loc_entry", "Emplacement de Stockage *", "E0-A1-01", side="left")
        self.create_entry_group(row4, "fournisseur_entry", "Fournisseur", "Inconnu", side="right")

        # Ligne 5: Description
        row5 = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        row5.pack(fill="x", pady=(0, 15))
        self.create_entry_group(row5, "description_entry", "Description", "Aucune description", side="left")

        # Ligne 6: Dates
        row6 = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        row6.pack(fill="x", pady=(0, 15))
        self.create_entry_group(row6, "date_fabrique_entry", "Date de fabrication (YYYY-MM-DD)", "", side="left")
        self.create_entry_group(row6, "date_peremption_entry", "Date de péremption (YYYY-MM-DD)", "", side="right")

        # Boutons
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0), side="bottom")
        ctk.CTkButton(btn_frame, text="Annuler", command=self.confirm_cancel, height=40, fg_color="#EF5350", text_color="white", hover_color="#E53935", corner_radius=8, font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", expand=True, padx=(0, 5))
        ctk.CTkButton(btn_frame, text="+ Ajouter le Produit", command=self.validate_and_add_product, height=40, fg_color="#F59E0B", hover_color="#D97706", corner_radius=8, font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", expand=True, padx=(5, 0))

    def confirm_cancel(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmation d'annulation")
        dialog.geometry("370x180")
        dialog.configure(fg_color='white')
        dialog.grab_set()
        dialog.resizable(False, False)
        
        ctk.CTkLabel(dialog, text="Voulez-vous vraiment annuler ?", font=ctk.CTkFont(size=16, weight='bold'), text_color='#333333').pack(pady=(28,8), padx=20)
        ctk.CTkLabel(dialog, text="Toutes les informations saisies seront perdues.", font=ctk.CTkFont(size=13), text_color='#666666').pack(pady=(0,10), padx=20)
        
        btn_dialog_frame = ctk.CTkFrame(dialog, fg_color='transparent')
        btn_dialog_frame.pack(pady=(0,18))
        
        ctk.CTkButton(btn_dialog_frame, text='Oui, annuler', width=140, height=38, fg_color='#EF5350', hover_color='#E53935', text_color='white', corner_radius=8, font=ctk.CTkFont(size=14, weight='bold'), command=lambda: (dialog.destroy(), self.destroy())).pack(side='left', padx=12)
        ctk.CTkButton(btn_dialog_frame, text='Non, rester', width=120, height=38, fg_color='#90A4AE', hover_color='#78909C', text_color='white', corner_radius=8, font=ctk.CTkFont(size=14), command=dialog.destroy).pack(side='left', padx=12)

    def create_entry_group(self, parent, entry_name, label_text, placeholder, side):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(side=side, expand=True, fill="x", padx=5 if side=="right" else (0,5))
        
        label = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(size=13, weight="bold"), text_color="#374151")
        label.pack(anchor="w", pady=(0, 4))
        
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder, fg_color="#F3F4F6", text_color="#111827", border_width=1, border_color="#D1D5DB", height=38, corner_radius=8)
        entry.pack(fill="x")
        setattr(self, entry_name, entry)
        
        error_label = ctk.CTkLabel(frame, text="", text_color="#DC2626", font=ctk.CTkFont(size=12))
        error_label.pack(anchor="w", pady=(2,0))
        setattr(self, f"{entry_name}_error", error_label)

    def validate_and_add_product(self):
        # Récupérer les valeurs du formulaire
        id_value = self.id_entry.get().strip()
        description = self.description_entry.get().strip() if hasattr(self, 'description_entry') else "Aucune description"
        fournisseur = self.fournisseur_entry.get().strip() if hasattr(self, 'fournisseur_entry') else "Inconnu"
        date_fabrique = self.date_fabrique_entry.get().strip() if hasattr(self, 'date_fabrique_entry') else None
        date_peremption = self.date_peremption_entry.get().strip() if hasattr(self, 'date_peremption_entry') else None
        product_data = {
            "id": int(id_value) if id_value else None,
            "name": self.nom_entry.get(),
            "code": self.code_entry.get(),
            "brand": self.brand_entry.get(),
            "sub": self.sub_entry.get(),
            "stock": int(self.stock_entry.get()),
            "alert": int(self.alert_entry.get()),
            "loc": self.loc_entry.get(),
            "description": description if description else "Aucune description",
            "date_fabrique": date_fabrique if date_fabrique else None,
            "date_peremption": date_peremption if date_peremption else None,
            "fournisseur": fournisseur if fournisseur else "Inconnu"
        }
        # Ajout en base
        if hasattr(self.master, '_add_product_db') and self.master._add_product_db:
            # Si id_produit est renseigné, on l'inclut dans la requête (il faudra adapter add_product si besoin)
            if product_data["id"] is not None:
                from database import psycopg2, PG_CONN
                conn = psycopg2.connect(**PG_CONN)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO sge_cre.produits (id_produit, nom, description, marque, modele, fournisseur, date_fabrique, date_peremption, stock, alert)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    product_data["id"],
                    product_data["name"],
                    product_data["description"],
                    product_data["brand"],
                    product_data["sub"],
                    product_data["fournisseur"],
                    product_data["date_fabrique"],
                    product_data["date_peremption"],
                    product_data["stock"],
                    product_data["alert"]
                ))
                conn.commit()
                conn.close()
            else:
                self.master._add_product_db(product_data)
        # Recharger la liste depuis la base
        self.master.products = self.master._reload_products()
        self.master.refresh_product_list()
        self.show_success_popup("Produit ajouté avec succès !")
        # Réinitialisation des erreurs
        for entry_name in ["nom_entry", "code_entry", "brand_entry", "sub_entry", "stock_entry", "alert_entry", "loc_entry"]:
            getattr(self, f"{entry_name}_error").configure(text="")

        is_valid = True
        
        def check_field(entry, error_label, name, is_numeric=False):
            nonlocal is_valid
            value = entry.get()
            if not value:
                error_label.configure(text=f"{name} requis")
                is_valid = False
            elif is_numeric and not value.isdigit():
                error_label.configure(text="Doit être un nombre")
                is_valid = False
            return value

        name = check_field(self.nom_entry, self.nom_entry_error, "Nom")
        code = check_field(self.code_entry, self.code_entry_error, "Code")
        brand = check_field(self.brand_entry, self.brand_entry_error, "Marque")
        sub = check_field(self.sub_entry, self.sub_entry_error, "Référence")
        stock = check_field(self.stock_entry, self.stock_entry_error, "Stock", is_numeric=True)
        alert = check_field(self.alert_entry, self.alert_entry_error, "Seuil", is_numeric=True)
        loc = check_field(self.loc_entry, self.loc_entry_error, "Emplacement")
        
        if not is_valid: return

        new_id = max(p['id'] for p in self.master.products) + 1 if self.master.products else 1
        new_product = {
            "id": new_id, "code": code, "name": name, "sub": sub, "brand": brand,
            "stock": int(stock), "alert": int(alert), "loc": loc, "status": "Normal"
        }
        
        if new_product["stock"] <= new_product["alert"]: new_product["status"] = "Critique"
        elif new_product["stock"] <= new_product["alert"] * 1.5: new_product["status"] = "Faible"

        self.master.products.append(new_product)
        self.master.refresh_product_list()
        self.show_success_popup("Produit ajouté !")


class AddLotPopup(BasePopup):
    def __init__(self, master=None):
        super().__init__(master, "Ajouter un Nouveau Lot", geometry="600x520")
        self.master = master
        self.create_form()

    def create_form(self):
        # Ligne 1: Produit
        product_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        product_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(product_frame, text="Produit Associé *", font=ctk.CTkFont(size=13, weight="bold"), text_color="#374151").pack(anchor="w", pady=(0, 4))
        
        product_names = [p["name"] for p in self.master.products]
        self.product_menu = ctk.CTkOptionMenu(product_frame, values=["Sélectionner un produit"] + product_names, fg_color="#F3F4F6", text_color="#111827", button_color="#E5E7EB", button_hover_color="#D1D5DB", dropdown_fg_color="#F3F4F6", dropdown_text_color="#111827", height=38, corner_radius=8)
        self.product_menu.pack(fill="x")
        self.product_error = ctk.CTkLabel(product_frame, text="", text_color="#DC2626", font=ctk.CTkFont(size=12))
        self.product_error.pack(anchor="w", pady=(2,0))

        # Ligne 2: Numéro de lot et Quantité
        row2 = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 15))
        self.create_entry_group(row2, "lot_entry", "Numéro de Lot *", "LOT-2024-001", side="left")
        self.create_entry_group(row2, "quantity_entry", "Quantité *", "100", side="right")

        # Ligne 3: Date de péremption et Emplacement
        row3 = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        row3.pack(fill="x", pady=(0, 15))
        self.create_entry_group(row3, "expiry_entry", "Date de Péremption", "JJ/MM/AAAA", side="left")
        self.create_entry_group(row3, "loc_entry", "Emplacement", self.master.products[0]['loc'] if self.master.products else 'E0-A0-00', side="right")

        # Boutons
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0), side="bottom")
        ctk.CTkButton(btn_frame, text="Annuler", command=self.destroy, height=40, fg_color="#E5E7EB", text_color="#374151", hover_color="#D1D5DB", corner_radius=8, font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", expand=True, padx=(0, 5))
        ctk.CTkButton(btn_frame, text="🗃️ Créer le Lot", command=self.validate_and_add_lot, height=40, corner_radius=8, font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", expand=True, padx=(5, 0))
    
    def create_entry_group(self, parent, entry_name, label_text, placeholder, side):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(side=side, expand=True, fill="x", padx=5 if side=="right" else (0,5))
        label = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(size=13, weight="bold"), text_color="#374151")
        label.pack(anchor="w", pady=(0, 4))
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder, fg_color="#F3F4F6", text_color="#111827", border_width=1, border_color="#D1D5DB", height=38, corner_radius=8)
        entry.pack(fill="x")
        setattr(self, entry_name, entry)
        error_label = ctk.CTkLabel(frame, text="", text_color="#DC2626", font=ctk.CTkFont(size=12))
        error_label.pack(anchor="w", pady=(2,0))
        setattr(self, f"{entry_name}_error", error_label)
        
    def validate_and_add_lot(self):
        self.product_error.configure(text="")
        self.lot_entry_error.configure(text="")
        self.quantity_entry_error.configure(text="")
        
        is_valid = True
        
        selected_product_name = self.product_menu.get()
        if selected_product_name == "Sélectionner un produit":
            self.product_error.configure(text="Veuillez sélectionner un produit")
            is_valid = False

        lot_number = self.lot_entry.get()
        if not lot_number:
            self.lot_entry_error.configure(text="Numéro de lot requis")
            is_valid = False
            
        quantity = self.quantity_entry.get()
        if not quantity:
            self.quantity_entry_error.configure(text="Quantité requise")
            is_valid = False
        elif not quantity.isdigit() or int(quantity) <= 0:
            self.quantity_entry_error.configure(text="Quantité invalide")
            is_valid = False

        if not is_valid:
            return

        # Mettre à jour le stock du produit
        for product in self.master.products:
            if product["name"] == selected_product_name:
                product["stock"] += int(quantity)
                # Mettre à jour le statut
                if product["stock"] <= product["alert"]:
                    product["status"] = "Critique"
                elif product["stock"] <= product["alert"] * 1.5:
                    product["status"] = "Faible"
                else:
                    product["status"] = "Normal"
                break
        
        self.master.refresh_product_list()
        self.show_success_popup("Lot ajouté avec succès!")

class ExportPopup(BasePopup):
    def __init__(self, master):
        super().__init__(master, "Exporter les Données", geometry="450x380")
        self.master = master
        self.create_form()

    def create_form(self):
        # ---- Choix du contenu ----
        ctk.CTkLabel(self.content_frame, text="1. Choisissez le contenu à exporter :", font=ctk.CTkFont(size=13, weight="bold"), text_color="#374151").pack(anchor="w")
        
        self.export_option = ctk.StringVar(value="current")
        
        current_view_count = len(self.master.get_filtered_products())
        total_count = len(self.master.products)

        ctk.CTkRadioButton(self.content_frame, text=f"Vue actuelle ({current_view_count} produits)", variable=self.export_option, value="current", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(5, 2))
        ctk.CTkRadioButton(self.content_frame, text=f"La totalité du stock ({total_count} produits)", variable=self.export_option, value="all", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=10, pady=(2, 15))

        # ---- Choix du format ----
        ctk.CTkLabel(self.content_frame, text="2. Choisissez le format d'export :", font=ctk.CTkFont(size=13, weight="bold"), text_color="#374151").pack(anchor="w")
        
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))

        ctk.CTkButton(btn_frame, text="Exporter en CSV", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#3B82F6", hover_color="#2563EB", command=lambda: self.export_data('csv')).pack(side="top", fill="x", pady=4, ipady=5)
        ctk.CTkButton(btn_frame, text="Exporter en Excel", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#10B981", hover_color="#059669", command=lambda: self.export_data('excel')).pack(side="top", fill="x", pady=4, ipady=5)
        ctk.CTkButton(btn_frame, text="Exporter en PDF", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#EF4444", hover_color="#DC2626", command=lambda: self.export_data('pdf')).pack(side="top", fill="x", pady=4, ipady=5)


    def export_data(self, file_format):
        if self.export_option.get() == "current":
            products_to_export = self.master.get_filtered_products()
        else:
            products_to_export = self.master.products
        
        if not products_to_export:
            # Gérer le cas où il n'y a rien à exporter
            return

        df = pd.DataFrame(products_to_export)
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=f".{file_format}",
            filetypes=[(f"{file_format.upper()} files", f"*.{file_format}"), ("All files", "*.*")]
        )
        if not save_path:
            return

        try:
            if file_format == 'csv':
                df.to_csv(save_path, index=False)
            elif file_format == 'excel':
                df.to_excel(save_path, index=False)
            elif file_format == 'pdf':
                fig, ax = plt.subplots(figsize=(12, 4))
                ax.axis('tight')
                ax.axis('off')
                the_table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
                fig.savefig(save_path)
                
            self.show_success_popup("Exportation réussie !")
        except Exception as e:
            # Gérer les erreurs d'exportation
            print(f"Erreur d'exportation: {e}")
        
        self.destroy()

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Gestion des Stocks")
    app.geometry("1400x900")
    ctk.set_appearance_mode("light")
    
    # This will be replaced by the main app logic
    user_info = {
        'prenom': 'Utilisateur',
        'nom': 'Test',
        'role': 'Admin',
        'email': 'test@example.com',
        'matricule': '12345'
    }

    stock_frame = StockManagementFrame(app, user_info)
    
    def confirm_exit():
        dialog = ctk.CTkToplevel(app)
        dialog.title("Quitter l'application")
        dialog.geometry("370x180")
        dialog.configure(fg_color='white')
        dialog.grab_set()
        dialog.resizable(False, False)
        ctk.CTkLabel(dialog, text="Voulez-vous vraiment quitter l'application ?", font=ctk.CTkFont(size=16, weight='bold'), text_color='#333333').pack(pady=(28,8), padx=20)
        ctk.CTkLabel(dialog, text="Toutes les modifications non enregistrées seront perdues.", font=ctk.CTkFont(size=13), text_color='#666666').pack(pady=(0,10), padx=20)
        btn_frame = ctk.CTkFrame(dialog, fg_color='transparent')
        btn_frame.pack(pady=(0,18))
        def quit_app():
            app.destroy()
        ctk.CTkButton(btn_frame, text='Oui, quitter', width=140, height=38, fg_color='#EF5350', hover_color='#E53935', text_color='white', corner_radius=8, font=ctk.CTkFont(size=14, weight='bold'), command=quit_app).pack(side='left', padx=12)
        ctk.CTkButton(btn_frame, text='Non, rester', width=120, height=38, fg_color='#90A4AE', hover_color='#78909C', text_color='white', corner_radius=8, font=ctk.CTkFont(size=14), command=dialog.destroy).pack(side='left', padx=12)

    app.protocol("WM_DELETE_WINDOW", confirm_exit)
    app.mainloop() 