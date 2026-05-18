#!/usr/bin/env python3
"""
Orchestrateur — Agent 2 (Job Matcher)
Lance le matching et injection des scores
"""

import os
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv(project_root / ".env")


def main():
    """Orchestrateur principal"""

    print("\n" + "="*60)
    print("🤖 Job Hunting System — Agent 2 Orchestrator")
    print("="*60)

    os.chdir(project_root)

    try:
        from agent_2_matcher import main as run_matcher

        # Sheet ID
        sheet_id = "1rdDZzXMXxs3Tm5-2zcAgwF4vjkhl4zYP21X7BRPv8rY"

        # Exécuter le matcher
        success = run_matcher(sheet_id=sheet_id)

        if success:
            print("\n" + "="*60)
            print("🎉 Agent 2 — Exécution réussie!")
            print("="*60)
            print("\n📋 Prochaines étapes:")
            print("  1. Ouvrez: https://docs.google.com/spreadsheets")
            print("  2. Consultez le sheet 'Job Hunter — Offres'")
            print("  3. Triez par colonne J (score_match) pour voir les meilleures offres")
            print("  4. Lancez ensuite Agent 3 (Application Generator)")
            print("\nCommande Agent 3:")
            print("  python code/run-agent-3.py")
            return True
        else:
            print("\n❌ Agent 2 échoué")
            return False

    except Exception as e:
        print(f"❌ Erreur Agent 2: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
