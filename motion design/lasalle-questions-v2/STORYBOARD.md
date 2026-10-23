---
format: 1080x1920
duration: 15s
message: "Avant de venir, on se pose des questions : LA SALLE y répond, et ce sont ses avis Google qui le disent."
arc: Question → réponse (×2 faits) → question → avis Google (×2) → invitation → carte finale
audience: "habitants de Conflans-Sainte-Honorine et alentours, 18-55 ans, qui hésitent à pousser la porte d'une salle"
mode: autonomous
music: none
bpm: 120
beat: 0.5s
cues: tools/cues.json
---

# LA SALLE · « Vos questions » · plan

**Ce film dit aux habitants de Conflans qui hésitent que LA SALLE répond à leurs questions : ouverte de 6 h à 23 h, 7 jours sur 7, 1 200 m², et que la propreté et l'accueil, ce sont ses avis Google qui en parlent.**

| Cadre | Rôle · durée | À l'écran | Pourquoi |
|---|---|---|---|
| 01 — Horaires | accroche · 2,5 s | Façade réelle, la cliente demande l'heure ; LA SALLE frappe « 6H – 23H » puis « 7J/7 » | L'image 0 porte déjà le lieu et une question qu'on se pose tous ; la promesse tombe à 1 s |
| 02 — Taille | preuve · 2,5 s | « C'est grand ? » → « 1 200 m² » · « MUSCULATION · CARDIO » sur les tapis et les haltères | Un fait chiffré, vérifiable, sur de vraies images |
| 03 — Propreté | preuve sociale · 2,5 s | « Je suis exigeante… c'est propre ? » → carte Avis Google ★★★★★ « Super salle super propre » | Le ressenti, ce sont les clients qui le disent, pas la salle |
| 04 — Accueil | cassure + preuve sociale · 2,5 s | « Et l'accueil ? » → cassure (musique coupée, saisie géante) → drop : « Accueil chaleureux. » | Le temps fort du film : le second avis tombe sur le drop |
| 05 — Invitation | appel · 2 s | « Je peux passer voir ? » → « AVEC PLAISIR. ON VOUS ATTEND ! », puis le volet des 3 bandes | La conversation se ferme sur une invitation, le volet ouvre la carte |
| 06 — Carte finale | marque · 3 s | Monogramme assemblé par ses 3 bandes, LA SALLE, « UNE QUESTION ? ÉCRIVEZ-NOUS. », adresse, horaires, mentions | Une action simple, adaptée au bouton « Envoyer un message » de Meta |

- **Récit** : 5 questions de la vraie vie, 2 réponses factuelles, 2 avis Google, 1 invitation. Aucune voix : la musique porte le rythme et chaque bulle est une note.
- **Durée** : 15,0 s (450 images à 30 i/s). Grille 120 BPM, temps = 0,5 s, double croche = 0,125 s.
- **Style** : charte « Le Trait Oblique » v2 (`frame.md`), vraies photos du club, aucune personne.

## Video direction

- **Palette** : `canvas` #0D0D0D (fond, carte d'avis, cassure), `text` #F4F1EC (bulle de la cliente, textes), `gold` #B8A07E (filets, étoiles, un mot par réponse), `surface` #222222 (bulle de LA SALLE, saisie, bandes, mentions), `scrim` sur chaque photo. Rien d'autre.
- **Grammaire de mouvement** : tout tombe sur la grille de `tools/cues.json`. Questions sur le premier temps de chaque cadre, saisie au temps suivant, réponse ou avis au troisième temps, précision au quatrième. Courbes longues et nettes (power3 / power4.out), jamais de rebond mou. Entrées par masque, coupe oblique qui s'ouvre ou frappe d'échelle ; **jamais d'opacité ni de fondu**.
- **Fonds** : vraie photo plein cadre sous le voile `scrim`, en léger zoom avant continu (1,0 → 1,06 sur la durée du plan), coupes sèches sur les temps. Pendant une tenue, seul le fond bouge.
- **Tenues** : la fin de chaque cadre (après la réponse) est une tenue de lecture. Tenue franche sur la carte finale, immobile de 13,5 à 15,0 s.
- **En-tête** « LA SALLE · CONFLANS » y 300–352, le même dans les cadres 1 à 5 (il passe sous les bandes du volet) ; **grain** fin sur chaque fond, sous le texte.
- **Interdits** : diaporama (tout poser à t=0 puis figer) et économiseur d'écran (tout flotte sans raison) ; interface d'application, téléphone, avatar, icône de personne, logo Google ; dégradé, halo, ombre, arrondi, couleur vive ; opacité animée, fondu ; prix, date, nom d'auteur d'avis.

