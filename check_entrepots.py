#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier les entrepôts existants
"""

import psycopg2

def check_entrepots():
    """Vérifie les entrepôts existants"""
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
        
        # Vérifier les entrepôts
        print("\n🏢 ENTREPÔTS DISPONIBLES:")
        cursor.execute("SELECT id_entrepot, nom_organisation, emplacement FROM sge_cre.entrepots ORDER BY id_entrepot")
        entrepots = cursor.fetchall()
        if entrepots:
            for ent in entrepots:
                print(f"   ID: {ent[0]} - {ent[1]} ({ent[2]})")
        else:
            print("   ❌ Aucun entrepôt trouvé")
        
        # Vérifier la structure de zone_stockage
        print("\n📋 STRUCTURE DE ZONE_STOCKAGE:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_schema = 'sge_cre' AND table_name = 'zone_stockage'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        if columns:
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                print(f"   - {col[0]} ({col[1]}) {nullable}")
        else:
            print("   ❌ Table zone_stockage non trouvée")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔍 Vérification des entrepôts...")
    check_entrepots() 