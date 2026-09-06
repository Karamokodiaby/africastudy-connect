# Encarts publicitaires

Créations destinées à promouvoir AfricaStudy Connect sur un site tiers, Daloa360 en premier lieu.

## Ce qu'il y a dans ce dossier

| Fichier | Format | Poids | Usage |
|---|---|---|---|
| `etudier-en-france-depuis-la-cote-divoire-africastudy-connect.png` | 1080 × 1080 | 82 Ko | **Facebook.** Publication carrée pour le fil. |
| `pub-daloa360-800x270.png` | 800 × 270 | 24 Ko | **Pour Daloa360.** Dessinée pour l'emplacement article, voir ci-dessous. |
| `bloc-daloa360.html` | responsive | 2 Ko | Pour un site acceptant du HTML. Daloa360 n'accepte que des images. |
| `pub-728x90.png` | bannière large | 12 Ko | Haut ou bas de page, écran d'ordinateur. |
| `pub-300x250.png` | rectangle moyen | 15 Ko | Colonne latérale. Le format le plus universel. |
| `pub-320x100.png` | bannière mobile | 8 Ko | Entre deux articles sur téléphone. |

## Campagne Facebook

### Le fichier

`etudier-en-france-depuis-la-cote-divoire-africastudy-connect.png`, 1080 × 1080 px.

Le format carré est celui qui occupe le plus de hauteur dans le fil sur mobile, donc le plus visible. C'est aussi celui que Facebook recadre le moins.

### Le nom de fichier

Il n'est pas décoratif. Facebook ne l'exploite pas, mais l'image est hébergée sur le site et se retrouve dans Google Images, où le nom de fichier compte parmi les signaux de pertinence.

Il reprend donc **la phrase que les gens tapent réellement** : « étudier en France depuis la Côte d'Ivoire ». Tout en minuscules, sans accent ni apostrophe, mots séparés par des traits d'union, marque à la fin. Un fichier nommé `affiche1.png` ou `IMG_2043.png` ne dit rien à personne.

Gardez cette règle pour les visuels suivants : la requête d'abord, la marque ensuite.

### Le texte de publication

L'image seule ne suffit pas : sur Facebook, c'est le texte qui déclenche le commentaire et le partage. Une proposition à adapter :

> Vous voulez étudier en France, au Canada ou en Europe, et vous ne savez pas par où commencer ?
>
> Nous étudions votre dossier gratuitement et nous vous disons franchement si votre projet est réaliste : les formations accessibles avec votre niveau, le budget complet à prévoir, et le calendrier à respecter.
>
> Plus de 10 ans d'accompagnement d'étudiants ivoiriens, maliens, burkinabè, guinéens, béninois et togolais.
>
> Accompagnement dès 400 000 FCFA au lieu de 492 000, jusqu'au 31 octobre.
>
> Étude de profil gratuite : africastudyconnect.com
> Ou écrivez-nous sur WhatsApp au +33 6 16 48 35 58

Trois choses à ne pas retirer de ce texte : la **question d'ouverture**, qui fait s'arrêter le lecteur ; le mot **gratuite**, qui lève l'objection immédiate ; et l'**échéance**, qui donne une raison d'agir aujourd'hui plutôt que d'y repenser.

### Densité de texte

L'affiche comporte six blocs de texte. Pour une **publication ordinaire**, aucune limite ne s'applique.

Si vous **sponsorisez** la publication, sachez que Meta réduit la diffusion des visuels chargés en texte. Dans ce cas, demandez une variante allégée : accroche, prix, appel à l'action, rien d'autre.

### À la fin de la promotion

L'affiche annonce « dès 400 000 FCFA » et « jusqu'au 31 octobre ». **Retirez la publication au 31 octobre**, ou faites régénérer l'image avec les tarifs en vigueur :

```bash
python3 tools/generer-affiche-facebook.py
```

Une promotion affichée après son terme est une pratique commerciale trompeuse, au même titre que les prix barrés du site.

## Pourquoi préférer le bloc HTML

Une grande partie des lecteurs de Daloa360 consulte le site en 3G, depuis un téléphone. Le bloc HTML pèse **2 Ko contre 15 Ko** pour l'image équivalente, reste net sur tous les écrans, y compris les écrans à haute densité où un PNG paraît flou, et s'adapte seul à la largeur disponible : disposition horizontale au-delà de 520 px, empilée en dessous.

