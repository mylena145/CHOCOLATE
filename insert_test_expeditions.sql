-- Script pour insérer des données de test dans la table bon_expeditions
-- À exécuter dans PostgreSQL pour tester les fonctionnalités dynamiques

-- Nettoyer la table (optionnel)
-- DELETE FROM sge_cre.bon_expeditions;

-- Insérer des expéditions de test
INSERT INTO sge_cre.bon_expeditions (client, reference_commande, date_livraison, observation, liste_articles_livres, transporteurs) VALUES
('Entreprise ABC', 'REF-20240318001', '2024-03-18', 'Client Premium - Livraison urgente', 'Produits électroniques', 'DHL Express'),
('Société XYZ', 'REF-20240318002', '2024-03-19', 'Livraison standard', 'Matériel de bureau', 'Chronopost'),
('SARL Technologie', 'REF-20240318003', '2024-03-20', 'Commande importante', 'Composants informatiques', 'Colissimo'),
('Bureau Solutions', 'REF-20240318004', '2024-03-18', 'Livraison express', 'Fournitures', 'UPS'),
('Tech Solutions', 'REF-20240318005', '2024-03-21', 'Commande régulière', 'Équipements', 'DHL Express'),
('Client Premium', 'REF-20240318006', '2024-03-18', 'URGENT - Livraison J+1', 'Produits critiques', 'DHL Express'),
('Entreprise Standard', 'REF-20240318007', '2024-03-22', 'Livraison normale', 'Articles divers', 'Chronopost'),
('Startup Innovante', 'REF-20240318008', '2024-03-19', 'Première commande', 'Prototypes', 'Colissimo');

-- Vérifier les données insérées
SELECT 
    id_bon_expedition,
    client,
    reference_commande,
    date_livraison,
    transporteurs,
    observation
FROM sge_cre.bon_expeditions
ORDER BY date_livraison, id_bon_expedition; 