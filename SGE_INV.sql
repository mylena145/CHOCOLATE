-- =====================================================================
-- Fichier : SGE_inv.sql
-- Objectif : Invariants requis — types, vues, fonctions, déclencheurs
-- Schéma : sge_cre
-- =====================================================================

SET search_path TO sge_cre;

-- ============================================================
-- SECTION 1 : DOMAINES (déjà définis dans le fichier SGE_CRE)
-- ============================================================
-- Aucune redéfinition ici (cf. fichier SGE_CRE.sql)

-- ================================
-- SECTION 2 : VUES
-- ================================

-- 1. Vue : Résumé des produits reçus avec infos produit et individu
CREATE OR REPLACE VIEW vw_bon_reception_details AS
SELECT
    br.id_bon_reception,
    br.date_reception,
    i.id_individu,
    i.nom AS nom_individu,
    i.prenom AS prenom_individu,
    i.role AS role_individu,
    p.id_produit,
    p.nom AS nom_produit,
    p.marque,
    p.modele,
    p.description AS description_produit
FROM
    bon_receptions br
JOIN
    individus i ON br.id_magasinier = i.id_individu
JOIN
    produits p ON br.reference_commande = p.id_produit;

-- 2. Vue : Commandes clients en attente ou expédiées
CREATE OR REPLACE VIEW vue_commandes_clients AS
SELECT 
    cv.id_commande,
    cv.date_commande,
    cv.statut,  -- Pas 'role', mais 'statut'
    cv.quantite,
    c.quantite AS quantite_commande,
    c.prix_unitaire
FROM 
    commandes_vends cv
JOIN 
    commandes c ON cv.id_commande = c.id_commandes  -- Jointure avec commandes, pas produits
WHERE 
    cv.statut IN ('en_attente', 'expedie');  -- Pas 'role', mais 'statut'

-- ================================
-- SECTION 3 : FONCTIONS
-- ================================

-- 1. Fonction : Calculer le poids total d’un colis
CREATE OR REPLACE FUNCTION poids_total_colis(p_colis_id INT)
RETURNS DECIMAL(10,2) AS $$
DECLARE
    total DECIMAL(10,2);
BEGIN
    SELECT poids INTO total
    FROM colis
    WHERE id_colis = p_colis_id;

    RETURN total;
END;
$$ LANGUAGE plpgsql;

-- 2. Fonction : Vérifier si une livraison est en retard (> 7 jours)
CREATE OR REPLACE FUNCTION est_livraison_retard(reference TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    date_cmd DATE;
    date_liv DATE;
BEGIN
    SELECT date_commande INTO date_cmd
    FROM commandes_vends
    WHERE reference_commande = reference;

    SELECT date_livraison INTO date_liv
    FROM bon_expeditions
    WHERE reference_commande = reference;

    RETURN date_liv > (date_cmd + INTERVAL '7 days');
END;
$$ LANGUAGE plpgsql;

-- ================================
-- SECTION 4 : DÉCLENCHEURS
-- ================================

-- 1. Déclencheur : Poids colis <= 100kg
CREATE OR REPLACE FUNCTION verifier_poids_colis()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.poids > 100 THEN
        RAISE EXCEPTION 'Le poids d’un colis ne peut pas dépasser 100 kg.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_verifier_poids_colis
BEFORE INSERT OR UPDATE ON colis
FOR EACH ROW EXECUTE FUNCTION verifier_poids_colis();

-- 2. Déclencheur : Quantité commande > 0
CREATE OR REPLACE FUNCTION verifier_quantite_commande()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.quantite <= 0 THEN
        RAISE EXCEPTION 'La quantité d’une commande doit être strictement positive.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_verifier_quantite
BEFORE INSERT OR UPDATE ON commandes
FOR EACH ROW EXECUTE FUNCTION verifier_quantite_commande();

-- 3. Déclencheur : Référence de commande unique
CREATE OR REPLACE FUNCTION verifier_reference_unique()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM bon_expeditions
        WHERE reference_commande = NEW.reference_commande
    ) THEN
        RAISE EXCEPTION 'Référence de commande déjà utilisée.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_reference_unique
BEFORE INSERT ON bon_expeditions
FOR EACH ROW EXECUTE FUNCTION verifier_reference_unique();

-- ================================
-- FIN DU FICHIER
-- ================================
