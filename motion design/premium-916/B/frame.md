---
version: v1
name: LA SALLE — Option Premium — Frame (charte « Le Trait Oblique » v2)
description: >
  Couche de cadre du kit Option Premium de LA SALLE (Urban Valley, Conflans-Sainte-Honorine) :
  vidéos 15 s et images, en story 1080×1920 et en post 1080×1350. 100 % motion design
  typographique (aucun rush, réponse Q5). Le noir porte, le blanc cassé parle, l'or signe.
unit: px sur une largeur de 1080 (identique en 9:16 et en 4:5 ; seule la hauteur change)
principle: une idée par temps · l'or ne signe que l'essentiel · chaque prix porte son qualificatif · les chiffres viennent du brief, jamais d'ailleurs

colors:
  canvas: "#0D0D0D"
  text: "#F4F1EC"
  gold: "#B8A07E"
  surface: "#222222"
  text-muted: "rgba(244,241,236,0.62)"
  gold-ghost: "rgba(184,160,126,0.16)"
  hairline: "rgba(244,241,236,0.18)"

typography:
  display:   { fontFamily: "Barlow Condensed", px: 168, weight: 900, lineHeight: 0.86, tracking: "-0.01em", upper: true }
  h1:        { fontFamily: "Barlow Condensed", px: 112, weight: 900, lineHeight: 0.9, tracking: "-0.005em", upper: true }
  h2:        { fontFamily: "Barlow Condensed", px: 76, weight: 800, lineHeight: 0.95, tracking: "0em", upper: true }
  label:     { fontFamily: "Barlow Condensed", px: 44, weight: 800, style: italic, tracking: "0.04em", upper: true }
  pastille:  { fontFamily: "Barlow Condensed", px: 36, weight: 800, style: italic, tracking: "0.02em", upper: true }
  qualifier: { fontFamily: "Barlow Condensed", px: 36, weight: 800, tracking: "0.03em", upper: true }
  body:      { fontFamily: "DM Sans", px: 36, weight: 500, lineHeight: 1.3 }
  mention:   { fontFamily: "DM Sans", px: 40, weight: 500, lineHeight: 1.18 }

spacing:
  safe-x: "108px → 972px (texte, prix, logo, CTA, mentions)"
  decor-x: "72px → 1008px"
  safe-y-916: "290px → 1240px"
  sticker-916: "y 1320px → 1540px, ~900×220 px laissés vides dans les images story"
  safe-y-45: "135px → 1215px"
  mention-916: "panneau x 108→972, y 1040→1240"
  mention-45: "panneau x 108→972, y 1015→1215"
  gap: "24px"

components:
  trait-oblique:
    slope: "0.42"
    description: "Pente du monogramme : le bord coupé avance de 0,42 px vers la droite par pixel de montée (penché à droite comme une italique, 22,78° par rapport à la verticale). Sert à couper les bandes, souligner, barrer, et assembler le logo."
  plus-premium:
    color: "gold"
    description: "Signature de l'option : un « + » or en italique. Barre horizontale à plat, barre verticale penchée de 0,42. Épaisseur des barres = 22 % de la taille. Apparaît à l'image 0 (déjà entier, jamais en cours de tracé), dans la pastille (en négatif #0D0D0D, devant « 2 € »), devant le prix (« +2 € ») et dans la carte finale (devant le CTA). Il veut dire « ajoutez l'option »."
  bande:
    fill: "surface"
    filet: "gold, 6px, sur le bord d'attaque"
    description: "Bande horizontale aux extrémités coupées à 0,42. Trois bandes = les trois avantages, numérotées 01, 02, 03 dans l'ordre où la voix les cite (A et B : fontaine, analyse 3D, posing ; C : analyse 3D, posing, fontaine). Variante compacte de 62–64 px sans filet pour les visuels fixes et les rappels."
  pastille:
    fill: "gold"
    text: "canvas"
    description: "Cartouche or aux extrémités coupées à 0,42, texte en style pastille : « 4 SEMAINES OFFERTES, PUIS +2 € TTC/SEM. » (le « + » en négatif). Toujours suivie, dans le même bloc, de la ligne qualifier 32 px « EN CE MOMENT · EN PLUS DE VOTRE ABONNEMENT »."
  mention-panel:
    fill: "surface"
    text: "text"
    description: "Mentions légales en style mention sur fond opaque, 3 ou 4 lignes, jamais sur une image ni sur un décor."
  grain:
    opacity: "0.7 (overlay)"
    description: "Grain fin et gris (feTurbulence, fréquence 0,85) en incrustation (overlay) à 0,7 : la valeur moyenne du fond reste #0D0D0D, amplitude ≈ ±0,014."
