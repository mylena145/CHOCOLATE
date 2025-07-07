# Ajouter un produit dans la table produits
def add_product(product_data):
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sge_cre.produits (id_produit, nom, description, marque, modele, fournisseur, date_fabrique, date_peremption, stock, alert)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        product_data.get("id"),
        product_data.get("name"),
        product_data.get("description"),
        product_data.get("brand"),
        product_data.get("sub"),
        product_data.get("fournisseur"),
        product_data.get("date_fabrique"),
        product_data.get("date_peremption"),
        product_data.get("stock"),
        product_data.get("alert")
    ))
    conn.commit()
    conn.close()

# Modifier un produit existant
def update_product(product_id, product_data):
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE sge_cre.produits SET nom=%s, description=%s, marque=%s, modele=%s, fournisseur=%s, date_fabrique=%s, date_peremption=%s, stock=%s, alert=%s
        WHERE id_produit=%s
    """, (
        product_data.get("name"),
        product_data.get("description"),
        product_data.get("brand"),
        product_data.get("sub"),
        product_data.get("fournisseur"),
        product_data.get("date_fabrique"),
        product_data.get("date_peremption"),
        product_data.get("stock"),
        product_data.get("alert"),
        product_id
    ))
    conn.commit()
    conn.close()

# Supprimer un produit
def delete_product(product_id):
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sge_cre.produits WHERE id_produit=%s", (product_id,))
    conn.commit()
    conn.close()
# Nouvelle fonction pour récupérer tous les produits depuis la table produits
def get_all_products():
    """Récupère tous les produits de la table sge_cre.produits (PostgreSQL)"""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_produit, nom, description, marque, modele, fournisseur, date_fabrique, date_peremption, stock, alert
        FROM sge_cre.produits
        ORDER BY nom
    """)
    produits = cursor.fetchall()
    conn.close()
    # Adapter au format attendu par l'UI (clé/valeur)
    produits_list = []
    for p in produits:
        stock = int(p[8]) if p[8] is not None else 0
        alert = int(p[9]) if p[9] is not None else 0
        produits_list.append({
            "id": p[0],
            "name": p[1],
            "sub": p[4],  # modele
            "brand": p[3],
            "stock": stock,
            "alert": alert,
            "loc": p[5] if p[5] else "",
            "status": "Critique" if stock <= alert else ("Faible" if stock <= alert*1.5 else "Normal"),
            "code": str(p[0]),
            "description": p[2],
            "date_fabrique": p[6],
            "date_peremption": p[7],
            "fournisseur": p[5]
        })
    return produits_list
import psycopg2
import hashlib
import os
import datetime

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

