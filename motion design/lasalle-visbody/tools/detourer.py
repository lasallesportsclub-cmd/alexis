"""Détoure la Visbody M60 depuis la capture de l'affiche 02/03 « UN SCAN À 360° » (659×818, seule source disponible).

La machine est sombre sur un fond sombre : un seuil ne suffit pas. Le masque est donc construit à partir de ses formes,
mesurées sur la capture (profils de luminance) :
  écran à coins arrondis x 107,5–250,5 / y 125,5–608 · poignées x 89,5–99,5 et 257,5–267,5 dès y 352,5 ·
  colonne x 139,5–219,5 · socle x 58,5–298,5 sous une ellipse (179, 683) · plateau : ellipse (179, 725), 149 × 17.
Les pastilles et filets des légendes sont effacés par interpolation (verticale sur l'écran et la poignée),
puis l'image est agrandie ×3 (Lanczos), alpha adouci, accentuation légère.

⚠ Résolution d'origine faible (machine ≈ 300 px de haut sur 610) et logo VISBODY lisible à l'écran : à remplacer par
une photo de la vraie machine au club (même nom de fichier, tools/build.py la recopie).

Usage : ~/.venvs/hyperframes-audio/bin/python -I tools/detourer.py ~/visbody-sources/3.webp ~/visbody-sources/m60_detouree.png
"""
import sys

import cv2
import numpy as np

CADRE = (26, 120, 332, 746)    # x0, y0, x1, y1 de la machine sur la capture
ECHELLE = 3


def interp_v(im, x0, x1, y0, y1):
    """Remplace les lignes y0..y1-1 par un fondu linéaire entre la ligne y0-1 et la ligne y1."""
    haut, bas = im[y0 - 1, x0:x1].copy(), im[y1, x0:x1].copy()
    for k, y in enumerate(range(y0, y1)):
        a = (k + 1) / (y1 - y0 + 1)
        im[y, x0:x1] = (1 - a) * haut + a * bas


def interp_h(im, x0, x1, y0, y1):
    """Remplace les colonnes x0..x1-1 par un fondu linéaire entre la colonne x0-1 et la colonne x1."""
    g, d = im[y0:y1, x0 - 1].copy(), im[y0:y1, x1].copy()
    for k, x in enumerate(range(x0, x1)):
        a = (k + 1) / (x1 - x0 + 1)
        im[y0:y1, x] = (1 - a) * g + a * d


def main(src, dst):
    im = cv2.imread(src, cv2.IMREAD_COLOR)
    assert im is not None and im.shape[:2] == (818, 659), "capture attendue : 659×818"
    im = im.astype(np.float32)
    interp_v(im, 216, 249, 403, 430)     # pastille 1 sur l'écran (écran uniforme à la verticale)
    interp_v(im, 236, 280, 412, 421)     # son filet : bord de l'écran, poignée droite
    interp_v(im, 248, 278, 533, 560)     # pastille 2 et son filet sur la poignée droite
    im = np.clip(im, 0, 255).astype(np.uint8)

    s = 8                                # masque dessiné à 8× puis réduit : bords lissés
    m = np.zeros((818 * s, 659 * s), np.uint8)
    def rect(x0, y0, x1, y1, r=0):
        p0, p1 = (round(x0 * s), round(y0 * s)), (round(x1 * s), round(y1 * s))
        if not r:
            cv2.rectangle(m, p0, p1, 255, -1)
            return
        r = round(r * s)
        cv2.rectangle(m, (p0[0] + r, p0[1]), (p1[0] - r, p1[1]), 255, -1)
        cv2.rectangle(m, (p0[0], p0[1] + r), (p1[0], p1[1] - r), 255, -1)
        for cx, cy in ((p0[0] + r, p0[1] + r), (p1[0] - r, p0[1] + r), (p0[0] + r, p1[1] - r), (p1[0] - r, p1[1] - r)):
            cv2.circle(m, (cx, cy), r, 255, -1)
    def ellipse(cx, cy, rx, ry):
        cv2.ellipse(m, (round(cx * s), round(cy * s)), (round(rx * s), round(ry * s)), 0, 0, 360, 255, -1)
    rect(107.5, 125.5, 250.5, 609, 5)    # écran
    rect(89.5, 352.5, 99.5, 690, 2)      # poignée gauche
    rect(257.5, 352.5, 267.5, 690, 2)    # poignée droite
    rect(139.5, 605, 219.5, 690)         # colonne
    ellipse(179, 683, 120, 9)            # dessus du socle
    rect(58.5, 683, 298.5, 721)          # socle
    ellipse(179, 725, 149, 17)           # plateau
    m = cv2.resize(m, (659, 818), interpolation=cv2.INTER_AREA)

    x0, y0, x1, y1 = CADRE
    im, m = im[y0:y1, x0:x1], m[y0:y1, x0:x1]
    w, h = (x1 - x0) * ECHELLE, (y1 - y0) * ECHELLE
    grand = cv2.resize(im, (w, h), interpolation=cv2.INTER_LANCZOS4)
    flou = cv2.GaussianBlur(grand, (0, 0), 1.6)
    grand = cv2.addWeighted(grand, 1.4, flou, -0.4, 0)
    alpha = cv2.GaussianBlur(cv2.resize(m, (w, h), interpolation=cv2.INTER_CUBIC), (0, 0), 0.8)
    cv2.imwrite(dst, np.dstack([grand, alpha]))
    print(f"{dst} : {w}×{h}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
