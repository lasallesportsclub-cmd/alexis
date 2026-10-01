#!/usr/bin/env python3
"""
Construit data/hypotheses.csv : hypothèses éditoriales (hyp.) de croissance annuelle du BPA non-GAAP de 2027 à 2031,
par scénario, plafond de P/E de sortie, paramètres des cycliques, avec une justification par ligne.
Point de départ : les hypothèses du screen du 30/09/2026 (dépôt elgateaux/bourse), reprises ou amendées (marqué « amendé »),
puis les valeurs ajoutées par la recherche du 01/10/2026.
"""
import csv
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO_HYP = os.environ.get("PEG_REPO_HYP", os.path.join(ROOT, "sources", "elgateaux-bourse", "hypotheses.csv"))
OUT = os.path.join(ROOT, "data", "hypotheses.csv")

# (g_pess, g_central, g_opt, pe_cap, justification) ; cycliques : ("cyc", m_pess, m_central, m_opt, pe_pess, pe_central, pe_opt, justif)
H = {}

# --- reprises du dépôt (30/09/2026), avec amendements signalés ---
with open(REPO_HYP, newline="", encoding="utf-8") as f:
    for h in csv.DictReader(f):
        t = h["ticker"]
        if h["cyclique"] == "1":
            H[t] = ("cyc", float(h["ratio_bpa_bear"]), float(h["ratio_bpa_base"]), float(h["ratio_bpa_bull"]),
                    float(h["pe_sortie_bear"]), float(h["pe_sortie_base"]), float(h["pe_sortie_bull"]),
                    "Repris du screen du 30/09 : " + h["justification"])
        else:
            H[t] = (float(h["g_bear"]), float(h["g_base"]), float(h["g_bull"]), float(h["pe_plafond"]),
                    "Repris du screen du 30/09 : " + h["justification"])

AMEND = {
    # amendements éditoriaux du 01/10/2026
    "NVDA": (0, 15, 25, 35, "Amendé : consensus FY28 +66 % déjà dans le BPA calendaire 2027 ; après 2027, LTG Zacks 14 % et montée des ASIC (74 % des engagements d'Anthropic en sur-mesure) : 15 % central, 0 % en digestion du capex 2028-29, 25 % si le GPU garde sa part"),
    "TSM": (6, 18, 26, 26, "Repris : LTG Zacks 27 % ramené à 18 % (cycle d'investissement N2/CoWoS, marge diluée par l'Arizona) ; plafond 26 pour le risque Taïwan"),
    "NU": (6, 22, 30, 15, "Repris : consensus 2027 +35 % ramené à 22 % (ROE 33 % sans dividende permettrait ~30 %) ; plafond 15 = banque émergente (médiane 1 an du P/E 12 mois 13,75)"),
    "UBER": (3, 20, 26, 30, "Repris : réservations +22 %, FCF 10 Md$, BPA non-GAAP guidé +28-35 % ; 20 % central ; pessimiste 3 % = robotaxis intégrés (Waymo, Tesla) contournent la plateforme"),
    "RNMBY": (5, 22, 35, 28, "Repris : objectif 2030 de 50 Md€ de CA et marge > 20 % (base = ~60 % de la trajectoire) ; carnet 80,5 Md€ ; pessimiste 5 % = paix durable et exécution ratée"),
    "LLY": (10, 20, 26, 35, "Hyp. : GLP-1 oral (orforglipron) et volumes ; consensus 2027 +28 % ; 20 % central après 2027 (concurrence Novo, baisse des prix, Medicare) ; plafond 35"),
}
for t, v in AMEND.items():
    H[t] = v

