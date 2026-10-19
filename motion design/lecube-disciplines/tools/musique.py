"""Musique originale d'une pub LE CUBE par discipline : 15 s, 120 BPM, mi mineur.

Instruments repris de lecube-chrono/tools/musique.py (synthèse pure, aucun échantillon, aucun morceau sous droits,
pas de MusicGen). Arrangement propre aux pubs par discipline :
  accroche : un impact et une frappe sur chacun des quatre mots, groove en demi-temps, souffle puis impact à « barre »
  étapes : groove qui s'installe (grosse caisse aux temps 1 et 3, claquement au 3), arpège en croches, un glissé
           et un impact à chaque étape, montée avant la cassure
  cassure : un demi-temps de silence (« ET TOI ? »), puis reprise à quatre temps avec impact et crash
  carte : impact à la carte et à l'appel à l'action, fondu final
Instants : tools/cues_<discipline>.json, la même feuille que les compositions.

Usage : ~/.venvs/hyperframes-audio/bin/python tools/musique.py pole
(numpy, scipy, soundfile, pyloudnorm ; cible −14 LUFS intégrés, crête vraie ≤ −1,5 dBTP)
"""
import json
import os
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import fftconvolve

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(ICI, "..", "..", "lecube-chrono", "tools")))
import musique as m  # noqa: E402  (instruments, mise en place, limiteur : même durée de 15 s, même 48 kHz)

SR, N = m.SR, m.N
TEMPS = 0.5
DC = TEMPS / 4
ACCORDS = [(0.0, "Em"), (2.0, "Em"), (4.0, "C"), (6.0, "D"), (9.0, "Em"), (11.0, "C"), (13.0, "Em")]
ARPEGE = {"Em": [64, 67, 71, 74], "C": [60, 64, 67, 71], "D": [62, 66, 69, 72]}


def accord(t):
    nom = ACCORDS[0][1]
    for t0, a in ACCORDS:
        if t >= t0 - 1e-9:
            nom = a
    return nom


def pincee(midi, d=0.42):
    """Corde pincée douce : deux sinus, attaque nette, longue décroissance."""
    t = m.tps(d)
    f = m.mtof(midi)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.05)
    return x * np.minimum(1, t / 0.003) * np.exp(-t / 0.16)


