---
workflow: general-video
flow: automation
storyboard: no
message: "L'analyse 3D Visbody M60 de l'option Premium : bien plus qu'une balance, une balance IA ; 1 analyse par semaine, +2 € TTC/sem., à activer à l'accueil"
destination: instagram-stories
aspect: 1080x1920 (story) et 1080x1350 (affiche)
language: fr
audience: "adhérents LA SALLE et abonnés Instagram, 18+"
angle: promo
narration: no
---

## Intent

Demande du 22/10/2026, dans ses mots : « réalise de nouveau une vidéo motion mais cette fois-ci pour parler de la balance
Visbody. Bien présenter le fait que c'est pas qu'une simple balance, ponctuation sur le fait que c'est une balance IA,
recherche également sur leur site […] l'IA intégrée permet également de produire des programmes pour les personnes
scannées (chose que tu peux rajouter sur une des affiches en respectant la charte graphique des documents) », puis
trois visuels de plus à intégrer.

Livré :
- `story-916/` : 9 scènes, 39 s, 60 i/s. Accroche « BIEN PLUS QU'UNE BALANCE. », ponctuation en coupe sèche sur le
  silence « UNE BALANCE / IA. », puis les 8 visuels fournis rejoués texte par texte, l'avatar 3D scanné (demande
  suivante, voir plus bas) et la scène « VOTRE PROGRAMME, PAR L'IA. ».
- `affiche-45/` : le visuel « VOTRE PROGRAMME, PAR L'IA. » au format des affiches du carrousel (1080×1350).

## Avatar scanné (demande du 22/10/2026)

Dans ses mots : « intégrer une personne comme ça sur la balance (sur la vidéo elle serait dos au spectateur) […] un
film qui scannerait la personne […] dos à nous, bras le long du corps, de couleur grise contrairement au bleu sur la
photo et tu fais passer un scan de haut en bas et de bas en haut […] l'avatar apparaît d'abord […] des bruits lors du
scan pour donner un aspect scientifique et futuriste », puis « que l'avatar soit mieux dessiné et paraisse plus
humain ».

- `_communs/js/avatar.js` (Three.js 0.185.1, MIT, dans `_communs/vendor/`) : silhouette décrite par une distance
  signée (ellipsoïdes et cônes arrondis fusionnés en douceur : crâne, chignon, oreilles, trapèzes, omoplates, sillon de
  la colonne, dorsaux, fessiers, ischios, mollets, talons, coudes, pouces), polygonisée par marching cubes (160³), matière
  grise, cheveux plus soutenus. Rendue depuis le temps de la scène (tween GSAP → rendre(t)), donc seek déterministe.
- Scan : plan or (anneau et voile translucide) ; à la descente, tours or au-dessus du front ; à la remontée, lignes
  verticales sous le front ; bande claire sur le front. Lignes nettes, sans halo (charte).
- Son (`tools/musique.py`) : faisceau glissant, cliquetis de données, carillon, apparition ; batterie coupée pendant
  le scan.

## Recherche Visbody (22/10/2026)

Le site visbody.com est bloqué en session cloud ; recherche web à la place (sources commerciales du fabricant et de
revendeurs, aucune vérification indépendante) :
- la M60 est vendue comme « Expert 3D Body Scanner & AI Body Composition Analyzer » : impédancemétrie 8 électrodes
  multifréquence, modèle 3D à 360°, composition, mensurations, posture ; comparaison des résultats d'une analyse à
  l'autre ;
- les **programmes d'entraînement personnalisés par l'IA** relèvent de la plateforme **Visbody WellnessHub** (abonnement
  à part) : le coach saisit l'objectif de l'adhérent et le système génère un programme adapté aux machines de la salle.
  D'où le ⚠ n° 1 de A_valider.md.
Pages : visbody.com/visbody-m60/, visbody.com/visbody-wellnesshub/, visbody.com (page d'accueil).

## Sources

- Visuels fournis dans la conversation (8) : couverture photo et couverture carrousel « VOS PROGRÈS, EN 3D. »,
  « UN SCAN À 360° » (02/03, avec la machine), « LE PRINCIPE », « CE QUE VOUS DÉCOUVREZ », « SUIVEZ VOTRE ÉVOLUTION »,
  « + 2 € », « ACTIVEZ-LA À L'ACCUEIL ». Captures hors dépôt dans `~/visbody-sources/`.
- Visbody M60 : détourée de la capture 02/03 par `tools/detourer.py` (formes mesurées, la machine sombre sur fond
  sombre ne se détoure pas au seuil). Hors dépôt : photo fabricant, logo de la marque à l'écran.
- Logo, polices, GSAP : `lasalle-fontaine/_communs/img/`, `_sources-premium/`.
- Musique : synthèse originale, `tools/musique.py` (instruments de `lecube-chrono`), graine fixe.

## Chaîne

```sh
~/.venvs/hyperframes-audio/bin/python -I tools/detourer.py ~/visbody-sources/3.webp ~/visbody-sources/m60_detouree.png
~/.venvs/hyperframes-audio/bin/python -I tools/musique.py && ~/.venvs/hyperframes-audio/bin/python -I tools/musique.py --bruitages
~/.venvs/hyperframes-audio/bin/python -I tools/build.py
(cd story-916 && npx --yes hyperframes@0.8.181 check --timeout 60000 && npx --yes hyperframes@0.8.181 render --fps 60 --quality delivery -o renders/story.mp4)
~/.venvs/hyperframes-audio/bin/python -I tools/livrer.py
```

## Notes

- Charte « Le Trait Oblique » et mise en page de la story fontaine v2 (retours du 22/10) : plein cadre, caches à la
  hauteur réelle du texte, dévoilements en biais de 0,9 s sous un filet or, 60 i/s, CRF 16.
- Image 0 : « + OPTION PREMIUM », le logo et « BIEN PLUS QU'UNE BALANCE. » déjà en place.
- Cassure de 0,5 s (2,5–3 s, musique coupée) : « UNE BALANCE » en coupe sèche, « IA. » frappe à la reprise.
- Les deux visuels « UN SCAN À 360° » forment une seule scène en deux temps : les 3 étapes (« LE PRINCIPE »), puis la
  machine et ses 3 légendes (« COMMENT ÇA MARCHE »), sous le même titre.
- Diffusion organique. Rien n'est publié sans l'accord de Mehdi.
