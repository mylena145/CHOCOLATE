-- =============================================
-- FICHIER DE TEST POSITIF (DONNÉES VALIDES)
-- =============================================

-- Ce fichier contient des données valides
-- qui respectent les contraintes du schéma 'sge_cre'

-- Insertion dans la table organisations
INSERT INTO "sge_cre".organisations (nom, adresse, telephone, statut, nbr_entrepot) VALUES
('LogiPlus',        'Zone Industrielle, Yaoundé',       '699001122', 'Fournisseur', 3),
('TransAfrica',     'Rue de l’Avenir, Douala',          '676543210', 'Transporteur', 5),
('DepotCentral',    'Quartier Mvan, Yaoundé',           '690112233', 'Destinataire', 1),
('Fournitech',      'Avenue Kennedy, Douala',           '655009988', 'Fournisseur', 2),
('RapidTrans',      'Bonabéri, Douala',                 '677778899', 'Transporteur', 4);

-- Insertion dans la table individus avec mots de passe valides (4-10 alphanumériques)
INSERT INTO "sge_cre".individus (nom, password, email, adresse, statut, telephone, prenom) VALUES
('JeanDupont',    'MG1234',  'jean.dupont@mail.com',       'Mvan, Yaoundé',         'Magasinier',    '690112233', 'Jean'),
('ClaireMbappe',  'MG4567',  'claire.mbappe@mail.com',     'Bonamoussadi, Douala',  'Responsable_stocks', '691223344', 'Claire'),
('LucienToko',    'MG7890',  'lucien.toko@mail.com',       'Cité Verte, Yaoundé',   'Magasinier',    '692334455', 'Lucien'),
('MarieNoel',     'MG0001',  'marie.noel@mail.com',        'Akwa, Douala',          'Responsable_stocks', '693445566', 'Marie'),
('AlbertNgoma',   'MG9988',  'albert.ngoma@mail.com',      'Essos, Yaoundé',        'Magasinier',    '694556677', 'Albert');

-- Insertion dans la table produits avec identifiants valides (4 caractères alphanumériques)
INSERT INTO "sge_cre".produits (id_produit, nom, description, marque, modele, fournisseur, date_fabrique, date_peremption) VALUES
('PR01',  'Clé USB',       'Stockage 32Go USB 3.0',        'SanDisk',     'Cruzer Blade',     'LogiPlus',     '2024-01-10', '2029-01-10'),
('PR02',  'Disque Dur',    'Disque dur externe 1To',       'Seagate',     'Backup Plus',      'Fournitech',   '2023-05-20', '2028-05-20'),
('PR03',  'Ecran LED',     'Écran 24 pouces Full HD',      'Samsung',     'S24F350',           'LogiPlus',     '2022-11-01', '2027-11-01'),
('PR04',  'Imprimante',    'Laser monochrome A4',          'HP',          'LaserJet P1102',    'EcomMat',      '2023-02-15', '2028-02-15'),
('PR05',  'Scanner',       'Scanner à plat haute vitesse', 'Canon',       'LiDE 300',          'DistribPlus',  '2024-03-10', '2029-03-10');

-- Insertion dans la table produits_logiciels avec domaines valides
INSERT INTO "sge_cre".produits_logiciels (id_pro_logiciel, id_produit, taille, licence) VALUES
('PL01', 'PR01', 125.4567, 'Opensource'),
('PL02', 'PR02', 512.0000, 'Proprietaire'),
('PL03', 'PR03', 1024.2500, 'Opensource'),
('PL04', 'PR04', 850.1256, 'Proprietaire');
