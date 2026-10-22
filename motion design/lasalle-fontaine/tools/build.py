"""Fontaine à boisson sportive LA SALLE : affiche 02/03 retravaillée (4:5) et story animée (9:16, 20 s).

Écrit :
  affiche-45/index.html                    affiche « COMMENT ÇA MARCHE » 1080×1350 (scène figée d'une seconde)
  story-916/index.html, compositions/*.html la story : les 6 visuels du carrousel rejoués texte par texte
Recopie dans <projet>/assets/ (ignorés par git) :
  polices et GSAP (_sources-premium/), logo (_communs/img/), fontaine détourée (~/fontaine-sources, hors dépôt),
  musique (story-916, fichier produit par tools/musique.py).

Les textes sont ceux des visuels fournis le 22/10/2026, mot pour mot ; seuls la mise en page et le mouvement changent.
Repères (secondes) : SCENES ci-dessous, partagés avec tools/musique.py et tools/livrer.py.

Usage : python3 tools/build.py   (puis tools/musique.py, rendu, tools/livrer.py)
"""
import os
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
MD = os.path.normpath(os.path.join(RACINE, ".."))
SOURCES = os.path.expanduser(os.environ.get("FONTAINE_SOURCES", "~/fontaine-sources"))

# Story : (id, début, durée) ; coupes sur la grille de 120 BPM (un temps = 0,5 s)
SCENES = [("s1", 0.0, 2.5), ("s2", 2.5, 4.5), ("s3", 7.0, 3.5), ("s4", 10.5, 3.0), ("s5", 13.5, 3.5), ("s6", 17.0, 3.0)]
DUREE = 20.0
CASSURE = (13.5, 14.0)     # musique coupée, « + 2 € » frappe à la reprise

PLUS = ('<svg class="plus" viewBox="-2 0 104 100" style="{s}"><polygon points="8.6,39 100.6,39 91.4,61 -0.6,61"/>'
        '<polygon points="59.05,0 82.95,0 40.95,100 17.05,100"/></svg>')

POLICES = "".join(
    f'@font-face {{ font-family: "{f}"; font-weight: {w}; font-style: {s}; font-display: block; '
    f'src: url("assets/fonts/{fic}") format("woff2"); }}\n'
    for f, w, s, fic in [
        ("Barlow Condensed", 700, "normal", "barlow-condensed-latin-700-normal.woff2"),
        ("Barlow Condensed", 800, "normal", "barlow-condensed-latin-800-normal.woff2"),
        ("Barlow Condensed", 800, "italic", "barlow-condensed-latin-800-italic.woff2"),
        ("Barlow Condensed", 900, "normal", "barlow-condensed-latin-900-normal.woff2"),
        ("Barlow Condensed", 900, "italic", "barlow-condensed-latin-900-italic.woff2"),
        ("DM Sans", 400, "normal", "dm-sans-latin-400-normal.woff2"),
        ("DM Sans", 500, "normal", "dm-sans-latin-500-normal.woff2"),
        ("DM Sans", 700, "normal", "dm-sans-latin-700-normal.woff2"),
    ])

# Atomes de la charte « Le Trait Oblique » (frame.md) : #0D0D0D, #F4F1EC, or #B8A07E, surface #222
CSS = POLICES + """
.fr { position: absolute; inset: 0; overflow: hidden; color: #F4F1EC; font-family: "Barlow Condensed", sans-serif; font-kerning: normal; }
.fr * { margin: 0; padding: 0; box-sizing: border-box; }
.fr .a { position: absolute; }
.fr .m { position: absolute; overflow: hidden; }
.fr .kick { font-family: "DM Sans", sans-serif; font-weight: 500; font-size: 34px; letter-spacing: .16em; text-transform: uppercase; color: #B8A07E; white-space: nowrap; line-height: 1; display: flex; align-items: center; gap: 18px; }
.fr .t9 { font-weight: 900; text-transform: uppercase; line-height: .88; letter-spacing: -.005em; white-space: nowrap; }
.fr .t8 { font-weight: 800; text-transform: uppercase; line-height: 1; white-space: nowrap; }
.fr .it { font-style: italic; }
.fr .or { color: #B8A07E; }
.fr .creux { color: transparent; -webkit-text-stroke: 3px #F4F1EC; background-image: linear-gradient(transparent, transparent); -webkit-background-clip: text; background-clip: text; }  /* lettres au trait (visuel ÉTAPE 02) */
.fr .corps { font-family: "DM Sans", sans-serif; font-weight: 500; line-height: 1.3; color: #F4F1EC; letter-spacing: -.01em; }
.fr .num { font-variant-numeric: tabular-nums; }
.fr .plus { fill: #B8A07E; overflow: visible; display: block; flex: none; }
.fr .puce { background: #222222; color: #F4F1EC; font-weight: 800; text-transform: uppercase; white-space: nowrap; display: flex; align-items: center; clip-path: polygon(var(--c) 0, 100% 0, calc(100% - var(--c)) 100%, 0 100%); }
.fr .mention { background: #222222; color: #F4F1EC; font-family: "DM Sans", sans-serif; font-weight: 500; letter-spacing: -.01em; }
.fr .filet { background: #B8A07E; }
.fr .point { width: 22px; height: 22px; border-radius: 50%; background: #B8A07E; outline: 7px solid rgba(184,160,126,.28); }
.fr .bande { display: flex; align-items: center; clip-path: polygon(37px 0, 100% 0, calc(100% - 37px) 100%, 0 100%); }
"""

