"""Génère les trois projets HyperFrames de la pub LE CUBE « LE CHRONO » : A (le chiffre), B (le défi), C (la nouvelle).

Même film de 15 s pour les trois, seule l'accroche (0–3 s) change :
  accroche (0–3) · rounds (3–8,5) · argument avec cassure (8,5–11,5) · carte finale (11,5–15) · chrono (0–15, au-dessus)
Instants : tools/cues.json (comme la musique). Design : _communs/frame.md. Les assets de _communs/ sont copiés dans
chaque projet (A/, B/, C/ : assets/ ignoré par git, régénéré ici).

Usage : python3 tools/build.py [A B C]
"""
import json
import os
import re
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
COMMUNS = os.path.join(RACINE, "_communs")
CUES = json.load(open(os.path.join(ICI, "cues.json"), encoding="utf-8"))
DUREE = CUES["duree"]
NB, FINE = " ", " "            # espace insécable ; fine insécable avant « ? »
BRONZE = "#B27639"

POLICES = "".join(
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:normal;font-display:block;'
    f'src:url("assets/fonts/{fichier}") format("woff2");}}\n'
    for fam, w, fichier in (("Oswald", 600, "oswald-latin-600-normal.woff2"), ("Oswald", 700, "oswald-latin-700-normal.woff2"),
                            ("Inter", 400, "inter-latin-400-normal.woff2"), ("Inter", 600, "inter-latin-600-normal.woff2"),
                            ("Inter", 700, "inter-latin-700-normal.woff2"), ("Anton", 400, "anton-latin-400-normal.woff2")))

CSS = POLICES + """#root{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}
.clip{position:absolute;left:0;top:0;width:1080px;height:1920px}
.ph{position:absolute;left:0;top:0;width:1080px;height:1920px;background-size:cover;background-position:center;transform-origin:50% 42%}
.voile{position:absolute;left:0;top:0;width:1080px;height:1920px;background:rgba(10,10,10,.52)}
.noir{position:absolute;left:0;top:0;width:1080px;height:1920px;background:#0A0A0A}
.a{position:absolute}
.centre{left:0;width:1080px;text-align:center}
.lab{font:600 44px/1 "Oswald";letter-spacing:.25em;color:#B27639;text-transform:uppercase;white-space:nowrap}
.nom{font:700 136px/1 "Oswald";color:#F5F2EC;text-transform:uppercase;white-space:nowrap}
.det{font:600 32px/1.2 "Inter";letter-spacing:.06em;color:rgba(245,242,236,.9);text-transform:uppercase;white-space:nowrap}
.ttl{font:700 104px/1.02 "Oswald";color:#F5F2EC;text-transform:uppercase;white-space:nowrap}
.num{font-family:"Anton";font-weight:400;line-height:.9;color:#B27639;white-space:nowrap}
.br{color:#B27639}
.masque{position:absolute;overflow:hidden;padding:.16em .04em .14em 0;margin-top:-.16em}
.masque>div{display:block}
.trait{position:absolute;height:8px;background:#B27639;transform-origin:0 50%}
"""

JS = """
  const $ = (id) => document.getElementById(id);
  // Coupes sèches : 1 ms (une durée nulle appliquerait l'état final dès la création)
  const montre = (id, t) => tl.fromTo($(id), { visibility: "hidden" }, { visibility: "visible", duration: 0.001, ease: "none", immediateRender: true }, t);
  const cache = (id, t) => tl.fromTo($(id), { visibility: "visible" }, { visibility: "hidden", duration: 0.001, ease: "none", immediateRender: false }, t);
  const frappe = (id, t, k = 1.25, d = 0.16) => tl.fromTo($(id), { scale: k }, { scale: 1, duration: d, ease: "power4.out" }, t);
  const chute = (id, t, d = 0.2) => tl.fromTo($(id), { yPercent: 110 }, { yPercent: 0, duration: d, ease: "power3.out" }, t);
  const balaie = (id, t, d = 0.24) => tl.fromTo($(id), { clipPath: "inset(0px 100% 0px 0px)" }, { clipPath: "inset(0px 0% 0px 0px)", duration: d, ease: "power3.out" }, t);
  const trace = (id, t, d = 0.2) => tl.fromTo($(id), { scaleX: 0 }, { scaleX: 1, duration: d, ease: "power3.out" }, t);
  const zoom = (id, t, d, a = 1.06) => tl.fromTo($(id), { scale: 1 }, { scale: a, duration: d, ease: "none" }, t);
"""


