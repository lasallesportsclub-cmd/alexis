# Oracle (NYSE : ORCL) — Deep dive sur la dette, 2 octobre 2026

**Cours de référence** : 137,30 $ (clôture du 30/09/2026, Google Finance via `portefeuille-peg-5-valeurs/data/data.csv`). Exercice fiscal clos le 31 mai : l'exercice qui s'achève le 31 mai 2027 est fy2027. Horizon d'analyse : octobre 2030. Devise : dollar américain.

**Définitions.** RPO (remaining performance obligations) : carnet de commandes contractuel non encore facturé. OCI : Oracle Cloud Infrastructure, la division de location de capacité de calcul. Capex : investissements en immobilisations (centres de données, serveurs). FCF (free cash flow) : flux de trésorerie opérationnel moins capex. ATM (at-the-market) : programme de vente d'actions nouvelles au fil de l'eau sur le marché. Levier : dette rapportée à l'EBITDA (résultat avant intérêts, impôts et amortissements). CDS : contrat d'assurance contre le défaut d'un emprunteur ; son prix en points de base mesure le risque perçu. BBB- et Baa3 sont les dernières notes de la catégorie « investissement » ; en dessous, c'est le « haut rendement » (junk).

**Pourquoi la dette est la question.** Oracle finance pour OpenAI et quelques autres clients la plus grande construction de centres de données de son histoire, avec un flux de trésorerie libre négatif de 23,7 Md$ sur l'exercice 2026 et encore −5,4 Md$ au premier trimestre 2027, en empruntant, en vendant des actions et en signant des baux qui n'apparaissent pas encore au bilan. Le marché actions paie 17 fois le bénéfice 2027 ; le marché obligataire, lui, exige 6,3 % à 7,6 % de rendement et S&P a placé le groupe à un cran de la catégorie spéculative. Ce dossier chiffre ce décalage.

## 1. Le métier en une page

Exercice 2026 (clos le 31/05/2026, publié le 10/06/2026) : chiffre d'affaires 67,4 Md$ (+17 %), dont cloud 34,0 Md$ (+39 %), licences et support logiciels 24,5 Md$ (−1 %), services 5,7 Md$, matériel 3,1 Md$ ; résultat net GAAP 17,0 Md$ (+36 %), non-GAAP 22,2 Md$ (+29 %) ; flux de trésorerie opérationnel record de 32,0 Md$ (+54 %) (source 1).

Premier trimestre 2027 (clos le 31/08/2026, publié le 10/09/2026) : chiffre d'affaires 19,35 Md$ (+30 %), cloud 11,6 Md$ (+62 %), infrastructure cloud 7,4 Md$ (+121 %), applications cloud 4,2 Md$ (+10 %) ; BPA non-GAAP 1,92 $ contre 1,74 $ attendus ; RPO 664 Md$ (+209 Md$ sur un an) ; guidance annuelle relevée à plus de 90 Md$ de chiffre d'affaires et 8,10 $ de BPA non-GAAP (source 2). Le directeur général Clay Magouyrk a précisé que l'essentiel de la hausse du RPO du trimestre venait de contrats où les clients prépaient les GPU ou les fournissaient eux-mêmes, « sans impact supplémentaire sur les plans de levée de capitaux » (source 2).

Le moteur est un seul produit, la location de capacité de calcul pour l'IA, vendue à une poignée de clients nommés par Larry Ellison : OpenAI, xAI, Meta, Nvidia, AMD, TikTok (source 3). Plus de 50 % du RPO vient d'OpenAI selon Bank of America ; environ la moitié des 638 Md$ de RPO de fin d'exercice 2026 selon S&P (sources 2, 4).

## 2. L'encours : ce qu'Oracle doit aujourd'hui

