"""Écrans réels de la fontaine (photos du 22/10/2026) : redressés, nettoyés, posés dans un cadre inox unique.

Sources hors dépôt (logo de la marque des concentrés à l'écran) : ~/fontaine-sources/ecran/
  1_gouts.jpg (« Sélectionnez le concentré »), 2_eau.jpg (« Choisissez l'eau … »), 3_debut.jpg (« distribution de
  boissons », bouton « Début »), 4_intensite.jpg (« Choisissez l'intensité du goût »), 2000×1500, prises en biais.

Étapes :
  1. redressement : les 4 coins de la dalle (mesurés au seuil de luminance 170) → 1280×1024 (dalle 17″ en 5:4) ;
  2. moiré de la photo d'écran : 3 filtres bilatéraux (les rides de ±9 niveaux disparaissent, les traits et les textes
     restent), fond relevé au blanc d'écran, teintes très pâles neutralisées (franges roses et vertes) ;
  3. reflets de plafond et curseur de souris : retouchés par inpainting, aux points listés dans RETOUCHES ;
  4. cadre inox : la photo 1 redressée avec une marge (le cadre est dans le plan de la dalle), découpée en rectangle,
     dalle évidée (les écrans passent dessous, le bord noir du cadre masque leurs bords) ;
  5. fontaine de l'affiche (rendu fabricant, écran d'une autre interface) : l'écran réel « goûts » posé dans sa dalle.

Écrit dans ~/fontaine-sources : ecran/propres/{gouts,intensite,eau,debut}.jpg, ecran/cadre.png, fontaine_ecran.png.
Usage : ~/.venvs/hyperframes-audio/bin/python -I tools/ecrans.py
"""
import os

import cv2
import numpy as np

SOURCES = os.path.expanduser(os.environ.get("FONTAINE_SOURCES", "~/fontaine-sources"))
W, H = 1280, 1024
# Coins de la dalle (haut gauche, haut droit, bas droit, bas gauche) sur chaque photo
COINS = {
    "gouts": ("1_gouts", [[347, 197], [1686, 202], [1629, 1214], [404, 1220]]),
    "eau": ("2_eau", [[387, 118], [1678, 132], [1642, 1135], [412, 1136]]),
    "debut": ("3_debut", [[395, 271], [1665, 274], [1635, 1267], [419, 1262]]),
    "intensite": ("4_intensite", [[411, 175], [1702, 197], [1638, 1180], [446, 1172]]),
}
# Reflets (x, y, rayon) et curseurs, en pixels de la dalle redressée
RETOUCHES = {
    "gouts": [(290, 187, 14)],
    "eau": [(262, 356, 13), (1019, 678, 12)],
    "debut": [(426, 557, 11), (295, 233, 9)],
    "intensite": [(242, 220, 13), (768, 512, 12)],
}
MARGE = 260                      # cadre : photo 1 redressée avec cette marge autour de la dalle
CADRE = (60, 130, 1740, 1420)    # x0, y0, x1, y1 du cadre inox dans l'image redressée avec marge
ECRAN_AFFICHE = [[385, 41], [774, 41], [774, 356], [385, 356]]   # dalle de la fontaine sur fontaine_detouree.png


def redresser(nom, coins, marge=0):
    im = cv2.imread(os.path.join(SOURCES, "ecran", nom + ".jpg"), cv2.IMREAD_COLOR)
    dst = np.float32([[marge, marge], [marge + W, marge], [marge + W, marge + H], [marge, marge + H]])
    M = cv2.getPerspectiveTransform(np.float32(coins), dst)
    return cv2.warpPerspective(im, M, (W + 2 * marge, H + 2 * marge), flags=cv2.INTER_LANCZOS4)


