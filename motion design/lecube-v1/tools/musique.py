"""Musique originale de la pub LE CUBE tirée du film V1 : 15 s, 120 BPM, mi mineur, une par variante d'accroche.

Arrangement des pubs par discipline (../lecube-disciplines/tools/musique.py : synthèse pure, aucun morceau sous droits,
pas de MusicGen), calé sur tools/cues_v1.json, la même feuille que les compositions. En plus, parce qu'ici les images
coupent plus souvent : un souffle court à chaque coupe à l'intérieur d'une étape et de l'argument (bibliothèque
Pixabay de media-use, usage commercial sans attribution) et un impact grave sur « ET TOI ? ».

Fichiers _communs/musique_v1_<V>.wav non suivis par git : graine fixe, on les régénère à l'identique.
Usage : ~/.venvs/hyperframes-audio/bin/python tools/musique.py [A B C]
(numpy, scipy, soundfile, pyloudnorm ; cible −14 LUFS intégrés, crête vraie ≤ −1,5 dBTP)
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

ICI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.normpath(os.path.join(ICI, "..", ".."))
SFX = os.path.normpath(os.path.join(MOTION, "..", ".claude", "skills", "media-use", "audio", "assets", "sfx"))

_spec = importlib.util.spec_from_file_location("musique_disciplines", os.path.join(MOTION, "lecube-disciplines", "tools", "musique.py"))
MD = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(MD)
m, SR, N = MD.m, MD.SR, MD.N


def son(nom):
    """Effet de la bibliothèque Pixabay, décodé en 48 kHz stéréo."""
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "x.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(SFX, f"{nom}.mp3"), "-ar", str(SR), "-ac", "2", wav], check=True)
        x, _ = sf.read(wav, always_2d=True)
    return x.T / max(1e-9, np.abs(x).max())


def coupes(C):
    """Instants des coupes qui ne tombent pas déjà sur une étape : plans à l'intérieur des étapes et de l'argument."""
    t = []
    for e in C["etapes"]:
        u = e["t"]
        for p in e["plans"][:-1]:
            u += p["d"]
            t.append(u)
    t += [s["t"] for s in C["argument"]["segments"][1:]]
    return sorted(t)


def arranger(C, v):
    mix = MD.arranger(C, v)
    fx = m.stereo()
    whoosh = son("whoosh-short")
    for k, t in enumerate(coupes(C)):
        m.poser(fx, t - 0.12, whoosh, 0.22, 0.3 * (-1) ** k)
    m.poser(fx, C["cassure"][0], son("impact-bass-1"), 0.5)
    return mix + fx


def ecrire(C, v):
    x = arranger(C, v)
    mesure = pyln.Meter(SR)
    for _ in range(4):
        x *= 10 ** ((-14.0 - mesure.integrated_loudness(x.T)) / 20)
        x = m.limiteur(x)
        if abs(mesure.integrated_loudness(x.T) + 14.0) < 0.15:
            break
    tp = m.crete_vraie(x)
    if tp > -1.6:
        x *= 10 ** ((-1.6 - tp) / 20)
    sortie = os.path.normpath(os.path.join(ICI, "..", "_communs", f"musique_v1_{v}.wav"))
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    sf.write(sortie, x.T, SR, subtype="PCM_24")
    print(f"{sortie} : {x.shape[1] / SR:.3f} s · {mesure.integrated_loudness(x.T):.1f} LUFS · crête vraie {m.crete_vraie(x):.2f} dBTP")


def main():
    C = json.load(open(os.path.join(ICI, "cues_v1.json"), encoding="utf-8"))
    assert abs(C["duree"] - N / SR) < 1e-6
    for v in sys.argv[1:] or list(C["accroches"]):
        ecrire(C, v)


if __name__ == "__main__":
    main()