# Fond commun : canvas, deux bandes obliques à peine plus claires (pente 0,42, comme les visuels), grain fin
FOND_CSS = """
.fond { position: absolute; inset: 0; background: #0D0D0D; overflow: hidden; }
.fond .b { position: absolute; top: 0; height: 100%; background: rgba(244,241,236,.022); }
.fond::after { content: ""; position: absolute; inset: 0; opacity: .7; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='256' height='256'><filter id='n' color-interpolation-filters='sRGB'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
"""


def fond(h, cid=""):
    d = round(0.42 * h)
    return (f'<div class="fond">'
            f'<div id="{cid}b1" class="b" style="left:-{d}px;width:{d + 380}px;clip-path:polygon({d}px 0,100% 0,calc(100% - {d}px) 100%,0 100%)"></div>'
            f'<div id="{cid}b2" class="b" style="left:{1080 - 260}px;width:{d + 420}px;clip-path:polygon({d}px 0,100% 0,calc(100% - {d}px) 100%,0 100%)"></div>'
            f'</div>')


def plus(taille, extra=""):
    return PLUS.format(s=f"width:{taille}px;height:{round(taille * 100 / 104)}px;{extra}")


def masque(left, top, w, h, inner, mid=""):
    i = f' id="{mid}"' if mid else ""
    return f'<div class="m" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px" data-layout-allow-overflow><div{i}>{inner}</div></div>'


def composition(cid, w, h, duree, corps, script):
    return f"""<!doctype html>
<html lang="fr">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template id="{cid}-template">
      <style>
{CSS}
        #{cid}-root {{ position: absolute; inset: 0; }}
      </style>
      <div id="{cid}-root" data-composition-id="{cid}" data-width="{w}" data-height="{h}" data-duration="{duree:g}">
        <div id="{cid}-scene" class="fr clip" data-start="0" data-duration="{duree:g}" data-track-index="0" style="width:{w}px;height:{h}px">
{corps}
        </div>
      </div>
      <script>
        const tl = gsap.timeline({{ paused: true }});
{script}
        window.__timelines["{cid}"] = tl;
      </script>
    </template>
  </body>
</html>
"""


# ---------------------------------------------------------------- textes (mot pour mot, visuels du 22/10/2026)
BOISSONS = ["COLLAGÈNE", "L-CARNITINE", "MULTIVITAMINES", "BCAA", "BOISSON CAFÉINÉE", "EAU AROMATISÉE"]
SAVEURS = ["PASSION", "PASTÈQUE", "ICE TEA", "ANANAS", "MULTIFRUIT"]
MENTION_CAFEINE = ("Boisson caféinée : teneur élevée en caféine, déconseillée aux enfants et aux femmes enceintes "
                   "ou allaitantes. Visuel non contractuel.")
MENTION_OPTION = ("Option Premium : 2 € TTC par semaine, soit 8 € prélevés toutes les 4 semaines en plus de votre "
                  "abonnement. Une boisson toutes les 30 minutes. Conditions à l’accueil.")
AVANTAGES = [("01", "FONTAINE À BOISSONS", "EN SERVICE"), ("02", "ANALYSE CORPORELLE 3D", "DÈS LE 22/10"),
             ("03", "SALLE DE POSING", "TRÈS BIENTÔT")]