## Frame 1 — Horaires

- status: animated
- src: compositions/frames/01-horaires.html
- duration: 2.5s
- transition_in: cut
- scene: Façade réelle ; la cliente demande l'heure, LA SALLE frappe « 6H – 23H » puis « 7J/7 »
- voiceover: (aucune voix : musique seule, repères de tools/cues.json à 0,0 · 0,5 · 1,0 · 1,5 s)
- type: hook
- blueprint: compose
- asset_candidates: assets/img/fond-facade.jpg, assets/img/fond-enseigne.jpg
- focal: la réponse « 6H – 23H »
- roles: fond-facade = background (scrim) · fond-enseigne = background (scrim)
- poster: 2.0s

Compose : une question, une saisie, une réponse qui frappe, une précision.
Scene 1 (0.0–0.5s) : fond-facade plein cadre sous le voile, zoom avant lent qui court sur tout le cadre. La bulle de la cliente « Vous ouvrez à quelle heure ? » (bulle-cliente, une ligne, haut y 520) est **déjà en place à l'image 0** : seulement un léger tassement d'échelle 1,03 → 1 en 0,12 s.
Scene 2 (0.5–1.0s) : l'indicateur de saisie de LA SALLE s'ouvre à droite (haut y 700) ; ses 3 barres s'allument en or à 0,5 · 0,625 · 0,75 s.
Scene 3 (1.0–1.5s) : sur le temps, coupe sèche du fond vers fond-enseigne (la vraie enseigne « 7/7 6H-23H ») ; la saisie laisse sa place à la réponse qui frappe : bulle-salle « 6H – 23H » en display, le filet or se trace.
Scene 4 (1.5–2.5s) : à 1,5 s la précision « 7J/7 » (label or) glisse depuis le bas dans la bulle. Tenue de lecture jusqu'à 2,5 s ; seul le fond zoome.

## Frame 2 — Taille

- status: animated
- src: compositions/frames/02-taille.html
- duration: 2.5s
- transition_in: cut
- scene: « C'est grand ? » → « 1 200 m² » et « MUSCULATION · CARDIO » sur les tapis puis les haltères
- voiceover: (aucune voix : repères à 0,0 · 0,5 · 1,0 · 1,5 · 2,0 s du cadre, soit 2,5 → 4,5 s du film)
- type: feature_showcase
- blueprint: compose
- asset_candidates: assets/img/fond-tapis.jpg, assets/img/fond-halteres.jpg, assets/img/fond-halteres-detail.jpg
- focal: la réponse « 1 200 m² »
- roles: fond-tapis = background (scrim) · fond-halteres = background (scrim) · fond-halteres-detail = background (scrim)
- poster: 2.0s

Compose : même mécanique que le cadre 1, autre contenu.
Scene 1 (0.0–0.5s) : fond-tapis plein cadre sous le voile, zoom avant lent. Sur le temps, la bulle de la cliente « C'est grand ? » entre (monte de 40 px, échelle 0,92 → 1, sa coupe s'ouvre, 0,18 s), haut y 520.
Scene 2 (0.5–1.0s) : saisie de LA SALLE à droite (haut y 700), barres or à 0,5 · 0,625 · 0,75 s.
Scene 3 (1.0–1.5s) : coupe sèche du fond vers fond-halteres ; la réponse frappe : bulle-salle « 1 200 m² » en display (espace fine insécable entre 1 et 200), filet or tracé.
Scene 4 (1.5–2.5s) : à 1,5 s la précision « MUSCULATION · CARDIO » (label or) glisse dans la bulle ; à 2,0 s coupe sèche du fond vers fond-halteres-detail. Tenue de lecture.

## Frame 3 — Propreté

- status: animated
- src: compositions/frames/03-proprete.html
- duration: 2.5s
- transition_in: cut
- scene: « Je suis exigeante… c'est propre ? » → carte Avis Google, 5 étoiles qui s'allument, « Super salle super propre »
- voiceover: (aucune voix : repères à 0,0 · 0,5 · 1,0 → 1,5 en doubles croches · 1,5 s du cadre, soit 5,0 → 6,5 s du film)
- type: social_proof
- blueprint: compose
- asset_candidates: assets/img/fond-tapis-detail.jpg, assets/img/fond-tapis.jpg
- focal: la carte d'avis
- roles: fond-tapis-detail = background (scrim) · fond-tapis = background (scrim)
- poster: 2.1s

