#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour tester l'export des rapports vers le dossier Téléchargements du PC
"""

import os
import datetime
import csv
import json
import psycopg2
import platform
import subprocess

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

def get_downloads_folder():
    """Obtient le dossier Téléchargements du système"""
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
        print(f"⚠️ Dossier téléchargements non trouvé, utilisation du dossier local: {downloads_path}")
    else:
        print(f"✅ Dossier téléchargements trouvé: {downloads_path}")
    
    return downloads_path

def export_users_to_downloads(format_export="csv"):
    """Exporte les utilisateurs vers le dossier téléchargements"""
    print(f"📤 Export des utilisateurs au format {format_export.upper()}...")
    
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        cursor.execute("SELECT nom, prenom, email, role, matricule, adresse, telephone FROM sge_cre.individus ORDER BY nom")
        users = cursor.fetchall()
        
        # Obtenir le dossier téléchargements
        downloads_path = get_downloads_folder()
        
        # Créer le nom de fichier
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{downloads_path}/SGE_Utilisateurs_{timestamp}.{format_export}"
        
        # Créer aussi une copie locale
        if not os.path.exists("exports"):
            os.makedirs("exports")
        local_filename = f"exports/utilisateurs_{timestamp}.{format_export}"
        
        if format_export == "csv":
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['NOM', 'PRÉNOM', 'EMAIL', 'RÔLE', 'MATRICULE', 'ADRESSE', 'TÉLÉPHONE'])
                writer.writerow(['---', '---', '---', '---', '---', '---', '---'])
                for user in users:
                    writer.writerow(user)
        
        elif format_export == "json":
            data = []
            for user in users:
                data.append({
                    'nom': user[0],
                    'prenom': user[1],
                    'email': user[2],
                    'role': user[3],
                    'matricule': user[4],
                    'adresse': user[5],
                    'telephone': user[6]
                })
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        # Créer une copie locale
        try:
            import shutil
            shutil.copy2(filename, local_filename)
            print(f"✅ Export terminé: {filename}")
            print(f"📁 Copie locale: {local_filename}")
            print(f"📊 {len(users)} utilisateur(s) exporté(s)")
        except Exception as e:
            print(f"✅ Export terminé: {filename}")
            print(f"⚠️ Impossible de créer la copie locale: {e}")
            print(f"📊 {len(users)} utilisateur(s) exporté(s)")
        
        # Ouvrir le fichier automatiquement
        try:
            abs_path = os.path.abspath(filename)
            print(f"📁 Fichier sauvegardé: {abs_path}")
            
            system = platform.system()
            if system == "Windows":
                os.startfile(abs_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", abs_path])
            else:  # Linux
                subprocess.run(["xdg-open", abs_path])
            
            print(f"🚀 Fichier ouvert automatiquement!")
            
        except Exception as e:
            print(f"⚠️ Impossible d'ouvrir le fichier automatiquement: {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")
        return False

def export_products_to_downloads(format_export="csv"):
    """Exporte les produits vers le dossier téléchargements"""
    print(f"📤 Export des produits au format {format_export.upper()}...")
    
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        cursor.execute("SELECT nom, description, marque, modele, fournisseur, stock FROM sge_cre.produits ORDER BY nom")
        products = cursor.fetchall()
        
        # Obtenir le dossier téléchargements
        downloads_path = get_downloads_folder()
        
        # Créer le nom de fichier
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{downloads_path}/SGE_Produits_{timestamp}.{format_export}"
        
        # Créer aussi une copie locale
        if not os.path.exists("exports"):
            os.makedirs("exports")
        local_filename = f"exports/produits_{timestamp}.{format_export}"
        
        if format_export == "csv":
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['NOM', 'DESCRIPTION', 'MARQUE', 'MODÈLE', 'FOURNISSEUR', 'STOCK'])
                writer.writerow(['---', '---', '---', '---', '---', '---'])
                for product in products:
                    writer.writerow(product)
        
        elif format_export == "json":
            data = []
            for product in products:
                data.append({
                    'nom': product[0],
                    'description': product[1],
                    'marque': product[2],
                    'modele': product[3],
                    'fournisseur': product[4],
                    'stock': product[5]
                })
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        # Créer une copie locale
        try:
            import shutil
            shutil.copy2(filename, local_filename)
            print(f"✅ Export terminé: {filename}")
            print(f"📁 Copie locale: {local_filename}")
            print(f"📊 {len(products)} produit(s) exporté(s)")
        except Exception as e:
            print(f"✅ Export terminé: {filename}")
            print(f"⚠️ Impossible de créer la copie locale: {e}")
            print(f"📊 {len(products)} produit(s) exporté(s)")
        
        # Ouvrir le fichier automatiquement
        try:
            abs_path = os.path.abspath(filename)
            print(f"📁 Fichier sauvegardé: {abs_path}")
            
            system = platform.system()
            if system == "Windows":
                os.startfile(abs_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", abs_path])
            else:  # Linux
                subprocess.run(["xdg-open", abs_path])
            
            print(f"🚀 Fichier ouvert automatiquement!")
            
        except Exception as e:
            print(f"⚠️ Impossible d'ouvrir le fichier automatiquement: {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")
        return False

def export_packaging_to_downloads(format_export="csv"):
    """Exporte les emballages vers le dossier téléchargements"""
    print(f"📤 Export des emballages au format {format_export.upper()}...")
    
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        cursor.execute("SELECT type_emballage, etat_emballage FROM sge_cre.materiel_emballage ORDER BY type_emballage")
        packaging = cursor.fetchall()
        
        # Obtenir le dossier téléchargements
        downloads_path = get_downloads_folder()
        
        # Créer le nom de fichier
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{downloads_path}/SGE_Emballages_{timestamp}.{format_export}"
        
        # Créer aussi une copie locale
        if not os.path.exists("exports"):
            os.makedirs("exports")
        local_filename = f"exports/emballages_{timestamp}.{format_export}"
        
        if format_export == "csv":
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(['TYPE', 'ÉTAT'])
                writer.writerow(['---', '---'])
                for pack in packaging:
                    writer.writerow(pack)
        
        elif format_export == "json":
            data = []
            for pack in packaging:
                data.append({
                    'type': pack[0],
                    'etat': pack[1]
                })
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        # Créer une copie locale
        try:
            import shutil
            shutil.copy2(filename, local_filename)
            print(f"✅ Export terminé: {filename}")
            print(f"📁 Copie locale: {local_filename}")
            print(f"📊 {len(packaging)} emballage(s) exporté(s)")
        except Exception as e:
            print(f"✅ Export terminé: {filename}")
            print(f"⚠️ Impossible de créer la copie locale: {e}")
            print(f"📊 {len(packaging)} emballage(s) exporté(s)")
        
        # Ouvrir le fichier automatiquement
        try:
            abs_path = os.path.abspath(filename)
            print(f"📁 Fichier sauvegardé: {abs_path}")
            
            system = platform.system()
            if system == "Windows":
                os.startfile(abs_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", abs_path])
            else:  # Linux
                subprocess.run(["xdg-open", abs_path])
            
            print(f"🚀 Fichier ouvert automatiquement!")
            
        except Exception as e:
            print(f"⚠️ Impossible d'ouvrir le fichier automatiquement: {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")
        return False

def main():
    print("🚀 Test d'export vers le dossier Téléchargements")
    print("=" * 60)
    
    # Vérifier le dossier téléchargements
    downloads_path = get_downloads_folder()
    print(f"📁 Dossier téléchargements: {downloads_path}")
    
    # Tester les exports
    print("\n📊 Tests d'export...")
    
    # Export utilisateurs
    print("\n👥 Export utilisateurs:")
    export_users_to_downloads("csv")
    
    # Export produits
    print("\n📦 Export produits:")
    export_products_to_downloads("csv")
    
    # Export emballages
    print("\n📦 Export emballages:")
    export_packaging_to_downloads("csv")
    
    print("\n🎉 Tests terminés!")
    print(f"\n📁 Vérifiez vos fichiers dans: {downloads_path}")
    print("📁 Et dans le dossier local: exports/")

if __name__ == "__main__":
    main() 