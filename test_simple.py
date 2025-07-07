#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test simplifié pour vérifier les connexions
"""

def test_frontend_only():
    """Test uniquement du frontend sans base de données"""
    print("🔍 Test du frontend (sans base de données)...")
    try:
        import customtkinter as ctk
        print("✅ CustomTkinter importé avec succès")
        
        # Test des modules principaux
        modules_to_test = [
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

def test_database_manual():
    """Test manuel de la base de données"""
    print("\n🔍 Test manuel de la base de données...")
    try:
        import psycopg2
        
        # Connexion avec paramètres explicites
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432",
            client_encoding="utf8"
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print(f"✅ Connexion PostgreSQL réussie - Version: {version[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        print("💡 Vérifiez que PostgreSQL est démarré et accessible")
        return False

def test_app_without_db():
    """Test de l'application sans initialisation de la base"""
    print("\n🔍 Test de l'application (sans initialisation DB)...")
    try:
        # Modifier temporairement la fonction init_database
        import database
        original_init = database.init_database
        
        def mock_init():
            print("✅ Initialisation de la base désactivée pour le test")
        
        database.init_database = mock_init
        
        # Test d'import de l'app principale
        from app import App
        print("✅ Classe App importée avec succès")
        
        # Test de création de l'instance (sans lancer la boucle principale)
        app = App()
        print("✅ Instance de l'application créée avec succès")
        
        # Fermer proprement
        app.destroy()
        print("✅ Application fermée proprement")
        
        # Restaurer la fonction originale
        database.init_database = original_init
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'application: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests simplifiés...\n")
    
    tests = [
        ("Frontend (sans DB)", test_frontend_only),
        ("Base de données manuelle", test_database_manual),
        ("Application (sans init DB)", test_app_without_db)
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
    print("📊 RÉSUMÉ DES TESTS SIMPLIFIÉS")
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
        print("✅ Le frontend et la base de données sont fonctionnels.")
        print("\n📝 Instructions pour tester l'application complète:")
        print("1. Assurez-vous que PostgreSQL est démarré")
        print("2. Lancez l'application: python app.py")
        print("3. Connectez-vous avec un utilisateur existant")
        print("4. Testez les différentes fonctionnalités")
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("❌ Vérifiez les erreurs ci-dessus")
        print("\n💡 Solutions possibles:")
        print("- Vérifiez que PostgreSQL est installé et démarré")
        print("- Vérifiez les paramètres de connexion dans database.py")
        print("- Vérifiez que toutes les dépendances Python sont installées")
    
    print("="*50)

if __name__ == "__main__":
    main() 