"""Génère les planches storyboard.html (esquisses statiques) et des PNG de contrôle.

Usage : python3 build_sheets.py [--png]
"""
import html
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import frames as F  # noqa: E402

MD = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SHARED = os.path.join(MD, "_sources-premium", "shared")
CHROME = os.path.expanduser(
    "~/.cache/hyperframes/chrome/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell")

CSS = open(os.path.join(SHARED, "premium.css"), encoding="utf-8").read()

# (id, fonction, titre, début, fin, note, raccord, format)
VIDEO = [
    ("A · 3 EN 1", [
        ("01", F.A1, "ACCROCHE", 0.0, 1.875, "<b>Image 0 :</b> le titre est déjà posé (lancé à −0,12 s) et le « + » or se trace. La pastille glisse à 0,3 s ; « PREMIUM. » prend le filet or quand la voix le dit.", "volet 3 bandes"),
        ("02", F.A2, "LES 3 BANDES", 1.875, 2.344, "<b>Un temps :</b> le trait ouvre l'écran en 3 bandes qui montrent les 3 avantages en même temps, de gauche à droite, décalées de 0,06 s.", "la bande 01 s'ouvre"),
        ("03", F.A3, "01 · FONTAINE", 2.344, 4.219, "<b>La bande 01 s'ouvre</b> plein cadre. « UNE BOISSON », puis « TOUTES LES 30 MINUTES. » sur la voix P5 ; l'aiguille trace le demi-tour de 30 min.", "volet vers 02"),
        ("04", F.A4, "02 · ANALYSE 3D", 4.219, 6.094, "<b>Le « 3D » en relief tourne</b> (rotation Y lente). « UNE ANALYSE EN 3D, » puis « CHAQUE SEMAINE. » sur P6 ; l'étiquette « 1 ANALYSE 3D PAR SEMAINE » se pose.", "volet vers 03"),
        ("05", F.A5, "03 · POSING (BIENTÔT)", 6.094, 7.5, "<b>Sans voix :</b> respiration sur la musique. « POSING » fantôme et son reflet de miroir ; « TRÈS BIENTÔT. » en or. La salle n'est jamais montrée.", "coupe sèche"),
    ]),
    ("FIN COMMUNE (A, B, C)", [
        ("06", F.F6a, "CASSURE", 7.5, 7.969, "<b>0,47 s de silence musical :</b> « ET EN CE MOMENT… » seul, en coupe sèche. Pas d'écran noir : le texte est là dès la première image.", "coupe sur le drop"),
        ("07", F.F6, "OFFRE", 7.969, 9.375, "<b>Réplique 25 :</b> ses groupes de mots défilent en haut (4 mots au plus) ; au drop (8,44 s), « OFFERTES » tombe en or avec son qualificatif, et le trait souligne.", "le bloc remonte"),
        ("08", F.F7, "PRIX", 9.375, 11.25, "<b>Le « + » or se trace</b>, « 2 € » frappe, puis « TTC PAR SEMAINE » et le qualificatif. La pastille revient en haut. Les mentions montent à 9,38 s et restent jusqu'à la fin.", "volet 3 bandes"),
        ("09", F.F8, "CARTE FINALE", 11.25, 14.933, "<b>Le monogramme s'assemble par ses 3 bandes</b> horizontales, puis « ACTIVEZ-LA À L'ACCUEIL, » et « EN QUELQUES SECONDES. » sur P9. Statique sur les 40 % finaux.", "fin"),
    ]),
    ("B · LA FONTAINE", [
        ("10", F.B1, "ACCROCHE", 0.0, 1.875, "<b>Image 0 :</b> « VOTRE BOISSON VOUS ATTEND. » posé, le « + » or ; la jauge or monte dans son cadre à droite, comme une gourde qui se remplit, sans illustration.", "volet vers 01"),
        ("11", F.B2, "01 · LES BOISSONS", 1.875, 5.156, "<b>P4 :</b> les boissons s'empilent une par une (4 mots au plus), puis « OU SIMPLEMENT / DE L'EAU. » les remplace. Les saveurs défilent à la verticale à droite.", "coupe"),
        ("12", F.B3, "30 MINUTES", 5.156, 6.563, "<b>P5 :</b> l'aiguille tracée par le trait fait son demi-tour pendant « TOUTES LES 30 MINUTES. »", "volet"),
        ("13", F.B4, "02 PUIS 03", 6.563, 7.5, "<b>Un temps chacun :</b> la bande 02 arrive, puis la 03. ⚠ B est le concept le plus chargé en voix : à recaler sur les vraies durées.", "fin commune"),
    ]),
    ("C · VOS PROGRÈS EN 3D", [
        ("14", F.C1, "ACCROCHE", 0.0, 1.875, "<b>Image 0 :</b> le « 3D » en relief tourne déjà ; « VOS PROGRÈS, EN 3D. » posé, le « + » or se trace.", "volet vers 02"),
        ("15", F.C2, "02 · ANALYSE 3D", 1.875, 4.688, "<b>P6</b> sur le relief qui pivote ; « 1 ANALYSE 3D PAR SEMAINE » se pose en étiquette.", "volet vers 03"),
        ("16", F.A5, "03 · POSING (BIENTÔT)", 4.688, 6.563, "<b>Même scène que A·05</b> : respiration sans voix, « TRÈS BIENTÔT. »", "volet vers 01"),
        ("17", F.C4, "01 · FONTAINE", 6.563, 7.5, "<b>Deux temps :</b> la bande 01 et « 1 BOISSON TOUTES LES 30 MIN », mini-horloge.", "fin commune"),
    ]),
]

