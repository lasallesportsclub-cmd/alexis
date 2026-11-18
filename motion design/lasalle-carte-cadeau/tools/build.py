"""Carte cadeau LA SALLE : stories 9:16 de 12 s, 30 i/s, 120 BPM, trois accroches (A « Offrez », B « La question »,
C « Le montant ») et la même suite de 2 à 12 s.

Demande du 18/11/2026 : présenter la carte cadeau « de la valeur dont la personne le souhaite » (100, 150, 200, 300 €
ou montant au choix), entièrement déductible sur un abonnement, vendue à l'accueil (carte physique ou image).

  0–2 s     accroche, propre à chaque variante ; tout est en place à l'image 0
  2–6,5 s   « Comment ça marche » : la carte, son montant qui défile, trois étapes numérotées
  6,5–7 s   cassure (musique coupée) : « ET EN PLUS, »
  7–9 s     « 45 € » barré par le filet or, « OFFERTS. » (⚠ frais d'inscription offerts : A_valider.md)
  9–12 s    carte finale : « EN VENTE À L'ACCUEIL. », les montants, Urban Valley, mention

Coupes franches sur la grille de 120 BPM (un temps = 0,5 s) ; le premier élément de chaque scène est là dès la coupe.
Charte « Le Trait Oblique » (_sources-premium/shared/frame.md). Atome récurrent : la carte cadeau (surface #222, filet
or, ruban or coupé à la pente 0,42, logo négatif, montant en or). Repères : SCENES et T, lus aussi par
tools/musique.py et tools/livrer.py.

Usage : python3 tools/build.py   (puis tools/musique.py, rendu, tools/livrer.py)
Recopie dans <projet>/assets/ (ignorés par git) : polices et GSAP (_sources-premium/), logo négatif
(lasalle-fontaine/_communs/img/), musique (_communs/).
"""
import os
import shutil

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
MD = os.path.normpath(os.path.join(RACINE, ".."))

FPS = 30
DUREE = 12.0
# Scènes communes (id, début, fin) ; la scène s1 est l'accroche de chaque variante
SCENES = [("s1", 0.0, 2.0), ("s2", 2.0, 6.5), ("s3", 6.5, 7.0), ("s4", 7.0, 9.0), ("s5", 9.0, 12.0)]
CASSURE = (6.5, 7.0)
# Instants absolus des entrées (secondes)
T = {
    "kick2": 2.05, "etape1": 2.25, "montants": [2.75, 3.25, 3.75, 4.25], "etape2": 4.75, "etape3": 5.5,
    "kick4": 7.05, "barre": 7.35, "offerts": 7.6, "pour": 8.0,
    "logo": 9.0, "vente": 9.15, "accueil": 9.4, "liste": 9.85, "infos": 10.2, "mention": 9.6,
}
VARIANTES = {
    "A": {"projet": "story-916-A", "nom": "A_offrez"},
    "B": {"projet": "story-916-B", "nom": "B_question"},
    "C": {"projet": "story-916-C", "nom": "C_montant"},
}

# ---------------------------------------------------------------- textes (vouvoiement, LA SALLE)
MONTANTS = ["100", "150", "200", "300"]            # demande du 18/11/2026
ETAPES = ["Choisissez le montant.", "Offrez-la à qui vous voulez.", "Elle est déduite de son abonnement."]
INFOS = "Urban Valley · 7j/7 · 6h–23h"
# ⚠ Frais d'inscription offerts à la personne qui reçoit la carte : proposé, pas encore confirmé (A_valider.md)
MENTION = ("Montant entièrement déductible sur un abonnement LA&nbsp;SALLE, pour la personne qui reçoit la carte. "
           "Conditions à l’accueil.")

