#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Carte de France en SVG, avec un point par ville d'implantation.

Règle éditoriale : les articles de filière montrent OÙ se trouvent les
formations, jamais QUELLES universités les proposent. Le lecteur mesure ainsi
l'étendue de l'offre et le travail accompli, mais l'appariement entre son
profil et un parcours reste ce que le cabinet vend.

Le SVG est produit en ligne, sans fichier externe ni police à charger : il
s'insère directement dans une page et reste net sur tous les écrans, ce qui
compte pour des lecteurs en 3G.

    python3 tools/generer-carte-france.py contenus/cartes/NOM.json

Le fichier de configuration liste des villes (nom seulement utilisé pour le
regroupement, jamais affiché), leurs coordonnées et un poids, plus une
légende par région.
"""

import json, math, os, sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Projection équirectangulaire calée sur la latitude moyenne de la France.
# Sans la correction en cosinus, l'Hexagone paraît étiré en largeur.
LAT0 = 46.5
K = 58.0
LON_MIN, LAT_MAX = -5.4, 51.3


def proj(lon, lat):
    x = (lon - LON_MIN) * math.cos(math.radians(LAT0)) * K
    y = (LAT_MAX - lat) * K
    return round(x, 1), round(y, 1)


# Contour simplifié : littoral et frontières, d'ouest en est par le sud.
# Une trentaine de points suffit à rendre la silhouette reconnaissable, et
# c'est tout ce qu'on demande à cette carte.
CONTOUR = [
    (2.38, 51.03), (1.85, 50.95), (1.61, 50.73), (1.55, 50.22), (1.08, 49.93),
    (0.11, 49.49), (-0.25, 49.35), (-1.62, 49.68), (-1.60, 48.84), (-2.02, 48.65),
    (-3.05, 48.78), (-4.49, 48.39), (-4.74, 48.04), (-3.37, 47.75), (-2.20, 47.28),
    (-1.78, 46.50), (-1.15, 46.16), (-1.03, 45.62), (-1.17, 44.66), (-1.56, 43.48),
    (-1.77, 43.35), (-0.75, 42.80), (1.53, 42.55), (3.03, 42.43), (3.15, 43.15),
    (3.88, 43.60), (5.37, 43.30), (5.93, 43.12), (7.27, 43.70), (7.50, 43.78),
    (6.65, 44.90), (6.86, 45.83), (6.14, 46.20), (5.97, 46.28), (7.59, 47.59),
    (7.80, 48.58), (8.18, 48.97), (6.99, 49.22), (5.99, 49.46), (4.79, 50.15),
    (4.00, 50.28), (3.20, 50.70),
]

CORSE = [
    (9.45, 43.00), (9.55, 42.70), (9.53, 42.10), (9.28, 41.60), (9.16, 41.39),
    (8.80, 41.60), (8.74, 41.93), (8.62, 42.35), (8.76, 42.57), (9.35, 42.72),
]


def chemin(points):
    d = " ".join(("M" if i == 0 else "L") + "%s %s" % proj(*p) for i, p in enumerate(points))
    return d + " Z"


def carte(cfg):
    villes = cfg["villes"]
    maxi = max(v["poids"] for v in villes)

    xs, ys = zip(*[proj(*p) for p in CONTOUR + CORSE])
    marge = 26
    larg = round(max(xs) + marge, 1)
    haut = round(max(ys) + marge, 1)

    out = [
        f'<svg viewBox="0 0 {larg} {haut}" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-labelledby="titre-{cfg["id"]} desc-{cfg["id"]}" '
        'style="width:100%; max-width:440px; height:auto; display:block; margin:0 auto;">',
        f'  <title id="titre-{cfg["id"]}">{cfg["titre_accessible"]}</title>',
        f'  <desc id="desc-{cfg["id"]}">{cfg["description_accessible"]}</desc>',
        f'  <path d="{chemin(CONTOUR)}" fill="#f1f5f9" stroke="#1e293b" stroke-width="1.6" stroke-linejoin="round"/>',
        f'  <path d="{chemin(CORSE)}" fill="#f1f5f9" stroke="#1e293b" stroke-width="1.6" stroke-linejoin="round"/>',
    ]

    # Le rayon suit la racine du poids : c'est la surface du disque, et non son
    # diamètre, que l'oeil compare. Un rayon proportionnel au poids exagérerait
    # les concentrations d'un facteur deux.
    for v in villes:
        x, y = proj(v["lon"], v["lat"])
        r = round(5.5 + 9.5 * math.sqrt(v["poids"] / maxi), 1)
        couleur = "#f59e0b" if v.get("cle") else "#2563eb"
        out.append(f'  <circle cx="{x}" cy="{y}" r="{r}" fill="{couleur}" fill-opacity="0.82" '
                   f'stroke="#ffffff" stroke-width="1.8"/>')

    out.append('</svg>')
    return "\n".join(out)


def legende(cfg):
    lignes = ['<div class="carte-legende">']
    for r in cfg["regions"]:
        lignes.append(
            f'  <div class="carte-legende-item"><span class="carte-legende-nb">{r["nb"]}</span>'
            f'<span class="carte-legende-nom">{r["nom"]}</span></div>')
    lignes.append('</div>')
    if cfg.get("hors_metropole"):
        lignes.append(f'<p class="carte-note">{cfg["note_hors_metropole"]}</p>')
    return "\n".join(lignes)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))

    # Garde-fou : la somme des régions doit retomber sur le total annoncé dans
    # l'article, et sur celle des points. Une agrégation fausse passerait
    # autrement inaperçue, et le chiffre publié serait faux.
    total_regions = sum(r["nb"] for r in cfg["regions"])
    total_villes = sum(v["poids"] for v in cfg["villes"]) + cfg.get("hors_metropole", 0)
    attendu = cfg.get("total_attendu")
    if total_regions != total_villes:
        print(f"\n  ERREUR : régions = {total_regions}, points = {total_villes}.\n")
        return 1
    if attendu is not None and total_regions != attendu:
        print(f"\n  ERREUR : total annoncé = {attendu}, relevé = {total_regions}.\n")
        return 1

    sortie = os.path.join(RACINE, "contenus", "cartes", cfg["id"] + ".svg.html")
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    bloc = carte(cfg) + "\n" + legende(cfg) + "\n"
    open(sortie, "w", encoding="utf-8").write(bloc)
    print(f"\n  {cfg['id']} : {len(cfg['villes'])} points, "
          f"{total_regions} {cfg.get('unite', 'parcours')}")
    print(f"  {os.path.relpath(sortie, RACINE)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
