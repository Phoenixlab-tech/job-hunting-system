# POS — Workflow Recherche d'Offres

## Déclenchement
Quotidien ou manuel (bouton dashboard)

## Étapes

### 1. Fetch offres (Agent 1)
- Appeler API France Travail avec les mots-clés des 6 casquettes
- Paramètres : Libourne 33500, rayon 25km, 30 derniers jours
- Dédupliquer les résultats
- Stocker dans Google Sheets

### 2. Scoring (Agent 2)
- Lire les nouvelles offres depuis Google Sheets
- Calculer score 0-100 pour chaque offre
- Écrire le score + détails dans Google Sheets

### 3. Affichage dashboard
- Le dashboard lit Google Sheets
- Affiche les offres triées par score
- Filtres : casquette, contrat, salaire min, score min

### 4. Sélection Arnaud
- Arnaud coche les offres intéressantes
- Clique "Générer CV + LM"

### 5. Génération (Agent 3)
- Pour chaque offre sélectionnée :
  - Identifier la casquette
  - Générer CV ATS adapté
  - Générer LM personnalisée
  - Stocker dans Google Drive

## Checklist quotidienne
- [ ] Offres récupérées (Agent 1)
- [ ] Scores calculés (Agent 2)
- [ ] Dashboard consulté
- [ ] Offres intéressantes sélectionnées
- [ ] CV + LM générés (Agent 3)
- [ ] Candidatures envoyées