def check_user(email, password):
    """
    Vérifie les identifiants de l'utilisateur.
    Retourne: ("SUCCESS", user_data) ou ("ERROR_TYPE", None)
    """
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        # Vérifier si l'utilisateur existe et récupérer ses données
        cursor.execute("SELECT id_individu, nom, password, email, adresse, prenom, role, telephone, matricule FROM sge_cre.individus WHERE email=%s", (email,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return "USER_NOT_FOUND", None
        stored_password = user[2]
        if password != stored_password:
            conn.close()
            return "WRONG_PASSWORD", None
        user_data = {
            "id": user[0],  # id_individu
            "nom": user[1],
            "password": user[2],
            "email": user[3],
            "adresse": user[4],
            "prenom": user[5],
            "role": user[6],
            "telephone": user[7],
            # Gestion défensive du matricule (peut être None ou absent)
            "matricule": user[8] if len(user) > 8 and user[8] is not None else ""
        }
        conn.close()
        return "SUCCESS", user_data
    except psycopg2.Error as e:
        print(f"Erreur base de données: {e}")
        return "DATABASE_ERROR", None
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return "UNKNOWN_ERROR", None

def init_database():
    """Initialise la base de données avec des utilisateurs de test et un système de rôles complet"""
    # PostgreSQL : pas de fichier local, on tente la création à chaque fois
    try:
        # On ne fait rien si la table individus existe déjà : on laisse l'utilisateur gérer ses données
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        cursor.execute("SELECT to_regclass('sge_cre.individus')")
        result = cursor.fetchone()
        if result and result[0] == 'sge_cre.individus':
            print("Table 'sge_cre.individus' déjà existante, aucune initialisation n'est faite.")
            conn.close()
            return
        else:
            print("Table 'sge_cre.individus' absente, vous devez la créer manuellement ou activer l'initialisation automatique si besoin.")
            conn.close()
            return
    except psycopg2.Error as e:
        print(f"Erreur lors de la vérification de la table individus: {e}")

# Initialisation automatique si besoin
# init_database()  # Désactivé pour éviter les erreurs d'encodage

# IMPORTANT: L'initialisation de la base de données se fait maintenant
# via les scripts SGE_*.sql (SGE_CRE.sql, SGE_JEU.sql, etc.)
# Exécutez ces scripts manuellement dans PostgreSQL avant de lancer l'application

def list_users():
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    # On récupère les utilisateurs depuis la table individus (pas users)
    cursor.execute("""
        SELECT id_individu, nom, prenom, email, role, adresse, telephone, matricule
        FROM sge_cre.individus
        ORDER BY nom, prenom
    """)
    users = cursor.fetchall()
    conn.close()
    return users

def get_user_permissions(role_name):
    """Récupère les permissions d'un rôle"""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nom, p.description, p.module, p.action
        FROM permissions p
        JOIN role_permissions rp ON p.id = rp.permission_id
        JOIN roles r ON rp.role_id = r.id
        WHERE r.nom = %s
        ORDER BY p.module, p.action
    """, (role_name,))
    permissions = cursor.fetchall()
    conn.close()
    return permissions

def get_all_roles():
    """Récupère tous les rôles avec leurs permissions"""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.nom, r.description, r.niveau_acces, r.couleur,
               STRING_AGG(p.nom, ',') as permissions
        FROM roles r
        LEFT JOIN role_permissions rp ON r.id = rp.role_id
        LEFT JOIN permissions p ON rp.permission_id = p.id
        GROUP BY r.id
        ORDER BY r.niveau_acces DESC, r.nom
    """)
    roles = cursor.fetchall()
    conn.close()
    return roles

def update_user(user_id, nom, prenom, email, role, adresse, telephone, matricule):
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE sge_cre.individus SET nom=%s, prenom=%s, email=%s, role=%s, adresse=%s, telephone=%s , matricule=%s WHERE id_individu=%s
    """, (nom, prenom, email, role, adresse, telephone, matricule, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sge_cre.individus WHERE id_individu=%s", (user_id,))
    conn.commit()
    conn.close()

def reset_password(user_id, new_password):
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("UPDATE sge_cre.individus SET password=%s WHERE id_individu=%s", (new_password, user_id))
    conn.commit()
    conn.close()

# Ajouter ces fonctions dans database.py après les fonctions existantes

def init_movements_tables():
    """Initialise les tables nécessaires pour les mouvements"""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    
    # Table des mouvements dans le schéma sge_cre
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
    
    # Table temporaire des produits si elle n'existe pas
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
    
    # Insérer quelques produits de test si la table est vide
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
    
    # Ajouter quelques mouvements de test
    cursor.execute("SELECT COUNT(*) FROM sge_cre.mouvements")
    if cursor.fetchone()[0] == 0:
        test_movements = [
            ("Entrée", "Souris optique Dell", 50, "REF-001", "Fournisseur Dell", "Zone A1", "Admin", "2024-01-15 09:00:00", "Réception initiale"),
            ("Sortie", "Clavier USB HP", 10, "REF-002", "Zone B2", "Service IT", "Admin", "2024-01-15 14:30:00", "Livraison service"),
            ("Entrée", "Moniteur Full HD", 20, "REF-003", "Fournisseur Samsung", "Zone C1", "Admin", "2024-01-16 10:15:00", "Nouvelle livraison")
        ]
        for movement in test_movements:
            cursor.execute('''
                INSERT INTO sge_cre.mouvements (type, produit_nom, quantite, reference, origine, destination, responsable, date_mouvement, commentaire)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', movement)
    
    conn.commit()
    conn.close()
    print("Tables des mouvements initialisées avec succès (PostgreSQL)")

def get_movement_stats():
    """Récupère les statistiques des mouvements"""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    stats = {}
    # Total entrées aujourd'hui
    cursor.execute("""
        SELECT COUNT(*) FROM sge_cre.mouvements 
        WHERE type = 'Entrée' AND date(date_mouvement) = CURRENT_DATE
    """)
    stats['entries_today'] = cursor.fetchone()[0]
    # Total sorties aujourd'hui
    cursor.execute("""
        SELECT COUNT(*) FROM sge_cre.mouvements 
        WHERE type = 'Sortie' AND date(date_mouvement) = CURRENT_DATE
    """)
    stats['exits_today'] = cursor.fetchone()[0]
    # Total mouvements cette semaine
    cursor.execute("""
        SELECT COUNT(*) FROM sge_cre.mouvements 
        WHERE date(date_mouvement) >= CURRENT_DATE - INTERVAL '7 days'
    """)
    stats['week_total'] = cursor.fetchone()[0]
    conn.close()
    return stats

# Appeler l'initialisation au démarrage
# init_movements_tables()  # Désactivé pour éviter les erreurs d'encodage

def deactivate_user(user_id):
    # Pour la démo, on supprime l'utilisateur (ou on pourrait ajouter un champ 'actif' dans la table)
    delete_user(user_id)

def get_all_emballages():
    """Récupère tous les emballages de la table sge_cre.materiel_emballage (PostgreSQL)"""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_emballeur, type_emballage, etat_emballage
        FROM sge_cre.materiel_emballage
        ORDER BY id_emballeur DESC
    """)
    emballages = cursor.fetchall()
    conn.close()
    
    emballages_list = []
    for e in emballages:
        emballages_list.append({
            "id": e[0],
            "type": e[1],
            "etat": e[2],
            "date_creation": "2024-01-15",  # À ajouter dans la table si nécessaire
            "responsable": "Système",  # À ajouter dans la table si nécessaire
            "statut": "En cours" if e[2] == "Neuf" else "Terminé"
        })
    return emballages_list