# --- valeurs ajoutées le 01/10/2026 ---
ADD = {
    # Japon (données de consensus incomplètes : exercice clos en mars 2027 seul ; à confirmer)
    "8035.T": ("cyc", 0.5, 0.8, 1.2, 16, 14, 12, "Hyp. : équipementier au sommet du cycle (prix capturé douteux, à confirmer) ; multiples de BPA 0,5/0,8/1,2 ; P/E de sortie plus élevé au creux"),
    "6146.T": ("cyc", 0.5, 0.8, 1.3, 25, 22, 18, "Hyp. : Disco, découpe/meulage pour HBM et packaging ; cyclique de qualité, multiples 0,5/0,8/1,3"),
    "6920.T": ("cyc", 0.4, 0.7, 1.2, 20, 18, 15, "Hyp. : Lasertec, inspection EUV, concurrence KLA ; multiples 0,4/0,7/1,2"),
    "7735.T": ("cyc", 0.5, 0.8, 1.2, 15, 13, 11, "Hyp. : Screen, nettoyage ; cyclique classique"),
    "6525.T": ("cyc", 0.5, 0.8, 1.2, 15, 13, 11, "Hyp. : Kokusai, dépôt pour DRAM/NAND ; cyclique mémoire"),
    "4062.T": (0, 15, 25, 30, "Hyp. : Ibiden, substrats de packaging IA ; croissance tirée par les capacités, cyclique en partie"),
    "5803.T": (0, 12, 20, 25, "Hyp. : Fujikura, fibre et connectique optique des datacenters ; consensus incomplet (un exercice), prudence"),
    "6501.T": (4, 12, 16, 30, "Hyp. : Hitachi, réseaux électriques (Hitachi Energy) et Lumada ; conglomérat, 12 % central"),
    "7011.T": (5, 15, 22, 30, "Hyp. : Mitsubishi Heavy, turbines à gaz pour datacenters et défense japonaise ; 15 % central"),
    "7013.T": (5, 15, 22, 28, "Hyp. : IHI, moteurs civils (après-vente) et défense ; 15 % central"),
    "6503.T": (3, 10, 14, 25, "Hyp. : Mitsubishi Electric, radars et missiles (défense) mais conglomérat mature"),
    "6504.T": (3, 10, 14, 25, "Hyp. : Fuji Electric, réseaux et semi-conducteurs de puissance ; mature"),
    "6861.T": (3, 9, 13, 35, "Hyp. : Keyence, automatisation ; stalwart de très grande qualité, croissance à un chiffre"),
    "6758.T": (4, 10, 14, 25, "Hyp. : Sony, jeux, musique, capteurs ; 10 % central"),
    "8136.T": (5, 15, 25, 30, "Hyp. : Sanrio, licences de personnages (Hello Kitty) ; momentum fort mais mode"),
    "6098.T": (4, 12, 16, 28, "Hyp. : Recruit (Indeed), IA et emploi ; cycle de l'emploi américain"),
    # Taïwan / Corée
    "2454.TW": (5, 20, 30, 26, "Hyp. : MediaTek, ASIC IA (TPU) et smartphones ; consensus 2027 +79 % ; après 2027, 20 % central ; plafond 26 (Taïwan) ; FY28 d'un courtier non retenu comme consensus"),
    "2317.TW": (3, 12, 18, 18, "Hyp. : Hon Hai, assemblage de racks IA ; marges d'EMS, plafond 18"),
    "2308.TW": (5, 18, 25, 30, "Hyp. : Delta Electronics, alimentation 800 V DC et refroidissement des datacenters ; 18 % central"),
    "6669.TW": (3, 15, 22, 18, "Hyp. : Wiwynn, serveurs IA pour hyperscalers ; P/E capturé incohérent (à confirmer) ; plafond 18"),
    "2382.TW": (3, 12, 18, 18, "Hyp. : Quanta, ODM de serveurs IA ; marges minces, plafond 18"),
    "000660.KS": ("cyc", 0.35, 0.65, 1.30, 14, 12, 10, "Hyp. : SK hynix, leader HBM, cyclique au sommet (P/E ~4) : mêmes règles que Micron"),
    "005930.KS": ("cyc", 0.5, 0.8, 1.30, 14, 12, 10, "Hyp. : Samsung Electronics, mémoire en rattrapage HBM4 ; cyclique, multiples 0,5/0,8/1,3"),
    # Amérique latine
    "DLO": (8, 18, 25, 25, "Hyp. : dLocal, paiements des marchands mondiaux dans les émergents ; consensus 2027 +26 % ; concurrence (Adyen, Stripe) et pression sur le take rate"),
    "GLOB": (0, 8, 12, 20, "Hyp. : Globant, services IT ; consensus +6 % ; l'IA comprime le modèle du temps facturé"),
    "VTEX": (10, 25, 35, 30, "Hyp. : VTEX, commerce composable ; petite capitalisation, croissance 2027 +33 % ; prudence 25 %"),
    "AFYA": (4, 10, 14, 20, "Hyp. : Afya, éducation médicale au Brésil ; un seul exercice de consensus"),
    "PAX": (5, 12, 16, 18, "Hyp. : Patria, gestion alternative LatAm ; 12 % central"),
    "BMA": ("cyc", 0.5, 0.8, 1.1, 8, 7, 6, "Hyp. : Banco Macro, Argentine, comptabilité d'hyperinflation : traité en cyclique (multiples 0,5/0,8/1,1)"),
    "GFNORTEO.MX": (4, 8, 11, 12, "Hyp. : Banorte, banque mexicaine mature ; 8 % central"),
    "EMBJ": (8, 18, 25, 25, "Hyp. : Embraer, carnet record (E2, défense C-390, Eve) ; consensus 2027 +30 % ; 18 % central ; chaîne d'approvisionnement = risque"),
    "CPA": (0, 8, 12, 12, "Hyp. : Copa, compagnie aérienne rentable ; cyclique économique, plafond 12"),
    "PAM": ("cyc", 0.5, 0.8, 1.2, 8, 7, 6, "Hyp. : Pampa Energía, gaz de Vaca Muerta ; cyclique énergie"),
    "VIST": ("cyc", 0.5, 0.8, 1.2, 8, 7, 6, "Hyp. : Vista Energy, pétrole de Vaca Muerta ; volumes en forte hausse mais prix du brut cyclique"),
    "PAC": (4, 10, 14, 20, "Hyp. : GAP, aéroports mexicains ; un exercice de consensus, 10 % central"),
    "ARCO": (2, 8, 12, 15, "Hyp. : Arcos Dorados, McDonald's LatAm ; consensus +5 %"),
    # États-Unis
    "DUOL": (8, 18, 28, 35, "Hyp. : Duolingo, abonnements et IA ; consensus 2027 +16 % ; 18 % central"),
    "CVNA": (8, 22, 32, 35, "Hyp. : Carvana, pénétration de l'occasion en ligne ; consensus +30 % puis +35 % ; 22 % central ; levier financier"),
}
for t, v in ADD.items():
    H.setdefault(t, v)


