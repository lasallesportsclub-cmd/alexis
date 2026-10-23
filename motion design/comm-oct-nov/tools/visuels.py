"""Visuels typographiques des posts et stories LA SALLE et LE CUBE, octobre-novembre 2026.

Chaque visuel est une page HTML (polices du dépôt, aucune image, aucune personne) capturée par Chromium sans
interface : post 1080×1350 (4:5), story 1080×1920 (9:16, rien d'important dans les 250 px du haut et du bas).
Chartes (skill « lasalle-comm-hebdo ») :
  LA SALLE : noir #0A0A0A, blanc, gris #B0B0B0 et #707070, aucune couleur d'accent ; le trait penché du monogramme.
  LE CUBE  : noir #0A0A0A, texte #F5F2EC, bronze #B27639, aucun rouge.
  Oswald (titres), Inter (texte), Anton (chiffres) ; apostrophes typographiques.
Les textes sont ceux des fichiers S43 à S48 du kit « Comm LA SALLE et LE CUBE/Octobre-novembre 2026 ».
Un titre trop large pour sa ligne est réduit jusqu'à tenir (script « ajuste » dans la page).

Usage : python3 tools/visuels.py [préfixe…]   (par ex. S43 pour ne refaire qu'une semaine)
"""
import html
import re
import os
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.normpath(os.path.join(ICI, "..", ".."))
SORTIE = os.path.normpath(os.path.join(MOTION, "..", "Comm LA SALLE et LE CUBE", "Octobre-novembre 2026", "visuels"))
POLICES = os.path.join(MOTION, "lecube-chrono", "_communs", "assets", "fonts")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FORMATS = {"post": (1080, 1350), "story": (1080, 1920)}

MARQUES = {
    "LA SALLE": {"fond": "#0A0A0A", "texte": "#FFFFFF", "doux": "#D6D6D6", "gris": "#B0B0B0", "accent": "#FFFFFF",
                 "num": "#707070", "pied": "LA SALLE · URBAN VALLEY · CONFLANS-SAINTE-HONORINE"},
    "LE CUBE": {"fond": "#0A0A0A", "texte": "#F5F2EC", "doux": "rgba(245,242,236,.88)", "gris": "#B27639", "accent": "#B27639",
                "num": "#B27639", "pied": "LE CUBE · CONFLANS-SAINTE-HONORINE"},
}

FONTES = "".join(
    f'@font-face{{font-family:"{f}";font-weight:{w};src:url("file://{POLICES}/{n}") format("woff2");font-display:block}}'
    for f, w, n in (("Oswald", 600, "oswald-latin-600-normal.woff2"), ("Oswald", 700, "oswald-latin-700-normal.woff2"),
                    ("Inter", 400, "inter-latin-400-normal.woff2"), ("Inter", 600, "inter-latin-600-normal.woff2"),
                    ("Inter", 700, "inter-latin-700-normal.woff2"), ("Anton", 400, "anton-latin-400-normal.woff2")))


def esc(t):
    t = re.sub(r"(?<=\d{2}) (?=\d{2}\b)", "\u00a0", t)        # numéros de téléphone insécables
    return html.escape(t.replace("'", "’"), quote=False).replace(" ?", " ?").replace(" !", " !").replace(" :", " :")


def bloc(b, m):
    """Un bloc de contenu : (genre, texte, options)."""
    g, t = b[0], b[1] if len(b) > 1 else ""
    o = b[2] if len(b) > 2 else {}
    if g == "kicker":
        return f'<div class="kicker">{esc(t)}</div>'
    if g == "titre":
        lignes = "".join(f'<div class="ligne ajuste"{" style=color:" + m["accent"] if l.startswith("*") else ""}>{esc(l.lstrip("*"))}</div>'
                         for l in t.split("\n"))
        return f'<div class="titre" style="font-size:{o.get("taille", 118)}px">{lignes}</div>'
    if g == "num":
        return f'<div class="num">{esc(t)}</div>'
    if g == "trait":
        return '<div class="trait"></div>'
    if g == "oblique":   # le trait penché du monogramme LA SALLE, pente 0,42
        return (f'<svg class="oblique" width="152" height="66" viewBox="0 0 152 66"><line x1="3" y1="63" x2="149" y2="3" '
                f'stroke="{m["texte"]}" stroke-width="6" stroke-linecap="square"/></svg>')
    if g == "texte":
        return f'<div class="texte" style="font-size:{o.get("taille", 42)}px">{esc(t).replace(chr(10), "<br>")}</div>'
    if g == "grand":
        return f'<div class="grand ajuste" style="font-size:{o.get("taille", 150)}px">{esc(t)}</div>'
    if g == "espace":
        return f'<div style="height:{t}px"></div>'
    if g == "zone":   # place libre pour un sticker Instagram (sondage, quiz, question, compte à rebours)
        return f'<div style="height:{t}px"></div>'
    raise ValueError(g)


