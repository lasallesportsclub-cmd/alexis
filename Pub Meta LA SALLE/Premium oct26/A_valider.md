# À valider avant diffusion : option Premium LA SALLE

Liste des ⚠ du kit, à trancher par Mehdi. **Rien n'est publié.**

## Déjà validé le 13/10/2026 (Mehdi ou Alexis)

- Offre : 4 premières semaines de l'option offertes, en ce moment, sans date de fin.
- Engagement : « sans engagement sur l'option », confirmé une seconde fois. ⚠ Le calendrier de communication du Drive (S40) dit encore « engagement d'un an sur l'option » : il faut le mettre à jour pour qu'il ne contredise pas les visuels.
- Salle de posing : pas de date, donc citée avec « BIENTÔT » et jamais montrée.
- Nom à l'écran : « Fontaine à boisson sportive ».
- Pastille : la ligne « EN CE MOMENT · EN PLUS DE VOTRE ABONNEMENT » est ajoutée sous la version courte du §4, avec un « + » en négatif dans la pastille or.
- Réplique 25 : « OFFERTES » tombe quand la voix l'aurait dit (vers 10,0 s). Conséquence : la carte finale des vidéos dure environ 2,7 s au lieu de 3,68 s.
- Vidéos : « fais sans les voix et musique ». Les 6 vidéos (A, B, C en story 9:16 et en post 4:5) sont livrées sans voix ni musique, avec les bruitages seuls. Le texte à l'écran garde le minutage prévu pour la voix. Il y a une seule version par vidéo, puisque sans musique les versions « avec » et « sans » seraient identiques.
- Versions post 4:5 des vidéos : « Oui, maintenant ».
- Voix (14/10/2026) : « c'est signé, utilise le ton pub pour les vidéos, fais plutôt toi-même une voix la plus humaine possible ». Les 6 vidéos existent maintenant aussi avec voix (voir la dernière section). Les versions sans voix restent dans `videos/`.

## À trancher

1. **Logo provisoire.** Les images utilisent le logo de la signature mail du Drive (170 px), mis en version négative. Il est net jusqu'à 170 px de large, ce qui est le cas des images. Pour les vidéos (carte finale à environ 280 px) et pour une netteté maximale, déposez `mono.png` et `word.png` du kit du PC dans `motion design/_sources-premium/`. Je régénère alors tout en une commande.
2. **Balance 3D en service ?** Le kit dit « une analyse 3D par semaine » (brief du 12/10 : en service à partir du 13/10). Le plan d'action du Drive mettait encore « salle de posing et balance connectée en service » à l'échéance du 31/12. Ne publiez le concept C et la slide 3 du carrousel que si la balance est réellement disponible.
3. **« Booster » et « multivitamines »** (réplique P4 et images B). Ce sont des allégations nutritionnelles implicites. « Multivitamines » n'est licite que si la boisson apporte au moins 7,5 % des VNR pour 100 ml (règlements 1169/2011 et 1924/2006). À vérifier sur la fiche GYMWA. Repli proposé : « caféine » au lieu de « booster », et le nom exact de la boisson au lieu de « multivitamines ».
4. **Caféine et cadence.** Le livret ingrédients indique 50 mg de caféine par verre de Power Drink et une limite de 200 mg en une prise. Avec une boisson toutes les 30 minutes, quelqu'un peut en boire 4 en 2 h. C'est hors publicité, mais à considérer, par exemple un affichage « Teneur élevée en caféine » sur la machine.
5. **Slide 5 du carrousel.** L'offre et le prix y forment un seul bloc : « 4 SEMAINES OFFERTES DE L'OPTION PREMIUM », puis « PUIS +2 € TTC PAR SEMAINE », puis « SOIT 8 € TOUTES LES 4 SEM. · EN PLUS DE VOTRE ABONNEMENT ». Ce bloc remplace la ligne exacte du §4 « PUIS 2 € TTC/SEM. (8 € TOUTES LES 4 SEM.) », qui disait la même chose.
6. **Rappel « FONTAINE · ANALYSE 3D · POSING (BIENTÔT) ».** « (BIENTÔT) » est ajouté au rappel du §6 pour tenir compte de Q3.
7. **Musique au moment de publier.** Les vidéos n'ont pas de musique. Si vous ajoutez une musique au moment de publier (un titre de la Sound Collection par exemple), réglez les deux volumes pour que les bruitages restent audibles sans couvrir la musique. Avec les versions voix, la musique doit rester nettement sous la voix. Étiquette IA : aucune pour les versions sans voix ; pour les versions avec voix, voir le point 2 de la dernière section.
8. **Hors kit, mais important.** Le document « Retours LP » (juillet) indique que l'option serait une case **pré-cochée** au moment de l'inscription. Le droit de la consommation interdit de faire payer une option par une case pré-cochée : il faut un consentement exprès. À vérifier dans Resamania et dans le parcours d'inscription.

## Plans sans accord écrit (NE PAS DIFFUSER)

Aucun. Le kit ne montre aucune personne (réponse Q5 : aucun rush). Pour le tournage du 18/10, utilisez `Autorisation_droit_image.md`.

## Versions avec voix « ton pub » (14/10/2026)

