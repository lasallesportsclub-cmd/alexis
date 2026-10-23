"""Musique originale de la pub « Vos questions » : 15 s, 120 BPM, ré mineur.

Tout est synthétisé ici : aucun échantillon, aucun morceau sous droits, pas de MusicGen (licence non
commerciale). Les bruits de la conversation font partie de la musique : la bulle de la cliente est une
note, la réponse de LA SALLE frappe sur le temps, les 5 étoiles d'un avis montent en doubles croches.
Les instants viennent de tools/cues.json, la même feuille que le storyboard.

Usage : $HYPERFRAMES_PYTHON tools/musique.py [-o assets/audio/musique.wav]
(numpy, scipy, soundfile, pyloudnorm ; cible −14 LUFS intégrés, crête vraie ≤ −1,5 dBTP)
"""
import argparse
import json
import os

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import butter, fftconvolve, resample_poly, sosfilt

SR = 48000
ICI = os.path.dirname(os.path.abspath(__file__))
CUES = json.load(open(os.path.join(ICI, "cues.json"), encoding="utf-8"))
TEMPS = 60 / CUES["bpm"]           # 0,5 s
DC = TEMPS / 4                     # double croche, 0,125 s
DUREE = CUES["duree"]
N = int(round(SR * DUREE))
CASSURE = tuple(CUES["cassure"])
rng = np.random.default_rng(2026)

# Grille harmonique, une mesure = 2 s : Dm, Bb, F, C, Dm, Bb, puis Bb, C (carte finale) et Dm final.
ACCORDS = [(0.0, "Dm"), (2.0, "Bb"), (4.0, "F"), (6.0, "C"), (8.0, "Dm"), (10.0, "Bb"),
           (12.0, "Bb"), (13.0, "C"), (14.0, "Dm")]
NAPPE = {"Dm": [50, 57, 62, 65], "Bb": [46, 53, 58, 62], "F": [53, 57, 60, 65], "C": [48, 55, 60, 64]}
BASSE = {"Dm": 38, "Bb": 34, "F": 41, "C": 36}
# Motif en 3+3+2+3+3+2 doubles croches, notes de l'accord (octave 4 ; +12 après la cassure)
MOTIF_PAS = [0, 3, 6, 8, 11, 14]
MOTIF = {"Dm": [62, 65, 69, 74, 69, 65], "Bb": [62, 65, 70, 74, 70, 65],
         "F": [60, 65, 69, 72, 69, 65], "C": [60, 64, 67, 72, 67, 64]}


def accord(t):
    nom = ACCORDS[0][1]
    for t0, a in ACCORDS:
        if t >= t0 - 1e-9:
            nom = a
    return nom


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tps(d):
    return np.arange(int(round(d * SR))) / SR


def stereo():
    return np.zeros((2, N))


def poser(buf, t0, x, gain=1.0, pan=0.0):
    """Ajoute un signal mono x à t0 (s), panoramique à puissance constante (−1 gauche … +1 droite)."""
    if x.ndim == 2:
        a, b = x[0], x[1]
    else:
        g = np.array([np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)]) * np.sqrt(2)
        a, b = x * g[0], x * g[1]
    i0 = int(round(t0 * SR))
    j0, j1 = max(0, i0), min(N, i0 + len(a))
    if j1 <= j0:
        return
    buf[0, j0:j1] += gain * a[j0 - i0:j1 - i0]
    buf[1, j0:j1] += gain * b[j0 - i0:j1 - i0]


def filtre(x, kind, f, ordre=2):
    sos = butter(ordre, f, btype=kind, fs=SR, output="sos")
    return sosfilt(sos, x)


def scie(f, d, phase=0.0):
    """Dent de scie à bande limitée (polyBLEP)."""
    n = int(round(d * SR))
    dt = f / SR
    ph = (phase + dt * np.arange(n)) % 1.0
    y = 2 * ph - 1
    m = ph < dt
    t = ph[m] / dt
    y[m] -= t + t - t * t - 1
    m = ph > 1 - dt
    t = (ph[m] - 1) / dt
    y[m] -= t * t + t + t + 1
    return y