def puces(ids, taille, h, pad, gap, prefixe):
    c = round(0.42 * h)
    return "".join(
        f'<div id="{prefixe}{k}" class="puce" style="--c:{c}px;height:{h}px;padding:0 {pad}px;font-size:{taille}px">{b}</div>'
        for k, b in enumerate(ids))


# ---------------------------------------------------------------- affiche 02/03 (4:5)
def affiche():
    # Fontaine : 1158×849 px affichée sur 540 px → 1 px de la capture d'origine = 3 × 540/1158 = 1,399 px
    W, X0, Y0 = 540, 64, 476
    k = 3 * W / 1158
    def px(x, y):
        return round(X0 + (x - 36) * k), round(Y0 + (y - 324) * k)
    e = px(292, 0)[0], 584            # point sur l'écran (bord droit de la dalle)
    g = px(247, 0)[0] + 12, 790       # point à droite de la gourde
    corps = f"""
{fond(1350)}
<img class="a" src="assets/img/logo-mono.png" alt="LA SALLE" style="left:108px;top:84px;height:70px">
<div class="a kick" style="left:auto;right:108px;top:102px;letter-spacing:.14em"><span class="num">02</span><span style="color:rgba(244,241,236,.62)">/ 03</span></div>
<div class="a kick" style="left:108px;top:196px">Comment ça marche</div>
<div class="a t9" style="left:104px;top:236px;font-size:118px">Votre boisson,</div>
<div class="a t9 it or" style="left:104px;top:340px;font-size:118px">À la carte.</div>
<img class="a" src="assets/img/fontaine.png" alt="" style="left:{X0}px;top:{Y0}px;width:{W}px">
<div class="a filet" style="left:{e[0]}px;top:{e[1] - 1}px;width:{596 - e[0]}px;height:3px"></div>
<div class="a point" style="left:{e[0] - 11}px;top:{e[1] - 11}px"></div>
<div class="a filet" style="left:{g[0]}px;top:{g[1] - 1}px;width:{596 - g[0]}px;height:3px"></div>
<div class="a point" style="left:{g[0] - 11}px;top:{g[1] - 11}px"></div>
<div class="a t8" style="left:612px;top:562px;font-size:46px">Écran tactile 17″</div>
<p class="a corps" style="left:612px;top:618px;width:362px;font-size:31px">Saveur, intensité, température&nbsp;: vous composez votre boisson.</p>
<div class="a t8" style="left:612px;top:768px;font-size:46px">1 boisson / 30 min</div>
<p class="a corps" style="left:612px;top:824px;width:362px;font-size:31px">À chaque séance, aussi souvent que vous venez.</p>
<div class="a kick" style="left:108px;top:924px;font-size:30px">Au choix</div>
<div class="a" style="left:104px;top:964px;width:880px;display:flex;flex-wrap:wrap;gap:12px 10px">{puces(BOISSONS, 37, 62, 28, 0, "p")}</div>
<div class="a kick" style="left:108px;top:1122px;font-size:30px">5 saveurs</div>
<div class="a t8" style="left:108px;top:1158px;font-size:40px;letter-spacing:.02em">Passion · Pastèque · Ice tea · Ananas · Multifruit</div>
<p class="a mention" style="left:72px;top:1222px;width:936px;padding:12px 24px;font-size:27px;line-height:1.28">{MENTION_CAFEINE}</p>
"""
    return composition("affiche", 1080, 1350, 1, corps, "")


def index_affiche():
    return """<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1350" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1080px; height: 1350px; overflow: hidden; background: #0D0D0D; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: #0D0D0D; }
      [data-composition-id="main"] > div[data-composition-src] { position: absolute; inset: 0; }
""" + FOND_CSS + """
    </style>
  </head>
  <body>
    <!-- Affiche 02/03 « COMMENT ÇA MARCHE », version lisible : scène figée d'une seconde, exportée par snapshot à 0,5 s -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="1" data-width="1080" data-height="1350" data-fps="30">
      <div id="h-affiche" data-composition-id="affiche" data-composition-src="compositions/affiche.html" data-start="0" data-duration="1" data-track-index="1" data-width="1080" data-height="1350"></div>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
"""


