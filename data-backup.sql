PGDMP      .                }           postgres    16.9    16.9 �    O           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            P           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            Q           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            R           1262    5    postgres    DATABASE     {   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'French_France.1252';
    DROP DATABASE postgres;
                postgres    false            S           0    0    DATABASE postgres    COMMENT     N   COMMENT ON DATABASE postgres IS 'default administrative connection database';
                   postgres    false    5202                        2615    19360    sge_cre    SCHEMA        CREATE SCHEMA sge_cre;
    DROP SCHEMA sge_cre;
                postgres    false            T           0    0    SCHEMA sge_cre    COMMENT     N   COMMENT ON SCHEMA sge_cre IS 'Schema pour le systeme de gestion d''entrepot';
                   postgres    false    8            U           0    0    SCHEMA sge_cre    ACL     )   GRANT USAGE ON SCHEMA sge_cre TO PUBLIC;
                   postgres    false    8            �           1247    19369    adresse    DOMAIN     �   CREATE DOMAIN sge_cre.adresse AS text
	CONSTRAINT adresse_check CHECK (((char_length(VALUE) >= 1) AND (char_length(VALUE) <= 50)));
    DROP DOMAIN sge_cre.adresse;
       sge_cre          postgres    false    8            �           1247    19384    description    DOMAIN     �   CREATE DOMAIN sge_cre.description AS text
	CONSTRAINT description_check CHECK (((char_length(VALUE) >= 1) AND (char_length(VALUE) <= 300)));
 !   DROP DOMAIN sge_cre.description;
       sge_cre          postgres    false    8            �           1247    19396    etat_em    DOMAIN     �   CREATE DOMAIN sge_cre.etat_em AS character varying(20)
	CONSTRAINT etat_em_check CHECK (((VALUE)::text = ANY ((ARRAY['Neuf'::character varying, 'Recupere'::character varying])::text[])));
    DROP DOMAIN sge_cre.etat_em;
       sge_cre          postgres    false    8            �           1247    19402 	   id_lettre    DOMAIN     �   CREATE DOMAIN sge_cre.id_lettre AS character varying(10)
	CONSTRAINT id_lettre_check CHECK (((VALUE)::text ~ '^[A-Z0-9]{1,10}$'::text));
    DROP DOMAIN sge_cre.id_lettre;
       sge_cre          postgres    false    8            �           1247    19387    id_prod    DOMAIN     �   CREATE DOMAIN sge_cre.id_prod AS character varying(4)
	CONSTRAINT id_prod_check CHECK (((VALUE)::text ~ '^[A-Z0-9]{4}$'::text));
    DROP DOMAIN sge_cre.id_prod;
       sge_cre          postgres    false    8            �           1247    19372    keyword    DOMAIN     �   CREATE DOMAIN sge_cre.keyword AS character varying(15)
	CONSTRAINT keyword_check CHECK (((length((VALUE)::text) >= 4) AND (length((VALUE)::text) <= 15) AND ((VALUE)::text ~* '^[a-z0-9]+$'::text)));
    DROP DOMAIN sge_cre.keyword;
       sge_cre          postgres    false    8            �           1247    19390    license    DOMAIN     �   CREATE DOMAIN sge_cre.license AS character varying(20)
	CONSTRAINT license_check CHECK (((VALUE)::text = ANY ((ARRAY['Opensource'::character varying, 'Proprietaire'::character varying])::text[])));
    DROP DOMAIN sge_cre.license;
       sge_cre          postgres    false    8            �           1247    19375    numero    DOMAIN     |   CREATE DOMAIN sge_cre.numero AS character varying(9)
	CONSTRAINT numero_check CHECK (((VALUE)::text ~ '^[0-9]{9}$'::text));
    DROP DOMAIN sge_cre.numero;
       sge_cre          postgres    false    8            �           1247    19378    role_ind    DOMAIN     (  CREATE DOMAIN sge_cre.role_ind AS character varying(30)
	CONSTRAINT role_ind_check CHECK (((VALUE)::text = ANY ((ARRAY['Responsable_stocks'::character varying, 'Magasinier'::character varying, 'Emballeur'::character varying, 'Agent_logistique'::character varying, 'Livreur'::character varying, 'Responsable_informatique'::character varying, 'Technicien_informatique'::character varying, 'Administrateur'::character varying, 'Responsable_securite_physique'::character varying, 'Fournisseur'::character varying, 'Client'::character varying])::text[])));
    DROP DOMAIN sge_cre.role_ind;
       sge_cre          postgres    false    8            �           1247    19399    statut    DOMAIN     �   CREATE DOMAIN sge_cre.statut AS character varying(30)
	CONSTRAINT statut_check CHECK (((VALUE)::text = ANY ((ARRAY['en_attente'::character varying, 'expedie'::character varying, 'recu'::character varying, 'annule'::character varying])::text[])));
    DROP DOMAIN sge_cre.statut;
       sge_cre          postgres    false    8            �           1247    19393    type_em    DOMAIN     �   CREATE DOMAIN sge_cre.type_em AS character varying(20)
	CONSTRAINT type_em_check CHECK (((VALUE)::text = ANY ((ARRAY['Boite'::character varying, 'Adhesive'::character varying, 'Bourrage'::character varying, 'Autre'::character varying])::text[])));
    DROP DOMAIN sge_cre.type_em;
       sge_cre          postgres    false    8            �           1247    19366    type_exception    DOMAIN     	  CREATE DOMAIN sge_cre.type_exception AS character varying(30)
	CONSTRAINT type_exception_check CHECK (((VALUE)::text = ANY ((ARRAY['Ecarts'::character varying, 'Erreurs'::character varying, 'Retards'::character varying, 'Incidents'::character varying])::text[])));
 $   DROP DOMAIN sge_cre.type_exception;
       sge_cre          postgres    false    8            �           1247    19363    type_org    DOMAIN     �   CREATE DOMAIN sge_cre.type_org AS character varying(30)
	CONSTRAINT type_org_check CHECK (((VALUE)::text = ANY ((ARRAY['Fournisseur'::character varying, 'Transporteur'::character varying, 'Destinataire'::character varying])::text[])));
    DROP DOMAIN sge_cre.type_org;
       sge_cre          postgres    false    8            �            1259    19633    bon_expeditions    TABLE     �  CREATE TABLE sge_cre.bon_expeditions (
    id_bon_expedition integer NOT NULL,
    id_colis integer,
    client character varying(50),
    reference_commande character varying(50) NOT NULL,
    date_livraison date NOT NULL,
    observation sge_cre.description,
    liste_articles_livres text,
    transporteurs character varying(50) NOT NULL,
    priorite character varying(20) DEFAULT 'moyenne'::character varying
);
 $   DROP TABLE sge_cre.bon_expeditions;
       sge_cre         heap    postgres    false    981    8            V           0    0    TABLE bon_expeditions    ACL     N   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.bon_expeditions TO PUBLIC;
          sge_cre          postgres    false    242            �            1259    19632 %   bon_expeditions_id_bon_expedition_seq    SEQUENCE     �   CREATE SEQUENCE sge_cre.bon_expeditions_id_bon_expedition_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 =   DROP SEQUENCE sge_cre.bon_expeditions_id_bon_expedition_seq;
       sge_cre          postgres    false    8    242            W           0    0 %   bon_expeditions_id_bon_expedition_seq    SEQUENCE OWNED BY     q   ALTER SEQUENCE sge_cre.bon_expeditions_id_bon_expedition_seq OWNED BY sge_cre.bon_expeditions.id_bon_expedition;
          sge_cre          postgres    false    241            �            1259    19578    bon_receptions    TABLE     A  CREATE TABLE sge_cre.bon_receptions (
    id_bon_reception integer NOT NULL,
    id_reception integer,
    id_magasinier integer,
    date_reception date NOT NULL,
    observation sge_cre.description,
    fournisseur character varying(50),
    liste_articles_recu text,
    reference_commande sge_cre.id_prod NOT NULL
);
 #   DROP TABLE sge_cre.bon_receptions;
       sge_cre         heap    postgres    false    981    8    985            X           0    0    TABLE bon_receptions    ACL     M   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.bon_receptions TO PUBLIC;
          sge_cre          postgres    false    235            �            1259    19577 #   bon_receptions_id_bon_reception_seq    SEQUENCE     �   CREATE SEQUENCE sge_cre.bon_receptions_id_bon_reception_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE sge_cre.bon_receptions_id_bon_reception_seq;
       sge_cre          postgres    false    8    235            Y           0    0 #   bon_receptions_id_bon_reception_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE sge_cre.bon_receptions_id_bon_reception_seq OWNED BY sge_cre.bon_receptions.id_bon_reception;
          sge_cre          postgres    false    234            �            1259    19510    cellules    TABLE     �   CREATE TABLE sge_cre.cellules (
    id_cellule sge_cre.id_prod NOT NULL,
    longueur numeric(6,2) NOT NULL,
    largeur numeric(6,2) NOT NULL,
    hauteur numeric(6,2) NOT NULL,
    masse_maximale numeric(6,2) NOT NULL
);
    DROP TABLE sge_cre.cellules;
       sge_cre         heap    postgres    false    8    985            Z           0    0    TABLE cellules    ACL     G   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.cellules TO PUBLIC;
          sge_cre          postgres    false    227            �            1259    19549    colis    TABLE     �   CREATE TABLE sge_cre.colis (
    id_colis integer NOT NULL,
    id_zo_stock integer,
    id_reception integer,
    dimension numeric(6,2) NOT NULL,
    poids numeric(6,2) NOT NULL,
    emplacement character varying(20) NOT NULL
);
    DROP TABLE sge_cre.colis;
       sge_cre         heap    postgres    false    8            [           0    0    TABLE colis    ACL     D   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.colis TO PUBLIC;
          sge_cre          postgres    false    232            �            1259    19548    colis_id_colis_seq    SEQUENCE     �   CREATE SEQUENCE sge_cre.colis_id_colis_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE sge_cre.colis_id_colis_seq;
       sge_cre          postgres    false    8    232            \           0    0    colis_id_colis_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE sge_cre.colis_id_colis_seq OWNED BY sge_cre.colis.id_colis;
          sge_cre          postgres    false    231            �            1259    19607 	   commandes    TABLE     �   CREATE TABLE sge_cre.commandes (
    id_commandes character varying(5) NOT NULL,
    quantite integer NOT NULL,
    prix_unitaire numeric(10,2) NOT NULL
);
    DROP TABLE sge_cre.commandes;
       sge_cre         heap    postgres    false    8            ]           0    0    TABLE commandes    ACL     H   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.commandes TO PUBLIC;
          sge_cre          postgres    false    238            �            1259    19612    commandes_achats    TABLE     �   CREATE TABLE sge_cre.commandes_achats (
    id_commande character varying(5) NOT NULL,
    date_commande date NOT NULL,
    statut character varying(20),
    quantite integer NOT NULL
);
 %   DROP TABLE sge_cre.commandes_achats;
       sge_cre         heap    postgres    false    8            ^           0    0    TABLE commandes_achats    ACL     O   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.commandes_achats TO PUBLIC;
          sge_cre          postgres    false    239            �            1259    19622    commandes_vends    TABLE     �   CREATE TABLE sge_cre.commandes_vends (
    id_commande character varying(5) NOT NULL,
    date_commande date NOT NULL,
    statut character varying(20),
    quantite integer NOT NULL
);
 $   DROP TABLE sge_cre.commandes_vends;
       sge_cre         heap    postgres    false    8            _           0    0    TABLE commandes_vends    ACL     N   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.commandes_vends TO PUBLIC;
          sge_cre          postgres    false    240            �            1259    19517 	   entrepots    TABLE       CREATE TABLE sge_cre.entrepots (
    id_entrepot sge_cre.id_lettre NOT NULL,
    id_organisation sge_cre.id_lettre,
    nom_organisation character varying(50) NOT NULL,
    capacite integer NOT NULL,
    stockage character varying(55),
    emplacement character varying(25) NOT NULL
);
    DROP TABLE sge_cre.entrepots;
       sge_cre         heap    postgres    false    1005    8    1005            `           0    0    TABLE entrepots    ACL     H   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.entrepots TO PUBLIC;
          sge_cre          postgres    false    228            �            1259    19414 	   individus    TABLE     �  CREATE TABLE sge_cre.individus (
    id_individu integer NOT NULL,
    nom character varying(50) NOT NULL,
    password character varying(15) NOT NULL,
    email character varying(100) NOT NULL,
    adresse character varying(50) NOT NULL,
    prenom character varying(50) NOT NULL,
    role sge_cre.role_ind NOT NULL,
    telephone character varying(20),
    matricule character varying(10)
);
    DROP TABLE sge_cre.individus;
       sge_cre         heap    postgres    false    977    8            a           0    0    TABLE individus    ACL     H   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.individus TO PUBLIC;
          sge_cre          postgres    false    220            �            1259    19413    individus_id_individu_seq    SEQUENCE     �   CREATE SEQUENCE sge_cre.individus_id_individu_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE sge_cre.individus_id_individu_seq;
       sge_cre          postgres    false    220    8            b           0    0    individus_id_individu_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE sge_cre.individus_id_individu_seq OWNED BY sge_cre.individus.id_individu;
          sge_cre          postgres    false    219            �            1259    19404    organisations    TABLE     �  CREATE TABLE sge_cre.organisations (
    id_organisation sge_cre.id_lettre NOT NULL,
    nom character varying(50) NOT NULL,
    adresse sge_cre.adresse NOT NULL,
    telephone character varying(20) NOT NULL,
    statut sge_cre.type_org,
    nbr_entrepot integer,
    date_creation timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    date_maj timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
 "   DROP TABLE sge_cre.organisations;
       sge_cre         heap    postgres    false    8    957    965    1005            c           0    0    TABLE organisations    ACL     L   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.organisations TO PUBLIC;
          sge_cre          postgres    false    218            �            1259    19475 
   repertoire    TABLE     �   CREATE TABLE sge_cre.repertoire (
    id_organisation sge_cre.id_lettre NOT NULL,
    id_individu integer NOT NULL,
    date_ajout date DEFAULT CURRENT_DATE
);
    DROP TABLE sge_cre.repertoire;
       sge_cre         heap    postgres    false    1005    8            d           0    0    TABLE repertoire    ACL     I   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.repertoire TO PUBLIC;
          sge_cre          postgres    false    223            �            1259    19674    individus_organisations    VIEW     �  CREATE VIEW sge_cre.individus_organisations AS
 SELECT i.id_individu,
    i.nom AS nom_individu,
    i.prenom,
    i.email,
    o.id_organisation,
    o.nom AS organisation,
    o.statut AS type_organisation
   FROM ((sge_cre.individus i
     JOIN sge_cre.repertoire r ON ((i.id_individu = r.id_individu)))
     JOIN sge_cre.organisations o ON (((o.id_organisation)::text = (r.id_organisation)::text)));
 +   DROP VIEW sge_cre.individus_organisations;
       sge_cre          postgres    false    218    220    223    223    220    218    220    218    220    957    1005    8            e           0    0    TABLE individus_organisations    ACL     V   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.individus_organisations TO PUBLIC;
          sge_cre          postgres    false    245            �            1259    40997    logs_activite    TABLE     G  CREATE TABLE sge_cre.logs_activite (
    id integer NOT NULL,
    type_action character varying(50) NOT NULL,
    description text NOT NULL,
    date_action timestamp without time zone DEFAULT now(),
    utilisateur character varying(100) NOT NULL,
    details text,
    created_at timestamp without time zone DEFAULT now()
);
 "   DROP TABLE sge_cre.logs_activite;
       sge_cre         heap    postgres    false    8            f           0    0    TABLE logs_activite    ACL     L   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.logs_activite TO PUBLIC;
          sge_cre          postgres    false    251            �            1259    40996    logs_activite_id_seq    SEQUENCE     �   CREATE SEQUENCE sge_cre.logs_activite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE sge_cre.logs_activite_id_seq;
       sge_cre          postgres    false    8    251            g           0    0    logs_activite_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE sge_cre.logs_activite_id_seq OWNED BY sge_cre.logs_activite.id;
          sge_cre          postgres    false    250            �            1259    19565    lots    TABLE       CREATE TABLE sge_cre.lots (
    id_lot character varying(6) NOT NULL,
    id_produit sge_cre.id_prod NOT NULL,
    fournisseur character varying(50) NOT NULL,
    date_reception date,
    date_expedition date,
    quantite integer NOT NULL,
    description sge_cre.description
);
    DROP TABLE sge_cre.lots;
       sge_cre         heap    postgres    false    985    981    8            h           0    0 
   TABLE lots    ACL     C   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.lots TO PUBLIC;
          sge_cre          postgres    false    233            �            1259    19425    magasiniers    TABLE     b   CREATE TABLE sge_cre.magasiniers (
    id_magasinier integer NOT NULL,
    id_individu integer
);
     DROP TABLE sge_cre.magasiniers;
       sge_cre         heap    postgres    false    8            i           0    0    TABLE magasiniers    ACL     J   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.magasiniers TO PUBLIC;
          sge_cre          postgres    false    222            �            1259    19424    magasiniers_id_magasinier_seq    SEQUENCE     �   CREATE SEQUENCE sge_cre.magasiniers_id_magasinier_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE sge_cre.magasiniers_id_magasinier_seq;
       sge_cre          postgres    false    222    8            j           0    0    magasiniers_id_magasinier_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE sge_cre.magasiniers_id_magasinier_seq OWNED BY sge_cre.magasiniers.id_magasinier;
          sge_cre          postgres    false    221            �            1259    19599    materiel_emballage    TABLE     �  CREATE TABLE sge_cre.materiel_emballage (
    id_emballeur integer NOT NULL,
    type_emballage sge_cre.type_em NOT NULL,
    etat_emballage sge_cre.etat_em NOT NULL,
    CONSTRAINT etat_emballage_check CHECK (((etat_emballage)::text = ANY ((ARRAY['Neuf'::character varying, 'Recupere'::character varying, 'En attente'::character varying, 'Rejeté'::character varying])::text[])))
);
 '   DROP TABLE sge_cre.materiel_emballage;
       sge_cre         heap    postgres    false    993    8    997            k           0    0    TABLE materiel_emballage    ACL     Q   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.materiel_emballage TO PUBLIC;
          sge_cre          postgres    false    237            �            1259    19598 #   materiel_emballage_id_emballeur_seq    SEQUENCE     �   CREATE SEQUENCE sge_cre.materiel_emballage_id_emballeur_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE sge_cre.materiel_emballage_id_emballeur_seq;
       sge_cre          postgres    false    8    237            l           0    0 #   materiel_emballage_id_emballeur_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE sge_cre.materiel_emballage_id_emballeur_seq OWNED BY sge_cre.materiel_emballage.id_emballeur;
          sge_cre          postgres    false    236            �            1259    24591 
   mouvements    TABLE     �  CREATE TABLE sge_cre.mouvements (
    id integer NOT NULL,
    type text NOT NULL,
    produit_id integer,
    produit_nom text NOT NULL,
    quantite integer NOT NULL,
    reference text,
    origine text,
    destination text,
    responsable text NOT NULL,
    date_mouvement timestamp without time zone NOT NULL,
    commentaire text,
    statut text DEFAULT 'Complété'::text
);
    DROP TABLE sge_cre.mouvements;
       sge_cre         heap    postgres    false    8            m           0    0    TABLE mouvements    ACL     I   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.mouvements TO PUBLIC;
          sge_cre          postgres    false    247            �            1259    24590    mouvements_id_seq    SEQUENCE     �   CREATE SEQUENCE sge_cre.mouvements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE sge_cre.mouvements_id_seq;
       sge_cre          postgres    false    247    8            n           0    0    mouvements_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE sge_cre.mouvements_id_seq OWNED BY sge_cre.mouvements.id;
          sge_cre          postgres    false    246            �            1259    24601    products    TABLE       CREATE TABLE sge_cre.products (
    id integer NOT NULL,
    code text NOT NULL,
    name text NOT NULL,
    stock integer DEFAULT 0,
    min_stock integer DEFAULT 10,
    location text,
    category text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE sge_cre.products;
       sge_cre         heap    postgres    false    8            o           0    0    TABLE products    ACL     G   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.products TO PUBLIC;
          sge_cre          postgres    false    249            �            1259    24600    products_id_seq    SEQUENCE     �   CREATE SEQUENCE sge_cre.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE sge_cre.products_id_seq;
       sge_cre          postgres    false    249    8            p           0    0    products_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE sge_cre.products_id_seq OWNED BY sge_cre.products.id;
          sge_cre          postgres    false    248            �            1259    19493    produits    TABLE       CREATE TABLE sge_cre.produits (
    id_produit sge_cre.id_prod NOT NULL,
    nom character varying(50) NOT NULL,
    description sge_cre.description,
    marque character varying(50) NOT NULL,
    modele character varying(50) NOT NULL,
    fournisseur character varying(50),
    date_fabrique date NOT NULL,
    date_peremption date NOT NULL,
    stock integer NOT NULL,
    alert integer NOT NULL,
    prix_unitaire numeric(12,2) DEFAULT 0,
    CONSTRAINT valid_dates CHECK ((date_peremption > date_fabrique))
);
    DROP TABLE sge_cre.produits;
       sge_cre         heap    postgres    false    8    985    981            q           0    0    TABLE produits    ACL     G   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.produits TO PUBLIC;
          sge_cre          postgres    false    224            �            1259    19649    rapports_exceptions    TABLE     �  CREATE TABLE sge_cre.rapports_exceptions (
    id_rapport integer NOT NULL,
    id_bon_reception integer,
    id_produit sge_cre.id_prod,
    id_individu integer,
    date date,
    type_exception sge_cre.type_exception NOT NULL,
    processus_concerne character varying(50) NOT NULL,
    produit_concerne character varying(50) NOT NULL,
    observation sge_cre.description,
    detecteur character varying(50) NOT NULL,
    action_entreprise sge_cre.description NOT NULL
);
 (   DROP TABLE sge_cre.rapports_exceptions;
       sge_cre         heap    postgres    false    985    981    961    8    981            r           0    0    TABLE rapports_exceptions    ACL     R   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.rapports_exceptions TO PUBLIC;
          sge_cre          postgres    false    244            �            1259    19648 "   rapports_exceptions_id_rapport_seq    SEQUENCE     �   CREATE SEQUENCE sge_cre.rapports_exceptions_id_rapport_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 :   DROP SEQUENCE sge_cre.rapports_exceptions_id_rapport_seq;
       sge_cre          postgres    false    244    8            s           0    0 "   rapports_exceptions_id_rapport_seq    SEQUENCE OWNED BY     k   ALTER SEQUENCE sge_cre.rapports_exceptions_id_rapport_seq OWNED BY sge_cre.rapports_exceptions.id_rapport;
          sge_cre          postgres    false    243            �            1259    19502 
   receptions    TABLE     �   CREATE TABLE sge_cre.receptions (
    id_reception integer NOT NULL,
    date_reception timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    statut character varying(20) DEFAULT 'en_cours'::character varying
);
    DROP TABLE sge_cre.receptions;
       sge_cre         heap    postgres    false    8            t           0    0    TABLE receptions    ACL     I   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.receptions TO PUBLIC;
          sge_cre          postgres    false    226            �            1259    19501    receptions_id_reception_seq    SEQUENCE     �   CREATE SEQUENCE sge_cre.receptions_id_reception_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE sge_cre.receptions_id_reception_seq;
       sge_cre          postgres    false    8    226            u           0    0    receptions_id_reception_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE sge_cre.receptions_id_reception_seq OWNED BY sge_cre.receptions.id_reception;
          sge_cre          postgres    false    225            �            1259    19530    zone_stockage    TABLE       CREATE TABLE sge_cre.zone_stockage (
    id_zo_stock integer NOT NULL,
    id_entrepot sge_cre.id_lettre NOT NULL,
    id_cellule sge_cre.id_prod NOT NULL,
    e1 character varying(40) NOT NULL,
    e2 character varying(40) NOT NULL,
    e3 character varying(40) NOT NULL
);
 "   DROP TABLE sge_cre.zone_stockage;
       sge_cre         heap    postgres    false    8    1005    985            v           0    0    TABLE zone_stockage    ACL     L   GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE sge_cre.zone_stockage TO PUBLIC;
          sge_cre          postgres    false    230            �            1259    19529    zone_stockage_id_zo_stock_seq    SEQUENCE     �   CREATE SEQUENCE sge_cre.zone_stockage_id_zo_stock_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE sge_cre.zone_stockage_id_zo_stock_seq;
       sge_cre          postgres    false    230    8            w           0    0    zone_stockage_id_zo_stock_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE sge_cre.zone_stockage_id_zo_stock_seq OWNED BY sge_cre.zone_stockage.id_zo_stock;
          sge_cre          postgres    false    229            G           2604    19636 !   bon_expeditions id_bon_expedition    DEFAULT     �   ALTER TABLE ONLY sge_cre.bon_expeditions ALTER COLUMN id_bon_expedition SET DEFAULT nextval('sge_cre.bon_expeditions_id_bon_expedition_seq'::regclass);
 Q   ALTER TABLE sge_cre.bon_expeditions ALTER COLUMN id_bon_expedition DROP DEFAULT;
       sge_cre          postgres    false    241    242    242            E           2604    19581    bon_receptions id_bon_reception    DEFAULT     �   ALTER TABLE ONLY sge_cre.bon_receptions ALTER COLUMN id_bon_reception SET DEFAULT nextval('sge_cre.bon_receptions_id_bon_reception_seq'::regclass);
 O   ALTER TABLE sge_cre.bon_receptions ALTER COLUMN id_bon_reception DROP DEFAULT;
       sge_cre          postgres    false    235    234    235            D           2604    19552    colis id_colis    DEFAULT     r   ALTER TABLE ONLY sge_cre.colis ALTER COLUMN id_colis SET DEFAULT nextval('sge_cre.colis_id_colis_seq'::regclass);
 >   ALTER TABLE sge_cre.colis ALTER COLUMN id_colis DROP DEFAULT;
       sge_cre          postgres    false    232    231    232            <           2604    19417    individus id_individu    DEFAULT     �   ALTER TABLE ONLY sge_cre.individus ALTER COLUMN id_individu SET DEFAULT nextval('sge_cre.individus_id_individu_seq'::regclass);
 E   ALTER TABLE sge_cre.individus ALTER COLUMN id_individu DROP DEFAULT;
       sge_cre          postgres    false    220    219    220            P           2604    41000    logs_activite id    DEFAULT     v   ALTER TABLE ONLY sge_cre.logs_activite ALTER COLUMN id SET DEFAULT nextval('sge_cre.logs_activite_id_seq'::regclass);
 @   ALTER TABLE sge_cre.logs_activite ALTER COLUMN id DROP DEFAULT;
       sge_cre          postgres    false    250    251    251            =           2604    19428    magasiniers id_magasinier    DEFAULT     �   ALTER TABLE ONLY sge_cre.magasiniers ALTER COLUMN id_magasinier SET DEFAULT nextval('sge_cre.magasiniers_id_magasinier_seq'::regclass);
 I   ALTER TABLE sge_cre.magasiniers ALTER COLUMN id_magasinier DROP DEFAULT;
       sge_cre          postgres    false    222    221    222            F           2604    19602    materiel_emballage id_emballeur    DEFAULT     �   ALTER TABLE ONLY sge_cre.materiel_emballage ALTER COLUMN id_emballeur SET DEFAULT nextval('sge_cre.materiel_emballage_id_emballeur_seq'::regclass);
 O   ALTER TABLE sge_cre.materiel_emballage ALTER COLUMN id_emballeur DROP DEFAULT;
       sge_cre          postgres    false    236    237    237            J           2604    24594    mouvements id    DEFAULT     p   ALTER TABLE ONLY sge_cre.mouvements ALTER COLUMN id SET DEFAULT nextval('sge_cre.mouvements_id_seq'::regclass);
 =   ALTER TABLE sge_cre.mouvements ALTER COLUMN id DROP DEFAULT;
       sge_cre          postgres    false    247    246    247            L           2604    24604    products id    DEFAULT     l   ALTER TABLE ONLY sge_cre.products ALTER COLUMN id SET DEFAULT nextval('sge_cre.products_id_seq'::regclass);
 ;   ALTER TABLE sge_cre.products ALTER COLUMN id DROP DEFAULT;
       sge_cre          postgres    false    249    248    249            I           2604    19652    rapports_exceptions id_rapport    DEFAULT     �   ALTER TABLE ONLY sge_cre.rapports_exceptions ALTER COLUMN id_rapport SET DEFAULT nextval('sge_cre.rapports_exceptions_id_rapport_seq'::regclass);
 N   ALTER TABLE sge_cre.rapports_exceptions ALTER COLUMN id_rapport DROP DEFAULT;
       sge_cre          postgres    false    244    243    244            @           2604    19505    receptions id_reception    DEFAULT     �   ALTER TABLE ONLY sge_cre.receptions ALTER COLUMN id_reception SET DEFAULT nextval('sge_cre.receptions_id_reception_seq'::regclass);
 G   ALTER TABLE sge_cre.receptions ALTER COLUMN id_reception DROP DEFAULT;
       sge_cre          postgres    false    225    226    226            C           2604    19533    zone_stockage id_zo_stock    DEFAULT     �   ALTER TABLE ONLY sge_cre.zone_stockage ALTER COLUMN id_zo_stock SET DEFAULT nextval('sge_cre.zone_stockage_id_zo_stock_seq'::regclass);
 I   ALTER TABLE sge_cre.zone_stockage ALTER COLUMN id_zo_stock DROP DEFAULT;
       sge_cre          postgres    false    229    230    230            D          0    19633    bon_expeditions 
   TABLE DATA                 sge_cre          postgres    false    242   B�       =          0    19578    bon_receptions 
   TABLE DATA                 sge_cre          postgres    false    235   �       5          0    19510    cellules 
   TABLE DATA                 sge_cre          postgres    false    227   ��       :          0    19549    colis 
   TABLE DATA                 sge_cre          postgres    false    232   F�       @          0    19607 	   commandes 
   TABLE DATA                 sge_cre          postgres    false    238   U�       A          0    19612    commandes_achats 
   TABLE DATA                 sge_cre          postgres    false    239   ��       B          0    19622    commandes_vends 
   TABLE DATA                 sge_cre          postgres    false    240   y�       6          0    19517 	   entrepots 
   TABLE DATA                 sge_cre          postgres    false    228   #�       .          0    19414 	   individus 
   TABLE DATA                 sge_cre          postgres    false    220   2�       L          0    40997    logs_activite 
   TABLE DATA                 sge_cre          postgres    false    251   ��       ;          0    19565    lots 
   TABLE DATA                 sge_cre          postgres    false    233   ��       0          0    19425    magasiniers 
   TABLE DATA                 sge_cre          postgres    false    222   ��       ?          0    19599    materiel_emballage 
   TABLE DATA                 sge_cre          postgres    false    237   ��       H          0    24591 
   mouvements 
   TABLE DATA                 sge_cre          postgres    false    247   O�       ,          0    19404    organisations 
   TABLE DATA                 sge_cre          postgres    false    218   ��       J          0    24601    products 
   TABLE DATA                 sge_cre          postgres    false    249   C�       2          0    19493    produits 
   TABLE DATA                 sge_cre          postgres    false    224   �       F          0    19649    rapports_exceptions 
   TABLE DATA                 sge_cre          postgres    false    244   �       4          0    19502 
   receptions 
   TABLE DATA                 sge_cre          postgres    false    226    �       1          0    19475 
   repertoire 
   TABLE DATA                 sge_cre          postgres    false    223   ��       8          0    19530    zone_stockage 
   TABLE DATA                 sge_cre          postgres    false    230   ;�       x           0    0 %   bon_expeditions_id_bon_expedition_seq    SEQUENCE SET     T   SELECT pg_catalog.setval('sge_cre.bon_expeditions_id_bon_expedition_seq', 1, true);
          sge_cre          postgres    false    241            y           0    0 #   bon_receptions_id_bon_reception_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('sge_cre.bon_receptions_id_bon_reception_seq', 2, true);
          sge_cre          postgres    false    234            z           0    0    colis_id_colis_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('sge_cre.colis_id_colis_seq', 37, true);
          sge_cre          postgres    false    231            {           0    0    individus_id_individu_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('sge_cre.individus_id_individu_seq', 11, true);
          sge_cre          postgres    false    219            |           0    0    logs_activite_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('sge_cre.logs_activite_id_seq', 1, false);
          sge_cre          postgres    false    250            }           0    0    magasiniers_id_magasinier_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('sge_cre.magasiniers_id_magasinier_seq', 1, false);
          sge_cre          postgres    false    221            ~           0    0 #   materiel_emballage_id_emballeur_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('sge_cre.materiel_emballage_id_emballeur_seq', 7, true);
          sge_cre          postgres    false    236                       0    0    mouvements_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('sge_cre.mouvements_id_seq', 1, false);
          sge_cre          postgres    false    246            �           0    0    products_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('sge_cre.products_id_seq', 1, false);
          sge_cre          postgres    false    248            �           0    0 "   rapports_exceptions_id_rapport_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('sge_cre.rapports_exceptions_id_rapport_seq', 1, false);
          sge_cre          postgres    false    243            �           0    0    receptions_id_reception_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('sge_cre.receptions_id_reception_seq', 10, true);
          sge_cre          postgres    false    225            �           0    0    zone_stockage_id_zo_stock_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('sge_cre.zone_stockage_id_zo_stock_seq', 7, true);
          sge_cre          postgres    false    229            ~           2606    19640 $   bon_expeditions bon_expeditions_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY sge_cre.bon_expeditions
    ADD CONSTRAINT bon_expeditions_pkey PRIMARY KEY (id_bon_expedition);
 O   ALTER TABLE ONLY sge_cre.bon_expeditions DROP CONSTRAINT bon_expeditions_pkey;
       sge_cre            postgres    false    242            �           2606    40986 6   bon_expeditions bon_expeditions_reference_commande_key 
   CONSTRAINT     �   ALTER TABLE ONLY sge_cre.bon_expeditions
    ADD CONSTRAINT bon_expeditions_reference_commande_key UNIQUE (reference_commande);
 a   ALTER TABLE ONLY sge_cre.bon_expeditions DROP CONSTRAINT bon_expeditions_reference_commande_key;
       sge_cre            postgres    false    242            r           2606    19585 "   bon_receptions bon_receptions_pkey 
   CONSTRAINT     o   ALTER TABLE ONLY sge_cre.bon_receptions
    ADD CONSTRAINT bon_receptions_pkey PRIMARY KEY (id_bon_reception);
 M   ALTER TABLE ONLY sge_cre.bon_receptions DROP CONSTRAINT bon_receptions_pkey;
       sge_cre            postgres    false    235            t           2606    19587 4   bon_receptions bon_receptions_reference_commande_key 
   CONSTRAINT     ~   ALTER TABLE ONLY sge_cre.bon_receptions
    ADD CONSTRAINT bon_receptions_reference_commande_key UNIQUE (reference_commande);
 _   ALTER TABLE ONLY sge_cre.bon_receptions DROP CONSTRAINT bon_receptions_reference_commande_key;
       sge_cre            postgres    false    235            h           2606    19516    cellules cellules_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY sge_cre.cellules
    ADD CONSTRAINT cellules_pkey PRIMARY KEY (id_cellule);
 A   ALTER TABLE ONLY sge_cre.cellules DROP CONSTRAINT cellules_pkey;
       sge_cre            postgres    false    227            n           2606    19554    colis colis_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY sge_cre.colis
    ADD CONSTRAINT colis_pkey PRIMARY KEY (id_colis);
 ;   ALTER TABLE ONLY sge_cre.colis DROP CONSTRAINT colis_pkey;
       sge_cre            postgres    false    232            z           2606    19616 &   commandes_achats commandes_achats_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY sge_cre.commandes_achats
    ADD CONSTRAINT commandes_achats_pkey PRIMARY KEY (id_commande);
 Q   ALTER TABLE ONLY sge_cre.commandes_achats DROP CONSTRAINT commandes_achats_pkey;
       sge_cre            postgres    false    239            x           2606    19611    commandes commandes_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY sge_cre.commandes
    ADD CONSTRAINT commandes_pkey PRIMARY KEY (id_commandes);
 C   ALTER TABLE ONLY sge_cre.commandes DROP CONSTRAINT commandes_pkey;
       sge_cre            postgres    false    238            |           2606    19626 $   commandes_vends commandes_vends_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY sge_cre.commandes_vends
    ADD CONSTRAINT commandes_vends_pkey PRIMARY KEY (id_commande);
 O   ALTER TABLE ONLY sge_cre.commandes_vends DROP CONSTRAINT commandes_vends_pkey;
       sge_cre            postgres    false    240            j           2606    19523    entrepots entrepots_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY sge_cre.entrepots
    ADD CONSTRAINT entrepots_pkey PRIMARY KEY (id_entrepot);
 C   ALTER TABLE ONLY sge_cre.entrepots DROP CONSTRAINT entrepots_pkey;
       sge_cre            postgres    false    228            Y           2606    19423    individus individus_email_key 
   CONSTRAINT     Z   ALTER TABLE ONLY sge_cre.individus
    ADD CONSTRAINT individus_email_key UNIQUE (email);
 H   ALTER TABLE ONLY sge_cre.individus DROP CONSTRAINT individus_email_key;
       sge_cre            postgres    false    220            [           2606    19421    individus individus_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY sge_cre.individus
    ADD CONSTRAINT individus_pkey PRIMARY KEY (id_individu);
 C   ALTER TABLE ONLY sge_cre.individus DROP CONSTRAINT individus_pkey;
       sge_cre            postgres    false    220            �           2606    41006     logs_activite logs_activite_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY sge_cre.logs_activite
    ADD CONSTRAINT logs_activite_pkey PRIMARY KEY (id);
 K   ALTER TABLE ONLY sge_cre.logs_activite DROP CONSTRAINT logs_activite_pkey;
       sge_cre            postgres    false    251            p           2606    19571    lots lots_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY sge_cre.lots
    ADD CONSTRAINT lots_pkey PRIMARY KEY (id_lot);
 9   ALTER TABLE ONLY sge_cre.lots DROP CONSTRAINT lots_pkey;
       sge_cre            postgres    false    233            ]           2606    19432 '   magasiniers magasiniers_id_individu_key 
   CONSTRAINT     j   ALTER TABLE ONLY sge_cre.magasiniers
    ADD CONSTRAINT magasiniers_id_individu_key UNIQUE (id_individu);
 R   ALTER TABLE ONLY sge_cre.magasiniers DROP CONSTRAINT magasiniers_id_individu_key;
       sge_cre            postgres    false    222            _           2606    19430    magasiniers magasiniers_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY sge_cre.magasiniers
    ADD CONSTRAINT magasiniers_pkey PRIMARY KEY (id_magasinier);
 G   ALTER TABLE ONLY sge_cre.magasiniers DROP CONSTRAINT magasiniers_pkey;
       sge_cre            postgres    false    222            v           2606    19606 *   materiel_emballage materiel_emballage_pkey 
   CONSTRAINT     s   ALTER TABLE ONLY sge_cre.materiel_emballage
    ADD CONSTRAINT materiel_emballage_pkey PRIMARY KEY (id_emballeur);
 U   ALTER TABLE ONLY sge_cre.materiel_emballage DROP CONSTRAINT materiel_emballage_pkey;
       sge_cre            postgres    false    237            �           2606    24599    mouvements mouvements_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY sge_cre.mouvements
    ADD CONSTRAINT mouvements_pkey PRIMARY KEY (id);
 E   ALTER TABLE ONLY sge_cre.mouvements DROP CONSTRAINT mouvements_pkey;
       sge_cre            postgres    false    247            V           2606    19412     organisations organisations_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY sge_cre.organisations
    ADD CONSTRAINT organisations_pkey PRIMARY KEY (id_organisation);
 K   ALTER TABLE ONLY sge_cre.organisations DROP CONSTRAINT organisations_pkey;
       sge_cre            postgres    false    218            �           2606    24613    products products_code_key 
   CONSTRAINT     V   ALTER TABLE ONLY sge_cre.products
    ADD CONSTRAINT products_code_key UNIQUE (code);
 E   ALTER TABLE ONLY sge_cre.products DROP CONSTRAINT products_code_key;
       sge_cre            postgres    false    249            �           2606    24611    products products_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY sge_cre.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);
 A   ALTER TABLE ONLY sge_cre.products DROP CONSTRAINT products_pkey;
       sge_cre            postgres    false    249            d           2606    19500    produits produits_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY sge_cre.produits
    ADD CONSTRAINT produits_pkey PRIMARY KEY (id_produit);
 A   ALTER TABLE ONLY sge_cre.produits DROP CONSTRAINT produits_pkey;
       sge_cre            postgres    false    224            �           2606    19656 ,   rapports_exceptions rapports_exceptions_pkey 
   CONSTRAINT     s   ALTER TABLE ONLY sge_cre.rapports_exceptions
    ADD CONSTRAINT rapports_exceptions_pkey PRIMARY KEY (id_rapport);
 W   ALTER TABLE ONLY sge_cre.rapports_exceptions DROP CONSTRAINT rapports_exceptions_pkey;
       sge_cre            postgres    false    244            f           2606    19509    receptions receptions_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY sge_cre.receptions
    ADD CONSTRAINT receptions_pkey PRIMARY KEY (id_reception);
 E   ALTER TABLE ONLY sge_cre.receptions DROP CONSTRAINT receptions_pkey;
       sge_cre            postgres    false    226            a           2606    19482    repertoire repertoire_pkey 
   CONSTRAINT     s   ALTER TABLE ONLY sge_cre.repertoire
    ADD CONSTRAINT repertoire_pkey PRIMARY KEY (id_organisation, id_individu);
 E   ALTER TABLE ONLY sge_cre.repertoire DROP CONSTRAINT repertoire_pkey;
       sge_cre            postgres    false    223    223            l           2606    19537     zone_stockage zone_stockage_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY sge_cre.zone_stockage
    ADD CONSTRAINT zone_stockage_pkey PRIMARY KEY (id_zo_stock);
 K   ALTER TABLE ONLY sge_cre.zone_stockage DROP CONSTRAINT zone_stockage_pkey;
       sge_cre            postgres    false    230            W           1259    19673    idx_individus_email    INDEX     K   CREATE INDEX idx_individus_email ON sge_cre.individus USING btree (email);
 (   DROP INDEX sge_cre.idx_individus_email;
       sge_cre            postgres    false    220            b           1259    19672    idx_produits_nom    INDEX     E   CREATE INDEX idx_produits_nom ON sge_cre.produits USING btree (nom);
 %   DROP INDEX sge_cre.idx_produits_nom;
       sge_cre            postgres    false    224            �           2606    19643 -   bon_expeditions bon_expeditions_id_colis_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.bon_expeditions
    ADD CONSTRAINT bon_expeditions_id_colis_fkey FOREIGN KEY (id_colis) REFERENCES sge_cre.colis(id_colis) ON DELETE SET NULL;
 X   ALTER TABLE ONLY sge_cre.bon_expeditions DROP CONSTRAINT bon_expeditions_id_colis_fkey;
       sge_cre          postgres    false    4974    232    242            �           2606    19593 0   bon_receptions bon_receptions_id_magasinier_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.bon_receptions
    ADD CONSTRAINT bon_receptions_id_magasinier_fkey FOREIGN KEY (id_magasinier) REFERENCES sge_cre.individus(id_individu) ON DELETE SET NULL;
 [   ALTER TABLE ONLY sge_cre.bon_receptions DROP CONSTRAINT bon_receptions_id_magasinier_fkey;
       sge_cre          postgres    false    4955    235    220            �           2606    19588 /   bon_receptions bon_receptions_id_reception_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.bon_receptions
    ADD CONSTRAINT bon_receptions_id_reception_fkey FOREIGN KEY (id_reception) REFERENCES sge_cre.receptions(id_reception) ON DELETE SET NULL;
 Z   ALTER TABLE ONLY sge_cre.bon_receptions DROP CONSTRAINT bon_receptions_id_reception_fkey;
       sge_cre          postgres    false    4966    226    235            �           2606    19560    colis colis_id_reception_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.colis
    ADD CONSTRAINT colis_id_reception_fkey FOREIGN KEY (id_reception) REFERENCES sge_cre.receptions(id_reception) ON DELETE CASCADE;
 H   ALTER TABLE ONLY sge_cre.colis DROP CONSTRAINT colis_id_reception_fkey;
       sge_cre          postgres    false    4966    226    232            �           2606    19555    colis colis_id_zo_stock_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.colis
    ADD CONSTRAINT colis_id_zo_stock_fkey FOREIGN KEY (id_zo_stock) REFERENCES sge_cre.zone_stockage(id_zo_stock) ON DELETE CASCADE;
 G   ALTER TABLE ONLY sge_cre.colis DROP CONSTRAINT colis_id_zo_stock_fkey;
       sge_cre          postgres    false    232    230    4972            �           2606    19617 2   commandes_achats commandes_achats_id_commande_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.commandes_achats
    ADD CONSTRAINT commandes_achats_id_commande_fkey FOREIGN KEY (id_commande) REFERENCES sge_cre.commandes(id_commandes) ON DELETE CASCADE;
 ]   ALTER TABLE ONLY sge_cre.commandes_achats DROP CONSTRAINT commandes_achats_id_commande_fkey;
       sge_cre          postgres    false    4984    238    239            �           2606    19627 0   commandes_vends commandes_vends_id_commande_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.commandes_vends
    ADD CONSTRAINT commandes_vends_id_commande_fkey FOREIGN KEY (id_commande) REFERENCES sge_cre.commandes(id_commandes) ON DELETE CASCADE;
 [   ALTER TABLE ONLY sge_cre.commandes_vends DROP CONSTRAINT commandes_vends_id_commande_fkey;
       sge_cre          postgres    false    240    238    4984            �           2606    19524 (   entrepots entrepots_id_organisation_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.entrepots
    ADD CONSTRAINT entrepots_id_organisation_fkey FOREIGN KEY (id_organisation) REFERENCES sge_cre.organisations(id_organisation) ON DELETE CASCADE;
 S   ALTER TABLE ONLY sge_cre.entrepots DROP CONSTRAINT entrepots_id_organisation_fkey;
       sge_cre          postgres    false    228    4950    218            �           2606    19572    lots lots_id_produit_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.lots
    ADD CONSTRAINT lots_id_produit_fkey FOREIGN KEY (id_produit) REFERENCES sge_cre.produits(id_produit) ON DELETE CASCADE;
 D   ALTER TABLE ONLY sge_cre.lots DROP CONSTRAINT lots_id_produit_fkey;
       sge_cre          postgres    false    233    4964    224            �           2606    19433 (   magasiniers magasiniers_id_individu_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.magasiniers
    ADD CONSTRAINT magasiniers_id_individu_fkey FOREIGN KEY (id_individu) REFERENCES sge_cre.individus(id_individu) ON DELETE CASCADE;
 S   ALTER TABLE ONLY sge_cre.magasiniers DROP CONSTRAINT magasiniers_id_individu_fkey;
       sge_cre          postgres    false    222    220    4955            �           2606    19667 =   rapports_exceptions rapports_exceptions_id_bon_reception_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.rapports_exceptions
    ADD CONSTRAINT rapports_exceptions_id_bon_reception_fkey FOREIGN KEY (id_bon_reception) REFERENCES sge_cre.bon_receptions(id_bon_reception) ON DELETE SET NULL;
 h   ALTER TABLE ONLY sge_cre.rapports_exceptions DROP CONSTRAINT rapports_exceptions_id_bon_reception_fkey;
       sge_cre          postgres    false    235    244    4978            �           2606    19657 8   rapports_exceptions rapports_exceptions_id_individu_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.rapports_exceptions
    ADD CONSTRAINT rapports_exceptions_id_individu_fkey FOREIGN KEY (id_individu) REFERENCES sge_cre.individus(id_individu) ON DELETE SET NULL;
 c   ALTER TABLE ONLY sge_cre.rapports_exceptions DROP CONSTRAINT rapports_exceptions_id_individu_fkey;
       sge_cre          postgres    false    244    4955    220            �           2606    19662 7   rapports_exceptions rapports_exceptions_id_produit_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.rapports_exceptions
    ADD CONSTRAINT rapports_exceptions_id_produit_fkey FOREIGN KEY (id_produit) REFERENCES sge_cre.produits(id_produit) ON DELETE SET NULL;
 b   ALTER TABLE ONLY sge_cre.rapports_exceptions DROP CONSTRAINT rapports_exceptions_id_produit_fkey;
       sge_cre          postgres    false    4964    244    224            �           2606    19488 &   repertoire repertoire_id_individu_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.repertoire
    ADD CONSTRAINT repertoire_id_individu_fkey FOREIGN KEY (id_individu) REFERENCES sge_cre.individus(id_individu) ON DELETE CASCADE;
 Q   ALTER TABLE ONLY sge_cre.repertoire DROP CONSTRAINT repertoire_id_individu_fkey;
       sge_cre          postgres    false    223    220    4955            �           2606    19483 *   repertoire repertoire_id_organisation_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.repertoire
    ADD CONSTRAINT repertoire_id_organisation_fkey FOREIGN KEY (id_organisation) REFERENCES sge_cre.organisations(id_organisation) ON DELETE CASCADE;
 U   ALTER TABLE ONLY sge_cre.repertoire DROP CONSTRAINT repertoire_id_organisation_fkey;
       sge_cre          postgres    false    223    4950    218            �           2606    19538 +   zone_stockage zone_stockage_id_cellule_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.zone_stockage
    ADD CONSTRAINT zone_stockage_id_cellule_fkey FOREIGN KEY (id_cellule) REFERENCES sge_cre.cellules(id_cellule) ON DELETE CASCADE;
 V   ALTER TABLE ONLY sge_cre.zone_stockage DROP CONSTRAINT zone_stockage_id_cellule_fkey;
       sge_cre          postgres    false    227    4968    230            �           2606    19543 ,   zone_stockage zone_stockage_id_entrepot_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY sge_cre.zone_stockage
    ADD CONSTRAINT zone_stockage_id_entrepot_fkey FOREIGN KEY (id_entrepot) REFERENCES sge_cre.entrepots(id_entrepot) ON DELETE CASCADE;
 W   ALTER TABLE ONLY sge_cre.zone_stockage DROP CONSTRAINT zone_stockage_id_entrepot_fkey;
       sge_cre          postgres    false    228    4970    230            �           826    19361    DEFAULT PRIVILEGES FOR TABLES    DEFAULT ACL     t   ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA sge_cre GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES TO PUBLIC;
          sge_cre          postgres    false    8            D   �   x���=�0��_q���
���G�D��WR�!�@	u�/5��p�{s��_b%�_�+��g���r�d�oy!�B6
n� �1L�,\�3�*��9VD��9ȳl;DW(E�րɣ�`/+1Y鏞�) ڷWJg-�4ܜn�AX��*)��%�q�嗓��^9S�0��L�      =   �   x���v
Q���W(NO�O.J�K�ϋ/JMN-(���+Vs�	uV�0�Q04�Q����QP7202�50�5�T�<���r!�K
r��M�+I�,J	)�$*^	5TOO��-81��4/]n�S�����5 ��/t      5   �   x���v
Q���W(NO�O.J�KN��)�I-Vs�	uV�Pw600T�Q042�35�Q�0�3 Rf�� DkZsyk��,�nsS�!�ĔT��AfB̲�b3�T�L�fYB4���q�^49���� �H3��2C
.t�d?�a ��3      :   �   x���=k�0�ݿ�6����2e�`0�k��!�R(	4�*$��p��=>�����x<Ӵ���\?�?kw~�躟/���P)�����I:�#oFn�wͤ
�P�P���,8L��J���X��*�� 8�����C���3�`h��sz��ɹ�;����|��G���7rVq<�����G@�+N �^q"���g:Qˡ!5������"�`���iC��P3�j����X��XW��ԺϊJ�������      @   n   x���v
Q���W(NO�O.J�K���M�KI-Vs�	uV�Pw�u10T�Q04 bS=Mk.O�uu�t�����h YV� 5[ m� G�)��@��ູ�  kSF      A   �   x���v
Q���W(NO�O.J�K���M�KI-�OL�H,)Vs�	uV�Pw�u10T�QP7202�50Ӆ�R��KJR�JR�<CMk.O��5B1�K�(HM��iD���(f�yE�ɥ@ڔ,�LP����Js@N� �DSM1�P.. �w]      B   �   x���v
Q���W(NO�O.J�K���M�KI-�/K�K)Vs�	uV�Pw�u10T�QP7202�50"/�� 5%3�4մ��$�D#��&��'���敀54 �TcS-@����R mL�q&(�Y�x�yy�9 ��c�)�����h4�� �4t#      6   �   x����N�0�=O�]51��r58!3�$�̑)�=؋���7��,0!������I�ŧ�$i~$�b�d�Lh�ZԊ����8#74Ns���;B�������W�V��6�NC�um��e�6t� ����}p��7�ޒ�%�-%/��������a-�Ϡ�����Amo3����N���=H+�u����)�fŧ���æEB/N�D�4k�p6��r�%��~��h����yC��Tʲ?      .   G  x���ю�@��}
�l���
��Mݭݸqݍkm�7f�)�����o���u挨�MC��������-��˕3[���M$�"�=ĥr֓�����{�tȳ�w����Y�
x��En��)��0��f�$�A�*$+x)͛`��~0�����U���άV_�\K��*4�B�t�/��˱T��p�̈%W;��ߨ�TY2�+�e{��ny��>��lV�K�]��@����沠�X�4���b�a���KnɈ��+���Ɇ��q�$�L�\�`��q��`�o�yȴ땁��c{�,B���J;�ホ�k6N�B2�*�W�0�sŏ@g�FТ=P`Ҁ�)�`A�p�X�|��*=��<f�/9��9F&[	�~d�e!��#�'�h�\������e��!�}��o�����w1����k���c�m=S7���"��o��aO_g���|cç����GB������߱�47[3��RX��tԀzn��t�G�cJa���g=�(m�+�
��m�4�����?�I�����h��R��	�)�iJt�e�ɂ <�A�z���i��      L   
   x���          ;   �   x����j�0��>Ź��2�t����A��غ�ѥA5�9�C���h�,z���$��e	٬����r��i=��k��0"��d��Y,'!�vmM��[0!)㔳���q�°�Z�j{�U�F�/Iv�)3�{�9k�V�3U��}�Z�u��^旅�^�U��ĩ�͟�I%�W��7�rb�;���Ѧ)e}{d���~;����7�rp�nJ��[����¨*k��I��Q�U      0   
   x���          ?   �   x���v
Q���W(NO�O.J��M,I-�L͉O�MJ��ILOUs�	uV�0�QPw��,IU2�RK��5��<I3���1%#�8�lLPjriAjQ*F��SZT��E& ��Q�S�С�3*�c��.. fg�N      H   �  x����J�0����
N��U�WsؠNY7o�̃�d&��G�s��<�n�O2�Er�)�}_��'�`:��dv��OsS�0G]8��&�A
G���.l]ap�y�P!5��̲��%B��fĨ5یq:C���9,�f$x4��nw�s��F0�o��E�-_�����AjY�Ly��g򥪫�������*��򛈞�V-��+�R���Ŗ�j�MѮ�a<�G�ø�!O��f�����`�N��׆��K�`ԧ�ءw~[�f�+��VQo��gd@̣/��ڈ9XD�`��$Y!���<�R��h����Ņ��^��8����o�k����5��˜O}j�;܏ڜ1�p�y���4�{ �Y�9p�M��8�4������j} 5i!%      ,   F  x��S�J1��+��Z2��<��Z�ն
��ع�������'�����B� ��Ir.��{RM�قT�Ŕ��-zWBI#��ʐ����hN���lLiuIt�W�q&�o�R������Fh���p���'�I��v�p�!�'	M�!��"4��ϊ^�2���R~�ԩ�h���@����R8s@j M6�$v�P;ѴwY��%1��5�7|'X�:���Ǡ,�&�K'�J@r�����w��R	+$���N�_a��|(4�O������ 8��,�b;A�N��2������^�X���.�<ϼ�m����t^�|�\      J   �  x���Mn�0��>���f@R�e�+�V##�!"�vW� �Ut)�A�У��X�J�]e��3��{o6I�ma�lSh��o�)��F��k��>�L�A�8clN(eS�d�7U��U?��e]c�q9N�P�1�<�����|��mm�S.	u� ��R^���K�\N?~�l����P�[�����Ui`��*�,\d�����cE��l��.F�X7UW�>�u�ky� '+�Hڹ�߅ɛK��Ѳ�S�T�0�$����c	������v�v05Ǫ�-����Qz�!���/B��G�����C��ML�g��QB����_�zJE��W���~ e401��,� +���+�Ze��+ه�Rm1D;o�e������!�G����q���X�-�}�mpG��_��(��F�y����w�d�m��z�7�^0EQ����[��L�pY4      2   �  x���͎�0��y��K+��&@f�3!S�$E�N6�����1��R��/V�P��,�"!�6���!ޥ�>�x���&g��b�Z�C�u���]�i�_����%9q��������l����@�Ɍ��l�b��;62����w^�{�VD�n��܅�|��
�]4���h���W��_�];j��
i��U�$��
�j'C�4KJ���-����+4�BT2���6=�� �`ԫ�Ay�{�sw���2N��Κ�р �}(<q訳��pq�e�ha>J��G��Z%����	}5��?׿ڳ�n��Lq쫹��Y�|2,�.2G@N�-��(R������p˭T�ݬO�Aud-�?(l�����[\ՊWD���9C�ރJ
I%+U[j�(�\
��u����{�4l�	���Q<�!t>���v�����_��9%���m%��H�L�]������¤tp1Fc���=	%�      F   
   x���          4   �   x���v
Q���W(NO�O.J�+JMN-(���+Vs�	uV�0�QP7202�50�54P00�#mCu�Lj^|r~iQ���5�'q!hJ���S�@$���BS��ƺ�FT0�� n����%��FPKJR�JRAfrq �E��      1   i   x���v
Q���W(NO�O.J�+J-H-*��,JUs�	uV�P�r700T�Q0�QP7202�50"uMk.OR�0aD��@#�)3�h�	eF��0�0�� �Z`      8   �   x���v
Q���W(NO�O.Jի��K�/.�O�NLOUs�	uV�0�QPw�100T���tP��#��X��� <�Y�i��i��I�F�a���#�,0�Y`��n�U|`�n�	6����)�c��p��^Y�ZT�J���#��ʱl�n�9Qpq $?�2     