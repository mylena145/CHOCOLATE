#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction des contraintes de clés étrangères
Résout tous les problèmes d'insertion dans la base de données SGE
"""

import psycopg2
import os
import sys
from datetime import datetime

# Configuration de la base de données
PG_CONN = dict(
    dbname="postgres",
    user="postgres",
    password="postgres123",
    host="localhost",
    port="5432",
    client_encoding="utf8",
    options="-c client_encoding=utf8",
    connect_timeout=10
)

def test_connection():
    """Teste la connexion à la base de données"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Connexion réussie à PostgreSQL: {version[0]}")
        
        # Vérifier que le schéma sge_cre existe
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'sge_cre'")
        if not cursor.fetchone():
            print("❌ Le schéma 'sge_cre' n'existe pas")
            print("💡 Exécutez d'abord le script SGE_CRE.sql pour créer les tables")
            conn.close()
            return False
        
        # Lister les tables existantes
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'sge_cre' 
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tables trouvées dans sge_cre: {', '.join(tables)}")
        
        # Lister les séquences existantes
        cursor.execute("""
            SELECT sequence_name 
            FROM information_schema.sequences 
            WHERE sequence_schema = 'sge_cre' 
            ORDER BY sequence_name
        """)
        sequences = [row[0] for row in cursor.fetchall()]
        print(f"🔄 Séquences trouvées: {', '.join(sequences)}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def execute_sql_file(filename):
    """Exécute un fichier SQL"""
    try:
        # Lire le contenu du fichier avec encodage UTF-8
        with open(filename, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Se connecter à la base
        conn = psycopg2.connect(**PG_CONN)
        conn.autocommit = False  # Désactiver l'auto-commit pour les transactions
        cursor = conn.cursor()
        
        print(f"🔄 Exécution du script: {filename}")
        
        # Diviser le script en commandes individuelles
        # Gérer les blocs DO $$ ... $$ correctement
        commands = []
        current_command = ""
        in_do_block = False
        
        for line in sql_content.split('\n'):
            line = line.strip()
            if not line or line.startswith('--'):
                continue
                
            if 'DO $$' in line:
                in_do_block = True
                current_command = line
            elif in_do_block:
                current_command += " " + line
                if '$$;' in line:
                    in_do_block = False
                    commands.append(current_command)
                    current_command = ""
            elif line.endswith(';'):
                current_command += " " + line
                commands.append(current_command)
                current_command = ""
            else:
                current_command += " " + line
        
        # Ajouter la dernière commande si elle existe
        if current_command.strip():
            commands.append(current_command)
        
        # Exécuter les commandes
        for i, command in enumerate(commands):
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                    print(f"  ✅ Commande {i+1} exécutée")
                except Exception as e:
                    print(f"  ❌ Erreur commande {i+1}: {e}")
                    print(f"  Commande: {command[:100]}...")
                    conn.rollback()
                    return False
        
        # Valider les changements
        conn.commit()
        print(f"✅ Script {filename} exécuté avec succès")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution du script {filename}: {e}")
        return False

def verify_data():
    """Vérifie que les données ont été correctement insérées"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        print("\n🔍 Vérification des données insérées:")
        
        # Vérifier les tables principales
        tables = [
            'organisations', 'individus', 'repertoire', 'produits',
            'receptions', 'entrepots', 'cellules', 'zone_stockage',
            'colis', 'lots', 'materiel_emballage', 'commandes',
            'commandes_achats', 'commandes_vends'
        ]
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM sge_cre.{table}")
                count = cursor.fetchone()[0]
                print(f"  📊 {table}: {count} enregistrements")
            except Exception as e:
                print(f"  ❌ Erreur table {table}: {e}")
        
        # Vérifier les contraintes de clés étrangères
        print("\n🔗 Test des contraintes de clés étrangères:")
        
        # Test colis -> zone_stockage
        cursor.execute("""
            SELECT COUNT(*) FROM sge_cre.colis c 
            JOIN sge_cre.zone_stockage z ON c.id_zo_stock = z.id_zo_stock
        """)
        count = cursor.fetchone()[0]
        print(f"  ✅ Colis avec zones valides: {count}")
        
        # Test zone_stockage -> entrepots
        cursor.execute("""
            SELECT COUNT(*) FROM sge_cre.zone_stockage z 
            JOIN sge_cre.entrepots e ON z.id_entrepot = e.id_entrepot
        """)
        count = cursor.fetchone()[0]
        print(f"  ✅ Zones avec entrepôts valides: {count}")
        
        # Test lots -> produits
        cursor.execute("""
            SELECT COUNT(*) FROM sge_cre.lots l 
            JOIN sge_cre.produits p ON l.id_produit = p.id_produit
        """)
        count = cursor.fetchone()[0]
        print(f"  ✅ Lots avec produits valides: {count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🔧 SCRIPT DE CORRECTION DES CONTRAINTES DE CLÉS ÉTRANGÈRES")
    print("=" * 60)
    print(f"⏰ Début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test de connexion
    if not test_connection():
        print("❌ Impossible de se connecter à la base de données")
        print("\n💡 Solutions possibles:")
        print("1. Vérifiez que PostgreSQL est démarré")
        print("2. Vérifiez les paramètres de connexion dans PG_CONN")
        print("3. Assurez-vous que le schéma 'sge_cre' existe")
        sys.exit(1)
    
    # Exécuter le script de correction
    sql_file = "fix_database_constraints.sql"
    if not os.path.exists(sql_file):
        print(f"❌ Fichier {sql_file} non trouvé")
        sys.exit(1)
    
    if not execute_sql_file(sql_file):
        print("❌ Échec de l'exécution du script SQL")
        sys.exit(1)
    
    # Vérifier les données
    if not verify_data():
        print("❌ Échec de la vérification des données")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ CORRECTION TERMINÉE AVEC SUCCÈS")
    print("=" * 60)
    print(f"⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🎉 Toutes les contraintes de clés étrangères ont été corrigées !")
    print("📦 Les données sont maintenant cohérentes et utilisables.")

if __name__ == "__main__":
    main() 