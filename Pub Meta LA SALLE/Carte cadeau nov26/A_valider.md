# À valider avant diffusion : carte cadeau LA SALLE (Noël 2026)

Demande du 18/11/2026 : une vidéo qui présente la carte cadeau « de la valeur dont la personne le souhaite »
(100, 150, 200, 300 € ou montant au choix), entièrement déductible sur un abonnement, vendue à l'accueil.
**Rien n'est publié** : tout est montré pour validation.

## Les trois stories (12 s, 1080×1920, 30 i/s, 120 BPM)

| Story | Accroche (0–2 s, en place à l'image 0) |
|---|---|
| A « Offrez » (`videos/LA_SALLE_Carte_cadeau_story_A_offrez_9x16.mp4`) | CARTE CADEAU · NOËL · OFFREZ LA SALLE. et la carte 150 € |
| B « La question » (`videos/LA_SALLE_Carte_cadeau_story_B_question_9x16.mp4`) | VOUS NE SAVEZ PAS QUOI OFFRIR ? et la carte 150 € |
| C « Le montant » (`videos/LA_SALLE_Carte_cadeau_story_C_montant_9x16.mp4`) | OFFREZ-LUI 150 € SUR SON ABONNEMENT. |

Suite commune : 2–6,5 s COMMENT ÇA MARCHE, la carte et son montant qui défile (100, 150, 200, 300 €, puis MONTANT AU
CHOIX), 01 Choisissez le montant. 02 Offrez-la à qui vous voulez. 03 Elle est déduite de son abonnement. ·
6,5–7 s ET EN PLUS, (musique coupée) · 7–9 s LES FRAIS D'INSCRIPTION 45 € (barré) OFFERTS. · 9–12 s EN VENTE À
L'ACCUEIL., les montants, Urban Valley · 7j/7 · 6h–23h, mention.

Chaque story existe aussi en version `_bruitages` (sans musique, −18 LUFS) pour poser une musique de la Sound
Collection dans Instagram. Plan de test : les trois accroches dans le même ensemble de publicités, budget égal, lecture
du taux à 3 s et du coût par résultat après 3 à 4 jours, on garde la gagnante.

## Points ⚠ à trancher

1. **Frais d'inscription offerts (45 €)** à la personne qui reçoit la carte : proposé le 18/11, pas encore confirmé
   (l'autre piste était une séance d'essai offerte, déjà offerte à tous). Si c'est non, on retire les scènes
   « ET EN PLUS, » et « 45 € OFFERTS. » : la story passe à 9,5 s.
2. **Montant au choix** : « ça peut être possible aussi ». Il apparaît sur la carte (MONTANT AU CHOIX) et sur la carte
   finale (« ou le montant de votre choix »). À confirmer, avec un montant minimum éventuel.
3. **Mention** : « Montant entièrement déductible sur un abonnement LA SALLE, pour la personne qui reçoit la carte.
   Conditions à l'accueil. » Les conditions restent à écrire (durée de validité, carte non remboursable, utilisable ou
   non par un adhérent déjà inscrit, report du reste sur le prélèvement suivant).
4. **La carte dessinée** dans la vidéo est une maquette dans la charte (surface anthracite, filet et ruban or, logo
   négatif). Si une carte physique est imprimée avec un autre dessin, il faut aligner la vidéo sur la vraie carte.
5. **Musique** : originale, synthétisée (graine fixe, aucun morceau sous droits), avec des grelots sur l'accroche et la
   fin. Contrôlée par mesures seulement (−14 LUFS, crête vraie ≤ −1,5 dBTP) : à écouter avant validation.

Aucune date de fin n'est annoncée, donc aucune mention d'urgence. Aucune photo de personne, aucun visuel de marque.

## Livrables

| Fichier | Contenu |
|---|---|
| `videos/*_9x16.mp4` | Les trois stories avec musique |
| `videos/*_9x16_bruitages.mp4` | Les mêmes, bruitages seuls |
| `controles/QC_carte_cadeau.txt` | Rapport de contrôle (66 contrôles réussis) |
| `controles/planche_*_4ips.jpg` | Planches à 4 images par seconde avec les zones Reels en rouge |
| `controles/image0_*.jpg` | L'image 0 de chaque accroche |
| `Textes_publication.md` | Légende, texte de publicité, message pour l'accueil |

Les vidéos ne sont pas sur GitHub (fichiers lourds) : elles sont envoyées dans la conversation, à déposer sur le Drive
du club. Sources : `motion design/lasalle-carte-cadeau/` (tools/build.py, musique.py, livrer.py).
