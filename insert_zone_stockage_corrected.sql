-- Script pour insérer des zones de stockage de test
-- (avec TOUTES les colonnes requises, y compris e3)

INSERT INTO sge_cre.zone_stockage (id_cellule, e1, e2, e3) VALUES
('C001', 'Zone A', 'Rayon 1', 'Étage 1'),
('C002', 'Zone A', 'Rayon 2', 'Étage 2'),
('C003', 'Zone B', 'Rayon 1', 'Étage 1'),
('C004', 'Zone B', 'Rayon 3', 'Étage 2'),
('C005', 'Zone C', 'Réserve', 'Étage 1');

-- Vérifier l'insertion
SELECT id_zo_stock, id_cellule, e1, e2, e3 
FROM sge_cre.zone_stockage 
ORDER BY id_cellule; 