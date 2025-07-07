#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier les IDs existants dans les tables
"""

import psycopg2

def check_existing_ids():
    """Vérifie les IDs existants dans les tables"""
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
        
        # Vérifier les individus
        print("\n👥 INDIVIDUS DISPONIBLES:")
        cursor.execute("SELECT id_individu, nom, prenom, email FROM sge_cre.individus ORDER BY id_individu")
        individus = cursor.fetchall()
        if individus:
            for ind in individus:
                print(f"   ID: {ind[0]} - {ind[1]} {ind[2]} ({ind[3]})")
        else:
            print("   ❌ Aucun individu trouvé")
        
        # Vérifier les organisations
        print("\n🏢 ORGANISATIONS DISPONIBLES:")
        cursor.execute("SELECT id_organisation, nom, statut FROM sge_cre.organisations ORDER BY id_organisation")
        organisations = cursor.fetchall()
        if organisations:
            for org in organisations:
                print(f"   ID: {org[0]} - {org[1]} ({org[2]})")
        else:
            print("   ❌ Aucune organisation trouvée")
        
        # Vérifier le répertoire existant
        print("\n📋 RÉPERTOIRE EXISTANT:")
        cursor.execute("SELECT id_organisation, id_individu FROM sge_cre.repertoire ORDER BY id_organisation")
        repertoire = cursor.fetchall()
        if repertoire:
            for rep in repertoire:
                print(f"   {rep[0]} -> {rep[1]}")
        else:
            print("   ❌ Aucune liaison trouvée")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔍 Vérification des IDs existants...")
    check_existing_ids() 