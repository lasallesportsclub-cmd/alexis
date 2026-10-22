"""Musique originale de la story fontaine LA SALLE : 34,5 s, 120 BPM, la mineur.

Instruments repris de lecube-chrono/tools/musique.py (synthèse pure, aucun échantillon, aucun morceau sous droits,
pas de MusicGen). Arrangement calé sur les repères de tools/build.py (SCENES, VOLET, CASSURE, reperes()) :
  accroche (0–2,5 s) : impact et crash à l'image 0, groove en demi-temps
  scène 2 : groove à quatre temps, arpège en croches, une note pincée par boisson qui entre
  parcours (7,5–19 s) : trait de lecture du scan, carillon de validation, « tic » à chaque choix sur l'écran,
                 une note pincée par étape
  bascule et versement (19–22,5 s) : souffle qui descend avec la caméra, batterie coupée ; écoulement synthétisé
                 (souffle d'éclaboussure, bulles, résonance de la gourde qui monte à mesure qu'elle se remplit),
                 carillon quand la contenance est atteinte, gouttes
  « 30 MIN » : impact ; montée avant la cassure
  volets : un souffle doux sur toute la durée de chaque dévoilement (0,9 s)
  cassure (27–27,5 s) : silence, puis reprise sur « + 2 € » avec impact et crash
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
m.N = N = int(round(SR * DUREE))      # les instruments écrivent dans des pistes de la durée de la story
TEMPS = 0.5
DC = TEMPS / 4
CASS = build.CASSURE
DEBUT = {c: t for c, t, _ in build.SCENES}
COUPES = [t for c, t, _ in build.SCENES[1:] if c not in build.BASCULE]
R = build.reperes()
VERSE = (R["bascule"], R["servez"])         # batterie coupée, arpège adouci : l'écoulement occupe l'espace

ACCORDS = [(0, "Am"), (2, "F"), (4, "C"), (6, "G"), (8, "Am"), (10, "F"), (12, "C"), (14, "G"), (16, "Am"), (18, "F"),
           (19.5, "C"), (22, "G"), (24, "Am"), (26, "G"), (27.5, "Am"), (29.5, "F"), (31, "C"), (32.5, "Am")]
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


def verse(t):
    return VERSE[0] - 1e-9 <= t < VERSE[1] - 1e-9


# ---------- sons du parcours et du versement (synthèse : aucun échantillon) ----------
def tic():
    """Toucher de l'écran : clic bref et petit « pop » grave."""
    t = m.tps(0.09)
    clic = m.filtre(m.rng.standard_normal(len(t)), "highpass", 2500) * np.exp(-t / 0.004)
    pop = np.sin(2 * np.pi * np.cumsum(420 + 500 * np.exp(-t / 0.01)) / SR) * np.exp(-t / 0.035)
    return clic * 0.5 + pop * 0.7


def faisceau(d, f0, f1):
    """Trait de lecture du scan : sinus et harmoniques qui glissent de f0 à f1, léger trémolo, sifflement."""
    t = m.tps(d)
    ph = 2 * np.pi * np.cumsum(f0 * (f1 / f0) ** (t / d)) / SR
    x = (np.sin(ph) + 0.45 * np.sin(2 * ph) + 0.18 * np.sin(3 * ph)) * (1 - 0.3 * (0.5 + 0.5 * np.sin(2 * np.pi * 17 * t)))
    souffle = m.filtre(m.rng.standard_normal(len(t)), "bandpass", [2500, 7000]) * 0.08
    return (x * 0.5 + souffle) * np.minimum(1, t / 0.04) * np.minimum(1, (d - t) / 0.1)


