# ⚡ Quick Start — 5 minutes

## Étapes avant de lancer le Job Fetcher

### 1. France Travail API (5 min) 🇫🇷
```
1. Aller sur https://francetravail.io/data/api
2. S'inscrire (gratuit)
3. Créer une application
4. Copier : Client ID + Client Secret
5. Ouvrir .env du projet
6. Remplacer :
   FRANCE_TRAVAIL_CLIENT_ID=votre_id
   FRANCE_TRAVAIL_CLIENT_SECRET=votre_secret
```

### 2. Google Cloud Setup (5 min) ☁️
```
1. Aller sur https://console.cloud.google.com
2. Créer un projet
3. Rechercher "Google Sheets API" → Activer
4. Aller dans "Service Accounts"
5. Créer service account
6. Générer clé JSON
7. Télécharger le fichier JSON
8. Le placer dans :
   mcp-config/google-sheets-credentials.json
```

### 3. Google Sheets (2 min) 📊
```
1. Aller sur https://docs.google.com/spreadsheets
2. Créer un nouveau sheet
3. Le nommer : "Job Hunter — Offres"
4. Créer 2 onglets :
   - "Offres"
   - "Suivi"
5. Voilà ! Les colonnes seront remplies automatiquement
```

### 4. Python (2 min) 🐍
```bash
# Dans le terminal, à la racine du projet :
pip install -r requirements.txt
```

---

## 🚀 Lancer le Job Fetcher

```bash
python code/run-agent-1.py
```

**Ça va** :
✅ Récupérer offres France Travail (6 casquettes)  
✅ Filtrer par rayon 25km autour de Libourne  
✅ Calculer distances  
✅ Injecter dans Google Sheets "Job Hunter — Offres"  

**Résultat** : 
→ Consultez le Google Sheet pour voir les offres !

---

## 📊 C'est quoi après ?

Après Agent 1, il y a 2 autres agents :

**Agent 2 — Matcher** :
- Score chaque offre (0-100) vs votre profil
- À faire après

**Agent 3 — Generator** :
- Génère CV + LM personalisés
- À faire pour les offres sélectionnées

---

## 🎯 Résumé rapide

| Étape | Temps | Action |
|-------|-------|--------|
| 1 | 5 min | API France Travail |
| 2 | 5 min | Google Cloud Setup |
| 3 | 2 min | Google Sheets |
| 4 | 2 min | pip install |
| **Total** | **14 min** | **Prêt !** |

Après setup → `python code/run-agent-1.py` suffit !

---

## 🆘 Ça bloque ?

**Erreur : "Client credentials not found"**
→ Vérifiez `.env` (bien remplies ?)

**Erreur : "Sheet not found"**
→ Créez le Google Sheet "Job Hunter — Offres"

**Erreur : "ModuleNotFoundError"**
→ `pip install -r requirements.txt`

---

## ✨ Les 6 casquettes qu'on cherche

1. 🏢 **RSG** — Responsable Services Généraux
2. 👥 **Manager** — Manager d'équipe technique
3. 🛠️ **Support** — Technicien Support N2/N3
4. 🌐 **Réseau** — Technicien Réseaux
5. 📞 **Client** — Chargé Relation Client
6. ⚙️ **Freelance** — Consultant Automatisation

Tout ça en même temps → France Travail API filtre automatiquement.

---

**Prêt ? Lancez : `python code/run-agent-1.py` 🚀**
