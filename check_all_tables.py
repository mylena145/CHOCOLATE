#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier toutes les tables existantes
"""

import psycopg2

def check_all_tables():
    """Vérifie toutes les tables existantes"""
    try:
        # Connexion
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
        
        print("✅ Connexion à PostgreSQL réussie")
        
        # Vérifier toutes les tables du schéma sge_cre
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'sge_cre'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"✅ {len(tables)} tables trouvées dans sge_cre:")
            for table in tables:
                # Compter les lignes dans chaque table
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM sge_cre.{table[0]}")
                    count = cursor.fetchone()[0]
                    print(f"   - {table[0]} ({count} lignes)")
                except:
                    print(f"   - {table[0]} (erreur de lecture)")
        else:
            print("❌ Aucune table trouvée dans sge_cre")
        
        # Vérifier spécifiquement les tables importantes
        important_tables = ['individus', 'organisations', 'produits', 'entrepots', 'zone_stockage']
        print(f"\n🔍 Vérification des tables importantes:")
        for table in important_tables:
            cursor.execute(f"SELECT to_regclass('sge_cre.{table}')")
            result = cursor.fetchone()
            if result and result[0]:
                cursor.execute(f"SELECT COUNT(*) FROM sge_cre.{table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table}: {count} lignes")
            else:
                print(f"   ❌ {table}: N'existe pas")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔍 Vérification de toutes les tables...")
    check_all_tables() 