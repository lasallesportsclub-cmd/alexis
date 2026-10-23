"""Livraison de la pub LE CUBE tirée du film V1, une vidéo par variante : piste son d'origine, mastering, contrôle.

1. Le rendu HyperFrames baisse la musique d'un gain fixe : l'image du rendu est reprise avec la musique d'origine
   (_communs/musique_v1_<V>.wav, −14 LUFS, crête ≤ −1,5 dBTP), puis master.py (Premium) en mode direct.
2. Contrôle : format, durée, poids, faststart, sonie, crête vraie, textes à l'écran, mots interdits, et rendu décodé
   comparé à l'aperçu HyperFrames aux mêmes instants (SSIM, règle des skills HyperFrames d'octobre 2026).
3. Planche à 2 i/s avec les zones masquées par Reels, image 0.

Tant que le film n'est pas dans ~/lecube-sources/v1/, la vidéo est une animatique (cartons à la place des plans) :
son nom finit par _ANIMATIQUE. Avec le film, elle montre des personnes : elle va dans « Pub Meta LE CUBE/Film V1 oct26/ »,
où les MP4 et les images de contrôle sont ignorés par git (dépôt public). Le rapport QC_v1.txt, lui, est suivi.
Usage : python3 tools/livrer.py [A B C]   (après tools/build.py et le rendu de chaque variante :
        npx --yes hyperframes@0.8.181 render --quality delivery -o renders/v1-<V>.mp4, dans v1-<V>/)
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
MOTION = os.path.normpath(os.path.join(RACINE, ".."))
LIVRAISON = os.path.normpath(os.path.join(MOTION, "..", "Pub Meta LE CUBE", "Film V1 oct26"))
CONTROLES = os.path.join(LIVRAISON, "controles")
sys.path.insert(0, os.path.join(MOTION, "_sources-premium", "tools"))
import master  # noqa: E402

_spec = importlib.util.spec_from_file_location("livrer_disciplines", os.path.join(MOTION, "lecube-disciplines", "tools", "livrer.py"))
LD = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(LD)

HF = ["npx", "--yes", re.search(r"hyperframes@[0-9.]+", open(os.path.join(RACINE, "v1-A", "package.json")).read()).group()]
INSTANTS = [0.0, 0.6, 2.6, 3.6, 5.2, 6.6, 8.0, 8.7, 9.6, 10.9, 12.0, 14.4]   # une image par plan ou par bloc
COMMUNS = ["LE CUBE · CONFLANS", "ET TOI ?", "RÉSERVE TA", "SÉANCE D'ESSAI"]
INTERDITS = LD.INTERDITS + ["abonnement", "sans engagement", "inscription en ligne"]


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        sys.exit(f"Échec : {' '.join(cmd)}\n{p.stderr[-2000:]}")
    return p.stdout


def attendus(C, v):
    l = [x["texte"] for p in C["accroches"][v]["plans"] for x in p["lignes"]]
    for e in C["etapes"]:
        l += [e["numero"], e["ligne1"], e["ligne2"]]
    for lignes in C["argument"]["lignes"]:
        l += lignes
    return COMMUNS + l + [C["carte_titre"], C["carte_sous"], C["carte_adresse"]]


def ssim(video, png, t):
    p = subprocess.run(["ffmpeg", "-nostats", "-ss", f"{t:g}", "-i", video, "-i", png, "-frames:v", "1",
                        "-lavfi", "[0:v][1:v]ssim", "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"All:([0-9.]+)", p.stderr)
    return float(m.group(1)) if m else 0.0


def livrer(C, v):
    proj = os.path.join(RACINE, f"v1-{v}")
    film = os.path.isdir(os.path.join(proj, "assets", "video"))
    nom = f"LE_CUBE_V1_{v}_story_9x16{'' if film else '_ANIMATIQUE'}.mp4"
    video = os.path.join(LIVRAISON, nom)
    for vieux in (f"LE_CUBE_V1_{v}_story_9x16.mp4", f"LE_CUBE_V1_{v}_story_9x16_ANIMATIQUE.mp4"):
        if os.path.exists(os.path.join(LIVRAISON, vieux)):
            os.remove(os.path.join(LIVRAISON, vieux))
    with tempfile.TemporaryDirectory() as tmp:
        remix = os.path.join(tmp, "remix.mp4")
        run(["ffmpeg", "-hide_banner", "-y", "-i", os.path.join(proj, "renders", f"v1-{v}.mp4"),
             "-i", os.path.join(RACINE, "_communs", f"musique_v1_{v}.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
             "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-t", "15", remix])
        master.main(remix, video, 15.0)
        # Aperçu HyperFrames et rendu décodé aux mêmes instants (captures jetables : dossier temporaire)
        run(HF + ["snapshot", "--at", ",".join(f"{t:g}" for t in INSTANTS), "--no-end", "-o", tmp, "--timeout", "60000", proj])
        pngs = sorted(f for f in os.listdir(tmp) if f.startswith("frame-") and f.endswith(".png"))
        scores = [ssim(video, os.path.join(tmp, f), t) for f, t in zip(pngs, INSTANTS)]

    p = json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration,size:stream=codec_type,codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
                        "-of", "json", video]))
    vi = next(s for s in p["streams"] if s["codec_type"] == "video")
    a = next(s for s in p["streams"] if s["codec_type"] == "audio")
    duree, taille = float(p["format"]["duration"]), int(p["format"]["size"]) / 1e6
    head = open(video, "rb").read(200000)
    faststart = head.find(b"moov") != -1 and (head.find(b"mdat") == -1 or head.find(b"moov") < head.find(b"mdat"))
    i, tp = master.controle(video)
    t = LD.texte_ecran(os.path.join("..", "lecube-v1", f"v1-{v}"))
    absents = [m for m in attendus(C, v) if m.replace("’", "'") not in t]
    interdits = [m for m in INTERDITS if m.lower() in f" {t.lower()} "]
    pire = min(scores) if len(scores) == len(INSTANTS) else 0.0
    tests = [
        ("Format 1080×1920, H.264 High, yuv420p, 30 i/s", vi["width"] == 1080 and vi["height"] == 1920 and vi["codec_name"] == "h264"
         and vi.get("profile") == "High" and vi["pix_fmt"] == "yuv420p" and vi["r_frame_rate"] == "30/1"),
        (f"Durée {duree:.3f} s (14,90–15,00)", 14.9 <= duree <= 15.0),
        (f"Poids {taille:.1f} Mo (≤ 25)", taille <= 25),
        ("faststart (moov avant mdat)", faststart),
        (f"Audio AAC {a['sample_rate']} Hz, {a['channels']} canaux", a["codec_name"] == "aac" and a["sample_rate"] == "48000" and a["channels"] == 2),
        (f"Sonie {i:.1f} LUFS (−14 ± 0,5)", abs(i + 14) <= 0.5),
        (f"Crête vraie {tp:.1f} dBTP (≤ −1,5)", tp <= -1.5),
        (f"Rendu décodé = aperçu sur {len(scores)} instants (SSIM mini {pire:.3f} ≥ 0,97)", pire >= 0.97),
        ("Textes attendus présents" + (f" (absents : {absents})" if absents else ""), not absents),
        ("Aucun mot interdit" + (f" (trouvés : {interdits})" if interdits else ""), not interdits),
    ]
    vf = ("fps=2,drawbox=x=0:y=0:w=1080:h=270:color=red@0.25:t=fill,drawbox=x=0:y=1250:w=1080:h=670:color=red@0.25:t=fill,"
          "drawbox=x=950:y=900:w=130:h=1020:color=red@0.25:t=fill,scale=216:384,tile=10x3")
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", vf, "-frames:v", "1", "-q:v", "3", os.path.join(CONTROLES, f"planche_v1_{v}_2ips.jpg")])
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-frames:v", "1", "-q:v", "2", os.path.join(CONTROLES, f"image0_v1_{v}.jpg")])
    ok = all(x for _, x in tests)
    return [f"QC — {nom} (variante {v} : « {C['accroches'][v]['titre']} »)",
            f"     Images : {'plans du film V1' if film else 'ANIMATIQUE, cartons numérotés à la place des plans du film'}",
            *(f"{'OK ' if x else 'NON'}  {n}" for n, x in tests),
            f"Verdict : {('GO technique' if film else 'GO technique de l’animatique (pas encore diffusable)') if ok else 'À CORRIGER'}", ""]


def main():
    C = json.load(open(os.path.join(ICI, "cues_v1.json"), encoding="utf-8"))
    os.makedirs(CONTROLES, exist_ok=True)
    lignes = []
    for v in sys.argv[1:] or list(C["accroches"]):
        lignes += livrer(C, v)
    lignes.append("Reste à valider par Mehdi : les points ⚠ de A_valider.md (droit à l'image et contrat RM Visual d'abord), "
                  "puis l'écoute de la musique.")
    open(os.path.join(CONTROLES, "QC_v1.txt"), "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print("\n".join(lignes))


if __name__ == "__main__":
    main()