# photos claires ou chargées (mur blanc, rangées de kettlebells) : voile plus dense pour que le bronze se lise
VOILE = {img: ' style="background:rgba(10,10,10,.66)"' for img in ("tatami", "kettlebells", "boxes", "rig")}


def r(x):
    return f"{round(x, 3):g}"


class Compo:
    """Une sous-composition : calques « clip » minutés en secondes locales et une timeline GSAP."""

    def __init__(self, cid, duree):
        self.cid, self.duree, self.calques, self.js, self.piste = cid, duree, [], [], 0

    def calque(self, nom, debut, duree, contenu, piste=None):
        if piste is None:
            self.piste += 1
            piste = self.piste
        self.calques.append(f'    <div id="{self.cid}-{nom}" class="clip" data-start="{r(debut)}" data-duration="{r(duree)}" '
                            f'data-track-index="{piste}">{contenu}</div>')

    def photo(self, nom, image, debut, duree, zoom=1.06, origine=None):
        o = f";transform-origin:{origine}" if origine else ""
        self.nb_photos = getattr(self, "nb_photos", 0) + 1     # deux pistes en alternance : timeline lisible
        self.calque(nom, debut, duree, f'<div id="{self.cid}-{nom}-ph" class="ph" style="background-image:url(assets/img/{image}.jpg){o}"></div>'
                    f'<div class="voile"{VOILE.get(image, "")}></div>', piste=0 if self.nb_photos % 2 else 90)
        self.js.append(f'  zoom("{self.cid}-{nom}-ph", {r(debut)}, {r(duree)}, {zoom});')

    def texte(self, nom, debut, duree, html, entree="frappe", **k):
        """Un texte = un calque qui apparaît à son instant ; entrée frappe, chute (masque) ou balayage."""
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


def bloc(cls, texte, left=96, top=0, style="", centre=False):
    pos = "centre " if centre else ""
    gauche = "" if centre else f"left:{left}px;"
    return f'<div id="ID" class="a {pos}{cls}" style="{gauche}top:{top}px;{style}">{texte}</div>'


def masque(cls, texte, left=96, top=0, style="", centre=False):
    """Ligne qui monte dans un masque fixe ; le masque prend la taille de la police (ses marges sont en em)."""
    pos = "left:0;width:1080px;text-align:center;" if centre else f"left:{left}px;"
    taille = re.search(r"font-size:\s*(\d+)px", style)
    fs = f"font-size:{taille.group(1)}px;" if taille else ""
    return (f'<div class="masque" style="{pos}top:{top}px;{fs}"><div id="ID" class="{cls}" style="{style}">{texte}</div></div>')


