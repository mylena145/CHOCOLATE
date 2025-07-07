-- Script corrigé pour insérer le répertoire avec les bons IDs
-- Basé sur les vrais id_individu trouvés (12-22)

-- Vérifier les individus disponibles
SELECT '=== INDIVIDUS DISPONIBLES ===' as info;
SELECT id_individu, nom, prenom, email 
FROM sge_cre.individus 
ORDER BY id_individu;

-- Vérifier les organisations disponibles
SELECT '=== ORGANISATIONS DISPONIBLES ===' as info;
SELECT id_organisation, nom, statut 
FROM sge_cre.organisations 
ORDER BY id_organisation;

-- Insérer le répertoire avec les vrais IDs
INSERT INTO sge_cre.repertoire (id_organisation, id_individu) VALUES
('ORG001', 12),  -- Noelle sielinou (Administrateur)
('ORG002', 13),  -- Brice brice (Responsable_stocks)
('ORG003', 14),  -- Orlane tiako (Agent_logistique)
('ORG004', 15),  -- Pharel pharel (Emballeur)
('ORG005', 16);  -- Abigael kemoe (Magasinier)

-- Vérifier le résultat
SELECT '=== RÉSULTAT ===' as info;
SELECT r.id_organisation, r.id_individu, o.nom as org_nom, i.nom as ind_nom, i.role
FROM sge_cre.repertoire r
JOIN sge_cre.organisations o ON r.id_organisation = o.id_organisation
JOIN sge_cre.individus i ON r.id_individu = i.id_individu
ORDER BY r.id_organisation; 