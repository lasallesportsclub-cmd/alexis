# Pubs LE CUBE par discipline : à valider avant diffusion

Rien n'est publié. Brouillon livré le 19/10/2026 pour validation par Mehdi.

On voit des personnes dans ces vidéos. Les MP4 et les images de contrôle ne sont donc **pas** dans le dépôt GitHub (public) : ils ont été envoyés directement. Les photos sources restent sur le Drive.

| Discipline | État |
|---|---|
| Pole Dance | **Livrée** : `LE_CUBE_Pole_Dance_story_9x16.mp4` |
| Boxing Club | En attente d'images de pratiquants (voir plus bas) |
| CrossFit CSH | En attente d'images de pratiquants (voir plus bas) |

## Pole Dance

- **Fichier :** 1080×1920, 30 i/s, 15,0 s, H.264, 6,4 Mo.
- **Son :** pas de voix. La musique est originale (120 BPM, synthétisée pour cette pub), sans morceau sous droits. −14,1 LUFS, crête vraie −1,7 dBTP.
- **Contrôles :** `controles/QC_pole.txt` donne un GO technique. La planche avec les zones Reels et l'image 0 ont été envoyées avec la vidéo.
- **Nom dans Meta :** `CUBE_POLE_A_story_musique_v1`. Ses scènes sont dans le skill « lasalle-pub-resultats ».
- **Source :** `motion design/lecube-disciplines/`. Le montage est généré par `tools/build.py` à partir de `tools/cues_pole.json`.

| Temps | À l'écran |
|---|---|
| 0 – 2 s | Un mot par temps, chacun sur sa photo : **FORCE.** (drapeau), **SOUPLESSE.** (pont), **ÉQUILIBRE.** (équilibre sur les mains), **GAINAGE.** (dos). Le premier mot est déjà à l'écran à l'image 0. |
| 2 – 3 s | « TOUT ÇA, SUR UNE BARRE. » sur la photo noir et blanc. |
| 3 – 8,5 s | Quatre étapes numérotées : 01 « TU COMMENCES AU SOL. » · 02 « TU MONTES SUR LA BARRE. » · 03 « TU PASSES TÊTE EN BAS. » · 04 « TU T'ENVOLES. » |
| 8,5 – 9 s | « ET TOI ? » sur noir. La musique se coupe. |
| 9 – 11,5 s | « PAS BESOIN D'ÊTRE SOUPLE POUR COMMENCER. », puis « ÇA SE TRAVAILLE ICI. » |
| 11,5 – 15 s | Carte finale, avec un chevron vers le bouton :<br>• POLE DANCE, AU CUBE · CONFLANS ;<br>• DE L'INITIATION À L'INTER · CERCEAU ;<br>• RÉSERVE TA SÉANCE D'ESSAI ;<br>• LE CUBE · ZAC DES BOUTRIES · CONFLANS-SAINTE-HONORINE. |

Le bandeau « POLE DANCE · LE CUBE » reste en haut de 0 à 11,5 s. Celui qui décroche tôt sait déjà où il est.

### ⚠ À confirmer

1. **Droit à l'image (bloquant).** On reconnaît chaque personne. Il faut une autorisation écrite qui couvre **la publicité payante sur Meta**, pas seulement les réseaux du club, pour :
   - toutes les personnes visibles sur les photos 1 à 7 du shooting pole du 12/11/2025 (Drive, dossier « POLE DANCE ») : au moins deux hommes et une femme. La photo 8, l'interview, n'est pas utilisée ;
   - la personne de la série pole noir et blanc de 2023 (photo DSC01363).

   Il faut aussi vérifier que le contrat des photographes autorise un usage publicitaire : le shooting de 2025 d’une part, celui de la série de 2023 d’autre part. Sans ces accords, je remplace les photos concernées.
2. **Le lieu.** Les photos ont été prises dans le studio de pole aux grandes baies vitrées. La carte finale dit « AU CUBE » et donne l'adresse ZAC des Boutries. Si les cours de pole n'ont pas lieu au CUBE, je change l'adresse et le bandeau.
3. **Niveaux.** « DE L'INITIATION À L'INTER · CERCEAU » vient du planning du CUBE. Est-ce toujours vrai ? Le cerceau est cité mais n'apparaît sur aucune photo.
4. **Ton.** « TU PASSES TÊTE EN BAS. » et « TU T'ENVOLES. » décrivent la progression des niveaux, pas un résultat promis en un temps donné. À valider.
5. **Séance d'essai.** Il faut confirmer qu'elle existe en pole et comment on la réserve. Ensuite, choisir le bouton Meta : « Réserver » ou « Envoyer un message ». Aucun prix n'est affiché.
6. **Compte de diffusion.** Le compte LE CUBE n'existe pas encore. Faut-il publier depuis la page pole du club ?
7. **Musique.** Elle est à écouter avant validation : je n'ai pu la contrôler que par mesures.

Images écartées volontairement :
- les photos de scène et de compétition (dossier « Photos Affiche », championnat) : les athlètes peuvent venir d'autres clubs ;
- toutes les images d'enfants.

## Boxing Club et CrossFit CSH : ce qui manque

J'ai cherché sur le Drive, dans Canva et du côté de Meta :
- **Drive, CrossFit :** il y a les rushs pro du 17/10/2025 (dossiers « C1 CRoss FIT » et « C2 cross fit », de 34 Mo à 7 Go par fichier). Le connecteur Drive ne télécharge pas les fichiers de plus de 10 Mo. Seules deux photos de coach aux anneaux (IMG_1773, IMG_1783, septembre 2025) sont exploitables : c'est trop peu pour 15 s.
- **Drive, boxe :** aucune photo ni vidéo avec des personnes.
- **Canva :** les designs « coach boxe », « PUBLIS COACHS » et « Intense Boxing Gym Vibe » contiennent des photos. Le réseau de cette session bloque leur téléchargement (`export-download.canva.com`).
- **Meta / Instagram :** inaccessible depuis cette session.

Pour débloquer, au choix :
1. **Déposer sur le Drive** 8 à 12 photos, ou des extraits vidéo de 3 à 6 s, par discipline, **chacun sous 10 Mo**. Un export 1080p depuis le téléphone suffit. Le dossier « 06 Photos et vidéos » convient.
2. **Ouvrir le réseau** de la session aux domaines `export-download.canva.com` et `design.canva.ai`. Je récupère alors les visuels Canva moi-même.

Le gabarit est prêt (`tools/cues_<discipline>.json`). Dès que les images sont là, chaque pub prend environ une heure.
