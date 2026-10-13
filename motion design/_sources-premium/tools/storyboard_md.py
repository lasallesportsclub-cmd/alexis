"""Écrit les STORYBOARD.md des projets Premium (plan figé, une entrée ## Frame N par scène ou par image)."""
import os

MD = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

HEAD_VIDEO = """---
format: 1080x1920
duration: 14.933s
message: "Option Premium LA SALLE : fontaine, analyse 3D et salle de posing pour +2 € TTC/sem., à activer à l'accueil"
arc: Accroche → 3 avantages → cassure → offre → prix → carte finale
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
mode: collaborative
---

# Option Premium · concept {concept} · plan v2

**Ce film dit aux adhérents de LA SALLE que l'option Premium (fontaine, analyse 3D, salle de posing bientôt) s'ajoute pour 2 € TTC par semaine, en plus de leur abonnement, avec 4 semaines offertes en ce moment, et qu'on l'active à l'accueil.**

- **Spine** : une promesse (le « + »), trois preuves (les 3 bandes), une condition claire (offre, prix, mentions), une action (l'accueil).
- **Rythme** : 128 BPM (temps 0,469 s, mesure 1,875 s). Schéma `fast-fast-fast-HOLD-cut-SLAM-build-hold`. Une idée par temps ; plans de 0,94 à 1,88 s dans les preuves (une frontière peut glisser d'un temps).
- **Tokens** : canvas #0D0D0D, text #F4F1EC, gold #B8A07E, surface #222222 (source : `frame.md`, charte « Le Trait Oblique » v2). Barlow Condensed 800–900, DM Sans 500.
- **Atomes récurrents** : le « + » or (image 0 entier, pastille en négatif, prix, CTA), les 3 bandes obliques (numérotées dans l'ordre de la voix), le filet or.
- **Bans** : écran noir ou logo en ouverture, fondu enchaîné ou d'opacité, halo, dégradé, glitch, fausse interface (jauge, écran de balance), icône de personne, fruit dessiné, slideshow (plans immobiles qui se suivent) et screensaver (mouvement sans intention).
- **Held frame** : la carte finale, statique sur ses derniers 40 %.
- **Voix** : Nika, une seule voix, {n_vo} répliques ({vo_list}). Durées **estimées** ; toutes les bornes sont recalées sur les WAV.
- **Son** : musique Sound Collection (en attente) creusée de 8 à 10 dB sous la voix (`carve.mjs --strength 0.4`) ; bruitages de la bibliothèque intégrée (whoosh-short sur chaque volet, impact-bass-1 sur le « + » et le drop, click sur les étiquettes). Version sans musique livrée.
- **Pastille** : de 0,3 à 7,5 s, avec sa ligne « EN CE MOMENT · EN PLUS DE VOTRE ABONNEMENT » dans le même bloc.
- **Mentions** : un seul panneau sur son propre calque, au-dessus de toutes les transitions, en place à 9,375 s (glissement terminé à 9,375) et immobile jusqu'à 14,933 s.

## Still open

- ⚠ Engagement : « sans engagement sur l'option » (Q2) contredit le calendrier S40 du Drive (« engagement d'un an sur l'option »).
- ⚠ Écart au §6 : la réplique 25 finit par « offertes » (≈ 3 s). Le drop (8,44 s) frappe donc « LES 4 PREMIÈRES SEMAINES » et « OFFERTES » n'arrive en or, avec sa condition, que quand la voix le dit (≈ 10,0–10,4 s). Le prix suit sans voix, puis la carte finale ; bornes exactes sur le WAV.
- ⚠ Conséquence de l'écart 25 : prix 10,97–12,19 s (au lieu de 9,38–11,25) ; carte finale 12,19–14,933 s, soit 2,74 s au lieu de 3,68 s, statique dès 13,84 s ; P9 (≈ 12,3–14,5 s) doit avoir posé « EN QUELQUES SECONDES. » avant 13,84 s. Si la 25 est plus courte sur le WAV, le prix et la carte finale récupèrent le temps.
- ⚠ Pastille : ligne « EN CE MOMENT · EN PLUS DE VOTRE ABONNEMENT » ajoutée sous la version courte du §4 (le prix doit porter « en plus de votre abonnement » avant 9,38 s).
- ⚠ « + » de la pastille en négatif #0D0D0D (26 px), car un « + » or serait invisible sur la pastille or : écart au « + » or du §3, à valider.
- ⚠ Rappel « FONTAINE · ANALYSE 3D · POSING (BIENTÔT) » : « (BIENTÔT) » ajouté au rappel du §6 (Q3).
- ⚠ Voix IA (Nika) : activer l'étiquette IA de Meta à la publication des vidéos, avec et sans musique (décision de Mehdi).
- ⚠ P4 « booster » et « multivitamines » : à confirmer sur la fiche GYMWA (allégations nutritionnelles) ; proposition de repli : « caféine ».
- ⚠ Logo : `mono.png` et `word.png` attendus ; la carte finale assemble le monogramme par ses 3 bandes horizontales.

"""

