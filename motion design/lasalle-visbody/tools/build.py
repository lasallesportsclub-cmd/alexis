"""Analyse 3D Visbody M60 LA SALLE : story animée (9:16, 39 s, 60 i/s) et affiche « programme IA » (4:5).

Écrit :
  story-916/index.html, compositions/*.html  la story : les 8 visuels fournis le 22/10/2026 rejoués texte par texte,
                                             plus l'accroche « BIEN PLUS QU'UNE BALANCE. », la ponctuation « UNE
                                             BALANCE IA. » et le visuel « VOTRE PROGRAMME, PAR L'IA. » (⚠ A_valider.md)
  affiche-45/index.html                      le visuel « programme IA » au format des affiches du carrousel (1080×1350)
Recopie dans <projet>/assets/ (ignorés par git) : polices et GSAP (_sources-premium/), logo (lasalle-fontaine/_communs/
img/), Visbody M60 détourée (~/visbody-sources, hors dépôt : photo fabricant, logo de la marque à l'écran), musique.

Mêmes atomes et même mise en page plein cadre que lasalle-fontaine (retours du 22/10) : texte entre x 96–984 et
y 210–1 660, caches à la hauteur réelle du texte, dévoilement en biais de VOLET s sous un filet or, 60 i/s.
Repères : SCENES et T ci-dessous ; reperes() les donne en absolu à tools/musique.py.

Usage : python3 tools/build.py   (puis tools/musique.py, rendu, tools/livrer.py)
"""
import json
import os
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
MD = os.path.normpath(os.path.join(RACINE, ".."))
SOURCES = os.path.expanduser(os.environ.get("VISBODY_SOURCES", "~/visbody-sources"))

# Story : (id, coupe, temps jusqu'à la coupe suivante) ; coupes sur la grille de 120 BPM (un temps = 0,5 s)
SCENES = [("s1", 0.0, 2.5), ("s2", 2.5, 2.5), ("s3", 5.0, 4.0), ("s4", 9.0, 10.5), ("s5", 19.5, 4.5),
          ("s6", 24.0, 4.0), ("s7", 28.0, 3.5), ("s8", 31.5, 4.0), ("s9", 35.5, 3.5)]
DUREE = 39.0
FPS = 60
VOLET = 0.9                # dévoilement en biais, centré sur chaque coupe
COUPES_SECHES = {"s2"}     # « UNE BALANCE » arrive en coupe sèche, sur le silence
CASSURE = (2.5, 3.0)       # musique coupée, « IA. » frappe à la reprise
# Entrées de chaque scène, en secondes après sa coupe ; « pas » = écart entre deux éléments d'une liste
T = {
    "s1": {"filet": 0.15},
    "s2": {"ia": 0.5, "tech": 0.95},
    "s3": {"badge": 0.05, "l1": 0.15, "l2": 0.3, "l3": 0.45, "machine": 0.5, "sous": 1.0, "pastille": 1.5,
           "qual": 1.65, "mention": 1.8},
    # s4, premier temps : l'avatar sort du plateau, le scan descend (tours) puis remonte (maillage) ; les 3 étapes
    # du visuel « Le principe » en sous-titres synchronisés. Second temps : la machine et ses 3 légendes.
    "s4": {"kick": 0.05, "l1": 0.15, "l2": 0.35, "plateau": 0.45, "montee": 0.75, "e0": 0.8, "descente": 2.0,
           "e1": 2.0, "remontee": 3.5, "e2": 4.9, "bascule": 6.0, "tag": 6.25, "machine": 6.35, "legendes": 6.9,
           "pas_leg": 0.55, "mention": 8.4},
    "s5": {"kick": 0.05, "l1": 0.15, "l2": 0.35, "items": 0.7, "pas": 0.2, "corps": 1.9, "mention": 2.2},
    "s6": {"kick": 0.05, "l1": 0.15, "l2": 0.3, "l3": 0.45, "etapes": 0.95, "pas": 0.4},
    "s7": {"kick": 0.05, "l1": 0.15, "l2": 0.35, "l3": 0.7, "l4": 0.95, "l5": 1.25, "corps": 1.8},
    "s8": {"kick": 0.05, "prix": 0.4, "kick2": 1.1, "bandes": 1.25, "pas": 0.22},
    "s9": {"logo": 0.0, "l1": 0.15, "l2": 0.35, "l3": 0.65, "l4": 0.85, "mention": 0.6},
}

# ---------------------------------------------------------------- textes (mot pour mot, visuels du 22/10/2026)
ETAPES_SCAN = ["Montez sur le plateau.",
               "Il tourne sur 360° pendant que la Visbody scanne votre silhouette en 3D.",
               "Vos résultats s’affichent à l’écran."]
TECH = "Capteur de profondeur 3D, intelligence artificielle et impédancemétrie 8 électrodes multifréquence."
LEGENDES = [("Silhouette 3D", "Votre corps modélisé et mesuré&nbsp;: tours de taille, de bras, de cuisses."),
            ("Composition", "Masse musculaire et masse grasse, par impédancemétrie 8 électrodes."),
            ("Posture", "Analysée pendant que le plateau tourne sur 360°.")]
RESULTATS = ["Masse musculaire", "Masse grasse", "Mensurations", "Posture", "Silhouette 3D"]
MENTION_OFFRE = ("Option Premium : 8 € toutes les 4 semaines en plus de l’abonnement après l’offre, sans engagement "
                 "sur l’option. Visuel non contractuel.")