# ---------------------------------------------------------------- story (9:16)
def s1():
    corps = f"""
<div class="a kick" style="left:108px;top:318px">{plus(34)}Option Premium</div>
<img class="a" src="assets/img/logo-complet.png" alt="LA SALLE" style="left:792px;top:290px;width:180px">
<div id="s1-titre" class="a" style="left:104px;top:470px">
  <div class="t9 or" style="font-size:164px">Bien plus</div>
  <div class="t9" style="font-size:164px">que de</div>
  <div class="t9" style="font-size:164px">l’eau.</div>
</div>
{masque(108, 950, 864, 130, '<p class="corps" style="font-size:46px">La fontaine à boissons sportives<br>de l’option Premium.</p>', "s1-sous")}
<div class="a" style="left:108px;top:1170px">{plus(52)}</div>
<div id="s1-filet" class="a filet" style="left:182px;top:1192px;width:898px;height:6px;transform-origin:left center"></div>
"""
    js = """
        tl.fromTo("#s1-titre", { scale: 1 }, { scale: 1.035, duration: 2.5, ease: "none", transformOrigin: "left center" }, 0);
        tl.from("#s1-filet", { scaleX: 0, duration: 0.8, ease: "power2.out" }, 0.15);
        tl.from("#s1-sous", { yPercent: 110, duration: 0.5, ease: "power3.out" }, 0.5);
"""
    return corps, js


def s2():
    # Fontaine 1158×849 affichée sur 520 px : 1 px de la capture = 1,347 px
    W, X0, Y0 = 520, 52, 574
    k = 3 * W / 1158
    ex, ey = round(X0 + (292 - 36) * k), 702
    corps = f"""
{masque(108, 300, 864, 40, '<div class="kick">Comment ça marche</div>', "s2-kick")}
{masque(100, 340, 900, 102, '<div class="t9" style="font-size:114px">Votre boisson,</div>', "s2-l1")}
{masque(100, 438, 900, 106, '<div class="t9 it or" style="font-size:114px">À la carte.</div>', "s2-l2")}
<div id="s2-machine" class="a" style="left:{X0}px;top:{Y0}px;width:{W}px;height:{round(849 * W / 1158)}px">
  <img id="s2-img" src="assets/img/fontaine.png" alt="" style="display:block;width:{W}px">
</div>
<div id="s2-trait" class="a filet" style="left:{ex}px;top:{ey - 1}px;width:{574 - ex}px;height:3px;transform-origin:left center"></div>
<div id="s2-point" class="a point" style="left:{ex - 11}px;top:{ey - 11}px"></div>
{masque(588, 676, 400, 52, '<div class="t8" style="font-size:48px">Écran tactile 17″</div>', "s2-ct")}
{masque(588, 734, 392, 180, '<p class="corps" style="font-size:34px">Saveur, intensité, température&nbsp;: vous composez votre boisson.</p>', "s2-cb")}
{masque(108, 978, 864, 36, '<div class="kick" style="font-size:30px">Au choix</div>', "s2-kick2")}
<div class="a" style="left:104px;top:1016px;width:880px;display:flex;flex-wrap:wrap;gap:10px 10px">{puces(BOISSONS, 37, 56, 26, 0, "s2-p")}</div>
<p id="s2-mention" class="a mention" style="left:72px;top:1146px;width:936px;padding:12px 24px;font-size:28px;line-height:1.28">{MENTION_CAFEINE}</p>
"""
    js = """
        tl.from("#s2-kick", { yPercent: 110, duration: 0.4, ease: "power3.out" }, 0.05);
        tl.from("#s2-l1", { yPercent: 105, duration: 0.5, ease: "power3.out" }, 0.1);
        tl.from("#s2-l2", { yPercent: 105, duration: 0.5, ease: "power3.out" }, 0.3);
        tl.fromTo("#s2-machine", { clipPath: "inset(100% 0% 0% 0%)", y: 80 }, { clipPath: "inset(0% 0% 0% 0%)", y: 0, duration: 0.6, ease: "power3.out" }, 0.45);
        tl.fromTo("#s2-img", { scale: 1 }, { scale: 1.04, duration: 4.05, ease: "none", transformOrigin: "50% 60%" }, 0.45);
        tl.from("#s2-point", { scale: 0, duration: 0.3, ease: "back.out(2)" }, 1.05);
        tl.from("#s2-trait", { scaleX: 0, duration: 0.3, ease: "power2.out" }, 1.1);
        tl.from("#s2-ct", { yPercent: 110, duration: 0.4, ease: "power3.out" }, 1.25);
        tl.from("#s2-cb", { yPercent: 102, duration: 0.5, ease: "power3.out" }, 1.45);
        tl.from("#s2-kick2", { yPercent: 110, duration: 0.4, ease: "power3.out" }, 1.95);
"""
    js += "".join(
        f'        tl.from("#s2-p{i}", {{ clipPath: "inset(0% 100% 0% 0%)", x: -30, duration: 0.3, ease: "power3.out" }}, {2.05 + 0.14 * i:.2f});\n'
        for i in range(len(BOISSONS)))
    js += '        tl.from("#s2-mention", { clipPath: "inset(0% 0% 100% 0%)", duration: 0.4, ease: "power2.out" }, 2.2);\n'
    return corps, js