POLICES = "".join(
    f'@font-face {{ font-family: "{f}"; font-weight: {w}; font-style: {s}; font-display: block; '
    f'src: url("assets/fonts/{fic}") format("woff2"); }}\n'
    for f, w, s, fic in [
        ("Barlow Condensed", 800, "normal", "barlow-condensed-latin-800-normal.woff2"),
        ("Barlow Condensed", 800, "italic", "barlow-condensed-latin-800-italic.woff2"),
        ("Barlow Condensed", 900, "normal", "barlow-condensed-latin-900-normal.woff2"),
        ("Barlow Condensed", 900, "italic", "barlow-condensed-latin-900-italic.woff2"),
        ("DM Sans", 500, "normal", "dm-sans-latin-500-normal.woff2"),
        ("DM Sans", 700, "normal", "dm-sans-latin-700-normal.woff2"),
    ])

CSS = POLICES + """
.fr { position: absolute; inset: 0; overflow: hidden; color: #F4F1EC; font-family: "Barlow Condensed", sans-serif; font-kerning: normal; }
.fr * { margin: 0; padding: 0; box-sizing: border-box; }
.fr .a { position: absolute; }
.fr .m { position: absolute; overflow: hidden; }
.fr .kick { font-family: "DM Sans", sans-serif; font-weight: 500; font-size: 34px; letter-spacing: .16em; text-transform: uppercase; color: #B8A07E; white-space: nowrap; line-height: 1; }
.fr .t9 { font-weight: 900; text-transform: uppercase; line-height: .88; letter-spacing: -.005em; white-space: nowrap; }
.fr .t8 { font-weight: 800; text-transform: uppercase; line-height: 1; white-space: nowrap; }
.fr .it { font-style: italic; }
.fr .or { color: #B8A07E; }
.fr .corps { font-family: "DM Sans", sans-serif; font-weight: 500; line-height: 1.3; color: #F4F1EC; letter-spacing: -.01em; }
.fr .num { font-variant-numeric: tabular-nums; }
.fr .mention { background: #222222; color: #F4F1EC; font-family: "DM Sans", sans-serif; font-weight: 500; letter-spacing: -.01em; }
.fr .filet { background: #B8A07E; }
.fr .carte { background: #222222; border-style: solid; border-color: #B8A07E; overflow: hidden; }
.fr .ruban { position: absolute; inset: 0; background: #B8A07E; }
.fr .valeur { font-family: "DM Sans", sans-serif; font-weight: 500; letter-spacing: .16em; text-transform: uppercase; color: rgba(244,241,236,.72); white-space: nowrap; line-height: 1; text-align: right; }
.fr .etape { display: flex; align-items: baseline; gap: 22px; }
.fr .etape .n { font-weight: 800; font-style: italic; color: #B8A07E; flex: none; }
"""

FOND_CSS = """
.fond { position: absolute; inset: 0; background: #0D0D0D; overflow: hidden; }
.fond .b { position: absolute; top: 0; height: 100%; background: rgba(244,241,236,.022); }
.fond::after { content: ""; position: absolute; inset: 0; opacity: .7; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='256' height='256'><filter id='n' color-interpolation-filters='sRGB'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>"); }
"""
PAD = 30


def fond(h, cid=""):
    """Canvas, deux bandes obliques à peine plus claires (pente 0,42), grain fin (frame.md)."""
    d = round(0.42 * h)
    return (f'<div class="fond">'
            f'<div id="{cid}b1" class="b" style="left:-{d}px;width:{d + 380}px;clip-path:polygon({d}px 0,100% 0,calc(100% - {d}px) 100%,0 100%)"></div>'
            f'<div id="{cid}b2" class="b" style="left:{1080 - 260}px;width:{d + 420}px;clip-path:polygon({d}px 0,100% 0,calc(100% - {d}px) 100%,0 100%)"></div>'
            f'</div>')


