# 🚀 Guide d'Utilisation du Système CRUD CLI

## 📋 Vue d'ensemble

Le système CRUD (Create, Read, Update, Delete) du CLI permet d'effectuer des opérations complètes sur la base de données directement depuis l'interface d'administration. Toutes les modifications sont persistantes et actualisent automatiquement les interfaces.

## 🎯 Fonctionnalités Principales

### ✅ Opérations CRUD Complètes
- **Création** : Ajout d'utilisateurs et produits
- **Lecture** : Consultation et recherche de données
- **Modification** : Mise à jour des informations
- **Suppression** : Suppression d'enregistrements

### 🔄 Actualisation Automatique
- Mise à jour immédiate des statistiques
- Rafraîchissement des listes d'utilisateurs
- Actualisation du journal d'activité
- Mise à jour des matricules

### 📊 Logs d'Activité
- Enregistrement automatique de toutes les actions
- Traçabilité complète des modifications
- Historique détaillé des opérations

## 💻 Commandes CLI Disponibles

### 👥 Gestion des Utilisateurs

#### Ajouter un utilisateur
```bash
user add <nom> <prenom> <email> <role>
```
**Exemple :**
```bash
user add Dupont Jean jean.dupont@example.com Magasinier
```

#### Supprimer un utilisateur
```bash
user del <email>
```
**Exemple :**
```bash
user del jean.dupont@example.com
```

#### Modifier un utilisateur
```bash
user mod <email> <champ> <valeur>
```
**Exemples :**
```bash
user mod jean.dupont@example.com role Responsable des stocks
user mod jean.dupont@example.com actif false
```

#### Lister tous les utilisateurs
```bash
user list
```

#### Rechercher un utilisateur
```bash
user search <terme>
```
**Exemple :**
```bash
user search Dupont
```

### 📦 Gestion des Produits

#### Ajouter un produit
```bash
product add <nom> <description> <prix>
```
**Exemple :**
```bash
product add "Chocolat Noir" "Chocolat noir 70% cacao" 12.99
```

#### Supprimer un produit
```bash
product del <nom>
```
**Exemple :**
```bash
product del "Chocolat Noir"
```

#### Modifier un produit
```bash
product mod <nom> <champ> <valeur>
```
**Exemples :**
```bash
product mod "Chocolat Noir" prix 14.99
product mod "Chocolat Noir" stock_disponible 150
```

#### Lister tous les produits
```bash
product list
```

#### Rechercher un produit
```bash
product search <terme>
```
**Exemple :**
```bash
product search chocolat
```

### 📊 Rapports et Statistiques

#### Rapport des utilisateurs
```bash
report users
```

#### Rapport des produits
```bash
report products
```

#### Rapport des mouvements
```bash
report movements
```

#### Rapport des emballages
```bash
report packaging
```

### 📤 Exports de Données

#### Exporter les utilisateurs
```bash
export users [format]
```
**Formats disponibles :** csv, json
**Exemples :**
```bash
export users csv
export users json
```

#### Exporter les produits
```bash
export products [format]
```

#### Exporter les mouvements
```bash
export movements [format]
```

#### Exporter les emballages
```bash
export packaging [format]
```

### 📥 Téléchargements

#### Télécharger un bon d'expédition
```bash
download expedition <id>
```

#### Télécharger un bon de réception
```bash
download reception <id>
```

### 🔧 Commandes Système

#### Afficher l'aide
```bash
help
help user
help product
help report
help export
help download
```

#### Statut du système
```bash
status
```

#### Effacer l'écran
```bash
clear
```

#### Date et heure
```bash
date
```

## 🛡️ Sécurité et Validation

### ✅ Validations Automatiques
- **Email unique** : Vérification de l'unicité des emails
- **Champs obligatoires** : Validation des données requises
- **Format des données** : Vérification des types de données
- **Permissions** : Contrôle des champs modifiables

### 🔒 Champs Modifiables
**Utilisateurs :**
- nom, prenom, email, role, actif, adresse, telephone

**Produits :**
- nom, description, prix, stock_disponible, categorie, fournisseur

### ⚠️ Messages d'Erreur
Le système affiche des messages d'erreur clairs :
- ❌ Email déjà existant
- ❌ Produit non trouvé
- ❌ Champ non autorisé
- ❌ Format invalide

## 📁 Structure des Fichiers

### Exports
Les fichiers d'export sont créés dans le dossier `exports/` :
```
exports/
├── users_20241201_143022.csv
├── products_20241201_143045.json
├── movements_20241201_143108.csv
└── packaging_20241201_143125.json
```

### Téléchargements
Les documents sont créés dans le dossier `downloads/` :
```
downloads/
├── bon_expedition_123_20241201_143022.txt
└── bon_reception_456_20241201_143045.txt
```

## 🔄 Actualisation des Interfaces

### Automatique
Après chaque opération CRUD, les interfaces suivantes sont automatiquement actualisées :
- 📊 Statistiques en temps réel
- 👥 Liste des utilisateurs
- 📝 Journal d'activité
- 🆔 Gestion des matricules

### Manuel
Vous pouvez aussi rafraîchir manuellement :
- Bouton "🔄 Rafraîchir" dans l'onglet Matricules
- Recherche en temps réel dans l'onglet Utilisateurs
- Mise à jour automatique toutes les 30 secondes pour les statistiques

## 🧪 Tests et Validation

### Script de Test
Exécutez le script de test pour vérifier le bon fonctionnement :
```bash
python test_crud_cli.py
```

### Vérifications
Le script teste :
- ✅ Connexion à la base de données
- ✅ Opérations CRUD utilisateurs
- ✅ Opérations CRUD produits
- ✅ Logs d'audit
- ✅ Génération de matricules

## 🎨 Interface Utilisateur

### Terminal CLI
- **Design moderne** : Interface sombre avec couleurs
- **Auto-complétion** : Suggestions de commandes
- **Historique** : Navigation dans les commandes précédentes
- **Messages colorés** : Feedback visuel des opérations

### Modales d'Administration
- **Validation en temps réel** : Messages d'erreur instantanés
- **Champs obligatoires** : Astérisques rouges
- **Boutons d'action** : Couleurs distinctives (vert/rouge)
- **Animations** : Transitions fluides

## 📈 Avantages du Système

### 🔄 Persistance des Données
- Toutes les modifications sont sauvegardées en base
- Pas de perte de données lors des redémarrages
- Cohérence garantie entre les interfaces

### ⚡ Performance
- Opérations rapides et efficaces
- Actualisation optimisée des interfaces
- Requêtes SQL optimisées

### 🛡️ Fiabilité
- Gestion d'erreurs complète
- Validation des données
- Logs d'audit détaillés

### 🎯 Facilité d'Utilisation
- Interface intuitive
- Commandes simples et logiques
- Aide contextuelle disponible

## 🚀 Prochaines Étapes

### Améliorations Futures
- [ ] Interface graphique pour les exports
- [ ] Rapports PDF automatiques
- [ ] Notifications par email
- [ ] Sauvegarde automatique
- [ ] Mode batch pour les opérations multiples

### Intégrations
- [ ] API REST pour les opérations externes
- [ ] Webhooks pour les notifications
- [ ] Synchronisation avec d'autres systèmes
- [ ] Import de données en masse

---

## 📞 Support

Pour toute question ou problème :
1. Consultez les logs d'activité dans l'onglet "Journal d'Activité"
2. Vérifiez la connexion à la base de données
3. Exécutez le script de test pour diagnostiquer les problèmes
4. Contactez l'équipe technique si nécessaire

**Le système CRUD CLI est maintenant entièrement opérationnel ! 🎉** 