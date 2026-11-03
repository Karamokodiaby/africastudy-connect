/**
 * Barricade du site pendant les travaux.
 *
 * La vitrine commerciale répond 503 et affiche /travaux.html. Un 503 assorti
 * d'un Retry-After dit à Google « revenez plus tard » : il met les pages de
 * côté sans les déréférencer. Un 200 sur une page de travaux lui ferait croire
 * que le contenu a été remplacé, et le référencement serait perdu.
 *
 * Restent ouverts : le blog, la page de vérification des cachets, les pages
 * légales et les fichiers techniques. Les cachets déjà imprimés sur les
 * factures des clients pointent vers /verifier : la barricade ne doit pas les
 * casser. Les pages légales restent accessibles parce que le blog, lui, est
 * toujours en ligne et doit pouvoir y renvoyer.
 *
 * Pour rouvrir le site : supprimer ce fichier, ou passer BARRICADE à false.
 */

const BARRICADE = true;

const OUVERT = [
  /^\/blog(\/|$)/,                 // les articles restent en ligne
  /^\/verifier(\/|$)/,             // les QR des documents déjà émis
  /^\/assets\//,                   // styles, scripts, images
  /^\/api\//,                      // points d'entrée techniques
  /^\/mentions-legales(\/|$)/,
  /^\/politique-confidentialite(\/|$)/,
  /^\/conditions-generales(\/|$)/,
  /^\/(robots\.txt|sitemap\.xml|favicon\.ico|travaux\.html)$/,
  /^\/apple-touch-icon.*\.png$/,
];

const estOuvert = (chemin) => OUVERT.some((r) => r.test(chemin));

export async function onRequest(context) {
  if (!BARRICADE) return context.next();

  const chemin = new URL(context.request.url).pathname;
  if (estOuvert(chemin)) return context.next();

  let corps;
  try {
    const page = await context.env.ASSETS.fetch(
      new URL("/travaux.html", context.request.url),
    );
    corps = await page.text();
  } catch (e) {
    corps = "<!doctype html><meta charset=utf-8>"
      + "<title>Site en travaux</title>"
      + "<h1>Nous faisons peau neuve</h1>"
      + "<p>Notre site est en travaux. Les dossiers en cours sont suivis normalement.</p>"
      + "<p>Écrivez-nous sur WhatsApp : "
      + "<a href=\"https://wa.me/2250172273220\">+225 01 72 27 32 20</a></p>";
  }

  return new Response(corps, {
    status: 503,
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Retry-After": "604800",          // une semaine, réévalué à chaque passage
      "Cache-Control": "no-store",
    },
  });
}
