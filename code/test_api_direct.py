#!/usr/bin/env python3
"""
Test Direct API Call
Teste les appels API en détail pour diagnostiquer la 403
"""

import os
import sys
import io
import requests
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv(project_root / ".env")

def test_oauth(scope="api_offresdemploiv2"):
    """Test l'authentification OAuth avec scope différent"""
    print("\n" + "="*60)
    print(f"🔐 Test OAuth (scope: {scope})")
    print("="*60)

    client_id = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
    client_secret = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")

    print(f"Client ID: {client_id[:30]}...")
    print(f"Client Secret: {client_secret[:30]}...")

    url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
    payload = {
        "grant_type": "client_credentials",
        "scope": scope
    }

    try:
        response = requests.post(url, data=payload, auth=(client_id, client_secret))
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")

        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"\n✅ Token obtenu: {token[:50]}...")
            return token
        else:
            print(f"❌ OAuth failed")
            return None
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None

def test_search_api(token):
    """Test l'API de recherche d'offres"""
    print("\n" + "="*60)
    print("🔍 Test API Recherche")
    print("="*60)

    if not token:
        print("❌ Pas de token disponible")
        return

    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    # Try with correct scope but without commune parameter
    params = {
        "motsCles": "responsable services généraux",
        "departement": "33",  # Gironde
        "distance": 25,
        "range": "0-150",
        "sort": "date_creation",
        "order": "desc"
    }

    print(f"Testing with departement=33 instead of commune=33410")

    print(f"\nURL: {url}")
    print(f"Headers: {headers}")
    print(f"Params: {params}\n")

    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}\n")
        print(f"Response text: {response.text[:1000]}")

        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Réponse valide: {len(data.get('resultats', []))} offres")
        else:
            print(f"\n❌ Erreur API: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Détails erreur: {error_data}")
            except:
                print(f"Réponse brute: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    # Try different scopes
    scopes_to_try = [
        "api_offresdemploiv2 o2dsoffre",
        "o2dsoffre",
        "api_offresdemploiv2",
        "api_offresdemploiv2 read",
    ]

    for scope in scopes_to_try:
        token = test_oauth(scope)
        if token:
            test_search_api(token)
            if token:  # Only print separator if we got a token
                print()
