---
format: 1080x1920
duration: 14.933s
message: "Option Premium LA SALLE : fontaine, analyse 3D et salle de posing pour +2 € TTC/sem., à activer à l'accueil"
arc: Accroche → 3 avantages → cassure → offre → prix → carte finale
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
mode: collaborative
---

# Option Premium · concept C · plan v2

**Ce film dit aux adhérents de LA SALLE que l'option Premium (fontaine, analyse 3D, salle de posing bientôt) s'ajoute pour 2 € TTC par semaine, en plus de leur abonnement, avec 4 semaines offertes en ce moment, et qu'on l'active à l'accueil.**

- **Spine** : une promesse (le « + »), trois preuves (les 3 bandes), une condition claire (offre, prix, mentions), une action (l'accueil).
- **Rythme** : 128 BPM (temps 0,469 s, mesure 1,875 s). Schéma `fast-fast-fast-HOLD-cut-SLAM-build-hold`. Une idée par temps ; plans de 0,94 à 1,88 s dans les preuves (une frontière peut glisser d'un temps).
- **Tokens** : canvas #0D0D0D, text #F4F1EC, gold #B8A07E, surface #222222 (source : `frame.md`, charte « Le Trait Oblique » v2). Barlow Condensed 800–900, DM Sans 500.
- **Atomes récurrents** : le « + » or (image 0 entier, pastille en négatif, prix, CTA), les 3 bandes obliques (numérotées dans l'ordre de la voix), le filet or.
- **Bans** : écran noir ou logo en ouverture, fondu enchaîné ou d'opacité, halo, dégradé, glitch, fausse interface (jauge, écran de balance), icône de personne, fruit dessiné, slideshow (plans immobiles qui se suivent) et screensaver (mouvement sans intention).
- **Held frame** : la carte finale, statique sur ses derniers 40 %.
- **Voix** : Nika, une seule voix, 4 répliques (P3, P6, 25, P9). Durées **estimées** ; toutes les bornes sont recalées sur les WAV.
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

## Frame 1 — Accroche

- scene: Le « 3D » en relief tourne déjà à l'image 0 ; « VOS PROGRÈS, EN 3D. » et le « + » or entiers. Pastille à 0,3 s.
- duration: 1.875s
- start: 0.000s
- poster: 1.2
- transition_in: cut
- status: built
- voiceover: P3 « Vos progrès, en trois D. » (≈ 0,05–1,4 s)
- src: compositions/frames/01-accroche.html
- blueprint: kinetic-type-beats
- rules: 3d-text-depth-layers, kinetic-beat-slam
- focal: le relief « 3D »
- onscreen: « VOS PROGRÈS, » « EN 3D. » · pastille
- sfx: impact-bass-1 à 0,00 · click à 0,3
- constraint: no body figure · no before/after
- sketch: ../storyboard.html#frame-15

Le suivi de progression, sans promesse de résultat.

## Frame 2 — 01 · Analyse 3D (deux plans)

- scene: Plan 1 (1,88–3,28) : « UNE ANALYSE EN 3D, » sur le relief qui pivote. Plan 2 (3,28–4,69) : « CHAQUE SEMAINE. » et l'étiquette « 1 ANALYSE 3D PAR SEMAINE ».
- duration: 2.813s
- start: 1.875s
- poster: 4.2
- transition_in: wipe
- status: built
- voiceover: P6 « Une analyse en trois D, chaque semaine. » (≈ 2,0–4,0 s)
- src: compositions/frames/02-analyse.html
- blueprint: compose
- rules: 3d-text-depth-layers, waterfall-entry
- focal: le relief
- onscreen: « UNE ANALYSE EN 3D, » → « CHAQUE » « SEMAINE. » · « 01 ANALYSE 3D » · « Analyse de composition corporelle » · « 1 ANALYSE 3D PAR SEMAINE »
- sfx: click
- constraint: no fake scale screen · no medical wording
- sketch: ../storyboard.html#frame-16

La fréquence est claire.

## Frame 3 — 02 · Salle de posing (bientôt)

- scene: Même scène que A·05, numérotée 02 : « ARRIVE TRÈS BIENTÔT. » et son reflet de miroir.
- duration: 1.875s
- start: 4.688s
- poster: 6.0
- transition_in: wipe
- status: built
- voiceover: aucune
- src: compositions/frames/03-posing.html
- blueprint: compose
- rules: css-marker-patterns
- focal: « TRÈS BIENTÔT. »
- onscreen: « 02 SALLE DE POSING » « ARRIVE » « TRÈS BIENTÔT. » « MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES »
- sfx: sparkle très bas
- constraint: no shot of the room
- sketch: ../storyboard.html#frame-17

On cite la salle sans la montrer.

## Frame 4 — 03 · Fontaine

- scene: Deux temps : la bande « 03 FONTAINE À BOISSON SPORTIVE » et « 1 BOISSON TOUTES LES 30 MIN », mini-horloge.
- duration: 0.937s
- start: 6.563s
- poster: 7.2
- transition_in: wipe
- status: built
- voiceover: aucune
- src: compositions/frames/04-fontaine.html
- blueprint: compose
- rules: gsap-effects, svg-path-draw
- focal: la bande
- onscreen: « 03 FONTAINE À BOISSON SPORTIVE » « 1 BOISSON TOUTES LES 30 MIN »
- sfx: whoosh-short
- constraint: no « à volonté »
- sketch: ../storyboard.html#frame-18

Le troisième avantage, avec sa limite.

## Frame 5 — Cassure

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

## Frame 6 — Offre

- scene: « ET EN CE MOMENT… » se réduit en étiquette « EN CE MOMENT ». Groupes de la 25, 4 mots au plus, avec la voix : « LES 4 PREMIÈRES » entre en coupe à 7,969 s, « SEMAINES » frappe au drop (8,44 s) ; puis « DE L'OPTION PREMIUM » ; puis « SONT OFFERTES. » : « OFFERTES. » en or et le qualificatif « LES 4 PREMIÈRES SEMAINES DE L'OPTION » / « PUIS 2 € TTC/SEM. (8 € TOUTES LES 4 SEM.) » / « EN PLUS DE VOTRE ABONNEMENT » entrent dans la même image ; le filet souligne. Le panneau des mentions est en place à 9,375 s.
- duration: 3.001s
- start: 7.969s
- poster: 10.4
- transition_in: cut
- status: built
- voiceover: 25 « Les 4 premières semaines de l'option Premium sont offertes. » (≈ 7,97–10,97 s)
- src: compositions/fin-commune.html
- blueprint: compose
- rules: kinetic-beat-slam, css-marker-patterns
- focal: « OFFERTES. » en or
- onscreen: « EN CE MOMENT » (étiquette) · « LES 4 PREMIÈRES SEMAINES » → « DE L'OPTION PREMIUM » → « SONT OFFERTES. » · qualificatif 40 px · mentions
- sfx: impact-bass-1 au drop (8,44) · click sur « OFFERTES »
- constraint: OFFERTES never without its condition in the same frame · no « gratuit » · no « offre limitée »
- sketch: ../storyboard.html#frame-07+08

Personne ne voit « OFFERTES » sans sa condition.

## Frame 7 — Prix

- scene: Sans voix. « PUIS », le « + » or se trace et « 2 € » frappe ; « TTC PAR SEMAINE » et « SOIT 8 € TOUTES LES 4 SEM. » / « EN PLUS DE VOTRE ABONNEMENT » sont déjà en place à la même image. Rappel « FONTAINE · ANALYSE 3D · POSING (BIENTÔT) ». Pas de pastille, pas de « OFFERTES ».
- duration: 1.220s
- start: 10.970s
- poster: 11.8
- transition_in: wipe
- status: built
- voiceover: aucune
- src: compositions/fin-commune.html
- blueprint: compose
- rules: svg-path-draw, kinetic-beat-slam
- focal: le « + » et « 2 € »
- onscreen: « PUIS » « +2 € » « TTC PAR SEMAINE » « SOIT 8 € TOUTES LES 4 SEM. » « EN PLUS DE VOTRE ABONNEMENT » « FONTAINE · ANALYSE 3D · POSING (BIENTÔT) » · mentions
- sfx: impact-bass-1 sur le « + » (11,1) · whoosh-short à 12,1
- constraint: price never without its qualifier
- sketch: ../storyboard.html#frame-09

Le prix TTC, la cadence et « en plus de votre abonnement » arrivent ensemble.

## Frame 8 — Carte finale

- scene: Le monogramme s'assemble par ses 3 bandes horizontales, le mot-symbole se pose, « OPTION PREMIUM » hors zone de protection. CTA « + ACTIVEZ-LA À L'ACCUEIL » (68 px) sur le 1er groupe de P9, puis « EN QUELQUES SECONDES. ». Statique sur les 40 % finaux.
- duration: 2.743s
- start: 12.190s
- poster: 13.9
- transition_in: wipe
- status: built
- voiceover: P9 « Activez-la à l'accueil, en quelques secondes. » (≈ 12,3–14,5 s)
- src: compositions/fin-commune.html
- blueprint: logo-assemble-lockup
- rules: gsap-effects, spring-pop-entrance
- focal: le CTA, puis le logo
- onscreen: logo · « OPTION PREMIUM » · « + ACTIVEZ-LA À L'ACCUEIL » · « EN QUELQUES SECONDES. » · mentions
- sfx: whoosh-short sur chaque bande du logo (12,2 / 12,26 / 12,32) · impact-bass-1 à 12,5
- constraint: no chevron to a Meta button (organique) · no online sign-up
- sketch: ../storyboard.html#frame-10

On sait quoi faire et où : à l'accueil.

