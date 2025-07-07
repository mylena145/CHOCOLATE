#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour insérer des données d'emballage de test dans la base de données PostgreSQL
"""

import psycopg2
from database import PG_CONN

def insert_test_emballages():
    """Insère des données d'emballage de test"""
    
    # Données de test
    emballages_test = [
        ("Boite", "Neuf"),
        ("Adhesive", "Neuf"),
        ("Bourrage", "Neuf"),
        ("Boite", "Recupere"),
        ("Adhesive", "Recupere"),
        ("Bourrage", "Recupere"),
        ("Autre", "Neuf"),
        ("Boite", "Neuf"),
        ("Adhesive", "Recupere"),
        ("Bourrage", "Neuf")
    ]
    
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        print("🔗 Connexion à la base de données établie")
        
        # Vérifier si la table existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'sge_cre' 
                AND table_name = 'materiel_emballage'
            );
        """)
        
        if not cursor.fetchone()[0]:
            print("❌ La table sge_cre.materiel_emballage n'existe pas!")
            print("Veuillez d'abord créer la table avec le script SQL approprié.")
            return False
        
        # Vérifier les données existantes
        cursor.execute("SELECT COUNT(*) FROM sge_cre.materiel_emballage")
        count_before = cursor.fetchone()[0]
        print(f"📊 Nombre d'emballages existants : {count_before}")
        
        # Insérer les données de test
        for type_emballage, etat_emballage in emballages_test:
            cursor.execute("""
                INSERT INTO sge_cre.materiel_emballage (type_emballage, etat_emballage)
                VALUES (%s, %s)
            """, (type_emballage, etat_emballage))
            print(f"✅ Ajouté : {type_emballage} - {etat_emballage}")
        
        # Valider les changements
        conn.commit()
        
        # Vérifier le nombre final
        cursor.execute("SELECT COUNT(*) FROM sge_cre.materiel_emballage")
        count_after = cursor.fetchone()[0]
        
        print(f"\n🎉 Insertion terminée avec succès!")
        print(f"📈 Nombre d'emballages ajoutés : {count_after - count_before}")
        print(f"📊 Total d'emballages : {count_after}")
        
        # Afficher un résumé
        cursor.execute("""
            SELECT type_emballage, etat_emballage, COUNT(*)
            FROM sge_cre.materiel_emballage
            GROUP BY type_emballage, etat_emballage
            ORDER BY type_emballage, etat_emballage
        """)
        
        print("\n📋 Résumé des emballages :")
        print("-" * 40)
        for type_emb, etat, count in cursor.fetchall():
            print(f"  {type_emb} - {etat} : {count}")
        
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Erreur PostgreSQL : {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def show_emballages():
    """Affiche tous les emballages existants"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_emballeur, type_emballage, etat_emballage
            FROM sge_cre.materiel_emballage
            ORDER BY id_emballeur
        """)
        
        emballages = cursor.fetchall()
        
        print("\n📦 Liste des emballages existants :")
        print("-" * 50)
        print(f"{'ID':<5} {'Type':<15} {'État':<15}")
        print("-" * 50)
        
        for id_emb, type_emb, etat in emballages:
            print(f"{id_emb:<5} {type_emb:<15} {etat:<15}")
        
        print(f"\nTotal : {len(emballages)} emballages")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'affichage : {e}")

if __name__ == "__main__":
    print("🚀 Script d'insertion des données d'emballage de test")
    print("=" * 60)
    
    # Afficher les emballages existants
    show_emballages()
    
    # Demander confirmation
    print("\n❓ Voulez-vous ajouter des données de test ? (o/n) : ", end="")
    try:
        response = input().lower().strip()
        if response in ['o', 'oui', 'y', 'yes']:
            print("\n🔄 Insertion des données de test...")
            if insert_test_emballages():
                print("\n✅ Données de test insérées avec succès!")
                print("\n📦 Nouvelle liste des emballages :")
                show_emballages()
            else:
                print("\n❌ Échec de l'insertion des données de test")
        else:
            print("❌ Insertion annulée")
    except KeyboardInterrupt:
        print("\n❌ Opération annulée par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur : {e}") 