-- Script pour insérer des zones de stockage de test
-- (avec les colonnes qui existent réellement dans la table)

INSERT INTO sge_cre.zone_stockage (id_cellule, e1, e2) VALUES
('C001', 'Zone A', 'Rayon 1'),
('C002', 'Zone A', 'Rayon 2'),
('C003', 'Zone B', 'Rayon 1'),
('C004', 'Zone B', 'Rayon 3'),
('C005', 'Zone C', 'Réserve');

-- Vérifier l'insertion
SELECT id_zo_stock, id_cellule, e1, e2 
FROM sge_cre.zone_stockage 
ORDER BY id_cellule; 