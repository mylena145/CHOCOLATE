-- Script complet d'initialisation de la base de données
-- Exécuter ce script dans pgAdmin ou psql

-- 1. Créer le schéma
CREATE SCHEMA IF NOT EXISTS sge_cre;

-- 2. Définir les domaines
CREATE DOMAIN sge_cre.type_org AS VARCHAR(30)
  CHECK (VALUE IN ('Fournisseur', 'Transporteur', 'Destinataire', 'Client'));

CREATE DOMAIN sge_cre.type_exception AS VARCHAR(30)
  CHECK (VALUE IN ('Erreur', 'Anomalie', 'Retard', 'Perte'));

CREATE DOMAIN sge_cre.adresse AS TEXT
  CHECK (char_length(VALUE) BETWEEN 5 AND 200);

CREATE DOMAIN sge_cre.keyword AS VARCHAR(15)
  CHECK (VALUE ~ '^[A-Za-z0-9_]+$');

CREATE DOMAIN sge_cre.numero AS VARCHAR(9)
  CHECK (VALUE ~ '^[0-9]{9}$');

CREATE DOMAIN sge_cre.role_ind AS VARCHAR(30)
  CHECK (VALUE IN ('admin', 'user', 'manager', 'operator'));

-- Domaine id_lettre flexible
CREATE DOMAIN sge_cre.id_lettre AS VARCHAR(10) 
  CHECK (VALUE ~ '^[A-Z0-9]{1,10}$');

CREATE DOMAIN sge_cre.description AS TEXT
  CHECK (char_length(VALUE) BETWEEN 1 AND 300);

CREATE DOMAIN sge_cre.id_prod AS VARCHAR(4)
  CHECK (VALUE ~ '^[A-Z0-9]{4}$');

CREATE DOMAIN sge_cre.license AS VARCHAR(20)
  CHECK (VALUE IN ('Opensource', 'Proprietaire'));

CREATE DOMAIN sge_cre.type_em AS VARCHAR(20)
  CHECK (VALUE IN ('Boite', 'Adhesive', 'Bourrage', 'Autre'));

CREATE DOMAIN sge_cre.etat_em AS VARCHAR(20)
  CHECK (VALUE IN ('Neuf', 'Recupere'));

CREATE DOMAIN sge_cre.statut AS VARCHAR(30)
  CHECK (VALUE IN ('en_attente', 'expedie', 'recu', 'annule'));

