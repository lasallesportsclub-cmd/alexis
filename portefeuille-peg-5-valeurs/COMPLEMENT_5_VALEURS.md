# Cinq valeurs pour compléter le portefeuille (2 octobre 2026)

Point de départ : Nu Holdings 25 %, Rheinmetall 20 %, Nvidia 20 % (en place de Broadcom), Uber 20 %, TSMC 15 %. Les cinq lignes couvrent quatre courants : la fintech émergente, le réarmement européen, le calcul de l'IA (deux lignes sur la même chaîne de fabrication) et la mobilité autonome. Il manque la santé, les paiements européens, l'électrification, la publicité et les plateformes d'Asie du Sud-Est. C'est ce que les cinq compléments apportent.

Méthode : même modèle PEG que le rapport (`portefeuille.py`, données du 30/09/2026, hypothèses de `data/hypotheses.csv`), relancé le 02/10/2026 sur onze variantes à dix lignes (`data/variantes_10_lignes.txt`, sorties dans `outputs/variantes_10_lignes.csv`). Les chiffres récents viennent des recherches web du 02/10/2026, sourcés en fin de note. Ne constitue pas un conseil en investissement.

## Les cinq retenues

| Valeur | Place | Thème | Cours 30/09/2026 | P/E NTM | Croiss. BPA 2027 | PEG LT | Rendement espéré (4 ans, par an) | Zone d'achat Lynch (PEG 1) |
|---|---|---|---|---|---|---|---|---|
| Alnylam (ALNY, Nasdaq) | États-Unis | Santé, ARN interférent | 246,74 $ | 21,3 | +40,9 % | 0,97 | +22,8 % (pess. +0,7 %, central +22,5 %) | 254 $ |
| Adyen (ADYEN, Amsterdam, PEA) | Europe | Paiements | 876,60 € | 19,2 | +22,5 % | 1,01 | +19,1 % (pess. −4,0 %, central +19,0 %) | 868 € |
| CATL (300750.SZ ; H-share 3750.HK) | Chine | Batteries et stockage | 286,80 CNY | 12,1 | +38,2 % | 0,81 | +21,8 % (pess. −6,2 %, central +21,5 %) | 354 CNY |
| Reddit (RDDT, NYSE) | États-Unis | Publicité et IA applicative | 142,44 $ | 21,8 | +31,7 % | 0,99 | +22,4 % (pess. −11,7 %, central +22,1 %) | 144 $ |
| Sea (SE, NYSE) | Singapour | Plateforme Asie du Sud-Est (Shopee, Monee, Garena) | 97,36 $ | 19,4 | +43,3 % | 0,97 | +21,4 % (pess. −11,7 %, central +20,5 %) | 100 $ |

Les cinq ont un PEG long terme de 0,81 à 1,01, soit la même zone que les cinq lignes existantes (0,58 à 1,34), et cotent au niveau ou sous leur zone d'achat Lynch, sauf CATL qui est nettement en dessous (source 1).

### 1. Alnylam : la ligne santé

Deuxième de la liste d'attente du rapport (§5.6). Amvuttra a dépassé 1 Md$ de ventes trimestrielles au T2 2026 (1 012 M$ ; revenus TTR totaux 1 030 M$, +89 % sur un an), mais la guidance TTR 2026 a été abaissée de 4,4-4,7 Md$ à 4,2-4,5 Md$ le 30 juillet et le titre a perdu 28,3 % en séance (source 2). Le consensus voit encore +41 % de BPA en 2027 puis +16 % en 2028 ; l'hypothèse centrale retenue est de 22 % par an, soit l'objectif « Alnylam 2030 » (revenus +25 %, marge opérationnelle 30 %) tenu aux trois quarts. Risque : un seul produit fait 88 % des revenus. Prochain test : les résultats du T3 vers le 29 octobre, avec un seuil de 1,1 Md$ de revenus TTR fixé par le dossier (source 2 ; `research/deepdives/ALNY.md`).

### 2. Adyen : les paiements, éligible au PEA

