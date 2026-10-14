"""Ressemblance entre une voix de référence et des fichiers générés (encodeur de voix de Chatterbox).

Usage : $CHATTERBOX_PYTHON ressemblance_voix.py --ref enregistrement.wav essai1.wav essai2.wav …
Affiche la similarité cosinus des empreintes vocales (1 = identique). Repères mesurés le 14/10/2026 contre
l'enregistrement complet de la voix du club : deux extraits de cette même voix 0,953 et 0,961 ; deux voix sans
rapport (Kokoro ff_siwis et un clone de celle-ci) 0,651 et 0,675. C'est un indicateur, pas un verdict : l'écoute
reste juge.
"""
import argparse

import librosa
import numpy as np
import torch
from chatterbox.models.voice_encoder import VoiceEncoder
from huggingface_hub import hf_hub_download


def empreinte(ve, chemin):
    # chargé directement à la fréquence de l'encodeur (16 kHz) : évite la dépendance resampy de librosa
    sr = ve.hp.sample_rate
    wav, _ = librosa.load(chemin, sr=sr, mono=True)
    return ve.embeds_from_wavs([wav], sr, as_spk=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", required=True)
    ap.add_argument("fichiers", nargs="+")
    a = ap.parse_args()
    ve = VoiceEncoder()
    ve.load_state_dict(torch.load(hf_hub_download("ResembleAI/chatterbox", "ve.pt"), map_location="cpu", weights_only=True))
    ve.eval()
    ref = empreinte(ve, a.ref)
    for f in a.fichiers:
        print(f"{float(np.dot(ref, empreinte(ve, f))):.3f}  {f}")


if __name__ == "__main__":
    main()
