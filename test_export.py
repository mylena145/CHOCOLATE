#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier les fonctionnalités d'export
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Expeditions import GestionExpeditionsApp
import customtkinter as ctk
from datetime import datetime

def test_export_functionality():
    """Test des fonctionnalités d'export"""
    print("🧪 Test des fonctionnalités d'export...")
    
    # Créer une instance de l'application
    root = ctk.CTk()
    root.withdraw()  # Cacher la fenêtre principale
    
    app = GestionExpeditionsApp(master=root)
    
    # Données de test
    test_data = [
        {
            'id': 1,
            'number': 'BE-2024-001',
            'client': 'Client Test 1',
            'shippingDate': '2024-07-08',
            'deliveryDate': '2024-07-10',
            'carrier': 'DHL Express',
            'priority': 'haute',
            'packages': 2,
            'totalWeight': 15.5,
            'status': 'preparing',
            'trackingNumber': 'REF001',
            'observation': 'Test observation 1'
        },
        {
            'id': 2,
            'number': 'BE-2024-002',
            'client': 'Client Test 2',
            'shippingDate': '2024-07-08',
            'deliveryDate': '2024-07-09',
            'carrier': 'Chronopost',
            'priority': 'moyenne',
            'packages': 1,
            'totalWeight': 8.2,
            'status': 'in-transit',
            'trackingNumber': 'REF002',
            'observation': 'Test observation 2'
        }
    ]
    
    # Assigner les données de test
    app.expeditions_data = test_data
    
    # Test des filtres
    print("📊 Test des filtres...")
    
    # Test filtre par période
    filtered_today = app._filter_export_data("Aujourd'hui", "Tous")
    print(f"   - Filtre 'Aujourd'hui': {len(filtered_today)} expéditions")
    
    filtered_all = app._filter_export_data("Toutes", "Tous")
    print(f"   - Filtre 'Toutes': {len(filtered_all)} expéditions")
    
    # Test des exports
    print("📁 Test des exports...")
    
    # Test Excel
    excel_file = app._export_to_excel(test_data, "exports", "test")
    if excel_file:
        print(f"   ✅ Export Excel réussi: {excel_file}")
    else:
        print("   ❌ Export Excel échoué")
    
    # Test CSV
    csv_file = app._export_to_csv(test_data, "exports", "test")
    if csv_file:
        print(f"   ✅ Export CSV réussi: {csv_file}")
    else:
        print("   ❌ Export CSV échoué")
    
    # Test PDF
    pdf_file = app._export_to_pdf(test_data, "exports", "test")
    if pdf_file:
        print(f"   ✅ Export PDF réussi: {pdf_file}")
    else:
        print("   ❌ Export PDF échoué")
    
    # Vérifier les fichiers créés
    print("📂 Vérification des fichiers...")
    if os.path.exists("exports"):
        files = os.listdir("exports")
        for file in files:
            if file.startswith("expeditions_test"):
                file_path = os.path.join("exports", file)
                file_size = os.path.getsize(file_path)
                print(f"   📄 {file} ({file_size} bytes)")
    
    print("✅ Test terminé !")
    root.destroy()

if __name__ == "__main__":
    test_export_functionality() 