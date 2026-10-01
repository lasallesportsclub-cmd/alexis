## 2. La méthode, en clair

**Trois définitions.**

- **BPA non-GAAP** : bénéfice par action « ajusté » des éléments que la société juge non récurrents (rémunération en actions, amortissements d'acquisitions, frais exceptionnels). C'est la base du consensus des analystes, donc celle du PEG. Quand une société ne publie pas de BPA ajusté (MercadoLibre, sociétés japonaises ou taïwanaises), nous prenons le BPA publié et nous le disons.
- **P/E** (*price/earnings*) : cours divisé par le BPA. Le **P/E NTM** (*next twelve months*) rapporte le cours au BPA des 12 prochains mois, obtenu en mélangeant 25 % de l'année civile 2026 et 75 % de 2027 (nous sommes au 1er octobre). Les exercices décalés (NVIDIA en janvier, Microsoft en juin, Japon en mars) sont d'abord ramenés en années civiles.
- **PEG** : P/E divisé par la croissance annuelle du BPA, en points. À PEG 1, on paie un point de P/E par point de croissance : c'est le juste prix selon Peter Lynch. Sous 1, c'est bon marché ; au-dessus de 1,5, c'est cher. Nous en calculons deux : le **PEG 2027**, sur la croissance du consensus pour 2027 (plafonnée à 50 % pour neutraliser les effets de base), et le **PEG long terme**, sur notre propre hypothèse de croissance de 2027 à 2031, toujours plus prudente que le consensus quand celui-ci prolonge un pic.

**Le moteur de scénarios.** Pour chaque valeur, trois scénarios sur quatre ans (du 30/09/2026 au 30/09/2030), pondérés 25 % pessimiste, 50 % central, 25 % optimiste, dividendes réinvestis :

- rendement total = (1 + croissance)^4 × (P/E de sortie / P/E NTM actuel) × (1 + dividende)^4 − 1 ;
- **central** : si le P/E dépasse 1,5 fois la croissance, il fait la moitié du chemin vers ce niveau ; s'il est sous la croissance (PEG < 1), il fait la moitié du chemin vers PEG 1 ; sinon il ne bouge pas ;
- **optimiste** : même règle avec la croissance optimiste ; sous PEG 1, le multiple remonte jusqu'à PEG 1, avec au plus +50 % ;
- **pessimiste** : le P/E est comprimé vers 1,5 fois la croissance pessimiste (au moins 5 %), avec une baisse comprise entre 20 % et 50 % ;
- **plafond** : le P/E de sortie ne dépasse jamais le plus haut entre le P/E actuel et un plafond propre à la valeur (26 pour les valeurs exposées à Taïwan ou à la Chine, 15 pour une banque émergente, 30 à 35 en général) ;
- **cycliques** (mémoire, équipementiers au sommet) : pas de PEG. Le BPA de 2030 vaut 35 %, 65 % ou 130 % du BPA actuel selon le scénario, avec un P/E de sortie plus élevé au creux qu'au sommet. C'est la règle de Lynch : un P/E bas sur une cyclique au sommet est un signal de vente.

**Le Nasdaq 100 est reconstitué ligne à ligne** avec les mêmes règles, à partir des poids du QQQ au 30/09/2026 ({{ix:n}} valeurs couvrant {{ix:couverture}} du poids, renormalisés à 100 %). La comparaison se fait donc à armes égales : mêmes hypothèses, même moteur, mêmes plafonds.

**Le classement.** Sont éligibles les valeurs non cycliques dont le PEG long terme est inférieur ou égal à 1,5. Le score Lynch additionne trois rangs centiles : 50 % pour le PEG long terme (le plus bas est le meilleur), 30 % pour le rendement espéré, 20 % pour le PEG 2027 ; il retire 5 points pour un Zacks Rank 4 et 10 points pour un Rank 5. Le classement sert à présélectionner ; le choix final reste éditorial, car le modèle mesure mal certains risques : dépendance à un client, dette, dilution, volatilité, doublon de thème.

**Le portefeuille.** Tous les quintets à poids égaux parmi les dix premiers du classement et les valeurs retenues sont calculés ({{nb_quintets}} combinaisons). On retient celui qui combine un rendement espéré élevé, un pire cas défendable (croissance réduite de 5 points et multiples figés) et cinq moteurs indépendants. Les stress tests mettent chaque ligne, puis les deux plus grosses, puis le thème dominant en scénario pessimiste, les autres restant en central. Les probabilités de finir sous l'indice et de perdre de l'argent viennent d'un tirage indépendant du scénario de chaque ligne (3^5 = 243 combinaisons) ; elles ignorent les crises corrélées, et nous le rappelons.

**Les données.** Consensus de BPA non-GAAP Zacks au 30/09/2026 pour les valeurs américaines et les ADR, tel qu'enregistré dans le dépôt public [elgateaux/bourse](https://github.com/elgateaux/bourse) (fichier `data/zacks_univers.csv`, 47 valeurs) ; recherche web du 1er octobre 2026 pour les valeurs d'Europe, d'Asie et d'Amérique latine (consensus Yahoo Finance, MarketScreener, StockAnalysis, courtiers, tels que cités), chaque ligne portant sa source ; cours de clôture du 30/09/2026 de Google Finance pour toutes les cotations. Les sites Zacks, Yahoo Finance, StockAnalysis et SEC étant bloqués par la politique réseau de l'environnement d'analyse, et Bigdata.com n'ayant pas pu être utilisé, les chiffres de consensus hors Zacks reposent sur des résumés de recherche datés ; les lignes dont les données sont incomplètes sont signalées et n'entrent pas dans le portefeuille. Toutes les hypothèses éditoriales sont marquées « hyp. » et listées en annexe avec leur justification.

Le code (`portefeuille.py`, bibliothèque Python standard) et les CSV reproduisent chaque chiffre de ce rapport.
