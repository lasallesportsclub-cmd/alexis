---
workflow: general-video
flow: automation
storyboard: yes
message: "Option Premium LA SALLE : fontaine, analyse 3D et salle de posing pour +2 € TTC/sem., à activer à l'accueil"
destination: instagram-stories
aspect: 1080x1920
language: fr
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
angle: promo
narration: no
---

## Intent

Demande de Mehdi Abid, directeur de LA SALLE, dans ses mots : « fais-moi une prompt pour créer une vidéo HyperFrames pour mettre en avant l'abonnement Premium de la salle […] il me faut des images et vidéos au format story et post ».

À l'écran, c'est l'**option Premium**, qui s'ajoute à l'abonnement (jamais « abonnement Premium »). Objectif unique : que les adhérents ajoutent l'option à leur abonnement, à l'accueil. Version 2 de l'option au 13/10/2026. Ton : vouvoiement, direct, premium, sans promesse de résultat. Mehdi et Alexis veulent du rythme, une voix off française comme dans les pubs d'octobre et des éléments visuels récurrents qui marquent la mémoire.

Ce projet : **images story 1080×1920**, PNG maîtres et JPG (qualité 90, sRGB, moins de 1 Mo).

## Assets

- assets/fonts/ — Barlow Condensed 700–900 (droit et italique) et DM Sans 400–700, woff2 latin de @fontsource 5.3.0, licence OFL (copie de `_sources-premium/fonts/`).
- assets/vendor/gsap.min.js — GSAP 3.14.2 en local (les CDN sont bloqués).
- frame.md — charte de travail, copie de `_sources-premium/shared/frame.md`.
- assets/img/mono.png, assets/img/word.png — ⚠ en attente (kit du PC).

## Customizations

- 4 images : visuel clé A (3 EN 1), visuel clé B (LA FONTAINE), visuel clé C (VOS PROGRÈS EN 3D), carte offre (« 4 SEMAINES OFFERTES »). Pas de D (Q9).
- Méthode : `index.html` enchaîne des scènes figées d'une seconde, une par image ; export par `npx hyperframes snapshot --at <milieu> --no-end`, puis JPG avec ffmpeg.
- Zone sticker : environ 900×220 px vers y 1320–1540 laissée vide (sondage ou compte à rebours natif).

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
- **Zones 9:16** : texte entre x 108 et 972, y 290 et 1240 ; décor entre x 72 et 1008 ; mentions dans le panneau y 1040–1240.
