
def create_export_buttons(self, parent):
    """Crée les boutons d'export pour l'interface graphique"""
    
    # Frame pour les boutons d'export
    export_frame = customtkinter.CTkFrame(parent)
    export_frame.pack(fill="x", padx=10, pady=5)
    
    # Titre
    title_label = customtkinter.CTkLabel(export_frame, text="📤 Export des Données", 
                                       font=customtkinter.CTkFont(size=16, weight="bold"))
    title_label.pack(pady=5)
    
    # Frame pour les boutons
    buttons_frame = customtkinter.CTkFrame(export_frame)
    buttons_frame.pack(fill="x", padx=10, pady=5)
    
    def export_users():
        """Export des utilisateurs"""
        try:
            downloads_path = self.get_downloads_folder()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{downloads_path}/SGE_Utilisateurs_{timestamp}.csv"
            
            # Créer une copie locale
            if not os.path.exists("exports"):
                os.makedirs("exports")
            local_filename = f"exports/utilisateurs_{timestamp}.csv"
            
            # Exporter les données
            conn = psycopg2.connect(**PG_CONN)
            cursor = conn.cursor()
            cursor.execute("SELECT nom, prenom, email, role, matricule, adresse, telephone FROM sge_cre.individus ORDER BY nom")
            users = cursor.fetchall()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['NOM', 'PRÉNOM', 'EMAIL', 'RÔLE', 'MATRICULE', 'ADRESSE', 'TÉLÉPHONE'])
                writer.writerow(['---', '---', '---', '---', '---', '---', '---'])
                for user in users:
                    writer.writerow(user)
            
            # Créer une copie locale
            try:
                import shutil
                shutil.copy2(filename, local_filename)
            except Exception as e:
                print(f"⚠️ Impossible de créer la copie locale: {e}")
            
            # Ouvrir le fichier automatiquement
            try:
                import subprocess
                import platform
                abs_path = os.path.abspath(filename)
                system = platform.system()
                if system == "Windows":
                    os.startfile(abs_path)
                elif system == "Darwin":  # macOS
                    subprocess.run(["open", abs_path])
                else:  # Linux
                    subprocess.run(["xdg-open", abs_path])
            except Exception as e:
                print(f"⚠️ Impossible d'ouvrir le fichier automatiquement: {e}")
            
            # Afficher une notification
            self.show_export_notification(f"✅ {len(users)} utilisateur(s) exporté(s) vers les téléchargements")
            
            conn.close()
            
        except Exception as e:
            self.show_export_notification(f"❌ Erreur lors de l'export: {e}")
    
    def export_products():
        """Export des produits"""
        try:
            downloads_path = self.get_downloads_folder()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{downloads_path}/SGE_Produits_{timestamp}.csv"
            
            # Créer une copie locale
            if not os.path.exists("exports"):
                os.makedirs("exports")
            local_filename = f"exports/produits_{timestamp}.csv"
            
            # Exporter les données
            conn = psycopg2.connect(**PG_CONN)
            cursor = conn.cursor()
            cursor.execute("SELECT nom, description, marque, modele, fournisseur, stock FROM sge_cre.produits ORDER BY nom")
            products = cursor.fetchall()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['NOM', 'DESCRIPTION', 'MARQUE', 'MODÈLE', 'FOURNISSEUR', 'STOCK'])
                writer.writerow(['---', '---', '---', '---', '---', '---'])
                for product in products:
                    writer.writerow(product)
            
            # Créer une copie locale
            try:
                import shutil
                shutil.copy2(filename, local_filename)
            except Exception as e:
                print(f"⚠️ Impossible de créer la copie locale: {e}")
            
            # Ouvrir le fichier automatiquement
            try:
                import subprocess
                import platform
                abs_path = os.path.abspath(filename)
                system = platform.system()
                if system == "Windows":
                    os.startfile(abs_path)
                elif system == "Darwin":  # macOS
                    subprocess.run(["open", abs_path])
                else:  # Linux
                    subprocess.run(["xdg-open", abs_path])
            except Exception as e:
                print(f"⚠️ Impossible d'ouvrir le fichier automatiquement: {e}")
            
            # Afficher une notification
            self.show_export_notification(f"✅ {len(products)} produit(s) exporté(s) vers les téléchargements")
            
            conn.close()
            
        except Exception as e:
            self.show_export_notification(f"❌ Erreur lors de l'export: {e}")
    
    # Boutons d'export
    users_btn = customtkinter.CTkButton(buttons_frame, text="👥 Export Utilisateurs", 
                                      command=export_users, fg_color="#366092", hover_color="#2E4A6B")
    users_btn.pack(side="left", padx=5, pady=5)
    
    products_btn = customtkinter.CTkButton(buttons_frame, text="📦 Export Produits", 
                                         command=export_products, fg_color="#366092", hover_color="#2E4A6B")
    products_btn.pack(side="left", padx=5, pady=5)
    
    return export_frame

def show_export_notification(self, message):
    """Affiche une notification d'export"""
    # Créer une fenêtre de notification
    notification = customtkinter.CTkToplevel(self)
    notification.title("📤 Export")
    notification.geometry("400x150")
    notification.resizable(False, False)
    
    # Centrer la fenêtre
    notification.update_idletasks()
    x = (notification.winfo_screenwidth() // 2) - (400 // 2)
    y = (notification.winfo_screenheight() // 2) - (150 // 2)
    notification.geometry(f"400x150+{x}+{y}")
    
    # Contenu
    label = customtkinter.CTkLabel(notification, text=message, font=customtkinter.CTkFont(size=14))
    label.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Fermer automatiquement après 3 secondes
    notification.after(3000, notification.destroy)
