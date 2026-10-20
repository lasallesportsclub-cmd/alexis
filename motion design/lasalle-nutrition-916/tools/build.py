"""Stories LA SALLE « Nutrimuscle et Nutripure, disponibles à l'accueil » : 4 scènes de 5 s en 1080×1920.

Chaque story reprend la direction artistique de sa marque (relevée dans frame.md) :
  s1  les deux marques à l'accueil : photo du rayon, bleu marine Nutrimuscle + bleu ciel Nutripure
  s2  Nutrimuscle : fond #F7F5F3, bloc #00253A, fiche produit sobre (Helvetica → Inter droit), filets fins
  s3  Nutripure : fond #FBF8F8, capitales grasses italiques, visuel partenaire officiel, pastille #77D2F5
  s4  « Une question sur un produit ? » : les deux marques côte à côte, zone vide pour un sticker Question

Une scène = une sous-composition (compositions/sN.html) montée dans index.html à t = 5 × (N−1).
Les images fixes sont prises à la fin de chaque scène (tout est en place), les vidéos sont découpées dans le rendu.

Sources hors dépôt (dépôt public) : ~/nutri-sources/raw (Drive, lecture seule) et ~/nutri-sources/fonts (@fontsource/inter).
assets/ est ignoré par git : ce script le reconstruit à l'identique.
Usage : python3 tools/build.py
"""
import os
import shutil
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
MD = os.path.dirname(RACINE)
SRC = os.path.expanduser("~/nutri-sources")
DUREE = 5.0
NB, NNB = " ", " "

# Sources Drive (lecture seule) à recopier dans ~/nutri-sources/raw si la session est neuve
DRIVE = {
    "nutripure.jpg": "« nutripure.jpg », photo du rayon de l'accueil, 1350×2400",
    "Salle présentation.png": "« Salle présentation.png », Partagés avec moi > Dossier partenaire > Communication > "
                              "🎁 -10% Daily / Muscle Protein > Daily + Muscle Protein",
}
# Recadrages : (source, x, y, largeur, hauteur, sortie)
IMAGES = [
    ("nutripure.jpg", 0, 1150, 1150, 1030, "etagere.jpg"),          # étagères du milieu et du bas, shakers compris
    ("nutripure.jpg", 0, 1700, 950, 530, "etagere-nm.jpg"),         # pots Nutrimuscle de l'étagère du bas
    ("Salle présentation.png", 0, 0, 1080, 1150, "nutripure-plv.jpg"),  # visuel partenaire sans sa pastille du bas
]
POLICES = [f"inter-latin-{w}-normal.woff2" for w in (400, 500, 600, 700, 800, 900)] + \
          [f"inter-latin-{w}-italic.woff2" for w in (800, 900)]

C = {"marine": "#00253A", "bleu": "#0093E5", "ciel": "#77D2F5", "pale": "#E8F5FC", "encre": "#111111",
     "texte": "#142323", "gris": "#667085", "fond_nm": "#F7F5F3", "fond_np": "#FBF8F8"}

NM_PRODUITS = [  # stock Resamania au 30/09/2026 + photo du rayon (⚠ à revérifier le jour de la publication)
    ("NATIVE WHEY PROTIMUSCLE", "Protéine en poudre"),
    ("LEAN GAINER WHEY & AVOINE", "En poudre"),
    ("CRÉATINE CREAPURE®", "En poudre"),
    ("COLLAGÈNE PEPTAN® · NATICOL®", "En poudre"),
    ("CITRATE DE MAGNÉSIUM", "Gélules ou poudre"),
]
NP_PRODUITS = "MUSCLE PROTEIN · CRÉATINE · SHAKER"


