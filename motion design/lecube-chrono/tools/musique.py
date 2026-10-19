"""Musique originale de la pub LE CUBE « LE CHRONO » : 15 s, 120 BPM, mi mineur, commune aux trois versions.

Tout est synthétisé ici : aucun échantillon, aucun morceau sous droits, pas de MusicGen (licence non
commerciale). Le chrono fait partie de la musique : un bip à chaque seconde (sur les temps), la cloche de boxe
à chaque round, le buzzer de fin de WOD quand le chrono tombe à 00:00. Cassure d'un demi-temps avant
l'argument, puis la reprise. Instants : tools/cues.json, la même feuille que les compositions.

Usage : ~/.venvs/hyperframes-audio/bin/python tools/musique.py [-o _communs/assets/audio/musique.wav]
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
TEMPS = 60 / CUES["bpm"]
DC = TEMPS / 4
DUREE = CUES["duree"]
N = int(round(SR * DUREE))
CASSURE = tuple(CUES["cassure"])
FIN = CUES["fin"]
rng = np.random.default_rng(78700)

# Une mesure = 2 s. Em, Em, C, D, (cassure), Em, C, Em final.
ACCORDS = [(0.0, "Em"), (2.0, "Em"), (4.0, "C"), (6.0, "D"), (9.0, "Em"), (11.0, "C"), (13.0, "Em")]
NAPPE = {"Em": [52, 59, 64, 67], "C": [48, 55, 60, 64], "D": [50, 57, 62, 66]}
BASSE = {"Em": 40, "C": 36, "D": 38}
RIFF = [0, 0, 12, 0, 0, 10, 0, 7]          # croches, en demi-tons au-dessus de la fondamentale


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
    if x.ndim == 2:
        a, b = x[0], x[1]
    else:
        g = np.array([np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)]) * np.sqrt(2)
        a, b = x * g[0], x * g[1]
    i0 = int(round(t0 * SR))
    j0, j1 = max(0, i0), min(N, i0 + len(a))
    if j1 > j0:
        buf[0, j0:j1] += gain * a[j0 - i0:j1 - i0]
        buf[1, j0:j1] += gain * b[j0 - i0:j1 - i0]


def filtre(x, kind, f, ordre=2):
    return sosfilt(butter(ordre, f, btype=kind, fs=SR, output="sos"), x)


def scie(f, d, phase=0.0):
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


def env(n, a, r, d=None):
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
    t = tps(0.45)
    f = 44 + 130 * np.exp(-t / 0.028)
    corps = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.18)
    clic = filtre(rng.standard_normal(len(t)), "highpass", 2800) * np.exp(-t / 0.004) * 0.35
    claque = filtre(rng.standard_normal(len(t)), "bandpass", [150, 450]) * np.exp(-t / 0.03) * 1.0
    return np.tanh((corps + clic + claque) * 2.0) / np.tanh(2.0)


def frappe():
    """Caisse claire sèche + claquement de mains : le « hit » d'une salle de boxe."""
    t = tps(0.3)
    bruit = filtre(rng.standard_normal(len(t)), "bandpass", [1100, 6500]) * np.exp(-t / 0.06)
    ton = np.sin(2 * np.pi * 185 * t) * np.exp(-t / 0.035)
    return np.tanh((bruit * 1.1 + ton * 0.6) * 1.6)


def charley(ouvert=False):
    t = tps(0.22 if ouvert else 0.045)
    return filtre(rng.standard_normal(len(t)) * np.exp(-t / (0.08 if ouvert else 0.012)), "highpass", 7800, 4)


def note_basse(m, d):
    f = mtof(m)
    n = int(round(d * SR))
    x = scie(f, d) * 0.7 + scie(f * 1.006, d, 0.4) * 0.5 + np.sin(2 * np.pi * f / 2 * np.arange(n) / SR) * 0.8
    t = np.arange(n) / SR
    y = filtre(x, "lowpass", 420) + np.exp(-t / 0.04) * (filtre(x, "lowpass", 3000) - filtre(x, "lowpass", 420))
    return np.tanh(y * 2.8) / np.tanh(2.8) * env(n, 0.002, 0.025, 0.2)


def nappe(notes, d):
    n = int(round(d * SR))
    g, dr = np.zeros(n), np.zeros(n)
    for k, m in enumerate(notes):
        for det, cote in ((-0.09, 0), (0.08, 1), (0.0, k % 2)):
            (g if cote == 0 else dr)[:] += scie(mtof(m + det), d, (k * 0.19 + det) % 1)
    e = env(n, 0.15, 0.25)
    return np.vstack([filtre(g, "lowpass", 1100) * e, filtre(dr, "lowpass", 1100) * e]) * 0.1


def bip(d=0.07, f=1950):
    """Bip du chrono de box : sinus pur, attaque franche."""
    t = tps(d)
    return np.sin(2 * np.pi * f * t) * np.minimum(1, t / 0.002) * np.minimum(1, (d - t) / 0.008)


