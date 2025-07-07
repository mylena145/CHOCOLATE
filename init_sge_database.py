#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'initialisation de la base de données SGE
Exécute les fichiers SGE_*.sql dans l'ordre correct
"""

import psycopg2
import os
import sys

# Paramètres de connexion PostgreSQL
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

def execute_sql_file(file_path, description):
    """Exécute un fichier SQL et affiche le résultat"""
    try:
        print(f"\n{'='*60}")
        print(f"Exécution de {description}")
        print(f"Fichier: {file_path}")
        print(f"{'='*60}")
        
        # Lire le contenu du fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Se connecter à la base de données
        conn = psycopg2.connect(**PG_CONN)
        conn.autocommit = True  # Important pour les commandes DDL
        cursor = conn.cursor()
        
        # Exécuter le script SQL
        cursor.execute(sql_content)
        
        print(f"✅ {description} exécuté avec succès")
        
        cursor.close()
        conn.close()
        
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {file_path}")
        return False
    except psycopg2.Error as e:
        print(f"❌ Erreur PostgreSQL lors de l'exécution de {file_path}:")
        print(f"   {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue lors de l'exécution de {file_path}:")
        print(f"   {e}")
        return False
    
    return True

def main():
    """Fonction principale d'initialisation"""
    print("🚀 Initialisation de la base de données SGE")
    print("=" * 60)
    
    # Vérifier la connexion
    try:
        conn = psycopg2.connect(**PG_CONN)
        conn.close()
        print("✅ Connexion à PostgreSQL réussie")
    except Exception as e:
        print(f"❌ Impossible de se connecter à PostgreSQL: {e}")
        print("Vérifiez que PostgreSQL est démarré et que les paramètres de connexion sont corrects")
        return False
    
    # Ordre d'exécution des scripts
    scripts = [
        ("SGE_DROP.sql", "Suppression des anciennes tables (si elles existent)"),
        ("SGE_CRE.sql", "Création du schéma et des tables"),
        ("SGE_JEU.sql", "Insertion des données de test"),
    ]
    
    success_count = 0
    
    for file_name, description in scripts:
        if os.path.exists(file_name):
            if execute_sql_file(file_name, description):
                success_count += 1
        else:
            print(f"⚠️  Fichier {file_name} non trouvé, ignoré")
    
    print(f"\n{'='*60}")
    print(f"Résumé: {success_count}/{len(scripts)} scripts exécutés avec succès")
    
    if success_count == len(scripts):
        print("🎉 Initialisation complète réussie!")
        print("\nVous pouvez maintenant lancer l'application avec: python app.py")
    else:
        print("⚠️  Certains scripts n'ont pas pu être exécutés")
        print("Vérifiez les erreurs ci-dessus")
    
    return success_count == len(scripts)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 