def env_adr(n, a, r, d=None):
    """Enveloppe attaque linéaire, décroissance exponentielle d (s) ou plateau, relâchement r (s)."""
    t = np.arange(n) / SR
    e = np.minimum(1.0, t / max(a, 1e-4))
    if d:
        e *= np.exp(-np.maximum(0, t - a) / d)
    nr = int(r * SR)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


# ---------- instruments ----------
def grosse_caisse():
    t = tps(0.42)
    f = 46 + 118 * np.exp(-t / 0.03)
    corps = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.16)
    clic = filtre(rng.standard_normal(len(t)), "highpass", 2500) * np.exp(-t / 0.004) * 0.3
    claque = filtre(rng.standard_normal(len(t)), "bandpass", [140, 420]) * np.exp(-t / 0.025) * 0.9
    return np.tanh((corps + clic + claque) * 1.5) / np.tanh(1.5)


def clap():
    t = tps(0.38)
    e = np.zeros_like(t)
    for o, tau in ((0.0, 0.006), (0.009, 0.006), (0.019, 0.12)):
        m = t >= o
        e[m] = np.maximum(e[m], np.exp(-(t[m] - o) / tau))
    return filtre(rng.standard_normal(len(t)) * e, "bandpass", [900, 3600]) * 1.6


def charley(ouvert=False):
    t = tps(0.24 if ouvert else 0.05)
    x = rng.standard_normal(len(t)) * np.exp(-t / (0.09 if ouvert else 0.013))
    return filtre(x, "highpass", 7500, 4)


def caisse_claire():
    t = tps(0.2)
    bruit = filtre(rng.standard_normal(len(t)), "bandpass", [1200, 7000]) * np.exp(-t / 0.05)
    ton = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.03)
    return bruit * 0.9 + ton * 0.5


def note_basse(m, d):
    f = mtof(m)
    n = int(round(d * SR))
    x = scie(f, d) * 0.55 + np.sin(2 * np.pi * f * np.arange(n) / SR) * 0.9
    clair, sombre = filtre(x, "lowpass", 2600), filtre(x, "lowpass", 360)
    t = np.arange(n) / SR
    y = sombre + np.exp(-t / 0.05) * (clair - sombre)
    y = np.tanh(y * 2.2) / np.tanh(2.2)                 # harmoniques : la basse s'entend sur un téléphone
    return y * env_adr(n, 0.003, 0.03, 0.16)


def pincee(m, d=0.34, brillance=1.0):
    f = mtof(m)
    n = int(round(d * SR))
    x = scie(f, d) * 0.7 + scie(f * 1.004, d, 0.31) * 0.5
    clair, sombre = filtre(x, "lowpass", 5200 * brillance), filtre(x, "lowpass", 850)
    t = np.arange(n) / SR
    y = sombre + np.exp(-t / 0.08) * (clair - sombre)
    return y * env_adr(n, 0.002, 0.04, 0.17)


def nappe(notes, d):
    n = int(round(d * SR))
    g, dr = np.zeros(n), np.zeros(n)
    for k, m in enumerate(notes):
        for det, cote in ((-0.08, 0), (0.07, 1), (0.0, k % 2)):
            v = scie(mtof(m + det), d, (k * 0.21 + det) % 1)
            (g if cote == 0 else dr)[:] += v
    e = env_adr(n, 0.22, 0.28)
    return np.vstack([filtre(g, "lowpass", 1500) * e, filtre(dr, "lowpass", 1500) * e]) * 0.11


def cloche(m, d=1.1):
    f = mtof(m)
    t = tps(d)
    y = np.zeros_like(t)
    for ratio, amp, tau in ((1, 1, 0.75), (2.0, 0.45, 0.4), (2.76, 0.3, 0.28), (4.07, 0.18, 0.18), (5.4, 0.1, 0.1)):
        y += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t / tau)
    return y * np.minimum(1, t / 0.0015) * 0.5


def bulle(m=81):
    """Bulle de la cliente : goutte accordée (la5), qui tombe vers sa note."""
    t = tps(0.16)
    f = mtof(m) * (1 + 0.32 * np.exp(-t / 0.012))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return x * np.exp(-t / 0.06) * np.minimum(1, t / 0.002)