def carillon(f=1318.5):
    """Validation : deux notes cristallines (une quinte plus une quarte au-dessus)."""
    t = m.tps(0.9)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.25)
    t2 = m.tps(0.78)
    y = np.zeros_like(x)
    y[int(0.12 * SR):int(0.12 * SR) + len(t2)] = (np.sin(2 * np.pi * f * 4 / 3 * t2) + 0.3 * np.sin(2 * np.pi * f * 8 / 3 * t2)) * np.exp(-t2 / 0.3)
    return (x + y) * np.minimum(1, np.arange(len(x)) / SR / 0.003)


def descente(d):
    """La caméra descend de l'écran à la buse : glissé grave et souffle."""
    t = m.tps(d)
    u = t / d
    x = np.sin(2 * np.pi * np.cumsum(260 * (70 / 260) ** u) / SR) * np.sin(np.pi * u) ** 1.5
    return x * 0.45 + m.filtre(m.rng.standard_normal(len(t)), "bandpass", [300, 3000]) * np.sin(np.pi * u) ** 2 * 0.5


def ecoulement(d, f0=300, f1=1050):
    """Boisson qui coule dans la gourde : résonance de la colonne d'air qui monte quand la gourde se remplit
    (f inversement proportionnelle à la hauteur d'air), souffle d'éclaboussure qui gargouille, bulles brèves."""
    t = m.tps(d)
    n, u = len(t), t / d
    f = f0 / (1 - (1 - f0 / f1) * u)
    ph = 2 * np.pi * np.cumsum(f) / SR
    bande = lambda: (lambda b: b / (np.std(b) + 1e-9))(m.filtre(m.rng.standard_normal(n), "lowpass", 90))
    resonance = bande() * np.sin(ph) + 0.45 * bande() * np.sin(2 * ph)
    gargouille = 0.6 + 0.4 * np.tanh(2 * (lambda b: b / (np.std(b) + 1e-9))(m.filtre(m.rng.standard_normal(n), "lowpass", 14)))
    eclabousse = m.filtre(m.rng.standard_normal(n), "bandpass", [900, 7000]) * gargouille
    bulles = np.zeros(n)
    for _ in range(int(70 * d)):
        i0 = int(m.rng.random() * (n - 0.1 * SR))
        db = 0.02 + 0.05 * m.rng.random()
        tb = m.tps(db)
        fb = (650 + 2600 * m.rng.random()) * (1 + 0.25 * tb / db)
        b = np.sin(2 * np.pi * np.cumsum(fb) / SR) * np.exp(-tb / (0.008 + 0.015 * m.rng.random()))
        bulles[i0:i0 + len(b)] += b * (0.3 + 0.7 * m.rng.random())
    x = resonance * 0.16 + eclabousse * 0.5 + bulles * 0.22
    return x * np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.25)


def plic():
    """Goutte qui tombe dans la boisson : sinus qui monte très vite, décroissance brève."""
    t = m.tps(0.12)
    return np.sin(2 * np.pi * np.cumsum(500 + 1300 * (1 - np.exp(-t / 0.012))) / SR) * np.exp(-t / 0.035) * np.minimum(1, t / 0.001)


