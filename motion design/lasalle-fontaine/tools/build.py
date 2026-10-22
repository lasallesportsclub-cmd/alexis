"""Fontaine à boisson sportive LA SALLE : affiche 02/03 retravaillée (4:5) et story animée (9:16, 34,5 s, 60 i/s).

Écrit :
  affiche-45/index.html                    affiche « COMMENT ÇA MARCHE » 1080×1350 (scène figée d'une seconde)
  story-916/index.html, compositions/*.html la story : les visuels du carrousel rejoués texte par texte, et (v3) le
                                           parcours sur l'écran réel de la fontaine, puis le versement de la boisson
Recopie dans <projet>/assets/ (ignorés par git) :
  polices et GSAP (_sources-premium/), logo (_communs/img/), fontaine détourée et écrans réels (~/fontaine-sources,
  hors dépôt, préparés par tools/detourer.py et tools/ecrans.py), musique (story-916, produite par tools/musique.py).

Les textes sont ceux des visuels fournis le 22/10/2026, mot pour mot ; seuls la mise en page et le mouvement changent.
Version 3 (demande du 22/10) : « scannez votre QR code ou votre carte », goût, intensité, eau, « Début », sur les
photos de l'écran ; puis la caméra descend sous l'écran et la gourde se remplit (0,7 L, contenance affichée à l'écran).
Repères (secondes) : SCENES et T ci-dessous ; reperes() les donne en absolu à tools/musique.py et tools/livrer.py.

Usage : python3 tools/build.py   (puis tools/musique.py, rendu, tools/livrer.py)
"""
import json
import os
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
MD = os.path.normpath(os.path.join(RACINE, ".."))
SOURCES = os.path.expanduser(os.environ.get("FONTAINE_SOURCES", "~/fontaine-sources"))

# Story : (id, coupe, temps jusqu'à la coupe suivante) ; coupes sur la grille de 120 BPM (un temps = 0,5 s)
SCENES = [("s1", 0.0, 2.5), ("s2", 2.5, 5.0), ("s3", 7.5, 12.0), ("s4", 19.5, 4.5), ("s5", 24.0, 3.0),
          ("s6", 27.0, 4.0), ("s7", 31.0, 3.5)]
