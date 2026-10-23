---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Avant de venir, on se pose des questions : LA SALLE y répond, et ce sont ses avis Google qui le disent."
destination: meta-reels
aspect: 1080x1920
language: fr
audience: "habitants de Conflans-Sainte-Honorine et alentours, 18-55 ans, qui hésitent à pousser la porte d'une salle"
length: 15s
angle: "conversation mise en scène entre une cliente et LA SALLE : questions fréquentes, réponses vérifiées, avis Google réels"
narration: no
---

## Intent

Demande du 14/10/2026, dans ses mots : « j'aimerai que tu réalise une publicité sans voix juste avec de la musique de 15 sec il faudrait mettre en situation une conversation avec une cliente et la salle ou on nous pose des questions communues ou on répond aux interrogations et il faut prendre depuis notre page google des avis qui te semble pertinent pour mettre en avant la structure tout ça en ryhtme avec la musique il faut utiliser hyper frame /product-launch-video ».

Pub Meta 15 s en 9:16 pour LA SALLE, Urban Valley, Conflans-Sainte-Honorine. Une cliente pose les questions qu'on entend à l'accueil ; LA SALLE répond quand c'est un fait vérifiable, et laisse ses avis Google répondre quand c'est une question de ressenti (propreté, accueil). Pas de voix : une musique originale, et chaque bulle, chaque étoile et chaque coupe tombe sur un temps. Vouvoiement, ton direct et chaleureux.

## Assets

- assets/img/ — vraies photos du club (Drive, dossier du kit et photos IMG_24xx), recadrées en 1350×2400 et étalonnées selon la charte : façade et enseigne, hall et escalier, tapis de course, haltères. Aucune personne à l'image.
  Exclus : plateau.jpg (trois adhérents reconnaissables), salle de vélos (cours collectifs = formule Privilège), étagère de compléments, portraits de coachs.
- assets/img/mono.png, word.png — logos du kit `kit_pub_motion_LA_SALLE_v2.zip` (Drive).
- assets/fonts/ — Barlow Condensed 700–900 (droit et italique) et DM Sans 400–700, woff2 @fontsource, licence OFL (copie de `_sources-premium/fonts/`).
- assets/vendor/gsap.min.js — GSAP 3.14.2 en local (les CDN sont bloqués dans le conteneur).
- assets/audio/ — musique originale synthétisée à 120 BPM en ré mineur, d'après la méthode du kit pub motion : aucun morceau sous droits, pas de MusicGen (licence non commerciale).

## Customizations

- Bulles de conversation dessinées dans la charte Le Trait Oblique : coupe oblique (pente 0,42), pas d'interface d'application, pas de téléphone, pas d'icône de personne.
- Les bruits de bulle sont des notes de la musique ; les 5 étoiles d'un avis arrivent en doubles croches.
- Coupes sur la grille 120 BPM (temps = 0,5 s), cassure de 0,5 s juste avant le second avis.

## Notes

- Déroulé : automatique, sans pause storyboard. Le plan est présenté avec la vidéo, qui est livrée en brouillon à valider. Rien n'est publié.
- Faits utilisés, tous déjà publiés par le club : 6H–23H · 7J/7, 1 200 m², musculation et cardio, Urban Valley · Conflans-Sainte-Honorine. Aucun prix, aucune offre, aucune date.
- Avis Google : seulement des textes d'origine complets, en français, reçus dans Gmail (lecture seule). Cités mot pour mot, sans le nom de l'auteur.
  - « Super salle super propre » : 5 étoiles, 13/10/2026.
  - « Accueil chaleureux. » : 5 étoiles, 12/10/2026 ; première phrase de l'avis.
- ⚠ Avis avec contrepartie : l'e-mail aux adhérents « Grande nouvelle : votre salle déménage » (15 et 20/07/2026) liait le maintien du tarif au dépôt d'un avis Google. Ces avis ne sont pas cités. Avant diffusion, confirmer que les deux avis retenus n'ont eu aucune contrepartie.
- Mentions à l'écran : « Conversation mise en scène. Extraits d'avis Google réels, cités sans modification. »
- Contenu clé entre y 290 et 1250 px et entre x 72 et 1008 px (zones Reels).
