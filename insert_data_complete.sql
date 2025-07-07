-- =============================================
-- SCRIPT D'INSERTION DE DONNÉES POUR SGE
-- Données fictives pour tests et démonstration
-- =============================================

-- Extension pour le cryptage
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Créer le schéma sge_cre s'il n'existe pas
CREATE SCHEMA IF NOT EXISTS sge_cre;

-- Insertion dans organisations
-- Vérifier les organisations existantes
SELECT * FROM sge_cre.organisations;

-- Insérer les nouvelles organisations (sans vérification de doublons)
INSERT INTO sge_cre.organisations (id_organisation, nom, adresse, telephone, statut, nbr_entrepot) VALUES
('ORG001', 'LogiPlus', 'Zone Industrielle, Yaoundé', '699001122', 'Fournisseur', 3),
('ORG002', 'TransAfrica', 'Rue de l''Avenir, Douala', '676543210', 'Transporteur', 5),
('ORG003', 'DepotCentral', 'Quartier Mvan, Yaoundé', '690112233', 'Destinataire', 1),
('ORG004', 'Fournitech', 'Avenue Kennedy, Douala', '655009988', 'Fournisseur', 2),
('ORG005', 'DistribPlus', 'Rue 12, Garoua', '688776655', 'Fournisseur', 4);

-- Vérifier le résultat
SELECT nom, statut, nbr_entrepot FROM sge_cre.organisations ORDER BY nom;

-- Insertion dans individus
INSERT INTO sge_cre.individus (nom, password, email, adresse, prenom, role, telephone, matricule) VALUES
('Noelle', 'noelle25', 'noelle.sielinou@sac.com', 'Mvan', 'sielinou', 'Administrateur', '690112233', 'MGMGT' ),
('Brice', 'brice25', 'brice.sodje@sac.com', 'Bonamoussadi', 'brice', 'Responsable_stocks', '691223344', 'MGMGR' ),
('Orlane', 'orlane25', 'orlane.takia@sac.com', 'Cité Verte', 'tiako', 'Agent_logistique', '692334455', 'MGMGZ'),
('Pharel', 'pharel', 'pharel.ngounou@sac.com', 'Akwa', 'pharel', 'Emballeur', '693445566', 'MGMGP'),
('Abigael', 'abigael25', 'abigael.kemoe@sac.com', 'Essos', 'kemoe', 'Magasinier', '694559677', 'MGMGN'),
('Roy', 'roy25', 'roy.houtento@sac.com', 'Essos', 'houtento', 'Livreur', '694599677', 'MGMGL'),
('Chris', 'chris25', 'chris.tankwa@sac.com', 'Bonaberie', 'tankwa', 'Responsable_informatique', '655556677', 'MGMGV'),
('Astrid', 'astrid25', 'astrid.soap@sac.com', 'Bonamoussadi', 'soap', 'Technicien_informatique', '684000077', 'MGMGC'),
('Antoine', 'antoine25', 'antoine.kwamou@sac.com', 'Japoma', 'kwamou', 'Fournisseur', '674000077', 'MGMGY'),
('Daniel', 'daniel', 'daniel.kwamou@sac.com', 'Yaticka', 'kwamou', 'Responsable_securite_physique', '664000077', 'MGMGW'),
('Joel', 'joel25', 'joel.ziko@sac.com', 'Yansoki', 'ziko', 'Client', '611000077', 'MGMGT');

SELECT * FROM sge_cre.individus;

-- Insertion dans repertoire (liaison individus et organisations)
INSERT INTO sge_cre.repertoire (id_organisation, id_individu) VALUES
('ORG001', 2),  -- Remplace par les vrais IDs
('ORG002', 3),
('ORG003', 4),
('ORG004', 5),
('ORG005', 6);

-- Insertion dans produits
INSERT INTO sge_cre.produits (id_produit, nom, description, marque, modele, fournisseur, date_fabrique, date_peremption, stock, alert) VALUES
('PRD1', 'Clavier mécanique', 'Clavier RGB AZERTY pour gamers', 'Logitech', 'G413', 'Logitech France', '2023-05-15', '2026-05-15', 120, 60),
('PRD2', 'Disque SSD', 'Disque SSD 1To NVMe haute vitesse', 'Samsung', 'Evo 980', 'Samsung Electronics', '2024-01-10', '2029-01-10', 40, 14),
('PRD3', 'Routeur Wi-Fi', 'Routeur Wi-Fi 6 double bande', 'TP-Link', 'Archer AX50', 'TP-Link Europe', '2023-03-20', '2028-03-20', 75, 25),
('PRD4', 'Batterie externe', 'Power bank 20000mAh avec charge rapide', 'Anker', 'PowerCore', 'AnkerTech', '2022-09-01', '2025-09-01', 15, 5),
('PRD5', 'Imprimante laser', 'Imprimante laser monochrome multifonction', 'HP', 'LaserJet MFP 137fnw', 'HP Inc.', '2023-11-05', '2027-11-05', 5, 2);

SELECT * FROM sge_cre.produits;

-- Insertion dans receptions
INSERT INTO sge_cre.receptions (date_reception) VALUES
('2025-01-10'),
('2025-01-15'),
('2025-02-03'),
('2025-02-25'),
('2025-03-12');

