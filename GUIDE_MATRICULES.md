# Guide d'Utilisation - Système de Génération Automatique de Matricules

## 📋 Vue d'ensemble

Le système de génération automatique de matricules permet de créer des identifiants uniques pour chaque utilisateur en fonction de son rôle dans l'organisation. Chaque matricule est composé d'un préfixe de 2 lettres (identifiant le rôle) suivi d'un numéro séquentiel.

## 🎯 Fonctionnalités

### ✅ Génération Automatique
- **Préfixe basé sur le rôle** : Chaque rôle a un préfixe unique de 2 lettres
- **Numérotation séquentielle** : Les matricules sont générés automatiquement (001, 002, 003...)
- **Unicité garantie** : Aucun matricule en double n'est généré

### ✅ Identification par Matricule
- **Reconnaissance du rôle** : Les 2 premières lettres identifient le rôle
- **Validation automatique** : Vérification du format et de la cohérence
- **Gestion des erreurs** : Messages d'erreur clairs et informatifs

### ✅ Interface d'Administration
- **Onglet dédié** : Section "Matricules" dans l'interface d'administration
- **Visualisation des mappings** : Tableau des rôles et leurs préfixes
- **Statistiques d'utilisation** : Nombre d'utilisateurs par rôle
- **Outils de test** : Validation et test de matricules

## 🔤 Mapping des Rôles vers Préfixes

| Rôle | Préfixe | Exemple |
|------|---------|---------|
| **Responsable des stocks** | RS | RS001, RS002 |
| **Magasinier** | MG | MG001, MG002 |
| **Emballeur** | EM | EM001, EM002 |
| **Responsable de la logistique** | RL | RL001, RL002 |
| **Agent de logistique** | AL | AL001, AL002 |
| **Livreur** | LV | LV001, LV002 |
| **Responsable informatique** | RI | RI001, RI002 |
| **Technicien informatique** | TI | TI001, TI002 |
| **Responsable de la sécurité physique** | RP | RP001, RP002 |
| **Garde de sécurité** | GS | GS001, GS002 |
| **Super Administrateur** | SA | SA001, SA002 |
| **Administrateur** | AD | AD001, AD002 |
| **Gestionnaire Entrepôt** | GE | GE001, GE002 |
| **Consultant** | CO | CO001, CO002 |
| **Stagiaire** | ST | ST001, ST002 |
| **Fournisseur** | FR | FR001, FR002 |
| **Client** | CL | CL001, CL002 |

## 🚀 Utilisation

### 1. Création d'un Nouvel Utilisateur

1. **Accéder à l'administration** : Menu → Administration
2. **Onglet Utilisateurs** : Cliquer sur "👥 Utilisateurs"
3. **Nouvel utilisateur** : Cliquer sur "➕ Nouvel utilisateur"
4. **Sélectionner le rôle** : Choisir le rôle dans la liste déroulante
5. **Matricule automatique** : Le matricule est généré automatiquement
6. **Validation** : Le système vérifie l'unicité et la cohérence

### 2. Modification d'un Utilisateur

1. **Éditer l'utilisateur** : Cliquer sur "✏️" dans la liste
2. **Changer le rôle** : Le matricule peut être mis à jour automatiquement
3. **Validation** : Le système vérifie la cohérence rôle/matricule

### 3. Consultation des Matricules

1. **Onglet Matricules** : Cliquer sur "🆔 Matricules"
2. **Mapping des rôles** : Voir tous les préfixes et exemples
3. **Statistiques** : Consulter l'utilisation par rôle
4. **Outils de test** : Valider des matricules manuellement

## 🔧 Outils de Validation

### Test de Matricule
- **Format** : 2 lettres + 3-8 chiffres (ex: AD001)
- **Validation** : Vérification automatique du format
- **Identification** : Reconnaissance du rôle correspondant

### Exemples de Validation
```
✅ AD001 → Administrateur
✅ LV002 → Livreur
✅ MG003 → Magasinier
❌ INVALID → Format invalide
❌ A1 → Trop court
❌ AD123456789 → Trop long
```

