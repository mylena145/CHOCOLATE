import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
from stock_management_page import SidebarFrame
import threading
import time
try:
    from tkcalendar import Calendar
    HAS_TKCALENDAR = True
except ImportError:
    HAS_TKCALENDAR = False

ctk.set_appearance_mode("light")

class RapportAnalyticsFrame(ctk.CTkFrame):
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
        # Définir le bouton Rapports comme actif
        self.sidebar.set_active_button("Rapports")
        self.main_content = ctk.CTkFrame(self, fg_color="white")
        self.main_content.pack(side="right", fill="both", expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # HEADER
        header = ctk.CTkFrame(self.main_content, fg_color="#fff", corner_radius=0)
        header.pack(fill="x", pady=(0, 0))
        left = ctk.CTkFrame(header, fg_color="#fff")
        left.pack(side="left", padx=32, pady=18)
        ctk.CTkLabel(left, text="Rapports et Analytics", font=ctk.CTkFont(size=28, weight="bold"), text_color="#222").pack(anchor="w")
        ctk.CTkLabel(left, text="Analysez les performances et générez des rapports détaillés", font=ctk.CTkFont(size=15), text_color="#6B7280").pack(anchor="w")
        right = ctk.CTkFrame(header, fg_color="#fff")
        right.pack(side="right", padx=32, pady=18)
        
        button_width = 160
        button_height = 40
        
        ctk.CTkButton(right, text="+ Nouveau Rapport", fg_color="#3B82F6", hover_color="#2563EB", text_color="white", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, height=button_height, width=button_width, command=lambda: AddReportPopup(self)).pack(side="left", padx=5)
        ctk.CTkButton(right, text="Programmer", fg_color="#a21caf", hover_color="#7c1d9c", text_color="white", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, height=button_height, width=button_width, command=lambda: ScheduleReportPopup(self)).pack(side="left", padx=5)
        ctk.CTkButton(right, text="⭳ Exporter Tout", fg_color="#16a34a", hover_color="#15803d", text_color="white", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, height=button_height, width=button_width, command=lambda: ExportAllPopup(self)).pack(side="left", padx=5)

        # SCROLLABLE CONTENT (contenu principal, largeur max 1100px)
        scrollable = ctk.CTkScrollableFrame(self.main_content, fg_color="#f3f4f6", width=1100)
        scrollable.pack(fill="both", expand=True, padx=0, pady=0)

        # KPI CARDS
        kpi_frame = ctk.CTkFrame(scrollable, fg_color="#f3f4f6")
        kpi_frame.pack(fill="x", padx=28, pady=(0, 18))
        kpis = [
            {"title": "Rotation Stock", "value": "4.2x", "desc": "+0.3 vs mois dernier", "icon": "", "color": "#3B82F6", "extra": "progress"},
            {"title": "Taux Livraison", "value": "96.8%", "desc": "+2.1% ce mois", "icon": "🚚", "color": "#22c55e", "extra": "icon"},
            {"title": "Coût par Commande", "value": "12 450", "devise": "FCFA", "desc": "-1 200 FCFA optimisé", "icon": "FCFA", "color": "#3B82F6", "extra": "icon"},
            {"title": "Satisfaction Client", "value": "4.7/5", "desc": "+0.2 amélioration", "icon": "⭐", "color": "#f59e42", "extra": "icon"},
        ]
        for i, kpi in enumerate(kpis):
            card = ctk.CTkFrame(kpi_frame, fg_color="white", border_color="#e5e7eb", border_width=1, corner_radius=16)
            card.pack(side="left", expand=True, fill="x", padx=12)
            ctk.CTkLabel(card, text=kpi["title"], font=ctk.CTkFont(size=15, weight="bold"), text_color="#374151").pack(anchor="w", padx=18, pady=(16,0))
            row = ctk.CTkFrame(card, fg_color="white")
            row.pack(fill="x", padx=18, pady=(0,10))
            if kpi["title"] == "Coût par Commande":
                value_label = ctk.CTkLabel(row, text=kpi["value"], font=ctk.CTkFont(size=28, weight="bold"), text_color="#111827")
                value_label.pack(side="left")
                devise_label = ctk.CTkLabel(row, text=kpi["devise"], font=ctk.CTkFont(size=20, weight="bold"), text_color="#16a34a")
                devise_label.pack(side="left", padx=(8,0))
            else:
                ctk.CTkLabel(row, text=kpi["value"], font=ctk.CTkFont(size=28, weight="bold"), text_color="#111827").pack(side="left")
            if kpi["extra"] == "progress":
                ring = ctk.CTkFrame(row, fg_color="#f3f4f6", width=38, height=38, corner_radius=19)
                ring.pack(side="left", padx=(12,0))
                ring.pack_propagate(False)
                ctk.CTkLabel(ring, text="", font=ctk.CTkFont(size=18), text_color=kpi["color"]).pack(expand=True)
            else:
                iconf = ctk.CTkFrame(row, fg_color=kpi["color"], width=38, height=38, corner_radius=8)
                iconf.pack(side="left", padx=(12,0))
                iconf.pack_propagate(False)
                ctk.CTkLabel(iconf, text=kpi["icon"], font=ctk.CTkFont(size=22), text_color="white").pack(expand=True)
            ctk.CTkLabel(card, text=kpi["desc"], font=ctk.CTkFont(size=13), text_color="#6B7280").pack(anchor="w", padx=18, pady=(0,12))

        # TYPES DE RAPPORTS
        types_frame = ctk.CTkFrame(scrollable, fg_color="#f3f4f6")
        types_frame.pack(fill="x", padx=28, pady=(0, 18))
        top = ctk.CTkFrame(types_frame, fg_color="#f3f4f6")
        top.pack(fill="x")
        ctk.CTkLabel(top, text="Types de Rapports", font=ctk.CTkFont(size=17, weight="bold"), text_color="#222").pack(side="left", pady=6)
        ctk.CTkLabel(top, text="75%", font=ctk.CTkFont(size=15, weight="bold"), text_color="#16a34a").pack(side="left", padx=14, pady=6)
        # Grille esthétique pour les cartes rapport
        cards = [
            {"title": "Rapport Performance", "desc": "KPI, productivité et analyse comparative des performances", "badge": "Performance", "badge_color": "#f3e8d2", "icon": "🕒", "color": "#f59e42", "gen": "Il y a 2 jours", "status": "À jour", "status_color": "#22c55e", "highlight": True},
            {"title": "Rapport Stocks", "desc": "Analyse des niveaux de stock, rotations et valorisation par période", "badge": "Disponible", "badge_color": "#dcfce7", "icon": "📦", "color": "#22c55e", "gen": "Hier", "status": "Nouveau", "status_color": "#3B82F6"},
            {"title": "Rapport Activité", "desc": "Performances réceptions, expéditions et flux logistiques", "badge": "Disponible", "badge_color": "#dbeafe", "icon": "📥", "color": "#3B82F6", "gen": "Aujourd'hui", "status": "À jour", "status_color": "#22c55e"},
            {"title": "Rapport Expédition", "desc": "Suivi des expéditions récentes et performance transporteurs", "badge": "Expédition", "badge_color": "#dbeafe", "icon": "🚚", "color": "#3B82F6", "gen": "3 nouvelles expéditions", "status": "À jour", "status_color": "#22c55e", "exp_list": [
                ("EXP-2024-021", "DHL Express", ("Livrée", "#22c55e"), "15/03/2024"),
                ("EXP-2024-020", "Chronopost", ("En transit", "#3B82F6"), "14/03/2024"),
                ("EXP-2024-019", "Colissimo", ("Retard", "#ef4444"), "13/03/2024")
            ]},
            {"title": "Rapport Exceptions", "desc": "Anomalies, écarts et incidents dans les opérations", "badge": "Urgent", "badge_color": "#fee2e2", "icon": "⚠️", "color": "#ef4444", "gen": "5 nouvelles exceptions", "status": "Critique", "status_color": "#ef4444"},
            {"title": "Rapport Financier", "desc": "Coûts, valorisation stocks et analyse budgétaire", "badge": "Mensuel", "badge_color": "#ede9fe", "icon": "💰", "color": "#a21caf", "gen": "Fin du mois", "status": "À jour", "status_color": "#22c55e"},
            {"title": "Rapport Qualité", "desc": "Taux de conformité, retours et satisfaction client", "badge": "Nouveau", "badge_color": "#fce7f3", "icon": "🏅", "color": "#f59e42", "gen": "Version bêta", "status": "Bêta", "status_color": "#a21caf"}
        ]
        grid_frame = ctk.CTkFrame(types_frame, fg_color="#f3f4f6")
        grid_frame.pack(fill="x", padx=0, pady=(6, 0))
        max_cols = 3
        for idx, card in enumerate(cards):
            row_idx = idx // max_cols
            col_idx = idx % max_cols
            card_frame = ctk.CTkFrame(grid_frame, fg_color="white", border_color=card["color"], border_width=2, corner_radius=14, height=160, width=300)
            card_frame.grid(row=row_idx, column=col_idx, padx=12, pady=12, sticky="nsew")
            card_frame.grid_propagate(False)
            # Icon + badge row
            icon_badge_row = ctk.CTkFrame(card_frame, fg_color="white")
            icon_badge_row.pack(fill="x", pady=(8,0))
            iconf = ctk.CTkFrame(icon_badge_row, fg_color=card["color"], width=32, height=32, corner_radius=8)
            iconf.pack(side="left", padx=(10,6))
            iconf.pack_propagate(False)
            icon_label = ctk.CTkLabel(iconf, text=card["icon"], font=ctk.CTkFont(size=18, weight="bold"), text_color="white")
            icon_label.pack(expand=True)
            def make_icon_tooltip(label, icon, title):
                label.bind("<Enter>", lambda e: label.configure(text=f"{icon}\n{title}"))
                label.bind("<Leave>", lambda e: label.configure(text=icon))
            make_icon_tooltip(icon_label, card["icon"], card["title"])
            badge = ctk.CTkFrame(icon_badge_row, fg_color=card["badge_color"], corner_radius=6)
            badge.pack(side="left", padx=(0,6), pady=(0,0))
            badge_label = ctk.CTkLabel(badge, text=card["badge"], font=ctk.CTkFont(size=12, weight="bold"), text_color=card["color"])
            badge_label.pack(padx=7, pady=2)
            def make_badge_tooltip(label, badge_text):
                label.bind("<Enter>", lambda e: label.configure(text=f"{badge_text}\nInfo"))
                label.bind("<Leave>", lambda e: label.configure(text=badge_text))
            make_badge_tooltip(badge_label, card["badge"])
            # Statut (badge à droite, fond gris clair, texte coloré)
            status_badge = ctk.CTkFrame(icon_badge_row, fg_color="#e5e7eb", corner_radius=6)
            status_badge.pack(side="right", padx=(0,6), pady=(0,0))
            status_label = ctk.CTkLabel(status_badge, text=card["status"], font=ctk.CTkFont(size=12, weight="bold"), text_color=card["status_color"])
            status_label.pack(padx=7, pady=2)
            # Titre
            ctk.CTkLabel(card_frame, text=card["title"], font=ctk.CTkFont(size=17, weight="bold"), text_color="#222").pack(anchor="w", padx=12, pady=(6,0))
            # Description
            ctk.CTkLabel(card_frame, text=card["desc"], font=ctk.CTkFont(size=13), text_color="#374151", wraplength=220, justify="left").pack(anchor="w", padx=12, pady=(0,4))
            # Helper text
            ctk.CTkLabel(card_frame, text=f"Dernière génération: {card['gen']}", font=ctk.CTkFont(size=11), text_color="#6B7280").pack(anchor="w", padx=12, pady=(0,4))
            # Boutons d'action
            btn_row = ctk.CTkFrame(card_frame, fg_color="white")
            btn_row.pack(fill="x", padx=6, pady=(0,4))
            detail_btn = ctk.CTkButton(btn_row, text="Voir le détail", fg_color="#3B82F6", hover_color="#2563EB", text_color="white", font=ctk.CTkFont(size=13, weight="bold"), corner_radius=8, height=28, width=90)
            detail_btn.pack(side="left", padx=(0,6))
            detail_btn.bind("<Enter>", lambda e, btn=detail_btn: btn.configure(fg_color="#2563EB"))
            detail_btn.bind("<Leave>", lambda e, btn=detail_btn: btn.configure(fg_color="#3B82F6"))
            detail_btn.bind("<Enter>", lambda e: detail_btn.configure(text="Voir le détail\nAfficher le rapport"))
            detail_btn.bind("<Leave>", lambda e: detail_btn.configure(text="Voir le détail"))
            # Bouton supprimer (sauf critique)
            if card.get("status") != "Critique":
                def confirm_delete(event=None, c=card["title"]):
                    import tkinter.messagebox as mb
                    if mb.askyesno("Confirmation", f"Voulez-vous vraiment supprimer '{c}' ?"):
                        mb.showinfo("Suppression", f"Le rapport '{c}' a été supprimé.")
                delete_btn = ctk.CTkButton(btn_row, text="🗑", fg_color="#fca5a5", hover_color="#ef4444", text_color="#991b1b", font=ctk.CTkFont(size=13, weight="bold"), corner_radius=8, height=28, width=28, command=confirm_delete)
                delete_btn.pack(side="left", padx=(0,6))
                delete_btn.bind("<Enter>", lambda e, btn=delete_btn: btn.configure(text="Supprimer\nRetirer ce rapport"))
                delete_btn.bind("<Leave>", lambda e, btn=delete_btn: btn.configure(text="🗑"))
            # Mini-liste expéditions dans la carte Expédition
            if card.get("exp_list"):
                list_frame = ctk.CTkFrame(card_frame, fg_color="#f9fafb", corner_radius=8)
                list_frame.pack(fill="x", padx=10, pady=(0, 6))
                for exp in card["exp_list"]:
                    row2 = ctk.CTkFrame(list_frame, fg_color="#f9fafb", height=22)
                    row2.pack(fill="x", pady=1)
                    ctk.CTkLabel(row2, text="🚚", font=ctk.CTkFont(size=12), text_color="#3B82F6").pack(side="left", padx=(0,4))
                    ctk.CTkLabel(row2, text=exp[0], font=ctk.CTkFont(size=12, weight="bold"), text_color="#222").pack(side="left", padx=(0,4))
                    ctk.CTkLabel(row2, text=exp[1], font=ctk.CTkFont(size=12), text_color="#374151").pack(side="left", padx=(0,4))
                    badge2 = ctk.CTkFrame(row2, fg_color=exp[2][1], corner_radius=6)
                    badge2.pack(side="left", padx=(0,4))
                    ctk.CTkLabel(badge2, text=exp[2][0], font=ctk.CTkFont(size=11, weight="bold"), text_color="white").pack(padx=4, pady=1)
                    ctk.CTkLabel(row2, text=exp[3], font=ctk.CTkFont(size=11), text_color="#6B7280").pack(side="left", padx=(0,4))
        for i in range(max_cols):
            grid_frame.grid_columnconfigure(i, weight=1)

        # SECTION GRAPHIQUES
        graph_section = ctk.CTkFrame(scrollable, fg_color="#f3f4f6")
        graph_section.pack(fill="x", padx=28, pady=(0, 18))
        ctk.CTkLabel(graph_section, text="Visualisations & Statistiques", font=ctk.CTkFont(size=20, weight="bold"), text_color="#222").pack(anchor="w", pady=(8, 18))
        # Graphique 1 : Evolution des stocks
        graph1_card = ctk.CTkFrame(graph_section, fg_color="#fff", corner_radius=18, border_color="#e5e7eb", border_width=1)
        graph1_card.pack(fill="x", padx=10, pady=(0, 28))
        title_row1 = ctk.CTkFrame(graph1_card, fg_color="#fff")
        title_row1.pack(fill="x", pady=(10,0))
        ctk.CTkLabel(title_row1, text="📈 Évolution des Stocks", font=ctk.CTkFont(size=18, weight="bold"), text_color="#111").pack(side="left", padx=18)
        ctk.CTkLabel(graph1_card, text="Suivi de la variation du stock moyen et du seuil critique par semaine.", font=ctk.CTkFont(size=13), text_color="#6B7280").pack(anchor="w", padx=18, pady=(0,8))
        graph1_bg = ctk.CTkFrame(graph1_card, fg_color="#f8fafc", corner_radius=14)
        graph1_bg.pack(fill="both", expand=True, padx=18, pady=(0,18))
        fig1 = Figure(figsize=(7,3.2), dpi=100)
        ax1 = fig1.add_subplot(111)
        x = np.arange(1, 5)
        stock = [1100, 1200, 1300, 1150]
        seuil = [1000, 1000, 1000, 1000]
        ax1.plot(x, stock, label="Stock Moyen", color="#3B82F6", linewidth=3)
        ax1.plot(x, seuil, label="Seuil Critique", color="#ef4444", linestyle="dashed", linewidth=2)
        ax1.set_xticks(x)
        ax1.set_xticklabels(["Sem 1", "Sem 2", "Sem 3", "Sem 4"])
        ax1.set_yticks([500, 1000, 1500])
        ax1.set_facecolor("#f8fafc")
        fig1.patch.set_facecolor('#f8fafc')
        ax1.legend(loc="upper left")
        for spine in ax1.spines.values():
            spine.set_visible(False)
        canvas1 = FigureCanvasTkAgg(fig1, master=graph1_bg)
        canvas1.get_tk_widget().pack(fill="both", expand=True, padx=0, pady=0)
        # Graphique 2 : Performance transporteurs
        graph2_card = ctk.CTkFrame(graph_section, fg_color="#fff", corner_radius=18, border_color="#e5e7eb", border_width=1)
        graph2_card.pack(fill="x", padx=10, pady=(0, 10))
        title_row2 = ctk.CTkFrame(graph2_card, fg_color="#fff")
        title_row2.pack(fill="x", pady=(10,0))
        ctk.CTkLabel(title_row2, text="🥧 Performance Transporteurs", font=ctk.CTkFont(size=18, weight="bold"), text_color="#111").pack(side="left", padx=18)
        ctk.CTkLabel(graph2_card, text="Répartition des expéditions par transporteur et taux de réussite.", font=ctk.CTkFont(size=13), text_color="#6B7280").pack(anchor="w", padx=18, pady=(0,8))
        graph2_bg = ctk.CTkFrame(graph2_card, fg_color="#f8fafc", corner_radius=14)
        graph2_bg.pack(fill="both", expand=True, padx=18, pady=(0,18))
        fig2 = Figure(figsize=(7,3.2), dpi=100)
        ax2 = fig2.add_subplot(111)
        labels = ["DHL Express", "Chronopost", "Colissimo", "UPS", "Autres"]
        sizes = [35, 25, 15, 15, 10]
        colors = ["#f59e42", "#3B82F6", "#a78bfa", "#fbbf24", "#9ca3af"]
        pie_result = ax2.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90, colors=colors, textprops={'color':"#222", 'fontsize':11})
        if len(pie_result) == 3:
            wedges, texts, autotexts = pie_result
        else:
            wedges, texts = pie_result
            autotexts = []
        ax2.axis('equal')
        fig2.patch.set_facecolor('#f8fafc')
        canvas2 = FigureCanvasTkAgg(fig2, master=graph2_bg)
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=0, pady=0)

        # TABLEAU RAPPORTS RECENTS - AVEC BOUTONS ACTIONS
        table_frame = ctk.CTkFrame(scrollable, fg_color="#fff", corner_radius=16, border_color="#e5e7eb", border_width=1)
        table_frame.pack(fill="x", padx=28, pady=(0, 18))
        title_row = ctk.CTkFrame(table_frame, fg_color="#fff")
        title_row.pack(fill="x")
        ctk.CTkLabel(title_row, text="Rapports Récents", font=ctk.CTkFont(size=20, weight="bold"), text_color="#111").pack(side="left", padx=18, pady=(18,0))
        ctk.CTkButton(title_row, text="Voir tous", fg_color="#3B82F6", hover_color="#2563EB", text_color="white", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8, height=34, width=110).pack(side="right", padx=18, pady=(18,0))
        # Header tableau
        header_bg = "#f3f4f6"
        table_scroll = ctk.CTkScrollableFrame(table_frame, fg_color="#fff", corner_radius=12, height=220, width=950, orientation="horizontal")
        table_scroll.pack(fill="x", padx=10, pady=(12,12))
        table_header = ctk.CTkFrame(table_scroll, fg_color=header_bg, height=48, corner_radius=0)
        table_header.pack(fill="x")
        headers = ["RAPPORT", "TYPE", "PÉRIODE", "GÉNÉRÉ PAR", "DATE", "STATUT", "ACTIONS"]
        col_widths = [240, 110, 120, 130, 90, 110, 110]
        for i, (header, width) in enumerate(zip(headers, col_widths)):
            cell = ctk.CTkFrame(table_header, fg_color="transparent", width=width, height=48)
            cell.grid(row=0, column=i, sticky="nsew")
            ctk.CTkLabel(cell, text=header, font=ctk.CTkFont(size=15, weight="bold"), text_color="#374151", anchor="center").pack(expand=True, fill="both")
        table_header.grid_columnconfigure(tuple(range(len(headers))), weight=1)
        # Séparateur horizontal header
        sep = tk.Frame(table_scroll, bg="#e5e7eb", height=2)
        sep.pack(fill="x")
        rows = [
            ["Analyse Stocks Mars 2024", "Stock", "01/03 - 31/03", "M. Martin", "15/03/2024", ("Terminé", "#22c55e"), ["download", "share"]],
            ["Performance Hebdomadaire", "Performance", "11/03 - 17/03", "Système", "18/03/2024", ("En cours", "#b45309"), ["hourglass", "delete"]],
            ["Exception du Jour", "Exception", "19/03/2024", "Mme Dubois", "19/03/2024", ("En cours", "#b45309"), ["hourglass", "delete"]],
            ["Exceptions du Jour", "Exception", "19/03/2024", "Mme Dubois", "19/03/2024", ("Terminé", "#22c55e"), ["download", "share"]],
        ]
        for idx, row in enumerate(rows):
            line = ctk.CTkFrame(table_scroll, fg_color="#fff", height=48)
            line.pack(fill="x")
            for i, val in enumerate(row):
                cell = ctk.CTkFrame(line, fg_color="#fff", width=col_widths[i], height=48)
                cell.grid(row=0, column=i, sticky="nsew")
                if i == 5:
                    badge = ctk.CTkFrame(cell, fg_color=val[1], corner_radius=20, width=90, height=36)
                    badge.pack(expand=True, padx=8, pady=10)
                    badge.pack_propagate(False)
                    ctk.CTkLabel(badge, text=val[0], font=ctk.CTkFont(size=14, weight="bold"), text_color="#fff").pack(expand=True)
                elif i == 6:
                    actions = ctk.CTkFrame(cell, fg_color="#fff")
                    actions.pack(expand=True)
                    for act in val:
                        if act == "download":
                            ctk.CTkButton(actions, text="⬇️", width=36, height=36, fg_color="#3B82F6", hover_color="#2563EB", text_color="white", corner_radius=10, font=ctk.CTkFont(size=17)).pack(side="left", padx=4)
                        elif act == "share":
                            ctk.CTkButton(actions, text="🔗", width=36, height=36, fg_color="#a21caf", hover_color="#7c1d9c", text_color="white", corner_radius=10, font=ctk.CTkFont(size=17)).pack(side="left", padx=4)
                        elif act == "hourglass":
                            ctk.CTkButton(actions, text="⏳", width=36, height=36, fg_color="#b45309", hover_color="#a16207", text_color="white", corner_radius=10, font=ctk.CTkFont(size=17)).pack(side="left", padx=4)
                        elif act == "delete":
                            ctk.CTkButton(actions, text="✗", width=36, height=36, fg_color="#ef4444", hover_color="#b91c1c", text_color="white", corner_radius=10, font=ctk.CTkFont(size=17)).pack(side="left", padx=4)
                else:
                    anchor = "w"
                    ctk.CTkLabel(cell, text=val, font=ctk.CTkFont(size=15, weight="bold" if i==0 else "normal"), text_color="#222" if i==0 else "#374151", anchor=anchor).pack(expand=True, fill="both", padx=8, pady=12)
            # Séparateur horizontal entre lignes
            if idx < len(rows)-1:
                sep2 = tk.Frame(table_scroll, bg="#e5e7eb", height=1)
                sep2.pack(fill="x")

    def load_data(self):
        # This method is called after create_widgets() to load data
        pass

    def export_all(self):
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Fichiers PDF", "*.pdf"), ("Fichiers Excel", "*.xlsx"), ("Tous les fichiers", "*.*")],
            title="Exporter toutes les données"
        )
        if file_path:
            # Ici, vous mettriez la logique d'exportation réelle
            print(f"Exportation de toutes les données vers : {file_path}")
            # Simuler un succès
            success_popup = ctk.CTkToplevel(self)
            success_popup.title("Succès")
            success_popup.geometry("300x150")
            success_popup.configure(fg_color="white")
            success_popup.grab_set()
            ctk.CTkLabel(success_popup, text="✅", font=ctk.CTkFont(size=40)).pack(pady=10)
            ctk.CTkLabel(success_popup, text="Exportation réussie !", font=ctk.CTkFont(size=16)).pack(pady=5)
            ctk.CTkButton(success_popup, text="OK", command=success_popup.destroy).pack(pady=10)

    def apply_theme(self, theme):
        """Applique le thème à la page des rapports analytics"""
        try:
            is_dark = theme == "dark"
            
            # Couleurs adaptatives
            bg_color = "#1a1a1a" if is_dark else "#f7fafd"
            card_bg = "#2d2d2d" if is_dark else "white"
            text_color = "#ffffff" if is_dark else "#222222"
            secondary_text = "#cccccc" if is_dark else "#666666"
            border_color = "#555555" if is_dark else "#e0e0e0"
            chart_bg = "#3d3d3d" if is_dark else "#f9fafb"
            
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
                            child.configure(fg_color=chart_bg, text_color=text_color, border_color=border_color)
                        elif isinstance(child, ctk.CTkButton):
                            # Garder les couleurs des boutons d'action
                            pass
                        elif isinstance(child, ctk.CTkFrame):
                            child.configure(fg_color=chart_bg, border_color=border_color)
            
            print(f"Thème appliqué à la page Analytics: {theme}")
            
        except Exception as e:
            print(f"Erreur lors de l'application du thème à la page Analytics: {e}")

