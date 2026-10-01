{{include:TITRE.md}}

*Méthode PEG de Peter Lynch, portefeuille concentré de cinq valeurs, horizon de quatre ans (du 30/09/2026 au 30/09/2030). Données arrêtées au 1er octobre 2026, cours de clôture du 30 septembre 2026. Consensus de BPA non-GAAP Zacks pour les valeurs américaines et les ADR ; consensus Yahoo Finance, MarketScreener, StockAnalysis et courtiers pour l'Europe, l'Asie et l'Amérique latine, tels que cités. Les chiffres marqués « hyp. » sont des hypothèses éditoriales, modifiables dans `data/hypotheses.csv`. Analyse quantitative et datée : elle ne constitue pas un conseil en investissement personnalisé.*

---

## En bref

{{include:ENBREF.md}}

{{tab_verdict}}

{{tab_vs_indice}}

{{include:ENBREF_MESSAGES.md}}

---

## 1. Le contexte : six méga-tendances et ce qui reste rare

{{include:CONTEXTE.md}}

---

{{include:METHODE.md}}

---

## 3. L'univers : {{nb_univers}} valeurs sur quatre continents, et le classement

{{include:UNIVERS.md}}

### 3.1 Le classement Lynch (valeurs éligibles : non cycliques, PEG long terme ≤ 1,5)

{{tab_classement}}

### 3.2 Les exclues et pourquoi

{{include:EXCLUES.md}}

{{tab_exclus}}

### 3.3 Le Nasdaq 100 reconstitué

{{include:INDICE.md}}

{{tab_indice}}

---

## 4. Le portefeuille : pourquoi ces cinq-là, et pas les autres

{{include:PORTEFEUILLE.md}}

### 4.1 Les {{nb_quintets}} quintets à poids égaux

{{tab_quintets}}

\* Pire cas : croissance réduite de 5 points par an pour chaque ligne et multiples figés.

### 4.2 Le portefeuille retenu face aux alternatives

{{tab_variantes}}

\* Pire cas : tout en pessimiste, croissance réduite de 5 points, multiples figés. P(sous l'indice) : probabilité de finir sous le scénario central du Nasdaq 100 quand chaque ligne tire son scénario indépendamment (243 combinaisons).

{{include:VARIANTES.md}}

### 4.3 Le coût de la concentration et la poche d'ETF

{{tab_proba}}

\* Tirage indépendant du scénario de chaque ligne (25/50/25) ; l'indice est pris dans son scénario central. Les crises corrélées n'y sont pas représentées.

{{tab_etf}}

{{include:CONCENTRATION.md}}

---

## 5. Analyses détaillées

{{include:ANALYSES.md}}

---

## 6. Risques et robustesse

### 6.1 Stress tests

{{tab_stress}}

### 6.2 Sensibilités

{{tab_sens}}

{{tab_lignes}}

{{include:RISQUES.md}}

### 6.3 Questions transverses

{{include:TRANSVERSES.md}}

{{tab_dilution}}

{{tab_cycliques}}

---

## 7. La critique : les questions qui fâchent

{{include:CRITIQUE.md}}

---

## 8. Plan d'action

{{include:PLAN.md}}

---

## 9. Limites

{{include:LIMITES.md}}

---

## 10. Reproduction

```bash
python3 portefeuille.py --data data/data.csv --hyp data/hypotheses.csv --index data/index_weights.csv \
  --portfolio data/portfolio.csv --variants data/variantes.txt --dilution NU:0.868 --out outputs
python3 acquisition.py --ticker NU   # scénarios Monzo (data/acquisition.csv → outputs/acquisition.json)
python3 rapport.py --template redaction/RAPPORT_template.md --out RAPPORT.md
python3 article.py --resume outputs/resume.json --content article/contenu.md --out ARTICLE.html
```

| Fichier | Contenu |
|---|---|
| `data/data.csv` | Univers : cours, devises, BPA par exercice, bêta, dividende, source de chaque ligne |
| `data/hypotheses.csv` | Hypothèses éditoriales (croissance par scénario, plafond de P/E, paramètres des cycliques) avec justification |
| `data/index_weights.csv` | Composition du QQQ au 30/09/2026 (100 lignes) |
| `data/portfolio.csv`, `data/variantes.txt` | Portefeuille retenu et variantes comparées |
| `fx.csv` | Taux de change du 30/09/2026 (Google Finance) |
| `outputs/resultats_par_valeur.csv` | Sortie du modèle, valeur par valeur |
| `outputs/classement.csv`, `outputs/exclus.csv` | Classement Lynch et exclues |
| `outputs/quintets.csv`, `outputs/variantes.csv` | Quintets et variantes |
| `outputs/indice.csv` | Nasdaq 100 reconstitué |
| `data/acquisition.csv`, `outputs/acquisition.csv` | Scénarios d'acquisition (Monzo) : dilution, BPA pro forma, rendements |
| `outputs/resume.json` | Toutes les sorties (stress tests, sensibilités, probabilités, poche d'ETF, dilution, cycliques) |
| `research/` | Données brutes des recherches du 01/10/2026 (Europe, Asie, États-Unis, méga-tendances, deep dives) avec leurs sources |

**Contrôle à la main (une ligne recalculée).** Nu : cours {{v:NU:price}} ; BPA 2026 de {{v:NU:cy2026}} $ et 2027 de {{v:NU:cy2027}} $ ; BPA des douze prochains mois = 0,25 × 0,864 + 0,75 × 1,166 = 1,0905 $ ; P/E NTM = 12,66 / 1,0905 = 11,6 ; PEG long terme = 11,6 / 20 = 0,58. Scénario central : BPA 2030 = 1,0905 × 1,20⁴ = 2,261 $ ; le P/E (11,6) est sous la croissance (20), il remonte à mi-chemin, soit 15,8, plafonné à 15 ; cours 2030 = 2,261 × 15 = 33,92 $ ; multiple de 33,92 / 12,66 = 2,679 sur quatre ans, soit 27,9 % par an. Le modèle donne {{v:NU:price_central}} et {{v:NU:central}}. Indice : la ligne Micron (5,0 % du QQQ) est traitée en cyclique, BPA 2030 à 65 % du niveau actuel et P/E de sortie de 12 en central.

---

## Sources

{{include:SOURCES.md}}

{{tab_sources}}

---

## Annexe A. L'univers complet

{{tab_univers}}

## Annexe B. Les hypothèses éditoriales

{{tab_hypotheses}}

---

*Analyse quantitative et datée du 1er octobre 2026. Elle ne constitue pas un conseil en investissement personnalisé. Les performances passées ne préjugent pas des performances futures ; les scénarios sont des hypothèses, pas des prévisions.*
