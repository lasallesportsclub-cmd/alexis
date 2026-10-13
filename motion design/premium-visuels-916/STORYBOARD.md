---
format: 1080x1920
duration: 4s
message: "Option Premium LA SALLE : fontaine, analyse 3D et salle de posing pour +2 € TTC/sem., à activer à l'accueil"
arc: images fixes, une scène figée d'une seconde par image
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
mode: collaborative
---

# Option Premium · images story · plan v2

Chaque image est une scène figée d'une seconde dans `index.html`, exportée par `npx hyperframes snapshot --at <milieu> --no-end`, puis convertie en JPG (qualité 90, sRGB, moins de 1 Mo). Tokens, bans et règles des prix : voir `frame.md`.

## Frame 1 — Visuel clé A

- scene: 3 EN 1 : titre, « + », 3 bandes, CTA, mentions ; zone sticker vide.
- duration: 1s
- start: 0s
- poster: 0.5
- status: built
- voiceover: onscreen
- src: compositions/frames/01.html
- onscreen: « PASSEZ EN VERSION PREMIUM. » · pastille · bandes 01/02/03 · « ACTIVEZ-LA À L'ACCUEIL » · mentions
- export: LA_SALLE_Premium_A_story_9x16
- sketch: storyboard.html#frame-01

## Frame 2 — Visuel clé B

- scene: LA FONTAINE : boissons et saveurs en toutes lettres, horloge des 30 min.
- duration: 1s
- start: 1s
- poster: 1.5
- status: built
- voiceover: onscreen
- src: compositions/frames/02.html
- onscreen: « VOTRE BOISSON VOUS ATTEND. » · « 01 FONTAINE À BOISSON SPORTIVE » · boissons · saveurs · « 1 BOISSON TOUTES LES 30 MIN » · « AUSSI : ANALYSE 3D · SALLE DE POSING (BIENTÔT) » · CTA · mentions
- export: LA_SALLE_Premium_B_story_9x16
- sketch: storyboard.html#frame-02

## Frame 3 — Visuel clé C

- scene: VOS PROGRÈS EN 3D : relief typographique, une analyse par semaine.
- duration: 1s
- start: 2s
- poster: 2.5
- status: built
- voiceover: onscreen
- src: compositions/frames/03.html
- onscreen: « VOS PROGRÈS, EN 3D. » · « 01 ANALYSE 3D · 1 PAR SEMAINE » · « Analyse de composition corporelle. » · « AUSSI : FONTAINE · SALLE DE POSING (BIENTÔT) » · CTA · mentions
- export: LA_SALLE_Premium_C_story_9x16
- sketch: storyboard.html#frame-03

## Frame 4 — Carte offre

- scene: Lancement du 13/10 : l'offre avec son qualificatif complet, le CTA et les mentions.
- duration: 1s
- start: 3s
- poster: 3.5
- status: built
- voiceover: onscreen
- src: compositions/frames/04.html
- onscreen: logo · « OPTION PREMIUM » · « ET EN CE MOMENT… » « 4 SEMAINES OFFERTES » « PUIS 2 € TTC/SEM. (8 € TOUTES LES 4 SEM.) » « EN PLUS DE VOTRE ABONNEMENT » · CTA · mentions
- export: LA_SALLE_Premium_offre_story_9x16
- sketch: storyboard.html#frame-04

