#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère les images publicitaires de assets/pub/ dans les trois formats
courants : bannière large, rectangle moyen, bannière mobile.

Nécessite Pillow :   pip install pillow

Les textes et les montants sont définis dans le corps du script. À
regénérer quand les tarifs changent, et impérativement à la fin de la
promotion : les créations actuelles annoncent « dès 400 000 FCFA
jusqu'au 31 octobre », mention qui devient trompeuse une fois l'échéance
passée.

Les polices sont celles de macOS. Sur un autre système, adaptez le
chemin de la constante F.
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.expanduser('~/africastudy-connect/assets/pub')
F = "/System/Library/Fonts/Supplemental/"
NUIT, BLANC, GRIS = (30, 41, 59), (255, 255, 255), (203, 213, 225)
BLEU, BLEU_CLAIR, AMBRE = (37, 99, 235), (96, 165, 250), (245, 158, 11)

def police(t, gras=True):
    return ImageFont.truetype(F + ("Arial Bold.ttf" if gras else "Arial.ttf"), t)

def ajuste(d, texte, largeur_max, taille, gras=True, mini=8):
    """Réduit la taille jusqu'à ce que le texte tienne dans la largeur."""
    while taille > mini:
        f = police(taille, gras)
        if d.textlength(texte, font=f) <= largeur_max:
            return f
        taille -= 1
    return police(mini, gras)

def bezier(p0, p1, p2, p3, n=200):
    o = []
    for i in range(n+1):
        t = i/n; u = 1-t
        o.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],
                  u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    return o

def marque(taille):
    S=4; T=taille*S; k=T/40
    im = Image.new("RGBA",(T,T),(0,0,0,0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,T-1,T-1], radius=int(9*k), fill=NUIT+(255,))
    d.line([(x*k,y*k) for x,y in bezier((10,30),(10,18.5),(17.5,11.5),(30,11))],
           fill=BLANC+(255,), width=int(3.4*k), joint="curve")
    for c,r,col in [((10,30),3.2,BLEU_CLAIR+(255,)), ((30,11),4.2,AMBRE+(255,))]:
        cx,cy,rr = c[0]*k, c[1]*k, r*k
        d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr], fill=col)
    return im.resize((taille,taille), Image.LANCZOS)

def fond(l,h):
    im = Image.new("RGB",(l,h),NUIT); d = ImageDraw.Draw(im)
    for y in range(h):
        t=y/h
        d.line([(0,y),(l,y)], fill=(int(30+(15-30)*t), int(41+(23-41)*t), int(59+(42-59)*t)))
    d.rectangle([0,0,4,h], fill=BLEU)
    return im,d

def bouton(d,x,y,l,h,texte,taille_max):
    d.rounded_rectangle([x,y,x+l,y+h], radius=h//2, fill=BLEU)
    f = ajuste(d, texte, l-18, taille_max)
    w = d.textlength(texte, font=f)
    d.text((x+(l-w)/2, y+(h-f.size)/2-2), texte, font=f, fill=BLANC)

def barre(d, x, y, texte, f, couleur):
    """Ancien prix, barré."""
    d.text((x,y), texte, font=f, fill=couleur)
    w = d.textlength(texte, font=f)
    d.line([(x, y+f.size*0.58), (x+w, y+f.size*0.58)], fill=(220,38,38), width=2)

# ══ 300 × 250 ═════════════════════════════════════════════════════════
L,H = 300,250
im,d = fond(L,H); M=20; util = L-2*M
lg = marque(32); im.paste(lg,(M,18),lg)
d.text((M+42,20), "AfricaStudy", font=police(14), fill=BLANC)
d.text((M+42,37), "Connect", font=police(14), fill=BLEU_CLAIR)
f1 = ajuste(d, "Étudier en France,", util, 22)
d.text((M,72), "Étudier en France,", font=f1, fill=BLANC)
f2 = ajuste(d, "au Canada, en Europe", util, 22)
d.text((M,98), "au Canada, en Europe", font=f2, fill=BLANC)
d.rectangle([M,130,M+52,134], fill=AMBRE)
d.text((M,145), "Étude de profil gratuite", font=police(12,False), fill=GRIS)
fp = police(16)
d.text((M,166), "Dès 400 000 FCFA", font=fp, fill=AMBRE)
barre(d, M+d.textlength("Dès 400 000 FCFA", font=fp)+10, 169, "492 000", police(11,False), GRIS)
bouton(d, M, 194, util, 32, "Faire évaluer mon dossier", 12)
d.text((M,234), "africastudyconnect.com", font=police(10,False), fill=GRIS)
im.save(f"{OUT}/pub-300x250.png","PNG",optimize=True)

# ══ 728 × 90 ══════════════════════════════════════════════════════════
L,H = 728,90
im,d = fond(L,H)
lg = marque(40); im.paste(lg,(20,25),lg)
d.text((70,26), "AfricaStudy", font=police(15), fill=BLANC)
d.text((70,45), "Connect", font=police(15), fill=BLEU_CLAIR)
BL, BX = 152, L-20-152
d.line([(196,22),(196,68)], fill=(71,85,105), width=1)
zone = BX-20-216
ft = ajuste(d, "Étudier en France, au Canada, en Europe", zone, 21)
d.text((216,24), "Étudier en France, au Canada, en Europe", font=ft, fill=BLANC)
sous = "Étude de profil gratuite  ·  dès 400 000 FCFA jusqu'au 31 octobre"
fs = ajuste(d, sous, zone, 13, gras=False)
d.text((216,52), sous, font=fs, fill=GRIS)
bouton(d, BX, 27, BL, 36, "Évaluer mon dossier", 13)
im.save(f"{OUT}/pub-728x90.png","PNG",optimize=True)

# ══ 320 × 100 ═════════════════════════════════════════════════════════
L,H = 320,100
im,d = fond(L,H); M=14
lg = marque(30); im.paste(lg,(M,14),lg)
d.text((M+38,16), "AfricaStudy Connect", font=police(12), fill=BLANC)
BL, BX = 92, L-M-92
zone = BX-M-12
ft = ajuste(d, "Étudier à l'étranger", zone, 17)
d.text((M+38,33), "Étudier à l'étranger", font=ft, fill=BLANC)
d.text((M,64), "Étude de profil gratuite", font=police(10,False), fill=GRIS)
d.text((M,79), "Dès 400 000 FCFA", font=police(12), fill=AMBRE)
bouton(d, BX, 58, BL, 30, "J'évalue", 12)
im.save(f"{OUT}/pub-320x100.png","PNG",optimize=True)

for f in sorted(os.listdir(OUT)):
    print(f"  {f:<20} {os.path.getsize(os.path.join(OUT,f))//1024} Ko")
