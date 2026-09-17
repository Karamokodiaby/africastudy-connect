#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Carrousel Facebook carré 1080 x 1080 aux couleurs d'AfricaStudy Connect.

Pourquoi un générateur plutôt qu'un fichier par affiche : la série est
destinée à couvrir toutes les filières qui aident un étudiant à choisir.
Le dessin est ici, le contenu dans un fichier de configuration JSON, ce qui
permet de produire une nouvelle filière sans retoucher une seule ligne de
code, et garantit que toutes les séries se ressemblent.

    python3 tools/generer-carrousel-filiere.py contenus/carrousels/humanites-numeriques.json

Charte respectée : bleu nuit #1E293B, bleu #2563EB, bleu clair #60A5FA,
ambre #F59E0B. L'ambre est la seule couleur chaude : elle signale la
destination, jamais la décoration.

Nécessite Pillow et Poppins dans ~/Library/Fonts.
"""

from PIL import Image, ImageDraw, ImageFont
import json, os, sys, unicodedata

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "assets", "pub")

NUIT      = (30, 41, 59)
NUIT_BAS  = (13, 20, 38)
BLANC     = (255, 255, 255)
GRIS      = (203, 213, 225)
GRIS_FONCE= (148, 163, 184)
BLEU      = (37, 99, 235)
BLEU_CLAIR= (96, 165, 250)
AMBRE     = (245, 158, 11)

MAISON = os.path.expanduser("~/Library/Fonts/")
SYS    = "/System/Library/Fonts/Supplemental/"

S = 1080          # côté de l'affiche
M = 84            # marge
UTIL = S - 2 * M


def police(taille, poids="bold"):
    """Poppins pour les titres, Arial pour le texte courant.

    Poppins n'est installé qu'en Bold et ExtraBold sur ce poste : le corps de
    texte emprunte donc Arial, dont les proportions restent proches.
    """
    fichiers = {
        "extra":   MAISON + "Poppins-ExtraBold.ttf",
        "bold":    MAISON + "Poppins-Bold.ttf",
        "texte":   SYS + "Arial.ttf",
        "texte-g": SYS + "Arial Bold.ttf",
    }
    return ImageFont.truetype(fichiers[poids], taille)


def largeur(d, txt, f):
    return d.textlength(txt, font=f)


def ajuste(d, txt, dispo, taille, poids="extra", mini=18):
    """Réduit la taille jusqu'à ce que le texte tienne sur la largeur donnée."""
    while taille > mini:
        f = police(taille, poids)
        if largeur(d, txt, f) <= dispo:
            return f
        taille -= 2
    return police(mini, poids)


def couper(d, txt, dispo, f):
    """Découpe un texte en lignes qui tiennent dans la largeur."""
    lignes, courante = [], ""
    for mot in txt.split():
        essai = (courante + " " + mot).strip()
        if largeur(d, essai, f) <= dispo or not courante:
            courante = essai
        else:
            lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    return lignes


def jetons(txt):
    """Découpe un texte en mots, en retenant lesquels sont en gras.

    La difficulté est l'apostrophe : dans "d'**Afrique**", le mot en gras
    suit immédiatement le d', sans espace. Une découpe naïve insérerait une
    espace parasite. On mémorise donc, pour chaque mot, s'il était réellement
    précédé d'une espace dans le texte d'origine.
    """
    sortie, parts = [], txt.split("**")
    fin_espace = False
    for i, bloc in enumerate(parts):
        if bloc == "":
            continue
        gras = (i % 2 == 1)
        debut_espace = bloc[:1].isspace()
        mots = bloc.split()
        for j, mot in enumerate(mots):
            avant = (j > 0) or fin_espace or debut_espace
            sortie.append((mot, gras, avant and bool(sortie)))
        fin_espace = bloc[-1:].isspace()
    return sortie


def lignes_riches(d, txt, dispo, f, fp):
    lignes, courante, lx = [], [], 0.0
    for mot, gras, avant in jetons(txt):
        ff = fp if gras else f
        w = largeur(d, mot, ff)
        we = largeur(d, " ", ff) if avant else 0.0
        if courante and lx + we + w > dispo:
            lignes.append(courante)
            courante, lx = [(mot, ff, 0.0)], w
        else:
            courante.append((mot, ff, we))
            lx += we + w
    if courante:
        lignes.append(courante)
    return lignes


