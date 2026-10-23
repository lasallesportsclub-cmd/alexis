"""Écrit les 6 cadres de la pub « Vos questions » v2 (sans avis Google : cadres 3 « cours » et 4 « essai ») (compositions/frames/NN-*.html) à partir de STORYBOARD.md.

Un cadre = un fragment <template> HyperFrames : racine #root avec data-composition-id = frame_id, calques
« clip » plein cadre minutés en secondes locales, une seule timeline GSAP en pause enregistrée dans
window.__timelines[frame_id]. Composants partagés (classes lsq-) et polices : frame.md. Instants : tools/cues.json.
Aucune opacité animée, aucun fondu (charte) : les coupes viennent des fenêtres des calques, les entrées
d'échelles, de glissements masqués et de clip-path.

Usage : python3 tools/cadres.py
"""
import os
import re

ICI = os.path.dirname(os.path.abspath(__file__))
PROJET = os.path.normpath(os.path.join(ICI, ".."))
SORTIE = os.path.join(PROJET, "compositions", "frames")
NB = " "                                   # espace insécable (« ? », « 1 200 m² », guillemets)

# polices et composants partagés, copiés de frame.md
FRAME_MD = open(os.path.join(PROJET, "frame.md"), encoding="utf-8").read()
POLICES = re.search(r"<style>\n(@font-face.*?)</style>", FRAME_MD, re.S).group(1)
COMPOSANTS = re.search(r"```css\n(.*?)```", FRAME_MD, re.S).group(1)

CSS_COMMUN = POLICES + """
#root{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}
.clip{position:absolute;left:0;top:0;width:1080px;height:1920px}
""" + COMPOSANTS + """
.lsq-q.l1{height:120px;--coupe:50px;white-space:nowrap}
.lsq-q.l2{height:180px;--coupe:76px}
.lsq-q,.lsq-r,.lsq-avis{box-sizing:border-box}
.lsq-r{padding-top:36px}
.lsq-masque{display:block;overflow:hidden}
.lsq-entete{position:absolute;left:108px;top:300px;height:52px;display:flex;align-items:center;gap:18px}
.lsq-entete-mono{width:76px;height:44px;background:url("assets/img/mono.png") 0 0/76px 44px no-repeat}
.lsq-entete-nom{font:italic 800 38px/1 "Barlow Condensed";letter-spacing:0.05em;text-transform:uppercase;color:#F4F1EC;white-space:nowrap}

.lsq-fond::after{content:"";position:absolute;inset:0;opacity:.7;mix-blend-mode:overlay;pointer-events:none;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='256' height='256'><filter id='n' color-interpolation-filters='sRGB'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.lsq-masque>span{display:block}
.lsq-avis .lsq-etoiles svg path{fill:none;stroke:rgba(244,241,236,0.62);stroke-width:1.4}
.lsq-geante{position:absolute;top:860px;width:120px;height:44px;background:rgba(244,241,236,0.62);
  clip-path:polygon(18px 0,100% 0,calc(100% - 18px) 100%,0 100%)}
"""

ETOILE = ('<svg viewBox="0 0 24 24"><path d="M12 1.6l3.1 6.9 7.5.7-5.7 5 1.7 7.4L12 17.8l-6.6 3.8 '
          '1.7-7.4-5.7-5 7.5-.7z"/></svg>')