FRAMES_A = [
    (1, "Accroche", "compositions/frames/01-accroche.html", 0.0, 1.875, 1.2, "cut",
     "« PASSEZ EN VERSION PREMIUM. » et le « + » or entiers à l'image 0 (frappe d'échelle lancée à −0,35 s, jamais d'opacité). La pastille et son qualificatif glissent à 0,3 s ; le filet or souligne « PREMIUM. » quand la voix le dit.",
     "P1 « Passez en version Premium. » (≈ 0,05–1,5 s)",
     "« PASSEZ EN » « VERSION » « PREMIUM. » · pastille « 4 SEMAINES OFFERTES, PUIS +2 € TTC/SEM. » + « EN CE MOMENT · EN PLUS DE VOTRE ABONNEMENT »",
     "kinetic-type-beats", "kinetic-beat-slam, css-marker-patterns", "le titre ; le « + » en second focal",
     "impact-bass-1 à 0,00 (son dès l'image 0) · click à 0,3 (pastille) · whoosh-short à 1,64 (volet)",
     "no black frame · no logo first · no fade", "La promesse et la signature sont lisibles même pour qui part à 1 s."),
    (2, "Volet 3 bandes (transition)", "compositions/frames/02-fontaine.html", 1.875, 2.344, 2.1, "wipe",
     "Transition d'un temps : le trait ouvre l'écran en 3 bandes obliques décalées de 0,06 s : 01 FONTAINE À BOISSON SPORTIVE, 02 ANALYSE 3D, 03 SALLE DE POSING · BIENTÔT. Reconnaissance, pas lecture ; la voix attend la bande 01.",
     "aucune (P5 démarre avec la bande 01)", "« 01 FONTAINE À BOISSON SPORTIVE » « 02 ANALYSE 3D » « 03 SALLE DE POSING · BIENTÔT » (étiquettes)",
     "compose", "gsap-effects (masked translate), css-marker-patterns", "les trois bandes, égales",
     "whoosh-short à 1,875", "no static hold over 1 beat", "Les trois avantages vus en même temps, dans l'ordre de la voix."),
    (3, "01 · Fontaine", "compositions/frames/02-fontaine.html", 2.344, 4.219, 3.8, "wipe",
     "La bande 01 s'ouvre. « UNE BOISSON » puis « TOUTES LES 30 MINUTES. » ; l'aiguille or trace le demi-tour de 30 min.",
     "P5 « Une boisson toutes les trente minutes. » (≈ 2,36–4,16 s)", "« UNE BOISSON » → « TOUTES LES » « 30 MINUTES. » · étiquette « 01 FONTAINE À BOISSON SPORTIVE »",
     "compose", "svg-path-draw, waterfall-entry", "« 30 MINUTES. » en or",
     "click à 2,344 (étiquette) · whoosh-short à 4,1", "no « à volonté » · no fruit · never « fontaine à eau »", "La limite d'une boisson toutes les 30 min est dite clairement."),
    (4, "02 · Analyse 3D (deux plans)", "compositions/frames/03-analyse.html", 4.219, 6.563, 6.0, "wipe",
     "Le « 3D » en relief (couches opaques) pivote lentement. Plan 4a (4,22–5,16) : « UNE ANALYSE » / « EN 3D, ». Plan 4b (5,16–6,56) : « CHAQUE » / « SEMAINE. » ; l'étiquette « 1 ANALYSE 3D PAR SEMAINE » se pose sous la bande.",
     "P6 « Une analyse en trois D, chaque semaine. » (≈ 4,25–6,25 s)", "« UNE ANALYSE EN 3D, » → « CHAQUE » « SEMAINE. » · « Analyse de composition corporelle » · « 1 ANALYSE 3D PAR SEMAINE »",
     "compose", "3d-text-depth-layers, waterfall-entry", "le relief « 3D »",
     "click à 5,2 (étiquette) · whoosh-short à 6,45", "no fake scale screen · no body figure · no medical wording", "La fréquence (une par semaine) est posée à côté de la promesse."),
    (5, "03 · Salle de posing (bientôt)", "compositions/frames/04-posing.html", 6.563, 7.5, 7.1, "wipe",
     "Respiration sans voix. « ARRIVE » / « TRÈS BIENTÔT. » en or et son reflet de miroir sous un filet ; « MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES ».",
     "aucune (musique seule)", "« 03 SALLE DE POSING » « ARRIVE » « TRÈS BIENTÔT. » « MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES »",
     "compose", "css-marker-patterns, gsap-effects", "« TRÈS BIENTÔT. »",
     "sparkle très bas à 6,7 (reflet)", "no shot of the room · never « en retard »", "On cite la salle sans la présenter comme une preuve."),
]

