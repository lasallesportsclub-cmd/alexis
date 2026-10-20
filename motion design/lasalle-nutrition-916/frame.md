# Stories « Nutrimuscle et Nutripure, disponibles à l'accueil » : direction artistique

Chaque story suit la direction artistique de sa marque, pas la charte « Le Trait Oblique » de LA SALLE. Le club signe en bas : logo négatif sur bande bleu marine, vouvoiement, « à l'accueil de LA SALLE ».

## Sources de la direction artistique (relevé du 20/10/2026)

Les sites nutripure.fr et nutrimuscle.com ainsi qu'Instagram ne sont pas accessibles depuis la session cloud : le proxy refuse la connexion. Le relevé s'appuie donc sur les supports officiels des marques :

- **Nutripure :**
  - le visuel partenaire « Salle présentation.png » (Drive, dossier partenaire Nutripure) ;
  - le code des e-mails pros Nutripure du 19/10/2026 : couleurs, polices, boutons.
- **Nutrimuscle :**
  - le code des e-mails Nutrimuscle Pro du 19/10/2026 ;
  - la photo du rayon de l'accueil, où l'on voit les pots blancs avec le carré « Nm » et le bandeau bleu clair ;
  - une recherche web : le logo carré inspiré du tableau périodique, la gamme bien-être renommée Nutrielement.

| | Nutrimuscle | Nutripure |
|---|---|---|
| Fond | #F7F5F3 (blanc chaud) | #FBF8F8 (blanc chaud) |
| Couleur forte | bleu marine #00253A, texte blanc | bleu ciel #77D2F5 / #80D1F5, texte #111 |
| Accent | bleu #0093E5 (liens, numéros) | bleu pâle #E8F5FC |
| Texte | #000 / marine | #111, #142323, gris #667085 |
| Typo | Helvetica / Arial, droite, sobre → **Inter droit 700–800** | Inter (e-mails) ; titres en **capitales grasses italiques** (visuel partenaire) → **Inter 900 italique** |
| Formes | blocs pleins, filets fins, rayon 5–6 px | pastille arrondie (bouton « Disponible dans votre salle »), rayon 5 px sur les boutons |
| Images | pots blancs, logo « Nm » carré, bandeau bleu clair par produit | sachets kraft, cuisine bois, scènes de vie lumineuses |
| Ton | factuel, ingrédients marqués (Creapure®, Peptan®, Naticol®), « Sportivement » | direct et positif : « À chaque objectif sa protéine ! » |

Inter vient de @fontsource/inter 5.3.0 (licence OFL), embarqué en local dans `assets/fonts`. Helvetica n'est pas libre : Inter la remplace pour Nutrimuscle.

## Les 4 stories (1080×1920, 5 s chacune)

1. **Les deux marques.**
   - Photo réelle du rayon de l'accueil.
   - Pastille bleu ciel « DISPONIBLES À L'ACCUEIL ».
   - « NUTRIMUSCLE » en marine droit et « & NUTRIPURE » en noir italique.
   - Une phrase sur les catégories de produits, puis la bande LA SALLE.
2. **Nutrimuscle.**
   - Bloc marine avec le titre.
   - Gros plan des pots Native Whey Protimuscle.
   - Fiche de 5 références numérotées en bleu, séparées par des filets.
   - Bouton marine « DISPONIBLE À L'ACCUEIL DE LA SALLE ».
3. **Nutripure.**
   - Titre en capitales grasses italiques.
   - Visuel partenaire officiel en carte, sans sa pastille du bas.
   - Ligne produits, puis pastille bleu ciel « Disponible / à l'accueil de LA SALLE », reprise du visuel partenaire.
4. **Une question ?**
   - « UNE QUESTION SUR UN PRODUIT ? ».
   - Une carte par marque, dans sa couleur.
   - **Zone vide de y 1230 à 1580 pour un sticker Question**, puis la bande LA SALLE.

## Règles

- Aucun prix, aucune promotion : la remise Nutripure est réservée aux revendeurs.
- Aucune allégation de santé ou de performance (règlement UE 432/2012) : on nomme les produits, on ne promet rien.
- Aucun logo de marque redessiné : les noms sont composés en Inter. Les vrais logos n'apparaissent que sur les produits photographiés et sur le visuel partenaire.
- Le logo LA SALLE est toujours en version négative, sur fond sombre. C'est le logo provisoire, en attente de `mono.png` et `word.png`.
- Le vouvoiement est obligatoire. Le lexique interdit du BRIEF Premium s'applique, et `tools/livrer.py` le vérifie.
- Haut des stories (y < 250) : zone de l'interface Instagram, décor seulement. Bas (y > 1760) : champ de réponse, rien d'important.
