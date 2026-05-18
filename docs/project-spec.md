# Project Spec — Job Hunting System

## Résumé
Système automatisé de recherche d'emploi pour Arnaud Chédeville utilisant l'architecture multi-agents Elliott Pierret (Claude Code + MCP Servers + Skills + Plugin Export).

## Stack
- **Orchestration :** Claude Code
- **API :** France Travail (francetravail.io)
- **Base de données :** Google Sheets
- **Dashboard :** HTML/CSS/JS hébergé sur Netlify
- **Génération documents :** Claude (CV + LM en Markdown → PDF)
- **Stockage :** Google Drive
- **Email :** Gmail (envoi candidatures)

## Architecture agents

```
[API France Travail]
       ↓
[Agent 1: Job Fetcher]
       ↓
[Google Sheets] ← stockage central
       ↓
[Agent 2: Job Matcher]
       ↓
[Google Sheets] ← scores mis à jour
       ↓
[Dashboard HTML] → sélection manuelle Arnaud
       ↓
[Agent 3: Application Generator]
       ↓
[CV PDF + LM PDF] → Google Drive → Gmail
```

## URLs
- Dashboard : https://fanciful-begonia-249b72.netlify.app/
- API France Travail : https://francetravail.io (compte à créer)

## Prérequis
- [ ] Compte France Travail API (Client ID + Secret)
- [ ] Google Sheet "Job Hunter — Offres" créé
- [ ] MCP Google Sheets connecté dans Claude
- [ ] MCP Google Drive connecté dans Claude
- [ ] MCP Gmail connecté dans Claude

## Timeline
- Phase 1 : Dashboard + protection (FAIT)
- Phase 2 : Agents + fichiers projet (FAIT)
- Phase 3 : Branchement API France Travail
- Phase 4 : Scoring automatique
- Phase 5 : Génération CV/LM en PDF
- Phase 6 : Envoi candidatures via Gmail