DUREE = 34.5
FPS = 60                   # mouvements et volets fluides (retour du 22/10 : transitions saccadées en 30 i/s)
VOLET = 0.9                # dévoilement en biais, centré sur chaque coupe
BASCULE = {"s4"}           # entrée en mouvement de caméra vertical (de l'écran à la buse) au lieu du volet en biais
CASSURE = (27.0, 27.5)     # musique coupée, « + 2 € » frappe à la reprise
# Entrées de chaque scène, en secondes après sa coupe ; « pas » = écart entre deux éléments d'une liste
T = {
    "s1": {"filet": 0.15, "sous": 0.5},
    "s2": {"kick": 0.05, "l1": 0.15, "l2": 0.35, "machine": 0.45, "point": 1.2, "trait": 1.3, "ct": 1.55, "cb": 1.85,
           "kick2": 2.35, "puces": 2.5, "pas": 0.15, "mention": 2.75},
    # Parcours : 5 étapes (débuts dans « etapes ») ; l'étape 1 (scan) se joue sur des pictogrammes, l'appareil monte
    # ensuite ; un « tap » or sur l'écran à chaque choix, l'écran suivant apparaît 0,25 s après
    "s3": {"kick": 0.05, "l1": 0.15, "l2": 0.35, "icones": 0.6, "ou": 0.8, "noms": 0.95, "balayage": 1.15,
           "valide": 1.85, "sortie": 2.05, "appareil": 2.2, "etapes": [0.0, 2.5, 5.0, 7.5, 9.5],
           "taps": [4.3, 6.8, 8.8, 10.7], "ecran": 0.25},
    # Versement : ouverture et fermeture de la buse, gouttes finales, « SERVEZ-VOUS. »
    "s4": {"ouvre": 0.5, "ferme": 2.8, "titre": 3.05, "gouttes": [3.25, 3.75]},
    "s5": {"kick": 0.05, "l2": 0.2, "l3": 0.45, "l4": 0.8, "corps": 1.35},
    "s6": {"kick": 0.05, "prix": 0.5, "kick2": 1.2, "bandes": 1.35, "pas": 0.22},
    "s7": {"logo": 0.0, "l1": 0.15, "l2": 0.35, "l3": 0.65, "l4": 0.85, "mention": 0.6},
}

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
.fr .tap { position: absolute; width: 96px; height: 96px; }
.fr .tap .anneau { position: absolute; inset: 0; border: 7px solid #B8A07E; border-radius: 50%; outline: 3px solid #0D0D0D; }
.fr .tap .pt { position: absolute; left: 33px; top: 33px; width: 30px; height: 30px; border-radius: 50%; background: #B8A07E; outline: 3px solid #0D0D0D; }
.fr .vf { left: 0; top: 0; width: 818px; height: 1920px; background: #B8A07E; clip-path: polygon(806px 0, 818px 0, 12px 100%, 0 100%); }
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
# Parcours sur l'écran (demande du 22/10, dans l'ordre de l'interface réelle) : (étiquette, ligne 1, ligne 2, corps)
ETAPES = [("01", "Scannez votre", "QR code ou carte.", None),
          ("02", "Choisissez", "votre saveur.", "Cinq saveurs, au choix sur l’écran tactile."),
          ("03", "Choisissez", "l’intensité.", "Léger, moyen ou fort."),
          ("04", "Choisissez", "votre eau.", "Fraîche ou normale."),
          ("05", "Appuyez sur", "«&nbsp;Début&nbsp;».", "Vous composez votre boisson.")]
# Contenance servie : celle qu'affiche l'écran de la fontaine (« 0,7 l ») ; ⚠ 750 ml dans la demande, voir A_valider.md
VOLUME_L, DECIMALES = 0.7, 1
VOLUME = f"{VOLUME_L:.{DECIMALES}f}".replace(".", ",") + " L"

# Appareil : cadre inox réel (photo 1 redressée, tools/ecrans.py) et dalle 1280×1024 affichée sur 936 px de large
ECRANS = ["gouts", "intensite", "eau", "debut"]
K = 936 / 1280
CADRE_PX, DALLE_PX = (1680, 1290), (200, 130)
APP_X = 72 - DALLE_PX[0] * K
Y_APP = 600                                   # haut du cadre pendant le parcours
Y_APP_BUSE = 380 - CADRE_PX[1] * K            # pendant le versement : seul le bas du cadre reste à l'image, en haut
BASCULE_DY = Y_APP - Y_APP_BUSE               # course de la « caméra » qui descend de l'écran à la buse
TAPS = [(762, 510), (726, 511), (466, 512), (640, 780)]   # Multifruits, « moyen », « EAU FRAICHE », « Début » (px de dalle)

# Versement (coordonnées de la scène) : buse sous le cadre, gourde à large goulot, jet en chute libre
VERSEMENT = {"cx": 540, "buse": 448, "jet": 26, "v0": 900, "g": 23500, "plein": 800,
             "gourde": {"col": 640, "epaule": 690, "corps": 770, "bas": 1236, "rayon": 36, "demiCol": 80, "demi": 150},
             "ox": 300, "oy": 440, "l": 480, "h": 830}


def chute(y0, y1):
    """Temps de chute du liquide de y0 à y1 (vitesse de sortie v0, gravité g), comme dans versement.js."""
    v0, g = VERSEMENT["v0"], VERSEMENT["g"]
    return (-v0 + (v0 * v0 + 2 * g * (y1 - y0)) ** 0.5) / g


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
# Plein cadre (retour du 22/10 : « tout est compact ») : texte entre x 96–984 et y 210–1660, corps plus grands.
# Transitions : la scène suivante se dévoile en biais (pente 0,42) sous un filet or, en VOLET s centrées sur la coupe ;
# la scène qui sort glisse de 60 px. Les caches (.m) prennent la hauteur réelle de leur texte, plus PAD en haut et
# en bas : un texte reste invisible tant qu'il n'est pas entré (correctif du « Saveur, intensité » apparu trop tôt).
PAD = 30
DEVOILE_DEBUT = "polygon(0px 0px, 0px 0px, -806px 1920px, 0px 1920px)"
DEVOILE_FIN = "polygon(0px 0px, 1886px 0px, 1080px 1920px, 0px 1920px)"


def bornes(cid):
    """Début et fin de la scène dans la story : elle chevauche ses voisines de VOLET/2 de chaque côté."""
    i = [c for c, _, _ in SCENES].index(cid)
    coupe = SCENES[i][1]
    debut = 0.0 if i == 0 else coupe - VOLET / 2
    fin = DUREE if i == len(SCENES) - 1 else SCENES[i + 1][1] + VOLET / 2
    return debut, fin


def at(cid, cle, k=0):
    """Instant local (dans la scène) d'une entrée de T, décalée de k pas."""
    debut, _ = bornes(cid)
    coupe = dict((c, t) for c, t, _ in SCENES)[cid]
    return round(coupe - debut + T[cid][cle] + k * T[cid].get("pas", 0), 3)


def reperes():
    """Instants absolus des entrées, pour tools/musique.py."""
    c = dict((cid, t) for cid, t, _ in SCENES)
    p, v = T["s3"], T["s4"]
    return {
        "puces": [c["s2"] + T["s2"]["puces"] + i * T["s2"]["pas"] for i in range(len(BOISSONS))],
        "etapes": [c["s3"] + e for e in p["etapes"]],
        "balayage": c["s3"] + p["balayage"] + 0.15,
        "valide": c["s3"] + p["valide"],
        "appareil": c["s3"] + p["appareil"],
        "taps": [c["s3"] + t for t in p["taps"]],
        "bascule": c["s4"] - VOLET / 2,
        "ouvre": c["s4"] + v["ouvre"],
        "ferme": c["s4"] + v["ferme"],
        "plein": c["s4"] + v["ferme"] + chute(VERSEMENT["buse"], VERSEMENT["plein"]),
        "gouttes": [c["s4"] + t for t in v["gouttes"]],
        "servez": c["s4"] + v["titre"],
        "trente": c["s5"] + T["s5"]["l4"],
        "prix": c["s6"] + T["s6"]["prix"],
        "bandes": [c["s6"] + T["s6"]["bandes"] + i * T["s6"]["pas"] for i in range(len(AVANTAGES))],
        "accueil": c["s7"] + T["s7"]["l2"],
    }


def cache(left, top, w, inner, mid, pad=PAD):
    """Glissement masqué : top est le haut du texte ; le cache déborde de pad au-dessus et au-dessous."""
    return (f'<div class="m" style="left:{left}px;top:{top - pad}px;width:{w}px;padding:{pad}px 0" '
            f'data-layout-allow-overflow><div id="{mid}">{inner}</div></div>')


def monte(mid, t, d=0.65, pad=PAD, ease="power3.out"):
    """Le texte part de sous le cache : sa hauteur + 2 × pad, pour que les accents (À, É) restent cachés aussi."""
    return (f'        tl.fromTo("#{mid}", {{ yPercent: 100, y: {2 * pad} }}, '
            f'{{ yPercent: 0, y: 0, duration: {d}, ease: "{ease}" }}, {t:.3f});\n')


def sort(mid, t, d=0.45, pad=PAD, ease="power2.in"):
    """Le texte quitte son cache par le haut."""
    return (f'        tl.to("#{mid}", {{ yPercent: -100, y: {-2 * pad}, duration: {d}, ease: "{ease}" }}, {t:.3f});\n')


def scene(cid, contenu, js):
    """Fond opaque identique à celui de la story (le volet ne révèle que le texte), contenu dans #<cid>-c,
    dévoilement en biais à l'entrée (sauf s1), glissement de 60 px à la sortie (sauf la dernière).
    Scène de BASCULE : elle monte du bas avec son fond, pendant que la précédente monte d'autant (même courbe) ;
    l'appareil, posé dans les deux scènes, reste continu : la caméra descend de l'écran à la buse."""
    debut, fin = bornes(cid)
    ids = [c for c, _, _ in SCENES]
    suivante = ids[ids.index(cid) + 1] if cid != ids[-1] else None
    corps = f'{fond(1920, cid + "-")}\n<div id="{cid}-c" class="a" style="inset:0">\n{contenu}\n</div>'
    if cid in BASCULE:
        js = (f'        tl.fromTo("#{cid}-scene", {{ y: {BASCULE_DY:g} }}, {{ y: 0, duration: {VOLET}, ease: "sine.inOut" }}, 0);\n') + js
    elif cid != ids[0]:
        js = (f'        tl.fromTo("#{cid}-scene", {{ clipPath: "{DEVOILE_DEBUT}" }}, {{ clipPath: "{DEVOILE_FIN}", '
              f'duration: {VOLET}, ease: "sine.inOut" }}, 0);\n') + js
    if suivante in BASCULE:
        js += (f'        tl.to("#{cid}-c", {{ y: {-BASCULE_DY:g}, duration: {VOLET}, ease: "sine.inOut" }}, '
               f'{fin - debut - VOLET:.3f});\n')
    elif suivante:
        js += (f'        tl.to("#{cid}-c", {{ x: -60, duration: {VOLET}, ease: "sine.in" }}, '
               f'{fin - debut - VOLET:.3f});\n')
    return composition(cid, 1080, 1920, round(fin - debut, 3), corps, js)


def appareil(prefixe, top, ecrans):
    """La fontaine vue de face : écrans réels (empilés, le dernier au-dessus) sous le cadre inox évidé."""
    w, h = CADRE_PX[0] * K, CADRE_PX[1] * K
    imgs = "".join(f'<img id="{prefixe}-e{i}" class="a" src="assets/img/ecran-{e}.jpg" alt="" '
                   f'style="left:{DALLE_PX[0] * K:g}px;top:{DALLE_PX[1] * K:g}px;width:936px;height:{1024 * K:g}px">'
                   for i, e in enumerate(ecrans))
    return (f'<div id="{prefixe}-app" class="a" style="left:{APP_X:g}px;top:{top:g}px;width:{w:g}px;height:{h:g}px">{imgs}'
            f'<img class="a" src="assets/img/cadre.png" alt="" style="left:0;top:0;width:{w:g}px;height:{h:g}px"></div>')


def qr(taille=300, n=25, pad=30):
    """Pictogramme de QR code : trois repères et des modules tirés au hasard (graine fixe). Ce n'est pas un code
    lisible (aucune donnée, aucun format) : personne ne peut le scanner depuis la vidéo."""
    import random
    r = random.Random(22)
    m = [[r.random() < 0.48 for _ in range(n)] for _ in range(n)]
    for x0, y0 in ((0, 0), (n - 7, 0), (0, n - 7)):
        for y in range(-1, 8):
            for x in range(-1, 8):
                if 0 <= x0 + x < n and 0 <= y0 + y < n:
                    bord = x in (0, 6) or y in (0, 6)
                    m[y0 + y][x0 + x] = 0 <= x <= 6 and 0 <= y <= 6 and (bord or (2 <= x <= 4 and 2 <= y <= 4))
    u = (taille - 2 * pad) / n
    rects = []
    for y in range(n):
        x = 0
        while x < n:
            if m[y][x]:
                x1 = x
                while x1 < n and m[y][x1]:
                    x1 += 1
                rects.append(f'<rect x="{pad + x * u:.1f}" y="{pad + y * u:.1f}" width="{(x1 - x) * u + 0.4:.1f}" height="{u + 0.4:.1f}"/>')
                x = x1
            else:
                x += 1
    return (f'<svg viewBox="0 0 {taille} {taille}" style="display:block;width:{taille}px;height:{taille}px">'
            f'<rect width="{taille}" height="{taille}" rx="24" fill="#222222"/><g fill="#F4F1EC">{"".join(rects)}</g></svg>')


def carte(w=380, h=240):
    """Pictogramme de carte du club : aplat anthracite, trait oblique or (pente 0,42), monogramme en négatif."""
    d = 0.42 * h
    return (f'<div style="position:relative;width:{w}px;height:{h}px">'
            f'<svg viewBox="0 0 {w} {h}" style="display:block;width:{w}px;height:{h}px"><rect width="{w}" height="{h}" rx="22" fill="#222222"/>'
            f'<polygon points="{w - 120:g},0 {w - 76:g},0 {w - 76 - d:g},{h} {w - 120 - d:g},{h}" fill="#B8A07E"/></svg>'
            f'<img src="assets/img/logo-mono.png" alt="" style="position:absolute;left:34px;top:34px;height:64px"></div>')


def puces_masquees(ids, taille, h, pad, prefixe):
    c = round(0.42 * h)
    return "".join(
        f'<div class="m" style="position:relative;height:{h}px" data-layout-allow-overflow><div id="{prefixe}{k}" class="puce" '
        f'style="--c:{c}px;height:{h}px;padding:0 {pad}px;font-size:{taille}px">{b}</div></div>'
        for k, b in enumerate(ids))


def s1():
    _, fin = bornes("s1")
    contenu = f"""
<div class="a kick" style="left:96px;top:236px;font-size:38px">{plus(40)}Option Premium</div>
<img class="a" src="assets/img/logo-complet.png" alt="LA SALLE" style="left:774px;top:212px;width:210px">
<div id="s1-titre" class="a" style="left:92px;top:560px">
  <div class="t9 or" style="font-size:168px;line-height:.92">Bien plus</div>
  <div class="t9" style="font-size:168px;line-height:.92">que de</div>
  <div class="t9" style="font-size:168px;line-height:.92">l’eau.</div>
</div>
{cache(96, 1120, 888, '<p class="corps" style="font-size:54px">La fontaine à boissons sportives<br>de l’option Premium.</p>', "s1-sous")}
<div class="a" style="left:96px;top:1560px">{plus(60)}</div>
<div id="s1-filet" class="a filet" style="left:178px;top:1586px;width:902px;height:6px;transform-origin:left center"></div>
"""
    js = (f'        tl.fromTo("#s1-titre", {{ scale: 1 }}, {{ scale: 1.03, duration: {fin:g}, ease: "none", transformOrigin: "left center" }}, 0);\n'
          f'        tl.from("#s1-filet", {{ scaleX: 0, duration: 1.0, ease: "power2.out" }}, {at("s1", "filet")});\n'
          + monte("s1-sous", at("s1", "sous")))
    return scene("s1", contenu, js)


def s2():
    # Fontaine 1158×849 affichée sur 620 px : 1 px de la capture = 1,606 px
    W, X0, Y0 = 620, 40, 616
    k = 3 * W / 1158
    ex, ey = round(X0 + (292 - 36) * k), 758
    debut, fin = bornes("s2")
    contenu = f"""
{cache(96, 236, 888, '<div class="kick" style="font-size:38px">Comment ça marche</div>', "s2-kick")}
{cache(92, 296, 900, '<div class="t9" style="font-size:140px">Votre boisson,</div>', "s2-l1")}
{cache(92, 424, 900, '<div class="t9 it or" style="font-size:140px">À la carte.</div>', "s2-l2")}
<div id="s2-machine" class="a" style="left:{X0}px;top:{Y0}px;width:{W}px;height:{round(849 * W / 1158)}px">
  <img id="s2-img" src="assets/img/fontaine.png" alt="" style="display:block;width:{W}px">
</div>
<div id="s2-trait" class="a filet" style="left:{ex}px;top:{ey - 1}px;width:{586 - ex}px;height:3px;transform-origin:left center"></div>
<div id="s2-point" class="a point" style="left:{ex - 11}px;top:{ey - 11}px"></div>
{cache(600, 734, 400, '<div class="t8" style="font-size:48px">Écran tactile 17″</div>', "s2-ct")}
{cache(600, 798, 384, '<p class="corps" style="font-size:38px">Saveur, intensité, température&nbsp;: vous composez votre boisson.</p>', "s2-cb")}
{cache(96, 1150, 888, '<div class="kick" style="font-size:34px">Au choix</div>', "s2-kick2")}
<div class="a" style="left:92px;top:1196px;width:900px;display:flex;flex-wrap:wrap;gap:14px 12px">{puces_masquees(BOISSONS, 44, 74, 32, "s2-p")}</div>
<p id="s2-mention" class="a mention" style="left:96px;top:1420px;width:888px;padding:16px 26px;font-size:32px;line-height:1.28">{MENTION_CAFEINE}</p>
"""
    js = (monte("s2-kick", at("s2", "kick"), 0.55) + monte("s2-l1", at("s2", "l1")) + monte("s2-l2", at("s2", "l2"))
          + f'        tl.fromTo("#s2-machine", {{ clipPath: "inset(100% 0% 0% 0%)", y: 70 }}, {{ clipPath: "inset(0% 0% 0% 0%)", y: 0, duration: 0.8, ease: "power2.out" }}, {at("s2", "machine")});\n'
          + f'        tl.fromTo("#s2-img", {{ scale: 1 }}, {{ scale: 1.04, duration: {fin - debut - at("s2", "machine"):.3f}, ease: "none", transformOrigin: "50% 60%" }}, {at("s2", "machine")});\n'
          + f'        tl.from("#s2-point", {{ scale: 0, duration: 0.35, ease: "back.out(2)" }}, {at("s2", "point")});\n'
          + f'        tl.from("#s2-trait", {{ scaleX: 0, duration: 0.4, ease: "power2.inOut" }}, {at("s2", "trait")});\n'
          + monte("s2-ct", at("s2", "ct"), 0.55) + monte("s2-cb", at("s2", "cb"), 0.7)
          + monte("s2-kick2", at("s2", "kick2"), 0.5)
          + "".join(monte(f"s2-p{i}", at("s2", "puces", i), 0.5, 0) for i in range(len(BOISSONS)))
          + f'        tl.from("#s2-mention", {{ clipPath: "inset(0% 0% 100% 0%)", duration: 0.5, ease: "power2.out" }}, {at("s2", "mention")});\n')
    return scene("s2", contenu, js)


def s3():
    """Parcours sur l'écran réel : 01 scan (pictogrammes), puis l'appareil monte ; 02 à 05 sur les photos de l'écran,
    un tap or à chaque choix, l'écran suivant apparaît. La ligne 1 ne change que si son texte change."""
    p = T["s3"]
    t0 = at("s3", "kick") - p["kick"]                     # instant local de la coupe
    e = [t0 + x for x in p["etapes"]]
    taps = [t0 + x for x in p["taps"]]
    ty = Y_APP + DALLE_PX[1] * K
    kicks = "".join(cache(96, 236, 600, f'<div class="kick" style="font-size:38px">Étape <span class="num">{n}</span></div>', f"s3-k{i}")
                    for i, (n, _, _, _) in enumerate(ETAPES))
    l1 = []                                               # (texte, étape d'entrée)
    for i, (_, a, _, _) in enumerate(ETAPES):
        if not l1 or l1[-1][0] != a:
            l1.append((a, i))
    lignes1 = "".join(cache(92, 296, 900, f'<div class="t9" style="font-size:126px">{a}</div>', f"s3-a{j}") for j, (a, _) in enumerate(l1))
    lignes2 = "".join(cache(92, 410, 900, f'<div class="t9 it or" style="font-size:126px">{b}</div>', f"s3-b{i}")
                      for i, (_, _, b, _) in enumerate(ETAPES))
    corps = "".join(cache(96, 1590, 888, f'<p class="corps" style="font-size:46px">{c}</p>', f"s3-c{i}")
                    for i, (_, _, _, c) in enumerate(ETAPES) if c)
    segs = "".join(f'<div class="a" style="left:{764 + 46 * i}px;top:246px;width:36px;height:22px;background:#222222;'
                   f'clip-path:polygon(9px 0,100% 0,calc(100% - 9px) 100%,0 100%)"><div id="s3-g{i}" '
                   f'style="width:100%;height:100%;background:#B8A07E;transform-origin:left center"></div></div>' for i in range(len(ETAPES)))
    pts = [(72 + x * K, ty + y * K) for x, y in TAPS]
    touches = "".join(f'<div id="s3-t{i}" class="tap" style="left:{x - 48:.1f}px;top:{y - 48:.1f}px"><div id="s3-ta{i}" class="anneau"></div>'
                      f'<div id="s3-tp{i}" class="pt"></div></div>' for i, (x, y) in enumerate(pts))
    contenu = f"""
{kicks}
{segs}
{lignes1}
{lignes2}
<div id="s3-scan" class="a" style="left:0;top:0;width:1080px;height:1920px">
  <div id="s3-qr" class="a" style="left:116px;top:850px">{qr()}</div>
  <div id="s3-carte" class="a" style="left:604px;top:880px">{carte()}</div>
  {cache(416, 962, 188, '<div class="t8" style="font-size:64px;text-align:center">ou</div>', "s3-ou")}
  {cache(116, 1186, 300, '<div class="kick" style="font-size:30px;justify-content:center">QR code</div>', "s3-n0")}
  {cache(604, 1186, 380, '<div class="kick" style="font-size:30px;justify-content:center">Carte</div>', "s3-n1")}
  <div id="s3-trait" class="a filet" style="left:72px;top:826px;width:936px;height:6px;transform-origin:left center"></div>
  <svg id="s3-ok" class="a" viewBox="0 0 120 120" style="left:450px;top:940px;width:120px;height:120px;overflow:visible">
    <circle cx="60" cy="60" r="60" fill="#B8A07E"/><path d="M 33 62 L 52 80 L 88 42" fill="none" stroke="#0D0D0D" stroke-width="12" stroke-linecap="square"/>
  </svg>
</div>
{appareil("s3", Y_APP, ECRANS)}
{touches}
{corps}
"""
    js = monte("s3-k0", e[0] + p["kick"], 0.55) + monte("s3-a0", e[0] + p["l1"]) + monte("s3-b0", e[0] + p["l2"])
    js += f'        tl.fromTo("#s3-g0", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "power2.out" }}, {e[0] + p["l1"]:.3f});\n'
    # 01 : QR code et carte entrent, le trait de lecture passe, coche de validation, puis l'appareil monte
    js += (f'        tl.fromTo("#s3-qr", {{ x: -90, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.55, ease: "power3.out" }}, {t0 + p["icones"]:.3f});\n'
           f'        tl.fromTo("#s3-carte", {{ x: 90, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.55, ease: "power3.out" }}, {t0 + p["icones"]:.3f});\n'
           + monte("s3-ou", t0 + p["ou"], 0.45) + monte("s3-n0", t0 + p["noms"], 0.45) + monte("s3-n1", t0 + p["noms"] + 0.08, 0.45)
           + f'        tl.fromTo("#s3-trait", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.15, ease: "power2.out" }}, {t0 + p["balayage"]:.3f});\n'
           f'        tl.to("#s3-trait", {{ y: 352, duration: 0.5, ease: "sine.inOut" }}, {t0 + p["balayage"] + 0.15:.3f});\n'
           f'        tl.to("#s3-trait", {{ opacity: 0, duration: 0.12 }}, {t0 + p["balayage"] + 0.65:.3f});\n'
           + sort("s3-ou", t0 + p["valide"] - 0.12, 0.3)
           + f'        tl.fromTo("#s3-ok", {{ scale: 0, rotation: -40 }}, {{ scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2.2)", svgOrigin: "60 60" }}, {t0 + p["valide"]:.3f});\n'
           f'        tl.to("#s3-scan", {{ y: -60, opacity: 0, duration: 0.35, ease: "power2.in" }}, {t0 + p["sortie"]:.3f});\n'
           f'        tl.fromTo("#s3-app", {{ clipPath: "inset(100% 0% 0% 0%)", y: 70 }}, {{ clipPath: "inset(0% 0% 0% 0%)", y: 0, duration: 0.8, ease: "power2.out" }}, {t0 + p["appareil"]:.3f});\n'
           f'        tl.set("#s3-app", {{ clipPath: "none" }}, {t0 + p["appareil"] + 0.81:.3f});\n')
    # 02 à 05 : changement d'étiquette, de lignes et de corps ; un tap par choix, l'écran suivant apparaît
    j1 = 0
    for i in range(1, len(ETAPES)):
        js += sort(f"s3-k{i - 1}", e[i] - 0.1, 0.35) + monte(f"s3-k{i}", e[i] + p["kick"] - 0.05, 0.55)
        js += f'        tl.fromTo("#s3-g{i}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "power2.out" }}, {e[i] + 0.05:.3f});\n'
        decal = 0.0
        if j1 + 1 < len(l1) and l1[j1 + 1][1] == i:
            js += sort(f"s3-a{j1}", e[i] - 0.1) + monte(f"s3-a{j1 + 1}", e[i] + 0.05)
            j1 += 1
            decal = 0.15
        js += sort(f"s3-b{i - 1}", e[i] - 0.05) + monte(f"s3-b{i}", e[i] + 0.2 + decal)
        if ETAPES[i - 1][3]:
            js += sort(f"s3-c{i - 1}", e[i] - 0.05, 0.4)
        js += monte(f"s3-c{i}", e[i] + 0.45 + decal, 0.6)
    for i, tt in enumerate(taps):
        js += (f'        tl.fromTo("#s3-t{i}", {{ scale: 1.7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.2, ease: "power2.out" }}, {tt:.3f});\n'
               f'        tl.fromTo("#s3-ta{i}", {{ scale: 1, opacity: 1 }}, {{ scale: 1.8, opacity: 0, duration: 0.42, ease: "power1.out" }}, {tt + 0.22:.3f});\n'
               f'        tl.fromTo("#s3-tp{i}", {{ scale: 1, opacity: 1 }}, {{ scale: 0.5, opacity: 0, duration: 0.3, ease: "power1.in" }}, {tt + 0.34:.3f});\n')
        if i + 1 < len(ECRANS):
            js += f'        tl.fromTo("#s3-e{i + 1}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power1.inOut" }}, {tt + p["ecran"]:.3f});\n'
    return scene("s3", contenu, js)


def s4():
    """Versement : la caméra est descendue sous l'écran (bas du cadre, buse) ; le jet remplit la gourde jusqu'à la
    contenance affichée à l'écran, le compteur suit le niveau, puis « SERVEZ-VOUS. »."""
    v, g = VERSEMENT, VERSEMENT["gourde"]
    debut, fin = bornes("s4")
    t0 = at("s4", "ouvre") - T["s4"]["ouvre"]             # instant local de la coupe
    R = dict(v, ouvre=at("s4", "ouvre"), ferme=at("s4", "ferme"), gouttes=[round(t0 + x, 3) for x in T["s4"]["gouttes"]])
    t_plein = R["ferme"] + chute(v["buse"], v["plein"])
    moteur = open(os.path.join(RACINE, "_communs", "js", "versement.js"), encoding="utf-8").read()
    moteur = "\n".join("        " + l if l else "" for l in moteur.splitlines())
    contenu = f"""
{appareil("s4", Y_APP_BUSE, ["debut"])}
<svg id="s4-buse" class="a" aria-hidden="true" viewBox="0 0 100 70" style="left:490px;top:378px;width:100px;height:70px">
  <rect x="8" y="0" width="84" height="14" fill="#3A3A3A"/><rect x="28" y="14" width="44" height="40" fill="#8E8E8E"/>
  <rect x="28" y="30" width="44" height="6" fill="#6B6B6B"/><rect x="38" y="54" width="24" height="16" fill="#5A5A5A"/>
  <rect x="34" y="14" width="7" height="40" fill="#B5B5B5"/>
</svg>
<div class="a" style="left:330px;top:1239px;width:420px;height:22px;background:#222222"></div>
<div class="a filet" style="left:330px;top:1239px;width:420px;height:4px"></div>
<canvas id="s4-verse" class="a" width="{v['l']}" height="{v['h']}" style="left:{v['ox']}px;top:{v['oy']}px;width:{v['l']}px;height:{v['h']}px"></canvas>
<div id="s4-compteur" class="a t9 num" style="left:40px;top:1300px;width:1000px;text-align:center;font-size:170px;transform-origin:50% 50%">{VOLUME}</div>
{cache(40, 1500, 1000, '<div class="t9" style="font-size:140px;text-align:center">Servez-vous.</div>', "s4-titre")}
"""
    js = (f"""        const R = {json.dumps(R)};
{moteur}
        const rendre = versement(document.getElementById("s4-verse"), R);
        const compteur = document.getElementById("s4-compteur");
        const etat = {{ t: 0 }};
        const dessiner = () => {{
          rendre(etat.t);
          const v = Math.floor(rendre.niveau(etat.t) * {VOLUME_L} * {10 ** DECIMALES} + 1e-6) / {10 ** DECIMALES};
          compteur.textContent = v.toFixed({DECIMALES}).replace(".", ",") + " L";
        }};
        tl.to(etat, {{ t: {fin - debut:.3f}, duration: {fin - debut:.3f}, ease: "none", onUpdate: dessiner }}, 0);
        dessiner();
"""
          + f'        tl.to("#s4-compteur", {{ color: "#B8A07E", duration: 0.25, ease: "power1.out" }}, {t_plein:.3f});\n'
          + f'        tl.fromTo("#s4-compteur", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }}, {t_plein:.3f});\n'
          + monte("s4-titre", at("s4", "titre")))
    return scene("s4", contenu, js)


def s5():
    contenu = f"""
{cache(96, 236, 888, '<div class="kick" style="font-size:38px">À chaque séance</div>', "s5-kick")}
{cache(90, 300, 960, '<div class="t9 num" style="font-size:200px">1 boisson</div>', "s5-l2")}
{cache(90, 476, 960, '<div class="t9" style="font-size:200px">toutes les</div>', "s5-l3")}
<div id="s5-l4" class="a t9 or num" style="left:90px;top:660px;font-size:340px;transform-origin:left center">30 min</div>
{cache(96, 1060, 640, '<p class="corps" style="font-size:50px">Aussi souvent<br>que vous venez.</p>', "s5-corps")}
<svg id="s5-horloge" class="a" aria-hidden="true" viewBox="0 0 220 220" style="left:764px;top:1050px;width:220px;height:220px;overflow:visible">
  <circle cx="110" cy="110" r="100" fill="none" stroke="rgba(244,241,236,.18)" stroke-width="4"/>
  <path id="s5-arc" d="M 110 10 A 100 100 0 0 1 110 210" fill="none" stroke="#B8A07E" stroke-width="10" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0"/>
  <line id="s5-aiguille" x1="110" y1="110" x2="110" y2="178" stroke="#B8A07E" stroke-width="6"/><circle cx="110" cy="110" r="9" fill="#B8A07E"/>
</svg>
"""
    t4 = at("s5", "l4")
    js = (monte("s5-kick", at("s5", "kick"), 0.55)
          + monte("s5-l2", at("s5", "l2")) + monte("s5-l3", at("s5", "l3"))
          + f'        tl.fromTo("#s5-l4", {{ scale: 1.3, clipPath: "inset(0% 100% 0% 0%)" }}, {{ scale: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power4.out" }}, {t4});\n'
          + f'        tl.from("#s5-arc", {{ attr: {{ "stroke-dashoffset": 1 }}, duration: 0.9, ease: "power2.inOut" }}, {t4});\n'
          + f'        tl.from("#s5-aiguille", {{ rotation: -180, svgOrigin: "110 110", duration: 0.9, ease: "power2.inOut" }}, {t4});\n'
          + monte("s5-corps", at("s5", "corps"), 0.7))
    return scene("s5", contenu, js)


def s6():
    bandes = ""
    for i, (n, nom, etat) in enumerate(AVANTAGES):
        fond_b, coul_n, coul_t, coul_e = (("#B8A07E", "#0D0D0D", "#0D0D0D", "#0D0D0D") if i == 0
                                          else ("#222222", "#B8A07E", "#F4F1EC", "#B8A07E"))
        bandes += (f'<div id="s6-b{i}" class="a bande" style="left:96px;top:{1110 + 140 * i}px;width:888px;height:124px;background:{fond_b};'
                   f'clip-path:polygon(52px 0,100% 0,calc(100% - 52px) 100%,0 100%)">'
                   f'<span class="t8 it num" style="font-size:64px;color:{coul_n};margin-left:76px;width:100px">{n}</span>'
                   f'<span style="display:flex;flex-direction:column;gap:12px">'
                   f'<span class="t8" style="font-size:52px;color:{coul_t}">{nom}</span>'
                   f'<span class="kick" style="font-size:26px;color:{coul_e};letter-spacing:.16em">{etat}</span></span></div>')
    tp = at("s6", "prix")
    contenu = f"""
{cache(96, 236, 888, f'<div class="kick" style="font-size:38px">{plus(40)}L’option Premium</div>', "s6-kick")}
<div id="s6-prix" class="a" style="left:96px;top:300px;display:flex;align-items:center;gap:26px">
  <div id="s6-plus">{plus(200)}</div>
  <div id="s6-deux" class="t9 num" style="font-size:410px;line-height:.86">2 €</div>
</div>
<div id="s6-ttc" class="a t8 it" style="left:96px;top:690px;font-size:116px">TTC par semaine</div>
<p id="s6-soit" class="a corps" style="left:96px;top:836px;width:888px;font-size:50px">Soit 8&nbsp;€ toutes les 4 semaines,<br>en plus de votre abonnement.</p>
{cache(96, 1056, 888, '<div class="kick" style="font-size:34px">3 avantages inclus</div>', "s6-kick2")}
{bandes}
"""
    js = (monte("s6-kick", at("s6", "kick"), 0.55)
          + f'        tl.fromTo("#s6-plus", {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.6)" }}, {tp});\n'
          + f'        tl.fromTo("#s6-deux", {{ scale: 1.3, clipPath: "inset(0% 100% 0% 0%)" }}, {{ scale: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power4.out", transformOrigin: "left center" }}, {tp});\n'
          + f'        tl.fromTo(["#s6-ttc", "#s6-soit"], {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.out" }}, {tp});\n'
          + monte("s6-kick2", at("s6", "kick2"), 0.5)
          + "".join(f'        tl.from("#s6-b{i}", {{ x: -1100, duration: 0.65, ease: "power3.out" }}, {at("s6", "bandes", i)});\n'
                    for i in range(len(AVANTAGES))))
    return scene("s6", contenu, js)


def s7():
    contenu = f"""
<div id="s7-logo" class="a" style="left:330px;top:250px;width:420px"><img src="assets/img/logo-complet.png" alt="LA SALLE" style="display:block;width:420px"></div>
{cache(40, 620, 1000, '<div class="t9" style="font-size:180px;text-align:center">Activez-la</div>', "s7-l1")}
{cache(40, 785, 1000, '<div class="t9" style="font-size:180px;text-align:center">à l’accueil.</div>', "s7-l2")}
{cache(40, 1010, 1000, '<div class="t8 it or" style="font-size:88px;text-align:center">En quelques secondes.</div>', "s7-l3")}
{cache(40, 1172, 1000, '<div class="kick" style="justify-content:center;font-size:38px">Urban Valley · 7J/7 · 6H–23H</div>', "s7-l4")}
<p id="s7-mention" class="a mention" style="left:96px;top:1290px;width:888px;padding:20px 30px;font-size:36px;line-height:1.26;text-align:center">{MENTION_OPTION}</p>
"""
    js = (f'        tl.from("#s7-logo", {{ clipPath: "inset(0% 0% 100% 0%)", y: -30, duration: 0.6, ease: "power3.out" }}, {at("s7", "logo")});\n'
          + monte("s7-l1", at("s7", "l1")) + monte("s7-l2", at("s7", "l2")) + monte("s7-l3", at("s7", "l3"))
          + monte("s7-l4", at("s7", "l4"), 0.55)
          + f'        tl.from("#s7-mention", {{ clipPath: "inset(100% 0% 0% 0%)", duration: 0.6, ease: "power2.out" }}, {at("s7", "mention")});\n')
    return scene("s7", contenu, js)


def volets():
    """Filet or sur le bord du dévoilement : même durée, même courbe que le clip-path de la scène qui entre
    (aucun filet sur une bascule : la caméra descend, rien ne se dévoile en biais)."""
    coupes = [t for c, t, _ in SCENES[1:] if c not in BASCULE]
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
    <!-- Story fontaine à boisson sportive : visuels rejoués texte par texte, parcours sur l'écran réel et versement,
         {DUREE:g} s, {FPS} i/s, 120 BPM. Coupes à {coupes} s : la scène suivante se dévoile en biais en {VOLET} s,
         centrées sur la coupe ; à {", ".join(f"{t:g}" for c, t, _ in SCENES if c in BASCULE)} s, la caméra descend de l'écran à la buse. -->
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
    fontaine = os.path.join(SOURCES, "fontaine_ecran.png")          # fontaine détourée, écran réel posé dans sa dalle
    if not os.path.exists(fontaine):
        sys.exit(f"Absent : {fontaine} (lancer tools/detourer.py puis tools/ecrans.py)")
    shutil.copy2(fontaine, os.path.join(p, "assets", "img", "fontaine.png"))
    if nom == "story-916":
        for e in ECRANS:
            shutil.copy2(os.path.join(SOURCES, "ecran", "propres", e + ".jpg"), os.path.join(p, "assets", "img", f"ecran-{e}.jpg"))
        shutil.copy2(os.path.join(SOURCES, "ecran", "cadre.png"), os.path.join(p, "assets", "img", "cadre.png"))
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
    for cid, f in zip([c for c, _, _ in SCENES] + ["fond", "volets"], (s1, s2, s3, s4, s5, s6, s7, fond_story, volets)):
        ecrire(os.path.join(s, "compositions", f"{cid}.html"), f())
    print("Écrit :", a, s)


if __name__ == "__main__":
    main()
