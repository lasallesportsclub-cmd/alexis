# Reddit : qui sont ses clients, comment ils ont changé en deux ans, et à quoi s'attendre

Dossier du 02/10/2026. Reddit n'a pas encore de deep dive complet dans `research/deepdives/` ; sa fiche de présentation est dans `portefeuille-peg-5-valeurs/COMPLEMENT_5_VALEURS.md`. Cours 142,44 $ (NYSE, clôture 30/09/2026), capitalisation 28,0 Md$. Position en portefeuille : 12,5 % (`portefeuille-peg-5-valeurs/data/portfolio.csv`).

Règles : aucun chiffre inventé. Chaque chiffre porte une source et une date. Donnée introuvable = « n.d. ». Les calculs maison sont signalés « calcul ». Exercice = année civile. DAUq = utilisateurs quotidiens uniques ; WAUq = hebdomadaires ; ARPU = revenu moyen par utilisateur quotidien sur le trimestre.

Avertissement : ce dossier est rédigé par Claude, un modèle d'Anthropic. Reddit poursuit Anthropic en justice pour collecte de contenu sans licence (section 4.3). Les passages sur ce procès reposent uniquement sur des sources publiques citées, et le lecteur doit tenir compte de ce conflit d'intérêts.

Différence avec les autres dossiers. Reddit a deux clientèles qui n'achètent pas la même chose : les annonceurs (94 % du revenu 2025), qui achètent l'attention des utilisateurs, et les laboratoires d'IA (Google, OpenAI), qui achètent le droit d'utiliser les textes. Les utilisateurs ne paient rien : ce sont le produit. Ce dossier traite les trois.

---

## 1. Résumé en dix lignes

- Les annonceurs font 94 % du revenu 2025 (2,06 Md$ sur 2,20 Md$). Les dix premiers pèsent 21 % du revenu (26 % en 2023), sans engagement de long terme. Aucun nom n'est publié.
- Le nombre d'annonceurs actifs croît de 75 % par an (T4 2025, T1 2026). Les publicités à la performance font plus de 60 % du revenu publicitaire.
- Les licences de données (Google ≈ 60 M$ par an, OpenAI ≈ 70 M$) font environ 6 % du revenu 2025. Renégociation en cours : Wells Fargo imagine 550 M$ par an, le WSJ rapporte des tensions avec Google (22/07/2026).
- Les utilisateurs quotidiens sont passés de 73,1 millions (fin 2023) à 130,3 millions (T2 2026), soit 1,8 fois. Mais 60 % sont « déconnectés », venus de Google pour la plupart, et les Américains connectés ne croissent plus que de 1 %.
- Le revenu par utilisateur a bondi : ARPU mondial 6,18 $ au T2 2026 (+36 %), 11,85 $ aux États-Unis, 2,26 $ à l'international. Un Américain vaut 5,2 fois un étranger (calcul).
- Les États-Unis font 79 % du revenu et 41 % des utilisateurs ; l'international croît de 84 % en revenu.
- Revenu du T2 2026 : 805 M$ (+61 %), huitième trimestre au-dessus de 60 % ; marge d'EBITDA ajusté 43 %. Guidance T3 : 860-870 M$ (+47-49 %).
- Le titre a perdu 12,5 % le jour des résultats (recherche Google « chahutée », utilisateurs américains en baisse séquentielle), 46 % depuis son plus haut de 52 semaines.
- Reddit cessera de publier la répartition connectés / déconnectés à partir du T3 2026 : moins de transparence au moment où la question compte le plus.
- Action à 27,0 fois le BPA 2026 et 20,5 fois celui de 2027 (calcul). Hypothèses du modèle (5 / 22 / 30 %) inchangées.

---

## 2. Qui sont les clients

### 2.1 Les annonceurs

