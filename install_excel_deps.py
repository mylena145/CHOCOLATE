#!/usr/bin/env python3
"""
Script d'installation des dépendances pour l'export Excel avec formatage
"""

import subprocess
import sys

def install_package(package):
    """Installer un package via pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installé avec succès")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Erreur lors de l'installation de {package}")
        return False

def main():
    print("🚀 Installation des dépendances pour l'export Excel...")
    print("=" * 50)
    
    packages = [
        "pandas",
        "openpyxl",
        "xlsxwriter"
    ]
    
    success_count = 0
    for package in packages:
        print(f"\n📦 Installation de {package}...")
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 50)
    if success_count == len(packages):
        print("🎉 Toutes les dépendances ont été installées avec succès!")
        print("✨ L'export Excel avec formatage est maintenant disponible")
        print("\n📋 Fonctionnalités disponibles:")
        print("   • Export en format .xlsx avec en-têtes colorés")
        print("   • Lignes alternées pour une meilleure lisibilité")
        print("   • Largeur des colonnes ajustée automatiquement")
        print("   • Ouverture automatique du fichier après export")
    else:
        print(f"⚠️ {len(packages) - success_count} package(s) n'ont pas pu être installé(s)")
        print("🔧 Vérifiez votre connexion internet et réessayez")

if __name__ == "__main__":
    main() 