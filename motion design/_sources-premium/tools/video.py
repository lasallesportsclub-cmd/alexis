"""Génère les compositions HyperFrames des vidéos Premium (story 9:16 et post 4:5) à partir des cadres validés.

Toutes les bornes de temps viennent de TIMING (secondes, temps global). Elles avaient été estimées pour la voix de Nika ;
décision du 13/10/2026 : vidéos livrées sans voix ni musique, sur ce minutage. Pour recaler : modifier ici puis relancer.
Version voix « ton pub » (14/10/2026) : --voix recale les textes sur les répliques préparées par voix.py (POSE_VOIX) et
ajoute les pistes voix. Les fichiers voix restent hors du dépôt (assets/voix/ ignoré par git).
Usage : python3 video.py A [B C]          → premium-916/<concept> (1080×1920)
        python3 video.py --45 A [B C]     → premium-45/<concept>  (1080×1350)
        python3 video.py [--45] --voix A B C

4:5 (règle de frame.md, adaptée au film) : la pastille passe à y 150, les mentions à y 1015–1215, les volets ont 3 bandes
de 450 px. Les scènes 1 à 4 (sans mentions) remontent de 60 px pour que le bloc reste centré sous la pastille (y 390–990) ;
la fin commune remonte de 100 px pour laisser 70 px au moins au-dessus des mentions. Les titres gardent leur taille 9:16 :
à largeur égale ils tiennent dans la zone 4:5 ; la réduction ×0,85 ne sert qu'aux images, plus chargées.
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
import frames as F  # noqa: E402
from frames import NB, FONTAINE, RAPPEL, GOLD, CANVAS, PLUS_PTS  # noqa: E402

MD = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSS = open(os.path.join(MD, "_sources-premium", "shared", "premium.css"), encoding="utf-8").read()
W, H = 1080, 1920
END = 14.933
# Paramètres du format (9:16 par défaut ; set_format("45") pour le post 4:5)
FMT = {"916": dict(H=1920, DY=0, DY_FIN=0, PAST_Y=300, MENT_Y=1040, DIR="premium-916", LABEL="9:16", RES="portrait"),
       "45": dict(H=1350, DY=-60, DY_FIN=-100, PAST_Y=150, MENT_Y=1015, DIR="premium-45", LABEL="4:5", RES="portrait")}
CUR = FMT["916"]


def set_format(key):
    global H, CUR
    CUR = FMT[key]
    H = CUR["H"]


def stage(inner, dy=None):
    """Calque 1080×1920 décalé de dy : les cadres 9:16 validés gardent leurs coordonnées (masques, clip-path, origines)."""
    dy = CUR["DY"] if dy is None else dy
    if not dy:
        return inner
    return f'<div class="a" data-layout-allow-overflow style="left:0;top:{dy}px;width:{W}px;height:1920px">{inner}</div>'

# ─── Minutage commun (fin commune, pastille, mentions) : identique pour A, B et C ───
COMMON = {
    "fin": 7.5,          # coupe sèche vers la cassure
    "g25_1": 7.969,      # « LES 4 PREMIÈRES » (voix 25)
    "drop": 8.4375,      # drop : « SEMAINES »
    "g25_2": 9.2,        # « DE L'OPTION PREMIUM »
    "mentions": 9.375,   # panneau des mentions en place
    "g25_3": 10.0,       # « SONT OFFERTES. » + condition
    "prix": 10.97,       # fin de la 25 → volet → prix
    "carte": 12.19,      # volet → carte finale
    "p9_1": 12.3,        # « ACTIVEZ-LA À L'ACCUEIL, »
    "p9_2": 13.4,        # « EN QUELQUES SECONDES. »
    "hold": 13.84,       # statique jusqu'à la fin
}
# ─── Minutage propre à chaque concept ───
TIMING = {
    "A": {"s": [0.0, 1.875, 4.219, 6.563], "volets": [4.219, 6.563], "premium": 1.1, "p5_1": 2.36, "p5_2": 3.05,
          "p6_1": 4.25, "p6_2": 5.156, "etiq": 5.6},
    "B": {"s": [0.0, 1.406, 4.219, 5.625], "volets": [1.406, 5.625],
          "p4": [1.45, 2.0, 2.813, 3.4], "eau": [4.25, 4.42], "saveurs": [4.25, 4.53, 4.81, 5.09, 5.37],
          "p5_1": 5.65, "p5_2": 6.3, "b02": 6.563, "b03": 7.031},
    "C": {"s": [0.0, 1.875, 4.688, 6.563], "volets": [1.875, 4.688], "p6_1": 2.0, "p6_2": 3.281, "etiq": 3.9},
}

# ─── Voix « ton pub » : début de parole de chaque réplique (temps global) ───
# Les textes tombent une image (AVANCE) avant leur mot ; repères des mots dans ~/voix-clone/premium/final/voix.json.
POSE_VOIX = {
    "A": [("P1", 0.06), ("P5", 2.36), ("P6", 4.27)],
    "B": [("P2", 0.06), ("P4a", 1.46), ("P4b", 4.79), ("P5r", 6.06)],   # B : coupes sèches avant « ou » et « une »
    "C": [("P3", 0.06), ("P6", 2.0)],
}
POSE_FIN = [("25", 7.97), ("P9", 12.31)]
AVANCE = 0.03
VOIX_JSON = os.path.expanduser("~/voix-clone/premium/final/voix.json")
SFX_VOIX = 0.72  # bruitages sous la voix (−2,9 dB ; les répliques sont à −16,4 LUFS, voir voix.py)


def timing_voix(concept):
    """Minutage recalé sur la voix : TIMING du concept, valeurs de COMMON, et data-start de chaque réplique."""
    V = json.load(open(VOIX_JSON))
    poses = POSE_VOIX[concept] + POSE_FIN
    debut = {n: round(t - V[n]["parole"][0], 3) for n, t in poses}
    dit = lambda n: round(dict(poses)[n] - AVANCE, 3)                      # noqa: E731
    mot = lambda n, k: round(debut[n] + V[n]["reperes"][k] - AVANCE, 3)    # noqa: E731
    T = json.loads(json.dumps(TIMING[concept]))
    C = {"g25_1": dit("25"), "drop": mot("25", "semaines"), "g25_2": mot("25", "de"), "g25_3": mot("25", "sont"),
         "p9_1": dit("P9"), "p9_2": mot("P9", "en")}
    if concept == "A":
        T.update(premium=mot("P1", "premium"), p5_1=dit("P5"), p5_2=mot("P5", "toutes"),
                 p6_1=dit("P6"), p6_2=mot("P6", "chaque"))
        T["etiq"] = round(T["p6_2"] + 0.25, 3)
    if concept == "B":
        s3, s4 = round(dit("P4b") - 0.02, 3), round(dit("P5r") - 0.02, 3)
        T["s"], T["volets"] = [0.0, 1.406, s3, s4], [1.406]
        T["p4"] = [mot("P4a", k) for k in ("collagene", "multivitamines", "carnitine", "booster")]
        T["eau"] = [dit("P4b"), mot("P4b", "eau")]
        pas = round((s4 - s3 - 0.33) / 4, 3)
        T["saveurs"] = [round(s3 + 0.03 + pas * i, 3) for i in range(5)]
        T.update(p5_1=dit("P5r"), p5_2=mot("P5r", "toutes"))
        T["b02"] = round(T["p5_2"] + 0.25, 3)
        T["b03"] = round(T["b02"] + 0.15, 3)
    if concept == "C":
        T.update(p6_1=dit("P6"), p6_2=mot("P6", "chaque"))
        T["etiq"] = round(T["p6_2"] + 0.25, 3)
    pistes = [(n, debut[n], V[n]["duree"]) for n, _ in poses]
    return T, C, pistes


def voix_audio(pistes):
    return "\n".join(
        f'      <audio id="voix-{n}" src="assets/voix/{n}.wav" data-audio-group="voix" data-start="{s:.3f}" '
        f'data-duration="{d:.3f}" data-track-index="{20 + i}" data-volume="1"></audio>'
        for i, (n, s, d) in enumerate(pistes))


EXTRA_CSS = """
.layer { position: absolute; inset: 0; }
.mask { position: absolute; overflow: hidden; padding: 0.2em 0.06em 0.08em 0; margin-top: -0.2em; }
.mask > div { display: block; }
.fr.ov { background: transparent; }
.fr.ov::after { display: none; }
"""

JS_HELPERS = """
      const tl = gsap.timeline({ paused: true });
      // Coupes sèches : 1 ms (une durée nulle appliquerait l'état final dès la création)
      const show = (s, t) => tl.fromTo(s, { visibility: "hidden" }, { visibility: "visible", duration: 0.001, ease: "none", immediateRender: true }, t);
      const hide = (s, t) => tl.fromTo(s, { visibility: "visible" }, { visibility: "hidden", duration: 0.001, ease: "none", immediateRender: false }, t);
      // Le masque reste masqué jusqu'à l'entrée de sa ligne (aucun texte en attente dans la page)
      const fall = (s, t, d = 0.18) => { show(s.replace(/-t$/, ""), t); tl.fromTo(s, { yPercent: 118 }, { yPercent: 0, duration: d, ease: "power4.out" }, t); };
      const slam = (s, t, k = 1.28) => { show(s, t); tl.fromTo(s, { scale: k }, { scale: 1, duration: 0.16, ease: "power4.out" }, t); };
      const wipe = (s, t, d = 0.22) => tl.fromTo(s, { clipPath: "inset(0px 100% 0px 0px)" }, { clipPath: "inset(0px 0% 0px 0px)", duration: d, ease: "power3.out" }, t);
      const drop = (s, t, d = 0.2) => tl.fromTo(s, { clipPath: "inset(0px 0px 100% 0px)" }, { clipPath: "inset(0px 0px 0% 0px)", duration: d, ease: "power2.out" }, t);
      const shake = (s, t) => tl.to(s, { keyframes: [{ x: 7, y: -5, duration: 1 / 30 }, { x: -5, y: 4, duration: 1 / 30 }, { x: 0, y: 0, duration: 1 / 30 }], ease: "none" }, t);
