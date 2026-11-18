"""Musique originale des stories « carte cadeau » LA SALLE : 12 s, 120 BPM, la mineur, commune aux trois accroches.

Synthèse pure, graine fixe, aucun échantillon, aucun morceau sous droits, pas de MusicGen. Instruments repris de
lecube-chrono/tools/musique.py (batterie, basse, nappe, impacts) ; corde pincée et carillon comme
lasalle-visbody/tools/musique.py. Touche de Noël : des grelots synthétisés (bruit filtré et partiels aigus) en
croches sur l'accroche et sur la carte finale. Calée sur les repères de tools/build.py :
  0 s        impact et crash à l'image 0, groove à quatre temps
  2 s        coupe : impact court ; montants 100 → 150 → 200 → 300 → au choix : une note pincée qui monte à chaque fois
  étapes     un souffle doux par étape (01, 02, 03)
  6–6,5 s    montée, puis 6,5–7 s cassure : musique coupée sous « ET EN PLUS, »
  7 s        reprise ; la barre or sur « 45 € » : souffle ; « OFFERTS. » : impact, crash et carillon
  9 s        carte finale : impact, grelots ; « À L'ACCUEIL. » : impact ; fondu sur la dernière demi-seconde

Usage : python3 tools/musique.py [--bruitages]
Écrit _communs/musique_carte_cadeau.wav (−14 LUFS, crête vraie ≤ −2,4 dBTP avant AAC) ou, avec --bruitages,
_communs/bruitages_carte_cadeau.wav (−18 LUFS, sans batterie, basse, nappe ni arpège). Fichiers non suivis par git :
graine fixe, on les régénère à l'identique.
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

_spec = importlib.util.spec_from_file_location(
    "musique_chrono", os.path.join(ICI, "..", "..", "lecube-chrono", "tools", "musique.py"))
m = importlib.util.module_from_spec(_spec)               # instruments, mise en place, limiteur (48 kHz)
_spec.loader.exec_module(m)

SR = m.SR
DUREE = build.DUREE
m.N = N = int(round(SR * DUREE))
TEMPS, DC = 0.5, 0.125
CASS = build.CASSURE
T = build.T
ACCORDS = ["Am", "F", "C", "G"]                          # une mesure de 2 s par accord, la mineur sur la fin
NAPPE = {"Am": [57, 60, 64, 69], "F": [53, 57, 60, 65], "C": [55, 60, 64, 67], "G": [55, 59, 62, 67]}
BASSE = {"Am": 45, "F": 41, "C": 36, "G": 43}
ARPEGE = {"Am": [69, 72, 76, 81], "F": [65, 69, 72, 77], "C": [67, 72, 76, 79], "G": [67, 71, 74, 79]}


def accord(t):
    return ACCORDS[int(t // 2) % 4] if t < DUREE - 2 else "Am"


def pincee(midi, d=0.42):
    """Corde pincée douce : deux sinus, attaque nette, longue décroissance."""
    t = m.tps(d)
    f = m.mtof(midi)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.05)
    return x * np.minimum(1, t / 0.003) * np.exp(-t / 0.16)


def carillon():
    """Deux notes cristallines (mi, puis la)."""
    t = m.tps(0.9)
    x = np.sin(2 * np.pi * 1318.5 * t) * np.exp(-t / 0.25)
    t2 = m.tps(0.78)
    y = np.zeros_like(x)
    y[int(0.12 * SR):int(0.12 * SR) + len(t2)] = (np.sin(2 * np.pi * 1760 * t2) + 0.3 * np.sin(2 * np.pi * 3520 * t2)) * np.exp(-t2 / 0.3)
    return (x + y) * np.minimum(1, np.arange(len(x)) / SR / 0.003)


def grelot(d=0.16):
    """Grelot synthétisé : bruit très aigu et quelques partiels inharmoniques, décroissance rapide."""
    t = m.tps(d)
    bruit = m.filtre(m.rng.standard_normal(len(t)), "highpass", 7000) * np.exp(-t / 0.03)
    cloche = sum(a * np.sin(2 * np.pi * f * t) for f, a in ((4200, 0.5), (5650, 0.35), (7300, 0.25))) * np.exp(-t / 0.05)
    return (bruit * 0.6 + cloche * 0.4) * np.minimum(1, t / 0.001)


def arranger(bruitages=False):
    bat, basse, pad, arp, fx, gre = (m.stereo() for _ in range(6))
    GC, FR, CH = m.grosse_caisse(), m.frappe(), m.charley()
    fin = DUREE - 0.5
    coups = []
    for b in range(int(DUREE / TEMPS)):
        t = b * TEMPS
        if CASS[0] - 1e-9 <= t < CASS[1] - 1e-9 or t >= fin:
            continue
        m.poser(bat, t, GC, 0.8)
        coups.append(t)
        if b % 2 == 1:
            m.poser(bat, t, FR, 0.36, 0.05)
        for k in (1, 2, 3):
            m.poser(bat, t + k * DC, CH, 0.18 if k == 2 else 0.07, 0.25 if k == 2 else -0.3)
        m.poser(basse, t, m.note_basse(BASSE[accord(t)], 0.42), 0.45)
        notes = ARPEGE[accord(t)]
        for k in range(2):
            m.poser(arp, t + k * TEMPS / 2, pincee(notes[(b * 2 + k) % 4] + 12, 0.35), 0.11, 0.35 * (-1) ** k)
    t0 = 0.0
    while t0 < DUREE:
        t1 = min(DUREE, t0 + 2.0)
        if t0 < CASS[0] < t1:
            m.poser(pad, t0, m.nappe(NAPPE[accord(t0)], CASS[0] - t0 + 0.1), 1.1)
            m.poser(pad, CASS[1], m.nappe(NAPPE[accord(CASS[1])], t1 - CASS[1] + 0.2), 1.2)
        else:
            m.poser(pad, t0, m.nappe(NAPPE[accord(t0)], t1 - t0 + 0.2), 1.1)
        t0 = t1
    # Grelots en croches : l'accroche (0–2 s) et la carte finale (9 s jusqu'au fondu)
    for debut, arret in ((0.0, 2.0), (9.0, fin)):
        t = debut
        while t < arret - 1e-9:
            m.poser(gre, t, grelot(), 0.5 if (t * 4) % 2 < 1e-6 else 0.3, 0.4 * (-1) ** int(t * 4))
            t += TEMPS / 2

    # Repères de l'image
    m.poser(fx, 0.0, m.impact(0.9), 0.55)
    m.poser(fx, 0.0, m.crash(1.2), 0.3)
    for debut in (2.0, 9.0):                              # coupes franches
        m.poser(fx, debut, m.impact(0.5), 0.3)
        m.poser(fx, debut - 0.12, m.souffle(0.2, 0.1), 0.15)
    for i, t in enumerate(T["montants"]):                 # 150, 200, 300, au choix : la note monte
        m.poser(fx, t, pincee(76 + [0, 3, 7, 12][i], 0.4), 0.3, 0.3 * (-1) ** i)
        m.poser(fx, t, m.impact(0.25), 0.12)
    for t in (T["etape1"], T["etape2"], T["etape3"]):
        m.poser(fx, t - 0.05, m.souffle(0.25, 0.1), 0.16)
    m.poser(fx, CASS[0] - 0.5, m.monte(0.5), 0.3)         # montée vers la cassure
    m.poser(fx, CASS[1], m.impact(0.8), 0.5)              # reprise
    m.poser(fx, T["barre"] - 0.05, m.souffle(0.3, 0.12), 0.25)
    m.poser(fx, T["offerts"], m.impact(1.0), 0.7)         # « OFFERTS. »
    m.poser(fx, T["offerts"], m.crash(1.3), 0.4)
    m.poser(fx, T["offerts"] + 0.05, carillon(), 0.22)
    m.poser(fx, T["accueil"], m.impact(0.6), 0.35)        # « À L'ACCUEIL. »
    m.poser(fx, fin, m.crash(0.6), 0.2)

    respire = np.ones(N)
    for tc in coups:
        i = int(tc * SR)
        n = min(N - i, int(0.22 * SR))
        respire[i:i + n] = np.minimum(respire[i:i + n], 1 - 0.5 * np.exp(-np.arange(n) / SR / 0.07))
    for buf in (basse, pad, arp):
        buf *= respire
    if bruitages:
        for buf in (bat, basse, pad, arp, gre):
            buf[:] = 0
    ri_t = m.tps(1.2)
    ri = np.vstack([m.rng.standard_normal(len(ri_t)), m.rng.standard_normal(len(ri_t))]) * np.exp(-ri_t / 0.3)
    ri = np.vstack([m.filtre(ri[0], "lowpass", 6000), m.filtre(ri[1], "lowpass", 6000)])
    ri /= np.sqrt((ri ** 2).sum(axis=1, keepdims=True))
    envoi = pad * 0.3 + arp * 0.4 + fx * 0.25 + gre * 0.3 + bat * 0.05
    rev = np.vstack([fftconvolve(envoi[k], ri[k])[:N] for k in range(2)])
    mix = bat * 0.9 + basse * 0.7 + pad * 1.0 + arp * 0.9 + fx * 0.9 + gre * 0.55 + rev * 0.5
    mix = np.vstack([m.filtre(mix[k], "highpass", 32) for k in range(2)])
    fondu = np.ones(N)
    i0 = int((DUREE - 0.5) * SR)
    fondu[i0:] = np.linspace(1, 0, N - i0) ** 1.5
    return mix * fondu


def main():
    bruitages = "--bruitages" in sys.argv
    cible, plafond = (-18.0, -3.6) if bruitages else (-14.0, -2.4)   # chocs brefs : l'AAC fait déborder la crête
    mesure = pyln.Meter(SR)
    x = arranger(bruitages)
    for _ in range(6):
        x *= 10 ** ((cible - mesure.integrated_loudness(x.T)) / 20)
        x = m.limiteur(x, plafond)
        if abs(mesure.integrated_loudness(x.T) - cible) < 0.15:
            break
    tp = m.crete_vraie(x)
    if tp > plafond + 0.3:
        x *= 10 ** ((plafond + 0.3 - tp) / 20)
    os.makedirs(os.path.join(ICI, "..", "_communs"), exist_ok=True)
    sortie = os.path.join(ICI, "..", "_communs", f"{'bruitages' if bruitages else 'musique'}_carte_cadeau.wav")
    sf.write(sortie, x.T, SR, subtype="PCM_24")
    print(f"{os.path.normpath(sortie)} : {x.shape[1] / SR:.3f} s · {mesure.integrated_loudness(x.T):.1f} LUFS · "
          f"crête vraie {m.crete_vraie(x):.2f} dBTP")


if __name__ == "__main__":
    main()
