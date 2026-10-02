# TSMC : qui sont ses clients, comment ils ont changé en deux ans, et à quoi s'attendre

Dossier du 02/10/2026, complément du deep dive `TSM.md` (01/10/2026). Cours TSM 456,19 $ par ADR (Google Finance, clôture 30/09/2026), capitalisation 2 370 Md$. Position en portefeuille : 10 % (`portefeuille-peg-5-valeurs/data/portfolio.csv`).

Règles : aucun chiffre inventé. Chaque chiffre porte une source et une date. Donnée introuvable = « n.d. ». Les calculs maison sont signalés « calcul ». Exercice TSMC = année civile. Les montants en dollars convertis par TSMC sont ceux de ses communiqués.

Avertissement : ce dossier est rédigé par Claude, un modèle d'Anthropic. Les puces sur lesquelles tournent les modèles d'Anthropic (Nvidia, TPU de Google, Trainium d'Amazon) sont toutes fabriquées par TSMC. Les passages sur ces clients reposent uniquement sur des sources publiques citées.

---

## 1. Résumé en dix lignes

- TSMC ne nomme pas ses clients. Son rapport annuel (20-F) donne la part du premier et du deuxième client et celle des dix premiers.
- En deux ans, le premier client a changé : Apple pesait 25 % en 2023 et 22 % en 2024 ; en 2025, le premier client fait 19 % et le deuxième 17 %. La presse identifie Nvidia en tête (19 %) et Apple en deuxième (17 %), ce que Jensen Huang a confirmé en janvier 2026.
- Les dix premiers clients pèsent 78 % du chiffre d'affaires 2025 (70 % en 2023). La concentration monte, mais sur des clients plus nombreux et plus riches qu'en 2023.
- Le chiffre d'affaires est passé de 69,3 Md$ (2023) à 122,4 Md$ (2025). Calcul : Nvidia serait passé de 7,6 à 23,3 Md$ de facturation, soit 3,1 fois. Apple de 17,3 à 20,8 Md$.
- Le calcul haute performance (HPC) est passé de 43 % du chiffre d'affaires en 2023 à 51 % en 2024, 58 % en 2025 et 66 % au T2 2026. Le smartphone a reculé de 38 % à 22 %.
- Derrière Nvidia et Apple viennent, selon les analystes, Broadcom (puces TPU de Google et MTIA de Meta), AMD, MediaTek, Qualcomm, Intel. Broadcom pourrait entrer dans le trio de tête en 2026.
- L'Amérique du Nord fait 75 % des ventes 2025 (78 % au T2 2026), la Chine 9 %, en recul structurel depuis les contrôles à l'export.
- TSMC est le goulot d'étranglement commun à tous les camps : GPU Nvidia, ASIC Broadcom, TPU, Trainium, puces Apple. Nvidia réserverait plus de la moitié des capacités d'emballage CoWoS.
- Pour l'avenir : croissance 2026 « légèrement au-dessus de 40 % », capex 2026 relevé à 60-64 Md$, accélérateurs IA en croissance annuelle de 54-56 % jusqu'en 2029, hausses de prix de 3 à 10 % en 2027.
- Risques : concentration sur Nvidia, retour partiel d'Apple chez Intel en 2027 (faible volume), Samsung et Intel en 2 nm, Taïwan, dilution de marge des usines étrangères.

---

## 2. Ce que TSMC publie officiellement

TSMC publie dans son 20-F la part de ses dix premiers clients et celles des deux premiers, sans les nommer.

| Année | Premier client | Deuxième client | Dix premiers | Chiffre d'affaires | Source |
|---|---|---|---|---|---|
| 2022 | Apple selon la presse, part n.d. | n.d. | 68 % | n.d. ici | Tom's Hardware, https://www.tomshardware.com/tech-industry/analyst-estimates-nvidia-is-now-tsmcs-second-largest-customer-accounting-for-11-of-revenue-in-2023 |
| 2023 | 25 % | 11 % | 70 % | 2 161,74 Md NT$, 69,30 Md$ (−4,5 %) | 20-F 2023 repris par Tom's Hardware ; 6-K revenus décembre 2023, https://www.sec.gov/Archives/edgar/data/1046179/000104617924000002/tsm-revenue20240110x6k.htm |
| 2024 | 22 % | 12 % | 76 % | 90,08 Md$ (+33,9 %) | 20-F 2024, https://www.sec.gov/Archives/edgar/data/1046179/000119312525083423/d896993d20f.htm ; Fortune, 10/01/2025, https://fortune.com/asia/2025/01/10/taiwan-chip-giant-tsmc-2024-revenue-rose-demand-ai-technology |
| 2025 | 19 % | 17 % | 78 % | 3 809,05 Md NT$, 122,42 Md$ (+35,9 %) | 20-F 2025 repris par TechPowerUp, https://www.techpowerup.com/346835/nvidia-beats-apple-to-become-tsmcs-largest-customer ; 6-K T4 2025, https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm |

Qui est qui. Pour 2023 et 2024, la presse identifie Apple en premier et Nvidia en deuxième (Tom's Hardware ; TechSoda, https://techsoda.substack.com/p/explainer-tsmcs-2024-annual-report). Pour 2025, Nvidia passe premier à 19 % (726,974 Md NT$, +106 % sur un an) et Apple deuxième à 17 % (BigGo Finance, https://finance.biggo.com/news/yT4Zn5wByH9TLH69YbuX ; MacRumors, 28/01/2026, https://www.macrumors.com/2026/01/28/nvidia-replaces-apple-as-biggest-tsmc-customer/). Jensen Huang l'a dit publiquement en janvier 2026 (eWeek, https://www.eweek.com/news/nvidia-overtakes-apple-tsmc-largest-customer/ ; CNBC, 26/01/2026, https://www.cnbc.com/2026/01/26/nvidia-set-to-supplant-apple-as-tsmcs-largest-customer.html).

Calculs en dollars (part × chiffre d'affaires de l'année, ordre de grandeur) :

| Client | 2023 | 2024 | 2025 | Variation deux ans |
|---|---|---|---|---|
| Nvidia | 7,6 Md$ (11 %) | 10,8 Md$ (12 %) | 23,3 Md$ (19 %) | × 3,1 |
| Apple | 17,3 Md$ (25 %) | 19,8 Md$ (22 %) | 20,8 Md$ (17 %) | + 20 % |
| Dix premiers | 48,5 Md$ (70 %) | 68,5 Md$ (76 %) | 95,5 Md$ (78 %) | × 2,0 |

Lecture. Apple n'a pas reculé en dollars : il a été rattrapé. Nvidia a triplé sa facture. La part des dix premiers monte parce que les concepteurs de puces IA (Nvidia, Broadcom, AMD) grossissent plus vite que le reste.

---

## 3. Les clients 3 à 10 selon les analystes

TSMC ne dit rien au-delà des deux premiers. Estimations externes :

| Client | Part estimée 2025 | Ce qu'il fait fabriquer | Source |
|---|---|---|---|
| Broadcom | 7 à 11 % | TPU de Google, MTIA de Meta, puces réseau ; 240 000 wafers CoWoS réservés en 2026 | Morgan Stanley via Moomoo, https://www.moomoo.com/community/feed/taiwan-tsmc-s-top-10-customer-list-updates-high-price-112597935194918 ; iTiger, https://www.itiger.com/news/1121636208 |
| AMD | 7 à 8 % | CPU EPYC, GPU Instinct MI350/MI450 ; 80 000 à 105 000 wafers CoWoS 2026 | Morgan Stanley via Moomoo ; iTiger |
| MediaTek | 9 à 10 % | SoC smartphone, puces IA pour Google | SmBom, https://www.smbom.com/news/45740 |
| Qualcomm | 8 % | Snapdragon | SmBom |
| Intel | 6 à 7 % | Lunar Lake, Arrow Lake, tuiles 3 nm | SmBom |
| Google, Amazon, OpenAI | via Broadcom, Alchip, Marvell | TPU, Trainium, puce OpenAI | CNBC, 26/01/2026 (lien section 2) |

Pour 2026, les estimations divergent. SmBom (projection faite avant les résultats 2025) voit encore Apple à 22-25 %, Broadcom monter à 11-15 % et Nvidia à 11 %. Une estimation postérieure (MacRumors, 28/01/2026) donne Nvidia à environ 33 Md$ soit 22 % du chiffre d'affaires 2026, Apple à environ 27 Md$ soit 18 %. Je retiens la seconde, cohérente avec le 20-F 2025 ; la première est périmée.

---

## 4. L'évolution sur deux ans

### 4.1 Par plateforme : l'IA remplace le smartphone

| Période | HPC | Smartphone | IoT | Automobile | Source |
|---|---|---|---|---|---|
| 2023 | 43 % | 38 % | n.d. | n.d. | DigiTimes, 16/01/2025, https://www.digitimes.com/news/a20250116VL206.html |
| 2024 | 51 % (+58 % en valeur) | 35 % (+23 %) | n.d. (+2 %) | n.d. (+4 %) | DigiTimes, même article |
| 2025 | 58 % (+48 %) | 29 % | n.d. | n.d. | transcript T4 2025 via Stock Taper, https://www.stocktaper.com/earningsCallSummary/TSM/2025/Q4 |
| T2 2026 | 66 % (+20 % t/t) | 22 % (−4 % t/t) | 5 % | 4 % | Investing.com, 16/07/2026, https://www.investing.com/news/company-news/tsmc-q2-2026-slides-ai-demand-drives-record-margins-hpc-surges-20-93CH-4794789 |

Calcul : le HPC en dollars passe d'environ 45,9 Md$ (2024) à 71,0 Md$ (2025) et à 26,5 Md$ sur le seul T2 2026. Les accélérateurs d'IA au sens strict (GPU, ASIC, HBM contrôleurs) ont pesé 17 à 19 % du revenu wafer 2025 (TrendForce, 16/10/2025, https://www.trendforce.com/news/2025/10/16/news-tsmc-unfazed-by-nvidia-gpu-curbs-in-china-eyes-mid-40-ai-revenue-cagr-through-2029/) ; le reste du HPC, ce sont les CPU, les puces réseau et les GPU de jeu.

### 4.2 Par nœud : le 3 nm passe devant

| Période | 2 nm | 3 nm | 5 nm | 7 nm | ≤ 7 nm | Source |
|---|---|---|---|---|---|---|
| 2023 | – | 6 % (lancement) | n.d. | n.d. | 58 % | DigiTimes, 16/01/2025 |
| 2024 | – | 18 % | 34 % | 17 % | 69 % | DigiTimes, 16/01/2025 |
| 2025 | – | 24 % | 36 % | 14 % | 74 % | Stock Taper, T4 2025 |
| T2 2026 | 3 % | 30 % | 33 % | 11 % | 77 % | Investing.com, 16/07/2026 |

Note : le 3 nm 2023 à 6 % vient de la présentation T4 2023 de TSMC ; chiffre non recoupé ici, à vérifier.

### 4.3 Par géographie : l'Amérique du Nord écrase tout

| Période | Amérique du Nord | Chine | Asie-Pacifique | Japon | EMEA | Source |
|---|---|---|---|---|---|---|
| T3 2024 | 71 % | 11 % | 10 % | 5 % | 3 % | DigiTimes, 17/10/2024, https://digitimes.com/news/a20241017VL205.html |
| 2024 | 75 % | 9 % | 9 % | 4 % | 3 % | TelecomLead, https://telecomlead.com/semiconductor/main-facts-about-tsmc-business-growth-from-ai-in-2024-119666 |
| 2025 | 75 % | 9 % | n.d. | n.d. | n.d. | FourWeekMBA, https://fourweekmba.com/tsmc-revenue-breakdown/ |
| T1 2026 | 77 % | n.d. | n.d. | n.d. | n.d. | FourWeekMBA (69 % au T1 2025) |
| T2 2026 | 78 % | 6 % | 8 % | 4 % | 4 % | deep dive `TSM.md`, section 1 |

La Chine pesait 22 % « il y a quelques années » (FourWeekMBA, date de référence n.d.). TSMC a cessé de fabriquer des accélérateurs IA et GPU en 7 nm et moins pour les clients chinois sur instruction du département du Commerce américain (3DTested, https://www.3dtested.com/tech-industry/tsmc-bans-more-chip-sales-to-china-due-to-stricter-u-s-export-sanctions). Impact estimé à l'époque : 5 à 8 % du chiffre d'affaires (iConnect007, https://mail.iconnect007.com/article/142965/reports-indicate-tsmc-to-tighten-scrutiny-on-chinese-ai-chip-clients-potential-revenue-impact-between-5-to-8/142962/ein). Les usines de Nankin et Shanghai (16 et 28 nm) ont dégagé 39,177 Md NT$ de résultat net en 2025 (TrendForce, 02/03/2026, https://www.trendforce.com/news/2026/03/02/news-tsmcs-2025-overseas-split-china-leads-profits-arizona-turns-profitable-japan-losses-triple/).

### 4.4 Le capex suit les clients

| Année | Capex | Capex / chiffre d'affaires (calcul) | Source |
|---|---|---|---|
| 2024 | 29,8 Md$ | 33 % | Nasdaq/Zacks, https://www.nasdaq.com/articles/tsmc-commits-higher-capex-2026-while-raising-dividend-payouts |
| 2025 | 40,9 Md$ | 33 % | même source |
| 2026 | 52-56 Md$ (01/2026), relevé à 60-64 Md$ (16/07/2026) ; 70-80 % pour les nœuds avancés, 10-20 % pour l'emballage | 36 % sur 171 Md$ de CA estimé | TrendForce, 15/01/2026, https://www.trendforce.com/news/2026/01/15/news-tsmc-q1-revenue-guidance-hits-35-8b-up-38-yoy-unveils-record-56b-capex-for-2026/ ; BigGo, 16/07/2026, https://finance.biggo.com/news/US_TSM_2026-07-16 |

Le capex a doublé en deux ans (calcul : 2,1 fois). C'est la réponse de TSMC à la demande de Nvidia, Broadcom et AMD. Le dossier Nvidia (`NVDA_CLIENTS.md`) montre que Nvidia se dit « contrainte par l'offre » pour FY2028 : la contrainte, c'est ce capex.

### 4.5 CoWoS : la file d'attente

| Élément | Chiffre | Source |
|---|---|---|
| Capacité CoWoS fin 2026 | 127 000 wafers par mois (TrendForce) ; 95 000 selon JPMorgan, 112 000 fin 2027 | iTiger, https://www.itiger.com/news/1121636208 ; TrendForce, https://www.trendforce.com/news/?p=59316 |
| Expansion 2027 | plus de 60 % de capacité supplémentaire ; rumeur à 200 000 par mois | TrendForce ; iTiger |
| Nvidia | plus de la moitié de la capacité, 800 000 à 850 000 wafers par an ; 1 200 000 attendus en 2027 | iTiger |
| Broadcom | plus de 240 000 wafers en 2026 (TPU Google, MTIA Meta) ; autre estimation 185 000 (+93 %) | iTiger |
| AMD | 80 000 à 105 000 wafers en 2026 | iTiger |

Calcul : 825 000 wafers Nvidia sur 1 524 000 de capacité annuelle (127 000 × 12) font 54 %. Sources de qualité moyenne (agrégateurs citant des rapports de courtiers) ; ordres de grandeur seulement.

---

## 5. Les trois camps qui passent tous par TSMC

| Camp | Clients TSMC | Nœud et emballage | Ce que ça change |
|---|---|---|---|
| GPU marchands | Nvidia (Blackwell, Rubin sur N3P, Rubin Ultra en 2 nm), AMD (MI450 en 2 nm) | 3 nm puis 2 nm, CoWoS-L | Nvidia à 19 % puis ~22 % du CA |
| ASIC des hyperscalers | Broadcom (TPU Google, MTIA Meta), Alchip et Marvell (Trainium Amazon), MediaTek (TPU Google) | 3 nm puis 2 nm, CoWoS | Broadcom vers le trio de tête |
| Appareils | Apple (A20 en 2 nm pour l'iPhone 18, plus de 50 % de l'allocation N2 initiale), Qualcomm, MediaTek | 3 nm, 2 nm | Apple reste n° 2 mais recule en part |

Sources : TweakTown, https://tweaktown.com/news/112989/tsmc-is-ramping-up-2nm-production-100k-monthly-wafers-by-the-end-of-2026/index.html ; iTiger, https://www.itiger.com/news/1105875242 ; TrendForce, 22/09/2025, 15 clients 2 nm dont 10 en HPC, https://www.trendforce.com/news/2025/09/22/news-tsmc-2nm-customer-surge-15-clients-reportedly-secured-10-in-hpc/.

Le 2 nm : production en volume début 2026 à Hsinchu (Fab 20), 50 000 à 60 000 wafers par mois au S1 2026, 100 000 visés fin 2026 (TweakTown). Il pèse déjà 3 % du revenu wafer au T2 2026.

Conclusion de la section : le dossier Nvidia montre que JPMorgan attend 54 % des unités d'accélérateurs en ASIC dès 2027. Pour TSMC, cette bataille est neutre en volume : les deux camps achètent les mêmes wafers 3 nm et 2 nm et le même CoWoS. Elle n'est pas neutre en prix : un ASIC est plus petit qu'un GPU Rubin et se vend moins cher, donc la facture par puce est plus basse. Chiffre n.d.

---

## 6. À quoi s'attendre pour les années à venir

### 6.1 Ce que dit TSMC

| Horizon | Indication | Source |
|---|---|---|
| T3 2026 | 44,6 à 45,8 Md$, marge brute 65-67 % | 6-K, 16/07/2026, https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000451/a2q26e_withguidancexfinal.htm |
| 2026 | croissance « légèrement au-dessus de 40 % » en dollars (contre « près de 30 % » en janvier) ; calcul : environ 171 Md$ | BigGo, 16/07/2026 |
| 2024-2029 | chiffre d'affaires total : croissance annuelle « proche de 25 % » (relevée de 20 %) ; calcul : environ 275 Md$ en 2029 | transcript T4 2025, https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-01/51d09df96cd89ac19d65af39032b038dc2896a24/TSMC%204Q25%20Transcript.pdf |
| 2024-2029 | accélérateurs IA : croissance annuelle 54-56 % (contre « mid-40s » un an plus tôt) ; calcul sur une base 2025 d'environ 22 Md$ : environ 127 Md$ en 2029 | Techleap, https://finder.techleap.nl/news/feed/tsmc-raises-ai-chip-revenue-forecast-to-50-cagr-through-2029 |
| Marges | dilution des usines étrangères 2-3 points au début, 3-4 points ensuite ; 2 nm : 3-4 points au S2 2026 | Yahoo Finance, T2 2026, https://finance.yahoo.com/markets/stocks/articles/taiwan-semiconductor-manufacturing-co-ltd-130034778.html |
| Prix 2027 | hausse de 3 à 6 % des wafers (KuCoin) ; jusqu'à 10 % y compris nœuds matures 12-28 nm (Nikkei via AI Weekly) ; prime de 10-15 % sur les volumes IA hors prévision | KuCoin, https://www.kucoin.com/blog/tsmc-reportedly-plans-3-6-wafer-price-hike-in-2027-as-ai-demand-pushes-orders-to-2030 ; AI Weekly, https://aiweekly.co/alerts/tsmc-to-lift-chip-prices-up-to-10-from-2027-nikkei-reports ; Tom's Hardware, https://www.tomshardware.com/tech-industry/semiconductors/tsmc-eyes-price-hikes-of-up-to-25-percent-on-chip-production-services-in-2027-report-claims-plans-to-raise-baseline-prices-by-5-percent-to-10-percent-on-advanced-nodes |

Ventes mensuelles : août 2026 à 514,81 Md NT$ (+53,3 % sur un an), janvier-août 3 386,87 Md NT$ (+39,3 %) (6-K, 10/09/2026, https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000658/tsm-revenue20260910.htm). Septembre sera publié le 08/10/2026, les résultats du T3 le 15/10/2026 (calendrier IR TSMC).

Consensus BPA par ADR : 16,56 $ (2026), 21,22 $ (2027), 28,05 $ (2028) selon Zacks et Yahoo au 30/09/2026 (`data/data.csv`). Au cours de 456,19 $ : 27,5 fois 2026, 21,5 fois 2027, 16,3 fois 2028 (calcul). Les analystes modélisent environ 17,5 % de croissance annuelle du chiffre d'affaires et 17,8 % du BPA à moyen terme (Simply Wall St, https://simplywall.st/stocks/ar/semiconductors/base-tsm/taiwan-semiconductor-manufacturing-shares/future), en dessous de la cible de 25 % de TSMC.

### 6.2 Ce qui soutient la demande

- Les commandes de Nvidia : 1 000 Md$ de Blackwell et Rubin visibles jusqu'à fin 2027 selon Huang, FY2028 à +70 % « contraint par l'offre » (voir `NVDA_CLIENTS.md`, section 7).
- Les ASIC : Broadcom guide 115 Md$ de chiffre d'affaires IA ; Anthropic a réservé un million de TPU, Meta en achète ; Trainium 3 et 4 chez Amazon ; tout cela est fabriqué chez TSMC.
- Le capex des hyperscalers : 725 Md$ en 2026, plus de 1 000 Md$ modélisés pour 2027 (voir `NVDA_CLIENTS.md`, section 4.5).
- Les prix : hausse de 3 à 10 % en 2027, marge brute à 67,7 % au T2 2026 malgré les usines étrangères.
- Le 2 nm : 15 clients, iPhone 18 en septembre 2026, AMD MI450, Rubin Ultra, TPU de 8e génération et Trainium 4 en 2027.

### 6.3 Ce qui menace la part ou la marge de TSMC

1. **La concentration sur Nvidia.** Un client à 19 % puis environ 22 %, dont le dossier `NVDA_CLIENTS.md` montre qu'il dépend lui-même de trois clients à 44 % et de clients déficitaires qu'il finance. Si le capex IA marque une pause en 2028-2029, TSMC le verra par Nvidia d'abord.
2. **Apple chez Intel.** Accord préliminaire pour fabriquer les puces M bas de gamme (MacBook Air, iPad Pro) sur Intel 18AP aux T2-T3 2027 ; 15 à 20 millions d'unités, jugé « non significatif pour TSMC pendant plusieurs années » (Ming-Chi Kuo via Appleosophy, 30/11/2025, https://appleosophy.com/2025/11/30/report-intel-may-manufacture-apples-low-end-m-series-chips-by-2027/ ; MobileSyrup, 06/02/2026, https://mobilesyrup.com/2026/02/06/apple-may-expand-chip-production-beyond-tsmc-amid-ai-boom/). Symbolique forte, impact chiffré faible.
3. **Samsung et Intel en 2 nm.** Samsung a signé un contrat pluriannuel avec Tesla ; Intel a Amazon et Apple en 18A ; six fondeurs auraient choisi Samsung faute de capacité TSMC (Motley Fool, 22/07/2026, https://fool.com/investing/2026/07/22/tsmc-cant-make-chips-fast-enough-and-rivals-are-po ; SemiWiki, https://semiwiki.com/semiconductor-manufacturers/intel/366523-tsmc-vs-intel-foundry-vs-samsung-foundry-2026/). Le marché mondial de la fonderie devrait croître de 29 % à 253,3 Md$ en 2026 (TechInsights via Motley Fool) : TSMC en prendrait environ deux tiers (calcul : 171 sur 253).
4. **Les marges.** Dilution de 3 à 4 points par les usines étrangères à terme, 3 à 4 points par le 2 nm au S2 2026. Arizona : 165 Md$ engagés, cinq usines de plus envisagées sous l'accord commercial États-Unis-Taïwan (TrendForce, 13/01/2026, https://www.trendforce.com/news/2026/01/13/news-tsmc-reportedly-plans-5-more-fabs-in-arizona-under-u-s-taiwan-trade-deal-investment-could-top-100b/). Blackwell est déjà produit à Phoenix (APH Networks, https://www.aphnetworks.com/news/30102-nvidia-amd-ramp-tsmc-arizona-us-tariffs-loom).
5. **Les droits de douane (Section 232).** Les fondeurs taïwanais qui construisent aux États-Unis pourraient importer 2,5 fois la capacité en construction sans droits, puis 1,5 fois la production américaine (Finviz, https://finviz.com/news/278421/trump-administration-offers-tariff-relief-in-exchange-for-250-billion-taiwan-chip-investment-tsmc-weighs-arizona-expansion-says-howard-lutnick). Détail et calendrier n.d.
6. **Taïwan.** Risque non chiffrable, déjà traité dans `TSM.md`. Il explique le plafond de P/E de sortie à 24 dans le modèle.
7. **La Chine.** 9 % des ventes, en baisse, et plus aucun accélérateur avancé. Un durcissement supplémentaire coûterait au plus quelques points ; une réouverture serait un bonus non modélisé.

### 6.4 Les trois scénarios pour un actionnaire

| Scénario | Hypothèse | Cohérence avec `data/hypotheses.csv` (TSM) |
|---|---|---|
| Pessimiste | plafonnement du capex hyperscaler en 2028, Nvidia ralentit, Apple bascule plus de volume chez Intel ; BPA +6 % par an | hypothèse basse : 6 % |
| Central | croissance du CA 2026 à +40 % puis retour vers 17-20 % (consensus), marge brute 63-65 % avec la dilution ; BPA +17 % par an | hypothèse centrale : 17 % |
| Optimiste | TSMC tient sa cible de 25 % par an jusqu'en 2029, prix +3-10 % en 2027, GPU et ASIC se cumulent ; BPA +24 % par an | hypothèse haute : 24 % |

Il n'y a pas lieu de modifier les hypothèses du modèle : la cible de 25 % de TSMC est déjà au-dessus de l'hypothèse haute, et le consensus (17,5 %) colle à l'hypothèse centrale.

---

## 7. Ce que ça change pour le portefeuille

- **TSMC (10 %)** est la ligne qui gagne quel que soit le vainqueur entre GPU et ASIC. C'est l'argument central pour la garder. Son risque n'est pas la part de marché, c'est le volume total de capex IA et Taïwan.
- **Nvidia (15 %) et TSMC** sont corrélées : Nvidia fait 19 à 22 % des ventes de TSMC. Les deux lignes font ensemble 25 % du portefeuille exposé au même capex. Le modèle le reflète déjà par le bêta et le stress test « krach IA ».
- **Broadcom** (sorti le 02/10/2026) : le dossier confirme que Broadcom monte vers le trio de tête de TSMC. Si l'on veut une couverture du scénario ASIC, c'est par Broadcom, pas par TSMC qui est déjà exposé aux deux.
- **Apple** n'est pas en portefeuille. Sa part chez TSMC recule, mais sa facture en dollars monte encore.

Points de contrôle : ventes de septembre le 08/10/2026 ; résultats du T3 le 15/10/2026 (guidance T4, capex 2027, premiers commentaires sur les prix 2027) ; 20-F 2026 au printemps 2027 pour la part de Nvidia.

---

## 8. Sources

1. TSMC, 20-F 2024 : https://www.sec.gov/Archives/edgar/data/1046179/000119312525083423/d896993d20f.htm
2. TSMC, 6-K revenus décembre 2023 (10/01/2024) : https://www.sec.gov/Archives/edgar/data/1046179/000104617924000002/tsm-revenue20240110x6k.htm
3. TSMC, 6-K T4 2025 (15/01/2026) : https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm
4. TSMC, transcript T4 2025 : https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-01/51d09df96cd89ac19d65af39032b038dc2896a24/TSMC%204Q25%20Transcript.pdf
5. TSMC, 6-K T2 2026 (16/07/2026) : https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000451/a2q26e_withguidancexfinal.htm
6. TSMC, 6-K revenus août 2026 (10/09/2026) : https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000658/tsm-revenue20260910.htm
7. Tom's Hardware, clients 2023 : https://www.tomshardware.com/tech-industry/analyst-estimates-nvidia-is-now-tsmcs-second-largest-customer-accounting-for-11-of-revenue-in-2023
8. TechSoda, rapport annuel 2024 : https://techsoda.substack.com/p/explainer-tsmcs-2024-annual-report
9. TechPowerUp, Nvidia premier client 2025 : https://www.techpowerup.com/346835/nvidia-beats-apple-to-become-tsmcs-largest-customer
10. BigGo Finance, 726,974 Md NT$ : https://finance.biggo.com/news/yT4Zn5wByH9TLH69YbuX
11. MacRumors, 28/01/2026 : https://www.macrumors.com/2026/01/28/nvidia-replaces-apple-as-biggest-tsmc-customer/
12. eWeek, Huang confirme : https://www.eweek.com/news/nvidia-overtakes-apple-tsmc-largest-customer/
13. CNBC, 26/01/2026 : https://www.cnbc.com/2026/01/26/nvidia-set-to-supplant-apple-as-tsmcs-largest-customer.html
14. Fortune, CA 2024 (10/01/2025) : https://fortune.com/asia/2025/01/10/taiwan-chip-giant-tsmc-2024-revenue-rose-demand-ai-technology
15. Moomoo / Morgan Stanley, parts AMD et Broadcom : https://www.moomoo.com/community/feed/taiwan-tsmc-s-top-10-customer-list-updates-high-price-112597935194918
16. SmBom, classement 2026 : https://www.smbom.com/news/45740
17. DigiTimes, plateformes et nœuds 2024 (16/01/2025) : https://www.digitimes.com/news/a20250116VL206.html
18. DigiTimes, géographie T3 2024 (17/10/2024) : https://digitimes.com/news/a20241017VL205.html
19. TelecomLead, géographie 2024 : https://telecomlead.com/semiconductor/main-facts-about-tsmc-business-growth-from-ai-in-2024-119666
20. FourWeekMBA, répartition 2025 : https://fourweekmba.com/tsmc-revenue-breakdown/
21. Stock Taper, transcript T4 2025 : https://www.stocktaper.com/earningsCallSummary/TSM/2025/Q4
22. Investing.com, slides T2 2026 (16/07/2026) : https://www.investing.com/news/company-news/tsmc-q2-2026-slides-ai-demand-drives-record-margins-hpc-surges-20-93CH-4794789
23. BigGo Finance, appel T2 2026 : https://finance.biggo.com/news/US_TSM_2026-07-16
24. Yahoo Finance, appel T2 2026 : https://finance.yahoo.com/markets/stocks/articles/taiwan-semiconductor-manufacturing-co-ltd-130034778.html
25. TrendForce, accélérateurs IA 17-19 % (16/10/2025) : https://www.trendforce.com/news/2025/10/16/news-tsmc-unfazed-by-nvidia-gpu-curbs-in-china-eyes-mid-40-ai-revenue-cagr-through-2029/
26. Techleap, CAGR IA 54-56 % : https://finder.techleap.nl/news/feed/tsmc-raises-ai-chip-revenue-forecast-to-50-cagr-through-2029
27. Nasdaq/Zacks, capex 2024-2026 : https://www.nasdaq.com/articles/tsmc-commits-higher-capex-2026-while-raising-dividend-payouts
28. TrendForce, capex 52-56 Md$ (15/01/2026) : https://www.trendforce.com/news/2026/01/15/news-tsmc-q1-revenue-guidance-hits-35-8b-up-38-yoy-unveils-record-56b-capex-for-2026/
29. iTiger, CoWoS 2026-2027 : https://www.itiger.com/news/1121636208
30. TrendForce, CoWoS : https://www.trendforce.com/news/?p=59316
31. TweakTown, 2 nm 100 000 wafers : https://tweaktown.com/news/112989/tsmc-is-ramping-up-2nm-production-100k-monthly-wafers-by-the-end-of-2026/index.html
32. iTiger, allocation 2 nm : https://www.itiger.com/news/1105875242
33. TrendForce, 15 clients 2 nm (22/09/2025) : https://www.trendforce.com/news/2025/09/22/news-tsmc-2nm-customer-surge-15-clients-reportedly-secured-10-in-hpc/
34. KuCoin, prix 2027 +3-6 % : https://www.kucoin.com/blog/tsmc-reportedly-plans-3-6-wafer-price-hike-in-2027-as-ai-demand-pushes-orders-to-2030
35. AI Weekly / Nikkei, prix 2027 jusqu'à 10 % : https://aiweekly.co/alerts/tsmc-to-lift-chip-prices-up-to-10-from-2027-nikkei-reports
36. Tom's Hardware, prix 2027 : https://www.tomshardware.com/tech-industry/semiconductors/tsmc-eyes-price-hikes-of-up-to-25-percent-on-chip-production-services-in-2027-report-claims-plans-to-raise-baseline-prices-by-5-percent-to-10-percent-on-advanced-nodes
37. Appleosophy / Ming-Chi Kuo, Apple-Intel (30/11/2025) : https://appleosophy.com/2025/11/30/report-intel-may-manufacture-apples-low-end-m-series-chips-by-2027/
38. MobileSyrup, Apple-Intel (06/02/2026) : https://mobilesyrup.com/2026/02/06/apple-may-expand-chip-production-beyond-tsmc-amid-ai-boom/
39. Motley Fool, concurrence Intel et Samsung (22/07/2026) : https://fool.com/investing/2026/07/22/tsmc-cant-make-chips-fast-enough-and-rivals-are-po
40. SemiWiki, TSMC contre Intel contre Samsung 2026 : https://semiwiki.com/semiconductor-manufacturers/intel/366523-tsmc-vs-intel-foundry-vs-samsung-foundry-2026/
41. TrendForce, Arizona cinq usines (13/01/2026) : https://www.trendforce.com/news/2026/01/13/news-tsmc-reportedly-plans-5-more-fabs-in-arizona-under-u-s-taiwan-trade-deal-investment-could-top-100b/
42. APH Networks, Blackwell en Arizona : https://www.aphnetworks.com/news/30102-nvidia-amd-ramp-tsmc-arizona-us-tariffs-loom
43. Finviz, Section 232 et accord Taïwan : https://finviz.com/news/278421/trump-administration-offers-tariff-relief-in-exchange-for-250-billion-taiwan-chip-investment-tsmc-weighs-arizona-expansion-says-howard-lutnick
44. 3DTested, arrêt des accélérateurs pour la Chine : https://www.3dtested.com/tech-industry/tsmc-bans-more-chip-sales-to-china-due-to-stricter-u-s-export-sanctions
45. iConnect007, impact 5-8 % : https://mail.iconnect007.com/article/142965/reports-indicate-tsmc-to-tighten-scrutiny-on-chinese-ai-chip-clients-potential-revenue-impact-between-5-to-8/142962/ein
46. TrendForce, résultats des usines étrangères 2025 (02/03/2026) : https://www.trendforce.com/news/2026/03/02/news-tsmcs-2025-overseas-split-china-leads-profits-arizona-turns-profitable-japan-losses-triple/
47. Simply Wall St, consensus de croissance : https://simplywall.st/stocks/ar/semiconductors/base-tsm/taiwan-semiconductor-manufacturing-shares/future
48. Google Finance, cours TSM au 30/09/2026 ; Zacks et Yahoo Finance, consensus BPA (`portefeuille-peg-5-valeurs/data/data.csv`) ; deep dive `research/deepdives/TSM.md` (01/10/2026) ; dossier `research/deepdives/NVDA_CLIENTS.md` (02/10/2026).
