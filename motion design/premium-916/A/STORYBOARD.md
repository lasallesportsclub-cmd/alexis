---
format: 1080x1920
duration: 14.933s
message: "Option Premium LA SALLE : fontaine, analyse 3D et salle de posing pour +2 € TTC/sem., à activer à l'accueil"
arc: Accroche → 3 avantages → cassure → offre → prix → carte finale
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
mode: collaborative
---

# Option Premium · concept A · plan v1

**Ce film dit aux adhérents de LA SALLE que l'option Premium (fontaine, analyse 3D, salle de posing bientôt) s'ajoute pour 2 € TTC par semaine, avec 4 semaines offertes en ce moment, et qu'on l'active à l'accueil.**

- **Spine** : une promesse (le « + »), trois preuves (les 3 bandes), une condition claire (offre + prix + mentions), une action (l'accueil).
- **Rythme** : 128 BPM (temps 0,469 s, mesure 1,875 s). Schéma `fast-fast-fast-HOLD-cut-SLAM-build-hold`. Une idée par temps.
- **Tokens** : canvas #0D0D0D, text #F4F1EC, gold #B8A07E, surface #222222 (source : `frame.md`, charte « Le Trait Oblique » v2). Barlow Condensed 800–900, DM Sans 500.
- **Atomes récurrents** : le « + » or (image 0, pastille, prix, carte finale), les 3 bandes obliques (une par avantage), le filet or.
- **Bans** : écran noir ou logo en ouverture, fondu enchaîné ou d'opacité, halo, dégradé, glitch, fausse interface, icône de personne, fruit dessiné, slideshow (plans immobiles qui se suivent) et screensaver (mouvement sans intention).
- **Held frame** : la carte finale, statique sur ses derniers 40 %.
- **Voix** : Nika, une seule voix, 5 répliques (P1, P5, P6, 25, P9). Durées **estimées** en attendant les fichiers ; la vraie durée d'une réplique décale la frontière suivante d'un temps au plus.
- **Son** : musique Sound Collection (en attente) creusée de 8 à 10 dB sous la voix (`carve.mjs --strength 0.4`) ; bruitages de la bibliothèque intégrée (whoosh-short sur chaque volet, impact-bass-1 sur le « + » et le drop, click sur les étiquettes). Version sans musique livrée.
- **Mentions** : panneau opaque de 9,38 s à la fin, texte de `mentionPremium`.

## Still open

- ⚠ Engagement : « sans engagement sur l'option » (Q2) contredit le calendrier S40 du Drive (« engagement d'un an sur l'option »).
- ⚠ Logo : `mono.png` et `word.png` attendus ; la carte finale assemble le monogramme par ses 3 bandes horizontales.
- ⚠ Réplique 25 (~3 s) : si elle ne tient pas entre 7,97 et 9,38 s, ses derniers mots passent sur le début du prix (le bloc offre reste à l'écran en pastille).

## Frame 1 — Accroche

- scene: « PASSEZ EN VERSION PREMIUM. » posé à l'image 0 (lancé à −0,12 s), le « + » or se trace, la pastille glisse à 0,3 s, le filet or souligne « PREMIUM. ».
- duration: 1.875s
- start: 0.000s
- poster: 1.2
- transition_in: cut
- status: built
- voiceover: P1 « Passez en version Premium. » (≈ 0,05–1,5 s)
- src: compositions/frames/01-accroche.html
- blueprint: kinetic-type-beats
- rules: kinetic-beat-slam, svg-path-draw, css-marker-patterns
- focal: le titre ; le « + » en second focal
- onscreen: « PASSEZ EN » « VERSION » « PREMIUM. » · pastille « 4 SEMAINES OFFERTES, PUIS 2 € TTC/SEM. »
- sfx: impact-bass-1 à 0,00 (son dès l'image 0) · click à 0,3 (pastille) · whoosh-short à 1,64 (volet)
- constraint: no black frame · no logo first · no fade
- sketch: ../storyboard.html#frame-01

La promesse et la signature sont lisibles même pour qui part à 1 s.

## Frame 2 — Les 3 bandes

- scene: Le trait ouvre l'écran en 3 bandes obliques décalées de 0,06 s : 01 FONTAINE À BOISSON SPORTIVE, 02 ANALYSE 3D, 03 SALLE DE POSING · BIENTÔT.
- duration: 0.469s
- start: 1.875s
- poster: 2.1
- transition_in: wipe
- status: built
- voiceover: onscreen
- src: compositions/frames/02-bandes.html
- blueprint: compose
- rules: gsap-effects (masked translate), css-marker-patterns
- focal: les trois bandes, égales
- onscreen: « 01 FONTAINE À BOISSON SPORTIVE » « 02 ANALYSE 3D » « 03 SALLE DE POSING · BIENTÔT »
- sfx: whoosh-short à 1,875
- constraint: no static hold over 1 beat
- sketch: ../storyboard.html#frame-02

Les trois avantages vus en même temps, dans l'ordre de la voix.

## Frame 3 — 01 · Fontaine

- scene: La bande 01 s'ouvre plein cadre. « UNE BOISSON » puis « TOUTES LES 30 MINUTES. » ; l'aiguille or trace le demi-tour de 30 min.
- duration: 1.875s
- start: 2.344s
- poster: 3.6
- transition_in: wipe
- status: built
- voiceover: P5 « Une boisson toutes les trente minutes. » (≈ 2,4–4,2 s)
- src: compositions/frames/03-fontaine.html
- blueprint: compose
- rules: svg-path-draw, waterfall-entry
- focal: « 30 MINUTES. » en or
- onscreen: « UNE BOISSON » → « TOUTES LES » « 30 MINUTES. » · étiquette « 01 FONTAINE À BOISSON SPORTIVE »
- sfx: click à 2,344 (étiquette) · whoosh-short à 4,0
- constraint: no « à volonté » · no fruit · no water-fountain wording
- sketch: ../storyboard.html#frame-03

La limite d'une boisson toutes les 30 min est dite clairement.

## Frame 4 — 02 · Analyse 3D

- scene: Le « 3D » en relief (couches empilées) tourne lentement. « UNE ANALYSE EN 3D, » puis « CHAQUE SEMAINE. » ; l'étiquette « 1 ANALYSE 3D PAR SEMAINE » se pose sous la bande.
- duration: 1.875s
- start: 4.219s
- poster: 5.6
- transition_in: wipe
- status: built
- voiceover: P6 « Une analyse en trois D, chaque semaine. » (≈ 4,3–6,3 s)
- src: compositions/frames/04-analyse.html
- blueprint: compose
- rules: 3d-text-depth-layers, waterfall-entry
- focal: le relief « 3D »
- onscreen: « UNE ANALYSE EN 3D, » → « CHAQUE » « SEMAINE. » · « Analyse de composition corporelle » · « 1 ANALYSE 3D PAR SEMAINE »
- sfx: click à 5,4 (étiquette) · whoosh-short à 5,9
- constraint: no fake scale screen · no body figure · no medical wording
- sketch: ../storyboard.html#frame-04

La fréquence (une par semaine) est posée à côté de la promesse.

## Frame 5 — 03 · Salle de posing (bientôt)

- scene: Respiration sans voix. « ARRIVE » / « TRÈS BIENTÔT. » en or et son reflet de miroir sous un filet ; « MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES ».
- duration: 1.406s
- start: 6.094s
- poster: 6.9
- transition_in: wipe
- status: built
- voiceover: aucune (musique seule)
- src: compositions/frames/05-posing.html
- blueprint: compose
- rules: css-marker-patterns, gsap-effects
- focal: « TRÈS BIENTÔT. »
- onscreen: « 03 SALLE DE POSING » « ARRIVE » « TRÈS BIENTÔT. » « MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES »
- sfx: sparkle très bas à 6,3 (reflet)
- constraint: no shot of the room · never « en retard »
- sketch: ../storyboard.html#frame-05

On cite la salle sans la présenter comme une preuve.

## Frame 6 — Cassure

- scene: Coupe sèche : « ET EN CE / MOMENT… » seul, musique coupée 0,47 s. La pastille disparaît.
- duration: 0.469s
- start: 7.500s
- poster: 7.7
- transition_in: cut
- status: built
- voiceover: aucune (silence musical)
- src: compositions/fin-commune.html
- blueprint: compose
- rules: kinetic-beat-slam
- focal: le texte seul
- onscreen: « ET EN CE MOMENT… »
- sfx: musique coupée · riser court avant le drop
- constraint: no black frame (le texte est là dès la première image)
- sketch: ../storyboard.html#frame-06

La cassure prépare l'offre.

## Frame 7 — Offre

- scene: Les groupes de mots de la 25 défilent en haut (4 mots au plus). Au drop (8,44 s), « 4 SEMAINES » puis « OFFERTES » en or frappent, le filet souligne, le qualificatif se pose.
- duration: 1.406s
- start: 7.969s
- poster: 9.0
- transition_in: cut
- status: built
- voiceover: 25 « Les 4 premières semaines de l'option Premium sont offertes. » (≈ 7,97–11,0 s)
- src: compositions/fin-commune.html
- blueprint: compose
- rules: kinetic-beat-slam, css-marker-patterns
- focal: « OFFERTES » en or
- onscreen: « LES 4 PREMIÈRES SEMAINES » → « DE L'OPTION PREMIUM » → « SONT OFFERTES. » · bloc « 4 SEMAINES OFFERTES » + « PUIS 2 € TTC/SEM. (8 € TOUTES LES 4 SEM.) »
- sfx: impact-bass-1 au drop (8,44)
- constraint: no « gratuit » · no « offre limitée » · qualifier ≥ 32 px in the same block
- sketch: ../storyboard.html#frame-07

Personne ne voit « OFFERTES » sans sa condition.

## Frame 8 — Prix

- scene: La pastille revient en haut. Le « + » or se trace, « 2 € » frappe, « TTC PAR SEMAINE », puis « SOIT 8 € TOUTES LES 4 SEM. · EN PLUS DE VOTRE ABONNEMENT » et le rappel « FONTAINE · ANALYSE 3D · POSING ». Le panneau des mentions monte à 9,38 s.
- duration: 1.875s
- start: 9.375s
- poster: 10.6
- transition_in: wipe
- status: built
- voiceover: suite de la 25
- src: compositions/fin-commune.html
- blueprint: compose
- rules: svg-path-draw, kinetic-beat-slam
- focal: le « + » et « 2 € »
- onscreen: « SONT OFFERTES. » · « +2 € » « TTC PAR SEMAINE » « SOIT 8 € TOUTES LES 4 SEM. » « EN PLUS DE VOTRE ABONNEMENT » · mentions
- sfx: impact-bass-1 sur le « + » (9,6) · whoosh-short à 11,0
- constraint: price never without its qualifier
- sketch: ../storyboard.html#frame-08

Le prix TTC, la cadence et « en plus de votre abonnement » arrivent ensemble.

## Frame 9 — Carte finale

- scene: Le monogramme s'assemble par ses 3 bandes horizontales, le mot-symbole se pose, « OPTION PREMIUM ». « ACTIVEZ-LA À L'ACCUEIL, » puis « EN QUELQUES SECONDES. » ; CTA « + ACTIVEZ-LA À L'ACCUEIL ». Statique sur les 40 % finaux.
- duration: 3.683s
- start: 11.250s
- poster: 13.5
- transition_in: wipe
- status: built
- voiceover: P9 « Activez-la à l'accueil, en quelques secondes. » (≈ 11,4–13,7 s)
- src: compositions/fin-commune.html
- blueprint: logo-assemble-lockup
- rules: gsap-effects, spring-pop-entrance
- focal: le logo puis le CTA
- onscreen: logo · « OPTION PREMIUM » · « ACTIVEZ-LA À L'ACCUEIL, » → « EN QUELQUES » « SECONDES. » · CTA · mentions
- sfx: whoosh-short sur chaque bande du logo (11,3 / 11,36 / 11,42) · impact-bass-1 à 11,6
- constraint: no chevron to a Meta button (organique) · no online sign-up
- sketch: ../storyboard.html#frame-09

On sait quoi faire et où : à l'accueil.

