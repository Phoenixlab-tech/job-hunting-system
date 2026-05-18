#!/usr/bin/env python3
"""
Google Sheets Injector
Injecte les offres d'emploi dans le sheet "Job Hunter — Offres"
"""

import json
import os
from typing import List, Dict, Optional

# Note: Nécessite gspread et google-auth
# pip install gspread google-auth google-auth-oauthlib


def get_google_sheets_client():
    """Initialise le client Google Sheets"""
    try:
        import gspread
        from google.auth.transport.requests import Request
        from google.oauth2.service_account import Credentials

        # Charger les credentials service account
        creds_path = "mcp-config/google-sheets-credentials.json"
        if not os.path.exists(creds_path):
            raise FileNotFoundError(f"Credentials file not found: {creds_path}")

        credentials = Credentials.from_service_account_file(
            creds_path,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        client = gspread.authorize(credentials)
        return client

    except ImportError:
        print("❌ Librairies manquantes: pip install gspread google-auth google-auth-oauthlib")
        return None
    except Exception as e:
        print(f"❌ Erreur authentification Google: {str(e)}")
        return None


def get_or_create_sheet(client, sheet_id: str = None, sheet_name: str = None) -> Optional[object]:
    """Récupère un Google Sheet par ID ou par nom"""
    try:
        if sheet_id:
            # Utiliser l'ID du sheet directement
            spreadsheet = client.open_by_key(sheet_id)
            print(f"✅ Sheet trouvé (ID: {sheet_id[:20]}...)")
            return spreadsheet
        else:
            # Fallback: chercher par nom
            spreadsheet = client.open(sheet_name)
            print(f"✅ Sheet '{sheet_name}' trouvé")
            return spreadsheet
    except Exception as e:
        print(f"❌ Sheet non trouvé: {str(e)}")
        if sheet_name:
            print(f"\n📋 Créez le sheet manuellement: https://docs.google.com/spreadsheets/create")
        return None


def inject_offers(client, offers: List[Dict], sheet_id: str = None, sheet_name: str = None) -> bool:
    """Injecte les offres dans le sheet"""

    # Récupérer le sheet
    spreadsheet = get_or_create_sheet(client, sheet_id=sheet_id, sheet_name=sheet_name)
    if not spreadsheet:
        return False

    # Récupérer l'onglet "Offres"
    try:
        worksheet = spreadsheet.worksheet("Offres")
    except:
        print("❌ Onglet 'Offres' non trouvé")
        print("   → Créez un onglet 'Offres' avec les colonnes:")
        headers = ["A: id_offre", "B: titre", "C: entreprise", "D: lieu",
                  "E: distance_km", "F: salaire", "G: contrat", "H: date_publication",
                  "I: casquette", "J: score_match", "K: description", "L: competences",
                  "M: url_offre", "N: statut"]
        for h in headers:
            print(f"   {h}")
        return False

    print(f"📝 Préparation de {len(offers)} offres pour injection...")

    # Préparer les données
    rows = []
    for offer in offers:
        row = [
            offer.get("id_offre", ""),
            offer.get("titre", ""),
            offer.get("entreprise", ""),
            offer.get("lieu", ""),
            offer.get("distance_km", ""),
            offer.get("salaire", ""),
            offer.get("contrat", ""),
            offer.get("date_publication", ""),
            offer.get("casquette", ""),
            "",  # score_match (rempli par Agent 2)
            offer.get("description", ""),
            offer.get("competences", ""),
            offer.get("url_offre", ""),
            offer.get("statut", "nouveau")
        ]
        rows.append(row)

    # Vérifier les offres existantes
    try:
        existing = worksheet.get_all_values()
        existing_ids = {row[0] for row in existing[1:] if row}  # Skip header
    except:
        existing_ids = set()

    # Filtrer les nouvelles offres
    new_rows = [r for r in rows if r[0] not in existing_ids]

    if not new_rows:
        print("✅ Aucune nouvelle offre à ajouter")
        return True

    # Injecter les nouvelles lignes
    print(f"📤 Injection de {len(new_rows)} nouvelles offres...")

    try:
        # Trouver la première ligne vide
        existing_count = len(existing) if existing else 1
        start_row = existing_count + 1 if existing else 2

        # Ajouter les offres
        worksheet.append_rows(new_rows, value_input_option="RAW")

        print(f"✅ {len(new_rows)} offres injectées avec succès!")
        print(f"   → Consultez: https://docs.google.com/spreadsheets")
        return True

    except Exception as e:
        print(f"❌ Erreur injection: {str(e)}")
        return False


def main(sheet_id: str = None):
    """Point d'entrée principal"""

    # Charger les offres depuis le JSON généré par Agent 1
    offers_file = "outputs/offers.json"

    if not os.path.exists(offers_file):
        print(f"❌ Fichier '{offers_file}' non trouvé")
        print("   Exécutez d'abord agent-1-fetcher.py")
        return

    with open(offers_file, "r", encoding="utf-8") as f:
        offers = json.load(f)

    print(f"📊 Chargement de {len(offers)} offres...")

    # Connexion Google Sheets
    client = get_google_sheets_client()
    if not client:
        print("❌ Impossible de se connecter à Google Sheets")
        return

    # Injection
    success = inject_offers(client, offers, sheet_id=sheet_id, sheet_name="Job Hunter — Offres")

    if success:
        print("\n🎉 Job Fetcher terminé avec succès!")
    else:
        print("\n❌ Erreur lors de l'injection")


if __name__ == "__main__":
    main()
