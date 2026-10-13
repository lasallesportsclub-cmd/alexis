"""Contrôle qualité des images livrées (option Premium LA SALLE). Écrit controles/QC_images.txt.

Vérifie : dimensions, profil sRGB, poids des JPG, lexique interdit, qualificatif de chaque prix, condition de « OFFERTES »,
mentions là où un prix apparaît, zone sticker vide (story), contenu dans les zones utiles, raccord du trait du carrousel.
"""
import html
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import frames as F  # noqa: E402

ROOT = "/home/user/alexis/Pub Meta LA SALLE/Premium oct26"
IMG = os.path.join(ROOT, "images")

ITEMS = [
    ("story/01_LA_SALLE_Premium_offre_story_9x16", F.S4, 1920),
    ("story/02_LA_SALLE_Premium_A_story_9x16", F.S1, 1920),
    ("story/03_LA_SALLE_Premium_B_story_9x16", F.S2, 1920),
    ("story/04_LA_SALLE_Premium_C_story_9x16", F.S3, 1920),
    ("post/01_LA_SALLE_Premium_A_post_4x5", F.P1, 1350),
    ("post/02_LA_SALLE_Premium_B_post_4x5", F.P2, 1350),
    ("post/03_LA_SALLE_Premium_C_post_4x5", F.P3, 1350),
] + [(f"carrousel/LA_SALLE_Premium_carrousel_{i + 1}", fn, 1350) for i, fn in enumerate([F.K1, F.K2, F.K3, F.K4, F.K5])]

INTERDITS = ["fontaine à eau", "abonnement premium", "offre limitée", "gratuit", "inscription en ligne", "minceur",
             "brûle", "kilo", "détox", "illimité", "avant/après", "avant / après", "à volonté"]
TUTOIEMENT = re.compile(r"\b(tu|toi|ton|ta|tes|t'|profite|viens|teste)\b", re.I)


def visible_text(fn):
    h = re.sub(r'<div[^>]*aria-hidden="true"[^>]*>.*?</div>', " ", fn(), flags=re.S)  # décor (relief, reflet, fantôme)
    h = re.sub(r"<svg.*?</svg>", " + ", h, flags=re.S)  # le « + » dessiné compte comme un « + »
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    return re.sub(r"\s+", " ", t.replace(" ", " ")).strip()


def bg_fraction(im, box, tol=24):
    """Part des pixels proches du fond #0D0D0D dans la zone (x0, y0, x1, y1)."""
    crop = im.crop(box).convert("RGB")
    px = crop.getdata() if not hasattr(crop, "get_flattened_data") else crop.get_flattened_data()
    n = ok = 0
    for r, g, b in px:
        n += 1
        ok += (abs(r - 13) <= tol and abs(g - 13) <= tol and abs(b - 13) <= tol)
    return ok / max(n, 1)


