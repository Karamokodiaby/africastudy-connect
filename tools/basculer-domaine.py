#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bascule le site de africastudy-connect.pages.dev vers le domaine définitif.

L'opération touche plus que l'adresse du site : les balises canoniques, le
sitemap, les images de partage social, les données structurées, l'adresse
e-mail affichée sur vingt-cinq pages et les variables du backend. Une bascule
partielle est pire que pas de bascule du tout, d'où ce script, qui fait tout
en une passe ou rien.

Un garde-fou vérifie que le domaine résout avant d'écrire quoi que ce soit :
pointer les balises canoniques vers un domaine inexistant empêcherait
l'indexation du site.

Usage :
    python3 tools/basculer-domaine.py africastudyconnect.com
    python3 tools/basculer-domaine.py africastudyconnect.com --simulation
    python3 tools/basculer-domaine.py africastudyconnect.com --sans-verification
"""

import glob
import os
import re
import socket
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ANCIEN_SITE = "africastudy-connect.pages.dev"
ANCIEN_MAIL_DOMAINE = "africastudy-connect.com"

EXTENSIONS = ("*.html", "*.xml", "*.txt", "*.toml", "*.md")


def fichiers():
    trouves = []
    for motif in EXTENSIONS:
        trouves += glob.glob(os.path.join(RACINE, motif))
        trouves += glob.glob(os.path.join(RACINE, "blog", motif))
        trouves += glob.glob(os.path.join(RACINE, "tools", motif))
    return sorted(set(trouves))


def resout(domaine):
    try:
        socket.getaddrinfo(domaine, None)
        return True
    except socket.gaierror:
        return False


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    options = {a for a in sys.argv[1:] if a.startswith("--")}

    if len(args) != 1:
        print(__doc__)
        return 2

    nouveau = args[0].strip().lower().removeprefix("https://").removeprefix("http://").rstrip("/")
    simulation = "--simulation" in options
    verifier = "--sans-verification" not in options

    if not re.fullmatch(r"[a-z0-9-]+(\.[a-z0-9-]+)+", nouveau):
        print(f"\n  Nom de domaine invalide : {nouveau}\n")
        return 1

    print()
    print(f"  Bascule vers : {nouveau}")
    print("  " + "─" * 62)

    if verifier:
        print("  Vérification DNS…", end=" ", flush=True)
        if resout(nouveau):
            print("le domaine résout.")
        else:
            print("ÉCHEC.")
            print()
            print(f"  {nouveau} ne résout pas encore.")
            print()
            print("  Basculer maintenant pointerait les balises canoniques, le sitemap")
            print("  et les images de partage vers une adresse injoignable : Google ne")
            print("  pourrait plus indexer le site, et les aperçus WhatsApp seraient vides.")
            print()
            print("  Enregistrez le domaine, branchez-le sur Cloudflare Pages, attendez")
            print("  que la propagation soit faite, puis relancez.")
            print("  Pour passer outre en connaissance de cause : --sans-verification")
            print()
            return 1

    remplacements = {
        # Adresse du site, dans les canoniques, le sitemap, les données structurées
        ANCIEN_SITE: nouveau,
        # Adresse e-mail affichée et configurée
        f"@{ANCIEN_MAIL_DOMAINE}": f"@{nouveau}",
        f"//{ANCIEN_MAIL_DOMAINE}": f"//{nouveau}",
    }

    total, touches = 0, []
    for chemin in fichiers():
        contenu = open(chemin, encoding="utf-8").read()
        n = sum(contenu.count(a) for a in remplacements)
        if not n:
            continue
        nouveau_contenu = contenu
        for ancien, remplacant in remplacements.items():
            nouveau_contenu = nouveau_contenu.replace(ancien, remplacant)
        if not simulation:
            open(chemin, "w", encoding="utf-8").write(nouveau_contenu)
        touches.append((os.path.relpath(chemin, RACINE), n))
        total += n

    if not total:
        print("\n  Aucune occurrence trouvée : la bascule a déjà été faite.\n")
        return 0

    for nom, n in touches:
        print(f"     {nom:<52} {n}")

    print()
    if simulation:
        print(f"  SIMULATION, {total} remplacements dans {len(touches)} fichiers.")
        print("  Relancez sans --simulation pour écrire.")
    else:
        print(f"  {total} remplacements effectués dans {len(touches)} fichiers.")
        print()
        print("  Il reste à faire, hors dépôt :")
        print("     • créer la boîte contact@" + nouveau)
        print("     • vérifier le domaine dans Brevo (sinon aucun e-mail ne partira)")
        print("     • ajouter le domaine personnalisé dans Cloudflare Pages")
        print("     • soumettre le nouveau sitemap dans Google Search Console")
        print("     • si l'ancien domaine est conservé, le rediriger en 301")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
