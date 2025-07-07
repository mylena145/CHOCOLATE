import os
import sqlite3
import hashlib

# Supprimer l'ancienne base si elle existe
if os.path.exists('sac.db'):
    os.remove('sac.db')

conn = sqlite3.connect('sac.db')
cursor = conn.cursor()

# Créer la table users avec les nouveaux champs
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        mot_de_passe TEXT NOT NULL,
        role TEXT NOT NULL,
        matricule TEXT UNIQUE NOT NULL,
        actif INTEGER DEFAULT 1,
        date_creation TEXT DEFAULT CURRENT_TIMESTAMP,
        derniere_connexion TEXT
    )
''')

# Créer la table des rôles avec permissions détaillées
cursor.execute('''
    CREATE TABLE IF NOT EXISTS roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT UNIQUE NOT NULL,
        description TEXT,
        niveau_acces INTEGER DEFAULT 1,
        couleur TEXT DEFAULT '#6B7280'
    )
''')

# Créer la table des permissions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT UNIQUE NOT NULL,
        description TEXT,
        module TEXT NOT NULL,
        action TEXT NOT NULL
    )
''')

# Créer la table de liaison rôles-permissions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS role_permissions (
        role_id INTEGER,
        permission_id INTEGER,
        FOREIGN KEY (role_id) REFERENCES roles (id),
        FOREIGN KEY (permission_id) REFERENCES permissions (id),
        PRIMARY KEY (role_id, permission_id)
    )
