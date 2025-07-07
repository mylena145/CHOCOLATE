import customtkinter as ctk
from PIL import Image, ImageTk
import os
import tkinter as tk
from stock_management_page import SidebarFrame
from tkinter import filedialog, messagebox
from datetime import datetime, date
import database

# Import des fonctions de base de données
try:
    from database import get_all_expeditions, add_expedition, update_expedition, delete_expedition, get_expedition_stats, search_expedition
    DB_AVAILABLE = True
except ImportError:
    print("⚠️ Base de données non disponible, utilisation des données de démonstration")
    DB_AVAILABLE = False

# Import optionnel pour éviter les erreurs
try:
    from responsive_utils import ThemeToggleButton
except ImportError:
    # Fallback si responsive_utils n'est pas disponible
    class ThemeToggleButton(ctk.CTkButton):
        def __init__(self, parent, app_instance, **kwargs):
            super().__init__(parent, text="☀️ Thème", width=100, height=32, command=lambda: print("Thème changé"), **kwargs)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class GestionExpeditionsApp(ctk.CTkFrame):
    def __init__(self, master=None, user_info=None):
        try:
            super().__init__(master)
            self.master = master
            self.user_info = user_info
            self.previous_page = getattr(master, 'last_page', None) if hasattr(master, 'last_page') else None
            self.configure(fg_color="white")
            
            # Données d'expéditions (sera rempli depuis la BD ou données de démonstration)
            self.expeditions_data = []
            self.expedition_stats = {}
            
            # Charger les données depuis la base de données
            self.load_expeditions_data()
            
            self.planning_frame = None  # Pour garder une référence au bloc planning
            self._build_interface()
            self._refresh_planning_periodically()  # Démarre le rafraîchissement auto
            self._auto_refresh_interval = 5000  # 5 secondes
            self._auto_refresh()
        except Exception as e:
            self._show_error(str(e))
    
    def load_expeditions_data(self):
        """Charge les données d'expéditions depuis la base de données"""
        try:
            if DB_AVAILABLE:
                # Récupérer les vraies données depuis la BD
                self.expeditions_data = get_all_expeditions()
                self.expedition_stats = get_expedition_stats()
                print(f"✅ {len(self.expeditions_data)} expéditions chargées depuis la base de données")
            else:
                # Données de démonstration si la BD n'est pas disponible
                self.expeditions_data = [
                    {
                        'id': 1,
                        'number': 'BE-2024-087',
                        'client': 'Entreprise ABC',
                        'shippingDate': '2024-03-15',
                        'deliveryDate': '2024-03-16',
                        'actualDeliveryDate': None,
                        'carrier': 'DHL Express',
                        'priority': 'haute',
                        'packages': 3,
                        'totalWeight': 12.5,
                        'status': 'shipped',
                        'trackingNumber': '1234567890'
                    },
                    {
                        'id': 2,
                        'number': 'BE-2024-086',
                        'client': 'Société XYZ',
                        'shippingDate': '2024-03-15',
                        'deliveryDate': '2024-03-17',
                        'actualDeliveryDate': None,
                        'carrier': 'Chronopost',
                        'priority': 'moyenne',
                        'packages': 5,
                        'totalWeight': 25.8,
                        'status': 'preparing',
                        'trackingNumber': None
                    }
                ]
                self.expedition_stats = {
                    "total": len(self.expeditions_data),
                    "en_preparation": 1,
                    "aujourd_hui": 1,
                    "livrees": 0,
                    "transporteurs": {"DHL Express": 1, "Chronopost": 1}
                }
                print("⚠️ Utilisation des données de démonstration")
            
            # Mettre à jour l'affichage si l'interface est déjà construite
            if hasattr(self, 'main_content'):
                self.update_expeditions_display()
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des données: {e}")
            # Fallback avec données minimales
            self.expeditions_data = []
            self.expedition_stats = {"total": 0, "en_preparation": 0, "aujourd_hui": 0, "livrees": 0, "transporteurs": {}}
    
    def update_expeditions_display(self):
        """Met à jour l'affichage des expéditions en temps réel"""
        try:
            print("🔄 Mise à jour de l'affichage des expéditions...")
            
            # Mettre à jour les statistiques
            if hasattr(self, 'stats_frame'):
                self.update_stats_display()
            
            # Mettre à jour le tableau
            if hasattr(self, 'table_frame'):
                self.update_table_display()
            
            # Mettre à jour les blocs centraux (planning et transporteurs)
            if hasattr(self, 'central_blocks_frame'):
                self.update_central_blocks()
                
            print("✅ Affichage des expéditions mis à jour avec succès")
                
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour de l'affichage: {e}")
    
    def update_central_blocks(self):
        """Met à jour les blocs centraux (planning et transporteurs)"""
        try:
            # Vider les blocs centraux existants
            for widget in self.central_blocks_frame.winfo_children():
                widget.destroy()
            
            # Recréer les blocs centraux avec les nouvelles données
            self.create_central_blocks()
            
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour des blocs centraux: {e}")
    
    def update_stats_display(self):
        """Met à jour l'affichage des statistiques"""
        try:
            # Mettre à jour les tuiles de statistiques
            if hasattr(self, 'total_expeditions_label'):
                self.total_expeditions_label.configure(text=str(self.expedition_stats.get("total", 0)))
            
            if hasattr(self, 'en_preparation_label'):
                self.en_preparation_label.configure(text=str(self.expedition_stats.get("en_preparation", 0)))
            
            if hasattr(self, 'aujourd_hui_label'):
                self.aujourd_hui_label.configure(text=str(self.expedition_stats.get("aujourd_hui", 0)))
            
            if hasattr(self, 'livrees_label'):
                self.livrees_label.configure(text=str(self.expedition_stats.get("livrees", 0)))
                
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour des stats: {e}")
    
    def update_table_display(self):
        """Met à jour l'affichage du tableau"""
        try:
            # Vider le tableau existant
            for widget in self.table_frame.winfo_children():
                widget.destroy()
            
            # Recréer le tableau avec les nouvelles données
            self.create_expeditions_table()
            
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour du tableau: {e}")
    
    def refresh_data(self):
        """Rafraîchit les données depuis la base en temps réel"""
        try:
            print("🔄 Rafraîchissement des données depuis la base...")
            
            # Recharger les données depuis la BD
            self.load_expeditions_data()
            
            # Mettre à jour complètement l'affichage
            self.update_expeditions_display()
            
            # Afficher une notification de succès
            if hasattr(self, 'master') and hasattr(self.master, 'show_notification'):
                self.master.show_notification("✅ Données rafraîchies avec succès")
            else:
                print("✅ Données rafraîchies avec succès")
                
        except Exception as e:
            print(f"❌ Erreur lors du rafraîchissement: {e}")
            if hasattr(self, 'master') and hasattr(self.master, 'show_notification'):
                self.master.show_notification("❌ Erreur lors du rafraîchissement")
    
    def _get_urgent_expeditions(self):
        """Récupère les expéditions urgentes (priorité haute ou livraison aujourd'hui)"""
        try:
            urgent_expeditions = []
            today = date.today()
            
            for exp in self.expeditions_data:
                # Expéditions avec priorité haute
                if exp.get('priority') == 'haute':
                    urgent_expeditions.append(exp)
                # Expéditions à livrer aujourd'hui
                elif exp.get('deliveryDate') == today.strftime('%Y-%m-%d'):
                    urgent_expeditions.append(exp)
                # Limiter à 3 expéditions urgentes
                if len(urgent_expeditions) >= 3:
                    break
            
            return urgent_expeditions
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des expéditions urgentes: {e}")
            return []
    
    def _get_today_planning(self):
        """Génère le planning du jour basé sur les expéditions réelles en temps réel"""
        try:
            today = date.today()
            today_str = today.strftime('%Y-%m-%d')
            
            # Récupérer les expéditions d'aujourd'hui depuis la BD en temps réel
            if DB_AVAILABLE:
                try:
                    # Requête directe à la BD pour les expéditions d'aujourd'hui
                    conn = psycopg2.connect(**PG_CONN)
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT 
                            be.id_bon_expedition,
                            be.client,
                            be.reference_commande,
                            be.date_livraison,
                            be.transporteurs,
                            be.observation,
                            be.liste_articles_livres
                        FROM sge_cre.bon_expeditions be
                        WHERE be.date_livraison = %s
                        ORDER BY be.transporteurs, be.id_bon_expedition
                    """, (today_str,))
                    
                    today_expeditions_db = cursor.fetchall()
                    conn.close()
                    
                    # Convertir au format attendu
                    today_expeditions = []
                    for exp in today_expeditions_db:
                        expedition_number = f"BE-2024-{exp[0]:03d}"
                        today_expeditions.append({
                            'id': exp[0],
                            'number': expedition_number,
                            'client': exp[1] if exp[1] else "Client non spécifié",
                            'carrier': exp[4] if exp[4] else "Non spécifié",
                            'observation': exp[5] if exp[5] else "",
                            'articles': exp[6] if exp[6] else ""
                        })
                    
                    print(f"📅 Planning temps réel : {len(today_expeditions)} expéditions pour aujourd'hui")
                    
                except Exception as e:
                    print(f"❌ Erreur requête BD planning: {e}")
                    # Fallback sur les données locales
                    today_expeditions = [exp for exp in self.expeditions_data if exp.get('deliveryDate') == today_str]
            else:
                # Mode démonstration
                today_expeditions = [exp for exp in self.expeditions_data if exp.get('deliveryDate') == today_str]
            
            if not today_expeditions:
                return []
            
            planning = []
            
            # Grouper par transporteur
            carriers = {}
            for exp in today_expeditions:
                carrier = exp.get('carrier', 'Non spécifié')
                if carrier not in carriers:
                    carriers[carrier] = []
                carriers[carrier].append(exp)
            
            # Créer le planning dynamique
            time_slots = [
                ("08:00 - 10:00", "Préparation commandes prioritaires"),
                ("10:00 - 12:00", "Enlèvement transporteurs"),
                ("14:00 - 16:00", "Préparation J+1"),
                ("16:00 - 18:00", "Clôture et vérifications")
            ]
            
            # Créer un planning basé sur les transporteurs réels
            carrier_list = list(carriers.keys())
            
            for i, (time, desc) in enumerate(time_slots):
                if i < len(carrier_list):
                    carrier_name = carrier_list[i]
                    exp_count = len(carriers[carrier_name])
                    
                    # Déterminer le statut selon l'heure actuelle
                    current_hour = datetime.now().hour
                    if time == "08:00 - 10:00" and current_hour < 10:
                        status = "En cours"
                        color = "#3867d6"
                    elif time == "10:00 - 12:00" and 10 <= current_hour < 12:
                        status = "En cours"
                        color = "#3867d6"
                    elif time == "14:00 - 16:00" and 14 <= current_hour < 16:
                        status = "En cours"
                        color = "#3867d6"
                    elif time == "16:00 - 18:00" and 16 <= current_hour < 18:
                        status = "En cours"
                        color = "#3867d6"
                    elif current_hour > 18:
                        status = "Terminé"
                        color = "#20bf6b"
                    else:
                        status = "Planifié"
                        color = "#f7b731"
                    
                    # Ajouter des détails sur les expéditions
                    exp_details = []
                    for exp in carriers[carrier_name][:3]:  # Limiter à 3 expéditions par créneau
                        exp_details.append(f"{exp['number']} ({exp['client']})")
                    
                    details_text = f"{desc} - {carrier_name}"
                    if exp_details:
                        details_text += f" - {', '.join(exp_details)}"
                    
                    planning.append({
                        "heure": time,
                        "desc": details_text,
                        "statut": f"{status} ({exp_count} colis)",
                        "color": color
                    })
                elif i == 0:  # Premier créneau même sans transporteur
                    planning.append({
                        "heure": time,
                        "desc": desc,
                        "statut": "Aucune expédition",
                        "color": "#6b7280"
                    })
            
            return planning
        except Exception as e:
            print(f"❌ Erreur lors de la génération du planning temps réel: {e}")
            return []
    
    def _get_carrier_stats(self):
        """Récupère les statistiques des transporteurs"""
        try:
            if not hasattr(self, 'expedition_stats') or not self.expedition_stats.get('transporteurs'):
                return []
            
            carriers = self.expedition_stats['transporteurs']
            carrier_list = []
            
            # Définir les couleurs pour les transporteurs
            colors = ["#20bf6b", "#3867d6", "#f7b731", "#e74c3c", "#9b59b6"]
            
            for i, (carrier_name, count) in enumerate(carriers.items()):
                if i >= len(colors):
                    break
                
                # Déterminer le statut basé sur le nombre de colis
                if count > 5:
                    status = "Actif"
                    color = colors[i]
                elif count > 0:
                    status = "En attente"
                    color = "#f7b731"
                else:
                    status = "Inactif"
                    color = "#6b7280"
                
                carrier_list.append({
                    "nom": carrier_name,
                    "statut": status,
                    "colis": str(count),
                    "color": color
                })
            
            return carrier_list
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des stats transporteurs: {e}")
            return []

    def _build_interface(self):
        """Construction de l'interface"""
        # Topbar - TOUJOURS VISIBLE
        self._build_topbar()
        
        # Contenu principal
        self._build_main_content()

    def _build_topbar(self):
        """Construction de la barre supérieure - TOUJOURS VISIBLE"""
        # Topbar fixe en haut
        self.topbar = ctk.CTkFrame(self, height=80, fg_color='#F7F9FC', border_width=1, border_color='#E0E0E0')
        self.topbar.pack(side='top', fill='x', pady=(0, 0))
        
        # Logo et titre
        try:
            logo_img = Image.open('logo.png')
            logo = ctk.CTkImage(light_image=logo_img, size=(60, 60))
            ctk.CTkLabel(self.topbar, image=logo, text='').pack(side='left', padx=25, pady=10)
        except:
            ctk.CTkLabel(self.topbar, text='SGE', font=ctk.CTkFont(size=24, weight='bold'), text_color='#333333').pack(side='left', padx=25)
        
        # Titre principal
        title_frame = ctk.CTkFrame(self.topbar, fg_color='transparent')
        title_frame.pack(side='left', padx=(20, 0))
        
        ctk.CTkLabel(title_frame, text='Gestion des Expéditions', font=ctk.CTkFont(size=24, weight='bold'), text_color='#333333').pack(anchor='w')
        ctk.CTkLabel(title_frame, text="Gérez les bons d'expédition et les livraisons", font=ctk.CTkFont(size=16), text_color='#666666').pack(anchor='w')
        
        # Bouton de rafraîchissement
        refresh_button = ctk.CTkButton(
            self.topbar, 
            text="🔄 Rafraîchir", 
            width=120, 
            height=32, 
            fg_color="#3b82f6", 
            hover_color="#2563eb",
            text_color="white",
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8,
            command=self.refresh_data
        )
        refresh_button.pack(side='right', padx=(10, 10), pady=10)
        
        # Bouton de thème
        try:
            self.theme_button = ThemeToggleButton(self.topbar, self.master)
            self.theme_button.pack(side='right', padx=(0, 20), pady=10)
        except Exception as e:
            print(f"Erreur bouton thème: {e}")
            # Bouton de thème simplifié
            theme_btn = ctk.CTkButton(self.topbar, text="☀️ Thème", width=100, height=32, command=self._toggle_theme)
            theme_btn.pack(side='right', padx=(0, 20), pady=10)
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(self.topbar, fg_color='transparent')
        buttons_frame.pack(side='right', padx=25, pady=10)
        
        btns = [
            ("+ Nouvelle Expédition", "#2563eb", self.open_new_expedition_modal),
            ("Planning", "#a21caf", self.action_planning),
            ("Suivi", "#059669", self.open_tracking_modal),
            ("⭳ Exporter", "#22c55e", self.action_export),
        ]
        
        for txt, color, cmd in btns:
            btn = ctk.CTkButton(buttons_frame, text=txt, width=120, height=58, fg_color=color, hover_color=color, text_color="white", font=ctk.CTkFont(size=16, weight="bold"), corner_radius=12, command=cmd)
            btn.pack(side='left', padx=5)

        # Ajout du bouton retour intelligent en haut à gauche
        topbar = ctk.CTkFrame(self, fg_color="transparent")
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

    def _build_main_content(self):
        """Construction du contenu principal"""
        # Frame principal avec scroll
        self.main_content = ctk.CTkScrollableFrame(self, fg_color='white')
        self.main_content.pack(side='top', fill='both', expand=True, padx=20, pady=20)

        # Tuiles statistiques
        self.create_stat_tiles()

        # Blocs centraux
        self.create_central_blocks()

        # Tableau des expéditions
        self.create_expedition_table()

    def _toggle_theme(self):
        """Basculement simple du thème"""
        current = ctk.get_appearance_mode()
        new_theme = "dark" if current == "light" else "light"
        ctk.set_appearance_mode(new_theme)
        print(f"Thème changé vers: {new_theme}")

    def create_stat_tiles(self):
        """Création des tuiles statistiques"""
        # Titre de section
        title_label = ctk.CTkLabel(self.main_content, text="Statistiques", font=ctk.CTkFont(size=20, weight="bold"), text_color="#1f2937")
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Frame pour les tuiles
        stats_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Utiliser les vraies statistiques si disponibles
        if hasattr(self, 'expedition_stats') and self.expedition_stats:
            stats = [
                {"label": "En Préparation", "value": str(self.expedition_stats.get("en_preparation", 0)), "desc": "À préparer", "color": "#f7b731", "icon": "📦"},
                {"label": "Expédiées Aujourd'hui", "value": str(self.expedition_stats.get("aujourd_hui", 0)), "desc": "En transit", "color": "#3867d6", "icon": "🚚"},
                {"label": "Livrées", "value": str(self.expedition_stats.get("livrees", 0)), "desc": "Ce mois", "color": "#20bf6b", "icon": "✅"},
                {"label": "Total", "value": str(self.expedition_stats.get("total", 0)), "desc": "Toutes les expéditions", "color": "#eb3b5a", "icon": "📊"},
            ]
        else:
            # Statistiques par défaut
            stats = [
                {"label": "En Préparation", "value": "0", "desc": "À préparer", "color": "#f7b731", "icon": "📦"},
                {"label": "Expédiées Aujourd'hui", "value": "0", "desc": "En transit", "color": "#3867d6", "icon": "🚚"},
                {"label": "Livrées", "value": "0", "desc": "Ce mois", "color": "#20bf6b", "icon": "✅"},
                {"label": "Total", "value": "0", "desc": "Toutes les expéditions", "color": "#eb3b5a", "icon": "📊"},
            ]
        
        # Créer une grille responsive
        for i, stat in enumerate(stats):
            # Frame de la tuile
            frame = ctk.CTkFrame(stats_frame, fg_color="white", border_width=1, border_color="#eee", corner_radius=8)
            frame.pack(side="left", expand=True, fill="x", padx=10, pady=5)
            
            # Contenu de la tuile
            content_frame = ctk.CTkFrame(frame, fg_color="transparent")
            content_frame.pack(padx=15, pady=15, fill="x")
            
            # Icône
            icon_frame = ctk.CTkFrame(content_frame, fg_color=stat["color"], width=40, height=40, corner_radius=8)
            icon_frame.pack(side="left", padx=(0, 15))
            icon_frame.pack_propagate(False)
            
            ctk.CTkLabel(icon_frame, text=stat["icon"], font=ctk.CTkFont(size=20), text_color="white", fg_color="transparent").pack(expand=True)
            
            # Texte
            text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(text_frame, text=stat["label"], font=ctk.CTkFont(size=13), text_color="#444").pack(anchor="w")
            ctk.CTkLabel(text_frame, text=stat["value"], font=ctk.CTkFont(size=24, weight="bold"), text_color=stat["color"]).pack(anchor="w")
            ctk.CTkLabel(text_frame, text=stat["desc"], font=ctk.CTkFont(size=12), text_color=stat["color"]).pack(anchor="w")

    def create_central_blocks(self):
        """Création des blocs centraux"""
        # Titre de section
        title_label = ctk.CTkLabel(self.main_content, text="Vue d'ensemble", font=ctk.CTkFont(size=20, weight="bold"), text_color="#1f2937")
        title_label.pack(anchor="w", pady=(20, 15))
        
        # Frame pour les blocs
        blocks_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        blocks_frame.pack(fill="x", pady=(0, 20))
        
        # Expéditions Urgentes
        urgentes_frame = ctk.CTkFrame(blocks_frame, fg_color="white", border_width=1, border_color="#eee", corner_radius=8)
        urgentes_frame.pack(side="left", expand=True, fill="both", padx=10, pady=5)
        
        ctk.CTkLabel(urgentes_frame, text="🚨 Expéditions Urgentes", font=ctk.CTkFont(size=18, weight="bold"), text_color="#b91c1c").pack(anchor="w", padx=15, pady=15)
        
        # Récupérer les expéditions urgentes depuis les données réelles
        urgent_expeditions = self._get_urgent_expeditions()
        
        if urgent_expeditions:
            for exp in urgent_expeditions:
                card = ctk.CTkFrame(urgentes_frame, fg_color="#fef2f2", border_width=2, border_color="#fecaca", corner_radius=8)
                card.pack(fill="x", padx=15, pady=5)
                ctk.CTkLabel(card, text=exp["number"], font=ctk.CTkFont(size=16, weight="bold"), text_color="#b91c1c", fg_color="transparent").pack(anchor="w", padx=10, pady=(5,0))
                ctk.CTkLabel(card, text=f"{exp['client']} - {exp['carrier']}", font=ctk.CTkFont(size=15), text_color="#b91c1c", fg_color="transparent").pack(anchor="w", padx=10, pady=(2,0))
                ctk.CTkLabel(card, text=exp["priority"].upper(), font=ctk.CTkFont(size=14, weight="bold"), text_color="#b91c1c", fg_color="transparent").pack(anchor="e", padx=10, pady=(0,5))
        else:
            # Message si aucune expédition urgente
            no_urgent_frame = ctk.CTkFrame(urgentes_frame, fg_color="#f9fafb", corner_radius=8)
            no_urgent_frame.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(no_urgent_frame, text="✅ Aucune expédition urgente", font=ctk.CTkFont(size=14), text_color="#059669", fg_color="transparent").pack(pady=10)

        # Planning du Jour
        if self.planning_frame:
            self.planning_frame.destroy()
        self.planning_frame = ctk.CTkFrame(blocks_frame, fg_color="white", border_width=1, border_color="#eee", corner_radius=8)
        self.planning_frame.pack(side="left", expand=True, fill="both", padx=10, pady=5)
        ctk.CTkLabel(self.planning_frame, text="📅 Planning du Jour", font=ctk.CTkFont(size=18, weight="bold"), text_color="#3867d6").pack(anchor="w", padx=15, pady=15)
        today_planning = self._get_today_planning()
        if today_planning:
            for planning in today_planning:
                item_frame = ctk.CTkFrame(self.planning_frame, fg_color="transparent")
                item_frame.pack(fill="x", padx=15, pady=5)
                ctk.CTkLabel(item_frame, text=planning["heure"], font=ctk.CTkFont(size=16, weight="bold"), text_color="#222").pack(anchor="w")
                ctk.CTkLabel(item_frame, text=planning["desc"], font=ctk.CTkFont(size=15), text_color="#555").pack(anchor="w")
                ctk.CTkLabel(item_frame, text=planning["statut"], font=ctk.CTkFont(size=14), text_color=planning["color"]).pack(anchor="e")
        else:
            no_planning_frame = ctk.CTkFrame(self.planning_frame, fg_color="#f9fafb", corner_radius=8)
            no_planning_frame.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(no_planning_frame, text="📅 Aucune expédition prévue aujourd'hui", font=ctk.CTkFont(size=14), text_color="#6b7280", fg_color="transparent").pack(pady=10)

        # Transporteurs
        transp_frame = ctk.CTkFrame(blocks_frame, fg_color="white", border_width=1, border_color="#eee", corner_radius=8)
        transp_frame.pack(side="left", expand=True, fill="both", padx=10, pady=5)
        
        ctk.CTkLabel(transp_frame, text="🚛 Transporteurs", font=ctk.CTkFont(size=18, weight="bold"), text_color="#20bf6b").pack(anchor="w", padx=15, pady=15)
        
        # Récupérer les statistiques des transporteurs depuis les données réelles
        carrier_stats = self._get_carrier_stats()
        
        if carrier_stats:
            for carrier in carrier_stats:
                item_frame = ctk.CTkFrame(transp_frame, fg_color="transparent")
                item_frame.pack(fill="x", padx=15, pady=5)
                ctk.CTkLabel(item_frame, text=carrier["nom"], font=ctk.CTkFont(size=16, weight="bold"), text_color="#222").pack(anchor="w")
                ctk.CTkLabel(item_frame, text=f"Statut: {carrier['statut']}", font=ctk.CTkFont(size=15), text_color=carrier["color"]).pack(anchor="w")
                ctk.CTkLabel(item_frame, text=f"{carrier['colis']} colis", font=ctk.CTkFont(size=14), text_color="#666").pack(anchor="e")
        else:
            # Message si aucun transporteur
            no_carrier_frame = ctk.CTkFrame(transp_frame, fg_color="#f9fafb", corner_radius=8)
            no_carrier_frame.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(no_carrier_frame, text="🚛 Aucun transporteur configuré", font=ctk.CTkFont(size=14), text_color="#6b7280", fg_color="transparent").pack(pady=10)

    def create_expedition_table(self):
        """Création du tableau des expéditions"""
        # Titre du tableau
        table_title = ctk.CTkLabel(self.main_content, text="Liste des Expéditions", font=ctk.CTkFont(size=20, weight="bold"), text_color="#1f2937")
        table_title.pack(anchor="w", pady=(20, 10))
        
        # Frame du tableau
        self.table_frame = ctk.CTkFrame(self.main_content, fg_color="white", corner_radius=8, border_width=1, border_color="#e5e7eb")
        self.table_frame.pack(fill="x", pady=(0, 20))
        
        # Créer le contenu du tableau
        self.create_expeditions_table()
    
    def create_expeditions_table(self):
        """Crée le contenu du tableau des expéditions"""
        # Vider le tableau existant
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # En-têtes
        headers = ["N° Expédition", "Client", "Transporteur", "Priorité", "Statut", "Poids (kg)", "Actions"]
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="#f8fafc")
        header_frame.pack(fill="x", padx=1, pady=1)
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(header_frame, text=header, font=ctk.CTkFont(size=13, weight="bold"), text_color="#374151")
            label.grid(row=0, column=i, sticky="ew", padx=15, pady=12)
            header_frame.grid_columnconfigure(i, weight=1)
        
        # Message si aucune expédition
        if not self.expeditions_data:
            no_data_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            no_data_frame.pack(fill="x", padx=1, pady=20)
            
            ctk.CTkLabel(
                no_data_frame, 
                text="📦 Aucune expédition trouvée", 
                font=ctk.CTkFont(size=16, weight="bold"), 
                text_color="#6b7280"
            ).pack(pady=20)
            
            ctk.CTkLabel(
                no_data_frame, 
                text="Cliquez sur 'Nouvelle Expédition' pour commencer", 
                font=ctk.CTkFont(size=14), 
                text_color="#9ca3af"
            ).pack()
            return
        
        # Données
        for row_idx, expedition in enumerate(self.expeditions_data):
            row_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=1, pady=1)
            
            # Couleur de fond alternée
            if row_idx % 2 == 0:
                row_frame.configure(fg_color="#f9fafb")
            
            # Données de la ligne
            row_data = [
                expedition['number'],
                expedition['client'],
                expedition['carrier'],
                expedition['priority'].title(),
                expedition['status'].title(),
                f"{expedition['totalWeight']} kg"
            ]
            
            for col_idx, cell_data in enumerate(row_data):
                label = ctk.CTkLabel(row_frame, text=str(cell_data), font=ctk.CTkFont(size=12), text_color="#6b7280")
                label.grid(row=0, column=col_idx, sticky="ew", padx=15, pady=8)
                row_frame.grid_columnconfigure(col_idx, weight=1)
            
            # Boutons d'action
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.grid(row=0, column=6, sticky="ew", padx=15, pady=8)
            
            ctk.CTkButton(actions_frame, text="👁️", width=30, height=25, command=lambda e=expedition: self.view_expedition(e)).pack(side="left", padx=2)
            ctk.CTkButton(actions_frame, text="✏️", width=30, height=25, command=lambda e=expedition: self.edit_expedition(e)).pack(side="left", padx=2)
            ctk.CTkButton(actions_frame, text="🗑️", width=30, height=25, command=lambda e=expedition: self.delete_expedition(e)).pack(side="left", padx=2)

    def view_expedition(self, expedition):
        """Afficher les détails d'une expédition"""
        print(f"Affichage de l'expédition: {expedition['number']}")

    def edit_expedition(self, expedition):
        """Modifier une expédition"""
        print(f"Modification de l'expédition: {expedition['number']}")
        
        # Créer une fenêtre modale
        modal = ctk.CTkToplevel(self)
        modal.title("Modifier l'Expédition")
        modal.geometry("800x600")
        modal.configure(fg_color='white')
        modal.grab_set()
        modal.resizable(False, False)
        
        # Titre
        title_label = ctk.CTkLabel(modal, text=f"✏️ Modifier l'Expédition {expedition['number']}", font=ctk.CTkFont(size=24, weight="bold"), text_color="#1f2937")
        title_label.pack(pady=(20, 30))
        
        # Frame principal avec scroll
        main_frame = ctk.CTkScrollableFrame(modal, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Formulaire
        form_frame = ctk.CTkFrame(main_frame, fg_color="white", border_width=1, border_color="#e5e7eb", corner_radius=8)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Titre du formulaire
        ctk.CTkLabel(form_frame, text="Informations de l'expédition", font=ctk.CTkFont(size=18, weight="bold"), text_color="#374151").pack(anchor="w", padx=20, pady=(20, 15))
        
        # Grille pour les champs
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Variables pour les champs (pré-remplies avec les données actuelles)
        client_var = tk.StringVar(value=expedition.get('client', ''))
        carrier_var = tk.StringVar(value=expedition.get('carrier', 'DHL Express'))
        priority_var = tk.StringVar(value=expedition.get('priority', 'moyenne'))
        weight_var = tk.StringVar(value=str(expedition.get('totalWeight', '')))
        packages_var = tk.StringVar(value=str(expedition.get('packages', '')))
        observation_var = tk.StringVar(value=expedition.get('observation', ''))
        status_var = tk.StringVar(value=expedition.get('status', 'preparing'))
        
        # Champs du formulaire
        fields = [
            ("Client:", client_var, "text"),
            ("Transporteur:", carrier_var, "combo", ["DHL Express", "Chronopost", "Colissimo", "UPS"]),
            ("Priorité:", priority_var, "combo", ["haute", "moyenne", "basse"]),
            ("Statut:", status_var, "combo", ["preparing", "in-transit", "delivered"]),
            ("Poids (kg):", weight_var, "text"),
            ("Nombre de colis:", packages_var, "text"),
        ]
        
        for i, (label, var, field_type, *args) in enumerate(fields):
            row = i // 2
            col = i % 2
            
            # Label
            ctk.CTkLabel(fields_frame, text=label, font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").grid(row=row*2, column=col, sticky="w", padx=(0, 10), pady=(15, 5))
            
            # Champ
            if field_type == "text":
                entry = ctk.CTkEntry(fields_frame, textvariable=var, width=200, height=35, font=ctk.CTkFont(size=14))
                entry.grid(row=row*2+1, column=col, sticky="ew", padx=(0, 20), pady=(0, 15))
            elif field_type == "combo":
                combo = ctk.CTkOptionMenu(fields_frame, variable=var, values=args[0], width=200, height=35, font=ctk.CTkFont(size=14))
                combo.grid(row=row*2+1, column=col, sticky="ew", padx=(0, 20), pady=(0, 15))
            
            fields_frame.grid_columnconfigure(col, weight=1)
        
        # Champ observation (pleine largeur)
        ctk.CTkLabel(fields_frame, text="Observation:", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").grid(row=len(fields)*2, column=0, columnspan=2, sticky="w", padx=(0, 10), pady=(15, 5))
        observation_entry = ctk.CTkEntry(fields_frame, textvariable=observation_var, width=400, height=35, font=ctk.CTkFont(size=14))
        observation_entry.grid(row=len(fields)*2+1, column=0, columnspan=2, sticky="ew", padx=(0, 20), pady=(0, 15))
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(modal, fg_color="transparent")
        buttons_frame.pack(pady=(0, 20))
        
        def update_expedition():
            """Mettre à jour l'expédition"""
            if not client_var.get() or not weight_var.get() or not packages_var.get():
                # Afficher une erreur
                error_label = ctk.CTkLabel(modal, text="❌ Veuillez remplir tous les champs obligatoires", text_color="#ef4444", font=ctk.CTkFont(size=14))
                error_label.pack(pady=10)
                modal.after(3000, error_label.destroy)
                return
            
            # Préparer les données pour la BD
            expedition_data = {
                'client': client_var.get(),
                'reference_commande': expedition.get('trackingNumber', ''),
                'date_livraison': expedition.get('deliveryDate', datetime.now().strftime('%Y-%m-%d')),
                'transporteurs': carrier_var.get(),
                'observation': observation_var.get(),
                'liste_articles_livres': expedition.get('articles', '')
            }
            
            try:
                if DB_AVAILABLE:
                    # Mettre à jour dans la base de données
                    success = update_expedition(expedition['id'], expedition_data)
                    if success:
                        print(f"✅ Expédition mise à jour dans la BD: {expedition['number']}")
                        # Recharger les données
                        self.load_expeditions_data()
                        # Mettre à jour l'affichage
                        self.update_expeditions_display()
                        success_msg = "✅ Expédition mise à jour avec succès !"
                    else:
                        print("❌ Erreur lors de la mise à jour dans la BD")
                        success_msg = "❌ Erreur lors de la mise à jour"
                else:
                    # Mode démonstration
                    self._update_local_expedition(expedition['id'], expedition_data)
                    success_msg = "✅ Expédition mise à jour (mode démonstration)"
                
                # Afficher un message de succès
                success_label = ctk.CTkLabel(modal, text=success_msg, text_color="#10b981" if "succès" in success_msg else "#ef4444", font=ctk.CTkFont(size=16, weight="bold"))
                success_label.pack(pady=10)
                
                # Fermer la modal après 2 secondes
                modal.after(2000, modal.destroy)
                    
            except Exception as e:
                print(f"❌ Erreur lors de la mise à jour: {e}")
                error_label = ctk.CTkLabel(modal, text=f"❌ Erreur: {str(e)}", text_color="#ef4444", font=ctk.CTkFont(size=14))
                error_label.pack(pady=10)
                modal.after(3000, error_label.destroy)
        
        def cancel_update():
            """Annuler la modification"""
            modal.destroy()
        
        # Boutons
        ctk.CTkButton(buttons_frame, text="❌ Annuler", width=120, height=40, fg_color="#ef4444", hover_color="#dc2626", command=cancel_update).pack(side="left", padx=10)
        ctk.CTkButton(buttons_frame, text="✅ Mettre à jour", width=150, height=40, fg_color="#10b981", hover_color="#059669", command=update_expedition).pack(side="left", padx=10)

    def delete_expedition(self, expedition):
        """Supprimer une expédition"""
        print(f"Suppression de l'expédition: {expedition['number']}")
        
        # Créer une fenêtre de confirmation
        modal = ctk.CTkToplevel(self)
        modal.title("Confirmer la suppression")
        modal.geometry("500x300")
        modal.configure(fg_color='white')
        modal.grab_set()
        modal.resizable(False, False)
        
        # Titre
        title_label = ctk.CTkLabel(modal, text="🗑️ Supprimer l'Expédition", font=ctk.CTkFont(size=24, weight="bold"), text_color="#1f2937")
        title_label.pack(pady=(20, 20))
        
        # Message de confirmation
        message = f"Êtes-vous sûr de vouloir supprimer l'expédition {expedition['number']} ?\n\nCette action est irréversible."
        message_label = ctk.CTkLabel(modal, text=message, font=ctk.CTkFont(size=16), text_color="#6b7280", justify="center")
        message_label.pack(pady=(0, 30))
        
        # Détails de l'expédition
        details_frame = ctk.CTkFrame(modal, fg_color="#f3f4f6", corner_radius=8)
        details_frame.pack(fill="x", padx=20, pady=(0, 30))
        
        details_text = f"Client: {expedition.get('client', 'N/A')}\nTransporteur: {expedition.get('carrier', 'N/A')}\nStatut: {expedition.get('status', 'N/A')}"
        details_label = ctk.CTkLabel(details_frame, text=details_text, font=ctk.CTkFont(size=14), text_color="#374151", justify="left")
        details_label.pack(padx=15, pady=15)
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(modal, fg_color="transparent")
        buttons_frame.pack(pady=(0, 20))
        
        def confirm_delete():
            """Confirmer la suppression"""
            try:
                if DB_AVAILABLE:
                    # Supprimer de la base de données
                    success = delete_expedition(expedition['id'])
                    if success:
                        print(f"✅ Expédition supprimée de la BD: {expedition['number']}")
                        # Recharger les données
                        self.load_expeditions_data()
                        # Mettre à jour l'affichage
                        self.update_expeditions_display()
                        success_msg = "✅ Expédition supprimée avec succès !"
                    else:
                        print("❌ Erreur lors de la suppression dans la BD")
                        success_msg = "❌ Erreur lors de la suppression"
                else:
                    # Mode démonstration
                    self._delete_local_expedition(expedition['id'])
                    success_msg = "✅ Expédition supprimée (mode démonstration)"
                
                # Fermer la modal de confirmation
                modal.destroy()
                
                # Afficher un message de succès
                success_modal = ctk.CTkToplevel(self)
                success_modal.title("Suppression terminée")
                success_modal.geometry("400x200")
                success_modal.configure(fg_color='white')
                success_modal.grab_set()
                success_modal.resizable(False, False)
                
                ctk.CTkLabel(success_modal, text=success_msg, text_color="#10b981" if "succès" in success_msg else "#ef4444", font=ctk.CTkFont(size=16, weight="bold")).pack(expand=True)
                success_modal.after(2000, success_modal.destroy)
                    
            except Exception as e:
                print(f"❌ Erreur lors de la suppression: {e}")
                modal.destroy()
                
                # Afficher un message d'erreur
                error_modal = ctk.CTkToplevel(self)
                error_modal.title("Erreur")
                error_modal.geometry("400x200")
                error_modal.configure(fg_color='white')
                error_modal.grab_set()
                error_modal.resizable(False, False)
                
                ctk.CTkLabel(error_modal, text=f"❌ Erreur: {str(e)}", text_color="#ef4444", font=ctk.CTkFont(size=16, weight="bold")).pack(expand=True)
                error_modal.after(3000, error_modal.destroy)
        
        def cancel_delete():
            """Annuler la suppression"""
            modal.destroy()
        
        # Boutons
        ctk.CTkButton(buttons_frame, text="❌ Annuler", width=120, height=40, fg_color="#6b7280", hover_color="#4b5563", command=cancel_delete).pack(side="left", padx=10)
        ctk.CTkButton(buttons_frame, text="🗑️ Supprimer", width=120, height=40, fg_color="#ef4444", hover_color="#dc2626", command=confirm_delete).pack(side="left", padx=10)

    def open_new_expedition_modal(self):
        """Ouvrir la modal de nouvelle expédition"""
        print("Ouverture de la modal nouvelle expédition")
        
        # Créer une fenêtre modale
        modal = ctk.CTkToplevel(self)
        modal.title("Nouvelle Expédition")
        modal.geometry("800x600")
        modal.configure(fg_color='white')
        modal.grab_set()  # Rendre la fenêtre modale
        modal.resizable(False, False)
        
        # Titre
        title_label = ctk.CTkLabel(modal, text="📦 Nouvelle Expédition", font=ctk.CTkFont(size=24, weight="bold"), text_color="#1f2937")
        title_label.pack(pady=(20, 30))
        
        # Frame principal avec scroll
        main_frame = ctk.CTkScrollableFrame(modal, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Formulaire
        form_frame = ctk.CTkFrame(main_frame, fg_color="white", border_width=1, border_color="#e5e7eb", corner_radius=8)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Titre du formulaire
        ctk.CTkLabel(form_frame, text="Informations de l'expédition", font=ctk.CTkFont(size=18, weight="bold"), text_color="#374151").pack(anchor="w", padx=20, pady=(20, 15))
        
        # Grille pour les champs
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Variables pour les champs
        client_var = tk.StringVar(value="")
        carrier_var = tk.StringVar(value="DHL Express")
        priority_var = tk.StringVar(value="moyenne")
        weight_var = tk.StringVar(value="")
        packages_var = tk.StringVar(value="")
        
        # Champs du formulaire
        fields = [
            ("Client:", client_var, "text"),
            ("Transporteur:", carrier_var, "combo", ["DHL Express", "Chronopost", "Colissimo", "UPS"]),
            ("Priorité:", priority_var, "combo", ["haute", "moyenne", "basse"]),
            ("Poids (kg):", weight_var, "text"),
            ("Nombre de colis:", packages_var, "text"),
        ]
        
        for i, (label, var, field_type, *args) in enumerate(fields):
            row = i // 2
            col = i % 2
            
            # Label
            ctk.CTkLabel(fields_frame, text=label, font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").grid(row=row*2, column=col, sticky="w", padx=(0, 10), pady=(15, 5))
            
            # Champ
            if field_type == "text":
                entry = ctk.CTkEntry(fields_frame, textvariable=var, width=200, height=35, font=ctk.CTkFont(size=14))
                entry.grid(row=row*2+1, column=col, sticky="ew", padx=(0, 20), pady=(0, 15))
            elif field_type == "combo":
                combo = ctk.CTkOptionMenu(fields_frame, variable=var, values=args[0], width=200, height=35, font=ctk.CTkFont(size=14))
                combo.grid(row=row*2+1, column=col, sticky="ew", padx=(0, 20), pady=(0, 15))
            
            fields_frame.grid_columnconfigure(col, weight=1)
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(modal, fg_color="transparent")
        buttons_frame.pack(pady=(0, 20))
        
        def create_expedition():
            """Créer l'expédition"""
            if not client_var.get() or not weight_var.get() or not packages_var.get():
                # Afficher une erreur
                error_label = ctk.CTkLabel(modal, text="❌ Veuillez remplir tous les champs obligatoires", text_color="#ef4444", font=ctk.CTkFont(size=14))
                error_label.pack(pady=10)
                modal.after(3000, error_label.destroy)
                return
            
            # Préparer les données pour la BD
            expedition_data = {
                'client': client_var.get(),
                'reference_commande': f"REF-{datetime.now().strftime('%Y%m%d%H%M')}",
                'date_livraison': datetime.now().strftime('%Y-%m-%d'),
                'transporteurs': carrier_var.get(),
                'observation': f"Poids: {weight_var.get()}kg, Colis: {packages_var.get()}",
                'liste_articles_livres': ''
            }
            
            try:
                if DB_AVAILABLE:
                    # Créer dans la base de données
                    expedition_id = add_expedition(expedition_data)
                    if expedition_id:
                        print(f"✅ Expédition créée dans la BD avec l'ID: {expedition_id}")
                        # Recharger les données
                        self.load_expeditions_data()
                        # Mettre à jour l'affichage
                        self.update_expeditions_display()
                        success_msg = "✅ Expédition créée avec succès !"
                    else:
                        print("❌ Erreur lors de la création dans la BD")
                        success_msg = "❌ Erreur lors de la création"
                else:
                    # Mode démonstration
                    self._add_local_expedition(expedition_data)
                    success_msg = "✅ Expédition créée (mode démonstration)"
                
                # Afficher un message de succès
                success_label = ctk.CTkLabel(modal, text=success_msg, text_color="#10b981" if "succès" in success_msg else "#ef4444", font=ctk.CTkFont(size=16, weight="bold"))
                success_label.pack(pady=10)
                
                # Fermer la modal après 2 secondes
                modal.after(2000, modal.destroy)
                    
            except Exception as e:
                print(f"❌ Erreur lors de la création: {e}")
                # Fallback avec données locales
                self._add_local_expedition(expedition_data)
                success_label = ctk.CTkLabel(modal, text="✅ Expédition créée (mode démonstration)", text_color="#10b981", font=ctk.CTkFont(size=16, weight="bold"))
                success_label.pack(pady=10)
                modal.after(2000, modal.destroy)
        
        def _add_local_expedition(expedition_data):
            """Ajoute une expédition en mode local (démonstration)"""
            new_expedition = {
                'id': len(self.expeditions_data) + 1,
                'number': f'BE-2024-{len(self.expeditions_data) + 1:03d}',
                'client': expedition_data['client'],
                'shippingDate': datetime.now().strftime('%Y-%m-%d'),
                'deliveryDate': expedition_data['date_livraison'],
                'actualDeliveryDate': None,
                'carrier': expedition_data['transporteurs'],
                'priority': 'moyenne',
                'packages': 1,
                'totalWeight': 0.0,
                'status': 'preparing',
                'trackingNumber': expedition_data['reference_commande'],
                'observation': expedition_data['observation'],
                'articles': expedition_data['liste_articles_livres']
            }
            
            # Ajouter à la liste
            self.expeditions_data.append(new_expedition)
            
            # Mettre à jour l'affichage
            self.update_expeditions_display()
        
        def cancel_creation():
            """Annuler la création"""
            modal.destroy()
        
        # Boutons
        ctk.CTkButton(buttons_frame, text="❌ Annuler", width=120, height=40, fg_color="#ef4444", hover_color="#dc2626", command=cancel_creation).pack(side="left", padx=10)
        ctk.CTkButton(buttons_frame, text="✅ Créer l'expédition", width=150, height=40, fg_color="#10b981", hover_color="#059669", command=create_expedition).pack(side="left", padx=10)

    def action_planning(self):
        """Afficher le planning"""
        print("Affichage du planning")
        
        # Créer une fenêtre modale pour le planning
        modal = ctk.CTkToplevel(self)
        modal.title("Planning des Expéditions")
        modal.geometry("1000x700")
        modal.configure(fg_color='white')
        modal.grab_set()
        modal.resizable(True, True)
        
        # Titre
        title_label = ctk.CTkLabel(modal, text="📅 Planning des Expéditions", font=ctk.CTkFont(size=24, weight="bold"), text_color="#1f2937")
        title_label.pack(pady=(20, 30))
        
        # Frame principal
        main_frame = ctk.CTkScrollableFrame(modal, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Planning par jour
        days = [
            {"day": "Lundi 18 Mars", "expeditions": [
                {"time": "08:00", "action": "Préparation commandes prioritaires", "status": "Terminé", "color": "#10b981"},
                {"time": "10:00", "action": "Enlèvement DHL Express", "status": "En cours", "color": "#3b82f6"},
                {"time": "14:00", "action": "Enlèvement Chronopost", "status": "Planifié", "color": "#f59e0b"},
            ]},
            {"day": "Mardi 19 Mars", "expeditions": [
                {"time": "09:00", "action": "Préparation commandes standard", "status": "À venir", "color": "#6b7280"},
                {"time": "11:00", "action": "Enlèvement Colissimo", "status": "À venir", "color": "#6b7280"},
                {"time": "15:00", "action": "Préparation J+1", "status": "À venir", "color": "#6b7280"},
            ]},
            {"day": "Mercredi 20 Mars", "expeditions": [
                {"time": "08:30", "action": "Préparation commandes urgentes", "status": "À venir", "color": "#6b7280"},
                {"time": "12:00", "action": "Enlèvement UPS", "status": "À venir", "color": "#6b7280"},
            ]},
        ]
        
        for day_data in days:
            # Frame pour chaque jour
            day_frame = ctk.CTkFrame(main_frame, fg_color="white", border_width=1, border_color="#e5e7eb", corner_radius=8)
            day_frame.pack(fill="x", pady=(0, 15))
            
            # Titre du jour
            ctk.CTkLabel(day_frame, text=day_data["day"], font=ctk.CTkFont(size=18, weight="bold"), text_color="#1f2937").pack(anchor="w", padx=20, pady=(15, 10))
            
            # Expéditions du jour
            for exp in day_data["expeditions"]:
                exp_frame = ctk.CTkFrame(day_frame, fg_color="#f9fafb", corner_radius=6)
                exp_frame.pack(fill="x", padx=20, pady=5)
                
                # Contenu de l'expédition
                content_frame = ctk.CTkFrame(exp_frame, fg_color="transparent")
                content_frame.pack(fill="x", padx=15, pady=10)
                
                # Heure
                ctk.CTkLabel(content_frame, text=exp["time"], font=ctk.CTkFont(size=16, weight="bold"), text_color="#374151").pack(side="left")
                
                # Action
                ctk.CTkLabel(content_frame, text=exp["action"], font=ctk.CTkFont(size=14), text_color="#6b7280").pack(side="left", padx=(20, 0))
                
                # Statut
                ctk.CTkLabel(content_frame, text=exp["status"], font=ctk.CTkFont(size=14, weight="bold"), text_color=exp["color"]).pack(side="right")
        
        # Bouton de fermeture
        ctk.CTkButton(modal, text="Fermer", width=120, height=40, command=modal.destroy).pack(pady=20)

    def open_tracking_modal(self):
        """Ouvrir la modal de suivi"""
        print("Ouverture de la modal de suivi")
        
        # Créer une fenêtre modale pour le suivi
        modal = ctk.CTkToplevel(self)
        modal.title("Suivi des Expéditions")
        modal.geometry("900x600")
        modal.configure(fg_color='white')
        modal.grab_set()
        modal.resizable(True, True)
        
        # Titre
        title_label = ctk.CTkLabel(modal, text="🔍 Suivi des Expéditions", font=ctk.CTkFont(size=24, weight="bold"), text_color="#1f2937")
        title_label.pack(pady=(20, 30))
        
        # Frame de recherche
        search_frame = ctk.CTkFrame(modal, fg_color="white", border_width=1, border_color="#e5e7eb", corner_radius=8)
        search_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(search_frame, text="Rechercher une expédition", font=ctk.CTkFont(size=16, weight="bold"), text_color="#374151").pack(anchor="w", padx=20, pady=(15, 10))
        
        # Champ de recherche
        search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=search_var, placeholder_text="Numéro d'expédition (ex: BE-2024-087)", width=300, height=35)
        search_entry.pack(side="left", padx=(20, 10), pady=(0, 15))
        
        def search_expedition():
            """Rechercher une expédition"""
            search_term = search_var.get().strip()
            if not search_term:
                return
            
            try:
                if DB_AVAILABLE:
                    # Rechercher dans la base de données
                    search_results = search_expedition(search_term)
                    if search_results:
                        found_expedition = search_results[0]  # Prendre le premier résultat
                        show_expedition_details(found_expedition)
                    else:
                        show_not_found()
                else:
                    # Recherche locale
                    found_expedition = None
                    for exp in self.expeditions_data:
                        if search_term.upper() in exp['number'].upper():
                            found_expedition = exp
                            break
                    
                    if found_expedition:
                        show_expedition_details(found_expedition)
                    else:
                        show_not_found()
                        
            except Exception as e:
                print(f"❌ Erreur lors de la recherche: {e}")
                show_not_found()
        
        ctk.CTkButton(search_frame, text="🔍 Rechercher", width=120, height=35, command=search_expedition).pack(side="left", padx=(0, 20), pady=(0, 15))
        
        # Frame pour les résultats
        results_frame = ctk.CTkFrame(modal, fg_color="transparent")
        results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        def show_expedition_details(expedition):
            """Afficher les détails d'une expédition"""
            # Nettoyer les résultats précédents
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            # Frame des détails
            details_frame = ctk.CTkFrame(results_frame, fg_color="white", border_width=1, border_color="#e5e7eb", corner_radius=8)
            details_frame.pack(fill="both", expand=True)
            
            # Titre
            ctk.CTkLabel(details_frame, text=f"📦 {expedition['number']}", font=ctk.CTkFont(size=20, weight="bold"), text_color="#1f2937").pack(anchor="w", padx=20, pady=(20, 15))
            
            # Informations
            info_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            info_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            info_data = [
                ("Client:", expedition['client']),
                ("Transporteur:", expedition['carrier']),
                ("Priorité:", expedition['priority'].title()),
                ("Statut:", expedition['status'].title()),
                ("Poids:", f"{expedition['totalWeight']} kg"),
                ("Colis:", str(expedition['packages'])),
            ]
            
            for i, (label, value) in enumerate(info_data):
                row = i // 2
                col = i % 2
                
                ctk.CTkLabel(info_frame, text=label, font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").grid(row=row*2, column=col, sticky="w", padx=(0, 10), pady=(10, 5))
                ctk.CTkLabel(info_frame, text=value, font=ctk.CTkFont(size=14), text_color="#6b7280").grid(row=row*2+1, column=col, sticky="w", padx=(0, 20), pady=(0, 10))
            
            # Timeline de suivi
            timeline_frame = ctk.CTkFrame(details_frame, fg_color="#f9fafb", corner_radius=8)
            timeline_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            ctk.CTkLabel(timeline_frame, text="📋 Timeline de suivi", font=ctk.CTkFont(size=16, weight="bold"), text_color="#374151").pack(anchor="w", padx=15, pady=(15, 10))
            
            timeline_events = [
                {"date": "2024-03-15 08:30", "event": "Expédition créée", "status": "✅"},
                {"date": "2024-03-15 10:15", "event": "En préparation", "status": "✅"},
                {"date": "2024-03-15 14:20", "event": "Expédiée", "status": "✅"},
                {"date": "2024-03-16 09:00", "event": "En transit", "status": "🔄"},
                {"date": "2024-03-17 11:30", "event": "Livraison prévue", "status": "⏳"},
            ]
            
            for event in timeline_events:
                event_frame = ctk.CTkFrame(timeline_frame, fg_color="transparent")
                event_frame.pack(fill="x", padx=15, pady=5)
                
                ctk.CTkLabel(event_frame, text=event["status"], font=ctk.CTkFont(size=16)).pack(side="left")
                ctk.CTkLabel(event_frame, text=event["event"], font=ctk.CTkFont(size=14), text_color="#374151").pack(side="left", padx=(10, 0))
                ctk.CTkLabel(event_frame, text=event["date"], font=ctk.CTkFont(size=12), text_color="#6b7280").pack(side="right")
        
        def show_not_found():
            """Afficher message si expédition non trouvée"""
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            not_found_frame = ctk.CTkFrame(results_frame, fg_color="white", border_width=1, border_color="#e5e7eb", corner_radius=8)
            not_found_frame.pack(fill="both", expand=True)
            
            ctk.CTkLabel(not_found_frame, text="❌ Expédition non trouvée", font=ctk.CTkFont(size=18, weight="bold"), text_color="#ef4444").pack(expand=True)
            ctk.CTkLabel(not_found_frame, text="Vérifiez le numéro d'expédition et réessayez", font=ctk.CTkFont(size=14), text_color="#6b7280").pack()
        
        # Bouton de fermeture
        ctk.CTkButton(modal, text="Fermer", width=120, height=40, command=modal.destroy).pack(pady=20)

    def action_export(self):
        """Exporter les données"""
        print("Export des données")
        
        # Créer une fenêtre modale pour l'export
        modal = ctk.CTkToplevel(self)
        modal.title("Export des Expéditions")
        modal.geometry("600x500")
        modal.configure(fg_color='white')
        modal.grab_set()
        modal.resizable(False, False)
        
        # Titre
        title_label = ctk.CTkLabel(modal, text="⭳ Export des Expéditions", font=ctk.CTkFont(size=24, weight="bold"), text_color="#1f2937")
        title_label.pack(pady=(20, 30))
        
        # Frame principal
        main_frame = ctk.CTkFrame(modal, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Options d'export
        options_frame = ctk.CTkFrame(main_frame, fg_color="white", border_width=1, border_color="#e5e7eb", corner_radius=8)
        options_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(options_frame, text="Options d'export", font=ctk.CTkFont(size=18, weight="bold"), text_color="#374151").pack(anchor="w", padx=20, pady=(20, 15))
        
        # Variables
        format_var = tk.StringVar(value="Excel")
        date_range_var = tk.StringVar(value="Toutes")
        status_var = tk.StringVar(value="Tous")
        
        # Format d'export
        format_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        format_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(format_frame, text="Format:", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(side="left")
        format_combo = ctk.CTkOptionMenu(format_frame, variable=format_var, values=["Excel", "CSV", "PDF"], width=150)
        format_combo.pack(side="left", padx=(10, 0))
        
        # Période
        period_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        period_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(period_frame, text="Période:", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(side="left")
        period_combo = ctk.CTkOptionMenu(period_frame, variable=date_range_var, values=["Toutes", "Aujourd'hui", "Cette semaine", "Ce mois"], width=150)
        period_combo.pack(side="left", padx=(10, 0))
        
        # Statut
        status_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(status_frame, text="Statut:", font=ctk.CTkFont(size=14, weight="bold"), text_color="#374151").pack(side="left")
        status_combo = ctk.CTkOptionMenu(status_frame, variable=status_var, values=["Tous", "En préparation", "Expédiées", "Livrées"], width=150)
        status_combo.pack(side="left", padx=(10, 0))
        
        # Résumé
        summary_frame = ctk.CTkFrame(main_frame, fg_color="#f0f9ff", border_width=1, border_color="#0ea5e9", corner_radius=8)
        summary_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(summary_frame, text="📊 Résumé de l'export", font=ctk.CTkFont(size=16, weight="bold"), text_color="#0c4a6e").pack(anchor="w", padx=15, pady=(15, 10))
        
        summary_text = f"• Format: {format_var.get()}\n• Période: {date_range_var.get()}\n• Statut: {status_var.get()}\n• Nombre d'expéditions: {len(self.expeditions_data)}"
        ctk.CTkLabel(summary_frame, text=summary_text, font=ctk.CTkFont(size=14), text_color="#0c4a6e", justify="left").pack(anchor="w", padx=15, pady=(0, 15))
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(modal, fg_color="transparent")
        buttons_frame.pack(pady=(0, 20))
        
        def perform_export():
            """Effectuer l'export"""
            # Simuler l'export
            print(f"Export en cours: Format={format_var.get()}, Période={date_range_var.get()}, Statut={status_var.get()}")
            
            # Afficher un message de succès
            success_label = ctk.CTkLabel(modal, text="✅ Export terminé avec succès !", text_color="#10b981", font=ctk.CTkFont(size=16, weight="bold"))
            success_label.pack(pady=10)
            
            # Fermer la modal après 2 secondes
            modal.after(2000, modal.destroy)
        
        def cancel_export():
            """Annuler l'export"""
            modal.destroy()
        
        # Boutons centrés et alignés avec couleurs bien visibles
        ctk.CTkButton(
            buttons_frame, 
            text="❌ Annuler", 
            width=140, 
            height=40, 
            fg_color="#dc2626", 
            hover_color="#b91c1c", 
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8,
            command=cancel_export
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkButton(
            buttons_frame, 
            text="⭳ Exporter", 
            width=140, 
            height=40, 
            fg_color="#059669", 
            hover_color="#047857", 
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8,
            command=perform_export
        ).pack(side="left", padx=(15, 0))
        
        # Centrer les boutons dans le frame
        buttons_frame.pack_configure(anchor="center")

    def apply_theme(self, theme):
        """Appliquer le thème à la page"""
        try:
            print(f"Thème appliqué à la page Expéditions: {theme}")
            
            # Couleurs selon le thème
            if theme == "dark":
                bg_color = "#1a1a1a"
                card_bg = "#2d2d2d"
                text_color = "#ffffff"
                border_color = "#555555"
            else:
                bg_color = "#ffffff"
                card_bg = "#ffffff"
                text_color = "#222222"
                border_color = "#e0e0e0"
            
            # Appliquer aux widgets principaux
            self.configure(fg_color=bg_color)
            
            # Appliquer récursivement aux enfants
            self._apply_theme_recursive(self, theme)
            
        except Exception as e:
            print(f"Erreur lors de l'application du thème: {e}")
    
    def _apply_theme_recursive(self, widget, theme):
        """Applique le thème de manière récursive"""
        try:
            is_dark = theme == "dark"
            
            # Couleurs adaptatives
            bg_color = "#1a1a1a" if is_dark else "#f7fafd"
            card_bg = "#2d2d2d" if is_dark else "white"
            text_color = "#ffffff" if is_dark else "#222222"
            border_color = "#555555" if is_dark else "#e0e0e0"
            
            # Appliquer aux widgets principaux
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=card_bg, border_color=border_color)
            elif isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=text_color)
            
            # Appliquer récursivement aux enfants
            for child in widget.winfo_children():
                self._apply_theme_recursive(child, theme)
                
        except Exception as e:
            # Ignorer les erreurs pour éviter les boucles infinies
            pass

    def _refresh_planning_periodically(self):
        """Rafraîchit le planning toutes les 30 secondes en temps réel"""
        try:
            if hasattr(self, 'planning_frame') and self.planning_frame:
                self.create_central_blocks()  # Reconstruit le bloc planning
        except Exception as e:
            print(f"Erreur lors du rafraîchissement du planning: {e}")
        self.after(30000, self._refresh_planning_periodically)  # 30 secondes

    def _auto_refresh(self):
        self.refresh_data()
        self.after(self._auto_refresh_interval, self._auto_refresh)

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
        ctk.CTkLabel(error_frame, text="❌ Erreur lors de l'affichage de la page expédition", font=ctk.CTkFont(size=20, weight="bold"), text_color="#b91c1c").pack(pady=(30, 10))
        ctk.CTkLabel(error_frame, text=message, font=ctk.CTkFont(size=15), text_color="#b91c1c").pack(pady=(0, 20))
        ctk.CTkButton(error_frame, text="🏠 Retour à l'accueil", fg_color="#2563eb", text_color="white", font=ctk.CTkFont(size=15, weight="bold"), command=self._go_back).pack(pady=10)

    def _update_local_expedition(self, expedition_id, expedition_data):
        """Met à jour une expédition en mode local (démonstration)"""
        for i, exp in enumerate(self.expeditions_data):
            if exp['id'] == expedition_id:
                self.expeditions_data[i].update({
                    'client': expedition_data['client'],
                    'carrier': expedition_data['transporteurs'],
                    'observation': expedition_data['observation'],
                    'trackingNumber': expedition_data['reference_commande']
                })
                break
        
        # Mettre à jour l'affichage
        self.update_expeditions_display()

    def _delete_local_expedition(self, expedition_id):
        """Supprime une expédition en mode local (démonstration)"""
        self.expeditions_data = [exp for exp in self.expeditions_data if exp['id'] != expedition_id]
        
        # Mettre à jour l'affichage
        self.update_expeditions_display()


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Gestion des Expéditions (test autonome)")
    root.geometry("1400x900")
    frame = GestionExpeditionsApp(master=root)
    frame.pack(fill="both", expand=True)
    root.mainloop()
