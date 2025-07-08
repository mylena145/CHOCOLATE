#!/usr/bin/env python3
"""
Script pour verifier la structure de la table individus
"""

import psycopg2

# Configuration de la base de donnees
PG_CONN = {
    'host': 'localhost',
    'database': 'sac',
    'user': 'postgres',
    'password': 'postgres'
}

def check_table_structure():
    """Verifie la structure de la table individus"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        # Verifier les colonnes de la table individus
        cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns 
            WHERE table_name = 'individus' 
            AND table_schema = 'sge_cre' 
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        
        print("Structure de la table sge_cre.individus:")
        print("=" * 50)
        
        for col in columns:
            column_name, data_type = col
            print(f"  {column_name}: {data_type}")
        
        print(f"\nTotal: {len(columns)} colonnes")
        
        # Verifier si la colonne actif existe
        column_names = [col[0] for col in columns]
        if 'actif' in column_names:
            print("La colonne 'actif' existe")
        else:
            print("La colonne 'actif' n'existe pas")
            print("Il faut l'ajouter ou utiliser une autre colonne")
        
        conn.close()
        
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    check_table_structure() 