| Poste | 31/05/2025 | 31/05/2026 | 31/08/2026 | Source |
|---|---|---|---|---|
| Emprunts obligataires et autres (valeur comptable) | n.d. | 130,1 Md$ (128,1 Md$ selon le 10-Q) | 125,0 Md$ | 10-K fy2026, 10-Q T1 fy2027 (5, 6) |
| Dette totale au bilan (y compris baux) | n.d. | 129,5 Md$ (hors baux, presse) | 155,9 Md$ (StockAnalysis) | 7 |
| Passifs de baux opérationnels, part non courante | n.d. | n.d. | 30,6 Md$ | 10-Q (6) |
| Trésorerie et équivalents | n.d. | 31,3 Md$ | 36,4 Md$ (+0,7 Md$ de titres) | 1, 6 |
| Dette nette hors baux (calcul de l'auteur) | – | environ 98 Md$ | environ 88 Md$ | – |
| Dette nette avec baux au bilan (calcul) | – | – | environ 122 Md$ | – |
| Levier dette/EBITDA | 3,6x (S&P, mai 2025 ajusté) ; « plus de 4x » ajusté | 4,3x (dette 129,5 Md$ sur EBITDA publié) | n.d. | 4, 8 |

La baisse de 128,1 à 125,0 Md$ entre mai et août 2026 n'est pas un désendettement : elle vient d'un remboursement net financé par 19,9 Md$ d'actions nouvelles (section 3). Rapportée au chiffre d'affaires, la dette obligataire représente 1,9 année de ventes de l'exercice 2026 (calcul de l'auteur).

## 3. Ce qui a été levé en douze mois

| Date | Opération | Montant | Conditions | Source |
|---|---|---|---|---|
| Septembre 2025 | Obligations | 18 Md$ | n.d. | 9 |
| Exercice 2026 (total) | Dette nouvelle et actions | 43 Md$ de dette, 5 Md$ d'actions | – | 10 |
| 1er février 2026 | Plan de financement 2026 | 45 à 50 Md$ annoncés | moitié dette, moitié fonds propres ; « une seule émission obligataire en 2026 » | 11 |
| 4 février 2026 | Obligations seniors, huit tranches | 25 Md$ | 4,55 % (2029) à 6,85 % (2066) ; coupon moyen pondéré 5,8 % (calcul) ; notées Baa2 (négatif) / BBB (négatif) / BBB (stable) | 12 |
| 5 février 2026 | Actions de préférence convertibles obligatoires série D (ORCL.PRD) | 5,0 Md$ nets | dividende 6,50 %, prime de conversion 25 % | 13 |
| Juin à août 2026 (T1 fy2027) | Programme ATM | 19,9 Md$ nets | 141 millions d'actions, soit 4,9 % du capital de fin mai (calcul) ; programme de 20 Md$ entièrement utilisé | 6, 14 |
| Exercice 2027 (plan) | Dette et actions | « environ 40 Md$ », dont les 20 Md$ d'ATM déjà réalisés | pas d'obligations supplémentaires en année civile 2026 | 2 |
| 2026 (hors bilan) | Campus de Saline Township (Michigan), loué par Oracle | 16 Md$ (Related Digital et Blackstone), dont 14 Md$ d'obligations placées par Bank of America, 10 Md$ repris par Pimco | coupon 7,5 %, échéance 2045 ; Blue Owl s'était retiré en décembre 2025 | 15 |

Le nombre d'actions est passé de 2 807 millions au 31 mai 2025 à 2 880 millions au 31 mai 2026, puis à environ 3 021 millions après l'ATM (calcul de l'auteur à partir des 141 millions émises ; le 10-Q donnera le chiffre exact) (sources 6, 14). Capitalisation à 137,30 $ : environ 415 Md$.

## 4. Échéancier et coût

Remboursements de principal au 31 mai 2026 : 7,21 Md$ sur l'exercice 2027, 10,15 Md$ sur 2028, 5,50 Md$ sur 2029 ; les tranches 2030 et au-delà ne sont pas lisibles dans l'extrait consulté du 10-K (source 5). Soit 22,9 Md$ à refinancer en trois ans, un montant modeste rapporté aux 125 Md$ d'encours : Oracle a allongé sa dette (tranches 2046, 2056, 2066 en février 2026).

Coût. Les obligations de février 2026 ont été placées à des écarts de 95 points de base (2029) et 115 points de base (2031) au-dessus des Treasuries (source 12). Sur le marché secondaire en septembre 2026, les titres Oracle rendent 6,26 % (échéance 2030), 6,93 % (2035) et 7,60 % (2061) (source 16), soit 1,3 à 2,6 points au-dessus du Trésor à 10 ans, lui-même à 5 % depuis la hausse de la Fed du 16 septembre. La charge d'intérêts du troisième trimestre 2026 était de 1,18 Md$, soit 7 % du chiffre d'affaires (source 17) ; annualisée et augmentée des 25 Md$ de février à 5,8 %, elle approche 6 Md$ par an (calcul de l'auteur ; le chiffre annuel exact du 10-K n'a pas pu être vérifié, les sources secondaires divergeant). À cela s'ajoutent 6,0 Md$ de dividende ordinaire (2 $ par action sur environ 3,02 Md d'actions) et 0,33 Md$ de dividende préférentiel (calculs). Le rachat d'actions ne compte plus que 6,3 Md$ d'autorisation résiduelle et n'est plus exécuté à l'échelle (source 18).

