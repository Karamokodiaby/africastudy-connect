/**
 * Utilitaires partagés par les fonctions de l'API.
 */

export const JSON_HEADERS = {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
};

export function json(body, status = 200) {
    return new Response(JSON.stringify(body), { status, headers: JSON_HEADERS });
}

export function fail(message, status = 400, code = 'bad_request') {
    return json({ error: message, code, statusCode: status }, status);
}

/** Coupe une chaîne et neutralise les caractères de contrôle. */
export function clean(value, maxLength) {
    if (typeof value !== 'string') return '';
    return value.replace(/[\x00-\x1F\x7F]/g, ' ').trim().slice(0, maxLength);
}

export const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

/** Échappe le HTML avant insertion dans un e-mail. */
export function escapeHtml(value) {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

/**
 * Découpe « Nom <adresse@domaine> » en { name, email }.
 * Brevo attend l'expéditeur en deux champs distincts, là où la
 * configuration le stocke sous sa forme lisible.
 */
function expediteur(valeur) {
    const brut = (valeur || 'AfricaStudy Connect <contact@africastudyconnect.com>').trim();
    const m = brut.match(/^\s*(.*?)\s*<([^>]+)>\s*$/);
    if (m) return { name: m[1] || 'AfricaStudy Connect', email: m[2].trim() };
    return { name: 'AfricaStudy Connect', email: brut };
}

/**
 * Envoie un e-mail via l'API transactionnelle de Brevo.
 * Ne lève jamais : un échec d'envoi ne doit pas faire perdre une demande.
 */
export async function sendEmail(env, { to, subject, html, replyTo }) {
    if (!env.BREVO_API_KEY) {
        console.warn('BREVO_API_KEY absente : e-mail non envoyé.');
        return false;
    }
    try {
        const destinataires = (Array.isArray(to) ? to : [to]).map((adresse) => ({ email: adresse }));
        const res = await fetch('https://api.brevo.com/v3/smtp/email', {
            method: 'POST',
            headers: {
                'api-key': env.BREVO_API_KEY,
                'content-type': 'application/json',
                accept: 'application/json',
            },
            body: JSON.stringify({
                sender: expediteur(env.FROM_EMAIL),
                to: destinataires,
                subject,
                htmlContent: html,
                ...(replyTo ? { replyTo: { email: replyTo } } : {}),
            }),
        });
        if (!res.ok) {
            console.error('Brevo a répondu', res.status, await res.text());
            return false;
        }
        return true;
    } catch (err) {
        console.error('Envoi e-mail impossible :', err);
        return false;
    }
}
