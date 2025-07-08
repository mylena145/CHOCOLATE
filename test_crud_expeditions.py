#!/usr/bin/env python3
"""
Script de test pour vérifier le CRUD des expéditions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_all_expeditions, add_expedition, update_expedition, delete_expedition, get_expedition_stats
from datetime import datetime

def test_crud_expeditions():
    """Test complet du CRUD des expéditions"""
    print("🧪 Test du CRUD des expéditions")
    print("=" * 50)
    
    # Test 1: Récupérer toutes les expéditions
    print("\n1️⃣ Test de récupération des expéditions...")
    try:
        expeditions = get_all_expeditions()
        print(f"✅ {len(expeditions)} expéditions récupérées")
        for exp in expeditions[:3]:  # Afficher les 3 premières
            print(f"   - {exp.get('number', 'N/A')} : {exp.get('client', 'N/A')}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération: {e}")
        return False
    
    # Test 2: Ajouter une nouvelle expédition
    print("\n2️⃣ Test d'ajout d'expédition...")
    try:
        new_expedition_data = {
            'client': 'Test Client CRUD',
            'reference_commande': 'TST',  # Référence très courte (3 caractères)
            'date_livraison': datetime.now().strftime('%Y-%m-%d'),
            'transporteurs': 'DHL Express',
            'observation': 'Test CRUD - Expédition de test',
            'liste_articles_livres': 'Articles de test'
        }
        
        expedition_id = add_expedition(new_expedition_data)
        if expedition_id:
            print(f"✅ Expédition créée avec l'ID: {expedition_id}")
            test_expedition_id = expedition_id
        else:
            print("❌ Échec de la création")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False
    
    # Test 3: Récupérer les statistiques
    print("\n3️⃣ Test des statistiques...")
    try:
        stats = get_expedition_stats()
        print(f"✅ Statistiques récupérées:")
        print(f"   - Total: {stats.get('total', 0)}")
        print(f"   - En préparation: {stats.get('en_preparation', 0)}")
        print(f"   - Livrées: {stats.get('livrees', 0)}")
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des stats: {e}")
    
    # Test 4: Mettre à jour l'expédition
    print("\n4️⃣ Test de mise à jour...")
    try:
        update_data = {
            'client': 'Test Client CRUD - Modifié',
            'reference_commande': 'MOD',  # Référence très courte (3 caractères)
            'date_livraison': datetime.now().strftime('%Y-%m-%d'),
            'transporteurs': 'Chronopost',
            'observation': 'Test CRUD - Expédition modifiée',
            'liste_articles_livres': 'Articles modifiés'
        }
        
        success = update_expedition(test_expedition_id, update_data)
        if success:
            print("✅ Expédition mise à jour avec succès")
        else:
            print("❌ Échec de la mise à jour")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False
    
    # Test 5: Vérifier la mise à jour
    print("\n5️⃣ Vérification de la mise à jour...")
    try:
        expeditions = get_all_expeditions()
        updated_exp = None
        for exp in expeditions:
            if exp.get('id') == test_expedition_id:
                updated_exp = exp
                break
        
        if updated_exp:
            print(f"✅ Expédition trouvée: {updated_exp.get('client', 'N/A')}")
            print(f"   - Transporteur: {updated_exp.get('carrier', 'N/A')}")
        else:
            print("❌ Expédition mise à jour non trouvée")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    
    # Test 6: Supprimer l'expédition
    print("\n6️⃣ Test de suppression...")
    try:
        success = delete_expedition(test_expedition_id)
        if success:
            print("✅ Expédition supprimée avec succès")
        else:
            print("❌ Échec de la suppression")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {e}")
        return False
    
    # Test 7: Vérifier la suppression
    print("\n7️⃣ Vérification de la suppression...")
    try:
        expeditions = get_all_expeditions()
        deleted_exp = None
        for exp in expeditions:
            if exp.get('id') == test_expedition_id:
                deleted_exp = exp
                break
        
        if not deleted_exp:
            print("✅ Expédition bien supprimée")
        else:
            print("❌ Expédition toujours présente après suppression")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    
    print("\n🎉 Tous les tests CRUD sont passés avec succès !")
    return True

if __name__ == "__main__":
    success = test_crud_expeditions()
    if success:
        print("\n✅ Le CRUD des expéditions fonctionne correctement")
        sys.exit(0)
    else:
        print("\n❌ Des erreurs ont été détectées dans le CRUD")
        sys.exit(1) 