def hauteur_riche(d, txt, dispo, f, fp, interligne=1.42):
    return len(lignes_riches(d, txt, dispo, f, fp)) * int(f.size * interligne)


def riche(d, x, y, txt, f, dispo, base=BLANC, fort=BLANC, fp=None, interligne=1.42):
    """Écrit un paragraphe où **ceci** est mis en valeur.

    Le passage en gras change de police et de couleur : c'est ce qui permet à
    l'oeil d'attraper l'information utile sans lire toute la phrase.
    """
    fp = fp or f
    h = int(f.size * interligne)
    for i, ligne in enumerate(lignes_riches(d, txt, dispo, f, fp)):
        cx = x
        for mot, ff, we in ligne:
            cx += we
            d.text((cx, y + i * h), mot, font=ff, fill=fort if ff is fp else base)
            cx += largeur(d, mot, ff)
    return y + len(lignes_riches(d, txt, dispo, f, fp)) * h


def bezier(p0, p1, p2, p3, n=260):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
                    u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
    return pts


def marque(taille):
    """Le logo d'AfricaStudy Connect, redessiné à la taille demandée."""
    sur = 3
    T = taille * sur
    k = T / 40
    im = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, T - 1, T - 1], radius=int(9 * k), fill=(15, 23, 42, 255))
    d.line([(x*k, y*k) for x, y in bezier((10, 30), (10, 18.5), (17.5, 11.5), (30, 11))],
           fill=BLANC + (255,), width=int(3.4 * k), joint="curve")
    for (cx, cy), r, col in [((10, 30), 3.2, BLEU_CLAIR), ((30, 11), 4.2, AMBRE)]:
        x, y, rr = cx * k, cy * k, r * k
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col + (255,))
    return im.resize((taille, taille), Image.LANCZOS)


# ── Pictogrammes ───────────────────────────────────────────────────────────
# Dessinés à la main plutôt qu'empruntés à une bibliothèque d'icônes : cela
# évite une dépendance et garantit une épaisseur de trait homogène.

def picto(nom, taille, couleur):
    sur = 4
    T = taille * sur
    k = T / 100.0
    im = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = couleur + (255,)
    t = int(8 * k)

    if nom == "check":
        d.line([(24*k, 52*k), (43*k, 70*k), (77*k, 31*k)], fill=c, width=t, joint="curve")
    elif nom == "loupe":
        d.ellipse([22*k, 20*k, 66*k, 64*k], outline=c, width=t)
        d.line([(60*k, 58*k), (80*k, 78*k)], fill=c, width=t)
    elif nom == "temple":
        d.polygon([(50*k, 18*k), (86*k, 38*k), (14*k, 38*k)], fill=c)
        for x in (24, 40, 56, 72):
            d.rectangle([x*k, 44*k, (x+6)*k, 74*k], fill=c)
        d.rectangle([14*k, 78*k, 86*k, 86*k], fill=c)
    elif nom == "ecran":
        d.rounded_rectangle([16*k, 22*k, 84*k, 66*k], radius=int(6*k), outline=c, width=t)
        d.rectangle([40*k, 72*k, 60*k, 78*k], fill=c)
        d.rectangle([30*k, 78*k, 70*k, 84*k], fill=c)
    elif nom == "donnees":
        d.ellipse([20*k, 16*k, 80*k, 36*k], outline=c, width=t)
        for y in (26, 46, 66):
            d.arc([20*k, y*k, 80*k, (y+20)*k], 0, 180, fill=c, width=t)
        d.line([(20*k, 26*k), (20*k, 76*k)], fill=c, width=t)
        d.line([(80*k, 26*k), (80*k, 76*k)], fill=c, width=t)
    elif nom == "megaphone":
        d.polygon([(22*k, 40*k), (56*k, 24*k), (56*k, 76*k), (22*k, 60*k)], fill=c)
        d.arc([56*k, 30*k, 84*k, 70*k], 270, 90, fill=c, width=t)
    elif nom == "toque":
        d.polygon([(50*k, 22*k), (90*k, 40*k), (50*k, 58*k), (10*k, 40*k)], fill=c)
        d.line([(28*k, 48*k), (28*k, 70*k)], fill=c, width=t)
        d.arc([28*k, 56*k, 72*k, 84*k], 0, 180, fill=c, width=t)
        d.line([(72*k, 48*k), (72*k, 70*k)], fill=c, width=t)
    elif nom == "document":
        d.rounded_rectangle([26*k, 16*k, 74*k, 84*k], radius=int(5*k), outline=c, width=t)
        for y in (34, 46, 58, 70):
            d.line([(38*k, y*k), (62*k, y*k)], fill=c, width=int(5*k))
    elif nom == "euro":
        d.arc([28*k, 20*k, 80*k, 80*k], 40, 320, fill=c, width=t)
        d.line([(18*k, 42*k), (58*k, 42*k)], fill=c, width=t)
        d.line([(18*k, 58*k), (58*k, 58*k)], fill=c, width=t)
    elif nom == "alerte":
        d.polygon([(50*k, 16*k), (90*k, 84*k), (10*k, 84*k)], outline=c, width=t)
        d.line([(50*k, 42*k), (50*k, 62*k)], fill=c, width=int(9*k))
        d.ellipse([45*k, 70*k, 55*k, 80*k], fill=c)
    return im.resize((taille, taille), Image.LANCZOS)


