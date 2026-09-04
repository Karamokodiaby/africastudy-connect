# AfricaStudy Connect

Site du cabinet AfricaStudy Connect, accompagnement des étudiants d'Afrique de l'Ouest vers les universités européennes, canadiennes et américaines.

Hébergé sur **Cloudflare Pages**, avec un backend serverless **Pages Functions + D1 + R2**. Aucun serveur à maintenir.

---

## État du site

Les informations légales du cabinet sont renseignées : entrepreneur individuel Karamoko DIABY, exerçant sous le nom commercial AfricaStudy Connect, 11B avenue Auguste Rodin, 94350 Villiers-sur-Marne, non assujetti à la TVA.

Il reste deux choses avant que le site soit pleinement opérationnel.

### 1. Provisionner le backend

Sans cela, **le formulaire n'enregistre aucune demande**. Les sept étapes sont détaillées plus bas, section « Mise en place du backend ».

### 2. Faire relire les documents juridiques

Les mentions légales, la politique de confidentialité et les conditions générales de vente ont été rédigées avec soin et sont cohérentes entre elles, mais elles n'ont pas été validées par un juriste. Deux articles engagent directement la responsabilité du cabinet :

- **Article 8 des CGV** — garantie en cas de refus de visa, avec un remboursement chiffré à 30 % après deux campagnes.
- **Article 7 des CGV** — rétractation. Cet article ne produit son effet que si **le contrat signé par le client comporte la mention de demande d'exécution immédiate**. Sans elle, un client peut se rétracter avec remboursement intégral pendant quatorze jours.

### Promotion en cours

Une offre spéciale court **jusqu'au 31 octobre 2026 inclus** :

| Formule | Tarif habituel | Tarif promotionnel | Remise |
|---|---|---|---|
| Essentiel | 750 € / 492 000 FCFA | 610 € / 400 000 FCFA | −18,7 % |
| Confort & Visa | 1 800 € / 1 181 000 FCFA | 1 524 € / 1 000 000 FCFA | −15,3 % |
| VIP Sérénité | 3 500 € / 2 296 000 FCFA | 2 973 € / 1 950 000 FCFA | −15,1 % |

L'option Admission Post-Bac (343 € / 225 000 FCFA) n'est pas concernée.

**À la fin de la promotion**, il faut retirer le bandeau et les prix barrés — un prix affiché comme réduit en permanence n'est plus une promotion mais le prix réel, et l'annoncer comme une remise est une pratique commerciale trompeuse. Les points à modifier : les cartes tarifaires et le bandeau dans `index.html`, les options du formulaire, le bloc `hasOfferCatalog` des données structurées, et le tableau de l'article 3 des CGV.

### Améliorations facultatives

- **Images des articles** — les sept fiches de villes ont leur emplacement prêt ; il ne reste qu'à déposer les fichiers dans `assets/img/`. Format, poids maximum et sources légales : voir [tools/README-images.md](tools/README-images.md). Tant qu'une image manque, son bloc disparaît automatiquement.
- **Image de partage** — créer `assets/og-image.png` en 1200 × 630 px. Sans elle, les partages WhatsApp et Facebook des pages autres que les fiches de villes affichent un aperçu vide.
- **Section « À propos »** — ajouter les photos de l'équipe et du bureau, et l'histoire du cabinet.
- **Pages destinations** — y porter les données chiffrées vérifiées chaque année (frais de scolarité, budget de vie, ressources à justifier). C'est ce qui fait leur valeur en référencement.
- **Nom de domaine** — le site pointe partout vers `africastudy-connect.pages.dev`. La bascule vers le domaine définitif se fait en une commande :
  ```bash
  python3 tools/basculer-domaine.py africastudyconnect.com
  ```
  Le script traite les 335 occurrences réparties dans 29 fichiers — balises canoniques, sitemap, données structurées, images de partage, adresse e-mail et variables du backend. Il refuse d'écrire tant que le domaine ne résout pas, car pointer les canoniques vers une adresse injoignable empêcherait Google d'indexer le site. Ajoutez `--simulation` pour voir ce qui changerait sans rien écrire.

Les rappels restants dans les pages se retrouvent avec :

```bash
grep -rn "todo-flag" --include="*.html" .
```

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
├── tools/
│   ├── sync-faq-jsonld.py          Régénère le JSON-LD depuis la FAQ visible
│   ├── stamp-assets.py             Versionne les liens CSS/JS (cache navigateur)
│   ├── README-images.md            Format, poids, sources légales des images
│   └── basculer-domaine.py         Migration vers le domaine définitif
├── _headers                        En-têtes de sécurité
├── robots.txt / sitemap.xml
└── wrangler.toml
```

Le CSS et le JS sont partagés par toutes les pages : une modification de `assets/styles.css` s'applique partout. En revanche l'en-tête et le pied de page sont dupliqués dans chaque fichier HTML — c'est le prix d'un site statique sans build. Si vous modifiez le menu, répercutez-le sur toutes les pages.

### Après toute modification de assets/

```bash
python3 tools/stamp-assets.py
```

Les fichiers de `assets/` sont mis en cache une semaine par les navigateurs, comme le demande `_headers`. Sans cette commande, **un visiteur déjà venu sur le site continuerait de voir l'ancien CSS pendant sept jours** : une promotion, un changement de tarif ou une correction d'affichage lui resteraient invisibles.

Le script calcule une empreinte du contenu et l'ajoute aux liens (`styles.css?v=88b035ed`). L'empreinte ne change que si le fichier change, ce qui préserve le bénéfice du cache. À lancer avant chaque déploiement qui touche au CSS ou au JavaScript.

### Après toute modification de la FAQ

```bash
python3 tools/sync-faq-jsonld.py
```

Régénère les données structurées à partir de la FAQ visible. Google n'accorde le résultat enrichi que si les deux correspondent exactement.

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
