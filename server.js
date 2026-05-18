require('dotenv').config();
const express = require('express');
const path = require('path');
const Anthropic = require('@anthropic-ai/sdk');
const app = express();
const PORT = 3000;

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

app.use(express.json());
app.use(express.static(path.join(__dirname, 'Dashboard')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'Dashboard', 'dashboard.html'));
});

app.get('/api/offers', (req, res) => {
  const filePath = path.join(__dirname, 'outputs', 'offers_scored.json');
  res.sendFile(filePath, err => {
    if (err) res.status(404).json({ error: 'offers_scored.json introuvable — lance run_agent_2.py' });
  });
});

app.get('/api/profile', (req, res) => {
  const filePath = path.join(__dirname, 'data', 'mon-profil.json');
  res.sendFile(filePath, err => {
    if (err) res.status(404).json({ error: 'mon-profil.json introuvable' });
  });
});

app.post('/api/generate-cv-lm', async (req, res) => {
  try {
    const { offerId, profile, offer, docType } = req.body;

    if (!docType || !['cv', 'lm'].includes(docType)) {
      return res.status(400).json({ success: false, error: 'Invalid docType (cv or lm)' });
    }

    let content;
    if (docType === 'cv') {
      content = await generateCV(profile, offer);
    } else {
      content = await generateLM(profile, offer);
    }

    res.json({
      success: true,
      content: content,
      docType: docType,
      offerId: offerId,
    });
  } catch (error) {
    console.error('Generation error:', error);
    res.status(500).json({
      success: false,
      error: error.message,
    });
  }
});

async function generateCV(profile, offer) {
  const casquette = offer.casquette_match || 'RSG';
  const accroche = profile.accroches?.[casquette] || '';
  const competences = profile.competences?.[casquette] || '';

  // Toutes les expériences, ordre chronologique inversé (plus récent en premier)
  const toutesExp = profile.experiences || [];

  const prompt = `Tu es un EXPERT RH senior. Génère un CV pour Arnaud Chédeville en JSON STRICT.
RÈGLE ABSOLUE : réponds UNIQUEMENT avec le JSON valide, aucun texte avant ou après.

OFFRE CIBLÉE :
Titre : ${offer.titre}
Entreprise : ${offer.entreprise}
Lieu : ${offer.lieu}
Compétences requises : ${offer.skills || offer.competences || ''}
Casquette : ${casquette}

ACCROCHE À ADAPTER (intègre 2-3 mots-clés de l'offre) :
${accroche}

TOUTES LES EXPÉRIENCES (à inclure intégralement dans le CV, dans cet ordre) :
${toutesExp.map(e => `- ${e.poste} — ${e.entreprise} (${e.debut} – ${e.fin})\n  Missions : ${e.missions.join(' | ')}`).join('\n')}

COMPÉTENCES POUR LA CASQUETTE ${casquette} :
${competences}

FORMATIONS :
${(profile.formations || []).slice(0, 3).map(f => `- ${f.diplome} — ${f.etablissement} (${f.annee})`).join('\n')}

RÈGLES STRICTES :
1. profil = accroche adaptée avec mots-clés de l'offre (3 phrases max, percutantes)
2. INCLURE TOUTES les expériences fournies sans exception, dans l'ordre donné
3. 3-4 missions par expérience, commençant par un verbe d'action fort
4. Intègre 5+ mots-clés de l'offre dans le profil uniquement (pas besoin de forcer dans chaque mission)
5. NE JAMAIS inventer de chiffres absents du profil
6. titre_poste = titre exact de l'offre adapté en majuscules

JSON EXACT à retourner :
{
  "nom": "Arnaud Chédeville",
  "titre_poste": "TITRE ADAPTÉ À L'OFFRE EN MAJUSCULES",
  "profil": "Accroche adaptée avec mots-clés de l'offre, 3 phrases max",
  "contact": {
    "adresse": "83 Av. des portes, 33450 IZON",
    "email": "Arnaudchedeville@gmail.com",
    "telephone": "06 29 62 04 02",
    "permis": "Permis B"
  },
  "formation": [
    {"annee": "2023", "diplome": "Nom diplôme", "etablissement": "Établissement"}
  ],
  "experiences": [
    {
      "date": "MMM. AAAA – MMM. AAAA",
      "entreprise": "Nom entreprise",
      "titre": "TITRE POSTE EN MAJUSCULES",
      "missions": ["Verbe d'action + résultat concret", "Verbe d'action + résultat concret", "Verbe d'action + résultat concret"]
    }
  ],
  "competences": {
    "langues": "Française (natif)",
    "logiciels": "Suite Office (Excel, Word, PowerPoint, Outlook) | Windows | Make | n8n | Outils de reporting",
    "cles": "${competences}"
  },
  "centres_interet": [
    {"titre": "CONCEPTION 3D", "detail": "Production de fichiers 3D (CAO)"},
    {"titre": "ÉCHECS", "detail": "Participation à des tournois – stratégie et anticipation"}
  ]
}`;

  const message = await client.messages.create({
    model: 'claude-opus-4-7',
    max_tokens: 4000,
    messages: [{ role: 'user', content: prompt }],
  });

  // Extraire uniquement le JSON (Claude peut ajouter du texte autour)
  const raw = message.content[0].text;
  const start = raw.indexOf('{');
  const end = raw.lastIndexOf('}');
  if (start === -1 || end === -1) return raw;
  return raw.slice(start, end + 1);
}