# ─────────────────────────── accroches (0–3 s) ───────────────────────────
def accroche(v):
    c = Compo("accroche", 3.0)
    if v == "A":   # le chiffre : 165 cours en une semaine (relevé Resamania du 14/10/2026)
        for k, img in enumerate(["rig-wallballs", "sacs", "traineaux", "tatami", "kettlebells", "rig"]):
            c.photo(f"p{k}", img, 0.5 * k, 0.5, 1.03)
        c.texte("n165", 0, 3.0, bloc("num", "165", top=560, style="font-size:400px"), "frappe", k=1.1, d=0.3)
        c.texte("cours", 0, 3.0, bloc("ttl", "COURS", top=930, style="font-size:110px"), "frappe", k=1.08, d=0.3)
        c.texte("sem", 1.0, 2.0, masque("ttl", "EN UNE SEMAINE.", top=1062, style="font-size:76px"), "chute")
        c.texte("lieu", 2.0, 1.0, masque("ttl br", "UN SEUL LIEU.", top=1150, style="font-size:76px"), "chute")
    elif v == "B":  # le défi : t'as 15 secondes ? (le chrono démarre en grand, puis monte en haut)
        c.photo("p0", "chrono-led", 0, 3.0, 1.12, origine="62% 8%")
        c.texte("q1", 0, 1.5, bloc("ttl", "T'AS 15", top=1000, style="font-size:120px"), "frappe", k=1.08, d=0.3)
        c.texte("q2", 0, 1.5, bloc("ttl br", f"SECONDES{FINE}?", top=1120, style="font-size:120px"), "frappe", k=1.08, d=0.3)
        c.texte("r1", 1.85, 1.15, bloc("ttl", "ON TE MONTRE", top=640, style="font-size:120px"), "frappe")
        c.texte("r2", 2.1, 0.9, bloc("ttl br", "TOUT.", top=762, style="font-size:120px"), "frappe")
    else:           # la nouvelle : le Boxing Club passe de 50 à 400 m²
        c.photo("p0", "tatami", 0, 1.5, 1.04)
        c.photo("p1", "ring", 1.5, 1.5, 1.05)
        c.texte("lab", 0, 3.0, bloc("lab", "BOXING CLUB CONFLANS", top=560), "frappe", k=1.05, d=0.2)
        c.texte("n50", 0, 3.0, bloc("num", f"50{NB}m²", top=630, style="font-size:220px;color:#F5F2EC")
                .replace('id="ID"', 'id="ID" data-layout-allow-occlusion'), "frappe", k=1.1, d=0.3)   # rayé exprès
        c.texte("barre", 0.5, 2.5, '<div id="ID" class="trait" data-layout-allow-occlusion style="left:86px;top:716px;width:500px;height:14px"></div>', "trace", d=0.16)
        c.texte("n400", 1.0, 2.0, bloc("num", f"400{NB}m²", top=870, style="font-size:290px"), "frappe", k=1.3)
        c.texte("change", 1.75, 1.25, masque("ttl", "ÇA CHANGE TOUT.", top=1160, style="font-size:72px"), "chute")
    return c


# ─────────────────────────── rounds (3–8,5 s) ───────────────────────────
def rounds():
    t0g = CUES["rounds"][0]["t"]
    c = Compo("rounds", CUES["rounds"][-1]["fin"] - t0g)
    for k, rd in enumerate(CUES["rounds"]):
        t0, d = rd["t"] - t0g, rd["fin"] - rd["t"]
        if rd["photos"]:
            a, b = rd["photos"]
            c.photo(f"r{k}a", a, t0, 0.75)
            c.photo(f"r{k}b", b, t0 + 0.75, d - 0.75)
        else:   # pole dance : aucune photo sans personne, round typographique (barre de pole et cerceau)
            c.calque(f"r{k}noir", t0, d, '<div class="noir"></div>', piste=0)
            c.texte(f"r{k}pole", t0, d, f'<div id="ID" class="a" style="left:836px;top:300px;width:16px;height:950px;'
                    f'background:{BRONZE};transform-origin:50% 100%"></div>', "frappe", k=0, d=0.3)
            c.calque(f"r{k}cerceau", t0 + 0.15, d - 0.15,
                     f'<svg class="a" style="left:560px;top:880px;width:300px;height:300px" viewBox="0 0 300 300">'
                     f'<circle id="rounds-r{k}cerceau-t" cx="150" cy="150" r="132" fill="none" stroke="{BRONZE}" '
                     f'stroke-width="10" stroke-dasharray="829.4" transform="rotate(-90 150 150)"/></svg>')
            c.js.append(f'  tl.fromTo($("rounds-r{k}cerceau-t"), {{ strokeDashoffset: 829.4 }}, '
                        f'{{ strokeDashoffset: 0, duration: 0.4, ease: "power2.out" }}, {r(t0 + 0.15)});')
        c.texte(f"r{k}lab", t0, d, bloc("lab", f"ROUND {rd['numero']}", top=600), "balaie", d=0.18)
        c.texte(f"r{k}nom", t0, d, bloc("nom", rd["nom"], top=656), "frappe", k=1.2)
        c.texte(f"r{k}trait", t0 + 0.1, d - 0.1, f'<div id="ID" class="trait" style="left:100px;top:812px;width:150px"></div>', "trace")
        c.texte(f"r{k}det", t0 + 0.25, d - 0.25, bloc("det", rd["detail"], top=840), "balaie")
    return c


