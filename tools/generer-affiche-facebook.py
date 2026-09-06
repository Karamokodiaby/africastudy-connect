#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère l'affiche carrée 1080 x 1080 destinée au fil Facebook.

Nécessite Pillow :   pip install pillow

À regénérer quand les tarifs changent, et impérativement après le
31 octobre : l'affiche annonce « dès 400 000 FCFA, offre valable jusqu'au
31 octobre », mention qui devient trompeuse une fois l'échéance passée.

Les polices sont celles de macOS. Sur un autre système, adaptez F.
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.expanduser('~/africastudy-connect/assets/pub')
F = "/System/Library/Fonts/Supplemental/"
NUIT, BLANC, GRIS = (30, 41, 59), (255, 255, 255), (203, 213, 225)
BLEU, BLEU_CLAIR, AMBRE = (37, 99, 235), (96, 165, 250), (245, 158, 11)

def police(t, gras=True):
    return ImageFont.truetype(F + ("Arial Bold.ttf" if gras else "Arial.ttf"), t)

def ajuste(d, txt, largeur, taille, gras=True, mini=14):
    while taille > mini:
        f = police(taille, gras)
        if d.textlength(txt, font=f) <= largeur: return f
        taille -= 1
    return police(mini, gras)

def bezier(p0,p1,p2,p3,n=260):
    o=[]
    for i in range(n+1):
        t=i/n; u=1-t
        o.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],
                  u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    return o

def marque(taille):
    S=3; T=taille*S; k=T/40
    im=Image.new("RGBA",(T,T),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,T-1,T-1],radius=int(9*k),fill=(15,23,42,255))
    d.line([(x*k,y*k) for x,y in bezier((10,30),(10,18.5),(17.5,11.5),(30,11))],
           fill=BLANC+(255,),width=int(3.4*k),joint="curve")
    for c,r,col in [((10,30),3.2,BLEU_CLAIR+(255,)),((30,11),4.2,AMBRE+(255,))]:
        cx,cy,rr=c[0]*k,c[1]*k,r*k
        d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr],fill=col)
    return im.resize((taille,taille),Image.LANCZOS)

S = 1080
im = Image.new("RGB",(S,S),NUIT); d = ImageDraw.Draw(im)
for y in range(S):
    t=y/S
    d.line([(0,y),(S,y)], fill=(int(30+(13-30)*t), int(41+(20-41)*t), int(59+(38-59)*t)))
d.rectangle([0,0,14,S], fill=BLEU)

M = 86
util = S - 2*M

# ── Marque ────────────────────────────────────────────────────────────
lg = marque(96); im.paste(lg,(M,72),lg)
d.text((M+120, 84), "AfricaStudy", font=police(38), fill=BLANC)
d.text((M+120, 128), "Connect", font=police(38), fill=BLEU_CLAIR)

# ── Accroche ──────────────────────────────────────────────────────────
f1 = ajuste(d, "Étudier en France,", util, 92)
d.text((M, 268), "Étudier en France,", font=f1, fill=BLANC)
f2 = ajuste(d, "au Canada, en Europe", util, 92)
d.text((M, 368), "au Canada, en Europe", font=f2, fill=BLANC)
d.rectangle([M, 486, M+150, 496], fill=AMBRE)

# ── Promesse ──────────────────────────────────────────────────────────
d.text((M, 536), "Étude de profil GRATUITE", font=police(46), fill=BLANC)
d.text((M, 596), "et sans engagement", font=police(38, False), fill=GRIS)

# ── Prix ──────────────────────────────────────────────────────────────
fp = police(64)
d.text((M, 686), "Dès 400 000 FCFA", font=fp, fill=AMBRE)
x = M + d.textlength("Dès 400 000 FCFA", font=fp) + 26
fb = police(38, False)
d.text((x, 704), "492 000", font=fb, fill=GRIS)
d.line([(x, 726), (x + d.textlength("492 000", font=fb), 726)], fill=(220,38,38), width=4)
d.text((M, 766), "Offre valable jusqu'au 31 octobre", font=police(32, False), fill=GRIS)

# ── Appel à l'action ──────────────────────────────────────────────────
BH, BY = 96, 848
d.rounded_rectangle([M, BY, S-M, BY+BH], radius=BH//2, fill=BLEU)
fbt = police(42)
txt = "Évaluer mon dossier"
d.text((M + (util - d.textlength(txt, font=fbt))/2, BY + (BH-fbt.size)/2 - 6), txt, font=fbt, fill=BLANC)

# ── Pied ──────────────────────────────────────────────────────────────
d.text((M, 986), "africastudyconnect.com", font=police(34), fill=BLANC)
wa = "WhatsApp +33 6 16 48 35 58"
fw = police(30, False)
d.text((S-M-d.textlength(wa, font=fw), 990), wa, font=fw, fill=GRIS)

nom = "etudier-en-france-depuis-la-cote-divoire-africastudy-connect.png"
im.save(f"{OUT}/{nom}", "PNG", optimize=True)
print(nom, "->", os.path.getsize(f"{OUT}/{nom}")//1024, "Ko")
