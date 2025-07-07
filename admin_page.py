import customtkinter as ctk
import tkinter as tk
from sidebar import SidebarFrame
import datetime
from database import list_users, delete_user, update_user, reset_password, deactivate_user

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

# Gestion sécurisée des imports optionnels
try:
    from tkcalendar import DateEntry
    HAS_TKCALENDAR = True
except ImportError:
    HAS_TKCALENDAR = False
    print("tkcalendar non disponible - fonctionnalités de calendrier désactivées")

try:
    from babel.dates import format_datetime
    HAS_BABEL = True
except ImportError:
    HAS_BABEL = False
    print("babel non disponible - formatage des dates en français désactivé")

try:
    from CTkToolTip import CTkToolTip
    HAS_TOOLTIP = True
except ImportError:
    HAS_TOOLTIP = False
    print("CTkToolTip non disponible - tooltips désactivés")

try:
    import locale
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    HAS_LOCALE = True
except:
    HAS_LOCALE = False
    print("Locale française non disponible")

import tkinter.messagebox as mbox

class AdminFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Configuration responsive
        self.responsive_config = {}
        if hasattr(parent, 'get_responsive_config'):
            self.responsive_config = parent.get_responsive_config()
        
        self.create_widgets()
        self.pack(fill="both", expand=True)
        
        # Lier le redimensionnement
        self.bind("<Configure>", self._on_frame_resize)

    def on_window_resize(self, width, height):
        """Méthode appelée quand la fenêtre est redimensionnée"""
        if hasattr(self.parent, 'get_responsive_config'):
            self.responsive_config = self.parent.get_responsive_config()
        self._adapt_layout_to_size(width, height)
    
    def _on_frame_resize(self, event):
        """Gère le redimensionnement du frame"""
        if event.width > 100 and event.height > 100:
            self._adapt_layout_to_size(event.width, event.height)
    
    def _adapt_layout_to_size(self, width, height):
        """Adapte la mise en page selon la taille"""
        # Adapter la table selon la largeur
        if width < 1200:
            # Mode compact - masquer certaines colonnes
            self._configure_table_compact(True)
        else:
            # Mode normal - afficher toutes les colonnes
            self._configure_table_compact(False)
    
    def _configure_table_compact(self, compact):
        """Configure la table en mode compact ou normal"""
        # Cette méthode peut être implémentée pour adapter la table
        pass

    def create_widgets(self):
        user_info = getattr(self.parent, 'user_info', None)
        if user_info is None:
            user_info = {
                'prenom': 'Utilisateur',
                'nom': 'Test',
                'role': 'Admin',
                'email': 'test@example.com',
                'matricule': '12345'
            }
        self.sidebar = SidebarFrame(self, self.parent)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.set_active_button("Admin")
        self.main_content = ctk.CTkFrame(self, fg_color="#f7fafd")
        self.main_content.pack(side="right", fill="both", expand=True)
        self._build_topbar()
        self._build_stats_cards()
        self._build_tabs()
        self._show_tab("Utilisateurs")
        self._update_time()

    def _build_topbar(self):
        topbar = ctk.CTkFrame(self.main_content, fg_color="white", height=70)
        topbar.pack(fill="x", pady=(18, 0), padx=24)
        topbar.grid_columnconfigure(0, weight=1)
        title = ctk.CTkLabel(topbar, text="Administration du Système", font=ctk.CTkFont(size=22, weight="bold"), text_color="#222")
        title.grid(row=0, column=0, sticky="w", pady=(8,0))
        subtitle = ctk.CTkLabel(topbar, text="Gestion des utilisateurs, paramètres et configurations", font=ctk.CTkFont(size=14), text_color="#666")
        subtitle.grid(row=1, column=0, sticky="w")
        self.time_label = ctk.CTkLabel(topbar, text="", font=ctk.CTkFont(size=13), text_color="#666")
        self.time_label.grid(row=0, column=2, rowspan=2, sticky="e", padx=(0,10))
        btn = ctk.CTkButton(topbar, text="👤  Nouvel Utilisateur", fg_color="#3b82f6", hover_color="#2563eb", text_color="white", corner_radius=8, font=ctk.CTkFont(size=14, weight="bold"), width=180, height=36, command=self._open_user_modal)
        btn.grid(row=0, column=1, rowspan=2, sticky="e", padx=(0,20))

    def _update_time(self):
        now = datetime.datetime.now()
        if HAS_LOCALE:
            txt = now.strftime("%A %d %B %Y à %H:%M")
        else:
            txt = now.strftime("%d/%m/%Y %H:%M")
        self.time_label.configure(text=txt)
        self.after(1000, self._update_time)

    def _build_stats_cards(self):
        stats_frame = ctk.CTkFrame(self.main_content, fg_color="#f7fafd")
        stats_frame.pack(fill="x", pady=(10, 8), padx=24)
        cards_data = [
            ("Utilisateurs Actifs", "8", "#10b981", "✅", "+2 ce mois", "#10b981"),
            ("Super Administrateurs", "2", "#DC2626", "🛡️", "Accès complet", "#DC2626"),
            ("Gestionnaires", "3", "#2563EB", "👔", "Accès étendu", "#2563EB"),
            ("Opérateurs", "3", "#D97706", "👷", "Accès limité", "#D97706")
        ]
        for i, (title, value, color, icon, sub, subcolor) in enumerate(cards_data):
            card = ctk.CTkFrame(stats_frame, fg_color="white", corner_radius=16, border_width=1, border_color="#e0e0e0", width=220, height=110)
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=28), text_color=color).place(x=12, y=10)
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=13), text_color="#666").place(x=54, y=12)
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold"), text_color="#222").place(x=54, y=36)
            ctk.CTkLabel(card, text=sub, font=ctk.CTkFont(size=12), text_color=subcolor).place(x=54, y=72)

    def _build_tabs(self):
        tab_frame = ctk.CTkFrame(self.main_content, fg_color="white")
        tab_frame.pack(fill="x", pady=(10, 0), padx=24)
        self.tabs = {}
        tab_labels = [
            ("Utilisateurs", "👥"),
            ("Rôles & Permissions", "🔖"),
            ("Paramètres Système", "⚙️"),
            ("Journal d'Activité", "📝"),
            ("CLI", "💻")
        ]
        for tab, icon in tab_labels:
            b = ctk.CTkButton(tab_frame, text=f"{icon} {tab}", fg_color="#f7fafd", hover_color="#e3e8ee", text_color="#222", corner_radius=6, font=ctk.CTkFont(size=13, weight="bold"), width=190, height=32, command=lambda t=tab: self._show_tab(t))
            b.pack(side="left", padx=(0, 8))
            self.tabs[tab] = b
        self.tab_contents = {}
        for tab, _ in tab_labels:
            frame = ctk.CTkFrame(self.main_content, fg_color="white")
            frame.pack(fill="both", expand=True, padx=24, pady=(0, 24))
            frame.pack_forget()
            self.tab_contents[tab] = frame
        self._build_users_tab(self.tab_contents["Utilisateurs"])
        self._build_roles_tab(self.tab_contents["Rôles & Permissions"])
        self._build_settings_tab(self.tab_contents["Paramètres Système"])
        self._build_audit_tab(self.tab_contents["Journal d'Activité"])
        self._build_cli_tab(self.tab_contents["CLI"])

    def _show_tab(self, tab):
        for t, btn in self.tabs.items():
            if t == tab:
                btn.configure(fg_color="#3b82f6", text_color="white")
            else:
                btn.configure(fg_color="#f7fafd", text_color="#222")
        for t, frame in self.tab_contents.items():
            if t == tab:
                frame.pack(fill="both", expand=True, padx=24, pady=(0, 24))
            else:
                frame.pack_forget()

    def _build_users_tab(self, parent):
        # Barre recherche et titre
        top = ctk.CTkFrame(parent, fg_color="white")
        top.pack(fill="x", pady=(10, 0))
        ctk.CTkLabel(top, text="Liste des Utilisateurs", font=ctk.CTkFont(size=16, weight="bold"), text_color="#222").pack(side="left", padx=8)
        search = ctk.CTkEntry(top, placeholder_text="Rechercher un utilisateur...", width=260)
        search.pack(side="right", padx=8)
        search.bind('<KeyRelease>', lambda e: self._refresh_users(table, search.get()))
        # Tableau utilisateurs
        table = ctk.CTkFrame(parent, fg_color="white", border_width=1, border_color="#e0e0e0")
        table.pack(fill="both", expand=True, pady=(8, 0))
        self._refresh_users(table, "")
        # Pagination fictive
        pag = ctk.CTkFrame(parent, fg_color="white")
        pag.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(pag, text="Affichage de 1 à 10 sur 24 utilisateurs", font=ctk.CTkFont(size=12), text_color="#666").pack(side="left", padx=8)
        for txt, color in [("Précédent", "#666"), ("1", "#fff"), ("2", "#666"), ("Suivant", "#666")]:
            ctk.CTkButton(pag, text=txt, fg_color="#3b82f6" if txt=="1" else "#f7fafd", text_color="#222" if txt!="1" else "#fff", width=38, height=28, corner_radius=6).pack(side="left", padx=2)

    def _refresh_users(self, table, search_term):
        for w in table.winfo_children():
            w.destroy()
        header = ctk.CTkFrame(table, fg_color="white")
        header.pack(fill="x")
        for col in ["Nom", "Email", "Rôle", "Dernière Connexion", "Statut", "Actions"]:
            ctk.CTkLabel(header, text=col, font=ctk.CTkFont(size=13, weight="bold"), text_color="#666", width=160, anchor="w").pack(side="left", padx=2)
        users = list_users()
        for user in users:
            uid, nom, prenom, email, role, matricule, actif, last_login = user
            if search_term and search_term.lower() not in (nom+prenom+email+role+matricule).lower():
                continue
            # Format date en français
            try:
                dt = datetime.datetime.strptime(last_login, "%d/%m/%Y %H:%M")
                if HAS_BABEL:
                    last_login_fr = format_datetime(dt, "d MMMM yyyy HH:mm", locale="fr_FR")
                else:
                    last_login_fr = dt.strftime("%d/%m/%Y %H:%M")
            except Exception:
                last_login_fr = last_login
            row = ctk.CTkFrame(table, fg_color="#f7fafd")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"👤 {prenom} {nom}\n{matricule}", font=ctk.CTkFont(size=13, weight="bold"), text_color="#222", width=160, anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=email, font=ctk.CTkFont(size=13), text_color="#222", width=160, anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=role, font=ctk.CTkFont(size=13), text_color="#7c3aed" if role=="Super Administrateur" else "#2563eb" if role=="Administrateur" else "#059669" if role=="Gestionnaire Entrepôt" else "#ef4444", width=160, anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=last_login_fr, font=ctk.CTkFont(size=13), text_color="#222", width=160, anchor="w").pack(side="left", padx=2)
            ctk.CTkLabel(row, text="🟢 Actif" if actif else "🔴 Inactif", font=ctk.CTkFont(size=13), text_color="#10b981" if actif else "#ef4444", width=160, anchor="w").pack(side="left", padx=2)
            actions = ctk.CTkFrame(row, fg_color="#f7fafd")
            actions.pack(side="left", padx=2)
            ctk.CTkButton(actions, text="✏️", width=32, height=32, fg_color="#3b82f6", text_color="#fff", corner_radius=8, command=lambda u=user: self._edit_user(u, table, search_term)).pack(side="left", padx=2)
            ctk.CTkButton(actions, text="🔑", width=32, height=32, fg_color="#10b981", text_color="#fff", corner_radius=8, command=lambda u=user: self._reset_user_pw(u, table, search_term)).pack(side="left", padx=2)
            ctk.CTkButton(actions, text="🚫", width=32, height=32, fg_color="#ef4444", text_color="#fff", corner_radius=8, command=lambda u=user: self._confirm_delete_user(u, table, search_term)).pack(side="left", padx=2)

    def _edit_user(self, user, table, search_term):
        uid, nom, prenom, email, role, matricule, actif, last_login = user
        modal = ctk.CTkToplevel(self)
        modal.title("Éditer l'utilisateur")
        modal.geometry("440x520")
        modal.grab_set()
        modal.resizable(False, False)
        ctk.CTkLabel(modal, text="✏️ Modifier un utilisateur", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2563eb").pack(pady=(22,8))
        form = ctk.CTkFrame(modal, fg_color="white", corner_radius=16)
        form.pack(fill="both", expand=True, padx=22, pady=8)
        entries = {}
        for label, val in [("Nom", nom), ("Prénom", prenom), ("Email", email), ("Rôle", role), ("Matricule", matricule)]:
            ctk.CTkLabel(form, text=label, font=ctk.CTkFont(size=14), text_color="#222").pack(anchor="w", pady=(10,0))
            if label == "Rôle":
                e = ctk.CTkComboBox(form, values=[
                    "Super Administrateur", "Administrateur", "Gestionnaire Entrepôt", 
                    "Responsable Réception", "Opérateur Stock", "Expéditeur", 
                    "Consultant", "Stagiaire"
                ])
                e.set(val)
            else:
                e = ctk.CTkEntry(form, height=36, font=ctk.CTkFont(size=13))
                e.insert(0, val)
            e.pack(fill="x", pady=2)
            entries[label] = e
        # Champ date avec calendrier
        ctk.CTkLabel(form, text="Dernière connexion", font=ctk.CTkFont(size=14), text_color="#222").pack(anchor="w", pady=(10,0))
        date_var = tk.StringVar(value=last_login)
        date_entry = DateEntry(form, locale='fr_FR', date_pattern='dd/MM/yyyy', textvariable=date_var, width=18, background='#3b82f6', foreground='white', borderwidth=2)
        date_entry.pack(fill="x", pady=2)
        btns = ctk.CTkFrame(form, fg_color="white")
        btns.pack(fill="x", pady=22)
        ctk.CTkButton(btns, text="Annuler", fg_color="#f7fafd", text_color="#222", corner_radius=8, height=38, command=modal.destroy).pack(side="left", padx=8)
        def save():
            update_user(uid, entries["Nom"].get(), entries["Prénom"].get(), entries["Email"].get(), entries["Rôle"].get(), entries["Matricule"].get())
            # Ici tu pourrais aussi sauvegarder la date si tu l'ajoutes en base
            modal.destroy()
            self._refresh_users(table, search_term)
        ctk.CTkButton(btns, text="💾 Enregistrer", fg_color="#3b82f6", text_color="#fff", corner_radius=8, height=38, command=save).pack(side="right", padx=8)

    def _reset_user_pw(self, user, table, search_term):
        uid = user[0]
        modal = ctk.CTkToplevel(self)
        modal.title("Réinitialiser le mot de passe")
        modal.geometry("420x240")
        modal.grab_set()
        modal.resizable(False, False)
        ctk.CTkLabel(modal, text="🔑 Réinitialiser le mot de passe", font=ctk.CTkFont(size=18, weight="bold"), text_color="#10b981").pack(pady=(22,8))
        pw = ctk.CTkEntry(modal, show="*", height=36, font=ctk.CTkFont(size=13))
        pw.pack(fill="x", padx=22, pady=10)
        btns = ctk.CTkFrame(modal, fg_color="white")
        btns.pack(fill="x", pady=22)
        ctk.CTkButton(btns, text="Annuler", fg_color="#f7fafd", text_color="#222", corner_radius=8, height=38, command=modal.destroy).pack(side="left", padx=8)
        def save():
            reset_password(uid, pw.get())
            modal.destroy()
        ctk.CTkButton(btns, text="🔄 Réinitialiser", fg_color="#10b981", text_color="#fff", corner_radius=8, height=38, command=save).pack(side="right", padx=8)

    def _confirm_delete_user(self, user, table, search_term):
        uid = user[0]
        modal = ctk.CTkToplevel(self)
        modal.title("Confirmation")
        modal.geometry("400x200")
        modal.grab_set()
        modal.resizable(False, False)
        ctk.CTkLabel(modal, text="🚫 Désactiver/Supprimer", font=ctk.CTkFont(size=18, weight="bold"), text_color="#ef4444").pack(pady=(22,8))
        ctk.CTkLabel(modal, text="Voulez-vous vraiment désactiver ou supprimer cet utilisateur ?", font=ctk.CTkFont(size=14), text_color="#d32f2f", wraplength=340, justify="center").pack(pady=(0,12), padx=20)
        btns = ctk.CTkFrame(modal, fg_color="white")
        btns.pack(pady=(0,18))
        ctk.CTkButton(btns, text="Oui, supprimer", fg_color="#ef4444", hover_color="#b91c1c", text_color="#fff", corner_radius=8, height=38, command=lambda: self._delete_user(uid, modal, table, search_term)).pack(side="left", padx=12)
        ctk.CTkButton(btns, text="Non, annuler", fg_color="#90A4AE", hover_color="#78909C", text_color="#fff", corner_radius=8, height=38, command=modal.destroy).pack(side="left", padx=12)

    def _delete_user(self, uid, modal, table, search_term):
        delete_user(uid)
        modal.destroy()
        self._refresh_users(table, search_term)

    def _build_roles_tab(self, parent):
        ctk.CTkLabel(parent, text="Gestion des Rôles et Permissions", font=ctk.CTkFont(size=19, weight="bold"), text_color="#2563eb").pack(pady=(18, 2))
        ctk.CTkLabel(parent, text="Visualisez, recherchez et comprenez les droits de chaque rôle du système.", font=ctk.CTkFont(size=13), text_color="#666").pack(pady=(0, 10))
        topbar = ctk.CTkFrame(parent, fg_color="white")
        topbar.pack(fill="x", padx=30, pady=(0, 8))
        search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(topbar, placeholder_text="Rechercher un rôle...", textvariable=search_var, width=220)
        search_entry.pack(side="left", padx=(0, 12))
        add_btn = ctk.CTkButton(topbar, text="➕ Ajouter un rôle", fg_color="#3b82f6", text_color="#fff", corner_radius=8, height=36)
        add_btn.pack(side="right")
        # Table responsive
        table_frame = ctk.CTkFrame(parent, fg_color="#f7fafd", corner_radius=14)
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)
        def render_table():
            for w in table_frame.winfo_children():
                w.destroy()
            header = ctk.CTkFrame(table_frame, fg_color="white")
            header.pack(fill="x")
            for col, w in zip(["Rôle", "Description", "Permissions"], [140, 260, 420]):
                ctk.CTkLabel(header, text=col, font=ctk.CTkFont(size=14, weight="bold"), text_color="#666", width=w, anchor="w").pack(side="left", padx=2)
            roles = [
                ("Super Administrateur", "Accès complet à toutes les fonctionnalités du système", [
                    ("Gestion utilisateurs", "Créer, éditer, supprimer tous les comptes"),
                    ("Gestion rôles", "Définir et modifier les rôles et permissions"),
                    ("Paramètres système", "Configuration complète du système"),
                    ("Sauvegardes", "Gestion des sauvegardes et restauration"),
                    ("Audit complet", "Accès à tous les logs d'activité")]),
                ("Administrateur", "Gestion complète des utilisateurs et paramètres système", [
                    ("Gestion utilisateurs", "Créer, éditer, supprimer des comptes"),
                    ("Gestion rôles", "Définir les rôles et permissions"),
                    ("Paramètres système", "Configuration du système"),
                    ("Audit", "Consulter les logs d'activité")]),
                ("Gestionnaire Entrepôt", "Gestion des stocks, réceptions, expéditions et rapports", [
                    ("Gestion stocks", "Créer, modifier, supprimer des produits"),
                    ("Réceptions", "Gérer les bons de réception"),
                    ("Expéditions", "Gérer les bons d'expédition"),
                    ("Emballages", "Gérer les matériaux d'emballage"),
                    ("Entrepôts", "Gérer les zones et cellules"),
                    ("Rapports", "Créer et exporter des rapports")]),
                ("Responsable Réception", "Gestion des réceptions et contrôle qualité", [
                    ("Réceptions", "Créer et valider les réceptions"),
                    ("Contrôle qualité", "Vérifier les marchandises reçues"),
                    ("Stocks", "Consulter les niveaux de stock"),
                    ("Emballages", "Consulter les emballages"),
                    ("Rapports", "Consulter les rapports")]),
                ("Opérateur Stock", "Opérations de stockage et inventaire", [
                    ("Stocks", "Consulter et modifier les stocks"),
                    ("Réceptions", "Enregistrer les réceptions"),
                    ("Entrepôts", "Consulter les zones de stockage")]),
                ("Expéditeur", "Gestion des expéditions et livraisons", [
                    ("Expéditions", "Créer et valider les expéditions"),
                    ("Livraisons", "Suivre les livraisons"),
                    ("Emballages", "Gérer les emballages"),
                    ("Rapports", "Consulter les rapports")]),
                ("Consultant", "Consultation des rapports et statistiques", [
                    ("Dashboard", "Consulter le tableau de bord"),
                    ("Stocks", "Consulter les stocks"),
                    ("Réceptions", "Consulter les réceptions"),
                    ("Expéditions", "Consulter les expéditions"),
                    ("Rapports", "Consulter et exporter les rapports")]),
                ("Stagiaire", "Accès limité en lecture seule", [
                    ("Dashboard", "Consulter le tableau de bord"),
                    ("Stocks", "Consulter les stocks"),
                    ("Réceptions", "Consulter les réceptions"),
                    ("Expéditions", "Consulter les expéditions")])
            ]
            filtered = [r for r in roles if search_var.get().lower() in r[0].lower() or search_var.get().lower() in r[1].lower() or any(search_var.get().lower() in p[0].lower() for p in r[2])]
            if not filtered:
                ctk.CTkLabel(table_frame, text="Aucun rôle ne correspond à votre recherche.", font=ctk.CTkFont(size=13), text_color="#ef4444").pack(pady=30)
                return
            for role, desc, perms in filtered:
                row = ctk.CTkFrame(table_frame, fg_color="#fff", corner_radius=10)
                row.pack(fill="x", pady=4, padx=2)
                # Couleurs selon le niveau d'accès
                if role == "Super Administrateur":
                    badge_color = "#DC2626"
                elif role == "Administrateur":
                    badge_color = "#7C3AED"
                elif role == "Gestionnaire Entrepôt":
                    badge_color = "#2563EB"
                elif role == "Responsable Réception":
                    badge_color = "#059669"
                elif role == "Opérateur Stock":
                    badge_color = "#D97706"
                elif role == "Expéditeur":
                    badge_color = "#F59E0B"
                elif role == "Consultant":
                    badge_color = "#6B7280"
                else:
                    badge_color = "#9CA3AF"
                badge = ctk.CTkLabel(row, text=role, font=ctk.CTkFont(size=13, weight="bold"), text_color="#fff", fg_color=badge_color, corner_radius=8, width=120, anchor="center")
                badge.pack(side="left", padx=8, pady=8)
                ctk.CTkLabel(row, text=desc, font=ctk.CTkFont(size=13), text_color="#222", width=260, anchor="w", wraplength=250, justify="left").pack(side="left", padx=2)
                perms_frame = ctk.CTkFrame(row, fg_color="#fff")
                perms_frame.pack(side="left", padx=2)
                for p, tip in perms:
                    lbl = ctk.CTkLabel(perms_frame, text=f"✔️ {p}", font=ctk.CTkFont(size=12), text_color="#2563eb", anchor="w")
                    lbl.pack(anchor="w", pady=1)
                    if HAS_TOOLTIP:
                        CTkToolTip(lbl, message=tip)
        render_table()
        search_entry.bind('<KeyRelease>', lambda e: render_table())

    def _build_settings_tab(self, parent):
        # Détecter le thème actuel
        current_theme = ctk.get_appearance_mode()
        is_dark = current_theme == "dark"
        
        # Couleurs adaptatives
        bg_color = "#404040" if is_dark else "#f7fafd"
        text_color = "#ffffff" if is_dark else "#222222"
        secondary_text = "#cccccc" if is_dark else "#666666"
        border_color = "#555555" if is_dark else "#e0e0e0"
        
        ctk.CTkLabel(parent, text="Paramètres du Système", 
                    font=ctk.CTkFont(size=19, weight="bold"), 
                    text_color="#00ff00" if is_dark else "#2563eb").pack(pady=(18, 2))
        
        ctk.CTkLabel(parent, text="Configurez les options globales du système. Les modifications sont immédiates.", 
                    font=ctk.CTkFont(size=13), 
                    text_color=secondary_text).pack(pady=(0, 10))
        
        # Variables pour stocker les états des switches
        self.settings_switches = {}
        
        settings = [
            ("Mode sombre", "Active le thème sombre pour tous les utilisateurs.", "dark_mode"),
            ("Notifications email", "Envoie des alertes par email pour les événements critiques.", "email_notifications"),
            ("Sauvegarde automatique", "Sauvegarde les données toutes les 10 minutes.", "auto_backup"),
            ("Maintenance", "Met le système en mode maintenance (accès restreint).", "maintenance_mode"),
            ("Rafraîchissement auto", "Rafraîchit les données automatiquement toutes les 30s.", "auto_refresh"),
            ("Logs détaillés", "Active les logs détaillés pour le débogage.", "detailed_logs")
        ]
        
        for label, tip, setting_key in settings:
            row = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=10, border_width=1, border_color=border_color)
            row.pack(fill="x", padx=40, pady=8)
            
            ctk.CTkLabel(row, text=label, 
                        font=ctk.CTkFont(size=14, weight="bold"), 
                        text_color=text_color, width=220, anchor="w").pack(side="left", padx=8)
            
            # Créer le switch avec fonction de callback
            switch = ctk.CTkSwitch(row, text="", width=60)
            switch.pack(side="left", padx=8)
            
            # Configurer la commande après avoir créé le switch
            switch.configure(command=lambda key=setting_key, sw=switch: self._on_setting_changed(key, sw))
            
            # Stocker la référence du switch
            self.settings_switches[setting_key] = switch
            
            # Charger l'état actuel depuis la base de données ou les préférences
            self._load_setting_state(setting_key, switch)
            
            if HAS_TOOLTIP:
                CTkToolTip(switch, message=tip)
            else:
                ctk.CTkLabel(row, text=tip, 
                            font=ctk.CTkFont(size=12), 
                            text_color=secondary_text, anchor="w").pack(side="left", padx=8)
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=10, border_width=1, border_color=border_color)
        buttons_frame.pack(fill="x", padx=40, pady=15)
        
        ctk.CTkButton(buttons_frame, text="💾 Sauvegarder", 
                     fg_color="#00ff00" if is_dark else "#10b981", 
                     text_color="#000000" if is_dark else "#ffffff", 
                     corner_radius=8, height=35, 
                     command=self._save_all_settings).pack(side="left", padx=10, pady=10)
        
        ctk.CTkButton(buttons_frame, text="🔄 Réinitialiser", 
                     fg_color="#ff0000" if is_dark else "#ef4444", 
                     text_color="#ffffff", 
                     corner_radius=8, height=35, 
                     command=self._reset_settings).pack(side="left", padx=10, pady=10)
        
        ctk.CTkButton(buttons_frame, text="📊 Statistiques", 
                     fg_color="#0000ff" if is_dark else "#3b82f6", 
                     text_color="#ffffff", 
                     corner_radius=8, height=35, 
                     command=self._show_settings_stats).pack(side="right", padx=10, pady=10)
        
        ctk.CTkLabel(parent, text="Les modifications sont appliquées immédiatement.", 
                    font=ctk.CTkFont(size=12, slant="italic"), 
                    text_color="#888888").pack(pady=(18, 0))

    def _load_setting_state(self, setting_key, switch):
        """Charge l'état d'un paramètre depuis la base de données"""
        try:
            # Pour l'instant, on utilise des valeurs par défaut
            # Plus tard, on peut charger depuis une table settings
            default_states = {
                "dark_mode": True,  # Mode sombre activé par défaut
                "email_notifications": False,
                "auto_backup": True,
                "maintenance_mode": False,
                "auto_refresh": True,
                "detailed_logs": False
            }
            
            is_enabled = default_states.get(setting_key, False)
            switch.select() if is_enabled else switch.deselect()
            
        except Exception as e:
            print(f"Erreur lors du chargement du paramètre {setting_key}: {e}")
            switch.deselect()

    def _on_setting_changed(self, setting_key, switch):
        """Appelé quand un paramètre change"""
        is_enabled = switch.get()
        
        try:
            if setting_key == "dark_mode":
                self._apply_dark_mode(is_enabled)
            elif setting_key == "email_notifications":
                self._toggle_email_notifications(is_enabled)
            elif setting_key == "auto_backup":
                self._toggle_auto_backup(is_enabled)
            elif setting_key == "maintenance_mode":
                self._toggle_maintenance_mode(is_enabled)
            elif setting_key == "auto_refresh":
                self._toggle_auto_refresh(is_enabled)
            elif setting_key == "detailed_logs":
                self._toggle_detailed_logs(is_enabled)
            
            # Sauvegarder dans la base de données
            self._save_setting_to_db(setting_key, is_enabled)
            
            # Afficher une notification
            status = "activé" if is_enabled else "désactivé"
            self._show_setting_notification(f"{setting_key.replace('_', ' ').title()} {status}")
            
        except Exception as e:
            print(f"Erreur lors de l'application du paramètre {setting_key}: {e}")
            # Remettre le switch dans son état précédent
            switch.select() if not is_enabled else switch.deselect()

    def _apply_dark_mode(self, enabled):
        """Applique le mode sombre à toute l'application de manière intelligente"""
        try:
            if enabled:
                # Activer le mode sombre global
                ctk.set_appearance_mode("dark")
                ctk.set_default_color_theme("dark-blue")
                
                # Appliquer aux fenêtres principales
                if hasattr(self.parent, 'configure'):
                    self.parent.configure(fg_color="#1a1a1a")
                
                # Appliquer aux frames principaux
                if hasattr(self, 'main_content'):
                    self.main_content.configure(fg_color="#1a1a1a")
                
                # Appliquer aux sidebar
                if hasattr(self, 'sidebar'):
                    self.sidebar.configure(fg_color="#2d2d2d")
                
                # Notifier tous les composants du changement
                self._notify_theme_change("dark")
                
                # Forcer le rafraîchissement de l'interface
                self.parent.update()
                
            else:
                # Activer le mode clair global
                ctk.set_appearance_mode("light")
                ctk.set_default_color_theme("blue")
                
                # Appliquer aux fenêtres principales
                if hasattr(self.parent, 'configure'):
                    self.parent.configure(fg_color="white")
                
                # Appliquer aux frames principaux
                if hasattr(self, 'main_content'):
                    self.main_content.configure(fg_color="#f7fafd")
                
                # Appliquer aux sidebar
                if hasattr(self, 'sidebar'):
                    self.sidebar.configure(fg_color="white")
                
                # Notifier tous les composants du changement
                self._notify_theme_change("light")
                
                # Forcer le rafraîchissement de l'interface
                self.parent.update()
                
        except Exception as e:
            print(f"Erreur lors de l'application du thème: {e}")

    def _notify_theme_change(self, theme):
        """Notifie tous les composants du changement de thème"""
        try:
            # Notifier l'application principale
            if hasattr(self.parent, 'notify_theme_change'):
                self.parent.notify_theme_change(theme)
            
            # Notifier la sidebar
            if hasattr(self, 'sidebar') and hasattr(self.sidebar, 'apply_theme'):
                self.sidebar.apply_theme(theme)
            
            # Notifier tous les frames enfants
            for widget in self.winfo_children():
                if hasattr(widget, 'apply_theme'):
                    widget.apply_theme(theme)
                elif hasattr(widget, 'configure'):
                    # Appliquer les couleurs de base selon le thème
                    if theme == "dark":
                        widget.configure(fg_color="#2d2d2d")
                    else:
                        widget.configure(fg_color="white")
            
            print(f"Thème appliqué globalement: {theme}")
            
        except Exception as e:
            print(f"Erreur lors de la notification du thème: {e}")

    def _toggle_email_notifications(self, enabled):
        """Active/désactive les notifications email"""
        if enabled:
            print("Notifications email activées")
            # Logique pour activer les notifications
        else:
            print("Notifications email désactivées")
            # Logique pour désactiver les notifications

    def _toggle_auto_backup(self, enabled):
        """Active/désactive la sauvegarde automatique"""
        if enabled:
            print("Sauvegarde automatique activée")
            # Démarrer le processus de sauvegarde
            self._start_backup_process()
        else:
            print("Sauvegarde automatique désactivée")
            # Arrêter le processus de sauvegarde
            self._stop_backup_process()

    def _toggle_maintenance_mode(self, enabled):
        """Active/désactive le mode maintenance"""
        if enabled:
            print("Mode maintenance activé")
            # Logique pour activer le mode maintenance
            self._show_maintenance_warning()
        else:
            print("Mode maintenance désactivé")
            # Logique pour désactiver le mode maintenance

    def _toggle_auto_refresh(self, enabled):
        """Active/désactive le rafraîchissement automatique"""
        if enabled:
            print("Rafraîchissement automatique activé")
            # Démarrer le rafraîchissement automatique
        else:
            print("Rafraîchissement automatique désactivé")
            # Arrêter le rafraîchissement automatique

    def _toggle_detailed_logs(self, enabled):
        """Active/désactive les logs détaillés"""
        if enabled:
            print("Logs détaillés activés")
            # Activer les logs détaillés
        else:
            print("Logs détaillés désactivés")
            # Désactiver les logs détaillés

    def _start_backup_process(self):
        """Démarre le processus de sauvegarde automatique"""
        # Simulation d'un processus de sauvegarde
        print("Processus de sauvegarde démarré")

    def _stop_backup_process(self):
        """Arrête le processus de sauvegarde automatique"""
        # Simulation d'arrêt du processus
        print("Processus de sauvegarde arrêté")

    def _show_maintenance_warning(self):
        """Affiche un avertissement pour le mode maintenance"""
        import tkinter.messagebox as mbox
        mbox.showwarning("Mode Maintenance", 
                        "Le mode maintenance est activé.\n"
                        "L'accès sera restreint pour les utilisateurs non-administrateurs.")

    def _save_setting_to_db(self, setting_key, value):
        """Sauvegarde un paramètre dans la base de données"""
        try:
            # Ici on peut sauvegarder dans une table settings
            # Pour l'instant, on simule
            print(f"Sauvegarde: {setting_key} = {value}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du paramètre: {e}")

    def _save_all_settings(self):
        """Sauvegarde tous les paramètres"""
        try:
            for setting_key, switch in self.settings_switches.items():
                value = switch.get()
                self._save_setting_to_db(setting_key, value)
            
            self._show_setting_notification("Tous les paramètres sauvegardés")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")

    def _reset_settings(self):
        """Réinitialise tous les paramètres"""
        try:
            for setting_key, switch in self.settings_switches.items():
                # Remettre les valeurs par défaut
                default_states = {
                    "dark_mode": True,
                    "email_notifications": False,
                    "auto_backup": True,
                    "maintenance_mode": False,
                    "auto_refresh": True,
                    "detailed_logs": False
                }
                
                is_enabled = default_states.get(setting_key, False)
                switch.select() if is_enabled else switch.deselect()
                
                # Appliquer le changement
                self._on_setting_changed(setting_key, switch)
            
            self._show_setting_notification("Paramètres réinitialisés")
        except Exception as e:
            print(f"Erreur lors de la réinitialisation: {e}")

    def _show_settings_stats(self):
        """Affiche les statistiques des paramètres"""
        try:
            stats_window = ctk.CTkToplevel(self)
            stats_window.title("Statistiques des Paramètres")
            stats_window.geometry("400x300")
            stats_window.grab_set()
            
            ctk.CTkLabel(stats_window, text="📊 Statistiques des Paramètres", 
                        font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
            
            # Afficher les statistiques
            enabled_count = sum(1 for switch in self.settings_switches.values() if switch.get())
            total_count = len(self.settings_switches)
            
            ctk.CTkLabel(stats_window, text=f"Paramètres activés: {enabled_count}/{total_count}").pack(pady=5)
            ctk.CTkLabel(stats_window, text=f"Taux d'activation: {(enabled_count/total_count)*100:.1f}%").pack(pady=5)
            
        except Exception as e:
            print(f"Erreur lors de l'affichage des statistiques: {e}")

    def _show_setting_notification(self, message):
        """Affiche une notification pour un changement de paramètre"""
        try:
            # Créer une notification temporaire
            notif = ctk.CTkToplevel(self)
            notif.title("Notification")
            notif.geometry("300x80")
            notif.grab_set()
            notif.resizable(False, False)
            
            ctk.CTkLabel(notif, text=message, font=ctk.CTkFont(size=14)).pack(expand=True)
            
            # Fermer automatiquement après 2 secondes
            notif.after(2000, notif.destroy)
        except Exception as e:
            print(f"Erreur lors de l'affichage de la notification: {e}")

    def _build_audit_tab(self, parent):
        ctk.CTkLabel(parent, text="Journal d'Activité", font=ctk.CTkFont(size=19, weight="bold"), text_color="#2563eb").pack(pady=(18, 2))
        ctk.CTkLabel(parent, text="Consultez l'historique des actions du système. Filtrez par type ou utilisateur.", font=ctk.CTkFont(size=13), text_color="#666").pack(pady=(0, 10))
        # Filtres
        filtres = ctk.CTkFrame(parent, fg_color="white")
        filtres.pack(fill="x", padx=30, pady=(0, 8))
        ctk.CTkLabel(filtres, text="Filtrer :", font=ctk.CTkFont(size=13), text_color="#222").pack(side="left", padx=(0, 8))
        for txt, color in [("Tous", "#3b82f6"), ("Connexion", "#10b981"), ("Modification", "#f59e42"), ("Suppression", "#ef4444")]:
            b = ctk.CTkButton(filtres, text=txt, fg_color=color, text_color="#fff", width=110, height=32, corner_radius=8)
            b.pack(side="left", padx=4)
        # Timeline moderne
        timeline = [
            ("Connexion", "Jean Dupont s'est connecté.", "15 mars 2024 09:24", "#10b981"),
            ("Modification", "Marie Martin a modifié un stock.", "15 mars 2024 09:30", "#f59e42"),
            ("Suppression", "Pierre Durand a supprimé un utilisateur.", "15 mars 2024 09:45", "#ef4444")
        ]
        for typ, msg, date, color in timeline:
            row = ctk.CTkFrame(parent, fg_color="#fff", corner_radius=10)
            row.pack(fill="x", padx=40, pady=6)
            badge = ctk.CTkLabel(row, text=typ, font=ctk.CTkFont(size=12, weight="bold"), text_color="#fff", fg_color=color, corner_radius=8, width=100, anchor="center")
            badge.pack(side="left", padx=8, pady=8)
            ctk.CTkLabel(row, text=msg, font=ctk.CTkFont(size=13), text_color="#222", width=340, anchor="w", wraplength=320, justify="left").pack(side="left", padx=2)
            ctk.CTkLabel(row, text=date, font=ctk.CTkFont(size=12), text_color="#666", width=160, anchor="e").pack(side="left", padx=2)
            if HAS_TOOLTIP:
                CTkToolTip(badge, message=f"Type d'action : {typ}")
        ctk.CTkLabel(parent, text="Pour plus de détails, exportez le journal ou contactez l'administrateur.", font=ctk.CTkFont(size=12, slant="italic"), text_color="#90A4AE").pack(pady=(18, 0))

    def _build_cli_tab(self, parent):
        ctk.CTkLabel(parent, text="Terminal CLI", font=ctk.CTkFont(size=19, weight="bold"), text_color="#00ff00").pack(pady=(18, 2))
        ctk.CTkLabel(parent, text="Terminal système compact - Commandes disponibles", font=ctk.CTkFont(size=13), text_color="#cccccc").pack(pady=(0, 10))
        
        # Terminal compact et sombre
        cli_frame = ctk.CTkFrame(parent, fg_color="#000000", corner_radius=8)
        cli_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Zone de sortie compacte
        output = ctk.CTkTextbox(cli_frame, height=120, font=ctk.CTkFont(size=11, family="Consolas"), fg_color="#000000", text_color="#00ff00")
        output.pack(pady=5, fill="both", expand=True, padx=5)
        
        # Message de bienvenue
        output.insert("end", "SAC Terminal v1.0 - Tapez 'help' pour l'aide\n")
        output.insert("end", "root@sac:~$ ")
        
        # Barre de commande compacte
        cmd_frame = ctk.CTkFrame(cli_frame, fg_color="#000000", height=30)
        cmd_frame.pack(fill="x", padx=5, pady=2)
        cmd_frame.pack_propagate(False)
        
        entry = ctk.CTkEntry(cmd_frame, placeholder_text="Commande...", font=ctk.CTkFont(size=11, family="Consolas"), 
                            height=25, fg_color="#000000", text_color="#00ff00", 
                            placeholder_text_color="#666666", border_width=0)
        entry.pack(side="left", fill="x", expand=True, padx=2)
        
        def on_enter(event=None):
            cmd = entry.get().strip()
            if not cmd:
                return
            
            output.insert("end", f"{cmd}\n")
            
            # Commandes simples
            if cmd.lower() == "help":
                output.insert("end", "help, users, stats, clear, date, ls, pwd, exit\n")
            elif cmd.lower() == "users":
                output.insert("end", "Liste des utilisateurs...\n")
            elif cmd.lower() == "stats":
                output.insert("end", "CPU: 15% | RAM: 2.1GB/8GB | Uptime: 2j 15h\n")
            elif cmd.lower() == "clear":
                output.delete("1.0", "end")
                output.insert("end", "SAC Terminal v1.0 - Tapez 'help' pour l'aide\n")
            elif cmd.lower() == "date":
                import datetime
                now = datetime.datetime.now()
                output.insert("end", f"{now.strftime('%d/%m/%Y %H:%M:%S')}\n")
            elif cmd.lower() == "ls":
                output.insert("end", "app.py  database.py  admin_page.py  sac.db\n")
            elif cmd.lower() == "pwd":
                output.insert("end", "/home/sac/admin\n")
            elif cmd.lower() == "exit":
                output.insert("end", "Déconnexion...\n")
            else:
                output.insert("end", f"Commande '{cmd}' non reconnue\n")
            
            output.insert("end", "root@sac:~$ ")
            output.see("end")
            entry.delete(0, "end")
        
        entry.bind('<Return>', on_enter)
        
        # Bouton compact
        ctk.CTkButton(cmd_frame, text="▶", width=30, height=25, fg_color="#00ff00", 
                     text_color="#000000", corner_radius=4, command=on_enter).pack(side="right", padx=2)
        
        ctk.CTkLabel(parent, text="Terminal compact - Utilisez Enter pour exécuter", 
                    font=ctk.CTkFont(size=10, slant="italic"), text_color="#888888").pack(pady=(5, 0))

    def _open_user_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Ajouter un Utilisateur")
        modal.geometry("440x540")
        modal.grab_set()
        modal.resizable(False, False)
        ctk.CTkLabel(modal, text="👤 Ajouter un Utilisateur", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2563eb").pack(pady=(22,8))
        form = ctk.CTkFrame(modal, fg_color="white", corner_radius=16)
        form.pack(fill="both", expand=True, padx=22, pady=8)
        entries = {}
        for label, val in [("Nom complet *", ""), ("Email *", ""), ("Rôle *", "combo"), ("Mot de passe *", "password"), ("Confirmation *", "password")]:
            ctk.CTkLabel(form, text=label, font=ctk.CTkFont(size=14), text_color="#222").pack(anchor="w", pady=(10,0))
            if val == "combo":
                e = ctk.CTkComboBox(form, values=[
                    "Super Administrateur", "Administrateur", "Gestionnaire Entrepôt", 
                    "Responsable Réception", "Opérateur Stock", "Expéditeur", 
                    "Consultant", "Stagiaire"
                ])
            elif val == "password":
                e = ctk.CTkEntry(form, height=36, font=ctk.CTkFont(size=13), show="*")
            else:
                e = ctk.CTkEntry(form, height=36, font=ctk.CTkFont(size=13))
            e.pack(fill="x", pady=2)
            entries[label] = e
        # Champ date avec calendrier
        ctk.CTkLabel(form, text="Date d'ajout", font=ctk.CTkFont(size=14), text_color="#222").pack(anchor="w", pady=(10,0))
        date_var = tk.StringVar()
        if HAS_TKCALENDAR:
            date_entry = DateEntry(form, locale='fr_FR', date_pattern='dd/MM/yyyy', textvariable=date_var, width=18, background='#3b82f6', foreground='white', borderwidth=2)
            date_entry.pack(fill="x", pady=2)
        else:
            # Fallback si tkcalendar n'est pas disponible
            date_entry = ctk.CTkEntry(form, height=36, font=ctk.CTkFont(size=13), placeholder_text="JJ/MM/AAAA")
            date_entry.pack(fill="x", pady=2)
        btns = ctk.CTkFrame(form, fg_color="white")
        btns.pack(fill="x", pady=22)
        ctk.CTkButton(btns, text="Annuler", fg_color="#f7fafd", text_color="#222", corner_radius=8, height=38, command=modal.destroy).pack(side="left", padx=8)
        def save():
            nom = entries["Nom complet *"].get()
            email = entries["Email *"].get()
            role = entries["Rôle *"].get()
            mdp = entries["Mot de passe *"].get()
            conf = entries["Confirmation *"].get()
            if not nom or not email or not role or not mdp or not conf:
                mbox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return
            if mdp != conf:
                mbox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
                return
            # Ajout utilisateur en base PostgreSQL
            try:
                import psycopg2
                conn = psycopg2.connect(**PG_CONN)
                cursor = conn.cursor()
                
                # Insérer dans la table individus
                cursor.execute("""
                    INSERT INTO sge_cre.individus (nom, prenom, email, password, role, matricule, adresse, telephone)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    nom.split()[-1],  # nom de famille
                    " ".join(nom.split()[:-1]),  # prénom
                    email,
                    mdp,  # mot de passe en clair (à hasher en production)
                    role,
                    email.split('@')[0].upper(),  # matricule basé sur email
                    "Adresse par défaut",  # adresse par défaut
                    "Téléphone par défaut"  # téléphone par défaut
                ))
                conn.commit()
                conn.close()
                
                mbox.showinfo("Succès", "Utilisateur ajouté avec succès !")
                modal.destroy()
                
                # Rafraîchir la liste si on est sur l'onglet Utilisateurs
                if hasattr(self, 'tab_contents') and "Utilisateurs" in self.tab_contents:
                    for w in self.tab_contents["Utilisateurs"].winfo_children():
                        w.destroy()
                    self._build_users_tab(self.tab_contents["Utilisateurs"])
                    
            except Exception as e:
                mbox.showerror("Erreur", f"Erreur lors de l'ajout : {e}")
                if 'conn' in locals():
                    conn.close()
        ctk.CTkButton(btns, text="💾 Enregistrer", fg_color="#3b82f6", text_color="#fff", corner_radius=8, height=38, command=save).pack(side="right", padx=8) 