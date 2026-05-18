#!/usr/bin/env python3
"""
Agent 2 — Job Matcher
Calcule un score de match entre chaque offre et les 6 casquettes d'Arnaud
"""

import json
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Optional
import re
from datetime import datetime, timedelta

class JobMatcher:
    """Matche les offres avec les casquettes et calcule un score"""

    def __init__(self, casquettes: Dict):
        self.casquettes = casquettes["casquettes"]

    def get_google_sheets_client(self):
        """Initialise le client Google Sheets"""
        try:
            creds_path = "mcp-config/google-sheets-credentials.json"
            credentials = Credentials.from_service_account_file(
                creds_path,
                scopes=["https://www.googleapis.com/auth/spreadsheets"]
            )
            client = gspread.authorize(credentials)
            return client
        except Exception as e:
            print(f"❌ Erreur authentification Google: {str(e)}")
            return None

    def calculate_match_score(self, offer: Dict, casquette: Dict) -> Dict:
        """
        Calcule le score de match entre une offre et une casquette
        Retourne: {score: 0-100, details: {...}}
        """
        score = 0
        details = {
            "keywords_match": 0,
            "contract_match": 0,
            "distance_bonus": 0,
            "recency_bonus": 0
        }

        # 1. Matchage des mots-clés (50 points max)
        keywords = casquette.get("mots_cles_ats", [])
        search_text = f"{offer.get('titre', '')} {offer.get('description', '')}".lower()

        keyword_matches = 0
        for kw in keywords:
            if kw.lower() in search_text:
                keyword_matches += 1

        if keywords:
            details["keywords_match"] = int((keyword_matches / len(keywords)) * 50)
            score += details["keywords_match"]

        # 2. Matchage contrat (20 points max)
        contract_type = offer.get("contrat", "").upper()
        accepted_contracts = [c.upper() for c in casquette.get("contrats", [])]

        if contract_type in accepted_contracts:
            details["contract_match"] = 20
            score += 20

        # 3. Bonus distance (15 points max)
        distance = offer.get("distance_km")
        if isinstance(distance, (int, float)):
            if distance <= 25:
                details["distance_bonus"] = 15
                score += 15
            elif distance <= 50:
                details["distance_bonus"] = 10
                score += 10
            elif distance <= 75:
                details["distance_bonus"] = 5
                score += 5

        # 4. Bonus récence (15 points max)
        pub_date_str = offer.get("date_publication", "")
        if pub_date_str:
            try:
                pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d")
                days_old = (datetime.now() - pub_date).days

                if days_old <= 3:
                    details["recency_bonus"] = 15
                    score += 15
                elif days_old <= 7:
                    details["recency_bonus"] = 10
                    score += 10
                elif days_old <= 14:
                    details["recency_bonus"] = 5
                    score += 5
            except:
                pass

        return {
            "score": min(score, 100),
            "details": details,
            "casquette_id": casquette["id"],
            "casquette_nom": casquette["nom"]
        }

    def match_offers(self, offers: List[Dict]) -> List[Dict]:
        """
        Matche tous les offres et retourne avec scores
        """
        matched_offers = []

        for offer in offers:
            # Calculer le score pour chaque casquette
            best_match = None
            best_score = 0

            for casquette in self.casquettes:
                result = self.calculate_match_score(offer, casquette)
                if result["score"] > best_score:
                    best_score = result["score"]
                    best_match = result

            # Ajouter le score et casquette match à l'offre
            offer["score_match"] = best_score
            if best_match:
                offer["casquette_match"] = best_match["casquette_nom"]

            matched_offers.append(offer)

        return matched_offers

    def inject_scores_to_sheets(self, sheet_id: str, matched_offers: List[Dict]) -> bool:
        """Injecte les scores dans Google Sheets en une seule opération"""
        client = self.get_google_sheets_client()
        if not client:
            return False

        try:
            spreadsheet = client.open_by_key(sheet_id)
            worksheet = spreadsheet.worksheet("Offres")

            # Récupérer les offres existantes
            all_rows = worksheet.get_all_values()

            if not all_rows:
                print("❌ Aucune donnée dans le sheet")
                return False

            # Créer un mapping id_offre -> score
            score_map = {offer["id_offre"]: offer["score_match"] for offer in matched_offers}

            # Construire la liste des scores pour la colonne J
            print("📝 Mise à jour des scores dans le sheet...")

            score_values = []
            for i, row in enumerate(all_rows[1:], start=2):  # Skip header
                if row:
                    offer_id = row[0] if row else ""
                    if offer_id in score_map:
                        score = int(score_map[offer_id])
                        score_values.append([score])
                    else:
                        score_values.append([""])
                else:
                    score_values.append([""])

            # Update la plage J2:J{n} en une seule opération
            if score_values:
                end_row = len(all_rows)
                range_str = f"J2:J{end_row}"
                worksheet.update(range_str, score_values)
                print(f"✅ {len(score_values)} scores mis à jour en une opération")

            return True

        except Exception as e:
            print(f"❌ Erreur injection scores: {str(e)}")
            return False


def main(sheet_id: str = None):
    """Point d'entrée principal"""

    # Charger les casquettes
    with open("data/casquettes.json", "r", encoding="utf-8") as f:
        casquettes = json.load(f)

    # Charger les offres depuis le JSON
    try:
        with open("outputs/offers.json", "r", encoding="utf-8") as f:
            offers = json.load(f)
    except FileNotFoundError:
        print("❌ Fichier outputs/offers.json non trouvé")
        print("   Exécutez d'abord Agent 1")
        return False

    print(f"📊 Chargement de {len(offers)} offres...")

    # Matcher les offres
    matcher = JobMatcher(casquettes)
    print("🎯 Calcul des scores de match...")

    matched_offers = matcher.match_offers(offers)

    # Statistiques
    avg_score = sum(o.get("score_match", 0) for o in matched_offers) / len(matched_offers) if matched_offers else 0
    high_matches = [o for o in matched_offers if o.get("score_match", 0) >= 70]
    medium_matches = [o for o in matched_offers if 40 <= o.get("score_match", 0) < 70]
    low_matches = [o for o in matched_offers if o.get("score_match", 0) < 40]

    print(f"\n📈 Résultats du matching:")
    print(f"   Score moyen: {avg_score:.1f}/100")
    print(f"   Matches excellents (>=70): {len(high_matches)}")
    print(f"   Matches bons (40-70): {len(medium_matches)}")
    print(f"   Matches faibles (<40): {len(low_matches)}")

    # Sauvegarder les scores en JSON
    with open("outputs/offers_scored.json", "w", encoding="utf-8") as f:
        json.dump(matched_offers, f, ensure_ascii=False, indent=2)
    print("📄 Offres scorées sauvegardées: outputs/offers_scored.json")

    # Injecter dans Google Sheets
    if sheet_id:
        print("\n📤 Injection des scores dans Google Sheets...")
        success = matcher.inject_scores_to_sheets(sheet_id, matched_offers)
        if success:
            print("✅ Scores injectés avec succès")
            return True
        else:
            print("⚠️  Injection échouée")
            return False
    else:
        print("⚠️  Pas de sheet_id fourni - offres scorées en JSON uniquement")
        return True


if __name__ == "__main__":
    sheet_id = "1rdDZzXMXxs3Tm5-2zcAgwF4vjkhl4zYP21X7BRPv8rY"
    success = main(sheet_id=sheet_id)
