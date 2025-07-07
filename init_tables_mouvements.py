#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour initialiser les tables de mouvements dans PostgreSQL
"""

import psycopg2

def init_mouvements_tables():
    """Initialise les tables de mouvements dans PostgreSQL"""
    print("🚀 Initialisation des tables de mouvements...")
    
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
    
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        # Table des mouvements
        print("1. Création de la table mouvements...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sge_cre.mouvements (
                id SERIAL PRIMARY KEY,
                type TEXT NOT NULL,
                produit_id INTEGER,
                produit_nom TEXT NOT NULL,
                quantite INTEGER NOT NULL,
                reference TEXT,
                origine TEXT,
                destination TEXT,
                responsable TEXT NOT NULL,
                date_mouvement TIMESTAMP NOT NULL,
                commentaire TEXT,
                statut TEXT DEFAULT 'Complété'
            )
        ''')
        print("   ✅ Table mouvements créée")
        
        # Table des produits temporaire
        print("2. Création de la table products...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sge_cre.products (
                id SERIAL PRIMARY KEY,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                stock INTEGER DEFAULT 0,
                min_stock INTEGER DEFAULT 10,
                location TEXT,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("   ✅ Table products créée")
        
        # Insérer des données de test
        print("3. Insertion des données de test...")
        
        # Produits de test
        cursor.execute("SELECT COUNT(*) FROM sge_cre.products")
        if cursor.fetchone()[0] == 0:
            test_products = [
                ("DELL-MS116-001", "Souris optique Dell", 125, 20, "E0-A1-01", "Périphériques"),
                ("HP-K120-001", "Clavier USB HP", 87, 15, "E1-B2-03", "Périphériques"),
                ("SAMSUNG-24-001", "Moniteur Full HD", 45, 10, "E2-C1-05", "Écrans"),
                ("DELL-LAPTOP-001", "Dell Latitude 7420", 23, 5, "E3-D3-02", "Ordinateurs"),
                ("LOGI-MX3-001", "Souris Logitech MX Master 3", 156, 30, "E0-A2-07", "Périphériques"),
                ("APPLE-MBP-001", "MacBook Pro 14", 12, 3, "E4-C2-01", "Ordinateurs"),
                ("SONY-WH1000-004", "Casque Sony WH-1000XM4", 34, 10, "E2-B1-04", "Audio"),
                ("ANKER-PWBC-001", "Power Bank 20000mAh", 89, 25, "E1-A3-08", "Accessoires")
            ]
            for product in test_products:
                cursor.execute('''
                    INSERT INTO sge_cre.products (code, name, stock, min_stock, location, category)
                    VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (code) DO NOTHING
                ''', product)
            print("   ✅ 8 produits de test ajoutés")
        
        # Mouvements de test
        cursor.execute("SELECT COUNT(*) FROM sge_cre.mouvements")
        if cursor.fetchone()[0] == 0:
            test_movements = [
                ("Entrée", "Souris optique Dell", 50, "REF-001", "Fournisseur Dell", "Zone A1", "Admin", "2024-01-15 09:00:00", "Réception initiale"),
                ("Sortie", "Clavier USB HP", 10, "REF-002", "Zone B2", "Service IT", "Admin", "2024-01-15 14:30:00", "Livraison service"),
                ("Entrée", "Moniteur Full HD", 20, "REF-003", "Fournisseur Samsung", "Zone C1", "Admin", "2024-01-16 10:15:00", "Nouvelle livraison"),
                ("Sortie", "Dell Latitude 7420", 2, "REF-004", "Zone C2", "Direction", "Admin", "2024-01-16 16:45:00", "Nouveaux employés"),
                ("Entrée", "Casque Sony WH-1000XM4", 15, "REF-005", "Fournisseur Sony", "Zone A2", "Admin", "2024-01-17 11:20:00", "Commande spéciale")
            ]
            for movement in test_movements:
                cursor.execute('''
                    INSERT INTO sge_cre.mouvements (type, produit_nom, quantite, reference, origine, destination, responsable, date_mouvement, commentaire)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', movement)
            print("   ✅ 5 mouvements de test ajoutés")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 Initialisation terminée avec succès!")
        print("✅ Tables mouvements et products créées")
        print("✅ Données de test insérées")
        print("\nVous pouvez maintenant utiliser la page des mouvements dans l'application")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return False

if __name__ == "__main__":
    init_mouvements_tables() 