def add_emballage(type_emballage, etat_emballage):
    """Ajoute un nouvel emballage dans la base de données"""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO sge_cre.materiel_emballage (type_emballage, etat_emballage)
            VALUES (%s, %s)
            RETURNING id_emballeur
        """, (type_emballage, etat_emballage))
        new_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return new_id
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e

def update_emballage(id_emballeur, type_emballage, etat_emballage):
    """Met à jour un emballage existant"""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE sge_cre.materiel_emballage 
            SET type_emballage = %s, etat_emballage = %s
            WHERE id_emballeur = %s
        """, (type_emballage, etat_emballage, id_emballeur))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e

def delete_emballage(id_emballeur):
    """Supprime un emballage"""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM sge_cre.materiel_emballage WHERE id_emballeur = %s", (id_emballeur,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e

def get_emballage_stats():
    """Récupère les statistiques des emballages"""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN etat_emballage = 'disponible' THEN 1 END) as disponible,
            COUNT(CASE WHEN etat_emballage = 'en_utilisation' THEN 1 END) as en_utilisation,
            COUNT(CASE WHEN etat_emballage = 'hors_service' THEN 1 END) as hors_service
        FROM sge_cre.materiel_emballage
    """)
    stats = cursor.fetchone()
    conn.close()
    return {
        "total": stats[0] if stats[0] else 0,
        "disponible": stats[1] if stats[1] else 0,
        "en_utilisation": stats[2] if stats[2] else 0,
        "hors_service": stats[3] if stats[3] else 0
    }

# =============================================
# FONCTIONS POUR LES EXPÉDITIONS
# =============================================

def get_all_expeditions():
    """Récupère toutes les expéditions depuis la base de données"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                be.id_bon_expedition,
                be.client,
                be.reference_commande,
                be.date_livraison,
                be.observation,
                be.liste_articles_livres,
                be.transporteurs,
                c.poids,
                c.dimension,
                COALESCE(c.id_colis, 0) as id_colis
            FROM sge_cre.bon_expeditions be
            LEFT JOIN sge_cre.colis c ON be.id_colis = c.id_colis
            ORDER BY be.date_livraison DESC
        """)
        expeditions = cursor.fetchall()
        conn.close()
        
        # Convertir en format attendu par l'UI
        expeditions_list = []
        for exp in expeditions:
            # Générer un numéro d'expédition basé sur l'ID
            expedition_number = f"BE-2024-{exp[0]:03d}"
            
            # Déterminer le statut basé sur la date de livraison
            from datetime import datetime, date
            today = date.today()
            delivery_date = exp[3] if exp[3] else today
            
            if delivery_date < today:
                status = "delivered"
            elif delivery_date == today:
                status = "in-transit"
            else:
                status = "preparing"
            
            # Déterminer la priorité basée sur la date
            days_diff = (delivery_date - today).days
            if days_diff <= 1:
                priority = "haute"
            elif days_diff <= 3:
                priority = "moyenne"
            else:
                priority = "basse"
            
            expeditions_list.append({
                'id': exp[0],
                'number': expedition_number,
                'client': exp[1] if exp[1] else "Client non spécifié",
                'shippingDate': today.strftime('%Y-%m-%d'),
                'deliveryDate': delivery_date.strftime('%Y-%m-%d'),
                'actualDeliveryDate': delivery_date.strftime('%Y-%m-%d') if status == "delivered" else None,
                'carrier': exp[6] if exp[6] else "Non spécifié",
                'priority': priority,
                'packages': 1,  # Par défaut
                'totalWeight': float(exp[7]) if exp[7] else 0.0,
                'status': status,
                'trackingNumber': exp[2] if exp[2] else None,
                'observation': exp[4] if exp[4] else "",
                'articles': exp[5] if exp[5] else ""
            })
        
        return expeditions_list
    except Exception as e:
        print(f"Erreur lors de la récupération des expéditions: {e}")
        return []

def add_expedition(expedition_data):
    """Ajoute une nouvelle expédition dans la base de données"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sge_cre.bon_expeditions 
            (client, reference_commande, date_livraison, observation, liste_articles_livres, transporteurs)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_bon_expedition
        """, (
            expedition_data.get('client'),
            expedition_data.get('reference_commande'),
            expedition_data.get('date_livraison'),
            expedition_data.get('observation', ''),
            expedition_data.get('liste_articles_livres', ''),
            expedition_data.get('transporteurs')
        ))
        
        expedition_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        print(f"Expédition créée avec l'ID: {expedition_id}")
        return expedition_id
    except Exception as e:
        print(f"Erreur lors de la création de l'expédition: {e}")
        return None

def update_expedition(expedition_id, expedition_data):
    """Met à jour une expédition existante"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE sge_cre.bon_expeditions 
            SET client = %s, reference_commande = %s, date_livraison = %s, 
                observation = %s, liste_articles_livres = %s, transporteurs = %s
            WHERE id_bon_expedition = %s
        """, (
            expedition_data.get('client'),
            expedition_data.get('reference_commande'),
            expedition_data.get('date_livraison'),
            expedition_data.get('observation', ''),
            expedition_data.get('liste_articles_livres', ''),
            expedition_data.get('transporteurs'),
            expedition_id
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'expédition: {e}")
        return False

def delete_expedition(expedition_id):
    """Supprime une expédition"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sge_cre.bon_expeditions WHERE id_bon_expedition = %s", (expedition_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression de l'expédition: {e}")
        return False

def get_expedition_stats():
    """Récupère les statistiques des expéditions"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        # Statistiques par statut
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN date_livraison > CURRENT_DATE THEN 1 END) as en_preparation,
                COUNT(CASE WHEN date_livraison = CURRENT_DATE THEN 1 END) as aujourd_hui,
                COUNT(CASE WHEN date_livraison < CURRENT_DATE THEN 1 END) as livrees
            FROM sge_cre.bon_expeditions
        """)
        stats = cursor.fetchone()
        
        # Statistiques par transporteur
        cursor.execute("""
            SELECT transporteurs, COUNT(*) as count
            FROM sge_cre.bon_expeditions
            GROUP BY transporteurs
            ORDER BY count DESC
        """)
        carriers = cursor.fetchall()
        
        conn.close()
        
        return {
            "total": stats[0] if stats[0] else 0,
            "en_preparation": stats[1] if stats[1] else 0,
            "aujourd_hui": stats[2] if stats[2] else 0,
            "livrees": stats[3] if stats[3] else 0,
            "transporteurs": {carrier[0]: carrier[1] for carrier in carriers}
        }
    except Exception as e:
        print(f"Erreur lors de la récupération des statistiques: {e}")
        return {
            "total": 0,
            "en_preparation": 0,
            "aujourd_hui": 0,
            "livrees": 0,
            "transporteurs": {}
        }

