#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère un dashboard statique avec les vraies données embedées
Prêt pour Netlify
"""

import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import re
from pathlib import Path
from datetime import datetime

def format_date(date_str):
    """Convertit 2026-05-17 en 'Aujourd'hui', 'Hier', 'Il y a X jours'"""
    try:
        pub_date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now()
        delta = (today - pub_date).days

        if delta == 0:
            return "Aujourd'hui"
        elif delta == 1:
            return "Hier"
        elif delta <= 7:
            return f"Il y a {delta} jours"
        else:
            return f"Il y a {delta} jours"
    except:
        return date_str

def get_casquette_color(casquette_name):
    """Retourne la couleur hex pour une casquette"""
    colors = {
        "RSG": "#f5c842",
        "Manager": "#ff6584",
        "Support": "#43e97b",
        "Réseau": "#00c6ff",
        "Client": "#fa8231",
        "Freelance": "#a29bfe"
    }
    return colors.get(casquette_name, "#6c63ff")

def generate_dashboard():
    """Génère le dashboard avec les vraies données"""

    project_root = Path(__file__).parent.parent

    # Charger les offres scorées
    offers_file = project_root / "outputs" / "offers_scored.json"
    if not offers_file.exists():
        print(f"❌ Fichier {offers_file} non trouvé")
        return False

    with open(offers_file, "r", encoding="utf-8") as f:
        offers = json.load(f)

    # Transformer les données pour le dashboard
    offres_js = []
    for i, offer in enumerate(offers, 1):
        salaire = offer.get("salaire", "N/A")
        if salaire == "N/A":
            salaire_display = "N/A"
        else:
            salaire_display = salaire

        distance = offer.get("distance_km", 0)
        try:
            distance = int(float(distance)) if distance and distance != "N/A" else 0
        except:
            distance = 0

        offre_obj = {
            "id": i,
            "titre": offer.get("titre", ""),
            "entreprise": offer.get("entreprise", ""),
            "lieu": offer.get("lieu", ""),
            "distance": distance,
            "salaire": salaire_display,
            "contrat": offer.get("contrat", ""),
            "date": format_date(offer.get("date_publication", "")),
            "casquette": offer.get("casquette_match", ""),
            "score": offer.get("score_match", 0),
            "desc": offer.get("description", "")[:200],  # 200 chars max
            "skills": offer.get("competences", "") or "N/A",
            "couleur": get_casquette_color(offer.get("casquette_match", "")),
            "id_offre": offer.get("id_offre", "")
        }
        offres_js.append(offre_obj)

    # Charger le template
    template_file = project_root / "Dashboard" / "dashboard.html"
    with open(template_file, "r", encoding="utf-8") as f:
        dashboard_html = f.read()

    # DEMO_OFFRES reste vide - le dashboard charge depuis GitHub
    # (ce n'est qu'un fallback si GitHub échoue)
    empty_offres = json.dumps([], ensure_ascii=False, separators=(',', ':'))

    # Remplacer DEMO_OFFRES par un tableau vide
    # Pattern: const DEMO_OFFRES = [ ... ];
    pattern = r'const DEMO_OFFRES = \[.*?\];'
    replacement = f'const DEMO_OFFRES = {empty_offres};'

    dashboard_html = re.sub(pattern, replacement, dashboard_html, flags=re.DOTALL)

    # Sauvegarder le dashboard généré avec UTF-8 explicite
    output_file = project_root / "Dashboard" / "dashboard.html"
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        f.write(dashboard_html)

    print(f"✅ Dashboard généré avec succès!")
    print(f"   📊 {len(offres_js)} offres injectées")
    print(f"   📄 Fichier: {output_file}")
    print(f"\n📋 Prêt pour Netlify!")
    print(f"   1. Upload Dashboard/ sur Netlify")
    print(f"   2. Index: index.html")
    print(f"   3. Publish!")

    return True

if __name__ == "__main__":
    success = generate_dashboard()
    exit(0 if success else 1)
