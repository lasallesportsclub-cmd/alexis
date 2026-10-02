# Uber : qui sont ses clients, comment ils ont changé en deux ans, et à quoi s'attendre

Dossier du 02/10/2026, complément du deep dive `UBER.md` (01/10/2026). Cours 68,51 $ (Google Finance, clôture 30/09/2026), capitalisation 141,7 Md$. Position en portefeuille : 15 % (`portefeuille-peg-5-valeurs/data/portfolio.csv`).

Règles : aucun chiffre inventé. Chaque chiffre porte une source et une date. Donnée introuvable = « n.d. ». Les calculs maison sont signalés « calcul ». Exercice Uber = année civile. « GB » = gross bookings, le volume d'affaires brut encaissé pour le compte des chauffeurs, coursiers et commerçants ; le chiffre d'affaires d'Uber n'en est qu'une fraction (environ 27 %).

Différence avec Nvidia et TSMC. Uber n'a pas de « gros client » au sens d'un acheteur à 10 % du chiffre d'affaires : aucun client ne dépasse ce seuil dans le 10-K. Ses clients sont cinq populations : les consommateurs (208 millions), les commerçants (plus de 1,5 million), les annonceurs, les entreprises (Uber for Business) et les chargeurs du fret. Ses « gros partenaires », qui sont aussi ses concurrents, sont les sociétés de robotaxis. Ce dossier traite les deux.

---

## 1. Résumé en dix lignes

- Uber a 208 millions de consommateurs actifs mensuels (T2 2026), contre 150 millions fin 2023 : +39 % en deux ans et demi.
- Le volume d'affaires brut est passé de 137,8 Md$ (2023) à 193,5 Md$ (2025), soit 1,4 fois, et 58,0 Md$ sur le seul T2 2026 (+24 %).
- Le client moyen dépense davantage : 919 $ par an en 2023, 958 $ en 2025, environ 1 115 $ en rythme annualisé au T2 2026 (calculs).
- Le client le plus rentable est l'abonné Uber One : 50 millions de membres au T1 2026 (30 millions fin 2024), 24 % des consommateurs, 50 % des GB mobilité et livraison.
- La livraison rattrape la mobilité : 47 % des GB au T2 2026 contre 50 % pour la mobilité ; elle croît plus vite (+25 % contre +20 % à change constant).
- Les annonceurs sont le client qui monte : 1,5 Md$ de revenus annualisés au T1 2025, en croissance de plus de 60 %.
- Le fret (Uber Freight) est le seul segment déficitaire : 1,58 Md$ de revenus au T2 2026, résultat opérationnel −24 M$.
- Les États-Unis font encore la moitié du chiffre d'affaires (50,9 % avec le Canada en 2025), mais 60 % des GB mobilité sont hors États-Unis.
- Les partenaires robotaxis sont passés de quelques pilotes à plus de 30 accords, 7 villes actives, 420 M$ de GB annualisés : 0,18 % du volume (calcul). Waymo, le plus gros, se retire de Phoenix et quittera Austin et Atlanta en 2028.
- Pour l'avenir : cadre 2024-2026 « mid-to-high teens » de croissance des GB tenu, guidance T3 à 59,25 Md$ au milieu, OPA de 14,8 Md$ sur Delivery Hero, 3 300 licenciements en septembre 2026, action à 20,4 fois le BPA 2026 (calcul).

---

## 2. Les cinq clientèles d'Uber