---

# LA SALLE — Option Premium : la couche de cadre

## Overview

Le kit vend une seule chose : ajouter l'option Premium à son abonnement, à l'accueil. Sans rushs, le film repose sur trois atomes récurrents que l'œil doit retenir comme une marque retient un jingle :

- **le « + » or** : il ouvre le film à l'image 0, revient devant le prix et ferme la carte finale ;
- **les 3 bandes obliques** : une par avantage, coupées à la pente du monogramme, elles reviennent assembler le logo ;
- **le filet or** : il souligne, barre et révèle.

Caractéristiques à l'échelle du cadre :
- un seul titre domine, entre 3 et 6 fois plus gros que le reste ;
- l'or est rare : un mot, un trait, une pastille par cadre ;
- le noir est un plan de travail, pas un vide : grain fin, bandes #222, texte fantôme or à 16 %.

## The Frame

- **Formats.** Story 1080×1920 : vidéos (Reels et Stories) et images. Post 1080×1350 : vidéos et images du fil, dont le carrousel de 5 slides. Le 4:5 est **recomposé**, pas recadré.
- **Zones utiles 9:16.** Texte, prix, logo, CTA et mentions entre x 108 et 972, y 290 et 1240. Décor entre x 72 et 1008. Dans les images story, une zone d'environ 900×220 px vers y 1320–1540 reste vide pour un sticker natif.
- **Zones utiles 4:5.** x 108 à 972, y 135 à 1215. Les couvertures restent lisibles en recadrage 3:4 dans la grille du profil et en vignette à 30 %.
- **Frame Craft Bar.**
  - Squint : en plissant les yeux, on ne voit qu'un titre et un éclat d'or.
  - Silence : au moins 40 % du cadre reste noir.
  - Restraint : jamais plus de deux tailles de titre dans un même cadre.
  - Reference : affiche de sport premium, pas page web.

## Colors

- `canvas` #0D0D0D : le fond de tous les cadres. Jamais de #000.
- `text` #F4F1EC : tout le texte courant et les titres. Jamais de #FFF.
- `gold` #B8A07E : signature uniquement. Le « + », la pastille, le filet, un mot-clé par cadre.
- `surface` #222222 : les bandes et le panneau des mentions. **Jamais pour du texte** (contraste 1,22 sur #0D0D0D).
- Les variantes d'opacité (`text-muted`, `gold-ghost`, `hairline`) sont les seules autorisées. Aucun autre hex.
- Contrastes : #F4F1EC sur #0D0D0D = 17,3 · #B8A07E sur #0D0D0D = 7,7 · #0D0D0D sur #B8A07E = 7,7 · #B8A07E sur #F4F1EC = 2,2 (**interdit** pour du texte).

## Typography

- Barlow Condensed 800–900 en capitales pour tous les titres. L'italique 800 est réservé aux étiquettes (01, 02, 03 et leur nom), à la pastille et au CTA. DM Sans 500 pour le texte et les mentions.
- Deux linéales : c'est l'exception assumée de la charte. Le contraste se fait entre condensé et large, et entre affiche et lecture.
- Planchers in-feed : titres ≥ 90 px, texte ≥ 32 px, étiquettes ≥ 36 px, mentions ≥ 40 px. Tout qualificatif de prix fait au moins 32 px (36 px ici).
- Chiffres en `tabular-nums`. Le signe € suit le chiffre après une espace insécable (« 2 € », « 8 € »).
- Polices embarquées en local (`assets/fonts/*.woff2`, licence OFL) : déclarer `@font-face` dans **chaque** fichier de composition.

## Depth & Surface

