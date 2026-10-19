"""Livraison des trois versions de la pub LE CUBE « LE CHRONO » : piste son d'origine, mastering, contrôle.

1. Le rendu HyperFrames 0.8.174 baisse la musique d'un gain fixe (−1,6 dB mesuré). L'image du rendu est donc
   reprise avec la musique d'origine (_communs/assets/audio/musique.wav, −14 LUFS, crête ≤ −1,5 dBTP).
2. master.py (Premium) passe alors en mode direct : pas de loudnorm dynamique sur la musique.
3. Contrôle : format, durée, poids, faststart, sonie, crête vraie, textes à l'écran, mots interdits.

Écrit dans « Pub Meta LE CUBE/Chrono oct26/ » : LE_CUBE_Chrono_<V>_story_9x16.mp4, et dans controles/ :
QC_videos.txt, planche_<V>_2ips.jpg (zones Reels en rouge) et image0_<V>.jpg.
Usage : python3 tools/livrer.py [A B C]
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
PROJET = os.path.normpath(os.path.join(ICI, ".."))
LIVRAISON = os.path.normpath(os.path.join(PROJET, "..", "..", "Pub Meta LE CUBE", "Chrono oct26"))
CONTROLES = os.path.join(LIVRAISON, "controles")
MUSIQUE = os.path.join(PROJET, "_communs", "assets", "audio", "musique.wav")
sys.path.insert(0, os.path.join(PROJET, "..", "_sources-premium", "tools"))
import master  # noqa: E402

COMMUNS = ["LE CUBE · CONFLANS", "00:15", "00:00", "ROUND 1", "CROSSFIT CSH", "WOD · HALTÉRO · GYM", "ROUND 2", "HYROX",
           "ENDURANCE · ENGINE · SIMULATION", "ROUND 3", "BOXING CLUB", "ANGLAISE · KICK · MMA · MUAY THAÏ", "ROUND 4",
           "POLE DANCE", "DE L'INITIATION À L'INTER · CERCEAU", "ET TOI ?", "PAS BESOIN D'ÊTRE EN FORME POUR COMMENCER.",
           "C'EST POUR ÇA QU'ON EST LÀ.", "CROSSFIT CSH · HYROX · BOXING CLUB · POLE DANCE", "RÉSERVE TA SÉANCE D'ESSAI",
           "ZAC DES BOUTRIES · CONFLANS-SAINTE-HONORINE"]
ACCROCHES = {"A": ["165", "COURS", "EN UNE SEMAINE.", "UN SEUL LIEU."],
             "B": ["T'AS 15 SECONDES ?", "ON TE MONTRE TOUT."],
             "C": ["BOXING CLUB CONFLANS", "50 m²", "400 m²", "ÇA CHANGE TOUT."]}
INTERDITS = ["€", "gratuit", "offre", "promo", "abonnement premium", "illimité", "garanti", "minceur", "kilo",
             "fontaine", "résultat", " vous ", " votre ", " vos "]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    return r.stdout


def texte_ecran(v):
    dossier = os.path.join(PROJET, v, "compositions")
    h = " ".join(open(os.path.join(dossier, f), encoding="utf-8").read() for f in sorted(os.listdir(dossier)))
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<br\s*/?>", " ", h)
    t = html.unescape(re.sub(r"<[^>]+>", "", h)).replace(" ", " ").replace(" ", " ").replace("’", "'")
    return re.sub(r"\s+", " ", t)


def livrer(v, tmp):
    rendu = os.path.join(PROJET, v, "renders", f"{v}.mp4")
    remix = os.path.join(tmp, f"{v}.mp4")
    sortie = os.path.join(LIVRAISON, f"LE_CUBE_Chrono_{v}_story_9x16.mp4")
    run(["ffmpeg", "-hide_banner", "-y", "-i", rendu, "-i", MUSIQUE, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-t", "15", remix])
    master.main(remix, sortie, 15.0)
    return sortie


def controler(v, video):
    p = json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration,size:stream=codec_type,codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
                        "-of", "json", video]))
    vi = next(s for s in p["streams"] if s["codec_type"] == "video")
    a = next(s for s in p["streams"] if s["codec_type"] == "audio")
    duree, taille = float(p["format"]["duration"]), int(p["format"]["size"]) / 1e6
    head = open(video, "rb").read(200000)
    faststart = head.find(b"moov") != -1 and (head.find(b"mdat") == -1 or head.find(b"moov") < head.find(b"mdat"))
    i, tp = master.controle(video)
    t = texte_ecran(v)
    absents = [m for m in COMMUNS + ACCROCHES[v] if m not in t]
    interdits = [m for m in INTERDITS if m.lower() in f" {t.lower()} "]
    tests = [
        ("Format 1080×1920, H.264 High, yuv420p, 30 i/s", vi["width"] == 1080 and vi["height"] == 1920 and vi["codec_name"] == "h264"
         and vi.get("profile") == "High" and vi["pix_fmt"] == "yuv420p" and vi["r_frame_rate"] == "30/1"),
        (f"Durée {duree:.3f} s (14,90–15,00)", 14.9 <= duree <= 15.0),
        (f"Poids {taille:.1f} Mo (≤ 25)", taille <= 25),
        ("faststart (moov avant mdat)", faststart),
        (f"Audio AAC {a['sample_rate']} Hz, {a['channels']} canaux", a["codec_name"] == "aac" and a["sample_rate"] == "48000" and a["channels"] == 2),
        (f"Sonie {i:.1f} LUFS (−14 ± 0,5)", abs(i + 14) <= 0.5),
        (f"Crête vraie {tp:.1f} dBTP (≤ −1,5)", tp <= -1.5),
        ("Textes attendus présents" + (f" (absents : {absents})" if absents else ""), not absents),
        ("Aucun mot interdit" + (f" (trouvés : {interdits})" if interdits else ""), not interdits),
    ]
    vf = ("fps=2,drawbox=x=0:y=0:w=1080:h=270:color=red@0.25:t=fill,drawbox=x=0:y=1250:w=1080:h=670:color=red@0.25:t=fill,"
          "drawbox=x=950:y=900:w=130:h=1020:color=red@0.25:t=fill,scale=216:384,tile=10x3")
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", vf, "-frames:v", "1", "-q:v", "3",
         os.path.join(CONTROLES, f"planche_{v}_2ips.jpg")])
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-frames:v", "1", "-q:v", "2", os.path.join(CONTROLES, f"image0_{v}.jpg")])
    return [f"QC — {os.path.basename(video)}", *(f"{'OK ' if ok else 'NON'}  {nom}" for nom, ok in tests),
            f"Verdict : {'GO technique' if all(ok for _, ok in tests) else 'À CORRIGER'}", ""]


def main():
    versions = sys.argv[1:] or ["A", "B", "C"]
    os.makedirs(CONTROLES, exist_ok=True)
    lignes = []
    with tempfile.TemporaryDirectory() as tmp:
        for v in versions:
            lignes += controler(v, livrer(v, tmp))
    lignes.append("Reste à valider par Mehdi : les points ⚠ de A_valider.md, puis l'écoute de la musique.")
    rapport = "\n".join(lignes)
    open(os.path.join(CONTROLES, "QC_videos.txt"), "w", encoding="utf-8").write(rapport + "\n")
    print(rapport)


if __name__ == "__main__":
    main()