Les 6 vidéos existent aussi avec voix : `LA_SALLE_Premium_{A,B,C}_{story_9x16,post_4x5}_voix.mp4`. Elles ne sont **pas sur GitHub** : le dépôt est public, et la voix d'une personne n'y va pas (`videos_voix/` est ignoré par git). Elles vous sont envoyées dans la conversation ; déposez-les sur le Drive du club. Contrôles : `controles/QC_videos_voix.txt`.

Pour une voix aussi humaine que possible, chaque réplique vient de l'enregistrement autorisé quand il la contient, bien dite. Sinon, c'est la voix clonée (Chatterbox) sur la référence « ton pub », celle de l'essai que vous avez retenu.

| Réplique | Texte dit | Source | Vidéos |
|---|---|---|---|
| P1 | Passez en version Premium. | prise réelle | A |
| P2 | Votre boisson vous attend. | prise réelle | B |
| P3 | Vos progrès, en trois D. | **voix clonée** : la phrase n'est pas dans l'enregistrement | C |
| P4 | Collagène, multivitamines, L-carnitine, booster… ou simplement de l'eau. | prise réelle, pauses resserrées et accélérée ×1,12 (sinon 5,9 s pour 4,1 s de scène) | B |
| P5 | Une boisson toutes les trente minutes. | **voix clonée** : dans l'enregistrement, on entend « toutes les dix minutes » | A, B |
| P6 | Une analyse en trois D, chaque semaine. | prise réelle | A, C |
| 25 | Les quatre premières semaines de l'option Premium sont offertes. | **voix clonée** : la phrase n'est pas dans l'enregistrement | A, B, C |
| P9 | Activez-la à l'accueil, en quelques secondes. | prise réelle | A, B, C |

Le texte à l'écran est recalé sur la voix : chaque ligne tombe une image avant son mot. Rien n'est ajouté ni retiré à l'écran. Ce qui bouge par rapport aux versions sans voix :

- A : le trait sous « PREMIUM » passe à 0,8 s ; « UNE BOISSON » arrive à 2,3 s, « TOUTES LES 30 MINUTES » à 2,8 s ; « UNE ANALYSE EN 3D » à 4,2 s, « CHAQUE SEMAINE » à 5,5 s.
- B : la liste dure jusqu'à 4,7 s (un mot par produit), puis « OU SIMPLEMENT DE L'EAU » jusqu'à 6,0 s, puis « UNE BOISSON TOUTES LES 30 MINUTES ». La transition entre ces deux dernières scènes devient une coupe sèche au lieu d'un volet, faute de place.
- C : « UNE ANALYSE EN 3D » arrive à 2,0 s, « CHAQUE SEMAINE » à 3,2 s.
- Fin commune : « SEMAINES » frappe à 8,73 s (au lieu de 8,44 s), « OFFERTES » à 9,9 s (au lieu de 10,0 s), « EN QUELQUES SECONDES » passe de 13,4 s à 13,7 s.

Son : voix et bruitages, sans musique (la musique reste un titre de la Sound Collection à ajouter à la publication, voir le point 7). Les bruitages sont baissés sous la voix et les impacts raccourcis : pendant la parole, ils restent au moins 6 dB sous la voix. Sonie −14 LUFS, crête vraie ≤ −1,5 dBTP.

### ⚠ À trancher pour les versions avec voix

1. **Écoute (bloquant).** J'ai contrôlé par mesures et par retranscription automatique que chaque mot attendu est prononcé, pas le ton. Écoutez les 6 fichiers, surtout les répliques clonées (P3, P5, 25) et P4 accélérée. Pour la 25, j'ai écarté une prise accélérée où « Premium » devenait ambigu. Si une réplique sonne faux, j'ai d'autres prises : 22 prises exactes de la 25, 24 de P3 et de P5. Dites-moi laquelle remplacer.
2. **Mention IA (bloquant).** P3, P5 et la 25 sont générées par IA à partir de la voix d'une personne réelle. Le règlement européen sur l'IA (art. 50, applicable depuis le 2 août 2026) demande de signaler un contenu audio généré par IA qui imite une personne réelle. Une voix clonée a de bonnes chances d'être concernée, même avec autorisation. Meta demande aussi l'étiquette « Info IA » pour un son réaliste généré par IA. Deux voies :
   - publier avec l'étiquette « Info IA » activée, et ajouter « Voix en partie générée par IA » dans les mentions (5 minutes, je régénère) ;
   - ou faire réenregistrer P3, P5 (en disant bien « trente ») et la 25 par la même personne : la voix devient entièrement réelle et la question disparaît. Une prise par phrase suffit, envoyée sur le Drive.
3. **Cases de l'autorisation.** L'autorisation signée a deux cases d'usage : les publications du club, et les publicités payantes sur Instagram et Facebook. Si ces vidéos passent en publicité, vérifiez que la seconde est cochée, ainsi que la durée. L'autorisation engage aussi le club à signaler l'IA quand la plateforme le demande (point 2).

Pour régénérer : `voix.py` (prépare les répliques depuis `~/voix-clone`, hors dépôt), puis `video.py --voix A B C` et `video.py --45 --voix A B C`, rendu, `master.py`, puis `qc_voix.py`. Sans `--voix`, `video.py` reconstruit les versions sans voix telles que livrées le 13/10.