# ─────────────────────────── cassure et argument (8,5–11,5 s) ───────────────────────────
def argument():
    t0g = CUES["cassure"][0]
    a = CUES["argument"]
    c = Compo("argument", a["fin"] - t0g)
    tc = a["t"] - t0g                    # fin de la cassure
    t2 = a["deuxieme"] - t0g
    c.calque("noir", 0, tc, '<div class="noir"></div>', piste=0)
    c.texte("toi", 0, tc, bloc("ttl", f"ET TOI{FINE}?", top=700, style="font-size:150px", centre=True), "frappe", k=1.3)
    c.photo("p0", a["photos"][0], tc, t2 - tc)
    c.photo("p1", a["photos"][1], t2, c.duree - t2)
    for k, (txt, cls) in enumerate([("PAS BESOIN", "ttl"), ("D'ÊTRE EN FORME", "ttl"), ("POUR COMMENCER.", "ttl br")]):
        c.texte(f"l{k}", tc + 0.12 * k, t2 - tc - 0.12 * k, masque(cls, txt, top=640 + 106 * k, style="font-size:96px"), "chute")
    c.texte("m0", t2, c.duree - t2, bloc("ttl", f"C'EST POUR ÇA", top=680, style="font-size:116px"), "frappe")
    c.texte("m1", t2 + 0.12, c.duree - t2 - 0.12, bloc("ttl br", f"QU'ON EST LÀ.", top=816, style="font-size:116px"), "frappe")
    return c


# ─────────────────────────── carte finale (11,5–15 s) ───────────────────────────
def carte():
    t0g = CUES["carte"]
    c = Compo("carte", DUREE - t0g)
    d = c.duree
    cta = CUES["cta"] - t0g
    c.calque("noir", 0, d, '<div class="noir"></div>', piste=0)
    c.texte("nom", 0, d, bloc("nom", "LE CUBE", top=500, style="font-size:190px", centre=True), "frappe", k=1.2)
    c.texte("trait", 0.1, d - 0.1, f'<div id="ID" class="trait" style="left:330px;top:716px;width:420px;transform-origin:50% 50%"></div>', "trace")
    c.texte("disc", 0.25, d - 0.25, bloc("det", "CROSSFIT CSH · HYROX · BOXING CLUB · POLE DANCE", top=752, style="font-size:30px", centre=True), "balaie")
    c.texte("cta1", cta, d - cta, bloc("ttl br", "RÉSERVE TA", top=840, centre=True), "frappe")
    c.texte("cta2", cta + 0.12, d - cta - 0.12, bloc("ttl br", "SÉANCE D'ESSAI", top=944, centre=True), "frappe")
    c.texte("adresse", cta + 0.25, d - cta - 0.25, bloc("det", "ZAC DES BOUTRIES · CONFLANS-SAINTE-HONORINE", top=1172, style="font-size:28px", centre=True), "balaie")
    c.calque("chevron", cta + 0.5, d - cta - 0.5,
             f'<svg id="carte-chevron-t" class="a" style="left:500px;top:1076px;width:80px;height:50px" viewBox="0 0 80 50">'
             f'<polyline points="6,8 40,42 74,8" fill="none" stroke="{BRONZE}" stroke-width="9" stroke-linecap="square"/></svg>')
    c.js.append(f'  tl.fromTo($("carte-chevron-t"), {{ y: 0 }}, {{ y: 16, duration: 0.25, ease: "power1.inOut", yoyo: true, repeat: 7 }}, {r(cta + 0.5)});')
    return c