Compose : la question appelle un avis, pas une réponse de la salle. Le texte de l'avis est cité **mot pour mot** : « Super salle super propre » (sans point final, casse d'origine), entre guillemets français or « … ».
Scene 1 (0.0–0.5s) : fond-tapis-detail plein cadre sous le voile, zoom avant lent. La bulle de la cliente « Je suis exigeante… c'est propre ? » entre sur le temps (deux lignes, `--coupe: 74px`, haut y 520).
Scene 2 (0.5–1.0s) : saisie de LA SALLE à droite, **haut y 760** (la question fait deux lignes), barres or à 0,5 · 0,625 · 0,75 s.
Scene 3 (1.0–1.5s) : la saisie laisse sa place à la carte-avis qui frappe (haut y 760) : en haut 5 étoiles en contour et « AVIS GOOGLE » ; dessous le texte de l'avis. Les 5 étoiles s'allument en or une par une à 1,0 · 1,125 · 1,25 · 1,375 · 1,5 s (échelle 1,5 → 1).
Scene 4 (1.5–2.5s) : à 1,5 s coupe sèche du fond vers fond-tapis. Tenue de lecture de la carte jusqu'à 2,5 s.

## Frame 4 — Accueil

- status: animated
- src: compositions/frames/04-accueil.html
- duration: 2.5s
- transition_in: cut
- scene: « Et l'accueil ? » → cassure : canevas nu, saisie géante → drop : carte Avis Google « Accueil chaleureux. »
- voiceover: (aucune voix : question à 0,0 ; cassure 0,5 → 1,0 (musique coupée) ; drop à 1,0 ; soit 7,5 → 8,5 s du film)
- type: social_proof
- blueprint: compose
- asset_candidates: assets/img/fond-facade.jpg, assets/img/fond-enseigne.jpg
- focal: la carte d'avis au drop
- roles: fond-facade = background (scrim) · fond-enseigne = background (scrim)
- poster: 2.2s

Compose : le temps fort. Le texte de l'avis est cité **mot pour mot** : « Accueil chaleureux. » (avec son point), entre guillemets français or.
Scene 1 (0.0–0.5s) : fond-facade plein cadre sous le voile, zoom avant lent. La bulle de la cliente « Et l'accueil ? » entre sur le temps (haut y 520).
Scene 2 (0.5–1.0s) : **cassure**. Coupe sèche vers le canevas nu #0D0D0D (la photo et le voile disparaissent d'un coup, sans fondu) ; la bulle de la cliente reste en place. Au centre (y ≈ 860–904), la saisie géante : 3 barres obliques 120×44 px, sans bulle autour, qui s'allument en or à 0,5 · 0,625 · 0,75 s.
Scene 3 (1.0–1.5s) : **drop**. Le fond revient d'un coup sur fond-enseigne avec une frappe d'échelle (1,08 → 1,0 en 0,3 s, puis le zoom lent reprend) ; la saisie géante laisse sa place à la carte-avis qui frappe (haut y 700). Étoiles allumées une par une à 1,0 · 1,125 · 1,25 · 1,375 · 1,5 s.
Scene 4 (1.5–2.5s) : à 2,0 s coupe sèche du fond vers fond-facade. Tenue de lecture.

## Frame 5 — Invitation

- status: animated
- src: compositions/frames/05-invitation.html
- duration: 2s
- transition_in: cut
- scene: « Je peux passer voir ? » → « AVEC PLAISIR. ON VOUS ATTEND ! », puis 3 bandes obliques ferment l'écran
- voiceover: (aucune voix : repères à 0,0 · 0,5 · 1,0 · 1,25 s, volet 1,5 → 2,0 s ; soit 10,0 → 12,0 s du film)
- type: cta
- blueprint: compose
- asset_candidates: assets/img/fond-halteres.jpg
- focal: la réponse « AVEC PLAISIR. »
- roles: fond-halteres = background (scrim)
- poster: 1.4s
- handoff_out: bandes — 3 bandes surface #222222, chacune 1700 × 640 px, haut y = 0, 640, 1280 ; translation x = −300 (elles couvrent tout le cadre), extrémités coupées à 0,42 (décalage 269 px), filet or 6 px sur le bord gauche (bord d'attaque) ; échelle 1 ; opacité 1 ; vitesse nulle à 2,0 s (arrivée en power2.out depuis la droite).

