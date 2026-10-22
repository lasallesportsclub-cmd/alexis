"""Détoure la fontaine à boisson sportive depuis la capture de l'affiche 02/03 (674×817, seule source disponible).

La fontaine était déjà détourée sur l'affiche : ses bords sont nets sur un fond sombre (luminance ≤ 40, machine ≥ 45).
Étapes :
  1. extrémité droite du plateau : remplacée par le miroir de l'extrémité gauche (le texte « vous venez. » la recouvrait) ;
     la machine est symétrique autour de x = 229 (colonnes 123–148 et 310–335) ;
  2. pastilles et filets or des légendes : effacés par interpolation (verticale sur les colonnes, horizontale sur le bac) ;
  3. masque = luminance > 44 dans le cadre de la machine, plus la gourde (bouchon sombre) en polygone ;
  4. agrandissement ×3 (Lanczos), alpha adouci, accentuation légère.

⚠ Résolution d'origine faible (machine ≈ 380 px de large) : à remplacer par la photo d'origine ou une photo de la vraie
machine au club dès qu'elle est disponible (même nom de fichier, tools/build.py la recopie).

Usage : ~/.venvs/hyperframes-audio/bin/python -I tools/detourer.py ~/fontaine-sources/affiche_02_03_capture.webp \
        ~/fontaine-sources/fontaine_detouree.png
"""
import sys

import cv2
import numpy as np

AXE = 458            # x' = AXE - x : symétrie gauche/droite de la machine
CADRE = (36, 324, 422, 607)   # x0, y0, x1, y1 de la machine sur la capture
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
    assert im is not None and im.shape[:2] == (817, 674), "capture attendue : 674×817"

    # 1. Extrémité droite du plateau = miroir de la gauche
    for x in range(365, 431):
        im[553:612, x] = im[553:612, AXE - x]

    # 2. Pastilles (anneau ≈ 7,5 px) et filets or des deux légendes (lignes 419–422 et 555–558, halo sombre compris).
    #    Colonnes et cadre d'écran sont uniformes à la verticale, le bac à l'horizontale : on interpole dans ce sens.
    im = im.astype(np.float32)
    interp_v(im, 276, 340, 410, 434)        # pastille 1 et son filet sur le cadre et la colonne droite
    interp_v(im, 300, 340, 551, 563)        # filet 2 sur la colonne droite
    interp_h(im, 246, 268, 546, 571)        # pastille 2 sur le bac, à droite de la gourde
    im = np.clip(im, 0, 255).astype(np.uint8)

    # 3. Masque
    gris = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    x0, y0, x1, y1 = CADRE
    seuil = (gris > 44).astype(np.uint8) * 255
    machine = np.zeros(gris.shape, np.uint8)                        # zone où la machine peut se trouver
    for p in (
        [(146, 325), (312, 325), (312, 468), (146, 468)],           # écran et son cadre
        [(121, 376), (150, 376), (150, 594), (121, 594)],           # colonne gauche
        [(308, 376), (338, 376), (338, 594), (308, 594)],           # colonne droite
        [(220, 454), (239, 454), (239, 472), (220, 472)],           # bec
        [(140, 558), (318, 558), (318, 572), (140, 572)],           # bac
        [(36, 607), (36, 584), (56, 568), (402, 568), (422, 584), (422, 607)],   # plateau
    ):
        cv2.fillPoly(machine, [np.array(p, np.int32)], 255)
    masque = cv2.bitwise_and(seuil, machine)
    gourde = [np.array(p, np.int32) for p in (
        [(223, 488), (234, 488), (234, 498), (223, 498)],           # bouchon
        [(213, 497), (244, 497), (244, 512), (213, 512)],           # col
        [(212, 510), (245, 510), (245, 576), (212, 576)],           # corps
    )]
    cv2.fillPoly(masque, gourde, 255)
    masque = cv2.morphologyEx(masque, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(masque, 8)
    garde = np.zeros_like(masque)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= 60:
            garde[lab == i] = 255
    masque = garde

    # 4. Recadrage, agrandissement, alpha
    im, masque = im[y0:y1, x0:x1], masque[y0:y1, x0:x1]
    w, h = (x1 - x0) * ECHELLE, (y1 - y0) * ECHELLE
    grand = cv2.resize(im, (w, h), interpolation=cv2.INTER_LANCZOS4)
    flou = cv2.GaussianBlur(grand, (0, 0), 1.6)
    grand = cv2.addWeighted(grand, 1.45, flou, -0.45, 0)
    alpha = cv2.resize(masque, (w, h), interpolation=cv2.INTER_LINEAR)
    alpha = cv2.GaussianBlur(alpha, (0, 0), 0.9)
    out = np.dstack([grand, alpha])
    cv2.imwrite(dst, out)
    print(f"{dst} : {w}×{h}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
