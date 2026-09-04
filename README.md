# AfricaStudy Connect

Site du cabinet AfricaStudy Connect, accompagnement des étudiants d'Afrique de l'Ouest vers les universités européennes, canadiennes et américaines.

Hébergé sur **Cloudflare Pages**, avec un backend serverless **Pages Functions + D1 + R2**. Aucun serveur à maintenir.

---

## À faire avant la mise en ligne

Ces points bloquent une mise en production propre. Ils sont signalés dans les pages par un encadré orange `À compléter`.

| # | Élément | Où | Pourquoi c'est bloquant |
|---|---|---|---|
| 1 | Raison sociale, forme juridique, adresse du siège, directeur de la publication | `mentions-legales.html` | Mentions légales incomplètes = sans valeur juridique |
| 2 | Identité du responsable de traitement, durées de conservation réelles | `politique-confidentialite.html` | Obligation RGPD |
| 3 | Politique de remboursement en cas de refus de visa, échéancier de paiement, médiateur | `conditions-generales.html` | Engage votre responsabilité contractuelle |
| 4 | Adresse physique | `index.html` + toutes les pages (bloc `footer-address`) | Élément de confiance pour les familles qui paient jusqu'à 3 500 € |
| 5 | Faire relire les trois documents légaux par un juriste | — | Ce sont des trames, pas des contrats prêts à l'emploi |

Les emplacements à remplir se repèrent d'un coup :

```bash
grep -rn "À COMPLÉTER\|A_COMPLETER\|todo-flag" --include="*.html" .
```

Deux autres réglages, non bloquants mais à faire rapidement :

- **Image de partage** — créer `assets/og-image.png` en 1200 × 630 px. Sans elle, les partages WhatsApp et Facebook affichent un aperçu vide.
- **Nom de domaine** — le site pointe partout vers `africastudy-connect.pages.dev`. Si vous branchez `africastudy-connect.com`, remplacez l'URL d'un coup :
  ```bash
  grep -rl "africastudy-connect.pages.dev" --include="*.html" --include="*.xml" --include="*.txt" --include="*.toml" . | xargs sed -i '' 's|africastudy-connect\.pages\.dev|africastudy-connect.com|g'
  ```

---

## Structure

```
.
├── index.html                      Page d'accueil
├── etudes-en-*.html                Pages destinations (SEO long-tail)
├── mentions-legales.html
├── politique-confidentialite.html
├── conditions-generales.html
├── 404.html / 500.html             Pages d'erreur
├── blog/
│   ├── index.html                  Hub éditorial
│   └── modele-article.html         Gabarit à dupliquer pour publier
├── assets/
│   ├── styles.css                  Feuille de style unique, partagée
│   └── app.js                      Menu, compteurs, formulaire, upload
├── functions/api/                  Backend serverless (Pages Functions)
│   ├── _shared.js                  Réponses JSON, validation, envoi d'e-mail
│   ├── submit.js                   POST — enregistre une demande
│   ├── upload.js                   POST — dépôt de document dans R2
│   └── leads.js                    GET/PATCH — consultation (protégé)
├── migrations/                     Schéma D1
├── _headers                        En-têtes de sécurité
├── robots.txt / sitemap.xml
└── wrangler.toml
```

Le CSS et le JS sont partagés par toutes les pages : une modification de `assets/styles.css` s'applique partout. En revanche l'en-tête et le pied de page sont dupliqués dans chaque fichier HTML — c'est le prix d'un site statique sans build. Si vous modifiez le menu, répercutez-le sur toutes les pages.

---

## Mise en place du backend

Sans ces étapes, le formulaire renvoie une erreur : il ne peut pas écrire en base.

### 1. Installer les dépendances

```bash
npm install
```

### 2. Créer la base de données D1

```bash
npx wrangler d1 create africastudy-leads
```

La commande affiche un `database_id`. Recopiez-le dans `wrangler.toml`, à la place de `REMPLACER_PAR_VOTRE_DATABASE_ID`.

### 3. Appliquer le schéma

```bash
npx wrangler d1 migrations apply africastudy-leads --remote
```

### 4. Créer le bucket de documents

```bash
npx wrangler r2 bucket create africastudy-documents
```