ADD_ASIA = {
    "3661.TW": (5, 25, 35, 26, "Hyp. : Alchip, ASIC IA sur mesure (TSMC 3/2 nm) ; consensus 2027 +73 % puis +35 % ; après 2027, 25 % central ; un client dominant ; plafond 26 (Taïwan)"),
    "3711.TW": ("cyc", 0.5, 0.8, 1.2, 15, 13, 11, "Hyp. : ASE, assemblage et test (OSAT), débordement de CoWoS ; cyclique"),
    "3017.TW": (5, 20, 30, 26, "Hyp. : AVC, refroidissement liquide des serveurs IA ; LTG 41 % ramené à 20 % (concurrence, prix) ; plafond 26"),
    "5274.TWO": (8, 25, 35, 35, "Hyp. : Aspeed, quasi-monopole des puces BMC de serveurs ; très cher (P/E > 70)"),
    "2383.TW": (5, 25, 35, 26, "Hyp. : Elite Material, stratifiés CCL très bas pertes pour 800G/1,6T ; consensus 2027 +98 % ; après, 25 % ; matériau de spécialité au cycle des serveurs ; plafond 26"),
    "3037.TW": ("cyc", 0.5, 0.8, 1.3, 15, 13, 11, "Hyp. : Unimicron, substrats ABF ; cyclique (bêta > 2)"),
    "4062.T": ("cyc", 0.5, 0.8, 1.3, 20, 18, 15, "Hyp. : Ibiden, substrats de packaging ; cyclique selon la recherche (capacités)"),
    "5803.T": ("cyc", 0.5, 0.8, 1.3, 20, 18, 15, "Hyp. : Fujikura, fibre pour datacenters ; cyclique selon la recherche"),
    "6501.T": (4, 12, 16, 30, "Hyp. : Hitachi, Hitachi Energy (réseaux) et Lumada ; LTG 20 % ramené à 12 % (conglomérat)"),
    "6861.T": (3, 9, 13, 35, "Hyp. : Keyence, LTG 9,7 % ; stalwart"),
    "8136.T": (5, 15, 25, 30, "Hyp. : Sanrio, licences de personnages ; split 5:1 en avril 2026"),
    "012450.KS": (5, 18, 25, 26, "Hyp. : Hanwha Aerospace, exportations K9/Chunmoo, moteurs ; LTG 21 % ramené à 18 % ; plafond 26 (décote coréenne, exécution)"),
    "207940.KS": (8, 15, 20, 35, "Hyp. : Samsung Biologics, CDMO ; 15 % central"),
    "267260.KS": (0, 15, 22, 22, "Hyp. : HD Hyundai Electric, transformateurs pour datacenters américains (carnet 8,5 Md$) ; cycle des prix possible après 2028 : pessimiste 0 %, plafond 22"),
    "079550.KS": (5, 18, 25, 26, "Hyp. : LIG Nex1, défense aérienne à l'export ; estimations d'un seul courtier (Mirae) : prudence"),
    "042700.KS": ("cyc", 0.5, 0.8, 1.3, 25, 20, 15, "Hyp. : Hanmi Semiconductor, TC bonders HBM ; cyclique, concurrence Hanwha Semitech"),
    "0700.HK": (5, 12, 16, 25, "Hyp. : Tencent, jeux et IA ; consensus 2027 +10 % ; 12 % central"),
    "PDD": (0, 10, 15, 15, "Hyp. : PDD, bénéfices 2026 en recul, Temu exposé aux droits de douane, gouvernance ; plafond 15"),
    "NTES": (4, 10, 14, 20, "Hyp. : NetEase, jeux ; 10 % central"),
    "1810.HK": (5, 18, 28, 25, "Hyp. : Xiaomi, VE (SU7/YU7) et écosystème ; rebond 2027 +38 % après recul 2026 ; plafond 25 (Chine)"),
    "300750.SZ": (3, 15, 22, 18, "Hyp. : CATL, batteries et stockage ; consensus 2027 +38 % ; traité non cyclique avec plafond 18 (surcapacités chinoises, prix)"),
    "9992.HK": (0, 15, 25, 25, "Hyp. : Pop Mart, propriété intellectuelle (Labubu) ; risque de mode : pessimiste 0 %"),
    "BHARTIARTL.NS": (6, 15, 20, 30, "Hyp. : Bharti Airtel, hausse de l'ARPU en Inde et Afrique ; 15 % central"),
    "POLYCAB.NS": (5, 15, 20, 30, "Hyp. : Polycab, câbles et électrification indienne ; 15 % central"),
    "TRENT.NS": (10, 22, 30, 40, "Hyp. : Trent (Zudio), mode à prix bas en Inde ; 22 % central mais P/E > 40"),
    "COFORGE.NS": (5, 18, 24, 30, "Hyp. : Coforge, services IT ; l'IA menace le modèle : pessimiste 5 %"),
    "PERSISTENT.NS": (5, 18, 24, 35, "Hyp. : Persistent Systems, ingénierie numérique ; même réserve sur l'IA"),
    "S63.SI": (5, 12, 16, 25, "Hyp. : ST Engineering, défense et aéronautique ; 12 % central"),
    "034020.KS": ("cyc", 0.5, 0.8, 1.2, 25, 20, 15, "Hyp. : Doosan Enerbility, nucléaire/SMR et turbines ; consensus 2028 en baisse : cyclique"),
    "6857.T": (3, 18, 25, 30, "Repris pour l'ADR ATEYY"),
}
for t, v in ADD_ASIA.items():
    H.setdefault(t, v)