def composition(cid, duree, corps, script):
    return f"""<!doctype html>
<html lang="fr">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template id="{cid}-template">
      <style>
{CSS}
{FOND_CSS}
        #{cid}-root {{ position: absolute; inset: 0; }}
      </style>
      <div id="{cid}-root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-duration="{duree:g}">
        <div id="{cid}-scene" class="fr clip" data-start="0" data-duration="{duree:g}" data-track-index="0" style="width:1080px;height:1920px">
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


def scene(cid, debut, fin, contenu, js):
    corps = f'{fond(1920, cid + "-")}\n<div id="{cid}-c" class="a" style="inset:0">\n{contenu}\n</div>'
    return composition(cid, round(fin - debut, 3), corps, js)


def cache(left, top, w, inner, mid, pad=PAD, attrs=""):
    """Glissement masqué : top est le haut du texte ; le cache déborde de pad au-dessus et au-dessous.
    attrs : marqueurs de mise en page voulus (montants empilés dans la carte, texte encore sous son cache)."""
    return (f'<div class="m" style="left:{left}px;top:{top - pad}px;width:{w}px;padding:{pad}px 0" '
            f'data-layout-allow-overflow{attrs}><div id="{mid}">{inner}</div></div>')


def monte(mid, t, d=0.45, pad=PAD, ease="power3.out"):
    return (f'        tl.fromTo("#{mid}", {{ yPercent: 100, y: {2 * pad} }}, '
            f'{{ yPercent: 0, y: 0, duration: {d}, ease: "{ease}" }}, {t:.3f});\n')


def sort(mid, t, d=0.3, pad=PAD):
    return f'        tl.to("#{mid}", {{ yPercent: -100, y: {-2 * pad}, duration: {d}, ease: "power2.in" }}, {t:.3f});\n'


def frappe(sel, t, origine="left center", echelle=1.35):
    """Le mot frappe : il entre trop grand et se pose en 0,45 s, dévoilé de gauche à droite."""
    return (f'        tl.fromTo("{sel}", {{ scale: {echelle}, clipPath: "inset(0% 100% 0% 0%)" }}, {{ scale: 1, clipPath: "inset(0% 0% 0% 0%)", '
            f'duration: 0.45, ease: "power4.out", transformOrigin: "{origine}" }}, {t:.3f});\n')


def montant_html(m, k, choix=False):
    if choix:
        return (f'<div class="t9 or" style="font-size:{round(96 * k)}px;text-align:right;line-height:.9">Montant<br>au choix</div>')
    return (f'<div class="t9 or num" style="font-size:{round(200 * k)}px;text-align:right">{m}&nbsp;€</div>')


def carte(cid, x, y, w, montants=("150",), choix=False):
    """La carte cadeau : surface #222, filet or, ruban or coupé à la pente 0,42 dans le coin, logo négatif, montant or.
    Les montants sont empilés au même endroit, chacun dans son cache (défilement par glissements masqués)."""
    k = w / 880
    W, H = 880, 555
    h = round(H * k)
    bord = max(2, round(4 * k))
    x0, bw = 742, 46                                    # bas du ruban (x) et largeur, en unités de la carte de 880
    def para(a, l):
        return (f"polygon({round((a + 0.42 * H) * k)}px 0, {round((a + 0.42 * H + l) * k)}px 0, "
                f"{round((a + l) * k)}px {h}px, {round(a * k)}px {h}px)")
    droite = round(690 * k)                             # bord droit des montants (le ruban passe à droite)
    larg = round(560 * k)
    pile = ""
    tous = list(montants) + (["choix"] if choix else [])
    for i, m in enumerate(tous):
        top = round((196 if m == "choix" else 190) * k)
        pile += cache(droite - larg, top, larg, montant_html(m, k, m == "choix"), f"{cid}-m{i}", round(24 * k),
                      " data-layout-allow-overlap data-layout-allow-occlusion")
    return f"""<div id="{cid}-carte" class="a carte" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-width:{bord}px;border-radius:{round(26 * k)}px">
  <div class="ruban" style="clip-path:{para(x0, bw)}"></div>
  <div class="ruban" style="clip-path:{para(x0 - 34, 9)}"></div>
  <img class="a" src="assets/img/logo-complet.png" alt="LA SALLE" style="left:{round(50 * k)}px;top:{round(44 * k)}px;width:{round(200 * k)}px">
  <div class="a valeur" style="left:{droite - larg}px;top:{round(150 * k)}px;width:{larg}px;font-size:{round(24 * k)}px">Valeur</div>
  {pile}
  <div class="a t9" style="left:{round(50 * k)}px;top:{round(440 * k)}px;font-size:{round(76 * k)}px">Carte cadeau</div>
