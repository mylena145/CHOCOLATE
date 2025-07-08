#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des matricules basé sur les rôles
Génère automatiquement des matricules uniques selon le rôle de l'utilisateur
"""

import psycopg2
import unicodedata
import re
from typing import Optional, Dict, List, Tuple

# Configuration de la base de données
PG_CONN = dict(
    dbname="postgres",
    user="postgres",
    password="postgres123",
    host="localhost",
    port="5432",
    client_encoding="utf8",
    options="-c client_encoding=utf8",
    connect_timeout=10
)

class MatriculeManager:
    """Gestionnaire de matricules basé sur les rôles"""
    
    # Mapping des rôles vers les préfixes de matricules
    ROLE_PREFIXES = {
        # Rôles de gestion et responsabilité
        "Responsable des stocks": "RS",
        "Responsable de la logistique": "RL",
        "Responsable informatique": "RI",
        "Responsable de la sécurité physique": "RP",
        
        # Rôles opérationnels
        "Magasinier": "MG",
        "Emballeur": "EM",
        "Agent de logistique": "AL",
        "Livreur": "LV",
        "Technicien informatique": "TI",
        "Garde de sécurité": "GS",
        
        # Rôles administratifs (pour compatibilité)
        "Super Administrateur": "SA",
        "Administrateur": "AD",
        "Gestionnaire Entrepôt": "GE",
        
        # Rôles spécialisés (pour compatibilité)
        "Consultant": "CO",
        "Stagiaire": "ST",
        "Fournisseur": "FR",
        "Client": "CL",
        
        # Rôle par défaut (si le rôle n'est pas dans la liste)
        "default": "US"
    }
    
    @staticmethod
    def get_role_prefix(role: str) -> str:
        """
        Retourne le préfixe de matricule pour un rôle donné
        
        Args:
            role (str): Le nom du rôle
            
        Returns:
            str: Le préfixe de matricule (2 lettres)
        """
        # Normaliser le rôle (supprimer accents, espaces, majuscules)
        normalized_role = unicodedata.normalize('NFD', role).encode('ascii', 'ignore').decode('utf-8')
        normalized_role = normalized_role.strip().upper()
        
        # Chercher dans le mapping exact (comparaison insensible à la casse)
        for role_name, prefix in MatriculeManager.ROLE_PREFIXES.items():
            if role_name.upper() == normalized_role:
                return prefix
        
        # Si pas trouvé, essayer une correspondance partielle
        for role_name, prefix in MatriculeManager.ROLE_PREFIXES.items():
            if role_name.upper() in normalized_role or normalized_role in role_name.upper():
                return prefix
        
        # Si pas trouvé, essayer une correspondance par mots-clés
        role_words = normalized_role.split()
        for role_name, prefix in MatriculeManager.ROLE_PREFIXES.items():
            role_name_words = role_name.upper().split()
            if any(word in role_name_words for word in role_words) or any(word in role_words for word in role_name_words):
                return prefix
        
        # Si pas trouvé, utiliser les 2 premières lettres du rôle normalisé
        if len(normalized_role) >= 2:
            return normalized_role[:2]
        
        # Fallback
        return MatriculeManager.ROLE_PREFIXES["default"]
    
    @staticmethod
    def generate_matricule(role: str) -> str:
        """
        Génère un matricule unique pour un rôle donné
        
        Args:
            role (str): Le nom du rôle
            
        Returns:
            str: Le matricule généré (format: XX001, XX002, etc.)
        """
        prefix = MatriculeManager.get_role_prefix(role)
        
        try:
            conn = psycopg2.connect(**PG_CONN)
            cursor = conn.cursor()
            
            # Chercher le dernier matricule avec ce préfixe
            cursor.execute("""
                SELECT matricule 
                FROM sge_cre.individus 
                WHERE matricule LIKE %s 
                ORDER BY matricule DESC 
                LIMIT 1
            """, (f"{prefix}%",))
            
            last_matricule = cursor.fetchone()
            conn.close()
            
            if last_matricule and last_matricule[0]:
                # Extraire le numéro du dernier matricule
                last_num = MatriculeManager._extract_number_from_matricule(last_matricule[0], prefix)
                if last_num is not None:
                    next_num = last_num + 1
                else:
                    next_num = 1
            else:
                next_num = 1
            
            # Formater le matricule (XX001, XX002, etc.)
            return f"{prefix}{next_num:03d}"
            
        except Exception as e:
            print(f"Erreur lors de la génération du matricule: {e}")
            # En cas d'erreur, retourner un matricule par défaut
            return f"{prefix}001"
    
    @staticmethod
    def _extract_number_from_matricule(matricule: str, prefix: str) -> Optional[int]:
        """
        Extrait le numéro d'un matricule existant
        
        Args:
            matricule (str): Le matricule complet
            prefix (str): Le préfixe attendu
            
        Returns:
            Optional[int]: Le numéro extrait ou None si invalide
        """
        if not matricule or len(matricule) < len(prefix) + 1:
            return None
        
        # Vérifier que le matricule commence par le bon préfixe
        if not matricule.startswith(prefix):
            return None
        
        # Extraire la partie numérique
        numeric_part = matricule[len(prefix):]
        
        # Vérifier que c'est bien un nombre
        if numeric_part.isdigit():
            return int(numeric_part)
        
        return None
    
    @staticmethod
    def get_role_from_matricule(matricule: str) -> Optional[str]:
        """
        Identifie le rôle probable d'un utilisateur à partir de son matricule
        
        Args:
            matricule (str): Le matricule à analyser
            
        Returns:
            Optional[str]: Le rôle probable ou None si non trouvé
        """
        if not matricule or len(matricule) < 2:
            return None
        
        prefix = matricule[:2].upper()
        
        # Chercher le rôle correspondant au préfixe
        for role_name, role_prefix in MatriculeManager.ROLE_PREFIXES.items():
            if role_prefix == prefix:
                return role_name
        
        return None
    
    @staticmethod
    def validate_matricule(matricule: str) -> Tuple[bool, str]:
        """
        Valide un matricule
        
        Args:
            matricule (str): Le matricule à valider
            
        Returns:
            Tuple[bool, str]: (valide, message d'erreur)
        """
        if not matricule:
            return False, "Le matricule ne peut pas être vide"
        
        if len(matricule) < 5:
            return False, "Le matricule doit contenir au moins 5 caractères"
        
        if len(matricule) > 10:
            return False, "Le matricule ne peut pas dépasser 10 caractères"
        
        # Vérifier le format: 2 lettres + chiffres
        if not re.match(r'^[A-Z]{2}\d{3,8}$', matricule.upper()):
            return False, "Format invalide: 2 lettres suivies de chiffres (ex: AD001)"
        
        return True, ""
    
    @staticmethod
    def is_matricule_available(matricule: str) -> Tuple[bool, str]:
        """
        Vérifie si un matricule est disponible (non utilisé)
        
        Args:
            matricule (str): Le matricule à vérifier
            
        Returns:
            Tuple[bool, str]: (disponible, message d'erreur)
        """
        try:
            conn = psycopg2.connect(**PG_CONN)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 1 FROM sge_cre.individus WHERE matricule = %s
            """, (matricule.upper(),))
            
            exists = cursor.fetchone() is not None
            conn.close()
            
            if exists:
                return False, "Ce matricule est déjà utilisé"
            else:
                return True, ""
                
        except Exception as e:
            return False, f"Erreur de vérification: {e}"
    
    @staticmethod
    def get_all_matricules_by_role(role: str) -> List[str]:
        """
        Récupère tous les matricules existants pour un rôle donné
        
        Args:
            role (str): Le nom du rôle
            
        Returns:
            List[str]: Liste des matricules pour ce rôle
        """
        prefix = MatriculeManager.get_role_prefix(role)
        
        try:
            conn = psycopg2.connect(**PG_CONN)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT matricule 
                FROM sge_cre.individus 
                WHERE matricule LIKE %s 
                ORDER BY matricule
            """, (f"{prefix}%",))
            
            matricules = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            return matricules
            
        except Exception as e:
            print(f"Erreur lors de la récupération des matricules: {e}")
            return []
    
    @staticmethod
    def get_statistics() -> Dict[str, int]:
        """
        Retourne des statistiques sur l'utilisation des matricules par rôle
        
        Returns:
            Dict[str, int]: Nombre d'utilisateurs par rôle
        """
        try:
            conn = psycopg2.connect(**PG_CONN)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT role, COUNT(*) as count
                FROM sge_cre.individus
                WHERE matricule IS NOT NULL
                GROUP BY role
                ORDER BY count DESC
            """)
            
            stats = {row[0]: row[1] for row in cursor.fetchall()}
            conn.close()
            
            return stats
            
        except Exception as e:
            print(f"Erreur lors de la récupération des statistiques: {e}")
            return {}