## 5. Notations et marché du crédit

- **S&P** : abaissé de BBB à BBB- le 9 juillet 2026, perspective stable. Motifs : déficit de flux de trésorerie opérationnel libre attendu à près de 42 Md$ sur l'exercice 2027, dépendance à OpenAI (« risque de crédit central », environ la moitié du RPO), levier projeté au pic à 4,4x ; « nous pourrions abaisser Oracle si le levier reste durablement au-dessus de 4,5x » (Andrew Chang, S&P) (sources 4, 8).
- **Moody's** : Baa2, perspective négative, confirmée à l'émission de février 2026 ; « aucun autre hyperscaler n'est aussi endetté ni autant en flux de trésorerie négatif à l'entrée de cette phase de construction » ; le levier « pourrait approcher 5x temporairement » (source 8).
- **Fitch** : BBB, perspective stable (source 12).
- **CDS à cinq ans** : record à 203 points de base en décembre 2025, plus haut depuis 2008, contre 144 points en début d'année 2025 ; les obligations 6,7 % 2056 traitaient alors à 263 points de base d'écart (source 19). Les actions montent quand le RPO grossit, les CDS ne redescendent pas : les deux marchés ne lisent pas la même histoire.
- Un passage en catégorie spéculative par deux agences forcerait certains fonds à vendre et renchérirait la dette à venir. Un article de Fortune du 18 septembre 2026 soutient que « les propres chiffres de S&P ne justifient pas » le maintien en catégorie investissement (source 20).

## 6. Les flux : d'où vient et où va l'argent

| Exercice (clos fin mai) | Flux opérationnel | Capex | FCF | Source |
|---|---|---|---|---|
| fy2025 | 20,8 Md$ (déduit : +54 % → 32,0) | 21,2 Md$ | −5,1 Md$ sur douze mois glissants au 31/05/2025 (S&P) | 1, 4 |
| fy2026 | 32,0 Md$ | 55,66 Md$ (objectif initial 25, puis 35, puis 50) | −23,7 Md$ | 1, 10 |
| T1 fy2027 | n.d. | 28,5 Md$ | −5,4 Md$ | 2, 21 |
| fy2027 (guidance) | n.d. | 70 Md$ nets ; 90 à 95 Md$ bruts, dont 20 à 25 Md$ payés directement par les clients | S&P : déficit d'environ 42 Md$ | 2, 4 |

Le capex a été multiplié par 2,6 en un an et le trimestre d'août (28,5 Md$) est supérieur au chiffre d'affaires du trimestre (19,35 Md$). Pour couvrir 70 Md$ nets avec un flux opérationnel qui, même en hausse de 30 %, resterait autour de 40 Md$, il manque environ 30 Md$ par an, plus 6 Md$ d'intérêts et 6 Md$ de dividendes (calcul de l'auteur). C'est le sens des « environ 40 Md$ » à lever sur l'exercice 2027. Oracle s'est engagée à ne plus émettre d'obligations en année civile 2026 ; les 20 Md$ manquants viendront donc d'obligations en 2027, de nouvelles actions, ou de structures hors bilan.

## 7. Le hors-bilan : les baux

Le 10-Q de novembre 2025 recensait 248 Md$ d'engagements de loyers « substantiellement tous » liés à des centres de données, devant commencer entre fin 2025 et l'exercice 2028, et non encore inscrits au bilan (source 22). Les baux déjà actifs pèsent 30,6 Md$ de passifs non courants au 31 août 2026, avec un échéancier de paiements de 3,2 Md$ sur le reste de l'exercice 2027, puis environ 4,1 Md$ par an de 2028 à 2032 et 24,4 Md$ au-delà (source 6). Le mécanisme : un développeur (Crusoe, Vantage, Related Digital) construit le campus, financé par des fonds (Blue Owl, Blackstone, Pimco) ; Oracle signe un bail de quinze à vingt ans qui garantit la dette du projet ; les prêteurs regardent la signature d'Oracle, Oracle regarde celle d'OpenAI.

