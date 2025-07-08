#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour mettre à jour l'interface graphique avec l'export vers les téléchargements
"""

import re
import os

def update_export_functionality():
    """Met à jour la fonctionnalité d'export dans admin_page.py"""
    
    print("🔧 Mise à jour de la fonctionnalité d'export vers les téléchargements...")
    
    # Lire le fichier admin_page.py
    try:
        with open('admin_page.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ Fichier admin_page.py non trouvé")
        return False
    
    # Vérifier si la fonctionnalité est déjà présente
    if "get_downloads_folder" in content:
        print("✅ La fonctionnalité d'export vers les téléchargements est déjà présente")
        return True
    
    # Ajouter la fonction get_downloads_folder
    downloads_function = '''
    def get_downloads_folder(self):
        """Obtient le dossier Téléchargements du système"""
        import os
        import platform
        
        # Essayer différents chemins selon le système d'exploitation
        system = platform.system()
        
        if system == "Windows":
            # Windows - utiliser le dossier Downloads de l'utilisateur
            downloads_path = os.path.expanduser("~/Downloads")
            if not os.path.exists(downloads_path):
                downloads_path = os.path.expanduser("~/Téléchargements")
        elif system == "Darwin":  # macOS
            downloads_path = os.path.expanduser("~/Downloads")
        else:  # Linux
            downloads_path = os.path.expanduser("~/Downloads")
            if not os.path.exists(downloads_path):
                downloads_path = os.path.expanduser("~/Téléchargements")
        
        # Fallback vers le dossier exports local si le dossier téléchargements n'existe pas
        if not os.path.exists(downloads_path):
            downloads_path = "exports"
        
        return downloads_path
'''
    
    # Trouver l'endroit où ajouter la fonction (après les imports)
    if 'class AdminFrame' in content:
        # Ajouter la fonction après la définition de la classe
        class_pattern = r'(class AdminFrame.*?)(def __init__)'
        match = re.search(class_pattern, content, re.DOTALL)
        if match:
            new_content = content.replace(
                match.group(1),
                match.group(1) + downloads_function + '\n    '
            )
            content = new_content
        else:
            print("❌ Impossible de trouver la classe AdminFrame")
            return False
    else:
        print("❌ Classe AdminFrame non trouvée")
        return False
    
    # Mettre à jour la fonction _cli_export pour utiliser le dossier téléchargements
    export_pattern = r'(def _cli_export\(self, args\):.*?)(# Créer le dossier exports s\'il n\'existe pas)'
    match = re.search(export_pattern, content, re.DOTALL)
    
    if match:
        new_export_code = '''
        # Créer le dossier exports s'il n'existe pas
        import os
        if not os.path.exists("exports"):
            os.makedirs("exports")
        
        # Obtenir le dossier Téléchargements du système
        downloads_path = self.get_downloads_folder()
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{downloads_path}/SGE_{table}_{timestamp}.{format_export}"
        
        # Créer aussi une copie dans le dossier exports local
        local_filename = f"exports/{table}_{timestamp}.{format_export}"
'''
        
        content = content.replace(match.group(2), new_export_code)
        
        # Ajouter la logique de copie locale et d'ouverture automatique
        # Chercher les endroits où afficher les messages de succès
        success_pattern = r'(output\.insert\("end", f"✅ Export terminé: \{filename\}\\n"\)\n\s*output\.insert\("end", f"📊 \{len\([^)]+\)\} [^)]+\) exporté\(s\)\\n"\))'
        
        new_success_code = '''
                # Créer une copie locale
                try:
                    import shutil
                    shutil.copy2(filename, local_filename)
                    output.insert("end", f"✅ Export terminé: {filename}\\n")
                    output.insert("end", f"📁 Copie locale: {local_filename}\\n")
                    output.insert("end", f"📊 {len(users)} utilisateur(s) exporté(s)\\n")
                except Exception as e:
                    output.insert("end", f"✅ Export terminé: {filename}\\n")
                    output.insert("end", f"⚠️ Impossible de créer la copie locale: {e}\\n")
                    output.insert("end", f"📊 {len(users)} utilisateur(s) exporté(s)\\n")
                
                # Ouvrir le fichier automatiquement
                try:
                    import os
                    import subprocess
                    import platform
                    
                    # Obtenir le chemin absolu du fichier
                    abs_path = os.path.abspath(filename)
                    output.insert("end", f"📁 Fichier sauvegardé: {abs_path}\\n")
                    
                    # Ouvrir le fichier selon le système d'exploitation
                    system = platform.system()
                    if system == "Windows":
                        os.startfile(abs_path)
                    elif system == "Darwin":  # macOS
                        subprocess.run(["open", abs_path])
                    else:  # Linux
                        subprocess.run(["xdg-open", abs_path])
                    
                    output.insert("end", f"🚀 Fichier ouvert automatiquement!\\n")
                    
                except Exception as e:
                    output.insert("end", f"⚠️ Impossible d'ouvrir le fichier automatiquement: {e}\\n")
'''
        
        # Remplacer les messages de succès existants
        content = re.sub(success_pattern, new_success_code, content, flags=re.DOTALL)
    
    # Écrire le fichier mis à jour
    try:
        with open('admin_page.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Fichier admin_page.py mis à jour avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'écriture du fichier: {e}")
        return False

def create_export_buttons_update():
    """Crée un script pour ajouter des boutons d'export dans l'interface"""
    
    print("🎨 Création de boutons d'export pour l'interface graphique...")
    
    button_code = '''
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
'''
    
    # Écrire le code dans un fichier séparé
    with open('export_buttons_code.py', 'w', encoding='utf-8') as f:
        f.write(button_code)
    
    print("✅ Code des boutons d'export créé dans export_buttons_code.py")
    return True

def main():
    print("🚀 Mise à jour de la fonctionnalité d'export vers les téléchargements")
    print("=" * 70)
    
    # Mettre à jour la fonctionnalité principale
    if update_export_functionality():
        print("✅ Fonctionnalité principale mise à jour")
    else:
        print("❌ Échec de la mise à jour de la fonctionnalité principale")
        return
    
    # Créer le code des boutons d'export
    if create_export_buttons_update():
        print("✅ Code des boutons d'export créé")
    else:
        print("❌ Échec de la création du code des boutons")
        return
    
    print("\n🎉 Mise à jour terminée!")
    print("\n📋 Prochaines étapes:")
    print("1. ✅ La fonctionnalité CLI est maintenant active")
    print("2. 📁 Les exports vont dans le dossier téléchargements")
    print("3. 🚀 Les fichiers s'ouvrent automatiquement")
    print("4. 📁 Une copie locale est créée dans exports/")
    print("5. 🎨 Pour ajouter des boutons dans l'interface, utilisez le code dans export_buttons_code.py")
    
    print("\n🧪 Test de la fonctionnalité:")
    print("python export_to_downloads.py")

if __name__ == "__main__":
    main() 