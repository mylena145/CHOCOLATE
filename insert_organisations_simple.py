#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplifié pour insérer des organisations
"""

import psycopg2

def insert_organisations_simple():
    """Insère des organisations de test (version simplifiée)"""
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
        
        # Insérer les organisations (sans vérification de doublons)
        organisations = [
            ('LogiPlus', 'Zone Industrielle, Yaoundé', '699001122', 'Fournisseur', 3),
            ('TransAfrica', 'Rue de l''Avenir, Douala', '676543210', 'Transporteur', 5),
            ('DepotCentral', 'Quartier Mvan, Yaoundé', '690112233', 'Destinataire', 1),
            ('Fournitech', 'Avenue Kennedy, Douala', '655009988', 'Fournisseur', 2),
            ('DistribPlus', 'Rue 12, Garoua', '688776655', 'Fournisseur', 4)
        ]
        
        for org in organisations:
            try:
                cursor.execute("""
                    INSERT INTO sge_cre.organisations (nom, adresse, telephone, statut, nbr_entrepot) 
                    VALUES (%s, %s, %s, %s, %s)
                """, org)
                print(f"✅ Ajouté: {org[0]}")
            except psycopg2.IntegrityError:
                print(f"⚠️  Déjà existant: {org[0]}")
        
        conn.commit()
        
        # Afficher toutes les organisations
        cursor.execute("SELECT nom, statut, nbr_entrepot FROM sge_cre.organisations ORDER BY nom")
        orgs = cursor.fetchall()
        print(f"\n📋 Total: {len(orgs)} organisations dans la base:")
        for org in orgs:
            print(f"   - {org[0]} ({org[1]}) - {org[2]} entrepôts")
        
        conn.close()
        print("\n✅ Opération terminée!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔧 Insertion simple des organisations...")
    insert_organisations_simple() 