# Fonctions utilitaires pour compatibilité avec l'ancien code
def slugify_role(role: str) -> str:
    """Fonction de compatibilité avec l'ancien code"""
    return MatriculeManager.get_role_prefix(role)

def generate_matricule(prefix: str) -> str:
    """Fonction de compatibilité avec l'ancien code"""
    # Chercher le rôle correspondant au préfixe
    for role_name, role_prefix in MatriculeManager.ROLE_PREFIXES.items():
        if role_prefix == prefix:
            return MatriculeManager.generate_matricule(role_name)
    
    # Si pas trouvé, générer avec le préfixe fourni
    return MatriculeManager.generate_matricule(f"Rôle {prefix}")

# Test du module
if __name__ == "__main__":
    print("=== Test du module MatriculeManager ===\n")
    
    # Test de génération de matricules
    test_roles = [
        "Administrateur",
        "Livreur", 
        "Magasinier",
        "Responsable des stocks",
        "Technicien informatique"
    ]
    
    print("Génération de matricules:")
    for role in test_roles:
        matricule = MatriculeManager.generate_matricule(role)
        prefix = MatriculeManager.get_role_prefix(role)
        print(f"  {role} -> {prefix} -> {matricule}")
    
    print("\nIdentification de rôles par matricule:")
    test_matricules = ["AD001", "LV002", "MG003", "RS001", "TI001"]
    for matricule in test_matricules:
        role = MatriculeManager.get_role_from_matricule(matricule)
        print(f"  {matricule} -> {role}")
    
    print("\nValidation de matricules:")
    test_validation = ["AD001", "INVALID", "A1", "AD123456789", ""]
    for matricule in test_validation:
        valid, message = MatriculeManager.validate_matricule(matricule)
        print(f"  {matricule}: {'✓' if valid else '✗'} {message}")
    
    print("\nStatistiques:")
    stats = MatriculeManager.get_statistics()
    for role, count in stats.items():
        print(f"  {role}: {count} utilisateurs") 