</div>"""


# ---------------------------------------------------------------- s1 : les trois accroches (tout est là à l'image 0)
def accroche(cle):
    d = 2.0
    if cle == "A":
        contenu = f"""
<div class="a kick" style="left:96px;top:300px">Carte cadeau · Noël</div>
<div id="s1-titre" class="a" style="left:92px;top:370px">
  <div class="t9" style="font-size:212px">Offrez</div>
  <div class="t9 or" style="font-size:212px">LA SALLE.</div>
</div>
{carte("s1", 160, 790, 760)}
"""
        js = (f'        tl.fromTo("#s1-titre", {{ scale: 1 }}, {{ scale: 1.04, duration: {d:g}, ease: "none", transformOrigin: "left center" }}, 0);\n'
              f'        tl.fromTo("#s1-carte", {{ rotation: -2.5, y: 0 }}, {{ rotation: 0, y: -18, duration: {d:g}, ease: "sine.inOut", transformOrigin: "50% 50%" }}, 0);\n')
    elif cle == "B":
        contenu = f"""
<div class="a kick" style="left:96px;top:300px">Carte cadeau · Noël</div>
<div id="s1-titre" class="a" style="left:92px;top:370px">
  <div class="t9" style="font-size:140px">Vous ne</div>
  <div class="t9" style="font-size:140px">savez pas</div>
  <div class="t9" style="font-size:140px">quoi</div>
  <div class="t9 or" style="font-size:140px">offrir&nbsp;?</div>
</div>
{carte("s1", 480, 920, 500)}
"""
        js = (f'        tl.fromTo("#s1-titre", {{ scale: 1 }}, {{ scale: 1.04, duration: {d:g}, ease: "none", transformOrigin: "left center" }}, 0);\n'
              f'        tl.fromTo("#s1-carte", {{ rotation: 6, y: 0 }}, {{ rotation: 3, y: -16, duration: {d:g}, ease: "sine.inOut", transformOrigin: "50% 50%" }}, 0);\n')
    else:
        contenu = """
<div class="a kick" style="left:96px;top:300px">Carte cadeau · Noël</div>
<div id="s1-titre" class="a" style="left:92px;top:370px">
  <div class="t9" style="font-size:150px">Offrez-lui</div>
  <div class="t9 or num" style="font-size:340px;line-height:.86">150&nbsp;€</div>
  <div class="t9" style="font-size:136px">sur son</div>
  <div class="t9" style="font-size:136px">abonnement.</div>
</div>
<div id="s1-filet" class="a filet" style="left:96px;top:1236px;width:888px;height:6px;transform-origin:left center"></div>
"""
        js = (f'        tl.fromTo("#s1-titre", {{ scale: 1 }}, {{ scale: 1.04, duration: {d:g}, ease: "none", transformOrigin: "left center" }}, 0);\n'
              f'        tl.fromTo("#s1-filet", {{ scaleX: 0.25 }}, {{ scaleX: 1, duration: 0.9, ease: "power2.out" }}, 0);\n')
    return scene("s1", 0.0, d, contenu, js)


# ---------------------------------------------------------------- s2 : comment ça marche
def s2():
    debut, fin = 2.0, 6.5
    etapes = "".join(cache(96, 1000 + 92 * i, 888,
                           f'<div class="etape"><span class="n num" style="font-size:60px;width:76px">{i + 1:02d}</span>'
                           f'<span class="corps" style="font-size:44px;white-space:nowrap">{e}</span></div>', f"s2-e{i}", 20)
                     for i, e in enumerate(ETAPES))
    contenu = f"""
{cache(96, 300, 888, '<div class="kick">Comment ça marche</div>', "s2-kick", PAD, " data-layout-allow-occlusion")}
{carte("s2", 100, 390, 880, MONTANTS, choix=True)}
{etapes}
"""
    k = 1.0
    js = (monte("s2-kick", T["kick2"] - debut, 0.4)
          + f'        tl.fromTo("#s2-carte", {{ scale: 0.92, rotation: -2 }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: "power3.out", transformOrigin: "50% 50%" }}, 0);\n'
          + monte("s2-e0", T["etape1"] - debut, 0.45, 20) + monte("s2-e1", T["etape2"] - debut, 0.45, 20)
          + monte("s2-e2", T["etape3"] - debut, 0.45, 20))
    pad = round(24 * k)
    # 100 € est là dès la coupe ; défilement en rouleau : le montant sort par le haut pendant que le suivant monte,
    # même durée et même courbe, si bien qu'ils restent séparés de 2 × pad (aucun chevauchement)
    for i, t in enumerate(T["montants"]):
        retard = 0.1 if i == len(T["montants"]) - 1 else 0.0   # « MONTANT AU CHOIX » est plus haut : il attend un peu
        js += (f'        tl.to("#s2-m{i}", {{ yPercent: -100, y: {-2 * pad}, duration: 0.32, ease: "power3.inOut" }}, {t - debut:.3f});\n'
               + monte(f"s2-m{i + 1}", t - debut + retard, 0.32, pad, "power3.inOut"))
    return scene("s2", debut, fin, contenu, js)


# ---------------------------------------------------------------- s3 : la cassure (musique coupée)
def s3():
    debut, fin = 6.5, 7.0
    contenu = """
