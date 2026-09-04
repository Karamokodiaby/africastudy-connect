#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Appose une empreinte de version sur les liens vers assets/styles.css et
assets/app.js dans toutes les pages HTML.

Pourquoi c'est nécessaire : `_headers` demande aux navigateurs de garder les
fichiers de assets/ en cache pendant une semaine. Sans empreinte, un visiteur
déjà venu sur le site continue de voir l'ancien CSS pendant sept jours après
une mise en ligne — une promotion, un changement de tarif ou une correction
d'affichage lui resteraient invisibles.

L'empreinte est calculée sur le contenu du fichier : elle ne change que si le
fichier change, ce qui préserve le bénéfice du cache.

À lancer après chaque modification de assets/styles.css ou assets/app.js,
avant de déployer :

    python3 tools/stamp-assets.py
"""

import glob
import hashlib
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSETS = ["assets/styles.css", "assets/app.js"]


def empreinte(chemin):
    contenu = open(os.path.join(RACINE, chemin), "rb").read()
    return hashlib.sha256(contenu).hexdigest()[:8]


def main():
    versions = {}
    for asset in ASSETS:
        chemin = os.path.join(RACINE, asset)
        if not os.path.exists(chemin):
            print(f"  Fichier introuvable : {asset}")
            return 1
        versions[asset] = empreinte(asset)

    fichiers = sorted(
        glob.glob(os.path.join(RACINE, "*.html"))
        + glob.glob(os.path.join(RACINE, "blog", "*.html"))
    )

    modifies = 0
    for chemin in fichiers:
        contenu = open(chemin, encoding="utf-8").read()
        origine = contenu

        for asset, version in versions.items():
            # Remplace /asset ou /asset?v=xxxx par /asset?v=<empreinte>
            motif = re.compile(r"(/" + re.escape(asset) + r")(\?v=[0-9a-f]+)?")
            contenu = motif.sub(r"\1?v=" + version, contenu)

        if contenu != origine:
            open(chemin, "w", encoding="utf-8").write(contenu)
            modifies += 1

    print()
    for asset, version in versions.items():
        print(f"  {asset:<22} v={version}")
    print(f"\n  {modifies} page(s) mise(s) à jour sur {len(fichiers)}.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