| Clientèle | Ce qu'elle paie | Taille | Source |
|---|---|---|---|
| Consommateurs | le prix des courses et livraisons ; Uber garde environ 27 % en revenus | 208 M actifs mensuels (T2 2026), 3,9 Md de trajets au trimestre | 8-K T2 2026, https://www.sec.gov/Archives/edgar/data/0001543151/000154315126000027/uberq226earningspressrelea.htm (05/08/2026) |
| Abonnés Uber One | abonnement mensuel ou annuel ; livraison offerte, remises | 50 M de membres payants (T1 2026) ; 50 % des GB mobilité et livraison | prepared remarks T1 2026, https://s23.q4cdn.com/407969754/files/doc_earnings/2026/q1/transcript/Uber-Q1-26-Prepared-Remarks.pdf (06/05/2026) |
| Commerçants et restaurants | commission sur les commandes Uber Eats, publicité | plus de 1,5 M de partenaires dans plus de 11 000 villes | Uber Eats merchants, https://merchants.ubereats.com/ca/en/resources/community/merchant-impact (consulté 02/10/2026) |
| Annonceurs | publicités dans l'application (Journey Ads, sponsored listings) | 1,5 Md$ de revenus annualisés, +60 % (T1 2025) ; proche de 2 % des GB livraison | Nasdaq, https://www.nasdaq.com/articles/uber-ads-hidden-gem-powering-ubers-next-growth-engine (2025) |
| Entreprises (Uber for Business, Uber Health) | déplacements et repas professionnels facturés à l'employeur | croît « plus de deux fois plus vite que la mobilité » ; GB n.d. | prepared remarks T4 2025, https://s23.q4cdn.com/407969754/files/doc_earnings/2025/q4/transcript/Uber-Q4-25-Prepared-Remarks.pdf (04/02/2026) |
| Chargeurs (Uber Freight) | courtage et transport géré | 1,58 Md$ de revenus au T2 2026 (+25 %), résultat opérationnel −24 M$ | FreightWaves, https://www.freightwaves.com/news/after-a-long-gap-uber-freights-revenue-turns-higher-from-year-earlier ; EdgeX, https://pro.edgex.exchange/en-US/news/article/uber-freight-q2-2026-revenue-surges |

De l'autre côté de la place de marché : 10 millions de chauffeurs et coursiers actifs fin 2025 (10-K 2025, https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm), soit environ 21 consommateurs par chauffeur (calcul).

Aucun client ne pèse 10 % du chiffre d'affaires : le 10-K ne mentionne aucune concentration. C'est l'inverse de Nvidia (trois clients à 44 %) et de TSMC (deux clients à 36 %).

---

## 3. L'évolution sur deux ans

### 3.1 Volume, clients, fréquence

| Année | GB | Chiffre d'affaires | Consommateurs actifs (T4) | Trajets | GB par consommateur (calcul) | Trajets par consommateur et par mois (calcul) | Source |
|---|---|---|---|---|---|---|---|
| 2023 | 137,8 Md$ (+19,5 %) | 37,3 Md$ (+17 %) | 150 M | 9,4 Md (+24 %) | 919 $ | 5,2 | communiqué T4 2023, https://investor.uber.com/news-events/news/press-release-details/2024/Uber-Announces-Results-for-Fourth-Quarter-and-Full-Year-2023/default.aspx (07/02/2024) |
| 2024 | 162,8 Md$ (+18 %) | 44,0 Md$ (+18 %) | 171 M (+14 %) | 11,3 Md | 952 $ | 5,5 | communiqué T4 2024, https://investor.uber.com/news-events/news/press-release-details/2025/Uber-Announces-Results-for-Fourth-Quarter-and-Full-Year-2024/default.aspx (05/02/2025) |
| 2025 | 193,5 Md$ (+19 %) | 52,0 Md$ (+18 %) | 202 M (+18 %) | 13,6 Md (+20 %) | 958 $ | 5,6 | 10-K 2025 ; BusinessWire, https://www.businesswire.com/news/home/20260204947622/en/ (04/02/2026) |
| T2 2026 | 58,0 Md$ (+24 %) | 14,2 Md$ (+12 %) | 208 M (+16 %) | 3,9 Md (+18 %) | ≈ 1 115 $ annualisé | n.d. | 8-K T2 2026 (05/08/2026) |

