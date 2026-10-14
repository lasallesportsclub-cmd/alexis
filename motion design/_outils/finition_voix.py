"""Finition d'une réplique générée (Chatterbox ou autre) avant montage.

Corrige les défauts typiques de la synthèse :
  - débris en fin de fichier (bruit isolé, à plus de 20 dB sous la crête, après un silence) : supprimés ;
  - silences de début et de fin : ramenés à 0,08 s ;
  - pauses internes de plus de 0,45 s : ramenées à 0,35 s ;
  - fondu d'entrée 15 ms et de sortie 40 ms (pas de clic à la coupe).
Usage : python finition_voix.py entree.wav [-o sortie.wav]   (par défaut : réécrit le fichier)
Seuils mesurés sur les essais du 14/10/2026 (posé 3 : pause de 1,77 s ; posé 4 : débris à −40 dB en fin).
"""
import argparse

import numpy as np
import soundfile as sf

PAS = 0.01          # résolution de l'enveloppe (s)
SEUIL = 40          # dB sous la crête de l'enveloppe = silence
PAUSE_MAX, PAUSE_CIBLE = 0.45, 0.35
MARGE = 0.08


def enveloppe(x, sr):
    hop, win = int(PAS * sr), int(0.03 * sr)
    e = np.array([np.sqrt(np.mean(x[i:i + win] ** 2) + 1e-12) for i in range(0, max(1, len(x) - win), hop)])
    return 20 * np.log10(e)


def zones_sonores(db, seuil):
    """Liste de (début, fin) en trames, pour les passages au-dessus du seuil."""
    actif = db > seuil
    zones, debut = [], None
    for i, a in enumerate(actif):
        if a and debut is None:
            debut = i
        elif not a and debut is not None:
            zones.append([debut, i])
            debut = None
    if debut is not None:
        zones.append([debut, len(actif)])
    return zones


def finir(x, sr):
    if x.ndim > 1:
        x = x.mean(axis=1)
    db = enveloppe(x, sr)
    crete = db.max()
    zones = zones_sonores(db, crete - SEUIL)
    if not zones:
        return x
    # débris final : dernière zone courte (< 0,25 s), séparée par ≥ 0,12 s, et à plus de 20 dB sous la crête
    while len(zones) > 1:
        d, f = zones[-1]
        if (f - d) * PAS < 0.25 and (d - zones[-2][1]) * PAS >= 0.12 and db[d:f].max() < crete - 20:
            zones.pop()
        else:
            break
    h = int(PAS * sr)
    morceaux, marge = [], int(MARGE * sr)
    debut = max(0, zones[0][0] * h - marge)
    for k, (d, f) in enumerate(zones):
        fin_zone = min(len(x), f * h + int(0.03 * sr))
        if k + 1 < len(zones):
            pause = (zones[k + 1][0] - f) * PAS
            if pause > PAUSE_MAX:
                morceaux.append(x[debut:fin_zone])
                morceaux.append(np.zeros(int(PAUSE_CIBLE * sr) - int(0.06 * sr)))
                debut = zones[k + 1][0] * h - int(0.03 * sr)  # 30 ms avant la reprise : l'attaque n'est pas rognée
        else:
            morceaux.append(x[debut:min(len(x), fin_zone + marge)])
    y = np.concatenate(morceaux)
    fi, fo = int(0.015 * sr), int(0.04 * sr)
    y[:fi] *= np.linspace(0, 1, fi)
    y[-fo:] *= np.linspace(1, 0, fo)
    return y


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entree")
    ap.add_argument("-o", "--sortie")
    a = ap.parse_args()
    x, sr = sf.read(a.entree)
    y = finir(x, sr)
    sf.write(a.sortie or a.entree, y, sr, subtype="PCM_16")
    print(f"{a.sortie or a.entree} : {len(x) / sr:.2f} s → {len(y) / sr:.2f} s")


if __name__ == "__main__":
    main()