def s3():
    lignes = "".join(
        masque(100, 606 + 101 * i, 900, 104,
               f'<div class="t9{" creux" if i % 2 else ""}" style="font-size:114px;line-height:.9">{s}</div>', f"s3-f{i}")
        for i, s in enumerate(SAVEURS))
    corps = f"""
<div id="s3-deux" class="a t9 creux" aria-hidden="true" style="left:600px;top:760px;font-size:980px;-webkit-text-stroke:3px rgba(244,241,236,.16)">2</div>
{masque(108, 300, 864, 40, '<div class="kick">Étape <span class="num">02</span></div>', "s3-kick")}
{masque(100, 344, 900, 114, '<div class="t9" style="font-size:128px">Choisissez</div>', "s3-l1")}
{masque(100, 456, 900, 116, '<div class="t9" style="font-size:128px">votre saveur</div>', "s3-l2")}
{lignes}
{masque(108, 1150, 864, 120, '<p class="corps" style="font-size:42px">Cinq saveurs, au choix<br>sur l’écran tactile.</p>', "s3-corps")}
"""
    js = """
        tl.fromTo("#s3-deux", { y: 120 }, { y: 0, duration: 3.5, ease: "none" }, 0);
        tl.from("#s3-kick", { yPercent: 110, duration: 0.4, ease: "power3.out" }, 0.05);
        tl.from("#s3-l1", { yPercent: 105, duration: 0.5, ease: "power3.out" }, 0.1);
        tl.from("#s3-l2", { yPercent: 105, duration: 0.5, ease: "power3.out" }, 0.28);
"""
    js += "".join(
        f'        tl.from("#s3-f{i}", {{ xPercent: -105, duration: 0.42, ease: "power3.out" }}, {0.6 + 0.22 * i:.2f});\n'
        for i in range(len(SAVEURS)))
    js += '        tl.from("#s3-corps", { yPercent: 102, duration: 0.5, ease: "power3.out" }, 1.8);\n'
    return corps, js


def s4():
    corps = f"""
<svg id="s4-horloge" class="a" aria-hidden="true" viewBox="0 0 220 220" style="left:792px;top:868px;width:220px;height:220px;overflow:visible">
  <circle cx="110" cy="110" r="96" fill="none" stroke="rgba(244,241,236,.18)" stroke-width="4"/>
  <path id="s4-arc" d="M 110 14 A 96 96 0 0 1 110 206" fill="none" stroke="#B8A07E" stroke-width="10" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0"/>
  <line x1="110" y1="110" x2="110" y2="178" stroke="#B8A07E" stroke-width="6"/><circle cx="110" cy="110" r="9" fill="#B8A07E"/>
</svg>
{masque(108, 300, 864, 40, '<div class="kick">Étape <span class="num">03</span></div>', "s4-kick")}
{masque(100, 344, 900, 114, '<div class="t9" style="font-size:128px">Servez-vous</div>', "s4-l1")}
{masque(96, 520, 940, 164, '<div class="t9 num" style="font-size:184px">1 boisson</div>', "s4-l2")}
{masque(96, 682, 940, 164, '<div class="t9" style="font-size:184px">toutes les</div>', "s4-l3")}
<div id="s4-l4" class="a t9 or num" style="left:96px;top:858px;font-size:272px;transform-origin:left center">30 min</div>
{masque(108, 1136, 864, 120, '<p class="corps" style="font-size:42px">À chaque séance, aussi souvent<br>que vous venez.</p>', "s4-corps")}
"""
    js = """
        tl.from("#s4-kick", { yPercent: 110, duration: 0.4, ease: "power3.out" }, 0.05);
        tl.from("#s4-l1", { yPercent: 105, duration: 0.5, ease: "power3.out" }, 0.1);
        tl.from("#s4-l2", { yPercent: 105, duration: 0.45, ease: "power3.out" }, 0.4);
        tl.from("#s4-l3", { yPercent: 105, duration: 0.45, ease: "power3.out" }, 0.62);
        tl.fromTo("#s4-l4", { scale: 1.32, clipPath: "inset(0% 100% 0% 0%)" }, { scale: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.35, ease: "power4.out" }, 0.95);
        tl.from("#s4-arc", { attr: { "stroke-dashoffset": 1 }, duration: 0.7, ease: "power2.inOut" }, 0.95);
        tl.from("#s4-corps", { yPercent: 102, duration: 0.5, ease: "power3.out" }, 1.45);
"""
    return corps, js