Lecture. En deux ans, le nombre de clients a crû de 35 %, les trajets de 45 %, le volume de 40 % (calculs). La croissance vient d'abord de nouveaux clients, ensuite de la fréquence. Dara Khosrowshahi : « nous avons ajouté plus de nouveaux utilisateurs sur les douze derniers mois que sur toute période des cinq dernières années » (8-K T2 2026). Le taux de prise (revenus sur GB) glisse de 27,1 % (2023) à 24,5 % au T2 2026 (calcul) : des changements de modèle d'affaires font sortir certains flux du chiffre d'affaires sans toucher aux GB.

### 3.2 Par segment : la livraison rattrape la mobilité

| Période | Mobilité | Livraison | Fret | Source |
|---|---|---|---|---|
| Chiffre d'affaires 2025 | 29,7 Md$ (57 %) | 17,3 Md$ (33 %) | 5,1 Md$ (10 %) | FourWeekMBA d'après le 10-K 2025, https://fourweekmba.com/uber-revenue-breakdown/ |
| GB T4 2025 | 27,4 Md$ | 25,4 Md$ | 1,3 Md$ | BusinessWire, 04/02/2026 |
| GB T2 2026 | 28,98 Md$ (+20 % à change constant), 50 % du total | 27,46 Md$ (+25 %), 47 % | 1,57 Md$ (+25 %), 2,7 % | prepared remarks T2 2026, https://s23.q4cdn.com/407969754/files/doc_earnings/2026/q2/transcript/Uber-Q2-26-Prepared-Remarks.pdf |
| Résultat opérationnel segment T2 2026 | 2 215 M$ | 1 055 M$ | −24 M$ | deep dive `UBER.md`, section 2 ; EdgeX |

Hors restaurants, la livraison d'épicerie et de détail visait 12,5 Md$ de GB annualisés fin 2025, contre 10 Md$ en mai 2025 (Transport Topics, https://www.ttnews.com/articles/uber-leaps-grocery-retail).

### 3.3 Par géographie : la moitié aux États-Unis

| Année | États-Unis | Royaume-Uni | Reste du monde | Source |
|---|---|---|---|---|
| 2023 | 18 620 M$ (49,9 %, calcul) | 6 522 M$ | 12 139 M$ | 10-K 2023, https://www.sec.gov/Archives/edgar/data/1543151/000154315124000012/uber-20231231.htm |
| 2024 | 21 429 M$ (48,7 %) | 8 373 M$ (19,0 %) | 14 176 M$ | 10-K 2024, https://www.sec.gov/Archives/edgar/data/1543151/000154315125000008/uber-20241231.htm |
| 2025 (par région) | États-Unis et Canada 26 469 M$ (50,9 %) | EMEA 16 364 M$ (31,2 %) | Asie-Pacifique 5 857 M$, Amérique latine 3 327 M$ | 10-K 2025 via StockAnalysis, repris dans `UBER.md` |

Attention : les bases changent (pays en 2023-2024, régions en 2025). En volume, 60 % des GB mobilité sont hors États-Unis (10-K 2025 via FourWeekMBA). Les États-Unis pèsent plus en revenus qu'en volume parce que le panier moyen y est plus élevé.

### 3.4 Les clients qui fidélisent : abonnés et annonceurs

| Indicateur | 2023 | Fin 2024 | 2025 | 2026 | Source |
|---|---|---|---|---|---|
| Membres Uber One | n.d. | 30 M (+60 %) | 36 M (T2 2025) | 50 M (T1 2026) | Motley Fool, https://www.fool.com/investing/2025/09/07/where-will-uber-technologies-stock-be-in-1-year ; prepared remarks T1 2026 |
| Part des consommateurs abonnés (calcul) | n.d. | 18 % | n.d. | 24 % | calcul sur 171 M et 208 M |
| Part des GB mobilité et livraison des membres | n.d. | n.d. | plus de 70 % des GB livraison (T1 2026) | 50 % des GB mobilité et livraison | prepared remarks T1 2026 |
| Publicité, revenus annualisés | 0,5 Md$ (début 2023) | plus de 1 Md$ | 1,5 Md$ (T1 2025, +60 %) | n.d. | Nasdaq (section 2) |

