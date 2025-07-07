-- Script pour insérer des entrepôts de test
-- (avec les colonnes qui existent réellement dans la table)

INSERT INTO sge_cre.entrepots (nom_organisation, capacite, stockage, emplacement) VALUES
('Entrepôt LogiPlus', 5000, 'Informatique', 'Yaoundé'),
('Entrepôt TransAfrica', 3000, 'Transport', 'Douala'),
('Entrepôt DepotCentral', 2000, 'Stock général', 'Garoua'),
('Entrepôt Fournitech', 4000, 'Composants', 'Bafoussam'),
('Entrepôt DistribPlus', 2500, 'Divers', 'Maroua');

-- Vérifier l'insertion
SELECT nom_organisation, capacite, stockage, emplacement 
FROM sge_cre.entrepots 
ORDER BY nom_organisation; 