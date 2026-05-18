#!/usr/bin/env python3
"""
Crée le Google Sheet 'Job Hunter — Offres' et le partage
"""

import gspread
from google.oauth2.service_account import Credentials
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Charger les credentials
creds_path = "mcp-config/google-sheets-credentials.json"
credentials = Credentials.from_service_account_file(
    creds_path,
    scopes=["https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"]
)

client = gspread.authorize(credentials)

# Créer le spreadsheet
print("Création du Google Sheet...")
spreadsheet = client.create("Job Hunter — Offres")
print(f"✅ Sheet créé: {spreadsheet.url}")

# Récupérer l'onglet par défaut et le renommer
worksheet = spreadsheet.worksheets()[0]
worksheet.update_title("Offres")
print("✅ Onglet renommé: 'Offres'")

# Ajouter les headers
headers = [
    "id_offre", "titre", "entreprise", "lieu", "distance_km",
    "salaire", "contrat", "date_publication", "casquette",
    "score_match", "description", "competences", "url_offre", "statut"
]
worksheet.append_row(headers, value_input_option="RAW")
print(f"✅ Headers ajoutés")

# Partager avec le service account
service_account_email = "job-hunter@make-agent-emploi.iam.gserviceaccount.com"
spreadsheet.share(service_account_email, perm_type='user', role='writer')
print(f"✅ Sheet partagé avec: {service_account_email}")

print(f"\n✅ Pret pour injection!")
print(f"   Sheet URL: {spreadsheet.url}")
