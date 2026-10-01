**Données de marché et de consensus**

- Consensus Zacks (BPA non-GAAP FY0/F1/F2, LTG, Zacks Rank, bêta, dividende, 52 semaines, objectifs) au 30/09/2026 pour 47 valeurs américaines et ADR, et composition du QQQ au 30/09/2026 (100 lignes) : dépôt public [elgateaux/bourse](https://github.com/elgateaux/bourse), fichiers `screens/2026-09-30_portefeuille-peg_nasdaq100/data/zacks_univers.csv` et `qqq_holdings.csv` (commit du 01/10/2026). Fiches Zacks d'origine : [NU](https://www.zacks.com/stock/quote/NU), [TSM](https://www.zacks.com/stock/quote/TSM), [UBER](https://www.zacks.com/stock/quote/UBER), [AVGO](https://www.zacks.com/stock/quote/AVGO), [NVDA](https://www.zacks.com/stock/quote/NVDA), [RNMBY](https://www.zacks.com/stock/quote/RNMBY), [QQQ](https://www.zacks.com/stock/quote/QQQ).
- Cours de clôture du 30/09/2026 et taux de change : Google Finance (fonction GOOGLEFINANCE, feuille de calcul du 01/10/2026), 372 cotations.
- Consensus et données des valeurs d'Europe (31), d'Asie (41), d'Amérique latine (24) et des États-Unis hors univers Zacks : recherches web du 01/10/2026 (Yahoo Finance, MarketScreener/Zonebourse, StockAnalysis, StocksGuide, aktien.guide, Boursorama, Investing.com, courtiers cités), fichiers `research/europe/screen_europe.json`, `research/asia/screen_asia.json`, `research/us/screen_us.json` et `research/phase1/*.json`, chaque enregistrement portant ses URL et dates.
- Nasdaq 100 : clôture du QQQ à 739,77 $ le 30/09/2026 (Yahoo Finance, StockAnalysis) ; indice NDX à 30 408,50 points ; P/E prospectif 21,95 (GuruFocus, septembre 2026) ; croissance du BPA à 12 mois de 43 % fin août 2026 (commentaire mensuel Invesco) ; rendement total du QQQ depuis le 1er janvier : +20,83 % (TotalRealReturns, 30/09/2026).

**Analyses détaillées, citations et méga-tendances**

- Deep dives du 01/10/2026 (`research/deepdives/*.md`) : communiqués de résultats, transcriptions de conférences, dépôts réglementaires et presse financière cités avec leur date dans chaque fiche.
- Méga-tendances (`research/megatrends/megatrends.json`, `MEGATENDANCES.md`) : prévisions de capex des hyperscalers, projet de prospectus d'Anthropic (révélé par Reuters le 28/09/2026), TrendForce et SemiAnalysis via la presse, OTAN et budget fédéral allemand, rapports Lilly/Novo, documents Nu, MercadoLibre, Sea.
- Analyses précédentes du même cahier (30/09 et 01/10/2026) : `RAPPORT.md`, `ARTICLE.html` et `BILAN.html` du dépôt elgateaux/bourse, pour les faits datés qui y sont sourcés (Monzo, prospectus d'Anthropic, Rheinmetall, Uber).

**Méthode**

- Peter Lynch, *One Up on Wall Street* (1989) et *Beating the Street* (1993) : PEG, catégories (fast growers, stalwarts, cyclicals), règle du P/E bas sur les cycliques.
- Cahier PEG, méthode réutilisable, version du 1er octobre 2026 (prompt fourni par l'investisseur).
