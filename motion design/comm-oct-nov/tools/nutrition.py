"""Visuels de la rubrique « Rayon nutrition » de LA SALLE, novembre 2026 à janvier 2027.

Même mise en page que tools/visuels.py (charte LA SALLE : noir, blanc, gris, trait penché du monogramme) : aucune image,
aucune personne, aucun logo de marque redessiné ; les noms des marques sont composés en texte.
Les textes sont ceux de « Comm LA SALLE et LE CUBE/Rayon nutrition/Rubrique_novembre-janvier.md ».
Allégations : uniquement celles du registre de l'Union européenne (règlement 432/2012), citées mot pour mot.

Usage : python3 tools/nutrition.py [préfixe…]   (par ex. NUT_P3 pour ne refaire que le post sur la créatine)
"""
import os
import sys
import tempfile

import visuels as V
from visuels import P, S, carrousel

V.SORTIE = os.path.normpath(os.path.join(V.MOTION, "..", "Comm LA SALLE et LE CUBE", "Rayon nutrition", "visuels"))
_esc = V.esc
V.esc = lambda t: _esc(t).replace("®", '<sup style="font-size:.42em;vertical-align:.95em">®</sup>')  # ® en exposant, pas en capitale
LS = "LA SALLE"
FIN = [("titre", "Une question\nsur un produit ?", {"taille": 130}), ("oblique",),
       ("texte", "Demandez à l'accueil, de 6h à 23h, 7 jours sur 7.")]

VISUELS = []

# ───────── Posts : un jeudi sur deux ─────────
VISUELS += carrousel("NUT_P1_rayon", LS, [
    [("kicker", "À l'accueil de LA SALLE"), ("titre", "Le rayon\nnutrition", {"taille": 200}), ("oblique",),
     ("texte", "Des marques choisies une par une.")],
    [("kicker", "Notre choix"), ("titre", "Pourquoi\nces marques ?", {"taille": 130}),
     ("texte", "Nous les avons choisies pour leur réputation. Nutrimuscle et Nutripure, en particulier, pour la traçabilité de leurs produits.")],
    [("num", "01"), ("titre", "Nutrimuscle", {"taille": 130}),
     ("texte", "Protéine Native Whey Protimuscle, créatine Creapure®, collagène Peptan® et Naticol®, citrate de magnésium.")],
    [("num", "02"), ("titre", "Nutripure", {"taille": 130}), ("texte", "Muscle Protein, créatine et shaker.")],
    [("num", "03"), ("titre", "Xtend", {"taille": 130}), ("texte", "Les BCAA Xtend, en poudre, à diluer dans l'eau.")],
    [("num", "04"), ("titre", "SFD Nutrition\n& All Nutrition", {"taille": 120}),
     ("texte", "Créatine et collagène SFD Nutrition. Vitamines D3 et K2, électrolytes All Nutrition.")],
    [("num", "05"), ("titre", "Ahead\net les en-cas", {"taille": 120}),
     ("texte", "La pâte à tartiner Ahead, des barres, des cookies et des boissons.")],
    FIN,
])

VISUELS += carrousel("NUT_P2_proteines", LS, [
    [("kicker", "Le rayon nutrition"), ("titre", "Les protéines,\nà quoi\nservent-elles ?", {"taille": 140}), ("oblique",)],
    [("kicker", "Ce que dit la réglementation"), ("titre", "Deux phrases\nautorisées", {"taille": 120}),
     ("texte", "« Les protéines contribuent à augmenter la masse musculaire. »\n« Les protéines contribuent au maintien de la masse musculaire. »"),
     ("texte", "Règlement européen 432/2012.", {"taille": 30})],
    [("kicker", "D'abord"), ("titre", "Votre\nassiette", {"taille": 150}),
     ("texte", "Viande, poisson, œufs, laitages, légumineuses : votre alimentation apporte déjà des protéines. La poudre est un complément pratique, pas une obligation.")],
    [("kicker", "À l'accueil"), ("titre", "Deux\nprotéines", {"taille": 150}),
     ("texte", "Native Whey Protimuscle, de Nutrimuscle.\nMuscle Protein, de Nutripure.")],
    FIN,
])

VISUELS += carrousel("NUT_P3_creatine", LS, [
    [("kicker", "Le rayon nutrition"), ("titre", "Créatine :\nce qu'on a\nle droit\nde dire", {"taille": 140}), ("oblique",)],
    [("kicker", "Ce que dit la réglementation"), ("titre", "Une seule\nphrase\nautorisée", {"taille": 120}),
     ("texte", "« La créatine augmente les performances physiques lors d'exercices brefs, de haute intensité et répétés. »"),
     ("texte", "L'effet bénéfique est obtenu par la consommation journalière de 3 g de créatine. Règlement européen 432/2012.", {"taille": 30})],
    [("kicker", "Avant d'en prendre"), ("titre", "Lisez\nl'étiquette", {"taille": 150}),
     ("texte", "Dose journalière, précautions d'emploi, personnes à qui le produit est déconseillé : tout est écrit sur le pot. En cas de doute, demandez l'avis d'un professionnel de santé.")],
    [("kicker", "À l'accueil"), ("titre", "Trois\ncréatines", {"taille": 150}),
     ("texte", "Créatine Creapure®, de Nutrimuscle.\nCréatine, de Nutripure.\nCréatine, de SFD Nutrition.")],
    FIN,
])

