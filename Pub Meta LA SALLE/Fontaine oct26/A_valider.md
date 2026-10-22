# À valider avant diffusion : fontaine à boisson sportive LA SALLE

Liste des ⚠ à trancher par Mehdi. **Rien n'est publié.**

## Livrables

| Fichier | Format | Contenu |
|---|---|---|
| `images/LA_SALLE_Fontaine_affiche_02-03_post_4x5.png` (+ `.jpg`) | 1080×1350 | L'affiche 02/03 « COMMENT ÇA MARCHE » retravaillée : mêmes textes, mot pour mot |
| `videos/LA_SALLE_Fontaine_story_9x16.mp4` | 1080×1920, 22 s, 60 i/s | Les 6 visuels rejoués texte par texte, avec musique originale et bruitages |
| `videos/LA_SALLE_Fontaine_story_9x16_bruitages.mp4` | 1080×1920, 22 s, 60 i/s | La même, bruitages seuls (pour ajouter une musique de la Sound Collection dans Instagram) |
| `Guide_tournage.md` | — | Les plans à filmer avec un coach ou un adhérent pour une version plus humaine |
| `controles/` | — | Rapport QC, planche à 2 i/s avec les zones Reels, image 0 |

Les images et vidéos ne sont pas sur GitHub (dépôt public, photo fabricant avec le logo de la marque) : elles sont
envoyées dans la conversation, à déposer sur le Drive du club.

### Ce qui a changé sur l'affiche 02/03

