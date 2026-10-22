---
workflow: general-video
flow: automation
storyboard: no
message: "La fontaine à boisson sportive de l'option Premium : votre boisson à la carte, 1 boisson toutes les 30 min, +2 € TTC/sem., à activer à l'accueil"
destination: instagram-stories
aspect: 1080x1920 (story) et 1080x1350 (affiche)
language: fr
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
angle: promo
narration: no
---

## Intent

Demande du 22/10/2026, dans ses mots : « retravaille ce visuel pour que les textes soient bien apparents » (affiche 02/03
« COMMENT ÇA MARCHE »), puis « réalise une vidéo motion avec HyperFrames […] une petite story, ou une vidéo en montrant
chaque texte de chaque visuel […] un petit défilé de chaque affiche », ou des pistes pour filmer un adhérent ou un coach.

Livré :
- `affiche-45/` : l'affiche 02/03 recomposée, mêmes textes mot pour mot, sur le fond plat de la série (plus de photo de
  salle floue sous le texte), corps de texte en blanc cassé et plus gros, puces opaques, mention lisible sur panneau.
- `story-916/` : les 6 visuels rejoués texte par texte en 22 s, 60 i/s (6 scènes, coupes sur la grille de 120 BPM,
  dévoilements en biais de 0,9 s sous un filet or).
- Guide de tournage : `Pub Meta LA SALLE/Fontaine oct26/Guide_tournage.md`.

## Sources

- Visuels fournis dans la conversation : capture de l'affiche 02/03 (seul fichier reçu, 674×817) et 5 visuels du carrousel
  (BIEN PLUS QUE DE L'EAU, ÉTAPE 02, ÉTAPE 03, +2 €, ACTIVEZ-LA À L'ACCUEIL), vus mais non reçus en fichiers : ils sont
  reconstruits en HTML (mêmes polices, mêmes couleurs, mêmes textes). Le zip annoncé n'est pas arrivé.
- Fontaine : détourée de la capture par `tools/detourer.py` (résolution faible, voir A_valider.md). Hors dépôt :
  `~/fontaine-sources/` (photo fabricant, logo de la marque à l'écran).
- Logo : « LA_SALLE_logo_fond-noir » du Drive (2600 px), recadré et teinté #F4F1EC dans `_communs/img/`.
- Polices et GSAP : `_sources-premium/` (Barlow Condensed, DM Sans, OFL ; GSAP 3.14.2).
- Musique : synthèse originale, `tools/musique.py` (instruments de `lecube-chrono`), graine fixe.

## Chaîne

```sh
~/.venvs/hyperframes-audio/bin/python -I tools/detourer.py ~/fontaine-sources/affiche_02_03_capture.webp ~/fontaine-sources/fontaine_detouree.png
~/.venvs/hyperframes-audio/bin/python -I tools/musique.py && ~/.venvs/hyperframes-audio/bin/python -I tools/musique.py --bruitages
~/.venvs/hyperframes-audio/bin/python -I tools/build.py
(cd story-916 && npx --yes hyperframes@0.8.181 check --timeout 60000 && npx --yes hyperframes@0.8.181 render --fps 60 --quality delivery -o renders/story.mp4)
~/.venvs/hyperframes-audio/bin/python -I tools/livrer.py
```

## Notes

- Charte « Le Trait Oblique » (`_sources-premium/shared/frame.md`) : #0D0D0D, #F4F1EC, or #B8A07E, surface #222,
  pente 0,42, vouvoiement.
- Retours du 22/10 sur la v1 : « tout est compact » → story plein cadre (texte entre x 96–984 et y 210–1 660, pensée
  pour les Stories) ; transitions « pixelisées, comme un souci de connexion » (la bande traversait 3 900 px en 0,5 s,
  jusqu'à 400 px par image) → dévoilement de 0,9 s, 60 i/s, CRF 16 ; « Saveur, intensité » visible avant
  « ÉCRAN TACTILE » (cache plus haut que le texte) → caches à la hauteur réelle du texte.
- Image 0 de la story : « + OPTION PREMIUM », le logo et « BIEN PLUS QUE DE L'EAU. » déjà en place.
- Cassure de 0,5 s (14,5–15 s, musique coupée) avant « + 2 € ».
- Diffusion organique. Rien n'est publié sans l'accord de Mehdi.
