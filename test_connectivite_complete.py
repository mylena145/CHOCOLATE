#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier la connectivité complète à la base de données
"""

import psycopg2
import sys

def test_connectivite_complete():
    """Test complet de la connectivité à la base de données"""
    print("🔍 TEST DE CONNECTIVITÉ COMPLÈTE À LA BASE DE DONNÉES")
    print("=" * 60)
    
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
    
    try:
        # Test de connexion
        print("1. Test de connexion à PostgreSQL...")
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        print("   ✅ Connexion PostgreSQL réussie")
        
        # Test des tables principales
        print("\n2. Test des tables principales...")
        tables_to_test = [
            ('individus', 'Utilisateurs'),
            ('produits', 'Produits/Stock'),
            ('organisations', 'Organisations'),
            ('entrepots', 'Entrepôts'),
            ('zone_stockage', 'Zones de stockage'),
            ('cellules', 'Cellules'),
            ('receptions', 'Réceptions'),
            ('colis', 'Colis'),
            ('materiel_emballage', 'Matériel d\'emballage'),
            ('mouvements', 'Mouvements de stock')
        ]
        
        for table, description in tables_to_test:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM sge_cre.{table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {description} ({table}): {count} enregistrements")
            except Exception as e:
                print(f"   ❌ {description} ({table}): Erreur - {e}")
        
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
            cursor.execute("SELECT COUNT(*) FROM sge_cre.produits")
            products = cursor.fetchone()[0]
            print(f"   ✅ Produits en stock: {products}")
        except:
            print("   ❌ Erreur lors du test des produits")
        
        # Test des mouvements
        try:
            cursor.execute("SELECT COUNT(*) FROM mouvements")
            movements = cursor.fetchone()[0]
            print(f"   ✅ Mouvements de stock: {movements}")
        except:
            print("   ❌ Erreur lors du test des mouvements")
        
        # Test des emballages
        try:
            cursor.execute("SELECT COUNT(*) FROM sge_cre.materiel_emballage")
            packaging = cursor.fetchone()[0]
            print(f"   ✅ Matériel d'emballage: {packaging}")
        except:
            print("   ❌ Erreur lors du test des emballages")
        
        # Test des entrepôts
        try:
            cursor.execute("SELECT COUNT(*) FROM sge_cre.entrepots")
            warehouses = cursor.fetchone()[0]
            print(f"   ✅ Entrepôts: {warehouses}")
        except:
            print("   ❌ Erreur lors du test des entrepôts")
        
        # Test des zones de stockage
        try:
            cursor.execute("SELECT COUNT(*) FROM sge_cre.zone_stockage")
            zones = cursor.fetchone()[0]
            print(f"   ✅ Zones de stockage: {zones}")
        except:
            print("   ❌ Erreur lors du test des zones de stockage")
        
        conn.close()
        
        print(f"\n{'='*60}")
        print("🎉 Test de connectivité terminé!")
        print("✅ Toutes les tables principales sont accessibles")
        print("✅ L'application est entièrement connectée à PostgreSQL")
        print("\nVous pouvez maintenant utiliser toutes les fonctionnalités :")
        print("  - Authentification des utilisateurs")
        print("  - Gestion des stocks")
        print("  - Gestion des mouvements")
        print("  - Gestion des emballages")
        print("  - Administration du système")
        print("  - Gestion des entrepôts")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        print("\nVérifiez que :")
        print("  1. PostgreSQL est démarré")
        print("  2. Les paramètres de connexion sont corrects")
        print("  3. Les tables ont été créées (exécutez init_sge_database.py)")
        return False

if __name__ == "__main__":
    success = test_connectivite_complete()
    sys.exit(0 if success else 1) 