"""


def mask(id_, x, y, cls, txt, style=""):
    """Ligne de texte cinétique : un masque fixe, le texte monte dedans (aucun fondu)."""
    return f'<div id="{id_}" class="mask" style="left:{x}px;top:{y}px"><div id="{id_}-t" class="{cls}" style="{style}">{txt}</div></div>'


def plus_bars(id_, x, y, size, color=GOLD):
    """Le « + » en deux SVG superposés (barre à plat, barre penchée) pour pouvoir le tracer."""
    st = f"left:{x}px;top:{y}px;width:{size*1.04:.0f}px;height:{size}px;fill:{color}"
    h, v = PLUS_PTS.split("/>", 1)
    return (f'<svg id="{id_}-h" class="a" style="{st}" viewBox="-2 0 104 100">{h}/></svg>'
            f'<svg id="{id_}-v" class="a" style="{st}" viewBox="-2 0 104 100">{v}</svg>')


def clock_anim(id_, cx, cy, r):
    s = 2 * r + 40
    c = s / 2
    arc_len = 3.14159 * r
    circ = 2 * 3.14159 * r
    return (f'<svg id="{id_}" class="a" style="left:{cx - c:.0f}px;top:{cy - c:.0f}px;width:{s}px;height:{s}px" viewBox="0 0 {s} {s}">'
            f'<circle id="{id_}-c" cx="{c}" cy="{c}" r="{r}" fill="none" stroke="rgba(244,241,236,0.18)" stroke-width="4" '
            f'stroke-dasharray="{circ:.1f}" transform="rotate(-90 {c} {c})"/>'
            f'<path id="{id_}-a" d="M {c} {c - r} A {r} {r} 0 0 1 {c} {c + r}" fill="none" stroke="{GOLD}" stroke-width="{max(8, r*0.16):.0f}" '
            f'stroke-dasharray="{arc_len:.1f}"/>'
            f'<g id="{id_}-n"><line x1="{c}" y1="{c}" x2="{c}" y2="{c - r + r*0.28:.0f}" stroke="{GOLD}" stroke-width="{max(6, r*0.1):.0f}"/></g>'
            f'<circle cx="{c}" cy="{c}" r="{max(6, r*0.12):.0f}" fill="{GOLD}"/></svg>'), circ, arc_len, c


def relief_anim(id_, x, y, size, depth_color, layers=12):
    lay = "".join(
        f'<div aria-hidden="true" data-layout-ignore style="position:absolute;left:0;top:0;transform:translateZ({-i*3.5:.1f}px);color:{depth_color}">3D</div>'
        for i in range(layers, 0, -1))
    return (f'<div class="a" style="left:{x}px;top:{y}px;perspective:1600px">'
            f'<div id="{id_}" style="position:relative;transform-style:preserve-3d;font-weight:900;font-size:{size}px;line-height:.86;letter-spacing:-.02em">'
            f'{lay}<div style="position:relative">3D</div></div></div>')


def bands_volet(id_):
    """Volet 3 bandes plein cadre : bandes #222 aux bords coupés à 0,42, filet or sur le bord d'attaque."""
    out = []
    bh = H // 3
    d = round(0.42 * bh)
    for i in range(3):
        out.append(
            f'<div id="{id_}-b{i}" class="a" style="left:0;top:{i*bh}px;width:1700px;height:{bh}px">'
            f'<div style="position:absolute;inset:0;background:var(--surface);clip-path:polygon({d}px 0,100% 0,calc(100% - {d}px) 100%,0 100%)"></div>'
            f'<div style="position:absolute;inset:0;background:var(--gold);clip-path:polygon(calc(100% - 7px) 0,100% 0,calc(100% - {d}px) 100%,calc(100% - {d + 7}px) 100%)"></div></div>')
    return "".join(out)