FRAMES_SHARED = [
    (6, "Cassure", "compositions/fin-commune.html", 7.5, 7.969, 7.7, "cut",
     "Coupe sèche : « ET EN CE / MOMENT… » seul, musique coupée 0,47 s. La pastille disparaît.",
     "aucune (silence musical)", "« ET EN CE MOMENT… »", "compose", "kinetic-beat-slam", "le texte seul",
     "musique coupée · riser court avant le drop", "no black frame (le texte est là dès la première image)", "La cassure prépare l'offre."),
    (7, "Offre", "compositions/fin-commune.html", 7.969, 10.97, 10.4, "cut",
     "« ET EN CE MOMENT… » se réduit en étiquette « EN CE MOMENT ». Groupes de la 25, 4 mots au plus, avec la voix : « LES 4 PREMIÈRES » entre en coupe à 7,969 s, « SEMAINES » frappe au drop (8,44 s) ; puis « DE L'OPTION PREMIUM » ; puis « SONT OFFERTES. » : « OFFERTES. » en or et le qualificatif « LES 4 PREMIÈRES SEMAINES DE L'OPTION » / « PUIS 2 € TTC/SEM. (8 € TOUTES LES 4 SEM.) » / « EN PLUS DE VOTRE ABONNEMENT » entrent dans la même image ; le filet souligne. Le panneau des mentions est en place à 9,375 s.",
     "25 « Les 4 premières semaines de l'option Premium sont offertes. » (≈ 7,97–10,97 s)",
     "« EN CE MOMENT » (étiquette) · « LES 4 PREMIÈRES SEMAINES » → « DE L'OPTION PREMIUM » → « SONT OFFERTES. » · qualificatif 40 px · mentions",
     "compose", "kinetic-beat-slam, css-marker-patterns", "« OFFERTES. » en or",
     "impact-bass-1 au drop (8,44) · click sur « OFFERTES »", "OFFERTES never without its condition in the same frame · no « gratuit » · no « offre limitée »", "Personne ne voit « OFFERTES » sans sa condition."),
    (8, "Prix", "compositions/fin-commune.html", 10.97, 12.19, 11.8, "wipe",
     "Sans voix. « PUIS », le « + » or se trace et « 2 € » frappe ; « TTC PAR SEMAINE » et « SOIT 8 € TOUTES LES 4 SEM. » / « EN PLUS DE VOTRE ABONNEMENT » sont déjà en place à la même image. Rappel « FONTAINE · ANALYSE 3D · POSING (BIENTÔT) ». Pas de pastille, pas de « OFFERTES ».",
     "aucune", "« PUIS » « +2 € » « TTC PAR SEMAINE » « SOIT 8 € TOUTES LES 4 SEM. » « EN PLUS DE VOTRE ABONNEMENT » « FONTAINE · ANALYSE 3D · POSING (BIENTÔT) » · mentions",
     "compose", "svg-path-draw, kinetic-beat-slam", "le « + » et « 2 € »",
     "impact-bass-1 sur le « + » (11,1) · whoosh-short à 12,1", "price never without its qualifier", "Le prix TTC, la cadence et « en plus de votre abonnement » arrivent ensemble."),
    (9, "Carte finale", "compositions/fin-commune.html", 12.19, 14.933, 13.9, "wipe",
     "Le monogramme s'assemble par ses 3 bandes horizontales, le mot-symbole se pose, « OPTION PREMIUM » hors zone de protection. CTA « + ACTIVEZ-LA À L'ACCUEIL » (68 px) sur le 1er groupe de P9, puis « EN QUELQUES SECONDES. ». Statique sur les 40 % finaux.",
     "P9 « Activez-la à l'accueil, en quelques secondes. » (≈ 12,3–14,5 s)",
     "logo · « OPTION PREMIUM » · « + ACTIVEZ-LA À L'ACCUEIL » · « EN QUELQUES SECONDES. » · mentions",
     "logo-assemble-lockup", "gsap-effects, spring-pop-entrance", "le CTA, puis le logo",
     "whoosh-short sur chaque bande du logo (12,2 / 12,26 / 12,32) · impact-bass-1 à 12,5", "no chevron to a Meta button (organique) · no online sign-up", "On sait quoi faire et où : à l'accueil."),
]

