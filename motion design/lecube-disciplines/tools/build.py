"""Génère le projet HyperFrames d'une pub LE CUBE par discipline (15 s, 9:16), avec de vraies photos de pratiquants.

Structure commune, instants dans tools/cues_<discipline>.json (comme la musique) :
  accroche (0–3) : quatre mots, un par temps, chacun sur sa photo, puis la phrase en deux temps qui les relie
  étapes (3–8,5) : quatre étapes numérotées 01 → 04, une photo et deux lignes chacune
  argument (8,5–11,5) : cassure « ET TOI ? » sur noir, puis la phrase qui rassure
  carte (11,5–15) : discipline, niveaux, « RÉSERVE TA SÉANCE D'ESSAI », chevron vers le bouton, adresse
  bandeau (0–11,5, au-dessus) : « <DISCIPLINE> · LE CUBE », pour que celui qui part tôt sache où il est
Les photos montrent des personnes : elles viennent de ~/lecube-sources/img/ (tools/photos.py) et sont copiées dans
<discipline>/assets/img/, dossier ignoré par git (dépôt public). Design : frame.md.

Usage : python3 tools/build.py pole
"""
import json
import os
import re
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
COMMUNS = os.path.join(RACINE, "_communs")
IMAGES = os.path.expanduser("~/lecube-sources/img")
POLICES_GSAP = os.path.normpath(os.path.join(RACINE, "..", "lecube-chrono", "_communs", "assets"))
FINE = " "            # fine insécable avant « ? »
BRONZE = "#B27639"

POLICES = "".join(
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:normal;font-display:block;'
    f'src:url("assets/fonts/{fichier}") format("woff2");}}\n'
    for fam, w, fichier in (("Oswald", 600, "oswald-latin-600-normal.woff2"), ("Oswald", 700, "oswald-latin-700-normal.woff2"),
                            ("Inter", 600, "inter-latin-600-normal.woff2"), ("Anton", 400, "anton-latin-400-normal.woff2")))

CSS = POLICES + """#root{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}
.clip{position:absolute;left:0;top:0;width:1080px;height:1920px}
.ph{position:absolute;left:0;top:0;width:1080px;height:1920px;background-size:cover;background-position:center;transform-origin:50% 45%}
.voile{position:absolute;left:0;top:0;width:1080px;height:1920px;background:linear-gradient(180deg,rgba(10,10,10,.7) 0%,rgba(10,10,10,.56) 30%,rgba(10,10,10,.16) 60%,rgba(10,10,10,.28) 100%)}
.noir{position:absolute;left:0;top:0;width:1080px;height:1920px;background:#0A0A0A}
.a{position:absolute}
.centre{left:0;width:1080px;text-align:center}
.mot{font:700 170px/1 "Oswald";color:#F5F2EC;text-transform:uppercase;white-space:nowrap}
.ttl{font:700 104px/1.02 "Oswald";color:#F5F2EC;text-transform:uppercase;white-space:nowrap}
.num{font-family:"Anton";font-weight:400;line-height:.9;color:#B27639;white-space:nowrap}
.det{font:600 30px/1.2 "Inter";letter-spacing:.06em;color:rgba(245,242,236,.92);text-transform:uppercase;white-space:nowrap}
.br{color:#B27639}
.pl{background:#0A0A0A;padding:.07em .2em .03em}
.masque{position:absolute;overflow:hidden;padding:.16em .04em .14em 0;margin-top:-.16em}
.masque>div{display:block}
.trait{position:absolute;height:8px;background:#B27639;transform-origin:0 50%}
"""

JS = """
  const $ = (id) => document.getElementById(id);
  const frappe = (id, t, k = 1.25, d = 0.16) => tl.fromTo($(id), { scale: k }, { scale: 1, duration: d, ease: "power4.out" }, t);
  const chute = (id, t, d = 0.2) => tl.fromTo($(id), { yPercent: 110 }, { yPercent: 0, duration: d, ease: "power3.out" }, t);
  const balaie = (id, t, d = 0.24) => tl.fromTo($(id), { clipPath: "inset(0px 100% 0px 0px)" }, { clipPath: "inset(0px 0% 0px 0px)", duration: d, ease: "power3.out" }, t);
  const trace = (id, t, d = 0.2) => tl.fromTo($(id), { scaleX: 0 }, { scaleX: 1, duration: d, ease: "power3.out" }, t);
  const zoom = (id, t, d, a = 1.06) => tl.fromTo($(id), { scale: 1 }, { scale: a, duration: d, ease: "none" }, t);
"""

