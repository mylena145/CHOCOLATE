#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour insérer le répertoire avec les bons IDs
"""

import psycopg2

def insert_repertoire():
    """Insère le répertoire avec les bons IDs"""
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
        
        # Insérer le répertoire avec les vrais IDs
        repertoire_data = [
            ('ORG001', 45),  # Noelle (Administrateur)
            ('ORG002', 46),  # Brice (Responsable_stocks)
            ('ORG003', 47),  # Orlane (Agent_logistique)
            ('ORG004', 48),  # Pharel (Emballeur)
            ('ORG005', 49)   # Abigael (Magasinier)
        ]
        
        for org_id, ind_id in repertoire_data:
            try:
                cursor.execute("""
                    INSERT INTO sge_cre.repertoire (id_organisation, id_individu) 
                    VALUES (%s, %s)
                """, (org_id, ind_id))
                print(f"✅ Ajouté: {org_id} -> {ind_id}")
            except psycopg2.IntegrityError:
                print(f"⚠️  Déjà existant: {org_id} -> {ind_id}")
        
        conn.commit()
        
        # Afficher le résultat
        cursor.execute("""
            SELECT r.id_organisation, r.id_individu, o.nom as org_nom, i.nom as ind_nom, i.role
            FROM sge_cre.repertoire r
            JOIN sge_cre.organisations o ON r.id_organisation = o.id_organisation
            JOIN sge_cre.individus i ON r.id_individu = i.id_individu
            ORDER BY r.id_organisation
        """)
        result = cursor.fetchall()
        
        print(f"\n📋 Répertoire créé ({len(result)} liaisons):")
        for row in result:
            print(f"   {row[0]} ({row[2]}) -> {row[1]} ({row[3]} - {row[4]})")
        
        conn.close()
        print("\n✅ Insertion terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔧 Insertion du répertoire...")
    insert_repertoire() 