async function generateLM(profile, offer) {
  const casquette = offer.casquette_match || 'RSG';
  const today = new Date().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });

  // 2 expériences les plus pertinentes pour les preuves
  const expTop2 = [...(profile.experiences || [])]
    .filter(e => (e.priorite?.[casquette] || 99) <= 2)
    .sort((a, b) => (a.priorite?.[casquette] || 99) - (b.priorite?.[casquette] || 99))
    .slice(0, 2);

  const prompt = `Tu es expert en lettres de motivation percutantes pour candidatures en France.
Génère une LM directe, sans clichés, qui se lit jusqu'au bout.

OFFRE :
Poste : ${offer.titre}
Entreprise : ${offer.entreprise}
Lieu : ${offer.lieu}
Compétences requises : ${offer.skills || offer.competences || ''}
Description : ${offer.description || ''}
Casquette : ${casquette}

PROFIL ARNAUD CHÉDEVILLE :
${profile.accroches?.[casquette] || ''}

Expériences clés pour cette casquette :
${expTop2.map(e => `- ${e.poste} chez ${e.entreprise} (${e.debut}–${e.fin}) : ${e.missions.slice(0, 3).join(' | ')}`).join('\n')}

RÈGLES ABSOLUES :
INTERDIT : "Je me permets de vous adresser", "Veuillez agréer", "Suite à votre annonce", tout cliché RH
OBLIGATOIRE :
- 220-260 mots, 3 paragraphes
- Ton direct et professionnel
- 2 chiffres concrets du profil (ex: 9 personnes, 14 ans)
- 1 raison spécifique pour CETTE entreprise (à inférer de l'offre/secteur)

STRUCTURE EXACTE (retourne uniquement le texte brut de la lettre) :

Arnaud Chédeville
83 Av. des portes, 33450 IZON
06 29 62 04 02 | Arnaudchedeville@gmail.com

Izon, ${today}

À l'attention du service Recrutement
${offer.entreprise}

Objet : Candidature au poste de ${offer.titre}

Bonjour,

[§1 ACCROCHE — 3-4 lignes : accroche sur le poste + Arnaud comme la bonne réponse]

[§2 PREUVES — 5-6 lignes : 2 réalisations concrètes avec chiffres, liées aux compétences de l'offre]

[§3 MOTIVATION + CTA — 3-4 lignes : pourquoi cette entreprise, disponibilité immédiate, invitation à échanger]

Cordialement,
Arnaud Chédeville`;

  const message = await client.messages.create({
    model: 'claude-opus-4-7',
    max_tokens: 1500,
    messages: [{ role: 'user', content: prompt }],
  });

  return message.content[0].text;
}

app.listen(PORT, () => {
  console.log(`Dashboard running on http://localhost:${PORT}`);
  console.log(`Press Ctrl+C to stop`);
});
