# Pub LE CUBE tirée du film V1 : à valider avant diffusion

Rien n’est publié. Brouillon livré le 23/10/2026 pour validation par Mehdi.

**État : animatique.** Le film « LE CUBE V1 » (99,6 Mo) est trop lourd pour le connecteur Drive. Les trois vidéos `LE_CUBE_V1_<V>_story_9x16_ANIMATIQUE.mp4` ont donc :
- le montage définitif : rythme, textes, motion design, carte finale et musique ;
- un carton gris numéroté à la place de chaque plan du film (« PLAN 20 · figure devant la baie vitrée »).

Elles servent à valider le déroulé, pas à diffuser. Dès que les images du film sont disponibles (voir ⚠ 1), les mêmes commandes produisent les vidéos finales.

Le montage suit le doc « Pub réseaux LE CUBE — analyse du film V1 et plan de montage ». Les étapes sont recalées sur la grille de la musique : 3,0 / 4,5 / 6,0 / 7,5 / 8,5 s.

## 3 variantes pour un test A/B

Les trois vidéos sont identiques de 3 à 15 s. Seule l’accroche (0–3 s) change, pour savoir quel angle retient le mieux.

| Variante | Accroche (0–3 s) | Plans du film | Nom dans Meta |
|---|---|---|---|
| **A · Tout est au Cube** | « HYROX, CROSSFIT, POLE, BOXE. » (déjà là à l’image 0), puis « TOUT EST AU CUBE. », « À CONFLANS. » | 20, 32, 8 (1 s chacun) | `CUBE_V1_A_story_musique_v1` |
| **B · Ton sport à Conflans** | « TU CHERCHES TON SPORT À CONFLANS ? », puis « IL EST PEUT-ÊTRE ICI. » | 20 (1 s), 32 (1,3 s), 8 (0,7 s) | `CUBE_V1_B_story_musique_v1` |
| **C · Tu tiens ?** | « 4 SPORTS EN 15 SECONDES. », puis « TU TIENS ? » | 8, 4, 20, 32 (0,75 s chacun) | `CUBE_V1_C_story_musique_v1` |

La variante D du doc (avec une offre) n’est pas faite : aucune offre n’est confirmée.

Partie commune (3 – 15 s) :

| Temps | Plans du film | À l’écran |
|---|---|---|
| 3 – 4,5 s | 3 SkiErg, 5 rameur, 9 wall balls | **01** HYROX · TU POUSSES. |
| 4,5 – 6 s | 13 toes-to-bar, 16 épaulé-développé | **02** CROSSFIT · TU SOULÈVES. |
| 6 – 7,5 s | 17 studio pole, 19 figure inversée | **03** POLE DANCE · TU T’ENVOLES. |
| 7,5 – 8,5 s | 33 pattes d’ours, 35 sparring | **04** BOXE · TU FRAPPES. |
| 8,5 – 9 s | noir | « ET TOI ? ». La musique se coupe sur un impact grave. |
| 9 – 10,5 s | images fixes 30 ring, 29 tatamis, 14 rig | « UN RING. », « DES TATAMIS. », « UN RIG. » : une ligne par image |
| 10,5 – 11,5 s | 25 échauffement autour des sacs | « TOUT ÇA, À CONFLANS. » |
| 11,5 – 15 s | image fixe 1, logo peint au sol, sous un voile | Carte finale :<br>• LE CUBE ;<br>• HYROX · CROSSFIT · POLE DANCE · BOXE ;<br>• RÉSERVE TA SÉANCE D’ESSAI ;<br>• un chevron vers le bouton ;<br>• ZAC DES BOUTRIES · CONFLANS-SAINTE-HONORINE. |

Le bandeau « LE CUBE · CONFLANS » reste en haut de 0 à 11,5 s.

- **Fichiers :** 1080×1920, 30 i/s, 15,0 s, H.264.
- **Son :**
  - pas de voix ;
  - musique originale à 120 BPM, synthétisée pour cette pub, sans morceau sous droits ; les coups de l’accroche suivent le texte de chaque variante ;
  - effets sonores : souffles aux coupes et impact sur « ET TOI ? », tirés de la bibliothèque Pixabay (usage commercial sans attribution) ;
  - −14 LUFS, crête vraie ≤ −1,5 dBTP.
