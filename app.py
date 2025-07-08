import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os
from AUTHENTIFICATION import AuthFrame
from dashboard import DashboardFrame
from stock_management_page import StockManagementFrame, SidebarFrame
from reception_page import ReceptionFrame
from rapport_analytics import RapportAnalyticsFrame
from warehouse_page import WarehouseFrame  
from Expeditions import GestionExpeditionsApp 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SAC - Système de Gestion d'Entrepôts")
        self.geometry("1400x900")
        self.minsize(1100, 700)
        
        # Configuration pour permettre le redimensionnement
        self.resizable(True, True)
        self.attributes('-topmost', False)
        
        # S'assurer que la fenêtre peut être redimensionnée
        self.minsize(1100, 700)
        self.maxsize(1920, 1080)  # Limite maximale raisonnable
        
        # Variables pour le responsive design
        self.current_width = 1400
        self.current_height = 900
        self.breakpoints = {
            'mobile': 768,
            'tablet': 1024,
            'desktop': 1400,
            'large': 1600
        }
        
        ctk.set_appearance_mode("light")
        self.current_frame = None
        self.user_info = None
        self.bg_image = None
        self.bg_label = None
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Configuration de l'icône pour la barre des tâches (après base_path)
        self.setup_icon()
        
        self.protocol("WM_DELETE_WINDOW", self.confirm_exit)
        
        # Configuration du redimensionnement avec gestion d'erreurs
        self.bind("<Configure>", self.on_resize)
        
        # S'assurer que la fenêtre s'affiche correctement
        self.after(100, self.show_auth_frame)
        
        # Forcer l'affichage de la fenêtre
        self.deiconify()
        self.lift()
        self.focus_force()

    def setup_icon(self):
        try:
            # Essayer d'abord l'icône ICO
            icon_path = os.path.join(self.base_path, "logo.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
                print("Icône ICO chargée avec succès")
                return
        except Exception as e:
            print(f"Erreur chargement icône ICO: {e}")
        
        try:
            # Essayer ensuite l'icône PNG
            icon_path_png = os.path.join(self.base_path, "logo.png")
            if os.path.exists(icon_path_png):
                # Créer une icône à partir du PNG
                from PIL import Image, ImageTk
                img = Image.open(icon_path_png)
                # Redimensionner à 32x32 pour la barre des tâches
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.iconphoto(True, photo)
                print("Icône PNG chargée avec succès")
                return
        except Exception as e:
            print(f"Erreur chargement icône PNG: {e}")
        
        print("Aucune icône trouvée, utilisation de l'icône par défaut")

    def setup_background(self):
        try:
            bg_image_path = os.path.join(self.base_path, "entrepot_bg.jpg")
            self.bg_image = ctk.CTkImage(light_image=Image.open(bg_image_path), size=(self.winfo_width(), self.winfo_height()))
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
        except Exception:
            self.bg_image = None
            self.bg_label = ctk.CTkLabel(self, text="Image 'entrepot_bg.jpg' non trouvée", fg_color="gray", font=("Segoe UI", 24))

    def show_auth_frame(self):
        self._clear_frame()
        self.user_info = None
        self.setup_background()
        if self.bg_label:
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.current_frame = AuthFrame(self)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")

    def show_dashboard(self, user_info):
        self._clear_frame()
        if self.bg_label:
            self.bg_label.place_forget()
        self.user_info = user_info
        self.current_frame = DashboardFrame(self, user_info, toplevel_window=self)
        self.current_frame.pack(fill="both", expand=True)
        
        # S'assurer que la fenêtre est visible et redimensionnable
        self.deiconify()
        self.lift()
        self.resizable(True, True)

    def show_stock(self):
        self._clear_frame()
        if self.bg_label:
            self.bg_label.place_forget()
        self.current_frame = StockManagementFrame(self, self.user_info)
        self.current_frame.pack(fill="both", expand=True)
        self.resizable(True, True)
        
    
    def show_movements(self):
        """Affiche la page de gestion des mouvements"""
        self._clear_frame()
        if self.bg_label:
            self.bg_label.place_forget()
        try:
            from movement_page import MovementsFrame
            self.current_frame = MovementsFrame(self, self.user_info)
            self.current_frame.pack(fill="both", expand=True)
            self.resizable(True, True)
        except ImportError as e:
            print(f"Erreur lors de l'import du module mouvements: {e}")
            # Afficher un message d'erreur
            error_frame = ctk.CTkFrame(self, fg_color="white")
            error_frame.pack(fill="both", expand=True)
            
            ctk.CTkLabel(
                error_frame,
                text="❌ Erreur de chargement",
                font=ctk.CTkFont(size=32, weight="bold"),
                text_color="#ef4444"
            ).pack(pady=(50, 20))
            
            ctk.CTkLabel(
                error_frame,
                text="Le module de mouvements n'a pas pu être chargé.",
                font=ctk.CTkFont(size=16),
                text_color="#6b7280"
            ).pack()
            
            ctk.CTkLabel(
                error_frame,
                text=f"Erreur: {str(e)}",
                font=ctk.CTkFont(size=14),
                text_color="#ef4444"
            ).pack(pady=(10, 0))

    def show_reception(self):
        self._clear_frame()
        if self.bg_label:
            self.bg_label.place_forget()
        self.current_frame = ReceptionFrame(self, self.user_info)
        self.current_frame.pack(fill="both", expand=True)
        self.resizable(True, True)

    def show_analytics(self):
        self._clear_frame()
        if self.bg_label:
            self.bg_label.place_forget()
        self.current_frame = RapportAnalyticsFrame(self, self.user_info)
        self.current_frame.pack(fill="both", expand=True)
        self.resizable(True, True)
    
    def show_warehouse(self):
        self._clear_frame()
        if self.bg_label:
            self.bg_label.place_forget()
        self.current_frame = WarehouseFrame(self, self.user_info)
        self.current_frame.pack(fill="both", expand=True)
        self.resizable(True, True)

    def show_admin(self):
        self._clear_frame()
        if self.bg_label:
            self.bg_label.place_forget()
        from admin_page import AdminFrame
        self.current_frame = AdminFrame(self)
        self.current_frame.pack(fill="both", expand=True)
        self.resizable(True, True)

    def show_expedition(self):
        self._clear_frame()
        if self.bg_label:
            self.bg_label.place_forget()
        from Expeditions import GestionExpeditionsApp
        self.current_frame = GestionExpeditionsApp(master=self, user_info=self.user_info)
        self.current_frame.pack(fill="both", expand=True)
        self.resizable(True, True)

    def show_packaging(self):
        self._clear_frame()
        if self.bg_label:
            self.bg_label.place_forget()
        from packaging_page import PackagingFrame
        self.current_frame = PackagingFrame(self, self.user_info)
        self.current_frame.pack(fill="both", expand=True)
        self.resizable(True, True)

    def confirm_logout(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmation de déconnexion")
        dialog.geometry("370x180")
        dialog.configure(fg_color='white')
        dialog.grab_set()
        dialog.resizable(False, False)
        ctk.CTkLabel(dialog, text="Voulez-vous vraiment vous déconnecter ?", font=ctk.CTkFont(size=16, weight='bold'), text_color='#333333').pack(pady=(28,8), padx=20)
        ctk.CTkLabel(dialog, text="Vous serez redirigé vers la page de connexion.", font=ctk.CTkFont(size=13), text_color='#666666').pack(pady=(0,10), padx=20)
        btn_frame = ctk.CTkFrame(dialog, fg_color='transparent')
        btn_frame.pack(pady=(0,18))
        ctk.CTkButton(btn_frame, text='Oui, me déconnecter', width=140, height=38, fg_color='#EF5350', hover_color='#E53935', text_color='white', corner_radius=8, font=ctk.CTkFont(size=14, weight='bold'), command=lambda: (dialog.destroy(), self.show_auth_frame())).pack(side='left', padx=12)
        ctk.CTkButton(btn_frame, text='Non, rester', width=120, height=38, fg_color='#90A4AE', hover_color='#78909C', text_color='white', corner_radius=8, font=ctk.CTkFont(size=14), command=dialog.destroy).pack(side='left', padx=12)

    def confirm_exit(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Quitter l'application")
        dialog.geometry("370x180")
        dialog.configure(fg_color='white')
        dialog.grab_set()
        dialog.resizable(False, False)
        ctk.CTkLabel(dialog, text="Voulez-vous vraiment quitter l'application ?", font=ctk.CTkFont(size=16, weight='bold'), text_color='#333333').pack(pady=(28,8), padx=20)
        ctk.CTkLabel(dialog, text="Toutes les modifications non enregistrées seront perdues.", font=ctk.CTkFont(size=13), text_color='#666666').pack(pady=(0,10), padx=20)
        btn_frame = ctk.CTkFrame(dialog, fg_color='transparent')
        btn_frame.pack(pady=(0,18))
        ctk.CTkButton(btn_frame, text='Oui, quitter', width=140, height=38, fg_color='#EF5350', hover_color='#E53935', text_color='white', corner_radius=8, font=ctk.CTkFont(size=14, weight='bold'), command=self._quit_application).pack(side='left', padx=12)
        ctk.CTkButton(btn_frame, text='Non, rester', width=120, height=38, fg_color='#90A4AE', hover_color='#78909C', text_color='white', corner_radius=8, font=ctk.CTkFont(size=14), command=dialog.destroy).pack(side='left', padx=12)

    def _quit_application(self):
        """Arrête la boucle mainloop et détruit l'application."""
        try:
            print("Fermeture de l'application...")
            
            # Fermer proprement tous les widgets enfants
            for widget in self.winfo_children():
                try:
                    widget.destroy()
                except:
                    pass
            
            # Arrêter la boucle principale
            self.quit()
            



            
            # Détruire la fenêtre principale
            self.destroy()
            
            # Forcer la fermeture si nécessaire
            import sys
            sys.exit(0)
            
        except Exception as e:
            print(f"Erreur lors de la fermeture: {e}")
            # Forcer la fermeture en cas d'erreur
            import sys
            sys.exit(1)

    def on_resize(self, event):
        """Gère le redimensionnement de la fenêtre avec responsive design"""
        # Éviter les redimensionnements trop fréquents
        if hasattr(self, '_resize_timer'):
            self.after_cancel(self._resize_timer)
        
        # Utiliser un timer pour différer le redimensionnement
        self._resize_timer = self.after(100, self._delayed_resize)
    
    def _delayed_resize(self):
        """Redimensionnement différé avec responsive design"""
        try:
            new_width = self.winfo_width()
            new_height = self.winfo_height()
            
            # Vérifier si la taille a vraiment changé
            if new_width != self.current_width or new_height != self.current_height:
                self.current_width = new_width
                self.current_height = new_height
                
                # Mettre à jour l'image de fond si elle existe
                if self.bg_image and new_width > 100 and new_height > 100:
                    self.bg_image.configure(size=(new_width, new_height))
                
                # Notifier le frame actuel du redimensionnement
                if self.current_frame and hasattr(self.current_frame, 'on_window_resize'):
                    try:
                        self.current_frame.on_window_resize(new_width, new_height)
                    except Exception as e:
                        # Ignorer les erreurs de redimensionnement
                        pass
                
                # Adapter la sidebar si nécessaire
                if hasattr(self, 'sidebar') and self.sidebar:
                    try:
                        self._adapt_sidebar_to_size(new_width)
                    except Exception as e:
                        # Ignorer les erreurs de sidebar
                        pass
                    
        except Exception as e:
            # Ignorer les erreurs de redimensionnement
            pass
    
    def _adapt_sidebar_to_size(self, width):
        """Adapte la sidebar selon la taille de l'écran"""
        if width < self.breakpoints['tablet']:
            # Mode mobile/tablet - sidebar plus compacte
            if hasattr(self.sidebar, 'configure_compact'):
                self.sidebar.configure_compact(True)
        else:
            # Mode desktop - sidebar normale
            if hasattr(self.sidebar, 'configure_compact'):
                self.sidebar.configure_compact(False)
    
    def get_responsive_config(self):
        """Retourne la configuration responsive selon la taille actuelle"""
        width = self.current_width
        
        if width < self.breakpoints['mobile']:
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
        elif width < self.breakpoints['tablet']:
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
        elif width < self.breakpoints['desktop']:
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

    def _clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def show_notification(self, message, duration=2000):
        """Affiche un message temporaire en haut de la fenêtre principale."""
        if hasattr(self, '_notif_label') and self._notif_label:
            self._notif_label.destroy()
        self._notif_label = ctk.CTkLabel(self, text=message, fg_color="#2563eb", text_color="white", font=ctk.CTkFont(size=15, weight="bold"), corner_radius=12, padx=24, pady=10)
        self._notif_label.place(relx=0.5, rely=0.03, anchor="n")
        self.after(duration, lambda: self._notif_label.destroy())

    def notify_theme_change(self, theme):
        """Notifie l'application principale d'un changement de thème"""
        try:
            # Appliquer le thème à la fenêtre principale
            if theme == "dark":
                self.configure(fg_color="#1a1a1a")
                ctk.set_appearance_mode("dark")
            else:
                self.configure(fg_color="white")
                ctk.set_appearance_mode("light")
            
            # Notifier le frame actuel s'il existe
            if self.current_frame and hasattr(self.current_frame, 'apply_theme'):
                self.current_frame.apply_theme(theme)
            
            # Appliquer le thème à tous les widgets enfants de manière récursivev
            self._apply_theme_recursive(self, theme)
            
            # Forcer le rafraîchissement
            self.update()
            
            print(f"Thème appliqué à l'application principale: {theme}")
            
        except Exception as e:
            print(f"Erreur lors de l'application du thème à l'app principale: {e}")
    
    def _apply_theme_recursive(self, widget, theme):
        """Applique le thème de manière récursive à tous les widgets"""
        try:
            is_dark = theme == "dark"
            
            # Couleurs adaptatives
            bg_color = "#1a1a1a" if is_dark else "#f7fafd"
            card_bg = "#2d2d2d" if is_dark else "white"
            text_color = "#ffffff" if is_dark else "#222222"
            secondary_text = "#cccccc" if is_dark else "#666666"
            border_color = "#555555" if is_dark else "#e0e0e0"
            table_bg = "#3d3d3d" if is_dark else "#f9fafb"
            
            # Appliquer aux widgets principaux
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=card_bg, border_color=border_color)
            elif isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=text_color)
            elif isinstance(widget, ctk.CTkEntry):
                widget.configure(fg_color=table_bg, text_color=text_color, border_color=border_color)
            elif isinstance(widget, ctk.CTkTextbox):
                widget.configure(fg_color=table_bg, text_color=text_color, border_color=border_color)
            elif isinstance(widget, ctk.CTkScrollableFrame):
                widget.configure(fg_color=card_bg, border_color=border_color)
            
            # Appliquer récursivement aux enfants
            for child in widget.winfo_children():
                self._apply_theme_recursive(child, theme)
                
        except Exception as e:
            # Ignorer les erreurs pour éviter les boucles infinies
            pass



if __name__ == "__main__":
    print("Démarrage de l'application...")
    # Initialisation de la base désactivée pour éviter les erreurs d'encodage
    # try:
    #     from database import init_database
    #     print("Initialisation de la base de données...")
    #     init_database()
    #     print("Base de données vérifiée/créée.")
    # except Exception as e:
    #     print(f"Erreur critique lors de l'initialisation de la base de données : {e}")
    #     import sys
    #     sys.exit(1)

    try:
        app = App()
        print("Application créée avec succès")
        print("Démarrage de la boucle principale...")
        app.mainloop()
        print("Boucle principale terminée")
    except Exception as e:
        print(f"Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()