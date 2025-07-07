#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour insérer des entrepôts de test
"""

import psycopg2

def insert_entrepots():
    """Insère des entrepôts de test"""
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
        
        # Vérifier les entrepôts existants
        cursor.execute("SELECT COUNT(*) FROM sge_cre.entrepots")
        count_before = cursor.fetchone()[0]
        print(f"📊 {count_before} entrepôts existants")
        
        # Insérer les entrepôts
        entrepots = [
            ('Entrepôt LogiPlus', 5000, 'Informatique', 'Yaoundé'),
            ('Entrepôt TransAfrica', 3000, 'Transport', 'Douala'),
            ('Entrepôt DepotCentral', 2000, 'Stock général', 'Garoua'),
            ('Entrepôt Fournitech', 4000, 'Composants', 'Bafoussam'),
            ('Entrepôt DistribPlus', 2500, 'Divers', 'Maroua')
        ]
        
        for entrepot in entrepots:
            try:
                cursor.execute("""
                    INSERT INTO sge_cre.entrepots (nom_organisation, capacite, stockage, emplacement) 
                    VALUES (%s, %s, %s, %s)
                """, entrepot)
                print(f"✅ Ajouté: {entrepot[0]}")
            except psycopg2.IntegrityError:
                print(f"⚠️  Déjà existant: {entrepot[0]}")
        
        conn.commit()
        
        # Afficher tous les entrepôts
        cursor.execute("SELECT nom_organisation, capacite, stockage, emplacement FROM sge_cre.entrepots ORDER BY nom_organisation")
        entrepots_list = cursor.fetchall()
        print(f"\n📋 Total: {len(entrepots_list)} entrepôts dans la base:")
        for entrepot in entrepots_list:
            print(f"   - {entrepot[0]} ({entrepot[2]}) - {entrepot[1]} unités - {entrepot[3]}")
        
        conn.close()
        print("\n✅ Insertion terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔧 Insertion des entrepôts...")
    insert_entrepots() 