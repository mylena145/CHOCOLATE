-- Script pour ajouter le champ priorite à la table bon_expeditions
-- Exécuter ce script dans votre base de données PostgreSQL

-- Ajouter le champ priorite à la table bon_expeditions
ALTER TABLE sge_cre.bon_expeditions 
ADD COLUMN priorite VARCHAR(20) DEFAULT 'moyenne';

-- Mettre à jour les enregistrements existants avec une priorité par défaut
UPDATE sge_cre.bon_expeditions 
SET priorite = 'moyenne' 
WHERE priorite IS NULL;

-- Ajouter une contrainte pour limiter les valeurs possibles
ALTER TABLE sge_cre.bon_expeditions 
ADD CONSTRAINT check_priorite 
CHECK (priorite IN ('haute', 'moyenne', 'basse'));

-- Vérifier que la modification a été appliquée
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_schema = 'sge_cre' 
AND table_name = 'bon_expeditions' 
AND column_name = 'priorite'; 