import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import re
import os
import json
from database import check_user

# Import direct de DashboardFrame
try:
    from dashboard import DashboardFrame
except ImportError:
    print("Erreur: Impossible d'importer DashboardFrame")
    DashboardFrame = None

class AuthFrame(ctk.CTkFrame):
    """La frame (page) de connexion."""
    def __init__(self, master):
        super().__init__(master, corner_radius=40, width=420, height=520, fg_color="#ffffff")
        self.master = master  # master est l'instance de App
        self.memory_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login_memory.json")

        self.grid_propagate(False)
        self.card_content = ctk.CTkFrame(self, fg_color="transparent")
        self.card_content.pack(fill="both", expand=True)

        self.create_logo()
        self.create_form()
        self.create_footer_links()
        
        self._load_remembered_email()

    def create_logo(self):
        try:
            # Utiliser directement le chemin du fichier courant
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
            logo_image = ctk.CTkImage(Image.open(logo_path), size=(200, 130))
        except FileNotFoundError:
            placeholder = Image.new('RGB', (200, 130), color='grey')
            d = ImageDraw.Draw(placeholder)
            d.text((10, 10), "logo.png\nnon trouvé", fill=(255, 255, 0))
            logo_image = ctk.CTkImage(light_image=placeholder, size=(200, 130))
        
        logo = ctk.CTkLabel(self.card_content, image=logo_image, text="")
        logo.pack(pady=(25, 15))

    def create_form(self):
        email_label = ctk.CTkLabel(self.card_content, text="Adresse email", font=("Segoe UI", 12, "bold"), text_color="#1e293b")
        email_label.pack(anchor="w", padx=20, pady=(0, 2))

        self.email_frame = ctk.CTkFrame(self.card_content, fg_color="transparent")
        self.email_frame.pack(pady=(8, 0), padx=20, fill="x")
        self.email_entry = ctk.CTkEntry(self.email_frame, placeholder_text="prenom.nom@sac.com", width=320, height=38, corner_radius=12, fg_color="#f8fafc", text_color="#1e293b", border_color="#2563eb", border_width=1)
        self.email_entry.pack(fill="x")
        self.email_error_label = ctk.CTkLabel(self.card_content, text="", font=("Segoe UI", 11), text_color="#ef4444")
        self.email_error_label.pack(anchor="w", padx=25, pady=(2, 0))

        pass_label = ctk.CTkLabel(self.card_content, text="Mot de passe", font=("Segoe UI", 12, "bold"), text_color="#1e293b")
        pass_label.pack(anchor="w", padx=20, pady=(10, 2))

        self.password_frame = ctk.CTkFrame(self.card_content, fg_color="transparent")
        self.password_frame.pack(pady=(8, 0), padx=20, fill="x")
        self.password_entry = ctk.CTkEntry(self.password_frame, fg_color="#f8fafc", placeholder_text="••••••••", width=320, height=38, show="•", corner_radius=12, text_color="#1e293b", border_color="#2563eb", border_width=1)
        self.password_entry.pack(fill="x")
        self.password_error_label = ctk.CTkLabel(self.card_content, text="", font=("Segoe UI", 11), text_color="#ef4444")
        self.password_error_label.pack(anchor="w", padx=25, pady=(2, 0))

        self.show_pass_var = tk.BooleanVar(value=False)
        show_pass_frame = ctk.CTkFrame(self.card_content, fg_color="transparent")
        show_pass_frame.pack(anchor="w", padx=18, pady=(0, 8))
        show_pass = ctk.CTkCheckBox(show_pass_frame, text="Afficher", variable=self.show_pass_var, command=self.toggle_password, checkbox_width=22, checkbox_height=22, text_color="#1e293b", fg_color="#f8fafc", border_color="#2563eb", border_width=2, checkmark_color="#2563eb")
        show_pass.pack(anchor="w", padx=4, pady=2)

        login_btn = ctk.CTkButton(self.card_content, text="Se connecter", command=self.authenticate, height=42, fg_color="#2563eb", hover_color="#1e40af", font=("Segoe UI", 14, "bold"), corner_radius=14)
        login_btn.pack(pady=20, ipadx=12)

    def _load_remembered_email(self):
        """Charge l'email depuis le fichier de sauvegarde et le pré-remplit."""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    email = data.get('last_email')
                    if email:
                        self.email_entry.insert(0, email)
                        self.password_entry.focus() # Met le focus sur le mot de passe
        except (IOError, json.JSONDecodeError):
            # Le fichier est peut-être corrompu ou illisible, on ne fait rien
            pass

    def _save_remembered_email(self, email):
        """Sauvegarde l'email dans un fichier JSON."""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump({'last_email': email}, f)
        except IOError:
            # Impossible d'écrire, on ne bloque pas l'application pour ça
            print(f"Avertissement: Impossible d'écrire dans {self.memory_file}")

    def toggle_password(self):
        self.password_entry.configure(show="" if self.show_pass_var.get() else "•")

    def authenticate(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        email_regex = r'^[a-zA-Z\.]+\@sac\.com$'

        # Réinitialiser les erreurs
        self.email_frame.configure(border_color="#2563eb")
        self.password_frame.configure(border_color="#2563eb")
        self.email_error_label.configure(text="")
        self.password_error_label.configure(text="")

        error = False
        if not email:
            self.email_error_label.configure(text="❌ L'adresse email est requise.")
            self.email_frame.configure(border_color="#ef4444")
            error = True
        if not password:
            self.password_error_label.configure(text="❌ Le mot de passe est requis.")
            self.password_frame.configure(border_color="#ef4444")
            error = True
        if error:
            if not email:
                self.email_entry.focus()
            elif not password:
                self.password_entry.focus()
            return

        if not re.match(email_regex, email):
            self.email_error_label.configure(text="❌ Format d'email invalide. Utilisez prenom.nom@sac.com")
            self.email_frame.configure(border_color="#ef4444")
            self.password_entry.delete(0, 'end')
            self.email_entry.focus()
            return
        
        # Vérification réelle via la base PostgreSQL (table individus)
        status, user = check_user(email, password)

        if status == "SUCCESS":
            self._save_remembered_email(email)  # Sauvegarde de l'email
            self.email_frame.configure(border_color="#22c55e")
            self.password_frame.configure(border_color="#22c55e")
            self.show_success_popup("Connexion réussie!", "Redirection vers le tableau de bord...")
            print("Connexion réussie, redirection...")
            self.master.after(800, lambda: self.redirect_to_dashboard(user))
        elif status == "USER_NOT_FOUND":
            self.show_popup_error("Erreur d'authentification", "Utilisateur non trouvé.")
            self.email_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.email_frame.configure(border_color="#ef4444")
            self.email_entry.focus()
        elif status == "WRONG_PASSWORD":
            self.password_error_label.configure(text="❌ Mot de passe incorrect.")
            self.password_frame.configure(border_color="#ef4444")
            self.password_entry.delete(0, 'end')
            self.password_entry.focus()
        elif status == "DATABASE_ERROR":
            self.show_popup_error("Erreur de connexion", "Impossible de se connecter à la base de données.")
        else:
            # Cas d'erreur inattendue
            self.show_popup_error("Erreur d'authentification", "Erreur inattendue. Veuillez réessayer.")

    def redirect_to_dashboard(self, user):
        """Redirige vers le dashboard"""
        try:
            print(f"Redirection avec utilisateur: {user}")
            self.master.show_dashboard(user)
        except Exception as e:
            print(f"Erreur lors de la redirection: {e}")
            # Fallback: afficher un message d'erreur
            error_label = ctk.CTkLabel(self.master, text=f"Erreur de redirection: {e}", font=("Segoe UI", 16), text_color="red")
            error_label.pack(expand=True)

    def create_footer_links(self):
        footer = ctk.CTkFrame(self.card_content, fg_color="transparent")
        footer.pack(side="bottom", fill="x", pady=(8, 10))
        links = [("Mot de passe oublié", lambda: print("Mot de passe oublié")), ("Aide", self.show_help_popup)]
        for i, (text, command) in enumerate(links):
            btn = ctk.CTkButton(footer, text=text, command=command, fg_color="transparent", hover_color="#f1f5f9", text_color="#2563eb", anchor="center")
            btn.pack(side="left", expand=True, padx=5)

    def show_popup(self, title, message, icon):
        popup = ctk.CTkToplevel(self.master)
        popup.title(title)
        popup.attributes("-topmost", True)
        popup.grab_set()

        width, height = (400, 220) if icon == "ℹ️" else (320, 160)
        x = self.master.winfo_x() + (self.master.winfo_width() - width) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - height) // 2
        popup.geometry(f"{width}x{height}+{x}+{y}")

        ctk.CTkLabel(popup, text=icon, font=("Segoe UI", 34)).pack(pady=(10,0))
        ctk.CTkLabel(popup, text=message, font=("Segoe UI", 14), wraplength=width-40, justify="left").pack(pady=10, padx=20, expand=True)
        ok_button = ctk.CTkButton(popup, text="OK", command=popup.destroy, width=80)
        ok_button.pack(pady=15)
        
        popup.wait_window()

    def show_popup_error(self, title, message):
        self.show_popup(title, message, "⚠️")

    def show_help_popup(self):
        title = "Aide & Support"
        message = "Contacter le Support Informatique\n\nPour toute assistance technique, veuillez contacter le service IT :\n\nEmail : support.it@sac.com\nTéléphone : 01 23 45 67 89"
        self.show_popup(title, message, "ℹ️")

    def show_success_popup(self, title, message):
        """Affiche un pop-up de succès vert très rapide"""
        popup = ctk.CTkToplevel(self.master)
        popup.title(title)
        popup.attributes("-topmost", True)
        popup.grab_set()
        popup.configure(fg_color='#f0fdf4')  # Fond vert clair

        width, height = 350, 180
        x = self.master.winfo_x() + (self.master.winfo_width() - width) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - height) // 2
        popup.geometry(f"{width}x{height}+{x}+{y}")

        ctk.CTkLabel(popup, text="✅", font=("Segoe UI", 48), text_color="#22c55e").pack(pady=(20,0))
        ctk.CTkLabel(popup, text=title, font=("Segoe UI", 18, "bold"), text_color="#166534").pack(pady=(5,0))
        ctk.CTkLabel(popup, text=message, font=("Segoe UI", 14), text_color="#166534").pack(pady=(5,20))
        
        # Le pop-up se ferme automatiquement après 0.8 secondes (temps pour le voir)
        popup.after(800, popup.destroy)