def tic():
    t = tps(0.04)
    return (filtre(rng.standard_normal(len(t)), "bandpass", [2500, 6500]) * np.exp(-t / 0.006) * 0.8
            + np.sin(2 * np.pi * 2350 * t) * np.exp(-t / 0.01) * 0.5)


def impact(grave=1.0):
    t = tps(1.0)
    f = 38 + 70 * np.exp(-t / 0.06)
    corps = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.3) * grave
    souffle = filtre(rng.standard_normal(len(t)), "lowpass", 2600) * np.exp(-t / 0.05) * 0.45
    return corps + souffle


def crash(d=1.6):
    t = tps(d)
    return filtre(rng.standard_normal(len(t)), "highpass", 3200, 3) * np.exp(-t / 0.55) * 0.5


def monte(d):
    """Montée : balayage sinus 200 → 1 600 Hz et souffle aigu qui grossissent jusqu'au bout."""
    t = tps(d)
    u = t / d
    f = 200 * 8 ** u
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * u ** 2 * 0.25
    b = filtre(rng.standard_normal(len(t)), "highpass", 1800) * u ** 3 * 0.6
    return s + b


def descente(d=0.42):
    t = tps(d)
    f = 95 * (0.4 ** (t / d))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 - t / d) ** 1.5 * 0.7


def souffle(d, pic):
    """Souffle filtré en cloche, culmine à pic (s) : sert au volet des bandes."""
    t = tps(d)
    e = np.where(t < pic, (t / pic) ** 2, np.exp(-(t - pic) / 0.06))
    return filtre(rng.standard_normal(len(t)), "bandpass", [500, 5000]) * e


def cymbale_inverse(d=0.3):
    t = tps(d)
    return filtre(rng.standard_normal(len(t)), "highpass", 4000, 3) * (t / d) ** 3


# ---------- écriture ----------
def joue_ici(t):
    return not (CASSURE[0] - 1e-9 <= t < CASSURE[1] - 1e-9)


