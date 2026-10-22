"""Musique originale de la story fontaine LA SALLE : 20 s, 120 BPM, la mineur.

Instruments repris de lecube-chrono/tools/musique.py (synthèse pure, aucun échantillon, aucun morceau sous droits,
pas de MusicGen). Arrangement calé sur les repères de tools/build.py (SCENES, CASSURE) :
  accroche (0–2,5 s) : impact et crash à l'image 0, groove en demi-temps
  scènes 2 à 4 : groove à quatre temps, arpège en croches, une note pincée par boisson et par saveur qui entre,
                 impact quand « 30 MIN » frappe, montée avant la cassure
  volets : un souffle centré sur chaque coupe
  cassure (13,5–14 s) : silence, puis reprise sur « + 2 € » avec impact et crash
  carte finale : impact, accord tenu, fondu sur la dernière seconde

Fichier _communs/musique_fontaine.wav non suivi par git : graine fixe, on le régénère à l'identique.
Usage : ~/.venvs/hyperframes-audio/bin/python tools/musique.py [--bruitages]   (puis tools/build.py le recopie dans story-916)
--bruitages : volets, impacts et notes pincées seuls, −18 LUFS (_communs/bruitages_fontaine.wav).
(numpy, scipy, soundfile, pyloudnorm ; cible −14 LUFS intégrés, crête vraie ≤ −1,5 dBTP)
"""
import importlib.util
import os
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import fftconvolve

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import build  # noqa: E402  (repères)

_spec = importlib.util.spec_from_file_location(        # même nom de fichier que celui-ci : chargé par son chemin
    "musique_chrono", os.path.join(ICI, "..", "..", "lecube-chrono", "tools", "musique.py"))
m = importlib.util.module_from_spec(_spec)               # instruments, mise en place, limiteur (48 kHz)
_spec.loader.exec_module(m)

SR = m.SR
DUREE = build.DUREE
m.N = N = int(round(SR * DUREE))      # les instruments écrivent dans des pistes de 20 s
TEMPS = 0.5
DC = TEMPS / 4
CASS = build.CASSURE
DEBUT = {c: t for c, t, _ in build.SCENES}
COUPES = [t for _, t, _ in build.SCENES[1:]]

ACCORDS = [(0, "Am"), (2, "F"), (4, "C"), (6, "G"), (8, "Am"), (10, "F"), (12, "G"), (14, "Am"), (16, "F"), (18, "Am")]
NAPPE = {"Am": [57, 60, 64, 69], "F": [53, 57, 60, 65], "C": [55, 60, 64, 67], "G": [55, 59, 62, 67]}
BASSE = {"Am": 45, "F": 41, "C": 36, "G": 43}
ARPEGE = {"Am": [69, 72, 76, 81], "F": [65, 69, 72, 77], "C": [67, 72, 76, 79], "G": [67, 71, 74, 79]}


def accord(t):
    nom = ACCORDS[0][1]
    for t0, a in ACCORDS:
        if t >= t0 - 1e-9:
            nom = a
    return nom


def pincee(midi, d=0.42):
    """Corde pincée douce (comme lecube-disciplines) : deux sinus, attaque nette, longue décroissance."""
    t = m.tps(d)
    f = m.mtof(midi)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.05)
    return x * np.minimum(1, t / 0.003) * np.exp(-t / 0.16)


def silence(t):
    return CASS[0] - 1e-9 <= t < CASS[1] - 1e-9