Plat. Aucune ombre, aucun halo, aucune lueur, aucun dégradé. La profondeur vient de trois calques :
1. le fond : `canvas` avec grain et texte fantôme `gold-ghost` ;
2. le plan médian : le message ;
3. le premier plan : filets, étiquettes, numéros.

## Shapes

- Tout ce qui est coupé l'est à la pente 0,42, penché à droite : bandes, pastille, cartouches, « + ».
- Pas d'arrondi, sauf les angles adoucis du monogramme lui-même.
- Le trait d'une bande ou d'un filet a une ancre de départ, une ancre d'arrivée et un rôle. Sinon, on le coupe.

## Components

- **« + » Premium** : SVG, deux barres, l'une à plat, l'autre penchée à 0,42. Épaisseur 22 % de la taille. En `gold`, sauf dans la pastille, où il est en négatif #0D0D0D (26 px) devant « 2 € ».
- **Bande** : parallélogramme `surface` de 160 à 220 px de haut, extrémités coupées à 0,42, filet or de 6 px sur le bord d'attaque, étiquette en style `label` (numéro en or, nom en `text`).
- **Pastille** : parallélogramme `gold`, hauteur 64 px, texte en style `pastille` couleur `canvas`.
- **Bloc prix** : « + » or tracé, « 2 € » en display, puis « TTC PAR SEMAINE » en style h2, puis le qualificatif « SOIT 8 € TOUTES LES 4 SEM. · EN PLUS DE VOTRE ABONNEMENT » en style qualifier. Les trois dans le même bloc, toujours.
- **Bloc offre** : « 4 SEMAINES » (text) et « OFFERTES » (gold) en display, puis « PUIS 2 € TTC/SEM. (8 € TOUTES LES 4 SEM.) » et « EN PLUS DE VOTRE ABONNEMENT » en style qualifier. Toujours ensemble. En vidéo, quand la voix dit « sont offertes », le qualificatif commence par « LES 4 PREMIÈRES SEMAINES DE L'OPTION ».
- **Panneau mentions** : `surface` opaque, x 108→972, DM Sans 500 40 px, interligne 1,18, texte de la variable `mentionPremium`. En vidéo : un seul élément sur son propre calque, au-dessus de toutes les transitions, en place à 9,375 s et immobile jusqu'à la fin. En images story : y 1080–1238.
- **Logo** : `mono.png` et `word.png` du kit du PC, jamais redessinés ni recolorés hors de la version négative (blanc cassé sur noir). Zone de protection = hauteur du monogramme. Assemblé en vidéo par ses 3 bandes horizontales.

## Frame Treatments

- **Accroche** (image 0) : fond `canvas`, registre affiche, titre display sur 2 ou 3 lignes ancré à gauche, « + » or entier à droite du titre, pastille et son qualificatif à partir de 0,3 s. Focal : le titre. Densité faible.
- **Preuve** (01, 02, 03) : une bande ouverte plein cadre, l'étiquette en haut, la phrase de la voix en h1, un décor typographique propre à l'avantage. Densité moyenne.
- **Cassure** : 0,47 s, `canvas` nu, « ET EN CE MOMENT… » seul en display, musique coupée. Le texte se réduit ensuite en étiquette « EN CE MOMENT » pendant l'offre.
- **Offre** : les groupes de la réplique 25 (4 mots au plus) ; « OFFERTES » en or n'arrive que quand la voix le dit, avec sa condition dans la même image.
- **Prix** : « PUIS », le « + » or se trace, « 2 € » frappe ; « TTC PAR SEMAINE » et le qualificatif sont déjà en place. Rappel « FONTAINE · ANALYSE 3D · POSING (BIENTÔT) » en `text-muted`. Jamais « OFFERTES » dans le même cadre que le prix.
- **Carte finale** : monogramme assemblé par ses 3 bandes, CTA « ACTIVEZ-LA À L'ACCUEIL » en style label, mentions. Statique sur les derniers 40 %.

## Composition Rules

### Do
- Ancrer les titres à gauche sur x 108. Laisser respirer à droite, là où vit le « + ».
- Une idée par temps (0,469 s à 128 BPM). Coupe sèche ou volet oblique entre deux idées.
- Les entrées se font par volet, glissement masqué ou frappe d'échelle (slam). Le héros est visible avant 0,5 s.
- Mot pour mot : le texte cinétique reprend la voix, 4 mots au plus à la fois, au-dessus de y 1040.