def bands_volet_js(id_, t):
    """Couvre l'écran pour la coupe à t (couverture complète à t), puis découvre."""
    return "\n".join(
        f'      tl.fromTo("#{id_}-b{i}", {{ x: -1750 }}, {{ x: -310, duration: 0.22, ease: "power3.in" }}, {t - 0.32 + 0.05*i:.3f});\n'
        f'      tl.fromTo("#{id_}-b{i}", {{ x: -310 }}, {{ x: 1150, duration: 0.22, ease: "power3.out", immediateRender: false }}, {t + 0.02 + 0.05*i:.3f});'
        for i in range(3))


def subcomp(cid, dur, inner, js, ground=True, h=None):
    h = h or H
    cls = ("fr" if ground else "fr ov") + (" p45" if h == 1350 else "")
    return f"""<!doctype html>
<html lang="fr">
  <head><meta charset="UTF-8" /></head>
  <body>
    <template id="{cid}-template">
      <style>
{CSS}
{EXTRA_CSS}
        #root {{ position: absolute; inset: 0; }}
      </style>
      <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{h}" data-duration="{dur:.3f}">
        <div id="{cid}-fond" class="{cls} clip" data-start="0" data-duration="{dur:.3f}" data-track-index="0">
{inner}
        </div>
      </div>
      <script>
{JS_HELPERS}
{js}
      window.__timelines["{cid}"] = tl;
      </script>
    </template>
  </body>
</html>
"""


# ─────────────────────────── Scènes du concept A ───────────────────────────

def scene_A1(T):
    d = T["s"][1] - T["s"][0]
    inner = (f'<div id="a1-stage" class="layer" style="transform-origin:540px 700px">'
             f'<div id="a1-title" class="layer" style="transform-origin:108px 690px">'
             + F.lines(108, 470, [("disp", "PASSEZ EN", ""), ("disp", "VERSION", ""), ("disp", "PREMIUM.", "")]) + '</div>'
             f'<div id="a1-plus" class="layer" style="transform-origin:865px 755px">{F.plus(745, 640, 230)}</div>'
             f'<div id="a1-trait" class="layer">{F.trait(108, 925, 600)}</div></div>')
    js = f"""
      // Image 0 : titre et « + » déjà posés (frappe lancée à −0,35 s), jamais d'opacité
      tl.fromTo("#a1-title", {{ scale: 1.06 }}, {{ scale: 1, duration: 0.35, ease: "power2.out" }}, 0);
      tl.fromTo("#a1-plus", {{ scale: 1.16, rotation: -6 }}, {{ scale: 1, rotation: 0, duration: 0.3, ease: "power3.out" }}, 0);
      tl.fromTo("#a1-stage", {{ scale: 1 }}, {{ scale: 1.03, duration: {d:.3f}, ease: "none" }}, 0);
      wipe("#a1-trait", {T["premium"]:.3f}, 0.25);"""
    return d, inner, js


def scene_A2(T):
    t0, d = T["s"][1], T["s"][2] - T["s"][1]
    u = lambda g: g - t0  # noqa: E731
    clock, circ, arc, c = clock_anim("a2-clock", 760, 640, 92)
    inner = (
        f'<div id="a2-b1" class="layer"><div id="a2-b1c" class="layer">{F.panel()}'
        f'<div id="a2-lab" class="layer">{F.lab(108, 498, F.num("01", FONTAINE))}</div></div></div>'
        f'<div id="a2-b2" class="layer">{F.bande(72, 644, 936, 160, "02", "ANALYSE 3D")}</div>'
        f'<div id="a2-b3" class="layer">{F.bande(72, 828, 936, 160, "03", "SALLE DE POSING", " <span class=\"muted\">· BIENTÔT</span>")}</div>'
        f'{clock}'
        + mask("a2-g1", 108, 790, "disp", "UNE BOISSON", "font-size:140px")
        + mask("a2-g2a", 108, 740, "h1", "TOUTES LES")
        + mask("a2-g2b", 108, 841, "disp", '<span class="gold">30 MINUTES.</span>', "font-size:140px"))
    js = f"""
      // Le trait ouvre l'écran en 3 bandes (01, 02, 03), décalées de 0,06 s
      tl.fromTo("#a2-b1", {{ x: -560 }}, {{ x: 0, duration: 0.2, ease: "power3.out" }}, 0);
      tl.fromTo("#a2-b2", {{ x: -700 }}, {{ x: 0, duration: 0.2, ease: "power3.out" }}, 0.0);
      tl.fromTo("#a2-b3", {{ x: -840 }}, {{ x: 0, duration: 0.2, ease: "power3.out" }}, 0.0);
      // La bande 01 s'ouvre, 02 et 03 sortent
      tl.fromTo("#a2-b1c", {{ clipPath: "inset(460px 0px 1300px 0px)" }}, {{ clipPath: "inset(460px 0px 930px 0px)", duration: 0.26, ease: "power3.out" }}, 0.469);
      tl.fromTo("#a2-lab", {{ y: 19 }}, {{ y: 0, duration: 0.26, ease: "power3.out" }}, 0.469);
      tl.fromTo("#a2-b2", {{ x: 0 }}, {{ x: 1150, duration: 0.2, ease: "power3.in", immediateRender: false }}, 0.469);
      tl.fromTo("#a2-b3", {{ x: 0 }}, {{ x: 1150, duration: 0.2, ease: "power3.in", immediateRender: false }}, 0.5);
      // Horloge : cercle tracé, puis demi-tour or pendant « 30 MINUTES »
      show("#a2-clock", 0.62);
      tl.fromTo("#a2-clock-c", {{ strokeDashoffset: {circ:.1f} }}, {{ strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }}, 0.62);
      tl.fromTo("#a2-clock-a", {{ strokeDashoffset: {arc:.1f} }}, {{ strokeDashoffset: 0, duration: 0.9, ease: "none" }}, {u(T["p5_2"]):.3f});
      tl.fromTo("#a2-clock-n", {{ rotation: 0, svgOrigin: "{c} {c}" }}, {{ rotation: 180, svgOrigin: "{c} {c}", duration: 0.9, ease: "none" }}, {u(T["p5_2"]):.3f});
      // P5 : « UNE BOISSON » puis « TOUTES LES 30 MINUTES. »
      fall("#a2-g1-t", {u(T["p5_1"]):.3f});
      hide("#a2-g1", {u(T["p5_2"]):.3f});
      fall("#a2-g2a-t", {u(T["p5_2"]):.3f});
      fall("#a2-g2b-t", {u(T["p5_2"]) + 0.08:.3f});"""
    return d, inner, js


