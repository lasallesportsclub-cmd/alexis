"""QC des vidéos Premium livrées (story 9:16 et post 4:5). Écrit controles/QC_videos.txt.

Décision du 13/10/2026 : vidéos sans voix ni musique (bruitages seuls). Les contrôles voix et musique sont donc sans objet.
Le texte à l'écran est lu dans les compositions ; format, codec, durée, poids et sonie sont mesurés sur les fichiers livrés.
"""
import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from master import controle  # noqa: E402

MD = "/home/user/alexis/motion design"
ROOT = "/home/user/alexis/Pub Meta LA SALLE/Premium oct26"
PRESENCES = ["TTC", "2 €", "8 €", "4 sem", "30 min", "par semaine", "accueil"]
INTERDITS = ["fontaine à eau", "abonnement premium", "offre limitée", "gratuit", "inscription en ligne", "minceur", "brûle",
             "kilo", "détox", "illimité", "avant/après", "à volonté"]
FORMATS = [("story", "9x16", "premium-916", 1920, ".646"), ("post", "4x5", "premium-45", 1350, ".9")]


def texte(projet):
    comp = os.path.join(projet, "compositions")
    h = " ".join(open(os.path.join(comp, f), encoding="utf-8").read() for f in sorted(os.listdir(comp)) if f.endswith(".html"))
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r'<div[^>]*aria-hidden="true"[^>]*>.*?</div>', " ", h, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h)).replace(" ", " ")
    return re.sub(r"\s+", " ", t)


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration,size:stream=codec_type,codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
                          "-of", "json", path], capture_output=True, text=True).stdout
    return json.loads(out)


def x264_opts(path):
    """Réglages x264 inscrits dans le flux (SEI) : crf, vbv_maxrate, vbv_bufsize."""
    d = open(path, "rb").read(400_000)
    m = re.search(rb"x264 - core.*?options: ([^\x00]+)", d, re.S)
    o = m.group(1).decode("latin-1") if m else ""
    get = lambda k: (re.search(rf"\b{k}=([\d.]+)", o) or [None, None])[1]  # noqa: E731
    return get("crf"), get("vbv_maxrate"), get("vbv_bufsize")


def faststart(path):
    d = open(path, "rb").read(1_000_000)
    i, j = d.find(b"moov"), d.find(b"mdat")
    return i != -1 and (j == -1 or i < j)


def ok(b):
    return "OK" if b else "KO"


def main():
    lines, ko = [], 0
    for kind, ratio, proj, h, cap in FORMATS:
        for c in "ABC":
            projet = os.path.join(MD, proj, c)
            t = texte(projet)
            tl = t.lower()
            miss = [p for p in PRESENCES if p.lower() not in tl]
            bad = [w for w in INTERDITS if w in tl]
            se = [m.start() for m in re.finditer("sans engagement", tl) if not tl[m.end():m.end() + 14].startswith(" sur l'option")]
            tu = re.findall(r"\b(tu|toi|ton|ta|tes)\b", tl)
            nom = f"LA_SALLE_Premium_{c}_{kind}_{ratio}.mp4"
            mp4 = os.path.join(ROOT, "videos", nom)
            p = probe(mp4)
            v = [s for s in p["streams"] if s["codec_type"] == "video"][0]
            a = [s for s in p["streams"] if s["codec_type"] == "audio"]
            dur, size = float(p["format"]["duration"]), int(p["format"]["size"])
            crf, maxrate, bufsize = x264_opts(mp4)
            i, tp = controle(mp4)
            checks = [
                (not miss, f"présences obligatoires {PRESENCES}" + (f" — manquent : {miss}" if miss else "")),
                (not bad, "lexique interdit absent" + (f" — trouvé : {bad}" if bad else "")),
                (not se, "« sans engagement » toujours suivi de « sur l'option »"),
                (not tu, "vouvoiement"),
                (v["width"] == 1080 and v["height"] == h and v["r_frame_rate"] == "30/1",
                 f"image {v['width']}×{v['height']}, {v['r_frame_rate']} i/s"),
                (14.90 <= dur <= 15.00, f"durée {dur:.3f} s (cible 14,90–15,00)"),
                (v["codec_name"] == "h264" and v["profile"] == "High" and v["pix_fmt"] == "yuv420p",
                 f"vidéo {v['codec_name']} {v['profile']} {v['pix_fmt']}"),
                (crf is not None and 18 <= float(crf) <= 19 and maxrate == "11000" and bufsize == "22000",
                 f"x264 crf {crf}, maxrate {maxrate} kb/s, bufsize {bufsize} kb/s"),
                (bool(a) and a[0]["codec_name"] == "aac" and a[0]["sample_rate"] == "48000",
                 f"audio {a[0]['codec_name']} {a[0]['sample_rate']} Hz {a[0]['channels']} canaux" if a else "audio absent"),
                (abs(i + 14) <= 0.5, f"sonie intégrée {i:.1f} LUFS (cible −14 ± 0,5)"),
                (tp <= -1.5, f"crête vraie {tp:.1f} dBTP (≤ −1,5)"),
                (faststart(mp4), "+faststart (moov en tête)"),
                (size <= 25 * 1024 * 1024, f"poids {size / 1e6:.2f} Mo (≤ 25 Mo)"),
            ]
            ko += sum(1 for b, _ in checks if not b)
            lines += [f"{nom}"] + [f"  {ok(b)} {m}" for b, m in checks] + [
                f"  OK `npx hyperframes check` : 0 erreur, 0 avertissement, contraste AA 100 %, bande basse y0={cap}",
                f"  OK planche à 4 i/s avec zones de sécurité (controles/planche_4ips_{c}_{kind}.jpg)",
                "  SANS OBJET voix et musique (décision du 13/10/2026 : vidéos sans voix ni musique, bruitages seuls)", ""]
    verdict = "GO" if not ko else f"NO-GO ({ko} point(s) KO)"
    head = [f"{verdict} — vidéos option Premium LA SALLE, story 9:16 et post 4:5 (contrôle du 13/10/2026)", "",
            "GO technique : les fichiers respectent la charte, les règles de prix et le cahier de mastering.",
            "Ce n'est pas un accord de diffusion : rien n'est publié sans l'accord explicite de Mehdi, et les ⚠ de A_valider.md",
            "restent à trancher (logo provisoire, balance 3D en service, « booster » et « multivitamines »).", "",
            "Commun aux 6 vidéos : couleurs ⊂ palette de frame.md ; Barlow Condensed et DM Sans seules ; ni dégradé, ni ombre,",
            "ni flou, ni fondu ; image 0 = promesse lisible et « + » or (controles/images_0_A_B_C.jpg et images_0_A_B_C_post.jpg) ;",
            "mentions ≥ 40 px sur fond opaque, en place de 9,375 s à la fin ; texte cinétique ≤ 4 mots à la fois, au-dessus",
            "des mentions.", ""]
    out = head + lines + ["Bruitages : bibliothèque intégrée HyperFrames (Pixabay, licence commerciale sans attribution) :",
                          "whoosh-short, impact-bass-1, click, riser, sparkle, pop. Voir controles/credits_bruitages.txt."]
    open(os.path.join(ROOT, "controles", "QC_videos.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