| Indicateur | 2023 | 2024 | 2025 | 2026 | Source |
|---|---|---|---|---|---|
| Revenu publicitaire | ≈ 789 M$ (98 % du total) | 1 185,5 M$ (+50 %, 91 %) | 2 062,5 M$ (+74 %, 94 %) | T1 : 625 M$ (+74 %) ; T2 : 762 M$ (+64 %) | S-1 via SiliconANGLE, https://siliconangle.com/2024/02/22/reddit-files-ipo-annual-revenue-tops-800m/ ; 10-K 2024, https://www.sec.gov/Archives/edgar/data/1713445/000171344525000018/rddt-20241231.htm ; Recho, https://www.recho.co/blog/reddit-q4-2025-earnings-report-analysis ; 8-K T2 2026, https://www.sec.gov/Archives/edgar/data/0001713445/000171344526000098/earningspressreleaseq226.htm |
| Dix premiers annonceurs | 26 % du revenu (calcul : ≈ 209 M$) | 25 % (≈ 325 M$) | 21 % (≈ 463 M$) | n.d. | 10-K 2024 ; 10-K 2025 via Panabee, https://www.panabee.com/bear/is-reddit-rddt-a-buy-08012026 |
| Annonceurs actifs | n.d. | n.d. | +75 % sur un an (T4) | +75 % (T1 2026) | PPC Land, https://ppc.land/reddits-ad-revenue-jumps-74-as-eps-misses-forecast-in-q1-2026/ |
| Part des publicités à la performance | n.d. | n.d. | n.d. | plus de 60 % du revenu publicitaire | PPC Land |