# Voile par défaut : dégradé, dense en haut sous les textes (y 290–900), léger sur les corps. Les lignes posées
# sur les corps ont leur bandeau noir (.pl), le bronze sur la peau ne se lirait pas.
# Photos à fond blanc : voile uniforme plus dense pour que le texte se lise.
VOILE = {"pole-nb": 0.6}


def r(x):
    return f"{round(x, 3):g}"


class Compo:
    """Une sous-composition : calques « clip » minutés en secondes locales et une timeline GSAP."""

    def __init__(self, cid, duree):
        self.cid, self.duree, self.calques, self.js, self.piste, self.nb_photos = cid, duree, [], [], 0, 0

    def calque(self, nom, debut, duree, contenu, piste=None):
        if piste is None:
            self.piste += 1
            piste = self.piste
        self.calques.append(f'    <div id="{self.cid}-{nom}" class="clip" data-start="{r(debut)}" data-duration="{r(duree)}" '
                            f'data-track-index="{piste}">{contenu}</div>')

    def photo(self, nom, image, debut, duree, zoom=1.06, voile=None):
        v = voile if voile is not None else VOILE.get(image)
        style = f' style="background:rgba(10,10,10,{v})"' if v is not None else ""   # voile uniforme à la place du dégradé
        self.nb_photos += 1     # deux pistes en alternance : timeline lisible
        self.calque(nom, debut, duree, f'<div id="{self.cid}-{nom}-ph" class="ph" style="background-image:url(assets/img/{image}.jpg)"></div>'
                    f'<div class="voile"{style}></div>', piste=0 if self.nb_photos % 2 else 90)
        self.js.append(f'  zoom("{self.cid}-{nom}-ph", {r(debut)}, {r(duree)}, {zoom});')

    def texte(self, nom, debut, duree, html, entree="frappe", **k):
        el = f"{self.cid}-{nom}-t"
        self.calque(nom, debut, duree, html.replace("ID", el))
        self.js.append(f'  {entree}("{el}", {r(debut)}{"".join(f", {v}" for v in k.values())});')

    def html(self):
        return f"""<template>
  <style>
{CSS}  </style>
  <div id="root" data-composition-id="{self.cid}" data-width="1080" data-height="1920" data-duration="{r(self.duree)}">
{chr(10).join(self.calques)}
  </div>
  <script src="assets/vendor/gsap.min.js"></script>
  <script>
  (function () {{
  const tl = gsap.timeline({{ paused: true }});
{JS}
{chr(10).join(self.js)}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["{self.cid}"] = tl;
  }})();
  </script>
</template>
"""


def bloc(cls, texte, left=72, top=0, style="", centre=False):
    pos = "centre " if centre else ""
    gauche = "" if centre else f"left:{left}px;"
    return f'<div id="ID" class="a {pos}{cls}" style="{gauche}top:{top}px;{style}">{texte}</div>'


def masque(cls, texte, left=72, top=0, style="", centre=False):
    """Ligne qui monte dans un masque fixe ; le masque prend la taille de la police (ses marges sont en em)."""
    pos = "left:0;width:1080px;text-align:center;" if centre else f"left:{left}px;"
    taille = re.search(r"font-size:\s*(\d+)px", style)
    fs = f"font-size:{taille.group(1)}px;" if taille else ""
    return f'<div class="masque" style="{pos}top:{top}px;{fs}"><div id="ID" class="{cls}" style="{style}">{texte}</div></div>'


def apos(s):
    return s.replace("'", "’")


# ─────────────────────────── accroche (0–3 s) ───────────────────────────
def accroche(C):
    a = C["accroche"]
    c = Compo("accroche", a["tout"] + 1.0)
    mots = a["mots"]
    for k, (t, mot, img) in enumerate(mots):
        fin = mots[k + 1][0] if k + 1 < len(mots) else a["tout"]
        c.photo(f"p{k}", img, t, fin - t, 1.05)
        if k == 0:   # la frame 0 porte déjà le premier mot, net et posé : pas d'entrée animée
            c.calque(f"m{k}", t, fin - t, bloc("mot", apos(mot), top=430).replace('id="ID" ', ""))
        else:
            c.texte(f"m{k}", t, fin - t, bloc("mot", apos(mot), top=430), "frappe", k=1.18, d=0.14)
    t2, t3 = a["tout"], a["barre"]
    c.photo("pf", a["photo_fin"], t2, c.duree - t2, 1.06)
    p1, p2 = a["phrase"]
    c.texte("tout", t2, c.duree - t2, masque("ttl", apos(p1), top=440, style="font-size:120px"), "chute")
    c.texte("barre", t3, c.duree - t3, masque("ttl br", apos(p2), top=570, style="font-size:120px"), "chute")
    return c