-- Insertion dans entrepots
INSERT INTO sge_cre.entrepots (nom_organisation, capacite, stockage, emplacement) VALUES
('Entrepôt LogiPlus', 5000, 'Informatique', 'Yaoundé'),
('Entrepôt TransAfrica', 3000, 'Transport', 'Douala'),
('Entrepôt DepotCentral', 2000, 'Stock général', 'Garoua'),
('Entrepôt Fournitech', 4000, 'Composants', 'Bafoussam'),
('Entrepôt DistribPlus', 2500, 'Divers', 'Maroua');

-- Vérifier
SELECT nom_organisation, capacite, stockage, emplacement 
FROM sge_cre.entrepots 
ORDER BY nom_organisation;

-- Insertion dans cellules
INSERT INTO sge_cre.cellules (id_cellule, longueur, largeur, hauteur, masse_maximale) VALUES
('C001', 120.5, 80.0, 60.0, 500.0),
('C002', 100.0, 75.0, 55.0, 450.0),
('C003', 150.0, 90.0, 65.0, 600.0),
('C004', 110.0, 70.0, 50.0, 400.0),
('C005', 130.0, 85.0, 70.0, 550.0);

-- Insertion dans zone_stockage
INSERT INTO sge_cre.zone_stockage (id_cellule, e1, e2, e3) VALUES
('C001', 'Zone A', 'Rayon 1', 'Étage 1'),
('C002', 'Zone A', 'Rayon 2', 'Étage 2'),
('C003', 'Zone B', 'Rayon 1', 'Étage 1'),
('C004', 'Zone B', 'Rayon 3', 'Étage 2'),
('C005', 'Zone C', 'Réserve', 'Étage 1');

-- Vérifier
SELECT id_zo_stock, id_cellule, e1, e2, e3 
FROM sge_cre.zone_stockage 
ORDER BY id_cellule;

-- Insertion dans colis
INSERT INTO sge_cre.colis (id_zo_stock, id_reception, dimension, poids, emplacement) VALUES
(2, 1, 50.0, 5.5, 'R1-E1'),
(3, 2, 60.0, 6.0, 'R1-E2'),
(4, 3, 55.0, 7.0, 'R2-E1'),
(5, 4, 65.0, 6.5, 'R2-E2'),
(6, 5, 70.0, 8.0, 'R3-E1');

-- Insertion dans lots
INSERT INTO sge_cre.lots (id_lot, id_produit, fournisseur, date_reception, date_expedition, quantite, description) VALUES
('LOT01', 'PRD1', 'LogiPlus', '2025-01-10', '2025-01-20', 100, 'Lot de clés USB'),
('LOT02', 'PRD2', 'Fournitech', '2025-01-15', '2025-01-25', 50, 'Lot de disques durs'),
('LOT03', 'PRD3', 'LogiPlus', '2025-02-03', '2025-02-10', 75, 'Lot decrans'),
('LOT04', 'PRD4', 'DistribPlus', '2025-02-25', '2025-03-05', 60, 'Lot dimprimantes'),
('LOT05', 'PRD5', 'DistribPlus', '2025-03-12', '2025-03-20', 80, 'Lot de scanners');

-- Insertion dans materiel_emballage
INSERT INTO sge_cre.materiel_emballage (type_emballage, etat_emballage) VALUES
('Boite', 'Neuf'),
('Adhesive', 'Recupere'),
('Bourrage', 'Neuf'),
('Autre', 'Recupere'),
('Boite', 'Recupere');

-- Insertion dans commandes
INSERT INTO sge_cre.commandes (id_commandes, quantite, prix_unitaire) VALUES
('CMD01', 10, 15000.00),
('CMD02', 20, 10000.00),
('CMD03', 5, 25000.00),
('CMD04', 8, 18000.00),
('CMD05', 15, 12000.00);

-- Insertion dans commandes_achats
INSERT INTO sge_cre.commandes_achats (id_commande, date_commande, statut, quantite) VALUES
('CMD01', '2025-06-01', 'en_attente', 10),
('CMD02', '2025-06-02', 'expedie', 20),
('CMD03', '2025-06-03', 'recu', 5),
('CMD04', '2025-06-04', 'annule', 8),
('CMD05', '2025-06-05', 'en_attente', 15);

-- Vérifier l'insertion
SELECT * FROM sge_cre.commandes_achats ORDER BY id_commande;

-- Insertion dans commandes_vends
INSERT INTO sge_cre.commandes_vends (id_commande, date_commande, statut, quantite) VALUES
('CMD01', '2025-06-06', 'expedie', 5),
('CMD02', '2025-06-07', 'en_attente', 10),
('CMD03', '2025-06-08', 'recu', 3),
('CMD04', '2025-06-09', 'annule', 4),
('CMD05', '2025-06-10', 'expedie', 6);

-- Vérification finale
SELECT '=== RÉSUMÉ FINAL ===' as info;
SELECT 'Organisations' as table_name, COUNT(*) as count FROM sge_cre.organisations
UNION ALL
SELECT 'Individus', COUNT(*) FROM sge_cre.individus
UNION ALL
SELECT 'Produits', COUNT(*) FROM sge_cre.produits
UNION ALL
SELECT 'Entrepôts', COUNT(*) FROM sge_cre.entrepots
UNION ALL
SELECT 'Zones de stockage', COUNT(*) FROM sge_cre.zone_stockage
UNION ALL
SELECT 'Lots', COUNT(*) FROM sge_cre.lots
UNION ALL
SELECT 'Colis', COUNT(*) FROM sge_cre.colis
UNION ALL
SELECT 'Commandes achats', COUNT(*) FROM sge_cre.commandes_achats
UNION ALL
SELECT 'Commandes ventes', COUNT(*) FROM sge_cre.commandes_vends; 