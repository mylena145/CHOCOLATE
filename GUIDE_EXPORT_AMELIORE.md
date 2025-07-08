# 📊 Guide d'Export Amélioré - SGE

## 🎯 Nouvelles Fonctionnalités

### ✨ Ouverture Automatique des Fichiers
Après chaque export, le fichier s'ouvre automatiquement dans l'application par défaut de votre système :
- **Windows** : Ouverture avec l'application associée
- **macOS** : Ouverture avec l'application par défaut
- **Linux** : Ouverture avec xdg-open

### 🎨 Formatage Amélioré

#### 📄 Fichiers CSV
- **Séparateur** : Point-virgule (;) pour une meilleure compatibilité
- **En-têtes** : En majuscules avec accents
- **Séparateur visuel** : Ligne de tirets pour distinguer les en-têtes des données

#### 📊 Fichiers Excel (.xlsx)
- **En-têtes colorés** : Fond bleu avec texte blanc
- **Lignes alternées** : Fond gris clair pour une meilleure lisibilité
- **Largeur automatique** : Colonnes ajustées au contenu
- **Police** : En-têtes en gras, taille 12

#### 📋 Fichiers JSON
- **Indentation** : Format lisible avec 2 espaces
- **Caractères spéciaux** : Support complet des accents français

## 🚀 Installation des Dépendances

### Pour l'Export Excel
```bash
python install_excel_deps.py
```

Ou manuellement :
```bash
pip install pandas openpyxl xlsxwriter
```

## 📝 Commandes CLI

### Export des Utilisateurs
```bash
export users csv      # Export CSV des utilisateurs
export users xlsx     # Export Excel des utilisateurs
export users json     # Export JSON des utilisateurs
```

### Export des Produits
```bash
export products csv   # Export CSV des produits
export products xlsx  # Export Excel des produits
export products json  # Export JSON des produits
```

### Export des Mouvements
```bash
export movements csv  # Export CSV des mouvements
export movements xlsx # Export Excel des mouvements
export movements json # Export JSON des mouvements
```

### Export des Emballages
```bash
export packaging csv  # Export CSV des emballages
export packaging xlsx # Export Excel des emballages
export packaging json # Export JSON des emballages
```

## 📁 Emplacement des Fichiers

Tous les exports sont sauvegardés dans le dossier `exports/` :
```
exports/
├── users_20241201_143022.csv
├── users_20241201_143022.xlsx
├── products_20241201_143022.csv
├── movements_20241201_143022.xlsx
└── packaging_20241201_143022.json
```

## 🎨 Exemples de Formatage

### CSV - Utilisateurs
```csv
NOM;PRÉNOM;EMAIL;RÔLE;MATRICULE;ADRESSE;TÉLÉPHONE
---;---;---;---;---;---;---
Dupont;Jean;jean.dupont@email.com;Le responsable des stocks;ADM001;123 Rue de la Paix;0123456789
Martin;Marie;marie.martin@email.com;Le magasinier;MAG002;456 Avenue des Fleurs;0987654321
```

### Excel - Produits
- **En-têtes** : Fond bleu (#366092), texte blanc, centré
- **Lignes paires** : Fond gris clair (#F2F2F2)
- **Largeur** : Ajustée automatiquement au contenu

### JSON - Mouvements
```json
[
  {
    "type": "ENTRÉE",
    "quantite": 100,
    "date": "2024-12-01T14:30:22",
    "produit_id": 1,
    "entrepot_id": 1
  }
]
```

## 🔧 Dépannage

### Erreur "pandas et openpyxl requis"
```bash
# Installer les dépendances
python install_excel_deps.py
```

### Fichier ne s'ouvre pas automatiquement
- Vérifiez que vous avez une application par défaut pour le type de fichier
- Sur Windows : Associez les fichiers .xlsx à Excel
- Sur macOS : Clic droit → "Ouvrir avec" → Choisir l'application

### Problème d'encodage CSV
- Les fichiers CSV utilisent l'encodage UTF-8
- Ouvrez avec un éditeur compatible (Excel, LibreOffice, etc.)

## 📊 Statistiques d'Export

Chaque export génère :
- ✅ Message de confirmation
- 📊 Nombre d'éléments exportés
- 📁 Chemin absolu du fichier
- 🚀 Confirmation d'ouverture automatique
- 📝 Log d'activité dans l'audit

## 🎯 Bonnes Pratiques

1. **Vérifiez l'espace disque** avant les gros exports
2. **Fermez les fichiers** avant de les réexporter
3. **Utilisez Excel** pour les rapports de présentation
4. **Utilisez CSV** pour l'import dans d'autres systèmes
5. **Utilisez JSON** pour l'intégration avec des APIs

## 🔄 Mise à Jour

Les nouvelles fonctionnalités sont automatiquement disponibles après redémarrage de l'application.

---

*Dernière mise à jour : Décembre 2024* 