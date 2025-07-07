# 🔧 Guide de Correction des Contraintes de Clés Étrangères

## 📋 Problème Identifié

Vous rencontrez des erreurs de contraintes de clés étrangères lors de l'insertion de données :

```
ERROR: une instruction insert ou update sur la table « colis » viole la contrainte de clé
étrangère « colis_id_zo_stock_fkey »
La clé (id_zo_stock)=(1) n'est pas présente dans la table « zone_stockage ».
```

## 🔍 Causes du Problème

1. **Ordre d'insertion incorrect** : Les tables avec des clés étrangères sont insérées avant les tables référencées
2. **IDs auto-incrémentés** : Les scripts utilisent des IDs fixes (1, 2, 3...) au lieu de laisser PostgreSQL générer les IDs
3. **Séquences non réinitialisées** : Les compteurs d'auto-increment ne sont pas remis à zéro

## ✅ Solution Complète

### Étape 1 : Exécuter le Script de Correction

```bash
python fix_database.py
```

Ce script va :
- Nettoyer toutes les tables existantes
- Réinitialiser les séquences d'auto-increment
- Insérer les données dans le bon ordre
- Vérifier l'intégrité des contraintes

### Étape 2 : Vérification Manuelle (Optionnel)

Si vous préférez exécuter le script SQL directement :

```sql
-- Dans pgAdmin ou psql
\i fix_database_constraints.sql
```

## 📊 Ordre d'Insertion Correct

Le script respecte cet ordre pour éviter les violations de contraintes :

1. **Tables sans dépendances** :
   - `organisations`
   - `individus`
   - `produits`
   - `receptions`
   - `cellules`
   - `materiel_emballage`
   - `commandes`

2. **Tables avec dépendances simples** :
   - `repertoire` (dépend de `organisations` et `individus`)
   - `entrepots` (dépend de `organisations`)

3. **Tables avec dépendances complexes** :
   - `zone_stockage` (dépend de `entrepots` et `cellules`)
   - `colis` (dépend de `zone_stockage` et `receptions`)
   - `lots` (dépend de `produits`)
   - `commandes_achats` (dépend de `commandes`)
   - `commandes_vends` (dépend de `commandes`)

## 🔗 Contraintes de Clés Étrangères Vérifiées

Le script vérifie automatiquement :

- ✅ `colis.id_zo_stock` → `zone_stockage.id_zo_stock`
- ✅ `zone_stockage.id_entrepot` → `entrepots.id_entrepot`
- ✅ `zone_stockage.id_cellule` → `cellules.id_cellule`
- ✅ `lots.id_produit` → `produits.id_produit`
- ✅ `repertoire.id_organisation` → `organisations.id_organisation`
- ✅ `repertoire.id_individu` → `individus.id_individu`

## 📈 Données Insérées

Après correction, vous aurez :

- **5 organisations** (LogiPlus, TransAfrica, etc.)
- **11 individus** (Noelle, Brice, Orlane, etc.)
- **5 produits** (Clavier, SSD, Routeur, etc.)
- **5 réceptions** (dates variées)
- **5 entrepôts** (un par organisation)
- **5 cellules** (C001 à C005)
- **5 zones de stockage** (liées aux entrepôts)
- **5 colis** (avec zones et réceptions valides)
- **5 lots** (liés aux produits)
- **5 commandes** et leurs variantes

## 🚨 En Cas d'Erreur

Si le script échoue :

1. **Vérifiez la connexion** :
   ```python
   # Dans fix_database.py, modifiez PG_CONN selon votre configuration
   PG_CONN = {
       'host': 'localhost',
       'database': 'sac',
       'user': 'votre_utilisateur',
       'password': 'votre_mot_de_passe',
       'port': '5432'
   }
   ```

2. **Vérifiez les permissions** :
   ```sql
   -- L'utilisateur doit avoir les droits sur le schéma sge_cre
   GRANT ALL PRIVILEGES ON SCHEMA sge_cre TO votre_utilisateur;
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA sge_cre TO votre_utilisateur;
   ```

3. **Vérifiez l'existence des tables** :
   ```sql
   SELECT table_name FROM information_schema.tables 
   WHERE table_schema = 'sge_cre' 
   ORDER BY table_name;
   ```

## 🔄 Réinitialisation Complète

Si vous voulez tout recommencer :

```sql
-- Supprimer et recréer le schéma
DROP SCHEMA IF EXISTS sge_cre CASCADE;
CREATE SCHEMA sge_cre;

-- Puis exécuter les scripts dans l'ordre :
-- 1. SGE_CRE.sql (création des tables)
-- 2. fix_database_constraints.sql (insertion des données)
```

## 📝 Logs de Vérification

Le script affiche des logs détaillés :

```
🔧 SCRIPT DE CORRECTION DES CONTRAINTES DE CLÉS ÉTRANGÈRES
============================================================
⏰ Début: 2025-01-27 14:30:00
✅ Connexion réussie à PostgreSQL: PostgreSQL 15.1
🔄 Exécution du script: fix_database_constraints.sql
  ✅ Commande 1 exécutée
  ✅ Commande 2 exécutée
  ...
✅ Script fix_database_constraints.sql exécuté avec succès

🔍 Vérification des données insérées:
  📊 organisations: 5 enregistrements
  📊 individus: 11 enregistrements
  📊 colis: 5 enregistrements
  ...

🔗 Test des contraintes de clés étrangères:
  ✅ Colis avec zones valides: 5
  ✅ Zones avec entrepôts valides: 5
  ✅ Lots avec produits valides: 5

✅ CORRECTION TERMINÉE AVEC SUCCÈS
============================================================
🎉 Toutes les contraintes de clés étrangères ont été corrigées !
📦 Les données sont maintenant cohérentes et utilisables.
```

## 🎯 Résultat Final

Après exécution du script :
- ✅ Toutes les contraintes de clés étrangères sont respectées
- ✅ Les données sont cohérentes et utilisables
- ✅ L'application peut fonctionner normalement
- ✅ Le planning temps réel fonctionne avec les vraies données

## 📞 Support

Si vous rencontrez encore des problèmes :
1. Vérifiez les logs d'erreur détaillés
2. Assurez-vous que PostgreSQL est bien configuré
3. Vérifiez que le schéma `sge_cre` existe et contient toutes les tables 