# Portefeuille à sept lignes : Adyen et Reddit ajoutés, Nvidia à la place de Broadcom (2 octobre 2026)

Composition retenue (`data/portfolio.csv`, l'ancienne est conservée dans `data/portfolio_2026-10-01.csv`) :

| Valeur | Poids | Thème | P/E NTM | Croiss. BPA 2027 | Croiss. centrale retenue | PEG LT | Zone d'achat Lynch (PEG 1) | Cours 30/09 | Rendement espéré (4 ans, par an) |
|---|---|---|---|---|---|---|---|---|---|
| Nu Holdings | 20 % | Fintech émergente | 11,6 | +35,0 % | 20 % | 0,58 | 21,81 $ | 12,66 $ | +25,5 % (pess. +2,1 %) |
| Rheinmetall | 15 % | Défense | 19,3 | +44,4 % | 20 % | 0,97 | 989 € | 956,40 € | +21,5 % (pess. −3,0 %) |
| Nvidia | 15 % | IA calcul | 17,1 | +67,0 % | 15 % | 1,14 | 200,05 $ | 228,38 $ | +17,8 % (pess. −15,5 %) |
| Uber | 15 % | IA physique | 16,0 | +36,8 % | 16 % | 1,00 | 68,51 $ | 68,51 $ | +16,9 % (pess. −11,7 %) |
| TSMC | 10 % | IA fonderie | 22,8 | +28,1 % | 17 % | 1,34 | 340,94 $ | 456,19 $ | +15,4 % (pess. −10,2 %) |
| Adyen | 12,5 % | Paiements (PEA) | 19,2 | +22,5 % | 19 % | 1,01 | 868 € | 876,60 € | +19,1 % (pess. −4,0 %) |
| Reddit | 12,5 % | Publicité et IA applicative | 21,8 | +31,7 % | 22 % | 0,99 | 143,50 $ | 142,44 $ | +22,4 % (pess. −11,7 %) |

Modèle : `portefeuille.py` relancé le 02/10/2026 sur les données du 30/09/2026 (`data/data.csv`, `data/hypotheses.csv`), sorties dans `outputs_7_lignes/` (les sorties du 01/10 restent dans `outputs/` pour le rapport). Variantes dans `data/variantes_7_lignes.txt`.

## Résultat du modèle pour le portefeuille retenu (P2)

| Indicateur | Valeur |
|---|---|
| P/E NTM du portefeuille | 16,7x (indice Nasdaq 100 reconstitué : 22,9x) |
| Croissance du BPA 2027 | +38,8 % |
| PEG long terme | 0,91 |
| Part IA (Nvidia + TSMC) | 25 % (35 % dans le portefeuille à cinq) |
| Bêta | 1,64 |
| Rendement annuel espéré sur quatre ans | **+20,4 %** (indice : +9,9 %) |
| Scénarios : pessimiste / central / optimiste | −6,5 % / +20,8 % / +35,6 % |
| Probabilité de finir sous le scénario central de l'indice | 5,0 % (2 187 combinaisons) |
| Probabilité de perdre de l'argent | 0,1 % |

Stress tests (rendement annuel) : une seule ligne en pessimiste coûte 2 à 5 points (Nu seule : +16,0 % ; les autres : +17,8 % à +18,9 %) ; double choc (Nu et Rheinmetall en pessimiste) : +12,7 % ; krach du thème dominant (fintech : Nu et Adyen) : +13,6 % ; tout en pessimiste : −6,5 % ; tout en optimiste : +35,6 %. Sensibilités : multiples figés +18,5 % ; croissance −5 points sur toutes les lignes +13,1 % ; pire combinaison (tout pessimiste, −5 points, multiples figés) +1,2 %.

## Comparaison des compositions

| Variante | P/E NTM | Croiss. 2027 | PEG LT | Part IA | Bêta | Espéré | Tout pess. | Double choc | Krach IA | Pire cas | P(sous l'indice) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P0 · Portefeuille du 01/10 (Broadcom) : NU 25, RHM 20, AVGO 20, UBER 20, TSM 15 | 16,3 | +40,3 % | 0,87 | 35 % | 1,39 | +21,0 % | −4,2 % | +11,4 % | +15,0 % | +2,6 % | 5,3 % |
| P1 · Base Nvidia : NU 25, RHM 20, NVDA 20, UBER 20, TSM 15 | 16,0 | +42,6 % | 0,90 | 35 % | 1,55 | +20,1 % | −6,3 % | +9,9 % | +13,7 % | +1,1 % | 8,8 % |
| **P2 · Retenu : P1 + Adyen 12,5 et Reddit 12,5** | 16,7 | +38,8 % | 0,91 | 25 % | 1,64 | **+20,4 %** | −6,5 % | +12,7 % | +16,0 % | +1,2 % | 5,0 % |
| P3 · Sept lignes à poids égaux | 17,5 | +37,9 % | 0,95 | 29 % | 1,68 | +19,9 % | −7,2 % | +13,8 % | +14,6 % | +1,2 % | 4,5 % |
| P4 · NU 22, RHM 16, NVDA 15, UBER 12, TSM 10, ADYEN 12,5, RDDT 12,5 | 16,6 | +38,9 % | 0,89 | 25 % | 1,65 | +20,6 % | −6,1 % | +12,2 % | +16,3 % | +1,3 % | 4,9 % |
| P5 · Neuf lignes : P2 réduite + CATL 7 + Sea 7 | 16,4 | +39,2 % | 0,89 | 22 % | 1,54 | +20,6 % | −6,7 % | +13,8 % | +16,7 % | +1,1 % | 3,1 % |
| P6 · Adyen seule ajoutée (15 %) | 16,3 | +39,6 % | 0,91 | 29 % | 1,59 | +20,0 % | −5,9 % | +11,3 % | +14,8 % | +1,4 % | 5,7 % |
| P7 · Reddit seule ajoutée (15 %) | 16,5 | +41,0 % | 0,90 | 29 % | 1,61 | +20,5 % | −7,0 % | +11,9 % | +15,4 % | +0,9 % | 6,2 % |

Pire cas : tout en pessimiste, croissance réduite de 5 points, multiples figés. P(sous l'indice) : probabilité de finir sous le scénario central du Nasdaq 100 quand chaque ligne tire son scénario indépendamment.

## Lecture

1. **Remplacer Broadcom par Nvidia coûte un point d'espérance** (+21,0 % → +20,1 %) et dégrade tous les stress tests : Nvidia a un PEG de 1,14 contre 0,96, un scénario pessimiste à −15,5 % par an (le pire des sept) et un bêta de 2,22. C'est la ligne la plus chère du portefeuille au sens de Lynch : elle cote 14 % au-dessus de sa zone d'achat (200,05 $).
2. **Ajouter Adyen et Reddit répare en partie ce coût.** L'espérance remonte à +20,4 %, la probabilité de finir sous l'indice retombe de 8,8 % à 5,0 %, le double choc passe de +9,9 % à +12,7 % et le krach IA de +13,7 % à +16,0 %, parce que la part IA descend de 35 % à 25 %. En revanche le bêta monte à 1,64 (Reddit est volatil) et le scénario « tout pessimiste » ne s'améliore pas (−6,5 %).
3. **Adyen et Reddit jouent des rôles différents.** Adyen est la ligne défensive du lot : scénario pessimiste à −4,0 % par an, le deuxième meilleur après Nu, éligible au PEA, mais croissance modeste (+22,5 % en 2027) ; seule, elle réduit l'espérance (P6 : +20,0 %). Reddit apporte la croissance (+31,7 % en 2027, espérance +22,4 %) mais un pessimiste à −11,7 % ; seule, elle augmente l'espérance mais aussi la probabilité de sous-performer (P7 : 6,2 %). Ensemble, elles se compensent : c'est la combinaison P2 ou P4.
4. **Les poids comptent peu.** Entre P2, P3 et P4, l'espérance varie de 0,7 point. P4 (Nu 22 %, Uber ramenée à 12 %) fait un peu mieux partout que P2 ; la différence tient à Uber, dont le scénario central est le plus bas des sept (+16,0 %).
5. **CATL et Sea restent la meilleure assurance contre l'indice.** La variante à neuf lignes (P5) a la plus faible probabilité de finir sous l'indice (3,1 %) et le bêta le plus bas (1,54), pour une espérance identique (+20,6 %). Les deux dossiers sont dans `research/deepdives/CATL.md` et `SE.md`.

## Les règles de vente ajoutées

- Adyen : croissance du revenu net à change constant sous 15 % sur un semestre (guidance 2026 : 21-23 %) ; marge d'EBITDA sous 45 % (49 % au S1 2026) ; perte d'un des cinq premiers clients.
- Reddit : croissance des revenus sous 25 % deux trimestres de suite (+61 % au T2 2026, guidance T3 +47 à +49 %) ; utilisateurs quotidiens en baisse sur un an ; non-renouvellement des licences de données Google ou OpenAI en 2027 sans contrat de remplacement.

## Prochaines dates des deux nouvelles lignes

- Adyen : point d'activité du T3 en novembre 2026 ; résultats annuels en février 2027.
- Reddit : résultats du T3 début novembre 2026 (seuil : revenus d'au moins 860 M$).

## Limites

Les cours et consensus datent du 30/09/2026 (Google Finance, Zacks) ; les hypothèses de croissance d'Adyen (8/19/25 %) et de Reddit (5/22/30 %) viennent du screen du 30/09 et n'ont pas fait l'objet d'un deep dive complet, contrairement aux cinq premières lignes. Le rapport `RAPPORT.md` et les articles décrivent toujours le portefeuille à cinq lignes du 01/10/2026 ; cette note le complète sans le réécrire.