def assets():
    a = os.path.join(RACINE, "assets")
    for d in ("fonts", "vendor", "img"):
        os.makedirs(os.path.join(a, d), exist_ok=True)
    fs = os.path.join(SRC, "fonts", "package")
    if not os.path.isdir(fs):
        sys.exit("Police Inter absente : cd ~/nutri-sources/fonts && npm pack @fontsource/inter@5.1.1 && tar -xzf fontsource-inter-5.1.1.tgz")
    for f in POLICES:
        shutil.copy(os.path.join(fs, "files", f), os.path.join(a, "fonts", f))
    shutil.copy(os.path.join(fs, "LICENSE"), os.path.join(a, "fonts", "OFL-inter.txt"))
    shutil.copy(os.path.join(MD, "premium-visuels-916", "assets", "vendor", "gsap.min.js"), os.path.join(a, "vendor"))
    shutil.copy(os.path.join(MD, "premium-visuels-916", "assets", "img", "logo-negatif-provisoire.png"), os.path.join(a, "img"))
    for src, x, y, w, h, out in IMAGES:
        p = os.path.join(SRC, "raw", src)
        if not os.path.exists(p):
            sys.exit(f"Source absente : {p}\nÀ télécharger depuis le Drive (fichier {DRIVE[src]}).")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-vf", f"crop={w}:{h}:{x}:{y}", "-q:v", "2",
                        os.path.join(a, "img", out)], check=True)


CSS = """
@font-face { font-family: "Inter"; font-weight: 400; font-style: normal; font-display: block; src: url("assets/fonts/inter-latin-400-normal.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-weight: 500; font-style: normal; font-display: block; src: url("assets/fonts/inter-latin-500-normal.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-weight: 600; font-style: normal; font-display: block; src: url("assets/fonts/inter-latin-600-normal.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-weight: 700; font-style: normal; font-display: block; src: url("assets/fonts/inter-latin-700-normal.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-weight: 800; font-style: normal; font-display: block; src: url("assets/fonts/inter-latin-800-normal.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-weight: 900; font-style: normal; font-display: block; src: url("assets/fonts/inter-latin-900-normal.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-weight: 800; font-style: italic; font-display: block; src: url("assets/fonts/inter-latin-800-italic.woff2") format("woff2"); }
@font-face { font-family: "Inter"; font-weight: 900; font-style: italic; font-display: block; src: url("assets/fonts/inter-latin-900-italic.woff2") format("woff2"); }
.st { position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden; font-family: "Inter", sans-serif; color: #111111; }
.st * { margin: 0; padding: 0; box-sizing: border-box; }
.st .a { position: absolute; }
.st .nw { white-space: nowrap; }
.st .kick { font-weight: 700; font-size: 30px; letter-spacing: .14em; text-transform: uppercase; white-space: nowrap; line-height: 1; }
.st .nm { font-weight: 800; letter-spacing: -.02em; line-height: 1; white-space: nowrap; }
.st .np { font-weight: 900; font-style: italic; letter-spacing: -.01em; line-height: 1; white-space: nowrap; text-transform: uppercase; }
.st .corps { font-weight: 500; font-size: 42px; line-height: 1.3; color: #142323; }
.st .pied { left: 0; top: 1580px; width: 1080px; height: 340px; background: #00253A; }
.st .pied img { position: absolute; left: 72px; top: 44px; width: 170px; }
.st .pied p { position: absolute; left: 282px; top: 62px; color: #FFFFFF; font-weight: 500; font-size: 32px; line-height: 1.35; white-space: nowrap; }
"""


def esc(s):
    return s.replace("&", "&amp;").replace("'", "’").replace(" ?", NNB + "?").replace(" :", NB + ":")


def pied():
    return ('<div class="a pied"><img src="assets/img/logo-negatif-provisoire.png" alt="LA SALLE">'
            '<p>LA SALLE · Urban Valley<br>Conflans-Sainte-Honorine</p></div>')