FRAMES_B = [
    (1, "Accroche", "compositions/frames/01-accroche.html", 0.0, 1.406, 1.1, "cut",
     "« VOTRE BOISSON VOUS ATTEND. » et le « + » or entiers à l'image 0 ; « BOISSON » se remplit d'or de bas en haut, bord net. Pastille à 0,3 s. Coupe à 1,41 s.",
     "P2 « Votre boisson vous attend. » (≈ 0,05–1,4 s)", "« VOTRE BOISSON » « VOUS ATTEND. » · pastille",
     "kinetic-type-beats", "stat-bars-and-fills (remplissage du mot), kinetic-beat-slam", "le titre",
     "remplissage synthétisé (bruit filtré) à 0,1 · impact-bass-1 à 0,00 · click à 0,3", "no gauge · no fruit · no bottle drawing", "La fontaine devient une promesse personnelle."),
    (2, "01 · Les boissons (deux plans)", "compositions/frames/02-boissons.html", 1.406, 4.219, 2.4, "wipe",
     "La bande 01 s'ouvre. Plan 2a (1,41–2,81) : « COLLAGÈNE, » / « MULTIVITAMINES, ». Plan 2b (2,81–4,22) : « L-CARNITINE, » / « BOOSTER… ». Un mot par temps ; bornes calées sur les pauses du WAV de P4.",
     "P4, début (≈ 1,45 s →)", "« COLLAGÈNE, » « MULTIVITAMINES, » → « L-CARNITINE, » « BOOSTER… » · étiquette « 01 FONTAINE À BOISSON SPORTIVE »",
     "compose", "waterfall-entry", "la liste", "click sur chaque mot", "no effect claimed for any drink", "La variété, en toutes lettres."),
    (3, "01 · De l'eau et les saveurs", "compositions/frames/03-eau.html", 4.219, 5.625, 5.0, "cut",
     "« OU SIMPLEMENT » / « DE L'EAU. » ; les saveurs défilent à la verticale dans une fenêtre d'une ligne, une à la fois, lettres droites (étiquette).",
     "P4, fin (→ ≈ 5,55 s)", "« OU SIMPLEMENT » « DE L'EAU. » · « SAVEUR · PASSION » → PASTÈQUE → ICE TEA → ANANAS → MULTIFRUIT",
     "compose", "waterfall-entry, vertical-spring-ticker", "« DE L'EAU. »", "click à chaque saveur", "one flavor visible at a time", "Les saveurs sont dites en toutes lettres."),
    (4, "30 minutes, puis 02 et 03", "compositions/frames/04-trente.html", 5.625, 7.5, 7.2, "wipe",
     "L'aiguille fait son demi-tour pendant « TOUTES LES 30 MINUTES. » ; sous la voix, la bande 02 entre à 6,56 s puis la 03 à 7,03 s (un temps chacune).",
     "P5 « Une boisson toutes les trente minutes. » (≈ 5,65–7,45 s)", "« UNE BOISSON » → « TOUTES LES » « 30 MINUTES. » · bandes « 02 ANALYSE 3D · 1 PAR SEMAINE » « 03 SALLE DE POSING · BIENTÔT »",
     "compose", "svg-path-draw, gsap-effects", "« 30 MINUTES. » en or", "whoosh-short à 6,56 et 7,03", "no « à volonté »", "La règle d'usage est claire ; les deux autres avantages sont nommés."),
]

