"""Recadre et étalonne les vraies photos du club pour les fonds de la pub (1350×2400, marge pour le zoom).

Sources (Drive du club, hors dépôt) : facade.jpg (1350×2400, dossier du kit), IMG_2426.jpeg (haltères),
IMG_2429.jpeg (tapis de course). Aucune personne à l'image : plateau.jpg (trois adhérents
reconnaissables), IMG_2428 (salle de vélos, cours = formule Privilège), IMG_2431 (hall : ascenseur et
poubelle) et IMG_2432 (compléments) sont écartées.
Étalonnage de la charte Le Trait Oblique : saturation 0,78, courbe en S douce, hautes lumières un peu
chaudes. L'assombrissement et le grain se font dans la composition.

Usage : python tools/photos.py DOSSIER_DES_ORIGINAUX
"""
import os
import sys

import numpy as np
from PIL import Image, ImageOps

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "assets", "img")
W, H = 1350, 2400

# nom → (fichier source, boîte de recadrage (x0, y0, x1, y1) au ratio 9:16 dans l'image redressée)
PLANS = {
    "fond-facade": ("facade.jpg", (0, 0, 1350, 2400)),
    "fond-enseigne": ("facade.jpg", (500, 640, 1300, 2062)),          # « LA SALLE » et « 7/7 6H-23H »
    "fond-tapis": ("IMG_2429.jpeg", (500, 0, 3713, 5712)),
    "fond-tapis-detail": ("IMG_2429.jpeg", (1500, 2400, 3300, 5600)),  # tapis et sol, sans l'écran
    "fond-halteres": ("IMG_2426.jpeg", (0, 0, 3213, 5712)),
    "fond-halteres-detail": ("IMG_2426.jpeg", (0, 600, 1800, 3800)),
}


def etalonner(im):
    a = np.asarray(im, dtype=np.float32) / 255.0
    lum = (a * [0.2126, 0.7152, 0.0722]).sum(axis=2, keepdims=True)
    a = lum + (a - lum) * 0.78                                   # saturation 0,78
    s = a * a * (3 - 2 * a)                                     # courbe en S
    a = a * 0.7 + s * 0.3
    hl = np.clip((lum - 0.55) / 0.45, 0, 1) ** 2                 # hautes lumières chaudes
    a[..., 0] += 0.025 * hl[..., 0]
    a[..., 2] -= 0.02 * hl[..., 0]
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def main():
    src = sys.argv[1]
    os.makedirs(SORTIE, exist_ok=True)
    for nom, (fichier, boite) in PLANS.items():
        im = ImageOps.exif_transpose(Image.open(os.path.join(src, fichier))).convert("RGB")
        x0, y0, x1, y1 = boite
        assert abs((x1 - x0) / (y1 - y0) - 9 / 16) < 0.01, nom
        im = etalonner(im.crop(boite).resize((W, H), Image.LANCZOS))
        im.save(os.path.join(SORTIE, nom + ".jpg"), quality=86, optimize=True, progressive=True)
        print(nom, im.size)


if __name__ == "__main__":
    main()