def page(v):
    m = MARQUES[v["marque"]]
    w, h = FORMATS[v["format"]]
    haut = 120 if v["format"] == "post" else 300
    bas = 96 if v["format"] == "post" else 300
    compteur = f'<div class="compteur">{v["compteur"]}</div>' if v.get("compteur") else ""
    pied = v.get("pied", m["pied"])
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{FONTES}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{w}px;height:{h}px;background:{m["fond"]};overflow:hidden}}
#v{{position:relative;width:{w}px;height:{h}px;color:{m["texte"]};font-family:Inter}}
.kicker{{font:600 28px/1.3 Inter;letter-spacing:.18em;text-transform:uppercase;color:{m["gris"]};margin-bottom:34px}}
.titre{{font-family:Oswald;font-weight:700;line-height:1.04;text-transform:uppercase;color:{m["texte"]}}}
.ligne{{white-space:nowrap}}
.num{{font:400 250px/0.9 Anton;color:{m["num"]};margin-bottom:26px}}
.trait{{width:120px;height:8px;background:{m["accent"]};margin:40px 0 44px}}
.oblique{{display:block;margin:44px 0 40px 4px}}
#contenu{{position:absolute;left:96px;right:96px;top:{haut}px;bottom:{bas + 110}px;display:flex;flex-direction:column;justify-content:center}}
.texte{{font-weight:400;line-height:1.38;color:{m["doux"]};margin-top:30px}}
.grand{{font:400 150px/1 Anton;color:{m["accent"]};white-space:nowrap;margin-top:34px}}
.compteur{{position:absolute;top:64px;right:96px;font:600 24px/1 Inter;letter-spacing:.12em;color:{m["gris"]}}}
.pied{{position:absolute;left:96px;right:96px;bottom:{bas}px;border-top:2px solid {m["gris"] if v["marque"] == "LE CUBE" else "#707070"};padding-top:26px;
  font:600 23px/1.3 Inter;letter-spacing:.16em;text-transform:uppercase;color:{m["gris"]}}}