ADD_EUROPE = {
    "ASM": (3, 15, 22, 30, "Hyp. : ASM International, dépôt ALD pour gate-all-around ; équipementier traité en croissance avec plafond 30 (comme ASML dans le screen du 30/09) ; pessimiste 3 % = creux de cycle 2028-29"),
    "BESI": (0, 20, 30, 30, "Hyp. : BESI, hybrid bonding pour HBM et packaging avancé ; consensus 2027 +48 % ; très cyclique (pessimiste 0 %)"),
    "IFX": (0, 15, 22, 25, "Hyp. : Infineon, semi-conducteurs de puissance (datacenters IA, auto) ; consensus 2027 +87 % sur base déprimée ; 15 % central ensuite ; plafond 25"),
    "VACN": (0, 14, 20, 35, "Hyp. : VAT Group, vannes à vide pour les fabs ; cyclique de qualité, P/E élevé"),
    "ENR": (8, 22, 30, 30, "Hyp. : Siemens Energy, turbines à gaz (carnet pluriannuel), réseaux (Grid Technologies) ; consensus FY27 +39 %, FY28 +30 % ; 22 % central (marges en rattrapage), plafond 30"),
    "SU": (6, 12, 15, 30, "Hyp. : Schneider Electric, électrification des datacenters ; consensus 2027 +21 % ; 12 % central (maturité)"),
    "PRY": (5, 12, 16, 25, "Hyp. : Prysmian, câbles HT et sous-marins ; carnet record ; 12 % central"),
    "LR": (4, 9, 12, 28, "Hyp. : Legrand, distribution électrique des datacenters ; stalwart"),
    "RHM": (5, 22, 35, 28, "Repris du screen du 30/09 (ligne Xetra en euros) : objectif 2030 de 50 Md€ de CA et marge > 20 % (base = ~60 % de la trajectoire) ; carnet 80,5 Md€ ; pessimiste 5 % = paix et exécution ratée"),
    "LDO": (5, 14, 18, 25, "Hyp. : Leonardo, électronique de défense et hélicoptères ; consensus 2027 +20 % ; 14 % central"),
    "HAG": (8, 22, 30, 30, "Hyp. : Hensoldt, radars et optronique ; consensus 2027 +33 % ; 22 % central"),
    "SAAB B": (8, 20, 28, 30, "Hyp. : Saab, Gripen, GlobalEye, munitions ; consensus 2027 +25 % ; 20 % central"),
    "RR.": (5, 12, 16, 28, "Hyp. : Rolls-Royce, après-vente des gros moteurs, SMR ; consensus 2027 +14 % ; 12 % central"),
    "SAF": (6, 14, 18, 28, "Hyp. : Safran, après-vente LEAP et défense ; consensus 2027 +27 % ; 14 % central"),
    "AIR": (5, 14, 18, 25, "Hyp. : Airbus, montée en cadence de l'A320neo ; 14 % central"),
    "KOG": (5, 15, 22, 28, "Hyp. : Kongsberg, missiles NSM/JSM et défense aérienne ; consensus 2027 +56 % puis repli 2028 : 15 % central"),
    "ADYEN": (8, 19, 25, 30, "Repris du screen du 30/09 (ligne Amsterdam) : objectif de CA net ~20 %/an et marge d'EBITDA > 55 % en 2028 ; base 19 % ; bear = take rate et Stripe"),
    "SPOT": (8, 20, 28, 35, "Hyp. : Spotify, hausses de prix et marge brute ; consensus 2027 +26 % ; 20 % central"),
    "FLUT": (5, 20, 30, 25, "Hyp. : Flutter, paris sportifs en ligne aux États-Unis (FanDuel) ; cours et consensus à confirmer (chute de 70 % en un an selon les données capturées) ; plafond 25"),
    "LSEG": (5, 11, 14, 28, "Hyp. : LSEG, données et indices ; 11 % central"),
    "PGHN": (5, 10, 14, 22, "Hyp. : Partners Group, marchés privés ; 10 % central"),
    "ARGX": (8, 22, 30, 35, "Hyp. : argenx, Vyvgart (indications multiples) ; consensus 2027 +27 % ; 22 % central"),
    "LONN": (6, 15, 20, 30, "Hyp. : Lonza, CDMO biologique (GLP-1, anticorps) ; consensus 2027 +19 % ; 15 % central"),
    "GALD": (8, 18, 25, 35, "Hyp. : Galderma, esthétique et Nemluvio ; consensus 2027 +37 % ; 18 % central"),
    "UCB": (5, 12, 16, 22, "Hyp. : UCB, Bimzelx ; 12 % central"),
    "RMS": (6, 11, 14, 45, "Hyp. : Hermès, rareté ; 11 % central, plafond 45 (prime de qualité historique)"),
    "RACE": (5, 10, 13, 45, "Hyp. : Ferrari, 10 % central, plafond 45"),
    "BC": (6, 12, 15, 35, "Hyp. : Brunello Cucinelli, 12 % central"),
    "ALC": (4, 10, 13, 25, "Hyp. : Alcon, ophtalmologie ; 10 % central"),
    "SRT3": (6, 16, 22, 35, "Hyp. : Sartorius, consommables bioprocess ; reprise après 2023-24 ; 16 % central"),
}
for t, v in ADD_EUROPE.items():
    H.setdefault(t, v)