# ─────────────────────────── chrono (0–15 s, au-dessus de tout) ───────────────────────────
def chrono(v):
    ch = CUES["chrono"]
    c = Compo("chrono", DUREE)
    tics = [0.0] + [ch["premier_tic"] + k * ch["pas"] for k in range(ch["depart"])]      # 16 valeurs : 15 → 0
    chiffres = "".join(f'<div id="chrono-d{15 - k}" class="a num" style="left:0;top:14px;width:394px;text-align:center;'
                       f'font-size:104px;{"color:#0A0A0A" if k == 15 else ""}">00:{15 - k:02d}</div>' for k in range(16))
    boite = (f'<div id="chrono-boite" class="a" style="left:340px;top:300px;width:400px;height:128px;border:3px solid {BRONZE};'
             f'background:rgba(10,10,10,.82);overflow:hidden">{chiffres}</div>')
    c.calque("cadre", 0, DUREE, f'<div id="chrono-vol" class="a" style="left:0;top:0;width:1080px;height:1920px;'
             f'transform-origin:540px 364px">{boite}</div>', piste=1)
    debut_lab = 1.85 if v == "B" else 0.0
    c.calque("lab", debut_lab, DUREE - debut_lab, '<div class="a centre" style="top:448px;font:600 28px/1 Oswald;'
             'letter-spacing:.3em;color:rgba(245,242,236,.88)">LE CUBE · CONFLANS</div>', piste=2)
    for k, t in enumerate(tics):
        val = 15 - k
        c.js.append(f'  montre("chrono-d{val}", {r(t)});')
        if k + 1 < len(tics):
            c.js.append(f'  cache("chrono-d{val}", {r(tics[k + 1])});')
        if k:
            c.js.append(f'  tl.fromTo($("chrono-d{val}"), {{ yPercent: 32 }}, {{ yPercent: 0, duration: 0.1, ease: "power2.out" }}, {r(t)});')
    fin = tics[-1]
    c.js.append(f'  tl.fromTo($("chrono-boite"), {{ backgroundColor: "rgba(10,10,10,0.82)" }}, '
                f'{{ backgroundColor: "{BRONZE}", duration: 0.001, ease: "none", immediateRender: false }}, {r(fin)});')
    c.js.append(f'  tl.fromTo($("chrono-boite"), {{ scale: 1.18 }}, {{ scale: 1, duration: 0.2, ease: "power4.out", immediateRender: false }}, {r(fin)});')
    if v == "B":   # le chrono démarre en grand au centre, puis monte à sa place
        c.js.append('  tl.fromTo($("chrono-vol"), { y: 420, scale: 2.0 }, { y: 0, scale: 1, duration: 0.35, ease: "power3.inOut", immediateRender: true }, 1.5);')
    return c


def index_html(v, hotes):
    hs = "\n".join(f'      <div id="h-{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                   f'data-start="{r(s)}" data-duration="{r(d)}" data-track-index="{p}" data-width="1080" data-height="1920"></div>'
                   for cid, s, d, p in hotes)
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
      #h-chrono {{ z-index: 50; }}
    </style>
  </head>
  <body>
    <!-- LE CUBE · « LE CHRONO » · version {v} · 9:16 · 15 s · 120 BPM. Généré par lecube-chrono/tools/build.py -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r(DUREE)}" data-width="1080" data-height="1920" data-fps="30">
{hs}
      <audio id="musique" src="assets/audio/musique.wav" data-start="0" data-duration="{r(DUREE)}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


ACCROCHES = {"A": "le chiffre : « 165 COURS, EN UNE SEMAINE, UN SEUL LIEU. »",
             "B": "le défi : « T'AS 15 SECONDES ? », le chrono démarre en grand puis monte à sa place",
             "C": "la nouvelle : « BOXING CLUB CONFLANS, 50 m² barré, 400 m², ÇA CHANGE TOUT. »"}