</style></head><body><div id="v">{compteur}<div id="contenu">{"".join(bloc(b, m) for b in v["blocs"])}</div><div class="pied">{esc(pied)}</div></div>
<script>
document.fonts.ready.then(() => {{
  const max = {w} - 192;
  document.querySelectorAll('.ajuste').forEach(el => {{   // ligne sans retour : on réduit jusqu'à ce qu'elle tienne
    let fs = parseFloat(getComputedStyle(el).fontSize);
    while (el.scrollWidth > max + 1 && fs > 20) {{ fs -= 2; el.style.fontSize = fs + 'px'; }}
  }});
  document.body.setAttribute('data-pret', '1');
}});
</script></body></html>"""


def P(nom, marque, blocs, **k):
    return dict(nom=nom, marque=marque, format="post", blocs=blocs, **k)


def S(nom, marque, blocs, **k):
    return dict(nom=nom, marque=marque, format="story", blocs=blocs, **k)


LS, LC = "LA SALLE", "LE CUBE"
APPEL_LS = "Séance d'essai : venez à l'accueil, de 6h à 23h, 7 jours sur 7."
CUBE_TEL = "06 61 49 04 63"


def carrousel(prefixe, marque, slides, pied=None):
    n = len(slides)
    return [P(f"{prefixe}_post_{i + 1}", marque, b, compteur=f"{i + 1}/{n}", **({"pied": pied} if pied else {}))
            for i, b in enumerate(slides)]


VISUELS = []

# ───────── S43 ─────────
VISUELS += carrousel("S43_LA_SALLE", LS, [
    [("kicker", "Dimanche 25 octobre"), ("titre", "Heure d'hiver :\n5 astuces\npour garder\nle rythme", {"taille": 132}), ("oblique",),
     ("texte", "On gagne une heure de sommeil, pas une excuse.")],
    [("num", "01"), ("titre", "Venez dès 6h", {"taille": 112}), ("texte", "La salle est ouverte tous les jours, de 6h à 23h. Le matin, la séance est faite avant que la journée commence.")],
    [("num", "02"), ("titre", "Préparez votre\nsac la veille", {"taille": 112}), ("texte", "Tenue, serviette, gourde : le sac prêt près de la porte, c'est une excuse de moins.")],
    [("num", "03"), ("titre", "Réservez vos\ncours à l'avance", {"taille": 112}), ("texte", "Le dimanche soir, dans l'application La Salle Conflans : vos séances de la semaine sont calées.")],
    [("num", "04"), ("titre", "Entraînez-vous\nà deux", {"taille": 112}), ("texte", "Un rendez-vous pris à deux, on le tient. On se motive mutuellement.")],
    [("num", "05"), ("titre", "La régularité\navant l'intensité", {"taille": 112}), ("texte", "Trois séances tenues chaque semaine valent mieux qu'une semaine à fond, puis plus rien.")],
    [("kicker", "Vacances de la Toussaint"), ("titre", "Ouvert\n*de 6h à 23h,\n7 jours sur 7", {"taille": 132}), ("oblique",),
     ("texte", "Enregistrez ce post et dites-nous laquelle de ces astuces vous appliquez déjà.")],
])
VISUELS += [
    S("S43_LA_SALLE_story_1", LS, [("kicker", "Vacances de la Toussaint"), ("titre", "La salle\nreste ouverte", {"taille": 150}), ("oblique",),
                                   ("grand", "6H – 23H", {"taille": 190}), ("texte", "Tous les jours, jusqu'au 2 novembre.")]),
    S("S43_LA_SALLE_story_2", LS, [("kicker", "Petit sondage"), ("titre", "Et vous,\nvous êtes\nplutôt…", {"taille": 160}), ("zone", 520)]),
    S("S43_LA_SALLE_story_3", LS, [("kicker", "Dimanche 25 octobre"), ("titre", "On recule\nd'une heure.\n*Pas votre\n*séance.", {"taille": 160})]),
    P("S43_LE_CUBE_post", LC, [("kicker", "Boxing Club Conflans"), ("grand", "DE 50 À 400 M²", {"taille": 200}), ("trait",),
                               ("titre", "Le club change\nde dimension", {"taille": 120}), ("texte", "Nouveau studio au CUBE. Ouverture très bientôt.")],
      pied="BOXING CLUB CONFLANS · LE CUBE"),
    S("S43_LE_CUBE_story_1", LC, [("kicker", "Boxing Club Conflans"), ("titre", "50 m² hier.", {"taille": 150}), ("titre", "*400 m²\n*demain.", {"taille": 190})],
      pied="BOXING CLUB CONFLANS · LE CUBE"),
    S("S43_LE_CUBE_story_2", LC, [("kicker", "Nouveau studio de boxe"), ("titre", "Ouverture\n*très bientôt", {"taille": 160}), ("zone", 420)],
      pied="BOXING CLUB CONFLANS · LE CUBE"),
    S("S43_LE_CUBE_story_3", LC, [("kicker", "Question"), ("titre", "Tu as déjà\nboxé ?", {"taille": 180}), ("zone", 420)],
      pied="BOXING CLUB CONFLANS · LE CUBE"),
]

# ───────── S44 ─────────
VISUELS += [
    S("S44_LA_SALLE_story_1", LS, [("kicker", "Samedi 31 octobre"), ("titre", "Halloween :\nvenez\ndéguisés\nau cours", {"taille": 160}), ("oblique",)]),
    S("S44_LA_SALLE_story_2", LS, [("kicker", "Halloween"), ("titre", "Le costume\ndu coach ?\n*C'est vous\n*qui choisissez.", {"taille": 140}), ("zone", 380)]),
    S("S44_LA_SALLE_story_3", LS, [("kicker", "Pendant les vacances"), ("titre", "Ouvert", {"taille": 170}), ("grand", "6H – 23H", {"taille": 190}),
                                   ("texte", "Tous les jours, jusqu'au 2 novembre.")]),
    P("S44_LE_CUBE_post", LC, [("kicker", "Boxing Club Conflans · LE CUBE"), ("titre", "Le nouveau\nstudio est\nouvert.", {"taille": 150}), ("trait",),
                               ("titre", "*Premier round ?", {"taille": 120}), ("texte", f"Ton cours d'essai : {CUBE_TEL}")],
      pied="BOXING CLUB CONFLANS · LE CUBE"),
    S("S44_LE_CUBE_story_2", LC, [("kicker", "Le nouveau studio"), ("titre", "Tu préfères…", {"taille": 170}), ("zone", 520)],
      pied="BOXING CLUB CONFLANS · LE CUBE"),
    S("S44_LE_CUBE_story_3", LC, [("kicker", "Cours d'essai"), ("titre", "Premier\nround ?", {"taille": 190}), ("trait",), ("grand", CUBE_TEL, {"taille": 130})],
      pied="BOXING CLUB CONFLANS · LE CUBE"),
]

# ───────── S45 ─────────
VISUELS += [
    P("S45_LA_SALLE_post_1", LS, [("kicker", "Nouvelle série"), ("titre", "Coach\ndu mois", {"taille": 210}), ("oblique",),
                                  ("titre", "Novembre", {"taille": 96}), ("texte", "Derrière chaque séance réussie, il y a un coach.")]),
    S("S45_LA_SALLE_story_1", LS, [("kicker", "Novembre"), ("titre", "C'est\nMovember.", {"taille": 190}), ("oblique",),
                                   ("texte", "Le mois de la moustache, à la salle aussi.")]),
    S("S45_LA_SALLE_story_3", LS, [("kicker", "Nouvelle série"), ("titre", "Le coach\ndu mois\nest sur\nnotre post", {"taille": 160})]),
]
VISUELS += carrousel("S45_LE_CUBE", LC, [
    [("kicker", "CrossFit CSH · LE CUBE"), ("titre", "Débuter le\nCrossFit :", {"taille": 140}), ("trait",),
     ("titre", "*les 5 questions\n*que tout le monde\n*se pose", {"taille": 104})],
    [("num", "01"), ("titre", "Faut-il être\nen forme pour\ncommencer ?", {"taille": 104}), ("texte", "Non. Chaque mouvement s'adapte à ton niveau du jour.")],
    [("num", "02"), ("titre", "Je n'ai jamais\nsoulevé une barre.", {"taille": 104}), ("texte", "Le coach te montre chaque geste, pas à pas.")],
    [("num", "03"), ("titre", "J'ai une douleur\nou une ancienne\nblessure.", {"taille": 104}),
     ("texte", "Parles-en au coach avant la séance. En cas de doute, demande l'avis d'un professionnel de santé.")],
    [("num", "04"), ("titre", "Combien de\nséances par\nsemaine ?", {"taille": 104}), ("texte", "Commence par deux ou trois : la régularité avant l'intensité.")],
    [("num", "05"), ("titre", "Quelle formule\nchoisir ?", {"taille": 104}), ("texte", "Essentiel, Performance ou Illimité : on en parle à ta séance d'essai.")],
    [("kicker", "Séance d'essai"), ("titre", "Pas besoin\nd'être en forme\npour commencer.", {"taille": 112}), ("trait",),
     ("texte", "Réserve ta séance d'essai CrossFit CSH :"), ("grand", CUBE_TEL, {"taille": 120})],
], pied="CROSSFIT CSH · LE CUBE · CONFLANS")
VISUELS += [
    S("S45_LE_CUBE_story_2", LC, [("kicker", "Question"), ("titre", "Qu'est-ce qui\nte freine pour\nessayer ?", {"taille": 140}), ("zone", 460)],
      pied="CROSSFIT CSH · LE CUBE · CONFLANS"),
    S("S45_LE_CUBE_story_3", LC, [("kicker", "Séance d'essai CrossFit"), ("titre", "Pas besoin\nd'être en forme\npour commencer.", {"taille": 130}), ("trait",),
                                  ("grand", CUBE_TEL, {"taille": 130})], pied="CROSSFIT CSH · LE CUBE · CONFLANS"),
]

# ───────── S46 ─────────
COURS = [("BODYPUMP", "Renforcement musculaire avec barre et poids, en musique.", "Pour travailler la force, à votre rythme."),
         ("RPM", "Vélo en salle, en musique.", "Pour le cardio, en groupe."),
         ("LES MILLS SPRINT", "Fractionné sur vélo, court et intense.", "Pour se dépasser en peu de temps."),
         ("Cuisses-abdos-\nfessiers", "Renforcement ciblé du bas du corps et de la sangle abdominale.", ""),
         ("Pilates", "Renforcement en profondeur, posture et contrôle du mouvement.", ""),
         ("Stretching", "Étirements et souplesse, pour finir la semaine en douceur.", "")]
VISUELS += carrousel("S46_LA_SALLE", LS, [
    [("kicker", "Cours collectifs"), ("titre", "Cardio, force\nou souplesse :", {"taille": 120}), ("oblique",),
     ("titre", "quel cours\nest fait\npour vous ?", {"taille": 150})],
    *[[("kicker", "Cours collectif"), ("titre", nom, {"taille": 150}), ("oblique",), ("texte", d + ("\n" + pour if pour else ""), {"taille": 46})]
      for nom, d, pour in COURS],
    [("kicker", "Séance d'essai en cours collectif"), ("titre", "Trouvez\nle vôtre", {"taille": 170}), ("oblique",),
     ("grand", "07 60 71 27 89", {"taille": 120}), ("texte", "Planning dans l'application La Salle Conflans.")],
])
VISUELS += [
    S("S46_LA_SALLE_story_1", LS, [("kicker", "Mercredi 11 novembre"), ("titre", "La salle\nest ouverte", {"taille": 160}), ("grand", "6H – 23H", {"taille": 190})]),
    S("S46_LA_SALLE_story_2", LS, [("kicker", "Mercredi 11 novembre"), ("titre", "Le planning\ndes cours est\ndans l'appli", {"taille": 140}), ("oblique",),
                                   ("texte", "Application La Salle Conflans")]),
    S("S46_LA_SALLE_story_3", LS, [("kicker", "Quiz"), ("titre", "Quel cours\nêtes-vous ?", {"taille": 170}), ("zone", 520)]),
    P("S46_LE_CUBE_post_1", LC, [("kicker", "Novembre"), ("titre", "Athlète\ndu mois", {"taille": 210}), ("trait",),
                                 ("texte", "Ce mois-ci, on met en lumière l'un des nôtres.")], pied="CROSSFIT CSH · LE CUBE · CONFLANS"),
    S("S46_LE_CUBE_story_1", LC, [("kicker", "Cette semaine"), ("titre", "Les records\nde la semaine", {"taille": 160}), ("trait",)],
      pied="LE CUBE · CONFLANS-SAINTE-HONORINE"),
    S("S46_LE_CUBE_story_3", LC, [("kicker", "Question"), ("titre", "Ton record\ndu mois ?", {"taille": 180}), ("zone", 460)]),
]

# ───────── S47 ─────────
VISUELS += [
    P("S47_LA_SALLE_post", LS, [("kicker", "Venez à deux"), ("titre", "S'entraîner\nà deux,\nc'est plus\nfacile.", {"taille": 150}), ("oblique",),
                                ("texte", "Demandez votre invitation à l'accueil.")]),
    S("S47_LA_SALLE_story_1", LS, [("kicker", "Venez à deux"), ("titre", "Avec qui\nvoulez-vous\nvous entraîner ?", {"taille": 140}), ("zone", 420)]),
    S("S47_LA_SALLE_story_2", LS, [("kicker", "Venez à deux"), ("titre", "Votre\ninvitation\nvous attend\nà l'accueil.", {"taille": 160}), ("oblique",)]),
    P("S47_LE_CUBE_post", LC, [("kicker", "Pole Dance Conflans · LE CUBE"), ("titre", "Envie\nd'essayer\nla pole ?", {"taille": 150}), ("trait",),
                               ("titre", "*Ta séance d'essai\n*remboursée si\n*tu t'abonnes.", {"taille": 96}), ("texte", f"Réservation : {CUBE_TEL}")],
      pied="POLE DANCE CONFLANS · LE CUBE"),
    S("S47_LE_CUBE_story_2", LC, [("kicker", "Pole dance"), ("titre", "Tu\noserais ?", {"taille": 200}), ("zone", 460)], pied="POLE DANCE CONFLANS · LE CUBE"),
    S("S47_LE_CUBE_story_3", LC, [("kicker", "Séance d'essai pole"), ("titre", "Remboursée\nsi tu\nt'abonnes.", {"taille": 160}), ("trait",),
                                  ("grand", CUBE_TEL, {"taille": 130})], pied="POLE DANCE CONFLANS · LE CUBE"),
]

# ───────── S48 ─────────
VISUELS += [
    P("S48_LA_SALLE_post", LS, [("kicker", "Du 27 au 30 novembre"), ("titre", "Black\nFriday", {"taille": 220}), ("oblique",),
                                ("titre", "Vos frais de\ndossier offerts", {"taille": 104}),
                                ("texte", "Pour toute inscription avec engagement de 12 mois. À l'accueil, de 6h à 23h.", {"taille": 36})]),
    S("S48_LA_SALLE_story_1", LS, [("kicker", "Vendredi 27 novembre"), ("titre", "Le Black\nFriday se\npasse à\nla salle.", {"taille": 160}), ("zone", 360)]),
    S("S48_LA_SALLE_story_2", LS, [("kicker", "Black Friday"), ("titre", "C'est parti :", {"taille": 150}), ("titre", "frais de\ndossier\nofferts", {"taille": 170}),
                                   ("texte", "Jusqu'au lundi 30 novembre, à l'accueil. Engagement de 12 mois.")]),
    S("S48_LA_SALLE_story_3", LS, [("kicker", "Lundi 30 novembre"), ("titre", "Dernier\njour", {"taille": 210}), ("oblique",),
                                   ("texte", "Frais de dossier offerts jusqu'à 23h, à l'accueil. Engagement de 12 mois.")]),
    P("S48_LE_CUBE_post", LC, [("kicker", "Du 27 au 30 novembre"), ("titre", "Black Friday\nversion CUBE", {"taille": 140}), ("trait",),
                               ("grand", "0 €", {"taille": 230}), ("texte", "de frais de dossier sur les formules Essentiel, Performance et Illimité.")]),
    S("S48_LE_CUBE_story_1", LC, [("kicker", "Vendredi 27 novembre"), ("titre", "Black Friday\n*version CUBE", {"taille": 150}), ("zone", 420)]),
    S("S48_LE_CUBE_story_2", LC, [("kicker", "Quiz"), ("titre", "Quelle\nformule\npour toi ?", {"taille": 180}), ("zone", 520)]),
    S("S48_LE_CUBE_story_3", LC, [("kicker", "Lundi 30 novembre"), ("titre", "Dernier jour :", {"taille": 150}), ("grand", "0 €", {"taille": 260}),
                                  ("texte", "de frais de dossier. Ta séance d'essai : " + CUBE_TEL)]),
]


def capturer(v, tmp):
    w, h = FORMATS[v["format"]]
    src = os.path.join(tmp, v["nom"] + ".html")
    png = os.path.join(tmp, v["nom"] + ".png")
    open(src, "w", encoding="utf-8").write(page(v))
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={w},{h}", "--virtual-time-budget=3000", "--allow-file-access-from-files",
                    f"--screenshot={png}", "file://" + src], capture_output=True, check=True, timeout=60)
    jpg = os.path.join(SORTIE, v["nom"] + ".jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", png, "-q:v", "2", jpg], check=True)
    return jpg


def main():
    filtre = sys.argv[1:]
    os.makedirs(SORTIE, exist_ok=True)
    noms = [v["nom"] for v in VISUELS]
    assert len(noms) == len(set(noms)), "nom de visuel en double"
    with tempfile.TemporaryDirectory() as tmp:
        for v in VISUELS:
            if not filtre or any(v["nom"].startswith(f) for f in filtre):
                print(os.path.basename(capturer(v, tmp)))


if __name__ == "__main__":
    main()