def scene_A3(T):
    t0, d = T["s"][2], T["s"][3] - T["s"][2]
    u = lambda g: g - t0  # noqa: E731
    inner = (F.panel() + F.lab(108, 498, F.num("02", "ANALYSE 3D")) +
             f'<div class="a body muted" style="left:108px;top:558px;font-size:32px">Analyse de composition corporelle</div>' +
             relief_anim("a3-rel", 660, 575, 200, CANVAS) +
             mask("a3-g1a", 108, 770, "h1", "UNE ANALYSE") + mask("a3-g1b", 108, 871, "h1", "EN 3D,") +
             mask("a3-g2a", 108, 770, "h1", "CHAQUE") + mask("a3-g2b", 108, 871, "h1", "SEMAINE.") +
             f'<div id="a3-etiq" class="layer">{F.lab(108, 1012, "<span class=\"gold\">1</span> ANALYSE 3D PAR SEMAINE")}</div>')
    js = f"""
      tl.fromTo("#a3-rel", {{ rotationY: -34, rotationX: 6 }}, {{ rotationY: -10, rotationX: 6, duration: {d:.3f}, ease: "none" }}, 0);
      fall("#a3-g1a-t", {u(T["p6_1"]):.3f}); fall("#a3-g1b-t", {u(T["p6_1"]) + 0.08:.3f});
      hide("#a3-g1a", {u(T["p6_2"]):.3f}); hide("#a3-g1b", {u(T["p6_2"]):.3f});
      fall("#a3-g2a-t", {u(T["p6_2"]):.3f}); fall("#a3-g2b-t", {u(T["p6_2"]) + 0.08:.3f});
      wipe("#a3-etiq", {u(T["etiq"]):.3f}, 0.24);"""
    return d, inner, js


def scene_A4(T):
    t0 = T["s"][3]
    d = COMMON["fin"] - t0
    inner = (F.panel() + F.lab(108, 498, F.num("03", "SALLE DE POSING")) +
             mask("a4-l1", 108, 600, "h1", "ARRIVE") +
             mask("a4-l2", 108, 717, "h1", '<span class="gold">TRÈS BIENTÔT.</span>') +
             f'<div id="a4-reflet" class="layer">{F.reflet(108, 834, "TRÈS BIENTÔT.")}</div>' +
             f'<div id="a4-faits" class="layer">{F.lab(108, 1012, "MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES", 36, "label muted")}</div>')
    js = """
      fall("#a4-l1-t", 0.03); fall("#a4-l2-t", 0.12);
      drop("#a4-reflet", 0.26, 0.26);
      wipe("#a4-faits", 0.34, 0.24);"""
    return d, inner, js



# ─────────────────────────── Scènes du concept B ───────────────────────────

def scene_B1(T):
    d = T["s"][1]
    gf = F.gold_fill("BOISSON", 1.0)
    inner = (f'<div id="b1-stage" class="layer" style="transform-origin:540px 760px">'
             f'<div id="b1-plus" class="layer" style="transform-origin:878px 535px">{F.plus(790, 450, 170)}</div>'
             f'<div class="a" style="left:108px;top:660px">'
             f'<div class="disp" style="font-size:126px">VOTRE <span id="b1-bo" style="position:relative;display:inline-block">BOISSON'
             f'<span id="b1-fill" style="position:absolute;left:0;top:0;color:var(--gold)">BOISSON</span></span></div>'
             f'<div class="disp" style="font-size:126px">VOUS ATTEND.</div></div></div>')
    js = f"""
      tl.fromTo("#b1-plus", {{ scale: 1.16, rotation: -6 }}, {{ scale: 1, rotation: 0, duration: 0.3, ease: "power3.out" }}, 0);
      tl.fromTo("#b1-stage", {{ scale: 1 }}, {{ scale: 1.03, duration: {d:.3f}, ease: "none" }}, 0);
      // « BOISSON » se remplit d'or de bas en haut, bord net
      tl.fromTo("#b1-fill", {{ clipPath: "inset(100% 0% 0% 0%)" }}, {{ clipPath: "inset(40% 0% 0% 0%)", duration: 1.1, ease: "power1.inOut" }}, 0.1);"""
    return d, inner, js


def scene_B2(T):
    t0, d = T["s"][1], T["s"][2] - T["s"][1]
    u = lambda g: g - t0  # noqa: E731
    w = T["p4"]
    inner = (F.panel() + F.lab(108, 498, F.num("01", FONTAINE)) + F.ghost(560, 790, "01", 220) +
             mask("b2-w1", 108, 600, "h1", "COLLAGÈNE,") + mask("b2-w2", 108, 701, "h1", "MULTIVITAMINES,") +
             mask("b2-w3", 108, 600, "h1", "L-CARNITINE,") + mask("b2-w4", 108, 701, "h1", "BOOSTER…"))
    js = f"""
      fall("#b2-w1-t", {u(w[0]):.3f}); fall("#b2-w2-t", {u(w[1]):.3f});
      hide("#b2-w1", {u(w[2]):.3f}); hide("#b2-w2", {u(w[2]):.3f});
      fall("#b2-w3-t", {u(w[2]):.3f}); fall("#b2-w4-t", {u(w[3]):.3f});"""
    return d, inner, js


