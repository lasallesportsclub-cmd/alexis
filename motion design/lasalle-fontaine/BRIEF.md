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
- `story-916/` : les visuels rejoués texte par texte et, depuis la v3, le parcours sur l'écran réel puis le versement :
  34,5 s, 60 i/s, 7 scènes, coupes sur la grille de 120 BPM, dévoilements en biais de 0,9 s sous un filet or.
- Guide de tournage : `Pub Meta LA SALLE/Fontaine oct26/Guide_tournage.md`.

## Version 3 : parcours sur l'écran et versement (demande du 22/10/2026)

Dans ses mots : « intégrer l'écoulement d'un liquide, présenter un peu plus la machine […] vous sélectionnez votre
goût, vous sélectionnez l'intensité, et ça remplit dans une quantité de 750 ml […] scanner votre QR code ou votre
carte physique, ensuite tu fais apparaître les différents goûts […] tu dis sélectionner votre intensité et après il
n'y a plus qu'à cliquer sur début et là après tu mets » (message coupé), avec 4 photos de l'écran de la fontaine.

- `tools/ecrans.py` : les 4 photos redressées (dalle 17″ en 5:4, 1280×1024), moiré de la photo d'écran, reflets de
  plafond et curseur de souris retirés ; cadre inox réel tiré de la photo 1 ; l'écran réel posé dans la dalle de la
  fontaine du visuel 02/03 (le rendu fabricant affichait une autre interface, avec la marque du fabricant).
- Scène 3 (7,5–19,5 s), étapes 01 à 05 : « SCANNEZ VOTRE QR CODE OU CARTE. » sur deux pictogrammes (QR code non
  lisible, carte du club stylisée), trait de lecture et coche ; puis l'appareil monte et l'écran réel suit l'ordre de
  l'interface : saveur (tap sur Multifruits), intensité (« moyen »), eau (« EAU FRAICHE »), récapitulatif et « Début ».
- Bascule (19,5 s) : la scène 4 monte avec son fond pendant que la 3 monte d'autant, l'appareil reste continu ; la
  caméra descend de l'écran à la buse.
- Scène 4 (19,5–24 s) : `_communs/js/versement.js` (canvas 2D, à plat) : jet en chute libre qui s'affine, gourde qui
  se remplit jusqu'à la graduation, bulles, gouttes, vaguelettes ; compteur jusqu'à la contenance affichée à l'écran
  (0,7 L, ⚠ 750 ml dans la demande), puis « SERVEZ-VOUS. ». Déterministe : rendre(t) ne dépend que de t.
- Son : « tic » à chaque choix, trait de lecture et carillon du scan, descente de la caméra, écoulement synthétisé
  (résonance de la gourde qui monte avec le niveau, bulles, éclaboussures), carillon au plein, gouttes ; batterie
  coupée pendant le versement.

## Sources

- Visuels fournis dans la conversation : capture de l'affiche 02/03 (seul fichier reçu, 674×817) et 5 visuels du carrousel
  (BIEN PLUS QUE DE L'EAU, ÉTAPE 02, ÉTAPE 03, +2 €, ACTIVEZ-LA À L'ACCUEIL), vus mais non reçus en fichiers : ils sont
  reconstruits en HTML (mêmes polices, mêmes couleurs, mêmes textes). Le zip annoncé n'est pas arrivé.
- Écrans de la fontaine : 4 photos reçues dans la conversation le 22/10 (2000×1500), hors dépôt dans
  `~/fontaine-sources/ecran/` (logo de la marque des concentrés à l'écran).
- Fontaine : détourée de la capture par `tools/detourer.py` (résolution faible, voir A_valider.md). Hors dépôt :
  `~/fontaine-sources/` (photo fabricant, logo de la marque à l'écran).
- Logo : « LA_SALLE_logo_fond-noir » du Drive (2600 px), recadré et teinté #F4F1EC dans `_communs/img/`.
- Polices et GSAP : `_sources-premium/` (Barlow Condensed, DM Sans, OFL ; GSAP 3.14.2).
- Musique : synthèse originale, `tools/musique.py` (instruments de `lecube-chrono`), graine fixe.

## Chaîne

```sh
~/.venvs/hyperframes-audio/bin/python -I tools/detourer.py ~/fontaine-sources/affiche_02_03_capture.webp ~/fontaine-sources/fontaine_detouree.png
~/.venvs/hyperframes-audio/bin/python -I tools/ecrans.py
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
- Cassure de 0,5 s (27–27,5 s, musique coupée) avant « + 2 € ».
- Diffusion organique. Rien n'est publié sans l'accord de Mehdi.
