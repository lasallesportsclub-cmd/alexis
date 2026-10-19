# frame.md — LE CUBE « LE CHRONO » (pub Meta 15 s, 9:16)

Source de vérité du design des trois versions A, B et C. Les compositions sont écrites par `tools/build.py`.

## Idée

Toute la pub est un chrono de séance : il décompte de 00:15 à 00:00, une seconde par temps (120 BPM), et
chaque discipline est un round. Le spectateur « fait » la séance en regardant. Les photos sont les vraies
images du CUBE, sans personne, étalonnées noir et bronze.

## Couleurs

| Rôle | Valeur |
|---|---|
| canevas | #0A0A0A |
| texte | #F5F2EC |
| texte secondaire | rgba(245,242,236,0.88) |
| bronze (accent unique) | #B27639 |
| voile sur photo | rgba(10,10,10,0.52) ; 0.66 sur les photos claires ou chargées (tatami, kettlebells, boxes, rig) |

Aucun rouge, aucun dégradé, aucune ombre, aucun fondu d'opacité. Le bronze sur noir fait 5,8:1.

## Typographie

- Titres : Oswald 700, capitales (noms des disciplines, phrases).
- Étiquettes : Oswald 600, capitales, interlettrage 0,25 em, bronze (« ROUND 1 »).
- Chiffres : Anton 400 (chrono, « 165 », « 50 m² », « 400 m² »).
- Texte : Inter 600, capitales, interlettrage 0,06 em.
Polices locales `assets/fonts/*.woff2` (OFL), déclarées dans chaque composition.

## Mise en page

- Zone utile Reels : y 290–1250, x 72–1008 ; rien d'important à droite de x 950 sous y 900.
- Chrono : boîte 400×128 centrée en haut (y 300–428), cadre bronze 3 px, chiffres Anton 104 px bronze ;
  « LE CUBE · CONFLANS » dessous (y 448). Il reste en place du début à la fin (calque au-dessus de tout).
- Rounds : étiquette bronze y 600, nom de la discipline y 660 (136 px), détail y 830, alignés à gauche x 96.
- Carte finale : centrée, « LE CUBE » y 520, disciplines y 750, appel à l'action y 840–1040, chevron, adresse y 1170.

## Mouvement

Coupes sèches sur les temps, une idée par temps. Entrées : frappe d'échelle (1,25 → 1 en 0,16 s), chute dans
un masque (110 % → 0), balayage par clip-path. Photos en zoom lent continu (1,00 → 1,06). Le chrono change de
chiffre à chaque tic avec une petite chute dans son masque ; à 00:00 la boîte passe en bronze plein.

## Règles

- Tutoiement (voix du CUBE). Aucun prix, aucune offre non validée, aucune promesse de résultat.
- Noms de disciplines tels qu'au planning : CROSSFIT CSH, HYROX, BOXING CLUB, POLE DANCE.
- Pas de logo dessiné : « LE CUBE » est écrit en Oswald tant que le logo n'est pas fourni.
- Aucune personne à l'image ; pas de photo de pole dance disponible : le round 4 est typographique.
