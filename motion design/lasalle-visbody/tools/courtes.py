"""Stories courtes du lancement Visbody (9:16, 10 à 12 s, 60 i/s) : deux propositions plus rythmées.

Demande du 17/11/2026 : « les vidéos sont trop longues pour le format story, 10/12 secondes max. Garde ce que tu as
fait mais adapte, rends-le plus dynamique et garde les éléments clés essentiels. Propose-moi 2 stories. »

  A « Le scan » (12 s)        EN SERVICE · BIEN PLUS QU'UNE BALANCE. → UNE BALANCE IA. → l'avatar 3D sort du plateau, le
                              scan descend puis remonte, les 5 résultats tombent au rythme du scan → + 2 € → l'accueil
  B « Vos résultats » (10 s)  EN SERVICE · VOS PROGRÈS, EN 3D. (la machine) → les 5 résultats, un par demi-temps →
                              UNE BALANCE IA. → + 2 € → l'accueil

Coupes franches sur la grille de 120 BPM (un temps = 0,5 s), sans volet : le mouvement est dans les entrées (frappes,
glissements masqués, scan) ; le premier élément de chaque scène entre dès la coupe (aucune image vide). Mêmes atomes, textes et charte que tools/build.py ; aucune allégation à prouver (ni
programme IA, ni « 3e salle de France »), aucune offre datée. Repères : HISTOIRES ci-dessous, lus aussi par
tools/musique_courtes.py et tools/livrer_courtes.py.

Usage : ~/.venvs/hyperframes-audio/bin/python -I tools/courtes.py   (puis musique_courtes.py, rendu, livrer_courtes.py)
"""
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import build  # noqa: E402  (atomes, textes, assets)
from build import cache, monte, plus  # noqa: E402

FPS = build.FPS
# Scènes de chaque story : (id, début, fin) en secondes ; instants des entrées en secondes absolues
HISTOIRES = {
    "A": {"projet": "story-916-courte-A", "nom": "story_courte_A_scan", "duree": 12.0,
          "scenes": [("a1", 0.0, 2.0), ("a2", 2.0, 3.5), ("a3", 3.5, 8.0), ("a4", 8.0, 10.0), ("a5", 10.0, 12.0)],
          "cassure": (2.0, 2.25), "ia": 2.25,
          "scan": {"plateau": [3.75, 0.35], "montee": [4.0, 0.6], "descente": [4.65, 1.0], "remontee": [5.75, 1.0]},
          "resultats": [4.75, 5.15, 5.55, 5.95, 6.35], "prix": 8.05, "ligne": 8.5, "accueil": 10.25},
    "B": {"projet": "story-916-courte-B", "nom": "story_courte_B_resultats", "duree": 10.0,
          "scenes": [("b1", 0.0, 2.0), ("b2", 2.0, 5.0), ("b3", 5.0, 6.5), ("b4", 6.5, 8.0), ("b5", 8.0, 10.0)],
          "cassure": (5.0, 5.25), "ia": 5.25,
          "resultats": [2.05, 2.45, 2.85, 3.25, 3.65], "plaque": 4.1, "prix": 6.55, "ligne": 6.95, "accueil": 8.25},
}
MENTION_FIN = build.MENTION_OPTION + " " + build.MENTION_SANTE


def scene(cid, debut, fin, contenu, js):
    """Scène en coupe franche : fond opaque de la série, entrées en secondes absolues ramenées au temps de la scène."""
    corps = f'{build.fond(1920, cid + "-")}\n<div id="{cid}-c" class="a" style="inset:0">\n{contenu}\n</div>'
    return build.composition(cid, 1080, 1920, round(fin - debut, 3), corps, js)


def frappe(sel, t, debut, origine="left center", echelle=1.35):
    """Le mot frappe : il entre trop grand et se pose en 0,45 s, dévoilé de gauche à droite."""
    return (f'        tl.fromTo("{sel}", {{ scale: {echelle}, clipPath: "inset(0% 100% 0% 0%)" }}, {{ scale: 1, clipPath: "inset(0% 0% 0% 0%)", '
            f'duration: 0.45, ease: "power4.out", transformOrigin: "{origine}" }}, {t - debut:.3f});\n')


def m(mid, t, debut, d=0.5, pad=build.PAD):
    return monte(mid, t - debut, d, pad)


