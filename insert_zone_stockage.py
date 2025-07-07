#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour insérer des zones de stockage de test
"""

import psycopg2

def insert_zone_stockage():
    """Insère des zones de stockage de test"""
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
        
        # Vérifier les zones existantes
        cursor.execute("SELECT COUNT(*) FROM sge_cre.zone_stockage")
        count_before = cursor.fetchone()[0]
        print(f"📊 {count_before} zones de stockage existantes")
        
        # Insérer les zones de stockage
        zones = [
            ('C001', 'Zone A', 'Rayon 1'),
            ('C002', 'Zone A', 'Rayon 2'),
            ('C003', 'Zone B', 'Rayon 1'),
            ('C004', 'Zone B', 'Rayon 3'),
            ('C005', 'Zone C', 'Réserve')
        ]
        
        for zone in zones:
            try:
                cursor.execute("""
                    INSERT INTO sge_cre.zone_stockage (id_cellule, e1, e2) 
                    VALUES (%s, %s, %s)
                """, zone)
                print(f"✅ Ajouté: {zone[0]} - {zone[1]} - {zone[2]}")
            except psycopg2.IntegrityError:
                print(f"⚠️  Déjà existant: {zone[0]}")
        
        conn.commit()
        
        # Afficher toutes les zones
        cursor.execute("SELECT id_zo_stock, id_cellule, e1, e2 FROM sge_cre.zone_stockage ORDER BY id_cellule")
        zones_list = cursor.fetchall()
        print(f"\n📋 Total: {len(zones_list)} zones de stockage dans la base:")
        for zone in zones_list:
            print(f"   - ID: {zone[0]}, Cellule: {zone[1]}, Zone: {zone[2]}, Rayon: {zone[3]}")
        
        conn.close()
        print("\n✅ Insertion terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔧 Insertion des zones de stockage...")
    insert_zone_stockage() 