Stargate compte sept sites : Abilene (Texas, 0,6 GW en service), Shackelford (Texas, 2,0 GW), Doña Ana (Nouveau-Mexique, 2,2 GW), Milam (Texas), Port Washington (Wisconsin, 1,3 GW), Saline Township (Michigan, 1,4 GW, livraison T4 2028), Lordstown (Ohio), pour plus de 9 GW visés en 2029 ; Oracle s'est engagée sur 4,5 GW pour OpenAI (sources 23, 24). Le retrait de Blue Owl du projet du Michigan en décembre 2025 a fait chuter l'action et élargi les écarts obligataires ; le financement a été rebouclé par Blackstone et Related à 7,5 % sur vingt ans (sources 15, 19). Ce taux, supérieur de 1,7 point à ce qu'Oracle paie elle-même, est le prix du risque que les prêteurs attachent aux baux.

Analyse de l'auteur : en ajoutant les 248 Md$ de loyers futurs aux 125 Md$ d'obligations, les engagements financiers d'Oracle approchent 375 Md$, soit 5,6 années de chiffre d'affaires 2026. Les agences n'actualisent qu'une partie de ces loyers dans le levier ; c'est pour cela que Moody's évoque 5x là où la dette comptable donne 4,3x.

## 8. La dépendance à OpenAI

Le contrat : environ 300 Md$ sur cinq ans à partir de 2027, soit 60 Md$ par an (calcul), adossé à 4,5 GW de capacité (source 24). Le payeur : OpenAI, dont le chiffre d'affaires annualisé approchait 70 Md$ fin septembre 2026 après avoir dépassé 40 Md$ pendant l'été, qui a levé 122 Md$ en mars 2026 à 852 Md$ de valorisation et discute d'une levée d'au moins 30 Md$ à 1 400 Md$ comme pont avant une introduction en Bourse retardée, et qui a ramené en février 2026 ses engagements de calcul de 1 400 Md$ à environ 600 Md$ jusqu'en 2030 (source 25). En avril 2026, des informations selon lesquelles OpenAI avait manqué ses objectifs d'utilisateurs et de revenus ont fait chuter Oracle ; en septembre, cinq séances de baisse (−13,6 %) ont suivi la publication des résultats pour les mêmes raisons (sources 26, 27).

Le point dur : à partir de 2027, OpenAI devra payer à Oracle un montant proche de l'intégralité de son chiffre d'affaires actuel, tout en honorant des engagements comparables envers Microsoft, CoreWeave, Amazon et d'autres. Si OpenAI renégocie, retarde ou réduit, Oracle garde les centres de données, les baux et la dette.

## 9. Trois trajectoires de levier 2027-2028 (calculs de l'auteur)

Hypothèses communes : EBITDA 2026 d'environ 30 Md$ (dette de 129,5 Md$ pour un levier de 4,3x, source 8) ; capex net 70 Md$ en fy2027 et 60 Md$ en fy2028 (S&P voit un pic « au-dessus de 60 Md$ » en 2028, source 4) ; dividendes 6,3 Md$ par an ; pas de rachat d'actions.

| Scénario | Hypothèses | Dette fin fy2028 | EBITDA fy2028 | Levier | Note probable |
|---|---|---|---|---|---|
| OpenAI paie | EBITDA +30 % par an (cloud +60 %) ; 20 Md$ d'actions nouvelles supplémentaires | environ 165 Md$ | environ 51 Md$ | 3,2x | BBB- maintenu, perspective stable |
| OpenAI paie en retard | EBITDA +20 % par an ; 20 Md$ d'actions | environ 170 Md$ | environ 43 Md$ | 4,0x | BBB- sous surveillance ; Moody's Baa3 |
| OpenAI réduit de moitié | EBITDA +10 % par an ; capex réduit à 45 Md$ en fy2028 ; aucune action nouvelle | environ 175 Md$ | environ 36 Md$ | 4,9x | passage en catégorie spéculative chez S&P (seuil 4,5x) |

Lecture. Dans les trois cas la dette brute augmente d'au moins 40 Md$ d'ici mai 2028 ; ce qui sépare les scénarios est le dénominateur. Le seuil de S&P (4,5x) est franchi dès que la croissance de l'EBITDA tombe sous 15 % par an sans nouvelle émission d'actions. Chaque tranche de 20 Md$ d'actions dilue d'environ 5 % au cours actuel.