Il est également accessible : le texte est du vrai texte, lisible par un lecteur d'écran et sélectionnable.

N'utilisez les images que si l'emplacement publicitaire n'accepte que des images.

## Intégration dans Daloa360

Daloa360 gère ses publicités dans Strapi, avec un content-type « Publicité » dont le champ image est obligatoire. **Le bloc HTML n'y est donc pas utilisable** : il faut passer par l'image.

Dans Strapi, créer une entrée avec :

| Champ | Valeur |
|---|---|
| Nom | AfricaStudy Connect, rentrée 2027 |
| Annonceur | AfricaStudy Connect |
| Emplacement | `article-top` ou `article-bottom` |
| Catégories ciblées | `education,economie` |
| Image | `pub-daloa360-800x270.png` |
| Lien | `https://africastudyconnect.com/?utm_source=daloa360&utm_medium=display&utm_campaign=rentree-2027` |
| Texte alternatif | AfricaStudy Connect, étude de profil gratuite pour étudier à l'étranger |
| Fin de campagne | 31 octobre 2026 |

Renseigner la date de fin est important : elle arrête la diffusion toute seule, sans intervention, le jour où la promotion annoncée sur la création expire.

Le format 800 × 270 n'est pas arbitraire. L'emplacement article fait 728 px sur ordinateur et environ 343 px sur mobile, avec un plafond de hauteur de 320 px. Ce rapport donne 246 px sur ordinateur et 116 px sur mobile : sous le plafond dans les deux cas, donc jamais rogné, et assez grand pour rester lisible sur téléphone.

## Intégration sur un autre site

Le bloc est autonome : aucun fichier externe, aucune police à charger, aucun script. Tous les styles sont en ligne, ce qui garantit qu'aucune feuille de style de Daloa360 ne le déformera, et réciproquement.

Copiez le contenu de `bloc-daloa360.html` à partir de la balise `<a href=…>` et collez-le là où l'encart doit apparaître : dans un composant Astro, dans un gabarit d'article, ou directement dans un fichier MDX.

Pour les images, référencez-les depuis le site plutôt que d'en dupliquer une copie. Elles resteront ainsi à jour :

```html
<a href="https://africastudyconnect.com/?utm_source=daloa360&utm_medium=display&utm_campaign=rentree-2027"
   target="_blank" rel="noopener sponsored">
  <img src="https://africastudyconnect.com/assets/pub/pub-300x250.png"
       alt="AfricaStudy Connect, étude de profil gratuite pour étudier à l'étranger"
       width="300" height="250" loading="lazy">
</a>
```

## Deux points à ne pas négliger

**`rel="sponsored"` est obligatoire.** C'est une publicité, et Google demande que les liens publicitaires soient déclarés comme tels. Un lien commercial non déclaré entre deux sites appartenant à la même personne est considéré comme une tentative de manipulation du classement, et expose les deux sites.

**Les paramètres `utm_` servent à mesurer.** Ils permettent de savoir combien de visiteurs viennent réellement de Daloa360. Une fois Plausible activé, la source apparaîtra dans les statistiques d'AfricaStudy Connect. Sans eux, la publicité serait invisible dans les chiffres et vous ne sauriez jamais si elle fonctionne.

## Ce que la création ne dit pas, et pourquoi

Le taux de réussite visa affiché sur le site ne figure volontairement dans aucune de ces créations.

Un taux de réussite est une allégation publicitaire : on peut vous demander de la prouver, et elle contredit vos propres conditions générales, qui rappellent qu'aucun cabinet ne peut garantir l'obtention d'un visa. L'argument retenu est plus solide et n'engage rien : **l'étude de profil est gratuite et sans engagement**, avec l'échéance de la promotion comme motif d'agir maintenant.

## À la fin de la promotion

Les créations mentionnent « dès 400 000 FCFA » et « jusqu'au 31 octobre ». **Au 31 octobre 2026, retirez-les ou faites-les régénérer.** Une promotion affichée après son terme est une pratique commerciale trompeuse, et le prix barré n'a plus de justification.

Le script qui les produit se trouve dans l'historique du projet ; demandez une régénération avec les tarifs en vigueur plutôt que de retoucher les images.
