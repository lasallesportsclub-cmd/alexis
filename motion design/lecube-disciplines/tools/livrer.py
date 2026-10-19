"""Livraison des pubs LE CUBE par discipline, une vidéo par variante : piste son d'origine, mastering, contrôle.

1. Le rendu HyperFrames 0.8.174 baisse la musique d'un gain fixe (−1,6 dB). L'image du rendu est reprise avec la musique
   d'origine (_communs/musique_<discipline>_<V>.wav, −14 LUFS, crête ≤ −1,5 dBTP).
2. master.py (Premium) passe alors en mode direct : pas de loudnorm dynamique sur la musique.
3. Contrôle : format, durée, poids, faststart, sonie, crête vraie, textes à l'écran, mots interdits.

La vidéo montre des personnes : elle va dans « Pub Meta LE CUBE/Disciplines oct26/ », où les MP4 et les images de
contrôle sont ignorés par git (dépôt public). Le rapport QC_<discipline>.txt, lui, est suivi.
Usage : python3 tools/livrer.py pole [A B C D]
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
LIVRAISON = os.path.normpath(os.path.join(RACINE, "..", "..", "Pub Meta LE CUBE", "Disciplines oct26"))
CONTROLES = os.path.join(LIVRAISON, "controles")
sys.path.insert(0, os.path.join(RACINE, "..", "_sources-premium", "tools"))
import master  # noqa: E402

COMMUNS = ["LE CUBE", "ET TOI ?", "RÉSERVE TA", "SÉANCE D'ESSAI", "AU CUBE · CONFLANS",
           "LE CUBE · ZAC DES BOUTRIES · CONFLANS-SAINTE-HONORINE"]
INTERDITS = ["€", "gratuit", "offre", "promo", "abonnement premium", "illimité", "garanti", "minceur", "kilo",
             "fontaine", "résultat", " vous ", " votre ", " vos "]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    return r.stdout


def texte_ecran(d):
    dossier = os.path.join(RACINE, d, "compositions")
    h = " ".join(open(os.path.join(dossier, f), encoding="utf-8").read() for f in sorted(os.listdir(dossier)))
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<br\s*/?>", " ", h)
    t = html.unescape(re.sub(r"<[^>]+>", "", h)).replace(" ", " ").replace(" ", " ").replace("’", "'")
    return re.sub(r"\s+", " ", t)


def attendus(C, v):
    l = [x["texte"] for p in C["accroches"][v]["plans"] for x in p["lignes"]] + [C["discipline"], C["carte_detail"]]
    for e in C["etapes"]:
        l += [e["numero"], e["ligne1"], e["ligne2"]]
    for lignes in C["argument"]["lignes"]:
        l += lignes
    return COMMUNS + l


def livrer(C, d, v):
    nom = f"LE_CUBE_{C['discipline'].title().replace(' ', '_')}_{v}_story_9x16.mp4"
    video = os.path.join(LIVRAISON, nom)
    with tempfile.TemporaryDirectory() as tmp:
        remix = os.path.join(tmp, "remix.mp4")
        run(["ffmpeg", "-hide_banner", "-y", "-i", os.path.join(RACINE, f"{d}-{v}", "renders", f"{d}-{v}.mp4"),
             "-i", os.path.join(RACINE, "_communs", f"musique_{d}_{v}.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
             "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-t", "15", remix])
        master.main(remix, video, 15.0)

    p = json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration,size:stream=codec_type,codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
                        "-of", "json", video]))
    vi = next(s for s in p["streams"] if s["codec_type"] == "video")
    a = next(s for s in p["streams"] if s["codec_type"] == "audio")
    duree, taille = float(p["format"]["duration"]), int(p["format"]["size"]) / 1e6
    head = open(video, "rb").read(200000)
    faststart = head.find(b"moov") != -1 and (head.find(b"mdat") == -1 or head.find(b"moov") < head.find(b"mdat"))
    i, tp = master.controle(video)
    t = texte_ecran(f"{d}-{v}")
    absents = [m for m in attendus(C, v) if m.replace("’", "'") not in t]
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
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", vf, "-frames:v", "1", "-q:v", "3", os.path.join(CONTROLES, f"planche_{d}_{v}_2ips.jpg")])
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-frames:v", "1", "-q:v", "2", os.path.join(CONTROLES, f"image0_{d}_{v}.jpg")])
    return [f"QC — {nom} (variante {v} : « {C['accroches'][v]['titre']} »)", *(f"{'OK ' if ok else 'NON'}  {n}" for n, ok in tests),
            f"Verdict : {'GO technique' if all(ok for _, ok in tests) else 'À CORRIGER'}", ""]


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "pole"
    C = json.load(open(os.path.join(ICI, f"cues_{d}.json"), encoding="utf-8"))
    os.makedirs(CONTROLES, exist_ok=True)
    lignes = []
    for v in sys.argv[2:] or list(C["accroches"]):
        lignes += livrer(C, d, v)
    lignes.append("Reste à valider par Mehdi : les points ⚠ de A_valider.md (droit à l'image d'abord), puis l'écoute de la musique.")
    open(os.path.join(CONTROLES, f"QC_{d}.txt"), "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print("\n".join(lignes))


if __name__ == "__main__":
    main()