def s1():
    corps = esc("Protéines, créatine, collagène, magnésium : une sélection des deux marques vous attend à l'accueil de LA SALLE.")
    html = f"""
  <div class="a" style="left:0;top:0;width:1080px;height:967px;overflow:hidden" data-layout-allow-overflow>
    <img id="s1-photo" src="assets/img/etagere.jpg" style="display:block;width:1080px;height:967px;object-fit:cover" alt="">
  </div>
  <div id="s1-pastille" class="a np" style="left:72px;top:922px;padding:20px 30px 18px;background:{C['ciel']};border-radius:6px;font-size:50px">{esc("Disponibles à l'accueil")}</div>
  <div class="a" style="left:66px;top:1060px;width:960px;height:130px;overflow:hidden" data-layout-allow-overflow><div id="s1-nm" class="nm" style="font-size:128px;color:{C['marine']}">NUTRIMUSCLE</div></div>
  <div class="a" style="left:66px;top:1188px;width:960px;height:124px;overflow:hidden" data-layout-allow-overflow><div id="s1-np" class="np" style="font-size:114px">&amp; NUTRIPURE</div></div>
  <p id="s1-corps" class="a corps" style="left:72px;top:1340px;width:936px">{corps}</p>
  {pied()}"""
    anim = """
      tl.from("#s1-photo", { scale: 1.08, duration: 5, ease: "none" }, 0);
      tl.from("#s1-pastille", { x: -700, duration: 0.5, ease: "power3.out" }, 0.15);
      tl.from("#s1-nm", { yPercent: 105, duration: 0.55, ease: "power3.out" }, 0.4);
      tl.from("#s1-np", { yPercent: 105, duration: 0.55, ease: "power3.out" }, 0.62);
      tl.from("#s1-corps", { y: 40, opacity: 0, duration: 0.5, ease: "power2.out" }, 0.95);
"""
    return C["fond_nm"], html, anim


def s2():
    lignes = []
    for i, (nom, desc) in enumerate(NM_PRODUITS):
        y = 1192 + i * 82
        lignes.append(
            f'<div id="s2-l{i}" class="a" style="left:72px;top:{y}px;width:936px;height:82px">'
            f'<span class="a nw" style="left:0;top:24px;font-weight:700;font-size:26px;color:{C["bleu"]};font-variant-numeric:tabular-nums">0{i + 1}</span>'
            f'<span class="a nw" style="left:60px;top:20px;font-weight:700;font-size:36px;color:{C["marine"]}">{esc(nom)}</span>'
            f'<span class="a nw" style="right:0;top:27px;font-weight:500;font-size:26px;color:{C["gris"]}">{esc(desc)}</span>'
            f'<span id="s2-f{i}" class="a" style="left:0;bottom:0;width:936px;height:2px;background:rgba(0,37,58,.16);transform-origin:left center"></span>'
            f'</div>')
    html = f"""
  <div id="s2-bloc" class="a" style="left:0;top:0;width:1080px;height:560px;background:{C['marine']};transform-origin:top center"></div>
  <div id="s2-kick" class="a kick" style="left:72px;top:300px;color:rgba(255,255,255,.72)">{esc("À l'accueil de LA SALLE")}</div>
  <div class="a" style="left:66px;top:354px;width:960px;height:132px;overflow:hidden" data-layout-allow-overflow><div id="s2-titre" class="nm" style="font-size:128px;color:#FFFFFF">NUTRIMUSCLE</div></div>
  <div id="s2-cadre" class="a" style="left:0;top:560px;width:1080px;height:603px;overflow:hidden" data-layout-allow-overflow>
    <img id="s2-photo" src="assets/img/etagere-nm.jpg" style="display:block;width:1080px;height:603px;object-fit:cover" alt="">
  </div>
  {''.join(lignes)}
  <div id="s2-cta" class="a nw" style="left:50%;top:1636px;transform:translateX(-50%);padding:26px 44px;background:{C['marine']};border-radius:6px;color:#FFFFFF;font-weight:800;font-size:34px;letter-spacing:.02em">{esc("DISPONIBLE À L'ACCUEIL DE LA SALLE")}</div>"""
    anim = """
      tl.from("#s2-bloc", { scaleY: 0, duration: 0.45, ease: "power3.inOut" }, 0);
      tl.from("#s2-kick", { y: 24, opacity: 0, duration: 0.4, ease: "power2.out" }, 0.3);
      tl.from("#s2-titre", { yPercent: 105, duration: 0.5, ease: "power3.out" }, 0.35);
      tl.from("#s2-cadre", { clipPath: "inset(0 100% 0 0)", duration: 0.6, ease: "power3.inOut" }, 0.45);
      tl.from("#s2-photo", { scale: 1.06, duration: 4.5, ease: "none" }, 0.45);
"""
    for i in range(len(NM_PRODUITS)):
        t = 0.95 + 0.12 * i
        anim += (f'      tl.from("#s2-l{i}", {{ x: 40, opacity: 0, duration: 0.4, ease: "power2.out" }}, {t:.2f});\n'
                 f'      tl.from("#s2-f{i}", {{ scaleX: 0, duration: 0.5, ease: "power2.inOut" }}, {t:.2f});\n')
    anim += '      tl.from("#s2-cta", { y: 50, opacity: 0, duration: 0.45, ease: "power3.out" }, 1.75);\n'
    return C["fond_nm"], html, anim


