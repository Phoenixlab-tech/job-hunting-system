# MCP Config — Google Sheets

## Utilisation
Stockage central des offres d'emploi récupérées par l'Agent 1, scores calculés par l'Agent 2, et suivi des candidatures.

## Google Sheet à créer
- Nom : "Job Hunter — Offres"
- Onglet 1 : "Offres" (offres récupérées)
- Onglet 2 : "Suivi" (candidatures envoyées)

## Structure Onglet "Offres"

| Colonne | Nom | Type | Rempli par |
|---------|-----|------|------------|
| A | id_offre | Texte | Agent 1 |
| B | titre | Texte | Agent 1 |
| C | entreprise | Texte | Agent 1 |
| D | lieu | Texte | Agent 1 |
| E | distance_km | Nombre | Agent 1 |
| F | salaire | Texte | Agent 1 |
| G | contrat | Texte | Agent 1 |
| H | date_publication | Date | Agent 1 |
| I | casquette | Texte | Agent 1 |
| J | score_match | Nombre | Agent 2 |
| K | description | Texte | Agent 1 |
| L | competences | Texte | Agent 1 |
| M | url_offre | URL | Agent 1 |
| N | statut | Texte | Manuel |
| O | points_forts | Texte | Agent 2 |
| P | points_faibles | Texte | Agent 2 |

## Structure Onglet "Suivi"

| Colonne | Nom | Type |
|---------|-----|------|
| A | id_offre | Texte |
| B | titre | Texte |
| C | entreprise | Texte |
| D | date_candidature | Date |
| E | cv_fichier | Texte |
| F | lm_fichier | Texte |
| G | statut | Texte (envoyé/lu/réponse/refus/entretien) |
| H | date_relance | Date |
| I | notes | Texte |

## MCP Server
- Nom : Google Sheets
- Déjà connecté dans Claude
- Permissions : lecture + écriture
