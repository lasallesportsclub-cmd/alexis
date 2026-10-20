"""Livraison des stories « Nutrimuscle et Nutripure, disponibles à l'accueil » : images, vidéos et contrôle.

1. Images : une capture à la fin de chaque scène (t = 5N − 0,4 s), tout est en place → JPG 1080×1920.
2. Vidéos : le rendu de 20 s (renders/nutrition.mp4) est découpé en 4 stories de 5 s, réencodées pour une coupe
   exacte, avec une piste son muette (la musique s'ajoute dans Instagram).
3. Contrôle : format, durée, poids, faststart, textes attendus, mots interdits, planche des 4 images.

Les images et vidéos montrent le visuel partenaire Nutripure (avec ses modèles) et l'étagère de l'accueil : elles vont
dans « Pub Meta LA SALLE/Nutrition accueil oct26/ », où les JPG et MP4 sont ignorés par git (dépôt public).
Usage : python3 tools/livrer.py   (après tools/build.py et le rendu : npx hyperframes@0.8.174 render --quality delivery -o renders/nutrition.mp4)
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
LIVRAISON = os.path.normpath(os.path.join(RACINE, "..", "..", "Pub Meta LA SALLE", "Nutrition accueil oct26"))
HF = ["npx", "--yes", "hyperframes@0.8.174"]
DUREE = 5.0
STORIES = [("s1", "1_marques"), ("s2", "2_nutrimuscle"), ("s3", "3_nutripure"), ("s4", "4_question")]
ATTENDUS = {
    "s1": ["DISPONIBLES À L'ACCUEIL", "NUTRIMUSCLE", "NUTRIPURE", "LA SALLE · Urban Valley"],
    "s2": ["NUTRIMUSCLE", "NATIVE WHEY PROTIMUSCLE", "CRÉATINE CREAPURE®", "DISPONIBLE À L'ACCUEIL DE LA SALLE"],
    "s3": ["NUTRIPURE", "MUSCLE PROTEIN", "Disponible", "à l'accueil de LA SALLE"],
    "s4": ["UNE QUESTION", "PRODUIT ?", "NUTRIMUSCLE", "NUTRIPURE", "Conflans-Sainte-Honorine"],
}
# Lexique interdit (BRIEF Premium LA SALLE) + allégations : aucun effet promis, aucun prix, pas de tutoiement
INTERDITS = ["€", "gratuit", "offre", "promo", "remise", "illimité", "minceur", "brûle", "kilo", "détox", "avant/après",
             "fontaine à eau", "abonnement premium", "inscription en ligne", "récupération", "performance", "énergie",
             "garanti", "résultat", "prise de masse", "sèche", " tu ", " ton ", " ta ", " tes ", " toi "]


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        sys.exit(f"Échec : {' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r.stdout


def texte(cid):
    h = open(os.path.join(RACINE, "compositions", f"{cid}.html"), encoding="utf-8").read()
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<br\s*/?>", " ", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h)).replace(" ", " ").replace(" ", " ").replace("’", "'")
    return re.sub(r"\s+", " ", t)


def sonde(f):
    p = json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration,size:stream=codec_type,codec_name,profile,width,height,r_frame_rate,pix_fmt",
                        "-of", "json", f]))
    return p, {s["codec_type"]: s for s in p["streams"]}


def main():
    rendu = os.path.join(RACINE, "renders", "nutrition.mp4")
    if not os.path.exists(rendu):
        sys.exit(f"Rendu absent : {rendu}")
    dimg, dvid, dctl = (os.path.join(LIVRAISON, d) for d in ("images", "videos", "controles"))
    for d in (dimg, dvid, dctl):
        os.makedirs(d, exist_ok=True)

    lignes, images = [], []
    with tempfile.TemporaryDirectory() as tmp:
        instants = [round((i + 1) * DUREE - 0.4, 2) for i in range(len(STORIES))]
        run(HF + ["snapshot", "--at", ",".join(f"{t:g}" for t in instants), "--no-end", "-o", tmp, "--timeout", "60000", RACINE])
        pngs = sorted(f for f in os.listdir(tmp) if f.startswith("frame-") and f.endswith(".png"))
        if len(pngs) != len(STORIES):
            sys.exit(f"Captures inattendues : {pngs}")
        for (cid, nom), png in zip(STORIES, pngs):
            jpg = os.path.join(dimg, f"LA_SALLE_Nutrition_{nom}_story_9x16.jpg")
            run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(tmp, png), "-q:v", "2", jpg])
            images.append(jpg)

    for i, (cid, nom) in enumerate(STORIES):
        mp4 = os.path.join(dvid, f"LA_SALLE_Nutrition_{nom}_story_9x16.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{i * DUREE:g}", "-t", f"{DUREE:g}", "-i", rendu,
             "-f", "lavfi", "-t", f"{DUREE:g}", "-i", "anullsrc=r=48000:cl=stereo",
             "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "17",
             "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "-shortest", mp4])
        p, s = sonde(mp4)
        v, a = s["video"], s.get("audio")
        duree, taille = float(p["format"]["duration"]), int(p["format"]["size"]) / 1e6
        head = open(mp4, "rb").read(200000)
        faststart = head.find(b"moov") != -1 and (head.find(b"mdat") == -1 or head.find(b"moov") < head.find(b"mdat"))
        pi, si = sonde(images[i])
        t = texte(cid)
        absents = [m for m in ATTENDUS[cid] if m.replace("’", "'").lower() not in t.lower()]  # capitales posées par le CSS
        interdits = [m for m in INTERDITS if m.lower() in f" {t.lower()} "]
        tests = [
            ("Image JPG 1080×1920", si["video"]["width"] == 1080 and si["video"]["height"] == 1920),
            ("Vidéo 1080×1920, H.264 High, yuv420p, 30 i/s", v["width"] == 1080 and v["height"] == 1920 and v["codec_name"] == "h264"
             and v.get("profile") == "High" and v["pix_fmt"] == "yuv420p" and v["r_frame_rate"] == "30/1"),
            (f"Durée {duree:.2f} s (4,95–5,05)", 4.95 <= duree <= 5.05),
            (f"Poids {taille:.1f} Mo (≤ 30)", taille <= 30),
            ("faststart (moov avant mdat)", faststart),
            ("Piste son AAC muette (musique ajoutée dans Instagram)", a is not None and a["codec_name"] == "aac"),
            ("Textes attendus présents" + (f" (absents : {absents})" if absents else ""), not absents),
            ("Aucun mot interdit ni allégation" + (f" (trouvés : {interdits})" if interdits else ""), not interdits),
        ]
        lignes += [f"QC — story {nom} : {os.path.basename(images[i])} + {os.path.basename(mp4)}",
                   *(f"{'OK ' if ok else 'NON'}  {n}" for n, ok in tests),
                   f"Verdict : {'GO technique' if all(ok for _, ok in tests) else 'À CORRIGER'}", ""]

    run(["ffmpeg", "-v", "error", "-y", *sum((["-i", f] for f in images), []), "-filter_complex",
         "".join(f"[{k}]scale=360:640[i{k}];" for k in range(len(images))) + "".join(f"[i{k}]" for k in range(len(images)))
         + f"hstack={len(images)}", "-frames:v", "1", "-q:v", "3", os.path.join(dctl, "planche_nutrition.jpg")])
    lignes.append("Reste à valider par Mehdi : les points ⚠ de A_valider.md (stock du jour, Daily Protein, visuel partenaire).")
    open(os.path.join(dctl, "QC_nutrition.txt"), "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print("\n".join(lignes))


if __name__ == "__main__":
    main()
