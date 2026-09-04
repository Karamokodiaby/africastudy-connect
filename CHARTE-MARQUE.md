# Charte de marque AfricaStudy Connect

Document de référence. À transmettre tel quel à un imprimeur, un graphiste ou toute personne appelée à utiliser la marque.

---

## 1. Le raisonnement

### Ce que la marque représente

Une **trajectoire ascendante entre un point de départ et une destination**.

La signature du cabinet dit : « Votre passerelle vers les meilleures universités ». La marque ne fait que dessiner cette phrase. Elle ne montre pas des études, elle montre un **passage accompagné**, ce que le cabinet vend réellement.

### Pourquoi chaque élément

**Deux points, et non un.** Un point isole un lieu ; deux points reliés créent une relation. Le nom se termine par *Connect* : la marque montre la connexion.

**Le point de départ est petit et bleu pâle.** C'est l'étudiant aujourd'hui, réel, mais pas encore arrivé.

**La destination est plus grande et ambre.** Plus grande parce que c'est le but. Ambre parce que c'est la seule couleur chaude de la charte, celle qui signale déjà ce qui compte sur le site. L'œil y va seul : la destination est ce que la famille achète.

**La courbe monte de gauche à droite.** Dans une lecture de gauche à droite, cela se lit comme une progression. Descendante ou plate, elle dirait le déclin ou l'immobilité.

**C'est une courbe, pas une droite.** Le chemin n'est pas direct : il est accompagné, il s'infléchit. Une ligne droite dirait « c'est simple », ce qui serait faux, et contraire au discours du cabinet, qui insiste sur les délais, le garant et les ressources à justifier.

**La courbe ne s'interrompt pas.** Du premier échange jusqu'à l'arrivée.

**Le carré arrondi bleu nuit** donne une silhouette reconnaissable à toute taille, fonctionne comme icône d'application, et porte le sérieux nécessaire quand on demande plusieurs centaines de milliers de francs à une famille.

### Ce qui a été écarté, et pourquoi

| Piste | Raison du rejet |
|---|---|
| **Mortier de diplômé** | Identifie un secteur, pas une entreprise. Représente la fin du parcours alors que le cabinet vend le passage. Illisible en dessous de 24 px. |
| **Carte de l'Afrique** | Réduit le cabinet à son point de départ, quand sa valeur est le pont vers l'Europe et le Canada. Pose la question des pays représentés : six sont accompagnés, pas cinquante-quatre. Cliché de toute marque « Afrique + X ». |
| **Globe ou avion** | Évoque une agence de voyage. La confusion nuit à un cabinet de conseil. |
| **Monogramme A/C** | Sûr mais muet. Un monogramme porte un sens qu'il ne crée pas : il suppose une marque déjà connue. |

### Les limites, assumées

Une marque abstraite ne se comprend pas seule au premier regard : sans le nom à côté, elle ne dit pas « études ». C'est le prix à payer pour ne pas être générique. Elle apparaît donc toujours avec le nom, sauf dans l'onglet du navigateur, où la reconnaissance naît de la répétition.

L'arc ascendant reste par ailleurs une forme employée ailleurs, notamment dans la finance. Les deux points colorés et le carré bleu nuit la distinguent, sans en faire une forme unique au monde.

---

## 2. Les fichiers

| Fichier | Usage |
|---|---|
| `assets/logo.svg` | Verrouillage horizontal, marque et nom. Documents, signature d'e-mail, supports imprimés. |
| `assets/logo-mark.svg` | Marque seule, à partir de 24 px. |
| `assets/favicon.svg` | Onglet de navigateur. **Dessin distinct**, voir §5. |
| `assets/apple-touch-icon.png` | Icône d'écran d'accueil iOS, 180 × 180 px. |
| `assets/og-image.png` | Aperçu de partage sur les réseaux, 1200 × 630 px. |

Le SVG est un format vectoriel : il s'agrandit sans perte, d'une carte de visite à une banderole. Ne jamais repartir d'une capture d'écran.

---

## 3. Les couleurs

| Rôle | Hexadécimal | RVB |
|---|---|---|
| Fond de la marque | `#1E293B` | 30, 41, 59 |
| Tracé | `#FFFFFF` | 255, 255, 255 |
| Point de départ | `#60A5FA` | 96, 165, 250 |
| Destination | `#F59E0B` | 245, 158, 11 |
| Bleu du nom | `#2563EB` | 37, 99, 235 |
| Encre du nom | `#1E293B` | 30, 41, 59 |

**Pour l'impression**, laissez l'imprimeur convertir ces valeurs en quadrichromie selon son profil et son papier : une conversion CMJN faite à l'aveugle donne des résultats faux. Le point à surveiller est l'ambre `#F59E0B`, qui vire facilement au moutarde sur papier non couché.

---

## 4. La typographie

Le nom est composé en **Poppins Bold** (graisse 800), la police du site, disponible gratuitement sur Google Fonts.

**Point d'attention pour l'impression.** Le fichier `logo.svg` contient le nom sous forme de texte, non de tracés. Sur un poste où Poppins n'est pas installée, le nom s'affichera dans une police de remplacement. Deux solutions :

- installer Poppins sur le poste qui prépare le document ;
- ou demander au graphiste de **vectoriser le texte** une fois, et conserver ce fichier pour les usages imprimés.

---

## 5. Tailles minimales

| Élément | Écran | Impression |
|---|---|---|
| Verrouillage horizontal | 140 px de large | 35 mm de large |
| Marque seule | 24 px | 8 mm |
| Favicon | 16 px | Sans objet |

**En dessous de 24 px, utilisez `favicon.svg` et non `logo-mark.svg`.** Ce n'est pas la même image : le favicon a un trait nettement plus épais et son point de départ a été supprimé. À cette taille, le tracé fin se brouille et les deux points se confondent. Un logo qui ne fonctionne qu'en grand est un logo raté ; c'est pourquoi il existe deux dessins.

---

## 6. Espace de respiration

Réservez autour de la marque un espace vide égal à **la moitié de sa hauteur**, sur les quatre côtés. Aucun texte, aucun trait, aucun bord de page ne doit y pénétrer.

---

## 7. Ce qu'il ne faut pas faire

- **Ne pas recolorer** le carré ni les points. Les quatre couleurs portent chacune un sens.
- **Ne pas déformer.** L'agrandissement se fait toujours en conservant les proportions.
- **Ne pas ajouter d'effet** : ombre portée, contour, dégradé, biseau.
- **Ne pas faire pivoter** la marque. La courbe monte de gauche à droite ; inclinée, elle perd sa lecture.
- **Ne pas recomposer le nom** dans une autre police. Utilisez `logo.svg`.
- **Ne pas poser la marque sans son carré** sur une photographie. Le carré existe pour garantir le contraste.
- **Ne pas recréer la marque** à la main. Les fichiers sources font autorité.

---

## 8. Usage en une seule couleur

En monochrome (tampon, télécopie, gravure, broderie, impression noir et blanc), la courbe conserve son sens. Composez le carré dans la couleur unique disponible et réservez le tracé et les points en blanc, sans chercher à distinguer le point de départ de la destination.

---

## 9. La phrase à dire

Si un client, un partenaire ou un imprimeur demande ce que représente le logo :

> Le logo montre le trajet d'un étudiant : d'où il part, où il arrive, et la courbe qui relie les deux. C'est exactement ce que fait le cabinet.