ADD_US = {
    "VRT": (4, 18, 25, 35, "Repris du screen du 30/09 : énergie et refroidissement liquide des datacenters ; consensus 2027 +36 %"),
    "GEV": (5, 18, 25, 35, "Hyp. : GE Vernova, turbines à gaz (carnet 176 Md$) et réseaux ; consensus 2027 +51 % puis +37 % ; 18 % central ; BPA GAAP"),
    "CLS": (0, 18, 28, 25, "Hyp. : Celestica, serveurs et commutateurs pour hyperscalers ; consensus 2027 +33 % ; marges d'EMS, concentration clients ; pessimiste 0 %"),
    "HIMS": (0, 25, 40, 35, "Hyp. : Hims & Hers, GLP-1 composés et télésanté ; pertes 2026, risque réglementaire (FDA) ; spéculatif"),
    "NTRA": (10, 30, 40, 40, "Hyp. : Natera, tests génétiques ; bénéfices à partir de 2028 seulement"),
    "PODD": (8, 18, 24, 35, "Hyp. : Insulet, pompes à insuline Omnipod ; consensus 2027 +24 %"),
    "TMDX": (10, 30, 40, 35, "Hyp. : TransMedics, perfusion d'organes ; consensus 2027 +62 % ; Zacks Rank 5 (révisions à la baisse)"),
    "ISRG": (6, 12, 15, 40, "Hyp. : Intuitive Surgical, robots chirurgicaux ; 12 % central, prime de qualité"),
    "RKLB": (10, 40, 60, 60, "Hyp. : Rocket Lab, lanceurs et satellites ; bénéfices à partir de 2028 ; récit"),
    "AXON": (8, 20, 28, 45, "Hyp. : Axon, tasers, caméras, logiciel et drones ; consensus 2027 +39 % ; cher"),
    "SHOP": (8, 22, 30, 45, "Hyp. : Shopify, commerce et agents IA ; consensus 2027 +30 % ; P/E GAAP élevé"),
    "DASH": (10, 28, 38, 45, "Hyp. : DoorDash, livraison locale ; consensus 2027 +73 % (base GAAP) puis +59 %"),
    "COIN": (0, 15, 30, 30, "Hyp. : Coinbase, crypto ; pertes 2026, cyclique des actifs numériques"),
    "IBKR": (5, 12, 18, 30, "Hyp. : Interactive Brokers, courtage mondial ; 12 % central ; sensible aux taux"),
    "CIEN": (0, 20, 30, 30, "Hyp. : Ciena, optique longue distance et datacenters ; consensus FY27 +78 % ; cyclique télécoms"),
    "ETN": (5, 12, 15, 30, "Hyp. : Eaton, électrification ; 12 % central"),
    "NOW": (8, 18, 22, 40, "Hyp. : ServiceNow, agents IA d'entreprise ; consensus 2027 +22 % ; risque de désintermédiation du logiciel par l'IA"),
    "CRWD": (8, 22, 30, 60, "Hyp. : CrowdStrike, cybersécurité ; P/E > 100 ; Zacks Rank 4"),
    "NET": (10, 28, 38, 80, "Hyp. : Cloudflare, edge et IA ; P/E > 200"),
    "DDOG": (8, 20, 26, 60, "Hyp. : Datadog, observabilité ; P/E ~90"),
    "VRTX": (4, 10, 13, 30, "Hyp. : Vertex, mucoviscidose et douleur ; 10 % central"),
    "ALNY": (10, 25, 35, 35, "Hyp. : Alnylam, ARNi (Amvuttra) ; consensus 2027 +41 % ; 25 % central"),
    "TTWO": (5, 20, 30, 35, "Hyp. : Take-Two, cycle GTA VI (FY27 +90 %) ; après le pic, 20 % central"),
    "ABNB": (5, 12, 16, 30, "Hyp. : Airbnb, voyages ; 12 % central"),
    "NBIS": (10, 40, 60, 60, "Hyp. : Nebius, néocloud IA ; pertes jusqu'en 2027 ; récit"),
    "CRWV": (10, 40, 60, 40, "Hyp. : CoreWeave, néocloud IA ; pertes, dette ; récit"),
}
for t, v in ADD_US.items():
    H.setdefault(t, v)

