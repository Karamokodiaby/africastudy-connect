/**
 * GET /api/leads
 * Consultation des demandes reçues. Réservé au cabinet.
 *
 * Authentification : en-tête `Authorization: Bearer <ADMIN_TOKEN>`.
 * Le secret se définit avec :  npx wrangler pages secret put ADMIN_TOKEN
 *
 * Sans ADMIN_TOKEN configuré, l'endpoint refuse tout accès : il ne doit
 * jamais exposer de données personnelles par défaut.
 *
 * Exemple :
 *   curl -H "Authorization: Bearer $ADMIN_TOKEN" \
 *        "https://africastudy-connect.pages.dev/api/leads?status=new&limit=50"
 */
import { json, fail } from './_shared.js';

const VALID_STATUS = ['new', 'contacted', 'qualified', 'converted', 'lost'];

/** Comparaison à durée constante, pour ne pas fuiter le secret octet par octet. */
function safeEqual(a, b) {
    if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
    let diff = 0;
    for (let i = 0; i < a.length; i++) {
        diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
    }
    return diff === 0;
}

function authorize(request, env) {
    if (!env.ADMIN_TOKEN) {
        console.error('ADMIN_TOKEN non configuré, accès aux leads refusé.');
        return false;
    }
    const header = request.headers.get('Authorization') || '';
    const match = header.match(/^Bearer\s+(.+)$/i);
    return !!match && safeEqual(match[1], env.ADMIN_TOKEN);
}

export async function onRequestGet(context) {
    const { request, env } = context;

    if (!authorize(request, env)) {
        return fail('Accès refusé.', 401, 'unauthorized');
    }
    if (!env.DB) {
        return fail('Service indisponible.', 503, 'db_unavailable');
    }

    const url = new URL(request.url);
    const status = url.searchParams.get('status');
    const limit = Math.min(parseInt(url.searchParams.get('limit') || '100', 10) || 100, 500);
    const offset = Math.max(parseInt(url.searchParams.get('offset') || '0', 10) || 0, 0);

    if (status && !VALID_STATUS.includes(status)) {
        return fail(`Statut inconnu. Valeurs acceptées : ${VALID_STATUS.join(', ')}.`, 400, 'invalid_status');
    }

    try {
        const query = status
            ? env.DB.prepare(
                `SELECT * FROM leads WHERE status = ?
                 ORDER BY created_at DESC LIMIT ? OFFSET ?`
              ).bind(status, limit, offset)
            : env.DB.prepare(
                `SELECT * FROM leads
                 ORDER BY created_at DESC LIMIT ? OFFSET ?`
              ).bind(limit, offset);

        const { results } = await query.all();
        const total = await env.DB.prepare('SELECT COUNT(*) AS count FROM leads').first();

        return json({
            leads: results,
            count: results.length,
            total: total ? total.count : results.length,
            limit,
            offset,
        });
    } catch (err) {
        console.error('Lecture des leads impossible :', err);
        return fail('Lecture impossible.', 500, 'db_error');
    }
}

/**
 * PATCH /api/leads
 * Met à jour le statut d'une demande.  Corps : { id, status }
 */
export async function onRequestPatch(context) {
    const { request, env } = context;

    if (!authorize(request, env)) {
        return fail('Accès refusé.', 401, 'unauthorized');
    }
    if (!env.DB) {
        return fail('Service indisponible.', 503, 'db_unavailable');
    }

    let data;
    try {
        data = await request.json();
    } catch {
        return fail('Requête illisible.', 400, 'invalid_json');
    }

    const id = parseInt(data.id, 10);
    if (!id) return fail('Identifiant manquant.', 400, 'missing_id');
    if (!VALID_STATUS.includes(data.status)) {
        return fail(`Statut inconnu. Valeurs acceptées : ${VALID_STATUS.join(', ')}.`, 400, 'invalid_status');
    }

    try {
        const result = await env.DB.prepare('UPDATE leads SET status = ? WHERE id = ?')
            .bind(data.status, id).run();
        const changed = result.meta ? result.meta.changes : 0;
        if (!changed) return fail('Demande introuvable.', 404, 'not_found');
        return json({ success: true, id, status: data.status });
    } catch (err) {
        console.error('Mise à jour du lead impossible :', err);
        return fail('Mise à jour impossible.', 500, 'db_error');
    }
}
