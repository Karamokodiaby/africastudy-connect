/**
 * POST /api/submit
 * Enregistre une demande d'étude de profil, puis envoie une confirmation
 * au candidat et une notification interne au cabinet.
 */
import { json, fail, clean, EMAIL_RE, escapeHtml, sendEmail } from './_shared.js';

const REQUIRED = ['name', 'email', 'country', 'destination', 'level'];

const LABELS = {
    name: 'nom',
    email: 'adresse e-mail',
    country: 'pays de résidence',
    destination: 'destination souhaitée',
    level: "niveau d'études",
};

export async function onRequestPost(context) {
    const { request, env } = context;

    if (!env.DB) {
        console.error('Binding D1 "DB" absent — vérifier wrangler.toml et les bindings Pages.');
        return fail('Service temporairement indisponible.', 503, 'db_unavailable');
    }

    let data;
    try {
        data = await request.json();
    } catch {
        return fail('Requête illisible.', 400, 'invalid_json');
    }

    // ── Validation ────────────────────────────────────────────────────────
    for (const field of REQUIRED) {
        if (!data[field] || !String(data[field]).trim()) {
            return fail(`Champ requis : ${LABELS[field]}.`, 400, 'missing_field');
        }
    }

    const email = clean(data.email, 180).toLowerCase();
    if (!EMAIL_RE.test(email)) {
        return fail('Adresse e-mail invalide.', 400, 'invalid_email');
    }

    if (data.consent !== true) {
        return fail('Votre accord est nécessaire pour traiter la demande.', 400, 'consent_required');
    }

    const lead = {
        name: clean(data.name, 120),
        email,
        phone: clean(data.phone, 40) || null,
        country: clean(data.country, 60),
        destination: clean(data.destination, 60),
        level: clean(data.level, 60),
        formula: clean(data.formula, 120) || 'À déterminer avec le conseiller',
        postbac: data.postbac ? 1 : 0,
        message: clean(data.message, 2000) || null,
    };

    // ── Anti-spam : une demande par e-mail et par heure ────────────────────
    try {
        const existing = await env.DB.prepare(
            `SELECT COUNT(*) AS count FROM leads
             WHERE email = ? AND created_at > datetime('now', '-1 hour')`
        ).bind(lead.email).first();

        if (existing && existing.count > 0) {
            return fail(
                'Une demande a déjà été enregistrée avec cette adresse. Patientez une heure ou écrivez-nous sur WhatsApp.',
                429,
                'rate_limited'
            );
        }
    } catch (err) {
        console.error('Contrôle anti-doublon impossible :', err);
        // On laisse passer : mieux vaut un doublon qu'un lead perdu.
    }

    // ── Enregistrement ────────────────────────────────────────────────────
    try {
        await env.DB.prepare(
            `INSERT INTO leads (name, email, phone, country, destination, level, formula, postbac, message)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`
        ).bind(
            lead.name, lead.email, lead.phone, lead.country,
            lead.destination, lead.level, lead.formula, lead.postbac, lead.message
        ).run();
    } catch (err) {
        console.error('Insertion du lead impossible :', err);
        return fail("Votre demande n'a pas pu être enregistrée. Réessayez ou écrivez-nous sur WhatsApp.", 500, 'db_error');
    }

    // ── E-mails (hors chemin critique : un échec ne casse pas la réponse) ──
    const safe = Object.fromEntries(
        Object.entries(lead).map(([k, v]) => [k, escapeHtml(v === null ? '—' : v)])
    );

    const confirmation = sendEmail(env, {
        to: lead.email,
        subject: 'Votre demande est bien enregistrée — AfricaStudy Connect',
        html: `
            <div style="font-family:Arial,Helvetica,sans-serif;color:#0f172a;line-height:1.6;">
              <h2 style="color:#1e293b;">Merci ${safe.name},</h2>
              <p>Votre demande d'étude de profil pour <strong>${safe.destination}</strong> nous est bien parvenue.</p>
              <p>Un conseiller l'examine et vous recontacte <strong>sous 24 heures</strong>, par e-mail ou sur WhatsApp.</p>
              <h3 style="color:#1e293b;margin-top:24px;">Récapitulatif</h3>
              <table cellpadding="6" style="border-collapse:collapse;font-size:14px;">
                <tr><td style="color:#64748b;">Pays de résidence</td><td><strong>${safe.country}</strong></td></tr>
                <tr><td style="color:#64748b;">Destination</td><td><strong>${safe.destination}</strong></td></tr>
                <tr><td style="color:#64748b;">Niveau d'études</td><td><strong>${safe.level}</strong></td></tr>
                <tr><td style="color:#64748b;">Formule envisagée</td><td><strong>${safe.formula}</strong></td></tr>
              </table>
              <p style="margin-top:24px;">Besoin d'échanger plus vite ?
                <a href="https://wa.me/33616483558" style="color:#2563eb;">Écrivez-nous sur WhatsApp</a>.</p>
              <hr style="border:none;border-top:1px solid #e2e8f0;margin:28px 0;">
              <p style="font-size:12px;color:#64748b;">
                AfricaStudy Connect — SIRET 8236043270010<br>
                Vos données sont traitées conformément à notre
                <a href="${env.SITE_URL || ''}/politique-confidentialite.html" style="color:#2563eb;">politique de confidentialité</a>.
              </p>
            </div>`,
    });

    const notification = sendEmail(env, {
        to: env.NOTIFY_EMAIL || 'contact@africastudy-connect.com',
        replyTo: lead.email,
        subject: `Nouvelle demande — ${lead.name} (${lead.destination})`,
        html: `
            <div style="font-family:Arial,Helvetica,sans-serif;color:#0f172a;line-height:1.6;">
              <h2>Nouvelle demande d'étude de profil</h2>
              <table cellpadding="6" style="border-collapse:collapse;font-size:14px;">
                <tr><td style="color:#64748b;">Nom</td><td><strong>${safe.name}</strong></td></tr>
                <tr><td style="color:#64748b;">E-mail</td><td>${safe.email}</td></tr>
                <tr><td style="color:#64748b;">Téléphone</td><td>${safe.phone}</td></tr>
                <tr><td style="color:#64748b;">Pays</td><td>${safe.country}</td></tr>
                <tr><td style="color:#64748b;">Destination</td><td>${safe.destination}</td></tr>
                <tr><td style="color:#64748b;">Niveau</td><td>${safe.level}</td></tr>
                <tr><td style="color:#64748b;">Formule</td><td>${safe.formula}</td></tr>
                <tr><td style="color:#64748b;">Option post-bac</td><td>${lead.postbac ? 'Oui' : 'Non'}</td></tr>
              </table>
              <h3>Message</h3>
              <p style="white-space:pre-wrap;">${safe.message}</p>
            </div>`,
    });

    context.waitUntil(Promise.allSettled([confirmation, notification]));

    return json({ success: true });
}
