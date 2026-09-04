# Encarts publicitaires

Créations destinées à promouvoir AfricaStudy Connect sur un site tiers, Daloa360 en premier lieu.

## Ce qu'il y a dans ce dossier

| Fichier | Format | Poids | Usage |
|---|---|---|---|
| `bloc-daloa360.html` | responsive | 2 Ko | **Option recommandée.** À coller dans une page ou un article. |
| `pub-728x90.png` | bannière large | 12 Ko | Haut ou bas de page, écran d'ordinateur. |
| `pub-300x250.png` | rectangle moyen | 15 Ko | Colonne latérale. Le format le plus universel. |
| `pub-320x100.png` | bannière mobile | 8 Ko | Entre deux articles sur téléphone. |

## Pourquoi préférer le bloc HTML

Une grande partie des lecteurs de Daloa360 consulte le site en 3G, depuis un téléphone. Le bloc HTML pèse **2 Ko contre 15 Ko** pour l'image équivalente, reste net sur tous les écrans, y compris les écrans à haute densité où un PNG paraît flou, et s'adapte seul à la largeur disponible : disposition horizontale au-delà de 520 px, empilée en dessous.

Il est également accessible : le texte est du vrai texte, lisible par un lecteur d'écran et sélectionnable.

N'utilisez les images que si l'emplacement publicitaire n'accepte que des images.

## Intégration dans Daloa360

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