# Aides GSAP communes, placées dans chaque cadre (portée locale : IIFE)
JS_AIDES = """
  const R = (id) => document.getElementById("f" + ID + "-" + id);
  const OR = "#B8A07E", GRIS = "rgba(244,241,236,0.62)";
  // zoom avant lent d'une photo de fond sur toute sa fenêtre
  const zoom = (id, t, d, de = 1.0, a = 1.06) =>
    tl.fromTo(R(id), { scale: de }, { scale: a, duration: d, ease: "none" }, t);
  // bulle de la cliente : monte de 40 px, échelle 0,92 → 1
  const question = (t) => tl.fromTo(R("q"), { y: 40, scale: 0.92 }, { y: 0, scale: 1, duration: 0.18, ease: "power3.out" }, t);
  // indicateur de saisie : la bulle s'ouvre, puis 3 barres s'allument en or en doubles croches
  const saisie = (t, prefixe = "s") => {
    if (R(prefixe)) tl.fromTo(R(prefixe), { scale: 0.6 }, { scale: 1, duration: 0.1, ease: "power3.out" }, t);
    [0, 1, 2].forEach((k) => {
      const b = R(prefixe + "-b" + k);
      tl.fromTo(b, { backgroundColor: GRIS, y: 0 }, { backgroundColor: OR, y: -8, duration: 0.05, ease: "power2.out" }, t + k * 0.125);
      tl.to(b, { y: 0, duration: 0.08, ease: "power2.in" }, t + k * 0.125 + 0.06);
    });
  };
  // réponse de LA SALLE : frappe d'échelle, le filet or se trace de bas en haut
  const reponse = (t) => {
    tl.fromTo(R("r"), { scale: 1.22 }, { scale: 1, duration: 0.22, ease: "power4.out" }, t);
    gsap.set(R("r-filet"), { skewX: -22.78, transformOrigin: "0% 100%" });
    tl.fromTo(R("r-filet"), { scaleY: 0 }, { scaleY: 1, duration: 0.2, ease: "power3.out" }, t);
  };
  // précision : glisse depuis le bas dans son masque
  const precision = (t) => tl.fromTo(R("p"), { yPercent: 110 }, { yPercent: 0, duration: 0.2, ease: "power3.out" }, t);
  // carte d'avis : frappe, puis les 5 étoiles s'allument une par une en doubles croches
  const avis = (t) => {
    tl.fromTo(R("a"), { scale: 1.1, y: 30 }, { scale: 1, y: 0, duration: 0.22, ease: "power4.out" }, t);
    [0, 1, 2, 3, 4].forEach((k) => {
      const e = R("e" + k);
      tl.fromTo(e.querySelector("path"), { fill: "rgba(0,0,0,0)", stroke: GRIS }, { fill: OR, stroke: OR, duration: 0.03, ease: "none" }, t + k * 0.125);
      tl.fromTo(e, { scale: 1.5 }, { scale: 1, duration: 0.15, ease: "power3.out" }, t + k * 0.125);
    });
  };
"""


def calque(id_, debut, duree, piste, contenu, extra=""):
    return (f'<div id="f{id_}" class="clip"{extra} data-start="{debut:g}" data-duration="{duree:g}" '
            f'data-track-index="{piste}">{contenu}</div>')


VOILE_FORT = {"fond-tapis", "fond-tapis-detail"}     # murs et fenêtres clairs : voile à 52 % au lieu de 42 %


def fond(fid, nom, debut, duree, photo):
    """Calque de fond : photo assombrie par le voile, ou canevas nu si photo est None."""
    img = f'<img id="f{fid}-{nom}-img" src="assets/img/{photo}.jpg" alt="" />' if photo else ""
    style = ' style="background:rgba(13,13,13,0.52)"' if photo in VOILE_FORT else ""
    voile = f'<div class="lsq-voile"{style}></div>' if photo else ""
    return calque(f"{fid}-{nom}", debut, duree, 0, f'<div class="lsq-fond" data-layout-allow-overflow>{img}{voile}</div>')


def entete(fid, duree):
    """En-tête « LA SALLE · CONFLANS » (y 300–352), le même dans les cadres 1 à 5 : il paraît fixe aux coupes."""
    return calque(f"{fid}-ch", 0, duree, 1, '<div class="lsq-entete"><div class="lsq-entete-mono"></div>'
                  '<div class="lsq-entete-nom">LA SALLE · CONFLANS</div></div>')


def bulle_question(fid, texte, duree, lignes=1):
    return calque(f"{fid}-cq", 0, duree, 2, f'<div id="f{fid}-q" class="lsq-q l{lignes}">{texte}</div>')


def saisie(fid, debut, duree, top=700):
    barres = "".join(f'<i id="f{fid}-s-b{k}" style="left:{42 + 40 * k}px"></i>' for k in range(3))
    return calque(f"{fid}-cs", debut, duree, 3,
                  f'<div id="f{fid}-s" class="lsq-saisie" style="top:{top}px;transform-origin:100% 50%">{barres}</div>')


def reponse(fid, debut, duree, titre, prec, hauteur, taille=150, top=700):
    coupe = round(0.42 * hauteur)
    style = f"top:{top}px;height:{hauteur}px;--coupe:{coupe}px;transform-origin:100% 50%"
    if taille != 150:
        style += f";font-size:{taille}px;line-height:0.9"
    contenu = (f'<div id="f{fid}-r" class="lsq-r" style="{style}">'
               f'<div id="f{fid}-r-filet" class="lsq-filet"></div>{titre}'
               f'<span class="lsq-precision lsq-masque"><span id="f{fid}-p">{prec}</span></span></div>')
    return calque(f"{fid}-cr", debut, duree, 4, contenu)


