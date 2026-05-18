#!/usr/bin/env python3
"""Quick test for Agent 3"""

import json
from pathlib import Path

# Check files
project_root = Path(__file__).parent
profile_path = project_root / "data" / "mon-profil.json"
offers_path = project_root / "outputs" / "offers_scored.json"

print(f"Profile exists: {profile_path.exists()}")
print(f"Offers exist: {offers_path.exists()}")

if offers_path.exists():
    with open(offers_path) as f:
        offers = json.load(f)
    print(f"Offers loaded: {len(offers)} offres")
    if offers:
        best = max(offers, key=lambda x: x.get("score_match", 0))
        print(f"Best offer: {best.get('titre')} (score: {best.get('score_match')})")