def search_expedition(search_term):
    """Recherche une expédition par numéro, client ou référence"""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                be.id_bon_expedition,
                be.client,
                be.reference_commande,
                be.date_livraison,
                be.observation,
                be.liste_articles_livres,
                be.transporteurs,
                c.poids,
                c.dimension
            FROM sge_cre.bon_expeditions be
            LEFT JOIN sge_cre.colis c ON be.id_colis = c.id_colis
            WHERE be.client ILIKE %s 
               OR be.reference_commande ILIKE %s
               OR CAST(be.id_bon_expedition AS TEXT) ILIKE %s
            ORDER BY be.date_livraison DESC
        """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        expeditions = cursor.fetchall()
        conn.close()
        
        # Convertir au même format que get_all_expeditions
        expeditions_list = []
        for exp in expeditions:
            expedition_number = f"BE-2024-{exp[0]:03d}"
            from datetime import datetime, date
            today = date.today()
            delivery_date = exp[3] if exp[3] else today
            
            if delivery_date < today:
                status = "delivered"
            elif delivery_date == today:
                status = "in-transit"
            else:
                status = "preparing"
            
            days_diff = (delivery_date - today).days
            if days_diff <= 1:
                priority = "haute"
            elif days_diff <= 3:
                priority = "moyenne"
            else:
                priority = "basse"
            
            expeditions_list.append({
                'id': exp[0],
                'number': expedition_number,
                'client': exp[1] if exp[1] else "Client non spécifié",
                'shippingDate': today.strftime('%Y-%m-%d'),
                'deliveryDate': delivery_date.strftime('%Y-%m-%d'),
                'actualDeliveryDate': delivery_date.strftime('%Y-%m-%d') if status == "delivered" else None,
                'carrier': exp[6] if exp[6] else "Non spécifié",
                'priority': priority,
                'packages': 1,
                'totalWeight': float(exp[7]) if exp[7] else 0.0,
                'status': status,
                'trackingNumber': exp[2] if exp[2] else None,
                'observation': exp[4] if exp[4] else "",
                'articles': exp[5] if exp[5] else ""
            })
        
        return expeditions_list
    except Exception as e:
        print(f"Erreur lors de la recherche d'expédition: {e}")
        return []

def get_today_expeditions():
    """Récupère les expéditions dont la date de livraison est aujourd'hui"""
    from datetime import date
    today = date.today()
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                be.id_bon_expedition,
                be.client,
                be.reference_commande,
                be.date_livraison,
                be.observation,
                be.liste_articles_livres,
                be.transporteurs,
                c.poids,
                c.dimension,
                COALESCE(c.id_colis, 0) as id_colis
            FROM sge_cre.bon_expeditions be
            LEFT JOIN sge_cre.colis c ON be.id_colis = c.id_colis
            WHERE be.date_livraison = %s
            ORDER BY be.id_bon_expedition
        ''', (today,))
        expeditions = cursor.fetchall()
        conn.close()
        expeditions_list = []
        for exp in expeditions:
            expedition_number = f"BE-2024-{exp[0]:03d}"
            expeditions_list.append({
                'id': exp[0],
                'number': expedition_number,
                'client': exp[1] if exp[1] else "Client non spécifié",
                'shippingDate': today.strftime('%Y-%m-%d'),
                'deliveryDate': today.strftime('%Y-%m-%d'),
                'carrier': exp[6] if exp[6] else "Non spécifié",
                'priority': "haute",
                'packages': 1,
                'totalWeight': float(exp[7]) if exp[7] else 0.0,
                'status': "in-transit",
                'trackingNumber': exp[2] if exp[2] else None,
                'observation': exp[4] if exp[4] else "",
                'articles': exp[5] if exp[5] else ""
            })
        return expeditions_list
    except Exception as e:
        print(f"Erreur lors de la récupération des expéditions du jour: {e}")
        return []

def get_all_colis():
    """Récupère tous les colis avec infos zone, réception, etc."""
    try:
        conn = psycopg2.connect(**PG_CONN)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                c.id_colis,
                c.id_zo_stock,
                c.id_reception,
                c.dimension,
                c.poids,
                c.emplacement,
                z.id_entrepot,
                z.id_cellule,
                z.e1, z.e2, z.e3,
                r.date_reception
            FROM sge_cre.colis c
            LEFT JOIN sge_cre.zone_stockage z ON c.id_zo_stock = z.id_zo_stock
            LEFT JOIN sge_cre.receptions r ON c.id_reception = r.id_reception
            ORDER BY c.id_colis
        ''')
        colis = cursor.fetchall()
        conn.close()
        colis_list = []
        for c in colis:
            colis_list.append({
                'id': c[0],
                'zone_stockage': c[1],
                'reception': c[2],
                'dimension': c[3],
                'poids': c[4],
                'emplacement': c[5],
                'entrepot': c[6],
                'cellule': c[7],
                'zone_e1': c[8],
                'zone_e2': c[9],
                'zone_e3': c[10],
                'date_reception': c[11]
            })
        return colis_list
    except Exception as e:
        print(f"Erreur lors de la récupération des colis: {e}")
        return []

