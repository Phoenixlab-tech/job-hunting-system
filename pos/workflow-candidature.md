# POS — Workflow Candidature

## Déclenchement
Après sélection d'offres dans le dashboard

## Étapes

### 1. Sélection offre dans le dashboard
- Cocher l'offre
- Vérifier le score (idéalement > 70%)
- Cliquer "Détail" pour lire la description complète

### 2. Génération CV
- Cliquer bouton "CV" sur l'offre
- Agent 3 identifie la casquette correspondante
- Génère CV ATS-friendly adapté à l'offre
- Export PDF dans /outputs/cv-[entreprise]-[date].pdf

### 3. Génération LM
- Cliquer bouton "LM" sur l'offre
- Agent 3 génère LM personnalisée
- Export PDF dans /outputs/lm-[entreprise]-[date].pdf

### 4. Vérification (Arnaud)
- Relire le CV : accroche OK ? Mots-clés OK ?
- Relire la LM : ton OK ? Pas de formules creuses ?
- Ajuster si besoin (demander à Claude de reformuler)

### 5. Envoi candidature
- Via le site de l'offre (lien dans le dashboard)
- Ou via Gmail (Agent 3 peut préparer le mail)
- Mettre à jour le statut dans Google Sheets : "postulé"

### 6. Suivi
- Mettre à jour Google Sheets si réponse reçue
- Relance possible après 7 jours sans réponse

## Nommage fichiers
- CV : `cv-[casquette]-[entreprise]-[date].pdf`
- LM : `lm-[casquette]-[entreprise]-[date].pdf`
- Exemple : `cv-rsg-safran-2026-05-17.pdf`
