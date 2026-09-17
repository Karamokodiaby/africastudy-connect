# Carrousels de filières

Série de visuels carrés 1080 x 1080 destinés à Facebook et Instagram, un carrousel par filière d'études. L'objectif est toujours le même : informer réellement, puis amener vers l'article correspondant sur le site.

## Produire un nouveau carrousel

```bash
python3 tools/generer-carrousel-filiere.py contenus/carrousels/NOM-DE-LA-FILIERE.json
```

Le script écrit dans `assets/pub/carrousels/<slug>/`. Le contenu vit dans le JSON, le dessin dans le script : pour une nouvelle filière, copiez un fichier de configuration existant et ne touchez pas au code.

## Les quatre types de diapositive

| Type | Usage | Champs |
|---|---|---|
| `couverture` | Première image, celle qui arrête le défilement | `titre` (liste de mots), `surligne` (index des mots en ambre), `accroche` |
| `texte` | Explication en deux ou trois paragraphes | `paragraphes` |
| `liste` | Énumération avec pastilles | `chapeau`, `items` (`icone`, `titre`, `detail`, `cle`) |
| `chiffre` | La dernière image, celle qui porte notre argument | `chiffre`, `legende`, `source`, `conclusion`, `bouton` |

Dans tous les textes, `**ceci**` met en valeur : changement de graisse et de couleur.

`"cle": true` sur un item le fait passer en ambre. Réservez-le à un seul item par diapositive, celui qui porte l'avertissement : c'est ce qui fait la différence avec une publication de brochure.

Pictogrammes disponibles : `check`, `loupe`, `temple`, `ecran`, `donnees`, `megaphone`, `toque`, `document`, `euro`, `alerte`.

## Deux règles de composition

**La mise en page s'ajuste seule.** Les corps de texte sont réduits par paliers jusqu'à ce que le contenu tienne. Un texte trop long ne débordera pas, il deviendra petit. Si une diapositive paraît tassée, ce n'est pas un défaut de rendu : c'est qu'elle dit trop de choses. Coupez.

**La dernière diapositive n'est pas décorative.** C'est celle qui justifie l'existence du carrousel. Elle porte un chiffre sourcé que la publication d'origine ne donne pas, et le bouton d'appel. Sans elle, nous republions une brochure.

## Ce qu'on ne met jamais

Ni taux de réussite visa, ni promesse d'admission, ni nom d'établissement partenaire. Une allégation publicitaire doit pouvoir être prouvée, et elle contredirait nos propres conditions générales.

**Ni la liste nominative des universités.** Ni sur les visuels, ni dans les articles. On publie une carte de France avec un point par ville, les compteurs par région, et un appel à nous contacter. La liste brute est publique et gratuite sur monmaster.gouv.fr : ce que nous vendons n'est pas la liste, c'est de savoir lequel de ces parcours correspond à un profil donné. Écrire « sept universités recrutent sans condition de contrat » vaut mieux que de les nommer.

Seule exception : une université citée comme **source d'une statistique** peut être nommée, parce qu'un chiffre sans attribution ne vaut rien.

Les cartes se produisent avec :

```bash
python3 tools/generer-carte-france.py contenus/cartes/NOM.json
```

## Carrousels produits

| Filière | Dossier | Article lié |
|---|---|---|
| Master Humanités numériques | `master-humanites-numeriques/` | `/blog/master-humanites-numeriques-etudiants-afrique-ouest` |
| Master MIAGE | `master-miage/` | `/blog/miage-etudiants-afrique-ouest` |
| Rapport du Sénat n° 943 | `rapport-senat-943/` | `/blog/rapport-senat-943-etudiants-etrangers-france` |
| Master en économie | `master-economie/` | `/blog/master-economie-etudiants-afrique-ouest` |

## Publier

Facebook et Instagram acceptent jusqu'à dix images par carrousel. Publiez-les dans l'ordre des numéros de fichier. Le lien vers l'article se place dans le texte de la publication, jamais dans l'image : un lien écrit sur une image n'est pas cliquable.