# Deep dives du 01/10/2026 (research/deepdives/*.md) : hypothèses révisées après lecture des dossiers.
# Elles remplacent les hypothèses précédentes pour les lignes du portefeuille et les candidates à la cinquième ligne.
DEEPDIVE = {
    "NU": (8, 20, 28, 15, "Hyp. (deep dive 01/10) : consensus 2027 +31 %, 2028 +27 % ; LTG 22-40 % selon les sources ; 20 % central = Mexique rentable, rachats compensant les RSU ; pess. 8 % = cycle de crédit brésilien, CSLL à 20 % en 2028 ; plafond 15 = banque émergente (18,98 $ au plus haut valait 22x 2026)"),
    "RHM": (8, 20, 30, 22, "Hyp. (deep dive 01/10) : pente du consensus 2026-2029 de 38 %/an, prise à moitié (carnet potentiel 100-120 Md€, marge 19 % visée, cash-flow négatif au S1) ; pess. 8 % = paix en Ukraine et retards Skyranger/Boxer ; opt. 30 % = objectif 2030 (50 Md€, marge > 20 %) ; plafond 22 = pas de re-notation (57x était une bulle)"),
    "TSM": (6, 17, 24, 24, "Hyp. (deep dive 01/10) : cible maison de ~25 %/an de CA 2024-2029 et LTG Zacks 33 %, ramenées à 17 % (dilution de marge 2 nm 3-4 pts et usines étrangères, digestion du capex IA après 2027) ; pess. 6 % = plafonnement du capex hyperscaler ; plafond 24 = risque Taïwan et cyclicité"),
    "UBER": (5, 16, 24, 22, "Hyp. (deep dive 01/10) : réservations « mid-to-high teens », levier opérationnel et rachats ; 16 % central ; pess. 5 % = Waymo/Tesla captent les centres-villes et Delivery Hero (14,8 Md$, dette) absorbe le FCF ; plafond 22 = marché mature, désintermédiation non résolue"),
    "AVGO": (8, 20, 30, 24, "Hyp. (deep dive 01/10) : guidance IA 115 Md$ (FY27) puis 230 Md$ (FY28), BPA FY28 > 30 $ visé ; 20 % central après la marche 2027 (capex hyperscaler, logiciel +15 % d'ARR) ; pess. 8 % = digestion du capex, perte d'un client XPU, marge brute vers 73 % ; plafond 24 = fabless concentré sur six clients"),
    "LLY": (6, 13, 20, 24, "Hyp. (deep dive 01/10) : consensus 2028 +10,5 % seulement (prix réalisés −13 %, Novo à 65 % des nouvelles prescriptions, Foundayo lent) ; 13 % central = marché GLP-1 à 114 Md$ en 2030 (Goldman) et part stable ; plafond 24"),
    "ENR": (4, 14, 22, 20, "Hyp. (deep dive 01/10) : consensus FY27 +23 %, FY28 +26 %, mais pic de cycle possible (Barclays : part de marché 42 % vs 27 % historique, BFR qui se retourne en 2028) ; 14 % central = objectif FY28 de marge 14-16 % ; plafond 20 = équipementier cyclique à bêta 1,84"),
    "ALNY": (10, 22, 32, 25, "Hyp. (deep dive 01/10) : consensus 2027 +41 %, 2028 +16 % après l'abaissement de guidance de juillet ; 22 % central = trajectoire « Alnylam 2030 » (revenus +25 %/an, marge 30 %) tenue aux trois quarts ; pess. 10 % = plafonnement d'Amvuttra, Attruby, génériques du tafamidis en 2031 ; plafond 25 = spécialité pharma à un produit (88 % des revenus)"),
    "3661.TW": (5, 20, 35, 18, "Hyp. (deep dive 01/10) : médiane FactSet (18 analystes) : BPA +102 % en 2026, +33,5 % en 2027, +39,8 % en 2028 ; 20 % central = N2 livré fin 2027, second hyperscaler lent ; pess. 5 % = Trainium 4 perdu ou internalisé (AWS = 60 % du CA en 2024) ; plafond 18 = sous-traitant à un client, bêta 1,72, Taïwan"),
}
for t, v in DEEPDIVE.items():
    H[t] = v

# valeurs de l'univers sans hypothèse explicite : lecture de data.csv pour les lister
data = list(csv.DictReader(open(os.path.join(ROOT, "data", "data.csv"), encoding="utf-8")))
missing = [r["ticker"] for r in data if r["ticker"] not in H]
if missing:
    print("SANS HYPOTHÈSE :", missing)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ticker", "g_pess", "g_central", "g_opt", "pe_cap", "cyc_mult_pess", "cyc_mult_central", "cyc_mult_opt",
                "cyc_pe_pess", "cyc_pe_central", "cyc_pe_opt", "justification"])
    for r in data:
        t = r["ticker"]
        v = H.get(t)
        if v is None:
            continue
        if v[0] == "cyc":
            w.writerow([t, "", "", "", "", v[1], v[2], v[3], v[4], v[5], v[6], v[7]])
        else:
            w.writerow([t, v[0], v[1], v[2], v[3], "", "", "", "", "", "", v[4]])
print("hypothèses écrites pour", len([r for r in data if r["ticker"] in H]), "valeurs")
