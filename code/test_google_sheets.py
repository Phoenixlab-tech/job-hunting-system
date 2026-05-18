#!/usr/bin/env python3
"""
Test Google Sheets Injection
Ignore le fetcher et teste juste l'injection des offres mockées
"""

import os
import sys
import io
import json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Ajouter le chemin du projet au sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv(project_root / ".env")

def test_injection():
    """Teste l'injection Google Sheets avec des données mockées"""
    print("\n" + "="*60)
    print("📊 Test Injection Google Sheets")
    print("="*60)

    try:
        from google_sheets_injector import get_google_sheets_client, inject_offers
        import json

        # Charger les offres mockées
        offers_file = project_root / "outputs" / "offers.json"
        if not offers_file.exists():
            print(f"❌ Fichier {offers_file} non trouvé")
            return False

        with open(offers_file, "r", encoding="utf-8") as f:
            offers = json.load(f)

        print(f"📋 Chargement de {len(offers)} offres mockées...")
        for offer in offers:
            print(f"   - {offer['intitule']} @ {offer['entreprise']['nom']}")

        # Connexion Google Sheets
        print("\n🔌 Connexion à Google Sheets...")
        client = get_google_sheets_client()
        if not client:
            print("❌ Impossible de se connecter à Google Sheets")
            print("   Vérifiez: mcp-config/google-sheets-credentials.json")
            return False

        print("✅ Connecté")

        # Injection
        print("\n📤 Injection des offres...")
        success = inject_offers(client, "Job Hunter — Offres", offers)

        if success:
            print("\n✅ Injection réussie!")
            print("\n📋 Prochaines étapes:")
            print("  1. Ouvrez: https://docs.google.com/spreadsheets/")
            print("  2. Vérifiez le sheet 'Job Hunter — Offres'")
            print("  3. Corrigez les credentials France Travail")
            print("  4. Relancez le Agent 1 complet avec python code/run_agent_1.py")
            return True
        else:
            print("⚠️  Injection échouée")
            return False

    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_injection()
    sys.exit(0 if success else 1)
