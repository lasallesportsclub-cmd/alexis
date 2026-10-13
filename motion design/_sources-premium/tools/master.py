"""Mastering des vidéos Premium pour Instagram : −14 LUFS ± 0,5, crête vraie ≤ −1,5 dBTP, H.264 CRF 18, maxrate 11M,
AAC 48 kHz, +faststart, ≤ 25 Mo, durée 14,90–15,00 s.

Usage : python3 master.py entree.mp4 sortie.mp4
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


def encode(src, dst, tp):
    m = mesure_loudnorm(src, tp)
    af = (f"loudnorm=I={I_CIBLE}:TP={tp}:LRA={LRA}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
          f"aresample=48000")
    r = run(["ffmpeg", "-hide_banner", "-y", "-i", src, "-t", f"{DUREE}", "-af", af,
             "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-maxrate", "11M", "-bufsize", "22M",
             "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30",
             "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
             "-movflags", "+faststart", dst])
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    return m


def main(src, dst):
    tp = TP_MAX
    for _ in range(5):
        m = encode(src, dst, tp)
        i, crete = controle(dst)
        if crete <= TP_MAX and abs(i - I_CIBLE) <= 0.5:
            break
        tp -= 0.3
    print(json.dumps({"fichier": dst, "source_I": float(m["input_i"]), "source_TP": float(m["input_tp"]),
                      "mode": m.get("normalization_type"), "cible_TP": round(tp, 2), "I": i, "TP": crete}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
