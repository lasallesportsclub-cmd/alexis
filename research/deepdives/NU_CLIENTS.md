# Nu Holdings : qui sont ses clients, comment ils ont changé en deux ans, et à quoi s'attendre

Dossier du 02/10/2026, complément du deep dive `NU.md` (01/10/2026) et du dossier `research/monzo/MONZO.md`. Cours 12,66 $ (Google Finance, clôture 30/09/2026), capitalisation 60,0 Md$. Position en portefeuille : 20 % (`portefeuille-peg-5-valeurs/data/portfolio.csv`), la plus grosse ligne.

Règles : aucun chiffre inventé. Chaque chiffre porte une source et une date. Donnée introuvable = « n.d. ». Les calculs maison sont signalés « calcul ». Exercice Nu = année civile. ARPAC = revenu mensuel moyen par client actif ; coût de service = coût mensuel moyen par client actif.

Différence avec Nvidia et TSMC. Comme Uber, Nu n'a aucun client à 10 % de ses revenus. Ses clients sont 139 millions de particuliers et 6 millions d'entreprises, répartis sur trois pays. La question n'est donc pas « qui sont les gros clients » mais « combien, où, combien rapportent-ils, et combien coûtent-ils ».

---

## 1. Résumé en dix lignes

- Nu sert 138,9 millions de clients au 30/06/2026, contre 93,9 millions fin 2023 : 1,5 fois en deux ans et demi.
- Le Brésil pèse encore 85 % des clients (118 millions, 62 % de la population adulte), mais sa part baisse : 94 % fin 2023. Le Mexique a triplé (5,2 → 15,8 millions), la Colombie a été multipliée par six (0,8 → 5 millions).
- 83,5 % des clients sont actifs, plus de 86 % au Brésil. 60 % des utilisateurs considèrent Nu comme leur banque principale.
- Chaque client actif rapporte 17,1 $ par mois (T2 2026) contre 10,6 $ fin 2023, soit +61 % (calcul), pour un coût de service de 0,8 $ par mois. Le revenu couvre 21 fois le coût (calcul).
- Le client moyen porte 326 $ de dépôts et 284 $ de crédit (calcul). Les dépôts ont presque doublé (23,7 → 45,3 Md$), le crédit aussi (18,2 → 39,4 Md$).
- Les revenus 2025 viennent à 91 % du Brésil, 7 % du Mexique et 2 % des autres pays (20-F 2025, calcul). Le Mexique a atteint le point mort au T1 2026 et a obtenu sa licence bancaire le 10/07/2026.
- Les clients les plus rentables sont les cohortes anciennes (ARPAC 25 $ dès fin 2024), les hauts revenus (Ultravioleta) et les 6 millions d'entreprises (Nu Empresas).
- Le crédit par carte fait 66 % du portefeuille ; les créances douteuses à plus de 90 jours montent à 6,9 %. C'est le risque principal.
- Pour l'avenir : États-Unis (approbation conditionnelle de l'OCC le 29/01/2026, lancement via Lead Bank le 10/09/2026), rachats d'actions de 1 Md$, Investor Day le 08/12/2026, Selic en baisse à 13,75 %.
- Rumeur Monzo (26/09/2026) démentie par Nu le 30/09/2026 : voir `research/monzo/MONZO.md`.

---

## 2. Qui sont les clients

