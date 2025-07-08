#!/usr/bin/env python3
"""
Script pour ajouter le champ priorite à la table bon_expeditions
"""

import psycopg2
from psycopg2 import sql

# Configuration de la base de données
PG_CONN = {
    'host': 'localhost',
    'database': 'sge_cre',
    'user': 'postgres',
    'password': 'postgres'
}

def add_priority_column():
    """Ajoute le champ priorite à la table bon_expeditions"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        print("🔄 Ajout du champ priorite à la table bon_expeditions...")
        
        # Vérifier si le champ existe déjà
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'sge_cre' 
            AND table_name = 'bon_expeditions' 
            AND column_name = 'priorite'
        """)
        
        if cursor.fetchone():
            print("✅ Le champ priorite existe déjà")
            return True
        
        # Ajouter le champ priorite
        cursor.execute("""
            ALTER TABLE sge_cre.bon_expeditions 
            ADD COLUMN priorite VARCHAR(20) DEFAULT 'moyenne'
        """)
        
        # Mettre à jour les enregistrements existants
        cursor.execute("""
            UPDATE sge_cre.bon_expeditions 
            SET priorite = 'moyenne' 
            WHERE priorite IS NULL
        """)
        
        # Ajouter une contrainte pour limiter les valeurs possibles
        cursor.execute("""
            ALTER TABLE sge_cre.bon_expeditions 
            ADD CONSTRAINT check_priorite 
            CHECK (priorite IN ('haute', 'moyenne', 'basse'))
        """)
        
        conn.commit()
        print("✅ Champ priorite ajouté avec succès")
        
        # Vérifier que la modification a été appliquée
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_schema = 'sge_cre' 
            AND table_name = 'bon_expeditions' 
            AND column_name = 'priorite'
        """)
        
        result = cursor.fetchone()
        if result:
            print(f"✅ Vérification: {result}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout du champ priorite: {e}")
        return False

if __name__ == "__main__":
    add_priority_column() 