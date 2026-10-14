"""Prépare les répliques voix « ton pub » des vidéos Premium et les copie dans les projets HyperFrames.

Les fichiers audio restent hors du dépôt (public) : sources dans ~/voix-clone (enregistrement autorisé et prises
clonées), sorties dans ~/voix-clone/premium/final puis dans <projet>/assets/voix/ (ignoré par git).

Prises réelles : découpées dans l'enregistrement nettoyé. P4 est trop longue pour sa scène : ses mots sont recollés
avec des pauses de 50 ms, puis accélérés ×1,12 sans changer la hauteur (rubberband).
Prises clonées (Chatterbox) : la meilleure de choisir_prise.py, déjà finie par finition_voix.py. Pour la 25, la prise 7
(référence « pub ») : assez courte pour la scène sans accélération ; accélérée, la prise 5 rendait « Premium » ambigu.
Repères : début des mots qui déclenchent un texte, mesurés à l'énergie et au centroïde spectral (whisper situe mal
les mots d'une phrase courte), en secondes dans le fichier source. voix.json les donne dans le temps de chaque réplique.
Toutes passent par la même chaîne : passe-haut 80 Hz, compression douce, présence +2 dB à 3,5 kHz, sonie −16,4 LUFS
avec crêtes limitées à −4,5 dBFS, 30 ms avant la parole et 80 ms après. Ce niveau fait sortir le rendu HyperFrames
à −14 LUFS : master.py copie alors l'audio sans le renormaliser (pas de loudnorm dynamique sur la voix).

Usage : ~/.venvs/hyperframes-audio/bin/python voix.py          → prépare et copie, affiche durées et repères
"""
import json
import os
import shutil
import subprocess
import tempfile

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

V = os.path.expanduser("~/voix-clone")
SOURCE = f"{V}/source/voix_nettoyee.wav"
CLONES = f"{V}/premium/finis"
FINAL = f"{V}/premium/final"
MD = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SR = 48000
LUFS = -16.4
CRETE = -4.5     # dBFS, limiteur après normalisation
AVANT, APRES = 0.03, 0.08
SEUIL = -34.0  # dB sous le maximum de la réplique : début et fin de parole

# Prises réelles : (début, fin) en secondes dans l'enregistrement ; plusieurs morceaux = mots recollés
REELLES = {
    "P1": {"morceaux": [(1.22, 2.56)], "reperes": {"premium": 2.01}},     # Passez en version Premium.
    "P2": {"morceaux": [(6.33, 7.50)]},                                   # Votre boisson vous attend.
    "P6": {"morceaux": [(10.30, 12.12)], "reperes": {"chaque": 11.53}},   # Une analyse en trois D, chaque semaine.
    "P9": {"morceaux": [(13.47, 15.74)], "reperes": {"en": 14.90}},       # Activez-la à l'accueil, en quelques secondes.
    "P4a": {"morceaux": [(122.40, 123.00), (123.10, 124.20), (124.35, 125.42), (125.97, 126.60)],
            "mots": ["collagene", "multivitamines", "carnitine", "booster"], "pause": 0.05, "tempo": 1.12},
    "P4b": {"morceaux": [(126.96, 127.81), (128.01, 128.46)],
            "mots": ["ou", "eau"], "pause": 0.05, "tempo": 1.12},
}
# Prises clonées retenues, toutes sur la référence « ton pub » (essai choisi par le club) : classement choisir_prise.py
# (texte exact, puis ressemblance). Repères dans le fichier fini.
CLONEES = {
    "P3": {"fichier": "P3_pub_e0.6_c0.4_g2.wav"},                                  # Vos progrès, en trois D.
    "P5": {"fichier": "P5_pub_e0.5_c0.5_g4.wav", "reperes": {"toutes": 0.60}},      # Une boisson toutes les trente minutes.
    "P5r": {"fichier": "P5_pub_e0.6_c0.4_g7.wav", "reperes": {"toutes": 0.58}},     # même réplique, plus rapide (concept B)
    "25": {"fichier": "25_pub_e0.5_c0.5_g7.wav",                                    # Les quatre premières semaines…
           "reperes": {"semaines": 0.89, "de": 1.21, "sont": 2.06}},
}
PROJETS = {"A": ["P1", "P5", "P6", "25", "P9"], "B": ["P2", "P4a", "P4b", "P5r", "25", "P9"],
           "C": ["P3", "P6", "25", "P9"]}


def ffmpeg(src, dst, filtre):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", filtre, "-ar", str(SR), "-ac", "1",
                    "-c:a", "pcm_s24le", dst], check=True)


def lire(path, t0=None, t1=None):
    x, sr = sf.read(path, always_2d=True)
    x = x.mean(1)
    if t0 is not None:
        x = x[int(t0 * sr):int(t1 * sr)]
    if sr != SR:
        with tempfile.TemporaryDirectory() as tmp:
            sf.write(f"{tmp}/a.wav", x, sr, subtype="FLOAT")
            ffmpeg(f"{tmp}/a.wav", f"{tmp}/b.wav", "anull")
            x, _ = sf.read(f"{tmp}/b.wav")
    return x