def get_mouvements_7_jours():
    """Retourne une liste du nombre de mouvements par jour sur les 7 derniers jours (du plus ancien au plus récent)."""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    # Générer les 7 derniers jours
    jours = [(datetime.date.today() - datetime.timedelta(days=i)) for i in range(6, -1, -1)]
    result = []
    for jour in jours:
        cursor.execute("""
            SELECT COUNT(*) FROM sge_cre.mouvements WHERE date(date_mouvement) = %s
        """, (jour,))
        count = cursor.fetchone()[0]
        result.append(count)
    conn.close()
    return result

def get_repartition_zones():
    """Retourne un dict {zone: nombre_de_produits} pour la répartition des produits par zone."""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT zone_stockage, COUNT(*) FROM sge_cre.produits GROUP BY zone_stockage
    """)
    data = cursor.fetchall()
    conn.close()
    return {row[0] if row[0] else 'Inconnu': row[1] for row in data}

def get_cellules_stats():
    """Retourne (nb_cellules_occupees, nb_cellules_total)"""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    # Nombre total de cellules
    cursor.execute("SELECT COUNT(*) FROM sge_cre.cellules")
    total = cursor.fetchone()[0]
    # Nombre de cellules occupées (présentes dans zone_stockage)
    cursor.execute("SELECT COUNT(DISTINCT id_cellule) FROM sge_cre.zone_stockage")
    occupees = cursor.fetchone()[0]
    conn.close()
    return occupees, total

def get_commandes_en_cours():
    """Retourne le nombre de commandes en cours (statut = 'en_cours' ou 'en_attente') dans commandes_achats et commandes_vends"""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    # Commandes achats
    cursor.execute("SELECT COUNT(*) FROM sge_cre.commandes_achats WHERE statut IN ('en_cours', 'en_attente')")
    achats = cursor.fetchone()[0]
    # Commandes ventes
    cursor.execute("SELECT COUNT(*) FROM sge_cre.commandes_vends WHERE statut IN ('en_cours', 'en_attente')")
    vends = cursor.fetchone()[0]
    conn.close()
    return achats + vends

def get_recent_activity(limit=10):
    """Retourne les derniers mouvements (activité récente) pour le dashboard."""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type, produit_nom, quantite, responsable, date_mouvement, commentaire
        FROM sge_cre.mouvements
        ORDER BY date_mouvement DESC
        LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    activity = []
    for row in rows:
        type_mvt, produit, quantite, responsable, date_mvt, commentaire = row
        # Mapping pour l'icône et la couleur
        if type_mvt == 'Entrée':
            icon = '📥'
            color = '#3B82F6'
        elif type_mvt == 'Sortie':
            icon = '🚚'
            color = '#10B981'
        else:
            icon = '✏️'
            color = '#F59E0B'
        # Format date
        if isinstance(date_mvt, str):
            time_str = date_mvt
        else:
            time_str = date_mvt.strftime('%d/%m/%Y %H:%M')
        activity.append({
            'icon': icon,
            'user': responsable,
            'action': f"{type_mvt.lower()} {quantite} x {produit}",
            'time': time_str,
            'color': color,
            'type': type_mvt
        })
    return activity

def get_all_zones():
    """Retourne la liste des zones de stockage avec cellules et statuts pour l'affichage temps réel de l'entrepôt."""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    # Récupérer toutes les zones de stockage
    cursor.execute('''
        SELECT z.id_entrepot, z.e1, z.e2, z.e3, z.id_cellule, c.longueur, c.largeur, c.hauteur, c.masse_maximale
        FROM sge_cre.zone_stockage z
        JOIN sge_cre.cellules c ON z.id_cellule = c.id_cellule
        ORDER BY z.e1, z.e2, z.e3, z.id_cellule
    ''')
    rows = cursor.fetchall()
    # Récupérer les cellules occupées (présence de colis)
    cursor.execute('SELECT DISTINCT id_cellule FROM sge_cre.zone_stockage WHERE id_zo_stock IN (SELECT id_zo_stock FROM sge_cre.colis)')
    occupees = set(r[0] for r in cursor.fetchall())
    # Pour la maintenance, on suppose qu'il y a un champ ou une logique à adapter (ici, aucune cellule en maintenance)
    zones_dict = {}
    for row in rows:
        id_entrepot, e1, e2, e3, id_cellule, longueur, largeur, hauteur, masse_maximale = row
        zone_key = f"{e1}"
        if zone_key not in zones_dict:
            zones_dict[zone_key] = {
                'name': f"{e1}",
                'desc': f"{e1} - {e2} - {e3}",
                'pct': 0,  # Calculé plus bas
                'cells': [],
                'statuses': []
            }
        zones_dict[zone_key]['cells'].append(id_cellule)
        if id_cellule in occupees:
            zones_dict[zone_key]['statuses'].append('occupied')
        else:
            zones_dict[zone_key]['statuses'].append('free')
    # Calcul du pourcentage d'occupation par zone
    for zone in zones_dict.values():
        total = len(zone['cells'])
        occ = sum(1 for s in zone['statuses'] if s == 'occupied')
        zone['pct'] = int((occ / total) * 100) if total > 0 else 0
        zone['desc'] = f"{zone['name']} - {occ}/{total} occupées"
    conn.close()
    return list(zones_dict.values())

def add_cellule(cell_name, zone_name):
    """Ajoute une nouvelle cellule et la zone de stockage associée dans la base."""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    # Insérer la cellule (dimensions par défaut, à adapter si besoin)
    try:
        cursor.execute("""
            INSERT INTO sge_cre.cellules (id_cellule, longueur, largeur, hauteur, masse_maximale)
            VALUES (%s, %s, %s, %s, %s)
        """, (cell_name, 100.0, 100.0, 100.0, 50.0))
    except Exception as e:
        print(f"Cellule déjà existante ou erreur: {e}")
    # Insérer la zone de stockage (e1=zone_name, e2/e3 valeurs par défaut)
    try:
        cursor.execute("""
            INSERT INTO sge_cre.zone_stockage (id_entrepot, id_cellule, e1, e2, e3)
            VALUES (%s, %s, %s, %s, %s)
        """, ("ENT001", cell_name, zone_name, "Rayon 1", "Étage 1"))
    except Exception as e:
        print(f"Zone de stockage déjà existante ou erreur: {e}")
    conn.commit()
    conn.close()

def get_all_zone_names():
    """Retourne la liste des noms de zones (e1) distincts dans la table zone_stockage."""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT e1 FROM sge_cre.zone_stockage ORDER BY e1')
    zones = [row[0] for row in cursor.fetchall()]
    conn.close()
    return zones

def get_cellules_stats_detail():
    """Retourne (total, occupees, libres, maintenance) selon la logique d'affichage (statut par cellule)."""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    # Récupérer toutes les cellules de zone_stockage
    cursor.execute('SELECT id_cellule FROM sge_cre.zone_stockage')
    all_cells = [r[0] for r in cursor.fetchall()]
    total = len(all_cells)
    # Récupérer les cellules occupées (présence de colis)
    cursor.execute('SELECT DISTINCT id_cellule FROM sge_cre.zone_stockage WHERE id_zo_stock IN (SELECT id_zo_stock FROM sge_cre.colis)')
    occupees = set(r[0] for r in cursor.fetchall())
    # Pour la maintenance, on suppose aucune cellule en maintenance (à adapter si besoin)
    libres = [c for c in all_cells if c not in occupees]
    maintenance = 0
    conn.close()
    return total, len(occupees), len(libres), maintenance