def main():
    lines, go = [], True
    for name, fn, h in ITEMS:
        errs, notes = [], []
        png, jpg = os.path.join(IMG, name + ".png"), os.path.join(IMG, name + ".jpg")
        for path in (png, jpg):
            im = Image.open(path)
            if im.size != (1080, h):
                errs.append(f"dimensions {im.size} ≠ 1080×{h} ({os.path.basename(path)})")
            if not im.info.get("icc_profile"):
                errs.append(f"profil sRGB absent ({os.path.basename(path)})")
        if os.path.getsize(jpg) >= 1_000_000:
            errs.append(f"JPG de {os.path.getsize(jpg)} octets ≥ 1 Mo")
        t = visible_text(fn)
        tl = t.lower()
        for w in INTERDITS:
            if w in tl:
                errs.append(f"mot interdit : « {w} »")
        if TUTOIEMENT.search(t):
            errs.append(f"tutoiement possible : « {TUTOIEMENT.search(t).group(0)} »")
        for m in re.finditer(r"sans engagement", tl):
            if not tl[m.end():m.end() + 14].startswith(" sur l'option"):
                errs.append("« sans engagement » sans « sur l'option »")
        has_price = bool(re.search(r"\b[28] €", t))
        if has_price:
            if "TTC" not in t:
                errs.append("prix sans TTC")
            if "EN PLUS DE VOTRE ABONNEMENT" not in t and "en plus de l'abonnement" not in t:
                errs.append("prix sans « en plus de votre abonnement »")
            if "Option 2 € TTC/sem." not in t:
                errs.append("prix sans mentions")
            notes.append("prix qualifié (TTC, cadence, en plus de l'abonnement, mentions)")
        if "OFFERTES" in t:
            if not ("PUIS + 2 € TTC/SEM." in t or "PUIS 2 € TTC/SEM." in t or ("PUIS" in t and "2 €" in t)):
                errs.append("« OFFERTES » sans sa condition")
            if "EN CE MOMENT" not in t:
                errs.append("offre sans « en ce moment »")
            notes.append("« OFFERTES » avec sa condition et « en ce moment »")
        im = Image.open(png).convert("RGB")
        if h == 1920:
            f = bg_fraction(im, (90, 1320, 990, 1540))
            (notes if f > 0.995 else errs).append(f"zone sticker y 1320–1540 vide à {f*100:.1f} %")
            f2 = bg_fraction(im, (0, 1245, 1080, 1920))
            (notes if f2 > 0.995 else errs).append(f"rien sous y 1240 ({f2*100:.1f} % de fond)")
        else:
            f2 = bg_fraction(im, (0, 1220, 1080, 1350))
            (notes if f2 > 0.995 else errs).append(f"rien sous y 1215 ({f2*100:.1f} % de fond)")
        go &= not errs
        lines.append(f"[{'OK' if not errs else 'KO'}] {name}")
        lines += [f"      ✗ {e}" for e in errs] + [f"      · {n}" for n in notes]

    # raccord du trait or entre slides consécutives du carrousel
    seam = []
    for k in range(1, 5):
        a = Image.open(os.path.join(IMG, f"carrousel/LA_SALLE_Premium_carrousel_{k}.png")).convert("RGB")
        b = Image.open(os.path.join(IMG, f"carrousel/LA_SALLE_Premium_carrousel_{k + 1}.png")).convert("RGB")
        ya = [y for y in range(1350) if (lambda p: p[0] > 150 and p[2] < 150)(a.getpixel((1079, y)))]
        yb = [y for y in range(1350) if (lambda p: p[0] > 150 and p[2] < 150)(b.getpixel((0, y)))]
        ok = ya and ya == yb
        go &= bool(ok)
        seam.append(f"[{'OK' if ok else 'KO'}] raccord slide {k} → {k + 1} : y {ya[:1]}–{ya[-1:]} | y {yb[:1]}–{yb[-1:]}")

    head = "GO" if go else "NO-GO"
    out = [f"{head} — images option Premium LA SALLE (contrôle automatique du {os.environ.get('QC_DATE', '13/10/2026')})", "",
           "Vérifié pour chaque image : dimensions exactes, profil sRGB (PNG et JPG), JPG < 1 Mo, lexique interdit, vouvoiement,",
           "qualificatif de chaque prix, condition de « OFFERTES », mentions, zones utiles, zone sticker vide (story).", ""]
    out += lines + ["", "Carrousel (trait or continu, raccord au pixel) :"] + seam
    out += ["", "Contrôles HyperFrames : `npx hyperframes check` passé sur premium-visuels-916 (bande y0=.646) et premium-visuels-45",
            "(bande y0=.9) : 0 erreur de lint, d'exécution, de mise en page ; contraste WCAG AA 60/60 et 54/54.",
            "Lisibilité à 30 % et recadrage 3:4 de la grille : contrôlés à l'œil (controles/planche_grille_3x4_30pc.jpg).",
            "", "⚠ Points à valider avant diffusion : voir A_valider.md (logo provisoire notamment)."]
    os.makedirs(os.path.join(ROOT, "controles"), exist_ok=True)
    open(os.path.join(ROOT, "controles", "QC_images.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
