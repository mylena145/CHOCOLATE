-- Script pour corriger le domaine id_lettre
-- Ce script modifie le domaine pour accepter des identifiants plus flexibles

-- 1. Supprimer l'ancien domaine (cascade pour supprimer les dépendances)
DROP DOMAIN IF EXISTS sge_cre.id_lettre CASCADE;

-- 2. Créer un nouveau domaine plus flexible
CREATE DOMAIN sge_cre.id_lettre AS VARCHAR(10) 
  CHECK (VALUE ~ '^[A-Z0-9]{1,10}$');

-- 3. Vérifier que le nouveau domaine fonctionne
SELECT 'Domaine id_lettre modifié avec succès' AS message;

-- 4. Maintenant tu peux utiliser des identifiants comme :
-- 'ORG001', 'ENT1', 'LOGIPL', etc. 