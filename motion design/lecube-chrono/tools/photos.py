"""Recadre en 9:16 et étalonne les 12 photos du CUBE (Drive, dossier des pages du site) pour la pub « LE CHRONO ».

Étalonnage LE CUBE, noir et bronze : couleur réduite à 22 %, courbe en S qui creuse les noirs, mi-tons
réchauffés vers le bronze #B27639, vignette. Le rouge des rigs et des murs devient un brun sourd : la charte
du CUBE n'a pas de rouge. Aucune personne sur ces photos.
Sortie : _communs/assets/img/<nom>.jpg en 1188×2112 (10 % de marge pour le zoom lent).

Usage : ~/.venvs/hyperframes-audio/bin/python tools/photos.py <dossier des photos sources>
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "_communs", "assets", "img")
L, H = 1188, 2112
BRONZE = np.array([0xB2, 0x76, 0x39]) / 255

# nom de sortie : (début du nom de fichier source, centre horizontal du recadrage, centre vertical)
PHOTOS = {
    "rig-wallballs": ("LE CUBE 01", 0.30, 0.5),
    "kettlebells": ("LE CUBE 02", 0.50, 0.5),
    "traineaux": ("LE CUBE 03", 0.50, 0.5),
    "sacs": ("LE CUBE 04", 0.50, 0.5),
    "piste": ("LE CUBE 05", 0.50, 0.5),
    "rameurs": ("LE CUBE 06", 0.42, 0.5),
    "rig": ("LE CUBE 07", 0.55, 0.5),
    "boxes": ("LE CUBE 08", 0.50, 0.5),
    "chrono-led": ("LE CUBE 09", 0.70, 0.5),
    "portique": ("LE CUBE 10", 0.45, 0.5),
    "ring": ("LE CUBE 11", 0.50, 0.5),
    "tatami": ("LE CUBE 12", 0.55, 0.5),
}


def recadrer(im, cx, cy):
    w, h = im.size
    if w / h > L / H:
        cw, ch = round(h * L / H), h
    else:
        cw, ch = w, round(w * H / L)
    x0 = min(max(0, round(cx * w - cw / 2)), w - cw)
    y0 = min(max(0, round(cy * h - ch / 2)), h - ch)
    return im.crop((x0, y0, x0 + cw, y0 + ch)).resize((L, H), Image.LANCZOS)


def etalonner(im):
    x = np.asarray(im.convert("RGB")).astype(np.float64) / 255
    y = (0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2])[..., None]
    c = y + 0.22 * (x - y)                                   # couleur réduite
    c = np.clip(c * 0.92, 0, 1) ** 1.18                      # noirs creusés
    c = c * c * (3 - 2 * c) * 0.55 + c * 0.45                # courbe en S douce
    yc = (0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2])[..., None]
    mi = 4 * yc * (1 - yc)                                   # poids des mi-tons
    c = c + 0.22 * mi * (BRONZE * (yc / 0.45) - c)           # mi-tons tirés vers le bronze
    c = c * np.array([1.0, 0.975, 0.94])                     # hautes lumières chaudes
    hh, ww = c.shape[:2]
    yy, xx = np.mgrid[0:hh, 0:ww]
    r = np.sqrt(((xx - ww / 2) / (ww / 2)) ** 2 + ((yy - hh / 2) / (hh / 2)) ** 2)
    c = c * (1 - 0.28 * np.clip(r - 0.55, 0, 1) ** 1.6)[..., None]   # vignette
    out = Image.fromarray((np.clip(c, 0, 1) * 255 + 0.5).astype(np.uint8))
    return out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=55, threshold=2))


def main():
    src = sys.argv[1]
    os.makedirs(SORTIE, exist_ok=True)
    fichiers = sorted(os.listdir(src))
    for nom, (prefixe, cx, cy) in PHOTOS.items():
        f = next(f for f in fichiers if f.startswith(prefixe))
        im = etalonner(recadrer(Image.open(os.path.join(src, f)), cx, cy))
        im.save(os.path.join(SORTIE, f"{nom}.jpg"), quality=86, optimize=True, progressive=True)
        print(f"{nom}.jpg ← {f}")


if __name__ == "__main__":
    main()
