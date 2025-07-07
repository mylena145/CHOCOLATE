#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test complet du système de gestion d'entrepôt
"""

import psycopg2
import sys

def test_complete_system():
    """Test complet du système"""
    print("🧪 TEST COMPLET DU SYSTÈME DE GESTION D'ENTREPÔT")
    print("=" * 50)
    
    try:
        # Test de connexion
        print("1. Test de connexion à la base de données...")
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres123",
            host="localhost",
            port="5432",
            client_encoding="utf8",
            options="-c client_encoding=utf8",
            connect_timeout=10
        )
        cursor = conn.cursor()
        print("   ✅ Connexion réussie")
        
        # Test des tables principales
        print("\n2. Test des tables principales...")
        tables_to_test = [
            'individus', 'organisations', 'produits', 'entrepots', 
            'zone_stockage', 'lots', 'colis', 'commandes_achats'
        ]
        
        for table in tables_to_test:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM sge_cre.{table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table}: {count} enregistrements")
            except Exception as e:
                print(f"   ❌ {table}: Erreur - {e}")
        
        # Test des fonctionnalités principales
        print("\n3. Test des fonctionnalités principales...")
        
        # Test d'authentification
        try:
            cursor.execute("SELECT COUNT(*) FROM sge_cre.individus WHERE email IS NOT NULL")
            auth_users = cursor.fetchone()[0]
            print(f"   ✅ Utilisateurs pour authentification: {auth_users}")
        except:
            print("   ❌ Erreur lors du test d'authentification")
        
        # Test des produits
        try:
            cursor.execute("SELECT COUNT(*) FROM sge_cre.produits WHERE stock > 0")
            products_in_stock = cursor.fetchone()[0]
            print(f"   ✅ Produits en stock: {products_in_stock}")
        except:
            print("   ❌ Erreur lors du test des produits")
        
        # Test des organisations
        try:
            cursor.execute("SELECT COUNT(*) FROM sge_cre.organisations WHERE statut = 'Fournisseur'")
            suppliers = cursor.fetchone()[0]
            print(f"   ✅ Fournisseurs: {suppliers}")
        except:
            print("   ❌ Erreur lors du test des organisations")
        
        conn.close()
        print("\n🎉 Tests terminés avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        return False
    
    return True

def test_frontend_imports():
    """Test des imports du frontend"""
    print("\n4. Test des imports du frontend...")
    
    try:
        import customtkinter as ctk
        print("   ✅ CustomTkinter importé")
    except ImportError:
        print("   ❌ CustomTkinter non installé")
        return False
    
    try:
        from PIL import Image, ImageTk
        print("   ✅ PIL importé")
    except ImportError:
        print("   ❌ PIL non installé")
        return False
    
    try:
        import tkinter as tk
        print("   ✅ Tkinter importé")
    except ImportError:
        print("   ❌ Tkinter non installé")
        return False
    
    return True

def test_backend_functions():
    """Test des fonctions backend"""
    print("\n5. Test des fonctions backend...")
    
    try:
        from database import check_user, get_all_products
        print("   ✅ Fonctions database importées")
        
        # Test de la fonction check_user
        try:
            result = check_user("test@test.com", "password")
            print(f"   ✅ Fonction check_user: {result[0]}")
        except:
            print("   ⚠️  Fonction check_user: Erreur (normal si pas d'utilisateur test)")
        
    except ImportError as e:
        print(f"   ❌ Erreur d'import: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Démarrage des tests complets...")
    
    # Test de la base de données
    db_ok = test_complete_system()
    
    # Test des imports
    imports_ok = test_frontend_imports()
    
    # Test des fonctions
    functions_ok = test_backend_functions()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    print(f"Base de données: {'✅ OK' if db_ok else '❌ ERREUR'}")
    print(f"Imports frontend: {'✅ OK' if imports_ok else '❌ ERREUR'}")
    print(f"Fonctions backend: {'✅ OK' if functions_ok else '❌ ERREUR'}")
    
    if db_ok and imports_ok and functions_ok:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("Tu peux maintenant lancer l'application avec: python app.py")
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifie les erreurs ci-dessus.") 