class App(ctk.CTk):
    """La fenêtre principale et le contrôleur de l'application."""
    def __init__(self):
        super().__init__()

        self.title("SAC - Système de Gestion d'Entrepôts")
        self.geometry("1000x600")
        self.minsize(800, 500)
        ctk.set_appearance_mode("light")

        self.current_frame = None
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        self.setup_background()
        self.setup_icon()
        
        self.show_auth_frame()

    def setup_background(self):
        try:
            bg_image_path = os.path.join(self.base_path, "entrepot_bg.jpg")
            self.bg_image = ctk.CTkImage(light_image=Image.open(bg_image_path), size=(1000, 600))
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
        except FileNotFoundError:
            self.bg_image = None
            self.bg_label = ctk.CTkLabel(self, text="Image 'entrepot_bg.jpg' non trouvée", fg_color="gray", font=("Segoe UI", 24))
        
        self.bind("<Configure>", self.on_resize)
    
    def setup_icon(self):
        try:
            icon_path = os.path.join(self.base_path, "logo.ico")
            self.iconbitmap(icon_path)
        except Exception:
            try:
                icon_path_png = os.path.join(self.base_path, "logo.png")
                self.iconphoto(False, tk.PhotoImage(file=icon_path_png))
            except Exception:
                pass
    
    def show_auth_frame(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.current_frame = AuthFrame(self)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")

    def show_dashboard(self, user):
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        self.bg_label.place_forget()
        if DashboardFrame is not None:
            self.current_frame = DashboardFrame(self, user, toplevel_window=self)
            self.current_frame.pack(fill="both", expand=True)
        else:
            print("Erreur: DashboardFrame n'est pas disponible")
            # Fallback: afficher un message d'erreur
            error_label = ctk.CTkLabel(self, text="Erreur: Impossible de charger le dashboard", font=("Segoe UI", 16), text_color="red")
            error_label.pack(expand=True)

    def on_resize(self, event):
        if self.bg_image:
            self.bg_image.configure(size=(event.width, event.height))

if __name__ == "__main__":
    app = App()
    app.mainloop()