Qui sont-ils. Reddit ne nomme aucun annonceur. Les verticales fortes sont le jeu vidéo, la technologie et les logiciels, l'e-commerce depuis les Dynamic Product Ads, la finance (Webtonic, https://www.webtonic.io/blog/e-commerce-reddit-ads-statistics). Les dix premiers ne fournissent « généralement pas d'engagements de long terme » (10-K 2025). La concentration baisse (26 % → 21 %) parce que les PME arrivent via les outils en libre-service : intégration Shopify mondiale le 27/05/2026, Collection Ads, retour sur dépense publicitaire de 7 fois pour les détaillants européens selon une étude TransUnion commandée par Reddit (PPC Land, https://ppc.land/reddit-launches-collection-ads-and-shopify-integration-for-dpa-at-shoptalk/).

### 2.2 Les acheteurs de données

| Client | Contrat | Statut | Source |
|---|---|---|---|
| Google | ≈ 60 M$ par an, signé début 2024 | renouvellement en discussion ; le WSJ rapporte des « turbulences » et Reddit envisage de couper l'accès ; titre −6 % le 22/07/2026 | AI Weekly, https://aiweekly.co/alerts/reddit-weighs-cutting-google-ai-access-as-60m-deal-expires ; Crypto Briefing, https://cryptobriefing.com/reddit-stock-google-ai-deal-non-renewal/ |
| OpenAI | ≈ 70 M$ par an | renouvellement en discussion | Insider Monkey, https://www.insidermonkey.com/blog/reddits-next-ai-catalyst-isnt-user-growth-its-what-alphabets-google-and-openai-do-next-1826466/ |
| Ensemble | ≈ 130-140 M$ en 2025, soit 6 % du revenu (calcul) ; Wells Fargo voit jusqu'à 550 M$ après renégociation, soit 25 % du revenu 2025 (calcul) | — | Insider Monkey |

Le revenu « autre » (licences et abonnements premium) est passé de 15 M$ (2023) à 114,7 M$ (2024) et 140 M$ (2025), puis 43 M$ au T2 2026 (+24 %). Le fichier `data/hypotheses.csv` note l'expiration des licences en 2027 ; les sources de 2026 parlent d'un renouvellement discuté dès 2026. Date exacte n.d.

### 2.3 Les utilisateurs, qui sont le produit

| Indicateur | T4 2023 | T4 2024 | T4 2025 | T2 2026 | Source |
|---|---|---|---|---|---|
| DAUq | 73,1 M | 101,7 M (+39 %) | 121,0 M | 130,3 M (+18 %) | SiliconANGLE ; BusinessWire, https://www.businesswire.com/news/home/20250210462815/en/ ; Recho ; 8-K T2 2026 |
| WAUq | n.d. | n.d. | n.d. | 514,6 M (+24 %) | 8-K T2 2026 |
| dont connectés | n.d. | n.d. | n.d. | 52,6 M (+7 %) : États-Unis 23,1 M (+1 %), international 29,5 M (+12 %) | 8-K T2 2026 |
| dont déconnectés | n.d. | n.d. | n.d. | 77,7 M (+27 %) : États-Unis 30,1 M (+10 %), international 47,6 M (+41 %) | 8-K T2 2026 |
| Revenu annuel par DAUq (calcul) | 11,0 $ | 12,8 $ | 18,2 $ | — | calcul sur le revenu annuel et les DAUq de fin d'année |

Lecture. Les utilisateurs ont presque doublé en deux ans et demi, mais la croissance vient des déconnectés (60 % du total, calcul), dont « la plupart viennent de Google » selon Steve Huffman (Sherwood, https://www.sherwood.news/tech/the-majority-of-reddits-user-growth-came-from-logged-out-users/). Les Américains connectés, les plus rentables, stagnent : +1 % au T2 2026, sixième trimestre de ralentissement. Reddit Answers, l'assistant d'IA interne, est passé de 1 million d'utilisateurs hebdomadaires (T1 2025) à 15 millions (T4 2025) (Octagon, https://www.octagonai.co/markets/financials/companies/reddit-daily-active-uniques-in-q3/) ; chiffre 2026 n.d.

---

## 3. L'évolution sur deux ans

### 3.1 Revenu, géographie, monétisation

| Période | Revenu total | États-Unis | International | Part internationale (calcul) | ARPU mondial | ARPU États-Unis | ARPU international | Source |
|---|---|---|---|---|---|---|---|---|
| 2023 | 804 M$ (+20 %) | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | SiliconANGLE |
| T2 2024 | 281,2 M$ | n.d. | n.d. | n.d. | n.d. | n.d. | n.d. | 8-K T2 2025, https://www.sec.gov/Archives/edgar/data/1713445/000171344525000194/earningspressreleaseq225.htm |
| 2024 | 1 300,2 M$ (+62 %) | 1 063,6 M$ | 236,6 M$ | 18,2 % | n.d. | n.d. | n.d. | 10-K 2025, https://www.sec.gov/Archives/edgar/data/1713445/000171344526000022/rddt-20251231.htm |
| T2 2025 | 500 M$ (+78 %) | n.d. | n.d. | n.d. | 4,53 $ (+47 %) | n.d. | n.d. | 8-K T2 2025 |
| 2025 | 2 202,5 M$ (+69 %) | 1 785,6 M$ (+68 %) | 416,9 M$ (+76 %, calcul) | 18,9 % | n.d. | n.d. | n.d. | 10-K 2025 |
| T2 2026 | 805 M$ (+61 %) | 638 M$ (+56 %) | 167 M$ (+84 %) | 20,7 % | 6,18 $ (+36 %) | 11,85 $ (+51 %) | 2,26 $ (+31 %) | 8-K T2 2026 ; Motley Fool, https://www.fool.com/earnings/call-transcripts/2026/07/30/reddit-rddt-q2-2026-earnings-call-transcript/ |

Le revenu du T2 a été multiplié par 2,9 en deux ans (calcul). Les États-Unis font encore 79 % du revenu avec 41 % des utilisateurs : un Américain rapporte 5,2 fois plus qu'un étranger (calcul). L'international croît plus vite en utilisateurs (+28 %) et en revenu (+84 %), aidé par la traduction automatique (10-Q T1 2026, https://www.sec.gov/Archives/edgar/data/0001713445/000171344526000069/rddt-20260331.htm).

### 3.2 Rentabilité

| Période | Résultat net | EBITDA ajusté | Marge | Source |
|---|---|---|---|---|
| T2 2024 | −10 M$ | n.d. | n.d. | 8-K T2 2025 |
| T2 2025 | 89 M$ | n.d. | n.d. ; marge brute 90,8 % | 8-K T2 2025 |
| T2 2026 | 253 M$ (BPA dilué 1,25 $) | 343 M$ | 43 % (calcul) | 8-K T2 2026 ; `COMPLEMENT_5_VALEURS.md` |

Rachat d'actions de 1 Md$ autorisé avec les résultats du T4 2025 (Recho).

### 3.3 Ce qui a changé dans la relation client

- **Du branding à la performance.** Plus de 60 % du revenu publicitaire vient désormais d'annonces mesurées à la conversion ; les Dynamic Product Ads ont amélioré le retour sur dépense de 91 % au T4 2025 (PPC Land). Les PME entrent via Shopify.
- **Des données vendues au contentieux.** Google et OpenAI paient ; Anthropic et Perplexity sont poursuivis (section 4.3). Reddit cherche à faire payer plus cher le droit d'entraîner des modèles sur ses textes.
- **De Google à Reddit Answers.** Reddit veut convertir les visiteurs envoyés par Google en utilisateurs connectés et répondre lui-même aux questions.

---

## 4. À quoi s'attendre pour les années à venir

### 4.1 Ce que dit Reddit

| Horizon | Indication | Source |
|---|---|---|
| T3 2026 | revenu 860 à 870 M$ (+47 à 49 %), EBITDA ajusté 385 à 395 M$ (+63 à 67 %), marge 45 % | 8-K T2 2026 ; MarketScreener, https://www.marketscreener.com/news/reddit-inc-provides-earnings-guidance-for-the-third-quarter-of-2026-ce7f50dbd88af320 |
| Utilisateurs | objectif de 100 millions d'Américains quotidiens (contre 53,2 millions au T2 2026) | Seeking Alpha, https://seekingalpha.com/news/4583636-reddit-outlines-715m-725m-q2-2026-revenue-while-targeting-100m-daily-u-s-users |
| Publication | fin de la répartition connectés / déconnectés à partir du T3 2026 | 8-K T2 2026 |
| Rendez-vous | résultats du T3 2026 fin octobre ou début novembre (date n.d.) | — |

Consensus BPA non-GAAP : 5,27 $ (2026), 6,94 $ (2027) selon Zacks au 30/09/2026 (`data/data.csv`) ; 2028 n.d. Au cours de 142,44 $ : 27,0 fois 2026, 20,5 fois 2027 (calcul). Objectif de cours moyen 214,84 $ (Tickflow, https://www.tickflow.io/stock/RDDT/forecast). Le titre est à 46 % sous son plus haut de 52 semaines (263,50 $) et à 9 % sous son cours du 03/09/2026 (calculs).

### 4.2 Ce qui soutient la clientèle

- **Les annonceurs arrivent.** +75 % d'annonceurs actifs par an, dix premiers ramenés à 21 % : la base s'élargit et se dé-risque.
- **La monétisation rattrape les pairs.** ARPU américain à 11,85 $ par trimestre, en hausse de 51 % ; Reddit « surpasse ses rivaux en monétisation » selon TradingPedia (https://www.tradingpedia.com/2026/08/17/reddit-outpaces-rivals-in-monetization-and-arpu-gains/).
- **L'international.** 59 % des utilisateurs, 21 % du revenu : l'écart d'ARPU (5,2 fois) est la réserve de croissance.
- **Les licences.** Si Wells Fargo a raison, 550 M$ par an de revenu à marge quasi totale.
- **La marge.** 43 à 45 % d'EBITDA ajusté, 1 Md$ de rachats.

### 4.3 Ce qui menace la clientèle

1. **Google.** Les AI Overviews répondent sans renvoyer vers Reddit ; Huffman parle de « choppy » et dit que les AI Overviews « font mal à l'écosystème du web » (Free Press Journal, https://www.freepressjournal.in/amp/tech/ai-overviews-are-hurting-the-web-ecosystem-reddit-ceo-steve-huffman-hits-out-at-google-over-search-traffic-decline). Une étude Pew voit le trafic réduit de près de moitié ; Google conteste. 60 % des utilisateurs sont déconnectés et viennent surtout de Google.
2. **La fin de la transparence.** Supprimer la répartition connectés / déconnectés au T3 2026 empêchera de mesurer ce risque.
3. **Les Américains connectés.** +1 % au T2 2026, en baisse séquentielle : le cœur du revenu ne croît plus en nombre, seulement en prix.
4. **Les licences.** Google est à la fois le premier fournisseur de trafic et un client de données en renégociation. Une rupture coûterait les deux.
5. **Les procès.** Reddit contre Anthropic : renvoyé devant la cour d'État de Californie en mars 2026 ; en août 2026 le juge « doute » des arguments d'Anthropic (Bloomberg Law, https://news.bgov.com/ip-law/anthropic-unlikely-to-beat-reddit-scraping-suit-judge-hints). Reddit contre Perplexity, Oxylabs, AWMProxy et SerpApi (10/2025) : en cours (eWeek, https://www.eweek.com/artificial-intelligence/reddit-sues-perplexity/). Une victoire renforce le prix des licences ; une défaite affaiblit tout le modèle « données payantes ». Rappel du conflit d'intérêts : l'auteur de ce dossier est un modèle d'Anthropic.
6. **La concurrence publicitaire.** Google, Meta et Amazon ont capté 98,27 % des dollars publicitaires supplémentaires des cinq grandes plateformes au T2 2026 (eMarketer, https://www.emarketer.com/content/q4-2025-advertising-earnings-tracker) ; Reddit pèse 0,5 % de la publicité numérique.
7. **La valorisation.** 27 fois 2026 pour une société qui a perdu 46 % en un an : le marché a déjà revu ses attentes, mais le plafond de P/E de sortie à 35 du modèle suppose qu'elle reste une valeur de croissance.

### 4.4 Les trois scénarios pour un actionnaire

| Scénario | Hypothèse | Cohérence avec `data/hypotheses.csv` (RDDT) |
|---|---|---|
| Pessimiste | Google coupe le trafic, licences non renouvelées, utilisateurs américains en baisse ; BPA +5 % par an | hypothèse basse : 5 % |
| Central | revenu +40 % en 2026 puis +25 %, licences renouvelées au prix actuel, ARPU international en rattrapage ; BPA +22 % par an | hypothèse centrale : 22 % |
| Optimiste | licences à 550 M$, 100 millions d'Américains quotidiens, Reddit Answers remplace Google comme porte d'entrée ; BPA +30 % par an | hypothèse haute : 30 % |

Le consensus (BPA +101 % en 2026, +32 % en 2027, calcul) est au-dessus de l'hypothèse centrale. Pas de modification.

---

## 5. Ce que ça change pour le portefeuille

- **Reddit (12,5 %)** est la ligne la plus dépendante d'un tiers qui n'est pas son client : Google lui envoie la majorité de ses nouveaux utilisateurs, lui achète ses données, et le concurrence en publicité. Aucune autre ligne du portefeuille n'a ce profil.
- **Le signal à suivre** : les utilisateurs quotidiens américains (53,2 millions au T2 2026). Comme Reddit cesse de distinguer connectés et déconnectés, c'est ce chiffre, avec l'ARPU américain, qui dira si le cœur tient. Un deuxième trimestre de baisse séquentielle validerait le scénario pessimiste.
- **Les licences** sont l'option : 6 % du revenu aujourd'hui, 25 % si Wells Fargo a raison. Le renouvellement Google est l'événement de l'automne 2026.
- **Lien avec le reste du portefeuille** : Google (TPU fabriqués chez TSMC) et OpenAI (client de Nvidia et d'Oracle) sont les deux clients de données de Reddit. Lien direct avec Adyen ou Nvidia : n.d.

Points de contrôle : résultats du T3 2026 (date n.d., fin octobre ou début novembre) ; issue des renégociations Google et OpenAI ; audience du procès Anthropic devant la cour d'État de Californie ; premier trimestre sans répartition connectés / déconnectés.

---

## 6. Sources

1. Reddit, 8-K T2 2026 (30/07/2026) : https://www.sec.gov/Archives/edgar/data/0001713445/000171344526000098/earningspressreleaseq226.htm
2. Reddit, lettre aux actionnaires T2 2026 : https://www.sec.gov/Archives/edgar/data/0001713445/000171344526000098/exhibit992q226.htm
3. Reddit, 10-Q T2 2026 : https://www.sec.gov/Archives/edgar/data/0001713445/000171344526000100/rddt-20260630.htm
4. Reddit, 10-Q T1 2026 : https://www.sec.gov/Archives/edgar/data/0001713445/000171344526000069/rddt-20260331.htm
5. Reddit, 10-K 2025 : https://www.sec.gov/Archives/edgar/data/1713445/000171344526000022/rddt-20251231.htm
6. Reddit, 10-K 2024 : https://www.sec.gov/Archives/edgar/data/1713445/000171344525000018/rddt-20241231.htm
7. Reddit, 8-K T2 2025 : https://www.sec.gov/Archives/edgar/data/1713445/000171344525000194/earningspressreleaseq225.htm
8. BusinessWire, résultats 2024 (10/02/2025) : https://www.businesswire.com/news/home/20250210462815/en/
9. SiliconANGLE, S-1 (22/02/2024) : https://siliconangle.com/2024/02/22/reddit-files-ipo-annual-revenue-tops-800m/
10. Recho, T4 2025 : https://www.recho.co/blog/reddit-q4-2025-earnings-report-analysis
11. Motley Fool, transcript T2 2026 (30/07/2026) : https://www.fool.com/earnings/call-transcripts/2026/07/30/reddit-rddt-q2-2026-earnings-call-transcript/
12. Investing.com, T2 2026, titre −12,5 % : https://www.investing.com/news/transcripts/earnings-call-transcript-reddit-tops-revenue-forecast-in-q2-2026-shares-fall-125-93CH-4826379
13. CNBC, T2 2026 : https://www.cnbc.com/2026/07/30/reddit-rddt-q2-2026-earnings-report.html
14. MarketScreener, guidance T3 2026 : https://www.marketscreener.com/news/reddit-inc-provides-earnings-guidance-for-the-third-quarter-of-2026-ce7f50dbd88af320
15. Panabee, 10-K 2025 et dix premiers annonceurs : https://www.panabee.com/bear/is-reddit-rddt-a-buy-08012026
16. PPC Land, T1 2026 : https://ppc.land/reddits-ad-revenue-jumps-74-as-eps-misses-forecast-in-q1-2026/
17. PPC Land, Shoptalk et Shopify : https://ppc.land/reddit-launches-collection-ads-and-shopify-integration-for-dpa-at-shoptalk/
18. Webtonic, verticales : https://www.webtonic.io/blog/e-commerce-reddit-ads-statistics
19. AI Weekly, licence Google : https://aiweekly.co/alerts/reddit-weighs-cutting-google-ai-access-as-60m-deal-expires
20. Crypto Briefing, WSJ 22/07/2026 : https://cryptobriefing.com/reddit-stock-google-ai-deal-non-renewal/
21. Insider Monkey, licences et Wells Fargo : https://www.insidermonkey.com/blog/reddits-next-ai-catalyst-isnt-user-growth-its-what-alphabets-google-and-openai-do-next-1826466/
22. Sherwood, utilisateurs déconnectés : https://www.sherwood.news/tech/the-majority-of-reddits-user-growth-came-from-logged-out-users/
23. Octagon, Reddit Answers : https://www.octagonai.co/markets/financials/companies/reddit-daily-active-uniques-in-q3/
24. Free Press Journal, Huffman sur les AI Overviews : https://www.freepressjournal.in/amp/tech/ai-overviews-are-hurting-the-web-ecosystem-reddit-ceo-steve-huffman-hits-out-at-google-over-search-traffic-decline
25. MLQ, titre −11 % : https://mlq.ai/news/reddit-shares-sink-11-as-search-referrals-wobble-despite-61-revenue-growth/
26. TradingPedia, ARPU : https://www.tradingpedia.com/2026/08/17/reddit-outpaces-rivals-in-monetization-and-arpu-gains/
27. Seeking Alpha, objectif 100 M d'Américains : https://seekingalpha.com/news/4583636-reddit-outlines-715m-725m-q2-2026-revenue-while-targeting-100m-daily-u-s-users
28. Bloomberg Law / BGov, procès Anthropic (08/2026) : https://news.bgov.com/ip-law/anthropic-unlikely-to-beat-reddit-scraping-suit-judge-hints
29. MLex, renvoi en cour d'État (03/2026) : https://www.mlex.com/mlex/artificial-intelligence/articles/2459465/reddit-s-data-scraping-lawsuit-against-anthropic-sent-back-to-california-state-court
30. eWeek, procès Perplexity : https://www.eweek.com/artificial-intelligence/reddit-sues-perplexity/
31. eMarketer, triopole publicitaire : https://www.emarketer.com/content/q4-2025-advertising-earnings-tracker
32. Tickflow, objectifs de cours : https://www.tickflow.io/stock/RDDT/forecast
33. Google Finance, cours RDDT au 30/09/2026 ; Zacks, consensus BPA (`portefeuille-peg-5-valeurs/data/data.csv`) ; `portefeuille-peg-5-valeurs/COMPLEMENT_5_VALEURS.md` (02/10/2026).
