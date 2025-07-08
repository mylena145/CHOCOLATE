#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour le système de génération de matricules
"""

import sys
import os

# Ajouter le répertoire courant au path pour importer les modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from matricule_manager import MatriculeManager

def test_matricule_system():
    """Test complet du système de matricules"""
    print("🧪 Test du Système de Génération de Matricules")
    print("=" * 50)
    
    # Test 1: Génération de préfixes
    print("\n1. Test de génération des préfixes:")
    test_roles = [
        "Responsable des stocks",
        "Magasinier",
        "Emballeur",
        "Responsable de la logistique",
        "Agent de logistique",
        "Livreur",
        "Responsable informatique",
        "Technicien informatique",
        "Responsable de la sécurité physique",
        "Garde de sécurité"
    ]
    
    for role in test_roles:
        prefix = MatriculeManager.get_role_prefix(role)
        print(f"   {role} -> {prefix}")
    
    # Test 2: Génération de matricules
    print("\n2. Test de génération de matricules:")
    for role in test_roles[:5]:  # Tester seulement les 5 premiers
        matricule = MatriculeManager.generate_matricule(role)
        print(f"   {role} -> {matricule}")
    
    # Test 3: Identification de rôles par matricule
    print("\n3. Test d'identification de rôles par matricule:")
    test_matricules = ["AD001", "LV002", "MG003", "RS001", "TI001", "SA001"]
    for matricule in test_matricules:
        role = MatriculeManager.get_role_from_matricule(matricule)
        print(f"   {matricule} -> {role}")
    
    # Test 4: Validation de matricules
    print("\n4. Test de validation de matricules:")
    test_validation = [
        "AD001",      # Valide
        "INVALID",    # Invalide
        "A1",         # Trop court
        "AD123456789", # Trop long
        "",           # Vide
        "AD001A",     # Format invalide
        "AD001",      # Valide
    ]
    
    for matricule in test_validation:
        is_valid, message = MatriculeManager.validate_matricule(matricule)
        status = "✅" if is_valid else "❌"
        print(f"   {status} {matricule}: {message}")
    
    # Test 5: Vérification de disponibilité
    print("\n5. Test de vérification de disponibilité:")
    test_availability = ["AD001", "TEST999", "LV999"]
    for matricule in test_availability:
        is_available, message = MatriculeManager.is_matricule_available(matricule)
        status = "✅" if is_available else "❌"
        print(f"   {status} {matricule}: {message}")
    
    # Test 6: Statistiques
    print("\n6. Test des statistiques:")
    try:
        stats = MatriculeManager.get_statistics()
        if stats:
            for role, count in stats.items():
                print(f"   {role}: {count} utilisateurs")
        else:
            print("   Aucune statistique disponible")
    except Exception as e:
        print(f"   Erreur lors de la récupération des statistiques: {e}")
    
    # Test 7: Récupération de matricules par rôle
    print("\n7. Test de récupération de matricules par rôle:")
    for role in test_roles[:3]:  # Tester seulement les 3 premiers
        try:
            matricules = MatriculeManager.get_all_matricules_by_role(role)
            print(f"   {role}: {matricules}")
        except Exception as e:
            print(f"   Erreur pour {role}: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés!")

def test_specific_scenarios():
    """Test de scénarios spécifiques"""
    print("\n🔍 Test de Scénarios Spécifiques")
    print("=" * 40)
    
    # Scénario 1: Création d'un nouveau livreur
    print("\nScénario 1: Création d'un nouveau livreur")
    role_livreur = "Livreur"
    matricule_livreur = MatriculeManager.generate_matricule(role_livreur)
    prefix_livreur = MatriculeManager.get_role_prefix(role_livreur)
    print(f"   Rôle: {role_livreur}")
    print(f"   Préfixe: {prefix_livreur}")
    print(f"   Matricule généré: {matricule_livreur}")
    
    # Vérifier que le matricule correspond au rôle
    role_identifie = MatriculeManager.get_role_from_matricule(matricule_livreur)
    print(f"   Rôle identifié: {role_identifie}")
    print(f"   ✅ Cohérence: {role_livreur == role_identifie}")
    
    # Scénario 2: Création d'un responsable des stocks
    print("\nScénario 2: Création d'un responsable des stocks")
    role_stocks = "Responsable des stocks"
    matricule_stocks = MatriculeManager.generate_matricule(role_stocks)
    prefix_stocks = MatriculeManager.get_role_prefix(role_stocks)
    print(f"   Rôle: {role_stocks}")
    print(f"   Préfixe: {prefix_stocks}")
    print(f"   Matricule généré: {matricule_stocks}")
    
    # Scénario 3: Création d'un magasinier
    print("\nScénario 3: Création d'un magasinier")
    role_magasinier = "Magasinier"
    matricule_magasinier = MatriculeManager.generate_matricule(role_magasinier)
    prefix_magasinier = MatriculeManager.get_role_prefix(role_magasinier)
    print(f"   Rôle: {role_magasinier}")
    print(f"   Préfixe: {prefix_magasinier}")
    print(f"   Matricule généré: {matricule_magasinier}")
    
    # Scénario 4: Test de validation d'un matricule existant
    print("\nScénario 4: Test de validation d'un matricule existant")
    matricule_test = "RS001"
    is_valid, validation_msg = MatriculeManager.validate_matricule(matricule_test)
    is_available, availability_msg = MatriculeManager.is_matricule_available(matricule_test)
    role_from_matricule = MatriculeManager.get_role_from_matricule(matricule_test)
    
    print(f"   Matricule: {matricule_test}")
    print(f"   Format valide: {is_valid}")
    print(f"   Disponible: {is_available}")
    print(f"   Rôle identifié: {role_from_matricule}")

if __name__ == "__main__":
    try:
        test_matricule_system()
        test_specific_scenarios()
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc() 