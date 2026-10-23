"""Génère les projets HyperFrames de la pub LE CUBE tirée du film « LE CUBE V1 » (RM Visual) : 15 s, 9:16, Meta.

Même structure et même charte que les pubs par discipline (../lecube-disciplines/tools/build.py, dont on reprend
les styles et les entrées de texte), mais les images sont des plans du film :
  accroche (0–3)      plans du film et lignes, propre à chaque variante (A, B, C : test A/B sur l'accroche seule)
  étapes (3–8,5)      01 HYROX, 02 CROSSFIT, 03 POLE DANCE, 04 BOXE : deux plans du film par étape, coupés sur le temps
  argument (8,5–11,5) cassure « ET TOI ? » sur noir, puis ring, tatamis, rig, et « TOUT ÇA, À CONFLANS. »
  carte (11,5–15)     LE CUBE, les quatre disciplines, « RÉSERVE TA SÉANCE D'ESSAI », chevron vers le bouton, adresse
  bandeau (0–11,5)    « LE CUBE · CONFLANS », pour que celui qui part tôt sache où il est
Instants, plans du film et recadrages : tools/cues_v1.json.

Le film montre des personnes : il n'est jamais dans le dépôt (public). On le dépose dans ~/lecube-sources/v1/ :
  - soit le film entier (un seul .mp4) ;
  - soit des extraits, décrits dans ~/lecube-sources/v1/sources.json :
    {"extraits": [{"fichier": "extrait_1.mp4", "debut": 0.0}, {"fichier": "extrait_2.mp4", "debut": 5.3}, …]}
    (« debut » = instant du film où commence l'extrait).
Chaque plan est alors découpé avec ffmpeg (recadrage 9:16 sur son centre, ralenti si besoin, 30 i/s) dans
_communs/video/, puis copié dans <variante>/assets/ (ignoré par git). Sans film, chaque plan devient un carton numéroté :
c'est l'animatique, qui sert à valider le rythme, les textes, la carte et la musique avant d'avoir les images.

Usage : python3 tools/build.py [A B C]
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
MOTION = os.path.normpath(os.path.join(RACINE, ".."))
FILM = os.environ.get("LECUBE_V1_FILM", os.path.expanduser("~/lecube-sources/v1"))   # variable : essais
COUPES = os.path.join(RACINE, "_communs", "video")

_spec = importlib.util.spec_from_file_location("build_disciplines", os.path.join(MOTION, "lecube-disciplines", "tools", "build.py"))
D = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(D)
r, bloc, masque, apos, FINE, BRONZE = D.r, D.bloc, D.masque, D.apos, D.FINE, D.BRONZE

# Calques : les médias sous le voile, les textes au-dessus, quel que soit l'ordre dans le fichier (une ligne peut durer
# plus longtemps que son plan). Carton d'animatique : rayures sombres, numéro du plan, ce qu'on y verra.
D.CSS += """.cadre{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:50% 45%;z-index:1}
video.clip{object-fit:cover}
.carton{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:50% 45%;
  background:repeating-linear-gradient(135deg,#151515 0 40px,#1c1c1c 40px 80px)}
.carton-n{position:absolute;left:0;width:1080px;top:960px;text-align:center;font:400 260px/1 "Anton";color:#6a6a6a}
.carton-q{position:absolute;left:0;width:1080px;top:1300px;text-align:center;font:600 28px/1.5 "Inter";letter-spacing:.08em;
  color:#b4b4b4;text-transform:uppercase}
"""
Z_MEDIA, Z_TEXTE = 1, 5


def parse(cle):
    """« v1:20 » → ("v1", "20", None) ; « v1img:30@13.35 » → ("v1img", "30", 13.35)."""
    genre, reste = cle.split(":")
    n, _, t = reste.partition("@")
    return genre, n, float(t) if t else None


def nom_fichier(cle, d):
    genre, n, t = parse(cle)
    return f"v1-{n}-{round(d * 1000)}ms.mp4" if genre == "v1" else f"v1img-{n}-{round(t * 100)}.jpg"


class Compo(D.Compo):
    """Sous-composition des pubs par discipline, avec des plans du film (vidéo, image fixe ou carton)."""

    film = False      # vrai quand les plans du film ont été découpés (sinon : animatique)
    plans = {}        # « cues.film.plans »
    demandes = set()  # plans du film utilisés : (clé, durée à l'écran) ; une même clé peut servir à plusieurs durées

    def calque(self, nom, debut, duree, contenu, piste=None, z=Z_TEXTE):
        super().calque(nom, debut, duree, contenu, piste)
        self.calques[-1] = self.calques[-1].replace('class="clip" ', f'class="clip" style="z-index:{z}" ', 1)

    def media(self, nom, cle, debut, duree, zoom=1.05, voile=None):
        genre, n, t = parse(cle)
        self.demandes.add((cle, round(duree, 3) if genre == "v1" else 0))
        self.nb_photos += 1
        piste = 0 if self.nb_photos % 2 else 90
        fond = f' style="background:rgba(10,10,10,{voile})"' if voile is not None else ""
        el = f"{self.cid}-{nom}"
        if self.film and genre == "v1":
            # La vidéo porte son propre minutage ; le cadre qui zoome n'est pas minuté (pas de vidéo dans un calque minuté)
            self.calques.append(f'    <div id="{el}-w" class="cadre" data-layout-allow-overflow><video id="{el}-v" class="clip" src="assets/video/{nom_fichier(cle, duree)}" '
                                f'muted playsinline data-hf-media-start-basis="local" data-start="{r(debut)}" data-duration="{r(duree)}" data-track-index="{piste}"></video></div>')
            self.calque(f"{nom}-voile", debut, duree, f'<div class="voile"{fond}></div>', piste=piste + 1, z=Z_MEDIA + 1)
            self.js.append(f'  zoom("{el}-w", {r(debut)}, {r(duree)}, {zoom});')
            return
        if self.film:
            image = f'<div id="{el}-ph" class="ph" style="background-image:url(assets/img/{nom_fichier(cle, duree)})"></div>'
        else:
            p = self.plans[n]
            quoi = apos(p["quoi"]) + (" · image fixe" if genre == "v1img" else "")
            # Repère d'animatique, sous le voile et sous les textes de la pub : chevauchement voulu
            ok = "data-layout-allow-occlusion data-layout-allow-overlap"
            image = (f'<div id="{el}-ph" class="carton"><div class="carton-n" {ok}>{n}</div><div class="carton-q" {ok}>Plan {n} du film V1 · {quoi}'
                     f'<br>Animatique : image du film à venir</div></div>')
        self.calque(nom, debut, duree, image + f'<div class="voile"{fond}></div>', piste=piste, z=Z_MEDIA)
        self.js.append(f'  zoom("{el}-ph", {r(debut)}, {r(duree)}, {zoom});')


# ─────────────────────────── accroche (0–3 s) ───────────────────────────
def accroche(C, v):
    plans = C["accroches"][v]["plans"]
    c = Compo("accroche", C["fin_accroche"])
    for k, p in enumerate(plans):
        fin = plans[k + 1]["t"] if k + 1 < len(plans) else c.duree
        c.media(f"p{k}", p["photo"], p["t"], fin - p["t"])
        for j, l in enumerate(p["lignes"]):
            genre = l["style"].split()[0]
            style = f'font-size:{l.get("taille", D.TAILLES[genre])}px'
            nom, d = f"p{k}l{j}", l.get("fin", fin) - l["t"]
            if l["t"] == 0:      # image 0 : la ligne est déjà posée, nette, sans entrée animée
                c.calque(nom, 0, d, bloc(l["style"], apos(l["texte"]), top=l["top"], style=style).replace('id="ID" ', ""))
            elif genre == "mot":
                c.texte(nom, l["t"], d, bloc(l["style"], apos(l["texte"]), top=l["top"], style=style), "frappe", k=1.18, d=0.14)
            else:
                c.texte(nom, l["t"], d, masque(l["style"], apos(l["texte"]), top=l["top"], style=style), "chute")
    return c


# ─────────────────────────── étapes (3–8,5 s) ───────────────────────────
def etapes(C):
    E = C["etapes"]
    t0g = E[0]["t"]
    c = Compo("etapes", E[-1]["fin"] - t0g)
    for k, e in enumerate(E):
        t0, d = e["t"] - t0g, e["fin"] - e["t"]
        t = t0
        for j, p in enumerate(e["plans"]):          # plans coupés sur le temps ; le dernier va jusqu'à l'étape suivante
            dp = p.get("d", t0 + d - t)
            c.media(f"e{k}p{j}", p["m"], t, dp, 1.06)
            t += dp
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
    c.calque("noir", 0, tc, '<div class="noir"></div>', piste=0, z=Z_MEDIA)
    c.texte("toi", 0, tc, bloc("ttl", f"ET TOI{FINE}?", top=700, style="font-size:150px", centre=True), "frappe", k=1.3)
    segs = a["segments"]
    for k, s in enumerate(segs):
        fin = segs[k + 1]["t"] if k + 1 < len(segs) else a["fin"]
        c.media(f"s{k}", s["m"], s["t"] - t0g, fin - s["t"], 1.08)
    l1, l2 = a["lignes"]
    for k, txt in enumerate(l1):                    # une ligne par image : le ring, les tatamis, le rig
        cls = "ttl br pl" if k == len(l1) - 1 else "ttl pl"
        tk = segs[k]["t"] - t0g
        c.texte(f"l{k}", tk, t2 - tk, masque(cls, apos(txt), top=640 + 112 * k, style="font-size:96px"), "chute")
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
    c.media("fond", C["carte_photo"], 0, d, 1.04, voile=0.7)
    c.texte("nom", 0, d, bloc("ttl", C["carte_titre"], top=470, style="font-size:170px", centre=True), "frappe", k=1.2)
    c.texte("sous", 0.12, d - 0.12, bloc("det", apos(C["carte_sous"]), top=664, style="font-size:32px;letter-spacing:.14em;color:#B27639", centre=True), "balaie")
    c.texte("trait", 0.2, d - 0.2, '<div id="ID" class="trait" style="left:420px;top:730px;width:240px;transform-origin:50% 50%"></div>', "trace")
    c.texte("cta1", cta, d - cta, bloc("ttl br", "RÉSERVE TA", top=850, centre=True), "frappe")
    c.texte("cta2", cta + 0.12, d - cta - 0.12, bloc("ttl br", "SÉANCE D’ESSAI", top=954, centre=True), "frappe")
    c.calque("chevron", cta + 0.5, d - cta - 0.5,
             f'<svg id="carte-chevron-t" class="a" style="left:500px;top:1084px;width:80px;height:50px" viewBox="0 0 80 50">'
             f'<polyline points="6,8 40,42 74,8" fill="none" stroke="{BRONZE}" stroke-width="9" stroke-linecap="square"/></svg>')
    c.js.append(f'  tl.fromTo($("carte-chevron-t"), {{ y: 0 }}, {{ y: 16, duration: 0.25, ease: "power1.inOut", yoyo: true, repeat: 7 }}, {r(cta + 0.5)});')
    c.texte("adresse", cta + 0.25, d - cta - 0.25, bloc("det", apos(C["carte_adresse"]), top=1176, style="font-size:26px", centre=True), "balaie")
    return c


# ─────────────────────────── bandeau (0 → carte, au-dessus de tout) ───────────────────────────
def bandeau(C):
    c = Compo("bandeau", C["carte"])
    c.calque("cadre", 0, c.duree, f'<div class="a centre" style="top:300px"><div style="display:inline-block;padding:14px 30px 12px;'
             f'border:3px solid {BRONZE};background:rgba(10,10,10,.72);font:600 34px/1 Oswald;letter-spacing:.24em;'
             f'color:#F5F2EC;white-space:nowrap">{C["bandeau"]}</div></div>', piste=1)
    return c


# ─────────────────────────── plans du film ───────────────────────────
def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        sys.exit(f"Échec : {' '.join(cmd)}\n{p.stderr[-1500:]}")
    return p.stdout


def sources():
    """[(chemin, instant du film où il commence, durée, largeur, hauteur)] : le film entier, ou les extraits de sources.json."""
    if not os.path.isdir(FILM):
        return []
    j = os.path.join(FILM, "sources.json")
    if os.path.exists(j):
        liste = [(os.path.join(FILM, s["fichier"]), float(s["debut"])) for s in json.load(open(j, encoding="utf-8"))["extraits"]]
    else:
        films = sorted(f for f in os.listdir(FILM) if f.lower().endswith((".mp4", ".mov")))
        if len(films) > 1:
            sys.exit(f"Plusieurs vidéos dans {FILM} : décrire les extraits dans sources.json")
        liste = [(os.path.join(FILM, f), 0.0) for f in films]
    S = []
    for chemin, dec in liste:
        p = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                            "-of", "json", chemin]))
        S.append((chemin, dec, float(p["format"]["duration"]), p["streams"][0]["width"], p["streams"][0]["height"]))
    return S


def morceaux(S, a, b):
    """Morceaux (source, de, à) qui couvrent [a, b] du film : un seul extrait si possible, sinon bout à bout."""
    for s in S:
        if s[1] - 1e-3 <= a and b <= s[1] + s[2] + 1e-3:
            return [(s, a, b)]
    out, t = [], a
    while t < b - 1e-3:
        s = max((s for s in S if s[1] - 1e-3 <= t < s[1] + s[2] - 1e-3), key=lambda s: s[1] + s[2], default=None)
        if s is None:
            sys.exit(f"Aucune source ne couvre {t:.2f} s du film : revoir les extraits de {FILM}")
        u = min(b, s[1] + s[2])
        out.append((s, t, u))
        t = u
    return out


def recadrage(s, centre):
    """Recadrage 9:16 pleine hauteur, centré sur « centre » (fraction de la largeur), sans sortir de l'image."""
    w, h = s[3], s[4]
    cw = int(round(h * 9 / 16 / 2)) * 2
    x = min(max(int(round(centre * w - cw / 2)), 0), w - cw)
    return f"crop={cw}:{h}:{x}:0,scale=1080:1920:flags=lanczos"


def decouper(C, S, demandes):
    """Découpe chaque plan demandé (clé, durée à l'écran) dans _communs/video/ ; renvoie {fichier: (plan, vitesse)}."""
    F = C["film"]
    os.makedirs(COUPES, exist_ok=True)
    faits = {}
    for cle, d in sorted(demandes):
        genre, n, t = parse(cle)
        p = F["plans"][n]
        sortie = os.path.join(COUPES, nom_fichier(cle, d))
        if genre == "v1img":
            s = max(S, key=lambda s: min(t - s[1], s[1] + s[2] - t))      # l'extrait où l'instant est le plus à l'intérieur
            if not s[1] <= t < s[1] + s[2]:
                sys.exit(f"Aucune source ne couvre {t:.2f} s du film : revoir les extraits de {FILM}")
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t - s[1]:.3f}", "-i", s[0], "-frames:v", "1",
                 "-vf", recadrage(s, p["centre"]), "-q:v", "2", sortie])
            if not os.path.exists(sortie):
                sys.exit(f"Image fixe du plan {n} à {t:.2f} s non extraite : revoir cues_v1.json")
            faits[os.path.basename(sortie)] = (n, None)
            continue
        a, b = p["debut"] + F["marge"], p["fin"] - F["marge"]
        vitesse = min(1.0, (b - a) / d)               # plan trop court pour sa place : ralenti (50 i/s → 30 i/s sans image dupliquée à 0,6)
        bouts = morceaux(S, a, a + d * vitesse)
        entrees = sum((["-ss", f"{u0 - s[1]:.3f}", "-t", f"{u1 - u0:.3f}", "-i", s[0]] for s, u0, u1 in bouts), [])
        graphe = ("".join(f"[{i}:v]{recadrage(s, p['centre'])},setsar=1[b{i}];" for i, (s, _, _) in enumerate(bouts))
                  + "".join(f"[b{i}]" for i in range(len(bouts))) + f"concat=n={len(bouts)}:v=1:a=0,"
                  f"setpts=(PTS-STARTPTS)/{vitesse:.4f},fps=30,tpad=stop_mode=clone:stop_duration=0.2,format=yuv420p[o]")
        run(["ffmpeg", "-v", "error", "-y", *entrees, "-filter_complex", graphe, "-map", "[o]",
             "-frames:v", str(round(d * 30)), "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-g", "10",
             "-movflags", "+faststart", sortie])
        # Les instants des plans viennent d'une détection de coupes (± 0,05 s) : pas de coupe du film dans un plan découpé
        coupe = subprocess.run(["ffmpeg", "-hide_banner", "-i", sortie, "-vf", "select='gt(scene,0.3)',showinfo", "-f", "null", "-"],
                               capture_output=True, text=True).stderr
        if "pts_time" in coupe:
            print(f"  ⚠ plan {n} : une coupe du film semble tomber dans {os.path.basename(sortie)}, revoir debut/fin dans cues_v1.json")
        faits[os.path.basename(sortie)] = (n, vitesse)
    return faits


# ─────────────────────────── projet ───────────────────────────
def index_html(v, C, hotes, film):
    hs = "\n".join(f'      <div id="h-{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                   f'data-start="{r(s)}" data-duration="{r(du)}" data-track-index="{p}" data-width="1080" data-height="1920"></div>'
                   for cid, s, du, p in hotes)
    etat = "plans du film" if film else "ANIMATIQUE (cartons à la place des plans du film)"
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
    <!-- LE CUBE · film V1 · variante {v} · 9:16 · 15 s · 120 BPM · {etat}. Généré par lecube-v1/tools/build.py -->
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


def brief(C, v, film):
    a = C["accroches"][v]
    lignes = " / ".join(l["texte"] for p in a["plans"] for l in p["lignes"])
    etat = ("Plans du film découpés depuis ~/lecube-sources/v1/ (hors dépôt)." if film else
            "ANIMATIQUE : le film n'est pas encore dans ~/lecube-sources/v1/, chaque plan est un carton numéroté.")
    return f"""---
workflow: general-video
flow: automation
storyboard: no
destination: meta-reels
aspect: 1080x1920
language: fr
length: 15s
narration: no
---

## Intent

Pub Meta LE CUBE tirée du film « LE CUBE V1 » (RM Visual), avec motion design et appel à l'action, variante {v}
(« {a["titre"]} ») d'un test A/B : seule l'accroche (0–3 s) change. Accroche : {lignes}. Plan de montage : doc
« Pub réseaux LE CUBE — analyse du film V1 et plan de montage ». Montage généré par `../tools/build.py` depuis
`../tools/cues_v1.json` ; design : `../frame.md`.

## Assets

- {etat} Personnes reconnaissables : autorisations écrites et contrat RM Visual (usage publicitaire, recadrage)
  à confirmer avant diffusion.
- Musique : originale, synthétisée (`../tools/musique.py {v}`), 120 BPM ; effets sonores de la bibliothèque Pixabay
  de `media-use` (usage commercial sans attribution).
"""


def main():
    C = json.load(open(os.path.join(ICI, "cues_v1.json"), encoding="utf-8"))
    S = sources()
    Compo.film, Compo.plans = bool(S), C["film"]["plans"]
    print("Film :", ", ".join(f"{os.path.basename(s[0])} ({s[1]:g}–{s[1] + s[2]:.1f} s)" for s in S) if S else "absent → animatique")

    variantes = sys.argv[1:] or list(C["accroches"])
    jeux = {v: [(accroche(C, v), 0.0, 1), (etapes(C), C["etapes"][0]["t"], 1), (argument(C), C["cassure"][0], 1),
                (carte(C), C["carte"], 1), (bandeau(C), 0.0, 2)] for v in variantes}
    if S:
        if os.path.exists(COUPES):
            shutil.rmtree(COUPES)
        for f, (n, vit) in sorted(decouper(C, S, Compo.demandes).items()):
            note = "" if vit is None or vit >= 1 else f" (vitesse {vit:.2f}" + (", sous 0,6 : quelques images doublées)" if vit < 0.6 else ")")
            print(f"  plan {n:>2} → {f}{note}")

    for v in variantes:
        proj = os.path.join(RACINE, f"v1-{v}")
        D.squelette(proj, f"lecube-v1-{v}")
        comp = os.path.join(proj, "compositions")
        os.makedirs(comp, exist_ok=True)
        assets = os.path.join(proj, "assets")
        if os.path.exists(assets):
            shutil.rmtree(assets)
        for sous in ("fonts", "vendor"):           # polices (OFL) et GSAP 3.14.2 : ceux de la pub « LE CHRONO »
            shutil.copytree(os.path.join(D.POLICES_GSAP, sous), os.path.join(assets, sous))
        os.makedirs(os.path.join(assets, "audio"), exist_ok=True)
        if S:
            os.makedirs(os.path.join(assets, "video"))
            os.makedirs(os.path.join(assets, "img"))
            for f in os.listdir(COUPES):
                shutil.copy(os.path.join(COUPES, f), os.path.join(assets, "video" if f.endswith(".mp4") else "img"))
        son = os.path.join(RACINE, "_communs", f"musique_v1_{v}.wav")
        if os.path.exists(son):
            shutil.copy(son, os.path.join(assets, "audio", "musique.wav"))
        for c, _, _ in jeux[v]:
            open(os.path.join(comp, f"{c.cid}.html"), "w", encoding="utf-8").write(c.html())
        open(os.path.join(proj, "index.html"), "w", encoding="utf-8").write(index_html(v, C, [(c.cid, s, c.duree, p) for c, s, p in jeux[v]], bool(S)))
        open(os.path.join(proj, "BRIEF.md"), "w", encoding="utf-8").write(brief(C, v, bool(S)))
        print(f"construit {proj} : " + ", ".join(f"{c.cid} {r(s)}+{r(c.duree)}" for c, s, _ in jeux[v]))


if __name__ == "__main__":
    main()
