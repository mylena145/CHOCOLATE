#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajouter la colonne priorite à la table bon_expeditions
"""

import psycopg2
from database import PG_CONN

def add_priority_column():
    """Ajoute la colonne priorite à la table bon_expeditions"""
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        print("🔧 Ajout de la colonne priorite à la table bon_expeditions...")
        
        # Ajouter la colonne priorite
        cursor.execute("""
            ALTER TABLE sge_cre.bon_expeditions 
            ADD COLUMN IF NOT EXISTS priorite VARCHAR(20) DEFAULT 'moyenne'
        """)
        
        # Mettre à jour les enregistrements existants
        cursor.execute("""
            UPDATE sge_cre.bon_expeditions 
            SET priorite = 'moyenne' 
            WHERE priorite IS NULL
        """)
        
        # Valider les changements
        conn.commit()
        
        print("✅ Colonne priorite ajoutée avec succès !")
        
        # Vérifier que la colonne existe
        cursor.execute("""
            SELECT column_name, data_type, column_default, is_nullable
            FROM information_schema.columns 
            WHERE table_schema = 'sge_cre' 
            AND table_name = 'bon_expeditions' 
            AND column_name = 'priorite'
        """)
        
        result = cursor.fetchone()
        if result:
            print(f"✅ Vérification : colonne {result[0]} de type {result[1]} avec valeur par défaut '{result[2]}'")
        else:
            print("❌ La colonne priorite n'a pas été trouvée")
        
        # Compter les enregistrements mis à jour
        cursor.execute("SELECT COUNT(*) FROM sge_cre.bon_expeditions")
        count = cursor.fetchone()[0]
        print(f"📊 Nombre total d'expéditions dans la table : {count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout de la colonne priorite : {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("🚀 Démarrage de la correction de la colonne priorite...")
    success = add_priority_column()
    
    if success:
        print("🎉 Correction terminée avec succès !")
        print("💡 Vous pouvez maintenant relancer l'application.")
    else:
        print("💥 Échec de la correction. Vérifiez les erreurs ci-dessus.") 