# ---------------------------------------------------------------- scènes communes
def couverture(cid, fin, titre, machine=False):
    """Image 0 : « + OPTION PREMIUM », le logo, la plaque « EN SERVICE » et le titre sont déjà en place."""
    lignes = "".join(f'<div class="t9{" or" if or_ else ""}{" it" if it else ""}" style="font-size:{taille}px;line-height:.92">{l}</div>'
                     for l, or_, it, taille in titre)
    img = ""
    if machine:
        W = 400
        img = (f'<div id="{cid}-machine" class="a" style="left:640px;top:520px;width:{W}px;height:{round(build.M60[1] * W / build.M60[0])}px">'
               f'<img src="assets/img/m60.png" alt="" style="display:block;width:{W}px"></div>')
    contenu = f"""
<div class="a kick" style="left:96px;top:236px;font-size:38px">{plus(40)}Option Premium</div>
<img class="a" src="assets/img/logo-complet.png" alt="LA SALLE" style="left:774px;top:212px;width:210px">
<div id="{cid}-plaque" class="a plaque" style="--c:{round(0.42 * 96)}px;left:96px;top:420px;height:96px;padding:0 52px;font-size:62px;transform-origin:left center">En service</div>
<div id="{cid}-titre" class="a" style="left:92px;top:620px">{lignes}</div>
{img}
<div class="a" style="left:96px;top:1560px">{plus(60)}</div>
<div id="{cid}-filet" class="a filet" style="left:178px;top:1586px;width:902px;height:6px;transform-origin:left center"></div>
"""
    js = (f'        tl.fromTo("#{cid}-titre", {{ scale: 1 }}, {{ scale: 1.04, duration: {fin:g}, ease: "none", transformOrigin: "left center" }}, 0);\n'
          f'        tl.fromTo("#{cid}-plaque", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }}, 0.5);\n'
          f'        tl.from("#{cid}-filet", {{ scaleX: 0, duration: 0.9, ease: "power2.out" }}, 0.1);\n')
    if machine:
        js += f'        tl.fromTo("#{cid}-machine", {{ y: 40, scale: 1 }}, {{ y: 0, scale: 1.05, duration: {fin:g}, ease: "none", transformOrigin: "50% 80%" }}, 0);\n'
    return contenu, js


def balance_ia(cid, debut, fin, t_ia):
    contenu = f"""
<div class="a kick" style="left:96px;top:236px;font-size:38px">Nouveau · Analyse 3D</div>
<div class="a t9" style="left:92px;top:560px;font-size:156px">Une balance</div>
<div id="{cid}-ia" class="a t9 or" style="left:84px;top:730px;font-size:600px;line-height:.86">IA.</div>
"""
    return scene(cid, debut, fin, contenu, frappe(f"#{cid}-ia", t_ia, debut))


def prix(cid, debut, fin, t_prix, t_ligne):
    contenu = f"""
{cache(96, 236, 888, f'<div class="kick" style="font-size:38px">{plus(40)}L’option Premium</div>', f"{cid}-kick")}
<div class="a" style="left:96px;top:420px;display:flex;align-items:center;gap:26px">
  <div id="{cid}-plus">{plus(200)}</div>
  <div id="{cid}-deux" class="t9 num" style="font-size:410px;line-height:.86">2 €</div>
</div>
<div id="{cid}-ttc" class="a t8 it" style="left:96px;top:810px;font-size:116px">TTC par semaine</div>
{cache(96, 1010, 900, f'<div class="plaque" style="--c:{round(0.42 * 92)}px;height:92px;padding:0 48px;font-size:58px">1 analyse 3D par semaine</div>', f"{cid}-ligne", 20)}
{cache(96, 1150, 888, '<p class="corps" style="font-size:46px">Soit 8&nbsp;€ toutes les 4 semaines,<br>en plus de votre abonnement.</p>', f"{cid}-soit")}
"""
    js = (m(f"{cid}-kick", debut + 0.05, debut, 0.45)
          + f'        tl.fromTo("#{cid}-plus", {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.6)" }}, {t_prix - debut:.3f});\n'
          + frappe(f"#{cid}-deux", t_prix, debut)
          + f'        tl.fromTo("#{cid}-ttc", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.out" }}, {t_prix - debut + 0.1:.3f});\n'
          + m(f"{cid}-ligne", t_ligne, debut, 0.5, 20) + m(f"{cid}-soit", t_ligne + 0.25, debut, 0.55))
    return scene(cid, debut, fin, contenu, js)