Compose : la conversation se ferme, le volet ouvre la carte finale.
Scene 1 (0.0–0.5s) : fond-halteres plein cadre sous le voile, zoom avant lent. La bulle de la cliente « Je peux passer voir ? » entre sur le temps (haut y 520).
Scene 2 (0.5–1.0s) : saisie de LA SALLE à droite (haut y 700), barres or à 0,5 · 0,625 · 0,75 s.
Scene 3 (1.0–1.5s) : la réponse frappe : bulle-salle « AVEC PLAISIR. » en h1 (104 px) ; à 1,25 s la précision « ON VOUS ATTEND ! » (label or) glisse dans la bulle.
Scene 4 (1.5–2.0s) : volet. Les 3 bandes entrent par la droite et couvrent tout le cadre (départs à 1,5 · 1,5625 · 1,625 s, chacune 0,375 s, power2.out), arrivées exactement à leur position de handoff_out à 2,0 s.

## Frame 6 — Carte finale

- status: animated
- src: compositions/frames/06-carte.html
- duration: 3s
- transition_in: cut
- scene: Les bandes s'ouvrent, le monogramme s'assemble par ses 3 bandes, LA SALLE, « UNE QUESTION ? ÉCRIVEZ-NOUS. », adresse, horaires, mentions
- voiceover: (aucune voix : logo 0,0 → 0,5 ; mot-symbole 0,5 ; CTA 1,0 ; infos 1,25 ; mentions 1,5 ; accord final 2,0 ; soit 12,0 → 14,0 s du film)
- type: cta
- blueprint: logo-assemble-lockup (Adapt)
- asset_candidates: assets/img/mono.png, assets/img/word.png
- focal: le monogramme puis le CTA
- roles: mono = cutout (centré) · word = supporting
- poster: 2.5s
- handoff_in: bandes — mêmes 3 bandes qu'en fin de cadre 5 : surface #222222, 1700 × 640 px, haut y = 0, 640, 1280, translation x = −300, extrémités coupées à 0,42 (décalage 269 px), filet or 6 px sur le bord gauche, échelle 1, opacité 1, vitesse nulle à 0,0 s ; elles repartent vers la gauche.

Adapt : on garde la signature (la marque se construit à partir de ses parties puis se verrouille en carte finale) ; les parties sont les 3 bandes horizontales du monogramme, et la carte se prolonge en CTA, infos et mentions.
Scene 1 (0.0–0.5s) : les 3 bandes sortent vers la gauche (départs 0 · 0,0625 · 0,125 s, 0,35 s chacune, power2.in) et découvrent le canevas #0D0D0D. En même temps le monogramme mono.png (largeur 340 px, centré sur x 540, haut y 380) s'assemble par ses 3 tiers horizontaux : haut depuis la droite, milieu depuis la gauche, bas depuis la droite, arrivées à 0,25 · 0,375 · 0,5 s (power3.out).
Scene 2 (0.5–1.0s) : le mot-symbole word.png (largeur 460 px, centré, haut y 600) se révèle par une coupe oblique de gauche à droite (0,25 s) ; un filet or de 120 px se trace dessous, centré (y 690).
Scene 3 (1.0–1.5s) : à 1,0 s le CTA frappe, centré : « UNE QUESTION ? » (h1, text, y 750) et « ÉCRIVEZ-NOUS. » (h1, gold, y 850). À 1,25 s glissent dessous, en label text-muted : « URBAN VALLEY · CONFLANS-SAINTE-HONORINE » (y 975) et « 6H – 23H · 7J/7 » (y 1022), puis le chevron or pointé vers le bas (36 px, y 1068).
Scene 4 (1.5–3.0s) : à 1,5 s le panneau des mentions (surface opaque, x 108 → 972, y 1110 → 1237, style mention, texte centré) monte de 30 px dans son masque : « Conversation mise en scène. Extraits d'avis Google réels, cités sans modification. » Puis **tenue immobile** jusqu'à 3,0 s : rien ne bouge (c'est le dernier cadre, pas de sortie, pas de fondu au noir).
