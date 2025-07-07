-- =============================================
-- SCHEMA : Systeme de Gestion d'Entrepot (SGE)
-- Version : 1.1 corrigée
-- =============================================

-- Suppression et création du schema
DROP SCHEMA IF EXISTS sge_cre CASCADE;
CREATE SCHEMA sge_cre;
SET search_path TO sge_cre;

-- Configuration des permissions
GRANT USAGE ON SCHEMA sge_cre TO PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA sge_cre 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO PUBLIC;

-- =============================================
-- SECTION 1 : DEFINITION DES DOMAINES
-- =============================================

CREATE DOMAIN type_org AS VARCHAR(30)
  CHECK (VALUE IN ('Fournisseur', 'Transporteur', 'Destinataire'));

CREATE DOMAIN type_exception AS VARCHAR(30)
  CHECK (VALUE IN ('Ecarts', 'Erreurs', 'Retards', 'Incidents'));

CREATE DOMAIN adresse AS TEXT
  CHECK (char_length(VALUE) BETWEEN 1 AND 50);

CREATE DOMAIN keyword AS VARCHAR(15)
  CHECK (
  LENGTH(VALUE) >= 4 AND LENGTH(VALUE) <= 15 AND
  VALUE ~* '^[a-z0-9]+$'
);

CREATE DOMAIN numero AS VARCHAR(9)
  CHECK (VALUE ~ '^[0-9]{9}$');

CREATE DOMAIN role_ind AS VARCHAR(30)
  CHECK (VALUE IN (
    'Responsable_stocks', 'Magasinier', 'Emballeur',
    'Agent_logistique', 'Livreur', 'Responsable_informatique',
    'Technicien_informatique', 'Administrateur', 'Responsable_securite_physique', 'Fournisseur', 'Client'
  ));

CREATE DOMAIN id_lettre AS VARCHAR(6)
  CHECK (VALUE ~ '^[A-Z]{6}$');

CREATE DOMAIN description AS TEXT
  CHECK (char_length(VALUE) BETWEEN 1 AND 300);

CREATE DOMAIN id_prod AS VARCHAR(4)
  CHECK (VALUE ~ '^[A-Z0-9]{4}$');


CREATE DOMAIN license AS VARCHAR(20)
  CHECK (VALUE IN ('Opensource', 'Proprietaire'));

CREATE DOMAIN type_em AS VARCHAR(20)
  CHECK (VALUE IN ('Boite', 'Adhesive', 'Bourrage', 'Autre'));

CREATE DOMAIN etat_em AS VARCHAR(20)
  CHECK (VALUE IN ('Neuf', 'Recupere'));

CREATE DOMAIN statut AS VARCHAR(30)
  CHECK (VALUE IN ('en_attente', 'expedie', 'recu', 'annule'));


-- 1. Supprimer l'ancien domaine (cascade pour supprimer les dépendances)
DROP DOMAIN IF EXISTS sge_cre.id_lettre CASCADE;

-- 2. Créer un nouveau domaine plus flexible
CREATE DOMAIN sge_cre.id_lettre AS VARCHAR(10) 
  CHECK (VALUE ~ '^[A-Z0-9]{1,10}$');

-- 3. Vérifier que le nouveau domaine fonctionne
SELECT 'Domaine id_lettre modifié avec succès' AS message;

-- =============================================
-- SECTION 2 : CREATION DES TABLES PRINCIPALES
-- =============================================

