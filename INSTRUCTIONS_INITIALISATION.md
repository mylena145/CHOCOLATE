# Instructions d'Initialisation de la Base de Données

## 🎯 Objectif
Initialiser complètement la base de données PostgreSQL avec toutes les tables et données nécessaires.

## 📋 Prérequis
- PostgreSQL installé et démarré
- pgAdmin installé (ou accès à psql)

## 🔧 Étapes à Suivre

### Étape 1 : Ouvrir pgAdmin
1. Lancer pgAdmin
2. Se connecter à ton serveur PostgreSQL
3. Sélectionner la base de données `postgres`

### Étape 2 : Exécuter le script d'initialisation
1. Dans pgAdmin, cliquer sur l'icône "Query Tool" (icône avec une loupe)
2. Ouvrir le fichier `init_database_complete.sql`
3. Copier tout le contenu du fichier
4. Coller dans l'éditeur SQL de pgAdmin
5. Cliquer sur "Execute" (F5)

### Étape 3 : Vérifier l'exécution
Tu devrais voir des messages comme :
```
Base de données initialisée avec succès
nb_organisations: 5
nb_individus: 5
nb_entrepots: 5
nb_produits: 5
```

## 🚨 En cas d'erreur

### Erreur : "schema already exists"
- C'est normal, le schéma existe déjà
- Continuer l'exécution

### Erreur : "domain already exists"
- C'est normal, les domaines existent déjà
- Continuer l'exécution

### Erreur : "table already exists"
- Supprimer d'abord les tables existantes :
```sql
DROP SCHEMA sge_cre CASCADE;
```
- Puis relancer le script

## ✅ Vérification

Après l'exécution, vérifier que les tables existent :
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'sge_cre';
```

Tu devrais voir :
- organisations
- individus
- produits
- entrepots
- etc.

## 🎉 Succès

Une fois le script exécuté avec succès :
1. ✅ Toutes les tables sont créées
2. ✅ Toutes les données sont insérées
3. ✅ La base est prête pour l'application

## 📝 Prochaines étapes

1. Tester la connexion Python :
```bash
python testeconnexion.py
```

2. Lancer l'application :
```bash
python app.py
```

3. Se connecter avec :
   - Email : dupont@email.com
   - Mot de passe : 1234

---

**Note** : Si tu rencontres des erreurs spécifiques, partage-les pour une assistance ciblée. 