def arranger(bruitages=False):
    bat, basse, pad, arp, fx = (m.stereo() for _ in range(5))
    GC, FR, CH = m.grosse_caisse(), m.frappe(), m.charley()
    fin = DUREE - 1.0
    coups = []
    for b in range(int(DUREE / TEMPS)):
        t = b * TEMPS
        if silence(t) or t >= fin:
            continue
        accroche = t < DEBUT["s2"]
        drop = t >= CASS[1]
        if accroche:
            if b % 4 == 0:
                m.poser(bat, t, GC, 0.75)
                coups.append(t)
            if b % 4 == 2:
                m.poser(bat, t, FR, 0.3, 0.05)
        else:
            m.poser(bat, t, GC, 0.8 if drop else 0.72)
            coups.append(t)
            if b % 2 == 1:
                m.poser(bat, t, FR, 0.36 if drop else 0.3, 0.05)
            m.poser(bat, t + TEMPS / 2, CH, 0.18, 0.25)
            if drop:
                for k in (1, 3):
                    m.poser(bat, t + k * DC, CH, 0.07, -0.3)
        r = BASSE[accord(t)]
        m.poser(basse, t, m.note_basse(r, 0.42 if not accroche else 0.9), 0.45 if not accroche or b % 2 == 0 else 0)
        if t >= 0.5:
            notes = ARPEGE[accord(t)]
            for k in range(2):
                m.poser(arp, t + k * TEMPS / 2, pincee(notes[(b * 2 + k) % 4] + (12 if drop else 0)), 0.15, 0.35 * (-1) ** k)

    for i, (t0, nom) in enumerate(ACCORDS):
        t1 = ACCORDS[i + 1][0] if i + 1 < len(ACCORDS) else DUREE
        if t0 < CASS[0] < t1:
            t1 = CASS[0]
        if t0 >= CASS[0] and t0 < CASS[1]:
            t0 = CASS[1]
        m.poser(pad, t0, m.nappe(NAPPE[nom], t1 - t0 + 0.2), 1.1 if t0 < CASS[1] else 1.3)

    # Repères de l'image
    m.poser(fx, 0.0, m.impact(0.9), 0.55)
    m.poser(fx, 0.0, m.crash(1.2), 0.3)
    for t in COUPES:                                       # volets
        m.poser(fx, t - 0.25, m.souffle(0.5, 0.25), 0.34)
        if t != CASS[0]:
            m.poser(fx, t, m.impact(0.5), 0.3)
    s2, s3, s4, s5 = DEBUT["s2"], DEBUT["s3"], DEBUT["s4"], DEBUT["s5"]
    for i in range(6):                                     # puces des boissons
        m.poser(fx, s2 + 2.05 + 0.14 * i, pincee(81 + [0, 3, 7, 12, 7, 3][i], 0.3), 0.22, 0.4 * (-1) ** i)
    for i in range(5):                                     # saveurs
        m.poser(fx, s3 + 0.6 + 0.22 * i, pincee(76 + [0, 3, 5, 7, 12][i], 0.35), 0.24, 0.3 * (-1) ** i)
    m.poser(fx, s4 + 0.95, m.impact(0.8), 0.5)             # « 30 MIN »
    m.poser(fx, s4 + 0.95, FR, 0.3)
    m.poser(fx, CASS[0] - 1.0, m.monte(1.0), 0.38)
    m.poser(fx, CASS[1], m.impact(1.0), 0.7)               # « + 2 € »
    m.poser(fx, CASS[1], m.crash(1.6), 0.45)
    for i in range(3):                                     # bandes des avantages
        m.poser(fx, s5 + 1.2 + 0.2 * i - 0.08, m.souffle(0.22, 0.1), 0.2)
    m.poser(fx, DEBUT["s6"] + 0.35, m.impact(0.6), 0.35)   # « À L'ACCUEIL. »
    m.poser(fx, fin, m.crash(0.8), 0.25)

    respire = np.ones(N)
    for tc in coups:
        i = int(tc * SR)
        n = min(N - i, int(0.24 * SR))
        respire[i:i + n] = np.minimum(respire[i:i + n], 1 - 0.5 * np.exp(-np.arange(n) / SR / 0.08))
    for buf in (basse, pad, arp):
        buf *= respire
    if bruitages:                                          # version « bruitages seuls » : musique ajoutée à la publication
        for buf in (bat, basse, pad, arp):
            buf[:] = 0

    ri_t = m.tps(1.4)
    ri = np.vstack([m.rng.standard_normal(len(ri_t)), m.rng.standard_normal(len(ri_t))]) * np.exp(-ri_t / 0.35)
    ri = np.vstack([m.filtre(ri[0], "lowpass", 6000), m.filtre(ri[1], "lowpass", 6000)])
    ri /= np.sqrt((ri ** 2).sum(axis=1, keepdims=True))
    envoi = pad * 0.3 + arp * 0.4 + fx * 0.25 + bat * 0.05
    rev = np.vstack([fftconvolve(envoi[k], ri[k])[:N] for k in range(2)])

    mix = bat * 0.9 + basse * 0.7 + pad * 1.1 + arp * 0.9 + fx * 0.9 + rev * 0.55
    mix = np.vstack([m.filtre(mix[k], "highpass", 32) for k in range(2)])
    fondu = np.ones(N)
    i0 = int((DUREE - 1.0) * SR)
    fondu[i0:] = np.linspace(1, 0, N - i0) ** 1.5
    return mix * fondu


def main():
    bruitages = "--bruitages" in sys.argv
    cible = -18.0 if bruitages else -14.0              # bruitages seuls : laissés sous la musique ajoutée dans Instagram
    x = arranger(bruitages)
    mesure = pyln.Meter(SR)
    for _ in range(4):
        x *= 10 ** ((cible - mesure.integrated_loudness(x.T)) / 20)
        x = m.limiteur(x)
        if abs(mesure.integrated_loudness(x.T) - cible) < 0.15:
            break
    tp = m.crete_vraie(x)
    if tp > -1.6:
        x *= 10 ** ((-1.6 - tp) / 20)
    sortie = os.path.join(ICI, "..", "_communs", "bruitages_fontaine.wav" if bruitages else "musique_fontaine.wav")
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    sf.write(sortie, x.T, SR, subtype="PCM_24")
    print(f"{os.path.normpath(sortie)} : {x.shape[1] / SR:.3f} s · {mesure.integrated_loudness(x.T):.1f} LUFS · "
          f"crête vraie {m.crete_vraie(x):.2f} dBTP")


if __name__ == "__main__":
    main()
