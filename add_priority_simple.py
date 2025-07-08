#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple pour ajouter le champ priorite
"""

import psycopg2

# Configuration de la base de données
PG_CONN = {
    'host': 'localhost',
    'database': 'sge_cre',
    'user': 'postgres',
    'password': 'postgres'
}

def add_priority_column():
    """Ajoute le champ priorite a la table bon_expeditions"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        print("Ajout du champ priorite...")
        
        # Ajouter le champ priorite
        cursor.execute("ALTER TABLE sge_cre.bon_expeditions ADD COLUMN IF NOT EXISTS priorite VARCHAR(20) DEFAULT 'moyenne'")
        
        # Mettre a jour les enregistrements existants
        cursor.execute("UPDATE sge_cre.bon_expeditions SET priorite = 'moyenne' WHERE priorite IS NULL")
        
        conn.commit()
        print("Champ priorite ajoute avec succes")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Erreur: {e}")
        return False

if __name__ == "__main__":
    add_priority_column() 