# ── Éléments communs à toutes les diapositives ──────────────────────────────

def fond(d):
    for y in range(S):
        t = y / S
        d.line([(0, y), (S, y)],
               fill=tuple(int(NUIT[i] + (NUIT_BAS[i] - NUIT[i]) * t) for i in range(3)))
    d.rectangle([0, 0, 12, S], fill=BLEU)


def signature(im, d):
    """Logo et nom, en haut à droite. Position constante sur toute la série."""
    lg = marque(58)
    x = S - M - 58
    im.paste(lg, (x, 56), lg)
    f = police(26, "bold")
    d.text((x - 12 - largeur(d, "AfricaStudy", f), 60), "AfricaStudy", font=f, fill=BLANC)
    d.text((x - 12 - largeur(d, "Connect", f), 92), "Connect", font=f, fill=BLEU_CLAIR)


def regle(d, y, x=M):
    """Le double filet bleu et ambre : la signature graphique de la série."""
    d.rectangle([x, y, x + 132, y + 9], fill=BLEU_CLAIR)
    d.rectangle([x + 144, y, x + 292, y + 9], fill=AMBRE)


def titre_encadre(d, y, texte):
    """Titre en bleu nuit sur bandeau blanc, comme un tampon."""
    f = ajuste(d, texte.upper(), UTIL - 64, 82, "extra", 34)
    h = int(f.size * 1.34)
    l = largeur(d, texte.upper(), f)
    d.rectangle([M, y, M + l + 56, y + h], fill=BLANC)
    d.text((M + 28, y + (h - f.size) / 2 - f.size * 0.13), texte.upper(), font=f, fill=NUIT)
    regle(d, y + h + 18)
    return y + h + 58


def pied(d, index, total, tagline="S'informer, puis décider."):
    regle(d, S - 118, M)
    d.text((M, S - 78), f"{index:02d}/{total:02d}", font=police(28, "bold"), fill=GRIS_FONCE)
    f = police(27, "texte")
    d.text((S - M - largeur(d, "africastudyconnect.com", f), S - 76),
           "africastudyconnect.com", font=f, fill=GRIS)
    ft = police(25, "texte")
    d.text((M + 130, S - 75), tagline, font=ft, fill=GRIS_FONCE)


