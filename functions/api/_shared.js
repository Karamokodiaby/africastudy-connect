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
 * Envoie un e-mail via l'API Resend.
 * Ne lève jamais : un échec d'envoi ne doit pas faire perdre une demande.
 */
export async function sendEmail(env, { to, subject, html, replyTo }) {
    if (!env.RESEND_API_KEY) {
        console.warn('RESEND_API_KEY absente : e-mail non envoyé.');
        return false;
    }
    try {
        const res = await fetch('https://api.resend.com/emails', {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${env.RESEND_API_KEY}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                from: env.FROM_EMAIL || 'AfricaStudy Connect <contact@africastudy-connect.com>',
                to: Array.isArray(to) ? to : [to],
                subject,
                html,
                ...(replyTo ? { reply_to: replyTo } : {}),
            }),
        });
        if (!res.ok) {
            console.error('Resend a répondu', res.status, await res.text());
            return false;
        }
        return true;
    } catch (err) {
        console.error('Envoi e-mail impossible :', err);
        return false;
    }
}
