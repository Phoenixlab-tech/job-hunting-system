const Anthropic = require("@anthropic-ai/sdk");

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method not allowed" };
  }

  try {
    const { offerId, profile, offer, docType } = JSON.parse(event.body);

    if (!docType || !["cv", "lm"].includes(docType)) {
      return { statusCode: 400, body: "Invalid docType (cv or lm)" };
    }

    let content;

    if (docType === "cv") {
      content = await generateCV(profile, offer);
    } else {
      content = await generateLM(profile, offer);
    }

    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        content: content,
        docType: docType,
        offerId: offerId,
      }),
    };
  } catch (error) {
    console.error("Generation error:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: error.message,
      }),
    };
  }
};

async function generateCV(profile, offer) {
  const prompt = `Tu es un expert en rédaction de CV ATS (optimisé pour les systèmes de scanning).

PROFIL CANDIDAT:
${JSON.stringify(profile, null, 2)}

OFFRE D'EMPLOI:
Titre: ${offer.titre}
Entreprise: ${offer.entreprise}
Description: ${offer.description || ""}
Lieu: ${offer.lieu}
Casquette cible: ${offer.casquette_match}

Génère un CV ATS-friendly en Markdown pour cette offre:
1. Adapte l'accroche aux besoins de l'offre
2. Réordonne les expériences par pertinence (la plus récente/pertinente d'abord)
3. Mets en avant les compétences qui matchent l'offre
4. Garde un format strictement lisible (pas de graphiques, pas de couleurs)
5. Inclus les habilitations électriques si pertinent pour le poste
6. Format: PRENOM NOM, email, téléphone, adresse en en-tête

CV résultat:`;

  const message = await client.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 2000,
    messages: [{ role: "user", content: prompt }],
  });

  return message.content[0].text;
}

async function generateLM(profile, offer) {
  const prompt = `Tu es un expert en lettres de motivation pour candidatures en France.

PROFIL CANDIDAT:
Nom: ${profile.nom || ""}
Adresse: ${profile.adresse || ""}
Téléphone: ${profile.telephone || ""}
Email: ${profile.email || ""}
Années d'expérience: ${profile.annees_experience || ""}
Compétences clés: ${profile.competences_cles?.join(", ") || ""}
Expériences: ${JSON.stringify(profile.experiences || [], null, 2)}

OFFRE D'EMPLOI:
Titre: ${offer.titre}
Entreprise: ${offer.entreprise}
Description: ${offer.description || ""}
Lieu: ${offer.lieu}
Casquette cible: ${offer.casquette_match}

Génère une lettre de motivation personnalisée:
1. Début avec adresse + date (format français)
2. Accroche percutante: montre que tu connais l'offre
3. 2-3 paragraphes: expériences pertinentes + résultats quantifiés
4. Paragraphe de conclusion: dispo + demande d'entretien
5. Signature: Cordialement, Nom Prénom
6. Longueur: ~250 mots, professionnel et chaleureux

Lettre résultat:`;

  const message = await client.messages.create({
    model: "claude-opus-4-7",
    max_tokens: 1500,
    messages: [{ role: "user", content: prompt }],
  });

  return message.content[0].text;
}
