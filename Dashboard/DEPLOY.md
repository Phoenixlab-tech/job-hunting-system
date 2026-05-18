# 🚀 Déployer sur Netlify

## Préparation

Le dashboard est **100% statique** — pas de backend, pas de base de données.

Fichiers à uploader:
- `index.html` (login page)
- `dashboard.html` (dashboard avec 460 offres)
- `netlify.toml` (config Netlify)

## Étapes

### 1. Générer le dashboard avec les vraies données
```bash
python code/generate_dashboard.py
```

Ça injecte les 460 offres de `outputs/offers_scored.json` dans `dashboard.html`.

### 2. Upload sur Netlify

**Option A : Drag & Drop (plus simple)**
1. Va sur https://app.netlify.com
2. Crée un nouveau site
3. Drag le dossier `Dashboard/` entier
4. Boom! 🎉 Ton site est live

**Option B : CLI Netlify**
```bash
npm install -g netlify-cli
netlify deploy --dir Dashboard/
```

**Option C : GitHub + Auto Deploy**
1. Push le dossier `Dashboard/` sur GitHub
2. Connecte le repo à Netlify
3. Chaque push = redeploy automatique

## Après chaque mise à jour

1. Relance `python code/generate_dashboard.py` pour injecter les nouvelles offres
2. Redeploy sur Netlify (drag/drop ou `netlify deploy`)

## Résultat

- URL: `https://ton-site.netlify.app`
- Login: Mot de passe défini dans `index.html` (ligne 10: `var MDP = "TON_MDP_ICI"`)
- Dashboard: 460 offres avec scores, filtres, génération CV/LM

## Notes

- **Pas de backend = pas de coûts**
- Les données sont embedées dans le HTML (460 offres ≈ 1-2 MB)
- Rechargement = réinitialise les sélections (normal, c'est du statique)
- Pour persister les sélections → faudrait un backend (API + BD)
