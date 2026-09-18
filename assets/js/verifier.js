/**
 * Vérification d'un cachet d'authenticité AfricaStudy Connect.
 *
 * Le paramètre ?c= contient deux parties séparées par un point : les données du
 * document en base64url, puis leur signature Ed25519. La signature est vérifiée
 * ici, dans le navigateur, avec la clé publique du cabinet. Aucune donnée n'est
 * envoyée à un serveur.
 */
import * as ed from './ed25519.js';

const CLE_PUBLIQUE = 'cc73df968680d04bcdd5b4546a028f301cd6c40b04c3eae3ba42b8b97dfa7096';

const boite = document.getElementById('resultat');

const echapper = (s) => String(s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const hexVersOctets = (h) => {
    const a = new Uint8Array(h.length / 2);
    for (let i = 0; i < a.length; i++) a[i] = parseInt(h.substr(i * 2, 2), 16);
    return a;
};

const b64urlVersOctets = (s) => {
    s = s.replace(/-/g, '+').replace(/_/g, '/');
    while (s.length % 4) s += '=';
    const bin = atob(s);
    const a = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) a[i] = bin.charCodeAt(i);
    return a;
};

const dateFr = (d) => /^\d{4}-\d{2}-\d{2}$/.test(d) ? d.split('-').reverse().join('/') : d;

function afficher(classe, icone, etat, detail, champs) {
    const lignes = (champs || [])
        .filter(([, v]) => v)
        .map(([k, v]) => `<tr><th>${echapper(k)}</th><td>${echapper(v)}</td></tr>`)
        .join('');
    boite.className = `verif-carte ${classe}`;
    boite.innerHTML =
        `<p class="verif-etat"><i class="fas ${icone}" aria-hidden="true"></i> ${echapper(etat)}</p>` +
        `<p class="verif-detail">${detail}</p>` +
        (lignes ? `<table class="verif-champs"><tbody>${lignes}</tbody></table>` : '');
}

async function verifier() {
    const code = new URLSearchParams(location.search).get('c');

    if (!code) {
        afficher('verif-vide', 'fa-qrcode', 'Aucun cachet à vérifier',
            "Scannez le code QR figurant sur votre document avec l'appareil photo de votre téléphone. Cette page s'ouvrira alors avec le résultat de la vérification.");
        return;
    }

    const morceaux = code.split('.');
    if (morceaux.length !== 2 || !morceaux[0] || !morceaux[1]) {
        afficher('verif-ko', 'fa-triangle-exclamation', 'Cachet illisible',
            "Le lien est incomplet ou a été tronqué. Scannez de nouveau le code QR du document, ou écrivez-nous à <a href=\"mailto:contact@africastudyconnect.com\">contact@africastudyconnect.com</a>.");
        return;
    }

    let donnees;
    try {
        donnees = JSON.parse(new TextDecoder().decode(b64urlVersOctets(morceaux[0])));
    } catch (e) {
        afficher('verif-ko', 'fa-triangle-exclamation', 'Cachet illisible',
            'Le contenu du cachet est corrompu. Scannez de nouveau le code QR du document.');
        return;
    }

    let valide = false;
    try {
        valide = await ed.verifyAsync(
            b64urlVersOctets(morceaux[1]),
            new TextEncoder().encode(morceaux[0]),
            hexVersOctets(CLE_PUBLIQUE),
        );
    } catch (e) {
        valide = false;
    }

    const champs = [
        ['Type de document', donnees.t],
        ['Référence', donnees.r],
        ['Client', donnees.c],
        ['Montant', donnees.m],
        ['Date d’émission', dateFr(donnees.d)],
    ];

    if (valide) {
        afficher('verif-ok', 'fa-circle-check', 'Document authentique',
            "Ce cachet a bien été émis par AfricaStudy Connect et ses données n'ont pas été modifiées. <strong>Vérifiez que les informations ci-dessous correspondent exactement à celles du document que vous avez en main.</strong>",
            champs);
    } else {
        afficher('verif-ko', 'fa-circle-xmark', 'Cachet non valide',
            "Ce cachet n'a pas pu être authentifié. Il peut avoir été modifié, recopié ou fabriqué. Ne donnez pas suite à ce document et signalez-le à <a href=\"mailto:contact@africastudyconnect.com\">contact@africastudyconnect.com</a>.",
            champs);
    }
}

verifier();