### Don't
- Centrer tout avec un poids égal. Mettre l'or sur plus d'un mot par cadre.
- Animer l'opacité pour faire entrer ou sortir un élément.

## What NOT to Do

- **Pas d'écran noir ni de logo en ouverture.** L'image 0 porte déjà la promesse et le « + ».
- Pas de look IA, de dégradé, de couleur vive, de fondu enchaîné, de halo ou lueur, de glitch, de fausse interface (écran de balance simulé, faux bouton, fausse application), d'icône de personne ni d'illustration de fruit.
- Jamais « fontaine à eau » : on dit « FONTAINE À BOISSON SPORTIVE ». Jamais « abonnement Premium » : on dit « option Premium ».
- Jamais « gratuit », « offre limitée », « inscription en ligne », « illimité », « sans engagement » seul.
- Jamais « minceur », « brûle-graisses », « détox », « énergie illimitée », de kilos, d'avant/après, de promesse de résultat.
- Aucun effet attribué aux boissons (collagène, L-carnitine, booster). Aucun vocabulaire médical : on dit « analyse de composition corporelle » et « suivre sa progression ».
- Pas de tutoiement : LA SALLE vouvoie.
- Pas de prix sans son qualificatif dans le même bloc. Pas de « OFFERTES » sans sa condition.
- Pas de logo de marque tierce (GYMWA, fabricant de la balance, équipementiers, Nutripure).
- La salle de posing n'est jamais montrée : elle est citée avec « BIENTÔT ».
- Pas de chevron vers un bouton Meta en organique.

## Aspect-Ratio Behavior

| Ratio | Canevas | Zone texte | Mentions | Particularités |
|---|---|---|---|---|
| 9:16 | 1080×1920 | x 108–972, y 290–1240 | y 1040–1240 | zone sticker 1320–1540 vide dans les images story |
| 4:5 | 1080×1350 | x 108–972, y 135–1215 | y 1015–1215 | recomposé : pastille à y 150, blocs au-dessus de 1040 remontés de 150 à 170 px, display ×0,85 (168 → 143) ; lisible en 3:4 et à 30 % |

## Approved Entities

LA SALLE · Urban Valley · Conflans-Sainte-Honorine · option Premium · FONTAINE À BOISSON SPORTIVE · ANALYSE 3D · analyse de composition corporelle · SALLE DE POSING · passion, pastèque, ice tea, ananas, multifruit · collagène, multivitamines, L-carnitine, booster, eau.

## Numerals & Claims (hard rule)

Seuls ces chiffres existent :
- 2 € TTC par semaine ;
- 8 € toutes les 4 semaines ;
- 4 premières semaines offertes (en ce moment, sans date de fin) ;
- 1 boisson toutes les 30 minutes ;
- 1 analyse 3D par semaine ;
- 01, 02, 03 (numérotation).

Aucun autre chiffre, aucune date, aucun avis, aucun résultat d'analyse. ⚠ L'engagement : « sans engagement sur l'option » (réponse Q2), alors que le calendrier S40 du Drive parle d'« engagement d'un an sur l'option ». À confirmer avant diffusion.

## Pre-Render Self-Audit

1. Squint : un seul titre domine, l'or ne marque qu'un point.
2. Prix : chaque « 2 € », « 8 € » et « OFFERTES » a son qualificatif, au moins 32 px, dans le même bloc.
3. Mentions : présentes de 9,38 s à la fin dans les vidéos, en bas dans les images, au moins 40 px, sur fond opaque.
4. Zones : rien d'important hors des zones utiles. Zone sticker vide dans les images story.
5. Lexique : rien de la section What NOT to Do.
6. Image 0 : le « + » et la promesse lisibles, pas d'écran noir.

## Known Gaps

- Logo : en attente de `mono.png` et `word.png`. Les esquisses utilisent un emplacement marqué.
- Voix (Nika) et musique (Sound Collection) : en attente des fichiers. Les durées des répliques sont estimées.
- Grain : équivalence approximative avec le moteur du PC.
