#!/usr/bin/env python3
"""
Orchestrateur — Agent 1 (Job Fetcher + Google Sheets Injector)
Exécute le Job Fetcher et injecte les résultats dans Google Sheets
"""

import os
import sys
import io
import subprocess
import json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Ajouter le chemin du projet au sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv(project_root / ".env")

def run_fetcher():
    """Lance Agent 1 — Job Fetcher"""
    print("\n" + "="*60)
    print("🔍 Agent 1 — Job Fetcher")
    print("="*60)

    os.chdir(project_root)

    # Import et exécution du fetcher
    try:
        from agent_1_fetcher import JobFetcher
        import json

        # Charger les casquettes
        with open("data/casquettes.json", "r", encoding="utf-8") as f:
            casquettes = json.load(f)

        # Vérifier credentials
        client_id = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
        client_secret = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")

        print(f"[DEBUG] client_id: {client_id[:30] if client_id else 'None'}...")
        print(f"[DEBUG] client_secret: {client_secret[:30] if client_secret else 'None'}...")

        if not client_id or not client_secret:
            print("❌ Erreur: credentials API France Travail manquants")
            print("   Définissez FRANCE_TRAVAIL_CLIENT_ID et FRANCE_TRAVAIL_CLIENT_SECRET dans .env")
            return False

        # Exécuter le fetcher
        fetcher = JobFetcher(client_id, client_secret)
        print("🔍 Récupération des offres France Travail...")
        offers = fetcher.fetch_all(casquettes)

        if not offers:
            print("⚠️  Aucune offre trouvée")
            return False

        print(f"✅ Total: {len(offers)} offres récupérées")

        # Sauvegarder en JSON
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/offers.json", "w", encoding="utf-8") as f:
            json.dump(offers, f, ensure_ascii=False, indent=2)
        print("📄 Résultats sauvegardés: outputs/offers.json")

        return True

    except Exception as e:
        print(f"❌ Erreur Job Fetcher: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_injector(sheet_id: str = None):
    """Lance l'injection Google Sheets"""
    print("\n" + "="*60)
    print("📤 Injection Google Sheets")
    print("="*60)

    os.chdir(project_root)

    try:
        from google_sheets_injector import get_google_sheets_client, inject_offers
        import json

        # Charger les offres
        if not os.path.exists("outputs/offers.json"):
            print("❌ Fichier offers.json non trouvé")
            return False

        with open("outputs/offers.json", "r", encoding="utf-8") as f:
            offers = json.load(f)

        print(f"📊 Chargement de {len(offers)} offres...")

        # Connexion Google Sheets
        client = get_google_sheets_client()
        if not client:
            print("❌ Impossible de se connecter à Google Sheets")
            print("   Vérifiez: mcp-config/google-sheets-credentials.json")
            return False

        # Injection
        success = inject_offers(client, offers, sheet_id=sheet_id)
        return success

    except Exception as e:
        print(f"❌ Erreur injection: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main(sheet_id: str = None):
    """Orchestrateur principal"""

    print("\n" + "="*60)
    print("🤖 Job Hunting System — Agent 1 Orchestrator")
    print("="*60)

    # Vérifier les fichiers de config
    if not (project_root / "data" / "casquettes.json").exists():
        print("❌ Fichier data/casquettes.json manquant")
        return False

    if not (project_root / ".env").exists():
        print("⚠️  Fichier .env manquant")
        print("   Créez-le en copiant .env.example et en remplissant vos credentials")
        return False

    # Étape 1: Job Fetcher
    if not run_fetcher():
        print("❌ Job Fetcher échoué")
        return False

    # Étape 2: Google Sheets Injector
    if not run_injector(sheet_id=sheet_id):
        print("⚠️  Injection Google Sheets échouée (mais offres sauvegardées en JSON)")
        return False

    print("\n" + "="*60)
    print("🎉 Agent 1 — Exécution réussie!")
    print("="*60)
    print("\n📋 Prochaines étapes:")
    print("  1. Ouvrez: https://docs.google.com/spreadsheets")
    print("  2. Consultez le sheet 'Job Hunter — Offres'")
    print("  3. Lancez ensuite Agent 2 (Job Matcher) pour scorer les offres")
    print("\nCommande Agent 2:")
    print("  python code/run-agent-2.py")

    return True


if __name__ == "__main__":
    # Sheet ID: 1rdDZzXMXxs3Tm5-2zcAgwF4vjkhl4zYP21X7BRPv8rY
    sheet_id = "1rdDZzXMXxs3Tm5-2zcAgwF4vjkhl4zYP21X7BRPv8rY"
    success = main(sheet_id=sheet_id)
    sys.exit(0 if success else 1)