- Le texte ne repose plus sur la photo de salle floue : fond plat #0D0D0D de la série (bandes obliques à peine visibles).
- Corps de texte des légendes en blanc cassé (au lieu du gris), 31 px au lieu d'environ 19 px.
- Puces des boissons opaques (#222), texte 37 px.
- « 5 SAVEURS » sur deux lignes, saveurs en capitales blanches de 40 px (au lieu de l'or clair sur une ligne).
- Mention caféine sur un panneau opaque, 27 px au lieu d'environ 12 px.
- Contraste vérifié par `check` : 95 textes sur 95 au niveau WCAG AA.

### Déroulé de la story (22 s, 120 BPM, 60 i/s)

Version 2 (retours du 22/10) : plein cadre et textes plus grands ; transitions plus lentes et fluides ; la légende
« ÉCRAN TACTILE 17″ » apparaît dans l'ordre (point et flèche, titre, puis texte : le texte n'apparaît plus avant).

| Temps | Visuel rejoué | Mouvement |
|---|---|---|
| 0–2,5 s | BIEN PLUS QUE DE L'EAU. | déjà en place à l'image 0, filet or qui se trace, sous-titre |
| 2,5–7,5 s | COMMENT ÇA MARCHE · VOTRE BOISSON, À LA CARTE. | la fontaine monte, point, flèche, titre puis texte de la légende, les 6 boissons une à une, mention caféine |
| 7,5–11,5 s | ÉTAPE 02 · CHOISISSEZ VOTRE SAVEUR | les 5 saveurs glissent une à une (pleines et au trait) |
| 11,5–14,5 s | ÉTAPE 03 · SERVEZ-VOUS · 1 BOISSON TOUTES LES 30 MIN | « 30 MIN » frappe, l'horloge trace une demi-heure |
| 14,5–18,5 s | + L'OPTION PREMIUM · +2 € TTC PAR SEMAINE · 3 AVANTAGES | 0,5 s de silence, puis « + 2 € » frappe ; les 3 bandes entrent |
| 18,5–22 s | ACTIVEZ-LA À L'ACCUEIL. EN QUELQUES SECONDES. | logo, appel, horaires, mentions ; immobile sur la fin |

Entre deux visuels : le visuel suivant se dévoile en biais (pente du monogramme) sous un filet or, en 0,9 s avec une
accélération douce ; le visuel qui sort glisse légèrement vers la gauche. Rendu en 60 images/s, encodage plus fin
(CRF 16) pour éviter les blocs sur les fonds sombres.

## À trancher

1. **Photo de la fontaine (le point le plus visible).** La seule source reçue est la capture de l'affiche (674×817 px) :
   la fontaine y fait 380 px de large. Je l'ai détourée, nettoyée (pastilles, filets et texte qui la recouvraient) et
   agrandie, mais elle reste un peu douce. De plus, le logo de la marque est lisible sur l'écran de la machine, ce que la
   charte exclut (« pas de logo de marque tierce »). Deux solutions :
   - photographier la vraie fontaine au club (voir le plan 8 du guide de tournage) : meilleure qualité, image réelle du
     club, et un angle où le logo n'est pas au centre ;
   - ou m'envoyer la photo d'origine du fabricant (fichier PNG ou JPG, pas une capture), avec son accord pour un usage
     publicitaire.
   Dans les deux cas, je remplace le fichier et je régénère l'affiche et la story en une commande.
2. **Faits repris des visuels, absents du brief validé du 13/10** : « écran tactile 17″ », « saveur, intensité,
   température », « BCAA » (absent de la liste validée : collagène, multivitamines, L-carnitine, booster, eau),
   « 7J/7 · 6H–23H » et « DÈS LE 22/10 » pour l'analyse 3D. Je les ai gardés mot pour mot. À confirmer.
3. **« DÈS LE 22/10 ».** La story sera vue après le 22/10 : si l'analyse 3D est bien en service, je propose
   « EN SERVICE », comme pour la fontaine.
4. **« Multivitamines »** reste une allégation nutritionnelle implicite (point 3 du kit Premium) : licite seulement si
   la boisson apporte assez de vitamines (au moins 7,5 % des VNR pour 100 ml pour une boisson). À vérifier sur la fiche
   produit, sinon remplacer par le nom exact de la boisson. Collagène, L-carnitine et BCAA sont cités comme choix, sans
   effet attribué : rien à changer.
5. **Nom de la fontaine.** Le nom validé (Q4) est « FONTAINE À BOISSON SPORTIVE ». Les visuels disent « fontaine à
   boissons sportives » (couverture) et « FONTAINE À BOISSONS » (bande 01). Repris tels quels ; je peux harmoniser.
6. **Étape 01.** Le carrousel commence à « ÉTAPE 02 ». Dans la story, l'affiche « COMMENT ÇA MARCHE » tient lieu
   d'étape 1. S'il existe un visuel « ÉTAPE 01 », envoyez-le en image et je l'ajoute.
7. **Légende « 1 BOISSON / 30 MIN » de l'affiche 02/03.** Elle n'est pas répétée dans la scène 2 de la story, puisque
   la scène 4 dit la même chose avec la même phrase.
8. **Mentions.** Celle du prix reprend votre texte (« Conditions à l'accueil »). Le kit Premium disait « Sans
   engagement sur l'option » : la question de l'engagement (calendrier S40 du Drive) reste ouverte. Dans la story, les
   mentions font 32 et 36 px sur panneau opaque (27 px sur l'affiche), sous le plancher de 40 px de la charte.
9. **Musique.** Synthèse originale, sans droits à payer ni crédit, contrôlée par mesures seulement (−14 LUFS, crête
   ≤ −1,5 dBTP) : à écouter avant validation. Sinon, prenez la version « bruitages seuls » et ajoutez une musique de la
   Sound Collection en publiant, en gardant les bruitages audibles.
10. **Durée et usage.** 22 s pour 6 visuels, en story organique, mise en page plein cadre (texte jusqu'à y ≈ 1 650).
    Publiée en Reel, la légende et les boutons d'Instagram peuvent recouvrir le bas de certaines scènes (mentions,
    bandes des avantages) : dites-moi si elle doit aussi servir en Reel, je fais une variante. Pour une publicité Meta, il faudrait une version de
    15 s et 3 ou 4 accroches à tester (méthode de la pub motion) : dites-moi si vous la voulez.
11. **Vidéos libres de droits en ligne.** Les banques de vidéos (Pexels, Pixabay) sont bloquées dans cette session. De
    plus, une vidéo de banque montre une autre salle et des inconnus, alors que la charte privilégie les vraies images
    du club : d'où le guide de tournage.

## Plans sans accord écrit (NE PAS DIFFUSER)

Aucun. Aucune personne n'apparaît dans ces fichiers.