class ExportAllPopup(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Exporter Tous les Rapports")
        self.geometry("450x340")
        self.configure(fg_color="white")
        self.resizable(False, False)
        self.grab_set()

        self.export_format = ctk.StringVar(value="")

        ctk.CTkLabel(self, text="Exporter Tous les Rapports", font=ctk.CTkFont(size=20, weight="bold"), text_color="#222").pack(pady=(20, 5))
        ctk.CTkLabel(self, text="Sélectionnez le format de fichier pour l'exportation.", justify="center", text_color="#555").pack(pady=(0, 20))
        
        # Frame for radio buttons
        radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        radio_frame.pack(pady=10, padx=30, fill="x")

        csv_radio = ctk.CTkRadioButton(radio_frame, text="CSV (.csv)", variable=self.export_format, value="csv", font=ctk.CTkFont(size=14))
        csv_radio.pack(anchor="w", pady=5)
        
        excel_radio = ctk.CTkRadioButton(radio_frame, text="Excel (.xlsx)", variable=self.export_format, value="xlsx", font=ctk.CTkFont(size=14))
        excel_radio.pack(anchor="w", pady=5)
        
        pdf_radio = ctk.CTkRadioButton(radio_frame, text="PDF (.pdf)", variable=self.export_format, value="pdf", font=ctk.CTkFont(size=14))
        pdf_radio.pack(anchor="w", pady=5)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=(5,0))

        # Separator
        separator = ctk.CTkFrame(self, height=1, fg_color="#e5e7eb")
        separator.pack(fill="x", padx=30, pady=(15, 0))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(15, 20), fill="x", padx=30)
        
        ctk.CTkButton(btn_frame, text="Annuler", command=self.destroy, fg_color="#EF5350", text_color="white", hover_color="#E53935", height=48, corner_radius=10, font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, padx=(0,10))
        ctk.CTkButton(btn_frame, text="Exporter", command=self.do_export, fg_color="#16a34a", hover_color="#15803d", text_color="white", height=48, corner_radius=10, font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", expand=True, padx=(10,0))

    def do_export(self):
        file_format = self.export_format.get()
        if not file_format:
            self.error_label.configure(text="Veuillez sélectionner un format d'exportation.")
            return

        self.error_label.configure(text="")
        self.destroy() # Ferme le popup de confirmation

        file_types = {
            "csv": [("Fichiers CSV", "*.csv")],
            "xlsx": [("Fichiers Excel", "*.xlsx")],
            "pdf": [("Fichiers PDF", "*.pdf")]
        }
        
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{file_format}",
            filetypes=file_types[file_format] + [("Tous les fichiers", "*.*")],
            title=f"Exporter en {file_format.upper()}"
        )

        if file_path:
            print(f"Exportation de toutes les données vers : {file_path} au format {file_format.upper()}")
            # Simuler un succès
            success_popup = ctk.CTkToplevel(self.master)
            success_popup.title("Succès")
            success_popup.geometry("300x150")
            success_popup.configure(fg_color="white")
            success_popup.grab_set()
            ctk.CTkLabel(success_popup, text="✅", font=ctk.CTkFont(size=40)).pack(pady=10)
            ctk.CTkLabel(success_popup, text="Exportation réussie !", font=ctk.CTkFont(size=16)).pack(pady=5)
            ctk.CTkButton(success_popup, text="OK", command=success_popup.destroy).pack(pady=10)