CREATE TABLE organisations (
  id_organisation  id_lettre PRIMARY KEY,
  nom VARCHAR(50) NOT NULL,
  adresse adresse NOT NULL,
  telephone VARCHAR(20) NOT NULL,
  statut type_org  NULL,
  nbr_entrepot INT,
  date_creation TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  date_maj TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE individus (
  id_individu SERIAL PRIMARY KEY,
  nom VARCHAR(50) NOT NULL,
  password VARCHAR(15) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  adresse VARCHAR(50) NOT NULL,
  prenom  VARCHAR(50) NOT NULL,
  role role_ind NOT NULL,
  telephone VARCHAR(20),
  matricule VARCHAR(10)
);

CREATE TABLE magasiniers (
  id_magasinier SERIAL PRIMARY KEY,
  id_individu INT UNIQUE,
  FOREIGN KEY (id_individu) REFERENCES individus(id_individu) ON DELETE CASCADE
);

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE repertoire (
  id_organisation id_lettre NOT NULL,
  id_individu INT NOT NULL,
  date_ajout DATE DEFAULT CURRENT_DATE,
  PRIMARY KEY (id_organisation, id_individu),
  FOREIGN KEY (id_organisation) REFERENCES organisations(id_organisation) ON DELETE CASCADE,
  FOREIGN KEY (id_individu) REFERENCES individus(id_individu) ON DELETE CASCADE
);

CREATE TABLE produits (
  id_produit id_prod PRIMARY KEY,
  nom VARCHAR(50) NOT NULL,
  description description,
  marque VARCHAR(50) NOT NULL,
  modele VARCHAR(50) NOT NULL,
  fournisseur VARCHAR(50) ,
  date_fabrique DATE NOT NULL,
  date_peremption DATE NOT NULL,
  stock INT NOT NULL,
  alert INT NOT NULL,
  CONSTRAINT valid_dates CHECK (date_peremption > date_fabrique)
);

CREATE TABLE receptions (
  id_reception SERIAL PRIMARY KEY,
  date_reception TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  statut VARCHAR(20) DEFAULT 'en_cours'
);

CREATE TABLE cellules (
  id_cellule id_prod PRIMARY KEY,
  longueur DECIMAL(6,2) NOT NULL,
  largeur DECIMAL(6,2) NOT NULL,
  hauteur DECIMAL(6,2) NOT NULL,
  masse_maximale DECIMAL(6,2) NOT NULL
);

CREATE TABLE entrepots (
  id_entrepot id_lettre PRIMARY KEY,
  id_organisation id_lettre,
  nom_organisation VARCHAR(50) NOT NULL,
  capacite INT NOT NULL,
  stockage VARCHAR(55),
  emplacement VARCHAR(25) NOT NULL,
  FOREIGN KEY (id_organisation) REFERENCES organisations(id_organisation) ON DELETE CASCADE
);

CREATE TABLE zone_stockage (
  id_zo_stock SERIAL PRIMARY KEY,
  id_entrepot id_lettre NOT NULL,
  id_cellule id_prod NOT NULL,
  e1 VARCHAR(40) NOT NULL,
  e2 VARCHAR(40) NOT NULL,
  e3 VARCHAR(40) NOT NULL,
  FOREIGN KEY (id_cellule) REFERENCES cellules(id_cellule) ON DELETE CASCADE,
  FOREIGN KEY (id_entrepot) REFERENCES entrepots(id_entrepot) ON DELETE CASCADE
);

CREATE TABLE colis (
  id_colis SERIAL PRIMARY KEY,
  id_zo_stock INT,
  id_reception INT,
  dimension DECIMAL(6,2) NOT NULL,
  poids DECIMAL(6,2) NOT NULL,
  emplacement VARCHAR(20) NOT NULL,
  FOREIGN KEY (id_zo_stock) REFERENCES zone_stockage(id_zo_stock) ON DELETE CASCADE,
  FOREIGN KEY (id_reception) REFERENCES receptions(id_reception) ON DELETE CASCADE
);

CREATE TABLE lots (
  id_lot VARCHAR(6) PRIMARY KEY,
  id_produit id_prod NOT NULL,
  fournisseur VARCHAR(50) NOT NULL,
  date_reception DATE,
  date_expedition DATE,
  quantite INT NOT NULL,
  description description,
  FOREIGN KEY (id_produit) REFERENCES produits(id_produit) ON DELETE CASCADE
);

CREATE TABLE bon_receptions (
  id_bon_reception SERIAL PRIMARY KEY,
  id_reception INT,
  id_magasinier INT,
  date_reception DATE NOT NULL,
  observation description,
  fournisseur VARCHAR(50),
  liste_articles_recu TEXT,
  reference_commande id_prod NOT NULL UNIQUE,
  FOREIGN KEY (id_reception) REFERENCES receptions(id_reception) ON DELETE SET NULL,
  FOREIGN KEY (id_magasinier) REFERENCES individus(id_individu) ON DELETE SET NULL
);

CREATE TABLE materiel_emballage(
  id_emballeur  SERIAL PRIMARY KEY,
  type_emballage type_em NOT NULL,
  etat_emballage etat_em NOT NULL
);

CREATE TABLE commandes(
  id_commandes VARCHAR(5) PRIMARY KEY,
  quantite INT NOT NULL, 
  prix_unitaire DECIMAL(10,2) NOT NULL
);

CREATE TABLE commandes_achats(
  id_commande VARCHAR(5) PRIMARY KEY,
  date_commande DATE NOT NULL, 
  statut VARCHAR(20),
  quantite INT NOT NULL,
  FOREIGN KEY (id_commande) REFERENCES commandes(id_commandes) ON DELETE CASCADE
);

CREATE TABLE commandes_vends(
  id_commande VARCHAR(5) PRIMARY KEY,
  date_commande DATE NOT NULL,
  statut VARCHAR(20),
  quantite INT NOT NULL,
  FOREIGN KEY (id_commande) REFERENCES commandes(id_commandes) ON DELETE CASCADE
);

CREATE TABLE bon_expeditions (
  id_bon_expedition SERIAL PRIMARY KEY,
  id_colis INT,
  client VARCHAR(50),
  reference_commande id_prod NOT NULL UNIQUE,
  date_livraison DATE NOT NULL,
  observation description,
  liste_articles_livres TEXT,
  transporteurs VARCHAR(50) NOT NULL,
  FOREIGN KEY (id_colis) REFERENCES colis(id_colis) ON DELETE SET NULL
);

CREATE TABLE rapports_exceptions (
  id_rapport SERIAL PRIMARY KEY,
  id_bon_reception INT,
  id_produit id_prod,
  id_individu INT,
  date DATE,
  type_exception type_exception NOT NULL,
  processus_concerne VARCHAR(50) NOT NULL,
  produit_concerne VARCHAR(50) NOT NULL,
  observation description,
  detecteur VARCHAR(50) NOT NULL,
  action_entreprise description NOT NULL,
  FOREIGN KEY (id_individu) REFERENCES individus(id_individu) ON DELETE SET NULL,
  FOREIGN KEY (id_produit) REFERENCES produits(id_produit) ON DELETE SET NULL,
  FOREIGN KEY (id_bon_reception) REFERENCES bon_receptions(id_bon_reception) ON DELETE SET NULL
);

-- =============================================
-- SECTION 3 : INDEX ET VUES
-- =============================================

CREATE INDEX idx_produits_nom ON produits(nom);
CREATE INDEX idx_individus_email ON individus(email);

-- VUE : individus et organisations
CREATE VIEW individus_organisations AS
SELECT 
  i.id_individu,
  i.nom AS nom_individu,
  i.prenom,
  i.email,
  o.id_organisation,
  o.nom AS organisation,
  o.statut AS type_organisation
FROM sge_cre.individus i
JOIN sge_cre.repertoire r ON i.id_individu = r.id_individu
JOIN sge_cre.organisations o ON o.id_organisation = r.id_organisation;

-- =============================================
-- SECTION 4 : VERIFICATIONS
-- =============================================

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'sge_cre' AND tablename = 'organisations') THEN
    RAISE EXCEPTION 'Table organisations manquante';
  END IF;
  
  IF (SELECT COUNT(*) FROM individus) < 1 THEN
    RAISE NOTICE 'Aucun individu inséré';
  END IF;
END $$;

COMMENT ON SCHEMA sge_cre IS 'Schema pour le systeme de gestion d''entrepot';
