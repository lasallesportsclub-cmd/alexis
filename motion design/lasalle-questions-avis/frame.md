---
version: v1
name: LA SALLE — « Vos questions » — Frame (charte « Le Trait Oblique » v2)
description: >
  Couche de cadre de la pub Meta 15 s « Vos questions » (9:16, 1080×1920, 30 i/s). Une conversation mise
  en scène entre une cliente et LA SALLE, sur de vraies photos du club. Base : preset broadside (plans plats,
  angles vifs, filets, un seul accent), remixé par build-frame.mjs puis remis à la main sur la charte du club
  (`motion design/_sources-premium/shared/frame.md`) : titres en capitales, DM Sans pour le texte, bulles à
  coupe oblique. Le noir porte, le blanc cassé parle, l'or signe.
unit: px sur 1080×1920
principle: une idée par temps · l'or ne signe que l'essentiel · les chiffres viennent du brief, les avis de Google, jamais d'ailleurs

colors:
  canvas: "#0D0D0D"
  text: "#F4F1EC"
  gold: "#B8A07E"
  surface: "#222222"
  text-muted: "rgba(244,241,236,0.62)"
  gold-ghost: "rgba(184,160,126,0.16)"
  hairline: "rgba(244,241,236,0.18)"
  scrim: "rgba(13,13,13,0.42)"

typography:
  display:   { fontFamily: "Barlow Condensed", px: 150, weight: 900, lineHeight: 0.88, tracking: "-0.01em", upper: true }
  h1:        { fontFamily: "Barlow Condensed", px: 104, weight: 900, lineHeight: 0.9, upper: true }
  h2:        { fontFamily: "Barlow Condensed", px: 72, weight: 800, lineHeight: 0.95, upper: true }
  label:     { fontFamily: "Barlow Condensed", px: 40, weight: 800, style: italic, tracking: "0.05em", upper: true }
  question:  { fontFamily: "DM Sans", px: 50, weight: 500, lineHeight: 1.18 }
  avis:      { fontFamily: "DM Sans", px: 66, weight: 500, lineHeight: 1.12 }
  mention:   { fontFamily: "DM Sans", px: 34, weight: 500, lineHeight: 1.22 }

spacing:
  safe-x: "108px → 972px (texte, bulles, logo, CTA, mentions)"
  decor-x: "72px → 1008px"
  safe-y: "290px → 1250px (contenu clé et mentions de la carte finale, y 1110 → 1240) ; rien sous 1594 px"
  question-y: "haut de la bulle de la cliente à y 520"
  reponse-y: "haut de la réponse, de l'indicateur de saisie ou de la carte d'avis à y 700"
  gap: "24px"

components:
  trait-oblique:
    slope: "0.42"
    description: "Pente du monogramme : le bord coupé avance de 0,42 px vers la droite par pixel de montée (penché à droite comme une italique). Coupe les bulles, les bandes, la carte d'avis et l'indicateur de saisie."
  bulle-cliente:
    fill: "text"
    text: "canvas"
    description: "Question de la cliente, à gauche (bord gauche x 108). Style question. Bord droit coupé à 0,42. Aucun nom, aucune icône."
  bulle-salle:
    fill: "surface"
    text: "text"
    filet: "gold, 6px, le long du bord gauche coupé à 0,42"
    description: "Réponse de LA SALLE, à droite (bord droit x 972). Titres Barlow Condensed en capitales ; la précision en style label or."
  saisie:
    description: "Indicateur « en train d'écrire » de LA SALLE : petite bulle surface à droite, 3 barres obliques (parallélogrammes 30×12 px, pente 0,42) qui s'allument en or l'une après l'autre en doubles croches. Version géante (barres 120×44 px) pendant la cassure."
  carte-avis:
    fill: "canvas (opaque)"
    border: "2px hairline"
    description: "Avis Google cité mot pour mot, centré x 108 → 972. En haut : 5 étoiles or (SVG plein) et l'étiquette « AVIS GOOGLE » en style label, text-muted. Le texte de l'avis en style avis, casse et ponctuation d'origine, guillemets français or. Coin haut droit coupé à 0,42. Jamais de nom d'auteur ni de date."
  bandes:
    fill: "surface"
    filet: "gold, 6px, sur le bord d'attaque"
    description: "Trois bandes horizontales de 640 px de haut, extrémités coupées à 0,42 : le volet qui ferme la conversation et ouvre la carte finale."
  grain:
    description: "Grain fin et gris (feTurbulence 0,85, incrustation à 0,7) sur chaque fond, sous le texte : il ne gêne ni la lecture ni le contrôle de contraste."
