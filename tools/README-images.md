# Images du site

Les emplacements sont déjà en place dans les sept fiches de villes. Il ne reste qu'à déposer les fichiers : ils apparaîtront d'eux-mêmes. Tant qu'une image manque, son bloc est retiré automatiquement : aucune icône cassée n'apparaît, et la page reste propre.

## Où déposer les fichiers

```
assets/img/ville-lyon.webp
assets/img/ville-lille.webp
assets/img/ville-clermont-ferrand.webp
assets/img/ville-poitiers.webp
assets/img/ville-compiegne.webp
assets/img/ville-reims.webp
assets/img/ville-amiens.webp
```

Le nom est imposé : il est déjà écrit dans les pages. Un fichier mal nommé ne s'affichera pas.

## Le format et le poids

C'est le point le plus important de ce document. Une grande partie des visiteurs consulte le site en 3G, depuis un téléphone. Une image mal préparée coûte plus de visiteurs qu'elle n'en gagne.

| Règle | Valeur |
|---|---|
| Format | **WebP**, deux à trois fois plus léger qu'un JPEG à qualité égale |
| Largeur | **1200 px**, jamais plus |
| Proportion | **16/9** (1200 × 675) pour les illustrations de tête |
| Poids maximum | **150 Ko par image**, 100 Ko de préférence |

Pour convertir et redimensionner sans installer de logiciel, [squoosh.app](https://squoosh.app) fait le travail dans le navigateur : glissez l'image, choisissez WebP, réglez la largeur à 1200 px, et surveillez le poids affiché en bas.

Vérifiez le poids de ce qui est déposé :

```bash
ls -lhS assets/img/
```

## Où trouver les images, légalement

C'est un site commercial. Une image récupérée sur un moteur de recherche est une contrefaçon, et les ayants droit de photographies de monuments sont actifs. Trois sources sûres :

**Wikimedia Commons**, la meilleure pour les monuments et les vues de villes. Vérifiez la licence de chaque fichier et **reportez le crédit demandé** dans la légende de la page : c'est la contrepartie obligatoire de la gratuité.

**Unsplash** et **Pexels**, photographies libres d'usage commercial, sans obligation de crédit. Moins précises sur les lieux identifiables, mais sans contrainte.

**Vos propres photos**, la meilleure option quand elle est possible. Si un étudiant que vous avez accompagné vous envoie une photo de sa ville, vous obtenez une image que personne d'autre n'a. Demandez son autorisation écrite.

## Le crédit photo

Chaque légende contient aujourd'hui la mention `Crédit photo à renseigner`. Remplacez-la par le crédit réel, ou supprimez la ligne `<span class="credit">…</span>` si la source n'en exige pas.

Exemple :

```html
<span class="credit">Photo : Jean Dupont, Wikimedia Commons, CC BY-SA 4.0</span>
```

## Le texte alternatif

Il est déjà rédigé pour chaque ville et décrit ce que montre l'image. Ne le remplacez pas par « photo de Lyon » : c'est ce texte que lisent les moteurs de recherche et les lecteurs d'écran, et il fait remonter les pages dans Google Images.

Si vous changez d'image, adaptez le texte alternatif à ce que la nouvelle montre réellement.

## Les pages sans image, et pourquoi

Le comparatif des villes, l'article sur le visa, celui sur la Belgique et celui sur le Canada n'ont volontairement pas d'illustration. Leur contenu est constitué de tableaux et de raisonnements ; une photo d'illustration générique y ajouterait du poids sans rien apprendre au lecteur.

Si l'un d'eux mérite un jour un visuel, ce sera un **schéma** : une carte des distances, une frise de calendrier, et non une photographie d'ambiance.

## L'image de partage social

Chaque fiche de ville utilise désormais sa propre photo comme aperçu lors d'un partage sur WhatsApp ou Facebook. Les autres pages pointent vers `assets/og-image.png`, qui existe et porte la marque et le nom du cabinet.

## Après avoir déposé des images

Rien de particulier, les images ne sont pas concernées par le versionnage des assets. En revanche, si vous modifiez `assets/styles.css` ou `assets/app.js` :

```bash
python3 tools/stamp-assets.py
```