<div id="s3-l" class="a" style="left:92px;top:720px">
  <div class="t9" style="font-size:230px">Et en</div>
  <div class="t9 or" style="font-size:230px">plus,</div>
</div>
"""
    js = '        tl.fromTo("#s3-l", { scale: 1 }, { scale: 1.06, duration: 0.5, ease: "none", transformOrigin: "left center" }, 0);\n'
    return scene("s3", debut, fin, contenu, js)


# ---------------------------------------------------------------- s4 : les frais d'inscription (⚠)
def s4():
    debut, fin = 7.0, 9.0
    c = round(0.42 * 18)
    contenu = f"""
{cache(96, 300, 888, '<div class="kick">Pour la personne qui la reçoit</div>', "s4-kick")}
<div class="a" style="left:92px;top:380px">
  <div class="t9" style="font-size:132px">Les frais</div>
  <div class="t9" style="font-size:132px">d’inscription</div>
</div>
<div id="s4-prix" class="a t9 num" data-layout-allow-occlusion style="left:92px;top:640px;font-size:320px">45&nbsp;€</div>
<div id="s4-barre" class="a filet" style="left:72px;top:766px;width:560px;height:18px;clip-path:polygon({c}px 0,100% 0,calc(100% - {c}px) 100%,0 100%);transform-origin:left center"></div>
<div id="s4-offerts" class="a t9 or" style="left:92px;top:960px;font-size:212px">Offerts.</div>
"""
    js = (monte("s4-kick", T["kick4"] - debut, 0.4)
          + f'        tl.fromTo("#s4-barre", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.out" }}, {T["barre"] - debut:.3f});\n'
          + f'        tl.to("#s4-prix", {{ opacity: 0.45, duration: 0.3, ease: "power1.out" }}, {T["barre"] - debut + 0.1:.3f});\n'
          + frappe("#s4-offerts", T["offerts"] - debut))
    return scene("s4", debut, fin, contenu, js)


# ---------------------------------------------------------------- s5 : carte finale
def s5():
    debut, fin = 9.0, 12.0
    liste = " · ".join(f"{m}&nbsp;€" for m in MONTANTS)
    contenu = f"""