def carte_avis(fid, debut, duree, texte, top=700):
    etoiles = "".join(ETOILE.replace("<svg ", f'<svg id="f{fid}-e{k}" ') for k in range(5))
    contenu = (f'<div id="f{fid}-a" class="lsq-avis" style="top:{top}px;transform-origin:50% 50%">'
               f'<div class="lsq-haut"><div class="lsq-etoiles">{etoiles}</div>'
               f'<div class="lsq-source">Avis Google</div></div>'
               f'<div class="lsq-texte"><span class="lsq-guillemet">«{NB}</span>{texte}'
               f'<span class="lsq-guillemet">{NB}»</span></div></div>')
    return calque(f"{fid}-ca", debut, duree, 4, contenu)


def ecrire(fid, duree, corps, script, css=""):
    html = f"""<template>
  <style>
{CSS_COMMUN}{css}
  </style>
  <div id="root" data-composition-id="{fid}" data-width="1080" data-height="1920" data-duration="{duree:g}">
    {corps}
  </div>
  <script src="assets/vendor/gsap.min.js"></script>
  <script>
  (function () {{
  const ID = "{fid}";
  const tl = gsap.timeline({{ paused: true }});
{JS_AIDES}
{script}
  window.__timelines = window.__timelines || {{}};
  window.__timelines[ID] = tl;
  }})();
  </script>
</template>
"""
    os.makedirs(SORTIE, exist_ok=True)
    with open(os.path.join(SORTIE, fid + ".html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(fid, f"{duree:g} s")


# ---------- 01 · Horaires (0,0 → 2,5 s) ----------
f = "01-horaires"
ecrire(f, 2.5, "\n    ".join([
    fond(f, "f1", 0, 1.0, "fond-facade"),
    fond(f, "f2", 1.0, 1.5, "fond-enseigne"),
    entete(f, 2.5),
    bulle_question(f, f"Vous ouvrez à quelle heure{NB}?", 2.5),
    saisie(f, 0.5, 0.5),
    reponse(f, 1.0, 1.5, f"6H{NB}–{NB}23H", "7J/7", 278),
]), """
  zoom("f1-img", 0, 1.0);
  zoom("f2-img", 1.0, 1.5);
  // image 0 : la question est déjà posée, simple tassement
  tl.fromTo(R("q"), { scale: 1.03 }, { scale: 1, duration: 0.12, ease: "power2.out" }, 0);
  saisie(0.5);
  reponse(1.0);
  precision(1.5);
""")

# ---------- 02 · Taille (2,5 → 5,0 s) ----------
f = "02-taille"
ecrire(f, 2.5, "\n    ".join([
    fond(f, "f1", 0, 1.0, "fond-tapis"),
    fond(f, "f2", 1.0, 1.0, "fond-halteres"),
    fond(f, "f3", 2.0, 0.5, "fond-halteres-detail"),
    entete(f, 2.5),
    bulle_question(f, f"C’est grand{NB}?", 2.5),
    saisie(f, 0.5, 0.5),
    reponse(f, 1.0, 1.5, f"1{NB}200{NB}<span style=\"text-transform:none\">m²</span>", f"MUSCULATION{NB}·{NB}CARDIO", 278),
]), """
  zoom("f1-img", 0, 1.0);
  zoom("f2-img", 1.0, 1.0);
  zoom("f3-img", 2.0, 0.5, 1.0, 1.03);
  question(0);
  saisie(0.5);
  reponse(1.0);
  precision(1.5);
""")

# ---------- 03 · Cours (5,0 → 7,5 s) ----------
f = "03-cours"
ecrire(f, 2.5, "\n    ".join([
    fond(f, "f1", 0, 1.5, "fond-tapis-detail"),
    fond(f, "f2", 1.5, 1.0, "fond-halteres"),
    entete(f, 2.5),
    bulle_question(f, f"Et si je n’aime pas<br>la muscu{NB}?", 2.5, lignes=2),
    saisie(f, 0.5, 0.5, top=760),
    reponse(f, 1.0, 1.5, "COURS COLLECTIFS", f"BODYPUMP{NB}·{NB}RPM{NB}·{NB}PILATES", 240, taille=96, top=760),
]), """
  zoom("f1-img", 0, 1.5);
  zoom("f2-img", 1.5, 1.0, 1.0, 1.04);
  question(0);
  saisie(0.5);
  reponse(1.0);
  precision(1.5);
""")

# ---------- 04 · Essai (7,5 → 10,0 s) : cassure 0,5 → 1,0, drop à 1,0 ----------
f = "04-essai"
geante = "".join(f'<div id="f{f}-g-b{k}" class="lsq-geante" style="left:{320 + 160 * k}px"></div>' for k in range(3))
ecrire(f, 2.5, "\n    ".join([
    fond(f, "f1", 0, 0.5, "fond-facade"),
    fond(f, "f2", 0.5, 0.5, None),                     # cassure : canevas nu, sans fondu
    fond(f, "f3", 1.0, 1.0, "fond-enseigne"),
    fond(f, "f4", 2.0, 0.5, "fond-tapis"),
    entete(f, 2.5),
    bulle_question(f, f"Je peux essayer avant{NB}?", 2.5),
    calque(f"{f}-cg", 0.5, 0.5, 3, geante),
    reponse(f, 1.0, 1.5, "SÉANCE D’ESSAI", "OFFERTE À L’ACCUEIL", 240, taille=104),
]), """
  zoom("f1-img", 0, 0.5, 1.0, 1.03);
  // drop : le fond revient avec une frappe d'échelle, puis le zoom lent reprend
  tl.fromTo(R("f3-img"), { scale: 1.08 }, { scale: 1.0, duration: 0.3, ease: "power3.out" }, 1.0);
  tl.fromTo(R("f3-img"), { scale: 1.0 }, { scale: 1.03, duration: 0.7, ease: "none", immediateRender: false }, 1.3);
  zoom("f4-img", 2.0, 0.5, 1.0, 1.03);
  question(0);
  saisie(0.5, "g");                                 // saisie géante, en silence
  reponse(1.0);
  precision(1.5);
""")

# ---------- 05 · Invitation (10,0 → 12,0 s) + volet des 3 bandes ----------
f = "05-invitation"
# bandes : 1700 × 640, extrémités coupées à 0,42 (décalage 269 px), filet or sur le bord gauche ;
# couvrent tout le cadre quand left = −300 (handoff_out)
bandes = "".join(
    f'<div id="f{f}-b{k}" class="f{f}-bande" style="top:{640 * k}px">'
    f'<div class="f{f}-bande-fond"></div><div class="f{f}-bande-filet"></div></div>' for k in range(3))
css_bandes = f"""
.f{f}-bande{{position:absolute;left:0;width:1700px;height:640px}}
.f{f}-bande-fond{{position:absolute;inset:0;background:#222222;clip-path:polygon(269px 0,1700px 0,1431px 640px,0 640px)}}
.f{f}-bande-filet{{position:absolute;inset:0;background:#B8A07E;clip-path:polygon(269px 0,275px 0,6px 640px,0 640px)}}
"""
ecrire(f, 2.0, "\n    ".join([
    fond(f, "f1", 0, 2.0, "fond-halteres"),
    entete(f, 2.0),
    bulle_question(f, f"Je peux passer voir{NB}?", 2.0),
    saisie(f, 0.5, 0.5),
    reponse(f, 1.0, 1.0, "AVEC PLAISIR.", f"ON VOUS ATTEND{NB}!", 240, taille=104),
    calque(f"{f}-cb", 1.5, 0.5, 6, bandes),
]), """
  zoom("f1-img", 0, 2.0, 1.0, 1.05);
  question(0);
  saisie(0.5);
  reponse(1.0);
  precision(1.25);
  // volet : les bandes entrent par la droite et s'arrêtent (vitesse nulle) en couvrant tout le cadre à 2,0 s
  [0, 1, 2].forEach((k) => tl.fromTo(R("b" + k), { x: 1180 }, { x: -300, duration: 0.375, ease: "power2.out" }, 1.5 + k * 0.0625));
""", css_bandes)

# ---------- 06 · Carte finale (12,0 → 15,0 s) ----------
f = "06-carte"
bandes6 = bandes.replace("05-invitation", "06-carte")
css6 = css_bandes.replace("05-invitation", "06-carte") + f"""
.f{f}-mono{{position:absolute;left:370px;top:380px;width:340px;height:196px;background:url("assets/img/mono.png") 0 0/340px 196px no-repeat}}
.f{f}-mot{{position:absolute;left:310px;top:600px;width:460px;height:auto}}
.f{f}-trait{{position:absolute;left:480px;top:690px;width:120px;height:4px;background:#B8A07E;transform-origin:50% 50%}}
.f{f}-cta{{position:absolute;left:108px;width:864px;text-align:center;font:900 104px/0.9 "Barlow Condensed";text-transform:uppercase;white-space:nowrap}}
.f{f}-info{{position:absolute;left:108px;width:864px;text-align:center;font:italic 800 40px/1 "Barlow Condensed";letter-spacing:0.05em;text-transform:uppercase;color:rgba(244,241,236,0.62);white-space:nowrap}}
.f{f}-chevron{{position:absolute;left:522px;top:1068px;width:36px;height:22px}}
.f{f}-mentions{{position:absolute;left:108px;top:1110px;width:864px;padding:22px 28px;box-sizing:border-box;background:#222222;color:#F4F1EC;text-align:center;font:500 34px/1.22 "DM Sans"}}
"""
tiers = [("0px 0px 66.667% 0px", 600), ("33.333% 0px 33.333% 0px", -600), ("66.667% 0px 0px 0px", 600)]
mono = "".join(f'<div id="f{f}-m{k}" class="f{f}-mono" style="clip-path:inset({ins})"></div>'
               for k, (ins, _) in enumerate(tiers))
chevron = ('<svg viewBox="0 0 36 22"><path d="M3 3 L18 18 L33 3" fill="none" '
           'stroke="#B8A07E" stroke-width="5" stroke-linecap="square" stroke-linejoin="miter"/></svg>')
ecrire(f, 3.0, "\n    ".join([
    fond(f, "f1", 0, 3.0, None),
    calque(f"{f}-cl", 0, 3.0, 2, mono + f'<img id="f{f}-w" class="f{f}-mot" src="assets/img/word.png" alt="" />'
           f'<div id="f{f}-t" class="f{f}-trait"></div>'),
    calque(f"{f}-cc", 1.0, 2.0, 3, f'<div id="f{f}-c1" class="f{f}-cta" style="top:750px;color:#F4F1EC">UNE QUESTION{NB}?</div>'
           f'<div id="f{f}-c2" class="f{f}-cta" style="top:850px;color:#B8A07E">ÉCRIVEZ-NOUS.</div>'),
    calque(f"{f}-ci", 1.25, 1.75, 4,
           f'<div class="f{f}-info lsq-masque" style="top:975px"><span id="f{f}-i1">URBAN VALLEY{NB}·{NB}CONFLANS-SAINTE-HONORINE</span></div>'
           f'<div class="f{f}-info lsq-masque" style="top:1022px"><span id="f{f}-i2">6H{NB}–{NB}23H{NB}·{NB}7J/7</span></div>'
           f'<div id="f{f}-v" class="f{f}-chevron">{chevron}</div>'),
    calque(f"{f}-cm", 1.5, 1.5, 5,
           f'<div class="lsq-masque" style="position:absolute;left:108px;top:1110px;width:864px;height:140px">'
           f'<div id="f{f}-mentions" class="f{f}-mentions" style="left:0;top:0">Conversation mise en scène.</div></div>'),
    calque(f"{f}-cb", 0, 0.6, 6, bandes6),
]), """
  // les bandes repartent vers la gauche (vitesse nulle au départ : power2.in) et découvrent le canevas
  [0, 1, 2].forEach((k) => tl.fromTo(R("b" + k), { x: -300 }, { x: -2300, duration: 0.35, ease: "power2.in" }, k * 0.0625));
  // monogramme assemblé par ses 3 bandes horizontales : haut depuis la droite, milieu depuis la gauche, bas depuis la droite
  [[600, 0], [-600, 0.125], [600, 0.25]].forEach(([dx, t], k) =>
    tl.fromTo(R("m" + k), { x: dx }, { x: 0, duration: 0.25, ease: "power3.out" }, t));
  // mot-symbole révélé par une coupe de gauche à droite, filet or dessous
  tl.fromTo(R("w"), { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.25, ease: "power2.out" }, 0.5);
  tl.fromTo(R("t"), { scaleX: 0 }, { scaleX: 1, duration: 0.2, ease: "power3.out" }, 0.625);
  // CTA : frappe sur le temps
  tl.fromTo([R("c1"), R("c2")], { scale: 1.2 }, { scale: 1, duration: 0.22, ease: "power4.out" }, 1.0);
  // adresse, horaires, chevron
  tl.fromTo([R("i1"), R("i2")], { yPercent: 110 }, { yPercent: 0, duration: 0.2, ease: "power3.out", stagger: 0.0625 }, 1.25);
  tl.fromTo(R("v"), { y: -16, scale: 0.6 }, { y: 0, scale: 1, duration: 0.2, ease: "power3.out" }, 1.375);
  // mentions : montent dans leur masque, puis tout reste immobile jusqu'à la fin
  tl.fromTo(R("mentions"), { yPercent: 100 }, { yPercent: 0, duration: 0.25, ease: "power3.out" }, 1.5);
""", css6)