- **Contrôles :** `controles/QC_v1.txt`. Les planches avec les zones Reels ont été envoyées avec les vidéos.
- **Source :** `motion design/lecube-v1/` : `tools/cues_v1.json` (instants, plans du film, recadrages), `tools/build.py`, `tools/musique.py`, `tools/livrer.py`.

**Plan de test (une fois les vraies images en place) :**
- mettre les trois variantes dans le même ensemble de publicités, avec un budget égal et le même texte ;
- après 3 à 4 jours, lire le taux d’accroche (part des impressions encore là à 3 s) et le coût par résultat ;
- garder la meilleure.

## ⚠ À confirmer

1. **Les images du film (bloquant).** Au choix :
   - déposer sur le Drive 3 extraits du film, sans le son, au même format (1920×1080, 50 i/s), compressés vers 6 000 kbit/s pour rester vers 4 Mo chacun : **0 – 5,5 s**, **5,3 – 11 s** et **10,8 – 16 s** ;
   - ou ouvrir le réseau de la session à `drive.google.com` et `drive.usercontent.google.com`, et partager par lien une copie du film.

   Ensuite, il faut un quart d’heure environ : découpe des plans, recadrage, ralentis, rendu des 3 variantes, contrôle, puis un regard sur chaque plan en pleine résolution. L’outil vérifie qu’aucune coupe du film ne tombe dans un plan.
2. **Droit à l’image (bloquant).** On reconnaît des personnes dans les plans 3, 4, 5, 8, 9, 13, 16, 17, 19, 20, 25, 32, 33 et 35. Il faut une autorisation écrite de chacune, qui couvre **la publicité payante sur Meta**. Les images fixes 1, 14, 29 et 30 (logo au sol, rig, tatamis, ring) doivent être vides de personnes : à vérifier sur les vraies images.
3. **Contrat RM Visual.** Il doit autoriser la publicité payante, le remontage, le recadrage en 9:16 et les ralentis.
4. **HYROX et CrossFit.** Ce sont des marques déposées. Les citer dans une pub suppose que LE CUBE soit partenaire HYROX et box affiliée CrossFit. Sinon, je remplace par « ENTRAÎNEMENT FONCTIONNEL » ou « CROSS-TRAINING ».
5. **Marques visibles.** Une marque se lit sur le short du plan 32, qui ouvre les trois accroches. Si c’est gênant, je mets un autre plan. Les plans 12 (tee-shirt Rogue) et 27 (maillot de l’équipe de France) ne sont pas utilisés.
6. **Mineurs.** Il faut vérifier qu’aucun mineur n’apparaît, surtout dans le plan 25 (échauffement en groupe).
7. **Séance d’essai et bouton.** Il faut confirmer qu’une séance d’essai existe dans les quatre disciplines et comment on la réserve. Ensuite, choisir le bouton Meta : « Réserver » ou « Envoyer un message ». Aucun prix n’est affiché.
8. **Lieu.** La carte donne une seule adresse, ZAC des Boutries, pour les quatre disciplines. Le studio pole aux baies vitrées est-il bien au CUBE ?
9. **Logo.** La carte montre le logo peint au sol, filmé dans le film : il n’est pas redessiné. Pour le logo officiel en surimpression, il me faut le fichier (PNG ou SVG).
10. **Ralentis.** Quelques plans sont ralentis sous 60 %, donc avec quelques images doublées : 4 (variante C), 13, 16, 19, et 20 dans A et B. À regarder sur les vraies images. Sinon, je raccourcis ces plans.
11. **Compte de diffusion.** Depuis quelle page diffuser, tant que le compte LE CUBE n’existe pas ?
12. **Musique.** Elle est à écouter avant validation : je n’ai pu la contrôler que par mesures.

Plans écartés (doc d’analyse) :
- 2 et 6 : enseigne d’une autre société ;
- 10, 11, 22, 23, 24 et 26 ;
- 18 : bas du dos ;
- 7, 15, 21, 31 et 34 : transitions floues.