def s3():
    html = f"""
  <div id="s3-kick" class="a kick" style="left:72px;top:290px;color:{C['gris']}">{esc("À l'accueil de LA SALLE")}</div>
  <div class="a" style="left:60px;top:336px;width:980px;height:128px;overflow:hidden" data-layout-allow-overflow><div id="s3-titre" class="np" style="font-size:120px;padding-left:6px">NUTRIPURE</div></div>
  <div id="s3-carte" class="a" style="left:72px;top:500px;width:936px;height:997px;border-radius:16px;overflow:hidden">
    <img src="assets/img/nutripure-plv.jpg" style="display:block;width:936px;height:997px" alt="">
  </div>
  <div id="s3-prod" class="a np" style="left:72px;top:1530px;width:936px;text-align:center;font-size:38px;font-weight:800">{esc(NP_PRODUITS)}</div>
  <div id="s3-cta" class="a" style="left:220px;top:1600px;width:640px;height:132px;border-radius:66px;background:{C['ciel']};text-align:center">
    <div class="nw" style="padding-top:22px;font-weight:800;font-size:46px;line-height:1">Disponible</div>
    <div class="nw" style="padding-top:10px;font-weight:500;font-size:32px;line-height:1">{esc("à l'accueil de LA SALLE")}</div>
  </div>"""
    anim = """
      tl.from("#s3-kick", { y: 24, opacity: 0, duration: 0.4, ease: "power2.out" }, 0.05);
      tl.from("#s3-titre", { xPercent: -105, duration: 0.55, ease: "power3.out" }, 0.15);
      tl.from("#s3-carte", { y: 80, scale: 0.94, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.35);
      tl.from("#s3-prod", { y: 30, opacity: 0, duration: 0.4, ease: "power2.out" }, 0.9);
      tl.from("#s3-cta", { scale: 0.6, opacity: 0, duration: 0.5, ease: "back.out(1.8)" }, 1.15);
"""
    return C["fond_np"], html, anim


