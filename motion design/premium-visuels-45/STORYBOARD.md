---
format: 1080x1350
duration: 8s
message: "Option Premium LA SALLE : fontaine, analyse 3D et salle de posing pour +2 € TTC/sem., à activer à l'accueil"
arc: images fixes, une scène figée d'une seconde par image
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
mode: collaborative
---

# Option Premium · images post · plan v2

Chaque image est une scène figée d'une seconde dans `index.html`, exportée par `npx hyperframes snapshot --at <milieu> --no-end`, puis convertie en JPG (qualité 90, sRGB, moins de 1 Mo). Tokens, bans et règles des prix : voir `frame.md`.

## Frame 1 — Visuel clé A

- scene: Recomposé en 4:5.
- duration: 1s
- start: 0s
- poster: 0.5
- status: built
- voiceover: onscreen
- src: compositions/frames/01.html
- onscreen: comme le visuel clé A story
- export: LA_SALLE_Premium_A_post_4x5
- sketch: storyboard.html#frame-01

## Frame 2 — Visuel clé B

- scene: Recomposé en 4:5.
- duration: 1s
- start: 1s
- poster: 1.5
- status: built
- voiceover: onscreen
- src: compositions/frames/02.html
- onscreen: comme le visuel clé B story
- export: LA_SALLE_Premium_B_post_4x5
- sketch: storyboard.html#frame-02

## Frame 3 — Visuel clé C

- scene: Recomposé en 4:5.
- duration: 1s
- start: 2s
- poster: 2.5
- status: built
- voiceover: onscreen
- src: compositions/frames/03.html
- onscreen: comme le visuel clé C story
- export: LA_SALLE_Premium_C_post_4x5
- sketch: storyboard.html#frame-03

## Frame 4 — Carrousel 1 · couverture

- scene: « PASSEZ EN VERSION PREMIUM. », pastille ; le trait or part sous le titre.
- duration: 1s
- start: 3s
- poster: 3.5
- status: built
- voiceover: onscreen
- src: compositions/frames/04.html
- onscreen: « PASSEZ EN VERSION PREMIUM. » · pastille + qualificatif · « FONTAINE · ANALYSE 3D · POSING (BIENTÔT) » · mentions
- export: LA_SALLE_Premium_carrousel_1
- sketch: storyboard.html#frame-04

## Frame 5 — Carrousel 2 · fontaine

- scene: 01 : boissons, saveurs, une boisson toutes les 30 min.
- duration: 1s
- start: 4s
- poster: 4.5
- status: built
- voiceover: onscreen
- src: compositions/frames/05.html
- onscreen: « 01 FONTAINE À BOISSON SPORTIVE » « VOTRE BOISSON VOUS ATTEND. » · boissons · saveurs · « 1 BOISSON TOUTES LES 30 MIN »
- export: LA_SALLE_Premium_carrousel_2
- sketch: storyboard.html#frame-05

## Frame 6 — Carrousel 3 · analyse 3D

- scene: 02 : une analyse par semaine, pour suivre votre progression.
- duration: 1s
- start: 5s
- poster: 5.5
- status: built
- voiceover: onscreen
- src: compositions/frames/06.html
- onscreen: « 02 ANALYSE 3D » « VOS PROGRÈS, EN 3D. » « 1 ANALYSE 3D PAR SEMAINE » · « Analyse de composition corporelle, pour suivre votre progression. »
- export: LA_SALLE_Premium_carrousel_3
- sketch: storyboard.html#frame-06

## Frame 7 — Carrousel 4 · salle de posing

- scene: 03 : citée, jamais montrée.
- duration: 1s
- start: 6s
- poster: 6.5
- status: built
- voiceover: onscreen
- src: compositions/frames/07.html
- onscreen: « 03 SALLE DE POSING » « ARRIVE TRÈS BIENTÔT. » « MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES »
- export: LA_SALLE_Premium_carrousel_4
- sketch: storyboard.html#frame-07

## Frame 8 — Carrousel 5 · offre

- scene: Un seul bloc offre + prix (à valider : il remplace la ligne « PUIS 2 € TTC/SEM. (8 € TOUTES LES 4 SEM.) ») ; le trait finit sous le CTA.
- duration: 1s
- start: 7s
- poster: 7.5
- status: built
- voiceover: onscreen
- src: compositions/frames/08.html
- onscreen: « ET EN CE MOMENT… » « 4 SEMAINES OFFERTES » « DE L'OPTION PREMIUM » « PUIS » « +2 € TTC PAR SEMAINE » « SOIT 8 € TOUTES LES 4 SEM. » « EN PLUS DE VOTRE ABONNEMENT » · CTA · logo · mentions
- export: LA_SALLE_Premium_carrousel_5
- sketch: storyboard.html#frame-08