MENTION_SANTE_SCAN = ("Outil de suivi sportif : il ne remplace pas un avis médical. Déconseillé aux porteurs de pacemaker "
                      "ou d’implant électronique et aux femmes enceintes. Visuel non contractuel.")
MENTION_SANTE = ("Outil de suivi sportif, il ne remplace pas un avis médical. Déconseillé aux porteurs de pacemaker "
                 "ou d’implant électronique et aux femmes enceintes.")
MENTION_OPTION = ("Option Premium : 2 € TTC par semaine, soit 8 € prélevés toutes les 4 semaines en plus de votre "
                  "abonnement. Une analyse 3D par semaine. Conditions à l’accueil.")
AVANTAGES = [("01", "FONTAINE À BOISSONS", "EN SERVICE"), ("02", "ANALYSE CORPORELLE 3D", "DÈS LE 22/10"),
             ("03", "SALLE DE POSING", "TRÈS BIENTÔT")]
# ⚠ Textes ajoutés (pas dans les visuels fournis) : à valider par Mehdi, voir A_valider.md
ACCROCHE = ["Bien plus", "qu’une", "balance."]
ETAPES_IA = ["Votre analyse 3D.", "Votre objectif, fixé<br>avec votre coach.",
             "Un programme d’entraînement adapté aux machines de LA&nbsp;SALLE."]

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
.fr .creux { color: transparent; -webkit-text-stroke: 3px rgba(244,241,236,.14); background-image: linear-gradient(transparent, transparent); -webkit-background-clip: text; background-clip: text; }  /* chiffre fantôme au trait */
.fr .corps { font-family: "DM Sans", sans-serif; font-weight: 500; line-height: 1.3; color: #F4F1EC; letter-spacing: -.01em; }
.fr .num { font-variant-numeric: tabular-nums; }
.fr .plus { fill: #B8A07E; overflow: visible; display: block; flex: none; }
.fr .mention { background: #222222; color: #F4F1EC; font-family: "DM Sans", sans-serif; font-weight: 500; letter-spacing: -.01em; }
.fr .filet { background: #B8A07E; }
.fr .point { width: 22px; height: 22px; border-radius: 50%; background: #B8A07E; outline: 7px solid rgba(184,160,126,.28); }
.fr .plaque { background: #B8A07E; color: #0D0D0D; font-weight: 800; font-style: italic; text-transform: uppercase; white-space: nowrap; display: inline-flex; align-items: center; clip-path: polygon(var(--c) 0, 100% 0, calc(100% - var(--c)) 100%, 0 100%); }
.fr .plaque sup { font-size: .55em; vertical-align: .75em; margin-left: .04em; }
.fr .cadre { border: 2px solid rgba(184,160,126,.85); color: #F4F1EC; font-weight: 800; text-transform: uppercase; letter-spacing: .06em; white-space: nowrap; display: inline-flex; align-items: center; gap: 16px; }
.fr .etape { display: flex; align-items: baseline; }
.fr .etape .n { font-weight: 800; font-style: italic; color: #B8A07E; flex: none; }
.fr .vf { left: 0; top: 0; width: 818px; height: 1920px; background: #B8A07E; clip-path: polygon(806px 0, 818px 0, 12px 100%, 0 100%); }
"""

# Fond commun : canvas, deux bandes obliques à peine plus claires (pente 0,42, comme les visuels), grain fin
FOND_CSS = """
.fond { position: absolute; inset: 0; background: #0D0D0D; overflow: hidden; }
.fond .b { position: absolute; top: 0; height: 100%; background: rgba(244,241,236,.022); }
.fond::after { content: ""; position: absolute; inset: 0; opacity: .7; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='256' height='256'><filter id='n' color-interpolation-filters='sRGB'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
"""
PAD = 30
DEVOILE_DEBUT = "polygon(0px 0px, 0px 0px, -806px 1920px, 0px 1920px)"
DEVOILE_FIN = "polygon(0px 0px, 1886px 0px, 1080px 1920px, 0px 1920px)"
SCAN = 1.4                 # durée d'un passage du scan (descente, puis remontée)
# Visbody M60 détourée : 918×1878 px, issue d'une capture (1 px de la capture = 3 px), origine (26, 120)
M60 = (918, 1878, 26, 120)


def fond(h, cid=""):
    d = round(0.42 * h)
    return (f'<div class="fond">'
            f'<div id="{cid}b1" class="b" style="left:-{d}px;width:{d + 380}px;clip-path:polygon({d}px 0,100% 0,calc(100% - {d}px) 100%,0 100%)"></div>'
            f'<div id="{cid}b2" class="b" style="left:{1080 - 260}px;width:{d + 420}px;clip-path:polygon({d}px 0,100% 0,calc(100% - {d}px) 100%,0 100%)"></div>'
            f'</div>')


def plus(taille, extra=""):
    return PLUS.format(s=f"width:{taille}px;height:{round(taille * 100 / 104)}px;{extra}")


def m60(x0, y0, largeur):
    """Position sur la page d'un point de la capture d'origine, la machine étant posée en (x0, y0) sur largeur px."""
    k = 3 * largeur / M60[0]
    return lambda x, y: (round(x0 + (x - M60[2]) * k), round(y0 + (y - M60[3]) * k))


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


# ---------------------------------------------------------------- mécanique des scènes
def bornes(cid):
    """Début et fin de la scène : elle chevauche ses voisines de VOLET/2, sauf de part et d'autre d'une coupe sèche."""
    ids = [c for c, _, _ in SCENES]
    i = ids.index(cid)
    coupe = SCENES[i][1]
    debut = 0.0 if i == 0 else coupe if cid in COUPES_SECHES else coupe - VOLET / 2
    if i == len(SCENES) - 1:
        fin = DUREE
    else:
        suivante, t = SCENES[i + 1][0], SCENES[i + 1][1]
        fin = t if suivante in COUPES_SECHES else t + VOLET / 2
    return debut, fin


def at(cid, cle, k=0, pas="pas"):
    debut, _ = bornes(cid)
    coupe = dict((c, t) for c, t, _ in SCENES)[cid]
    return round(coupe - debut + T[cid][cle] + k * T[cid].get(pas, 0), 3)


def reperes():
    """Instants absolus des entrées, pour tools/musique.py."""
    c = dict((cid, t) for cid, t, _ in SCENES)
    return {
        "ia": c["s2"] + T["s2"]["ia"],
        "etapes": [c["s4"] + T["s4"][f"e{i}"] for i in range(3)],
        "scan": {k: c["s4"] + T["s4"][k] for k in ("plateau", "montee", "descente", "remontee")},
        "bascule": c["s4"] + T["s4"]["bascule"],
        "legendes": [c["s4"] + T["s4"]["legendes"] + i * T["s4"]["pas_leg"] for i in range(3)],
        "items": [c["s5"] + T["s5"]["items"] + i * T["s5"]["pas"] for i in range(len(RESULTATS))],
        "etapes_ia": [c["s6"] + T["s6"]["etapes"] + i * T["s6"]["pas"] for i in range(3)],
        "semaine": c["s7"] + T["s7"]["l5"],
        "prix": c["s8"] + T["s8"]["prix"],
        "bandes": [c["s8"] + T["s8"]["bandes"] + i * T["s8"]["pas"] for i in range(3)],
        "accueil": c["s9"] + T["s9"]["l2"],
    }


def cache(left, top, w, inner, mid, pad=PAD):
    """Glissement masqué : top est le haut du texte ; le cache déborde de pad au-dessus et au-dessous."""
    return (f'<div class="m" style="left:{left}px;top:{top - pad}px;width:{w}px;padding:{pad}px 0" '
            f'data-layout-allow-overflow><div id="{mid}">{inner}</div></div>')


def monte(mid, t, d=0.65, pad=PAD, ease="power3.out"):
    """Le texte part de sous le cache : sa hauteur + 2 × pad, pour que les accents (À, É) restent cachés aussi."""
    return (f'        tl.fromTo("#{mid}", {{ yPercent: 100, y: {2 * pad} }}, '
            f'{{ yPercent: 0, y: 0, duration: {d}, ease: "{ease}" }}, {t:.3f});\n')


def sort(mid, t, d=0.45, pad=PAD):
    """Le texte ressort par le haut du cache."""
    return (f'        tl.to("#{mid}", {{ yPercent: -100, y: {-2 * pad}, duration: {d}, ease: "power2.in" }}, {t:.3f});\n')


def scene(cid, contenu, js):
    """Fond opaque identique à celui de la story (le volet ne révèle que le texte), contenu dans #<cid>-c,
    dévoilement en biais à l'entrée et glissement de 60 px à la sortie, sauf autour d'une coupe sèche."""
    debut, fin = bornes(cid)
    ids = [c for c, _, _ in SCENES]
    i = ids.index(cid)
    corps = f'{fond(1920, cid + "-")}\n<div id="{cid}-c" class="a" style="inset:0">\n{contenu}\n</div>'
    if i > 0 and cid not in COUPES_SECHES:
        js = (f'        tl.fromTo("#{cid}-scene", {{ clipPath: "{DEVOILE_DEBUT}" }}, {{ clipPath: "{DEVOILE_FIN}", '
              f'duration: {VOLET}, ease: "sine.inOut" }}, 0);\n') + js
    if i < len(ids) - 1 and ids[i + 1] not in COUPES_SECHES:
        js += (f'        tl.to("#{cid}-c", {{ x: -60, duration: {VOLET}, ease: "sine.in" }}, '
               f'{fin - debut - VOLET:.3f});\n')
    return composition(cid, 1080, 1920, round(fin - debut, 3), corps, js)


def etapes(prefixe, textes, top, ecarts, taille_n, taille_t, largeur_t=740, x=96):
    return "".join(
        cache(x, top + sum(ecarts[:i]), 900,
              f'<div class="etape"><span class="n num" style="font-size:{taille_n}px;width:{round(taille_n * 1.5)}px">{i + 1:02d}</span>'
              f'<p class="corps" style="font-size:{taille_t}px;width:{largeur_t}px">{t}</p></div>', f"{prefixe}{i}", 24)
        for i, t in enumerate(textes))


# ---------------------------------------------------------------- scènes de la story
def s1():
    _, fin = bornes("s1")
    lignes = "".join(f'<div class="t9{" or" if i == 0 else ""}" style="font-size:168px;line-height:.92">{l}</div>'
                     for i, l in enumerate(ACCROCHE))
    contenu = f"""
<div class="a kick" style="left:96px;top:236px;font-size:38px">{plus(40)}Option Premium</div>
<img class="a" src="assets/img/logo-complet.png" alt="LA SALLE" style="left:774px;top:212px;width:210px">
<div id="s1-titre" class="a" style="left:92px;top:600px">{lignes}</div>
<div class="a" style="left:96px;top:1560px">{plus(60)}</div>
<div id="s1-filet" class="a filet" style="left:178px;top:1586px;width:902px;height:6px;transform-origin:left center"></div>
"""
    js = (f'        tl.fromTo("#s1-titre", {{ scale: 1 }}, {{ scale: 1.03, duration: {fin:g}, ease: "none", transformOrigin: "left center" }}, 0);\n'
          f'        tl.from("#s1-filet", {{ scaleX: 0, duration: 1.0, ease: "power2.out" }}, {at("s1", "filet")});\n')
    return scene("s1", contenu, js)


def s2():
    t = at("s2", "ia")
    contenu = f"""
<div class="a kick" style="left:96px;top:236px;font-size:38px">Nouveau · Analyse 3D</div>
<div class="a t9" style="left:92px;top:560px;font-size:156px">Une balance</div>
<div id="s2-ia" class="a t9 or" style="left:84px;top:730px;font-size:600px;line-height:.86;transform-origin:left center">IA.</div>
{cache(96, 1320, 888, f'<p class="corps" style="font-size:46px">{TECH}</p>', "s2-tech")}
"""
    js = (f'        tl.fromTo("#s2-ia", {{ scale: 1.35, clipPath: "inset(0% 100% 0% 0%)" }}, {{ scale: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power4.out" }}, {t});\n'
          + monte("s2-tech", at("s2", "tech"), 0.7))
    return scene("s2", contenu, js)


def s3():
    W, X0, Y0 = 350, 640, 360
    c = round(0.42 * 76)
    contenu = f"""
{cache(96, 236, 888, f'<div class="plaque" style="--c:{round(0.42 * 70)}px;height:70px;padding:0 40px;font-size:40px">La 3<sup>e</sup>&nbsp;salle de France équipée</div>', "s3-badge", 20)}
{cache(92, 390, 560, '<div class="t9" style="font-size:132px">Vos</div>', "s3-l1")}
{cache(92, 506, 560, '<div class="t9" style="font-size:132px">progrès,</div>', "s3-l2")}
{cache(92, 622, 560, '<div class="t9 it or" style="font-size:132px">en 3D.</div>', "s3-l3")}
<div id="s3-machine" class="a" style="left:{X0}px;top:{Y0}px;width:{W}px;height:{round(M60[1] * W / M60[0])}px">
  <img id="s3-img" src="assets/img/m60.png" alt="" style="display:block;width:{W}px">
</div>
{cache(96, 800, 530, '<p class="corps" style="font-size:44px">L’analyse corporelle Visbody M60, en service à LA SALLE dès le 22&nbsp;octobre.</p>', "s3-sous")}
{cache(96, 1170, 900, f'<div class="plaque" style="--c:{c}px;height:76px;padding:0 40px;font-size:44px">4 semaines offertes, puis 2&nbsp;€ TTC/sem.</div>', "s3-pastille", 20)}
{cache(96, 1266, 888, '<div class="t8" style="font-size:32px;letter-spacing:.03em">En ce moment · en plus de votre abonnement</div>', "s3-qual", 16)}
<p id="s3-mention" class="a mention" style="left:96px;top:1340px;width:888px;padding:16px 26px;font-size:32px;line-height:1.28">{MENTION_OFFRE}</p>
"""
    debut, fin = bornes("s3")
    tm = at("s3", "machine")
    js = (f'        tl.fromTo("#s3-badge", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.out" }}, {at("s3", "badge")});\n'
          + monte("s3-l1", at("s3", "l1")) + monte("s3-l2", at("s3", "l2")) + monte("s3-l3", at("s3", "l3"))
          + f'        tl.fromTo("#s3-machine", {{ clipPath: "inset(100% 0% 0% 0%)", y: 70 }}, {{ clipPath: "inset(0% 0% 0% 0%)", y: 0, duration: 0.8, ease: "power2.out" }}, {tm});\n'
          + f'        tl.fromTo("#s3-img", {{ scale: 1 }}, {{ scale: 1.04, duration: {fin - debut - tm:.3f}, ease: "none", transformOrigin: "50% 80%" }}, {tm});\n'
          + monte("s3-sous", at("s3", "sous"), 0.7) + monte("s3-pastille", at("s3", "pastille"), 0.55, 20)
          + monte("s3-qual", at("s3", "qual"), 0.5, 16)
          + f'        tl.from("#s3-mention", {{ clipPath: "inset(0% 0% 100% 0%)", duration: 0.5, ease: "power2.out" }}, {at("s3", "mention")});\n')
    return scene("s3", contenu, js)


def s4():
    W, X0, Y0 = 330, 40, 720
    p = m60(X0, Y0, W)
    points = [(p(244, 0)[0], 860), (p(262.5, 0)[0], 1100), (p(296, 0)[0], 1345)]   # écran, poignée droite, socle
    legendes = ""
    for i, ((px_, py), (titre, texte)) in enumerate(zip(points, LEGENDES)):
        legendes += (f'<div id="s4-t{i}" class="a filet" style="left:{px_}px;top:{py - 1}px;width:{440 - px_}px;height:3px;transform-origin:left center"></div>\n'
                     f'<div id="s4-p{i}" class="a point" style="left:{px_ - 11}px;top:{py - 11}px"></div>\n'
                     + cache(456, py - 24, 540, f'<div class="t8" style="font-size:50px">{titre}</div>', f"s4-lt{i}") + "\n"
                     + cache(456, py + 36, 528, f'<p class="corps" style="font-size:36px">{texte}</p>', f"s4-lb{i}") + "\n")
    # Avatar 3D (assets/js/avatar.js, Three.js) : toile de 640×1120 à droite, rendue depuis le temps de la scène
    debut, fin = bornes("s4")
    R = {"largeur": 640, "hauteur": 1120, "plateau": [at("s4", "plateau"), 0.5], "montee": [at("s4", "montee"), 0.8],
         "descente": [at("s4", "descente"), SCAN], "remontee": [at("s4", "remontee"), SCAN], "fin": round(fin - debut, 3)}
    sous_titres = "".join(
        cache(96, 1474, 900, f'<div class="etape"><span class="n num" style="font-size:88px;width:132px">{i + 1:02d}</span>'
              f'<p class="corps" style="font-size:50px;width:752px">{e}</p></div>', f"s4-e{i}", 24)
        for i, e in enumerate(ETAPES_SCAN))
    contenu = f"""
{cache(96, 236, 888, '<div class="kick" style="font-size:38px">Le principe</div>', "s4-kick")}
{cache(96, 236, 888, '<div class="kick" style="font-size:38px">Comment ça marche</div>', "s4-kick2")}
{cache(92, 296, 900, '<div class="t9" style="font-size:150px">Un scan</div>', "s4-l1")}
{cache(92, 430, 900, '<div class="t9 it or" style="font-size:150px">à 360°</div>', "s4-l2")}
<div id="s4-scan" class="a" style="left:0;top:0;width:1080px;height:1920px">
<canvas id="s4-avatar" class="a" width="{R['largeur']}" height="{R['hauteur']}" style="left:440px;top:330px;width:{R['largeur']}px;height:{R['hauteur']}px"></canvas>
{sous_titres}
</div>
<div id="s4-tag" class="a cadre" style="left:96px;top:600px;padding:14px 26px;font-size:40px">{plus(30)}1 analyse / semaine</div>
<div id="s4-machine" class="a" style="left:{X0}px;top:{Y0}px;width:{W}px;height:{round(M60[1] * W / M60[0])}px">
  <img id="s4-img" src="assets/img/m60.png" alt="" style="display:block;width:{W}px">
</div>
{legendes}
<p id="s4-mention" class="a mention" style="left:96px;top:1516px;width:888px;padding:14px 24px;font-size:30px;line-height:1.28">{MENTION_SANTE_SCAN}</p>
"""
    b, tm = at("s4", "bascule"), at("s4", "machine")
    e = [at("s4", f"e{i}") for i in range(3)]
    js = (f'''        const scan = {{ t: 0 }};
        let rendre = null;
        window.__hf = window.__hf || {{}};
        window.__hf.buildReady = window.__hf.buildReady || {{}};
        window.__hf.buildReady["s4-avatar"] = import("./assets/js/avatar.js").then((m) => {{
          rendre = m.creer(document.getElementById("s4-avatar"), {json.dumps(R)});
          rendre(scan.t);
        }});
        tl.to(scan, {{ t: {R["fin"]}, duration: {R["fin"]}, ease: "none", onUpdate: () => {{ if (rendre) rendre(scan.t); }} }}, 0);
'''
          + monte("s4-kick", at("s4", "kick"), 0.55) + monte("s4-l1", at("s4", "l1")) + monte("s4-l2", at("s4", "l2"))
          + monte("s4-e0", e[0], 0.65, 24) + sort("s4-e0", e[1] - 0.05, 0.4, 24) + monte("s4-e1", e[1] + 0.25, 0.65, 24)
          + sort("s4-e1", e[2] - 0.05, 0.4, 24) + monte("s4-e2", e[2] + 0.25, 0.65, 24)
          + f'        tl.set("#s4-kick2", {{ yPercent: 100, y: {2 * PAD} }}, 0);\n'
          + f'        tl.to("#s4-scan", {{ x: -1150, duration: 0.6, ease: "power2.in" }}, {b});\n'
          + sort("s4-kick", b) + monte("s4-kick2", b + 0.3, 0.55)
          + f'        tl.fromTo("#s4-tag", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.out" }}, {at("s4", "tag")});\n'
          + f'        tl.fromTo("#s4-machine", {{ clipPath: "inset(100% 0% 0% 0%)", y: 70 }}, {{ clipPath: "inset(0% 0% 0% 0%)", y: 0, duration: 0.8, ease: "power2.out" }}, {tm});\n'
          + f'        tl.fromTo("#s4-img", {{ scale: 1 }}, {{ scale: 1.04, duration: {fin - debut - tm:.3f}, ease: "none", transformOrigin: "50% 80%" }}, {tm});\n')
    for i in range(3):
        t = at("s4", "legendes", i, "pas_leg")
        js += (f'        tl.from("#s4-p{i}", {{ scale: 0, duration: 0.35, ease: "back.out(2)" }}, {t});\n'
               f'        tl.from("#s4-t{i}", {{ scaleX: 0, duration: 0.4, ease: "power2.inOut" }}, {t + 0.1:.3f});\n'
               + monte(f"s4-lt{i}", t + 0.25, 0.55) + monte(f"s4-lb{i}", t + 0.45, 0.65))
    js += f'        tl.from("#s4-mention", {{ clipPath: "inset(0% 0% 100% 0%)", duration: 0.5, ease: "power2.out" }}, {at("s4", "mention")});\n'
    return scene("s4", contenu, js)


def s5():
    debut, fin = bornes("s5")
    items = "".join(
        cache(92, 650 + 118 * i, 900, f'<div class="t9" style="font-size:104px;display:flex;align-items:center;gap:26px">{plus(58)}{r}</div>', f"s5-i{i}", 20)
        for i, r in enumerate(RESULTATS))
    contenu = f"""
<div id="s5-fantome" class="a t9 creux" aria-hidden="true" data-layout-allow-overflow style="left:520px;top:900px;font-size:900px">3D</div>
{cache(96, 236, 888, '<div class="kick" style="font-size:38px">Vos résultats</div>', "s5-kick")}
{cache(92, 296, 900, '<div class="t9" style="font-size:146px">Ce que vous</div>', "s5-l1")}
{cache(92, 430, 900, '<div class="t9" style="font-size:146px">découvrez</div>', "s5-l2")}
{items}
{cache(96, 1290, 888, '<p class="corps" style="font-size:50px">Un rapport complet à chaque analyse.</p>', "s5-corps")}
<p id="s5-mention" class="a mention" style="left:96px;top:1440px;width:888px;padding:14px 24px;font-size:30px;line-height:1.28">{MENTION_SANTE}</p>
"""
    js = (f'        tl.fromTo("#s5-fantome", {{ y: 140 }}, {{ y: 0, duration: {fin - debut:.3f}, ease: "none" }}, 0);\n'
          + monte("s5-kick", at("s5", "kick"), 0.55) + monte("s5-l1", at("s5", "l1")) + monte("s5-l2", at("s5", "l2"))
          + "".join(f'        tl.fromTo("#s5-i{i}", {{ xPercent: -105 }}, {{ xPercent: 0, duration: 0.6, ease: "power3.out" }}, {at("s5", "items", i)});\n'
                    for i in range(len(RESULTATS)))
          + monte("s5-corps", at("s5", "corps"), 0.7)
          + f'        tl.from("#s5-mention", {{ clipPath: "inset(0% 0% 100% 0%)", duration: 0.5, ease: "power2.out" }}, {at("s5", "mention")});\n')
    return scene("s5", contenu, js)


def s6():
    debut, fin = bornes("s6")
    contenu = f"""
<div id="s6-fantome" class="a t9 creux" aria-hidden="true" data-layout-allow-overflow style="left:480px;top:960px;font-size:860px">IA</div>
{cache(96, 236, 888, '<div class="kick" style="font-size:38px">L’intelligence artificielle</div>', "s6-kick")}
{cache(92, 296, 900, '<div class="t9" style="font-size:150px">Votre</div>', "s6-l1")}
{cache(92, 428, 900, '<div class="t9" style="font-size:150px">programme,</div>', "s6-l2")}
{cache(92, 560, 900, '<div class="t9 it or" style="font-size:150px">par l’IA.</div>', "s6-l3")}
{etapes("s6-e", ETAPES_IA, 790, [130, 200], 88, 52, 756)}
"""
    js = (f'        tl.fromTo("#s6-fantome", {{ y: 140 }}, {{ y: 0, duration: {fin - debut:.3f}, ease: "none" }}, 0);\n'
          + monte("s6-kick", at("s6", "kick"), 0.55) + monte("s6-l1", at("s6", "l1")) + monte("s6-l2", at("s6", "l2"))
          + monte("s6-l3", at("s6", "l3"))
          + "".join(monte(f"s6-e{i}", at("s6", "etapes", i), 0.65, 24) for i in range(3)))
    return scene("s6", contenu, js)


def s7():
    contenu = f"""
{cache(96, 236, 888, '<div class="kick" style="font-size:38px">Votre suivi</div>', "s7-kick")}
{cache(92, 296, 900, '<div class="t9" style="font-size:146px">Suivez votre</div>', "s7-l1")}
{cache(92, 430, 900, '<div class="t9" style="font-size:146px">évolution</div>', "s7-l2")}
{cache(90, 650, 960, '<div class="t9 num" style="font-size:182px">1 analyse</div>', "s7-l3")}
{cache(90, 810, 960, '<div class="t9" style="font-size:182px">3D par</div>', "s7-l4")}
<div id="s7-l5" class="a t9 or" style="left:88px;top:980px;font-size:252px;transform-origin:left center">semaine</div>
{cache(96, 1280, 888, '<p class="corps" style="font-size:50px">Incluse dans l’option Premium. Comparez vos résultats d’une analyse à l’autre.</p>', "s7-corps")}
"""
    js = (monte("s7-kick", at("s7", "kick"), 0.55) + monte("s7-l1", at("s7", "l1")) + monte("s7-l2", at("s7", "l2"))
          + monte("s7-l3", at("s7", "l3")) + monte("s7-l4", at("s7", "l4"))
          + f'        tl.fromTo("#s7-l5", {{ scale: 1.3, clipPath: "inset(0% 100% 0% 0%)" }}, {{ scale: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power4.out" }}, {at("s7", "l5")});\n'
          + monte("s7-corps", at("s7", "corps"), 0.7))
    return scene("s7", contenu, js)


def s8():
    bandes = ""
    for i, (n, nom, etat) in enumerate(AVANTAGES):
        fond_b, coul_n, coul_t, coul_e = (("#B8A07E", "#0D0D0D", "#0D0D0D", "#0D0D0D") if i == 1      # l'analyse 3D en or
                                          else ("#222222", "#B8A07E", "#F4F1EC", "#B8A07E"))
        bandes += (f'<div id="s8-b{i}" class="a" style="left:96px;top:{1110 + 140 * i}px;width:888px;height:124px;background:{fond_b};display:flex;align-items:center;'
                   f'clip-path:polygon(52px 0,100% 0,calc(100% - 52px) 100%,0 100%)">'
                   f'<span class="t8 it num" style="font-size:64px;color:{coul_n};margin-left:76px;width:100px">{n}</span>'
                   f'<span style="display:flex;flex-direction:column;gap:12px">'
                   f'<span class="t8" style="font-size:52px;color:{coul_t}">{nom}</span>'
                   f'<span class="kick" style="font-size:26px;color:{coul_e};letter-spacing:.16em">{etat}</span></span></div>')
    tp = at("s8", "prix")
    contenu = f"""
{cache(96, 236, 888, f'<div class="kick" style="font-size:38px">{plus(40)}L’option Premium</div>', "s8-kick")}
<div class="a" style="left:96px;top:300px;display:flex;align-items:center;gap:26px">
  <div id="s8-plus">{plus(200)}</div>
  <div id="s8-deux" class="t9 num" style="font-size:410px;line-height:.86">2 €</div>
</div>
<div id="s8-ttc" class="a t8 it" style="left:96px;top:690px;font-size:116px">TTC par semaine</div>
<p id="s8-soit" class="a corps" style="left:96px;top:836px;width:888px;font-size:50px">Soit 8&nbsp;€ toutes les 4 semaines,<br>en plus de votre abonnement.</p>
{cache(96, 1056, 888, '<div class="kick" style="font-size:34px">3 avantages inclus</div>', "s8-kick2")}
{bandes}
"""
    js = (monte("s8-kick", at("s8", "kick"), 0.55)
          + f'        tl.fromTo("#s8-plus", {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.6)" }}, {tp});\n'
          + f'        tl.fromTo("#s8-deux", {{ scale: 1.3, clipPath: "inset(0% 100% 0% 0%)" }}, {{ scale: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power4.out", transformOrigin: "left center" }}, {tp});\n'
          + f'        tl.fromTo(["#s8-ttc", "#s8-soit"], {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.out" }}, {tp});\n'
          + monte("s8-kick2", at("s8", "kick2"), 0.5)
          + "".join(f'        tl.from("#s8-b{i}", {{ x: -1100, duration: 0.65, ease: "power3.out" }}, {at("s8", "bandes", i)});\n'
                    for i in range(len(AVANTAGES))))
    return scene("s8", contenu, js)


def s9():
    contenu = f"""
<div id="s9-logo" class="a" style="left:330px;top:250px;width:420px"><img src="assets/img/logo-complet.png" alt="LA SALLE" style="display:block;width:420px"></div>
{cache(40, 620, 1000, '<div class="t9" style="font-size:180px;text-align:center">Activez-la</div>', "s9-l1")}
{cache(40, 785, 1000, '<div class="t9" style="font-size:180px;text-align:center">à l’accueil.</div>', "s9-l2")}
{cache(40, 1010, 1000, '<div class="t8 it or" style="font-size:88px;text-align:center">En quelques secondes.</div>', "s9-l3")}
{cache(40, 1172, 1000, '<div class="kick" style="justify-content:center;font-size:38px">Urban Valley · 7J/7 · 6H–23H</div>', "s9-l4")}
<p id="s9-mention" class="a mention" style="left:96px;top:1290px;width:888px;padding:20px 30px;font-size:36px;line-height:1.26;text-align:center">{MENTION_OPTION}</p>
"""
    js = (f'        tl.from("#s9-logo", {{ clipPath: "inset(0% 0% 100% 0%)", y: -30, duration: 0.6, ease: "power3.out" }}, {at("s9", "logo")});\n'
          + monte("s9-l1", at("s9", "l1")) + monte("s9-l2", at("s9", "l2")) + monte("s9-l3", at("s9", "l3"))
          + monte("s9-l4", at("s9", "l4"), 0.55)
          + f'        tl.from("#s9-mention", {{ clipPath: "inset(100% 0% 0% 0%)", duration: 0.6, ease: "power2.out" }}, {at("s9", "mention")});\n')
    return scene("s9", contenu, js)


def volets():
    """Filet or sur le bord du dévoilement : même durée, même courbe que le clip-path de la scène qui entre."""
    coupes = [t for c, t, _ in SCENES[1:] if c not in COUPES_SECHES]
    corps = "\n".join(f'<div id="filet{i}" class="a vf" data-layout-allow-overflow></div>' for i, _ in enumerate(coupes))
    js = "".join(
        f'        tl.fromTo("#filet{i}", {{ x: -812 }}, {{ x: 1074, duration: {VOLET}, ease: "sine.inOut" }}, {t - VOLET / 2:g});\n'
        for i, t in enumerate(coupes))
    return composition("volets", 1080, 1920, DUREE, corps, js)


def fond_story():
    return composition("fond", 1080, 1920, DUREE, fond(1920, "f"), "")


def index_story():
    hotes = []
    for z, (c, _, _) in enumerate(SCENES, start=1):
        debut, fin = bornes(c)
        hotes.append(f'      <div id="h-{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{debut:g}" '
                     f'data-duration="{fin - debut:g}" data-track-index="{1 + (z + 1) % 2}" data-width="1080" data-height="1920" style="z-index:{z}"></div>')
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
    </style>
  </head>
  <body>
    <!-- Story analyse 3D Visbody M60 : 9 scènes, {DUREE:g} s, {FPS} i/s, 120 BPM. Coupes à {coupes} s :
         la scène suivante se dévoile en biais en {VOLET} s, sauf « UNE BALANCE IA. » qui arrive en coupe sèche. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUREE:g}" data-width="1080" data-height="1920" data-fps="{FPS}">
      <div id="h-fond" data-composition-id="fond" data-composition-src="compositions/fond.html" data-start="0" data-duration="{DUREE:g}" data-track-index="0" data-width="1080" data-height="1920" style="z-index:0"></div>
{chr(10).join(hotes)}
      <div id="h-volets" data-composition-id="volets" data-composition-src="compositions/volets.html" data-start="0" data-duration="{DUREE:g}" data-track-index="3" data-width="1080" data-height="1920" style="z-index:20"></div>
      <audio id="musique" src="assets/audio/musique.wav" data-start="0" data-duration="{DUREE:g}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


# ---------------------------------------------------------------- affiche « programme IA » (4:5, format du carrousel)
def affiche():
    corps = f"""
{fond(1350)}
<div class="a t9 creux" aria-hidden="true" data-layout-allow-overflow style="left:520px;top:640px;font-size:760px">IA</div>
<div class="a kick" style="left:108px;top:150px">L’intelligence artificielle</div>
<div class="a t9" style="left:104px;top:206px;font-size:132px">Votre</div>
<div class="a t9" style="left:104px;top:322px;font-size:132px">programme,</div>
<div class="a t9 it or" style="left:104px;top:438px;font-size:132px">par l’IA.</div>
""" + "".join(
        f'<div class="a etape" style="left:108px;top:{t}px"><span class="n num" style="font-size:76px;width:118px">{i + 1:02d}</span>'
        f'<p class="corps" style="font-size:44px;width:700px">{e}</p></div>\n'
        for i, (t, e) in enumerate(zip((640, 750, 920), ETAPES_IA))) + """
<div class="a filet" style="left:0;top:1236px;width:1080px;height:6px"></div>
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
    <!-- Affiche « VOTRE PROGRAMME, PAR L'IA. » au format du carrousel Visbody : scène figée d'une seconde, snapshot à 0,5 s -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="1" data-width="1080" data-height="1350" data-fps="30">
      <div id="h-affiche" data-composition-id="affiche" data-composition-src="compositions/affiche.html" data-start="0" data-duration="1" data-track-index="1" data-width="1080" data-height="1350"></div>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
"""


# ---------------------------------------------------------------- assets et projet
def projet(nom):
    p = os.path.join(RACINE, nom)
    for d in ("assets/fonts", "assets/vendor", "assets/img", "assets/audio", "compositions"):
        os.makedirs(os.path.join(p, d), exist_ok=True)
    for f in os.listdir(os.path.join(MD, "_sources-premium", "fonts")):
        shutil.copy2(os.path.join(MD, "_sources-premium", "fonts", f), os.path.join(p, "assets", "fonts", f))
    shutil.copy2(os.path.join(MD, "_sources-premium", "js", "gsap.min.js"), os.path.join(p, "assets", "vendor", "gsap.min.js"))
    shutil.copy2(os.path.join(MD, "lasalle-fontaine", "_communs", "img", "logo-complet.png"), os.path.join(p, "assets", "img", "logo-complet.png"))
    m = os.path.join(SOURCES, "m60_detouree.png")
    if not os.path.exists(m):
        sys.exit(f"Absent : {m} (lancer tools/detourer.py)")
    shutil.copy2(m, os.path.join(p, "assets", "img", "m60.png"))
    if nom == "story-916":                                     # avatar 3D de la scène du scan (Three.js 0.185.1, MIT)
        os.makedirs(os.path.join(p, "assets", "js"), exist_ok=True)
        shutil.copy2(os.path.join(RACINE, "_communs", "js", "avatar.js"), os.path.join(p, "assets", "js", "avatar.js"))
        for f in ("three.module.min.js", "three.core.min.js", "MarchingCubes.js", "LICENSE-three.txt"):
            shutil.copy2(os.path.join(RACINE, "_communs", "vendor", f), os.path.join(p, "assets", "vendor", f))
    musique = os.path.join(RACINE, "_communs", "musique_visbody.wav")
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
  "name": "lasalle-visbody-{nom}",
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
    ecrire(os.path.join(p, "meta.json"), f'{{\n  "id": "lasalle-visbody-{nom}",\n  "name": "lasalle-visbody-{nom}",\n  "createdAt": "2026-10-22T09:30:00.000Z"\n}}\n')
    return p


def ecrire(chemin, texte):
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)


def main():
    a = projet("affiche-45")
    ecrire(os.path.join(a, "index.html"), index_affiche())
    ecrire(os.path.join(a, "compositions", "affiche.html"), affiche())
    s = projet("story-916")
    ecrire(os.path.join(s, "index.html"), index_story())
    ids = [c for c, _, _ in SCENES]
    for cid, f in zip(ids + ["fond", "volets"], (s1, s2, s3, s4, s5, s6, s7, s8, s9, fond_story, volets)):
        ecrire(os.path.join(s, "compositions", f"{cid}.html"), f())
    print("Écrit :", a, s)


if __name__ == "__main__":
    main()
