"""Classe les prises d'une même réplique générée (voix clonée) et garde la meilleure.

Pour chaque fichier : finition (finition_voix.py), transcription whisper-cli comparée au texte attendu,
ressemblance avec la voix de référence (encodeur de Chatterbox), durée et débit. Classement : texte exact
d'abord, puis ressemblance, puis débit proche de celui de la référence.

Usage :
    $CHATTERBOX_PYTHON choisir_prise.py --ref voix.wav --texte "Vos progrès, en trois D." \
        --dossier finis/ essais/P3_*.wav
Le modèle whisper vient de $WHISPER_MODEL (par défaut ~/.cache/hyperframes/whisper/models/ggml-small.bin).
L'écoute reste juge : ce classement écarte les prises fausses ou étrangères, il ne choisit pas le ton.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

import librosa
import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from finition_voix import finir  # noqa: E402

MODELE = os.environ.get("WHISPER_MODEL", os.path.expanduser("~/.cache/hyperframes/whisper/models/ggml-small.bin"))
CHIFFRES = {"3d": "trois d", "3": "trois", "4": "quatre", "30": "trente", "10": "dix", "2": "deux", "8": "huit"}


def mots(texte):
    t = unicodedata.normalize("NFKD", texte.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[’'`-]", " ", t)
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    out = []
    for m in t.split():
        out.extend(CHIFFRES.get(m, m).split())
    return out


def distance(a, b):
    """Distance d'édition en mots."""
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        prev, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (x != y))
    return d[-1]


def transcrire(chemin):
    with tempfile.TemporaryDirectory() as tmp:
        wav16 = os.path.join(tmp, "a.wav")
        y, sr = librosa.load(chemin, sr=16000, mono=True)
        sf.write(wav16, y, 16000, subtype="PCM_16")
        r = subprocess.run(["whisper-cli", "-m", MODELE, "-l", "fr", "-t", "2", "-nt", "-f", wav16],
                           capture_output=True, text=True)
        return " ".join(l.strip() for l in r.stdout.splitlines() if l.strip())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--texte", required=True)
    ap.add_argument("--dossier", required=True, help="où écrire les prises finies")
    ap.add_argument("fichiers", nargs="+")
    a = ap.parse_args()
    os.makedirs(a.dossier, exist_ok=True)

    import torch
    from chatterbox.models.voice_encoder import VoiceEncoder
    from huggingface_hub import hf_hub_download
    ve = VoiceEncoder()
    ve.load_state_dict(torch.load(hf_hub_download("ResembleAI/chatterbox", "ve.pt"), map_location="cpu", weights_only=True))
    ve.eval()
    sr_ve = ve.hp.sample_rate
    emb = lambda y: ve.embeds_from_wavs([y], sr_ve, as_spk=True)
    ref = emb(librosa.load(a.ref, sr=sr_ve, mono=True)[0])

    attendu = mots(a.texte)
    lignes = []
    for f in a.fichiers:
        x, sr = sf.read(f)
        y = finir(x, sr)
        sortie = os.path.join(a.dossier, os.path.basename(f))
        sf.write(sortie, y, sr, subtype="PCM_16")
        entendu = transcrire(sortie)
        err = distance(attendu, mots(entendu))
        sim = float(np.dot(ref, emb(librosa.resample(y.astype(np.float32), orig_sr=sr, target_sr=sr_ve))))
        duree = len(y) / sr
        lignes.append((err, -sim, duree, sortie, entendu))
    lignes.sort()
    print(f"Attendu : « {a.texte} »")
    for err, msim, duree, sortie, entendu in lignes:
        print(f"{'OK ' if err == 0 else f'×{err} '} ress. {-msim:.3f}  {duree:5.2f} s  {os.path.basename(sortie)}  « {entendu} »")


if __name__ == "__main__":
    main()