FRAMES_C = [
    (1, "Accroche", "compositions/frames/01-accroche.html", 0.0, 1.875, 1.2, "cut",
     "Le « 3D » en relief tourne déjà à l'image 0 ; « VOS PROGRÈS, EN 3D. » et le « + » or entiers. Pastille à 0,3 s.",
     "P3 « Vos progrès, en trois D. » (≈ 0,05–1,4 s)", "« VOS PROGRÈS, » « EN 3D. » · pastille",
     "kinetic-type-beats", "3d-text-depth-layers, kinetic-beat-slam", "le relief « 3D »",
     "impact-bass-1 à 0,00 · click à 0,3", "no body figure · no before/after", "Le suivi de progression, sans promesse de résultat."),
    (2, "01 · Analyse 3D (deux plans)", "compositions/frames/02-analyse.html", 1.875, 4.688, 4.2, "wipe",
     "Plan 1 (1,88–3,28) : « UNE ANALYSE EN 3D, » sur le relief qui pivote. Plan 2 (3,28–4,69) : « CHAQUE SEMAINE. » et l'étiquette « 1 ANALYSE 3D PAR SEMAINE ».",
     "P6 « Une analyse en trois D, chaque semaine. » (≈ 2,0–4,0 s)", "« UNE ANALYSE EN 3D, » → « CHAQUE » « SEMAINE. » · « 01 ANALYSE 3D » · « Analyse de composition corporelle » · « 1 ANALYSE 3D PAR SEMAINE »",
     "compose", "3d-text-depth-layers, waterfall-entry", "le relief", "click", "no fake scale screen · no medical wording", "La fréquence est claire."),
    (3, "02 · Salle de posing (bientôt)", "compositions/frames/03-posing.html", 4.688, 6.563, 6.0, "wipe",
     "Même scène que A·05, numérotée 02 : « ARRIVE TRÈS BIENTÔT. » et son reflet de miroir.",
     "aucune", "« 02 SALLE DE POSING » « ARRIVE » « TRÈS BIENTÔT. » « MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES »",
     "compose", "css-marker-patterns", "« TRÈS BIENTÔT. »", "sparkle très bas", "no shot of the room", "On cite la salle sans la montrer."),
    (4, "03 · Fontaine", "compositions/frames/04-fontaine.html", 6.563, 7.5, 7.2, "wipe",
     "Deux temps : la bande « 03 FONTAINE À BOISSON SPORTIVE » et « 1 BOISSON TOUTES LES 30 MIN », mini-horloge.",
     "aucune", "« 03 FONTAINE À BOISSON SPORTIVE » « 1 BOISSON TOUTES LES 30 MIN »",
     "compose", "gsap-effects, svg-path-draw", "la bande", "whoosh-short", "no « à volonté »", "Le troisième avantage, avec sa limite."),
]


