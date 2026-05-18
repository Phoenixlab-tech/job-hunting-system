#!/usr/bin/env python3
"""
Agent 1 — Job Fetcher
Récupère les offres d'emploi France Travail pour les 6 casquettes d'Arnaud
Localisation : Libourne 33500, rayon 25km
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import math

class JobFetcher:
    """Récupère les offres d'emploi via l'API France Travail"""

    def __init__(self, client_id: str, client_secret: str):
        """
        Args:
            client_id: Client ID de l'API France Travail
            client_secret: Client Secret de l'API France Travail
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.francetravail.io/partenaire"
        self.token = None
        self.token_expiry = None

        # Coordonnées de Libourne
        self.libourne_lat = 44.9044
        self.libourne_lon = 0.2518
        self.rayon_km = 25

    def get_token(self) -> str:
        """Obtient un token d'accès via OAuth2"""
        if self.token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.token

        url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
        payload = {
            "grant_type": "client_credentials",
            "scope": "api_offresdemploiv2 o2dsoffre"
        }

        try:
            response = requests.post(
                url,
                data=payload,
                auth=(self.client_id, self.client_secret)
            )
            print(f"[DEBUG] OAuth response: {response.text}")
            response.raise_for_status()
            data = response.json()
            self.token = data.get("access_token")
            expires_in = data.get("expires_in", 3600)
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in - 60)
            print(f"✅ Token obtenu (expire dans {expires_in}s)")
            return self.token
        except Exception as e:
            raise Exception(f"Erreur OAuth: {str(e)}")

    def search_offers(self, keywords: List[str], casquette_id: int) -> List[Dict]:
        """Recherche les offres pour une liste de mots-clés"""
        token = self.get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        all_offers = []

        for keyword in keywords:
            url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
            params = {
                "motsCles": keyword,
                "departement": "33"  # Gironde (Libourne)
            }

            try:
                response = requests.get(url, headers=headers, params=params)
                print(f"[DEBUG] Recherche '{keyword}': Status {response.status_code}")
                response.raise_for_status()
                data = response.json()

                if "resultats" in data:
                    for offer in data["resultats"]:
                        offer["casquette_id"] = casquette_id
                        offer["keyword_match"] = keyword
                        all_offers.append(offer)

            except requests.exceptions.RequestException as e:
                print(f"[DEBUG] Erreur '{keyword}': {str(e)}")
                if hasattr(e.response, 'text'):
                    print(f"[DEBUG] Réponse: {e.response.text[:500]}")
                continue

        return all_offers

    def deduplicate_offers(self, offers: List[Dict]) -> List[Dict]:
        """Supprime les doublons par ID d'offre"""
        seen = {}
        deduped = []

        for offer in offers:
            offer_id = offer.get("id")
            if offer_id not in seen:
                seen[offer_id] = offer
                deduped.append(offer)

        return deduped

    def format_offer(self, offer: Dict, casquette_id: int) -> Optional[Dict]:
        """Formate une offre pour Google Sheets"""
        try:
            # Extraction des données
            offer_id = offer.get("id", "")
            title = offer.get("intitule", "")
            company = offer.get("entreprise", {}).get("nom", "") if isinstance(offer.get("entreprise"), dict) else ""

            lieu_travail = offer.get("lieuTravail", {})
            city = lieu_travail.get("commune", "") if isinstance(lieu_travail, dict) else ""
            postal_code = lieu_travail.get("codePostal", "") if isinstance(lieu_travail, dict) else ""

            # Distance (calculée à partir des coordonnées si disponible)
            distance = "N/A"
            if isinstance(lieu_travail, dict) and "latitude" in lieu_travail and "longitude" in lieu_travail:
                lat = lieu_travail["latitude"]
                lon = lieu_travail["longitude"]
                if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                    distance = self.calculate_distance(self.libourne_lat, self.libourne_lon, lat, lon)

            # Salaire
            salary = "N/A"
            salaire = offer.get("salaire")
            if salaire and isinstance(salaire, dict):
                if salaire.get("salaireMensuelMinimum"):
                    salary = f"{salaire['salaireMensuelMinimum']:.0f}€"
                elif salaire.get("commentaire"):
                    salary = salaire["commentaire"]

            # Contrat (API retourne une string)
            contract = offer.get("typeContratLibelle", offer.get("typeContrat", "N/A"))

            # Date publication
            pub_date = offer.get("dateCreation", "")
            if pub_date:
                pub_date = pub_date.split("T")[0]

            # Description
            description = offer.get("description", "")

            # Compétences (non disponible dans cette API)
            competences = ""

            # URL offre
            contact = offer.get("contact", {})
            url = contact.get("urlPostulation", "") if isinstance(contact, dict) else ""

            # Vérifier si offre n'a pas plus de 30 jours
            if pub_date:
                pub_datetime = datetime.strptime(pub_date, "%Y-%m-%d")
                if (datetime.now() - pub_datetime).days > 30:
                    return None

            return {
                "id_offre": offer_id,
                "titre": title,
                "entreprise": company,
                "lieu": f"{city} ({postal_code})" if city else "N/A",
                "distance_km": float(distance) if isinstance(distance, (int, float)) else distance,
                "salaire": salary,
                "contrat": contract,
                "date_publication": pub_date,
                "casquette": casquette_id,
                "description": description,
                "competences": competences,
                "url_offre": url,
                "statut": "nouveau"
            }

        except Exception as e:
            print(f"Erreur formatage offre {offer.get('id', 'unknown')}: {str(e)}")
            return None

    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcule la distance en km entre deux points (formule de Haversine)"""
        R = 6371  # Rayon de la Terre en km
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c

    def fetch_all(self, casquettes: Dict) -> List[Dict]:
        """Récupère tous les offres pour les 6 casquettes"""
        all_offers = []

        for casquette in casquettes["casquettes"]:
            casquette_id = casquette["id"]
            keywords = casquette.get("mots_cles_api", [])

            print(f"\n📌 Casquette {casquette_id}: {casquette['nom']}")
            print(f"   Mots-clés: {', '.join(keywords)}")

            # Rechercher offres
            offers = self.search_offers(keywords, casquette_id)
            print(f"   {len(offers)} offre(s) trouvée(s) (avec doublons)")

            # Dédupliquer
            deduped = self.deduplicate_offers(offers)
            print(f"   {len(deduped)} offre(s) après déduplication")

            # Formater
            formatted = []
            for offer in deduped:
                formatted_offer = self.format_offer(offer, casquette_id)
                if formatted_offer:
                    formatted.append(formatted_offer)

            print(f"   {len(formatted)} offre(s) valides")
            all_offers.extend(formatted)

        # Dédupliquer globalement par ID offre
        seen = {}
        final_offers = []
        for offer in all_offers:
            if offer["id_offre"] not in seen:
                seen[offer["id_offre"]] = offer
                final_offers.append(offer)

        return final_offers


def main():
    """Point d'entrée principal"""

    # Charger les casquettes
    with open("data/casquettes.json", "r", encoding="utf-8") as f:
        casquettes = json.load(f)

    # Vérifier credentials API
    client_id = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
    client_secret = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("❌ Erreur: variables d'environnement manquantes")
        print("   Définissez FRANCE_TRAVAIL_CLIENT_ID et FRANCE_TRAVAIL_CLIENT_SECRET")
        return

    # Créer fetcher et récupérer offres
    fetcher = JobFetcher(client_id, client_secret)
    print("🔍 Récupération des offres France Travail...")

    offers = fetcher.fetch_all(casquettes)

    # Afficher résumé
    print(f"\n✅ Total: {len(offers)} offres uniques récupérées")

    # Sauvegarder en JSON
    output_file = "outputs/offers.json"
    os.makedirs("outputs", exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(offers, f, ensure_ascii=False, indent=2)
    print(f"📄 Résultats sauvegardés: {output_file}")

    # Retourner pour injection dans Google Sheets
    return offers


if __name__ == "__main__":
    offers = main()
    if offers:
        print(f"\n🎯 Prêt à injecter dans Google Sheets: {len(offers)} offres")