VIS916 = [("IMAGES STORY 1080×1920", [
    ("01", F.S1, "VISUEL CLÉ A", None, None, "<b>3 EN 1 :</b> le titre, le « + », les 3 bandes, le CTA et les mentions. Zone sticker vide sous les mentions.", "—"),
    ("02", F.S2, "VISUEL CLÉ B", None, None, "<b>LA FONTAINE :</b> boissons et saveurs en toutes lettres, horloge des 30 min.", "—"),
    ("03", F.S3, "VISUEL CLÉ C", None, None, "<b>VOS PROGRÈS EN 3D :</b> relief typographique, une analyse par semaine.", "—"),
    ("04", F.S4, "CARTE OFFRE", None, None, "<b>Lancement du 13/10 :</b> « 4 SEMAINES OFFERTES » avec son qualificatif complet, le CTA et les mentions.", "—"),
])]

VIS45 = [("IMAGES POST 1080×1350", [
    ("01", F.P1, "VISUEL CLÉ A", None, None, "<b>Recomposé en 4:5</b>, pas recadré. Lisible en 3:4 et à 30 %.", "—"),
    ("02", F.P2, "VISUEL CLÉ B", None, None, "<b>La fontaine</b> en 4:5.", "—"),
    ("03", F.P3, "VISUEL CLÉ C", None, None, "<b>L'analyse 3D</b> en 4:5.", "—"),
]), ("CARROUSEL 5 SLIDES (trait or continu)", [
    ("04", F.K1, "SLIDE 1 · COUVERTURE", None, None, "<b>« PASSEZ EN VERSION PREMIUM. »</b> avec la pastille. Le trait or part sous le titre.", "trait → 2"),
    ("05", F.K2, "SLIDE 2 · FONTAINE", None, None, "<b>01 :</b> boissons, saveurs, une boisson toutes les 30 min.", "trait → 3"),
    ("06", F.K3, "SLIDE 3 · ANALYSE 3D", None, None, "<b>02 :</b> une analyse par semaine, pour suivre votre progression.", "trait → 4"),
    ("07", F.K4, "SLIDE 4 · POSING", None, None, "<b>03 :</b> citée, jamais montrée : « ARRIVE TRÈS BIENTÔT. »", "trait → 5"),
    ("08", F.K5, "SLIDE 5 · OFFRE", None, None, "<b>Offre, prix, CTA, mentions.</b> Le trait finit sous le CTA.", "fin"),
])]


def fmt_t(t):
    return f"{t:.2f}".replace(".", ",")


def cell(i, fid, fn, title, t0, t1, note, seam, p45):
    w = 300
    h = 375 if p45 else 533.33
    s = w / 1080
    tt = f"{fmt_t(t0)}–{fmt_t(t1)} s" if t0 is not None else "image fixe"
    return f"""
<figure class="cell">
  <div class="frame" id="frame-{fid}" style="width:{w}px;height:{h:.0f}px">
    <div class="fr{' p45' if p45 else ''}" style="transform:scale({s:.5f});transform-origin:0 0">{fn()}</div>
  </div>
  <figcaption>
    <div class="row"><span>{fid} · {html.escape(title)}</span><span>{tt}</span></div>
    <p>{note}</p>
    <span class="chip">{html.escape(seam)}</span>
  </figcaption>
</figure>"""