def musique():
    bat, basse, pad, motif, conv, fx = (stereo() for _ in range(6))
    GC, CL, CH, CHO = grosse_caisse(), clap(), charley(), charley(True)
    nb_temps = int(DUREE / TEMPS)
    coups = []                                         # instants de grosse caisse (pour le sidechain)

    for b in range(nb_temps):
        t = b * TEMPS
        if not joue_ici(t) or t > 14.0 + 1e-9:
            continue
        fin = t >= 12.0
        poser(bat, t, GC, 0.8)
        coups.append(t)
        if b % 2 == 1 and t < 14.0:
            poser(bat, t, CL, 0.5 if not fin else 0.36, 0.05)
        if t < 14.0:
            gros = t >= CASSURE[1]
            poser(bat, t + TEMPS / 2, CHO if (gros and b % 2 == 1) else CH, 0.3, 0.25)
            if not fin:
                for k in (1, 3):
                    poser(bat, t + k * DC, CH, 0.07 + 0.03 * (b % 2), -0.3)

    # roulement 7,5 → 8,0 qui mène à la cassure (doubles puis triples croches)
    for k, tt in enumerate(np.concatenate([7.5 + np.arange(2) * DC, 7.75 + np.arange(4) * DC / 2])):
        poser(bat, tt, caisse_claire(), 0.12 + 0.05 * k, 0.1)
    # roulement 11,5 → 12,0 avant le volet
    for k in range(4):
        poser(bat, 11.5 + k * DC, caisse_claire(), 0.1 + 0.05 * k, -0.1)

    # basse : croche à contretemps sur chaque temps, octave sur le dernier temps de la mesure
    for b in range(nb_temps):
        t = b * TEMPS
        if not joue_ici(t) or t >= 14.0:
            continue
        r = BASSE[accord(t)]
        poser(basse, t + TEMPS / 2, note_basse(r + (12 if b % 4 == 3 else 0), 0.22), 0.5)
        if b % 2 == 0:
            poser(basse, t, note_basse(r, 0.16), 0.3)
    poser(basse, 14.0, note_basse(38, 0.9), 0.55)      # tonique finale

    # nappe
    for t0, nom in ACCORDS:
        d = {12.0: 1.0, 13.0: 1.0, 14.0: 1.0}.get(t0, 2.0)
        debut = CASSURE[1] if t0 == CASSURE[0] else t0
        d -= debut - t0
        g = 0.75 if t0 < CASSURE[0] else 1.0
        poser(pad, debut, nappe(NAPPE[nom], d + 0.25), g)
        if t0 >= CASSURE[1] - 0.6 and t0 < 12.0:      # après la cassure : doublure à l'octave
            poser(pad, debut, nappe([m + 12 for m in NAPPE[nom]], d + 0.25), 0.45)

    # motif pincé (avec écho pointé gauche/droite)
    for mesure in range(6):
        t0 = mesure * 2.0
        nom = accord(t0)
        haut = 12 if t0 >= CASSURE[0] else 0
        for pas, m in zip(MOTIF_PAS, MOTIF[nom]):
            t = t0 + pas * DC
            if not joue_ici(t):
                continue
            poser(motif, t, pincee(m + haut, brillance=1.3 if haut else 1.0), 0.36 if haut else 0.33,
                  -0.15 if pas % 2 else 0.15)
            if haut:
                poser(motif, t, pincee(m + haut - 12, 0.3), 0.12)
    for t, m in ((12.0, 70), (12.375, 74), (12.75, 77), (13.0, 72), (13.375, 76), (13.75, 79)):
        poser(motif, t, pincee(m), 0.2, 0.2 if m % 2 else -0.2)

    # conversation : chaque évènement de cues.json joue sa note
    for e in CUES["evenements"]:
        t, ty = e["t"], e["type"]
        nom = accord(t)
        if ty == "question":
            poser(conv, t, bulle(81), 0.42, -0.35)
            poser(conv, t + 0.06, bulle(86), 0.18, -0.35)
        elif ty in ("saisie", "saisie-cassure"):
            for k in range(3):
                poser(conv, t + k * DC, tic(), 0.16 if ty == "saisie" else 0.26, 0.35)
        elif ty == "reponse":
            poser(fx, t, impact(0.8), 0.55)
            for m in NAPPE[nom][1:]:
                poser(conv, t, pincee(m + 12, 0.4, 1.4), 0.2, 0.3)
        elif ty in ("precision", "reponse-courte"):
            poser(conv, t, pincee(MOTIF[nom][2] + 12, 0.3, 1.2), 0.24, 0.3)
        elif ty == "avis":
            poser(fx, t, impact(1.0 if e.get("drop") else 0.6), 0.75 if e.get("drop") else 0.45)
            for k, m in enumerate((86, 89, 93, 96, 98)):          # 5 étoiles, ré-fa-la-do-ré
                poser(conv, t + k * DC, cloche(m), 0.32, -0.4 + 0.2 * k)
        elif ty == "volet":
            poser(fx, t, souffle(0.6, 0.45), 0.5)
        elif ty == "logo":
            for k in range(3):                                     # 3 bandes = 3 glissés
                poser(fx, t + k * DC, souffle(0.2, 0.06), 0.28, -0.5 + 0.5 * k)
            poser(conv, t + 0.5, cloche(98, 1.4), 0.22)
        elif ty == "cta":
            poser(fx, t, impact(0.6), 0.4)
            for m in NAPPE[nom][1:]:
                poser(conv, t, pincee(m + 12, 0.45, 1.3), 0.18, 0.25)
        elif ty == "final":
            poser(fx, t, impact(1.0), 0.6)
            poser(fx, t, crash(1.0), 0.45)
            for m in (62, 65, 69, 74):
                poser(conv, t, pincee(m, 0.9, 1.2), 0.2)

    # transitions de la cassure : montée, chute, cymbale inversée, puis le drop
    poser(fx, 6.6, monte(1.4), 0.45)
    poser(fx, CASSURE[0], descente(), 0.5)
    poser(fx, CASSURE[1] - 0.3, cymbale_inverse(0.3), 0.35)
    poser(fx, CASSURE[1], crash(1.6), 0.5)

    # sidechain : la basse, la nappe et le motif respirent sous la grosse caisse
    t = np.arange(N) / SR
    souffle_gc = np.ones(N)
    for tc in coups:
        i = int(tc * SR)
        n = min(N - i, int(0.25 * SR))
        souffle_gc[i:i + n] = np.minimum(souffle_gc[i:i + n], 1 - 0.6 * np.exp(-np.arange(n) / SR / 0.08))
    for buf in (basse, pad, motif):
        buf *= souffle_gc

    # réverbération : réponse impulsionnelle synthétique (bruit décorrélé, décroissance 1,3 s)
    ri_t = tps(1.6)
    ri = np.vstack([rng.standard_normal(len(ri_t)), rng.standard_normal(len(ri_t))]) * np.exp(-ri_t / 0.42)
    ri = np.vstack([filtre(ri[0], "lowpass", 6000), filtre(ri[1], "lowpass", 6000)])
    ri /= np.sqrt((ri ** 2).sum(axis=1, keepdims=True))
    envoi = pad * 0.35 + motif * 0.3 + conv * 0.35 + bat * 0.06 + fx * 0.2
    rev = np.vstack([fftconvolve(envoi[c], ri[c])[:N] for c in range(2)])

    mix = bat * 0.9 + basse * 0.75 + pad * 1.2 + motif + conv + fx * 0.9 + rev * 0.55
    mix = np.vstack([filtre(mix[c], "highpass", 30) for c in range(2)])
    fondu = np.ones(N)
    i0 = int(14.65 * SR)
    fondu[i0:] = np.linspace(1, 0, N - i0) ** 1.5
    return mix * fondu