def accueil(cid, debut, fin, t_acc):
    contenu = f"""
<div id="{cid}-logo" class="a" style="left:350px;top:230px;width:380px"><img src="assets/img/logo-complet.png" alt="LA SALLE" style="display:block;width:380px"></div>
{cache(40, 600, 1000, '<div class="t9" style="font-size:180px;text-align:center">Activez-la</div>', f"{cid}-l1")}
{cache(40, 765, 1000, '<div class="t9 or" style="font-size:180px;text-align:center">à l’accueil.</div>', f"{cid}-l2")}
{cache(40, 990, 1000, '<div class="t8 it" style="font-size:84px;text-align:center">En quelques secondes.</div>', f"{cid}-l3")}
<p id="{cid}-mention" class="a mention" style="left:96px;top:1150px;width:888px;padding:22px 30px;font-size:33px;line-height:1.28;text-align:center">{MENTION_FIN}</p>
"""
    js = (f'        tl.from("#{cid}-logo", {{ clipPath: "inset(0% 0% 100% 0%)", y: -30, duration: 0.5, ease: "power3.out" }}, 0.0);\n'
          + m(f"{cid}-l1", t_acc - 0.15, debut, 0.5) + m(f"{cid}-l2", t_acc, debut, 0.5) + m(f"{cid}-l3", t_acc + 0.3, debut, 0.5)
          + f'        tl.from("#{cid}-mention", {{ clipPath: "inset(100% 0% 0% 0%)", duration: 0.5, ease: "power2.out" }}, {t_acc - debut + 0.2:.3f});\n')
    return scene(cid, debut, fin, contenu, js)


def liste_resultats(cid, temps, debut, top, taille, ecart, x=96):
    """Les 5 résultats du visuel « CE QUE VOUS DÉCOUVREZ », un par entrée, avec le + or de la série."""
    html = "".join(cache(x, top + ecart * i, 980, f'<div class="t8" style="font-size:{taille}px;display:flex;align-items:center;gap:22px">'
                                               f'{plus(round(taille * 0.62))}{r}</div>', f"{cid}-r{i}", 22)
                   for i, r in enumerate(build.RESULTATS))
    js = "".join(m(f"{cid}-r{i}", t, debut, 0.4, 22) for i, t in enumerate(temps))
    return html, js


# ---------------------------------------------------------------- story A « Le scan »
def scenes_A():
    h = HISTOIRES["A"]
    (c1, d1, f1), (c2, d2, f2), (c3, d3, f3), (c4, d4, f4), (c5, d5, f5) = h["scenes"]
    contenu, js = couverture(c1, f1, [("Bien plus", True, False, 168), ("qu’une", False, False, 168), ("balance.", False, False, 168)])
    sortie = {c1: scene(c1, d1, f1, contenu, js), c2: balance_ia(c2, d2, f2, h["ia"])}
    # Avatar 3D (assets/js/avatar.js) : même rendu que la story longue, scan deux fois plus court
    R = {"largeur": 640, "hauteur": 1120, **{k: [round(t - d3, 3), dur] for k, (t, dur) in h["scan"].items()},
         "fin": round(f3 - d3, 3)}
    resultats, js_res = liste_resultats(c3, h["resultats"], d3, 760, 52, 112)
    contenu = f"""
{cache(96, 236, 888, '<div class="kick" style="font-size:38px">Le principe</div>', f"{c3}-kick")}
{cache(92, 296, 900, '<div class="t9" style="font-size:150px">Un scan</div>', f"{c3}-l1")}
{cache(92, 430, 900, '<div class="t9 it or" style="font-size:150px">à 360°</div>', f"{c3}-l2")}
<canvas id="{c3}-avatar" class="a" width="{R['largeur']}" height="{R['hauteur']}" style="left:440px;top:560px;width:{R['largeur']}px;height:{R['hauteur']}px"></canvas>
{resultats}
"""
    js = (f'''        const scan = {{ t: 0 }};
        let rendre = null;
        window.__hf = window.__hf || {{}};
        window.__hf.buildReady = window.__hf.buildReady || {{}};
        window.__hf.buildReady["{c3}-avatar"] = import("./assets/js/avatar.js").then((m) => {{
          rendre = m.creer(document.getElementById("{c3}-avatar"), {json.dumps(R)});
          rendre(scan.t);
        }});
        tl.to(scan, {{ t: {R["fin"]}, duration: {R["fin"]}, ease: "none", onUpdate: () => {{ if (rendre) rendre(scan.t); }} }}, 0);
'''
          + m(f"{c3}-kick", d3 + 0.05, d3, 0.45) + m(f"{c3}-l1", d3 + 0.1, d3, 0.5) + m(f"{c3}-l2", d3 + 0.25, d3, 0.5) + js_res)
    sortie[c3] = scene(c3, d3, f3, contenu, js)
    sortie[c4] = prix(c4, d4, f4, h["prix"], h["ligne"])
    sortie[c5] = accueil(c5, d5, f5, h["accueil"])
    return sortie


