# Nvidia : qui sont ses clients, comment ils ont changé en deux ans, et à quoi s'attendre

Dossier du 02/10/2026. Cours Nvidia 228,38 $ (Google Finance, clôture 30/09/2026), capitalisation 5 476 Md$. Position en portefeuille : 15 % (`portefeuille-peg-5-valeurs/data/portfolio.csv`).

Règles : aucun chiffre inventé. Chaque chiffre porte une source et une date. Donnée introuvable = « n.d. ». Les calculs maison sont signalés « calcul ». Exercice fiscal Nvidia : clôture fin janvier (FY2026 = février 2025 à janvier 2026).

Avertissement : ce dossier est rédigé par Claude, un modèle d'Anthropic. Anthropic est un client de Nvidia et une participation de Nvidia (jusqu'à 10 Md$ investis, cf. section 6). Les passages sur Anthropic reposent uniquement sur des sources publiques citées.

---

## 1. Résumé en dix lignes

- Nvidia ne nomme jamais ses clients. Ses dépôts à la SEC donnent seulement des « clients directs » anonymes (A, B, C, D) dépassant 10 % du chiffre d'affaires.
- La concentration a explosé en deux ans : 1 client à 13 % en FY2024, 3 clients à 12/11/11 % en FY2025, 2 clients à 22 % et 14 % en FY2026 (soit 36 % du chiffre d'affaires, calcul : 77,7 Md$).
- Au premier semestre FY2027, trois clients directs pèsent 16 %, 15 % et 13 % (44 % au total, calcul : 78 Md$ sur six mois).
- Derrière ces lettres, les analystes placent Microsoft en tête (environ 19 % du chiffre d'affaires selon Bloomberg, estimation début 2025), puis Meta (environ 9 %), Amazon et Alphabet. Les intermédiaires (Dell, Supermicro, Foxconn) comptent souvent comme « clients directs ».
- Le chiffre d'affaires data center est passé de 47,5 Md$ (FY2024) à 193,7 Md$ (FY2026), soit 4,1 fois (calcul), puis 164,2 Md$ sur le seul premier semestre FY2027.
- Depuis mai 2026, Nvidia publie deux blocs : « Hyperscale » (48,7 Md$ au T2 FY2027) et « AI Clouds, Industrial & Enterprise » (40,3 Md$). Le second croît plus vite (+138 % contre +102 %).
- Nouveaux gros clients : OpenAI, Anthropic, xAI, CoreWeave, Nebius, les États (« IA souveraine », plus de 30 Md$ en FY2026). Une partie est financée par Nvidia elle-même (42 Md$ de participations non cotées fin avril 2026).
- La Chine est tombée à 6,9 % du chiffre d'affaires FY2026 et les prévisions n'intègrent plus aucune vente de calcul data center en Chine.
- Pour l'avenir : guidance T3 FY2027 à 108 Md$, « environ +70 % » pour FY2028, 1 000 Md$ de commandes visibles jusqu'à fin 2027 selon Jensen Huang. Capex des quatre hyperscalers : 725 Md$ en 2026, plus de 1 000 Md$ modélisés pour 2027.
- Risques : puces maison (54 % des unités d'accélérateurs en 2027 selon JPMorgan), financement circulaire, concentration, Chine à zéro.

---

## 2. Ce que Nvidia publie officiellement

Nvidia distingue les « clients directs » (ceux qui lui achètent : assembleurs, distributeurs, ODM, OEM, fournisseurs de cloud, créateurs de modèles, intégrateurs) et les « clients indirects » (qui achètent via les premiers : clouds, consumer internet, entreprises, secteur public). Source : 10-K FY2026, https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm (25/01/2026).

| Période | Clients directs ≥ 10 % | Total des clients ≥ 10 % | Client indirect signalé | Source |
|---|---|---|---|---|
| FY2024 (clos 28/01/2024) | A : 13 % | 13 % | un client indirect ≈ 19 % (achète via A) | 10-K FY2024, https://www.sec.gov/Archives/edgar/data/1045810/000104581024000029/nvda-20240128.htm |
| FY2025 (clos 26/01/2025) | A : 12 %, B : 11 %, C : 11 % | 34 % | un client indirect ≥ 10 % (achète via B) | 10-K FY2025, https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm |
| T1 FY2026 | A : 16 %, B : 14 % | 30 % | n.d. | 10-Q, https://www.sec.gov/Archives/edgar/data/1045810/000104581025000116/nvda-20250427.htm |
| T2 FY2026 | A : 23 %, B : 16 % | 39 % | n.d. | 10-Q, https://www.sec.gov/Archives/edgar/data/1045810/000104581025000209/nvda-20250727.htm |
| T3 FY2026 | A : 22 %, B : 15 %, C : 13 %, D : 11 % | 61 % | n.d. | 10-Q, https://www.sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm |
| FY2026 (clos 25/01/2026) | A : 22 %, B : 14 % | 36 % | n.d. | 10-K FY2026 (lien ci-dessus) |
| T1 FY2027 (clos 26/04/2026) | 16 %, 14 % | 30 % | n.d. | 10-Q, https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000052/nvda-20260426.htm |
| T2 FY2027 (clos 26/07/2026) | un client : 16 % ; S1 : 16 %, 15 %, 13 % | 16 % (trimestre), 44 % (semestre) | n.d. | 10-Q, https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000075/nvda-20260726.htm |

Deux précisions du 10-Q du 26/07/2026. Cinq clients directs détenaient 22 %, 14 %, 13 %, 11 % et 10 % des créances clients, soit 70 % de l'encours (source : même 10-Q, repris par Hudson Labs, https://www.hudson-labs.com/research/nvidia-q2-2027-earnings). Et 38 % du chiffre d'affaires du T2 FY2027 vient de clients dont le siège est hors des États-Unis, contre 30 % un an plus tôt.

Lecture. Les lettres changent d'un trimestre à l'autre (le « A » d'un trimestre n'est pas forcément le « A » du suivant). La chute apparente de 61 % (T3 FY2026) à 16 % (T2 FY2027) ne signifie pas une dispersion de la clientèle : sur le semestre, trois clients font encore 44 %. Elle traduit plutôt des achats par vagues et le passage de certains hyperscalers en achat direct plutôt que via Dell ou Supermicro.

---

## 3. Qui se cache derrière les lettres

Nvidia ne confirme rien. Voici ce que disent les sources externes.

| Client probable | Estimation | Source et date |
|---|---|---|
| Microsoft | ≈ 19 % du chiffre d'affaires Nvidia en rythme annualisé ; 47 % de son capex irait à Nvidia | Bloomberg, repris par Yahoo Finance (« Big Tech's spending drove Nvidia's rise »), données au T4 FY2025 (26/01/2025) : https://finance.yahoo.com/news/big-techs-spending-drove-nvidias-rise-154027146.html |
| Meta | ≈ 9 % du chiffre d'affaires Nvidia ; 25 % de son capex | même source |
| Amazon, Alphabet | 3e et 4e contributeurs, part n.d. | même source |
| Dell, Supermicro, Foxconn (intermédiaires) | comptés comme « clients directs » ; Dell a enregistré 60,9 Md$ de commandes de serveurs IA au trimestre mai-juillet 2026 | BigGo Finance, 2026 : https://finance.biggo.com/news/2abfd8af-8b6b-4583-bbe4-7cc44f0af0e4 |

Le « client indirect ≈ 19 % » du 10-K FY2024 correspond, selon la presse, à Microsoft (Benzinga, 05/2024 : https://benzinga.com/markets/equities/24/05/39104473/nvidias-top-customer-may-be-microsoft-accounting-for-a-fifth-of-its-revenue-report). Trois ans plus tôt, Microsoft pesait moins de 1 % du chiffre d'affaires Nvidia (Bloomberg, données T4 FY2022).

Contrats publics récents avec les hyperscalers :

- **Meta**, 17/02/2026 : accord pluriannuel pour « des millions » de GPU Blackwell et Rubin, premier déploiement massif de CPU Grace seuls, serveurs Vera CPU en 2027, réseau Spectrum-X. Montant non communiqué. Sources : Bloomberg, https://www.bloomberg.com/news/articles/2026-02-17/meta-deepens-nvidia-ties-with-pact-to-use-millions-of-chips ; PureAI, 18/02/2026, https://pureai.com/Articles/2026/02/18/NVIDIA-expands-multiyear-AI-infrastructure-deal-with-Meta.aspx.
- **Microsoft** : partenaire du contrat Anthropic-Azure de 30 Md$ sur puces Grace Blackwell et Vera Rubin (cf. section 6).

La directrice financière Colette Kress a indiqué que les hyperscalers représentaient environ 50 % du chiffre d'affaires data center en FY2026 (CNBC, 25/08/2026 : https://www.cnbc.com/2026/08/25/nvidias-dependence-on-hyperscalers-faces-big-test-in-earnings-report.html).

---

## 4. L'évolution sur deux ans

### 4.1 Le chiffre d'affaires

| Exercice | Chiffre d'affaires total | Data center | Part data center (calcul) | Source |
|---|---|---|---|---|
| FY2024 | 60,9 Md$ | 47,5 Md$ | 78 % | 8-K T4 FY2025, https://www.sec.gov/Archives/edgar/data/1045810/000104581025000021/q4fy25cfocommentary.htm |
| FY2025 | 130,5 Md$ (+114 %) | 115,2 Md$ (+142 %) | 88 % | même source, 26/02/2025 |
| FY2026 | 215,9 Md$ (+65 %) | 193,7 Md$ (+68 %) | 90 % | 8-K T4 FY2026, https://www.sec.gov/Archives/edgar/data/1045810/000104581026000019/q4fy26pr.htm, 25/02/2026 |
| T1 FY2027 | 81,6 Md$ (+85 %) | 75,2 Md$ (+92 %) | 92 % | 8-K T1 FY2027, https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000051/q1fy27pr.htm, 05/2026 |
| T2 FY2027 | 96,2 Md$ (+106 %) | 89,0 Md$ (+117 %) | 92,5 % | Communiqué, https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027, 26/08/2026 |

Le data center a été multiplié par 4,1 entre FY2024 et FY2026 (calcul). La croissance a réaccéléré pendant quatre trimestres consécutifs jusqu'au T2 FY2027 (transcript, Motley Fool, 31/08/2026 : https://www.fool.com/earnings/call-transcripts/2026/08/31/nvidia-nvda-q2-2027-earnings-call-transcript/).

### 4.2 La nouvelle grille de lecture : Hyperscale contre « AI Clouds, Industrial & Enterprise »

Depuis FY2027, Nvidia découpe son chiffre d'affaires en trois blocs. Chiffres du T2 FY2027 (26/08/2026) :

| Bloc | T2 FY2027 | Variation annuelle | Part du data center (calcul) | Contenu |
|---|---|---|---|---|
| Hyperscale | 48,7 Md$ | +102 % | 54,7 % | Amazon, Microsoft, Alphabet, Meta et assimilés |
| AI Clouds, Industrial & Enterprise (ACIE) | 40,3 Md$ | +138 % | 45,3 % | néoclouds (CoreWeave, Nebius, Oracle Cloud), créateurs de modèles, entreprises, États |
| Edge Computing | 7,2 Md$ | +27 % | hors data center | jeu, pro, auto |

Source : StorageNewsletter, 27/08/2026, https://www.storagenewsletter.com/2026/08/27/nvidia-fiscal-2q27-financial-results/ ; Edgen, https://www.edgen.tech/news/post/nvidia-neocloud-sales-surge-138-as-data-center-revenue-hits-89b. La part ACIE monte : 41,2 % un an plus tôt, 42,8 % au T1 FY2027, 45,3 % au T2 (Edgen). Les néoclouds partenaires doivent finir 2026 avec 8 GW installés contre environ 3 GW fin 2025 (transcript du 26/08/2026).

### 4.3 L'IA souveraine

Le chiffre d'affaires « souverain » a plus que triplé en FY2026 et dépasse 30 Md$, tiré par le Canada, la France, les Pays-Bas, Singapour et le Royaume-Uni (Kress, appel du T4 FY2026, 25/02/2026 ; AOL/Motley Fool, https://www.aol.com/finance/nvidia-earnings-call-nvidias-ai-112000775.html). Calcul : 13,9 % du chiffre d'affaires FY2026. Autres projets : Humain (Arabie saoudite) avec xAI, jusqu'à 500 MW ; Stargate UAE à Abou Dabi avec G42, OpenAI, Oracle, SoftBank (Nasdaq, https://www.nasdaq.com/articles/nvidia-bets-sovereign-ai-will-it-shield-against-trade-war).

### 4.4 La Chine, de client majeur à zéro

- T1 FY2026 : 4,6 Md$ de ventes H20 avant la nouvelle obligation de licence (09/04/2025), 2,5 Md$ non livrés, charge de 4,5 Md$ sur les stocks (communiqué T1 FY2026, repris par MarketBeat : https://www.marketbeat.com/earnings/reports/2025-5-28-nvidia-co-stock).
- Accord de reversement de 15 % des ventes H20 au gouvernement américain (Benzinga, 07/2025 : https://benzinga.com/z/46453723).
- FY2026 : la Chine (Hong Kong incluse) tombe à 19,7 Md$ ; par siège du client, la Chine pèse 6,9 % du chiffre d'affaires, les États-Unis 70,6 %, Taïwan 17,3 %, Singapour 3,7 %. La direction se dit « effectivement exclue du marché chinois du data center » (10-K FY2026 repris par TickerLeague, https://tickerleague.com/companies/NVDA/how-it-makes-money, et Kalkine). Attention : 19,7 Md$ feraient 9,1 % du total (calcul) ; l'écart avec 6,9 % tient au changement de méthode géographique au T3 FY2026 (siège du client au lieu du lieu de facturation).
- La guidance du T3 FY2027 (108 Md$) ne suppose aucun revenu de calcul data center en Chine (InsiderFinance, https://www.insiderfinance.io/news/nvidia-earnings-record-quarter-china-caveat).

### 4.5 Le capex des quatre hyperscalers, moteur de tout le reste

| Année | Capex combiné | Détail | Source |
|---|---|---|---|
| 2024 | 256 Md$ (cinq acteurs, Oracle inclus) | Amazon 134,7 pour 2024 selon Introl ; Alphabet 52,5 ; Meta 72,2 (chiffres Introl, à recouper) | Introl, 01/01/2026, https://introl.com/blog/hyperscaler-capex-600b-ai-infrastructure-debt-financing-2026 |
| 2025 | ≈ 410 Md$ (quatre acteurs) ; 443 Md$ (cinq acteurs) | | Tom's Hardware, 2026, https://www.tomshardware.com/tech-industry/big-tech/big-techs-ai-spending-plans-reach-725-billion ; Introl |
| 2026 (guidance) | ≈ 725 Md$ (+77 %) | Amazon ≈ 200, Microsoft ≈ 190, Alphabet 175-185, Meta 115-135 | Tom's Hardware ; MLQ, https://mlq.ai/news/big-techs-2026-capex-range-reaches-720-billion-to-745-billion/ |
| 2027 (modèles) | > 1 000 Md$ | Evercore, Bank of America | Tom's Hardware (même article) |

Environ la moitié de ces budgets va aux serveurs et aux puces : systèmes Nvidia GB200/GB300, mais aussi TPU v6/v7 de Google, Trainium 2/3 d'Amazon et Maia de Microsoft (Tom's Hardware). Nvidia ne capte donc qu'une fraction, inconnue, de ce capex.

---

## 5. Les nouveaux gros clients : créateurs de modèles et néoclouds

| Client | Engagement envers Nvidia | Date | Source |
|---|---|---|---|
| OpenAI | lettre d'intention : au moins 10 GW de systèmes Nvidia, premier GW sur Vera Rubin au S2 2026 ; soit 4 à 5 millions de GPU | 22/09/2025 | Barchart, https://www.barchart.com/story/news/34966864/openai-and-nvidia-announce-100-billion-strategic-partnership-to-build-10gw-of-ai-data-centers |
| Anthropic | 30 Md$ d'achats Azure sur Grace Blackwell et Vera Rubin (jusqu'à 1 GW) ; accord Nscale 45 Md$ sur six ans en calcul Nvidia ; 10 Md$ avec Volta Infra (Norvège) ; 517 Md$ d'engagements de calcul au total, « derrière presque chaque dollar, Nvidia » | 11/2025 à 09/2026 | TechEconomy, 05/09/2026, https://techeconomy.ng/microsoft-nvidia-invest-anthropic-30b-cloud-deal ; 24/7 Wall St, 13/09/2026, https://247wallst.com/investing/2026/09/13/anthropic-locks-down-517-billion-in-compute-ahead-of-ipo-and-its-still-not-enough/ |
| xAI | 555 000 GPU (GB200, GB300) pour environ 18 Md$ ; Colossus porté à 2 GW ; financement de 20 Md$ via un véhicule qui achète les GPU et les loue à xAI | 10/2025 à 01/2026 | Tom's Hardware, https://www.tomshardware.com/pc-components/gpus/nvidia-backs-20-billion-xai-chip-deal ; Introl, https://introl.com/blog/xai-colossus-2-gigawatt-expansion-555k-gpus-january-2026 |
| Meta | « millions » de GPU Blackwell et Rubin, CPU Grace, Spectrum-X | 17/02/2026 | Bloomberg (section 3) |
| CoreWeave, Nebius, Oracle Cloud, Google Cloud, Microsoft Azure | cités par Nvidia comme exploitants de racks Vera Rubin au T2 FY2027 | 26/08/2026 | Edgen (section 4.2) |
| Thinking Machines Lab | au moins 1 GW de systèmes Vera Rubin | 2026 | TechnoSports, https://technosports.co.in/openai-first-to-announce-nvidia-vera-rubin/ |
| Dell (intermédiaire) | 60,9 Md$ de commandes de serveurs IA sur un trimestre | mai-juillet 2026 | BigGo (section 3) |

Nvidia dit vendre désormais une « plateforme AI factory complète » et capter une part plus grande de la dépense totale du data center (transcript du 26/08/2026). Autrement dit, la facture par client monte avec les CPU Vera, le réseau Spectrum-X et NVLink, pas seulement avec les GPU.

---

## 6. Nvidia finance une partie de ses propres clients

C'est le point le plus débattu. Les faits :

| Participation ou garantie | Montant | Date | Source |
|---|---|---|---|
| OpenAI | 30 Md$ investis dans le tour de mars 2026 (à 730 Md$ pré-money), au lieu des 100 Md$ de la lettre d'intention ; Huang : « peut-être la dernière fois » avant l'IPO | 03/2026 | Finviz, https://finviz.com/news/330373/jensen-huang-says-nvidias-30-billion-openai-investment-might-be-the-last-before-ipo ; DCD, https://www.datacenterdynamics.com/en/news/nvidia-plans-30bn-investment-in-upcoming-openai-funding-round/ |
| OpenAI (Ohio) | discussions sur une garantie de financement de 250 Md$ liée à un projet de 500 Md$ de data centers | 2026 | The Next Web, https://thenextweb.com/news/nvidia-40bn-ai-equity-investments-2026 |
| Anthropic | jusqu'à 10 Md$ | 11/2025 | TechEconomy (section 5) |
| xAI | jusqu'à 2 Md$ dans un tour de 20 Md$ | 10/2025 | TipRanks/The Fly, https://www.tipranks.com/news/the-fly/musks-xai-close-to-20b-funding-round-with-nvidia-investing-bloomberg-says-thefly |
| CoreWeave | 2 Md$ d'actions (22,9 M de titres à 87,20 $) ; engagement d'acheter la capacité invendue jusqu'en avril 2032 (commande de 6,3 Md$) | 01/2026 | Edgen (section 4.2) ; MarketBeat, https://www.marketbeat.com/articles/nvidias-openai-backstop-puts-ai-financing-risk-in-focus/ |
| Nebius | 9,3 % du capital ; Nebius prévoit 20 à 25 Md$ de capex en 2026 | 2026 | Edgen |
| Total participations non cotées | 42 Md$ au 30/04/2026 contre 3 Md$ un an plus tôt | 30/04/2026 | The Next Web (ci-dessus) |

Calcul : 42 Md$ représentent 0,77 % de la capitalisation de Nvidia. Le risque n'est pas la taille des participations. Il est dans la dépendance du chiffre d'affaires à des clients déficitaires : CoreWeave a perdu 740 M$ au T1 2026 avec 536 M$ d'intérêts et un flux de trésorerie libre de −4,7 Md$ (Kavout, https://www.kavout.com/market-lens/nvidia-s-ai-dominance-meets-circular-financing-a-systemic-risk-underpriced). OpenAI a perdu 38,5 Md$ en 2025 (cf. `research/anthropic/OPENAI.md`). Jensen Huang rejette le terme de financement circulaire (InvestingLive, https://investinglive.com/stocks/nvidia-s-huang-rejects-circular-financing-claims-as-investment-scrutiny-grows/). Les critiques renvoient au financement fournisseur de Cisco et Nortel en 2000 (Kavout).

---

## 7. À quoi s'attendre pour les années à venir

### 7.1 Ce que dit Nvidia

| Horizon | Indication | Source |
|---|---|---|
| T3 FY2027 (clos fin octobre 2026) | 108 Md$ ± 2 % de chiffre d'affaires, marge brute 74 %, hors Chine ; +89 % sur un an (calcul, base 57,0 Md$ au T3 FY2026) | Webull, 26/08/2026, https://www.webull.com/blog/304-Nvidia-Q2-FY2027-Earnings-Beats-Revenue-EPS-Estimates-Guides-Q3-to-108B |
| FY2028 (février 2027 à janvier 2028) | « attente préliminaire d'une croissance d'environ 70 % », « dans un scénario contraint par l'offre » (Kress) | transcript du 26/08/2026 |
| Carnet de commandes | 500 Md$ de commandes Blackwell et Rubin jusqu'à fin 2026 (GTC, 28/10/2025) ; « au moins 1 000 Md$ jusqu'à 2027 » (Huang, GTC 2026) | Motley Fool, https://www.fool.com/investing/2025/11/05/ceo-jensen-huang-just-delivered-fantastic-news-for ; IT Daily, https://itdaily.com/news/business/nvidia-dendert-naar-5-biljoen |
| Produits | Vera Rubin NVL144 au S2 2026 (3 nm, HBM4, 3 fois Blackwell Ultra) ; Rubin Ultra au S2 2027 ; Feynman en 2028 | TrendForce, https://www.trendforce.com/news/2025/03/19/news-gtc-2025-nvidia-unveils-more-on-rubin-gpus-announces-feynman-for-2028-in-roadmap-update/ ; VRLA Tech, https://vrlatech.com/nvidia-gpu-roadmap-2026-2030/ |

Calcul maison, à prendre comme ordre de grandeur : FY2027 ≈ 81,6 + 96,2 + 108 + T4 ≈ 394 à 407 Md$ selon que le T4 est stable ou en hausse de 12 %. Une croissance de 70 % en FY2028 donnerait 670 à 690 Md$. Le chiffre de 561,5 Md$ de consensus FY2027 cité par Value Add VC (https://valueaddvc.com/blog/big-tech-ai-capex-in-2025-microsoft-google-meta-amazon-and-the-spending-race) est incompatible avec les trimestres publiés ; je ne le retiens pas.

Consensus BPA : 8,79 $ pour FY2027 et 12,12 $ pour FY2028 selon Barchart (https://www.barchart.com/story/news/3449043/what-to-expect-from-nvidia-s-q2-2027-earnings-report, avant les résultats du 26/08/2026) ; 9,25 $ et 15,33 $ selon Zacks au 30/09/2026 (fichier `data/data.csv`). Au cours de 228,38 $, cela fait 24,7 fois FY2027 et 14,9 fois FY2028 sur la base Zacks (calcul).

### 7.2 Ce qui soutient la demande

- Capex des quatre hyperscalers : 725 Md$ en 2026, plus de 1 000 Md$ modélisés pour 2027 (section 4.5).
- Néoclouds : 3 GW fin 2025, 8 GW attendus fin 2026 (section 4.2).
- Créateurs de modèles : OpenAI 10 GW, Anthropic 517 Md$ d'engagements, xAI 2 GW, Thinking Machines 1 GW (section 5).
- États : plus de 30 Md$ en FY2026, croissance attendue « au moins en ligne avec le marché » (section 4.3).
- Demande d'inférence : deux tiers du calcul IA selon Introl (https://introl.com/blog/custom-silicon-inflection-2026-hyperscaler-asics-nvidia-gpu), ce qui est aussi la faiblesse (voir ci-dessous).

### 7.3 Ce qui menace la part de Nvidia

1. **Les puces maison des hyperscalers.** JPMorgan prévoit que les ASIC/XPU représenteront 41 % des unités d'accélérateurs IA en 2026, 54 % en 2027 et 55 % en 2028, dépassant les GPU (Futu, https://news.futunn.com/en/post/79488724/jpmorgan-custom-chips-will-account-for-more-than-50-of). Morgan Stanley reste plus prudent : les puces commerciales gardent environ 90 % de la valeur (X, 02/2025, https://x.com/Jukanlosreve/status/1890347962804625866). Introl cite des analystes voyant la part de Nvidia en inférence tomber de plus de 90 % à 20-30 % en 2028 ; source faible, à traiter comme un scénario bas. Microsoft a déployé Maia 200 en janvier 2026 (TSMC 3 nm, 30 % de performance par dollar en plus selon Microsoft). Broadcom guide 115 Md$ de chiffre d'affaires IA (Value Invest US, https://valueinvestus.com/articles/broadcom-115b-ai-forecast-nvidia-hbm-networking-trade).
2. **Les TPU de Google vendus à l'extérieur.** Anthropic a réservé jusqu'à un million de TPU, plus de 1 GW en 2026 (DCD, https://www.datacenterdynamics.com/en/news/google-and-anthropic-confirm-massive-1gw-cloud-deal-with-up-to-one-million-google-tpus/). Meta est cité comme autre grand client TPU (Yahoo Finance, https://finance.yahoo.com/news/google-takes-another-piece-nvidia-150700993.html). Anthropic utilise aussi Trainium d'Amazon.
3. **La concentration.** Trois clients à 44 % du semestre (section 2). Un report de capex chez un seul hyperscaler se verrait tout de suite.
4. **Le financement circulaire.** 42 Md$ de participations, garantie de 250 Md$ en discussion, engagement d'acheter la capacité invendue de CoreWeave jusqu'en 2032 (section 6).
5. **La Chine à zéro.** Aucune vente de calcul data center prévue. Toute réouverture serait un bonus, toute extension des contrôles à l'export (Blackwell B30A) un risque sur les ventes en Asie hors Chine.
6. **L'offre.** Nvidia se dit contrainte par l'offre pour FY2028. Le risque est chez TSMC (CoWoS) et sur la mémoire HBM4, pas chez les clients.

### 7.4 Les trois scénarios pour un actionnaire

| Scénario | Hypothèse | Cohérence avec le modèle du dépôt (`data/hypotheses.csv`, NVDA) |
|---|---|---|
| Pessimiste | digestion du capex en 2028-2029 ; les ASIC prennent la moitié des unités ; un hyperscaler coupe ; croissance du BPA 0 % après 2027 | hypothèse basse du modèle : 0 % |
| Central | capex > 1 000 Md$ en 2027, part Nvidia en valeur qui s'érode doucement ; BPA +15 % par an après 2027 | hypothèse centrale : 15 % |
| Optimiste | le GPU garde sa part, la plateforme complète (CPU, réseau) élargit la facture, FY2028 à +70 % puis +25 % | hypothèse haute : 25 % |

Le modèle du dépôt attribue 14 % de croissance long terme à Nvidia (Zacks) et plafonne le P/E de sortie. La guidance du 26/08/2026 (+70 % en FY2028) est au-dessus du consensus Zacks FY2028 (15,33 $ contre 9,25 $, soit +66 %, calcul). Il n'y a donc pas lieu de relever les hypothèses : l'écart entre la guidance et le consensus est déjà quasi nul.

---

## 8. Ce que ça change pour le portefeuille

- **Nvidia (15 %)** : la clientèle est plus large qu'il y a deux ans (néoclouds, États, créateurs de modèles), mais pas moins concentrée (44 % sur trois clients). Le vrai signal à surveiller trimestre par trimestre est le bloc ACIE : s'il décroche, c'est que les clients financés par la dette ou par Nvidia elle-même ralentissent.
- **TSMC (10 %)** : contrainte d'offre reconnue par Nvidia pour FY2028. Chaque GPU Rubin et chaque TPU ou Trainium passe par TSMC. C'est la ligne la moins exposée à la bataille GPU contre ASIC.
- **Oracle** (proposition, cf. `research/deepdives/ORCL.md`) : Oracle est à la fois client Nvidia (racks Vera Rubin) et fournisseur d'OpenAI. Le risque OpenAI décrit en section 6 est le même que celui du dossier Oracle.
- **Broadcom** (sorti du portefeuille le 02/10/2026) : le dossier confirme que l'arbitrage Nvidia contre Broadcom est un pari sur GPU contre ASIC. Le portefeuille a choisi le GPU.

Points de contrôle à venir : résultats du T3 FY2027 vers le 19/11/2026 (date n.d., à confirmer), 10-Q associé pour la concentration clients, capex trimestriels des quatre hyperscalers (fin octobre 2026), introduction en Bourse d'Anthropic (avant Thanksgiving selon Bloomberg, cf. `research/anthropic/ANTHROPIC_IPO.md`).

---

## 9. Sources

1. Nvidia, 10-K FY2024 (28/01/2024) : https://www.sec.gov/Archives/edgar/data/1045810/000104581024000029/nvda-20240128.htm
2. Nvidia, 10-K FY2025 (26/01/2025) : https://www.sec.gov/Archives/edgar/data/1045810/000104581025000023/nvda-20250126.htm
3. Nvidia, 10-K FY2026 (25/01/2026) : https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm
4. Nvidia, 10-Q T1 FY2026 : https://www.sec.gov/Archives/edgar/data/1045810/000104581025000116/nvda-20250427.htm
5. Nvidia, 10-Q T2 FY2026 : https://www.sec.gov/Archives/edgar/data/1045810/000104581025000209/nvda-20250727.htm
6. Nvidia, 10-Q T3 FY2026 : https://www.sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm
7. Nvidia, 10-Q T1 FY2027 : https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000052/nvda-20260426.htm
8. Nvidia, 10-Q T2 FY2027 : https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000075/nvda-20260726.htm
9. Nvidia, 8-K T4 FY2025, commentaire CFO : https://www.sec.gov/Archives/edgar/data/1045810/000104581025000021/q4fy25cfocommentary.htm
10. Nvidia, 8-K T4 FY2026 : https://www.sec.gov/Archives/edgar/data/1045810/000104581026000019/q4fy26pr.htm
11. Nvidia, 8-K T1 FY2027 : https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000051/q1fy27pr.htm
12. Nvidia, communiqué T2 FY2027 (26/08/2026) : https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027
13. Nvidia, 8-K T3 FY2026 (19/11/2025) : https://www.sec.gov/Archives/edgar/data/1045810/000104581025000228/q3fy26pr.htm
14. Motley Fool, transcript T2 FY2027 (31/08/2026) : https://www.fool.com/earnings/call-transcripts/2026/08/31/nvidia-nvda-q2-2027-earnings-call-transcript/
15. Hudson Labs, 10-Q T2 FY2027 : https://www.hudson-labs.com/research/nvidia-q2-2027-earnings
16. Daloopa, concentration clients : https://daloopa.com/blog/analyst-pov/nvidia-customer-concentration-a-big-4-earnings-preview
17. DCD, deux clients à 40 % (T2 FY2026) : https://www.datacenterdynamics.com/en/news/two-unnamed-customers-accounted-for-almost-40-of-nvidias-q2-2026-revenue/
18. Yahoo Finance / Bloomberg, Microsoft et Meta : https://finance.yahoo.com/news/big-techs-spending-drove-nvidias-rise-154027146.html
19. Benzinga, Microsoft client n° 1 (05/2024) : https://benzinga.com/markets/equities/24/05/39104473/nvidias-top-customer-may-be-microsoft-accounting-for-a-fifth-of-its-revenue-report
20. CNBC, dépendance aux hyperscalers (25/08/2026) : https://www.cnbc.com/2026/08/25/nvidias-dependence-on-hyperscalers-faces-big-test-in-earnings-report.html
21. StorageNewsletter, T2 FY2027 (27/08/2026) : https://www.storagenewsletter.com/2026/08/27/nvidia-fiscal-2q27-financial-results/
22. Edgen, néoclouds +138 % : https://www.edgen.tech/news/post/nvidia-neocloud-sales-surge-138-as-data-center-revenue-hits-89b
23. Webull, guidance T3 à 108 Md$ (26/08/2026) : https://www.webull.com/blog/304-Nvidia-Q2-FY2027-Earnings-Beats-Revenue-EPS-Estimates-Guides-Q3-to-108B
24. AOL / Motley Fool, IA souveraine > 30 Md$ : https://www.aol.com/finance/nvidia-earnings-call-nvidias-ai-112000775.html
25. Nasdaq, IA souveraine : https://www.nasdaq.com/articles/nvidia-bets-sovereign-ai-will-it-shield-against-trade-war
26. MarketBeat, transcript T1 FY2026 (H20) : https://www.marketbeat.com/earnings/reports/2025-5-28-nvidia-co-stock
27. Benzinga, accord 15 % H20 : https://benzinga.com/z/46453723
28. TickerLeague, géographie FY2026 : https://tickerleague.com/companies/NVDA/how-it-makes-money
29. InsiderFinance, guidance hors Chine : https://www.insiderfinance.io/news/nvidia-earnings-record-quarter-china-caveat
30. Tom's Hardware, capex 725 Md$ : https://www.tomshardware.com/tech-industry/big-tech/big-techs-ai-spending-plans-reach-725-billion
31. MLQ, fourchette 720-745 Md$ : https://mlq.ai/news/big-techs-2026-capex-range-reaches-720-billion-to-745-billion/
32. Introl, capex 2024-2025 (01/01/2026) : https://introl.com/blog/hyperscaler-capex-600b-ai-infrastructure-debt-financing-2026
33. Barchart, OpenAI 10 GW (22/09/2025) : https://www.barchart.com/story/news/34966864/openai-and-nvidia-announce-100-billion-strategic-partnership-to-build-10gw-of-ai-data-centers
34. Finviz, 30 Md$ dans OpenAI (03/2026) : https://finviz.com/news/330373/jensen-huang-says-nvidias-30-billion-openai-investment-might-be-the-last-before-ipo
35. DCD, 30 Md$ OpenAI : https://www.datacenterdynamics.com/en/news/nvidia-plans-30bn-investment-in-upcoming-openai-funding-round/
36. TechEconomy, Anthropic-Microsoft-Nvidia (05/09/2026) : https://techeconomy.ng/microsoft-nvidia-invest-anthropic-30b-cloud-deal
37. 24/7 Wall St, Anthropic 517 Md$ (13/09/2026) : https://247wallst.com/investing/2026/09/13/anthropic-locks-down-517-billion-in-compute-ahead-of-ipo-and-its-still-not-enough/
38. Tom's Hardware, xAI 20 Md$ : https://www.tomshardware.com/pc-components/gpus/nvidia-backs-20-billion-xai-chip-deal
39. Introl, Colossus 2 GW (01/2026) : https://introl.com/blog/xai-colossus-2-gigawatt-expansion-555k-gpus-january-2026
40. TipRanks, Nvidia dans xAI : https://www.tipranks.com/news/the-fly/musks-xai-close-to-20b-funding-round-with-nvidia-investing-bloomberg-says-thefly
41. Bloomberg, Meta-Nvidia (17/02/2026) : https://www.bloomberg.com/news/articles/2026-02-17/meta-deepens-nvidia-ties-with-pact-to-use-millions-of-chips
42. PureAI, détail Meta-Nvidia (18/02/2026) : https://pureai.com/Articles/2026/02/18/NVIDIA-expands-multiyear-AI-infrastructure-deal-with-Meta.aspx
43. BigGo Finance, Dell 60,9 Md$ : https://finance.biggo.com/news/2abfd8af-8b6b-4583-bbe4-7cc44f0af0e4
44. The Next Web, 42 Md$ de participations : https://thenextweb.com/news/nvidia-40bn-ai-equity-investments-2026
45. MarketBeat, garantie OpenAI : https://www.marketbeat.com/articles/nvidias-openai-backstop-puts-ai-financing-risk-in-focus/
46. Kavout, financement circulaire : https://www.kavout.com/market-lens/nvidia-s-ai-dominance-meets-circular-financing-a-systemic-risk-underpriced
47. InvestingLive, Huang sur le financement circulaire : https://investinglive.com/stocks/nvidia-s-huang-rejects-circular-financing-claims-as-investment-scrutiny-grows/
48. Motley Fool, 500 Md$ de commandes (05/11/2025) : https://www.fool.com/investing/2025/11/05/ceo-jensen-huang-just-delivered-fantastic-news-for
49. IT Daily, 1 000 Md$ jusqu'à 2027 : https://itdaily.com/news/business/nvidia-dendert-naar-5-biljoen
50. TrendForce, feuille de route Rubin/Feynman : https://www.trendforce.com/news/2025/03/19/news-gtc-2025-nvidia-unveils-more-on-rubin-gpus-announces-feynman-for-2028-in-roadmap-update/
51. VRLA Tech, feuille de route 2026-2030 : https://vrlatech.com/nvidia-gpu-roadmap-2026-2030/
52. TechnoSports, Vera Rubin et Thinking Machines : https://technosports.co.in/openai-first-to-announce-nvidia-vera-rubin/
53. Barchart, consensus BPA FY2027-2028 : https://www.barchart.com/story/news/3449043/what-to-expect-from-nvidia-s-q2-2027-earnings-report
54. Value Add VC, estimation FY2027 (non retenue) : https://valueaddvc.com/blog/big-tech-ai-capex-in-2025-microsoft-google-meta-amazon-and-the-spending-race
55. Futu / JPMorgan, ASIC 54 % des unités en 2027 : https://news.futunn.com/en/post/79488724/jpmorgan-custom-chips-will-account-for-more-than-50-of
56. X / Morgan Stanley, ASIC contre GPU (02/2025) : https://x.com/Jukanlosreve/status/1890347962804625866
57. Introl, point d'inflexion des ASIC : https://introl.com/blog/custom-silicon-inflection-2026-hyperscaler-asics-nvidia-gpu
58. Value Invest US, Broadcom 115 Md$ : https://valueinvestus.com/articles/broadcom-115b-ai-forecast-nvidia-hbm-networking-trade
59. DCD, Anthropic un million de TPU : https://www.datacenterdynamics.com/en/news/google-and-anthropic-confirm-massive-1gw-cloud-deal-with-up-to-one-million-google-tpus/
60. Yahoo Finance, TPU et Meta : https://finance.yahoo.com/news/google-takes-another-piece-nvidia-150700993.html
61. Google Finance, cours NVDA au 30/09/2026 ; Zacks, consensus BPA au 30/09/2026 (fichier `portefeuille-peg-5-valeurs/data/data.csv`).
