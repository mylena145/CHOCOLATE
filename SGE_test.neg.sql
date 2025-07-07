-- =============================================
-- FICHIER DE TEST NÉGATIF (DONNÉES INVALIDE)
-- =============================================

-- Ce fichier contient des données invalides
-- qui violent les contraintes du schéma 'sge_cre'

-- Insertion dans la table organisations avec erreur sur le statut (valeur non prévue dans le domaine)
INSERT INTO "sge_cre".organisations (nom, adresse, telephone, statut, nbr_entrepot) VALUES
('BadOrg1', 'Adresse Invalide 1', '699000000', 'InvalideStatut', 2),
('BadOrg2', 'Adresse Invalide 2', '699111111', 'Manager', 3);

-- Insertion dans la table individus avec mots de passe invalides (moins de 4 ou plus de 10 caractères, ou caractères non autorisés)
INSERT INTO "sge_cre".individus (nom, password, email, adresse, statut, telephone, prenom) VALUES
('User1', 'M1', 'user1@mail.com', 'Adresse1', 'Magasinier', '600000000', 'Test'),
('User2', 'MGTR12345678', 'user2@mail.com', 'Adresse2', 'Responsable_stocks', '600000001', 'Test');

-- Insertion dans la table produits avec id_produit invalide (trop court ou caractères spéciaux)
INSERT INTO "sge_cre".produits (id_produit, nom, description, marque, modele, fournisseur, date_fabrique, date_peremption) VALUES
('P$', 'Produit Invalide 1', 'Desc', 'Marque', 'Modele', 'Fournisseur', '2024-01-01', '2029-01-01'),
('TOOLONG123', 'Produit Invalide 2', 'Desc', 'Marque', 'Modele', 'Fournisseur', '2024-01-01', '2029-01-01');

-- Insertion dans la table produits_logiciels avec licence invalide (valeur hors domaine)
INSERT INTO "sge_cre".produits_logiciels (id_pro_logiciel, id_produit, taille, licence) VALUES
('PLX1', 'PR01', 125.00, 'Freeware'),
('PLX2', 'PR02', 256.00, 'Undefined');
