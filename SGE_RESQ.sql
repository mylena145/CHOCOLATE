-- =============================
-- FICHIER DE REQUÊTES SQL TEST
-- =============================

-- 1. Lister tous les individus avec leur statut et email
SELECT nom, prenom, email, statut FROM "sge_cre".individus;

-- 2. Trouver tous les produits qui expirent en 2025
SELECT id_produit, nom, date_peremption FROM "sge_cre".produits
WHERE date_part('year', date_peremption) = 2025;

-- 3. Afficher les logiciels dont la taille est supérieure à 500 Mo
SELECT p.nom, pl.taille, pl.licence FROM "sge_cre".produits_logiciels pl
JOIN "sge_cre".produits p ON pl.id_produit = p.id_produit
WHERE pl.taille > 500;

-- 4. Lister les organisations avec plus de 2 entrepôts
SELECT nom, telephone, nbr_entrepot FROM "sge_cre".organisations
WHERE nbr_entrepot > 2;

-- 5. Rechercher les produits de la marque 'HP'
SELECT id_produit, nom, modele FROM "sge_cre".produits
WHERE marque = 'HP';

-- 6. Trouver les produits dont le nom contient 'USB'
SELECT id_produit, nom, description FROM "sge_cre".produits
WHERE nom ILIKE '%USB%';

-- 7. Lister tous les rapports d'exception avec les noms des individus
SELECT r.date, r.type_exception, r.observation, i.nom FROM "sge_cre".rapports_exceptions r
JOIN "sge_cre".individus i ON r.id_individu = i.id_individu;

-- 8. Afficher tous les lots réceptionnés entre janvier et mars 2025
SELECT * FROM "sge_cre".lots
WHERE date_reception BETWEEN '2025-01-01' AND '2025-03-31';

-- 9. Afficher les cellules avec une masse maximale > 500 kg
SELECT id_cellule, masse_maximale FROM "sge_cre".cellules
WHERE masse_maximale > 500;

-- 10. Compter le nombre d'individus par statut
SELECT statut, COUNT(*) as total FROM "sge_cre".individus
GROUP BY statut;

-- 11. Récupérer les données de zone de stockage par entrepôt
SELECT z.id_entrepot, e.emplacement, z.id_cellule FROM "sge_cre".zone_stockage z
JOIN "sge_cre".entrepots e ON z.id_entrepot = e.id_entrepot;

-- 12. Voir les commandes avec leur montant total (prix * quantité)
SELECT id_commande, quantite, prix_unitaire, quantite * prix_unitaire AS montant_total
FROM "sge_cre".commandes;

-- 13. Afficher les individus affectés à une organisation (via répertoire)
SELECT i.nom AS individu, o.nom AS organisation FROM "sge_cre".repertoire r
JOIN "sge_cre".individus i ON r.id_individu = i.id_individu
JOIN "sge_cre".organisations o ON r.id_organisation = o.id_organisation;

-- 14. Lister les produits qui n'ont pas encore été expédiés (NULL date_expedition)
SELECT id_lot, id_produit, date_reception FROM "sge_cre".lots
WHERE date_expedition IS NULL;

-- 15. Afficher les 5 derniers individus inscrits (basé sur id croissant)
SELECT * FROM "sge_cre".individus
ORDER BY id_individu DESC
LIMIT 5;

\dt