''')

# Insérer les rôles standards
roles = [
    ("Super Administrateur", "Accès complet à toutes les fonctionnalités du système", 5, "#DC2626"),
    ("Administrateur", "Gestion complète des utilisateurs et paramètres système", 4, "#7C3AED"),
    ("Gestionnaire Entrepôt", "Gestion des stocks, réceptions, expéditions et rapports", 3, "#2563EB"),
    ("Responsable Réception", "Gestion des réceptions et contrôle qualité", 2, "#059669"),
    ("Opérateur Stock", "Opérations de stockage et inventaire", 2, "#D97706"),
    ("Expéditeur", "Gestion des expéditions et livraisons", 2, "#F59E0B"),
    ("Consultant", "Consultation des rapports et statistiques", 1, "#6B7280"),
    ("Stagiaire", "Accès limité en lecture seule", 1, "#9CA3AF")
]

for nom, desc, niveau, couleur in roles:
    cursor.execute("INSERT INTO roles (nom, description, niveau_acces, couleur) VALUES (?, ?, ?, ?)", 
                 (nom, desc, niveau, couleur))

# Insérer les permissions détaillées
permissions = [
    # Gestion des utilisateurs
    ("user_create", "Créer des utilisateurs", "users", "create"),
    ("user_read", "Lire les informations utilisateurs", "users", "read"),
    ("user_update", "Modifier les utilisateurs", "users", "update"),
    ("user_delete", "Supprimer des utilisateurs", "users", "delete"),
    ("user_reset_pwd", "Réinitialiser les mots de passe", "users", "reset_password"),
    
    # Gestion des rôles
    ("role_manage", "Gérer les rôles et permissions", "roles", "manage"),
    
    # Dashboard
    ("dashboard_view", "Voir le tableau de bord", "dashboard", "view"),
    ("dashboard_export", "Exporter les données du dashboard", "dashboard", "export"),
    
    # Stocks
    ("stock_view", "Consulter les stocks", "stock", "view"),
    ("stock_create", "Créer des produits", "stock", "create"),
    ("stock_update", "Modifier les produits", "stock", "update"),
    ("stock_delete", "Supprimer des produits", "stock", "delete"),
    ("stock_export", "Exporter les données de stock", "stock", "export"),
    ("stock_alert", "Gérer les alertes de stock", "stock", "alert"),
    
    # Réceptions
    ("reception_view", "Consulter les réceptions", "reception", "view"),
    ("reception_create", "Créer des bons de réception", "reception", "create"),
    ("reception_update", "Modifier les réceptions", "reception", "update"),
    ("reception_validate", "Valider les réceptions", "reception", "validate"),
    ("reception_export", "Exporter les données de réception", "reception", "export"),
    
    # Expéditions
    ("expedition_view", "Consulter les expéditions", "expedition", "view"),
    ("expedition_create", "Créer des bons d'expédition", "expedition", "create"),
    ("expedition_update", "Modifier les expéditions", "expedition", "update"),
    ("expedition_validate", "Valider les expéditions", "expedition", "validate"),
    ("expedition_export", "Exporter les données d'expédition", "expedition", "export"),
    
    # Emballages
    ("packaging_view", "Consulter les emballages", "packaging", "view"),
    ("packaging_manage", "Gérer les emballages", "packaging", "manage"),
    
    # Entrepôts
    ("warehouse_view", "Consulter les entrepôts", "warehouse", "view"),
    ("warehouse_manage", "Gérer les entrepôts", "warehouse", "manage"),
    
    # Rapports
    ("report_view", "Consulter les rapports", "reports", "view"),
    ("report_create", "Créer des rapports", "reports", "create"),
    ("report_export", "Exporter les rapports", "reports", "export"),
    ("report_schedule", "Programmer des rapports", "reports", "schedule"),
    
    # Administration
    ("admin_settings", "Gérer les paramètres système", "admin", "settings"),
    ("admin_audit", "Consulter les logs d'activité", "admin", "audit"),
    ("admin_backup", "Gérer les sauvegardes", "admin", "backup"),
    
    # CLI
    ("cli_access", "Accès à l'interface CLI", "cli", "access")
]

for nom, desc, module, action in permissions:
    cursor.execute("INSERT INTO permissions (nom, description, module, action) VALUES (?, ?, ?, ?)", 
                 (nom, desc, module, action))

# Assigner les permissions aux rôles
role_permissions = {
    "Super Administrateur": [p[0] for p in permissions],  # Toutes les permissions
    "Administrateur": [p[0] for p in permissions if p[0] not in ["admin_backup"]],  # Sauf backup
    "Gestionnaire Entrepôt": [
        "dashboard_view", "dashboard_export",
        "stock_view", "stock_create", "stock_update", "stock_export", "stock_alert",
        "reception_view", "reception_create", "reception_update", "reception_validate", "reception_export",
        "expedition_view", "expedition_create", "expedition_update", "expedition_validate", "expedition_export",
        "packaging_view", "packaging_manage",
        "warehouse_view", "warehouse_manage",
        "report_view", "report_create", "report_export", "report_schedule"
    ],
    "Responsable Réception": [
        "dashboard_view",
        "stock_view",
        "reception_view", "reception_create", "reception_update", "reception_validate", "reception_export",
        "packaging_view",
        "report_view"
    ],
    "Opérateur Stock": [
        "dashboard_view",
        "stock_view", "stock_update",
        "reception_view", "reception_update",
        "warehouse_view"
    ],
    "Expéditeur": [
        "dashboard_view",
        "stock_view",
        "expedition_view", "expedition_create", "expedition_update", "expedition_validate", "expedition_export",
        "packaging_view",
        "report_view"
    ],
    "Consultant": [
        "dashboard_view",
        "stock_view",
        "reception_view",
        "expedition_view",
        "report_view", "report_export"
    ],
    "Stagiaire": [
        "dashboard_view",
        "stock_view",
        "reception_view",
        "expedition_view"
    ]
}

# Insérer les liaisons rôles-permissions
for role_name, perms in role_permissions.items():
    cursor.execute("SELECT id FROM roles WHERE nom = ?", (role_name,))
    role_id = cursor.fetchone()[0]
    
    for perm_name in perms:
        cursor.execute("SELECT id FROM permissions WHERE nom = ?", (perm_name,))
        perm_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO role_permissions (role_id, permission_id) VALUES (?, ?)", (role_id, perm_id))

# Ajouter des utilisateurs de test avec les nouveaux rôles
test_users = [
    ("Dupont", "Jean", "jean.dupont@sac.com", "password123", "Super Administrateur", "SA001"),
    ("Martin", "Marie", "marie.martin@sac.com", "password123", "Gestionnaire Entrepôt", "GE002"),
    ("Durand", "Pierre", "pierre.durand@sac.com", "password123", "Responsable Réception", "RR003"),
    ("Sielinou", "Noelle", "noelle.sielinou@sac.com", "noelle25", "Super Administrateur", "SA004"),
    ("Bernard", "Sophie", "sophie.bernard@sac.com", "password123", "Opérateur Stock", "OS005"),
    ("Leroy", "Thomas", "thomas.leroy@sac.com", "password123", "Expéditeur", "EX006"),
    ("Moreau", "Julie", "julie.moreau@sac.com", "password123", "Consultant", "CO007"),
    ("Petit", "Lucas", "lucas.petit@sac.com", "password123", "Stagiaire", "ST008")
]

for nom, prenom, email, password, role, matricule in test_users:
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute(
        "INSERT INTO users (nom, prenom, email, mot_de_passe, role, matricule) VALUES (?, ?, ?, ?, ?, ?)",
        (nom, prenom, email, hashed_password, role, matricule)
    )

conn.commit()
print("Base de données réinitialisée avec le nouveau système de rôles professionnels.")
print("Utilisateurs créés :")
for row in cursor.execute("SELECT id, nom, prenom, email, role, matricule FROM users ORDER BY role, nom"):
    print(f"  {row[1]} {row[2]} ({row[4]}) - {row[3]}")
conn.close() 