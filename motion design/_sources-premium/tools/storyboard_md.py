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

# Option Premium · concept {concept} · plan v1

**Ce film dit aux adhérents de LA SALLE que l'option Premium (fontaine, analyse 3D, salle de posing bientôt) s'ajoute pour 2 € TTC par semaine, avec 4 semaines offertes en ce moment, et qu'on l'active à l'accueil.**

- **Spine** : une promesse (le « + »), trois preuves (les 3 bandes), une condition claire (offre + prix + mentions), une action (l'accueil).
- **Rythme** : 128 BPM (temps 0,469 s, mesure 1,875 s). Schéma `fast-fast-fast-HOLD-cut-SLAM-build-hold`. Une idée par temps.
- **Tokens** : canvas #0D0D0D, text #F4F1EC, gold #B8A07E, surface #222222 (source : `frame.md`, charte « Le Trait Oblique » v2). Barlow Condensed 800–900, DM Sans 500.
- **Atomes récurrents** : le « + » or (image 0, pastille, prix, carte finale), les 3 bandes obliques (une par avantage), le filet or.
- **Bans** : écran noir ou logo en ouverture, fondu enchaîné ou d'opacité, halo, dégradé, glitch, fausse interface, icône de personne, fruit dessiné, slideshow (plans immobiles qui se suivent) et screensaver (mouvement sans intention).
- **Held frame** : la carte finale, statique sur ses derniers 40 %.
- **Voix** : Nika, une seule voix, {n_vo} répliques ({vo_list}). Durées **estimées** en attendant les fichiers ; la vraie durée d'une réplique décale la frontière suivante d'un temps au plus.
- **Son** : musique Sound Collection (en attente) creusée de 8 à 10 dB sous la voix (`carve.mjs --strength 0.4`) ; bruitages de la bibliothèque intégrée (whoosh-short sur chaque volet, impact-bass-1 sur le « + » et le drop, click sur les étiquettes). Version sans musique livrée.
- **Mentions** : panneau opaque de 9,38 s à la fin, texte de `mentionPremium`.

## Still open

- ⚠ Engagement : « sans engagement sur l'option » (Q2) contredit le calendrier S40 du Drive (« engagement d'un an sur l'option »).
- ⚠ Logo : `mono.png` et `word.png` attendus ; la carte finale assemble le monogramme par ses 3 bandes horizontales.
- ⚠ Réplique 25 (~3 s) : si elle ne tient pas entre 7,97 et 9,38 s, ses derniers mots passent sur le début du prix (le bloc offre reste à l'écran en pastille).

"""

FRAMES_A = [
    (1, "Accroche", "compositions/frames/01-accroche.html", 0.0, 1.875, 1.2, "cut",
     "« PASSEZ EN VERSION PREMIUM. » posé à l'image 0 (lancé à −0,12 s), le « + » or se trace, la pastille glisse à 0,3 s, le filet or souligne « PREMIUM. ».",
     "P1 « Passez en version Premium. » (≈ 0,05–1,5 s)",
     "« PASSEZ EN » « VERSION » « PREMIUM. » · pastille « 4 SEMAINES OFFERTES, PUIS 2 € TTC/SEM. »",
     "kinetic-type-beats", "kinetic-beat-slam, svg-path-draw, css-marker-patterns", "le titre ; le « + » en second focal",
     "impact-bass-1 à 0,00 (son dès l'image 0) · click à 0,3 (pastille) · whoosh-short à 1,64 (volet)",
     "no black frame · no logo first · no fade", "La promesse et la signature sont lisibles même pour qui part à 1 s."),
    (2, "Les 3 bandes", "compositions/frames/02-bandes.html", 1.875, 2.344, 2.1, "wipe",
     "Le trait ouvre l'écran en 3 bandes obliques décalées de 0,06 s : 01 FONTAINE À BOISSON SPORTIVE, 02 ANALYSE 3D, 03 SALLE DE POSING · BIENTÔT.",
     "onscreen", "« 01 FONTAINE À BOISSON SPORTIVE » « 02 ANALYSE 3D » « 03 SALLE DE POSING · BIENTÔT »",
     "compose", "gsap-effects (masked translate), css-marker-patterns", "les trois bandes, égales",
     "whoosh-short à 1,875", "no static hold over 1 beat", "Les trois avantages vus en même temps, dans l'ordre de la voix."),
    (3, "01 · Fontaine", "compositions/frames/03-fontaine.html", 2.344, 4.219, 3.6, "wipe",
     "La bande 01 s'ouvre plein cadre. « UNE BOISSON » puis « TOUTES LES 30 MINUTES. » ; l'aiguille or trace le demi-tour de 30 min.",
     "P5 « Une boisson toutes les trente minutes. » (≈ 2,4–4,2 s)", "« UNE BOISSON » → « TOUTES LES » « 30 MINUTES. » · étiquette « 01 FONTAINE À BOISSON SPORTIVE »",
     "compose", "svg-path-draw, waterfall-entry", "« 30 MINUTES. » en or",
     "click à 2,344 (étiquette) · whoosh-short à 4,0", "no « à volonté » · no fruit · no water-fountain wording", "La limite d'une boisson toutes les 30 min est dite clairement."),
    (4, "02 · Analyse 3D", "compositions/frames/04-analyse.html", 4.219, 6.094, 5.6, "wipe",
     "Le « 3D » en relief (couches empilées) tourne lentement. « UNE ANALYSE EN 3D, » puis « CHAQUE SEMAINE. » ; l'étiquette « 1 ANALYSE 3D PAR SEMAINE » se pose sous la bande.",
     "P6 « Une analyse en trois D, chaque semaine. » (≈ 4,3–6,3 s)", "« UNE ANALYSE EN 3D, » → « CHAQUE » « SEMAINE. » · « Analyse de composition corporelle » · « 1 ANALYSE 3D PAR SEMAINE »",
     "compose", "3d-text-depth-layers, waterfall-entry", "le relief « 3D »",
     "click à 5,4 (étiquette) · whoosh-short à 5,9", "no fake scale screen · no body figure · no medical wording", "La fréquence (une par semaine) est posée à côté de la promesse."),
    (5, "03 · Salle de posing (bientôt)", "compositions/frames/05-posing.html", 6.094, 7.5, 6.9, "wipe",
     "Respiration sans voix. « ARRIVE » / « TRÈS BIENTÔT. » en or et son reflet de miroir sous un filet ; « MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES ».",
     "aucune (musique seule)", "« 03 SALLE DE POSING » « ARRIVE » « TRÈS BIENTÔT. » « MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES »",
     "compose", "css-marker-patterns, gsap-effects", "« TRÈS BIENTÔT. »",
     "sparkle très bas à 6,3 (reflet)", "no shot of the room · never « en retard »", "On cite la salle sans la présenter comme une preuve."),
]

FRAMES_SHARED = [
    (6, "Cassure", "compositions/fin-commune.html", 7.5, 7.969, 7.7, "cut",
     "Coupe sèche : « ET EN CE / MOMENT… » seul, musique coupée 0,47 s. La pastille disparaît.",
     "aucune (silence musical)", "« ET EN CE MOMENT… »", "compose", "kinetic-beat-slam", "le texte seul",
     "musique coupée · riser court avant le drop", "no black frame (le texte est là dès la première image)", "La cassure prépare l'offre."),
    (7, "Offre", "compositions/fin-commune.html", 7.969, 9.375, 9.0, "cut",
     "Les groupes de mots de la 25 défilent en haut (4 mots au plus). Au drop (8,44 s), « 4 SEMAINES » puis « OFFERTES » en or frappent, le filet souligne, le qualificatif se pose.",
     "25 « Les 4 premières semaines de l'option Premium sont offertes. » (≈ 7,97–11,0 s)",
     "« LES 4 PREMIÈRES SEMAINES » → « DE L'OPTION PREMIUM » → « SONT OFFERTES. » · bloc « 4 SEMAINES OFFERTES » + « PUIS 2 € TTC/SEM. (8 € TOUTES LES 4 SEM.) »",
     "compose", "kinetic-beat-slam, css-marker-patterns", "« OFFERTES » en or",
     "impact-bass-1 au drop (8,44)", "no « gratuit » · no « offre limitée » · qualifier ≥ 32 px in the same block", "Personne ne voit « OFFERTES » sans sa condition."),
    (8, "Prix", "compositions/fin-commune.html", 9.375, 11.25, 10.6, "wipe",
     "La pastille revient en haut. Le « + » or se trace, « 2 € » frappe, « TTC PAR SEMAINE », puis « SOIT 8 € TOUTES LES 4 SEM. · EN PLUS DE VOTRE ABONNEMENT » et le rappel « FONTAINE · ANALYSE 3D · POSING ». Le panneau des mentions monte à 9,38 s.",
     "suite de la 25", "« SONT OFFERTES. » · « +2 € » « TTC PAR SEMAINE » « SOIT 8 € TOUTES LES 4 SEM. » « EN PLUS DE VOTRE ABONNEMENT » · mentions",
     "compose", "svg-path-draw, kinetic-beat-slam", "le « + » et « 2 € »",
     "impact-bass-1 sur le « + » (9,6) · whoosh-short à 11,0", "price never without its qualifier", "Le prix TTC, la cadence et « en plus de votre abonnement » arrivent ensemble."),
    (9, "Carte finale", "compositions/fin-commune.html", 11.25, 14.933, 13.5, "wipe",
     "Le monogramme s'assemble par ses 3 bandes horizontales, le mot-symbole se pose, « OPTION PREMIUM ». « ACTIVEZ-LA À L'ACCUEIL, » puis « EN QUELQUES SECONDES. » ; CTA « + ACTIVEZ-LA À L'ACCUEIL ». Statique sur les 40 % finaux.",
     "P9 « Activez-la à l'accueil, en quelques secondes. » (≈ 11,4–13,7 s)",
     "logo · « OPTION PREMIUM » · « ACTIVEZ-LA À L'ACCUEIL, » → « EN QUELQUES » « SECONDES. » · CTA · mentions",
     "logo-assemble-lockup", "gsap-effects, spring-pop-entrance", "le logo puis le CTA",
     "whoosh-short sur chaque bande du logo (11,3 / 11,36 / 11,42) · impact-bass-1 à 11,6", "no chevron to a Meta button (organique) · no online sign-up", "On sait quoi faire et où : à l'accueil."),
]

FRAMES_B = [
    (1, "Accroche", "compositions/frames/01-accroche.html", 0.0, 1.875, 1.2, "cut",
     "« VOTRE BOISSON VOUS ATTEND. » posé à l'image 0, le « + » or ; la jauge or monte dans son cadre à droite, comme une gourde qui se remplit, sans illustration.",
     "P2 « Votre boisson vous attend. » (≈ 0,05–1,4 s)", "« VOTRE BOISSON » « VOUS ATTEND. » · pastille",
     "kinetic-type-beats", "stat-bars-and-fills, kinetic-beat-slam", "le titre",
     "remplissage synthétisé (bruit filtré) à 0,1 · impact-bass-1 à 0,00", "no fruit · no bottle drawing", "La fontaine devient une promesse personnelle."),
    (2, "01 · Les boissons", "compositions/frames/02-boissons.html", 1.875, 5.156, 4.6, "wipe",
     "Les boissons s'empilent une par une (4 mots au plus), puis « OU SIMPLEMENT / DE L'EAU. » les remplace. Les saveurs défilent à la verticale à droite.",
     "P4 « Collagène, multivitamines, L-carnitine, booster… ou simplement de l'eau. » (≈ 1,9–6,0 s)",
     "« COLLAGÈNE, » « MULTIVITAMINES, » « L-CARNITINE, » « BOOSTER… » → « OU SIMPLEMENT » « DE L'EAU. » · ticker « PASSION · PASTÈQUE · ICE TEA · ANANAS · MULTIFRUIT »",
     "compose", "waterfall-entry, vertical-spring-ticker", "la liste",
     "click sur chaque mot", "no effect claimed for any drink", "La variété, en toutes lettres."),
    (3, "30 minutes", "compositions/frames/03-trente.html", 5.156, 6.563, 6.3, "wipe",
     "L'aiguille tracée par le trait fait son demi-tour pendant « TOUTES LES 30 MINUTES. ».",
     "P5 « Une boisson toutes les trente minutes. » (≈ 5,2–7,0 s)", "« UNE BOISSON » → « TOUTES LES » « 30 MINUTES. »",
     "compose", "svg-path-draw, waterfall-entry", "« 30 MINUTES. » en or",
     "click", "no « à volonté »", "La règle d'usage est claire."),
    (4, "02 puis 03", "compositions/frames/04-bandes.html", 6.563, 7.5, 7.2, "wipe",
     "Un temps chacun : la bande « 02 ANALYSE 3D · 1 PAR SEMAINE », puis « 03 SALLE DE POSING · BIENTÔT ».",
     "aucune", "« 02 ANALYSE 3D · 1 PAR SEMAINE » « 03 SALLE DE POSING · BIENTÔT »",
     "compose", "gsap-effects", "les deux bandes",
     "whoosh-short ×2", "no static hold", "Le prix couvre les trois avantages : on les nomme tous."),
]

FRAMES_C = [
    (1, "Accroche", "compositions/frames/01-accroche.html", 0.0, 1.875, 1.2, "cut",
     "Le « 3D » en relief tourne déjà à l'image 0 ; « VOS PROGRÈS, EN 3D. » posé ; le « + » or se trace.",
     "P3 « Vos progrès, en trois D. » (≈ 0,05–1,4 s)", "« VOS PROGRÈS, » « EN 3D. » · pastille",
     "kinetic-type-beats", "3d-text-depth-layers, kinetic-beat-slam", "le relief « 3D »",
     "impact-bass-1 à 0,00", "no body figure · no before/after", "Le suivi de progression, sans promesse de résultat."),
    (2, "02 · Analyse 3D", "compositions/frames/02-analyse.html", 1.875, 4.688, 4.2, "wipe",
     "P6 sur le relief qui pivote ; « 1 ANALYSE 3D PAR SEMAINE » se pose en étiquette.",
     "P6 « Une analyse en trois D, chaque semaine. » (≈ 2,0–4,0 s)", "« UNE ANALYSE EN 3D, » → « CHAQUE » « SEMAINE. » · « Analyse de composition corporelle » · « 1 ANALYSE 3D PAR SEMAINE »",
     "compose", "3d-text-depth-layers, waterfall-entry", "le relief",
     "click", "no fake scale screen · no medical wording", "La fréquence est claire."),
    (3, "03 · Salle de posing (bientôt)", "compositions/frames/03-posing.html", 4.688, 6.563, 6.0, "wipe",
     "Même scène que A·05 : « ARRIVE TRÈS BIENTÔT. » et son reflet de miroir.",
     "aucune", "« 03 SALLE DE POSING » « ARRIVE » « TRÈS BIENTÔT. » « MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES »",
     "compose", "css-marker-patterns", "« TRÈS BIENTÔT. »",
     "sparkle très bas", "no shot of the room", "On cite la salle sans la montrer."),
    (4, "01 · Fontaine", "compositions/frames/04-fontaine.html", 6.563, 7.5, 7.2, "wipe",
     "Deux temps : la bande « 01 FONTAINE À BOISSON SPORTIVE » et « 1 BOISSON TOUTES LES 30 MIN », mini-horloge.",
     "aucune", "« 01 FONTAINE À BOISSON SPORTIVE » « 1 BOISSON TOUTES LES 30 MIN »",
     "compose", "gsap-effects, svg-path-draw", "la bande",
     "whoosh-short", "no « à volonté »", "Le troisième avantage, avec sa limite."),
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


write_video("A", FRAMES_A, "P1, P5, P6, 25, P9", 5, ["01", "02", "03", "04", "05", "06", "07", "08", "09"])
write_video("B", FRAMES_B, "P2, P4, P5, 25, P9", 5, ["10", "11", "12", "13", "06", "07", "08", "09"])
write_video("C", FRAMES_C, "P3, P6, 25, P9", 4, ["14", "15", "16", "17", "06", "07", "08", "09"])

IMG_HEAD = """---
format: {fmt}
duration: {dur}s
message: "Option Premium LA SALLE : fontaine, analyse 3D et salle de posing pour +2 € TTC/sem., à activer à l'accueil"
arc: images fixes, une scène figée d'une seconde par image
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
mode: collaborative
---

# Option Premium · {name} · plan v1

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
     "« VOTRE BOISSON VOUS ATTEND. » · « 01 FONTAINE À BOISSON SPORTIVE » · boissons · saveurs · « 1 BOISSON TOUTES LES 30 MIN » · CTA · mentions", "LA_SALLE_Premium_B_story_9x16"),
    ("Visuel clé C", "VOS PROGRÈS EN 3D : relief typographique, une analyse par semaine.",
     "« VOS PROGRÈS, EN 3D. » · « 02 ANALYSE 3D · 1 PAR SEMAINE » · « Analyse de composition corporelle. » · CTA · mentions", "LA_SALLE_Premium_C_story_9x16"),
    ("Carte offre", "Lancement du 13/10 : l'offre avec son qualificatif complet, le CTA et les mentions.",
     "« ET EN CE MOMENT… » « 4 SEMAINES OFFERTES » « PUIS 2 € TTC/SEM. (8 € TOUTES LES 4 SEM.) » « EN PLUS DE VOTRE ABONNEMENT » · CTA · mentions", "LA_SALLE_Premium_offre_story_9x16"),
])
write_images("premium-visuels-45", "1080x1350", "images post", [
    ("Visuel clé A", "Recomposé en 4:5.", "comme le visuel clé A story", "LA_SALLE_Premium_A_post_4x5"),
    ("Visuel clé B", "Recomposé en 4:5.", "comme le visuel clé B story", "LA_SALLE_Premium_B_post_4x5"),
    ("Visuel clé C", "Recomposé en 4:5.", "comme le visuel clé C story", "LA_SALLE_Premium_C_post_4x5"),
    ("Carrousel 1 · couverture", "« PASSEZ EN VERSION PREMIUM. », pastille ; le trait or part sous le titre.",
     "« PASSEZ EN VERSION PREMIUM. » · pastille · « FONTAINE · ANALYSE 3D · POSING » · mentions", "LA_SALLE_Premium_carrousel_1"),
    ("Carrousel 2 · fontaine", "01 : boissons, saveurs, une boisson toutes les 30 min.",
     "« 01 FONTAINE À BOISSON SPORTIVE » « VOTRE BOISSON VOUS ATTEND. » · boissons · saveurs · « 1 BOISSON TOUTES LES 30 MIN »", "LA_SALLE_Premium_carrousel_2"),
    ("Carrousel 3 · analyse 3D", "02 : une analyse par semaine, pour suivre votre progression.",
     "« 02 ANALYSE 3D » « VOS PROGRÈS, EN 3D. » « 1 ANALYSE 3D PAR SEMAINE » · « Analyse de composition corporelle, pour suivre votre progression. »", "LA_SALLE_Premium_carrousel_3"),
    ("Carrousel 4 · salle de posing", "03 : citée, jamais montrée.",
     "« 03 SALLE DE POSING » « ARRIVE TRÈS BIENTÔT. » « MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES »", "LA_SALLE_Premium_carrousel_4"),
    ("Carrousel 5 · offre", "Offre, prix, CTA, logo, mentions ; le trait finit sous le CTA.",
     "« ET EN CE MOMENT… » « 4 SEMAINES OFFERTES » + qualificatif · « +2 € TTC PAR SEMAINE » + qualificatif · CTA · logo · mentions", "LA_SALLE_Premium_carrousel_5"),
])
print("STORYBOARD.md écrits")
