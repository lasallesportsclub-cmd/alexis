# Recherches du 1er octobre 2026

- `phase1/` : screens régionaux de la première passe (JSON par région : États-Unis, Asie-Japon, Asie-Taïwan-Corée, Amérique latine) avec sources et dates.
- `europe/`, `asia/`, `us/` : screens complémentaires des sessions de recherche (31, 41 et 44 candidates), consensus de BPA par exercice, cours, bêta, 52 semaines, citations.
- `megatrends/megatrends.json` : méga-tendances documentées (taille de marché, goulots d'étranglement, leaders, citations, documents clés, risques, sources) et contexte macro du 30/09/2026.
- `deepdives/` : neuf dossiers approfondis (Nu, Rheinmetall, TSMC, Uber, Broadcom, Eli Lilly, Siemens Energy, Alnylam, Alchip) de douze sections chacun, et leurs résumés JSON (`summary_*.json`) lus par `build_data.py`.
- `histoire/` : cinq dossiers historiques (fiche d'identité, chronologie datée, trajectoire financière 2018-2025, trajectoire boursière, comment l'entreprise a gagné, concurrents, capital et dirigeants, épisodes marquants, sources) et `histoire.json` qui alimente les tableaux et graphiques de l'article long.
- `monzo/` : la rumeur de rachat de Monzo par Nu (26-30/09/2026) jour par jour, Monzo en chiffres, la stratégie internationale de Nu, l'analyse de l'opération (multiples, dilution, capital, précédents, analystes), les alternatives et les risques réglementaires ; `monzo.json` alimente `data/acquisition.csv`.
- `news/` : revues de presse datées (`AAAA-MM-JJ.md`, sections macro et valeur par valeur, chaque fait avec source et date, tableaux des cours et calendrier) et `news.json` lu par `news.py`.