## 10. Ce que cela veut dire pour l'action

| Donnée | Valeur | Source |
|---|---|---|
| BPA non-GAAP fy2026 réalisé | 7,63 $ | data.csv (Zacks, 30/09/2026) |
| BPA fy2027 (consensus) | 8,12 $ ; guidance 8,10 $ | Zacks ; Oracle (2) |
| BPA fy2028 | 10,86 $ (+34 %) | Zacks |
| BPA fy2029 | n.d. ; chiffre d'affaires 2029 attendu 183 Md$ (17 analystes) | Barchart / Tickflow (28) |
| P/E fy2027 / fy2028 | 16,9x / 12,6x (calcul) | – |
| PEG sur la croissance 2027→2028 | 0,50 (calcul) ; PEG long terme du modèle du dépôt 0,82 (croissance centrale 18 %) | modèle (29) |
| Objectif de cours moyen | 243 à 252 $ selon les sources (45 analystes), « Strong Buy » ; probablement antérieur à la baisse de septembre | 28 |
| 52 semaines | 114,50 $ – 345,72 $ ; −40 % depuis le pic de septembre 2025, −25 % au premier semestre 2026 | 26, 28 |
| Zacks Rank | n° 3 (Hold) | 28 |
| Dividende | 2,00 $ par an (rendement 1,5 %) | 18 |
| Bêta (modèle) | 1,47 | data.csv |

Le modèle du dépôt donne un rendement espéré de +21,9 % par an sur quatre ans, mais un scénario pessimiste de −14,4 % par an, le troisième plus mauvais des 55 valeurs éligibles après Nvidia et AppLovin (source 29). La raison est dans ce dossier : le BPA 2028 à 10,86 $ suppose que les centres de données se remplissent et qu'OpenAI paie ; la dette, elle, est déjà là.

Règles de vente mesurables.
1. Dégradation en catégorie spéculative par S&P ou Moody's.
2. Levier dette/EBITDA publié au-dessus de 4,5x deux trimestres de suite.
3. Nouvelle émission d'actions au-delà des 40 Md$ annoncés pour fy2027, ou suspension du dividende.
4. RPO en baisse d'un trimestre sur l'autre, ou annonce d'une renégociation du contrat OpenAI.
5. Croissance de l'infrastructure cloud sous 60 % sur un trimestre (121 % au T1 fy2027).