<div id="s5-logo" class="a" style="left:390px;top:290px;width:300px"><img src="assets/img/logo-complet.png" alt="LA SALLE" style="display:block;width:300px"></div>
{cache(40, 540, 1000, '<div class="t9" style="font-size:176px;text-align:center">En vente</div>', "s5-l1")}
{cache(40, 700, 1000, '<div class="t9 or" style="font-size:140px;text-align:center">à l’accueil.</div>', "s5-l2")}
{cache(40, 880, 1000, f'<div class="t8 num" style="font-size:58px;text-align:center">{liste}</div>', "s5-l3", 20)}
{cache(40, 950, 1000, '<p class="corps" style="font-size:40px;text-align:center">ou le montant de votre choix</p>', "s5-l4", 20)}
{cache(40, 1032, 1000, f'<div class="kick" style="text-align:center">{INFOS}</div>', "s5-l5", 20, " data-layout-allow-occlusion")}
<p id="s5-mention" class="a mention" style="left:108px;top:1100px;width:864px;padding:18px 28px;font-size:29px;line-height:1.3;text-align:center">{MENTION}</p>
"""
    js = (f'        tl.from("#s5-logo", {{ clipPath: "inset(0% 0% 100% 0%)", y: -30, duration: 0.45, ease: "power3.out" }}, 0.0);\n'
          + monte("s5-l1", T["vente"] - debut, 0.45) + monte("s5-l2", T["accueil"] - debut, 0.45)
          + monte("s5-l3", T["liste"] - debut, 0.45, 20) + monte("s5-l4", T["liste"] - debut + 0.15, 0.45, 20)
          + monte("s5-l5", T["infos"] - debut, 0.45, 20)
          + f'        tl.from("#s5-mention", {{ clipPath: "inset(100% 0% 0% 0%)", duration: 0.5, ease: "power2.out" }}, {T["mention"] - debut:.3f});\n')
    return scene("s5", debut, fin, contenu, js)


def index(cle):
    hotes = "\n".join(
        f'      <div id="h-{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{a:g}" '
        f'data-duration="{b - a:g}" data-track-index="{1 + i % 2}" data-width="1080" data-height="1920" style="z-index:{i + 1}"></div>'
        for i, (c, a, b) in enumerate(SCENES))
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
    </style>
  </head>
  <body>
    <!-- Carte cadeau LA SALLE, accroche {cle} : {len(SCENES)} scènes en coupes franches, {DUREE:g} s, {FPS} i/s, 120 BPM -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUREE:g}" data-width="1080" data-height="1920" data-fps="{FPS}">
{hotes}
      <audio id="musique" src="assets/audio/musique.wav" data-start="0" data-duration="{DUREE:g}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


# ---------------------------------------------------------------- assets et projet
def projet(cle):
    nom = VARIANTES[cle]["projet"]
    p = os.path.join(RACINE, nom)
    for d in ("assets/fonts", "assets/vendor", "assets/img", "assets/audio", "compositions"):
        os.makedirs(os.path.join(p, d), exist_ok=True)
    for f in os.listdir(os.path.join(MD, "_sources-premium", "fonts")):
        shutil.copy2(os.path.join(MD, "_sources-premium", "fonts", f), os.path.join(p, "assets", "fonts", f))
    shutil.copy2(os.path.join(MD, "_sources-premium", "js", "gsap.min.js"), os.path.join(p, "assets", "vendor", "gsap.min.js"))
    shutil.copy2(os.path.join(MD, "lasalle-fontaine", "_communs", "img", "logo-complet.png"),
                 os.path.join(p, "assets", "img", "logo-complet.png"))
    musique = os.path.join(RACINE, "_communs", "musique_carte_cadeau.wav")
    if os.path.exists(musique):
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
  "name": "lasalle-carte-cadeau-{nom}",
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
    ecrire(os.path.join(p, "meta.json"), f'{{\n  "id": "lasalle-carte-cadeau-{nom}",\n  "name": "lasalle-carte-cadeau-{nom}",\n  "createdAt": "2026-11-18T18:30:00.000Z"\n}}\n')
    return p


def ecrire(chemin, texte):
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)


def main():
    communes = {"s2": s2(), "s3": s3(), "s4": s4(), "s5": s5()}
    for cle in VARIANTES:
        p = projet(cle)
        for f in os.listdir(os.path.join(p, "compositions")):
            os.remove(os.path.join(p, "compositions", f))
        ecrire(os.path.join(p, "index.html"), index(cle))
        ecrire(os.path.join(p, "compositions", "s1.html"), accroche(cle))
        for cid, html in communes.items():
            ecrire(os.path.join(p, "compositions", f"{cid}.html"), html)
        print("Écrit :", p)


if __name__ == "__main__":
    main()