def scene_B3(T):
    t0, d = T["s"][2], T["s"][3] - T["s"][2]
    u = lambda g: g - t0  # noqa: E731
    sav = ["PASSION", "PASTÈQUE", "ICE TEA", "ANANAS", "MULTIFRUIT"]
    win = "".join(f'<div id="b3-s{i}" class="label" style="position:absolute;left:180px;top:0;color:var(--text)">{n}</div>' for i, n in enumerate(sav))
    inner = (F.panel() + F.lab(108, 498, F.num("01", FONTAINE)) +
             mask("b3-l1", 108, 600, "h1", "OU SIMPLEMENT") + mask("b3-l2", 108, 701, "disp", "DE L'EAU.") +
             f'<div class="a" style="left:108px;top:888px;width:560px;height:52px;overflow:hidden">'
             f'<div class="label muted" style="position:absolute;left:0;top:0">SAVEUR ·</div>{win}</div>')
    sv = T["saveurs"]
    js = [f'      fall("#b3-l1-t", {u(T["eau"][0]):.3f}); fall("#b3-l2-t", {u(T["eau"][1]):.3f});']
    for i in range(5):
        js.append(f'      tl.fromTo("#b3-s{i}", {{ yPercent: 130 }}, {{ yPercent: 0, duration: 0.14, ease: "power3.out" }}, {u(sv[i]):.3f});')
        if i < 4:
            js.append(f'      tl.fromTo("#b3-s{i}", {{ yPercent: 0 }}, {{ yPercent: -130, duration: 0.14, ease: "power3.in", immediateRender: false }}, {u(sv[i + 1]) - 0.01:.3f});')
    return d, inner, "\n".join(js)


def scene_B4(T):
    t0 = T["s"][3]
    d = COMMON["fin"] - t0
    u = lambda g: g - t0  # noqa: E731
    clock, circ, arc, c = clock_anim("b4-clock", 790, 640, 80)
    inner = (F.panel(72, 460, 936, 400) + F.lab(108, 498, F.num("01", FONTAINE)) + clock +
             mask("b4-g1", 108, 690, "disp", "UNE BOISSON", "font-size:132px") +
             mask("b4-g2a", 108, 620, "h1", "TOUTES LES") +
             mask("b4-g2b", 108, 721, "disp", '<span class="gold">30 MINUTES.</span>', "font-size:132px") +
             f'<div id="b4-b02" class="layer">{F.bande(72, 880, 936, 64, "02", "ANALYSE 3D", " <span class=\"muted\">· 1 PAR SEMAINE</span>", label_size=36, filet=False)}</div>'
             f'<div id="b4-b03" class="layer">{F.bande(72, 954, 936, 64, "03", "SALLE DE POSING", " <span class=\"muted\">· BIENTÔT</span>", label_size=36, filet=False)}</div>')
    js = f"""
      tl.fromTo("#b4-clock-c", {{ strokeDashoffset: {circ:.1f} }}, {{ strokeDashoffset: 0, duration: 0.3, ease: "power2.out" }}, 0.02);
      tl.fromTo("#b4-clock-a", {{ strokeDashoffset: {arc:.1f} }}, {{ strokeDashoffset: 0, duration: 0.9, ease: "none" }}, {u(T["p5_2"]):.3f});
      tl.fromTo("#b4-clock-n", {{ rotation: 0, svgOrigin: "{c} {c}" }}, {{ rotation: 180, svgOrigin: "{c} {c}", duration: 0.9, ease: "none" }}, {u(T["p5_2"]):.3f});
      fall("#b4-g1-t", {u(T["p5_1"]):.3f});
      hide("#b4-g1", {u(T["p5_2"]):.3f});
      fall("#b4-g2a-t", {u(T["p5_2"]):.3f}); fall("#b4-g2b-t", {u(T["p5_2"]) + 0.08:.3f});
      tl.fromTo("#b4-b02", {{ x: -1120 }}, {{ x: 0, duration: 0.22, ease: "power3.out" }}, {u(T["b02"]):.3f});
      tl.fromTo("#b4-b03", {{ x: -1120 }}, {{ x: 0, duration: 0.22, ease: "power3.out" }}, {u(T["b03"]):.3f});"""
    return d, inner, js


# ─────────────────────────── Scènes du concept C ───────────────────────────

def scene_C1(T):
    d = T["s"][1]
    inner = (f'<div id="c1-stage" class="layer" style="transform-origin:540px 760px">'
             + relief_anim("c1-rel", 108, 450, 330, "#222222")
             + f'<div id="c1-plus" class="layer" style="transform-origin:878px 555px">{F.plus(790, 470, 170)}</div>'
             + F.lines(108, 770, [("disp", "VOS PROGRÈS,", "font-size:140px"), ("disp", "EN 3D.", "font-size:140px")]) + '</div>')
    js = f"""
      tl.fromTo("#c1-rel", {{ rotationY: -30, rotationX: 6 }}, {{ rotationY: 4, rotationX: 6, duration: {d:.3f}, ease: "none" }}, 0);
      tl.fromTo("#c1-plus", {{ scale: 1.16, rotation: -6 }}, {{ scale: 1, rotation: 0, duration: 0.3, ease: "power3.out" }}, 0);
      tl.fromTo("#c1-stage", {{ scale: 1 }}, {{ scale: 1.03, duration: {d:.3f}, ease: "none" }}, 0);"""
    return d, inner, js


def scene_C2(T):
    t0, d = T["s"][1], T["s"][2] - T["s"][1]
    u = lambda g: g - t0  # noqa: E731
    inner = (F.panel() + F.lab(108, 498, F.num("01", "ANALYSE 3D")) +
             f'<div class="a body muted" style="left:108px;top:558px;font-size:32px">Analyse de composition corporelle</div>' +
             relief_anim("c2-rel", 660, 575, 200, CANVAS) +
             mask("c2-g1a", 108, 770, "h1", "UNE ANALYSE") + mask("c2-g1b", 108, 871, "h1", "EN 3D,") +
             mask("c2-g2a", 108, 770, "h1", "CHAQUE") + mask("c2-g2b", 108, 871, "h1", "SEMAINE.") +
             f'<div id="c2-etiq" class="layer">{F.lab(108, 1012, "<span class=\"gold\">1</span> ANALYSE 3D PAR SEMAINE")}</div>')
    js = f"""
      tl.fromTo("#c2-rel", {{ rotationY: -34, rotationX: 6 }}, {{ rotationY: -6, rotationX: 6, duration: {d:.3f}, ease: "none" }}, 0);
      fall("#c2-g1a-t", {u(T["p6_1"]):.3f}); fall("#c2-g1b-t", {u(T["p6_1"]) + 0.08:.3f});
      hide("#c2-g1a", {u(T["p6_2"]):.3f}); hide("#c2-g1b", {u(T["p6_2"]):.3f});
      fall("#c2-g2a-t", {u(T["p6_2"]):.3f}); fall("#c2-g2b-t", {u(T["p6_2"]) + 0.08:.3f});
      wipe("#c2-etiq", {u(T["etiq"]):.3f}, 0.24);"""
    return d, inner, js


