# Stories nutrition à l'accueil : à valider avant publication

Rien n'est publié. Brouillon livré le 20/10/2026 pour validation par Mehdi.

Les images et vidéos montrent le visuel partenaire Nutripure, avec ses deux modèles, et le rayon de l'accueil. Elles ne sont donc **pas** dans le dépôt GitHub (public) : elles ont été envoyées directement.

## Les 4 stories, à publier dans cet ordre

| # | Story | Contenu | Fichiers |
|---|---|---|---|
| 1 | Les deux marques | Photo du rayon, « DISPONIBLES À L'ACCUEIL », « NUTRIMUSCLE & NUTRIPURE », bande LA SALLE | `LA_SALLE_Nutrition_1_marques_story_9x16` |
| 2 | Nutrimuscle | Direction artistique Nutrimuscle (marine, fiche sobre), gros plan des pots, 5 références | `LA_SALLE_Nutrition_2_nutrimuscle_story_9x16` |
| 3 | Nutripure | Direction artistique Nutripure (italique gras, bleu ciel), visuel partenaire officiel, pastille « Disponible à l'accueil de LA SALLE » | `LA_SALLE_Nutrition_3_nutripure_story_9x16` |
| 4 | Une question ? | Les deux marques côte à côte, zone libre pour un sticker Question, bande LA SALLE | `LA_SALLE_Nutrition_4_question_story_9x16` |

- **Formats :** chaque story existe en image fixe (`images/*.jpg`) et en vidéo animée de 5 s (`videos/*.mp4`). Vous choisissez l'une ou l'autre.
- **Caractéristiques techniques :** 1080×1920, 30 i/s, H.264, piste son muette.
- **Contrôles :** GO technique pour les 4 dans `controles/QC_nutrition.txt` (format, durée, textes, mots interdits). La planche est dans `controles/planche_nutrition.jpg`.
- **Direction artistique :** relevée dans les supports officiels des marques, voir `motion design/lasalle-nutrition-916/frame.md`. Les sites et Instagram des marques sont bloqués par le réseau de la session.
- **Source :** `motion design/lasalle-nutrition-916/` (`tools/build.py`, `tools/livrer.py`).

**Stickers à ajouter dans Instagram :**
- story 1 : sticker Lieu « LA SALLE » ;
- story 4 : sticker Question « Une question sur Nutrimuscle ou Nutripure ? », placé dans la zone libre entre les cartes et la bande du bas.

Pour la musique, prendre un titre de la bibliothèque Instagram.

## ⚠ À confirmer

1. **Le stock du jour.** Les références citées viennent de l'état du stock au 30/09 et de la photo du rayon :
   - Nutrimuscle : Native Whey Protimuscle, Lean Gainer Whey & Avoine, Créatine Creapure®, Collagène Peptan® et Naticol®, Citrate de magnésium ;
   - Nutripure : Muscle Protein, Créatine, Shaker.

   Certaines étaient en très petite quantité. Il faut vérifier qu'elles sont toujours en rayon le jour de la publication. Je retire ce qui manque.
2. **Daily Protein (Nutripure).** Le visuel partenaire montre « DAILY & MUSCLE PROTEIN » et les deux sachets. Le stock du 30/09 ne mentionne que la Muscle Protein. Si la Daily n'est pas vendue à l'accueil, je recadre le visuel sur le seul sachet Muscle Protein.
3. **Le visuel partenaire Nutripure.** Nutripure l'a fourni aux salles partenaires, avec la mention « Disponible dans votre salle ». Il montre deux modèles et la mention « NOUVEAU ».
   - Il faut confirmer avec le commercial Nutripure qu'on peut le reprendre dans les stories Instagram de LA SALLE.
   - Sinon, je le remplace par une version purement typographique.
4. **La photo du rayon.**
   - Il faut confirmer qu'elle a été prise à l'accueil de LA SALLE et que le rayon est toujours rangé ainsi.
   - Aucune personne n'y apparaît. Le cadrage exclut la caméra, l'extincteur et les effets personnels.
   - On voit aussi d'autres marques sur la photo complète, mais le cadrage les écarte, sauf quelques pots de pâte à tartiner sur la story 1.
5. **Le logo LA SALLE.** C'est le logo provisoire. À remplacer dès réception des fichiers définitifs.
6. **« L'équipe vous présente les références disponibles. »** (story 4) L'équipe de l'accueil doit être prévenue. Dans les réponses aux questions, ne promettre aucun effet : ni prise de muscle, ni récupération, ni performance (règlement UE 432/2012).

Ce qui a été écarté volontairement :
- les prix, ainsi que la remise Nutripure, réservée aux revendeurs ;
- l'« Offre Santé », qui ne s'adresse pas aux adhérents ;
- toute allégation de santé ;
- tout logo de marque redessiné.
