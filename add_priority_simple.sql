-- Script simple pour ajouter le champ priorite
ALTER TABLE sge_cre.bon_expeditions ADD COLUMN IF NOT EXISTS priorite VARCHAR(20) DEFAULT 'moyenne';
UPDATE sge_cre.bon_expeditions SET priorite = 'moyenne' WHERE priorite IS NULL; 