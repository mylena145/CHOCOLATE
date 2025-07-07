-- Script pour insérer des organisations de test
-- (sans la colonne id_organisation qui n'existe pas)

INSERT INTO sge_cre.organisations (nom, adresse, telephone, statut, nbr_entrepot) VALUES
('LogiPlus', 'Zone Industrielle, Yaoundé', '699001122', 'Fournisseur', 3),
('TransAfrica', 'Rue de l''Avenir, Douala', '676543210', 'Transporteur', 5),
('DepotCentral', 'Quartier Mvan, Yaoundé', '690112233', 'Destinataire', 1),
('Fournitech', 'Avenue Kennedy, Douala', '655009988', 'Fournisseur', 2),
('DistribPlus', 'Rue 12, Garoua', '688776655', 'Fournisseur', 4);

-- Vérifier l'insertion
SELECT * FROM sge_cre.organisations ORDER BY nom; 