def s4():
    titre = ["UNE QUESTION", "SUR UN", "PRODUIT ?"]
    lignes = "".join(
        f'<div class="a" style="left:66px;top:{336 + i * 106}px;width:960px;height:110px;overflow:hidden" data-layout-allow-overflow>'
        f'<div id="s4-t{i}" class="nw" style="font-weight:900;font-size:108px;line-height:1.02;letter-spacing:-.02em">{esc(t)}</div></div>'
        for i, t in enumerate(titre))
    corps = esc("Passez à l'accueil : l'équipe vous présente les références disponibles des deux marques.")
    nm = "".join(f'<div class="nw" style="font-weight:500;font-size:30px;line-height:1.45;color:rgba(255,255,255,.86)">{esc(x)}</div>'
                 for x in ("Native Whey Protimuscle", "Lean Gainer Whey & Avoine", "Créatine Creapure®", "Collagène, magnésium"))
    np = "".join(f'<div class="nw" style="font-weight:500;font-size:30px;line-height:1.45">{esc(x)}</div>'
                 for x in ("Muscle Protein", "Créatine", "Shaker"))
    html = f"""
  <div id="s4-kick" class="a kick" style="left:72px;top:290px;color:{C['gris']}">NUTRIMUSCLE · NUTRIPURE</div>
  {lignes}
  <p id="s4-corps" class="a corps" style="left:72px;top:690px;width:936px">{corps}</p>
  <div id="s4-c1" class="a" style="left:72px;top:900px;width:452px;height:330px;border-radius:12px;background:{C['marine']};padding:38px 34px">
    <div class="nm" style="font-size:44px;color:#FFFFFF;margin-bottom:22px">NUTRIMUSCLE</div>{nm}
  </div>
  <div id="s4-c2" class="a" style="left:556px;top:900px;width:452px;height:330px;border-radius:12px;background:{C['ciel']};padding:38px 34px">
    <div class="np" style="font-size:44px;margin-bottom:22px">NUTRIPURE</div>{np}
  </div>
  {pied()}"""
    anim = """
      tl.from("#s4-kick", { y: 24, opacity: 0, duration: 0.4, ease: "power2.out" }, 0);
      tl.from(["#s4-t0", "#s4-t1", "#s4-t2"], { yPercent: 105, duration: 0.5, ease: "power3.out", stagger: 0.12 }, 0.1);
      tl.from("#s4-corps", { y: 40, opacity: 0, duration: 0.5, ease: "power2.out" }, 0.6);
      tl.from("#s4-c1", { y: 120, opacity: 0, duration: 0.55, ease: "power3.out" }, 0.85);
      tl.from("#s4-c2", { y: 120, opacity: 0, duration: 0.55, ease: "power3.out" }, 0.97);
"""
    return C["fond_nm"], html, anim


SCENES = [("s1", s1), ("s2", s2), ("s3", s3), ("s4", s4)]


def compo(cid, fond, html, anim):
    return f"""<!doctype html>
<html lang="fr">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template id="{cid}-template">
      <style>
{CSS}
        #{cid}-root {{ position: absolute; inset: 0; }}
      </style>
      <div id="{cid}-root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-duration="{DUREE:g}">
        <div id="{cid}-scene" class="st clip" data-start="0" data-duration="{DUREE:g}" data-track-index="0" style="background:{fond}">{html}
        </div>
      </div>
      <script>
        const tl = gsap.timeline({{ paused: true }});
{anim}        window.__timelines["{cid}"] = tl;
      </script>
    </template>
  </body>
</html>
"""


def index():
    hotes = "\n".join(
        f'      <div id="h-{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
        f'data-start="{i * DUREE:g}" data-duration="{DUREE:g}" data-track-index="1" data-width="1080" data-height="1920"></div>'
        for i, (cid, _) in enumerate(SCENES))
    return f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #F7F5F3; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #F7F5F3; }}
      [data-composition-id="main"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
    </style>
  </head>
  <body>
    <!-- 4 stories de 5 s : images fixes prises à la fin de chaque scène, vidéos découpées dans le rendu -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{len(SCENES) * DUREE:g}" data-width="1080" data-height="1920" data-fps="30">
{hotes}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def main():
    assets()
    os.makedirs(os.path.join(RACINE, "compositions"), exist_ok=True)
    for cid, fn in SCENES:
        fond, html, anim = fn()
        open(os.path.join(RACINE, "compositions", f"{cid}.html"), "w", encoding="utf-8").write(compo(cid, fond, html, anim))
    open(os.path.join(RACINE, "index.html"), "w", encoding="utf-8").write(index())
    print(f"{len(SCENES)} stories écrites dans {RACINE}")


if __name__ == "__main__":
    main()