def sheet(title, dek, tag, acts, p45=False):
    body = []
    for act, items in acts:
        body.append(f'<h2 class="act">{html.escape(act)}</h2><div class="grid">')
        for it in items:
            body.append(cell(0, *it, p45=p45))
        body.append("</div>")
    tokens = """<div class="tokens"><h2 class="act">TOKENS</h2>
<div class="sw"><i style="background:#0D0D0D"></i>canvas #0D0D0D</div>
<div class="sw"><i style="background:#F4F1EC"></i>text #F4F1EC</div>
<div class="sw"><i style="background:#B8A07E"></i>gold #B8A07E (signature seulement)</div>
<div class="sw"><i style="background:#222"></i>surface #222 (bandes, mentions ; jamais du texte)</div>
<p>Barlow Condensed 900/800 en capitales · 800 italique : étiquettes, pastille, CTA · DM Sans 500 : texte et mentions ≥ 40 px.</p>
<p><b>Bans :</b> écran noir ou logo en ouverture, fondu, halo, dégradé, glitch, fausse interface, icône de personne, fruit dessiné, « fontaine à eau », « abonnement Premium », « gratuit », « offre limitée », tutoiement.</p>
<p>⚠ Logo provisoire (signature 170 px du Drive) en attendant <code>mono.png</code> et <code>word.png</code>.</p></div>"""
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>
{CSS}
body {{ margin:0; background:#161616; color:#F4F1EC; font-family:"DM Sans",sans-serif; padding:28px; }}
header h1 {{ font-family:"Barlow Condensed"; font-weight:900; font-size:44px; margin:0; text-transform:uppercase; }}
header p {{ margin:6px 0 0; color:rgba(244,241,236,.7); font-size:16px; }}
header .tag {{ display:inline-block; margin-top:10px; background:#B8A07E; color:#0D0D0D; font:800 italic 15px "Barlow Condensed"; padding:4px 12px; letter-spacing:.04em; }}
h2.act {{ font:800 italic 22px "Barlow Condensed"; letter-spacing:.06em; color:#B8A07E; margin:30px 0 12px; border-bottom:1px solid rgba(244,241,236,.18); padding-bottom:6px; }}
.grid {{ display:grid; grid-template-columns:repeat(4, 300px); gap:26px 22px; }}
.cell {{ margin:0; }}
.frame {{ overflow:hidden; outline:1px solid rgba(244,241,236,.18); }}
figcaption .row {{ display:flex; justify-content:space-between; font:800 14px "Barlow Condensed"; letter-spacing:.04em; margin-top:8px; text-transform:uppercase; }}
figcaption p {{ font-size:12.5px; line-height:1.35; margin:4px 0 6px; color:rgba(244,241,236,.82); }}
figcaption .chip {{ font:800 italic 11px "Barlow Condensed"; background:#222; padding:2px 8px; letter-spacing:.05em; text-transform:uppercase; }}
.tokens .sw {{ display:flex; align-items:center; gap:10px; font-size:14px; margin:6px 0; }}
.tokens i {{ width:28px; height:28px; display:inline-block; outline:1px solid rgba(244,241,236,.3); }}
.tokens p {{ font-size:13px; max-width:900px; }}
</style></head><body>
<header><h1>{html.escape(title)}</h1><p>{html.escape(dek)}</p><span class="tag">{html.escape(tag)}</span></header>
{''.join(body)}
{tokens}
</body></html>"""


def frame_page(fn, p45):
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{CSS} body{{margin:0;background:#0D0D0D}}</style></head>
<body><div class="fr{' p45' if p45 else ''}">{fn()}</div></body></html>"""


def shoot(html_path, png, w, h):
    subprocess.run([CHROME, "--no-sandbox", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={w},{h}", f"--screenshot={png}", "--virtual-time-budget=4000",
                    "--default-background-color=0D0D0DFF", "file://" + html_path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main(png=False):
    jobs = [
        ("premium-916", "Option Premium · vidéos 9:16 · v1", "Esquisses statiques des concepts A, B et C, et de la fin commune. Le build habille ces mises en page sans les redessiner.", "1080×1920 · 15 s · 30 i/s · 128 BPM · 17 cadres", VIDEO, False, "A"),
        ("premium-visuels-916", "Option Premium · images story · v1", "Visuels clés A, B, C et carte offre. PNG maîtres et JPG < 1 Mo.", "1080×1920 · 4 images", VIS916, False, None),
        ("premium-visuels-45", "Option Premium · images post · v1", "Visuels clés A, B, C et carrousel de 5 slides au trait continu.", "1080×1350 · 8 images", VIS45, True, None),
    ]
    for proj, title, dek, tag, acts, p45, sub in jobs:
        root = os.path.join(MD, proj)
        fonts_root = os.path.join(root, sub) if sub else root
        doc = sheet(title, dek, tag, acts, p45)
        if sub:  # la planche vidéo vit à la racine de premium-916 et lit les polices du projet A
            doc = doc.replace('url("assets/', f'url("{sub}/assets/').replace('src="assets/', f'src="{sub}/assets/')
        out = os.path.join(root, "storyboard.html")
        open(out, "w", encoding="utf-8").write(doc)
        print("écrit", out)
        if png:
            prev = os.path.join(fonts_root, ".hyperframes", "sketch-png")
            os.makedirs(prev, exist_ok=True)
            for act, items in acts:
                for fid, fn, t, *_ in items:
                    page = os.path.join(fonts_root, f".sketch-{fid}.html")
                    open(page, "w", encoding="utf-8").write(frame_page(fn, p45))
                    shoot(page, os.path.join(prev, f"{fid}.png"), 1080, 1350 if p45 else 1920)
                    os.remove(page)
            n_rows = sum((len(it) + 3) // 4 for _, it in acts)
            shoot(out, os.path.join(root, "storyboard.png"), 1330, 200 + n_rows * ((375 if p45 else 533) + 150) + 120 * len(acts) + 260)
            print("png", prev)


if __name__ == "__main__":
    main(png="--png" in sys.argv)
