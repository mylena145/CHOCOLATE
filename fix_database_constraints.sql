-- =============================================
-- SCRIPT DE CORRECTION DES CONTRAINTES DE CLÉS ÉTRANGÈRES
-- Résout tous les problèmes d'insertion dans l'ordre correct
-- =============================================

-- 1. Nettoyer les tables existantes (dans l'ordre inverse des dépendances)
DELETE FROM sge_cre.colis;
DELETE FROM sge_cre.lots;
DELETE FROM sge_cre.zone_stockage;
DELETE FROM sge_cre.cellules;
DELETE FROM sge_cre.entrepots;
DELETE FROM sge_cre.receptions;
DELETE FROM sge_cre.produits;
DELETE FROM sge_cre.repertoire;
DELETE FROM sge_cre.individus;
DELETE FROM sge_cre.organisations;
DELETE FROM sge_cre.commandes_achats;
DELETE FROM sge_cre.commandes_vends;
DELETE FROM sge_cre.commandes;
DELETE FROM sge_cre.materiel_emballage;

-- 2. Réinitialiser les séquences d'auto-increment (détection automatique)
-- Détecter et réinitialiser les séquences existantes
DO $$
DECLARE
    seq_name text;
    seq_record record;
BEGIN
    -- Trouver toutes les séquences dans le schéma sge_cre
    FOR seq_record IN 
        SELECT sequence_name 
        FROM information_schema.sequences 
        WHERE sequence_schema = 'sge_cre'
    LOOP
        seq_name := 'sge_cre.' || seq_record.sequence_name;
        EXECUTE 'ALTER SEQUENCE ' || seq_name || ' RESTART WITH 1';
        RAISE NOTICE 'Séquence réinitialisée: %', seq_name;
    END LOOP;
END $$;

-- 3. Insérer les données dans l'ordre correct (sans dépendances)

-- 3.1 Organisations (pas de dépendances) - Utilise id_lettre (VARCHAR)
INSERT INTO sge_cre.organisations (id_organisation, nom, adresse, telephone, statut, nbr_entrepot) VALUES
('ORG001', 'LogiPlus', 'Zone Industrielle, Yaoundé', '699001122', 'Fournisseur', 3),
('ORG002', 'TransAfrica', 'Rue de l''Avenir, Douala', '676543210', 'Transporteur', 5),
('ORG003', 'DepotCentral', 'Quartier Mvan, Yaoundé', '690112233', 'Destinataire', 1),
('ORG004', 'Fournitech', 'Avenue Kennedy, Douala', '655009988', 'Fournisseur', 2),
('ORG005', 'DistribPlus', 'Rue 12, Garoua', '688776655', 'Fournisseur', 4);

-- 3.2 Individus (pas de dépendances) - SERIAL auto-incrémenté
INSERT INTO sge_cre.individus (nom, password, email, adresse, prenom, role, telephone, matricule) VALUES
('Noelle', 'noelle25', 'noelle.sielinou@sac.com', 'Mvan', 'sielinou', 'Administrateur', '690112233', 'MGMGT'),
('Brice', 'brice25', 'brice.sodje@sac.com', 'Bonamoussadi', 'brice', 'Responsable_stocks', '691223344', 'MGMGR'),
('Orlane', 'orlane25', 'orlane.takia@sac.com', 'Cité Verte', 'tiako', 'Agent_logistique', '692334455', 'MGMGZ'),
('Pharel', 'pharel', 'pharel.ngounou@sac.com', 'Akwa', 'pharel', 'Emballeur', '693445566', 'MGMGP'),
('Abigael', 'abigael25', 'abigael.kemoe@sac.com', 'Essos', 'kemoe', 'Magasinier', '694559677', 'MGMGN'),
('Roy', 'roy25', 'roy.houtento@sac.com', 'Essos', 'houtento', 'Livreur', '694599677', 'MGMGL'),
('Chris', 'chris25', 'chris.tankwa@sac.com', 'Bonaberie', 'tankwa', 'Responsable_informatique', '655556677', 'MGMGV'),
('Astrid', 'astrid25', 'astrid.soap@sac.com', 'Bonamoussadi', 'soap', 'Technicien_informatique', '684000077', 'MGMGC'),
('Antoine', 'antoine25', 'antoine.kwamou@sac.com', 'Japoma', 'kwamou', 'Fournisseur', '674000077', 'MGMGY'),
('Daniel', 'daniel', 'daniel.kwamou@sac.com', 'Yaticka', 'kwamou', 'Responsable_securite_physique', '664000077', 'MGMGW'),
('Joel', 'joel25', 'joel.ziko@sac.com', 'Yansoki', 'ziko', 'Client', '611000077', 'MGMGT');

-- 3.3 Répertoire (dépend de organisations et individus)
INSERT INTO sge_cre.repertoire (id_organisation, id_individu) VALUES
('ORG001', 1),  -- LogiPlus - Noelle
('ORG002', 2),  -- TransAfrica - Brice
('ORG003', 3),  -- DepotCentral - Orlane
('ORG004', 4),  -- Fournitech - Pharel
('ORG005', 5);  -- DistribPlus - Abigael

-- 3.4 Produits (pas de dépendances) - Utilise id_prod (VARCHAR)
INSERT INTO sge_cre.produits (id_produit, nom, description, marque, modele, fournisseur, date_fabrique, date_peremption, stock, alert) VALUES
('PRD1', 'Clavier mécanique', 'Clavier RGB AZERTY pour gamers', 'Logitech', 'G413', 'Logitech France', '2023-05-15', '2026-05-15', 120, 60),
('PRD2', 'Disque SSD', 'Disque SSD 1To NVMe haute vitesse', 'Samsung', 'Evo 980', 'Samsung Electronics', '2024-01-10', '2029-01-10', 40, 14),
('PRD3', 'Routeur Wi-Fi', 'Routeur Wi-Fi 6 double bande', 'TP-Link', 'Archer AX50', 'TP-Link Europe', '2023-03-20', '2028-03-20', 75, 25),
('PRD4', 'Batterie externe', 'Power bank 20000mAh avec charge rapide', 'Anker', 'PowerCore', 'AnkerTech', '2022-09-01', '2025-09-01', 15, 5),
('PRD5', 'Imprimante laser', 'Imprimante laser monochrome multifonction', 'HP', 'LaserJet MFP 137fnw', 'HP Inc.', '2023-11-05', '2027-11-05', 5, 2);

-- 3.5 Réceptions (pas de dépendances) - SERIAL auto-incrémenté
INSERT INTO sge_cre.receptions (date_reception) VALUES
('2025-01-10'),
('2025-01-15'),
('2025-02-03'),
('2025-02-25'),
('2025-03-12');

-- 3.6 Entrepôts (dépend de organisations) - Utilise id_lettre (VARCHAR)
INSERT INTO sge_cre.entrepots (id_entrepot, id_organisation, nom_organisation, capacite, stockage, emplacement) VALUES
('ENT001', 'ORG001', 'Entrepôt LogiPlus', 5000, 'Informatique', 'Yaoundé'),
('ENT002', 'ORG002', 'Entrepôt TransAfrica', 3000, 'Transport', 'Douala'),
('ENT003', 'ORG003', 'Entrepôt DepotCentral', 2000, 'Stock général', 'Garoua'),
('ENT004', 'ORG004', 'Entrepôt Fournitech', 4000, 'Composants', 'Bafoussam'),
('ENT005', 'ORG005', 'Entrepôt DistribPlus', 2500, 'Divers', 'Maroua');

-- 3.7 Cellules (pas de dépendances) - Utilise id_prod (VARCHAR)
INSERT INTO sge_cre.cellules (id_cellule, longueur, largeur, hauteur, masse_maximale) VALUES
('C001', 120.5, 80.0, 60.0, 500.0),
('C002', 100.0, 75.0, 55.0, 450.0),
('C003', 110.0, 85.0, 65.0, 550.0),
('C004', 95.0, 70.0, 50.0, 400.0),
('C005', 130.0, 90.0, 70.0, 600.0);

-- 3.8 Zones de stockage (dépend de entrepots et cellules) - SERIAL auto-incrémenté
INSERT INTO sge_cre.zone_stockage (id_entrepot, id_cellule, e1, e2, e3) VALUES
('ENT001', 'C001', 'Zone A', 'Rayon 1', 'Étage 1'),
('ENT001', 'C002', 'Zone A', 'Rayon 2', 'Étage 2'),
('ENT002', 'C003', 'Zone B', 'Rayon 1', 'Étage 1'),
('ENT002', 'C004', 'Zone B', 'Rayon 3', 'Étage 2'),
('ENT003', 'C005', 'Zone C', 'Réserve', 'Étage 1');

-- 3.9 Colis (dépend de zone_stockage et receptions) - SERIAL auto-incrémenté
INSERT INTO sge_cre.colis (id_zo_stock, id_reception, dimension, poids, emplacement) VALUES
(1, 1, 50.0, 5.5, 'R1-E1'),
(2, 2, 60.0, 6.0, 'R1-E2'),
(3, 3, 55.0, 7.0, 'R2-E1'),
(4, 4, 65.0, 6.5, 'R2-E2'),
(5, 5, 70.0, 8.0, 'R3-E1');

-- 3.10 Lots (dépend de produits) - Utilise VARCHAR(6)
INSERT INTO sge_cre.lots (id_lot, id_produit, fournisseur, date_reception, date_expedition, quantite, description) VALUES
('LOT01', 'PRD1', 'LogiPlus', '2025-01-10', '2025-01-20', 100, 'Lot de clés USB'),
('LOT02', 'PRD2', 'Fournitech', '2025-01-15', '2025-01-25', 50, 'Lot de disques durs'),
('LOT03', 'PRD3', 'LogiPlus', '2025-02-03', '2025-02-10', 75, 'Lot d''écrans'),
('LOT04', 'PRD4', 'DistribPlus', '2025-02-25', '2025-03-05', 60, 'Lot d''imprimantes'),
('LOT05', 'PRD5', 'DistribPlus', '2025-03-12', '2025-03-20', 80, 'Lot de scanners');

-- 3.11 Matériel d'emballage (pas de dépendances) - SERIAL auto-incrémenté
INSERT INTO sge_cre.materiel_emballage (type_emballage, etat_emballage) VALUES
('Boite', 'Neuf'),
('Adhesive', 'Recupere'),
('Bourrage', 'Neuf'),
('Autre', 'Recupere'),
('Boite', 'Recupere');

-- 3.12 Commandes (pas de dépendances)
INSERT INTO sge_cre.commandes (id_commandes, quantite, prix_unitaire) VALUES
('CMD01', 10, 15000.00),
('CMD02', 20, 10000.00),
('CMD03', 5, 25000.00),
('CMD04', 8, 18000.00),
('CMD05', 15, 12000.00);

-- 3.13 Commandes d'achats (dépend de commandes)
INSERT INTO sge_cre.commandes_achats (id_commande, date_commande, statut, quantite) VALUES
('CMD01', '2025-06-01', 'en_attente', 10),
('CMD02', '2025-06-02', 'expedie', 20),
('CMD03', '2025-06-03', 'recu', 5),
('CMD04', '2025-06-04', 'annule', 8),
('CMD05', '2025-06-05', 'en_attente', 15);

-- 3.14 Commandes de vente (dépend de commandes)
INSERT INTO sge_cre.commandes_vends (id_commande, date_commande, statut, quantite) VALUES
('CMD01', '2025-06-06', 'expedie', 5),
('CMD02', '2025-06-07', 'en_attente', 10),
('CMD03', '2025-06-08', 'recu', 3),
('CMD04', '2025-06-09', 'annule', 4),
('CMD05', '2025-06-10', 'expedie', 6);

-- 4. Vérifications finales
SELECT '=== VÉRIFICATIONS ===' as info;

SELECT 'Organisations:' as table_name, COUNT(*) as count FROM sge_cre.organisations
UNION ALL
SELECT 'Individus:', COUNT(*) FROM sge_cre.individus
UNION ALL
SELECT 'Répertoire:', COUNT(*) FROM sge_cre.repertoire
UNION ALL
SELECT 'Produits:', COUNT(*) FROM sge_cre.produits
UNION ALL
SELECT 'Réceptions:', COUNT(*) FROM sge_cre.receptions
UNION ALL
SELECT 'Entrepôts:', COUNT(*) FROM sge_cre.entrepots
UNION ALL
SELECT 'Cellules:', COUNT(*) FROM sge_cre.cellules
UNION ALL
SELECT 'Zones stockage:', COUNT(*) FROM sge_cre.zone_stockage
UNION ALL
SELECT 'Colis:', COUNT(*) FROM sge_cre.colis
UNION ALL
SELECT 'Lots:', COUNT(*) FROM sge_cre.lots
UNION ALL
SELECT 'Matériel emballage:', COUNT(*) FROM sge_cre.materiel_emballage
UNION ALL
SELECT 'Commandes:', COUNT(*) FROM sge_cre.commandes
UNION ALL
SELECT 'Commandes achats:', COUNT(*) FROM sge_cre.commandes_achats
UNION ALL
SELECT 'Commandes vends:', COUNT(*) FROM sge_cre.commandes_vends;

-- 5. Test des contraintes de clés étrangères
SELECT '=== TEST DES CONTRAINTES ===' as info;

-- Vérifier que tous les colis ont des zones de stockage valides
SELECT 'Colis avec zones valides:' as test, COUNT(*) as count 
FROM sge_cre.colis c 
JOIN sge_cre.zone_stockage z ON c.id_zo_stock = z.id_zo_stock;

-- Vérifier que toutes les zones ont des entrepôts valides
SELECT 'Zones avec entrepôts valides:' as test, COUNT(*) as count 
FROM sge_cre.zone_stockage z 
JOIN sge_cre.entrepots e ON z.id_entrepot = e.id_entrepot;

-- Vérifier que tous les lots ont des produits valides
SELECT 'Lots avec produits valides:' as test, COUNT(*) as count 
FROM sge_cre.lots l 
JOIN sge_cre.produits p ON l.id_produit = p.id_produit;

SELECT '=== SCRIPT TERMINÉ AVEC SUCCÈS ===' as info; 