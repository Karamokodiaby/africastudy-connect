#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Régénère le bloc JSON-LD « FAQPage » à partir de la FAQ visible d'index.html.

Google n'accorde le rich result FAQ que si les données structurées reprennent
exactement les questions et réponses affichées. Recopier à la main finit
toujours par diverger : ce script lit la section #faq et réécrit le bloc.

À lancer après chaque modification de la FAQ :

    python3 tools/sync-faq-jsonld.py
"""

import html
import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(RACINE, "index.html")


def texte_brut(fragment):
    """Réduit un fragment HTML au texte lisible, listes comprises."""
    # Les puces deviennent des phrases séparées par un point-virgule.
    fragment = re.sub(r"</li>", " ; ", fragment)
    fragment = re.sub(r"<br\s*/?>", " ", fragment)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    texte = html.unescape(fragment)
    texte = texte.replace(" ", " ")
    texte = re.sub(r"\s+", " ", texte).strip()
    texte = re.sub(r"\s+;", " ;", texte)
    texte = re.sub(r";\s*\.", ".", texte)
    return texte.strip(" ;")


def main():
    source = open(INDEX, encoding="utf-8").read()

    debut = source.find('<section id="faq"')
    if debut == -1:
        print("  Section #faq introuvable dans index.html.")
        return 1
    fin = source.find("</section>", debut)
    section = source[debut:fin]

    items = re.findall(
        r'<details class="faq-item">\s*<summary>(.*?)</summary>\s*'
        r'<div class="faq-answer">(.*?)</div>\s*</details>',
        section,
        re.S,
    )

    if not items:
        print("  Aucune question trouvée. La structure de la FAQ a-t-elle changé ?")
        return 1

    entrees = []
    for question, reponse in items:
        entrees.append({
            "@type": "Question",
            "name": texte_brut(question),
            "acceptedAnswer": {"@type": "Answer", "text": texte_brut(reponse)},
        })

    bloc = json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entrees},
        ensure_ascii=False,
        indent=2,
    )
    bloc = "\n".join("    " + ligne for ligne in bloc.splitlines())

    nouveau = (
        '    <!-- Données structurées : FAQ, généré par tools/sync-faq-jsonld.py,\n'
        '         ne pas éditer à la main, relancer le script après modification de la FAQ -->\n'
        '    <script type="application/ld+json">\n'
        + bloc
        + "\n    </script>\n"
    )

    motif = re.compile(
        r'[ \t]*<!-- Données structurées : FAQ.*?</script>\n',
        re.S,
    )
    if not motif.search(source):
        print("  Bloc JSON-LD FAQ introuvable dans le <head>.")
        return 1

    open(INDEX, "w", encoding="utf-8").write(motif.sub(nouveau, source, count=1))

    print(f"\n  {len(entrees)} questions synchronisées :\n")
    for e in entrees:
        print(f"     {e['name']}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
