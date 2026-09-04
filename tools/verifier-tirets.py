#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vérifie qu'aucun tiret cadratin (—) ne s'est glissé dans le dépôt.

Le cabinet n'en emploie pas. Le caractère revient pourtant facilement :
copier-coller depuis un document, correction automatique d'un traitement
de texte, ou génération de contenu. Ce contrôle se lance avant toute
mise en ligne.

    python3 tools/verifier-tirets.py

Sortie 0 si le dépôt est propre, 1 sinon.

Selon le rôle du tiret, le remplacement n'est pas le même :
  • étiquette suivie de sa définition      → deux-points
  • incise encadrée par deux tirets        → parenthèses, ou virgules
  • rupture explicative en fin de phrase   → deux-points, ou point
  • tiret précédant « et », « mais »       → virgule
  • séparateur dans un titre de page       → barre verticale
"""

import glob
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTENSIONS = ("*.html", "*.md", "*.js", "*.css", "*.txt", "*.xml", "*.toml", "*.py", "*.svg")


def fichiers():
    trouves = []
    for dossier in ("", "blog", "tools", "assets", "functions/api", "migrations"):
        for motif in EXTENSIONS:
            trouves += glob.glob(os.path.join(RACINE, dossier, motif))
    return sorted(set(trouves))


MOI = os.path.abspath(__file__)


def main():
    trouvailles = []
    for chemin in fichiers():
        # Ce fichier contient nécessairement le caractère qu'il recherche.
        if os.path.abspath(chemin) == MOI:
            continue
        try:
            lignes = open(chemin, encoding="utf-8").read().splitlines()
        except UnicodeDecodeError:
            continue
        for i, ligne in enumerate(lignes, 1):
            if "—" in ligne:
                extrait = re.sub(r"\s+", " ", ligne).strip()
                trouvailles.append((os.path.relpath(chemin, RACINE), i, extrait[:120]))

    if not trouvailles:
        print("\n  Aucun tiret cadratin. Le dépôt est propre.\n")
        return 0

    print(f"\n  {len(trouvailles)} tiret(s) cadratin(s) à remplacer :\n")
    for nom, ligne, extrait in trouvailles:
        print(f"  {nom}:{ligne}")
        print(f"     {extrait}")
    print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
