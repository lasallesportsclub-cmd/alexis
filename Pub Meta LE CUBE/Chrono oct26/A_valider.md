# Pub LE CUBE « LE CHRONO » : à valider avant diffusion

Rien n'est publié. Ce brouillon a été livré le 19/10/2026 pour validation par Mehdi.

## Les fichiers

Il y a trois versions qui ne diffèrent que par l'accroche (0 à 3 s), pour un test A/B :

| Fichier | Accroche | Nom dans Meta |
|---|---|---|
| `LE_CUBE_Chrono_A_story_9x16.mp4` | A · le chiffre : « 165 COURS EN UNE SEMAINE. UN SEUL LIEU. » | `CUBE_CHRONO_A_story_musique_v1` |
| `LE_CUBE_Chrono_B_story_9x16.mp4` | B · le défi : « T'AS 15 SECONDES ? ON TE MONTRE TOUT. » | `CUBE_CHRONO_B_story_musique_v1` |
| `LE_CUBE_Chrono_C_story_9x16.mp4` | C · la nouvelle : « BOXING CLUB CONFLANS · ~~50 m²~~ 400 m² · ÇA CHANGE TOUT. » | `CUBE_CHRONO_C_story_musique_v1` |

- **Format :** 1080×1920, 30 i/s, 15,0 s, H.264. Chaque fichier pèse de 7 à 8 Mo et convient aux Reels comme aux Stories.
- **Son :** pas de voix. La musique est originale, à 120 BPM, synthétisée pour cette pub, sans morceau sous droits. Sonie −14,1 LUFS, crête vraie −1,7 dBTP.
- **Contrôles :**
  - `controles/QC_videos.txt` : GO technique pour les trois ;
  - `controles/planche_<V>_2ips.jpg` : zones masquées par Reels en rouge ;
  - `controles/image0_<V>.jpg`.
- **Source :** `motion design/lecube-chrono/`, compositions HyperFrames générées par `tools/build.py`, livraison par `tools/livrer.py`.
- **Suivi des résultats :** les noms Meta ci-dessus et les scènes sont déjà dans le skill « lasalle-pub-resultats ». Garder ces noms tels quels pour que le bilan hebdomadaire retrouve les vidéos.

## Ce que montre la vidéo

Un chrono de séance (00:15 → 00:00) reste en haut de l'écran du début à la fin. Il change à chaque seconde, sur les bips de la musique, et chaque discipline est un round.

| Temps | À l'écran |
|---|---|
| 0 – 3 s | L'accroche (A, B ou C, voir plus haut). |
| 3 – 4,5 s | ROUND 1 · CROSSFIT CSH · WOD · HALTÉRO · GYM, sur le rig puis le chrono LED. |
| 4,5 – 6 s | ROUND 2 · HYROX · ENDURANCE · ENGINE · SIMULATION, sur la piste puis les rameurs. |
| 6 – 7,5 s | ROUND 3 · BOXING CLUB · ANGLAISE · KICK · MMA · MUAY THAÏ, sur le portique puis le ring. |
| 7,5 – 8,5 s | ROUND 4 · POLE DANCE · DE L'INITIATION À L'INTER · CERCEAU, en typographie seule : une barre et un cercle bronze. |
| 8,5 – 9 s | « ET TOI ? » sur noir. La musique se coupe. |
| 9 – 11,5 s | « PAS BESOIN D'ÊTRE EN FORME POUR COMMENCER. » puis « C'EST POUR ÇA QU'ON EST LÀ. » |
| 11,5 – 15 s | Carte finale :<br>• LE CUBE et ses 4 disciplines ;<br>• « RÉSERVE TA SÉANCE D'ESSAI », avec un chevron vers le bouton ;<br>• ZAC DES BOUTRIES · CONFLANS-SAINTE-HONORINE.<br>Le chrono arrive à 00:00 et passe en bronze plein (14,5 s). |

## ⚠ À confirmer

