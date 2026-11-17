"""Livraison des stories courtes du lancement Visbody (A « Le scan » 12 s, B « Vos résultats » 10 s), 60 i/s.

Pour chaque story : l'image du rendu (<projet>/renders/story.mp4) reprise avec le WAV d'origine, encodée comme
tools/livrer.py (H.264 High, CRF 16, faststart), en version musique et bruitages seuls, puis les mêmes contrôles :
format, durée (≤ 12 s), poids, sonie, crête vraie, aperçu = rendu décodé (SSIM, image choisie par son numéro), textes,
mots interdits, check HyperFrames ; planche à 4 i/s et image 0. Fichiers dans « Pub Meta LA SALLE/Visbody oct26/ »
(vidéos ignorées par git), rapport controles/QC_visbody_stories_courtes.txt.

Usage : ~/.venvs/hyperframes-audio/bin/python -I tools/livrer_courtes.py   (après courtes.py, musique_courtes.py et
        le rendu : npx --yes hyperframes@0.8.181 render --fps 60 --quality delivery -o renders/story.mp4)
"""
import os
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import build  # noqa: E402
import courtes  # noqa: E402
import livrer as L  # noqa: E402  (contrôles et encodeur de la story longue)
import master  # noqa: E402

COMMUNS = ["OPTION PREMIUM", "EN SERVICE", "L'OPTION PREMIUM", "2 €", "TTC PAR SEMAINE", "1 ANALYSE 3D PAR SEMAINE",
           "Soit 8 € toutes les 4 semaines, en plus de votre abonnement.", "NOUVEAU · ANALYSE 3D", "UNE BALANCE", "IA.",
           *[r.upper() for r in build.RESULTATS], "ACTIVEZ-LA", "À L'ACCUEIL.", "EN QUELQUES SECONDES.", courtes.MENTION_FIN]
ATTENDUS = {"A": COMMUNS + ["BIEN PLUS", "QU'UNE", "BALANCE.", "LE PRINCIPE", "UN SCAN", "À 360°"],
            "B": COMMUNS + ["VOS", "PROGRÈS,", "EN 3D.", "CE QUE VOUS DÉCOUVREZ", "EN 1 SCAN À 360°"]}


def story(cle, dvid, dctl, lignes):
    h = courtes.HISTOIRES[cle]
    projet, d = h["projet"], h["duree"]
    rendu = os.path.join(build.RACINE, projet, "renders", "story.mp4")
    if not os.path.exists(rendu):
        sys.exit(f"Rendu absent : {rendu}")
    verif = L.check(projet)
    t_ecran = L.texte(projet)
    absents = L.manquants(ATTENDUS[cle], t_ecran)
    interdits = L.trouves(t_ecran)
    instants = [round(fin - 0.1, 2) for _, _, fin in h["scenes"]]
    if "scan" in h:
        instants += [round(h["scan"]["descente"][0] + 0.5, 2), round(h["scan"]["remontee"][0] + 0.5, 2)]
    instants += [round(h["resultats"][2] + 0.2, 2)]
    nom = f"{L.NOM}_{h['nom']}_9x16"
    with tempfile.TemporaryDirectory() as tmp:
        L.run(L.HF + ["snapshot", "--at", ",".join(f"{t:g}" for t in instants), "--no-end", "-o", tmp, "--timeout", "60000",
                      os.path.join(build.RACINE, projet)])
        apercus = sorted((f for f in os.listdir(tmp) if f.startswith("frame-") and f.endswith(".png")), key=lambda f: int(f.split("-")[1]))
        for version, wav in (("", "musique"), ("_bruitages", "bruitages")):
            video = os.path.join(dvid, f"{nom}{version}.mp4")
            remix = os.path.join(tmp, f"remix{version}.mp4")
            L.run(["ffmpeg", "-hide_banner", "-y", "-i", rendu, "-i", os.path.join(build.RACINE, "_communs", f"{wav}_visbody_courte_{cle}.wav"),
                   "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2",
                   "-t", f"{d:g}", remix])
            L.encoder(remix, video, d)
            p, s = L.sonde(video)
            v, a = s["video"], s["audio"]
            duree, taille = float(p["format"]["duration"]), int(p["format"]["size"]) / 1e6
            i, tp = master.controle(video)
            scores = [L.ssim(video, t, os.path.join(tmp, f)) for t, f in zip(instants, apercus)]
            cible = -18.0 if version else -14.0
            lignes += L.ligne(os.path.basename(video), [
                (f"Format 1080×1920, H.264 High, yuv420p, {build.FPS} i/s", v["width"] == 1080 and v["height"] == 1920 and v["codec_name"] == "h264"
                 and v.get("profile") == "High" and v["pix_fmt"] == "yuv420p" and v["r_frame_rate"] == f"{build.FPS}/1"),
                (f"Durée {duree:.3f} s ({d - 0.1:g}–{d:g}, 12 s au plus)", d - 0.1 <= duree <= d + 0.001 and duree <= 12.001),
                (f"Poids {taille:.1f} Mo (≤ 25)", taille <= 25),
                ("faststart (moov avant mdat)", L.faststart(video)),
                (f"Audio AAC {a['sample_rate']} Hz, {a['channels']} canaux", a["codec_name"] == "aac" and a["sample_rate"] == "48000" and a["channels"] == 2),
                (f"Sonie {i:.1f} LUFS ({cible:g} ± 0,5)", abs(i - cible) <= 0.5),
                (f"Crête vraie {tp:.1f} dBTP (≤ −1,5)", tp <= -1.5),
                ("Aperçu = rendu décodé (SSIM " + ", ".join(f"{x:.3f}" for x in scores) + " ≥ 0,97)",
                 len(scores) == len(instants) and min(scores) >= 0.97),
                (f"check HyperFrames passé, {verif[1]} ({projet})", verif[0] and verif[1].split()[-1].split("/")[0] == verif[1].split()[-1].split("/")[-1]),
                ("Textes présents" + (f" (absents : {absents})" if absents else ""), not absents),
                ("Aucun mot interdit ni allégation" + (f" (trouvés : {interdits})" if interdits else ""), not interdits),
            ])
    video = os.path.join(dvid, f"{nom}.mp4")
    vf = ("fps=4,drawbox=x=0:y=0:w=1080:h=270:color=red@0.25:t=fill,drawbox=x=0:y=1250:w=1080:h=670:color=red@0.25:t=fill,"
          "drawbox=x=950:y=900:w=130:h=1020:color=red@0.25:t=fill,scale=216:384,tile=12x4")
    L.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", vf, "-frames:v", "1", "-q:v", "3", os.path.join(dctl, f"planche_{h['nom']}_4ips.jpg")])
    L.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-frames:v", "1", "-q:v", "2", os.path.join(dctl, f"image0_{h['nom']}.jpg")])


def main():
    dvid, dctl = (os.path.join(L.LIVRAISON, x) for x in ("videos", "controles"))
    lignes = []
    for cle in courtes.HISTOIRES:
        story(cle, dvid, dctl, lignes)
    lignes.append("Reste à valider : les points ⚠ de A_valider.md, puis l'écoute de la musique (contrôlée par mesures seulement).")
    open(os.path.join(dctl, "QC_visbody_stories_courtes.txt"), "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print("\n".join(lignes))


if __name__ == "__main__":
    main()
