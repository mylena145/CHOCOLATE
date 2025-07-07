#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour insérer des organisations de test
"""

import psycopg2

def insert_organisations():
    """Insère des organisations de test"""
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
        
        # Vérifier si les organisations existent déjà
        cursor.execute("SELECT COUNT(*) FROM sge_cre.organisations")
        count_before = cursor.fetchone()[0]
        print(f"📊 {count_before} organisations existantes")
        
        # Insérer les organisations
        organisations = [
            ('LogiPlus', 'Zone Industrielle, Yaoundé', '699001122', 'Fournisseur', 3),
            ('TransAfrica', 'Rue de l''Avenir, Douala', '676543210', 'Transporteur', 5),
            ('DepotCentral', 'Quartier Mvan, Yaoundé', '690112233', 'Destinataire', 1),
            ('Fournitech', 'Avenue Kennedy, Douala', '655009988', 'Fournisseur', 2),
            ('DistribPlus', 'Rue 12, Garoua', '688776655', 'Fournisseur', 4)
        ]
        
        for org in organisations:
            cursor.execute("""
                INSERT INTO sge_cre.organisations (nom, adresse, telephone, statut, nbr_entrepot) 
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (nom) DO NOTHING
            """, org)
        
        conn.commit()
        
        # Vérifier l'insertion
        cursor.execute("SELECT COUNT(*) FROM sge_cre.organisations")
        count_after = cursor.fetchone()[0]
        print(f"📊 {count_after} organisations après insertion")
        
        # Afficher les organisations
        cursor.execute("SELECT nom, statut, nbr_entrepot FROM sge_cre.organisations ORDER BY nom")
        orgs = cursor.fetchall()
        print("\n📋 Organisations dans la base:")
        for org in orgs:
            print(f"   - {org[0]} ({org[1]}) - {org[2]} entrepôts")
        
        conn.close()
        print("\n✅ Insertion terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔧 Insertion des organisations...")
    insert_organisations() 