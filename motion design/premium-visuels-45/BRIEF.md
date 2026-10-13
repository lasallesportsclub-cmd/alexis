---
workflow: general-video
flow: automation
storyboard: yes
message: "Option Premium LA SALLE : fontaine, analyse 3D et salle de posing pour +2 € TTC/sem., à activer à l'accueil"
destination: instagram-feed
aspect: 1080x1350
language: fr
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
angle: promo
narration: no
---

## Intent

Demande de Mehdi Abid, directeur de LA SALLE, dans ses mots : « fais-moi une prompt pour créer une vidéo HyperFrames pour mettre en avant l'abonnement Premium de la salle […] il me faut des images et vidéos au format story et post ».

À l'écran, c'est l'**option Premium**, qui s'ajoute à l'abonnement (jamais « abonnement Premium »). Objectif unique : que les adhérents ajoutent l'option à leur abonnement, à l'accueil. Version 2 de l'option au 13/10/2026. Ton : vouvoiement, direct, premium, sans promesse de résultat. Mehdi et Alexis veulent du rythme, une voix off française comme dans les pubs d'octobre et des éléments visuels récurrents qui marquent la mémoire.

Ce projet : **images post 1080×1350**, PNG maîtres et JPG (qualité 90, sRGB, moins de 1 Mo). Le format 1080×1350 (4:5) est un choix explicite du brief, hors du vocabulaire par défaut (`1080x1080`).

## Assets

- assets/fonts/ — Barlow Condensed 700–900 (droit et italique) et DM Sans 400–700, woff2 latin de @fontsource 5.3.0, licence OFL (copie de `_sources-premium/fonts/`).
- assets/vendor/gsap.min.js — GSAP 3.14.2 en local (les CDN sont bloqués).
- frame.md — charte de travail, copie de `_sources-premium/shared/frame.md`.
- assets/img/mono.png, assets/img/word.png — ⚠ en attente (kit du PC).

## Customizations

- 3 visuels clés (A, B, C) et un carrousel de 5 slides :
  1. « PASSEZ EN VERSION PREMIUM. » ;
  2. la fontaine ;
  3. l'analyse 3D ;
  4. la salle de posing (BIENTÔT, citée et non montrée) ;
  5. l'offre, le prix, le CTA et les mentions.
- Le trait or traverse les 5 slides en continu, raccordé au pixel près d'une slide à l'autre (une seule droite calculée sur 5 × 1080 px).
- Méthode : scènes figées d'une seconde dans `index.html`, export par `snapshot --at <milieu> --no-end`.

## Notes

- **Réponses du 13/10/2026 (Mehdi ou Alexis)**
  - Q1 : 4 premières semaines offertes, en ce moment, sans date de fin.
  - Q2 : sans engagement sur l'option. ⚠ Le calendrier S40 du Drive dit « engagement d'un an sur l'option » : à confirmer avant diffusion.
  - Q3 : salle de posing sans date. Citée avec « BIENTÔT », jamais montrée.
  - Q4 : la fontaine s'appelle « FONTAINE À BOISSON SPORTIVE ».
  - Q5 : aucun rush. 100 % motion design typographique, sans personne à l'écran.
  - Q6 : voix Nika, générée par Mehdi ou Alexis dans AI Studio (textes dans `motion design/_sources-premium/voix/a_generer.md`).
  - Q7 : musique de la Sound Collection Meta fournie par Mehdi. Une version sans musique est toujours livrée.
  - Q8 : accords de droit à l'image pour Instagram seulement. Sans objet, puisque personne n'apparaît.
  - Q9 : happening pas fixé, donc pas de concept D.
  - Q10 : diffusion organique seulement.
- **Où** : session cloud, sans les fichiers du PC (prompt maître, kit `reel-la-salle-hyperframes`, banque de voix, bruitages). Polices Barlow Condensed et DM Sans prises sur npm (OFL), GSAP en local, logo en attente de `mono.png` et `word.png`.
- **Pastille** : « 4 SEMAINES OFFERTES, PUIS 2 € TTC/SEM. ».
- **Mention** (`mentionPremium`, 123 caractères, au moins 40 px, fond opaque) : « Option 2 € TTC/sem. (8 €/4 sem.) en plus de l'abonnement. 1 boisson/30 min. 1 analyse 3D/sem. Sans engagement sur l'option. »
- **Règle des prix** : « +2 € TTC/SEM. » va avec « SOIT 8 € TOUTES LES 4 SEM. · EN PLUS DE VOTRE ABONNEMENT ». « OFFERTES » va avec « PUIS 2 € TTC/SEM. (8 € TOUTES LES 4 SEM.) ». Qualificatif d'au moins 32 px dans le même bloc.
- **Interdits** : voir `frame.md`, section What NOT to Do. Lexique interdit : « fontaine à eau », « abonnement Premium », « offre limitée », « gratuit », « inscription en ligne », « minceur », « brûle », « kilo », « détox », « illimité », « avant/après », tout tutoiement, tout concurrent, « sans engagement » non suivi de « sur l'option ». « À volonté » n'est pas utilisé dans cette version.
- **⚠ Drive** : aucune source sur le Drive pour « une boisson toutes les 30 minutes » ni pour « une analyse par semaine ». Ce sont des faits donnés par Mehdi et Alexis (brief du 12/10). Le livret ingrédients signale la caféine du Power Drink (50 mg par verre) : aucune allégation sur les boissons.
- **Zones 4:5** : texte entre x 108 et 972, y 135 et 1215 ; mentions dans le panneau y 1015–1215 ; lisible en recadrage 3:4 et en vignette à 30 %.
