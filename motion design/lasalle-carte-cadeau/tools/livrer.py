"""Livraison des stories « carte cadeau » LA SALLE (accroches A, B, C ; 12 s, 1080×1920, 30 i/s).

Pour chaque accroche : l'image du rendu (<projet>/renders/story.mp4) reprise avec le WAV d'origine (le rendu HyperFrames
baisse la musique de 1,6 dB), encodée en H.264 High (CRF 16, BT.709, faststart), en version musique et bruitages seuls
(−18 LUFS, pour poser une musique de la Sound Collection dans Instagram). Contrôles : format, durée (12 s au plus),
poids, faststart, sonie, crête vraie, aperçu = rendu décodé (SSIM, image choisie par son numéro), check HyperFrames
(contraste AA), textes attendus, mots interdits et tutoiement ; planche à 4 i/s avec les zones Reels, image 0.

Fichiers dans « Pub Meta LA SALLE/Carte cadeau nov26/ » : vidéos ignorées par git (envoyées directement), planches,
images 0 et rapport controles/QC_carte_cadeau.txt suivis.

Usage : python3 tools/livrer.py   (après build.py, musique.py, musique.py --bruitages et, dans chaque projet,
        npx --yes hyperframes@0.8.181 render --fps 30 --quality delivery -o renders/story.mp4)
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
LIVRAISON = os.path.normpath(os.path.join(RACINE, "..", "..", "Pub Meta LA SALLE", "Carte cadeau nov26"))
sys.path.insert(0, ICI)
sys.path.insert(1, os.path.join(RACINE, "..", "_sources-premium", "tools"))
import build  # noqa: E402
import master  # noqa: E402

HF = ["npx", "--yes", "hyperframes@0.8.181"]
NOM = "LA_SALLE_Carte_cadeau_story"
COMMUNS = ["COMMENT ÇA MARCHE", "Valeur", *[f"{x} €" for x in build.MONTANTS], "MONTANT AU CHOIX", "CARTE CADEAU",
           "01", "02", "03", *build.ETAPES, "ET EN", "PLUS,", "POUR LA PERSONNE QUI LA REÇOIT", "LES FRAIS",
           "D'INSCRIPTION", "45 €", "OFFERTS.", "EN VENTE", "À L'ACCUEIL.", " · ".join(f"{x} €" for x in build.MONTANTS),
           "ou le montant de votre choix", build.INFOS.upper(), build.MENTION]
ATTENDUS = {"A": COMMUNS + ["CARTE CADEAU · NOËL", "OFFREZ", "LA SALLE."],
            "B": COMMUNS + ["CARTE CADEAU · NOËL", "VOUS NE", "SAVEZ PAS", "QUOI", "OFFRIR ?"],
            "C": COMMUNS + ["CARTE CADEAU · NOËL", "OFFREZ-LUI", "150 €", "SUR SON", "ABONNEMENT."]}
# BRIEF Premium et skill lasalle-pub-motion : lexique interdit ; LA SALLE vouvoie
INTERDITS = ["fontaine à eau", "abonnement premium", "offre limitée", "inscription en ligne", "gratuit", "illimité",
             "minceur", "brûle", "kilo", "détox", "avant/après", "maigrir", "perte de poids", "garanti"]
TUTOIEMENT = r"\b(tu|ton|ta|tes|toi|t')\b"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(" ".join(cmd[:4]) + "\n" + r.stderr[-2000:])
    return r.stdout


def texte(projet):
    """Texte à l'écran tel qu'affiché : capitales posées par le CSS (classes kick, t8, t9) rétablies."""
    dossier = os.path.join(RACINE, projet, "compositions")
    h = " ".join(open(os.path.join(dossier, f), encoding="utf-8").read() for f in sorted(os.listdir(dossier)))
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<br\s*/?>", " ", h)
    h = re.sub(r'<(\w+)[^>]*class="[^"]*\b(kick|t8|t9)\b[^"]*"[^>]*>(.*?)</\1>',
               lambda m: " " + html.unescape(re.sub(r"<[^>]+>", "", m.group(3))).upper() + " ", h, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    t = t.replace(" ", " ").replace(" ", " ").replace("’", "'")
    return re.sub(r"\s+", " ", t)


def manquants(attendus, t):
    norm = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))
                            .replace(" ", " ").replace(" ", " ").replace("’", "'")).strip()
    return [a for a in attendus if norm(a) not in t]


def trouves(t):
    t = t.lower()
    return [m for m in INTERDITS if m in t] + re.findall(TUTOIEMENT, t)


def sonde(f):
    p = json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration,size:stream=codec_type,codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
                        "-of", "json", f]))
    return p, {s["codec_type"]: s for s in p["streams"]}


def faststart(f):
    head = open(f, "rb").read(200000)
    return head.find(b"moov") != -1 and (head.find(b"mdat") == -1 or head.find(b"moov") < head.find(b"mdat"))


def ssim(video, t, image):
    """SSIM entre l'aperçu à l'instant t et l'image n° round(t × FPS) du rendu décodé."""
    with tempfile.TemporaryDirectory() as tmp:
        img = os.path.join(tmp, "rendu.png")
        run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", f"select=eq(n\\,{round(t * build.FPS)})", "-frames:v", "1", img])
        r = subprocess.run(["ffmpeg", "-nostats", "-i", img, "-i", image, "-lavfi", "[0:v][1:v]ssim", "-f", "null", "-"],
                           capture_output=True, text=True)
    m = re.search(r"All:([0-9.]+)", r.stderr)
    return float(m.group(1)) if m else 0.0