# ---------------------------------------------------------------- story B « Vos résultats »
def scenes_B():
    h = HISTOIRES["B"]
    (c1, d1, f1), (c2, d2, f2), (c3, d3, f3), (c4, d4, f4), (c5, d5, f5) = h["scenes"]
    contenu, js = couverture(c1, f1, [("Vos", False, False, 150), ("progrès,", False, False, 150), ("en 3D.", True, True, 150)],
                             machine=True)
    sortie = {c1: scene(c1, d1, f1, contenu, js)}
    resultats, js_res = liste_resultats(c2, h["resultats"], d2, 460, 96, 150)
    contenu = f"""
{cache(96, 236, 888, '<div class="kick" style="font-size:38px">Ce que vous découvrez</div>', f"{c2}-kick")}
{resultats}
{cache(96, 1250, 900, f'<div class="plaque" style="--c:{round(0.42 * 92)}px;height:92px;padding:0 48px;font-size:58px">En 1 scan à 360°</div>', f"{c2}-plaque", 20)}
"""
    js = m(f"{c2}-kick", d2 + 0.05, d2, 0.45) + js_res + m(f"{c2}-plaque", h["plaque"], d2, 0.45, 20)
    sortie[c2] = scene(c2, d2, f2, contenu, js)
    sortie[c3] = balance_ia(c3, d3, f3, h["ia"])
    sortie[c4] = prix(c4, d4, f4, h["prix"], h["ligne"])
    sortie[c5] = accueil(c5, d5, f5, h["accueil"])
    return sortie


def index(cle):
    h = HISTOIRES[cle]
    d = h["duree"]
    hotes = "\n".join(
        f'      <div id="h-{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{a:g}" '
        f'data-duration="{b - a:g}" data-track-index="{1 + i % 2}" data-width="1080" data-height="1920" style="z-index:{i + 1}"></div>'
        for i, (c, a, b) in enumerate(h["scenes"]))
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
{build.FOND_CSS}
    </style>
  </head>
  <body>
    <!-- Story courte {cle} du lancement Visbody : {len(h["scenes"])} scènes en coupes franches, {d:g} s, {FPS} i/s, 120 BPM -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{d:g}" data-width="1080" data-height="1920" data-fps="{FPS}">
{hotes}
      <audio id="musique" src="assets/audio/musique.wav" data-start="0" data-duration="{d:g}" data-track-index="10" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def main():
    import shutil
    for cle, scenes in (("A", scenes_A), ("B", scenes_B)):
        h = HISTOIRES[cle]
        p = build.projet(h["projet"])                             # assets, avatar et Three.js recopiés
        for f in os.listdir(os.path.join(p, "compositions")):
            os.remove(os.path.join(p, "compositions", f))
        musique = os.path.join(build.RACINE, "_communs", f"musique_visbody_courte_{cle}.wav")
        if os.path.exists(musique):
            shutil.copy2(musique, os.path.join(p, "assets", "audio", "musique.wav"))
        build.ecrire(os.path.join(p, "index.html"), index(cle))
        for cid, html in scenes().items():
            build.ecrire(os.path.join(p, "compositions", f"{cid}.html"), html)
        print("Écrit :", p)


if __name__ == "__main__":
    main()