def storyboard(v):
    lignes = [f"---\nduration: {r(DUREE)}\nmusic: none\nbpm: {CUES['bpm']}\ncues: ../tools/cues.json\n---\n",
              f"# LE CUBE « LE CHRONO » — version {v}\n",
              "Plan généré par `../tools/build.py` (une composition par scène). Design : `frame.md`.\n"]
    scenes = [("accroche", 0, 3.0, f"Accroche {v}, {ACCROCHES[v]}"),
              ("rounds", 3.0, 5.5, "4 rounds de 1,5 s (pole 1 s) : étiquette ROUND n, nom, trait, détail ; 2 photos par round, zoom lent"),
              ("argument", 8.5, 3.0, "Cassure 0,5 s « ET TOI ? » sur noir, puis « PAS BESOIN D'ÊTRE EN FORME POUR COMMENCER. » et « C'EST POUR ÇA QU'ON EST LÀ. »"),
              ("carte", 11.5, 3.5, "LE CUBE, disciplines, « RÉSERVE TA SÉANCE D'ESSAI », chevron vers le bouton, ZAC des Boutries"),
              ("chrono", 0, DUREE, "Calque au-dessus de tout : 00:15 → 00:00 sur les temps, boîte bronze pleine à 00:00")]
    for k, (cid, s, d, txt) in enumerate(scenes, 1):
        lignes.append(f"## Frame {k}\n- frame_id: {cid}\n- status: animated\n- src: compositions/{cid}.html\n"
                      f"- start: {r(s)}\n- duration: {r(d)}\n- rules: frappe d'échelle, chute dans un masque, balayage clip-path, zoom lent\n- beat: {txt}\n")
    return "\n".join(lignes)


def brief(v):
    return f"""---
workflow: general-video
flow: automation
storyboard: no
message: "LE CUBE : quatre disciplines coachées sous un même toit, ta séance d'essai t'attend."
destination: meta-reels
aspect: 1080x1920
language: fr
audience: "habitants de Conflans-Sainte-Honorine et alentours, 18-45 ans, curieux de CrossFit, Hyrox, boxe ou pole dance"
length: 15s
angle: "le chrono d'une séance : chaque discipline est un round"
narration: no
---

## Intent

Demande du 19/10/2026 : « propose moi une nouvelle vidéo de pub avec un concept différent pour le cube propose moi 3 variantes », puis « fait moi la production avec hyper frame des trois ensemble ». Concept retenu : « LE CHRONO ». Trois versions qui ne diffèrent que par l'accroche, pour un test A/B. Version {v} : {ACCROCHES[v]}.

## Assets

- Photos : les 12 photos du CUBE du Drive (dossier des pages du site), sans personne, recadrées en 9:16 et étalonnées noir et bronze (`../tools/photos.py`).
- Musique : originale, synthétisée (`../tools/musique.py`), 120 BPM, bips du chrono, cloche de ring, buzzer.
- Polices : Oswald, Inter, Anton (OFL, @fontsource).

## Customizations

- Pas de voix. Pas de prix. Tutoiement.
- Round 4 (pole dance) typographique : aucune photo de pole dance sans personne.
- « LE CUBE » écrit en Oswald : pas de fichier de logo trouvé.
"""


def main():
    versions = sys.argv[1:] or ["A", "B", "C"]
    for v in versions:
        proj = os.path.join(RACINE, v)
        comp = os.path.join(proj, "compositions")
        os.makedirs(comp, exist_ok=True)
        if os.path.exists(os.path.join(proj, "assets")):
            shutil.rmtree(os.path.join(proj, "assets"))
        shutil.copytree(os.path.join(COMMUNS, "assets"), os.path.join(proj, "assets"))
        shutil.copy(os.path.join(COMMUNS, "frame.md"), proj)
        compos = [(accroche(v), 0.0, 1), (rounds(), CUES["rounds"][0]["t"], 1), (argument(), CUES["cassure"][0], 1),
                  (carte(), CUES["carte"], 1), (chrono(v), 0.0, 2)]
        for c, _, _ in compos:
            open(os.path.join(comp, f"{c.cid}.html"), "w", encoding="utf-8").write(c.html())
        hotes = [(c.cid, s, c.duree, p) for c, s, p in compos]
        open(os.path.join(proj, "index.html"), "w", encoding="utf-8").write(index_html(v, hotes))
        open(os.path.join(proj, "STORYBOARD.md"), "w", encoding="utf-8").write(storyboard(v))
        open(os.path.join(proj, "BRIEF.md"), "w", encoding="utf-8").write(brief(v))
        print(f"construit {proj} : " + ", ".join(f"{c.cid} {r(s)}+{r(c.duree)}" for c, s, _ in compos))


if __name__ == "__main__":
    main()
