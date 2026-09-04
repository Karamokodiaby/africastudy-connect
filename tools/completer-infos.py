#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remplit en une passe les informations du cabinet dans toutes les pages HTML.

Le pied de page est dupliqué dans une douzaine de fichiers : ce script évite
d'avoir à les éditer un par un et garantit que l'adresse est identique partout,
y compris dans les données structurées JSON-LD de la page d'accueil.

Usage :
    python3 tools/completer-infos.py

Le script pose les questions, affiche ce qu'il va changer, et demande
confirmation avant d'écrire. Rien n'est modifié tant que vous n'avez pas
répondu « o ».
"""

import os
import sys
import glob

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Chaque entrée : (clé, question, valeur par défaut, [gabarits à remplacer])
CHAMPS = [
    ("raison_sociale",
     "Raison sociale (nom légal de la société)",
     None,
     ["[RAISON SOCIALE À COMPLÉTER]"]),

    ("forme_juridique",
     "Forme juridique (SAS, SARL, entreprise individuelle…)",
     None,
     ["[FORME JURIDIQUE — SAS, SARL, entreprise individuelle…]"]),

    ("capital",
     "Capital social (laissez vide si sans objet)",
     "Sans objet",
     ["[MONTANT DU CAPITAL, le cas échéant]"]),

    ("rue",
     "Adresse — rue et numéro",
     None,
     ["[ADRESSE À COMPLÉTER]"]),

    ("code_postal_ville",
     "Adresse — code postal et ville (ex : 75011 Paris)",
     None,
     ["[CODE POSTAL — VILLE]"]),

    ("pays",
     "Adresse — pays",
     "France",
     ["[PAYS]"]),

    ("directeur",
     "Directeur de la publication (nom et prénom)",
     None,
     ["[NOM ET PRÉNOM DU DIRECTEUR DE LA PUBLICATION]"]),

    ("tva",
     "Numéro de TVA intracommunautaire (laissez vide si non assujetti)",
     "Non assujetti",
     ["[NUMÉRO DE TVA, si assujetti]"]),
]


def demander(question, defaut):
    suffixe = f" [{defaut}]" if defaut else ""
    while True:
        reponse = input(f"  {question}{suffixe} : ").strip()
        if reponse:
            return reponse
        if defaut:
            return defaut
        print("     Cette information est obligatoire.")


def main():
    print()
    print("  Informations légales du cabinet")
    print("  " + "─" * 60)
    print("  Ces valeurs seront écrites dans toutes les pages du site.")
    print()

    valeurs = {}
    for cle, question, defaut, _ in CHAMPS:
        valeurs[cle] = demander(question, defaut)

    adresse_complete = f"{valeurs['rue']}, {valeurs['code_postal_ville']}, {valeurs['pays']}"

    # Remplacements simples : gabarit → valeur
    remplacements = {}
    for cle, _, _, gabarits in CHAMPS:
        for g in gabarits:
            remplacements[g] = valeurs[cle]

    # Les deux adresses rédigées en une seule ligne
    remplacements["[ADRESSE COMPLÈTE — RUE, CODE POSTAL, VILLE, PAYS]"] = adresse_complete
    remplacements["[ADRESSE COMPLÈTE DU SIÈGE SOCIAL]"] = adresse_complete

    # Données structurées JSON-LD de la page d'accueil
    code_postal = valeurs["code_postal_ville"].split()[0]
    ville = " ".join(valeurs["code_postal_ville"].split()[1:]) or valeurs["code_postal_ville"]
    remplacements["ADRESSE_A_COMPLETER"] = valeurs["rue"]
    remplacements["VILLE_A_COMPLETER"] = ville
    remplacements["CODE_POSTAL_A_COMPLETER"] = code_postal

    fichiers = sorted(
        glob.glob(os.path.join(RACINE, "*.html")) +
        glob.glob(os.path.join(RACINE, "blog", "*.html"))
    )

    # Simulation
    apercu = []
    total = 0
    for chemin in fichiers:
        contenu = open(chemin, encoding="utf-8").read()
        n = sum(contenu.count(g) for g in remplacements)
        if n:
            apercu.append((os.path.relpath(chemin, RACINE), n))
            total += n

    if not total:
        print("\n  Aucun gabarit trouvé : les pages sont déjà complétées.\n")
        return 0

    print()
    print("  Récapitulatif")
    print("  " + "─" * 60)
    print(f"  Raison sociale      {valeurs['raison_sociale']} ({valeurs['forme_juridique']})")
    print(f"  Siège social        {adresse_complete}")
    print(f"  Directeur publi.    {valeurs['directeur']}")
    print(f"  Capital / TVA       {valeurs['capital']} / {valeurs['tva']}")
    print()
    print(f"  {total} remplacements dans {len(apercu)} fichiers :")
    for nom, n in apercu:
        print(f"     {nom:<34} {n}")
    print()

    if input("  Écrire ces modifications ? [o/N] ").strip().lower() not in ("o", "oui"):
        print("\n  Annulé, aucun fichier modifié.\n")
        return 1

    for chemin in fichiers:
        contenu = open(chemin, encoding="utf-8").read()
        origine = contenu
        for gabarit, valeur in remplacements.items():
            contenu = contenu.replace(gabarit, valeur)
        if contenu != origine:
            open(chemin, "w", encoding="utf-8").write(contenu)

    print()
    print(f"  {total} remplacements effectués.")
    print()
    print("  Il reste à traiter à la main, car ces textes vous engagent :")
    print("     conditions-generales.html   article 5  — échéancier de paiement")
    print("     conditions-generales.html   article 8  — remboursement si refus de visa")
    print("     conditions-generales.html   article 12 — médiateur de la consommation")
    print("     politique-confidentialite.html          — durées de conservation réelles")
    print("     index.html  section FAQ                 — mêmes réponses que les CGV")
    print()
    print("  Pour les retrouver :")
    print("     grep -rn 'todo-flag' --include='*.html' .")
    print()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n  Interrompu, aucun fichier modifié.\n")
        sys.exit(1)
