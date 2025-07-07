-- Script pour insérer les données avec les identifiants corrigés
-- Exécuter d'abord fix_domain.sql avant ce script

-- 1. Insérer les organisations
INSERT INTO sge_cre.organisations (id_organisation, nom, adresse, telephone, statut, nbr_entrepot) VALUES
('ORG001', 'LogiPlus', 'Zone Industrielle, Yaoundé', '699001122', 'Fournisseur', 3),
('ORG002', 'TransAfrica', 'Rue de l''Avenir, Douala', '676543210', 'Transporteur', 5),
('ORG003', 'DepotCentral', 'Quartier Mvan, Yaoundé', '690112233', 'Destinataire', 1),
('ORG004', 'Fournitech', 'Avenue Kennedy, Douala', '655009988', 'Fournisseur', 2),
('ORG005', 'DistribPlus', 'Rue 12, Garoua', '688776655', 'Fournisseur', 4);

-- 2. Insérer les individus (si pas déjà fait)
INSERT INTO sge_cre.individus (nom, password, email, adresse, prenom, role, telephone, matricule) VALUES
('Dupont', '1234', 'dupont@email.com', 'Yaoundé', 'Jean', 'admin', '699001122', 'EMP001'),
('Martin', '1234', 'martin@email.com', 'Douala', 'Marie', 'user', '676543210', 'EMP002'),
('Durand', '1234', 'durand@email.com', 'Garoua', 'Pierre', 'user', '690112233', 'EMP003'),
('Bernard', '1234', 'bernard@email.com', 'Bafoussam', 'Sophie', 'user', '655009988', 'EMP004'),
('Petit', '1234', 'petit@email.com', 'Maroua', 'Lucas', 'user', '688776655', 'EMP005');

-- 3. Insérer dans le répertoire
INSERT INTO sge_cre.repertoire (id_organisation, id_individu) VALUES
('ORG001', 1),
('ORG002', 2),
('ORG003', 3),
('ORG004', 4),
('ORG005', 5);

-- 4. Insérer les entrepôts
INSERT INTO sge_cre.entrepots (id_entrepot, id_organisation, nom_organisation, capacite, stockage, emplacement) VALUES
('ENT001', 'ORG001', 'Entrepôt LogiPlus', 5000, 'Informatique', 'Yaoundé'),
('ENT002', 'ORG002', 'Entrepôt TransAfrica', 3000, 'Transport', 'Douala'),
('ENT003', 'ORG003', 'Entrepôt DepotCentral', 2000, 'Stock général', 'Garoua'),
('ENT004', 'ORG004', 'Entrepôt Fournitech', 4000, 'Composants', 'Bafoussam'),
('ENT005', 'ORG005', 'Entrepôt DistribPlus', 2500, 'Divers', 'Maroua');

-- 5. Insérer les produits
INSERT INTO sge_cre.produits (id_produit, nom, description, marque, modele, fournisseur, date_fabrique, date_peremption, stock, alert) VALUES
('PROD1', 'Ordinateur portable', 'Ordinateur portable 15 pouces', 'Dell', 'Latitude 7420', 'ORG001', '2024-01-01', '2027-01-01', 50, 10),
('PROD2', 'Souris optique', 'Souris optique sans fil', 'Logitech', 'MX Master 3', 'ORG001', '2024-01-01', '2027-01-01', 100, 20),
('PROD3', 'Clavier mécanique', 'Clavier mécanique RGB', 'Corsair', 'K70', 'ORG004', '2024-01-01', '2027-01-01', 75, 15),
('PROD4', 'Moniteur 24"', 'Moniteur Full HD 24 pouces', 'Samsung', 'LS24F350', 'ORG004', '2024-01-01', '2027-01-01', 30, 5),
('PROD5', 'Disque dur externe', 'Disque dur externe 1TB', 'Western Digital', 'My Passport', 'ORG005', '2024-01-01', '2027-01-01', 200, 40);

-- 6. Insérer les cellules
INSERT INTO sge_cre.cellules (id_cellule, longueur, largeur, hauteur, masse_maximale) VALUES
('CELL1', 100.00, 100.00, 100.00, 50.00),
('CELL2', 150.00, 120.00, 120.00, 75.00),
('CELL3', 200.00, 150.00, 150.00, 100.00),
('CELL4', 120.00, 100.00, 100.00, 60.00),
('CELL5', 180.00, 130.00, 130.00, 85.00);

-- 7. Insérer les zones de stockage
INSERT INTO sge_cre.zone_stockage (id_entrepot, id_cellule, e1, e2, e3) VALUES
('ENT001', 'CELL1', 'Zone A', 'Rangée 1', 'Étagère 1'),
('ENT001', 'CELL2', 'Zone A', 'Rangée 1', 'Étagère 2'),
('ENT002', 'CELL3', 'Zone B', 'Rangée 2', 'Étagère 1'),
('ENT003', 'CELL4', 'Zone C', 'Rangée 1', 'Étagère 1'),
('ENT004', 'CELL5', 'Zone D', 'Rangée 1', 'Étagère 1');

-- Vérification
SELECT 'Données insérées avec succès' AS message;
SELECT COUNT(*) AS nb_organisations FROM sge_cre.organisations;
SELECT COUNT(*) AS nb_individus FROM sge_cre.individus;
SELECT COUNT(*) AS nb_entrepots FROM sge_cre.entrepots;
SELECT COUNT(*) AS nb_produits FROM sge_cre.produits; 