def buzzer(d=0.62):
    """Buzzer de fin de WOD : deux carrés graves, légèrement désaccordés."""
    t = tps(d)
    x = np.sign(np.sin(2 * np.pi * 523 * t)) * 0.5 + np.sign(np.sin(2 * np.pi * 784 * t)) * 0.4
    return filtre(x, "lowpass", 3200) * np.minimum(1, t / 0.004) * np.minimum(1, (d - t) / 0.04) * 0.6


def cloche_boxe(d=1.5):
    """Cloche de ring : partiels inharmoniques autour de 1,1 kHz, attaque métallique."""
    t = tps(d)
    y = np.zeros_like(t)
    for ratio, amp, tau in ((1.0, 1.0, 0.9), (2.32, 0.55, 0.5), (3.71, 0.35, 0.3), (5.12, 0.22, 0.18), (6.9, 0.12, 0.1)):
        y += amp * np.sin(2 * np.pi * 1080 * ratio * t) * np.exp(-t / tau)
    choc = filtre(rng.standard_normal(len(t)), "highpass", 3000) * np.exp(-t / 0.004) * 0.6
    return (y * 0.45 + choc) * np.minimum(1, t / 0.0008)


def impact(grave=1.0):
    t = tps(1.0)
    f = 36 + 80 * np.exp(-t / 0.05)
    corps = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.28) * grave
    return corps + filtre(rng.standard_normal(len(t)), "lowpass", 2400) * np.exp(-t / 0.05) * 0.5


def crash(d=1.4):
    t = tps(d)
    return filtre(rng.standard_normal(len(t)), "highpass", 3000, 3) * np.exp(-t / 0.5) * 0.5


def monte(d):
    t = tps(d)
    u = t / d
    s = np.sin(2 * np.pi * np.cumsum(180 * 9 ** u) / SR) * u ** 2 * 0.25
    return s + filtre(rng.standard_normal(len(t)), "highpass", 1800) * u ** 3 * 0.6


def souffle(d, pic):
    t = tps(d)
    e = np.where(t < pic, (t / pic) ** 2, np.exp(-(t - pic) / 0.06))
    return filtre(rng.standard_normal(len(t)), "bandpass", [500, 5000]) * e


# ---------- écriture ----------
def joue(t):
    return not (CASSURE[0] - 1e-9 <= t < CASSURE[1] - 1e-9) and t < FIN - 1e-9


