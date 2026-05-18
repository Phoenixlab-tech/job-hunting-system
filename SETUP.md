# Job Hunting System — Setup Checklist

## Prerequisites (Completed ✅)
- [x] France Travail API credentials in `.env`
- [x] Google Sheets service account configured
- [x] Python code structure ready
- [x] OAuth authentication tested (works)

## Critical Blocker: France Travail API Permissions ⚠️
**Status**: API returns 403 "insufficient_scope" on search endpoint

### Action Required:
1. Go to: https://francetravail.io/data/api
2. Login to your developer account
3. Find application: **"agentemploiarnaud"**
4. Grant permission for: **"Offres d'emploi v2 - Recherche"**
5. Save changes
6. Test with: `python code/test_api_direct.py`

**Expected output after fix**: Should show job offers instead of 403 error.

---

## Setup Steps (After API Permissions Fixed)

### 1. Create Google Sheet
- Go to: https://docs.google.com/spreadsheets/create
- Name it: **"Job Hunter — Offres"**
- Rename sheet tab: "Feuille 1" → **"Offres"**
- Add headers (columns A-N):
  - A: id_offre
  - B: titre
  - C: entreprise
  - D: lieu
  - E: distance_km
  - F: salaire
  - G: contrat
  - H: date_publication
  - I: casquette
  - J: score_match
  - K: description
  - L: competences
  - M: url_offre
  - N: statut

### 2. Share Google Sheet
- Click "Share" button
- Add: `job-hunter@make-agent-emploi.iam.gserviceaccount.com`
- Role: **Editor**
- Uncheck "Notify people"
- Share

### 3. Run Agent 1
```bash
python code/run_agent_1.py
```
This will:
- Fetch 24 job offers (6 profiles × 4 keywords)
- Deduplicate
- Inject into Google Sheets
- Save JSON to `outputs/offers.json`

---

## Test Commands

```bash
# Test API connection (shows detailed error if permissions not granted)
python code/test_api_direct.py

# Test full Agent 1 pipeline
python code/run_agent_1.py

# Test Google Sheets injection with mock data
python code/test_google_sheets.py
```

---

## Troubleshooting

**403 Insufficient Scope**
→ API permissions not granted in France Travail dashboard

**Google Sheet Not Found**
→ Create manually and share with service account email

**No Offers Found**
→ Check that keywords in `data/casquettes.json` are valid French job titles

---

## Architecture Summary

```
Data Source (France Travail API)
        ↓
   Agent 1: Fetch & Format
        ↓
   Google Sheets (offers stored)
        ↓
   Agent 2: Score & Match
        ↓
   Agent 3: Generate Applications
```
