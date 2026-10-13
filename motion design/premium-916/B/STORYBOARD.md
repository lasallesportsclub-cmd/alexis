---
format: 1080x1920
duration: 14.933s
message: "Option Premium LA SALLE : fontaine, analyse 3D et salle de posing pour +2 € TTC/sem., à activer à l'accueil"
arc: Accroche → 3 avantages → cassure → offre → prix → carte finale
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
mode: collaborative
---

# Option Premium · concept B · plan v1

**Ce film dit aux adhérents de LA SALLE que l'option Premium (fontaine, analyse 3D, salle de posing bientôt) s'ajoute pour 2 € TTC par semaine, avec 4 semaines offertes en ce moment, et qu'on l'active à l'accueil.**

- **Spine** : une promesse (le « + »), trois preuves (les 3 bandes), une condition claire (offre + prix + mentions), une action (l'accueil).
- **Rythme** : 128 BPM (temps 0,469 s, mesure 1,875 s). Schéma `fast-fast-fast-HOLD-cut-SLAM-build-hold`. Une idée par temps.
- **Tokens** : canvas #0D0D0D, text #F4F1EC, gold #B8A07E, surface #222222 (source : `frame.md`, charte « Le Trait Oblique » v2). Barlow Condensed 800–900, DM Sans 500.
- **Atomes récurrents** : le « + » or (image 0, pastille, prix, carte finale), les 3 bandes obliques (une par avantage), le filet or.
- **Bans** : écran noir ou logo en ouverture, fondu enchaîné ou d'opacité, halo, dégradé, glitch, fausse interface, icône de personne, fruit dessiné, slideshow (plans immobiles qui se suivent) et screensaver (mouvement sans intention).
- **Held frame** : la carte finale, statique sur ses derniers 40 %.
- **Voix** : Nika, une seule voix, 5 répliques (P2, P4, P5, 25, P9). Durées **estimées** en attendant les fichiers ; la vraie durée d'une réplique décale la frontière suivante d'un temps au plus.
- **Son** : musique Sound Collection (en attente) creusée de 8 à 10 dB sous la voix (`carve.mjs --strength 0.4`) ; bruitages de la bibliothèque intégrée (whoosh-short sur chaque volet, impact-bass-1 sur le « + » et le drop, click sur les étiquettes). Version sans musique livrée.
- **Mentions** : panneau opaque de 9,38 s à la fin, texte de `mentionPremium`.

## Still open

- ⚠ Engagement : « sans engagement sur l'option » (Q2) contredit le calendrier S40 du Drive (« engagement d'un an sur l'option »).
- ⚠ Logo : `mono.png` et `word.png` attendus ; la carte finale assemble le monogramme par ses 3 bandes horizontales.
- ⚠ Réplique 25 (~3 s) : si elle ne tient pas entre 7,97 et 9,38 s, ses derniers mots passent sur le début du prix (le bloc offre reste à l'écran en pastille).

## Frame 1 — Accroche

- scene: « VOTRE BOISSON VOUS ATTEND. » posé à l'image 0, le « + » or ; la jauge or monte dans son cadre à droite, comme une gourde qui se remplit, sans illustration.
- duration: 1.875s
- start: 0.000s
- poster: 1.2
- transition_in: cut
- status: built
- voiceover: P2 « Votre boisson vous attend. » (≈ 0,05–1,4 s)
- src: compositions/frames/01-accroche.html
- blueprint: kinetic-type-beats
- rules: stat-bars-and-fills, kinetic-beat-slam
- focal: le titre
- onscreen: « VOTRE BOISSON » « VOUS ATTEND. » · pastille
- sfx: remplissage synthétisé (bruit filtré) à 0,1 · impact-bass-1 à 0,00
- constraint: no fruit · no bottle drawing
- sketch: ../storyboard.html#frame-10

La fontaine devient une promesse personnelle.

## Frame 2 — 01 · Les boissons

- scene: Les boissons s'empilent une par une (4 mots au plus), puis « OU SIMPLEMENT / DE L'EAU. » les remplace. Les saveurs défilent à la verticale à droite.
- duration: 3.281s
- start: 1.875s
- poster: 4.6
- transition_in: wipe
- status: built
- voiceover: P4 « Collagène, multivitamines, L-carnitine, booster… ou simplement de l'eau. » (≈ 1,9–6,0 s)
- src: compositions/frames/02-boissons.html
- blueprint: compose
- rules: waterfall-entry, vertical-spring-ticker
- focal: la liste
- onscreen: « COLLAGÈNE, » « MULTIVITAMINES, » « L-CARNITINE, » « BOOSTER… » → « OU SIMPLEMENT » « DE L'EAU. » · ticker « PASSION · PASTÈQUE · ICE TEA · ANANAS · MULTIFRUIT »
- sfx: click sur chaque mot
- constraint: no effect claimed for any drink
- sketch: ../storyboard.html#frame-11

La variété, en toutes lettres.

## Frame 3 — 30 minutes

- scene: L'aiguille tracée par le trait fait son demi-tour pendant « TOUTES LES 30 MINUTES. ».
- duration: 1.407s
- start: 5.156s
- poster: 6.3
- transition_in: wipe
- status: built
- voiceover: P5 « Une boisson toutes les trente minutes. » (≈ 5,2–7,0 s)
- src: compositions/frames/03-trente.html
- blueprint: compose
- rules: svg-path-draw, waterfall-entry
- focal: « 30 MINUTES. » en or
- onscreen: « UNE BOISSON » → « TOUTES LES » « 30 MINUTES. »
- sfx: click
- constraint: no « à volonté »
- sketch: ../storyboard.html#frame-12

La règle d'usage est claire.

## Frame 4 — 02 puis 03

- scene: Un temps chacun : la bande « 02 ANALYSE 3D · 1 PAR SEMAINE », puis « 03 SALLE DE POSING · BIENTÔT ».
- duration: 0.937s
- start: 6.563s
- poster: 7.2
- transition_in: wipe
- status: built
- voiceover: aucune
- src: compositions/frames/04-bandes.html
- blueprint: compose
- rules: gsap-effects
- focal: les deux bandes
- onscreen: « 02 ANALYSE 3D · 1 PAR SEMAINE » « 03 SALLE DE POSING · BIENTÔT »
- sfx: whoosh-short ×2
- constraint: no static hold
- sketch: ../storyboard.html#frame-13

Le prix couvre les trois avantages : on les nomme tous.

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

## Frame 7 — Prix

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

## Frame 8 — Carte finale

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