# ─────────────────────────── étapes (3–8,5 s) ───────────────────────────
def etapes(C):
    E = C["etapes"]
    t0g = E[0]["t"]
    c = Compo("etapes", E[-1]["fin"] - t0g)
    for k, e in enumerate(E):
        t0, d = e["t"] - t0g, e["fin"] - e["t"]
        c.photo(f"e{k}", e["photo"], t0, d, 1.06)
        c.texte(f"e{k}n", t0, d, bloc("num", e["numero"], top=420, style="font-size:150px"), "frappe", k=1.3, d=0.18)
        c.texte(f"e{k}tr", t0 + 0.06, d - 0.06, '<div id="ID" class="trait" style="left:76px;top:580px;width:120px"></div>', "trace", d=0.16)
        c.texte(f"e{k}l1", t0 + 0.1, d - 0.1, masque("ttl pl", apos(e["ligne1"]), top=630, style="font-size:104px"), "chute")
        c.texte(f"e{k}l2", t0 + 0.2, d - 0.2, masque("ttl br pl", apos(e["ligne2"]), top=748, style="font-size:104px"), "chute")
    return c


# ─────────────────────────── cassure et argument (8,5–11,5 s) ───────────────────────────
def argument(C):
    t0g = C["cassure"][0]
    a = C["argument"]
    c = Compo("argument", a["fin"] - t0g)
    tc, t2 = a["t"] - t0g, a["deuxieme"] - t0g
    c.calque("noir", 0, tc, '<div class="noir"></div>', piste=0)
    c.texte("toi", 0, tc, bloc("ttl", f"ET TOI{FINE}?", top=700, style="font-size:150px", centre=True), "frappe", k=1.3)
    c.photo("p0", a["photos"][0], tc, t2 - tc)
    c.photo("p1", a["photos"][1], t2, c.duree - t2)
    l1, l2 = a["lignes"]
    for k, txt in enumerate(l1):
        cls = "ttl br pl" if k == len(l1) - 1 else "ttl pl"
        c.texte(f"l{k}", tc + 0.12 * k, t2 - tc - 0.12 * k, masque(cls, apos(txt), top=640 + 112 * k, style="font-size:96px"), "chute")
    for k, txt in enumerate(l2):
        cls = "ttl br pl" if k == len(l2) - 1 else "ttl pl"
        c.texte(f"m{k}", t2 + 0.12 * k, c.duree - t2 - 0.12 * k, bloc(cls, apos(txt), top=680 + 140 * k, style="font-size:116px"), "frappe")
    return c


# ─────────────────────────── carte finale (11,5–15 s) ───────────────────────────
def carte(C):
    t0g = C["carte"]
    c = Compo("carte", C["duree"] - t0g)
    d = c.duree
    cta = C["cta"] - t0g
    c.photo("fond", C["carte_photo"], 0, d, 1.04, voile=0.74)
    c.texte("nom", 0, d, bloc("ttl", C["discipline"], top=470, style="font-size:170px", centre=True), "frappe", k=1.2)
    c.texte("cube", 0.12, d - 0.12, bloc("det", "AU CUBE · CONFLANS", top=664, style="font-size:34px;letter-spacing:.3em;color:#B27639", centre=True), "balaie")
    c.texte("trait", 0.2, d - 0.2, '<div id="ID" class="trait" style="left:420px;top:724px;width:240px;transform-origin:50% 50%"></div>', "trace")
    c.texte("niv", 0.3, d - 0.3, bloc("det", apos(C["carte_detail"]), top=760, centre=True), "balaie")
    c.texte("cta1", cta, d - cta, bloc("ttl br", "RÉSERVE TA", top=850, centre=True), "frappe")
    c.texte("cta2", cta + 0.12, d - cta - 0.12, bloc("ttl br", "SÉANCE D’ESSAI", top=954, centre=True), "frappe")
    c.calque("chevron", cta + 0.5, d - cta - 0.5,
             f'<svg id="carte-chevron-t" class="a" style="left:500px;top:1084px;width:80px;height:50px" viewBox="0 0 80 50">'
             f'<polyline points="6,8 40,42 74,8" fill="none" stroke="{BRONZE}" stroke-width="9" stroke-linecap="square"/></svg>')
    c.js.append(f'  tl.fromTo($("carte-chevron-t"), {{ y: 0 }}, {{ y: 16, duration: 0.25, ease: "power1.inOut", yoyo: true, repeat: 7 }}, {r(cta + 0.5)});')
    c.texte("adresse", cta + 0.25, d - cta - 0.25, bloc("det", "LE CUBE · ZAC DES BOUTRIES · CONFLANS-SAINTE-HONORINE", top=1176, style="font-size:26px", centre=True), "balaie")
    return c


