"""Manifeste du dossier livré (controles/manifest.json) : images et vidéos, dimensions, poids, empreinte SHA-256.

Usage : python3 manifest.py
"""
import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from master import controle  # noqa: E402

ROOT = "/home/user/alexis/Pub Meta LA SALLE/Premium oct26"


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def dims(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                          "-of", "json", path], capture_output=True, text=True).stdout
    d = json.loads(out)
    return d["streams"][0]["width"], d["streams"][0]["height"], float(d["format"].get("duration", 0))


def main():
    fichiers = []
    for dossier in ("images/story", "images/post", "images/carrousel", "videos"):
        base = os.path.join(ROOT, dossier)
        for f in sorted(os.listdir(base)):
            p = os.path.join(base, f)
            w, h, dur = dims(p)
            e = {"fichier": f"{dossier}/{f}", "largeur": w, "hauteur": h, "octets": os.path.getsize(p), "sha256": sha(p)}
            if f.endswith(".mp4"):
                i, tp = controle(p)
                c = f.split("_")[3]
                e.update({"duree_s": round(dur, 3), "sonie_LUFS": i, "crete_vraie_dBTP": tp,
                          "source": f"motion design/{'premium-916' if h == 1920 else 'premium-45'}/{c}",
                          "audio": "bruitages seuls (sans voix ni musique, décision du 13/10/2026)"})
            else:
                e.update({"source": "motion design/" + ("premium-visuels-916" if h == 1920 else "premium-visuels-45"), "profil": "sRGB"})
            fichiers.append(e)
    m = {"kit": "Option Premium LA SALLE", "version": "v2 images et vidéos", "date": "2026-10-13",
         "statut": "à valider par Mehdi, non publié",
         "logo": "provisoire (signature 170 px du Drive) — voir A_valider.md",
         "decisions": ["vidéos sans voix ni musique, bruitages seuls (13/10/2026)",
                       "un seul fichier par vidéo : sans musique, les versions « avec » et « sans » musique seraient identiques"],
         "fichiers": fichiers,
         "en_attente": ["logo mono.png/word.png", "concept D (date du happening non fixée)"]}
    json.dump(m, open(os.path.join(ROOT, "controles", "manifest.json"), "w"), ensure_ascii=False, indent=2)
    print(len(fichiers), "fichiers")


if __name__ == "__main__":
    main()