def get_reception_stats():
    """Retourne (colis_en_attente, capacite_max, occupation_pct) pour la zone de réception."""
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    # Nombre de colis en attente (statut en_cours ou en_attente dans receptions)
    cursor.execute("SELECT COUNT(*) FROM sge_cre.colis c JOIN sge_cre.receptions r ON c.id_reception = r.id_reception WHERE r.statut IN ('en_cours', 'en_attente')")
    colis_en_attente = cursor.fetchone()[0]
    # Capacité maximale (à adapter si champ spécifique, ici valeur fixe 50)
    capacite_max = 50
    # Occupation = (colis en attente / capacité max)
    occupation_pct = int((colis_en_attente / capacite_max) * 100) if capacite_max else 0
    conn.close()
    return colis_en_attente, capacite_max, occupation_pct

def get_total_products():
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM sge_cre.produits')
    total = cursor.fetchone()[0]
    conn.close()
    return total

def get_lots_actifs():
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM sge_cre.lots')
    total = cursor.fetchone()[0]
    conn.close()
    return total

def get_stock_critique():
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM sge_cre.produits WHERE stock <= alert')
    total = cursor.fetchone()[0]
    conn.close()
    return total

def get_valeur_stock():
    conn = psycopg2.connect(**PG_CONN)
    cursor = conn.cursor()
    # On suppose qu'il y a un champ prix_unitaire dans produits, sinon retourne 0
    try:
        cursor.execute('SELECT SUM(stock * prix_unitaire) FROM sge_cre.produits')
        total = cursor.fetchone()[0]
        if total is None:
            total = 0
    except Exception:
        total = 0
    conn.close()
    return total

if __name__ == "__main__":
    init_database()  # Désactivé pour éviter les erreurs d'encodage
    pass 