#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Affiche carrée 1080 x 1080 conçue pour faire cliquer, et non pour tout dire.

Elle pose un écart de prix vrai et surprenant sans en donner l'explication :
c'est l'article qui la donne. Une affiche qui délivre toute l'information
ne laisse aucune raison de cliquer.

Les montants proviennent du barème officiel 2026-2027 repris dans
blog/frais-inscription-universite-publique-france-2026-2027.html.
À regénérer quand ce barème change.

Nécessite Pillow. Polices macOS : adapter F sur un autre système.
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

M = 86; util = S - 2*M

lg = marque(68); im.paste(lg,(M,64),lg)
d.text((M+90, 76), "AfricaStudy", font=police(27), fill=BLANC)
d.text((M+90, 108), "Connect", font=police(27), fill=BLEU_CLAIR)

d.text((M, 232), "UNIVERSITÉ PUBLIQUE EN FRANCE · LICENCE",
       font=police(28), fill=AMBRE)

d.text((M, 292), "178 €", font=police(150), fill=BLANC)
d.text((M, 452), "ou", font=police(50, False), fill=GRIS)
d.text((M, 524), "2 902 €", font=police(150), fill=AMBRE)

d.rectangle([M, 706, M+150, 714], fill=BLEU)
f1 = ajuste(d, "Pour la même licence, la même année.", util, 40, gras=False)
d.text((M, 752), "Pour la même licence, la même année.", font=f1, fill=BLANC)
f2 = ajuste(d, "Tout dépend de l'université que vous visez.", util, 40, gras=False)
d.text((M, 802), "Tout dépend de l'université que vous visez.", font=f2, fill=GRIS)

BH, BY = 96, 884
d.rounded_rectangle([M, BY, S-M, BY+BH], radius=BH//2, fill=BLEU)
fbt = police(42); txt = "Comprendre la différence"
d.text((M + (util - d.textlength(txt, font=fbt))/2, BY + (BH-fbt.size)/2 - 6), txt, font=fbt, fill=BLANC)

fu = police(32)
d.text((M + (util - d.textlength("africastudyconnect.com", font=fu))/2, 1006),
       "africastudyconnect.com", font=fu, fill=GRIS)

nom = "frais-inscription-universite-france-2026-2027-africastudy-connect.png"
im.save(f"{OUT}/{nom}", "PNG", optimize=True)
print(nom, "->", os.path.getsize(f"{OUT}/{nom}")//1024, "Ko")
