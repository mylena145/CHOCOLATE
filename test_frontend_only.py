#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test uniquement du frontend sans base de données
"""

def test_customtkinter():
    """Test de CustomTkinter"""
    print("🔍 Test de CustomTkinter...")
    try:
        import customtkinter as ctk
        print("✅ CustomTkinter importé avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur CustomTkinter: {e}")
        return False

def test_modules_individually():
    """Test des modules un par un"""
    print("\n🔍 Test des modules individuels...")
    
    modules = [
        'dashboard',
        'stock_management_page', 
        'reception_page',
        'rapport_analytics',
        'warehouse_page',
        'Expeditions'
    ]
    
    success_count = 0
    for module in modules:
        try:
            # Essayer d'importer sans déclencher l'initialisation de la base
            module_obj = __import__(module, fromlist=['*'])
            print(f"✅ Module {module} importé avec succès")
            success_count += 1
        except Exception as e:
            print(f"❌ Erreur module {module}: {e}")
    
    return success_count == len(modules)

def test_app_creation():
    """Test de création de l'application"""
    print("\n🔍 Test de création de l'application...")
    try:
        # Désactiver temporairement les imports de base de données
        import sys
        import types
        
        # Créer un module mock pour database
        mock_database = types.ModuleType('database')
        mock_database.check_user = lambda email, password: ("SUCCESS", {"id": 1, "nom": "Test", "role": "admin"})
        mock_database.get_all_products = lambda: []
        mock_database.list_users = lambda: []
        mock_database.init_database = lambda: None
        mock_database.init_movements_tables = lambda: None
        
        # Remplacer le module database
        sys.modules['database'] = mock_database
        
        # Importer l'app
        from app import App
        print("✅ Classe App importée avec succès")
        
        # Créer une instance
        app = App()
        print("✅ Instance de l'application créée avec succès")
        
        # Fermer
        app.destroy()
        print("✅ Application fermée proprement")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création app: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🚀 Test du frontend uniquement...\n")
    
    tests = [
        ("CustomTkinter", test_customtkinter),
        ("Modules individuels", test_modules_individually),
        ("Création application", test_app_creation)
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
    print("📊 RÉSUMÉ DES TESTS FRONTEND")
    print("="*50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 FRONTEND FONCTIONNEL !")
        print("✅ L'interface utilisateur est prête.")
        print("\n📝 Prochaines étapes:")
        print("1. Résoudre le problème de connexion PostgreSQL")
        print("2. Vérifier les paramètres de connexion")
        print("3. Tester l'application complète")
    else:
        print("⚠️  PROBLÈMES DÉTECTÉS DANS LE FRONTEND")
        print("❌ Vérifiez les erreurs ci-dessus")
    
    print("="*50)

if __name__ == "__main__":
    main() 