def fondus(x, entree=0.005, sortie=0.015):
    x = x.copy()
    a, b = int(entree * SR), int(sortie * SR)
    x[:a] *= np.linspace(0, 1, a)
    x[-b:] *= np.linspace(1, 0, b)
    return x


def parole(x):
    """(début, fin) de la parole en secondes, par énergie sur 10 ms."""
    hop = SR // 100
    n = len(x) // hop
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
    on = np.nonzero(20 * np.log10(rms / rms.max()) > SEUIL)[0]
    return on[0] / 100, (on[-1] + 1) / 100


def preparer(nom):
    """Renvoie le signal brut 48 kHz de la réplique et, pour un montage par mots, le début de chaque mot."""
    if nom in CLONEES:
        return lire(os.path.join(CLONES, CLONEES[nom]["fichier"])), dict(CLONEES[nom].get("reperes", {}))
    r = REELLES[nom]
    if "mots" not in r:
        a = r["morceaux"][0][0]
        return fondus(lire(SOURCE, *r["morceaux"][0])), {k: t - a for k, t in r.get("reperes", {}).items()}
    parts, debuts, t = [], [], 0.0
    for k, (a, b) in enumerate(r["morceaux"]):
        m = fondus(lire(SOURCE, a, b))
        if k:
            parts.append(np.zeros(int(r.get("pause", 0) * SR)))
            t += r.get("pause", 0)
        debuts.append(t + parole(m)[0])
        parts.append(m)
        t += len(m) / SR
    return np.concatenate(parts), dict(zip(r["mots"], debuts))


def traiter(nom):
    x, reperes = preparer(nom)
    tempo = {**REELLES, **CLONEES}[nom].get("tempo", 1.0)
    with tempfile.TemporaryDirectory() as tmp:
        sf.write(f"{tmp}/in.wav", x, SR, subtype="FLOAT")
        chaine = ["highpass=f=80:poles=2",
                  "acompressor=threshold=-22dB:ratio=2.5:attack=6:release=80:knee=4",
                  "equalizer=f=3500:t=q:w=1.0:g=2"]
        if tempo != 1.0:
            chaine.insert(0, f"rubberband=tempo={tempo}:pitch=1:transients=mixed:formant=preserved:pitchq=quality")
        ffmpeg(f"{tmp}/in.wav", f"{tmp}/out.wav", ",".join(chaine))
        y, _ = sf.read(f"{tmp}/out.wav")
    a, b = parole(y)
    i0, i1 = max(0, int((a - AVANT) * SR)), min(len(y), int((b + APRES) * SR))
    y = fondus(y[i0:i1], 0.004, 0.03)
    for _ in range(3):  # sonie cible, puis limiteur ; le limiteur baisse un peu la sonie, d'où les reprises
        y = y * 10 ** ((LUFS - pyln.Meter(SR).integrated_loudness(y)) / 20)
        y = limiter(y)
    return y, {k: round(t / tempo - i0 / SR, 3) for k, t in reperes.items()}


def limiter(y):
    with tempfile.TemporaryDirectory() as tmp:
        sf.write(f"{tmp}/in.wav", y, SR, subtype="FLOAT")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{tmp}/in.wav", "-af",
                        f"alimiter=limit={10 ** (CRETE / 20):.4f}:attack=1.5:release=40:level=false:latency=true",
                        "-c:a", "pcm_f32le", f"{tmp}/out.wav"], check=True)
        return sf.read(f"{tmp}/out.wav")[0][:len(y)]


def main():
    os.makedirs(FINAL, exist_ok=True)
    infos = {}
    for nom in sorted(set(sum(PROJETS.values(), []))):
        y, reperes = traiter(nom)
        sf.write(os.path.join(FINAL, f"{nom}.wav"), y, SR, subtype="PCM_24")
        a, b = parole(y)
        crete = 20 * np.log10(np.abs(y).max())
        infos[nom] = {"duree": round(len(y) / SR, 3), "parole": [float(a), float(b)], "reperes": reperes}
        print(f"{nom:4s} {len(y) / SR:5.2f} s  parole {a:.2f}–{b:.2f}  crête {crete:5.1f} dBFS  "
              + " ".join(f"{k}@{t:.2f}" for k, t in reperes.items()))
    json.dump(infos, open(os.path.join(FINAL, "voix.json"), "w"), indent=1)
    for fmt in ("premium-916", "premium-45"):
        for concept, noms in PROJETS.items():
            dst = os.path.join(MD, fmt, concept, "assets", "voix")
            os.makedirs(dst, exist_ok=True)
            for nom in noms:
                shutil.copy(os.path.join(FINAL, f"{nom}.wav"), dst)
    print("copié dans premium-916/* et premium-45/* (assets/voix, hors git)")


if __name__ == "__main__":
    main()