def check(projet):
    r = subprocess.run(HF + ["check", "--timeout", "60000", os.path.join(RACINE, projet)], capture_output=True, text=True)
    sortie = r.stdout + r.stderr
    m = re.search(r"(\d+)/(\d+) text checks pass WCAG AA", sortie)
    return "Check passed" in sortie, (f"contraste AA {m.group(1)}/{m.group(2)}" if m else "contraste non mesuré")


def encoder(src, dst, duree):
    """Réglages de master.py (H.264 High, BT.709, faststart), CRF 16. Piste AAC copiée ; si l'AAC fait dépasser la
    crête vraie de −1,5 dBTP, elle est réencodée avec un gain abaissé de 0,3 dB à chaque essai."""
    image = dst + ".image.mp4"
    run(["ffmpeg", "-hide_banner", "-y", "-i", src, "-t", f"{duree}", "-an",
         "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-maxrate", "20M", "-bufsize", "40M",
         "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", str(build.FPS),
         "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", image])
    gain = None
    for _ in range(6):
        audio = ["-c:a", "copy"] if gain is None else [
            "-af", f"volume={gain}dB,aresample=48000", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2"]
        run(["ffmpeg", "-hide_banner", "-y", "-i", image, "-i", src, "-map", "0:v", "-map", "1:a", "-t", f"{duree}",
             "-c:v", "copy", *audio, "-movflags", "+faststart", dst])
        if master.controle(dst)[1] <= master.TP_MAX:
            break
        gain = -0.3 if gain is None else round(gain - 0.3, 1)
    os.remove(image)


def ligne(nom, tests):
    return [f"== {nom}"] + [f"  {'OK ' if ok else 'ÉCHEC'} {libelle}" for libelle, ok in tests] + [""]


def story(cle, dvid, dctl, lignes):
    v = build.VARIANTES[cle]
    projet, d = v["projet"], build.DUREE
    rendu = os.path.join(RACINE, projet, "renders", "story.mp4")
    if not os.path.exists(rendu):
        sys.exit(f"Rendu absent : {rendu}")
    verif = check(projet)
    t_ecran = texte(projet)
    absents = manquants(ATTENDUS[cle], t_ecran)
    interdits = trouves(t_ecran)
    instants = [round(fin - 0.1, 2) for _, _, fin in build.SCENES] + [0.0, 3.1, 4.6, 8.2]
    nom = f"{NOM}_{v['nom']}_9x16"
    with tempfile.TemporaryDirectory() as tmp:
        run(HF + ["snapshot", "--at", ",".join(f"{t:g}" for t in instants), "--no-end", "-o", tmp, "--timeout", "60000",
                  os.path.join(RACINE, projet)])
        apercus = sorted((f for f in os.listdir(tmp) if f.startswith("frame-") and f.endswith(".png")), key=lambda f: int(f.split("-")[1]))
        for version, wav in (("", "musique"), ("_bruitages", "bruitages")):
            video = os.path.join(dvid, f"{nom}{version}.mp4")
            remix = os.path.join(tmp, f"remix{version}.mp4")
            run(["ffmpeg", "-hide_banner", "-y", "-i", rendu, "-i", os.path.join(RACINE, "_communs", f"{wav}_carte_cadeau.wav"),
                 "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                 "-t", f"{d:g}", remix])
            encoder(remix, video, d)
            p, s = sonde(video)
            vi, a = s["video"], s["audio"]
            duree, taille = float(p["format"]["duration"]), int(p["format"]["size"]) / 1e6
            i, tp = master.controle(video)
            scores = [ssim(video, t, os.path.join(tmp, f)) for t, f in zip(instants, apercus)]
            cible = -18.0 if version else -14.0
            lignes += ligne(os.path.basename(video), [
                (f"Format 1080×1920, H.264 High, yuv420p, {build.FPS} i/s", vi["width"] == 1080 and vi["height"] == 1920
                 and vi["codec_name"] == "h264" and vi.get("profile") == "High" and vi["pix_fmt"] == "yuv420p"
                 and vi["r_frame_rate"] == f"{build.FPS}/1"),
                (f"Durée {duree:.3f} s ({d - 0.1:g}–{d:g}, 12 s au plus)", d - 0.1 <= duree <= d + 0.001 and duree <= 12.001),
                (f"Poids {taille:.1f} Mo (≤ 25)", taille <= 25),
                ("faststart (moov avant mdat)", faststart(video)),
                (f"Audio AAC {a['sample_rate']} Hz, {a['channels']} canaux", a["codec_name"] == "aac" and a["sample_rate"] == "48000" and a["channels"] == 2),
                (f"Sonie {i:.1f} LUFS ({cible:g} ± 0,5)", abs(i - cible) <= 0.5),
                (f"Crête vraie {tp:.1f} dBTP (≤ −1,5)", tp <= -1.5),
                ("Aperçu = rendu décodé (SSIM " + ", ".join(f"{x:.3f}" for x in scores) + " ≥ 0,97)",
                 len(scores) == len(instants) and min(scores) >= 0.97),
                (f"check HyperFrames passé, {verif[1]} ({projet})", verif[0]),
                ("Textes présents" + (f" (absents : {absents})" if absents else ""), not absents),
                ("Aucun mot interdit ni tutoiement" + (f" (trouvés : {interdits})" if interdits else ""), not interdits),
            ])
    video = os.path.join(dvid, f"{nom}.mp4")
    vf = ("fps=4,drawbox=x=0:y=0:w=1080:h=270:color=red@0.25:t=fill,drawbox=x=0:y=1250:w=1080:h=670:color=red@0.25:t=fill,"
          "drawbox=x=950:y=900:w=130:h=1020:color=red@0.25:t=fill,scale=216:384,tile=12x4")
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", vf, "-frames:v", "1", "-q:v", "3",
         os.path.join(dctl, f"planche_{v['nom']}_4ips.jpg")])
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-frames:v", "1", "-q:v", "2", os.path.join(dctl, f"image0_{v['nom']}.jpg")])


def main():
    dvid, dctl = (os.path.join(LIVRAISON, x) for x in ("videos", "controles"))
    os.makedirs(dvid, exist_ok=True)
    os.makedirs(dctl, exist_ok=True)
    lignes = []
    for cle in build.VARIANTES:
        story(cle, dvid, dctl, lignes)
    lignes.append("Reste à valider : les points ⚠ de A_valider.md, puis l'écoute de la musique (contrôlée par mesures seulement).")
    open(os.path.join(dctl, "QC_carte_cadeau.txt"), "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print("\n".join(lignes))


if __name__ == "__main__":
    main()
