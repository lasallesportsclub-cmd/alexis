# Portefeuille PEG à cinq valeurs (1er octobre 2026)

Portefeuille concentré de cinq valeurs construit avec la méthode PEG de Peter Lynch pour battre le Nasdaq 100 sur quatre ans (du 30/09/2026 au 30/09/2030). Univers de 159 valeurs sur quatre continents (États-Unis, Europe, Asie, Amérique latine), neuf deep dives, six méga-tendances documentées.

**Retenu : Nu Holdings 25 %, Rheinmetall 20 %, Broadcom 20 %, Uber 20 %, TSMC 15 %.**

## Livrables

| Fichier | Contenu |
|---|---|
| `RAPPORT.md` | Rapport complet (contexte, méthode, univers et classement, portefeuille et variantes, cinq analyses détaillées, stress tests, critique, plan d'action, limites, sources, annexes) |
| `ARTICLE.html`, `ARTICLE.pdf` | Article autonome (thème clair/sombre, mobile, infographies SVG, titre de journal fictif), et sa version A4 |
| `outputs/` | Sorties du modèle : `resultats_par_valeur.csv`, `classement.csv`, `exclus.csv`, `quintets.csv`, `variantes.csv`, `indice.csv`, `resume.json` |
| `data/` | Univers (`data.csv`), hypothèses éditoriales (`hypotheses.csv`), poids du QQQ (`index_weights.csv`), portefeuille et variantes |
| `../research/` | Données brutes des recherches du 01/10/2026 : screens Europe, Asie, États-Unis, Amérique latine (`phase1/`), méga-tendances, et les huit deep dives (`deepdives/`) |

## Reproduction (bibliothèque standard Python uniquement)

```bash
cd portefeuille-peg-5-valeurs
python3 build_data.py            # assemble data/data.csv et data/index_weights.csv depuis sources/ et ../research/
python3 build_hypotheses.py      # écrit data/hypotheses.csv (hypothèses « hyp. » avec justification)
python3 portefeuille.py --data data/data.csv --hyp data/hypotheses.csv --index data/index_weights.csv \
  --portfolio data/portfolio.csv --variants data/variantes.txt --dilution NU:0.868 --out outputs
python3 rapport.py --template redaction/RAPPORT_template.md --out RAPPORT.md
python3 rapport.py --template redaction/ARTICLE_template.md --out article/contenu.md
python3 article.py --resume outputs/resume.json --content article/contenu.md --out ARTICLE.html
```

Les textes du rapport et de l'article sont dans `redaction/` ; tous les chiffres des tableaux, des graphiques et des phrases chiffrées sont des balises `{{...}}` remplies par `rapport.py` depuis `outputs/resume.json`. Aucun chiffre du modèle n'est recopié à la main. Les faits datés (résultats, carnets, citations) viennent des deep dives et des sources citées.

## Sources des données

Consensus Zacks du 30/09/2026 pour les valeurs américaines et les ADR (dépôt public elgateaux/bourse, copie dans `sources/`), cours de clôture et taux de change du 30/09/2026 (Google Finance, `gf.csv`, `fx.csv`), consensus Europe, Asie et Amérique latine issus des recherches web du 01/10/2026 (`../research/`), chaque enregistrement avec ses URL et dates.

*Analyse quantitative et datée. Elle ne constitue pas un conseil en investissement personnalisé.*
