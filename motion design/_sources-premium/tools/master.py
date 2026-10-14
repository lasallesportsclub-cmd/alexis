"""Mastering des vidéos Premium pour Instagram : −14 LUFS ± 0,5, crête vraie ≤ −1,5 dBTP, H.264 CRF 18, maxrate 11M,
AAC 48 kHz, +faststart, ≤ 25 Mo, durée 14,90–15,00 s.

Usage : python3 master.py entree.mp4 sortie.mp4 [durée en s, 14.933 par défaut]
Deux passes loudnorm (mesure, puis correction), puis mesure de contrôle EBU R128 du fichier livré.
Si la crête vraie dépasse encore −1,5 dBTP, la cible de crête est abaissée de 0,3 dB et la passe recommence.
"""
import json
import re
import subprocess
import sys

I_CIBLE, TP_MAX, LRA = -14.0, -1.5, 20
DUREE = 14.933


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def mesure_loudnorm(src, tp):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-vn", "-af",
               f"loudnorm=I={I_CIBLE}:TP={tp}:LRA={LRA}:print_format=json", "-f", "null", "-"]).stderr
    return json.loads(err[err.rindex("{"):err.rindex("}") + 1])


def controle(path):
    """Mesure EBU R128 du fichier livré : intégrée (LUFS) et crête vraie (dBTP)."""
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    resume = err[err.rindex("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+) LUFS", resume).group(1))
    tp = float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+) dBFS", resume, re.S).group(1))
    return i, tp


def encode(src, dst, tp, duree=DUREE):
    m = mesure_loudnorm(src, tp)
    af = (f"loudnorm=I={I_CIBLE}:TP={tp}:LRA={LRA}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
          f"aresample=48000")
    r = run(["ffmpeg", "-hide_banner", "-y", "-i", src, "-t", f"{duree}", "-af", af,
             "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-maxrate", "11M", "-bufsize", "22M",
             "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30",
             "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
             "-movflags", "+faststart", dst])
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    return m


def encode_direct(src, dst, duree, gain_db=None):
    """Audio déjà conforme : pas de loudnorm (qui passerait en mode dynamique et ferait déborder la crête
    à l'encodage AAC). gain_db=None : la piste AAC est copiée telle quelle (pas de seconde génération AAC) ;
    sinon elle est réencodée avec un gain fixe."""
    audio = ["-c:a", "copy"] if gain_db is None else [
        "-af", f"volume={gain_db}dB,aresample=48000", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
    r = run(["ffmpeg", "-hide_banner", "-y", "-i", src, "-t", f"{duree}",
             "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-maxrate", "11M", "-bufsize", "22M",
             "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30",
             "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
             *audio, "-movflags", "+faststart", dst])
    if r.returncode:
        sys.exit(r.stderr[-2000:])


def main(src, dst, duree=DUREE):
    i0, tp0 = controle(src)
    if abs(i0 - I_CIBLE) <= 0.5 and tp0 <= TP_MAX:
        gain = None
        for _ in range(6):
            encode_direct(src, dst, duree, gain)
            i, crete = controle(dst)
            if crete <= TP_MAX:
                break
            gain = -0.3 if gain is None else gain - 0.3
        print(json.dumps({"fichier": dst, "source_I": i0, "source_TP": tp0, "mode": "direct", "gain_dB": gain,
                          "I": i, "TP": crete}, ensure_ascii=False))
        return
    tp = TP_MAX
    for _ in range(5):
        m = encode(src, dst, tp, duree)
        i, crete = controle(dst)
        if crete <= TP_MAX and abs(i - I_CIBLE) <= 0.5:
            break
        tp -= 0.3
    print(json.dumps({"fichier": dst, "source_I": float(m["input_i"]), "source_TP": float(m["input_tp"]),
                      "mode": m.get("normalization_type"), "cible_TP": round(tp, 2), "I": i, "TP": crete}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else DUREE)
