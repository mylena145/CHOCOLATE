#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier l'état de la base de données
"""

import psycopg2

def check_database():
    """Vérifie l'état de la base de données"""
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
        
        # Vérifier si le schéma existe
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'sge_cre'")
        if cursor.fetchone():
            print("✅ Schéma sge_cre existe")
        else:
            print("❌ Schéma sge_cre n'existe pas")
            conn.close()
            return
        
        # Vérifier les tables
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
                print(f"   - {table[0]}")
        else:
            print("❌ Aucune table trouvée dans sge_cre")
        
        # Vérifier spécifiquement la table organisations
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'sge_cre' AND table_name = 'organisations'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        if columns:
            print(f"✅ Table organisations existe avec {len(columns)} colonnes:")
            for col in columns:
                print(f"   - {col[0]} ({col[1]})")
        else:
            print("❌ Table organisations n'existe pas")
        
        # Vérifier les données
        cursor.execute("SELECT COUNT(*) FROM sge_cre.organisations")
        count = cursor.fetchone()[0]
        print(f"📊 {count} organisations dans la table")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔍 Vérification de la base de données...")
    check_database() 