-- 3. Créer les tables
CREATE TABLE sge_cre.organisations (
  id_organisation sge_cre.id_lettre PRIMARY KEY,
  nom VARCHAR(50) NOT NULL,
  adresse sge_cre.adresse NOT NULL,
  telephone VARCHAR(20) NOT NULL,
  statut sge_cre.type_org NULL,
  nbr_entrepot INT,
  date_creation TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  date_maj TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sge_cre.individus (
  id_individu SERIAL PRIMARY KEY,
  nom VARCHAR(50) NOT NULL,
  password VARCHAR(15) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  adresse VARCHAR(50) NOT NULL,
  prenom VARCHAR(50) NOT NULL,
  role sge_cre.role_ind NOT NULL,
  telephone VARCHAR(20),
  matricule VARCHAR(10)
);

CREATE TABLE sge_cre.magasiniers (
  id_magasinier SERIAL PRIMARY KEY,
  id_individu INT UNIQUE,
  FOREIGN KEY (id_individu) REFERENCES sge_cre.individus(id_individu) ON DELETE CASCADE
);

CREATE TABLE sge_cre.repertoire (
  id_organisation sge_cre.id_lettre NOT NULL,
  id_individu INT NOT NULL,
  date_ajout DATE DEFAULT CURRENT_DATE,
  PRIMARY KEY (id_organisation, id_individu),
  FOREIGN KEY (id_organisation) REFERENCES sge_cre.organisations(id_organisation) ON DELETE CASCADE,
  FOREIGN KEY (id_individu) REFERENCES sge_cre.individus(id_individu) ON DELETE CASCADE
);

CREATE TABLE sge_cre.produits (
  id_produit sge_cre.id_prod PRIMARY KEY,
  nom VARCHAR(50) NOT NULL,
  description sge_cre.description,
  marque VARCHAR(50) NOT NULL,
  modele VARCHAR(50) NOT NULL,
  fournisseur VARCHAR(50),
  date_fabrique DATE NOT NULL,
  date_peremption DATE NOT NULL,
  stock INT NOT NULL,
  alert INT NOT NULL,
  CONSTRAINT valid_dates CHECK (date_peremption > date_fabrique)
);

CREATE TABLE sge_cre.receptions (
  id_reception SERIAL PRIMARY KEY,
  date_reception TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  statut VARCHAR(20) DEFAULT 'en_cours'
);

CREATE TABLE sge_cre.cellules (
  id_cellule sge_cre.id_prod PRIMARY KEY,
  longueur DECIMAL(6,2) NOT NULL,
  largeur DECIMAL(6,2) NOT NULL,
  hauteur DECIMAL(6,2) NOT NULL,
  masse_maximale DECIMAL(6,2) NOT NULL
);

CREATE TABLE sge_cre.entrepots (
  id_entrepot sge_cre.id_lettre PRIMARY KEY,
  id_organisation sge_cre.id_lettre,
  nom_organisation VARCHAR(50) NOT NULL,
  capacite INT NOT NULL,
  stockage VARCHAR(55),
  emplacement VARCHAR(25) NOT NULL,
  FOREIGN KEY (id_organisation) REFERENCES sge_cre.organisations(id_organisation) ON DELETE CASCADE
);

CREATE TABLE sge_cre.zone_stockage (
  id_zo_stock SERIAL PRIMARY KEY,
  id_entrepot sge_cre.id_lettre NOT NULL,
  id_cellule sge_cre.id_prod NOT NULL,
  e1 VARCHAR(40) NOT NULL,
  e2 VARCHAR(40) NOT NULL,
  e3 VARCHAR(40) NOT NULL,
  FOREIGN KEY (id_cellule) REFERENCES sge_cre.cellules(id_cellule) ON DELETE CASCADE,
  FOREIGN KEY (id_entrepot) REFERENCES sge_cre.entrepots(id_entrepot) ON DELETE CASCADE
);

CREATE TABLE sge_cre.colis (
  id_colis SERIAL PRIMARY KEY,
  id_zo_stock INT,
  id_reception INT,
  dimension DECIMAL(6,2) NOT NULL,
  poids DECIMAL(6,2) NOT NULL,
  emplacement VARCHAR(20) NOT NULL,
  FOREIGN KEY (id_zo_stock) REFERENCES sge_cre.zone_stockage(id_zo_stock) ON DELETE CASCADE,
  FOREIGN KEY (id_reception) REFERENCES sge_cre.receptions(id_reception) ON DELETE CASCADE
);

CREATE TABLE sge_cre.lots (
  id_lot VARCHAR(6) PRIMARY KEY,
  id_produit sge_cre.id_prod NOT NULL,
  fournisseur VARCHAR(50) NOT NULL,
  date_reception DATE,
  date_expedition DATE,
  quantite INT NOT NULL,
  description sge_cre.description,
  FOREIGN KEY (id_produit) REFERENCES sge_cre.produits(id_produit) ON DELETE CASCADE
);

CREATE TABLE sge_cre.bon_receptions (
  id_bon_reception SERIAL PRIMARY KEY,
  id_reception INT,
  id_magasinier INT,
  date_reception DATE NOT NULL,
  observation sge_cre.description,
  fournisseur VARCHAR(50),
  liste_articles_recu TEXT,
  reference_commande sge_cre.id_prod NOT NULL UNIQUE,
  FOREIGN KEY (id_reception) REFERENCES sge_cre.receptions(id_reception) ON DELETE SET NULL,
  FOREIGN KEY (id_magasinier) REFERENCES sge_cre.individus(id_individu) ON DELETE SET NULL
);

CREATE TABLE sge_cre.materiel_emballage(
  id_emballeur SERIAL PRIMARY KEY,
  type_emballage sge_cre.type_em NOT NULL,
  etat_emballage sge_cre.etat_em NOT NULL
);

CREATE TABLE sge_cre.commandes(
  id_commandes VARCHAR(4) PRIMARY KEY,
  quantite INT NOT NULL, 
  prix_unitaire DECIMAL(10,2) NOT NULL
);

CREATE TABLE sge_cre.commandes_achats(
  id_commande VARCHAR(4) PRIMARY KEY,
  date_commande DATE NOT NULL, 
  statut VARCHAR(6),
  quantite INT NOT NULL,
  FOREIGN KEY (id_commande) REFERENCES sge_cre.commandes(id_commandes) ON DELETE CASCADE
);

CREATE TABLE sge_cre.commandes_vends(
  id_commande VARCHAR(4) PRIMARY KEY,
  date_commande DATE NOT NULL,
  statut VARCHAR(6),
  quantite INT NOT NULL,
  FOREIGN KEY (id_commande) REFERENCES sge_cre.commandes(id_commandes) ON DELETE CASCADE
);

CREATE TABLE sge_cre.bon_expeditions (
  id_bon_expedition SERIAL PRIMARY KEY,
  id_colis INT,
  client VARCHAR(50),
  reference_commande sge_cre.id_prod NOT NULL UNIQUE,
  date_livraison DATE NOT NULL,
  observation sge_cre.description,
  liste_articles_livres TEXT,
  transporteurs VARCHAR(50) NOT NULL,
  FOREIGN KEY (id_colis) REFERENCES sge_cre.colis(id_colis) ON DELETE SET NULL
);

CREATE TABLE sge_cre.rapports_exceptions (
  id_rapport SERIAL PRIMARY KEY,
  id_bon_reception INT,
  id_produit sge_cre.id_prod,
  id_individu INT,
  date DATE,
  type_exception sge_cre.type_exception NOT NULL,
  processus_concerne VARCHAR(50) NOT NULL,
  produit_concerne VARCHAR(50) NOT NULL,
  observation sge_cre.description,
  detecteur VARCHAR(50) NOT NULL,
  action_entreprise sge_cre.description NOT NULL,
  FOREIGN KEY (id_individu) REFERENCES sge_cre.individus(id_individu) ON DELETE SET NULL,
  FOREIGN KEY (id_produit) REFERENCES sge_cre.produits(id_produit) ON DELETE SET NULL,
  FOREIGN KEY (id_bon_reception) REFERENCES sge_cre.bon_receptions(id_bon_reception) ON DELETE SET NULL
);

-- 4. Créer les index
CREATE INDEX idx_produits_nom ON sge_cre.produits(nom);
CREATE INDEX idx_individus_email ON sge_cre.individus(email);

-- 5. Insérer les données de test
INSERT INTO sge_cre.organisations (id_organisation, nom, adresse, telephone, statut, nbr_entrepot) VALUES
('ORG001', 'LogiPlus', 'Zone Industrielle, Yaoundé', '699001122', 'Fournisseur', 3),
('ORG002', 'TransAfrica', 'Rue de l''Avenir, Douala', '676543210', 'Transporteur', 5),
('ORG003', 'DepotCentral', 'Quartier Mvan, Yaoundé', '690112233', 'Destinataire', 1),
('ORG004', 'Fournitech', 'Avenue Kennedy, Douala', '655009988', 'Fournisseur', 2),
('ORG005', 'DistribPlus', 'Rue 12, Garoua', '688776655', 'Fournisseur', 4);

INSERT INTO sge_cre.individus (nom, password, email, adresse, prenom, role, telephone, matricule) VALUES
('Dupont', '1234', 'dupont@email.com', 'Yaoundé', 'Jean', 'admin', '699001122', 'EMP001'),
('Martin', '1234', 'martin@email.com', 'Douala', 'Marie', 'user', '676543210', 'EMP002'),
('Durand', '1234', 'durand@email.com', 'Garoua', 'Pierre', 'user', '690112233', 'EMP003'),
('Bernard', '1234', 'bernard@email.com', 'Bafoussam', 'Sophie', 'user', '655009988', 'EMP004'),
('Petit', '1234', 'petit@email.com', 'Maroua', 'Lucas', 'user', '688776655', 'EMP005');

INSERT INTO sge_cre.repertoire (id_organisation, id_individu) VALUES
('ORG001', 1),
('ORG002', 2),
('ORG003', 3),
('ORG004', 4),
('ORG005', 5);

INSERT INTO sge_cre.entrepots (id_entrepot, id_organisation, nom_organisation, capacite, stockage, emplacement) VALUES
('ENT001', 'ORG001', 'Entrepôt LogiPlus', 5000, 'Informatique', 'Yaoundé'),
('ENT002', 'ORG002', 'Entrepôt TransAfrica', 3000, 'Transport', 'Douala'),
('ENT003', 'ORG003', 'Entrepôt DepotCentral', 2000, 'Stock général', 'Garoua'),
('ENT004', 'ORG004', 'Entrepôt Fournitech', 4000, 'Composants', 'Bafoussam'),
('ENT005', 'ORG005', 'Entrepôt DistribPlus', 2500, 'Divers', 'Maroua');

INSERT INTO sge_cre.produits (id_produit, nom, description, marque, modele, fournisseur, date_fabrique, date_peremption, stock, alert) VALUES
('PROD1', 'Ordinateur portable', 'Ordinateur portable 15 pouces', 'Dell', 'Latitude 7420', 'ORG001', '2024-01-01', '2027-01-01', 50, 10),
('PROD2', 'Souris optique', 'Souris optique sans fil', 'Logitech', 'MX Master 3', 'ORG001', '2024-01-01', '2027-01-01', 100, 20),
('PROD3', 'Clavier mécanique', 'Clavier mécanique RGB', 'Corsair', 'K70', 'ORG004', '2024-01-01', '2027-01-01', 75, 15),
('PROD4', 'Moniteur 24"', 'Moniteur Full HD 24 pouces', 'Samsung', 'LS24F350', 'ORG004', '2024-01-01', '2027-01-01', 30, 5),
('PROD5', 'Disque dur externe', 'Disque dur externe 1TB', 'Western Digital', 'My Passport', 'ORG005', '2024-01-01', '2027-01-01', 200, 40);

INSERT INTO sge_cre.cellules (id_cellule, longueur, largeur, hauteur, masse_maximale) VALUES
('CELL1', 100.00, 100.00, 100.00, 50.00),
('CELL2', 150.00, 120.00, 120.00, 75.00),
('CELL3', 200.00, 150.00, 150.00, 100.00),
('CELL4', 120.00, 100.00, 100.00, 60.00),
('CELL5', 180.00, 130.00, 130.00, 85.00);

INSERT INTO sge_cre.zone_stockage (id_entrepot, id_cellule, e1, e2, e3) VALUES
('ENT001', 'CELL1', 'Zone A', 'Rangée 1', 'Étagère 1'),
('ENT001', 'CELL2', 'Zone A', 'Rangée 1', 'Étagère 2'),
('ENT002', 'CELL3', 'Zone B', 'Rangée 2', 'Étagère 1'),
('ENT003', 'CELL4', 'Zone C', 'Rangée 1', 'Étagère 1'),
('ENT004', 'CELL5', 'Zone D', 'Rangée 1', 'Étagère 1');

-- 6. Vérification
SELECT 'Base de données initialisée avec succès' AS message;
SELECT COUNT(*) AS nb_organisations FROM sge_cre.organisations;
SELECT COUNT(*) AS nb_individus FROM sge_cre.individus;
SELECT COUNT(*) AS nb_entrepots FROM sge_cre.entrepots;
SELECT COUNT(*) AS nb_produits FROM sge_cre.produits; 