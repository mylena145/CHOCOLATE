import customtkinter as ctk

class ResponsiveConfig:
    """Configuration responsive pour l'application"""
    
    @staticmethod
    def get_config(width):
        """Retourne la configuration selon la largeur de l'écran"""
        if width < 768:
            return {
                'sidebar_width': 200,
                'card_columns': 1,
                'table_compact': True,
                'font_size_small': 10,
                'font_size_normal': 12,
                'font_size_large': 16,
                'padding_small': 8,
                'padding_normal': 12,
                'padding_large': 16
            }
        elif width < 1024:
            return {
                'sidebar_width': 220,
                'card_columns': 2,
                'table_compact': False,
                'font_size_small': 11,
                'font_size_normal': 13,
                'font_size_large': 18,
                'padding_small': 10,
                'padding_normal': 15,
                'padding_large': 20
            }
        elif width < 1400:
            return {
                'sidebar_width': 240,
                'card_columns': 3,
                'table_compact': False,
                'font_size_small': 12,
                'font_size_normal': 14,
                'font_size_large': 20,
                'padding_small': 12,
                'padding_normal': 18,
                'padding_large': 24
            }
        else:
            return {
                'sidebar_width': 260,
                'card_columns': 4,
                'table_compact': False,
                'font_size_small': 13,
                'font_size_normal': 15,
                'font_size_large': 22,
                'padding_small': 15,
                'padding_normal': 20,
                'padding_large': 28
            }
    
    @staticmethod
    def create_responsive_cards(parent, cards_data, columns=3):
        """Crée des cartes responsive"""
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configurer la grille
        for i in range(columns):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        # Créer les cartes
        for i, data in enumerate(cards_data):
            card = ResponsiveConfig._create_card(cards_frame, data)
            row = i // columns
            col = i % columns
            card.grid(row=row, column=col, sticky="ew", padx=10, pady=5)
        
        return cards_frame
    
    @staticmethod
    def _create_card(parent, data):
        """Crée une carte individuelle"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        
        # Icône
        icon_frame = ctk.CTkFrame(card, fg_color=data.get("color", "#00B8D4"), width=40, height=40, corner_radius=8)
        icon_frame.pack(pady=(10, 0))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text=data.get("icon", "📦"), font=ctk.CTkFont(size=22), text_color="white").pack(expand=True)
        
        # Titre
        ctk.CTkLabel(card, text=data.get("title", ""), font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(pady=(8, 0))
        
        # Valeur
        ctk.CTkLabel(card, text=data.get("value", ""), font=ctk.CTkFont(size=28, weight="bold"), text_color="#111827").pack()
        
        # Sous-titre (optionnel)
        if "subtitle" in data:
            ctk.CTkLabel(card, text=data["subtitle"], font=ctk.CTkFont(size=12), text_color=data.get("subtitle_color", "#6B7280")).pack(pady=(0, 10))
        
        return card
    
    @staticmethod
    def adapt_layout_to_size(widget, width, height):
        """Adapte la mise en page d'un widget selon la taille"""
        if hasattr(widget, 'cards_frame'):
            # Adapter les colonnes selon la largeur
            if width < 1200:
                columns = 2
            elif width < 1600:
                columns = 3
            else:
                columns = 4
            
            # Recréer les cartes avec la nouvelle disposition
            ResponsiveConfig._recreate_cards(widget, columns)
    
    @staticmethod
    def _recreate_cards(widget, columns):
        """Recrée les cartes avec une nouvelle disposition"""
        if hasattr(widget, 'cards_frame') and hasattr(widget, 'cards_data'):
            # Supprimer les cartes existantes
            for child in widget.cards_frame.winfo_children():
                child.destroy()
            
            # Recréer les cartes
            for i, data in enumerate(widget.cards_data):
                card = ResponsiveConfig._create_card(widget.cards_frame, data)
                row = i // columns
                col = i % columns
                card.grid(row=row, column=col, sticky="ew", padx=10, pady=5)
            
            # Configurer les poids des colonnes
            for i in range(columns):
                widget.cards_frame.grid_columnconfigure(i, weight=1) 