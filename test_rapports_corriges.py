#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test pour vérifier que tous les rapports fonctionnent avec les bonnes tables
"""

import psycopg2
import datetime
import os

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

def test_table_exists(table_name):
    """Teste si une table existe"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'sge_cre' 
                AND table_name = %s
            );
        """, (table_name,))
        exists = cursor.fetchone()[0]
        conn.close()
        return exists
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de {table_name}: {e}")
        return False

def test_export_users():
    """Teste l'export des utilisateurs"""
    print("🔍 Test export utilisateurs...")
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        cursor.execute("SELECT nom, prenom, email, role, matricule, adresse, telephone FROM sge_cre.individus ORDER BY nom")
        users = cursor.fetchall()
        conn.close()
        print(f"✅ {len(users)} utilisateurs trouvés")
        return True
    except Exception as e:
        print(f"❌ Erreur export utilisateurs: {e}")
        return False

def test_export_products():
    """Teste l'export des produits"""
    print("🔍 Test export produits...")
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        cursor.execute("SELECT nom, description, marque, modele, fournisseur, stock FROM sge_cre.produits ORDER BY nom")
        products = cursor.fetchall()
        conn.close()
        print(f"✅ {len(products)} produits trouvés")
        return True
    except Exception as e:
        print(f"❌ Erreur export produits: {e}")
        return False

def test_export_movements():
    """Teste l'export des mouvements"""
    print("🔍 Test export mouvements...")
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        cursor.execute("SELECT type, quantite, date_mouvement, produit_nom, reference FROM sge_cre.mouvements ORDER BY date_mouvement DESC")
        movements = cursor.fetchall()
        conn.close()
        print(f"✅ {len(movements)} mouvements trouvés")
        return True
    except Exception as e:
        print(f"❌ Erreur export mouvements: {e}")
        return False

def test_export_packaging():
    """Teste l'export des emballages"""
    print("🔍 Test export emballages...")
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        cursor.execute("SELECT type_emballage, etat_emballage FROM sge_cre.materiel_emballage ORDER BY type_emballage")
        packaging = cursor.fetchall()
        conn.close()
        print(f"✅ {len(packaging)} emballages trouvés")
        return True
    except Exception as e:
        print(f"❌ Erreur export emballages: {e}")
        return False

def create_test_export_files():
    """Crée des fichiers d'export de test"""
    print("\n📁 Création des fichiers d'export de test...")
    
    # Créer le dossier exports s'il n'existe pas
    if not os.path.exists("exports"):
        os.makedirs("exports")
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Test CSV
    try:
        import csv
        
        # Export utilisateurs CSV
        filename = f"exports/test_users_{timestamp}.csv"
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
        
        print(f"✅ Fichier CSV créé: {filename}")
        
        # Export produits CSV
        filename = f"exports/test_products_{timestamp}.csv"
        cursor.execute("SELECT nom, description, marque, modele, fournisseur, stock FROM sge_cre.produits ORDER BY nom")
        products = cursor.fetchall()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['NOM', 'DESCRIPTION', 'MARQUE', 'MODÈLE', 'FOURNISSEUR', 'STOCK'])
            writer.writerow(['---', '---', '---', '---', '---', '---'])
            for product in products:
                writer.writerow(product)
        
        print(f"✅ Fichier CSV créé: {filename}")
        
        # Export emballages CSV
        filename = f"exports/test_packaging_{timestamp}.csv"
        cursor.execute("SELECT type_emballage, etat_emballage FROM sge_cre.materiel_emballage ORDER BY type_emballage")
        packaging = cursor.fetchall()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['TYPE', 'ÉTAT'])
            writer.writerow(['---', '---'])
            for pack in packaging:
                writer.writerow(pack)
        
        print(f"✅ Fichier CSV créé: {filename}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur création fichiers CSV: {e}")

def main():
    print("🚀 Test des rapports corrigés")
    print("=" * 50)
    
    # Vérifier l'existence des tables
    print("\n📋 Vérification des tables...")
    tables = ['individus', 'produits', 'mouvements', 'materiel_emballage']
    
    for table in tables:
        if test_table_exists(table):
            print(f"✅ Table sge_cre.{table} existe")
        else:
            print(f"❌ Table sge_cre.{table} n'existe pas")
    
    # Tester les exports
    print("\n📊 Test des exports...")
    test_export_users()
    test_export_products()
    test_export_movements()
    test_export_packaging()
    
    # Créer des fichiers de test
    create_test_export_files()
    
    print("\n🎉 Tests terminés!")
    print("\n📝 Commandes CLI disponibles:")
    print("  export users csv      # Export CSV des utilisateurs")
    print("  export users xlsx     # Export Excel des utilisateurs")
    print("  export products csv   # Export CSV des produits")
    print("  export products xlsx  # Export Excel des produits")
    print("  export movements csv  # Export CSV des mouvements")
    print("  export movements xlsx # Export Excel des mouvements")
    print("  export packaging csv  # Export CSV des emballages")
    print("  export packaging xlsx # Export Excel des emballages")

if __name__ == "__main__":
    main() 