def arranger(bruitages=False):
    bat, basse, pad, arp, fx = (m.stereo() for _ in range(5))
    GC, FR, CH = m.grosse_caisse(), m.frappe(), m.charley()
    fin = DUREE - 1.0
    coups = []
    for b in range(int(DUREE / TEMPS)):
        t = b * TEMPS
        if silence(t) or t >= fin or verse(t):
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
                if verse(t) and k:                            # versement : une croche sur deux
                    continue
                m.poser(arp, t + k * TEMPS / 2, pincee(notes[(b * 2 + k) % 4] + (12 if drop else 0)), 0.1 if verse(t) else 0.15, 0.35 * (-1) ** k)

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
    for t in COUPES:                                       # volets : souffle sur tout le dévoilement
        m.poser(fx, t - build.VOLET / 2, m.souffle(build.VOLET, build.VOLET / 2), 0.26)
        if t != CASS[0]:
            m.poser(fx, t, m.impact(0.45), 0.22)
    for i, t in enumerate(R["puces"]):                     # puces des boissons
        m.poser(fx, t, pincee(81 + [0, 3, 7, 12, 7, 3][i], 0.3), 0.22, 0.4 * (-1) ** i)
    for i, t in enumerate(R["etapes"]):                    # une note par étape du parcours
        m.poser(fx, t + 0.2, pincee(76 + [0, 3, 5, 7, 12][i], 0.35), 0.24, 0.3 * (-1) ** i)
    m.poser(fx, R["balayage"], faisceau(0.5, 900, 1900), 0.2)     # trait de lecture du QR code et de la carte
    m.poser(fx, R["valide"], carillon(), 0.26)
    m.poser(fx, R["appareil"], m.souffle(0.8, 0.35), 0.22)        # l'appareil monte
    for i, t in enumerate(R["taps"]):                      # choix sur l'écran, puis l'écran suivant
        m.poser(fx, t + 0.05, tic(), 0.42, 0.15 * (-1) ** i)
        if i < len(R["taps"]) - 1:
            m.poser(fx, t + 0.25, m.souffle(0.25, 0.1), 0.1)
    m.poser(fx, R["bascule"], descente(build.VOLET), 0.3)         # la caméra descend à la buse
    hv = build.VERSEMENT
    arrivee = R["ouvre"] + build.chute(hv["buse"], hv["gourde"]["bas"] - 4)
    m.poser(fx, arrivee, m.filtre(m.rng.standard_normal(int(0.25 * SR)), "bandpass", [600, 5000]) * np.exp(-m.tps(0.25) / 0.05), 0.4)
    m.poser(fx, arrivee, ecoulement(R["plein"] - arrivee + 0.15), 0.85)
    m.poser(fx, R["plein"], carillon(1046.5), 0.3)                # contenance atteinte
    for t in R["gouttes"]:
        m.poser(fx, t + 0.12 + (2 * (hv["plein"] - hv["buse"] - 4) / hv["g"]) ** 0.5, plic(), 0.3)
    m.poser(fx, R["servez"], m.impact(0.6), 0.35)                 # « SERVEZ-VOUS. »
    m.poser(fx, R["trente"], m.impact(0.8), 0.5)           # « 30 MIN »
    m.poser(fx, R["trente"], FR, 0.3)
    m.poser(fx, CASS[0] - 1.0, m.monte(1.0), 0.38)
    m.poser(fx, R["prix"], m.impact(1.0), 0.7)             # « + 2 € »
    m.poser(fx, R["prix"], m.crash(1.6), 0.45)
    for t in R["bandes"]:                                  # bandes des avantages
        m.poser(fx, t - 0.08, m.souffle(0.3, 0.12), 0.2)
    m.poser(fx, R["accueil"], m.impact(0.6), 0.35)         # « À L'ACCUEIL. »
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
    plafond = -3.0 if bruitages else -1.9               # bruitages : impacts isolés, l'AAC fait plus déborder la crête
    x = arranger(bruitages)
    mesure = pyln.Meter(SR)
    for _ in range(6):
        x *= 10 ** ((cible - mesure.integrated_loudness(x.T)) / 20)
        x = m.limiteur(x, plafond)
        if abs(mesure.integrated_loudness(x.T) - cible) < 0.15:
            break
    tp = m.crete_vraie(x)
    if tp > plafond + 0.3:
        x *= 10 ** ((plafond + 0.3 - tp) / 20)
    sortie = os.path.join(ICI, "..", "_communs", "bruitages_fontaine.wav" if bruitages else "musique_fontaine.wav")
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    sf.write(sortie, x.T, SR, subtype="PCM_24")
    print(f"{os.path.normpath(sortie)} : {x.shape[1] / SR:.3f} s · {mesure.integrated_loudness(x.T):.1f} LUFS · "
          f"crête vraie {m.crete_vraie(x):.2f} dBTP")


if __name__ == "__main__":
    main()