# ─────────────────────────── bandeau (0 → carte, au-dessus de tout) ───────────────────────────
def bandeau(C):
    c = Compo("bandeau", C["carte"])
    texte = f'{C["discipline"]} · LE CUBE'
    c.calque("cadre", 0, c.duree, f'<div class="a centre" style="top:300px"><div style="display:inline-block;padding:14px 30px 12px;'
             f'border:3px solid {BRONZE};background:rgba(10,10,10,.72);font:600 34px/1 Oswald;letter-spacing:.24em;'
             f'color:#F5F2EC;white-space:nowrap">{texte}</div></div>', piste=1)
    return c


def index_html(d, C, hotes):
    hs = "\n".join(f'      <div id="h-{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                   f'data-start="{r(s)}" data-duration="{r(du)}" data-track-index="{p}" data-width="1080" data-height="1920"></div>'
                   for cid, s, du, p in hotes)
    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0A0A0A; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #0A0A0A; }}
      [data-composition-id="main"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
      #h-bandeau {{ z-index: 50; }}
    </style>
  </head>
  <body>
    <!-- LE CUBE · {C["discipline"]} · 9:16 · 15 s · 120 BPM. Généré par lecube-disciplines/tools/build.py -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r(C["duree"])}" data-width="1080" data-height="1920" data-fps="30">
{hs}
      <audio id="musique" src="assets/audio/musique.wav" data-start="0" data-duration="{r(C["duree"])}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def main():
    for d in sys.argv[1:] or ["pole"]:
        C = json.load(open(os.path.join(ICI, f"cues_{d}.json"), encoding="utf-8"))
        proj = os.path.join(RACINE, d)
        comp = os.path.join(proj, "compositions")
        os.makedirs(comp, exist_ok=True)
        assets = os.path.join(proj, "assets")
        if os.path.exists(assets):
            shutil.rmtree(assets)
        for sous in ("fonts", "vendor"):           # polices (OFL) et GSAP : ceux de la pub « LE CHRONO »
            shutil.copytree(os.path.join(POLICES_GSAP, sous), os.path.join(assets, sous))
        os.makedirs(os.path.join(assets, "img"), exist_ok=True)
        os.makedirs(os.path.join(assets, "audio"), exist_ok=True)
        for f in sorted(os.listdir(IMAGES)):
            if f.startswith(d + "-"):
                shutil.copy(os.path.join(IMAGES, f), os.path.join(assets, "img"))
        son = os.path.join(RACINE, "_communs", f"musique_{d}.wav")
        if os.path.exists(son):
            shutil.copy(son, os.path.join(assets, "audio", "musique.wav"))
        compos = [(accroche(C), 0.0, 1), (etapes(C), C["etapes"][0]["t"], 1), (argument(C), C["cassure"][0], 1),
                  (carte(C), C["carte"], 1), (bandeau(C), 0.0, 2)]
        for c, _, _ in compos:
            open(os.path.join(comp, f"{c.cid}.html"), "w", encoding="utf-8").write(c.html())
        open(os.path.join(proj, "index.html"), "w", encoding="utf-8").write(index_html(d, C, [(c.cid, s, c.duree, p) for c, s, p in compos]))
        print(f"construit {proj} : " + ", ".join(f"{c.cid} {r(s)}+{r(c.duree)}" for c, s, _ in compos))


if __name__ == "__main__":
    main()
