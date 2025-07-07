# Guide Complet de Résolution - Système de Gestion d'Entrepôts

## 🎯 Objectif
Résoudre tous les problèmes de base de données et de connexion pour que ton application fonctionne correctement.

## 📋 Problèmes Identifiés

### 1. Problème d'encodage UTF-8 avec PostgreSQL
**Symptôme** : `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9`

### 2. Problème de domaine id_lettre trop restrictif
**Symptôme** : `la valeur pour le domaine sge_cre.id_lettre viole la contrainte de vérification`

### 3. Problème de connexion à la base de données
**Symptôme** : L'application ne peut pas se connecter à PostgreSQL

## 🔧 Solutions

### Étape 1 : Résoudre le problème d'encodage

#### Solution A : Modifier les paramètres de connexion
Dans `database.py`, essayer cette configuration :

```python
PG_CONN = dict(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432",
    client_encoding="utf8",
    options="-c client_encoding=utf8",
    connect_timeout=10
)
```

#### Solution B : Utiliser une chaîne de connexion
```python
PG_CONN = "postgresql://postgres:1234@localhost:5432/postgres?client_encoding=utf8"
```

#### Solution C : Vérifier PostgreSQL
1. Ouvrir pgAdmin
2. Se connecter à ta base
3. Exécuter : `SHOW SERVER_ENCODING;`
4. Si ce n'est pas UTF8, modifier la configuration PostgreSQL

### Étape 2 : Corriger le domaine id_lettre

#### Exécuter le script de correction
1. Ouvrir pgAdmin ou psql
2. Exécuter le contenu de `fix_domain.sql` :
```sql
DROP DOMAIN IF EXISTS sge_cre.id_lettre CASCADE;
CREATE DOMAIN sge_cre.id_lettre AS VARCHAR(10) 
  CHECK (VALUE ~ '^[A-Z0-9]{1,10}$');
```

### Étape 3 : Insérer les données

#### Exécuter le script d'insertion
1. Dans pgAdmin ou psql
2. Exécuter le contenu de `insert_data.sql`

### Étape 4 : Tester la connexion

#### Test simple
```bash
python testeconnexion.py
```

#### Test complet
```bash
python test_connections.py
```

## 🚀 Instructions Détaillées

### 1. Préparer la base de données

#### Option A : Avec pgAdmin
1. Ouvrir pgAdmin
2. Se connecter à ta base PostgreSQL
3. Ouvrir l'éditeur SQL
4. Copier-coller le contenu de `fix_domain.sql`
5. Exécuter
6. Copier-coller le contenu de `insert_data.sql`
7. Exécuter

#### Option B : Avec psql (si disponible)
```bash
psql -h localhost -U postgres -d postgres -f fix_domain.sql
psql -h localhost -U postgres -d postgres -f insert_data.sql
```

### 2. Tester la connexion Python

#### Modifier database.py
```python
# Paramètres de connexion PostgreSQL
PG_CONN = dict(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432",
    client_encoding="utf8",
    options="-c client_encoding=utf8",
    connect_timeout=10
)
```

#### Réactiver l'initialisation
Dans `database.py`, décommenter :
```python
# Initialisation automatique si besoin
init_database()
init_movements_tables()
```

### 3. Lancer l'application

```bash
python app.py
```

## 📊 Tests de Validation

### Test 1 : Connexion à la base
```bash
python testeconnexion.py
```
**Résultat attendu** : "Connexion OK"

### Test 2 : Fonctions backend
```bash
python test_connections.py
```
**Résultat attendu** : Tous les tests passent

### Test 3 : Application complète
```bash
python app.py
```
**Résultat attendu** : L'application se lance sans erreur

## 🚨 Résolution des Problèmes Persistants

### Si l'erreur d'encodage persiste

#### Vérifier PostgreSQL
1. Ouvrir les Services Windows
2. Chercher "PostgreSQL"
3. Redémarrer le service

#### Vérifier la configuration
1. Dans pgAdmin, exécuter :
```sql
SHOW SERVER_ENCODING;
SHOW CLIENT_ENCODING;
```

#### Réinstaller psycopg2
```bash
pip uninstall psycopg2
pip install psycopg2-binary
```

### Si les données ne s'insèrent pas

#### Vérifier les contraintes
```sql
SELECT * FROM information_schema.table_constraints 
WHERE table_schema = 'sge_cre';
```

#### Vérifier les domaines
```sql
SELECT * FROM information_schema.domains 
WHERE domain_schema = 'sge_cre';
```

## 🎉 Succès

Une fois tous les tests passés :
1. ✅ Base de données accessible
2. ✅ Données insérées
3. ✅ Application fonctionnelle
4. ✅ Frontend connecté au backend

## 📞 Support

En cas de problème :
1. Vérifier les logs PostgreSQL
2. Vérifier les logs Python
3. Tester avec pgAdmin
4. Vérifier la configuration réseau

---

**Note** : Ce guide résout les problèmes principaux. Si tu rencontres d'autres erreurs spécifiques, partage-les pour une assistance ciblée. 