def scene_C3(T):
    t0, d = T["s"][2], T["s"][3] - T["s"][2]
    inner = (f'<div id="c3-stage" class="layer" style="transform-origin:400px 760px">' + F.panel() + F.lab(108, 498, F.num("02", "SALLE DE POSING")) +
             mask("c3-l1", 108, 600, "h1", "ARRIVE") +
             mask("c3-l2", 108, 717, "h1", '<span class="gold">TRÈS BIENTÔT.</span>') +
             f'<div id="c3-reflet" class="layer">{F.reflet(108, 834, "TRÈS BIENTÔT.")}</div>' +
             f'<div id="c3-faits" class="layer">{F.lab(108, 1012, "MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES", 36, "label muted")}</div></div>')
    js = f"""
      fall("#c3-l1-t", 0.05); fall("#c3-l2-t", 0.16);
      drop("#c3-reflet", 0.34, 0.3);
      wipe("#c3-faits", 0.5, 0.24);
      tl.fromTo("#c3-stage", {{ scale: 1 }}, {{ scale: 1.025, duration: {d:.3f}, ease: "none" }}, 0);"""
    return d, inner, js


def scene_C4(T):
    t0 = T["s"][3]
    d = COMMON["fin"] - t0
    clock, circ, arc, c = clock_anim("c4-clock", 880, 890, 66)
    inner = (f'<div id="c4-b" class="layer">{F.bande(72, 600, 936, 190, "03", FONTAINE)}</div>' +
             f'<div id="c4-lab" class="layer">{F.lab(108, 868, "<span class=\"gold\">1</span> BOISSON TOUTES LES 30" + NB + "MIN")}</div>' + clock)
    js = f"""
      tl.fromTo("#c4-b", {{ x: -560 }}, {{ x: 0, duration: 0.18, ease: "power3.out" }}, 0);
      wipe("#c4-lab", 0.3, 0.24);
      show("#c4-clock", 0.3);
      tl.fromTo("#c4-clock-c", {{ strokeDashoffset: {circ:.1f} }}, {{ strokeDashoffset: 0, duration: 0.25, ease: "power2.out" }}, 0.3);
      tl.fromTo("#c4-clock-a", {{ strokeDashoffset: {arc:.1f} }}, {{ strokeDashoffset: 0, duration: 0.45, ease: "none" }}, 0.45);
      tl.fromTo("#c4-clock-n", {{ rotation: 0, svgOrigin: "{c} {c}" }}, {{ rotation: 180, svgOrigin: "{c} {c}", duration: 0.45, ease: "none" }}, 0.45);"""
    return d, inner, js


# ─────────────────────────── Éléments communs ───────────────────────────

def comp_pastille():
    d = COMMON["fin"]
    inner = f'<div id="pa-p" class="layer">{F.pastille(y=CUR["PAST_Y"])}</div>'
    js = """
      wipe("#pa-p", 0.3, 0.24);"""
    return d, inner, js


def comp_mentions():
    d = END - (COMMON["mentions"] - 0.175)
    bas = CUR["MENT_Y"] + 200
    inner = (f'<div class="layer" style="clip-path:inset(0px 0px {H - bas}px 0px)">'
             f'<div id="me-p" class="layer">{F.mention(CUR["MENT_Y"])}</div></div>')
    js = f"""
      // Le panneau monte depuis sous y {bas} (masque fixe) et finit en place à 9,375 s
      tl.fromTo("#me-p", {{ y: 220 }}, {{ y: 0, duration: 0.175, ease: "power3.out" }}, 0);"""
    return d, inner, js


def comp_volet(t_cut):
    return 0.66, bands_volet("vo"), bands_volet_js("vo", 0.32)