### 5. Configurer l'envoi d'e-mails

Créez un compte sur [resend.com](https://resend.com), vérifiez votre domaine d'envoi, puis :

```bash
npx wrangler pages secret put RESEND_API_KEY
```

Sans cette clé, les demandes sont bien enregistrées mais aucun e-mail n'est envoyé — ni au candidat, ni au cabinet.

### 6. Protéger la consultation des demandes

```bash
npx wrangler pages secret put ADMIN_TOKEN
```

Utilisez un jeton long et aléatoire, par exemple `openssl rand -hex 32`. Tant qu'il n'est pas défini, `/api/leads` refuse tout accès — c'est volontaire : cet endpoint expose des données personnelles.

### 7. Lier les ressources dans le tableau de bord

Dans **Cloudflare Pages → votre projet → Settings → Functions**, ajoutez les bindings :

| Type | Nom de la variable | Ressource |
|---|---|---|
| D1 database | `DB` | `africastudy-leads` |
| R2 bucket | `R2` | `africastudy-documents` |

C'est l'étape la plus souvent oubliée. `wrangler.toml` suffit en local, mais Pages exige que les bindings soient déclarés dans l'interface pour les déploiements.

---

## Développement local

```bash
npm run dev
```

Le site est servi sur `http://localhost:8788`, avec une base D1 et un bucket R2 locaux. Pour les secrets en local, copiez `.dev.vars.example` en `.dev.vars` et renseignez vos valeurs — ce fichier est ignoré par git.

Première utilisation, créez le schéma local :

```bash
npm run db:migrate:local
```

---

## Consulter les demandes reçues

En ligne de commande :

```bash
npm run db:leads
```

Ou via l'API, avec le jeton d'administration :

```bash
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
     "https://africastudy-connect.pages.dev/api/leads?limit=50"
```

Changer le statut d'une demande (`new`, `contacted`, `qualified`, `converted`, `lost`) :

```bash
curl -X PATCH -H "Authorization: Bearer $ADMIN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"id": 1, "status": "contacted"}' \
     "https://africastudy-connect.pages.dev/api/leads"
```

---

## Mesure d'audience

Le site est prêt pour [Plausible](https://plausible.io) — sans cookie, sans données personnelles, donc **sans bandeau de consentement à afficher**. Créez le site sur Plausible, puis décommentez la ligne `<script defer data-domain=…>` présente dans le `<head>` de chaque page.

Le formulaire déclenche déjà un événement `Lead` en cas de succès : il suffit de créer l'objectif correspondant dans Plausible pour suivre le taux de conversion.

Si vous ajoutez un jour Google Analytics ou tout autre outil déposant des cookies non essentiels, un bandeau de consentement devient obligatoire. C'est la seule raison pour laquelle il n'y en a pas aujourd'hui.

---

## Sécurité

Les en-têtes sont définis dans `_headers` : `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, HSTS et une Content-Security-Policy.

La CSP autorise explicitement Google Fonts, Font Awesome (cdnjs) et Plausible. **Si vous ajoutez un script ou une police venant d'un autre domaine, ajoutez-le à la CSP**, sinon le navigateur le bloquera silencieusement.

Côté API : validation systématique des entrées, requêtes SQL préparées, limite d'une demande par e-mail et par heure, types et taille de fichiers contrôlés à l'upload, et clés R2 construites à partir de valeurs assainies.

---

## Publier un article de blog

1. Dupliquez `blog/modele-article.html` sous `blog/mon-sujet.html`.
2. Mettez à jour le `<title>`, la `<meta name="description">` et le `<link rel="canonical">`.
3. Rédigez le contenu, puis supprimez l'encadré orange du modèle.
4. Ajoutez l'URL dans `sitemap.xml`.
5. Remplacez la mention « article en préparation » par un lien dans `blog/index.html`.

Une règle de fond : n'écrivez que ce que vous pouvez sourcer. Les règles de visa et les frais de scolarité changent chaque année, et un article inexact coûte plus cher en crédibilité qu'une page vide.

---

## Déploiement

Cloudflare Pages déploie automatiquement à chaque push sur la branche de production. Manuellement :

```bash
npm run deploy
```
