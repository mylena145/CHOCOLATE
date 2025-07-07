# Guide de Test des Connexions - Système de Gestion d'Entrepôts

## 🎯 Objectif
Vérifier que la base de données PostgreSQL, le backend Python et le frontend CustomTkinter sont correctement connectés.

## 📋 Prérequis
- Python 3.x installé
- PostgreSQL installé et démarré
- Toutes les dépendances Python installées

## 🔧 Tests à Effectuer

### 1. Test du Frontend (✅ DÉJÀ RÉUSSI)
```bash
python test_frontend_only.py
```
**Résultat attendu** : Tous les modules frontend s'importent correctement.

### 2. Test de la Base de Données PostgreSQL

#### 2.1 Vérifier que PostgreSQL est démarré
- Ouvrir les Services Windows (services.msc)
- Chercher "PostgreSQL" et vérifier qu'il est "En cours d'exécution"
- Ou utiliser pgAdmin pour se connecter

#### 2.2 Tester la connexion avec les paramètres actuels
```bash
python testeconnexion.py
```

#### 2.3 Si erreur d'encodage, essayer ces solutions :

**Solution A : Modifier les paramètres de connexion**
Dans `database.py`, essayer :
```python
PG_CONN = dict(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432",
    client_encoding="utf8",
    options="-c client_encoding=utf8"
)
```

**Solution B : Utiliser une chaîne de connexion**
```python
PG_CONN = "postgresql://postgres:1234@localhost:5432/postgres?client_encoding=utf8"
```

**Solution C : Vérifier le mot de passe PostgreSQL**
1. Ouvrir pgAdmin
2. Se connecter avec le mot de passe actuel
3. Si ça ne marche pas, réinitialiser le mot de passe :
   ```sql
   ALTER USER postgres PASSWORD '1234';
   ```

### 3. Test du Backend

#### 3.1 Réactiver l'initialisation de la base
Dans `database.py`, décommenter :
```python
# Initialisation automatique si besoin
init_database()
init_movements_tables()
```

#### 3.2 Tester les fonctions backend
```bash
python test_connections.py
```

### 4. Test de l'Application Complète

#### 4.1 Lancer l'application
```bash
python app.py
```

#### 4.2 Tests à effectuer dans l'interface :
1. **Connexion utilisateur**
   - Essayer de se connecter avec un utilisateur existant
   - Vérifier que la connexion fonctionne

2. **Navigation**
   - Tester toutes les pages du menu
   - Vérifier que les données s'affichent

3. **Fonctionnalités CRUD**
   - Ajouter un produit
   - Modifier un produit
   - Supprimer un produit
   - Vérifier que les changements persistent

## 🚨 Résolution des Problèmes

### Problème : Erreur d'encodage UTF-8
**Symptôme** : `'utf-8' codec can't decode byte 0xe9 in position 103`

**Solutions** :
1. Vérifier que PostgreSQL est configuré en UTF-8
2. Ajouter `client_encoding="utf8"` aux paramètres de connexion
3. Vérifier qu'il n'y a pas de caractères spéciaux dans les paramètres

### Problème : Connexion refusée
**Symptôme** : `connection refused` ou `timeout`

**Solutions** :
1. Vérifier que PostgreSQL est démarré
2. Vérifier le port (5432 par défaut)
3. Vérifier l'adresse IP (localhost)
4. Vérifier le pare-feu Windows

### Problème : Authentification échouée
**Symptôme** : `authentication failed`

**Solutions** :
1. Vérifier le nom d'utilisateur (postgres)
2. Vérifier le mot de passe
3. Réinitialiser le mot de passe si nécessaire

### Problème : Base de données inexistante
**Symptôme** : `database "postgres" does not exist`

**Solutions** :
1. Créer la base de données :
   ```sql
   CREATE DATABASE postgres;
   ```
2. Ou utiliser une base existante

## 📊 Checklist de Validation

- [ ] PostgreSQL est démarré
- [ ] Connexion à la base réussie
- [ ] Tables existent (produits, individus, etc.)
- [ ] Frontend s'importe correctement
- [ ] Application se lance sans erreur
- [ ] Connexion utilisateur fonctionne
- [ ] Navigation entre pages fonctionne
- [ ] CRUD des produits fonctionne
- [ ] Données persistent en base

## 🎉 Succès
Si tous les tests passent, votre système est correctement configuré et connecté !

## 📞 Support
En cas de problème persistant :
1. Vérifier les logs PostgreSQL
2. Vérifier les logs Python
3. Tester avec pgAdmin pour isoler le problème
4. Vérifier la configuration réseau/firewall 