def comp_fin():
    t0 = COMMON["fin"]
    d = END - t0
    u = lambda g: g - t0  # noqa: E731
    C = COMMON
    qual = [("qual", "LES 4 PREMIÈRES SEMAINES DE L'OPTION", "font-size:40px"),
            ("qual", f"PUIS 2{NB}€ TTC/SEM. (8{NB}€ TOUTES LES 4{NB}SEM.)", "font-size:40px"),
            ("qual", "EN PLUS DE VOTRE ABONNEMENT", "font-size:40px")]
    inner = stage(dy=CUR["DY_FIN"], inner=
        # cassure et offre
        f'<div id="fi-stage" class="layer">'
        f'<div id="fi-cas" class="layer" style="transform-origin:108px 740px">{F.lines(108, 600, [("disp", "ET EN CE", ""), ("disp", "MOMENT…", "")])}</div>'
        f'<div id="fi-lab" class="layer">{F.lab(108, 420, "EN CE MOMENT", 44, "label muted")}</div>'
        + mask("fi-g1a", 108, 520, "h1", "LES 4 PREMIÈRES")
        + f'<div id="fi-g1b" class="layer" style="transform-origin:108px 690px">{F.lines(108, 621, [("disp", "SEMAINES", "")])}</div>'
        + mask("fi-g2a", 108, 520, "h1", "DE L'OPTION") + mask("fi-g2b", 108, 621, "disp", "PREMIUM")
        + f'<div id="fi-g3" class="layer">'
        + F.lines(108, 520, [("h1", "SONT", "")])
        + f'<div id="fi-off" class="layer" style="transform-origin:108px 690px">{F.lines(108, 621, [("disp", "<span class=\"gold\">OFFERTES.</span>", "")])}</div>'
        + f'<div id="fi-trait" class="layer">{F.trait(108, 785, 650)}</div>'
        + F.lines(108, 815, qual) + '</div></div>'
        # prix
        + f'<div id="fi-prix" class="layer" style="background:var(--canvas)">'
        + F.lab(108, 440, "PUIS", None, "h2 muted") + plus_bars("fi-plus", 108, 548, 190)
        + f'<div id="fi-2e" class="layer" style="transform-origin:420px 640px"><div class="a disp num" style="left:330px;top:514px;font-size:250px">2{NB}€</div></div>'
        + F.lab(108, 752, "TTC PAR SEMAINE", None, "h2")
        + F.lines(108, 846, [("qual", f"SOIT 8{NB}€ TOUTES LES 4{NB}SEM.", "font-size:40px"), ("qual", "EN PLUS DE VOTRE ABONNEMENT", "font-size:40px")])
        + F.lab(108, 960, RAPPEL, 38, "label muted") + '</div>'
        # carte finale
        + f'<div id="fi-carte" class="layer" style="background:var(--canvas)">'
        + "".join(f'<div id="fi-logo{k}" class="layer" style="clip-path:inset({330 + k*57.3:.1f}px 0px {1920 - 330 - (k+1)*57.3:.1f}px 0px)">'
                  f'<div class="a" role="img" aria-label="LA SALLE" style="left:108px;top:330px;width:280px;height:171.3px;'
                  f'background:url(assets/img/logo-negatif-provisoire.png) 0 0 / 100% 100% no-repeat"></div></div>' for k in range(3))
        + f'<div id="fi-op" class="layer">{F.lab(108, 626, "OPTION PREMIUM", 40, "label muted")}</div>'
        + f'<div id="fi-ctap" class="layer" style="transform-origin:150px 768px">{F.plus(108, 726, 84)}</div>'
        + mask("fi-cta", 216, 734, "label", "ACTIVEZ-LA À L'ACCUEIL", "font-size:68px")
        + mask("fi-sec", 108, 856, "h2", "EN QUELQUES SECONDES.") + '</div>') + (
        # volets internes
        f'<div id="fi-v1" class="layer">{bands_volet("fv1")}</div><div id="fi-v2" class="layer">{bands_volet("fv2")}</div>')
    js = f"""
      // Cassure : « ET EN CE MOMENT… » seul, en coupe sèche
      tl.fromTo("#fi-cas", {{ scale: 1.05 }}, {{ scale: 1, duration: 0.2, ease: "power2.out" }}, 0);
      hide("#fi-cas", {u(C["g25_1"]):.3f});
      show("#fi-lab", {u(C["g25_1"]):.3f});
      // Réplique 25, 4 mots au plus à la fois
      fall("#fi-g1a-t", {u(C["g25_1"]):.3f});
      slam("#fi-g1b", {u(C["drop"]):.3f});
      shake("#fi-stage", {u(C["drop"]):.3f});
      hide("#fi-g1a", {u(C["g25_2"]):.3f}); hide("#fi-g1b", {u(C["g25_2"]):.3f});
      fall("#fi-g2a-t", {u(C["g25_2"]):.3f}); fall("#fi-g2b-t", {u(C["g25_2"]) + 0.06:.3f});
      hide("#fi-g2a", {u(C["g25_3"]):.3f}); hide("#fi-g2b", {u(C["g25_3"]):.3f});
      // « OFFERTES. » et sa condition complète dans la même image
      show("#fi-g3", {u(C["g25_3"]):.3f});
      tl.fromTo("#fi-off", {{ scale: 1.22 }}, {{ scale: 1, duration: 0.16, ease: "power4.out" }}, {u(C["g25_3"]):.3f});
      wipe("#fi-trait", {u(C["g25_3"]) + 0.1:.3f}, 0.25);
      // Volet → prix (sans voix) : le prix et ses qualificatifs dans la même image ; le « + » se trace, « 2 € » frappe
{bands_volet_js("fv1", u(C["prix"]))}
      show("#fi-prix", {u(C["prix"]):.3f}); hide("#fi-g3", {u(C["prix"]):.3f}); hide("#fi-lab", {u(C["prix"]):.3f});
      tl.fromTo("#fi-plus-h", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.16, ease: "power2.out" }}, {u(C["prix"]) + 0.1:.3f});
      tl.fromTo("#fi-plus-v", {{ clipPath: "inset(0% 0% 100% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.16, ease: "power2.out" }}, {u(C["prix"]) + 0.18:.3f});
      slam("#fi-2e", {u(C["prix"]) + 0.23:.3f}, 1.3);
      // Volet → carte finale : le monogramme s'assemble par ses 3 bandes
{bands_volet_js("fv2", u(C["carte"]))}
      show("#fi-carte", {u(C["carte"]):.3f}); hide("#fi-prix", {u(C["carte"]):.3f}); hide("#fi-2e", {u(C["carte"]):.3f});
      tl.fromTo("#fi-logo0", {{ x: -260 }}, {{ x: 0, duration: 0.24, ease: "power3.out" }}, {u(C["carte"]) + 0.04:.3f});
      tl.fromTo("#fi-logo1", {{ x: 260 }}, {{ x: 0, duration: 0.24, ease: "power3.out" }}, {u(C["carte"]) + 0.10:.3f});
      tl.fromTo("#fi-logo2", {{ x: -260 }}, {{ x: 0, duration: 0.24, ease: "power3.out" }}, {u(C["carte"]) + 0.16:.3f});
      wipe("#fi-op", {u(C["carte"]) + 0.4:.3f}, 0.24);
      slam("#fi-ctap", {u(C["p9_1"]):.3f}, 1.35);
      fall("#fi-cta-t", {u(C["p9_1"]) + 0.04:.3f});
      fall("#fi-sec-t", {u(C["p9_2"]):.3f});"""
    return d, inner, js


SFX_GAIN = 1.0   # SFX_VOIX avec --voix
SFX_COURTS = {}  # avec --voix : {fichier: (durée, fondu de sortie)}, pour que la traîne des impacts (2 s) ne couvre pas la voix
ZONES_VOIX = []  # avec --voix : (début, fin) de chaque réplique ; un bruitage qui tombe dessus est baissé de 6 dB


def sfx(n, src, start, vol, dur=None, media_start=None):
    fo = ""
    if dur is None and os.path.basename(src) in SFX_COURTS:
        dur, f = SFX_COURTS[os.path.basename(src)]
        fo = f' data-fade-out="{f:.2f}"'
    if any(a < start + (dur or 0.5) and start < b for a, b in ZONES_VOIX):
        vol *= 0.5
    ms = f' data-media-start="{media_start:.3f}"' if media_start is not None else ""
    du = f' data-duration="{dur:.3f}"' if dur is not None else ""
    return (f'      <audio id="sfx-{n}" src="{src}" data-audio-group="sfx" data-start="{start:.3f}"{du}{ms}{fo} '
            f'data-track-index="{30 + int(n)}" data-volume="{round(vol * SFX_GAIN, 3)}"></audio>')