1. **Version A, « 165 cours en une semaine ».** Ce chiffre vient du relevé Resamania du 14/10/2026 : 165 créneaux du 12 au 18 octobre. Il change d'une semaine à l'autre. Faut-il le garder tel quel, ou passer à « plus de 150 cours par semaine », qui reste vrai plus longtemps ?
2. **Version C, « de 50 à 400 m² ».** Le chiffre vient du calendrier de communication (teasing S43).
   - Le nouveau studio est-il ouvert ? Tant qu'il ne l'est pas, cette version ne peut pas sortir.
   - Les photos du tatami et du ring montrent-elles bien le nouvel espace ?
   - Je n'ai pas utilisé la vidéo `travaux_cube-V4` du Drive, donc la version C n'a pas d'images avant / après. Je peux en ajouter si elles ne montrent personne de reconnaissable.
3. **Marques HYROX et CrossFit.** La pub payante affiche les noms « HYROX » et « CROSSFIT CSH ». Vérifier que l'accord HYROX du club autorise la publicité, et que les règles d'affilié CrossFit sont respectées. Aucun logo de ces marques n'est à l'image.
4. **Intitulés des cours.** Ils sont repris du planning du CUBE :
   - WOD · HALTÉRO · GYM ;
   - ENDURANCE · ENGINE · SIMULATION ;
   - ANGLAISE · KICK · MMA · MUAY THAÏ ;
   - DE L'INITIATION À L'INTER · CERCEAU.

   Sont-ils tous encore au planning ?
5. **Séance d'essai.** La carte finale dit « RÉSERVE TA SÉANCE D'ESSAI ». Confirmer :
   - qu'elle existe dans toutes les disciplines ;
   - comment on la réserve ;
   - quel bouton Meta mettre sous la pub (« Réserver » ou « Envoyer un message »).

   Aucun prix n'est affiché. Pour une publication organique, sans bouton, il faut une version sans chevron (5 minutes).
6. **Adresse.** « ZAC DES BOUTRIES · CONFLANS-SAINTE-HONORINE » vient du formulaire d'autorisation du CUBE (ZAC des Boutries, 8 rue Léonard de Vinci, 78700 Conflans-Sainte-Honorine). Faut-il ajouter la rue ?
7. **Logo.** Je n'ai trouvé aucun fichier de logo LE CUBE sur le Drive. « LE CUBE » est donc écrit en Oswald. Avec le logo, je refais la carte finale.
8. **Pole Dance.** Je n'ai aucune photo du studio sans personne, donc le round 4 est typographique. Une photo du studio vide, ou des images de personnes qui ont signé une autorisation, le rendraient plus fort.
9. **Compte de diffusion.** Le compte LE CUBE n'existe pas encore. Depuis quelle page la pub part-elle (par exemple CrossFit CSH) ?
10. **Musique.** Elle est à écouter avant validation. Elle est faite maison, et je n'ai pu la contrôler que par mesures, pas à l'oreille.

## Conseil pour le test

- **Démarrage :** lancer A et B ensemble, avec le même budget, la même audience et le même texte. Ajouter C seulement quand le nouveau studio est ouvert.
- **Indicateur :** le taux d'accroche, c'est-à-dire la part des impressions encore là à 3 s, départage les deux versions.
- **Règle :** ne rien modifier pendant la phase d'apprentissage.

## Règles respectées

- Le tutoiement est utilisé partout.
- Rien n'est affiché sans source :
  - aucun prix, aucune offre, aucune date ;
  - aucun avis ;
  - aucune promesse de résultat.
- Aucune personne à l'image. Les 12 photos du CUBE (Drive, dossier des pages du site) sont recadrées et étalonnées en noir et bronze. Il n'y a ni logo dessiné, ni fausse photo.
- Charte LE CUBE :
  - noir #0A0A0A et bronze #B27639, aucun rouge ;
  - polices Oswald, Inter et Anton (OFL).
- Le contenu clé reste entre y 290 et 1 250 px, hors de la colonne d'icônes Reels.