def crete_vraie(x):
    return 20 * np.log10(np.max(np.abs(resample_poly(x, 4, 1, axis=1))) + 1e-12)


def limiteur(x, plafond_db=-1.9, attaque=0.002, relache=0.08):
    """Limiteur à anticipation sur la crête suréchantillonnée ×4."""
    plafond = 10 ** (plafond_db / 20)
    pic = np.max(np.abs(resample_poly(x, 4, 1, axis=1)), axis=0).reshape(-1, 4).max(axis=1)[:x.shape[1]]
    if len(pic) < x.shape[1]:
        pic = np.pad(pic, (0, x.shape[1] - len(pic)))
    besoin = np.minimum(1.0, plafond / np.maximum(pic, 1e-9))
    la = int(attaque * SR)
    g = np.ones_like(besoin)
    ar, rr = np.exp(-1 / (attaque * SR)), np.exp(-1 / (relache * SR))
    cur = 1.0
    # anticipation : on prend le minimum du besoin sur la fenêtre d'attaque à venir
    fen = np.lib.stride_tricks.sliding_window_view(np.concatenate([besoin, np.ones(la)]), la + 1).min(axis=1)
    for i, b in enumerate(fen):
        cur = ar * cur + (1 - ar) * b if b < cur else rr * cur + (1 - rr) * b
        g[i] = cur
    return x * np.minimum(g, fen)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--sortie", default=os.path.join(ICI, "..", "assets", "audio", "musique.wav"))
    ap.add_argument("--lufs", type=float, default=-14.0)
    a = ap.parse_args()
    x = musique()
    mesure = pyln.Meter(SR)
    for _ in range(4):                                # gain → limiteur → nouvelle mesure
        x *= 10 ** ((a.lufs - mesure.integrated_loudness(x.T)) / 20)
        x = limiteur(x)
        if abs(mesure.integrated_loudness(x.T) - a.lufs) < 0.15:
            break
    tp = crete_vraie(x)
    if tp > -1.6:                                     # garde-fou : crête vraie ≤ −1,6 dBTP
        x *= 10 ** ((-1.6 - tp) / 20)
    os.makedirs(os.path.dirname(os.path.abspath(a.sortie)), exist_ok=True)
    sf.write(a.sortie, x.T, SR, subtype="PCM_24")
    print(f"{a.sortie} : {x.shape[1] / SR:.3f} s · {mesure.integrated_loudness(x.T):.1f} LUFS · "
          f"crête vraie {crete_vraie(x):.2f} dBTP")


if __name__ == "__main__":
    main()
