#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration du système de génération automatique de matricules
"""

import sys
import os

# Ajouter le répertoire courant au path pour importer les modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from matricule_manager import MatriculeManager

def demo_generation_matricules():
    """Démonstration de la génération de matricules"""
    print("🎯 DÉMONSTRATION - Système de Génération Automatique de Matricules")
    print("=" * 70)
    
    # Liste des rôles spécifiques
    roles_specifiques = [
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
    
    print("\n📋 RÔLES ET PRÉFIXES DE MATRICULES")
    print("-" * 50)
    
    for i, role in enumerate(roles_specifiques, 1):
        prefix = MatriculeManager.get_role_prefix(role)
        print(f"{i:2d}. {role:<35} → {prefix}")
    
    print("\n🚀 GÉNÉRATION AUTOMATIQUE DE MATRICULES")
    print("-" * 50)
    
    # Simuler la création de plusieurs utilisateurs pour chaque rôle
    for role in roles_specifiques:
        print(f"\n👤 {role}:")
        prefix = MatriculeManager.get_role_prefix(role)
        
        # Générer 3 matricules pour ce rôle (simulation de 3 utilisateurs)
        for i in range(3):
            matricule = MatriculeManager.generate_matricule(role)
            print(f"   • Utilisateur {i+1}: {matricule}")
    
    print("\n🔍 IDENTIFICATION DE RÔLES PAR MATRICULE")
    print("-" * 50)
    
    # Tester l'identification de rôles
    matricules_test = [
        "RS001",  # Responsable des stocks
        "MG002",  # Magasinier
        "EM003",  # Emballeur
        "LV001",  # Livreur
        "RI001",  # Responsable informatique
        "TI002",  # Technicien informatique
        "RP001",  # Responsable de la sécurité physique
        "GS001"   # Garde de sécurité
    ]
    
    for matricule in matricules_test:
        role_identifie = MatriculeManager.get_role_from_matricule(matricule)
        print(f"   {matricule} → {role_identifie}")
    
    print("\n✅ VALIDATION DE MATRICULES")
    print("-" * 50)
    
    # Tester la validation
    matricules_validation = [
        "RS001",      # ✅ Valide
        "MG002",      # ✅ Valide
        "INVALID",    # ❌ Invalide
        "A1",         # ❌ Trop court
        "RS123456789", # ❌ Trop long
        "RS001A",     # ❌ Format invalide
    ]
    
    for matricule in matricules_validation:
        is_valid, message = MatriculeManager.validate_matricule(matricule)
        status = "✅" if is_valid else "❌"
        print(f"   {status} {matricule:<12} : {message}")

def demo_scenarios_reels():
    """Démonstration de scénarios réels d'utilisation"""
    print("\n\n🎬 SCÉNARIOS RÉELS D'UTILISATION")
    print("=" * 50)
    
    # Scénario 1: Nouvelle embauche
    print("\n📝 Scénario 1: Nouvelle embauche")
    print("   Situation: L'entreprise embauche un nouveau livreur")
    
    role = "Livreur"
    matricule = MatriculeManager.generate_matricule(role)
    prefix = MatriculeManager.get_role_prefix(role)
    
    print(f"   Rôle sélectionné: {role}")
    print(f"   Préfixe automatique: {prefix}")
    print(f"   Matricule généré: {matricule}")
    print(f"   ✅ Prêt à être attribué au nouvel employé")
    
    # Scénario 2: Promotion interne
    print("\n📈 Scénario 2: Promotion interne")
    print("   Situation: Un magasinier devient responsable des stocks")
    
    ancien_role = "Magasinier"
    nouveau_role = "Responsable des stocks"
    ancien_matricule = "MG001"
    nouveau_matricule = MatriculeManager.generate_matricule(nouveau_role)
    
    print(f"   Ancien rôle: {ancien_role} ({ancien_matricule})")
    print(f"   Nouveau rôle: {nouveau_role} ({nouveau_matricule})")
    print(f"   ✅ Le matricule reflète la nouvelle responsabilité")
    
    # Scénario 3: Équipe de sécurité
    print("\n🛡️ Scénario 3: Équipe de sécurité")
    print("   Situation: Création d'une équipe de sécurité")
    
    roles_securite = ["Responsable de la sécurité physique", "Garde de sécurité", "Garde de sécurité"]
    matricules_securite = []
    
    for role in roles_securite:
        matricule = MatriculeManager.generate_matricule(role)
        matricules_securite.append(matricule)
        print(f"   {role}: {matricule}")
    
    print(f"   ✅ Équipe complète avec matricules cohérents")

def demo_avantages_systeme():
    """Démonstration des avantages du système"""
    print("\n\n💡 AVANTAGES DU SYSTÈME")
    print("=" * 50)
    
    avantages = [
        "🎯 Identification rapide du rôle par matricule",
        "🔢 Numérotation automatique et séquentielle", 
        "🔄 Génération automatique sans intervention manuelle",
        "✅ Validation et vérification d'unicité",
        "📊 Traçabilité et statistiques d'utilisation",
        "🛡️ Cohérence entre rôle et matricule",
        "⚡ Interface intuitive d'administration",
        "🔧 Outils de test et validation intégrés"
    ]
    
    for avantage in avantages:
        print(f"   {avantage}")

if __name__ == "__main__":
    try:
        demo_generation_matricules()
        demo_scenarios_reels()
        demo_avantages_systeme()
        
        print("\n" + "=" * 70)
        print("🎉 DÉMONSTRATION TERMINÉE")
        print("Le système est prêt à être utilisé dans l'application!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc() 