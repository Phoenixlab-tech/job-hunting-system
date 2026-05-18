#!/usr/bin/env python3
"""
Agent 3 — Application Generator
Génère un CV ATS + lettre de motivation personnalisés pour une offre
"""

import json
import os
from pathlib import Path
from datetime import datetime
import anthropic


class ApplicationGenerator:
    """Génère CV et lettre de motivation adaptés à une offre"""

    def __init__(self, profile_path: str, offers_path: str):
        self.profile = self._load_json(profile_path)
        self.offers = self._load_json(offers_path)
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def _load_json(self, path: str) -> dict:
        """Charge un fichier JSON"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise FileNotFoundError(f"Impossible de lire {path}: {str(e)}")

    def select_offer(self, offer_id: str = None) -> dict:
        """Sélectionne une offre par ID ou utilise la meilleure"""
        if offer_id:
            for offer in self.offers:
                if offer.get("id_offre") == offer_id:
                    return offer
            raise ValueError(f"Offre {offer_id} non trouvée")

        # Retourner la meilleure offre (score le plus élevé)
        best = max(self.offers, key=lambda x: x.get("score_match", 0))
        return best

    def generate_cv(self, offer: dict) -> str:
        """Génère un CV ATS adapté à l'offre"""
        prompt = f"""Tu es un expert en rédaction de CV ATS (optimisé pour les systèmes de scanning).

PROFIL CANDIDAT:
{json.dumps(self.profile, ensure_ascii=False, indent=2)}

OFFRE D'EMPLOI:
Titre: {offer.get('titre', '')}
Entreprise: {offer.get('entreprise', '')}
Description: {offer.get('description', '')}
Casquette cible: {offer.get('casquette_match', '')}

Génère un CV ATS-friendly en Markdown pour cette offre:
1. Adapte l'accroche aux besoins de l'offre
2. Réordonne les expériences par pertinence (la plus récente/pertinente d'abord)
3. Mets en avant les compétences qui matchent l'offre
4. Garde un format strictement lisible (pas de graphiques, pas de couleurs)
5. Inclus les habilitations électriques si pertinent pour le poste
6. Format: PRENOM NOM, email, téléphone, adresse en en-tête

CV résultat:"""

        message = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    def generate_cover_letter(self, offer: dict) -> str:
        """Génère une lettre de motivation personnalisée"""
        prompt = f"""Tu es un expert en lettres de motivation pour candidatures en France.

PROFIL CANDIDAT:
Nom: {self.profile.get('nom', '')}
Adresse: {self.profile.get('adresse', '')}
Téléphone: {self.profile.get('telephone', '')}
Email: {self.profile.get('email', '')}
Années d'expérience: {self.profile.get('annees_experience', '')}
Compétences clés: {', '.join(self.profile.get('competences_cles', []))}
Expériences: {json.dumps(self.profile.get('experiences', []), ensure_ascii=False, indent=2)}

OFFRE D'EMPLOI:
Titre: {offer.get('titre', '')}
Entreprise: {offer.get('entreprise', '')}
Description: {offer.get('description', '')}
Casquette cible: {offer.get('casquette_match', '')}

Génère une lettre de motivation personnalisée:
1. Début avec adresse + date (format français)
2. Accroche percutante: montre que tu connais l'offre
3. 2-3 paragraphes: expériences pertinentes + résultats quantifiés
4. Paragraphe de conclusion: dispo + demande d'entretien
5. Signature: Cordialement, Nom Prénom
6. Longueur: ~250 mots, professionnel et chaleureux

Lettre résultat:"""

        message = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    def save_documents(self, cv: str, letter: str, offer: dict, output_dir: str = "outputs") -> dict:
        """Sauvegarde CV et lettre de motivation"""
        os.makedirs(output_dir, exist_ok=True)

        # Noms de fichiers basés sur l'offre
        offer_id = offer.get("id_offre", "unknown")
        casquette = offer.get("casquette_match", "applicant").lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        cv_filename = f"{output_dir}/CV_{casquette}_{offer_id}_{timestamp}.md"
        letter_filename = f"{output_dir}/LM_{casquette}_{offer_id}_{timestamp}.md"

        # Sauvegarde CV
        with open(cv_filename, 'w', encoding='utf-8') as f:
            f.write(f"# CV ATS — {offer.get('titre', '')}\n\n")
            f.write(f"**Offre:** {offer.get('titre', '')} ({casquette})\n")
            f.write(f"**Entreprise:** {offer.get('entreprise', '')}\n")
            f.write(f"**Généré:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(cv)

        # Sauvegarde lettre
        with open(letter_filename, 'w', encoding='utf-8') as f:
            f.write(f"# Lettre de Motivation — {offer.get('titre', '')}\n\n")
            f.write(f"**Offre:** {offer.get('titre', '')} ({casquette})\n")
            f.write(f"**Entreprise:** {offer.get('entreprise', '')}\n")
            f.write(f"**Généré:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(letter)

        return {
            "cv_path": cv_filename,
            "letter_path": letter_filename,
            "offer_id": offer_id,
            "casquette": casquette
        }


def main(offer_id: str = None, output_dir: str = "outputs") -> bool:
    """Orchestrateur principal"""
    try:
        project_root = Path(__file__).parent.parent

        generator = ApplicationGenerator(
            profile_path=str(project_root / "data" / "mon-profil.json"),
            offers_path=str(project_root / "outputs" / "offers_scored.json")
        )

        # Sélectionner l'offre
        print("\n📋 Sélection de l'offre...")
        offer = generator.select_offer(offer_id)
        print(f"✅ Offre sélectionnée: {offer.get('titre')} (score: {offer.get('score_match')}/100)")

        # Générer CV
        print("\n📝 Génération du CV ATS...")
        cv = generator.generate_cv(offer)
        print("✅ CV généré")

        # Générer lettre
        print("\n💌 Génération de la lettre de motivation...")
        letter = generator.generate_cover_letter(offer)
        print("✅ Lettre générée")

        # Sauvegarder
        print(f"\n💾 Sauvegarde dans {output_dir}...")
        result = generator.save_documents(cv, letter, offer, output_dir=str(project_root / output_dir))
        print(f"✅ Fichiers sauvegardés:")
        print(f"   - CV: {result['cv_path']}")
        print(f"   - LM: {result['letter_path']}")

        return True

    except Exception as e:
        print(f"❌ Erreur Agent 3: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    offer_id = sys.argv[1] if len(sys.argv) > 1 else None
    success = main(offer_id=offer_id)
    sys.exit(0 if success else 1)