Calcul : 1,5 Md$ de publicité font 2,9 % du chiffre d'affaires 2025 et 0,8 % des GB. C'est petit en volume, mais c'est du revenu à marge quasi totale.

### 3.5 Les parts de marché

| Marché | Uber | Principal rival | Source |
|---|---|---|---|
| VTC États-Unis (ventes) | 71 % | Lyft 29 % | Apurple, https://www.apurple.co/?p=986 (2026) ; autre estimation 55 % contre 31 %, Citizen Daily Post |
| VTC New York (mai 2026) | 69 % | n.d. | Citizen Daily Post, https://www.citizendailypost.com/faq/who-has-bigger-market-share-uber-or-lyft/ |
| Livraison de repas États-Unis | Uber Eats 23 % | DoorDash 66-67 %, Grubhub 8 % | WMtips, https://www.wmtips.com/technologies/food-delivery/country/us (2026) |

Sources de qualité moyenne pour les parts de marché ; ordres de grandeur. Le point clé : Uber domine le VTC américain mais reste un distant numéro deux en livraison aux États-Unis. D'où l'offre sur Delivery Hero (section 5), qui joue l'Europe, l'Asie et le Moyen-Orient plutôt que les États-Unis.

---

## 4. Les gros partenaires : les robotaxis, clients et concurrents à la fois

### 4.1 Ce qui existe

| Partenaire | Accord | Statut | Source |
|---|---|---|---|
| Waymo (Alphabet) | Phoenix, Austin, Atlanta via l'application Uber | pilote de Phoenix arrêté le 29/06/2026 ; Waymo a notifié son entrée en propre à Austin et Atlanta en janvier 2028 ; contrat jusqu'en mai 2028 ; Uber parle de « unsustainable financial terms » | Bloomberg Law, https://news.bloomberglaw.com/private-equity/waymo-plans-end-of-uber-robotaxi-tie-up-stepping-up-rivalry-1 (2026) ; `UBER.md`, section 4 |
| Nuro + Lucid | 20 000 robotaxis ou plus, « dizaines de marchés » ; lancement Bay Area fin 2026, Hertz pour les flottes | annoncé, lancement en cours | Nuro, https://www.nuro.ai/nuro-lucid-uber-robotaxi ; Uber IR, https://investor.uber.com/news-events/news/press-release-details/2026/Hertz-and-Uber-Partner-to-Power-Autonomous-Robotaxi-and-Driver-Led-Fleet-Operations/default.aspx |
| WeRide | Abou Dabi, Dubaï (sans opérateur à bord), Riyad, Madrid | commercial à Dubaï | Uber IR, https://investor.uber.com/news-events/news/press-release-details/2026/WeRide-and-Uber-Launch-Fully-Driverless-Robotaxi-Fare-Charging-Operations-in-Dubai-Accelerating-Autonomous-Mobility-in-the-Middle-East-2026-NSiF0EFKhd/default.aspx |
| Wayve + Nissan, Wayve + Stellantis | Tokyo fin 2026 (Nissan Leaf), Londres, douze villes | pilotes | Uber IR, https://investor.uber.com/news-events/news/press-release-details/2026/Wayve-Uber-and-Nissan-Announce-Collaboration-on-Robotaxis/default.aspx ; Stellantis, 06/2026, https://www.stellantis.com/en/news/press-releases/2026/june/stellantis-wayve-and-uber-partner-to-scale-robotaxis-globally |
| Zoox (Amazon) | Las Vegas 2026, Los Angeles 2027 | accord 03/2026 | TechCrunch, 01/08/2026, https://techcrunch.com/2026/08/01/ubers-autonomous-vehicle-deal-tracker/ |
| Baidu Apollo Go | tests à Londres prévus S1 2026 | non commencés en juin 2026 | TechCrunch |
| Nvidia + Stellantis | au moins 5 000 véhicules, cible 100 000 véhicules L4 à partir de 2027 | annoncé 28/10/2025 | `UBER.md`, section 4 |

