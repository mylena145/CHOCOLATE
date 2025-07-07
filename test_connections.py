#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier les connexions entre BD, Backend et Frontend
"""

import sys
import traceback

def test_database_connection():
    """Test de la connexion à la base de données PostgreSQL"""
    print("🔍 Test de connexion à la base de données...")
    try:
        import psycopg2
        from database import PG_CONN
        
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        # Test simple de requête
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print(f"✅ Connexion PostgreSQL réussie - Version: {version[0]}")
        
        # Test de la table produits
        cursor.execute("SELECT COUNT(*) FROM sge_cre.produits")
        count = cursor.fetchone()
        print(f"✅ Table produits accessible - {count[0]} produits trouvés")
        
        # Test de la table individus
        cursor.execute("SELECT COUNT(*) FROM sge_cre.individus")
        count = cursor.fetchone()
        print(f"✅ Table individus accessible - {count[0]} utilisateurs trouvés")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def test_backend_functions():
    """Test des fonctions backend"""
    print("\n🔍 Test des fonctions backend...")
    try:
        import database
        
        # Test de la fonction get_all_products
        products = database.get_all_products()
        print(f"✅ Fonction get_all_products() - {len(products)} produits récupérés")
        
        # Test de la fonction list_users
        users = database.list_users()
        print(f"✅ Fonction list_users() - {len(users)} utilisateurs récupérés")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans les fonctions backend: {e}")
        traceback.print_exc()
        return False

def test_frontend_imports():
    """Test des imports du frontend"""
    print("\n🔍 Test des imports du frontend...")
    try:
        import customtkinter as ctk
        print("✅ CustomTkinter importé avec succès")
        
        # Test des modules principaux
        modules_to_test = [
            'AUTHENTIFICATION',
            'dashboard', 
            'stock_management_page',
            'reception_page',
            'rapport_analytics',
            'warehouse_page',
            'Expeditions'
        ]
        
        for module in modules_to_test:
            try:
                __import__(module)
                print(f"✅ Module {module} importé avec succès")
            except ImportError as e:
                print(f"❌ Erreur import module {module}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans les imports frontend: {e}")
        return False

def test_app_launch():
    """Test du lancement de l'application"""
    print("\n🔍 Test du lancement de l'application...")
    try:
        # Test d'import de l'app principale
        from app import App
        print("✅ Classe App importée avec succès")
        
        # Test de création de l'instance (sans lancer la boucle principale)
        app = App()
        print("✅ Instance de l'application créée avec succès")
        
        # Fermer proprement
        app.destroy()
        print("✅ Application fermée proprement")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'application: {e}")
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests de connexion...\n")
    
    tests = [
        ("Base de données", test_database_connection),
        ("Fonctions Backend", test_backend_functions),
        ("Imports Frontend", test_frontend_imports),
        ("Lancement App", test_app_launch)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 TOUS LES TESTS SONT PASSÉS !")
        print("✅ La base de données, le backend et le frontend sont connectés.")
        print("\n📝 Instructions pour tester l'application complète:")
        print("1. Lancez l'application: python app.py")
        print("2. Connectez-vous avec un utilisateur existant")
        print("3. Testez les différentes fonctionnalités")
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("❌ Vérifiez les erreurs ci-dessus avant de lancer l'application")
    
    print("="*50)

if __name__ == "__main__":
    main() 