def musique():
    bat, basse, pad, fx, chrono = (stereo() for _ in range(5))
    GC, FR, CH, CHO = grosse_caisse(), frappe(), charley(), charley(True)
    coups = []
    for b in range(int(DUREE / TEMPS)):
        t = b * TEMPS
        if not joue(t):
            continue
        apres = t >= CASSURE[1]
        poser(bat, t, GC, 0.85)
        coups.append(t)
        if b % 2 == 1:
            poser(bat, t, FR, 0.42, 0.05)
        poser(bat, t + TEMPS / 2, CHO if apres and b % 2 else CH, 0.26, 0.25)
        for k in ((1, 3) if not apres else (1, 2, 3)):
            poser(bat, t + k * DC, CH, 0.08 + 0.03 * (k == 2), -0.3)
        # basse : riff en croches, plus serré (doubles croches) après la cassure
        r = BASSE[accord(t)]
        for k in range(2):
            pas = (b * 2 + k) % len(RIFF)
            poser(basse, t + k * TEMPS / 2, note_basse(r + RIFF[pas], 0.2), 0.5)
        if apres and t < 11.5:
            poser(basse, t + 3 * DC, note_basse(r + 12, 0.08), 0.22)
    # roulement de frappes avant la cassure et avant la carte
    for k in range(4):
        poser(bat, 8.0 + k * DC, FR, 0.14 + 0.07 * k, 0.1)
        poser(bat, 11.0 + k * DC, FR, 0.1 + 0.05 * k, -0.1)

    for i, (t0, nom) in enumerate(ACCORDS):
        t1 = ACCORDS[i + 1][0] if i + 1 < len(ACCORDS) else FIN
        t1 = min(t1, CASSURE[0]) if t0 < CASSURE[0] else t1
        poser(pad, t0, nappe(NAPPE[nom], t1 - t0 + 0.2), 1.0 if t0 < 9 else 1.25)

    # le chrono : un bip par seconde, sur les temps ; les trois derniers plus longs ; buzzer à 00:00
    c = CUES["chrono"]
    for k in range(c["depart"]):
        t = c["premier_tic"] + k * c["pas"]
        reste = c["depart"] - 1 - k
        if reste == 0:
            poser(chrono, t, buzzer(), 0.55)
        elif reste <= 2:
            poser(chrono, t, bip(0.16, 1950), 0.3)
        else:
            poser(chrono, t, bip(), 0.17)

    # accroche : impact à l'image 0, frappe au deuxième temps fort
    poser(fx, 0.0, impact(1.0), 0.7)
    poser(fx, 0.0, crash(1.2), 0.32)
    poser(fx, 1.5, impact(0.7), 0.45)
    # rounds : cloche de ring à chaque round, glissé avant
    for r in CUES["rounds"]:
        poser(fx, r["t"] - 0.18, souffle(0.24, 0.16), 0.3)
        poser(fx, r["t"], cloche_boxe(), 0.3, 0.2)
        poser(fx, r["t"], impact(0.6), 0.4)
    # montée, cassure (un seul bip dans le silence), reprise
    poser(fx, 7.5, monte(1.0), 0.4)
    poser(fx, CASSURE[1], impact(1.0), 0.7)
    poser(fx, CASSURE[1], crash(1.6), 0.45)
    a = CUES["argument"]
    poser(fx, a["deuxieme"], impact(0.6), 0.35)
    # carte finale et appel à l'action
    poser(fx, CUES["carte"] - 0.3, souffle(0.5, 0.3), 0.4)
    poser(fx, CUES["carte"], impact(0.9), 0.55)
    poser(fx, CUES["cta"], impact(0.6), 0.4)
    poser(fx, FIN, crash(0.5), 0.3)

    t = np.arange(N) / SR
    respire = np.ones(N)
    for tc in coups:
        i = int(tc * SR)
        n = min(N - i, int(0.24 * SR))
        respire[i:i + n] = np.minimum(respire[i:i + n], 1 - 0.55 * np.exp(-np.arange(n) / SR / 0.08))
    for buf in (basse, pad):
        buf *= respire

    ri_t = tps(1.2)
    ri = np.vstack([rng.standard_normal(len(ri_t)), rng.standard_normal(len(ri_t))]) * np.exp(-ri_t / 0.3)
    ri = np.vstack([filtre(ri[0], "lowpass", 6000), filtre(ri[1], "lowpass", 6000)])
    ri /= np.sqrt((ri ** 2).sum(axis=1, keepdims=True))
    envoi = pad * 0.3 + fx * 0.25 + chrono * 0.15 + bat * 0.05
    rev = np.vstack([fftconvolve(envoi[k], ri[k])[:N] for k in range(2)])

    mix = bat * 0.9 + basse * 0.7 + pad * 1.1 + fx * 0.9 + chrono + rev * 0.5
    mix = np.vstack([filtre(mix[k], "highpass", 32) for k in range(2)])
    fondu = np.ones(N)
    i0 = int(14.8 * SR)
    fondu[i0:] = np.linspace(1, 0, N - i0) ** 1.5
    return mix * fondu


def crete_vraie(x):
    return 20 * np.log10(np.max(np.abs(resample_poly(x, 4, 1, axis=1))) + 1e-12)


def limiteur(x, plafond_db=-1.9, attaque=0.002, relache=0.08):
    plafond = 10 ** (plafond_db / 20)
    pic = np.max(np.abs(resample_poly(x, 4, 1, axis=1)), axis=0).reshape(-1, 4).max(axis=1)[:x.shape[1]]
    if len(pic) < x.shape[1]:
        pic = np.pad(pic, (0, x.shape[1] - len(pic)))
    besoin = np.minimum(1.0, plafond / np.maximum(pic, 1e-9))
    la = int(attaque * SR)
    g = np.ones_like(besoin)
    ar, rr = np.exp(-1 / (attaque * SR)), np.exp(-1 / (relache * SR))
    cur = 1.0
    fen = np.lib.stride_tricks.sliding_window_view(np.concatenate([besoin, np.ones(la)]), la + 1).min(axis=1)
    for i, b in enumerate(fen):
        cur = ar * cur + (1 - ar) * b if b < cur else rr * cur + (1 - rr) * b
        g[i] = cur
    return x * np.minimum(g, fen)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--sortie", default=os.path.join(ICI, "..", "_communs", "assets", "audio", "musique.wav"))
    ap.add_argument("--lufs", type=float, default=-14.0)
    a = ap.parse_args()
    x = musique()
    mesure = pyln.Meter(SR)
    for _ in range(4):
        x *= 10 ** ((a.lufs - mesure.integrated_loudness(x.T)) / 20)
        x = limiteur(x)
        if abs(mesure.integrated_loudness(x.T) - a.lufs) < 0.15:
            break
    tp = crete_vraie(x)
    if tp > -1.6:
        x *= 10 ** ((-1.6 - tp) / 20)
    os.makedirs(os.path.dirname(os.path.abspath(a.sortie)), exist_ok=True)
    sf.write(a.sortie, x.T, SR, subtype="PCM_24")
    print(f"{a.sortie} : {x.shape[1] / SR:.3f} s · {mesure.integrated_loudness(x.T):.1f} LUFS · "
          f"crête vraie {crete_vraie(x):.2f} dBTP")


if __name__ == "__main__":
    main()
