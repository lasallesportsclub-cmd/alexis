"""QC des vidéos Premium avec voix « ton pub » (story 9:16 et post 4:5). Écrit controles/QC_videos_voix.txt.

Mêmes contrôles techniques que qc_videos.py, sur les fichiers de videos_voix/ (hors git : la voix d'une personne ne va
pas dans ce dépôt public), plus la voix : la piste son de chaque vidéo livrée est retranscrite par whisper-cli et
comparée mot à mot au texte attendu. Les homophones (« passer » / « passez », « 30 » / « trente »…) ne comptent pas.
Usage : python3 qc_voix.py
"""
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

sys.path.insert(0, os.path.dirname(__file__))
from master import controle  # noqa: E402
from qc_videos import FORMATS, INTERDITS, MD, PRESENCES, ROOT, faststart, ok, probe, texte, x264_opts  # noqa: E402

MODELE = os.environ.get("WHISPER_MODEL", os.path.expanduser("~/.cache/hyperframes/whisper/models/ggml-small.bin"))
FIN = "Les quatre premières semaines de l'option Premium sont offertes. Activez-la à l'accueil, en quelques secondes."
SCRIPT = {
    "A": "Passez en version Premium. Une boisson toutes les trente minutes. Une analyse en trois D, chaque semaine. " + FIN,
    "B": "Votre boisson vous attend. Collagène, multivitamines, L-carnitine, booster… ou simplement de l'eau. "
         "Une boisson toutes les trente minutes. " + FIN,
    "C": "Vos progrès, en trois D. Une analyse en trois D, chaque semaine. " + FIN,
}
ORIGINE = {
    "A": "P1, P6, P9 : prises réelles ; P5 et 25 : voix clonée",
    "B": "P2, P4, P9 : prises réelles (P4 resserrée, ×1,12) ; P5 et 25 : voix clonée",
    "C": "P6, P9 : prises réelles ; P3 et 25 : voix clonée",
}
EGAUX = {"passer": "passez", "passe": "passez", "3d": "trois d", "3": "trois", "4": "quatre", "30": "trente",
         "l": "elle", "carnetine": "carnitine", "carnitines": "carnitine", "accueille": "accueil",
         "multivitamine": "multivitamines"}


def mots(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[’'`-]", " ", t)
    out = []
    for m in re.sub(r"[^a-z0-9 ]", " ", t).split():
        out.extend(EGAUX.get(m, m).split())
    return out


def ecarts(a, b):
    """Alignement mot à mot : liste des différences (attendu → entendu)."""
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    out, i, j = [], n, m
    while i or j:
        if i and j and d[i][j] == d[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            if a[i - 1] != b[j - 1]:
                out.append(f"{a[i - 1]} → {b[j - 1]}")
            i, j = i - 1, j - 1
        elif i and d[i][j] == d[i - 1][j] + 1:
            out.append(f"{a[i - 1]} → ∅")
            i -= 1
        else:
            out.append(f"∅ → {b[j - 1]}")
            j -= 1
    return out[::-1]


def entendre(mp4):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vn", "-ac", "1", "-ar", "16000", f"{tmp}/a.wav"], check=True)
        r = subprocess.run(["whisper-cli", "-m", MODELE, "-l", "fr", "-t", "4", "-nt", "-f", f"{tmp}/a.wav"],
                           capture_output=True, text=True)
    return " ".join(l.strip() for l in r.stdout.splitlines() if l.strip())


def main():
    lines, ko = [], 0
    for kind, ratio, proj, h, cap in FORMATS:
        for c in "ABC":
            projet = os.path.join(MD, proj, c)
            tl = texte(projet).lower()
            miss = [p for p in PRESENCES if p.lower() not in tl]
            bad = [w for w in INTERDITS if w in tl]
            nom = f"LA_SALLE_Premium_{c}_{kind}_{ratio}_voix.mp4"
            mp4 = os.path.join(ROOT, "videos_voix", nom)
            p = probe(mp4)
            v = [s for s in p["streams"] if s["codec_type"] == "video"][0]
            a = [s for s in p["streams"] if s["codec_type"] == "audio"]
            dur, size = float(p["format"]["duration"]), int(p["format"]["size"])
            crf, maxrate, bufsize = x264_opts(mp4)
            i, tp = controle(mp4)
            entendu = entendre(mp4)
            diff = ecarts(mots(SCRIPT[c]), mots(entendu))
            checks = [
                (not miss, "présences obligatoires à l'écran" + (f" — manquent : {miss}" if miss else "")),
                (not bad, "lexique interdit absent" + (f" — trouvé : {bad}" if bad else "")),
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
                (not diff, "voix retranscrite = texte attendu" + (f" — écarts : {diff}" if diff else "")),
            ]
            ko += sum(1 for b, _ in checks if not b)
            lines += [nom] + [f"  {ok(b)} {m}" for b, m in checks] + [
                f"  Entendu (whisper) : « {entendu} »", f"  Voix : {ORIGINE[c]}", ""]
    verdict = "GO technique" if not ko else f"NO-GO ({ko} point(s) KO)"
    head = [f"{verdict} — vidéos option Premium LA SALLE avec voix « ton pub », story 9:16 et post 4:5", "",
            "Fichiers hors dépôt (videos_voix/ est ignoré par git) : la voix d'une personne ne va pas sur ce dépôt public.",
            "Ce n'est pas un accord de diffusion : rien n'est publié sans l'accord explicite de Mehdi. L'écoute reste juge :",
            "ce contrôle vérifie que chaque mot attendu est prononcé, pas le ton.", "",
            "Voix : passe-haut 80 Hz, compression douce, présence +2 dB, −16,4 LUFS par réplique, crêtes limitées à",
            "−4,5 dBFS ; le rendu sort à −14 LUFS et master.py copie l'audio sans le renormaliser.",
            "Bruitages sous la voix : −2,9 dB en général, −6 dB de plus quand ils tombent sur une réplique, impacts",
            "raccourcis à 0,8 s avec fondu de 0,5 s. Pendant la parole, ils restent au moins 6 dB sous la voix.", ""]
    out = head + lines
    open(os.path.join(ROOT, "controles", "QC_videos_voix.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
