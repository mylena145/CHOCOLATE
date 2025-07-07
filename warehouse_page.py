import customtkinter as ctk
from stock_management_page import SidebarFrame

class WarehouseFrame(ctk.CTkFrame):
    def __init__(self, master, user_info=None):
        super().__init__(master, fg_color="white")
        self.pack(fill="both", expand=True)
        if user_info is None:
            user_info = {'prenom':'Utilisateur','nom':'Test','role':'Admin','email':'test@example.com','matricule':'12345'}
        self.sidebar = SidebarFrame(self, master)
        self.sidebar.pack(side="left", fill="y")
        self.main = ctk.CTkFrame(self, fg_color="white")
        self.main.pack(side="right", fill="both", expand=True)
        self._create_header()
        self._create_summary()
        body = ctk.CTkScrollableFrame(self.main, fg_color="white", corner_radius=0)
        body.pack(fill="both", expand=True, padx=20, pady=10)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        zones = [
            {'name':'Zone E0','desc':'Matériel informatique - 85/100','pct':85,
             'cells':['A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4'],
             'statuses':['occupied','occupied','free','occupied','occupied','free','occupied','free','occupied','occupied','maintenance','free']},
            {'name':'Zone E1','desc':'Électronique - 92/120','pct':77,
             'cells':['A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4'],
             'statuses':['free','occupied','occupied','occupied','occupied','free','occupied','occupied','occupied','free','occupied','occupied']},
            {'name':'Zone E2','desc':'Mobilier - 67/110','pct':61,
             'cells':['A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4'],
             'statuses':['occupied','free','occupied','free','occupied','occupied','free','occupied','occupied','free','occupied','free']},
            {'name':'Zone E3','desc':'Emballage - 98/120','pct':82,
             'cells':['A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','C3','C4'],
             'statuses':['occupied','occupied','occupied','occupied','occupied','occupied','occupied','occupied','free','occupied','free','occupied']},
        ]
        for idx, zone in enumerate(zones):
            col = idx % 2
            row = idx // 2
            self._create_zone_card(body, zone).grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        self._create_reception_card(body).grid(row=(len(zones)//2)+1, column=0, columnspan=2, pady=10, sticky="ew")

    def _create_header(self):
        hdr = ctk.CTkFrame(self.main, fg_color="#F3F4F6")
        hdr.pack(fill="x")
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            hdr, text="Gestion des Entrepôts",
            font=ctk.CTkFont(size=24, weight="bold"), text_color="#212224"
        ).grid(row=0, column=0, padx=20, pady=(20,2), sticky="w")
        ctk.CTkLabel(
            hdr, text="Organisation de l'espace de stockage et des cellules",
            font=ctk.CTkFont(size=14), text_color="#6B7280"
        ).grid(row=1, column=0, padx=20, pady=(0,12), sticky="w")
        act = ctk.CTkFrame(hdr, fg_color="transparent")
        act.grid(row=0, column=1, rowspan=2, padx=20)
        ctk.CTkButton(
            act, text="+ Nouvelle Cellule",
            fg_color="#2563EB", hover_color="#1E40AF",
            text_color="white",
            font=ctk.CTkFont(size=13, weight="bold"), corner_radius=8, height=38,
            command=self._open_new_cell_popup
        ).pack(side="left")
        ctk.CTkEntry(
            act, width=250, height=38,
            fg_color="white", border_color="#D1D5DB",
            placeholder_text="Rechercher cellule…"
        ).pack(side="left", padx=(10,0))

    def _create_summary(self):
        frame = ctk.CTkFrame(self.main, fg_color="white")
        frame.pack(fill="x", padx=20, pady=(0,20))
        stats = [
            ("Total Cellules","450","4 zones actives","🗔","#14B8A6"),
            ("Cellules Occupées","342","76% occupation","✅","#10B981"),
            ("Cellules Libres","108","24% disponible","◻️","#EF4444"),
            ("Maintenance","0","Toutes opérationnelles","🛠️","#6B7280"),
        ]
        for title, val, sub, ic, color in stats:
            card = ctk.CTkFrame(
                frame, fg_color="white",
                border_width=1, border_color="#E5E7EB",
                corner_radius=10
            )
            card.pack(side="left", expand=True, fill="x", padx=8, ipady=12)
            circ = ctk.CTkFrame(card, fg_color=color, width=40, height=40, corner_radius=8)
            circ.pack(pady=(10,0))
            circ.pack_propagate(False)
            circ.grid_columnconfigure(0, weight=1)
            circ.grid_rowconfigure(0, weight=1)
            ctk.CTkLabel(
                circ, text=ic,
                font=ctk.CTkFont(size=20), text_color="white"
            ).grid(row=0, column=0, sticky="nsew")
            ctk.CTkLabel(
                card, text=title,
                font=ctk.CTkFont(size=14), text_color="#374151"
            ).pack(pady=(8,0))
            ctk.CTkLabel(
                card, text=val,
                font=ctk.CTkFont(size=28, weight="bold"), text_color=color
            ).pack()
            ctk.CTkLabel(
                card, text=sub,
                font=ctk.CTkFont(size=12), text_color="#6B7280"
            ).pack(pady=(0,10))

    def _create_zone_card(self, parent, zone):
        card = ctk.CTkFrame(
            parent, fg_color="white",
            border_width=1, border_color="#E5E7EB",
            corner_radius=10
        )
        hdr = ctk.CTkFrame(card, fg_color="#2563EB", corner_radius=10)
        hdr.pack(fill="x")
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            hdr, text=zone['name'],
            font=ctk.CTkFont(size=16, weight="bold"), text_color="white"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        ctk.CTkLabel(
            hdr, text=f"{zone['pct']}%",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="white"
        ).grid(row=0, column=1, padx=10, pady=8, sticky="e")
        ctk.CTkLabel(
            hdr, text=zone['desc'],
            font=ctk.CTkFont(size=12), text_color="white"
        ).grid(row=1, column=0, columnspan=2, padx=10, pady=(0,8), sticky="w")
        grid = ctk.CTkFrame(card, fg_color="white")
        grid.pack(padx=10, pady=(0,10))
        color_map = {'occupied':'#10B981','free':None,'maintenance':'#EF4444'}
        for j in range(4): grid.grid_columnconfigure(j, weight=1)
        for i, (name, st) in enumerate(zip(zone['cells'], zone['statuses'])):
            r, c = divmod(i, 4)
            if st == 'free':
                btn = ctk.CTkButton(
                    grid, text=name, fg_color="transparent",
                    hover_color="#F3F4F6", border_width=2,
                    border_color="#D1D5DB", text_color="#212224",
                    width=80, height=80, corner_radius=8
                )
            else:
                clr = color_map.get(st)
                btn = ctk.CTkButton(
                    grid, text=name, fg_color=clr,
                    hover_color=clr, text_color="white",
                    width=80, height=80, corner_radius=8
                )
            btn.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
        leg = ctk.CTkFrame(card, fg_color="white")
        leg.pack(fill="x", padx=10, pady=(0,10))
        for st, lbl in [('occupied','Occupée'),('free','Libre'),('maintenance','Maintenance')]:
            dot_color = '#10B981' if st=='occupied' else ('#F3F4F6' if st=='free' else '#EF4444')
            dot = ctk.CTkLabel(leg, text="●", text_color=dot_color)
            dot.pack(side="left", padx=(10,2))
            ctk.CTkLabel(
                leg, text=lbl,
                font=ctk.CTkFont(size=12), text_color="#374151"
            ).pack(side="left", padx=(0,10))
        return card

    def _create_reception_card(self, parent):
        card = ctk.CTkFrame(
            parent, fg_color="white",
            border_width=1, border_color="#E5E7EB",
            corner_radius=10
        )
        hdr = ctk.CTkFrame(card, fg_color="#2563EB", corner_radius=10)
        hdr.pack(fill="x")
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            hdr, text="Zone de Réception",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="white"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        status = ctk.CTkLabel(
            hdr, text="Opérationnelle",
            font=ctk.CTkFont(size=12, weight="bold"), fg_color="#10B981",
            corner_radius=8, text_color="white"
        )
        status.grid(row=0, column=1, padx=10, pady=8, sticky="e")
        infos = [("Colis en attente","12"),("Capacité maximale","50"),("Occupation","24%")]
        for txt,val in infos:
            f = ctk.CTkFrame(card, fg_color="#F3F4F6", corner_radius=8)
            f.pack(fill="x", padx=10, pady=6)
            ctk.CTkLabel(
                f, text=txt,
                font=ctk.CTkFont(size=12), text_color="#374151"
            ).pack(side="left", padx=10, pady=8)
            ctk.CTkLabel(
                f, text=val,
                font=ctk.CTkFont(size=12, weight="bold"), text_color="#212224"
            ).pack(side="right", padx=10, pady=8)
        return card

    def _open_new_cell_popup(self):
        """Ouvre une fenêtre pop-up scrollable pour ajouter une nouvelle cellule."""
        popup = ctk.CTkToplevel(self)
        popup.title("Nouvelle Cellule")
        popup.geometry("400x450")  # Taille un peu plus grande pour le scroll
        popup.transient(self.master)
        popup.grab_set()
        
        # Création du frame scrollable principal
        main_scroll_frame = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        main_scroll_frame.pack(fill="both", expand=True)
        
        # Variables pour les messages d'erreur
        self.cell_name_error = ctk.StringVar()
        self.zone_error = ctk.StringVar()
        
        # Titre
        ctk.CTkLabel(
            main_scroll_frame, 
            text="Ajouter une nouvelle cellule",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10))
        
        # Conteneur des champs de formulaire
        form_frame = ctk.CTkFrame(main_scroll_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=20)
        
        # Champ Nom de la cellule
        ctk.CTkLabel(
            form_frame,
            text="Nom de la cellule:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(0, 5))
        
        self.cell_name_entry = ctk.CTkEntry(
            form_frame,
            width=350,
            placeholder_text="Ex: A1, B2, C3..."
        )
        self.cell_name_entry.pack()
        
        # Message erreur nom
        ctk.CTkLabel(
            form_frame,
            textvariable=self.cell_name_error,
            text_color="red",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")
        
        # Champ Zone
        ctk.CTkLabel(
            form_frame,
            text="Zone:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(10, 5))
        
        self.zone_optionmenu = ctk.CTkOptionMenu(
            form_frame,
            values=["Zone E0", "Zone E1", "Zone E2", "Zone E3"],
            width=350
        )
        self.zone_optionmenu.pack()
        
        # Message erreur zone
        ctk.CTkLabel(
            form_frame,
            textvariable=self.zone_error,
            text_color="red",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", pady=(0, 20))  # Espace avant les boutons
        
        # Conteneur des boutons
        button_frame = ctk.CTkFrame(main_scroll_frame, fg_color="transparent")
        button_frame.pack(pady=(10, 20))
        
        # Bouton Valider
        ctk.CTkButton(
            button_frame,
            text="Valider",
            fg_color="#10B981",
            hover_color="#0E9F72",
            width=120,
            height=40,
            command=lambda: self._validate_cell(popup)
        ).pack(side="left", padx=10)
        
        # Bouton Annuler
        ctk.CTkButton(
            button_frame,
            text="Annuler",
            fg_color="#EF4444",
            hover_color="#D63535",
            width=120,
            height=40,
            command=lambda: self._confirm_cancel(popup)
        ).pack(side="right", padx=10)
        
        # Positionnement automatique et focus
        popup.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (popup.winfo_width() // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        self.cell_name_entry.focus()

    def _validate_form(self):
        """Valide les champs du formulaire."""
        valid = True
        
        # Validation nom
        if not self.cell_name_entry.get().strip():
            self.cell_name_error.set("Veuillez entrer un nom de cellule")
            valid = False
        else:
            self.cell_name_error.set("")
        
        # Validation zone (toujours sélectionnée avec les valeurs par défaut)
        if not self.zone_optionmenu.get():
            self.zone_error.set("Veuillez sélectionner une zone")
            valid = False
        else:
            self.zone_error.set("")
            
        return valid

    def _validate_cell(self, popup):
        """Valide et traite la création d'une nouvelle cellule."""
        if not self._validate_form():
            return  # Ne pas fermer si formulaire invalide
            
        # Récupération des valeurs
        cell_name = self.cell_name_entry.get().strip()
        zone = self.zone_optionmenu.get()
        
        # Fermeture du popup
        popup.destroy()
        
        # Affichage du message de succès
        self._show_success_message(cell_name, zone)

    def _confirm_cancel(self, popup):
        """Affiche une confirmation pour l'annulation."""
        confirm = ctk.CTkToplevel(self)
        confirm.title("Confirmer annulation")
        confirm.geometry("350x200")
        confirm.transient(popup)
        confirm.grab_set()
        
        # Message
        ctk.CTkLabel(
            confirm,
            text="Confirmer l'annulation?",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            confirm,
            text="Les modifications non enregistrées seront perdues.",
            text_color="#6B7280",
            font=ctk.CTkFont(size=14)
        ).pack(pady=10)
        
        # Boutons
        btn_frame = ctk.CTkFrame(confirm, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Confirmer",
            fg_color="#EF4444",
            hover_color="#D63535",
            command=lambda: [confirm.destroy(), popup.destroy()]
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Continuer",
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=confirm.destroy
        ).pack(side="right", padx=10)
        
        # Centrage
        confirm.update_idletasks()
        x = popup.winfo_x() + (popup.winfo_width() // 2) - (confirm.winfo_width() // 2)
        y = popup.winfo_y() + (popup.winfo_height() // 2) - (confirm.winfo_height() // 2)
        confirm.geometry(f"+{x}+{y}")

    def _show_success_message(self, cell_name, zone):
        """Affiche un message de succès après validation."""
        success = ctk.CTkToplevel(self)
        success.title("Succès")
        success.geometry("400x250")
        
        # Icône de succès
        icon_frame = ctk.CTkFrame(success, fg_color="#D1FAE5", width=80, height=80, corner_radius=40)
        icon_frame.pack(pady=20)
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(
            icon_frame,
            text="✓",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#10B981"
        ).pack(expand=True)
        
        # Message
        ctk.CTkLabel(
            success,
            text="Cellule créée avec succès!",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack()
        
        # Détails
        details_frame = ctk.CTkFrame(success, fg_color="transparent")
        details_frame.pack(pady=10)
        
        ctk.CTkLabel(
            details_frame,
            text=f"Nom: {cell_name}",
            font=ctk.CTkFont(size=14)
        ).pack()
        
        ctk.CTkLabel(
            details_frame,
            text=f"Zone: {zone}",
            font=ctk.CTkFont(size=14)
        ).pack()
        
        # Bouton OK
        ctk.CTkButton(
            success,
            text="OK",
            fg_color="#10B981",
            hover_color="#0E9F72",
            width=120,
            height=40,
            command=success.destroy
        ).pack(pady=10)
        
        # Centrage
        success.update_idletasks()
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (success.winfo_width() // 2)
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (success.winfo_height() // 2)
        success.geometry(f"+{x}+{y}")

    def apply_theme(self, theme):
        """Applique le thème à la page des entrepôts"""
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
            if hasattr(self, 'main'):
                self.main.configure(fg_color=bg_color)
            
            # Adapter tous les widgets enfants
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    widget.configure(fg_color=card_bg, border_color=border_color)
                    
                    # Adapter les labels dans les frames
                    for child in widget.winfo_children():
                        if isinstance(child, ctk.CTkLabel):
                            child.configure(text_color=text_color)
                        elif isinstance(child, ctk.CTkEntry):
                            child.configure(fg_color=card_bg, text_color=text_color, border_color=border_color)
                        elif isinstance(child, ctk.CTkButton):
                            # Garder les couleurs des boutons d'action
                            pass
                        elif isinstance(child, ctk.CTkFrame):
                            child.configure(fg_color=card_bg, border_color=border_color)
            
            print(f"Thème appliqué à la page Entrepôts: {theme}")
            
        except Exception as e:
            print(f"Erreur lors de l'application du thème à la page Entrepôts: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = ctk.CTk()
    app.geometry("1200x900")
    WarehouseFrame(app)
    app.mainloop()
