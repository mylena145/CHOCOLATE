# Guide d'Initialisation de la Base de Données SGE

## 🎯 Vue d'ensemble

Ce projet utilise des scripts SQL préexistants (`SGE_*.sql`) pour initialiser la base de données PostgreSQL. L'application ne fait plus d'initialisation automatique pour éviter les erreurs d'encodage.

## 📁 Fichiers SGE disponibles

- **`SGE_CRE.sql`** - Crée le schéma et toutes les tables
- **`SGE_JEU.sql`** - Insère les données de test
- **`SGE_DROP.sql`** - Supprime les tables existantes
- **`SGE_INV.sql`** - Scripts d'inventaire
- **`SGE_RESQ.sql`** - Scripts de requêtes

## 🚀 Initialisation rapide

### Option 1: Script automatique (Recommandé)

```bash
python init_sge_database.py
```

Ce script exécute automatiquement les fichiers dans le bon ordre :
1. `SGE_DROP.sql` - Nettoie l'existant
2. `SGE_CRE.sql` - Crée la structure
3. `SGE_JEU.sql` - Insère les données

### Option 2: Manuel avec psql

```bash
# 1. Supprimer l'existant
psql -U postgres -d postgres -f SGE_DROP.sql

# 2. Créer la structure
psql -U postgres -d postgres -f SGE_CRE.sql

# 3. Insérer les données
psql -U postgres -d postgres -f SGE_JEU.sql
```

## 🔧 Paramètres de connexion

Les scripts utilisent ces paramètres par défaut :
- **Base de données**: `postgres`
- **Utilisateur**: `postgres`
- **Mot de passe**: `postgres123`
- **Hôte**: `localhost`
- **Port**: `5432`

Si vos paramètres sont différents, modifiez le fichier `init_sge_database.py`.

## 👥 Utilisateurs de test créés

Après l'initialisation, vous pouvez vous connecter avec :

| Email | Mot de passe | Rôle |
|-------|-------------|------|
| `noelle.sielinou@sac.com` | `noelle25` | Administrateur |
| `brice.sodje@sac.com` | `brice25` | Responsable_stocks |
| `orlane.takia@sac.com` | `orlane25` | Agent_logistique |
| `pharel.ngounou@sac.com` | `pharel` | Emballeur |
| `abigael.kemoe@sac.com` | `abigael25` | Magasinier |

## 🏃‍♂️ Lancement de l'application

Une fois l'initialisation terminée :

```bash
python app.py
```

## 🔍 Vérification

Pour vérifier que tout fonctionne :

```bash
python test_complete_system.py
```

## ❗ Résolution de problèmes

### Erreur d'encodage UTF-8
- Assurez-vous que PostgreSQL est configuré pour UTF-8
- Vérifiez que les fichiers SQL sont en UTF-8

### Erreur de connexion
- Vérifiez que PostgreSQL est démarré
- Vérifiez les paramètres de connexion
- Testez avec : `python testeconnexion.py`

### Erreur de permissions
- Assurez-vous que l'utilisateur `postgres` a les droits nécessaires
- Vérifiez que la base `postgres` existe

## 📝 Notes importantes

- L'application ne fait plus d'initialisation automatique
- Les scripts SGE sont la source de vérité pour la structure de la BD
- Toujours exécuter les scripts dans l'ordre : DROP → CRE → JEU
- Les données de test sont incluses dans `SGE_JEU.sql` 