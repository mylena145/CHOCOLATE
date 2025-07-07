# Guide d'Utilisation - Système de Gestion d'Entrepôt

## 🚀 Démarrage Rapide

### 1. Prérequis
- Python 3.8+
- PostgreSQL
- pgAdmin (optionnel mais recommandé)

### 2. Installation des dépendances
```bash
pip install customtkinter pillow psycopg2-binary
```

### 3. Configuration de la base de données
1. Créer une base PostgreSQL nommée `postgres`
2. Utilisateur: `postgres`
3. Mot de passe: `postgres123`
4. Port: `5432`

### 4. Initialisation de la base
1. Ouvrir pgAdmin
2. Se connecter à la base `postgres`
3. Exécuter le script `init_database_complete.sql`

### 5. Lancement de l'application
```bash
python app.py
```

## 📋 Fonctionnalités Principales

### 🔐 Authentification
- **Email**: brice.sodje@sac.com
- **Mot de passe**: brice25
- **Rôle**: Responsable_stocks

### 📦 Gestion des Produits
- Ajouter des produits
- Modifier les informations
- Supprimer des produits
- Voir le stock en temps réel

### 🏢 Gestion des Organisations
- Fournisseurs
- Transporteurs
- Destinataires

### 📍 Gestion des Entrepôts
- Zones de stockage
- Cellules
- Capacités

### 📊 Rapports
- Mouvements de stock
- Statistiques
- Alertes de stock

## 🛠️ Scripts Utiles

### Test du système
```bash
python test_complete_system.py
```

### Vérification de la base
```bash
python check_database.py
```

### Insertion de données de test
```bash
python insert_organisations_simple.py
python insert_entrepots.py
python insert_zone_stockage_corrected.py
```

## 🔧 Dépannage

### Erreur de connexion UTF-8
- Vérifier les paramètres de connexion dans `database.py`
- S'assurer que `client_encoding="utf8"` est présent

### Tables manquantes
- Exécuter le script d'initialisation complet
- Vérifier que le schéma `sge_cre` existe

### Erreurs de clés étrangères
- Insérer les données dans l'ordre logique :
  1. Organisations
  2. Produits
  3. Entrepôts
  4. Zones de stockage
  5. Lots
  6. Colis

### Erreurs de contraintes
- Vérifier la structure des tables avec les scripts de diagnostic
- Respecter les limites de caractères des colonnes

## 📁 Structure des Fichiers

```
CHOCOLATE/
├── app.py                    # Application principale
├── database.py              # Fonctions de base de données
├── AUTHENTIFICATION.py      # Interface d'authentification
├── DASHBOARD.py             # Tableau de bord
├── GESTION_PRODUITS.py      # Gestion des produits
├── GESTION_UTILISATEURS.py  # Gestion des utilisateurs
├── MOUVEMENTS_STOCK.py      # Mouvements de stock
├── RAPPORTS.py              # Rapports et statistiques
├── init_database_complete.sql # Script d'initialisation
├── test_complete_system.py  # Tests complets
└── GUIDE_UTILISATION.md     # Ce guide
```

## 🎯 Prochaines Étapes

1. **Tester toutes les fonctionnalités**
2. **Ajouter des données réelles**
3. **Configurer les alertes de stock**
4. **Personnaliser l'interface**
5. **Ajouter de nouvelles fonctionnalités**

## 📞 Support

En cas de problème :
1. Vérifier les logs d'erreur
2. Exécuter les scripts de diagnostic
3. Vérifier la configuration de la base de données
4. Consulter ce guide

## 🎉 Félicitations !

Ton système de gestion d'entrepôt est maintenant opérationnel ! 