---

# LA SALLE — « Vos questions » : la couche de cadre

## Overview

Une cliente écrit à LA SALLE. Ses questions sont celles qu'on entend à l'accueil ; LA SALLE répond quand c'est un fait, et laisse ses avis Google répondre quand c'est un ressenti. Trois atomes reviennent comme un refrain :

- **la bulle claire de la cliente**, coupée à 0,42 à droite ;
- **la bulle sombre de LA SALLE**, coupée à 0,42 à gauche et signée d'un filet or ;
- **les 5 étoiles or** de la carte d'avis, qui s'allument une par une sur la musique.

Derrière, de vraies photos du club (façade, enseigne, tapis, haltères), assombries, coupées sur les temps. Aucune personne à l'image.

## The Frame

- **Format.** 1080×1920, 30 i/s, 15,0 s. Reels et Stories.
- **Zones utiles.** Texte, bulles, logo, CTA entre x 108 et 972, y 290 et 1250. Décor entre x 72 et 1008. Mentions de la carte finale y 1110–1240. Rien d'important sous y 1594.
- **En-tête** « LA SALLE · CONFLANS » (monogramme + nom), y 300–352, identique dans les cadres 1 à 5 : il paraît fixe aux coupes et passe sous les bandes du volet. **Grain** fin sur chaque fond (photo ou canevas), sous le texte.
- **Frame Craft Bar.**
  - Squint : on voit une bulle, une réponse, un éclat d'or.
  - Restraint : au plus deux tailles de titre par cadre.
  - Reference : affiche de sport premium, pas capture d'écran d'application.

## Colors

- `canvas` #0D0D0D : fond, carte d'avis, cassure. Jamais de #000.
- `text` #F4F1EC : texte, bulle de la cliente. Jamais de #FFF.
- `gold` #B8A07E : signature uniquement. Filets, étoiles, un mot par réponse, guillemets.
- `surface` #222222 : bulle de LA SALLE, bandes, panneau des mentions. Jamais pour du texte.
- `scrim` : voile canvas à 42 % posé sur chaque photo de fond, pour que les bulles dominent.
- Contrastes : #F4F1EC sur #0D0D0D = 17,3 · #0D0D0D sur #F4F1EC = 17,3 · #B8A07E sur #0D0D0D = 7,7 · #B8A07E sur #222 = 6,3 · #B8A07E sur #F4F1EC = 2,2 (**interdit** pour du texte).

## Typography