def s5():
    bandes = ""
    for i, (n, nom, etat) in enumerate(AVANTAGES):
        fond_b, coul_n, coul_e = ("#B8A07E", "#0D0D0D", "#0D0D0D") if i == 0 else ("#222222", "#B8A07E", "#B8A07E")
        coul_t = "#0D0D0D" if i == 0 else "#F4F1EC"
        bandes += (f'<div id="s5-b{i}" class="a bande" style="left:108px;top:{962 + 98 * i}px;width:864px;height:88px;background:{fond_b}">'
                   f'<span class="t8 it num" style="font-size:50px;color:{coul_n};margin-left:62px;width:66px">{n}</span>'
                   f'<span class="t8" style="font-size:50px;color:{coul_t}">{nom}</span>'
                   f'<span class="kick" style="font-size:22px;color:{coul_e};letter-spacing:.14em;margin-left:auto;margin-right:62px">{etat}</span></div>')
    corps = f"""
<div class="a kick" style="left:108px;top:300px">{plus(34)}L’option Premium</div>
<div id="s5-prix" class="a" style="left:108px;top:356px;display:flex;align-items:center;gap:22px">
  <div id="s5-plus">{plus(170)}</div>
  <div id="s5-deux" class="t9 num" style="font-size:330px;line-height:.86">2 €</div>
</div>
<div id="s5-ttc" class="a t8 it" style="left:108px;top:664px;font-size:96px">TTC par semaine</div>
<p id="s5-soit" class="a corps" style="left:108px;top:772px;width:864px;font-size:42px">Soit 8&nbsp;€ toutes les 4 semaines,<br>en plus de votre abonnement.</p>
{masque(108, 918, 864, 36, '<div class="kick" style="font-size:30px">3 avantages inclus</div>', "s5-kick2")}
{bandes}
"""
    js = """
        tl.fromTo("#s5-plus", { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, duration: 0.35, ease: "back.out(1.6)" }, 0.5);
        tl.fromTo("#s5-deux", { scale: 1.3, clipPath: "inset(0% 100% 0% 0%)" }, { scale: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.35, ease: "power4.out", transformOrigin: "left center" }, 0.5);
        tl.fromTo(["#s5-ttc", "#s5-soit"], { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.35, ease: "power3.out" }, 0.5);
        tl.from("#s5-kick2", { yPercent: 110, duration: 0.35, ease: "power3.out" }, 1.05);
        tl.from("#s5-b0", { x: -1100, duration: 0.45, ease: "power3.out" }, 1.2);
        tl.from("#s5-b1", { x: -1100, duration: 0.45, ease: "power3.out" }, 1.4);
        tl.from("#s5-b2", { x: -1100, duration: 0.45, ease: "power3.out" }, 1.6);
"""
    return corps, js


