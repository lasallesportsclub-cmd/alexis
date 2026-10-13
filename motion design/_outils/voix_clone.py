"""Voix off avec la voix clonée (Chatterbox multilingue, licence MIT), en français par défaut.

Une phrase :
    $CHATTERBOX_PYTHON voix_clone.py --ref ref.wav --texte "Passez en version Premium." -o P1.wav
Un lot (une ligne par fichier, « nom|texte ») :
    $CHATTERBOX_PYTHON voix_clone.py --ref ref.wav --lot repliques.txt --dossier sortie/

Réglages utiles :
    --exageration 0.5   expressivité (0.3 posé · 0.5 naturel · 0.7 pub énergique)
    --cfg 0.5           fidélité au rythme de la référence (baisser à 0.3 si le débit est trop lent)
    --graine 7          même graine = même rendu, pour pouvoir refaire une réplique à l'identique
La référence : 10 à 20 s de voix propre, sans musique ni écho, dans le ton voulu (extrait des enregistrements du Drive).
Seules les voix dont la personne a signé l'autorisation de clonage peuvent servir de référence.
"""
import argparse
import os
import sys

import soundfile as sf
import torch
from chatterbox.mtl_tts import ChatterboxMultilingualTTS


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", help="enregistrement de référence (wav, mp3, m4a) ; sans lui, voix par défaut du modèle")
    ap.add_argument("--texte")
    ap.add_argument("-o", "--sortie", default="voix.wav")
    ap.add_argument("--lot", help="fichier texte « nom|texte » par ligne")
    ap.add_argument("--dossier", default=".")
    ap.add_argument("--langue", default="fr")
    ap.add_argument("--exageration", type=float, default=0.5)
    ap.add_argument("--cfg", type=float, default=0.5)
    ap.add_argument("--graine", type=int, default=7)
    a = ap.parse_args()
    if not a.texte and not a.lot:
        ap.error("--texte ou --lot est requis")

    jobs = []
    if a.lot:
        os.makedirs(a.dossier, exist_ok=True)
        for ligne in open(a.lot, encoding="utf-8"):
            if "|" in ligne and not ligne.lstrip().startswith("#"):
                nom, texte = ligne.split("|", 1)
                jobs.append((os.path.join(a.dossier, nom.strip() + ".wav"), texte.strip()))
    else:
        jobs.append((a.sortie, a.texte))

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = ChatterboxMultilingualTTS.from_pretrained(device=device)
    for sortie, texte in jobs:
        torch.manual_seed(a.graine)
        wav = model.generate(texte, language_id=a.langue, audio_prompt_path=a.ref,
                             exaggeration=a.exageration, cfg_weight=a.cfg)
        sf.write(sortie, wav.squeeze(0).cpu().numpy(), model.sr)
        print(f"{sortie} : {wav.shape[-1] / model.sr:.2f} s · « {texte} »", flush=True)


if __name__ == "__main__":
    sys.exit(main())
