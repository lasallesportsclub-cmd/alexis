"""Musique des stories courtes du lancement Visbody (A : 12 s, B : 10 s), 120 BPM, la mineur.

Mêmes instruments que tools/musique.py (synthèse pure, graine fixe, pas de MusicGen), arrangement plus serré :
groove à quatre temps dès l'image 0, impact à chaque coupe, quart de temps de silence avant « IA. » qui frappe avec
un crash, une note pincée par résultat, sons du scan sur l'avatar (A), « + 2 € » sur un impact, accord tenu et fondu
sur la dernière demi-seconde. Repères : tools/courtes.py (HISTOIRES).

Usage : ~/.venvs/hyperframes-audio/bin/python -I tools/musique_courtes.py [--bruitages]
Écrit _communs/{musique,bruitages}_visbody_courte_{A,B}.wav (non suivis par git ; −14 LUFS, bruitages −18 LUFS).
"""
import os
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import fftconvolve

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import courtes  # noqa: E402
import musique as mu  # noqa: E402  (instruments de la story longue et de lecube-chrono)

m, SR = mu.m, mu.SR
TEMPS, DC = 0.5, 0.125
ACCORDS = ["Am", "F", "C", "G"]                      # une mesure de 2 s par accord


def arranger(cle, bruitages=False):
    h = courtes.HISTOIRES[cle]
    duree = h["duree"]
    m.N = N = int(round(SR * duree))
    bat, basse, pad, arp, fx = (m.stereo() for _ in range(5))
    GC, FR, CH = m.grosse_caisse(), m.frappe(), m.charley()
    cass = h["cassure"]
    fin = duree - 0.5
    scan = None
    if "scan" in h:                                  # batterie allégée pendant le passage du scan (A)
        s = h["scan"]
        scan = (s["descente"][0] - 0.05, s["remontee"][0] + s["remontee"][1])
    accord = lambda t: ACCORDS[int(t // 2) % 4] if t < duree - 2 else "Am"
    coups = []
    for b in range(int(duree / TEMPS)):
        t = b * TEMPS
        if cass[0] - 1e-9 <= t < cass[1] - 1e-9 or t >= fin:
            continue
        calme = scan is not None and scan[0] <= t < scan[1]
        m.poser(bat, t, GC, 0.55 if calme else 0.8)
        coups.append(t)
        if not calme:
            if b % 2 == 1:
                m.poser(bat, t, FR, 0.36, 0.05)
            for k in (1, 2, 3):
                m.poser(bat, t + k * DC, CH, 0.18 if k == 2 else 0.07, 0.25 if k == 2 else -0.3)
        m.poser(basse, t, m.note_basse(mu.BASSE[accord(t)], 0.42), 0.45)
        notes = mu.ARPEGE[accord(t)]
        for k in range(2):
            m.poser(arp, t + k * TEMPS / 2, mu.pincee(notes[(b * 2 + k) % 4] + 12, 0.35), 0.11, 0.35 * (-1) ** k)
    t0 = 0.0
    while t0 < duree:
        t1 = min(duree, t0 + 2.0)
        if t0 < cass[0] < t1:
            m.poser(pad, t0, m.nappe(mu.NAPPE[accord(t0)], cass[0] - t0 + 0.1), 1.1)
            m.poser(pad, cass[1], m.nappe(mu.NAPPE[accord(cass[1])], t1 - cass[1] + 0.2), 1.2)
        else:
            m.poser(pad, t0, m.nappe(mu.NAPPE[accord(t0)], t1 - t0 + 0.2), 1.1)
        t0 = t1

    # Repères de l'image
    m.poser(fx, 0.0, m.impact(0.9), 0.55)
    m.poser(fx, 0.0, m.crash(1.2), 0.3)
    for _, debut, _ in h["scenes"][1:]:              # coupes franches : impact court et souffle (sauf sous « + 2 € »)
        if abs(debut - cass[0]) > 1e-6 and not 0 <= h["prix"] - debut < 0.3:
            m.poser(fx, debut, m.impact(0.4), 0.25)
            m.poser(fx, debut - 0.12, m.souffle(0.2, 0.1), 0.15)
    m.poser(fx, cass[0] - 0.5, m.monte(0.5), 0.3)
    m.poser(fx, h["ia"], m.impact(1.0), 0.7)          # « IA. »
    m.poser(fx, h["ia"], m.crash(1.4), 0.45)
    for i, t in enumerate(h["resultats"]):           # les 5 résultats
        m.poser(fx, t, mu.pincee(76 + [0, 3, 5, 7, 12][i], 0.35), 0.26, 0.3 * (-1) ** i)
    if "scan" in h:
        s = h["scan"]
        m.poser(fx, s["plateau"][0], m.impact(0.35), 0.22)
        m.poser(fx, s["montee"][0], mu.apparition(s["montee"][1]), 0.3)
        for (t, d), f0, f1 in ((s["descente"], 900, 300), (s["remontee"], 300, 900)):
            m.poser(fx, t, mu.faisceau(d, f0, f1), 0.3)
            m.poser(fx, t, mu.donnees(d), 0.08, 0.25)
        m.poser(fx, s["remontee"][0] + s["remontee"][1], mu.carillon(), 0.2)
    if "plaque" in h:
        m.poser(fx, h["plaque"], m.souffle(0.25, 0.1), 0.2)
    m.poser(fx, h["prix"], m.impact(1.0), 0.65)       # « + 2 € »
    m.poser(fx, h["prix"], m.crash(1.2), 0.35)
    m.poser(fx, h["accueil"], m.impact(0.6), 0.35)    # « À L'ACCUEIL. »
    m.poser(fx, fin, m.crash(0.6), 0.2)

    respire = np.ones(N)
    for tc in coups:
        i = int(tc * SR)
        n = min(N - i, int(0.22 * SR))
        respire[i:i + n] = np.minimum(respire[i:i + n], 1 - 0.5 * np.exp(-np.arange(n) / SR / 0.07))
    for buf in (basse, pad, arp):
        buf *= respire
    if bruitages:
        for buf in (bat, basse, pad, arp):
            buf[:] = 0
    ri_t = m.tps(1.2)
    ri = np.vstack([m.rng.standard_normal(len(ri_t)), m.rng.standard_normal(len(ri_t))]) * np.exp(-ri_t / 0.3)
    ri = np.vstack([m.filtre(ri[0], "lowpass", 6000), m.filtre(ri[1], "lowpass", 6000)])
    ri /= np.sqrt((ri ** 2).sum(axis=1, keepdims=True))
    envoi = pad * 0.3 + arp * 0.4 + fx * 0.25 + bat * 0.05
    rev = np.vstack([fftconvolve(envoi[k], ri[k])[:N] for k in range(2)])
    mix = bat * 0.9 + basse * 0.7 + pad * 1.0 + arp * 0.9 + fx * 0.9 + rev * 0.5
    mix = np.vstack([m.filtre(mix[k], "highpass", 32) for k in range(2)])
    fondu = np.ones(N)
    i0 = int((duree - 0.5) * SR)
    fondu[i0:] = np.linspace(1, 0, N - i0) ** 1.5
    return mix * fondu


def main():
    bruitages = "--bruitages" in sys.argv
    cible, plafond = (-18.0, -3.6) if bruitages else (-14.0, -2.4)   # chocs brefs : l'AAC fait déborder la crête
    mesure = pyln.Meter(SR)
    for cle in courtes.HISTOIRES:
        x = arranger(cle, bruitages)
        for _ in range(6):
            x *= 10 ** ((cible - mesure.integrated_loudness(x.T)) / 20)
            x = m.limiteur(x, plafond)
            if abs(mesure.integrated_loudness(x.T) - cible) < 0.15:
                break
        tp = m.crete_vraie(x)
        if tp > plafond + 0.3:
            x *= 10 ** ((plafond + 0.3 - tp) / 20)
        sortie = os.path.join(ICI, "..", "_communs", f"{'bruitages' if bruitages else 'musique'}_visbody_courte_{cle}.wav")
        sf.write(sortie, x.T, SR, subtype="PCM_24")
        print(f"{os.path.normpath(sortie)} : {x.shape[1] / SR:.3f} s · {mesure.integrated_loudness(x.T):.1f} LUFS · "
              f"crête vraie {m.crete_vraie(x):.2f} dBTP")


if __name__ == "__main__":
    main()