def puce(im, d, x, y, icone, teinte, r=34):
    """Pastille ronde portant un pictogramme."""
    d.ellipse([x, y, x + 2*r, y + 2*r], fill=teinte)
    p = picto(icone, int(r * 1.15), NUIT if teinte == AMBRE else BLANC)
    im.paste(p, (x + r - p.width // 2, y + r - p.height // 2), p)
    return 2 * r


# ── Diapositives ───────────────────────────────────────────────────────────

def slide_couverture(cfg, s, index, total):
    im = Image.new("RGB", (S, S), NUIT)
    d = ImageDraw.Draw(im)
    fond(d)
    signature(im, d)

    # On mesure le bloc avant de le poser, pour le centrer optiquement plutôt
    # que de le caler en haut et laisser un vide en bas de l'affiche.
    ft = [ajuste(d, m.upper(), UTIL, 124, "extra", 44) for m in s["titre"]]
    fa = police(40, "bold")
    la = couper(d, s["accroche"], UTIL - 44, fa)
    h = sum(int(f.size * 1.3) for f in ft) + 26 + len(la) * int(fa.size * 1.5)
    y = int((S - h) / 2) - 20

    for f, mot in zip(ft, s["titre"]):
        if s["titre"].index(mot) in s.get("surligne", []):
            d.rectangle([M - 14, y - 6, M + largeur(d, mot.upper(), f) + 26,
                         y + f.size * 1.22], fill=AMBRE)
            d.text((M, y), mot.upper(), font=f, fill=NUIT)
        else:
            d.text((M, y), mot.upper(), font=f, fill=BLANC)
        y += int(f.size * 1.3)

    y += 26
    for ligne in la:
        l = largeur(d, ligne, fa)
        d.rectangle([M - 14, y - 8, M + l + 26, y + fa.size * 1.3], fill=BLANC)
        d.text((M, y), ligne, font=fa, fill=NUIT)
        y += int(fa.size * 1.5)

    pied(d, index, total, cfg.get("tagline", "S'informer, puis décider."))
    return im


def slide_texte(cfg, s, index, total):
    im = Image.new("RGB", (S, S), NUIT)
    d = ImageDraw.Draw(im)
    fond(d)
    signature(im, d)
    y = titre_encadre(d, 228, s["titre"])
    f = police(38, "texte")
    fg = police(38, "texte-g")
    for para in s["paragraphes"]:
        y = riche(d, M, y, para, f, UTIL, BLANC, AMBRE, fg) + 34
    pied(d, index, total, cfg.get("tagline", "S'informer, puis décider."))
    return im


def slide_liste(cfg, s, index, total):
    im = Image.new("RGB", (S, S), NUIT)
    d = ImageDraw.Draw(im)
    fond(d)
    signature(im, d)
    haut = titre_encadre(d, 214, s["titre"])

    items = s["items"]
    bas = S - 150

    # Le contenu est réduit par paliers jusqu'à tenir dans la zone
    # disponible. Cinq entrées à deux lignes de détail ne rentrent pas au
    # corps nominal : sans ce garde-fou, la dernière passerait sous le pied.
    for e in [1.0, 0.94, 0.88, 0.82, 0.76, 0.7, 0.64, 0.58]:
        fch = police(int(34 * e), "texte")
        fchg = police(int(34 * e), "texte-g")
        ft  = police(int(35 * e), "texte-g")
        fd  = police(int(28 * e), "texte")
        r   = int(34 * e)
        dispo_txt = UTIL - (2 * r + 24)

        y0 = haut
        if s.get("chapeau"):
            y0 += hauteur_riche(d, s["chapeau"], UTIL, fch, fchg) + int(28 * e)

        hauteurs = []
        for it in items:
            n = len(couper(d, it["detail"], dispo_txt, fd)) if it.get("detail") else 0
            hauteurs.append(max(2 * r, int(ft.size * 1.35) + n * int(fd.size * 1.24)))
        if y0 + sum(hauteurs) + 12 * (len(items) - 1) <= bas:
            break

    y = haut
    if s.get("chapeau"):
        y = riche(d, M, y, s["chapeau"], fch, UTIL, GRIS, BLANC, fchg) + int(28 * e)

    reste = bas - y - sum(hauteurs)
    ecart = max(10, min(int(34 * e), reste / max(len(items) - 1, 1)))

    for it, hi in zip(items, hauteurs):
        teinte = AMBRE if it.get("cle") else BLEU
        puce(im, d, M, y, it.get("icone", "check"), teinte, r)
        tx = M + 2 * r + 24
        d.text((tx, y + int(r * 0.12)), it["titre"], font=ft, fill=BLANC)
        if it.get("detail"):
            for j, lg in enumerate(couper(d, it["detail"], dispo_txt, fd)):
                d.text((tx, y + int(ft.size * 1.35) + j * int(fd.size * 1.24)),
                       lg, font=fd, fill=GRIS)
        y += int(hi + ecart)

    pied(d, index, total, cfg.get("tagline", "S'informer, puis décider."))
    return im


def slide_chiffre(cfg, s, index, total):
    """La diapositive qui porte l'argument propre au cabinet.

    Elle est composée de bas en haut : le bouton et le pied sont posés
    d'abord, le reste occupe ce qui est disponible. Les corps de texte sont
    ensuite réduits par paliers jusqu'à ce que l'ensemble tienne, afin qu'une
    légende bavarde ne puisse jamais passer sous le bouton.
    """
    im = Image.new("RGB", (S, S), NUIT)
    d = ImageDraw.Draw(im)
    fond(d)
    signature(im, d)
    haut = titre_encadre(d, 206, s["titre"])

    bh, by = 94, S - 216
    dispo = (by - 30) - haut

    for echelle in [1.0, 0.94, 0.88, 0.82, 0.76, 0.7, 0.64]:
        fl  = police(int(35 * echelle), "texte")
        flg = police(int(35 * echelle), "texte-g")
        fc  = police(int(33 * echelle), "texte")
        fcg = police(int(33 * echelle), "texte-g")
        fs  = police(int(24 * echelle), "texte")
        h_leg = hauteur_riche(d, s["legende"], UTIL, fl, flg)
        h_con = hauteur_riche(d, s["conclusion"], UTIL, fc, fcg)
        fixe = 16 + h_leg + 14 + int(fs.size * 1.4) + 44 + 8 + 26 + h_con
        f = ajuste(d, s["chiffre"], UTIL, 186, "extra", 74)
        while f.size > 74 and int(f.size * 1.24) + fixe > dispo:
            f = police(f.size - 4, "extra")
        if int(f.size * 1.24) + fixe <= dispo:
            break

    y = haut + 4
    d.text((M, y), s["chiffre"], font=f, fill=AMBRE)
    y += int(f.size * 1.24) + 16

    y = riche(d, M, y, s["legende"], fl, UTIL, BLANC, BLEU_CLAIR, flg) + 14
    d.text((M, y), s["source"], font=fs, fill=GRIS_FONCE)
    y += int(fs.size * 1.4) + 44

    d.rectangle([M, y, M + 150, y + 8], fill=BLEU)
    y += 26
    riche(d, M, y, s["conclusion"], fc, UTIL, GRIS, BLANC, fcg)

    d.rounded_rectangle([M, by, S - M, by + bh], radius=bh // 2, fill=BLEU)
    fb = police(40, "bold")
    t = s["bouton"]
    d.text((M + (UTIL - largeur(d, t, fb)) / 2, by + (bh - fb.size) / 2 - 7),
           t, font=fb, fill=BLANC)

    pied(d, index, total, cfg.get("tagline", "S'informer, puis décider."))
    return im


RENDUS = {
    "couverture": slide_couverture,
    "texte": slide_texte,
    "liste": slide_liste,
    "chiffre": slide_chiffre,
}


def ardoise(txt):
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    return "".join(c if c.isalnum() else "-" for c in txt.lower()).strip("-").replace("--", "-")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    base = cfg["slug"]
    dossier = os.path.join(SORTIE, "carrousels", base)
    os.makedirs(dossier, exist_ok=True)

    total = len(cfg["slides"])
    print(f"\n  Carrousel : {cfg['titre']}")
    print("  " + "-" * 62)
    poids = 0
    for i, s in enumerate(cfg["slides"], 1):
        im = RENDUS[s["type"]](cfg, s, i, total)
        nom = f"{i:02d}-{ardoise(s.get('fichier', s.get('titre', 'slide')))}-{base}.png"
        chemin = os.path.join(dossier, nom)
        im.save(chemin, "PNG", optimize=True)
        ko = os.path.getsize(chemin) // 1024
        poids += ko
        print(f"     {nom:<62} {ko:>4} Ko")
    print(f"\n  {total} visuels, {poids} Ko au total, dans assets/pub/carrousels/{base}/\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
