---
workflow: general-video
flow: automation
storyboard: yes
message: "Option Premium LA SALLE : fontaine, analyse 3D et salle de posing pour +2 € TTC/sem., à activer à l'accueil"
destination: instagram-feed
aspect: 1080x1350
language: fr
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
length: 15s
angle: promo
narration: minimal
---

## Intent

Demande de Mehdi Abid, directeur de LA SALLE, dans ses mots : « fais-moi une prompt pour créer une vidéo HyperFrames pour mettre en avant l'abonnement Premium de la salle […] il me faut des images et vidéos au format story et post ».

À l'écran, c'est l'**option Premium**, qui s'ajoute à l'abonnement (jamais « abonnement Premium »). Objectif unique : que les adhérents ajoutent l'option à leur abonnement, à l'accueil. Version 2 de l'option au 13/10/2026. Ton : vouvoiement, direct, premium, sans promesse de résultat. Mehdi et Alexis veulent du rythme, une voix off française comme dans les pubs d'octobre et des éléments visuels récurrents qui marquent la mémoire.

Ce projet : **concept C · VOS PROGRÈS EN 3D**, vidéo 15 s en post 4:5 (feed et reel), 30 i/s.

## Assets

- assets/fonts/ — Barlow Condensed 700–900 (droit et italique) et DM Sans 400–700, woff2 latin de @fontsource 5.3.0, licence OFL (copie de `_sources-premium/fonts/`).
- assets/vendor/gsap.min.js — GSAP 3.14.2 en local (les CDN sont bloqués).
- frame.md — charte de travail, copie de `_sources-premium/shared/frame.md`.
- assets/img/mono.png, assets/img/word.png — ⚠ en attente (kit du PC).
- compositions/fin-commune.html — fin partagée par A, B et C (7,5 s → 14,933 s : cassure, offre, prix, carte finale), copie de `_sources-premium/shared/`.
- .media/audio/voice/ — ⚠ répliques de Nika en attente (P3 « Vos progrès, en trois D. » · P6 « Une analyse en trois D, chaque semaine. » · 25 · P9).
- .media/audio/bgm/ — ⚠ titre de la Sound Collection en attente.
- .media/audio/sfx/ — bruitages de la bibliothèque intégrée HyperFrames (Pixabay, licence commerciale sans attribution) ou synthétisés avec ffmpeg.

## Customizations

- Concept C · VOS PROGRÈS EN 3D : accroche « VOS PROGRÈS, EN 3D. » en relief typographique qui tourne, étiquette « 1 ANALYSE 3D PAR SEMAINE », puis la salle de posing (BIENTÔT), puis la fontaine.
- Voix : P3 « Vos progrès, en trois D. » · P6 « Une analyse en trois D, chaque semaine. » · 25 · P9 (4 répliques ; P7 exclue tant que la salle de posing n'a pas de date).
- Grille : 128 BPM (temps 0,469 s, mesure 1,875 s), racine `data-duration` 14.933 (448 images). Accroche 0–1,88 · preuves 1,88–7,5 · cassure et offre 7,5–9,38 · prix 9,38–11,25 · carte finale 11,25–14,93.
- Signature : le « + » or à l'image 0, dans la pastille, devant le prix et dans la carte finale.
- Deux mixages : avec musique, et sans musique (voix et bruitages).
- Un projet par concept (les répliques ne passent jamais par une variable) ; la fin commune est un seul fichier source copié dans A, B et C.

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

## Décisions du 13/10/2026 (Mehdi ou Alexis)

- Storyboard v2 validé ; construction lancée en automation.
- Réplique 25 : écart au §6 validé (« OFFERTES » quand la voix le dit ; carte finale ≈ 2,7 s).
- Engagement : « sans engagement sur l'option » confirmé une seconde fois, malgré le calendrier S40.
- Pastille : ligne « EN CE MOMENT · EN PLUS DE VOTRE ABONNEMENT » et « + » en négatif validés.
- Brouillon sans voix ni musique rendu le 13/10 ; rendu final quand les répliques de Nika et la musique Sound Collection sont déposées (bornes à recaler dans `_sources-premium/tools/video.py`, TIMING et COMMON).
- **Après les brouillons (13/10/2026)** : « fais sans les voix et musique ». Vidéos finales livrées sans voix ni musique, bruitages seuls, sur le minutage prévu pour la voix (texte cinétique gardé tel quel). Une seule version par vidéo : sans musique, « avec » et « sans » musique seraient identiques. Mastering −14 LUFS, crête vraie ≤ −1,5 dBTP, H.264 CRF 18 (`_sources-premium/tools/master.py`).
- Correction avant le rendu final : le relief « 3D » des plans « UNE ANALYSE EN 3D » (A·02, C·01) est réduit (240 → 200 px) et déplacé à droite ; il touchait le haut de « UNE ANALYSE ».
- Versions post 4:5 produites le 13/10 dans `motion design/premium-45/` (« Oui, maintenant »).

## Version post 4:5 (13/10/2026)

- Projet généré par `python3 _sources-premium/tools/video.py --45 A B C` à partir des mêmes scènes que `premium-916/` : même minutage, mêmes textes, mêmes bruitages.
- Cadre 1080×1350. Pastille à y 150. Scènes 1 à 4 remontées de 60 px (bloc centré sous la pastille, y 390–990). Fin commune remontée de 100 px. Mentions à y 1015–1215, en place de 9,375 s à la fin. Volets en 3 bandes de 450 px.
- Les titres gardent leur taille 9:16 : à largeur égale, ils tiennent dans la zone 4:5 (x 108–972, y 135–1215). La réduction ×0,85 de `frame.md` ne sert qu'aux images, plus chargées.
- Contrôle : `npx hyperframes check --caption-zone "x0=0;y0=.9;x1=1;y1=1;severity=warning"`.
