import customtkinter as ctk

class SidebarFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.parent = parent
        
        # Configuration responsive
        self.is_compact = False
        self.normal_width = 240
        self.compact_width = 180
        
        self.configure(fg_color="white", width=self.normal_width)
        self.pack_propagate(False)
        self.pack(side="left", fill="y", padx=0, pady=0)
        
        # Configuration du style
        self.title_font = ctk.CTkFont(family="Helvetica", size=16, weight="bold")
        self.menu_font = ctk.CTkFont(family="Helvetica", size=13)
        self.submenu_font = ctk.CTkFont(family="Helvetica", size=11)
        
        # Lier la sidebar à l'app pour le responsive
        self.app.sidebar = self
        
        self.active_button = None  # Pour stocker le bouton actuellement actif
        self.nav_buttons = {}  # Pour stocker tous les boutons de navigation
        self.button_labels = {}  # Ajout d'un dictionnaire pour stocker label et couleur
        
        # Correction : sécuriser l'accès à user_info
        if not hasattr(app, 'user_info') or app.user_info is None:
            app.user_info = {
                'prenom': 'Utilisateur',
                'nom': 'Test',
                'role': 'Admin',
                'email': 'test@example.com',
                'matricule': '12345'
            }
        nav_items = [
            ('🏠', 'Dashboard', '#0288D1'),
            ('🗺️', 'Entrepôt', '#43A047'),
            ('📦', 'Stocks', '#FFA000'),
            ('🔄', 'Mouvements', '#9C27B0'),
            ('📥', 'Réception', '#388E3C'),
            ('🚚', 'Expédition', '#F4511E'),
            ('📦‍📦', 'Emballages', '#00B8D4'),
            ('📊', 'Rapports', '#6A1B9A'),
            ('⚙️', 'Admin', '#D32F2F')
        ]
        btn_frame = ctk.CTkFrame(self, fg_color='transparent')
        btn_frame.pack(side='top', fill='x', expand=False, pady=(10,0))
        
        for icon, label, color in nav_items:
            btn = ctk.CTkButton(
                btn_frame,
                text=f"{icon}  {label}",
                fg_color='transparent',
                hover_color=color,
                text_color=color,
                corner_radius=12,
                height=40,
                font=ctk.CTkFont(size=14, weight='bold'),
                hover=True,
                command=lambda l=label, c=color, b=None: self._on_nav_click(l, c, b)
            )
            # Stocker label et couleur dans le dictionnaire
            self.button_labels[btn] = (label, color)
            btn.configure(command=lambda l=label, c=color, b=btn: self._on_nav_click(l, c, b))
            def on_enter(e, b=btn): 
                if b != self.active_button:
                    b.configure(text_color='white')
            def on_leave(e, b=btn, c=color): 
                if b != self.active_button:
                    b.configure(text_color=c)
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
            btn.pack(fill='x', pady=1, padx=10)
            self.nav_buttons[label] = btn
            
        # Carte profil utilisateur esthétique avec bouton déconnexion en bas
        profile_card = ctk.CTkFrame(self, fg_color='#fff', corner_radius=14, border_width=1, border_color='#e0e0e0')
        profile_card.pack(side='bottom', fill='x', padx=14, pady=12)
        ctk.CTkLabel(profile_card, text='👤', font=ctk.CTkFont(size=32), text_color='#2563eb').pack(pady=(10,0))
        ctk.CTkLabel(profile_card, text=f"{app.user_info['prenom']} {app.user_info['nom']}", font=ctk.CTkFont(size=15, weight='bold'), text_color='#222').pack(pady=(2,0))
        ctk.CTkLabel(profile_card, text=app.user_info['role'], font=ctk.CTkFont(size=13), text_color='#2563eb').pack()
        ctk.CTkLabel(profile_card, text=app.user_info['email'], font=ctk.CTkFont(size=12), text_color='#666').pack(pady=(0,2))
        ctk.CTkLabel(profile_card, text=f"Matricule : {app.user_info['matricule']}", font=ctk.CTkFont(size=12, slant='italic'), text_color='#90A4AE').pack(pady=(0,8))
        ctk.CTkButton(profile_card, text='🚪 Déconnexion', fg_color='#EF5350', hover_color='#E53935', text_color='white', corner_radius=8, height=38, font=ctk.CTkFont(size=14, weight='bold'), command=self.confirm_logout).pack(fill='x', padx=10, pady=(0,10))

    def configure_compact(self, compact=True):
        """Configure la sidebar en mode compact ou normal"""
        if compact != self.is_compact:
            self.is_compact = compact
            width = self.compact_width if compact else self.normal_width
            self.configure(width=width)
            
            # Adapter les polices selon le mode
            if compact:
                self.title_font = ctk.CTkFont(family="Helvetica", size=14, weight="bold")
                self.menu_font = ctk.CTkFont(family="Helvetica", size=12)
                self.submenu_font = ctk.CTkFont(family="Helvetica", size=10)
            else:
                self.title_font = ctk.CTkFont(family="Helvetica", size=16, weight="bold")
                self.menu_font = ctk.CTkFont(family="Helvetica", size=13)
                self.submenu_font = ctk.CTkFont(family="Helvetica", size=11)
            
            # Mettre à jour les widgets existants
            self._update_widget_fonts()
    
    def _update_widget_fonts(self):
        """Met à jour les polices des widgets existants"""
        for widget in self.winfo_children():
            if hasattr(widget, 'configure'):
                if 'font' in widget.configure():
                    if 'title' in str(widget).lower():
                        widget.configure(font=self.title_font)
                    elif 'menu' in str(widget).lower():
                        widget.configure(font=self.menu_font)
                    elif 'submenu' in str(widget).lower():
                        widget.configure(font=self.submenu_font)

    def set_active_button(self, label):
        for btn_label, btn in self.nav_buttons.items():
            # Utiliser le dictionnaire pour récupérer la couleur
            color = self.button_labels.get(btn, (None, '#0288D1'))[1]
            btn.configure(fg_color='transparent', text_color=color)
        if label in self.nav_buttons:
            active_btn = self.nav_buttons[label]
            color = self.button_labels.get(active_btn, (None, '#0288D1'))[1]
            active_btn.configure(fg_color=color, text_color='white')
            self.active_button = active_btn

    def confirm_logout(self):
        if hasattr(self, 'app') and self.app:
            self.app.confirm_logout()

    def apply_theme(self, theme):
        """Applique le thème à la sidebar"""
        try:
            if theme == "dark":
                # Mode sombre
                self.configure(fg_color="#2d2d2d")
                
                # Adapter les couleurs des boutons
                for btn in self.nav_buttons.values():
                    if btn != self.active_button:
                        color = self.button_labels.get(btn, (None, '#0288D1'))[1]
                        btn.configure(fg_color='transparent', text_color=color)
                
                # Adapter la carte profil
                for widget in self.winfo_children():
                    if isinstance(widget, ctk.CTkFrame) and hasattr(widget, 'configure'):
                        widget.configure(fg_color="#3d3d3d", border_color="#555555")
                
            else:
                # Mode clair
                self.configure(fg_color="white")
                
                # Adapter les couleurs des boutons
                for btn in self.nav_buttons.values():
                    if btn != self.active_button:
                        color = self.button_labels.get(btn, (None, '#0288D1'))[1]
                        btn.configure(fg_color='transparent', text_color=color)
                
                # Adapter la carte profil
                for widget in self.winfo_children():
                    if isinstance(widget, ctk.CTkFrame) and hasattr(widget, 'configure'):
                        widget.configure(fg_color="#fff", border_color="#e0e0e0")
            
            print(f"Thème appliqué à la sidebar: {theme}")
            
        except Exception as e:
            print(f"Erreur lors de l'application du thème à la sidebar: {e}")

    def _on_nav_click(self, label, color, button):
        if not hasattr(self, 'app') or self.app is None:
            return
        # Mettre à jour l'apparence du bouton actif
        self.set_active_button(label)
        # Afficher la notification de changement de page
        self.app.show_notification(f"Page changée : {label}")
        if label == "Stocks":
            self.app.show_stock()
        elif label == "Dashboard":
            self.app.show_dashboard(self.app.user_info)
        elif label == "Réception":
            self.app.show_reception()
        elif label == "Rapports":
            self.app.show_analytics()
        elif label == "Entrepôt":
            self.app.show_warehouse()
        elif label == "Admin":
            self.app.show_admin()
        elif label == "Expédition":
            self.app.show_expedition()
        elif label == "Emballages":
            self.app.show_packaging()
        elif label == "Mouvements":  # Nouveau !
            self.app.show_movements()
        # Les autres boutons peuvent être ajoutés plus tard 