def s6():
    corps = f"""
<div id="s6-logo" class="a" style="left:375px;top:290px;width:330px"><img src="assets/img/logo-complet.png" alt="LA SALLE" style="display:block;width:330px"></div>
{masque(40, 560, 1000, 134, '<div class="t9" style="font-size:152px;text-align:center">Activez-la</div>', "s6-l1")}
{masque(40, 694, 1000, 138, '<div class="t9" style="font-size:152px;text-align:center">à l’accueil.</div>', "s6-l2")}
{masque(40, 852, 1000, 80, '<div class="t8 it or" style="font-size:72px;text-align:center">En quelques secondes.</div>', "s6-l3")}
{masque(40, 966, 1000, 40, '<div class="kick" style="justify-content:center;font-size:32px">Urban Valley · 7J/7 · 6H–23H</div>', "s6-l4")}
<p id="s6-mention" class="a mention" style="left:108px;top:1040px;width:864px;padding:16px 26px;font-size:34px;line-height:1.26;text-align:center">{MENTION_OPTION}</p>
"""
    js = """
        tl.from("#s6-logo", { clipPath: "inset(0% 0% 100% 0%)", y: -30, duration: 0.4, ease: "power3.out" }, 0);
        tl.from("#s6-l1", { yPercent: 105, duration: 0.45, ease: "power3.out" }, 0.15);
        tl.from("#s6-l2", { yPercent: 105, duration: 0.45, ease: "power3.out" }, 0.35);
        tl.from("#s6-l3", { yPercent: 105, duration: 0.45, ease: "power3.out" }, 0.6);
        tl.from("#s6-l4", { yPercent: 110, duration: 0.4, ease: "power3.out" }, 0.8);
        tl.from("#s6-mention", { clipPath: "inset(100% 0% 0% 0%)", duration: 0.4, ease: "power2.out" }, 0.5);
"""
    return corps, js


def volets():
    """Volet oblique entre deux scènes : bande #0D0D0D (pente 0,42) au filet or sur le bord d'attaque, 0,5 s centrée sur la coupe."""
    coupes = [t for _, t, _ in SCENES[1:]]
    corps = "\n".join(f'<div id="volet{i}" class="a volet" data-layout-allow-overflow><div class="vb"></div><div class="vf"></div></div>' for i, _ in enumerate(coupes))
    js = "\n".join(
        f'        tl.fromTo("#volet{i}", {{ x: -2800 }}, {{ x: 1080, duration: 0.5, ease: "power1.inOut" }}, {t - 0.25:g});'
        for i, t in enumerate(coupes))
    return corps, js


def fond_story():
    js = """
        tl.fromTo("#fb1", { x: 0 }, { x: -90, duration: %g, ease: "none" }, 0);
        tl.fromTo("#fb2", { x: 0 }, { x: -60, duration: %g, ease: "none" }, 0);
""" % (DUREE, DUREE)
    return fond(1920, "f"), js


