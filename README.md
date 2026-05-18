# Job Hunting System 🎯

Système automatisé de recherche d'emploi multi-agents pour Arnaud Chédeville.  
Récupère offres France Travail → Filtre par 6 casquettes → Génère CV + LM personnalisés.

---

## 🚀 Démarrage rapide

### Étape 0️⃣ : Prérequis
```bash
# 1. Cloner/télécharger le projet
cd job-hunting-system

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer .env avec vos credentials
cp .env.example .env
# ← Puis remplissez vos credentials API
```

### Étape 1️⃣ : API France Travail
**Source** : https://francetravail.io/data/api

1. Créer un compte
2. Générer Client ID + Client Secret
3. Copier dans `.env` :
   ```
   FRANCE_TRAVAIL_CLIENT_ID=votre_id
   FRANCE_TRAVAIL_CLIENT_SECRET=votre_secret
   ```

### Étape 2️⃣ : Google Sheets
**Source** : https://console.cloud.google.com

1. Créer projet Google Cloud
2. Activer API Google Sheets
3. Service account → Télécharger clé JSON
4. Sauvegarder dans `mcp-config/google-sheets-credentials.json`
5. Créer Google Sheet "Job Hunter — Offres" (2 onglets : "Offres" + "Suivi")

### Étape 3️⃣ : Lancer Agent 1
```bash
python code/run-agent-1.py
```

Cela :
- ✅ Récupère offres France Travail
- ✅ Filtre par 6 casquettes
- ✅ Calcule distances (rayon 25km autour de Libourne)
- ✅ Injecte dans Google Sheets

---

## 📊 Architecture

| Agent | Rôle | Input | Output |
|-------|------|-------|--------|
| **Agent 1** | Job Fetcher | API France Travail | JSON offres + Google Sheets |
| **Agent 2** | Job Matcher | Google Sheets | Scores matching (0-100) |
| **Agent 3** | Generator | Offres sélectionnées | CV + LM personnalisés |

---

## 🎯 Les 6 casquettes

1. **RSG** — Responsable Services Généraux / Facility Manager
2. **Manager** — Manager d'Équipe Technique
3. **Support** — Technicien Support N2/N3
4. **Réseau** — Technicien Réseaux Informatiques
5. **Client** — Chargé Relation Client Technique B2B/B2C
6. **Freelance** — Consultant Automatisation No-Code

---

## 📁 Structure du projet

```
job-hunting-system/
├── .context.md              ← Contexte projet
├── .env.example             ← Template credentials
├── SETUP.md                 ← Guide setup détaillé
├── README.md                ← Ce fichier
├── requirements.txt         ← Dépendances Python
├── agents/
│   ├── agent-1-fetcher.md   ← Prompt Agent 1
│   ├── agent-2-matcher.md   ← Prompt Agent 2
│   └── agent-3-generator.md ← Prompt Agent 3
├── code/
│   ├── agent-1-fetcher.py      ← Job Fetcher (API)
│   ├── google-sheets-injector.py
│   └── run-agent-1.py        ← Orchestrateur Agent 1
├── data/
│   ├── mon-profil.json      ← Profil Arnaud
│   └── casquettes.json      ← Définition 6 casquettes
├── mcp-config/
│   ├── google-sheets-setup.md
│   └── google-sheets-credentials.json ← À créer
├── outputs/
│   └── offers.json          ← Résultats Agent 1
└── examples/                ← Templates CV/LM
```

---

## 🔧 Configuration détaillée

### 1. API France Travail
```env
FRANCE_TRAVAIL_CLIENT_ID=your_client_id
FRANCE_TRAVAIL_CLIENT_SECRET=your_client_secret
```

**Tests** :
- Consulter https://francetravail.io/data/api/documentation
- Sandbox disponible pour tester

### 2. Google Sheets
```env
GOOGLE_SHEETS_CREDENTIALS=mcp-config/google-sheets-credentials.json
```

**Structure sheet** :
- Onglet "Offres" : colonnes A-N (voir mcp-config/google-sheets-setup.md)
- Onglet "Suivi" : candidatures envoyées

### 3. Variables de recherche
```json
// data/casquettes.json — Mots-clés ATS automatiques par casquette
{
  "casquettes": [
    {
      "id": 1,
      "nom": "RSG",
      "mots_cles_api": ["responsable services généraux", "facility manager", ...]
    },
    ...
  ]
}
```

---

## 📈 Workflow quotidien

**Matin** (15 min) :
```bash
# 1. Récupérer offres du jour
python code/run-agent-1.py

# 2. Consulter Google Sheet
# → https://docs.google.com/spreadsheets

# 3. Attendre scoring Agent 2
```

**Après-midi** (selon offres sélectionnées) :
```bash
# 4. Générer CV + LM (Agent 3)
python code/run-agent-3.py --offres-ids="id1,id2,id3"

# 5. Consulter Drive
# → Dossier /outputs/
```

---

## 📊 Exemple de résultat Agent 1

```json
{
  "id_offre": "12345678",
  "titre": "Technicien Support N3",
  "entreprise": "Acme Corp",
  "lieu": "Libourne (33500)",
  "distance_km": 8.5,
  "salaire": "2200€",
  "contrat": "CDI",
  "date_publication": "2026-05-15",
  "casquette": 3,
  "competences": "Support | Dépannage | Windows | Firmware",
  "url_offre": "https://...",
  "statut": "nouveau"
}
```

---

## 🐛 Dépannage

| Erreur | Solution |
|--------|----------|
| `ModuleNotFoundError: gspread` | `pip install -r requirements.txt` |
| `FRANCE_TRAVAIL_CLIENT_ID not found` | Remplissez `.env` |
| `Sheet 'Job Hunter — Offres' not found` | Créez manuellement le Google Sheet |
| `KeyError: casquettes` | Vérifiez `data/casquettes.json` |

---

## 💡 Optimisations budget

- **API France Travail** : Gratuite ✅
- **Google Sheets** : Gratuit ✅
- **Requêtes API** : 150/jour (suffisant)
- **Stockage Drive** : 15GB gratuit (généralement OK)

**À surveiller** : Nombre d'appels API (fetch quotidien = ~30 requêtes)

---

## 📞 Contact

**Arnaud Chédeville**
- Email : Arnaudchedeville@gmail.com
- Tél : 06 29 62 04 02
- Localisation : Izon (33450)
- Recherche : Libourne, rayon 25km

---

## 📝 Notes importantes

- ⏰ **Ancienneté max offres** : 30 jours
- 📍 **Localisation** : Libourne (33500), +25km
- 🎓 **Contrats acceptés** : CDI, CDD, Freelance, Intérim
- 🔑 **Mots-clés ATS** : Définis par casquette dans `data/casquettes.json`

---

**Version** : 1.0  
**Dernière mise à jour** : 2026-05-17  
**Status** : ✅ Prêt à déployer