## 📊 Statistiques et Monitoring

### Informations Disponibles
- **Nombre d'utilisateurs par rôle**
- **Matricules existants par rôle**
- **Utilisation des préfixes**
- **Tendances d'attribution**

### Accès aux Statistiques
1. **Onglet Matricules** → Section "📊 Statistiques d'Utilisation"
2. **Rafraîchissement** : Bouton "🔄 Rafraîchir"
3. **Export** : Possibilité d'exporter les données

## 🛠️ Fonctions Techniques

### Génération de Matricule
```python
from matricule_manager import MatriculeManager

# Générer un matricule pour un rôle
matricule = MatriculeManager.generate_matricule("Livreur")
# Résultat: LV001 (ou le prochain disponible)
```

### Identification de Rôle
```python
# Identifier le rôle d'un matricule
role = MatriculeManager.get_role_from_matricule("AD001")
# Résultat: "Administrateur"
```

### Validation
```python
# Valider un matricule
is_valid, message = MatriculeManager.validate_matricule("AD001")
# Résultat: (True, "") si valide
```

## ⚠️ Règles et Contraintes

### Format des Matricules
- **Longueur** : 5 à 10 caractères
- **Structure** : 2 lettres majuscules + chiffres
- **Exemple** : AD001, LV002, MG003

### Contraintes
- **Unicité** : Aucun matricule en double
- **Cohérence** : Le matricule doit correspondre au rôle
- **Validation** : Format strict obligatoire

### Gestion des Erreurs
- **Matricule déjà utilisé** : Génération du suivant
- **Format invalide** : Message d'erreur explicite
- **Rôle non reconnu** : Utilisation du préfixe par défaut (US)

## 🔄 Maintenance

### Ajout d'un Nouveau Rôle
1. **Modifier le mapping** : Ajouter dans `MatriculeManager.ROLE_PREFIXES`
2. **Préfixe unique** : S'assurer qu'il n'existe pas déjà
3. **Test** : Vérifier la génération et l'identification

### Migration des Données
- **Matricules existants** : Compatibles avec le nouveau système
- **Rôles non mappés** : Utilisation du préfixe par défaut
- **Validation** : Vérification de la cohérence

## 📝 Exemples d'Utilisation

### Scénario 1 : Nouveau Livreur
```
Rôle sélectionné: Livreur
Préfixe généré: LV
Matricule créé: LV001
Validation: ✅ Cohérent
```

### Scénario 2 : Administrateur
```
Rôle sélectionné: Administrateur
Préfixe généré: AD
Matricule créé: AD002 (si AD001 existe déjà)
Validation: ✅ Cohérent
```

### Scénario 3 : Rôle Personnalisé
```
Rôle sélectionné: Responsable Marketing
Préfixe généré: RM (2 premières lettres)
Matricule créé: RM001
Validation: ✅ Format valide
```

## 🆘 Dépannage

### Problèmes Courants

**Q: Le matricule n'est pas généré automatiquement**
A: Vérifier que le rôle est sélectionné et que la base de données est accessible

**Q: Erreur "Matricule déjà utilisé"**
A: Le système génère automatiquement le suivant disponible

**Q: "Format invalide" lors de la validation**
A: Vérifier que le matricule suit le format XX001 (2 lettres + chiffres)

**Q: Rôle non reconnu**
A: Le rôle n'est pas dans le mapping, utilisation du préfixe par défaut

### Support Technique
- **Logs** : Vérifier les logs d'erreur
- **Base de données** : Contrôler la connexion PostgreSQL
- **Permissions** : S'assurer des droits d'accès

## 📈 Évolutions Futures

### Fonctionnalités Prévues
- **Génération par lot** : Création multiple d'utilisateurs
- **Import/Export** : Gestion des matricules en masse
- **Historique** : Suivi des modifications de matricules
- **API** : Interface programmatique pour les intégrations

### Améliorations
- **Préfixes personnalisables** : Configuration par organisation
- **Validation avancée** : Règles métier spécifiques
- **Notifications** : Alertes sur les attributions
- **Audit** : Traçabilité complète des opérations 