| Clientèle | Taille | Ce qu'elle apporte | Source |
|---|---|---|---|
| Particuliers, Brésil | environ 118 M (30/06/2026), 62 % des adultes | 91 % des revenus 2025 | communiqué T2 2026, https://international.nubank.com.br/company/nu-holdings-ltd-reports-second-quarter-2026-financial-results/ (13/08/2026) ; 20-F 2025 |
| Particuliers, Mexique | 15,8 M (16 M en juillet 2026), 15 % des adultes, 12 000 clients ajoutés par jour | 7 % des revenus 2025 ; point mort au T1 2026 ; dépôts 5,7 Md$ | Crowdfund Insider, 07/2026, https://www.crowdfundinsider.com/2026/07/291252-nubank-subsidiary-nu-mexico-obtains-authorization-to-start-operations-as-licensed-bank/ ; NeoFeed, 14/05/2026 |
| Particuliers, Colombie | plus de 5 M (5 ans d'activité), 11 % des adultes | 2 % des revenus 2025 (« autres pays ») ; dépôts 3,3 Md$ | Nubank, https://international.nubank.com.br/company/nu-colombia-turns-five-with-5-million-customers-and-reinforces-its-long-term-commitment-to-the-country/ |
| Entreprises (Nu Empresas, Brésil) | 6 M de clients, première institution du pays en nombre de CNPJ ; 2 M de cartes de crédit émises | surtout des micro-entrepreneurs (MEI) ; montée vers les PME | Nubank, 05/2026, https://international.nubank.com.br/company/nu-empresas-reaches-6-million-customers-and-becomes-the-largest-financial-institution-in-brazil-in-number-of-cnpjs/ |
| Hauts revenus (Ultravioleta) | nombre n.d. | carte métal, 1 % de cashback, compte global Wise en plus de 40 devises, eSIM voyage | Nubank, https://international.nubank.com.br/consumers/high-income-focused-nubank-expands-benefits-for-ultravioleta-customers/ |
| Abonnés télécoms (NuCel) | 1 M (06/2026), 18 mois après le lancement | revenu hors banque, fidélisation | Nubank, https://international.nubank.com.br/consumers/nucel-reaches-1-million-customers-and-consolidates-nubank-as-a-platform-beyond-finance/ |
| États-Unis | lancement le 10/09/2026 via Lead Bank : compte d'épargne à 3,5 %, Nu Global (USDC/EURC, plus de 35 pays) | clients n.d. | `NU.md`, section 5 |

Aucun client ne pèse 10 % des revenus : le 20-F ne signale aucune concentration. Les trois moteurs de revenu par client sont le crédit (41 % de la marge brute au T2 2026), le placement des dépôts (34 %) et les commissions (25 %) (`NU.md`, section 1).

---

## 3. L'évolution sur deux ans

### 3.1 Combien de clients, et où

| Date | Total | Brésil | Mexique | Colombie | Part du Brésil (calcul) | Source |
|---|---|---|---|---|---|---|
| 31/12/2023 | 93,9 M (+19,3 M sur un an) | 87,8 M (53 % des adultes) | 5,2 M | 0,8 M | 94 % | communiqué T4 2023, https://international.nubank.com.br/company/nu-holdings-ltd-reports-fourth-quarter-and-full-year-2023-financial-results/ (22/02/2024) |
| 31/12/2024 | 114,2 M (+20,4 M) | ≈ 101,7 M (calcul) | 10 M | 2,5 M | 89 % | communiqué T4 2024, https://international.nubank.com.br/company/nu-holdings-ltd-reports-fourth-quarter-and-full-year-2024-financial-results/ (20/02/2025) |
| 31/12/2025 | 131 M (+17 M) | 113 M (62 % des adultes) | 14 M (15 % des adultes) | 4 M (11 % des adultes) | 86 % | BusinessWire, https://www.businesswire.com/news/home/20260225967630/en/ (25/02/2026) ; Globe and Mail |
| 30/06/2026 | 138,9 M (+13 %) | ≈ 118 M | 15,8 M | 5 M | 85 % | communiqué T2 2026 |

Lecture. Les ajouts nets ralentissent au Brésil parce que Nu approche du plafond : 62 % des adultes. Le Mexique et la Colombie prennent le relais : ils font 15 % des clients mais fournissent une part croissante des nouveaux. Nu est la plus grande institution financière privée du Brésil en nombre de clients selon la banque centrale (Nubank, https://nu.com/en/newsroom/company/nubank-reaches-more-than-112-million-customers-and-becomes-the-largest-private-financial-institution-in-brazil-according-to-the-central-bank).

### 3.2 Combien ils rapportent, combien ils coûtent

| Indicateur | T4 2023 | T4 2024 | T4 2025 | T2 2026 | Source |
|---|---|---|---|---|---|
| Taux d'activité | 83,1 % | n.d. | n.d. | 83,5 % (Brésil > 86 %) | communiqués T4 2023 et T2 2026 |
| ARPAC (revenu mensuel par client actif) | 10,6 $ | 10,7 $ (cohortes mûres 25 $) | 15,0 $ (+27 %) | 17,1 $ | communiqués ; Investing.com, https://www.investing.com/news/company-news/nu-holdings-q4-2025-slides-revenue-surges-45-efficiency-hits-record-20-93CH-4526260 |
| Coût de service mensuel par client actif | 0,9 $ | 0,8 $ (ajusté) | 0,8 $ | n.d. | communiqués T4 2023, T4 2024, T4 2025 |
| Ratio ARPAC / coût (calcul) | 11,8 | 13,4 | 18,8 | 21 (sur 0,8 $) | calcul |
| Ratio d'efficacité | n.d. | n.d. | 19,9 % | 19,5 % | communiqués |

L'ARPAC a stagné en 2024 (effet de change et dilution par les nouveaux clients mexicains et colombiens, à faible revenu initial) puis a bondi en 2025 et 2026. Calcul : +61 % entre fin 2023 et mi-2026. Les 116 millions de clients actifs du T2 2026 (calcul : 83,5 % de 138,9 M) à 17,1 $ par mois font environ 23,8 Md$ de revenus annualisés (calcul), à comparer aux 16,3 Md$ de 2025.

### 3.3 Revenus et résultat par client

| Année | Revenus | Résultat net | Revenus par client (calcul) | Résultat net par client (calcul) | Source |
|---|---|---|---|---|---|
| 2023 | plus de 8 Md$ | 1,0 Md$ | 85 $ | 11 $ | communiqué T4 2023 |
| 2024 | ≈ 11,2 Md$ (calcul : 16,3 / 1,45) | ≈ 2,0 Md$ | 101 $ | 18 $ | communiqué T4 2024 |
| 2025 | 16,3 Md$ (+45 %) | 2,9 Md$ | 124 $ | 22 $ | BusinessWire, 25/02/2026 |
| T2 2026 | 5,9 Md$ bruts, 4,1 Md$ nets | 1,06 Md$ (+49 %) | — | — | communiqué T2 2026 |

Note : la croissance des revenus bruts du T2 2026 est donnée à +39 % dans `NU.md` et à +56 % par Quartr ; les deux bases diffèrent (change constant ou publié). Les revenus 2025 sont de 16,3 Md$ dans le communiqué et de 15,8 Md$ dans le 20-F (définitions différentes). Je garde les chiffres des communiqués.

Le résultat net par client a doublé en deux ans (calcul : 11 → 22 $). C'est le levier opérationnel : le coût de service est fixe à 0,8 $, le revenu monte.

### 3.4 Ce que les clients confient et empruntent

| Date | Dépôts | Crédit | Dépôts par client (calcul) | Crédit par client (calcul) | Prêts / dépôts (calcul) | Source |
|---|---|---|---|---|---|---|
| 31/12/2023 | 23,7 Md$ | 18,2 Md$ (+49 % FXN) | 252 $ | 194 $ | 77 % | communiqué T4 2023 |
| 31/12/2024 | 28,9 Md$ (+55 % FXN) | 20,7 Md$ (+45 %) | 253 $ | 181 $ | 72 % | communiqué T4 2024 |
| 31/12/2025 | 41,9 Md$ (+29 %) | 32,7 Md$ (+40 %) | 320 $ | 250 $ | 78 % | Techleap, https://finder.techleap.nl/news/feed/nu-holdings-posts-895m-net-income-in-q4-with-33-return-on-equity |
| 30/06/2026 | 45,3 Md$ (+18 %) | 39,4 Md$ (+37 %) | 326 $ | 284 $ | 87 % | communiqué T2 2026 |

Par pays au 30/06/2026 : dépôts Brésil 36,4 Md$ (80 %), Mexique 5,7 Md$ (13 %), Colombie 3,3 Md$ (7 %) (`NU.md`, section 1 ; calculs). Calcul par client : 308 $ au Brésil, 361 $ au Mexique, 660 $ en Colombie. Les nouveaux pays attirent d'abord l'épargne (taux rémunérateurs), le crédit vient ensuite : le ratio prêts/dépôts n'est que de 35 % au Mexique (`NU.md`, section 4). Les dépôts mexicains ont été multipliés par 5,4 en 2023-2024 (438 %, communiqué T4 2024).

### 3.5 Ce qu'ils empruntent, et comment ils remboursent

| Portefeuille au 30/06/2026 | Montant | Part (calcul) | Croissance annuelle | Source |
|---|---|---|---|---|
| Cartes de crédit | 26,0 Md$ | 66 % | +35 % | Rio Times, https://www.riotimesonline.com/nu-holdings-billion-quarterly-profit-2026/ |
| Prêts non garantis | 10,3 Md$ | 26 % | +45 % | même source |
| Prêts garantis (FGTS, consignado) | 3,1 Md$ | 8 % | +30 % | même source |

Qualité : créances douteuses 15-90 jours 4,8 % (−16 pb), plus de 90 jours 6,9 % (+35 pb) ; marge d'intérêt ajustée du risque 12,4 % contre 9,9 % un an plus tôt (communiqué T2 2026). Une panne du système INSS a fait chuter de 50 % l'origination de prêts sur pension publique au T2 2026 (Stock Taper, https://www.stocktaper.com/earningsCallSummary/NU/2026/Q2). Le directeur financier : « cette primauté auprès du client n'est pas seulement un avantage de croissance et de revenus, c'est aussi un avantage de crédit » (`NU.md`, section 3).

### 3.6 Face aux concurrents

| Concurrent | Clients | Point fort | Source |
|---|---|---|---|
| Mercado Pago | 78 M d'utilisateurs mensuels actifs, crédit 12,5 Md$ (+90 %) | commerce et paiement, 57 Md R$ d'investissements au Brésil en 2026 | `NU.md`, section 4 |
| PicPay | 66 M de clients enregistrés, IPO Nasdaq 29/01/2026 (434 M$) | paiements | `NU.md`, section 4 ; F-1, https://www.sec.gov/Archives/edgar/data/1841644/000121390026005383/ea0201690-19.htm |
| iti (Itaú) | plus de 25 M (2025) | adossé à la première banque privée | PDP Spectra, https://pdpspectra.com/blog/brazil-fintech-nubank-ecosystem-2026 |
| PagBank | 30 M | PME et paiements | Future Nexus, https://www.heyfuturenexus.com/brazils-pagbank-hits-30m-clients-claims-a-spot-among-latams-largest-neobanks/ |
| Cinq grandes banques | n.d. | environ 70 % du profit du secteur | PDP Spectra |

Nu a plus de clients que tous ses rivaux numériques, mais les cinq grandes banques gardent 70 % du profit du secteur. La bataille se joue sur le compte principal : Nu dit être la première institution principale dans 17 États, pour environ 30 % de la population (NPS Prism, T4 2025, via Nubank, https://international.nubank.com.br/company/data-nubank-nubank-leads-as-brazilians-primary-financial-institution/), et 60 % de ses utilisateurs la considèrent comme banque principale (DataNubank, 07/2026, https://international.nubank.com.br/wp-content/uploads/2026/07/DataNubank-8_2026_Nubanks-presence-and-impact-across-Brazil.pdf).

---

## 4. À quoi s'attendre pour les années à venir

### 4.1 Ce que dit Nu

Nu ne donne pas de guidance chiffrée. Indications :

| Sujet | Indication | Source |
|---|---|---|
| Efficacité | ratio autour de 20 % en moyenne sur 2026 ; agents d'IA sur plus de 60 % des conversations de support au Brésil ; effectifs proches de 10 400 | `NU.md`, section 2 |
| Mexique | licence bancaire CNBV (10/07/2026), opérations bancaires depuis le 06/08/2026, 4,2 Md$ d'investissement d'ici 2030 ; « Mexico is Brazil's playbook, running faster » (Vélez, 13/08/2026) | Mexico Business News, https://mexicobusiness.news/finance/news/nu-mexico-launch-commercial-banking-operations-aug-6 ; Crowdfund Insider |
| Colombie | plus de 473 Md COP (environ 130 M$) d'investissement annoncés pour 2026 ; approbations de cartes triplées | Nubank (section 2) ; BusinessWire, 25/02/2026 |
| États-Unis | approbation conditionnelle OCC (29/01/2026) pour Nubank N.A. ; capitaliser sous 12 mois, ouvrir sous 18 mois ; approbations FDIC et Fed en attente | PYMNTS, https://www.pymnts.com/bank-regulation/2026/nu-wins-conditional-approval-for-us-national-bank-charter/ |
| Capital | premier rachat d'actions, jusqu'à 1 Md$ sur douze mois depuis le 04/06/2026 ; 500 M$ exécutés au 30/06/2026 | `NU.md`, section 2 |
| Rendez-vous | T3 2026 le 12/11/2026 ; premier Investor Day le 08/12/2026 à New York | `NU.md`, section 2 |

Consensus BPA ajusté : 0,864 $ (2026), 1,166 $ (2027), 1,41 $ (2028) selon Zacks et StockAnalysis au 30/09/2026 (`data/data.csv`). Au cours de 12,66 $ : 14,7 fois 2026, 10,9 fois 2027, 9,0 fois 2028 (calcul). Objectif moyen 14,98 $, Goldman Sachs à 21 $ (Tickflow, https://www.tickflow.io/stock/NU/forecast) ; Itaú BBA abaissé à 18 $ le 16/09/2026 (`NU.md`).

### 4.2 Ce qui soutient la clientèle

- **Le Brésil n'est pas fini.** 38 % des adultes ne sont pas clients, et surtout la montée en gamme : les cohortes mûres sont à 25 $ d'ARPAC contre 17,1 $ en moyenne. Si la moyenne rejoint les cohortes mûres, le revenu par client monte encore de 46 % sans un seul client de plus (calcul).
- **Le Mexique rentable.** 15,8 millions de clients, licence bancaire, point mort atteint, ratio prêts/dépôts à 35 % : la hausse du crédit est devant.
- **Les entreprises.** 6 millions de CNPJ, 2 millions de cartes : un client sur trois seulement a une carte.
- **La baisse de la Selic.** 13,75 % le 16/09/2026 après cinq baisses depuis 15 % (Rio Times, https://www.riotimesonline.com/brazil-economy-2026-state-of/). Taux réel encore proche de 9,5 %. Une baisse réduit le coût du crédit des clients et le risque de défaut.
- **Les nouveaux revenus.** NuCel (1 M), voyages, compte global, investissements : chacun ajoute à l'ARPAC sans coût d'acquisition.

### 4.3 Ce qui menace la clientèle

1. **Le crédit à la consommation brésilien.** 66 % du portefeuille en cartes, créances à plus de 90 jours à 6,9 % et en hausse. Le programme Desenrola 3.0 (25/09/2026) peut imposer des renégociations (`NU.md`, section 7). Taux réel à 9,5 % : les ménages restent sous pression.
2. **La fiscalité.** CSLL à 20 % en 2028 dans l'hypothèse basse du modèle (`data/hypotheses.csv`).
3. **La concurrence sur le compte principal.** Mercado Pago, PicPay, iti, et les grandes banques qui regagnent des parts sur certains segments (PDP Spectra). Pix et l'open finance réduisent le coût de changement.
4. **La dilution des nouveaux pays.** Chaque Mexicain ou Colombien rapporte d'abord moins qu'un Brésilien et coûte des dépôts chers (660 $ par client en Colombie, calcul). La rentabilité du Mexique date d'un trimestre.
5. **L'exécution hors Amérique latine.** États-Unis : marché saturé de néobanques, approbations FDIC et Fed en attente. Royaume-Uni : rumeur Monzo à 8-10 Md£ démentie, mais l'épisode a coûté 10 % au titre le 28/09/2026 (`MONZO.md`).
6. **Le change.** 91 % des revenus en réaux ; une dépréciation du réal réduit mécaniquement l'ARPAC et le BPA en dollars.

### 4.4 Les trois scénarios pour un actionnaire

| Scénario | Hypothèse | Cohérence avec `data/hypotheses.csv` (NU) |
|---|---|---|
| Pessimiste | cycle de crédit brésilien, CSLL à 20 %, ARPAC plafonne, réal faible ; BPA +8 % par an | hypothèse basse : 8 % |
| Central | Brésil monte en gamme vers 25 $ d'ARPAC, Mexique rentable, rachats compensent les RSU ; BPA +20 % par an | hypothèse centrale : 20 % |
| Optimiste | Mexique et Colombie répliquent le Brésil, États-Unis lancés, ARPAC groupe à 25 $ ; BPA +28 % par an | hypothèse haute : 28 % |

Le consensus (BPA +35 % en 2027, +21 % en 2028, calcul sur `data.csv`) est au-dessus de l'hypothèse centrale. Le plafond de P/E de sortie à 15 reflète le statut de banque émergente. Pas de modification.

---

## 5. Ce que ça change pour le portefeuille

- **Nu (20 %)** est la plus grosse ligne et la seule banque. Sa clientèle est la plus large du portefeuille (139 millions) et la moins concentrée : le risque n'est pas un client, c'est un pays (91 % des revenus au Brésil) et un produit (66 % du crédit en cartes).
- **Le signal à suivre** : l'écart entre l'ARPAC moyen (17,1 $) et celui des cohortes mûres (25 $). S'il se referme, le scénario central se réalise sans croissance du nombre de clients. Et les créances à plus de 90 jours : au-dessus de 7,5 %, le scénario pessimiste gagne.
- **Le Mexique** est l'option gratuite : 11 % des clients, 7 % des revenus, licence bancaire depuis août. Les résultats du T3 (12/11/2026) donneront le premier trimestre complet en tant que banque.
- **L'Investor Day du 08/12/2026** sera la première fois que Nu donne un cadre chiffré à moyen terme. C'est le rendez-vous pour réviser les hypothèses du modèle.

Points de contrôle : résultats du T3 2026 le 12/11/2026 ; Investor Day le 08/12/2026 ; décision du Copom (prochaine réunion n.d.) ; 20-F 2026 au printemps 2027 pour les revenus par pays.

---

## 6. Sources

1. Nu, communiqué T2 2026 (13/08/2026) : https://international.nubank.com.br/company/nu-holdings-ltd-reports-second-quarter-2026-financial-results/
2. BusinessWire, T2 2026 : https://www.businesswire.com/news/home/20260813187996/en/Nu-Holdings-Ltd.-Reports-Second-Quarter-2026-Financial-Results
3. Quartr, résumé T2 2026 : https://quartr.com/events/nu-holdings-ltd-nu-q2-2026_oja0su5j
4. Nu, 6-K T4 2025 (25/02/2026) : https://www.sec.gov/Archives/edgar/data/1691493/000129281426000501/nu20260225_6k.htm
5. BusinessWire, T4 2025 : https://www.businesswire.com/news/home/20260225967630/en/
6. Investing.com, slides T4 2025 : https://www.investing.com/news/company-news/nu-holdings-q4-2025-slides-revenue-surges-45-efficiency-hits-record-20-93CH-4526260
7. Globe and Mail, T4 2025 : https://www.theglobeandmail.com/investing/markets/stocks/NU/pressreleases/455186/nu-holdings-q4-2025-results-showcase-profit-surge-and-latin-american-scale-up/
8. Techleap, T4 2025 : https://finder.techleap.nl/news/feed/nu-holdings-posts-895m-net-income-in-q4-with-33-return-on-equity
9. Nu, 20-F 2025 : https://www.sec.gov/Archives/edgar/data/1691493/000129281426002166/nuform20f_2025.htm
10. Nu, communiqué T4 2024 (20/02/2025) : https://international.nubank.com.br/company/nu-holdings-ltd-reports-fourth-quarter-and-full-year-2024-financial-results/
11. Nu, communiqué T4 2023 (22/02/2024) : https://international.nubank.com.br/company/nu-holdings-ltd-reports-fourth-quarter-and-full-year-2023-financial-results/
12. Nu, 20-F 2023 : https://www.sec.gov/Archives/edgar/data/1691493/000129281424001464/nuform20f_2023.htm
13. Rio Times, portefeuille T2 2026 : https://www.riotimesonline.com/nu-holdings-billion-quarterly-profit-2026/
14. Stock Taper, appel T2 2026 : https://www.stocktaper.com/earningsCallSummary/NU/2026/Q2
15. Nubank, Nu Colombia 5 M : https://international.nubank.com.br/company/nu-colombia-turns-five-with-5-million-customers-and-reinforces-its-long-term-commitment-to-the-country/
16. Nubank, Nu Empresas 6 M (05/2026) : https://international.nubank.com.br/company/nu-empresas-reaches-6-million-customers-and-becomes-the-largest-financial-institution-in-brazil-in-number-of-cnpjs/
17. Nubank, Ultravioleta : https://international.nubank.com.br/consumers/high-income-focused-nubank-expands-benefits-for-ultravioleta-customers/
18. Nubank, NuCel 1 M (06/2026) : https://international.nubank.com.br/consumers/nucel-reaches-1-million-customers-and-consolidates-nubank-as-a-platform-beyond-finance/
19. Nubank, première institution privée du Brésil : https://nu.com/en/newsroom/company/nubank-reaches-more-than-112-million-customers-and-becomes-the-largest-private-financial-institution-in-brazil-according-to-the-central-bank
20. Nubank, institution principale (NPS Prism) : https://international.nubank.com.br/company/data-nubank-nubank-leads-as-brazilians-primary-financial-institution/
21. DataNubank 8 (07/2026) : https://international.nubank.com.br/wp-content/uploads/2026/07/DataNubank-8_2026_Nubanks-presence-and-impact-across-Brazil.pdf
22. Crowdfund Insider, licence Mexique (07/2026) : https://www.crowdfundinsider.com/2026/07/291252-nubank-subsidiary-nu-mexico-obtains-authorization-to-start-operations-as-licensed-bank/
23. Mexico Business News, lancement bancaire 06/08/2026 : https://mexicobusiness.news/finance/news/nu-mexico-launch-commercial-banking-operations-aug-6
24. PYMNTS, approbation OCC (29/01/2026) : https://www.pymnts.com/bank-regulation/2026/nu-wins-conditional-approval-for-us-national-bank-charter/
25. Nu, 6-K OCC (28/01/2026) : https://www.sec.gov/Archives/edgar/data/1691493/000129281426000201/nu20260128_6k.htm
26. PDP Spectra, écosystème fintech brésilien 2026 : https://pdpspectra.com/blog/brazil-fintech-nubank-ecosystem-2026
27. PicPay, F-1/A : https://www.sec.gov/Archives/edgar/data/1841644/000121390026005383/ea0201690-19.htm
28. Future Nexus, PagBank 30 M : https://www.heyfuturenexus.com/brazils-pagbank-hits-30m-clients-claims-a-spot-among-latams-largest-neobanks/
29. Rio Times, économie brésilienne 2026 (Selic) : https://www.riotimesonline.com/brazil-economy-2026-state-of/
30. MNI, Copom 25/09 : https://www.mnimarkets.com/articles/mni-bcb-review-sep-25-on-hold-hawkish-guidance-maintained-1758193001761
31. Tickflow, objectifs de cours : https://www.tickflow.io/stock/NU/forecast
32. Axios, rumeur Monzo (28/09/2026) : https://www.axios.com/2026/09/28/nu-monzo-acquisition-talks
33. Google Finance, cours NU au 30/09/2026 ; Zacks et StockAnalysis, consensus BPA (`portefeuille-peg-5-valeurs/data/data.csv`) ; deep dive `research/deepdives/NU.md` (01/10/2026) ; dossier `research/monzo/MONZO.md` (01/10/2026).
