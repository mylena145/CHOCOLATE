-- =============================================
-- SCRIPT DE SUPPRESSION DU SCHÉMA SGE
-- Version : Basé sur structure corrigée
-- =============================================

SET SCHEMA 'sge_cre';

-- Suppression des vues
DROP VIEW IF EXISTS individus_organisations CASCADE;

-- Suppression des tables dans l'ordre inverse de dépendance
DROP TABLE IF EXISTS rapports_exceptions CASCADE;
DROP TABLE IF EXISTS bon_expeditions CASCADE;
DROP TABLE IF EXISTS commandes_vends CASCADE;
DROP TABLE IF EXISTS commandes_achats CASCADE;
DROP TABLE IF EXISTS commandes CASCADE;
DROP TABLE IF EXISTS bon_receptions CASCADE;
DROP TABLE IF EXISTS lots CASCADE;
DROP TABLE IF EXISTS colis CASCADE;
DROP TABLE IF EXISTS zone_stockage CASCADE;
DROP TABLE IF EXISTS entrepots CASCADE;
DROP TABLE IF EXISTS cellules CASCADE;
DROP TABLE IF EXISTS materiel_emballage CASCADE;
DROP TABLE IF EXISTS receptions CASCADE;
DROP TABLE IF EXISTS produits CASCADE;
DROP TABLE IF EXISTS repertoire CASCADE;
DROP TABLE IF EXISTS magasiniers CASCADE;
DROP TABLE IF EXISTS individus CASCADE;
DROP TABLE IF EXISTS organisations CASCADE;

-- Suppression des domaines personnalisés
DROP DOMAIN IF EXISTS type_org CASCADE;
DROP DOMAIN IF EXISTS type_exception CASCADE;
DROP DOMAIN IF EXISTS adresse CASCADE;
DROP DOMAIN IF EXISTS keyword CASCADE;
DROP DOMAIN IF EXISTS numero CASCADE;
DROP DOMAIN IF EXISTS role_ind CASCADE;
DROP DOMAIN IF EXISTS id_lettre CASCADE;
DROP DOMAIN IF EXISTS description CASCADE;
DROP DOMAIN IF EXISTS id_prod CASCADE;
DROP DOMAIN IF EXISTS license CASCADE;
DROP DOMAIN IF EXISTS type_em CASCADE;
DROP DOMAIN IF EXISTS etat_em CASCADE;
DROP DOMAIN IF EXISTS statut CASCADE;
DROP DOMAIN IF EXISTS niveau_alerte CASCADE;

-- Supression des extension --
DROP EXTENSION IF EXISTS pgcrypto;


-- Suppression du schéma
DROP SCHEMA IF EXISTS sge_cre CASCADE;
