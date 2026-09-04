/**
 * POST /api/upload
 * Reçoit un document (CV, relevé de notes, diplôme) et le range dans R2,
 * sous un préfixe dérivé de l'adresse e-mail du candidat.
 */
import { json, fail, clean, EMAIL_RE } from './_shared.js';

const MAX_SIZE = 5 * 1024 * 1024; // 5 Mo
const ALLOWED = {
    'application/pdf': 'pdf',
    'image/jpeg': 'jpg',
    'image/png': 'png',
};

export async function onRequestPost(context) {
    const { request, env } = context;

    if (!env.R2) {
        console.error('Binding R2 absent, vérifier wrangler.toml et les bindings Pages.');
        return fail('Service de dépôt indisponible.', 503, 'r2_unavailable');
    }

    let formData;
    try {
        formData = await request.formData();
    } catch {
        return fail('Requête illisible.', 400, 'invalid_form');
    }

    const file = formData.get('file');
    const email = clean(formData.get('email') || '', 180).toLowerCase();

    if (!file || typeof file === 'string') {
        return fail('Aucun fichier reçu.', 400, 'missing_file');
    }
    if (!EMAIL_RE.test(email)) {
        return fail('Adresse e-mail invalide.', 400, 'invalid_email');
    }

    const extension = ALLOWED[file.type];
    if (!extension) {
        return fail('Format non accepté : PDF, JPG ou PNG uniquement.', 400, 'invalid_type');
    }
    if (file.size > MAX_SIZE) {
        return fail('Fichier trop volumineux : 5 Mo maximum.', 400, 'file_too_large');
    }
    if (file.size === 0) {
        return fail('Fichier vide.', 400, 'empty_file');
    }

    // Le nom d'origine n'est jamais utilisé tel quel dans la clé R2 :
    // on le réduit à des caractères sûrs pour éviter toute traversée de chemin.
    const safeEmail = email.replace(/[^a-z0-9]/g, '_');
    const safeName = clean(file.name || 'document', 80)
        .replace(/[^a-zA-Z0-9._-]/g, '_')
        .replace(/_{2,}/g, '_');
    const key = `uploads/${safeEmail}/${Date.now()}_${safeName}`;

    try {
        await env.R2.put(key, file.stream(), {
            httpMetadata: { contentType: file.type },
            customMetadata: { email, originalName: safeName },
        });
    } catch (err) {
        console.error('Écriture R2 impossible :', err);
        return fail("Le document n'a pas pu être enregistré.", 500, 'r2_error');
    }

    // La référence en base est utile mais non bloquante.
    if (env.DB) {
        try {
            await env.DB.prepare(
                `INSERT INTO documents (email, r2_key, filename, mime_type, size_bytes)
                 VALUES (?, ?, ?, ?, ?)`
            ).bind(email, key, safeName, file.type, file.size).run();
        } catch (err) {
            console.error('Référencement du document impossible :', err);
        }
    }

    return json({ success: true, key });
}
