#!/usr/bin/env python3
"""
Orchestrateur — Agent 3 (Application Generator)
Lance la génération du CV et lettre de motivation
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
    print("🤖 Job Hunting System — Agent 3 Orchestrator")
    print("="*60)

    os.chdir(project_root)

    # Vérifier que Claude API key est configurée
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n⚠️  CONFIGURATION MANQUANTE")
        print("Ajoutez votre clé Claude API dans .env:")
        print("  ANTHROPIC_API_KEY=sk-ant-...")
        print("\nObtenir une clé sur: https://console.anthropic.com/")
        return False

    try:
        from agent_3_generator import main as run_generator

        # Récupérer l'offre ID depuis argument (optionnel)
        offer_id = sys.argv[1] if len(sys.argv) > 1 else None

        # Exécuter le générateur
        success = run_generator(offer_id=offer_id)

        if success:
            print("\n" + "="*60)
            print("🎉 Agent 3 — Exécution réussie!")
            print("="*60)
            print("\n📋 Prochaines étapes:")
            print("  1. Vérifiez les fichiers dans: outputs/")
            print("  2. Ajustez le CV et la LM si nécessaire")
            print("  3. Copiez-collez dans votre candidature")
            return True
        else:
            print("\n❌ Agent 3 échoué")
            return False

    except Exception as e:
        print(f"❌ Erreur Agent 3: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