def block(n, title, src, t0, t1, poster, tin, scene, vo, onscreen, bp, rules, focal, sfx, constraint, why, sketch):
    return f"""## Frame {n} — {title}

- scene: {scene}
- duration: {t1 - t0:.3f}s
- start: {t0:.3f}s
- poster: {poster}
- transition_in: {tin}
- status: built
- voiceover: {vo}
- src: {src}
- blueprint: {bp}
- rules: {rules}
- focal: {focal}
- onscreen: {onscreen}
- sfx: {sfx}
- constraint: {constraint}
- sketch: {sketch}

{why}

"""


def write_video(concept, frames, vo_list, n_vo, sheet_ids):
    out = HEAD_VIDEO.format(concept=concept, vo_list=vo_list, n_vo=n_vo)
    allf = frames + [(len(frames) + 1 + i, *f[1:]) for i, f in enumerate(FRAMES_SHARED)]
    for f, sid in zip(allf, sheet_ids):
        out += block(*f, sketch=f"../storyboard.html#frame-{sid}")
    open(os.path.join(MD, "premium-916", concept, "STORYBOARD.md"), "w", encoding="utf-8").write(out)


write_video("A", FRAMES_A, "P1, P5, P6, 25, P9", 5, ["01", "02", "03", "04", "05", "06", "07+08", "09", "10"])
write_video("B", FRAMES_B, "P2, P4, P5, 25, P9", 5, ["11", "12", "13", "14", "06", "07+08", "09", "10"])
write_video("C", FRAMES_C, "P3, P6, 25, P9", 4, ["15", "16", "17", "18", "06", "07+08", "09", "10"])

IMG_HEAD = """---
format: {fmt}
duration: {dur}s
message: "Option Premium LA SALLE : fontaine, analyse 3D et salle de posing pour +2 € TTC/sem., à activer à l'accueil"
arc: images fixes, une scène figée d'une seconde par image
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
mode: collaborative
---

# Option Premium · {name} · plan v2

⚠ « + » de la pastille en négatif #0D0D0D (26 px), car un « + » or serait invisible sur la pastille or : écart au « + » or du §3, à valider.

Chaque image est une scène figée d'une seconde dans `index.html`, exportée par `npx hyperframes snapshot --at <milieu> --no-end`, puis convertie en JPG (qualité 90, sRGB, moins de 1 Mo). Tokens, bans et règles des prix : voir `frame.md`.

"""


def write_images(proj, fmt, name, items):
    out = IMG_HEAD.format(fmt=fmt, dur=len(items), name=name)
    for i, (title, desc, onscreen, fname) in enumerate(items):
        out += f"""## Frame {i + 1} — {title}

- scene: {desc}
- duration: 1s
- start: {i}s
- poster: {i + 0.5}
- status: built
- voiceover: onscreen
- src: compositions/frames/{i + 1:02d}.html
- onscreen: {onscreen}
- export: {fname}
- sketch: storyboard.html#frame-{i + 1:02d}

"""
    open(os.path.join(MD, proj, "STORYBOARD.md"), "w", encoding="utf-8").write(out)