Calendrier.
- Octobre 2026 : issue de la levée de 30 Md$ d'OpenAI ; mise à jour trimestrielle de l'avancement des sites Stargate.
- Début décembre 2026 : résultats du T2 fy2027 (chiffre d'affaires, capex, RPO, trésorerie).
- Janvier-février 2027 : éventuelle nouvelle émission obligataire (le moratoire porte sur l'année civile 2026) ; un an après la dégradation S&P, revue annuelle.
- Mars 2027 : résultats du T3 ; début des paiements du contrat OpenAI en 2027.

## 11. Le cas de l'ours et le cas du taureau

L'ours. Oracle a transformé un éditeur de logiciels à 30 % de marge de trésorerie en un promoteur immobilier de centres de données à levier de 4 à 5x, dont la moitié du carnet dépend d'un client qui perd de l'argent et qui a lui-même réduit ses ambitions de 1 400 à 600 Md$. Les prêteurs des projets exigent 7,5 %, les obligations Oracle rendent jusqu'à 7,6 %, les CDS ont touché un record depuis 2008, S&P est à un cran du junk et dit qu'il dégradera au-dessus de 4,5x. L'action a été divisée par 2,5 depuis son pic alors que les bénéfices montent : le marché actions commence à lire le bilan comme le marché obligataire. Si la croissance de l'EBITDA tombe à 10 %, le levier passe 4,9x en 2028 (section 9), la note tombe, le coût de la dette monte, et le BPA 2028 de 10,86 $ n'arrive jamais.

Le taureau. 664 Md$ de RPO, dont une part croissante prépayée ou en GPU fournis par les clients, un flux opérationnel de 32 Md$ qui croît de 54 %, une infrastructure cloud à +121 %, et un marché qui, à 17 fois le bénéfice 2027 et 12,6 fois celui de 2028, ne paie plus la croissance. Les échéances sont lointaines (22,9 Md$ sur trois ans), la trésorerie est de 37 Md$, et le programme d'actions a montré qu'Oracle pouvait lever 20 Md$ en un trimestre sans fermer le marché. Si OpenAI paie, le levier redescend sous 3,5x dès 2028 et le titre revient vers son P/E historique de 20 à 25.

Ce qui me ferait changer d'avis sur l'ours : un trimestre de flux de trésorerie libre positif, une baisse du capex guidée pour fy2028, et un contrat de taille comparable à celui d'OpenAI signé avec un client déjà rentable (Meta, Microsoft, un État). Confiance que l'ours est réfuté : 45 %.

## 12. Fiscalité et change pour un investisseur français

- Cotation : NYSE, ticker ORCL, en dollars. Pas de ligne Euronext liquide.
- PEA : non éligible (société américaine).
- Dividendes : retenue à la source américaine de 15 % avec formulaire W-8BEN, imposition française au PFU de 30 % avec crédit d'impôt. Le dividende de 2 $ est faible face aux engagements de capex ; sa coupe est un scénario que la presse évoque déjà (source 18).
- Change : exposition totale au dollar.

## 13. Sources

1. Oracle, résultats du T4 et de l'exercice 2026, 10/06/2026 : https://www.oracle.com/news/announcement/q4fy26-earnings-release-2026-06-10/ ; Storage Newsletter : https://www.storagenewsletter.com/2026/06/12/oracle-fiscal-4q26-and-fy26-financial-results/.
2. Oracle, 8-K résultats du T1 fy2027, 10/09/2026 : https://www.sec.gov/Archives/edgar/data/0001341439/000119312526265848/orcl-ex99_1.htm ; Benzinga : https://www.benzinga.com/node/61728003 ; Outlook Business, capex 95 Md$ et 40 Md$ à lever : https://www.outlookbusiness.com/amp/story/corporate/oracle-forecasts-95-bn-in-capex-for-fy27-plans-to-raise-40-bn-in-debt-and-equity ; CryptoBriefing, RPO 664 Md$ et commentaire Magouyrk : https://cryptobriefing.com/oracle-q1-fy27-earnings-revenue-rpo/.
3. Oracle, plan de financement 2026, 01/02/2026 (clients cités par Larry Ellison) : https://www.oracle.com/news/announcement/oracle-announces-equity-and-debt-financing-plan-2026-02-01/.
4. Heise, 09/07/2026, dégradation S&P à BBB- : https://www.heise.de/en/news/S-P-downgrades-Oracle-to-BBB-only-one-notch-above-junk-level-11363472.html ; Yahoo Finance, « Oracle stock shrugs off S&P downgrade » : https://finance.yahoo.com/markets/stocks/articles/oracle-stock-shrugs-off-p-185346661.html ; Investing.com, notations confirmées : https://www.investing.com/news/stock-market-news/oracles-credit-ratings-affirmed-amid-ai-infrastructure-expansion-93CH-4253750.
5. Oracle, 10-K fy2026 (31/05/2026) : https://www.sec.gov/Archives/edgar/data/0001341439/000119312526277521/orcl-20260531.htm (valeur comptable des emprunts 130 105 M$ ; échéances fy2027 7 210, fy2028 10 145, fy2029 5 500 M$).
6. Oracle, 10-Q T1 fy2027 (31/08/2026) : https://www.sec.gov/Archives/edgar/data/0001341439/000119312526389274/orcl-20260831.htm (emprunts 125,0 Md$ contre 128,1 ; trésorerie 36 369 M$ ; baux non courants 30 594 M$ ; échéancier des baux ; ATM 141 millions d'actions pour 19,9 Md$).
7. StockAnalysis, bilan ORCL : https://stockanalysis.com/stocks/orcl/financials/balance-sheet/ ; Macrotrends, dette long terme : https://www.macrotrends.net/stocks/charts/ORCL/oracle/long-term-debt.
8. Reuters via The Star, 05/08/2026, « Oracle goes for high-stakes ratings gamble » (levier 4,3x ; S&P 3,6x → 4,4x, seuil 4,5x ; Moody's « approcher 5x ») : https://www.thestar.com.my/tech/tech-news/2026/08/05/analysis-oracle-corp-goes-for-high-stakes-ratings-gamble-in-ai-strategy.
9. Khaleej Times, « Oracle's OpenAI reliance faces scrutiny » (18 Md$ levés en septembre 2025 ; 124 Md$ dus fin novembre 2025 baux compris) : https://www.khaleejtimes.com/business/tech/oracles-openai-reliance-faces-scrutiny-as-debt-fuelled-ai-buildout-raises-worries.
10. Fortune, 10/03/2026, « Oracle best quarter, negative free cash flow » : https://fortune.com/2026/03/10/oracle-best-quarter-negative-free-cash-flow-ai-spending/ ; Webull, fy2026 : 43 Md$ de dette et 5 Md$ d'actions levés : https://www.webull.com/news/15405690457662464.
11. Oracle, communiqué du 01/02/2026 : https://www.prnewswire.com/news-releases/oracle-announces-equity-and-debt-financing-plan-for-calendar-year-2026-302675778.html ; IFR, « bottom-up approach » : https://www.ifre.com/equities/2379787/oracle-takes-bottom-up-approach-to-funding-2026-capex.
12. Oracle, 424B2 du 04/02/2026 (tranches et coupons) : https://www.sec.gov/Archives/edgar/data/1341439/000119312526035603/d33906d424b2.htm ; FWP (écarts de 95 et 115 pb, notations attendues) : https://www.sec.gov/Archives/edgar/data/1341439/000119312526032650/d36096dfwp.htm ; Investing.com : https://www.investing.com/news/sec-filings/oracle-launches-20-billion-atthemarket-stock-offering-and-completes-25-billion-debt-issuance-93CH-4486640.
13. Oracle, 8-K du 10/03/2026 et FWP (préférentielles 6,50 %, 5,0 Md$ nets) : https://www.sec.gov/Archives/edgar/data/1341439/000119312526100148/orcl-20260310.htm ; https://www.sec.gov/Archives/edgar/data/1341439/000119312526034351/d24013dfwp.htm.
14. Oracle, 10-Q fy2025 T1 (2 841 M d'actions au 31/08/2025, 2 807 M au 31/05/2025) : https://www.sec.gov/Archives/edgar/data/1341439/000119312525200095/orcl-20250831.htm ; ROIC.ai, ATM 20 Md$ : https://www.roic.ai/news/oracle-plans-20-billion-in-common-stock-sales-to-fuel-cloud-infrastructure-expansion-02-02-2026.
15. DCD, Related Digital et financement de 16 Md$ : https://www.datacenterdynamics.com/en/news/related-digital-closes-in-on-16bn-financing-for-oracle-data-center-in-michigan-report/ ; Baxtel, Pimco 14 Md$ : https://baxtel.com/news/pimco-to-provide-14bn-for-oracle-michigan-data-center-project ; Yahoo/FT, retrait de Blue Owl : https://finance.yahoo.com/news/funding-stalls-oracle-8217-michigan-155238542.html ; CRE Daily : https://www.credaily.com/?p=217474.
16. Börse Stuttgart, cotations septembre 2026 : notes 2030 https://www.boerse-stuttgart.de/en/products/bonds/stuttgart/a4ehy6-oracle-corp-dl-notes-2025-25-30/ ; 2035 https://www.boerse-stuttgart.de/en/products/bonds/stuttgart/a4d6mv-oracle-corp-dl-notes-2025-25-35/ ; 2061 https://www.boerse-stuttgart.de/en/products/bonds/stuttgart/a3knyu--oracle-61/.
17. Oracle, résultats du T3 fy2026 (intérêts 1 180 M$, 7 % du chiffre d'affaires) : https://finviz.com/news/335854/oracle-announces-fiscal-year-2026-third-quarter-financial-results ; 10-Q du 28/02/2026 : https://www.sec.gov/Archives/edgar/data/1341439/000119312526101045/orcl-20260228.htm.
18. Simply Wall St, dividende : https://simplywall.st/stocks/us/software/nyse-orcl/oracle/dividend ; Yahoo Finance, « Oracle stock dividend under threat » : https://finance.yahoo.com/markets/stocks/articles/oracle-stock-dividend-under-threat-220700509.html ; Fintel, rachat résiduel 6,3 Md$ : https://fintel.io/s/us/ORCL.
19. AI Weekly, CDS record 203 pb : https://aiweekly.co/alerts/oracle-nvidia-alphabet-spacex-cds-hit-records-on-ai-debt ; Wealth Professional, « Oracle's race to power OpenAI puts its own credit on the line » : https://www.wealthprofessional.ca/investments/equity-markets/oracles-race-to-power-openai-puts-its-own-credit-on-the-line/391194 ; BondbloX, écarts après le retrait de Blue Owl : https://bondblox.com/news/oracles-bonds-slip-further-on-data-centre-split-with-blue-owl ; The Motley Fool, 18/12/2025 : https://www.fool.com/investing/2025/12/18/why-shares-of-oracle-are-getting-crushed-this-week.
20. Fortune, 18/09/2026, « S&P kept Oracle investment grade. Its own numbers don't support that call » : https://fortune.com/2026/09/18/sp-kept-oracle-investment-grade-its-own-numbers-dont-support-that-call/.
21. FourWeekMBA, T1 fy2027 (capex 28,5 Md$, FCF −5,4 Md$) : https://fourweekmba.com/ai-oracle-q1-fy2027-backlog-capex-analysis/ ; Constellation Research : https://www.constellationr.com/insights/news/oracle-q1-strong-and-so-capital-expenditures.
22. Bloomberg via Advisor Perspectives, 17/12/2025, « Oracle's $248 billion rent AI bombshell » : https://www.advisorperspectives.com/articles/2025/12/17/oracles-248-billion-rent-ai-bombshell ; Hudson Labs, baux de centres de données : https://www.hudson-labs.com/research/oracle-data-center-leases-orcl.
23. Epoch AI, « OpenAI Stargate: where the US sites stand » : https://epoch.ai/blog/openai-stargate-where-the-us-sites-stand ; OpenAI, cinq nouveaux sites : https://openai.com/index/five-new-stargate-sites/.
24. ETCentric, contrat de 300 Md$ : https://www.etcentric.org/?p=195746 ; Arabian Post, 4,5 GW : https://thearabianpost.com/openai-secures-massive-4-5-gw-cloud-power-from-oracle/.
25. TechCrunch, 29/09/2026, levée de 30 Md$ à 1 400 Md$ : https://techcrunch.com/2026/09/29/openai-reportedly-in-talks-to-raise-30b-round-at-1-4t-valuation/ ; Bloomberg : https://www.bloomberg.com/news/articles/2026-09-29/openai-targets-30-billion-in-new-funding-at-1-4-trillion-value ; Luminix, revenus annualisés et engagements ramenés à 600 Md$ : https://www.useluminix.com/reports/company-overviews/openai-financial-fact-sheet-june-2026 ; Tech Insider, levée de 122 Md$ : https://tech-insider.org/openai-122-billion-funding-round-852-billion-valuation-2026/.
26. Yahoo Finance, « Oracle made a $300 billion bet on OpenAI. It's paying the price » : https://finance.yahoo.com/news/oracle-made-a-300-billion-bet-on-openai-its-paying-the-price-205441863.html ; « Oracle stock plummeted by 25% in the first half of 2026 » : https://finance.yahoo.com/technology/ai/articles/oracle-stock-plummeted-25-first-012000513.html ; Invezz, 28/04/2026 : https://invezz.com/news/2026/04/28/oracle-stock-falls-as-openai-reportedly-misses-targets-300b-deal-in-focus/.
27. Stocktwits, cinq séances de baisse (−13,6 %) : https://stocktwits.com/news-articles/markets/equity/orcl-stock-falls-for-fifth-straight-session-traders-eye-open-ai-funding-news-potential-japan-cloud-deal-as-catalysts/cZtYInqRB2a ; FX Leaders, 29/09/2026 : https://www.fxleaders.com/news/2026/09/29/orcl-stock-attempts-a-rebound-as-openai-growth-boosts-oracles-cloud-outlook/.
28. Barchart, prévisions et objectifs : https://www.barchart.com/story/news/3478052/earnings-preview-what-to-expect-from-oracles-report ; Tickflow : https://tickflow.io/stock/ORCL/forecast ; Angel One, 52 semaines : https://angelone.in/us-stocks/oracle-corp ; Zacks via Nasdaq (Rank n° 3) : https://www.nasdaq.com/articles/oracle-orcl-surpasses-market-returns-some-facts-worth-knowing.
29. Modèle du dépôt : `portefeuille-peg-5-valeurs/outputs_7_lignes/resultats_par_valeur.csv` et `variantes_8_lignes.csv` (02/10/2026) ; hypothèses `data/hypotheses.csv` (ORCL : 5/18/25 %, plafond 25).