Bilan au T2 2026 : plus de 30 partenaires (TechCrunch), 7 villes actives et 8 de plus prévues d'ici fin 2026, 420 M$ de GB annualisés en autonome, plus de 10 Md$ d'investissement prévus (DT Next d'après le 8-K T2 2026, https://www.dtnext.in/news/business/uber-building-infrastructure-to-commercialise-autonomous-mobility-at-global-scale-q2-earnings-report). Calcul : 420 M$ font 0,18 % des GB annualisés du T2 (232 Md$).

### 4.2 Ce qui menace

- **Waymo seul.** Plus de 400 000 trajets payants par semaine dans six métropoles, dix marchés visés, objectif 1 million de trajets par semaine fin 2026 (San Mateo Daily Journal, https://www.smdailyjournal.com/business/waymos-robotaxis-now-being-dispatched-in-10-major-u-s-markets-with-expansion-in-texas/article_09e1086a-fe59-5784-b47b-24d573000c3a.html). Calcul : 500 000 trajets par semaine font 26 millions par an, soit 0,19 % des 13,6 Md de trajets Uber de 2025. La menace est dans la trajectoire, pas dans le niveau.
- **Tesla.** Cybercab ouvert au public à Austin le 03/09/2026 ; le titre Uber a perdu 4 % le 08/09/2026 (`UBER.md`, section 4 ; Stockwatch, 03/09/2026, https://wwww.stockwatch.com/News/Item/Z-C!UBER-3860454/C/UBER).
- **Le pire cas chiffré.** Une analyse citée par Sherwood estime la baisse des profits d'Uber à « high-single to low-double digit » si la majorité de l'autonome se faisait sans Uber (Sherwood, https://www.sherwood.news/business/uber-and-lyft-shares-tap-the-brakes-on-a-potential-long-term-threat-from).

---

## 5. À quoi s'attendre pour les années à venir

### 5.1 Ce que dit Uber

| Horizon | Indication | Source |
|---|---|---|
| T3 2026 | GB 58,25 à 60,25 Md$ (+18 à 22 % à change constant), EBITDA ajusté 2,86 à 2,96 Md$, BPA non-GAAP 0,84 à 0,88 $ | 8-K T2 2026 (05/08/2026) |
| Cadre 2024-2026 | GB « mid-to-high teens » par an, EBITDA ajusté +30 à 40 % par an, conversion en FCF ≥ 90 % ; « tracking exactly » selon la direction au T3 2025 | TipRanks, https://www.tipranks.com/news/the-fly/uber-sees-three-year-gross-bookings-growth-in-mid-to-high-teens-cagr ; résumé T3 2025, https://transcripts.platformaeronaut.com/summaries/UBER-3Q25-AI-Summary |
| Delivery Hero | OPA à 41,50 € par action, 14,8 Md$, seuil 50 % plus une action ; Prosus (17 %) vend ; Uber détient déjà près de 37 % avec les dérivés ; 14 marchés cédés à SSW Partners pour 1,4 Md€ ; clôture attendue S2 2027 | WLRK, https://www.wlrk.com/transaction/uber-in-its-14-8-billion-voluntary-takeover-offer-for-all-outstanding-shares-of-delivery-hero/ ; Khaleej Times, https://www.khaleejtimes.com/business/uber-launches-15-billion-bid-for-delivery-hero-to-create-global-takeout-giant (16/07/2026) |
| Effectifs | 3 300 licenciements, 10 % des effectifs, septembre 2026 | Stockwatch, 03/09/2026 |
| Robotaxis | 15 villes fin 2026, plus de 10 Md$ investis, 100 000 véhicules L4 visés à partir de 2027 | section 4 |

Consensus BPA non-GAAP : 3,355 $ (2026), 4,591 $ (2027), 5,73 $ (2028) selon Zacks au 30/09/2026 (`data/data.csv`). Au cours de 68,51 $ : 20,4 fois 2026, 14,9 fois 2027, 12,0 fois 2028 (calcul). Objectif de cours moyen 110 $, fourchette 82 à 150 $ (Tickflow, https://tickflow.io/stock/UBER/forecast). Le titre perd 16,6 % depuis le 1er janvier 2026 (`UBER.md`).

Calcul maison : 14,8 Md$ pour Delivery Hero font 1,5 année de FCF (10 Md$ sur douze mois glissants). Le directeur financier a dit que les rachats reprendraient « dans des mois, pas des trimestres » (`UBER.md`, section 3).

### 5.2 Ce qui soutient la clientèle

- La base croît encore de 16 % par an et la meilleure cohorte de nouveaux clients depuis cinq ans arrive (8-K T2 2026).
- L'abonnement : 50 millions de membres, 24 % des clients, qui dépensent plus et partent moins.
- Les nouveaux verticaux : épicerie et détail (12,5 Md$ annualisés), publicité (1,5 Md$), Uber for Business (deux fois la croissance de la mobilité).
- L'international : 60 % des GB mobilité hors États-Unis ; Delivery Hero ajouterait l'Europe, l'Asie et le Moyen-Orient en livraison.
- Les robotaxis en tant que fournisseurs : chaque partenaire hors Waymo et Tesla a besoin de la demande d'Uber pour remplir ses véhicules.

### 5.3 Ce qui menace la clientèle

1. **Waymo et Tesla en direct.** Les deux acteurs les plus avancés veulent la relation client. Le contrat Waymo court jusqu'en mai 2028 ; après, Austin et Atlanta se font sans Uber.
2. **DoorDash aux États-Unis.** Uber Eats est à 23 % contre 66 % ; la croissance de la livraison d'Uber vient de l'international et de l'épicerie.
3. **Le Brésil et les prix.** Concurrence au Brésil et inquiétudes sur les marges citées à la publication du T2 2026 (StartupMap, https://startupmap.iamsterdam.com/news/feed/uber-q2-revenue-misses-at-14-19b-as-brazil-competition-and-margin-concerns-weigh-on-investors).
4. **Le droit du travail.** Directive européenne 2024/2831 sur le travail de plateforme, transposition avant le 02/12/2026 (`UBER.md`, section 5). Chiffre n.d.
5. **L'assurance.** 31 % du prix d'une course en Californie (`UBER.md`, section 4) ; provisions d'assurance 13,3 Md$ au 30/06/2026.
6. **Delivery Hero.** 14,8 Md$ de trésorerie engagés, dette de la cible, intégration de 2027 à 2029, risque antitrust.

### 5.4 Les trois scénarios pour un actionnaire

| Scénario | Hypothèse | Cohérence avec `data/hypotheses.csv` (UBER) |
|---|---|---|
| Pessimiste | Waymo et Tesla prennent les centres-villes américains, Delivery Hero absorbe le FCF, taux de prise en baisse ; BPA +5 % par an | hypothèse basse : 5 % |
| Central | GB « mid-to-high teens », levier opérationnel, rachats ; BPA +16 % par an | hypothèse centrale : 16 % |
| Optimiste | Uber devient la couche de demande de 100 000 robotaxis, l'abonnement dépasse 30 % des clients, publicité à 3 Md$ ; BPA +24 % par an | hypothèse haute : 24 % |

Pas de raison de modifier les hypothèses : le consensus Zacks (BPA +37 % en 2026 puis +25 % en 2027 et 2028, calcul) est au-dessus de l'hypothèse centrale, et le plafond de P/E de sortie à 22 reflète la désintermédiation non résolue.

---

## 6. Ce que ça change pour le portefeuille

- **Uber (15 %)** est la seule ligne du portefeuille sans client concentré : 208 millions de consommateurs, aucun à 10 %. Son risque n'est pas la perte d'un client, c'est la perte d'un rôle (l'intermédiaire) face à Waymo et Tesla.
- **Nvidia (15 %)** est partenaire d'Uber dans l'autonome (accord du 28/10/2025) : le scénario optimiste d'Uber est aussi un scénario de ventes de puces Nvidia aux flottes.
- **Le signal à suivre** : la part des GB réalisée par les membres Uber One et le nombre de villes robotaxis actives. Si la première monte et la seconde aussi, Uber garde le client. Si Waymo passe le million de trajets par semaine fin 2026 sans Uber, le scénario pessimiste gagne en probabilité.
- **Delivery Hero** : la période d'acceptation court jusqu'au 05/11/2026 (`UBER.md`). C'est l'événement qui décidera de la reprise des rachats.

Points de contrôle : résultats du T3 2026 le 03/11/2026 (date non confirmée par Uber), fin de l'offre Delivery Hero le 05/11/2026, résultats Lyft le 11/11/2026, bilan Waymo fin 2026 (objectif 1 million de trajets par semaine).

---

## 7. Sources

1. Uber, 8-K T2 2026 (05/08/2026) : https://www.sec.gov/Archives/edgar/data/0001543151/000154315126000027/uberq226earningspressrelea.htm
2. Uber, prepared remarks T2 2026 : https://s23.q4cdn.com/407969754/files/doc_earnings/2026/q2/transcript/Uber-Q2-26-Prepared-Remarks.pdf
3. Uber, 10-Q T2 2026 : https://www.sec.gov/Archives/edgar/data/0001543151/000154315126000032/uber-20260630.htm
4. Uber, prepared remarks T1 2026 (06/05/2026) : https://s23.q4cdn.com/407969754/files/doc_earnings/2026/q1/transcript/Uber-Q1-26-Prepared-Remarks.pdf
5. Uber, prepared remarks T4 2025 (04/02/2026) : https://s23.q4cdn.com/407969754/files/doc_earnings/2025/q4/transcript/Uber-Q4-25-Prepared-Remarks.pdf
6. Uber, 10-K 2025 : https://www.sec.gov/Archives/edgar/data/1543151/000154315126000015/uber-20251231.htm
7. Uber, 10-K 2024 : https://www.sec.gov/Archives/edgar/data/1543151/000154315125000008/uber-20241231.htm
8. Uber, 10-K 2023 : https://www.sec.gov/Archives/edgar/data/1543151/000154315124000012/uber-20231231.htm
9. Uber, résultats T4 2023 (07/02/2024) : https://investor.uber.com/news-events/news/press-release-details/2024/Uber-Announces-Results-for-Fourth-Quarter-and-Full-Year-2023/default.aspx
10. Uber, résultats T4 2024 (05/02/2025) : https://investor.uber.com/news-events/news/press-release-details/2025/Uber-Announces-Results-for-Fourth-Quarter-and-Full-Year-2024/default.aspx
11. BusinessWire, résultats T4 2025 (04/02/2026) : https://www.businesswire.com/news/home/20260204947622/en/
12. CNBC, T2 2026 : https://www.cnbc.com/2026/08/05/uber-stock-q2-2026-earnings.html
13. FourWeekMBA, répartition 2025 : https://fourweekmba.com/uber-revenue-breakdown/
14. Uber Eats, commerçants : https://merchants.ubereats.com/ca/en/resources/community/merchant-impact
15. Nasdaq, Uber Ads : https://www.nasdaq.com/articles/uber-ads-hidden-gem-powering-ubers-next-growth-engine
16. Motley Fool, Uber One (07/09/2025) : https://www.fool.com/investing/2025/09/07/where-will-uber-technologies-stock-be-in-1-year
17. Transport Topics, épicerie et détail : https://www.ttnews.com/articles/uber-leaps-grocery-retail
18. FreightWaves, Uber Freight : https://www.freightwaves.com/news/after-a-long-gap-uber-freights-revenue-turns-higher-from-year-earlier
19. EdgeX, Uber Freight T2 2026 : https://pro.edgex.exchange/en-US/news/article/uber-freight-q2-2026-revenue-surges
20. Apurple, parts VTC : https://www.apurple.co/?p=986
21. Citizen Daily Post, parts VTC : https://www.citizendailypost.com/faq/who-has-bigger-market-share-uber-or-lyft/
22. WMtips, parts livraison : https://www.wmtips.com/technologies/food-delivery/country/us
23. TechCrunch, suivi des accords autonomes (01/08/2026) : https://techcrunch.com/2026/08/01/ubers-autonomous-vehicle-deal-tracker/
24. Bloomberg Law, Waymo et Uber : https://news.bloomberglaw.com/private-equity/waymo-plans-end-of-uber-robotaxi-tie-up-stepping-up-rivalry-1
25. Nuro, Lucid et Uber : https://www.nuro.ai/nuro-lucid-uber-robotaxi
26. Uber IR, Hertz : https://investor.uber.com/news-events/news/press-release-details/2026/Hertz-and-Uber-Partner-to-Power-Autonomous-Robotaxi-and-Driver-Led-Fleet-Operations/default.aspx
27. Uber IR, WeRide Dubaï : https://investor.uber.com/news-events/news/press-release-details/2026/WeRide-and-Uber-Launch-Fully-Driverless-Robotaxi-Fare-Charging-Operations-in-Dubai-Accelerating-Autonomous-Mobility-in-the-Middle-East-2026-NSiF0EFKhd/default.aspx
28. Uber IR, Wayve et Nissan : https://investor.uber.com/news-events/news/press-release-details/2026/Wayve-Uber-and-Nissan-Announce-Collaboration-on-Robotaxis/default.aspx
29. Stellantis, Wayve et Uber (06/2026) : https://www.stellantis.com/en/news/press-releases/2026/june/stellantis-wayve-and-uber-partner-to-scale-robotaxis-globally
30. DT Next, autonome T2 2026 : https://www.dtnext.in/news/business/uber-building-infrastructure-to-commercialise-autonomous-mobility-at-global-scale-q2-earnings-report
31. San Mateo Daily Journal, Waymo dix marchés : https://www.smdailyjournal.com/business/waymos-robotaxis-now-being-dispatched-in-10-major-u-s-markets-with-expansion-in-texas/article_09e1086a-fe59-5784-b47b-24d573000c3a.html
32. Sherwood, menace Tesla : https://www.sherwood.news/business/uber-and-lyft-shares-tap-the-brakes-on-a-potential-long-term-threat-from
33. Stockwatch, licenciements et concurrence (03/09/2026) : https://wwww.stockwatch.com/News/Item/Z-C!UBER-3860454/C/UBER
34. TipRanks, cadre trois ans : https://www.tipranks.com/news/the-fly/uber-sees-three-year-gross-bookings-growth-in-mid-to-high-teens-cagr
35. Platform Aeronaut, résumé T3 2025 : https://transcripts.platformaeronaut.com/summaries/UBER-3Q25-AI-Summary
36. WLRK, offre Delivery Hero : https://www.wlrk.com/transaction/uber-in-its-14-8-billion-voluntary-takeover-offer-for-all-outstanding-shares-of-delivery-hero/
37. Khaleej Times, offre Delivery Hero (16/07/2026) : https://www.khaleejtimes.com/business/uber-launches-15-billion-bid-for-delivery-hero-to-create-global-takeout-giant
38. StartupMap, Brésil et marges : https://startupmap.iamsterdam.com/news/feed/uber-q2-revenue-misses-at-14-19b-as-brazil-competition-and-margin-concerns-weigh-on-investors
39. Tickflow, objectifs de cours : https://tickflow.io/stock/UBER/forecast
40. Google Finance, cours UBER au 30/09/2026 ; Zacks, consensus BPA (`portefeuille-peg-5-valeurs/data/data.csv`) ; deep dive `research/deepdives/UBER.md` (01/10/2026).