def index_story():
    hotes = "\n".join(
        f'      <div id="h-{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{t:g}" '
        f'data-duration="{d:g}" data-track-index="1" data-width="1080" data-height="1920"></div>'
        for c, t, d in SCENES)
    coupes = ", ".join(f"{t:g}" for _, t, _ in SCENES[1:])
    return f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0D0D0D; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #0D0D0D; }}
      [data-composition-id="main"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
{FOND_CSS}
      .volet {{ left: 0; top: 0; width: 2800px; height: 1920px; transform: translateX(-2800px); }}
      .volet .vb {{ position: absolute; inset: 0; background: #0D0D0D; clip-path: polygon(806px 0, 100% 0, calc(100% - 806px) 100%, 0 100%); }}
      .volet .vf {{ position: absolute; inset: 0; background: #B8A07E; clip-path: polygon(calc(100% - 12px) 0, 100% 0, calc(100% - 806px) 100%, calc(100% - 818px) 100%); }}
    </style>
  </head>
  <body>
    <!-- Story fontaine à boisson sportive : 6 visuels rejoués texte par texte, 20 s, 120 BPM ; coupes à {coupes} s -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUREE:g}" data-width="1080" data-height="1920" data-fps="30">
      <div id="h-fond" data-composition-id="fond" data-composition-src="compositions/fond.html" data-start="0" data-duration="{DUREE:g}" data-track-index="0" data-width="1080" data-height="1920"></div>
{hotes}
      <div id="h-volets" data-composition-id="volets" data-composition-src="compositions/volets.html" data-start="0" data-duration="{DUREE:g}" data-track-index="3" data-width="1080" data-height="1920"></div>
      <audio id="musique" src="assets/audio/musique.wav" data-start="0" data-duration="{DUREE:g}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


# ---------------------------------------------------------------- assets et projet
def logos():
    """Logo négatif du Drive (« LA_SALLE_logo_fond-noir », 2600×1607, blanc) : recadré, teinté #F4F1EC, monogramme seul."""
    dst = os.path.join(RACINE, "_communs", "img")
    if os.path.exists(os.path.join(dst, "logo-complet.png")):
        return
    from PIL import Image
    import numpy as np
    im = Image.open(os.path.join(SOURCES, "logo_fond_noir.png")).convert("RGBA")
    a = np.array(im)[..., 3]
    lignes = np.where(a.max(axis=1) > 16)[0]
    vide = np.where(np.diff(lignes) > 40)[0]            # bande vide entre monogramme et mot
    coupe = lignes[vide[0]] + 1
    def recadre(y0, y1, largeur, nom):
        sous = a[y0:y1]
        cols = np.where(sous.max(axis=0) > 16)[0]
        rows = np.where(sous.max(axis=1) > 16)[0]
        alpha = Image.fromarray(sous[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1])
        out = Image.new("RGBA", alpha.size, (244, 241, 236, 0))
        out.putalpha(alpha)
        out = out.resize((largeur, round(alpha.size[1] * largeur / alpha.size[0])), Image.LANCZOS)
        out.save(os.path.join(dst, nom), optimize=True)
    os.makedirs(dst, exist_ok=True)
    recadre(lignes[0], lignes[-1] + 1, 720, "logo-complet.png")
    recadre(lignes[0], coupe, 480, "logo-mono.png")


def projet(nom, w, h):
    p = os.path.join(RACINE, nom)
    for d in ("assets/fonts", "assets/vendor", "assets/img", "assets/audio", "compositions"):
        os.makedirs(os.path.join(p, d), exist_ok=True)
    for f in os.listdir(os.path.join(MD, "_sources-premium", "fonts")):
        shutil.copy2(os.path.join(MD, "_sources-premium", "fonts", f), os.path.join(p, "assets", "fonts", f))
    shutil.copy2(os.path.join(MD, "_sources-premium", "js", "gsap.min.js"), os.path.join(p, "assets", "vendor", "gsap.min.js"))
    for f in ("logo-complet.png", "logo-mono.png"):
        shutil.copy2(os.path.join(RACINE, "_communs", "img", f), os.path.join(p, "assets", "img", f))
    fontaine = os.path.join(SOURCES, "fontaine_detouree.png")
    if not os.path.exists(fontaine):
        sys.exit(f"Absent : {fontaine} (lancer tools/detourer.py)")
    shutil.copy2(fontaine, os.path.join(p, "assets", "img", "fontaine.png"))
    musique = os.path.join(RACINE, "_communs", "musique_fontaine.wav")
    if nom == "story-916" and os.path.exists(musique):
        shutil.copy2(musique, os.path.join(p, "assets", "audio", "musique.wav"))
    ecrire(os.path.join(p, "hyperframes.json"), """{
  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": {
    "blocks": "compositions",
    "components": "compositions/components",
    "assets": "assets"
  },
  "media": {
    "autoProxy": true
  }
}
""")
    ecrire(os.path.join(p, "package.json"), f"""{{
  "name": "lasalle-fontaine-{nom}",
  "private": true,
  "type": "module",
  "scripts": {{
    "dev": "npx --yes hyperframes@0.8.181 preview",
    "check": "npx --yes hyperframes@0.8.181 check",
    "render": "npx --yes hyperframes@0.8.181 render",
    "publish": "npx --yes hyperframes@0.8.181 publish"
  }}
}}
""")
    ecrire(os.path.join(p, "meta.json"), f'{{\n  "id": "lasalle-fontaine-{nom}",\n  "name": "lasalle-fontaine-{nom}",\n  "createdAt": "2026-10-22T08:00:00.000Z"\n}}\n')
    return p


def ecrire(chemin, texte):
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)


def main():
    logos()
    a = projet("affiche-45", 1080, 1350)
    ecrire(os.path.join(a, "index.html"), index_affiche())
    ecrire(os.path.join(a, "compositions", "affiche.html"), affiche())
    s = projet("story-916", 1080, 1920)
    ecrire(os.path.join(s, "index.html"), index_story())
    for (cid, _, d), f in zip(SCENES + [("fond", 0, DUREE), ("volets", 0, DUREE)], (s1, s2, s3, s4, s5, s6, fond_story, volets)):
        corps, js = f()
        ecrire(os.path.join(s, "compositions", f"{cid}.html"), composition(cid, 1080, 1920, d, corps, js))
    print("Écrit :", a, s)


if __name__ == "__main__":
    main()
