#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier la structure de la table zone_stockage
"""

import psycopg2

def check_zone_stockage():
    """Vérifie la structure de la table zone_stockage"""
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
        
        # Vérifier la structure de la table zone_stockage
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_schema = 'sge_cre' AND table_name = 'zone_stockage'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        if columns:
            print(f"✅ Table zone_stockage existe avec {len(columns)} colonnes:")
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                print(f"   - {col[0]} ({col[1]}) {nullable}")
        else:
            print("❌ Table zone_stockage n'existe pas")
            return
        
        # Vérifier les données existantes
        cursor.execute("SELECT COUNT(*) FROM sge_cre.zone_stockage")
        count = cursor.fetchone()[0]
        print(f"\n📊 {count} zones de stockage dans la table")
        
        if count > 0:
            cursor.execute("SELECT * FROM sge_cre.zone_stockage LIMIT 3")
            sample = cursor.fetchall()
            print("📋 Exemples de zones:")
            for row in sample:
                print(f"   - {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔍 Vérification de la table zone_stockage...")
    check_zone_stockage() 