def sfx_list(concept, T):
    C = COMMON
    S = ".media/audio/sfx/"
    ev = [(S + "sfx_002.mp3", 0.0, 0.35), (S + "sfx_006.mp3", 0.3, 0.3)]          # impact image 0 · pop pastille
    if concept == "A":
        ev += [(S + "sfx_001.mp3", T["s"][1] - 0.02, 0.35), (S + "sfx_003.mp3", T["s"][1] + 0.469, 0.3),
               (S + "sfx_003.mp3", T["etiq"], 0.3), (S + "sfx_005.mp3", T["s"][3] + 0.26, 0.18)]
    if concept == "B":
        ev += [(S + "sfx_003.mp3", t, 0.22) for t in T["p4"]] + [(S + "sfx_003.mp3", t, 0.18) for t in T["saveurs"]]
        ev += [(S + "sfx_001.mp3", T["b02"], 0.3), (S + "sfx_001.mp3", T["b03"], 0.3)]
    if concept == "C":
        ev += [(S + "sfx_003.mp3", T["etiq"], 0.3), (S + "sfx_005.mp3", T["s"][2] + 0.34, 0.18), (S + "sfx_001.mp3", T["s"][3], 0.3)]
    ev += [(S + "sfx_001.mp3", t - 0.3, 0.35) for t in T["volets"]]                 # whoosh : volets
    out = [sfx(i + 1, *e) for i, e in enumerate(ev)]
    n = len(out)
    out += [
        sfx(n + 1, S + "sfx_004.mp3", C["g25_1"], 0.32, dur=C["drop"] - C["g25_1"], media_start=10.032 - (C["drop"] - C["g25_1"])),
        sfx(n + 2, S + "sfx_002.mp3", C["drop"], 0.4), sfx(n + 3, S + "sfx_006.mp3", C["g25_3"], 0.3),
        sfx(n + 4, S + "sfx_001.mp3", C["prix"] - 0.3, 0.35), sfx(n + 5, S + "sfx_002.mp3", C["prix"] + 0.23, 0.35),
        sfx(n + 6, S + "sfx_001.mp3", C["carte"] - 0.3, 0.35), sfx(n + 7, S + "sfx_001.mp3", C["carte"] + 0.06, 0.25),
        sfx(n + 8, S + "sfx_002.mp3", C["p9_1"], 0.3)]
    return out


def index_html(concept, hosts, audios, voix=False):
    zs = "\n".join(f"      #h-{h[0]} {{ z-index: {h[4]}; }}" for h in hosts)
    fmt, res = CUR["LABEL"], CUR["RES"]
    hs = "\n".join(
        f'      <div id="h-{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
        f'data-start="{s:.3f}" data-duration="{d:.3f}" data-track-index="{ti}" data-width="{W}" data-height="{H}"></div>'
        for cid, s, d, ti, z in hosts)
    return f"""<!doctype html>
<html lang="fr" data-resolution="{res}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #0D0D0D; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #0D0D0D; }}
      [data-composition-id="main"] > div[data-composition-src] {{ position: absolute; inset: 0; }}
{zs}
    </style>
  </head>
  <body>
    <!-- Option Premium LA SALLE · concept {concept} · {fmt} · 15 s · 128 BPM{" · voix « ton pub »" if voix else ""}. Généré par _sources-premium/tools/video.py -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="{W}" data-height="{H}" data-fps="30">
{hs}
{audios}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


SCENES = {"A": [scene_A1, scene_A2, scene_A3, scene_A4], "B": [scene_B1, scene_B2, scene_B3, scene_B4],
          "C": [scene_C1, scene_C2, scene_C3, scene_C4]}


def build(concept, voix=False):
    T, pistes = TIMING[concept], []
    if voix:
        T, C, pistes = timing_voix(concept)
        COMMON.update(C)
        ZONES_VOIX[:] = [(st, st + d) for _, st, d in pistes]
    root = os.path.join(MD, CUR["DIR"], concept)
    comp = os.path.join(root, "compositions")
    os.makedirs(comp, exist_ok=True)
    hosts = []
    for i, fn in enumerate(SCENES[concept]):
        d, inner, js = fn(T)
        inner = stage(inner)
        cid = f"s{i + 1:02d}"
        open(os.path.join(comp, f"{cid}.html"), "w", encoding="utf-8").write(subcomp(cid, d, inner, js))
        hosts.append((cid, T["s"][i], d, 1, i + 1))
    d, inner, js = comp_fin()
    open(os.path.join(comp, "fin-commune.html"), "w", encoding="utf-8").write(subcomp("fin-commune", d, inner, js))
    hosts.append(("fin-commune", COMMON["fin"], d, 1, 5))
    for f in os.listdir(comp):  # volets d'un minutage précédent (B voix n'en a qu'un)
        if f.startswith("volet-"):
            os.remove(os.path.join(comp, f))
    for k, t in enumerate(T["volets"]):
        d, inner, js = comp_volet(t)
        cid = f"volet-{k + 1}"
        open(os.path.join(comp, f"{cid}.html"), "w", encoding="utf-8").write(subcomp(cid, d, inner, js, ground=False))
        hosts.append((cid, t - 0.32, d, 2, 25))
    d, inner, js = comp_pastille()
    open(os.path.join(comp, "pastille.html"), "w", encoding="utf-8").write(subcomp("pastille", d, inner, js, ground=False))
    hosts.append(("pastille", 0.0, d, 3, 30))
    d, inner, js = comp_mentions()
    open(os.path.join(comp, "mentions.html"), "w", encoding="utf-8").write(subcomp("mentions", d, inner, js, ground=False))
    hosts.append(("mentions", COMMON["mentions"] - 0.175, d, 4, 40))
    audios = "\n".join(sfx_list(concept, T) + ([voix_audio(pistes)] if voix else []))
    open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(index_html(concept, hosts, audios, voix))
    json.dump({"concept": concept, "format": f"{W}x{H}", "timing": T, "common": COMMON, "end": END,
               "voix": [{"replique": n, "start": st, "duree": d} for n, st, d in pistes]},
              open(os.path.join(root, "timing.json"), "w"), ensure_ascii=False, indent=2)
    print("construit", root, len(hosts), "sous-compositions")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--45" in args:
        args.remove("--45")
        set_format("45")
    voix = "--voix" in args
    if voix:
        args.remove("--voix")
        SFX_GAIN = SFX_VOIX
        SFX_COURTS = {"sfx_002.mp3": (0.8, 0.5)}
    for c in args or ["A"]:
        build(c, voix)
