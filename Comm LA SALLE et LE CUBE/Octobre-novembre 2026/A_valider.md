# Kit de communication LA SALLE et LE CUBE : octobre et novembre 2026

Rien n'est publié ni envoyé. Brouillon livré le 23/10/2026 pour validation par Mehdi et Nicolas.
Il suit le calendrier de communication du Drive (S43 à S48) et le plan de communication de novembre à janvier.

## Ce qu'il contient

| Fichier | Contenu |
|---|---|
| `S43_19-25_octobre.md` à `S48_23-29_novembre.md` | Chaque semaine, pour LA SALLE et LE CUBE : la légende du post prête à copier, le script de la story écran par écran, le texte alternatif, la publication pour la fiche Google, et les points à vérifier |
| `visuels/` | 60 visuels typographiques (30 posts 4:5 et 30 stories 9:16), sans photo ni personne, prêts à publier une fois validés |
| `Pubs_novembre.md` | Les pubs Meta de novembre : déjà livrées, nouvelles (Vos questions v2, Black Friday ×2, cartes cadeaux) et leurs ⚠ |
| `Messages_adherents.md` | E-mails et SMS pour SmartMessaging : fin des 4 semaines Premium, parcours de fidélisation, 11 novembre, Black Friday |
| `../Rayon nutrition/` | Rubrique « Rayon nutrition » de LA SALLE (ajoutée le 28/10) : une story par semaine et un post tous les quinze jours, de novembre à janvier, avec ses propres points à valider |

## Semaine par semaine

| Semaine | LA SALLE | LE CUBE |
|---|---|---|
| S43 · 19 – 25 oct. | Heure d'hiver : 5 astuces (carrousel 7) | Teasing boxe : de 50 à 400 m² ⚠ |
| S44 · 26 oct. – 1er nov. | Option Premium : l'analyse 3D ⚠ (visuels du kit Premium), story Halloween ⚠ | Le nouveau studio de boxe ouvre ⚠ date |
| S45 · 2 – 8 nov. | Coach du mois (photo à prendre), story Movember | Débuter le CrossFit : 5 questions (carrousel 7) |
| S46 · 9 – 15 nov. | Quel cours est fait pour vous ? (carrousel 8), 11 novembre ⚠ | Athlète du mois (photo à prendre) |
| S47 · 16 – 22 nov. | Venez à deux ⚠ conditions | Pole : séance d'essai remboursée ⚠ |
| S48 · 23 – 29 nov. | Black Friday ⚠ offre | Black Friday version CUBE ⚠ offre |

## ⚠ À trancher, par ordre d'urgence

1. **Date d'ouverture du studio de boxe :** elle conditionne S43 (compte à rebours) et S44.
2. **Balance connectée en service ?** Si oui, S44 version A ; sinon version B (fontaine).
3. **Halloween :** cours du samedi 31 octobre et idée du déguisement.
4. **Coach du mois et athlète du mois :** qui, avec quelle autorisation écrite pour la photo.
5. **Horaires et cours du mercredi 11 novembre.**
6. **BODYATTACK et GRIT au planning ?** Ils sont retirés du carrousel S46 tant que ce n'est pas confirmé.
7. **Parrainage :** quel avantage, pour qui, jusqu'à quand. Le calendrier disait « Ramène ton pote », qui tutoie : la phrase devient « Venez à deux » pour LA SALLE.
8. **Pole :** la séance d'essai à 25 € remboursée en cas d'abonnement est-elle toujours valable ?
9. **Black Friday :** l'offre, ses dates, l'engagement et les formules. Bloquant pour toute la semaine S48 et pour les deux pubs.
10. **Cartes cadeaux :** existent-elles déjà, avec quels montants, quelle validité et quelles conditions ?
11. **SmartMessaging :** comment arrêter l'option Premium, si la mention STOP est ajoutée automatiquement aux SMS, et si l'application sert aussi aux réservations du CUBE.
12. **Compte LE CUBE :** tant qu'il n'existe pas, les posts LE CUBE partent sur CrossFit CSH, Boxing Club Conflans et Pole Dance Conflans.

## À corriger dans le calendrier du Drive

Je n'ai pas modifié le calendrier du Drive (lecture seule). Quatre changements sont à reporter :
- S40 : « engagement d'un an » sur l'option devient « sans engagement sur l'option » ;
- S41 : « Avant / après » devient « Le chantier et la salle aujourd'hui » ;
- S47 : « Ramène ton pote » devient « Venez à deux » ;
- S48 : « Inscrivez-vous à l'accueil ou en ligne » devient « Inscrivez-vous à l'accueil ».

## Règles appliquées partout

- LA SALLE vouvoie, LE CUBE tutoie.
- Aucun prix ni aucune offre hors de ceux du calendrier ou déjà validés ; les offres non validées portent ⚠.
- Aucune promesse de résultat, de minceur ou d'énergie ; aucune liste d'ingrédients de la fontaine.
- Aucun avis Google réutilisé (plan d'action A1).
- Aucune personne sur les visuels produits ; les photos à prendre exigent une autorisation écrite.
- Pas de musique Les Mills.
- Chartes : noir, blanc et gris pour LA SALLE, avec le trait penché du monogramme ; noir et bronze pour LE CUBE ; Oswald, Inter et Anton.

## Pour refaire les visuels

`python3 "motion design/comm-oct-nov/tools/visuels.py"` (ou `… visuels.py S46` pour une semaine). Les textes des visuels sont dans ce script.
Pubs : `~/.venvs/hyperframes-audio/bin/python "motion design/comm-oct-nov/tools/pubs.py"` (Black Friday et cartes cadeaux) et `python3 "motion design/lasalle-questions-v2/tools/qc.py"` après le rendu de « Vos questions » v2.
