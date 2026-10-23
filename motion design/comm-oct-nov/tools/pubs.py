"""Pubs Meta typographiques de novembre 2026 : Black Friday (LA SALLE, LE CUBE) et cartes cadeaux (LA SALLE).

Une pub = un projet HyperFrames d'une seule composition (pubs/<id>/), 10 s, 9:16, 120 BPM, quatre cartes de 2,5 s
coupées sur le temps ; la première ligne est déjà posée à l'image 0. Aucune photo, aucune personne : seulement du
texte, dans la charte de chaque marque.
  LA SALLE : « Le Trait Oblique » des pubs (noir #0D0D0D, blanc cassé #F4F1EC, or taupe #B8A07E réservé à
             l'essentiel, Barlow Condensed 900 et DM Sans, trait penché du monogramme, logo en carte finale).
  LE CUBE  : noir #0A0A0A, texte #F5F2EC, bronze #B27639, Oswald, Inter, Anton ; « LE CUBE » écrit (pas de logo
             tant que le fichier officiel n'est pas fourni).
Musique originale synthétisée (instruments de ../../lecube-chrono/tools/musique.py, aucun morceau sous droits,
pas de MusicGen), calée sur les cartes ; −14 LUFS, crête vraie ≤ −1,5 dBTP après mastering.

Les offres (frais de dossier offerts du 27 au 30 novembre, engagement de 12 mois) reprennent la proposition du
calendrier de communication : ⚠ à valider par Mehdi avant toute diffusion.

Usage : ~/.venvs/hyperframes-audio/bin/python tools/pubs.py [id…]   (construit, rend, masterise et contrôle)
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, ".."))
MOTION = os.path.normpath(os.path.join(RACINE, ".."))
DEPOT = os.path.normpath(os.path.join(MOTION, ".."))
sys.path.insert(0, os.path.join(MOTION, "lecube-chrono", "tools"))
import musique as m  # noqa: E402  (instruments, limiteur, crête vraie ; 48 kHz)
sys.path.insert(0, os.path.join(MOTION, "_sources-premium", "tools"))
import master  # noqa: E402

HF = ["npx", "--yes", "hyperframes@0.8.181"]
DUREE, CARTE = 10.0, 2.5
NB = " "

CHARTES = {
    "LA SALLE": dict(fond="#0D0D0D", texte="#F4F1EC", accent="#B8A07E", doux="rgba(244,241,236,.78)",
                     titre="900 {t}px/0.92 'Barlow Condensed'", chiffre="900 {t}px/0.9 'Barlow Condensed'",
                     petit="500 {t}px/1.3 'DM Sans'", label="italic 800 {t}px/1 'Barlow Condensed'",
                     polices=[("Barlow Condensed", 800, "italic", "barlow-condensed-latin-800-italic.woff2"),
                              ("Barlow Condensed", 900, "normal", "barlow-condensed-latin-900-normal.woff2"),
                              ("DM Sans", 500, "normal", "dm-sans-latin-500-normal.woff2")],
                     dossier_polices=os.path.join(MOTION, "_sources-premium", "fonts"),
                     accords=["Dm", "Bb", "F", "C"]),
    "LE CUBE": dict(fond="#0A0A0A", texte="#F5F2EC", accent="#B27639", doux="rgba(245,242,236,.85)",
                    titre="700 {t}px/1.02 'Oswald'", chiffre="400 {t}px/0.9 'Anton'",
                    petit="600 {t}px/1.3 'Inter'", label="600 {t}px/1 'Oswald'",
                    polices=[("Oswald", 600, "normal", "oswald-latin-600-normal.woff2"),
                             ("Oswald", 700, "normal", "oswald-latin-700-normal.woff2"),
                             ("Inter", 600, "normal", "inter-latin-600-normal.woff2"),
                             ("Anton", 400, "normal", "anton-latin-400-normal.woff2")],
                    dossier_polices=os.path.join(MOTION, "lecube-chrono", "_communs", "assets", "fonts"),
                    accords=["Em", "C", "D", "Em"]),
}
NOTES = {"Dm": (38, [50, 57, 62, 65]), "Bb": (34, [46, 53, 58, 62]), "F": (41, [53, 57, 60, 65]), "C": (36, [48, 55, 60, 64]),
         "Em": (40, [52, 59, 64, 67]), "D": (38, [50, 57, 62, 66])}


def L(texte, top, taille=150, genre="titre", couleur="texte", dt=0.0, entree="frappe", centre=False):
    """Une ligne de texte d'une carte : genre titre | chiffre | petit | label ; dt = décalage d'entrée dans la carte."""
    return dict(texte=texte, top=top, taille=taille, genre=genre, couleur=couleur, dt=dt, entree=entree, centre=centre)


ADRESSE_LS = f"URBAN VALLEY{NB}·{NB}CONFLANS-SAINTE-HONORINE"
ADRESSE_LC = f"LE CUBE{NB}·{NB}8 RUE LÉONARD DE VINCI{NB}·{NB}CONFLANS"

PUBS = {
    "bf-lasalle": dict(
        marque="LA SALLE", titre="Black Friday LA SALLE", livraison=("Pub Meta LA SALLE", "Black Friday nov26"),
        fichier="LA_SALLE_Black_Friday_story_9x16.mp4", nom_meta="SALLE_BF_story_musique_v1",
        cartes=[
            [L("DU 27 AU 30 NOVEMBRE", 470, 46, "label", "accent"), L("BLACK", 560, 300), L("FRIDAY", 830, 300), "oblique:1130"],
            [L("VOS FRAIS", 470, 210), L("DE DOSSIER", 680, 210, dt=0.12), L("OFFERTS", 900, 250, couleur="accent", dt=0.25)],
            [L(f"1{NB}200{NB}M²", 470, 230, "chiffre"), L(f"MUSCULATION{NB}·{NB}CARDIO", 720, 96, dt=0.12),
             L("COURS COLLECTIFS", 830, 96, dt=0.24), L(f"6H{NB}–{NB}23H{NB}·{NB}7J/7", 970, 60, "label", "accent", dt=0.36)],
            [L("INSCRIVEZ-VOUS", 520, 150, centre=True), L("À L’ACCUEIL", 680, 150, couleur="accent", dt=0.12, centre=True),
             "chevron:860", L(ADRESSE_LS, 940, 40, "label", "doux", dt=0.25, centre=True),
             L("Offre valable du 27 au 30 novembre 2026 pour toute inscription avec engagement de 12 mois.",
               1040, 32, "petit", "doux", dt=0.4, entree="glisse", centre=True)],
        ],
        logo=True,
        attendus=["BLACK", "FRIDAY", "DU 27 AU 30 NOVEMBRE", "VOS FRAIS", "DE DOSSIER", "OFFERTS", "INSCRIVEZ-VOUS",
                  "À L’ACCUEIL", "engagement de 12 mois"]),
    "bf-lecube": dict(
        marque="LE CUBE", titre="Black Friday LE CUBE", livraison=("Pub Meta LE CUBE", "Black Friday nov26"),
        fichier="LE_CUBE_Black_Friday_story_9x16.mp4", nom_meta="CUBE_BF_story_musique_v1",
        cartes=[
            [L("DU 27 AU 30 NOVEMBRE", 470, 40, "label", "accent"), L("BLACK FRIDAY", 560, 170),
             L("VERSION CUBE", 750, 170, couleur="accent"), "trait:960"],
            [L("0 €", 440, 420, "chiffre", "accent"), L("DE FRAIS", 860, 130, dt=0.12), L("DE DOSSIER", 1000, 130, dt=0.24)],
            [L("CROSSFIT", 470, 150), L("HYROX", 630, 150, dt=0.12), L("BOXE", 790, 150, dt=0.24),
             L("POLE DANCE", 950, 150, couleur="accent", dt=0.36)],
            [L("TA SÉANCE", 500, 150, centre=True), L("D’ESSAI", 660, 150, couleur="accent", dt=0.12, centre=True),
             L(f"06{NB}61{NB}49{NB}04{NB}63", 840, 110, "chiffre", dt=0.24, centre=True), "chevron:980",
             L(ADRESSE_LC, 1060, 34, "label", "doux", dt=0.3, centre=True),
             L("Frais de dossier offerts du 27 au 30 novembre 2026 sur les formules Essentiel, Performance et Illimité.",
               1120, 30, "petit", "doux", dt=0.4, entree="glisse", centre=True)],
        ],
        logo=False,
        attendus=["BLACK FRIDAY", "VERSION CUBE", "0 €", "DE FRAIS", "DE DOSSIER", "CROSSFIT", "HYROX", "BOXE",
                  "POLE DANCE", "TA SÉANCE", "D’ESSAI", "06 61 49 04 63"]),
    "cadeaux-lasalle": dict(
        marque="LA SALLE", titre="Cartes cadeaux LA SALLE", livraison=("Pub Meta LA SALLE", "Cartes cadeaux nov26"),
        fichier="LA_SALLE_Cartes_cadeaux_story_9x16.mp4", nom_meta="SALLE_CADEAUX_story_musique_v1",
        cartes=[
            [L("À NOËL", 470, 46, "label", "accent"), L("OFFREZ", 560, 270), L("DU SPORT.", 820, 270), "oblique:1110"],
            [L("LA CARTE", 470, 220), L("CADEAU", 690, 220, couleur="accent", dt=0.12), L("LA SALLE", 910, 220, dt=0.24)],
            [L(f"1{NB}200{NB}M²", 470, 230, "chiffre"), L(f"MUSCULATION{NB}·{NB}CARDIO", 720, 96, dt=0.12),
             L("COURS COLLECTIFS", 830, 96, dt=0.24), L(f"6H{NB}–{NB}23H{NB}·{NB}7J/7", 970, 60, "label", "accent", dt=0.36)],
            [L("EN VENTE", 520, 160, centre=True), L("À L’ACCUEIL", 690, 160, couleur="accent", dt=0.12, centre=True),
             "chevron:880", L(ADRESSE_LS, 960, 40, "label", "doux", dt=0.25, centre=True)],
        ],
        logo=True,
        attendus=["OFFREZ", "DU SPORT.", "LA CARTE", "CADEAU", "EN VENTE", "À L’ACCUEIL"]),
}
INTERDITS = ["gratuit", "offre limitée", "inscription en ligne", "minceur", "brûle", "kilo", "détox", "avant/après",
             "abonnement premium", "garanti", "résultat"]


# ─────────────────────────── composition ───────────────────────────
def polices(c):
    return "".join(f'@font-face{{font-family:"{f}";font-weight:{w};font-style:{s};font-display:block;'
                   f'src:url("assets/fonts/{n}") format("woff2")}}\n' for f, w, s, n in c["polices"])


def esc(t):
    return html.escape(t.replace("'", "’"), quote=False).replace(" ?", NB + "?").replace(" :", NB + ":")


def composition(pid, P):
    c = CHARTES[P["marque"]]
    calques, js = [], []
    for k, carte in enumerate(P["cartes"]):
        t0 = k * CARTE
        corps = []
        for j, e in enumerate(carte):
            eid = f"c{k}e{j}"
            if isinstance(e, str):
                genre, y = e.split(":")
                y = int(y)
                if genre == "oblique":     # trait penché du monogramme, pente 0,42, en or
                    corps.append(f'<svg id="{eid}" class="a" style="left:96px;top:{y}px" width="190" height="84" viewBox="0 0 190 84">'
                                 f'<line x1="4" y1="80" x2="186" y2="4" stroke="{c["accent"]}" stroke-width="8" stroke-linecap="square"/></svg>')
                    js.append(f'tl.fromTo("#{eid}", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.2, ease: "power3.out" }}, {t0 + 0.2:g});')
                elif genre == "trait":
                    corps.append(f'<div id="{eid}" class="a" style="left:96px;top:{y}px;width:160px;height:10px;background:{c["accent"]};transform-origin:0 50%"></div>')
                    js.append(f'tl.fromTo("#{eid}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.2, ease: "power3.out" }}, {t0 + 0.2:g});')
                elif genre == "chevron":
                    corps.append(f'<svg id="{eid}" class="a" style="left:500px;top:{y}px" width="80" height="50" viewBox="0 0 80 50">'
                                 f'<polyline points="6,8 40,42 74,8" fill="none" stroke="{c["accent"]}" stroke-width="9" stroke-linecap="square"/></svg>')
                    js.append(f'tl.fromTo("#{eid}", {{ y: 0 }}, {{ y: 16, duration: 0.25, ease: "power1.inOut", yoyo: true, repeat: 3 }}, {t0 + 0.5:g});')
                continue
            police = c[e["genre"]].format(t=e["taille"])
            couleur = c[e["couleur"]]
            pos = "left:96px;width:888px;text-align:center" if e["centre"] else "left:96px"
            ecart = ";letter-spacing:.08em" if e["genre"] == "label" else ""
            casse = "" if e["genre"] == "petit" else ";text-transform:uppercase"
            blanc = ";white-space:normal;width:888px" if e["genre"] == "petit" else ";white-space:nowrap"
            corps.append(f'<div class="masque" style="{pos};top:{e["top"]}px"><div id="{eid}" class="ajuste" style="font:{police};'
                         f'color:{couleur}{ecart}{casse}{blanc}">{esc(e["texte"])}</div></div>')
            t = t0 + e["dt"]
            if k == 0 and e["dt"] == 0:
                continue                      # image 0 : la promesse est déjà posée, nette
            if e["entree"] == "glisse":
                js.append(f'tl.fromTo("#{eid}", {{ yPercent: 110 }}, {{ yPercent: 0, duration: 0.25, ease: "power3.out" }}, {t:g});')
            else:
                js.append(f'tl.fromTo("#{eid}", {{ scale: 1.22 }}, {{ scale: 1, duration: 0.18, ease: "power4.out" }}, {t:g});')
        if k == len(P["cartes"]) - 1 and P["logo"]:
            corps.insert(0, '<div class="a" style="left:0;width:1080px;top:330px;text-align:center">'
                            '<img id="logo-m" src="assets/img/mono.png" style="width:150px" alt=""/></div>')
            js.append(f'tl.fromTo("#logo-m", {{ scale: 1.3 }}, {{ scale: 1, duration: 0.2, ease: "power4.out" }}, {t0:g});')
        calques.append(f'<div id="carte{k}" class="clip" data-start="{t0:g}" data-duration="{CARTE:g}" data-track-index="{k % 2}">'
                       f'{"".join(corps)}</div>')
    marque = esc(P["marque"])
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/vendor/gsap.min.js"></script>
<style>
{polices(c)}* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {c["fond"]}; }}
#root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: {c["fond"]}; }}
.clip {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
.a {{ position: absolute; }}
.masque {{ position: absolute; overflow: hidden; padding: .1em 0 .06em; margin-top: -.1em; }}
#bandeau {{ position: absolute; left: 96px; top: 300px; font: {c["label"].format(t=34)}; letter-spacing: .2em; color: {c["doux"]}; text-transform: uppercase; }}
</style>
</head>
<body>
<!-- {esc(P["titre"])} · 9:16 · 10 s · 120 BPM. Généré par motion design/comm-oct-nov/tools/pubs.py -->
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUREE:g}" data-width="1080" data-height="1920" data-fps="30">
{chr(10).join(calques)}
<div id="cb" class="clip" data-start="0" data-duration="{3 * CARTE:g}" data-track-index="3"><div id="bandeau">{marque}{NB}·{NB}CONFLANS</div></div>
<audio id="musique" src="assets/audio/musique.wav" data-start="0" data-duration="{DUREE:g}" data-track-index="10" data-volume="1"></audio>
</div>
<script>
(function () {{
  // une ligne trop large pour le cadre (888 px) est réduite jusqu'à tenir, une fois les polices chargées
  // (la timeline n'anime que l'échelle et le glissement : elle ne dépend pas de ces tailles)
  document.fonts.ready.then(() => document.querySelectorAll(".ajuste").forEach((el) => {{
    if (getComputedStyle(el).whiteSpace !== "nowrap") return;
    let fs = parseFloat(getComputedStyle(el).fontSize);
    while (el.scrollWidth > 888 && fs > 20) {{ fs -= 2; el.style.fontSize = fs + "px"; }}
  }}));
  const tl = gsap.timeline({{ paused: true }});
  {(chr(10) + "  ").join(js)}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["main"] = tl;
}})();
</script>
</body>
</html>
"""


