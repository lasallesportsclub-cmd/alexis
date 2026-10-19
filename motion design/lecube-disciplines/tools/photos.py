"""Recadre en 9:16 et étalonne les photos de pratiquants des pubs LE CUBE par discipline.

Les photos montrent des personnes : elles restent HORS du dépôt (public). Sources dans ~/lecube-sources/raw/
(téléchargées du Drive), sorties dans ~/lecube-sources/img/, puis copiées par build.py dans <discipline>/assets/img/
(dossier ignoré par git).
Étalonnage LE CUBE, noir et bronze, plus doux que celui des photos de salle vide pour garder des peaux naturelles :
exposition remontée (+18 %), couleur à 38 %, courbe en S, mi-tons tirés vers le bronze #B27639, vignette.
Sortie en 1188×2112 (10 % de marge pour le zoom lent).

Usage : ~/.venvs/hyperframes-audio/bin/python tools/photos.py [nom…]
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter, ImageOps

SRC = os.path.expanduser("~/lecube-sources/raw")
SORTIE = os.path.expanduser("~/lecube-sources/img")
L, H = 1188, 2112
BRONZE = np.array([0xB2, 0x76, 0x39]) / 255

# nom de sortie : (fichier source, centre x, centre y, zoom ≥ 1 sur la hauteur disponible)
PHOTOS = {
    # Pole dance : shooting pro du 12/11/2025 (Drive « PHOTOS POLE-1…8 ») et série pole noir et blanc de 2023 (fichier DSC01363)
    "pole-assis": ("PHOTOS POLE-1.jpg", 0.50, 0.42, 1.0),
    "pole-pont": ("PHOTOS POLE-2.jpg", 0.56, 0.52, 1.0),
    "pole-etirement": ("PHOTOS POLE-3.jpg", 0.395, 0.52, 1.0),
    "pole-equilibre": ("PHOTOS POLE-4.jpg", 0.50, 0.50, 1.0),
    "pole-dos": ("PHOTOS POLE-5.jpg", 0.40, 0.50, 1.0),
    "pole-grand-ecart": ("PHOTOS POLE-6.jpg", 0.50, 0.42, 1.0),
    "pole-drapeau": ("PHOTOS POLE-7.jpg", 0.50, 0.40, 1.0),
    "pole-nb": ("DSC01363.jpg", 0.50, 0.50, 1.0),
}


def recadrer(im, cx, cy, z):
    w, h = im.size
    if w / h > L / H:
        ch = h / z
        cw = ch * L / H
    else:
        cw = w / z
        ch = cw * H / L
    x0 = min(max(0, cx * w - cw / 2), w - cw)
    y0 = min(max(0, cy * h - ch / 2), h - ch)
    return im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((L, H), Image.LANCZOS)


def etalonner(im):
    x = np.asarray(im.convert("RGB")).astype(np.float64) / 255
    y = (0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2])[..., None]
    c = y + 0.38 * (x - y)                                   # couleur réduite
    c = np.clip(c * 1.18, 0, 1) ** 0.92                      # studio sous-exposé : on remonte l'exposition
    c = c * c * (3 - 2 * c) * 0.5 + c * 0.5                  # courbe en S douce
    yc = (0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2])[..., None]
    mi = 4 * yc * (1 - yc)
    c = c + 0.2 * mi * (BRONZE * (yc / 0.45) - c)            # mi-tons tirés vers le bronze
    c = c * np.array([1.0, 0.975, 0.94])                     # hautes lumières chaudes
    hh, ww = c.shape[:2]
    yy, xx = np.mgrid[0:hh, 0:ww]
    r = np.sqrt(((xx - ww / 2) / (ww / 2)) ** 2 + ((yy - hh / 2) / (hh / 2)) ** 2)
    c = c * (1 - 0.3 * np.clip(r - 0.55, 0, 1) ** 1.6)[..., None]
    out = Image.fromarray((np.clip(c, 0, 1) * 255 + 0.5).astype(np.uint8))
    return out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=45, threshold=2))


def main():
    os.makedirs(SORTIE, exist_ok=True)
    for nom, (f, cx, cy, z) in PHOTOS.items():
        if len(sys.argv) > 1 and nom not in sys.argv[1:]:
            continue
        im = etalonner(recadrer(ImageOps.exif_transpose(Image.open(os.path.join(SRC, f))), cx, cy, z))
        im.save(os.path.join(SORTIE, f"{nom}.jpg"), quality=86, optimize=True, progressive=True)
        print(f"{nom}.jpg ← {f}")


if __name__ == "__main__":
    main()
