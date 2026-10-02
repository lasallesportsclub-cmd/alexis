# Cinq propositions supplémentaires pour le portefeuille à sept lignes (2 octobre 2026)

Point de départ : Nu 20 %, Rheinmetall 15 %, Nvidia 15 %, Uber 15 %, TSMC 10 %, Adyen 12,5 %, Reddit 12,5 % (`data/portfolio.csv`). Déjà proposées et écartées ou en attente : Alnylam et Insulet (santé, écartées à la demande de l'investisseur), CATL et Sea (dossiers complets dans `research/deepdives/`). Les cinq noms ci-dessous sont nouveaux, hors santé, et viennent du classement PEG de 159 valeurs du dépôt.

Méthode : chaque candidat a été ajouté à 10 % au portefeuille retenu (les sept lignes réduites de 10 %), et le modèle `portefeuille.py` a été relancé le 02/10/2026 sur les données du 30/09/2026 (`data/variantes_8_lignes.txt`, sorties `outputs_7_lignes/variantes_8_lignes.csv`). Les chiffres récents viennent des recherches web du 02/10/2026, sourcées en fin de note. Ne constitue pas un conseil en investissement.

## Les cinq retenues

| Valeur | Place | Thème | Cours 30/09 | P/E NTM | Croiss. BPA 2027 | PEG LT | Rendement espéré (par an) | Effet sur le portefeuille (+10 %) |
|---|---|---|---|---|---|---|---|---|
| Flutter Entertainment (FLUT, NYSE ; FLTR, Londres ; PEA) | Irlande / États-Unis | Paris sportifs en ligne (FanDuel) | 74,54 $ (76,54 $ selon StockAnalysis) | 9,1 | +52,7 % | 0,45 | +31,4 % (pess. −0,7 %) | espéré +21,6 % ; P(sous l'indice) 2,3 % |
| dLocal (DLO, Nasdaq) | Uruguay | Paiements des marchands mondiaux dans les émergents | 13,76 $ | 13,7 | +26,2 % | 0,76 | +23,3 % (pess. +2,1 %) | espéré +20,7 % ; pessimiste −5,5 % (le meilleur) |
| Oracle (ORCL, NYSE) | États-Unis | Cloud et infrastructure d'IA | 137,30 $ | 14,8 | +22,8 % | 0,82 | +21,9 % (pess. −14,4 %) | espéré +20,5 % ; part IA remonte à 32 % |
| Xiaomi (1810.HK) | Chine | Smartphones, objets connectés, véhicules électriques | 25,24 HKD | 16,4 | +38,2 % | 0,91 | +21,4 % (pess. −11,7 %) | espéré +20,5 % ; bêta du portefeuille 1,55 (le plus bas) |
| Embraer (EMBJ, NYSE ; EMBR3, São Paulo) | Brésil | Aéronautique et défense | 75,32 $ | 21,8 | +29,8 % | 1,21 | +16,7 % (pess. −7,0 %) | espéré +20,0 % ; seul nouveau secteur |

Portefeuille retenu sans ajout, pour comparaison : espéré +20,4 %, tout pessimiste −6,5 %, P(sous l'indice) 5,0 %, bêta 1,64, part IA 25 %.

### 1. Flutter : le PEG le plus bas de l'univers, pour une raison

Le titre a été divisé par plus de trois en un an : FanDuel a vu son EBITDA ajusté du T2 2026 chuter de 70 % à 119 M$, les parieurs ayant gagné pendant la Coupe du monde et les finales NBA, et le chiffre d'affaires de FanDuel a reculé de 15 % (source 1). L'activité au Brésil a été suspendue et le titre a encore perdu 6,4 % le 30 septembre (source 1). FanDuel reste pourtant numéro un américain avec 39 % du marché des paris sportifs et 27 % de l'iGaming, et le consensus voit le BPA passer de 5,90 $ en 2026 à 9,01 $ en 2027, pour un objectif moyen de 134,87 $ (33 analystes) (source 1). D'où un P/E de 9 et un PEG de 0,45. Les réserves : Zacks Rank n° 5, estimations en baisse, risque réglementaire (Brésil, fiscalité des États américains, marchés de prédiction) et une volatilité de résultats liée au sport. Le rapport du 01/10 l'avait écartée pour « cours douteux » ; le cours est confirmé, c'est la chute qui est réelle. **Éligible au PEA** (société irlandaise, à vérifier auprès du courtier). À ne prendre qu'après un dossier complet.

### 2. dLocal : la meilleure ligne défensive du modèle

T2 2026 : volume de paiements 17,7 Md$ (+92 %, septième trimestre consécutif au-dessus de +50 %), revenus 399,7 M$ (+56 %), résultat net 55 M$ (+28 %), BPA dilué 0,18 $ ; guidance 2026 relevée à +60-70 % de volume et +25-30 % de marge brute (source 2). Scénario pessimiste positif (+2,1 % par an), ce qui fait d'elle la seule candidate avec Flutter à ne pas perdre d'argent dans le pire cas du modèle. Réserves : 3,9 Md$ de capitalisation, concentration sur quelques marchands (le titre a baissé le jour des résultats pour cette raison, source 2), et un troisième nom latino-américain après Nu et, si retenue, Embraer. Taille de ligne conseillée : 5 %, pas 10 %.

### 3. Oracle : le pari IA le moins cher, financé par la dette

T1 de l'exercice 2027 (publié en septembre 2026) : chiffre d'affaires 19,35 Md$ (+30 %), cloud 11,6 Md$ (+62 %), infrastructure cloud 7,4 Md$ (+121 %), BPA ajusté 1,92 $ contre 1,74 $ attendus, carnet (RPO) 664 Md$ (+209 Md$ sur un an) ; guidance de BPA annuel relevée à 8,10 $ et chiffre d'affaires supérieur à 90 Md$ (source 3). Le titre a bondi de 6,6 % à 163,10 $ après la publication, avant de revenir à 137,30 $ au 30 septembre. Le prix de cette croissance : 70 Md$ d'investissements nets sur l'exercice (90 à 95 Md$ bruts) et environ 40 Md$ à lever en dette et en actions, dont 20 Md$ d'émission d'actions au fil de l'eau (source 3). Plus de 300 Md$ du carnet dépendent d'OpenAI. Oracle ramène la part IA du portefeuille à 32 % : c'est le choix de celui qui veut plus d'IA, pas moins.

### 4. Xiaomi : la Chine par la consommation, avec le bêta le plus bas

T2 2026 : chiffre d'affaires 108,9 Md CNY, résultat net ajusté 6,2 Md CNY, marge brute 19,8 % ; 104 199 véhicules livrés (+28 %), plus de 500 000 SU7 cumulés, revenus automobiles 23,9 Md CNY (+15,9 %) ; le titre a gagné 6 % à la publication (source 4). La division automobile perd encore de l'argent et les prix de la mémoire pèsent sur les marges des smartphones. Le consensus attend un rebond du BPA de 38 % en 2027 après une année 2026 en recul ; le modèle plafonne le P/E de sortie à 25 (Chine). C'est la candidate qui abaisse le plus le bêta du portefeuille (1,55). Alternative à CATL pour l'exposition chinoise, sans la prime de 54 % de l'action H.

### 5. Embraer : un secteur absent, un carnet record

T2 2026 : chiffre d'affaires 2,2 Md$ (+23 %), EBIT ajusté 296,9 M$ (marge 13,3 %), 65 avions livrés (meilleur deuxième trimestre en seize ans), carnet record de 34,5 Md$ (+16 %, septième record consécutif), défense +38 % grâce au KC-390 ; guidance 2026 relevée : marge d'EBIT ajusté de 10 à 10,6 % (8,7 à 9,3 % auparavant), flux de trésorerie libre d'au moins 400 M$, chiffre d'affaires de 8,2 à 8,5 Md$ (source 5). PEG de 1,21, le plus élevé des cinq : on paie la visibilité du carnet. Apporte un secteur (aéronautique civile) que le portefeuille n'a pas, et une défense non européenne qui ne dépend pas des mêmes budgets que Rheinmetall. Réserves : droits de douane américains (exemptions obtenues), réal brésilien, élection du 4 octobre.

## Les écartées de ce tour et pourquoi

- **Pop Mart (9992.HK)** : PEG 0,85, mais revenus internationaux en baisse de 11,1 % au S1 2026, Labubu (« The Monsters ») en recul de 7,5 %, et le fondateur Wang Ning prévient que l'objectif de +20 % de chiffre d'affaires 2026 ne sera pas tenu (source 6). Risque de mode confirmé.
- **Duolingo (DUOL)** : scénario pessimiste doux (−4,1 %), 375 M$ de flux de trésorerie libre attendus en 2026, mais réservations ralenties à +8 % au T2 et +9 % attendus au T3 ; le titre a perdu 11 % à la publication (source 7). Croissance insuffisante pour la méthode.
- **Patria (PAX)** : P/E de 6,8, PEG 0,57, dividende trimestriel de 0,1625 $, FRE +24 % au T2 2026 et 48,9 Md$ d'actifs générant des commissions (+32 %) (source 8). Petite capitalisation et quatrième ligne latino-américaine : à garder pour une poche « rendement », pas pour celle-ci.
- **HD Hyundai Electric (267260.KS)** : couvre l'électricité des centres de données (carnet 8,49 Md$, +29,6 % ; marge opérationnelle 24,9 %) (source 9), mais PEG de 1,35 et rendement espéré de 13,7 %, le plus bas de la liste ; le modèle le classe dernier des ajouts.
- **Elite Material, Credo, Celestica** : bons chiffres mais thème IA, qui remonterait la part IA à 32 % sans l'argument du prix d'Oracle.
- **Hanwha Aerospace, Hensoldt, Leonardo** : doublons de Rheinmetall.
- **Tencent, Partners Group, Carvana, AppLovin** : rendement espéré du portefeuille en baisse après ajout (19,8 à 20,3 %) ; AppLovin cumule une action collective sur ses annonces IA et le pire cas le plus bas (+0,3 %).

## Ce que dit le modèle, en une phrase par scénario

Avec Flutter à 10 %, le portefeuille à huit lignes espère +21,6 % par an et n'a que 2,3 % de probabilité de finir sous l'indice, le meilleur résultat de tous les tests ; avec dLocal, le scénario « tout pessimiste » s'améliore à −5,5 % ; avec Oracle, le krach IA redevient le pire stress test (+13,9 %) ; avec Xiaomi, le bêta tombe à 1,55 ; avec Embraer, l'espérance recule à +20,0 % mais la dépendance aux budgets européens de défense diminue. Les cinq ensemble feraient douze lignes : au-delà de dix, la cinquième ligne supplémentaire n'améliore plus les probabilités (voir `RAPPORT.md`, §4.3).

## Sources

1. StockAnalysis, fiche et prévisions FLUT (76,54 $ au 30/09/2026, consensus 5,90 $ et 9,01 $, objectif 134,87 $) : https://stockanalysis.com/stocks/flut/ ; https://stockanalysis.com/stocks/flut/forecast/ ; Covers, 05/08/2026, FanDuel T2 : https://www.covers.com/industry/fanduel-q2-revenue-dips-behind-bettors-world-cup-nba-success-aug-5-2026 ; Investing.com, transcription T2 2026 : https://www.investing.com/news/transcripts/earnings-call-transcript-flutter-entertainment-beats-q2-2026-eps-forecast-shares-fall-93CH-4838045 ; Defense World, 30/09/2026, −6,4 % : https://www.defenseworld.net/2026/09/30/flutter-entertainment-nyseflut-stock-falls-6-4-heres-why.html ; ad-hoc-news, suspension au Brésil : https://www.ad-hoc-news.de/boerse/news/corporate-news/flutter-entertainment-stock-rises-1-53-percent-to-eur-66-25-after-brazil/70205115.
2. dLocal, 6-K T2 2026 : https://www.sec.gov/Archives/edgar/data/0001846832/000184683226000031/ex_991-dlocalxearningsxres.htm ; MarketBeat, 13/08/2026 : https://www.marketbeat.com/instant-alerts/dlocal-q2-earnings-call-highlights-2026-08-13/ ; Simply Wall St, concentration : https://simplywall.st/stocks/us/diversified-financials/nasdaq-dlo/dlocal/news/dlocal-dlo-stock-falls-as-strong-growth-meets-concentration.
3. Oracle, 8-K T1 FY2027 : https://www.sec.gov/Archives/edgar/data/0001341439/000119312526265848/orcl-ex99_1.htm ; TIKR, « Oracle stock fell 8% after a record quarter » : https://www.tikr.com/blog/oracle-stock-fell-8-after-a-record-quarter-heres-why-the-selloff-may-be-overblown ; Benzinga : https://www.benzinga.com/node/61728003.
4. Quartr, Xiaomi T2 2026 : https://quartr.com/events/xiaomi-corporation-1810-q2-2026_FGdE5TS2 ; Gasgoo, revenus automobiles : https://autonews.gasgoo.com/articles/ev/xiaomis-ev-business-generates-239-billion-yuan-in-revenue-in-q2-2026-2090683982835630080 ; Electrive, 21/08/2026 : https://www.electrive.com/2026/08/21/xiaomi-posts-further-loss-in-q2-with-its-ev-division/.
5. Leeham News, 10/08/2026, Embraer T2 : https://leehamnews.com/2026/08/10/embraer-posts-record-q2-revenue-as-deliveries-hit-16-year-high/ ; AeroCorner : https://aerocorner.com/news/embraer-q2-2026-record-revenue-profit-guidance/ ; Asian Aviation : https://asianaviation.com/posts/embraer-sets-q2-record-with-us2-2-billion-in-revenue-and-announces-new-financial-targets.
6. The Standard, 20/08/2026, Pop Mart S1 : https://www.thestandard.com.hk/finance/article/340505/Popmart-net-profit-rises-101pc-to-504-billion-yuan-in-first-half-of-2026 ; KrASIA, « Pop Mart's next act gets harder » : https://kr-asia.com/pop-marts-next-act-gets-harder-as-labubu-growth-cools ; Spielwarenmesse, baisse des revenus internationaux : https://www.spielwarenmesse.de/en/mag/toy-market-news/pop-mart-reports-first-decline-in-overseas-revenue/.
7. Duolingo, 8-K T2 2026 : https://www.sec.gov/Archives/edgar/data/0001562088/000162828026053299/q2fy26duolingo6-30x26share.htm ; Barchart : https://www.barchart.com/story/news/3672969/duolingo-reports-second-quarter-2026-results.
8. Patria, résultats du T2 2026, 31/07/2026 : https://ir.patria.com/news-releases/news-release-details/patria-reports-second-quarter-2026-earnings-results.
9. Transformer Technology, HD Hyundai Electric : https://transformer-technology.com/hd-hyundai-electric-posts-record-profit-as-ai-driven-power-demand-boosts-margins/ ; Quartr, T2 2026 : https://quartr.com/events/hd-hyundai-electric-co-ltd-267260-q2-2026_FTH0T4Rk.
10. Modèle du dépôt : `portefeuille.py`, `data/data.csv` (cours Google Finance et consensus Zacks du 30/09/2026), `data/hypotheses.csv`, `data/variantes_8_lignes.txt`, `outputs_7_lignes/variantes_8_lignes.csv` (02/10/2026).