def nettoyer(im, retouches):
    masque = np.zeros(im.shape[:2], np.uint8)
    for x, y, r in retouches:
        cv2.circle(masque, (x, y), r, 255, -1)
    im = cv2.inpaint(im, masque, 5, cv2.INPAINT_TELEA)
    for _ in range(3):
        im = cv2.bilateralFilter(im, d=13, sigmaColor=14, sigmaSpace=6)
    lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).astype(np.float32)
    L, a, b = lab[..., 0] * 244 / 226, lab[..., 1] - 128, lab[..., 2] - 128
    haut = L > 236
    L[haut] = 236 + (L[haut] - 236) * 0.3                     # fond : blanc d'écran, rides résiduelles écrasées
    seuil = 6 + 8 * np.clip((L - 220) / 15, 0, 1)             # plus le pixel est clair, plus sa teinte doit être nette
    f = np.clip((np.hypot(a, b) - seuil) / 8, 0, 1)
    lab = np.dstack([np.clip(L, 0, 255), a * f + 128, b * f + 128]).astype(np.uint8)
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


def cadre():
    nom, coins = COINS["gouts"]
    im = redresser(nom, coins, MARGE)
    x0, y0, x1, y1 = CADRE
    c = im[y0:y1, x0:x1]
    hc, wc = c.shape[:2]
    alpha = np.full((hc, wc), 255, np.uint8)
    r = 14                                                     # coins extérieurs légèrement arrondis
    for x, y in ((0, 0), (wc - r, 0), (0, hc - r), (wc - r, hc - r)):
        alpha[y:y + r, x:x + r] = 0
    for cx, cy in ((r, r), (wc - 1 - r, r), (r, hc - 1 - r), (wc - 1 - r, hc - 1 - r)):
        cv2.circle(alpha, (cx, cy), r, 255, -1)
    ex, ey = MARGE - x0, MARGE - y0                            # dalle évidée, 3 px en retrait : le bord noir couvre l'écran
    alpha[ey + 3:ey + H - 3, ex + 3:ex + W - 3] = 0
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
    out = np.dstack([c, alpha])
    k = 936 / W                                                # à la taille d'affichage de la story (dalle sur 936 px)
    out = cv2.resize(out, (round(out.shape[1] * k), round(out.shape[0] * k)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(os.path.join(SOURCES, "ecran", "cadre.png"), out, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    return out.shape[1], out.shape[0], ex, ey


def fontaine(gouts):
    im = cv2.imread(os.path.join(SOURCES, "fontaine_detouree.png"), cv2.IMREAD_UNCHANGED)
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [W, 0], [W, H], [0, H]]), np.float32(ECRAN_AFFICHE))
    h, w = im.shape[:2]
    ecran = cv2.warpPerspective(cv2.resize(gouts, (W, H), interpolation=cv2.INTER_AREA), M, (w, h), flags=cv2.INTER_AREA)
    m = cv2.warpPerspective(np.full((H, W), 255, np.uint8), M, (w, h))
    m = cv2.erode(m, np.ones((3, 3), np.uint8))[..., None] / 255.0
    im[..., :3] = (im[..., :3] * (1 - m) + ecran * m).astype(np.uint8)
    cv2.imwrite(os.path.join(SOURCES, "fontaine_ecran.png"), im, [cv2.IMWRITE_PNG_COMPRESSION, 9])


def main():
    d = os.path.join(SOURCES, "ecran", "propres")
    os.makedirs(d, exist_ok=True)
    propres = {}
    for cle, (nom, coins) in COINS.items():
        propres[cle] = nettoyer(redresser(nom, coins), RETOUCHES[cle])
        cv2.imwrite(os.path.join(d, cle + ".jpg"), propres[cle], [cv2.IMWRITE_JPEG_QUALITY, 92])
    w, h, ex, ey = cadre()
    fontaine(propres["gouts"])
    print(f"Écrans : {d} ({W}×{H}) · cadre {w}×{h} (photo : {CADRE[2] - CADRE[0]}×{CADRE[3] - CADRE[1]}, dalle à ({ex}, {ey})) · fontaine_ecran.png")


if __name__ == "__main__":
    main()
