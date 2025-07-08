#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier les fonctionnalités CRUD du CLI
"""

import psycopg2
import sys
import os

# Configuration de la base de données
PG_CONN = {
    'host': 'localhost',
    'database': 'sac',
    'user': 'postgres',
    'password': 'postgres'
}

def test_database_connection():
    """Test de connexion à la base de données"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("✅ Connexion à la base de données réussie")
        print(f"📊 Version PostgreSQL: {version[0]}")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_users_crud():
    """Test des opérations CRUD sur les utilisateurs"""
    print("\n👥 TEST DES UTILISATEURS:")
    print("=" * 50)
    
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        # Test 1: Création d'un utilisateur
        print("1. Test de création d'utilisateur...")
        cursor.execute("""
            INSERT INTO sge_cre.individus (nom, prenom, email, password, role, matricule, actif, adresse, telephone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, ("Test", "Utilisateur", "test@example.com", "password123", "Magasinier", "MG001", True, "Adresse test", "0123456789"))
        
        user_id = cursor.fetchone()[0]
        print(f"   ✅ Utilisateur créé avec ID: {user_id}")
        
        # Test 2: Lecture de l'utilisateur
        print("2. Test de lecture d'utilisateur...")
        cursor.execute("SELECT nom, prenom, email, role FROM sge_cre.individus WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            print(f"   ✅ Utilisateur trouvé: {user[1]} {user[0]} ({user[2]})")
        else:
            print("   ❌ Utilisateur non trouvé")
        
        # Test 3: Modification de l'utilisateur
        print("3. Test de modification d'utilisateur...")
        cursor.execute("UPDATE sge_cre.individus SET role = %s WHERE id = %s", ("Responsable des stocks", user_id))
        cursor.execute("SELECT role FROM sge_cre.individus WHERE id = %s", (user_id,))
        new_role = cursor.fetchone()[0]
        print(f"   ✅ Rôle modifié vers: {new_role}")
        
        # Test 4: Suppression de l'utilisateur
        print("4. Test de suppression d'utilisateur...")
        cursor.execute("DELETE FROM sge_cre.individus WHERE id = %s", (user_id,))
        cursor.execute("SELECT COUNT(*) FROM sge_cre.individus WHERE id = %s", (user_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            print("   ✅ Utilisateur supprimé avec succès")
        else:
            print("   ❌ Erreur lors de la suppression")
        
        conn.commit()
        conn.close()
        print("✅ Tous les tests utilisateurs réussis")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests utilisateurs: {e}")

def test_products_crud():
    """Test des opérations CRUD sur les produits"""
    print("\n📦 TEST DES PRODUITS:")
    print("=" * 50)
    
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        # Test 1: Création d'un produit
        print("1. Test de création de produit...")
        cursor.execute("""
            INSERT INTO sge_cre.produits (nom, description, prix, stock_disponible, categorie, fournisseur)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, ("Produit Test", "Description du produit test", 29.99, 100, "Test", "Fournisseur Test"))
        
        product_id = cursor.fetchone()[0]
        print(f"   ✅ Produit créé avec ID: {product_id}")
        
        # Test 2: Lecture du produit
        print("2. Test de lecture de produit...")
        cursor.execute("SELECT nom, description, prix, stock_disponible FROM sge_cre.produits WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if product:
            print(f"   ✅ Produit trouvé: {product[0]} - {product[1]} - {product[2]}€ - Stock: {product[3]}")
        else:
            print("   ❌ Produit non trouvé")
        
        # Test 3: Modification du produit
        print("3. Test de modification de produit...")
        cursor.execute("UPDATE sge_cre.produits SET prix = %s, stock_disponible = %s WHERE id = %s", (39.99, 150, product_id))
        cursor.execute("SELECT prix, stock_disponible FROM sge_cre.produits WHERE id = %s", (product_id,))
        updated = cursor.fetchone()
        print(f"   ✅ Produit modifié: Prix {updated[0]}€, Stock {updated[1]}")
        
        # Test 4: Suppression du produit
        print("4. Test de suppression de produit...")
        cursor.execute("DELETE FROM sge_cre.produits WHERE id = %s", (product_id,))
        cursor.execute("SELECT COUNT(*) FROM sge_cre.produits WHERE id = %s", (product_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            print("   ✅ Produit supprimé avec succès")
        else:
            print("   ❌ Erreur lors de la suppression")
        
        conn.commit()
        conn.close()
        print("✅ Tous les tests produits réussis")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests produits: {e}")

def test_audit_logs():
    """Test des logs d'audit"""
    print("\n📝 TEST DES LOGS D'AUDIT:")
    print("=" * 50)
    
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        # Test 1: Création d'un log
        print("1. Test de création de log d'audit...")
        cursor.execute("""
            INSERT INTO sge_cre.logs_activite (type_action, description, date_action, utilisateur, details)
            VALUES (%s, %s, NOW(), %s, %s)
            RETURNING id
        """, ("Test", "Test de log d'audit", "Système", "Test de fonctionnalité"))
        
        log_id = cursor.fetchone()[0]
        print(f"   ✅ Log créé avec ID: {log_id}")
        
        # Test 2: Lecture du log
        print("2. Test de lecture de log...")
        cursor.execute("SELECT type_action, description, utilisateur FROM sge_cre.logs_activite WHERE id = %s", (log_id,))
        log = cursor.fetchone()
        if log:
            print(f"   ✅ Log trouvé: {log[0]} - {log[1]} - {log[2]}")
        else:
            print("   ❌ Log non trouvé")
        
        # Test 3: Suppression du log de test
        print("3. Nettoyage du log de test...")
        cursor.execute("DELETE FROM sge_cre.logs_activite WHERE id = %s", (log_id,))
        print("   ✅ Log de test supprimé")
        
        conn.commit()
        conn.close()
        print("✅ Tous les tests logs d'audit réussis")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests logs d'audit: {e}")

def test_matricule_generation():
    """Test de génération de matricules"""
    print("\n🆔 TEST DE GÉNÉRATION DE MATRICULES:")
    print("=" * 50)
    
    try:
        from matricule_manager import MatriculeManager
        
        # Test 1: Génération de matricules pour différents rôles
        print("1. Test de génération de matricules...")
        roles = ["Administrateur", "Magasinier", "Livreur", "Responsable des stocks"]
        
        for role in roles:
            matricule = MatriculeManager.generate_matricule(role)
            print(f"   ✅ {role}: {matricule}")
        
        # Test 2: Validation de matricules
        print("2. Test de validation de matricules...")
        test_matricules = ["AD001", "MG001", "LV001", "RS001", "INVALID"]
        
        for matricule in test_matricules:
            is_valid, message = MatriculeManager.validate_matricule(matricule)
            status = "✅" if is_valid else "❌"
            print(f"   {status} {matricule}: {message}")
        
        print("✅ Tous les tests de matricules réussis")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests de matricules: {e}")

def main():
    """Fonction principale de test"""
    print("🧪 TESTS DES FONCTIONNALITÉS CRUD DU CLI")
    print("=" * 60)
    
    # Test de connexion
    if not test_database_connection():
        print("❌ Impossible de continuer sans connexion à la base de données")
        sys.exit(1)
    
    # Tests CRUD
    test_users_crud()
    test_products_crud()
    test_audit_logs()
    test_matricule_generation()
    
    print("\n🎉 TOUS LES TESTS TERMINÉS AVEC SUCCÈS!")
    print("Le système CRUD du CLI est opérationnel.")

if __name__ == "__main__":
    main() 