VISUELS += carrousel("NUT_P4_cadeaux", LS, [
    [("kicker", "Noël"), ("titre", "Un cadeau\npour un\nsportif ?", {"taille": 160}), ("oblique",),
     ("texte", "Trois idées au rayon de l'accueil.")],
    [("num", "01"), ("titre", "Le shaker", {"taille": 130}), ("texte", "Le shaker Nutripure, pour emporter sa boisson à la salle.")],
    [("num", "02"), ("titre", "La pâte\nà tartiner", {"taille": 130}), ("texte", "La pâte à tartiner Ahead, pour les gourmands.")],
    [("num", "03"), ("titre", "Une protéine", {"taille": 130}),
     ("texte", "Native Whey Protimuscle de Nutrimuscle, ou Muscle Protein de Nutripure.")],
    FIN,
])

VISUELS += carrousel("NUT_P5_collagene", LS, [
    [("kicker", "Le rayon nutrition"), ("titre", "Collagène :\npourquoi\nnous ne vous\npromettons rien", {"taille": 120}), ("oblique",)],
    [("kicker", "La réglementation"), ("titre", "Aucune\nallégation\nautorisée", {"taille": 130}),
     ("texte", "En Europe, aucune allégation de santé n'est autorisée pour le collagène. Nous vous présentons donc nos produits, sans promesse.")],
    [("kicker", "À l'accueil"), ("titre", "Nos\ncollagènes", {"taille": 150}),
     ("texte", "Collagène Peptan® et collagène marin Naticol®, de Nutrimuscle.\nSuper Collagen Mix, de Nutrimuscle.\nCollagen, de SFD Nutrition.")],
    FIN,
])

VISUELS += carrousel("NUT_P6_vitamines", LS, [
    [("kicker", "Le rayon nutrition"), ("titre", "Vitamines\net minéraux", {"taille": 160}), ("oblique",),
     ("texte", "Ce que dit la réglementation, mot pour mot.")],
    [("kicker", "All Nutrition"), ("titre", "Vitamines\nD3 et K2", {"taille": 140}),
     ("texte", "« La vitamine D contribue au maintien d'une fonction musculaire normale. »\n« La vitamine K contribue au maintien d'une ossature normale. »")],
    [("kicker", "Nutrimuscle"), ("titre", "Citrate de\nmagnésium", {"taille": 140}),
     ("texte", "« Le magnésium contribue à réduire la fatigue. »\n« Le magnésium contribue à une fonction musculaire normale. »")],
    FIN,
])

# ───────── Stories : « Le produit de la semaine », chaque mardi ─────────
PRODUITS = [  # (semaine, nom à l'écran, marque, description)
    ("S45", "Native Whey\nProtimuscle", "Nutrimuscle", "Protéine en poudre"),
    ("S46", "Muscle\nProtein", "Nutripure", "Protéine en poudre"),
    ("S47", "BCAA", "Xtend", "En poudre, à diluer dans l'eau"),
    ("S48", "Créatine\nCreapure®", "Nutrimuscle", "En poudre"),
    ("S49", "Créatine", "Nutripure", "En poudre"),
    ("S50", "Collagen", "SFD Nutrition", "En poudre, plusieurs parfums"),
    ("S51", "Pâte\nà tartiner", "Ahead", "Idée cadeau pour les gourmands"),
    ("S52", "Le shaker", "Nutripure", "Idée cadeau"),
    ("S53", "Vitamines\nD3 et K2", "All Nutrition", "Compléments alimentaires"),
    ("S01", "Citrate de\nmagnésium", "Nutrimuscle", "En gélules ou en poudre"),
    ("S02", "Créatine", "SFD Nutrition", "En poudre"),
    ("S03", "Collagène\nmarin Naticol®", "Nutrimuscle", "En poudre"),
    ("S04", "Électrolytes", "All Nutrition", "En poudre, à diluer dans l'eau"),
]
VISUELS += [S(f"NUT_{sem}_story", LS, [("kicker", "Le produit de la semaine"), ("titre", nom, {"taille": 150}), ("oblique",),
                                         ("texte", f"{marque} · {desc}\nDisponible à l'accueil.", {"taille": 44}), ("zone", 300)])
            for sem, nom, marque, desc in PRODUITS]


def main():
    filtre = sys.argv[1:]
    os.makedirs(V.SORTIE, exist_ok=True)
    noms = [v["nom"] for v in VISUELS]
    assert len(noms) == len(set(noms)), "nom de visuel en double"
    with tempfile.TemporaryDirectory() as tmp:
        for v in VISUELS:
            if not filtre or any(v["nom"].startswith(f) for f in filtre):
                print(os.path.basename(V.capturer(v, tmp)))


if __name__ == "__main__":
    main()