class AddReportPopup(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Créer un Nouveau Rapport")
        self.geometry("580x590") # Taille ajustée
        self.resizable(False, False)
        self.configure(fg_color="white")
        self.grab_set()
        self._drag_start_x = None
        self._drag_start_y = None
        self.error_labels = {}

        # Header
        header = ctk.CTkFrame(self, fg_color="white")
        header.pack(fill="x", pady=(18,0), padx=24)
        ctk.CTkLabel(header, text="Créer un Nouveau Rapport", font=ctk.CTkFont(size=22, weight="bold"), text_color="#222").pack(side="left", pady=6)
        
        # Main content (scrollable)
        content = ctk.CTkScrollableFrame(self, fg_color="white")
        content.pack(fill="both", expand=True, padx=24, pady=8)
        self.content = content

        # Type de rapport
        ctk.CTkLabel(content, text="Type de Rapport *", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w", pady=(8,0))
        self.type_menu = ctk.CTkOptionMenu(content, values=["Sélectionner un type", "Stocks", "Performance", "Exception", "Financier", "Qualité"], fg_color="#f3f4f6", text_color="#222", button_color="#e5e7eb", button_hover_color="#d1d5db", dropdown_fg_color="#f3f4f6", dropdown_text_color="#222", font=ctk.CTkFont(size=14))
        self.type_menu.pack(fill="x", pady=(4,0))
        self.error_labels['type'] = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=12), text_color="#ef4444")
        self.error_labels['type'].pack(anchor="w", pady=(0,8))

        # Nom du rapport
        ctk.CTkLabel(content, text="Nom du Rapport *", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w")
        self.nom_entry = ctk.CTkEntry(content, fg_color="#f3f4f6", text_color="#222", border_color="#d1d5db", border_width=1, height=38, font=ctk.CTkFont(size=14), placeholder_text="Ex: Analyse Stocks Trimestrielle")
        self.nom_entry.pack(fill="x", pady=(4,0))
        self.error_labels['nom'] = ctk.CTkLabel(content, text="", font=ctk.CTkFont(size=12), text_color="#ef4444")
        self.error_labels['nom'].pack(anchor="w", pady=(0,8))

        # Dates
        row_dates = ctk.CTkFrame(content, fg_color="white")
        row_dates.pack(fill="x", pady=(0,0))
        # Date de début
        date_debut_frame = ctk.CTkFrame(row_dates, fg_color="white")
        date_debut_frame.pack(side="left", expand=True, fill="x", padx=(0,8))
        ctk.CTkLabel(date_debut_frame, text="Date de Début *", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w")
        date_debut_row = ctk.CTkFrame(date_debut_frame, fg_color="white")
        date_debut_row.pack(fill="x")
        self.date_debut = ctk.CTkEntry(date_debut_row, fg_color="#f3f4f6", text_color="#222", border_color="#d1d5db", border_width=1, height=38, font=ctk.CTkFont(size=14))
        self.date_debut.pack(side="left", fill="x", expand=True, pady=(4,0))
        ctk.CTkButton(date_debut_row, text="📅", width=38, height=38, fg_color="#e0e7ff", hover_color="#c7d2fe", text_color="#1e40af", corner_radius=8, command=lambda: self.open_calendar(self.date_debut)).pack(side="left", padx=(6,0))
        self.error_labels['date_debut'] = ctk.CTkLabel(date_debut_frame, text="", font=ctk.CTkFont(size=12), text_color="#ef4444")
        self.error_labels['date_debut'].pack(anchor="w", pady=(0,0))
        # Date de fin
        date_fin_frame = ctk.CTkFrame(row_dates, fg_color="white")
        date_fin_frame.pack(side="left", expand=True, fill="x", padx=(8,0))
        ctk.CTkLabel(date_fin_frame, text="Date de Fin *", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w")
        date_fin_row = ctk.CTkFrame(date_fin_frame, fg_color="white")
        date_fin_row.pack(fill="x")
        self.date_fin = ctk.CTkEntry(date_fin_row, fg_color="#f3f4f6", text_color="#222", border_color="#d1d5db", border_width=1, height=38, font=ctk.CTkFont(size=14))
        self.date_fin.pack(side="left", fill="x", expand=True, pady=(4,0))
        ctk.CTkButton(date_fin_row, text="📅", width=38, height=38, fg_color="#e0e7ff", hover_color="#c7d2fe", text_color="#1e40af", corner_radius=8, command=lambda: self.open_calendar(self.date_fin)).pack(side="left", padx=(6,0))
        self.error_labels['date_fin'] = ctk.CTkLabel(date_fin_frame, text="", font=ctk.CTkFont(size=12), text_color="#ef4444")
        self.error_labels['date_fin'].pack(anchor="w", pady=(0,0))
        row_dates.pack(pady=(0,8))

        # Format d'export
        ctk.CTkLabel(content, text="Format d'Export", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w", pady=(8,0))
        row_format = ctk.CTkFrame(content, fg_color="white")
        row_format.pack(fill="x", pady=(4,12))
        self.format_pdf = ctk.CTkCheckBox(row_format, text="PDF", font=ctk.CTkFont(size=13), fg_color="#3B82F6", border_color="#d1d5db", text_color="#222")
        self.format_pdf.pack(side="left", padx=8)
        self.format_pdf.select()
        self.format_excel = ctk.CTkCheckBox(row_format, text="Excel", font=ctk.CTkFont(size=13), fg_color="#3B82F6", border_color="#d1d5db", text_color="#222")
        self.format_excel.pack(side="left", padx=8)
        self.format_csv = ctk.CTkCheckBox(row_format, text="CSV", font=ctk.CTkFont(size=13), fg_color="#3B82F6", border_color="#d1d5db", text_color="#222")
        self.format_csv.pack(side="left", padx=8)

        # Filtres avancés
        ctk.CTkLabel(content, text="Filtres Avancés", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w", pady=(8,0))
        row_filtres = ctk.CTkFrame(content, fg_color="white")
        row_filtres.pack(fill="x", pady=(4,12))
        self.entrepot_menu = ctk.CTkOptionMenu(row_filtres, values=["Tous les entrepôts", "Entrepôt A", "Entrepôt B"], fg_color="#f3f4f6", text_color="#222", button_color="#e5e7eb", button_hover_color="#d1d5db", dropdown_fg_color="#f3f4f6", dropdown_text_color="#222", font=ctk.CTkFont(size=14))
        self.entrepot_menu.pack(side="left", expand=True, fill="x", padx=(0,8))
        self.categorie_menu = ctk.CTkOptionMenu(row_filtres, values=["Toutes catégories", "Informatique", "Mobilier", "Fournitures"], fg_color="#f3f4f6", text_color="#222", button_color="#e5e7eb", button_hover_color="#d1d5db", dropdown_fg_color="#f3f4f6", dropdown_text_color="#222", font=ctk.CTkFont(size=14))
        self.categorie_menu.pack(side="left", expand=True, fill="x", padx=(8,0))

        # Commentaires
        ctk.CTkLabel(content, text="Commentaires", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(anchor="w", pady=(8,0))
        self.comment_text = ctk.CTkTextbox(content, fg_color="#f3f4f6", text_color="#222", border_color="#d1d5db", border_width=1, height=60, font=ctk.CTkFont(size=14))
        self.comment_text.insert("0.0", "Objectif du rapport, destinataires...")
        self.comment_text.pack(fill="x", pady=(4,12))

        # Boutons bas
        btn_row = ctk.CTkFrame(content, fg_color="white")
        btn_row.pack(fill="x", pady=(18,0))
        ctk.CTkButton(btn_row, text="Annuler", fg_color="#EF5350", hover_color="#E53935", text_color="white", corner_radius=12, height=44, font=ctk.CTkFont(size=16, weight="bold"), command=self.destroy).pack(side="left", expand=True, fill="x", padx=(0,12))
        ctk.CTkButton(
            btn_row,
            text="📝 Générer le Rapport",
            fg_color="#3B82F6",
            hover_color="#2563EB",
            text_color="white",
            corner_radius=12,
            height=44,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.validate_and_generate
        ).pack(side="left", expand=True, fill="x", padx=(12,0))

    def open_calendar(self, entry_widget):
        if not HAS_TKCALENDAR:
            popup = ctk.CTkToplevel(self)
            popup.title("Erreur")
            popup.geometry("320x120")
            popup.configure(fg_color="#fff0f0")
            ctk.CTkLabel(popup, text="tkcalendar n'est pas installé !", font=ctk.CTkFont(size=15, weight="bold"), text_color="#ef4444").pack(pady=24)
            ctk.CTkButton(popup, text="Fermer", fg_color="#ef4444", text_color="white", command=popup.destroy).pack(pady=8)
            return

        cal_popup = ctk.CTkToplevel(self)
        cal_popup.title("Sélectionner une date")
        cal_popup.geometry("270x250")
        cal_popup.configure(fg_color="#fff")
        cal_popup.grab_set()
        cal_popup.resizable(False, False)
        # Fade-in animation
        try:
            cal_popup.attributes('-alpha', 0.0)
            def fade_in(window, step=0.07, delay=10):
                try:
                    alpha = window.attributes('-alpha')
                except Exception:
                    alpha = 1.0
                if alpha < 1.0:
                    alpha = min(1.0, alpha + step)
                    window.attributes('-alpha', alpha)
                    window.after(delay, lambda: fade_in(window, step, delay))
            fade_in(cal_popup)
        except Exception:
            pass

        cal_frame = ctk.CTkFrame(cal_popup, fg_color="#fff")
        cal_frame.pack(fill="both", expand=True, padx=8, pady=8)

        cal = Calendar(
            cal_frame,
            selectmode='day',
            date_pattern='dd/mm/yyyy',
            background='#fff',
            disabledbackground='#f3f4f6',
            bordercolor='#3B82F6',
            headersbackground='#e0e7ff',
            headersforeground='#1e40af',
            foreground='#222',
            normalbackground='#fff',
            normalforeground='#222',
            weekendbackground='#e0e7ff',
            weekendforeground='#1e40af',
            othermonthbackground='#f3f4f6',
            othermonthwebackground='#e0e7ff',
            othermonthforeground='#d1d5db',
            othermonthweforeground='#d1d5db',
            selectbackground='#3B82F6',
            selectforeground='#fff',
            font=('Segoe UI', 12),
            disabledforeground='#d1d5db',
            borderwidth=0,
            showweeknumbers=False,
            cursor="hand2"
        )
        cal.pack(pady=0, padx=0, fill="both", expand=True)

        # Effet hover sur les jours
        def on_enter(e):
            e.widget.config(bg="#e0e7ff", font=("Segoe UI", 13, "bold"))
        def on_leave(e):
            e.widget.config(bg="#fff", font=("Segoe UI", 12))
        for day in cal._calendar.winfo_children():
            day.bind("<Enter>", on_enter)
            day.bind("<Leave>", on_leave)

        # Effet pulse sur le jour sélectionné
        def pulse(widget, count=0):
            if count < 4:
                size = 14 if count % 2 == 0 else 12
                widget.config(font=("Segoe UI", size, "bold"))
                widget.after(60, lambda: pulse(widget, count+1))

        # Bouton Valider
        def on_validate():
            try:
                date_str = cal.get_date()
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, date_str)
                # Pulse sur le jour sélectionné
                for day in cal._calendar.winfo_children():
                    if hasattr(day, 'cget') and day.cget('text') == str(cal.selection_get().day):
                        pulse(day)
                        break
            except Exception:
                pass
            cal_popup.after(120, cal_popup.destroy)
        validate_btn = ctk.CTkButton(cal_frame, text="Valider", fg_color="#3B82F6", hover_color="#2563EB", text_color="white", corner_radius=10, height=32, font=ctk.CTkFont(size=13, weight="bold"), command=on_validate)
        validate_btn.pack(pady=(6,0))

    def validate_and_generate(self):
        valid = True
        # Réinitialiser les erreurs
        for key in self.error_labels:
            self.error_labels[key].configure(text="")
        # Vérification des champs obligatoires
        if self.type_menu.get() == "Sélectionner un type":
            self.error_labels['type'].configure(text="Veuillez sélectionner un type de rapport.")
            valid = False
        if not self.nom_entry.get().strip():
            self.error_labels['nom'].configure(text="Veuillez saisir un nom de rapport.")
            valid = False
        if not self.date_debut.get().strip():
            self.error_labels['date_debut'].configure(text="Veuillez saisir la date de début.")
            valid = False
        if not self.date_fin.get().strip():
            self.error_labels['date_fin'].configure(text="Veuillez saisir la date de fin.")
            valid = False
        if valid:
            # Récupérer les données du formulaire
            report_data = {
                "type": self.type_menu.get(),
                "nom": self.nom_entry.get().strip(),
                "date_debut": self.date_debut.get().strip(),
                "date_fin": self.date_fin.get().strip(),
                "format_pdf": self.format_pdf.get(),
                "format_excel": self.format_excel.get(),
                "format_csv": self.format_csv.get(),
                "entrepot": self.entrepot_menu.get(),
                "categorie": self.categorie_menu.get(),
                "commentaire": self.comment_text.get("0.0", "end").strip()
            }
            self.show_loading_popup()
            self.after(1200, lambda: self.generate_report(report_data))

    def generate_report(self, report_data):
        import datetime
        import json
        import pandas as pd
        from fpdf import FPDF
        import os
        # Générer des données factices pour l'exemple
        data = [
            {"Produit": "Souris optique Dell", "Quantité": 50, "Date": report_data["date_debut"]},
            {"Produit": "Clavier USB HP", "Quantité": 10, "Date": report_data["date_fin"]}
        ]
        # Générer le nom de fichier de base
        base_name = report_data["nom"].replace(" ", "_") + "_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Export PDF
        if report_data["format_pdf"]:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt=report_data["nom"], ln=1, align="C")
            pdf.set_font("Arial", size=11)
            pdf.cell(200, 8, txt=f"Type: {report_data['type']} | Période: {report_data['date_debut']} - {report_data['date_fin']}", ln=2, align="C")
            pdf.ln(6)
            pdf.multi_cell(0, 8, f"Commentaire: {report_data['commentaire']}")
            pdf.ln(4)
            pdf.set_font("Arial", size=10)
            for row in data:
                pdf.cell(0, 8, txt=f"{row['Produit']} - Quantité: {row['Quantité']} - Date: {row['Date']}", ln=1)
            pdf_file = base_name + ".pdf"
            pdf.output(pdf_file)
        # Export Excel
        if report_data["format_excel"]:
            df = pd.DataFrame(data)
            excel_file = base_name + ".xlsx"
            df.to_excel(excel_file, index=False)
        # Export CSV
        if report_data["format_csv"]:
            df = pd.DataFrame(data)
            csv_file = base_name + ".csv"
            df.to_csv(csv_file, index=False)
        # Export JSON (toujours généré pour la démo)
        json_file = base_name + ".json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump({"rapport": report_data, "data": data}, f, ensure_ascii=False, indent=2)
        self.show_success_popup()

    def show_loading_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Génération en cours...")
        popup.geometry("500x260")
        popup.resizable(False, False)
        popup.configure(fg_color="white")
        popup.grab_set()
        # Icon
        icon_frame = ctk.CTkFrame(popup, fg_color="#e0e7ff", width=80, height=80, corner_radius=40)
        icon_frame.pack(pady=(24,0))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="📝", font=ctk.CTkFont(size=38), text_color="#1e40af").pack(expand=True)
        # Texte
        ctk.CTkLabel(popup, text="Génération en cours...", font=ctk.CTkFont(size=22, weight="bold"), text_color="#222").pack(pady=(18,0))
        ctk.CTkLabel(popup, text="Veuillez patienter pendant la création de votre rapport", font=ctk.CTkFont(size=15), text_color="#6B7280").pack(pady=(6,0))
        # Progress bar
        progress = ctk.CTkProgressBar(popup, width=420, height=12, progress_color="#1e40af")
        progress.pack(pady=(28,0))
        progress.set(0.0)
        # Finalisation
        final_label = ctk.CTkLabel(popup, text="Finalisation...", font=ctk.CTkFont(size=15), text_color="#6B7280")
        final_label.pack(pady=(18,0))
        def animate():
            for i in range(21):
                progress.set(i/20)
                popup.update_idletasks()
                time.sleep(0.08)
            time.sleep(0.5)
            popup.destroy()
            self.show_success_popup()
        threading.Thread(target=animate, daemon=True).start()

    def show_success_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Succès")
        popup.geometry("420x200")
        popup.resizable(False, False)
        popup.configure(fg_color="#fff0f6")
        popup.grab_set()
        ctk.CTkLabel(popup, text="📝", font=ctk.CTkFont(size=38), text_color="#be185d").pack(pady=(18,0))
        ctk.CTkLabel(popup, text=f"{self.nom_entry.get().strip()} généré avec succès !", font=ctk.CTkFont(size=18, weight="bold"), text_color="#be185d").pack(pady=(8,0))
        ctk.CTkLabel(popup, text="Le rapport a été ajouté à vos rapports récents et est prêt à être téléchargé.", font=ctk.CTkFont(size=14), text_color="#be185d").pack(pady=(4,0))
        ctk.CTkButton(popup, text="OK", fg_color="#f9a8d4", hover_color="#f472b6", text_color="#be185d", corner_radius=16, height=38, font=ctk.CTkFont(size=15, weight="bold"), command=lambda: (popup.destroy(), self.destroy())).pack(pady=18)

class ScheduleReportPopup(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.title("Programmer un Rapport")
        self.geometry("500x550")
        self.configure(fg_color="white")
        self.resizable(False, False)
        self.grab_set()

        ctk.CTkLabel(self, text="Programmer un Rapport", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # Type de rapport
        ctk.CTkLabel(content, text="Type de Rapport *").pack(anchor="w")
        report_types = ["Sélectionner un type", "Rapport de Performance", "Rapport des Stocks", "Rapport d'Activité"]
        self.report_type_menu = ctk.CTkOptionMenu(content, values=report_types, height=38)
        self.report_type_menu.pack(fill="x", pady=(0, 2))
        self.report_type_error = ctk.CTkLabel(content, text="", text_color="red", font=("Segoe UI", 12))
        self.report_type_error.pack(anchor="w", pady=(0, 10))

        # Fréquence
        ctk.CTkLabel(content, text="Fréquence *").pack(anchor="w")
        frequencies = ["Sélectionner une fréquence", "Quotidien", "Hebdomadaire", "Mensuel"]
        self.frequency_menu = ctk.CTkOptionMenu(content, values=frequencies, height=38)
        self.frequency_menu.pack(fill="x", pady=(0, 2))
        self.frequency_error = ctk.CTkLabel(content, text="", text_color="red", font=("Segoe UI", 12))
        self.frequency_error.pack(anchor="w", pady=(0, 10))

        # Destinataires
        ctk.CTkLabel(content, text="Destinataires (e-mails séparés par des virgules) *").pack(anchor="w")
        self.recipients_entry = ctk.CTkEntry(content, placeholder_text="exemple1@sac.com, exemple2@sac.com", height=38)
        self.recipients_entry.pack(fill="x", pady=(0, 2))
        self.recipients_error = ctk.CTkLabel(content, text="", text_color="red", font=("Segoe UI", 12))
        self.recipients_error.pack(anchor="w", pady=(0, 10))

        # Heure d'envoi
        ctk.CTkLabel(content, text="Heure d'envoi *").pack(anchor="w")
        time_frame = ctk.CTkFrame(content, fg_color="transparent")
        time_frame.pack(fill="x", pady=(0, 0))
        self.hour_spinbox = ctk.CTkEntry(time_frame, width=80, placeholder_text="HH")
        self.hour_spinbox.pack(side="left")
        ctk.CTkLabel(time_frame, text=":", font=ctk.CTkFont(size=20)).pack(side="left", padx=5)
        self.minute_spinbox = ctk.CTkEntry(time_frame, width=80, placeholder_text="MM")
        self.minute_spinbox.pack(side="left")
        self.time_error = ctk.CTkLabel(content, text="", text_color="red", font=("Segoe UI", 12))
        self.time_error.pack(anchor="w", pady=(0, 10))

        # Boutons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20, side="bottom")
        ctk.CTkButton(btn_frame, text="Annuler", command=self.destroy, fg_color="#EF5350", text_color="white", hover_color="#E53935", height=40).pack(side="left", expand=True, padx=(0,10))
        ctk.CTkButton(btn_frame, text="Programmer le Rapport", command=self.schedule, height=40).pack(side="left", expand=True)

    def schedule(self):
        # Reset errors
        self.report_type_error.configure(text="")
        self.frequency_error.configure(text="")
        self.recipients_error.configure(text="")
        self.time_error.configure(text="")
        
        is_valid = True
        
        if self.report_type_menu.get() == "Sélectionner un type":
            self.report_type_error.configure(text="Veuillez sélectionner un type de rapport.")
            is_valid = False
            
        if self.frequency_menu.get() == "Sélectionner une fréquence":
            self.frequency_error.configure(text="Veuillez sélectionner une fréquence.")
            is_valid = False
            
        if not self.recipients_entry.get().strip():
            self.recipients_error.configure(text="Veuillez entrer au moins un destinataire.")
            is_valid = False
            
        hour = self.hour_spinbox.get()
        minute = self.minute_spinbox.get()
        if not hour.isdigit() or not minute.isdigit() or not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
            self.time_error.configure(text="Heure invalide (HH:MM).")
            is_valid = False

        if not is_valid:
            return

        print("Rapport programmé !")
        self.destroy()

# Point d'entrée
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Rapports & Analytics")
    root.geometry("1400x950")
    RapportAnalyticsFrame(root)
    root.mainloop() 