write_images("premium-visuels-916", "1080x1920", "images story", [
    ("Visuel clé A", "3 EN 1 : titre, « + », 3 bandes, CTA, mentions ; zone sticker vide.",
     "« PASSEZ EN VERSION PREMIUM. » · pastille · bandes 01/02/03 · « ACTIVEZ-LA À L'ACCUEIL » · mentions", "LA_SALLE_Premium_A_story_9x16"),
    ("Visuel clé B", "LA FONTAINE : boissons et saveurs en toutes lettres, horloge des 30 min.",
     "« VOTRE BOISSON VOUS ATTEND. » · « 01 FONTAINE À BOISSON SPORTIVE » · boissons · saveurs · « 1 BOISSON TOUTES LES 30 MIN » · « AUSSI : ANALYSE 3D · SALLE DE POSING (BIENTÔT) » · CTA · mentions", "LA_SALLE_Premium_B_story_9x16"),
    ("Visuel clé C", "VOS PROGRÈS EN 3D : relief typographique, une analyse par semaine.",
     "« VOS PROGRÈS, EN 3D. » · « 01 ANALYSE 3D · 1 PAR SEMAINE » · « Analyse de composition corporelle. » · « AUSSI : FONTAINE · SALLE DE POSING (BIENTÔT) » · CTA · mentions", "LA_SALLE_Premium_C_story_9x16"),
    ("Carte offre", "Lancement du 13/10 : l'offre avec son qualificatif complet, le CTA et les mentions.",
     "logo · « OPTION PREMIUM » · « ET EN CE MOMENT… » « 4 SEMAINES OFFERTES » « PUIS 2 € TTC/SEM. (8 € TOUTES LES 4 SEM.) » « EN PLUS DE VOTRE ABONNEMENT » · CTA · mentions", "LA_SALLE_Premium_offre_story_9x16"),
])
write_images("premium-visuels-45", "1080x1350", "images post", [
    ("Visuel clé A", "Recomposé en 4:5.", "comme le visuel clé A story", "LA_SALLE_Premium_A_post_4x5"),
    ("Visuel clé B", "Recomposé en 4:5.", "comme le visuel clé B story", "LA_SALLE_Premium_B_post_4x5"),
    ("Visuel clé C", "Recomposé en 4:5.", "comme le visuel clé C story", "LA_SALLE_Premium_C_post_4x5"),
    ("Carrousel 1 · couverture", "« PASSEZ EN VERSION PREMIUM. », pastille ; le trait or part sous le titre.",
     "« PASSEZ EN VERSION PREMIUM. » · pastille + qualificatif · « FONTAINE · ANALYSE 3D · POSING (BIENTÔT) » · mentions", "LA_SALLE_Premium_carrousel_1"),
    ("Carrousel 2 · fontaine", "01 : boissons, saveurs, une boisson toutes les 30 min.",
     "« 01 FONTAINE À BOISSON SPORTIVE » « VOTRE BOISSON VOUS ATTEND. » · boissons · saveurs · « 1 BOISSON TOUTES LES 30 MIN »", "LA_SALLE_Premium_carrousel_2"),
    ("Carrousel 3 · analyse 3D", "02 : une analyse par semaine, pour suivre votre progression.",
     "« 02 ANALYSE 3D » « VOS PROGRÈS, EN 3D. » « 1 ANALYSE 3D PAR SEMAINE » · « Analyse de composition corporelle, pour suivre votre progression. »", "LA_SALLE_Premium_carrousel_3"),
    ("Carrousel 4 · salle de posing", "03 : citée, jamais montrée.",
     "« 03 SALLE DE POSING » « ARRIVE TRÈS BIENTÔT. » « MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES »", "LA_SALLE_Premium_carrousel_4"),
    ("Carrousel 5 · offre", "Un seul bloc offre + prix (à valider : il remplace la ligne « PUIS 2 € TTC/SEM. (8 € TOUTES LES 4 SEM.) ») ; le trait finit sous le CTA.",
     "« ET EN CE MOMENT… » « 4 SEMAINES OFFERTES » « DE L'OPTION PREMIUM » « PUIS » « +2 € TTC PAR SEMAINE » « SOIT 8 € TOUTES LES 4 SEM. » « EN PLUS DE VOTRE ABONNEMENT » · CTA · logo · mentions", "LA_SALLE_Premium_carrousel_5"),
])
print("STORYBOARD.md écrits")