# ─────────────────────────── musique ───────────────────────────
def musique(P, sortie):
    c = CHARTES[P["marque"]]
    bat, basse, pad, fx = (m.stereo() for _ in range(4))
    GC, FR, CH = m.grosse_caisse(), m.frappe(), m.charley()
    n = int(DUREE / 0.5)
    for b in range(n):
        t = b * 0.5
        k = int(t // CARTE)
        if t >= DUREE - 0.5:
            break
        m.poser(bat, t, GC, 0.8)
        if b % 2 == 1:
            m.poser(bat, t, FR, 0.34, 0.05)
        m.poser(bat, t + 0.25, CH, 0.16, 0.25)
        racine = NOTES[c["accords"][k]][0]
        m.poser(basse, t, m.note_basse(racine, 0.42), 0.45)
    for k, a in enumerate(c["accords"]):
        m.poser(pad, k * CARTE, m.nappe(NOTES[a][1], CARTE + 0.2), 1.1)
        m.poser(fx, k * CARTE, m.impact(0.9 if k in (0, 3) else 0.6), 0.55 if k in (0, 3) else 0.4)
        if k:
            m.poser(fx, k * CARTE - 0.22, m.souffle(0.26, 0.2), 0.3)
    m.poser(fx, 0.0, m.crash(1.2), 0.3)
    m.poser(fx, 3 * CARTE, m.crash(1.4), 0.35)
    mix = bat * 0.9 + basse * 0.7 + pad * 1.1 + fx * 0.9
    mix = np.vstack([m.filtre(mix[i], "highpass", 32) for i in range(2)])[:, :int(DUREE * m.SR)]
    fondu = np.ones(mix.shape[1])
    i0 = int((DUREE - 0.4) * m.SR)
    fondu[i0:] = np.linspace(1, 0, mix.shape[1] - i0) ** 1.5
    x = mix * fondu
    mesure = pyln.Meter(m.SR)
    for _ in range(4):
        x *= 10 ** ((-14.0 - mesure.integrated_loudness(x.T)) / 20)
        x = m.limiteur(x)
        if abs(mesure.integrated_loudness(x.T) + 14.0) < 0.15:
            break
    tp = m.crete_vraie(x)
    if tp > -1.6:
        x *= 10 ** ((-1.6 - tp) / 20)
    sf.write(sortie, x.T, m.SR, subtype="PCM_24")


# ─────────────────────────── projet, rendu, livraison ───────────────────────────
def run(cmd, **k):
    p = subprocess.run(cmd, capture_output=True, text=True, **k)
    if p.returncode:
        sys.exit(f"Échec : {' '.join(cmd)}\n{p.stdout[-1500:]}\n{p.stderr[-1500:]}")
    return p.stdout


def construire(pid, P):
    proj = os.path.join(RACINE, "pubs", pid)
    if not os.path.exists(os.path.join(proj, "hyperframes.json")):
        os.makedirs(proj, exist_ok=True)
        modele = os.path.join(MOTION, "lecube-chrono", "A")
        for f in ("hyperframes.json", "AGENTS.md", "CLAUDE.md"):
            shutil.copy(os.path.join(modele, f), proj)
        paquet = json.load(open(os.path.join(modele, "package.json"), encoding="utf-8"))
        paquet["name"] = pid
        json.dump(paquet, open(os.path.join(proj, "package.json"), "w", encoding="utf-8"), indent=2)
        json.dump({"id": pid, "name": pid}, open(os.path.join(proj, "meta.json"), "w", encoding="utf-8"), indent=2)
    assets = os.path.join(proj, "assets")
    if os.path.exists(assets):
        shutil.rmtree(assets)
    c = CHARTES[P["marque"]]
    os.makedirs(os.path.join(assets, "fonts"))
    for *_, f in c["polices"]:
        shutil.copy(os.path.join(c["dossier_polices"], f), os.path.join(assets, "fonts"))
    shutil.copytree(os.path.join(MOTION, "lecube-chrono", "_communs", "assets", "vendor"), os.path.join(assets, "vendor"))
    os.makedirs(os.path.join(assets, "audio"))
    if P["logo"]:
        os.makedirs(os.path.join(assets, "img"))
        shutil.copy(os.path.join(MOTION, "lasalle-questions-avis", "assets", "img", "mono.png"), os.path.join(assets, "img"))
    musique(P, os.path.join(assets, "audio", "musique.wav"))
    open(os.path.join(proj, "index.html"), "w", encoding="utf-8").write(composition(pid, P))
    return proj


def texte_ecran(proj):
    h = open(os.path.join(proj, "index.html"), encoding="utf-8").read()
    h = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", " ", h, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h)).replace(NB, " "))


def livrer(pid, P, proj):
    out = run(HF + ["check", "--timeout", "60000"], cwd=proj)
    erreurs = re.search(r"(\d+) error\(s\)", out)
    run(HF + ["render", "--quality", "delivery", "-o", "renders/video.mp4"], cwd=proj)
    dossier = os.path.join(DEPOT, *P["livraison"])
    os.makedirs(os.path.join(dossier, "controles"), exist_ok=True)
    video = os.path.join(dossier, P["fichier"])
    with tempfile.TemporaryDirectory() as tmp:
        remix = os.path.join(tmp, "remix.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(proj, "renders", "video.mp4"), "-i", os.path.join(proj, "assets", "audio", "musique.wav"),
             "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-t", f"{DUREE:g}", remix])
        master.main(remix, video, DUREE)
        # aperçu HyperFrames et rendu décodé aux mêmes instants (une image par carte, en tenue)
        instants = [k * CARTE + 2.0 for k in range(4)]
        run(HF + ["snapshot", "--at", ",".join(f"{t:g}" for t in instants), "--no-end", "-o", tmp, "--timeout", "60000", proj])
        pngs = sorted(f for f in os.listdir(tmp) if f.startswith("frame-") and f.endswith(".png"))
        scores = []
        for f, t in zip(pngs, instants):
            r = subprocess.run(["ffmpeg", "-nostats", "-ss", f"{t:g}", "-i", video, "-i", os.path.join(tmp, f), "-frames:v", "1",
                                "-lavfi", "[0:v][1:v]ssim", "-f", "null", "-"], capture_output=True, text=True)
            s = re.search(r"All:([0-9.]+)", r.stderr)
            scores.append(float(s.group(1)) if s else 0.0)
    p = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_type,codec_name,profile,width,height,r_frame_rate,pix_fmt",
                        "-of", "json", video]))
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    duree, taille = float(p["format"]["duration"]), int(p["format"]["size"]) / 1e6
    i, tp = master.controle(video)
    t = texte_ecran(proj)
    absents = [a for a in P["attendus"] if a.replace(NB, " ") not in t]
    interdits = [a for a in INTERDITS if a in t.lower()]
    tests = [
        ("Format 1080×1920, H.264 High, 30 i/s", v["width"] == 1080 and v["height"] == 1920 and v.get("profile") == "High" and v["r_frame_rate"] == "30/1"),
        (f"Durée {duree:.2f} s (9,9–10,0)", 9.9 <= duree <= 10.0),
        (f"Poids {taille:.1f} Mo (≤ 25)", taille <= 25),
        (f"Sonie {i:.1f} LUFS (−14 ± 0,5)", abs(i + 14) <= 0.5),
        (f"Crête vraie {tp:.1f} dBTP (≤ −1,5)", tp <= -1.5),
        (f"HyperFrames check : {erreurs.group(1) if erreurs else '?'} erreur", bool(erreurs) and erreurs.group(1) == "0"),
        (f"Rendu décodé = aperçu (SSIM mini {min(scores):.3f} ≥ 0,97)", len(scores) == 4 and min(scores) >= 0.97),
        ("Textes attendus présents" + (f" (absents : {absents})" if absents else ""), not absents),
        ("Aucun mot interdit" + (f" (trouvés : {interdits})" if interdits else ""), not interdits),
    ]
    vf = ("fps=2,drawbox=x=0:y=0:w=1080:h=270:color=red@0.25:t=fill,drawbox=x=0:y=1250:w=1080:h=670:color=red@0.25:t=fill,"
          "drawbox=x=950:y=900:w=130:h=1020:color=red@0.25:t=fill,scale=216:384,tile=10x2")
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", vf, "-frames:v", "1", "-q:v", "3", os.path.join(dossier, "controles", f"planche_{pid}_2ips.jpg")])
    lignes = [f"QC — {P['fichier']} (nom Meta : {P['nom_meta']})", *(f"{'OK ' if ok else 'NON'}  {n}" for n, ok in tests),
              f"Verdict : {'GO technique' if all(ok for _, ok in tests) else 'À CORRIGER'}",
              "Reste à valider par Mehdi : l'offre et ses conditions (⚠), puis l'écoute de la musique."]
    open(os.path.join(dossier, "controles", f"QC_{pid}.txt"), "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print("\n".join(lignes) + "\n")


def main():
    for pid in sys.argv[1:] or list(PUBS):
        P = PUBS[pid]
        livrer(pid, P, construire(pid, P))


if __name__ == "__main__":
    main()