- Barlow Condensed 800–900 en capitales pour les réponses de LA SALLE et la carte finale. L'italique 800 est réservé aux étiquettes (« AVIS GOOGLE », « 7J/7 », CTA).
- DM Sans 500 pour ce que disent les gens : les questions de la cliente et le texte des avis (casse d'origine, jamais en capitales).
- Planchers : titres ≥ 72 px, questions ≥ 50 px, étiquettes ≥ 36 px, mentions ≥ 34 px.
- Chiffres en `tabular-nums`. « 1 200 m² » avec une espace insécable fine (U+202F) entre 1 et 200, et une espace insécable avant « m² ».
- Polices en local (`assets/fonts/*.woff2`, OFL) : copier le bloc `@font-face` ci-dessous dans **chaque** cadre.

## Depth & Surface

Plat. Aucune ombre, aucun halo, aucune lueur, aucun dégradé, aucun arrondi. Trois calques : la photo (assombrie par le voile), le message (bulles, carte), les filets et étoiles.

## Composants — CSS à copier tel quel dans chaque cadre

Les classes `lsq-` sont **partagées volontairement** : mêmes définitions dans chaque cadre, donc pas de collision possible. Les id et les classes propres à un cadre prennent le préfixe `<frame_id>-`.

```css
.lsq-fond{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;background:#0D0D0D}
.lsq-fond img{position:absolute;left:-135px;top:-240px;width:1350px;height:2400px;object-fit:cover}
.lsq-voile{position:absolute;inset:0;background:rgba(13,13,13,0.42)}
.lsq-q{position:absolute;left:108px;top:520px;max-width:780px;padding:30px 64px 32px 36px;background:#F4F1EC;color:#0D0D0D;
  font:500 50px/1.18 "DM Sans";clip-path:polygon(0 0,100% 0,calc(100% - var(--coupe,49px)) 100%,0 100%)}
.lsq-r{position:absolute;right:108px;top:700px;padding:34px 44px 38px 96px;background:#222222;color:#F4F1EC;text-align:right;
  font:900 150px/0.88 "Barlow Condensed";text-transform:uppercase;letter-spacing:-0.01em;font-variant-numeric:tabular-nums;
  clip-path:polygon(var(--coupe,92px) 0,100% 0,100% 100%,0 100%)}
.lsq-r .lsq-precision{display:block;margin-top:18px;font:italic 800 56px/1 "Barlow Condensed";letter-spacing:0.05em;color:#B8A07E}
.lsq-filet{position:absolute;top:0;bottom:0;left:0;width:6px;background:#B8A07E;transform-origin:50% 100%}
.lsq-saisie{position:absolute;right:108px;top:700px;width:190px;height:96px;background:#222222;
  clip-path:polygon(40px 0,100% 0,100% 100%,0 100%)}
.lsq-saisie i{position:absolute;top:42px;width:30px;height:12px;background:rgba(244,241,236,0.62);
  clip-path:polygon(5px 0,100% 0,calc(100% - 5px) 100%,0 100%)}
.lsq-avis{position:absolute;left:108px;top:700px;width:864px;padding:40px 52px 50px 52px;box-sizing:border-box;background:#0D0D0D;
  border:2px solid rgba(244,241,236,0.18);clip-path:polygon(0 0,calc(100% - 48px) 0,100% 114px,100% 100%,0 100%)}
.lsq-avis .lsq-haut{display:flex;align-items:center;justify-content:space-between;margin-bottom:30px}
.lsq-avis .lsq-etoiles{display:flex;gap:12px}
.lsq-avis .lsq-etoiles svg{width:50px;height:50px}
.lsq-avis .lsq-source{font:italic 800 38px/1 "Barlow Condensed";letter-spacing:0.05em;color:rgba(244,241,236,0.62);text-transform:uppercase}
.lsq-avis .lsq-texte{font:500 66px/1.12 "DM Sans";color:#F4F1EC}
.lsq-avis .lsq-guillemet{color:#B8A07E;font-weight:700}
```

- **Étoile** : `<svg viewBox="0 0 24 24"><path d="M12 1.6l3.1 6.9 7.5.7-5.7 5 1.7 7.4L12 17.8l-6.6 3.8 1.7-7.4-5.7-5 7.5-.7z"/></svg>`. Avant de s'allumer : `fill:none; stroke:rgba(244,241,236,0.62); stroke-width:1.4`. Allumée : `fill:#B8A07E; stroke:#B8A07E`.
- **Coupe d'une bulle** : `--coupe` = 0,42 × hauteur de la bulle. Bulle de la cliente sur une ligne (116 px) : 49 px ; sur deux lignes (175 px) : 74 px. Réponse de LA SALLE : 0,42 × sa hauteur (≈ 92 px pour 220 px, ≈ 120 px pour 285 px).
- **Filet or de la bulle de LA SALLE** : un `div.lsq-filet` dans la bulle (`left: 0`), penché pour suivre la coupe. Penchez-le avec GSAP, pas en CSS (sinon GSAP écrase la transformation) : `gsap.set(filet, { skewX: -22.78, transformOrigin: "0% 100%" })`. Il se trace de bas en haut (scaleY 0 → 1, `fromTo`) quand la réponse frappe.
- **Indicateur de saisie** : 3 barres `<i>` à `left: 42px, 82px, 122px`.

## Motion

- Une idée par temps (0,5 s à 120 BPM). Les instants viennent de `tools/cues.json` : chaque bulle, chaque étoile, chaque coupe de fond tombe sur un temps ou une double croche (0,125 s).
- Entrées : glissement masqué, coupe oblique qui s'ouvre (clip-path), frappe d'échelle (slam). **Jamais d'opacité** pour faire entrer ou sortir un élément, jamais de fondu enchaîné.
- Bulle de la cliente : monte de 40 px et passe de l'échelle 0,92 à 1 en 0,18 s (power3.out), son bord coupé s'ouvre de gauche à droite.
- Réponse de LA SALLE : frappe (échelle 1,22 → 1, 0,22 s, power4.out), le filet or se trace en même temps ; la précision glisse depuis le bas dans son masque un temps plus tard.
- Saisie : la bulle s'ouvre en 0,1 s ; les barres s'allument en or l'une après l'autre (0, 0,125, 0,25 s), puis la saisie laisse sa place à la réponse au temps suivant.
- Carte d'avis : frappe (échelle 1,1 → 1, y 30 → 0, 0,22 s) ; les étoiles s'allument une par une en doubles croches (échelle 1,5 → 1).
- Fond : photo en léger zoom avant continu (échelle 1,0 → 1,06 sur sa durée), coupes sèches sur les temps. Pendant les tenues, seul le fond bouge.

## What NOT to Do

- Pas d'écran noir ni de logo en ouverture : l'image 0 montre déjà la façade et la première question.
- Pas d'interface d'application, de téléphone, de barre d'état, d'avatar ni d'icône de personne. Pas de logo Google : « AVIS GOOGLE » est écrit en texte.
- Pas de look IA, de dégradé, de couleur vive, de halo, de glitch, d'arrondi, d'ombre.
- Pas de prix, d'offre, de date, de chiffre hors de ceux du brief. Pas de nom d'auteur d'avis.
- Ne jamais corriger, compléter ni mettre en capitales le texte d'un avis.
- Pas de tutoiement : LA SALLE vouvoie.
- Pas d'opacité animée, pas de fondu.

## Approved Entities

LA SALLE · Urban Valley · Conflans-Sainte-Honorine · musculation · cardio · Avis Google.

## Numerals & Claims (hard rule)

Seuls ces chiffres existent : 6H – 23H · 7J/7 · 1 200 m² · 5 étoiles (la note de chacun des deux avis cités). Aucun autre chiffre, aucun prix, aucune date.

## Pre-Render Self-Audit

1. Image 0 : façade visible, première question lisible, en-tête en place.
2. Chaque avis est cité mot pour mot (« Super salle super propre » ; « Accueil chaleureux. »), sans nom.
3. Les bulles tombent sur les temps de `tools/cues.json`.
4. Rien d'important hors des zones utiles.
5. Mentions présentes sur la carte finale, sur fond opaque.

## Font loading (auto-generated)

The brand font ships as local files in `assets/fonts/` — do NOT link Google Fonts for it. Paste this `<style>` into every frame's `<head>`/`<template>` (captions use the same files) so `font-family` resolves in preview, snapshot, and render alike:

```html
<style>
@font-face{font-family:"Barlow Condensed";font-weight:700;font-style:italic;font-display:block;src:url("assets/fonts/BarlowCondensed-700-Italic.woff2") format("woff2");}
@font-face{font-family:"Barlow Condensed";font-weight:700;font-style:normal;font-display:block;src:url("assets/fonts/BarlowCondensed-700.woff2") format("woff2");}
@font-face{font-family:"Barlow Condensed";font-weight:800;font-style:italic;font-display:block;src:url("assets/fonts/BarlowCondensed-800-Italic.woff2") format("woff2");}
@font-face{font-family:"Barlow Condensed";font-weight:800;font-style:normal;font-display:block;src:url("assets/fonts/BarlowCondensed-800.woff2") format("woff2");}
@font-face{font-family:"Barlow Condensed";font-weight:900;font-style:italic;font-display:block;src:url("assets/fonts/BarlowCondensed-900-Italic.woff2") format("woff2");}
@font-face{font-family:"Barlow Condensed";font-weight:900;font-style:normal;font-display:block;src:url("assets/fonts/BarlowCondensed-900.woff2") format("woff2");}
@font-face{font-family:"DM Sans";font-weight:400;font-style:normal;font-display:block;src:url("assets/fonts/DMSans-400.woff2") format("woff2");}
@font-face{font-family:"DM Sans";font-weight:500;font-style:normal;font-display:block;src:url("assets/fonts/DMSans-500.woff2") format("woff2");}
@font-face{font-family:"DM Sans";font-weight:700;font-style:normal;font-display:block;src:url("assets/fonts/DMSans-700.woff2") format("woff2");}
</style>
```