def arranger(C):
    cass, fin = C["cassure"], C["fin"]
    bat, basse, pad, arp, fx = (m.stereo() for _ in range(5))
    GC, FR, CH = m.grosse_caisse(), m.frappe(), m.charley()
    coups = []
    for b in range(int(C["duree"] / TEMPS)):
        t = b * TEMPS
        if cass[0] - 1e-9 <= t < cass[1] - 1e-9 or t >= fin - 1e-9:
            continue
        apres = t >= cass[1]
        debut = t < C["etapes"][0]["t"]
        if apres or b % 2 == 0:                       # demi-temps avant la cassure, quatre temps après
            if not (debut and b % 4 == 2):
                poser_gc = 0.8 if apres else 0.75
                m.poser(bat, t, GC, poser_gc)
                coups.append(t)
        if b % 4 == 2 or (apres and b % 2 == 1):
            m.poser(bat, t, FR, 0.36, 0.05)
        if not debut:
            m.poser(bat, t + TEMPS / 2, CH, 0.18, 0.25)
            if apres:
                for k in (1, 3):
                    m.poser(bat, t + k * DC, CH, 0.07, -0.3)
        r = m.BASSE[accord(t)]
        if b % 2 == 0:
            m.poser(basse, t, m.note_basse(r, 0.9 if not apres else 0.42), 0.45)
        if apres and b % 2 == 1:
            m.poser(basse, t, m.note_basse(r + 12, 0.2), 0.25)
        if not debut:
            notes = ARPEGE[accord(t)]
            for k in range(2):
                m.poser(arp, t + k * TEMPS / 2, pincee(notes[(b * 2 + k) % 4] + (12 if apres else 0)), 0.16, 0.35 * (-1) ** k)

    for i, (t0, nom) in enumerate(ACCORDS):
        t1 = ACCORDS[i + 1][0] if i + 1 < len(ACCORDS) else fin
        t1 = min(t1, cass[0]) if t0 < cass[0] else t1
        m.poser(pad, t0, m.nappe(m.NAPPE[nom], t1 - t0 + 0.2), 1.1 if t0 < 9 else 1.3)

    a = C["accroche"]
    for k, (t, _, _) in enumerate(a["mots"]):          # un coup par mot
        m.poser(fx, t, m.impact(0.9 if k == 0 else 0.6), 0.6 if k == 0 else 0.42)
        m.poser(fx, t, FR, 0.3, 0.1 * (-1) ** k)
    m.poser(fx, 0.0, m.crash(1.2), 0.3)
    m.poser(fx, a["tout"] - 0.2, m.souffle(0.26, 0.2), 0.32)
    m.poser(fx, a["barre"], m.impact(0.8), 0.5)
    for e in C["etapes"]:
        m.poser(fx, e["t"] - 0.18, m.souffle(0.24, 0.16), 0.3)
        m.poser(fx, e["t"], m.impact(0.6), 0.4)
    m.poser(fx, cass[0] - 1.0, m.monte(1.0), 0.4)
    m.poser(fx, cass[1], m.impact(1.0), 0.7)
    m.poser(fx, cass[1], m.crash(1.6), 0.45)
    m.poser(fx, C["argument"]["deuxieme"], m.impact(0.6), 0.35)
    m.poser(fx, C["carte"] - 0.3, m.souffle(0.5, 0.3), 0.4)
    m.poser(fx, C["carte"], m.impact(0.9), 0.55)
    m.poser(fx, C["cta"], m.impact(0.6), 0.4)
    m.poser(fx, fin, m.crash(0.5), 0.3)

    respire = np.ones(N)
    for tc in coups:
        i = int(tc * SR)
        n = min(N - i, int(0.24 * SR))
        respire[i:i + n] = np.minimum(respire[i:i + n], 1 - 0.5 * np.exp(-np.arange(n) / SR / 0.08))
    for buf in (basse, pad, arp):
        buf *= respire

    ri_t = m.tps(1.4)
    ri = np.vstack([m.rng.standard_normal(len(ri_t)), m.rng.standard_normal(len(ri_t))]) * np.exp(-ri_t / 0.35)
    ri = np.vstack([m.filtre(ri[0], "lowpass", 6000), m.filtre(ri[1], "lowpass", 6000)])
    ri /= np.sqrt((ri ** 2).sum(axis=1, keepdims=True))
    envoi = pad * 0.3 + arp * 0.4 + fx * 0.25 + bat * 0.05
    rev = np.vstack([fftconvolve(envoi[k], ri[k])[:N] for k in range(2)])

    mix = bat * 0.9 + basse * 0.7 + pad * 1.1 + arp * 0.9 + fx * 0.9 + rev * 0.55
    mix = np.vstack([m.filtre(mix[k], "highpass", 32) for k in range(2)])
    fondu = np.ones(N)
    i0 = int(14.8 * SR)
    fondu[i0:] = np.linspace(1, 0, N - i0) ** 1.5
    return mix * fondu


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "pole"
    C = json.load(open(os.path.join(ICI, f"cues_{d}.json"), encoding="utf-8"))
    assert abs(C["duree"] - N / SR) < 1e-6
    x = arranger(C)
    mesure = pyln.Meter(SR)
    for _ in range(4):
        x *= 10 ** ((-14.0 - mesure.integrated_loudness(x.T)) / 20)
        x = m.limiteur(x)
        if abs(mesure.integrated_loudness(x.T) + 14.0) < 0.15:
            break
    tp = m.crete_vraie(x)
    if tp > -1.6:
        x *= 10 ** ((-1.6 - tp) / 20)
    sortie = os.path.join(ICI, "..", "_communs", f"musique_{d}.wav")
    sf.write(sortie, x.T, SR, subtype="PCM_24")
    print(f"{sortie} : {x.shape[1] / SR:.3f} s · {mesure.integrated_loudness(x.T):.1f} LUFS · crête vraie {m.crete_vraie(x):.2f} dBTP")


if __name__ == "__main__":
    main()
