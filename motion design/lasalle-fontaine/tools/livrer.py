"""Livraison fontaine LA SALLE : affiche 02/03 retravaillée (PNG + JPG) et story 9:16, 60 i/s (avec musique, bruitages seuls).

1. Affiche : snapshot de affiche-45 à 0,5 s → PNG maître et JPG (qualité 90, sRGB, < 1 Mo).
2. Story : l'image du rendu (story-916/renders/story.mp4) est reprise avec le WAV d'origine (le rendu HyperFrames baisse
   la musique de 1,6 dB), puis réencodée en H.264 60 i/s (master.py fixe 30 i/s ; mêmes réglages sinon, CRF 16).
   Version « bruitages seuls » à −18 LUFS pour ajouter une musique de la Sound Collection à la publication.
3. Contrôles : format, durée, poids, faststart, sonie, crête vraie, aperçu = rendu décodé (SSIM), textes, mots interdits,
   planche à 2 i/s avec les zones Reels, image 0.

Les fichiers montrent la photo fabricant de la fontaine (logo de la marque à l'écran) : images, vidéos et planches vont
dans « Pub Meta LA SALLE/Fontaine oct26/ », où ils sont ignorés par git (dépôt public). Le rapport QC est suivi.
Usage : python3 tools/livrer.py   (après build.py, musique.py, musique.py --bruitages et le rendu :
        npx --yes hyperframes@0.8.181 render --fps 60 --quality delivery -o renders/story.mp4, dans story-916)
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
LIVRAISON = os.path.normpath(os.path.join(RACINE, "..", "..", "Pub Meta LA SALLE", "Fontaine oct26"))
sys.path.insert(0, ICI)
sys.path.insert(1, os.path.join(RACINE, "..", "_sources-premium", "tools"))
import build  # noqa: E402
import master  # noqa: E402

HF = ["npx", "--yes", "hyperframes@0.8.181"]
NOM = "LA_SALLE_Fontaine"
ATTENDUS_AFFICHE = ["COMMENT ÇA MARCHE", "VOTRE BOISSON,", "À LA CARTE.", "ÉCRAN TACTILE 17″",
                    "Saveur, intensité, température : vous composez votre boisson.", "1 BOISSON / 30 MIN",
                    "À chaque séance, aussi souvent que vous venez.", "AU CHOIX", *build.BOISSONS, "5 SAVEURS",
                    "PASSION · PASTÈQUE · ICE TEA · ANANAS · MULTIFRUIT", build.MENTION_CAFEINE]
ATTENDUS_STORY = ["OPTION PREMIUM", "BIEN PLUS", "QUE DE", "L'EAU.", "La fontaine à boissons sportives de l'option Premium.",
                  "COMMENT ÇA MARCHE", "VOTRE BOISSON,", "À LA CARTE.", "ÉCRAN TACTILE 17″", *build.BOISSONS,
                  "ÉTAPE 02", "CHOISISSEZ", "VOTRE SAVEUR", *build.SAVEURS, "Cinq saveurs, au choix sur l'écran tactile.",
                  "ÉTAPE 03", "SERVEZ-VOUS", "1 BOISSON", "TOUTES LES", "30 MIN", "À chaque séance, aussi souvent que vous venez.",
                  "L'OPTION PREMIUM", "2 €", "TTC PAR SEMAINE", "Soit 8 € toutes les 4 semaines, en plus de votre abonnement.",
                  "3 AVANTAGES INCLUS", *[x for a in build.AVANTAGES for x in a], "ACTIVEZ-LA", "À L'ACCUEIL.",
                  "EN QUELQUES SECONDES.", "URBAN VALLEY · 7J/7 · 6H–23H", build.MENTION_CAFEINE, build.MENTION_OPTION]
# BRIEF Premium et frame.md : lexique interdit ; aucun effet attribué aux boissons
INTERDITS = ["fontaine à eau", "abonnement premium", "offre limitée", "inscription en ligne", "gratuit", "illimité",
             "minceur", "brûle", "kilo", "détox", "avant/après", "énergie", "récupération", "performance", "booster"]
TUTOIEMENT = r"\b(tu|ton|ta|tes|toi|t')\b"          # LA SALLE vouvoie


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
    h = re.sub(r'<(\w+)[^>]*class="[^"]*\b(kick|t8|t9)\b[^"]*"[^>]*>(.*?)</\1>',
               lambda m: " " + html.unescape(re.sub(r"<[^>]+>", "", m.group(3))).upper() + " ", h, flags=re.S)
    h = re.sub(r"<br\s*/?>", " ", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    t = t.replace(" ", " ").replace(" ", " ").replace("’", "'")
    return re.sub(r"\s+", " ", t)


def manquants(attendus, t):
    norm = lambda x: re.sub(r"\s+", " ", x.replace(" ", " ").replace(" ", " ").replace("’", "'"))
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
    r = subprocess.run(["ffmpeg", "-nostats", "-ss", f"{t:g}", "-i", video, "-i", image, "-frames:v", "1",
                        "-lavfi", "[0:v][1:v]ssim", "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"All:([0-9.]+)", r.stderr)
    return float(m.group(1)) if m else 0.0


def check(projet):
    """check HyperFrames (lint, rendu, mise en page, mouvement, contraste AA) : (réussi, résumé du contraste)."""
    r = subprocess.run(HF + ["check", "--timeout", "60000", os.path.join(RACINE, projet)], capture_output=True, text=True)
    sortie = r.stdout + r.stderr
    m = re.search(r"(\d+)/(\d+) text checks pass WCAG AA", sortie)
    return "Check passed" in sortie, (f"contraste AA {m.group(1)}/{m.group(2)}" if m else "contraste non mesuré")


def encoder(src, dst, duree):
    """Réglages de master.py (H.264 High, BT.709, faststart), mais à 60 i/s et en CRF 16 : les volets et les entrées
    restent nets, sans blocs sur les aplats sombres. Piste AAC copiée ; si l'encodage AAC fait dépasser la crête
    vraie de −1,5 dBTP, elle est réencodée avec un gain fixe abaissé de 0,3 dB à chaque essai (comme master.py)."""
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
    return [f"QC — {nom}", *(f"{'OK ' if ok else 'NON'}  {n}" for n, ok in tests),
            f"Verdict : {'GO technique' if all(ok for _, ok in tests) else 'À CORRIGER'}", ""]


def affiche(dimg, lignes):
    with tempfile.TemporaryDirectory() as tmp:
        run(HF + ["snapshot", "--at", "0.5", "--no-end", "-o", tmp, "--timeout", "60000", os.path.join(RACINE, "affiche-45")])
        png_tmp = os.path.join(tmp, "frame-00-at-0.5s.png")
        png = os.path.join(dimg, f"{NOM}_affiche_02-03_post_4x5.png")
        jpg = png[:-4] + ".jpg"
        run(["ffmpeg", "-v", "error", "-y", "-i", png_tmp, "-frames:v", "1", "-update", "1", png])
        run(["ffmpeg", "-v", "error", "-y", "-i", png_tmp, "-q:v", "2", jpg])
    _, s = sonde(jpg)
    verif = check("affiche-45")
    poids = os.path.getsize(jpg) / 1e6
    t = texte("affiche-45")
    absents = manquants(ATTENDUS_AFFICHE, t)
    interdits = trouves(t)
    lignes += ligne(os.path.basename(jpg) + " (+ PNG maître)", [
        ("Image 1080×1350 (4:5)", s["video"]["width"] == 1080 and s["video"]["height"] == 1350),
        (f"Poids JPG {poids:.2f} Mo (< 1)", poids < 1),
        (f"check HyperFrames passé, {verif[1]} (affiche-45)", verif[0] and verif[1].split()[-1].split("/")[0] == verif[1].split()[-1].split("/")[-1]),
        ("Textes de l'affiche d'origine, mot pour mot" + (f" (absents : {absents})" if absents else ""), not absents),
        ("Aucun mot interdit ni allégation" + (f" (trouvés : {interdits})" if interdits else ""), not interdits),
    ])


def story(dvid, dctl, lignes):
    rendu = os.path.join(RACINE, "story-916", "renders", "story.mp4")
    if not os.path.exists(rendu):
        sys.exit(f"Rendu absent : {rendu}")
    d = build.DUREE
    verif = check("story-916")
    t_ecran = texte("story-916")
    absents = manquants(ATTENDUS_STORY, t_ecran)
    interdits = trouves(t_ecran)
    with tempfile.TemporaryDirectory() as tmp:
        instants = [round(t + dur - build.VOLET / 2 - 0.1, 2) for _, t, dur in build.SCENES[:-1]] + [round(d - 0.4, 2)]
        run(HF + ["snapshot", "--at", ",".join(f"{t:g}" for t in instants), "--no-end", "-o", tmp, "--timeout", "60000",
                  os.path.join(RACINE, "story-916")])
        apercus = sorted(f for f in os.listdir(tmp) if f.startswith("frame-") and f.endswith(".png"))
        for version, wav in (("", "musique_fontaine.wav"), ("_bruitages", "bruitages_fontaine.wav")):
            video = os.path.join(dvid, f"{NOM}_story_9x16{version}.mp4")
            remix = os.path.join(tmp, f"remix{version}.mp4")
            run(["ffmpeg", "-hide_banner", "-y", "-i", rendu, "-i", os.path.join(RACINE, "_communs", wav),
                 "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                 "-t", f"{d:g}", remix])
            encoder(remix, video, d)
            p, s = sonde(video)
            v, a = s["video"], s["audio"]
            duree, taille = float(p["format"]["duration"]), int(p["format"]["size"]) / 1e6
            i, tp = master.controle(video)
            scores = [ssim(video, t, os.path.join(tmp, f)) for t, f in zip(instants, apercus)]
            cible = -18.0 if version else -14.0
            lignes += ligne(os.path.basename(video), [
                (f"Format 1080×1920, H.264 High, yuv420p, {build.FPS} i/s", v["width"] == 1080 and v["height"] == 1920 and v["codec_name"] == "h264"
                 and v.get("profile") == "High" and v["pix_fmt"] == "yuv420p" and v["r_frame_rate"] == f"{build.FPS}/1"),
                (f"Durée {duree:.3f} s ({d - 0.1:g}–{d:g})", d - 0.1 <= duree <= d + 0.001),
                (f"Poids {taille:.1f} Mo (≤ 25)", taille <= 25),
                ("faststart (moov avant mdat)", faststart(video)),
                (f"Audio AAC {a['sample_rate']} Hz, {a['channels']} canaux", a["codec_name"] == "aac" and a["sample_rate"] == "48000" and a["channels"] == 2),
                (f"Sonie {i:.1f} LUFS ({cible:g} ± 0,5)", abs(i - cible) <= 0.5),
                (f"Crête vraie {tp:.1f} dBTP (≤ −1,5)", tp <= -1.5),
                ("Aperçu = rendu décodé à la fin de chaque scène (SSIM " + ", ".join(f"{x:.3f}" for x in scores) + " ≥ 0,97)",
                 len(scores) == len(build.SCENES) and min(scores) >= 0.97),
                (f"check HyperFrames passé, {verif[1]} (story-916)", verif[0] and verif[1].split()[-1].split("/")[0] == verif[1].split()[-1].split("/")[-1]),
                ("Textes des 6 visuels présents" + (f" (absents : {absents})" if absents else ""), not absents),
                ("Aucun mot interdit ni allégation" + (f" (trouvés : {interdits})" if interdits else ""), not interdits),
            ])
    video = os.path.join(dvid, f"{NOM}_story_9x16.mp4")
    vf = ("fps=2,drawbox=x=0:y=0:w=1080:h=270:color=red@0.25:t=fill,drawbox=x=0:y=1250:w=1080:h=670:color=red@0.25:t=fill,"
          "drawbox=x=950:y=900:w=130:h=1020:color=red@0.25:t=fill,scale=216:384,tile=10x4")
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", vf, "-frames:v", "1", "-q:v", "3", os.path.join(dctl, "planche_story_2ips.jpg")])
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-frames:v", "1", "-q:v", "2", os.path.join(dctl, "image0_story.jpg")])


def main():
    dimg, dvid, dctl = (os.path.join(LIVRAISON, x) for x in ("images", "videos", "controles"))
    for x in (dimg, dvid, dctl):
        os.makedirs(x, exist_ok=True)
    lignes = []
    affiche(dimg, lignes)
    story(dvid, dctl, lignes)
    lignes.append("Reste à valider par Mehdi : les points ⚠ de A_valider.md, puis l'écoute de la musique (contrôlée par mesures seulement).")
    open(os.path.join(dctl, "QC_fontaine.txt"), "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print("\n".join(lignes))


if __name__ == "__main__":
    main()
