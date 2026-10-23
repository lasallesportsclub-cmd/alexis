"""Livraison et contrôle de la pub « Vos questions » v2 (sans avis Google) : musique d'origine, mastering, fichier,
sonie, texte à l'écran, planche avec zones Reels.

Le rendu HyperFrames (renders/video.mp4) est repris avec la musique d'origine (assets/audio/musique.wav), puis master.py
en mode direct. Écrit dans « Pub Meta LA SALLE/Vos questions v2 nov26/controles/ » : QC_video.txt, planche_2ips.jpg (zones Reels
superposées : haut 270 px, bas au-delà de 1250 px, colonne d'icônes à droite) et image0.jpg.
Usage : python3 tools/qc.py
"""
import html
import json
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
PROJET = os.path.normpath(os.path.join(ICI, ".."))
LIVRAISON = os.path.normpath(os.path.join(PROJET, "..", "..", "Pub Meta LA SALLE", "Vos questions v2 nov26"))
VIDEO = os.path.join(LIVRAISON, "LA_SALLE_Vos_questions_v2_story_9x16.mp4")
CONTROLES = os.path.join(LIVRAISON, "controles")
sys.path.insert(0, os.path.join(PROJET, "..", "_sources-premium", "tools"))
import master  # noqa: E402
from master import controle  # noqa: E402
import tempfile

PRESENCES = ["Vous ouvrez à quelle heure", "6H – 23H", "7J/7", "C’est grand", "1 200 m²", "MUSCULATION · CARDIO",
             "Et si je n’aime pas la muscu", "COURS COLLECTIFS", "BODYPUMP · RPM · PILATES", "Je peux essayer avant",
             "SÉANCE D’ESSAI", "OFFERTE À L’ACCUEIL",
             "Je peux passer voir", "AVEC PLAISIR.", "ON VOUS ATTEND !", "UNE QUESTION ?", "ÉCRIVEZ-NOUS.",
             "URBAN VALLEY · CONFLANS-SAINTE-HONORINE", "Conversation mise en scène."]
INTERDITS = ["€", "gratuit", "offre ", "promo", "avis", "inscription en ligne", "abonnement premium", "illimité", "garanti",
             "minceur", "kilo", " tu ", " ton ", " ta "]


def texte_ecran():
    dossier = os.path.join(PROJET, "compositions", "frames")
    h = " ".join(open(os.path.join(dossier, f), encoding="utf-8").read() for f in sorted(os.listdir(dossier)))
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<br\s*/?>", " ", h)
    t = html.unescape(re.sub(r"<[^>]+>", "", h)).replace(" ", " ")
    return re.sub(r"\s+", " ", t)


def livrer():
    with tempfile.TemporaryDirectory() as tmp:
        remix = os.path.join(tmp, "remix.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PROJET, "renders", "video.mp4"),
                        "-i", os.path.join(PROJET, "assets", "audio", "musique.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-t", "15", remix], check=True)
        master.main(remix, VIDEO, 15.0)


def main():
    os.makedirs(CONTROLES, exist_ok=True)
    livrer()
    p = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                   "format=duration,size:stream=codec_type,codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
                                   "-of", "json", VIDEO], capture_output=True, text=True).stdout)
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    a = next(s for s in p["streams"] if s["codec_type"] == "audio")
    duree, taille = float(p["format"]["duration"]), int(p["format"]["size"]) / 1e6
    head = open(VIDEO, "rb").read(200000)
    faststart = head.find(b"moov") != -1 and (head.find(b"mdat") == -1 or head.find(b"moov") < head.find(b"mdat"))
    i, tp = controle(VIDEO)
    t = texte_ecran()
    absents = [m for m in PRESENCES if m not in t]
    interdits = [m for m in INTERDITS if m.lower() in f" {t.lower()} "]
    tests = [
        ("Format 1080×1920, H.264 High, yuv420p, 30 i/s", v["width"] == 1080 and v["height"] == 1920 and v["codec_name"] == "h264"
         and v.get("profile") == "High" and v["pix_fmt"] == "yuv420p" and v["r_frame_rate"] == "30/1"),
        (f"Durée {duree:.3f} s (14,90–15,00)", 14.9 <= duree <= 15.0),
        (f"Poids {taille:.1f} Mo (≤ 25)", taille <= 25),
        ("faststart (moov avant mdat)", faststart),
        (f"Audio AAC {a['sample_rate']} Hz, {a['channels']} canaux", a["codec_name"] == "aac" and a["sample_rate"] == "48000" and a["channels"] == 2),
        (f"Sonie {i:.1f} LUFS (−14 ± 0,5)", abs(i + 14) <= 0.5),
        (f"Crête vraie {tp:.1f} dBTP (≤ −1,5)", tp <= -1.5),
        ("Textes attendus présents" + (f" (absents : {absents})" if absents else ""), not absents),
        ("Aucun mot interdit" + (f" (trouvés : {interdits})" if interdits else ""), not interdits),
    ]
    lignes = [f"{'OK ' if ok else 'NON'}  {nom}" for nom, ok in tests]
    verdict = "GO technique" if all(ok for _, ok in tests) else "À CORRIGER"
    rapport = "\n".join(["QC — LA_SALLE_Vos_questions_v2_story_9x16.mp4", *lignes, "", f"Verdict : {verdict}",
                         "Reste à valider par Mehdi : horaires, surface, cours cités, séance d'essai offerte, puis l'écoute de la musique."])
    open(os.path.join(CONTROLES, "QC_video.txt"), "w", encoding="utf-8").write(rapport + "\n")
    print(rapport)

    # planche 2 i/s avec les zones Reels, et image 0
    vf = ("fps=2,drawbox=x=0:y=0:w=1080:h=270:color=red@0.25:t=fill,drawbox=x=0:y=1250:w=1080:h=670:color=red@0.25:t=fill,"
          "drawbox=x=950:y=900:w=130:h=1020:color=red@0.25:t=fill,scale=216:384,tile=10x3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VIDEO, "-vf", vf, "-frames:v", "1", "-q:v", "3",
                    os.path.join(CONTROLES, "planche_2ips.jpg")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VIDEO, "-frames:v", "1", "-q:v", "2",
                    os.path.join(CONTROLES, "image0.jpg")], check=True)


if __name__ == "__main__":
    main()