Résultats du premier semestre 2026 (13 août) : revenu net 1,30 Md€ (+19 %, +21 % à change constant), volumes traités 803,8 Md€ (+24 %), EBITDA 642 M€ (marge 49 %, 50 % hors coûts d'acquisition). La guidance 2026 est relevée à 21-23 % de croissance à change constant (20-22 % auparavant) grâce aux rachats de Talon.One et Orb ; le titre a gagné 12 % à 1 014,80 € ce jour-là, avant de revenir à 876,60 € au 30 septembre (source 3). PEG de 1,01 pour 19 % de croissance retenue, scénario pessimiste le moins mauvais du lot (−4,0 % par an). C'est la seule ligne du complément logeable dans un PEA.

### 3. CATL : l'électrification, par les H-shares de Hong Kong

Premier semestre 2026 : chiffre d'affaires 277 Md CNY (+54,8 %), résultat net 43,3 Md CNY (+42 %), stockage d'énergie +87,5 % à 53,3 Md CNY (source 4). PEG de 0,81, le plus bas des cinq, et un P/E de 12,1 fois les douze prochains mois ; le modèle plafonne le P/E de sortie à 18 pour tenir compte des surcapacités chinoises. Le rapport la jugeait « la plus solide » des trois valeurs chinoises du classement. Pour un investisseur français, la ligne s'achète via les actions H cotées à Hong Kong (3750.HK, introduites en mai 2025) plutôt qu'à Shenzhen ; le modèle utilise le cours de Shenzhen (286,80 CNY) et le consensus en yuans. Risques : prix des cellules, gouvernance chinoise, droits de douane.

### 4. Reddit : la publicité et les données d'entraînement

T2 2026 : revenus 805 M$ (+61 %, huitième trimestre consécutif au-dessus de 60 %), résultat net 253 M$, EBITDA ajusté 343 M$ (marge 43 %), 130,3 millions d'utilisateurs quotidiens (+18 %). Guidance T3 : 860 à 870 M$ (+47 à 49 %), 4,2 % au-dessus du consensus. Le titre a pourtant baissé après la publication, de 178,60 $ à 162,71 $ en après-Bourse, puis à 142,44 $ au 30 septembre (source 5). PEG de 0,99 pour 22 % de croissance retenue. Risques inscrits dans les hypothèses : les licences de données avec Google et OpenAI expirent en 2027 ; le trafic venu de la recherche peut souffrir des réponses générées par l'IA. Préféré à AppLovin, dont le T2 a manqué le consensus (1,92 Md$ contre 1,94 attendus, titre −21 %) (source 6).

### 5. Sea : la plateforme d'Asie du Sud-Est

T2 2026 : revenus 7,8 Md$ (+48,1 %) contre 7,09 attendus, résultat net 458,1 M$, EBITDA ajusté 917,2 M$ ; Shopee 38,3 Md$ de volume (+28,4 %), Monee (crédit) +58,9 % à 1,4 Md$ de revenus avec 11,1 Md$ d'encours et 1,0 % de créances à plus de 90 jours. Le BPA ajusté (0,70 $) a manqué le consensus (0,86 $) ; la direction maintient environ 25 % de croissance du volume Shopee en 2026 (source 7). Le rapport la désignait comme remplaçante naturelle d'Uber. Pénalité : révisions négatives (Zacks n° 5), d'où une croissance retenue de 20 % contre 43 % au consensus 2027. Alternative à bêta plus bas : Xiaomi (voir ci-dessous).

## Ce que le passage à dix lignes change, selon le modèle

| Composition | P/E NTM | Croiss. 2027 | PEG LT | Part IA | Bêta | Espéré | Tout pessimiste | Double choc | Krach IA | Pire cas | P(sous l'indice) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Référence : NU 25, RHM 20, NVDA 20, UBER 20, TSM 15 | 16,0 | +42,6 % | 0,90 | 35 % | 1,55 | +20,1 % | −6,3 % | +9,9 % | +13,7 % | +1,1 % | 8,8 % |
| V1 : dix lignes à 10 % (base + ALNY, ADYEN, CATL, RDDT, SE) | 17,2 | +38,8 % | 0,92 | 20 % | 1,48 | +20,6 % | −6,6 % | +16,3 % | +16,8 % | +1,4 % | 2,0 % |
| V10 : 65/35 (NU 16, RHM 13, NVDA 13, UBER 13, TSM 10 ; 7 % chacune pour les cinq nouvelles) | 16,6 | +40,0 % | 0,90 | 23 % | 1,49 | +20,6 % | −6,3 % | +14,2 % | +16,4 % | +1,3 % | 2,2 % |
| V3 : V1 avec Xiaomi à la place de Sea | 16,9 | +38,3 % | 0,92 | 20 % | 1,39 | +20,6 % | −6,6 % | +16,1 % | +16,7 % | +1,4 % | 2,0 % |
| V4 : V1 avec Insulet à la place de Sea | 17,0 | +36,8 % | 0,92 | 20 % | 1,43 | +20,4 % | −5,6 % | +16,1 % | +16,6 % | +1,7 % | 1,9 % |
| V9 : V1 avec dLocal à la place de Sea | 16,6 | +37,1 % | 0,90 | 20 % | 1,42 | +20,8 % | −5,2 % | +16,5 % | +17,0 % | +1,7 % | 1,6 % |

Lecture. Passer de cinq à dix lignes ne coûte rien en rendement espéré (+20,6 % contre +20,1 % par an) et change trois choses : la probabilité de finir sous le Nasdaq 100 passe de 8,8 % à environ 2 % ; le « double choc » (les deux plus grosses lignes en scénario pessimiste) passe de +9,9 % à +14 à +16 % ; le « krach IA » passe de +13,7 % à +16,4 %, parce que la part IA tombe de 35 % à 20-23 %. Le pire cas (tout en pessimiste, croissance amputée de 5 points) reste positif. Les variantes se tiennent à quelques dixièmes : le choix des noms compte plus que les poids, comme dans le rapport (source 1).

**Poids proposés (V10).** Garder la hiérarchie actuelle sur 65 % du capital (Nu 16 %, Rheinmetall 13 %, Nvidia 13 %, Uber 13 %, TSMC 10 %) et mettre 7 % sur chacune des cinq nouvelles. Les dossiers des cinq nouvelles sont moins approfondis que ceux des cinq premières (seule Alnylam a un deep dive complet), ce qui justifie des lignes plus petites.

## Les écartées et pourquoi

- **Xiaomi (1810.HK)** : PEG 0,91, bêta le plus bas (variante V3 à 1,39), T2 2026 à 108,9 Md CNY de revenus et 104 199 véhicules livrés (+28 %), mais la division automobile perd encore de l'argent et une deuxième ligne chinoise porterait la Chine à 20 % du portefeuille (source 8). Première remplaçante si Sea déçoit.
- **Insulet (PODD)** : PEG 0,95, meilleur scénario pessimiste (V4 à −5,6 %), mais guidance 2026 abaissée à 20-22 % de croissance le 5 août (rétention des diabétiques de type 2, prix) et doublon santé avec Alnylam (source 9).
- **dLocal (DLO)** : les meilleurs chiffres du modèle (V9) mais 3,9 Md$ de capitalisation et une liquidité insuffisante pour une ligne de 7 à 10 %.
- **AppLovin (APP)** : PEG 0,95 mais T2 sous le consensus et titre −21 % ; Reddit a la meilleure dynamique de revenus (source 6).
- **Oracle, Celestica, Elite Material, Coherent, Credo** : rapprocheraient la part IA de 30 % alors que le but du complément est de la réduire.
- **Hanwha Aerospace, Hensoldt** : doublons de Rheinmetall sur la défense.
- **Eli Lilly, Siemens Energy** : PEG de 2,00 et 1,90, hors zone ; Siemens Energy à reprendre sous 100 € selon le rapport.
- **Flutter, Wiwynn, VTEX** : en tête du classement brut mais données jugées fragiles dans le rapport (cours douteux, consensus de deux analystes, capitalisation de 0,6 Md$).

## Agenda des cinq nouvelles

| Valeur | Prochain rendez-vous | Seuil à surveiller |
|---|---|---|
| Alnylam | T3 vers le 29/10/2026 | revenus TTR > 1,1 Md$ ; guidance 2026 tenue |
| Adyen | point d'activité T3 (novembre), résultats annuels (février 2027) | croissance à change constant dans la fourchette 21-23 % |
| CATL | T3 (fin octobre) | marge brute et prix des cellules ; décote des H-shares |
| Reddit | T3 (début novembre) | revenus ≥ 860 M$ ; renouvellement des licences de données 2027 |
| Sea | T3 (mi-novembre) | EBITDA ajusté de Shopee en route vers 1 Md$ ; créances à 90 jours ≤ 1,0 % |

## Sources

1. Modèle du dépôt : `portefeuille.py` relancé le 02/10/2026 avec `data/data.csv` (cours Google Finance du 30/09/2026, consensus Zacks du 30/09/2026 et recherches du 01/10/2026), `data/hypotheses.csv` et `data/variantes_10_lignes.txt` ; sorties `outputs/variantes_10_lignes.csv` ; rapport `RAPPORT.md` §3, §4 et §5.6.
2. Alnylam, résultats du T2 2026 (Barchart) : https://www.barchart.com/story/news/3549160/alnylam-pharmaceuticals-reports-second-quarter-2026-financial-results-and-highlights-recent-period-progress ; Pulse2, abaissement de guidance et −28,3 % : https://pulse2.com/alnylam-amvuttra-revenue-tops-1-billion-but-pent-up-demand-normalization-triggers-guidance-cut/ ; date du T3 : https://www.allinvestview.com/earnings/ALNY/.
3. Adyen, S1 2026 (13/08/2026) : https://quartr.com/events/adyen-n-v-adyen-h1-2026_3eY9CaJF ; Traders Union, +12 % à 1 014,80 € : https://tradersunion.com/news/stocks/show/2985048-adyen-strong-h1-rally/ ; Parameter.io, guidance 21-23 % : https://parameter.io/adyen-adyey-stock-soars-12-on-upward-revision-to-2026-growth-forecast/.
4. CATL, S1 2026 : Gasgoo, https://autonews.gasgoo.com/articles/market-industry/catl-h1-2026-net-profit-leaps-4198-yoy-2081569461860540416 ; Bamboo Works : https://thebambooworks.com/catl-reports-strong-growth-announces-major-buyback-for-shenzhen-stock/.
5. Reddit, T2 2026 : Webull, https://www.webull.com/news/15318181402731520 ; Shacknews : https://shacknews.com/article/150199/reddit-rddt-q2-2026-earnings-results ; Barchart : https://www.barchart.com/story/news/3580702/rddt-q2-deep-dive-monetization-growth-outpaces-user-expansion-amid-search-headwinds.
6. AppLovin, T2 2026 (8-K) : https://www.sec.gov/Archives/edgar/data/0001751008/000175100826000057/exhibit991-2q26earningspre.htm ; Game Industry Library : https://gameindustrylibrary.com/documents/applovin-q2-2026-earnings-a-rare-earnings-miss.
7. Sea, T2 2026 (11/08/2026) : présentation https://cdn.sea.com/investor/2Q2026/wFBC39MbqnfLb3MGY6LP/2026.08.11%20Sea%20Second%20Quarter%202026%20Results%20Deck.pdf ; Investing.com : https://www.investing.com/news/earnings/sea-limited-misses-eps-but-revenue-beat-pushes-shares-higher-4851179.
8. Xiaomi, T2 2026 : Quartr, https://quartr.com/events/xiaomi-corporation-1810-q2-2026_FGdE5TS2 ; Electrive, 21/08/2026 : https://www.electrive.com/2026/08/21/xiaomi-posts-further-loss-in-q2-with-its-ev-division/.
9. Insulet, T2 2026 (8-K, 05/08/2026) : https://www.sec.gov/Archives/edgar/data/0001145197/000114519726000167/podd2026-06x30ex991.htm ; Finviz : https://finviz.com/news/377724/insulet-reports-second-quarter-revenue-growth-as-full-year-us-omnipod-outlook-is-lowered.
