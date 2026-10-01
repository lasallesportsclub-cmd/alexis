#!/usr/bin/env python3
"""
Portefeuille concentré de 5 valeurs — méthode PEG de Peter Lynch.
Moteur de scénarios reproductible, bibliothèque standard uniquement.

Règles (cahier PEG, version du 1er octobre 2026) :
  - calendarisation des exercices décalés : BPA année civile Y = (m/12)·BPA FY(Y) + ((12−m)/12)·BPA FY(Y+1)
  - BPA NTM à la date d'analyse : (12−k)/12 · BPA CY(N) + k/12 · BPA CY(N+1), k = mois écoulés (9 au 30/09)
  - P/E NTM = cours / BPA NTM ; P/E N+1 = cours / BPA CY(N+1)
  - PEG N+1 = P/E N+1 / min(croissance BPA N+1 en %, 50)
  - PEG LT = P/E NTM / croissance centrale
  - zones d'achat : PEG LT = 1 → cours = g_central × BPA NTM ; PEG 0,8 → 0,8 × g_central × BPA NTM
  - cycliques : pas de PEG ; BPA de fin d'horizon = multiple du BPA NTM (0,35 / 0,65 / 1,30 par défaut)
  - scénarios 25 % / 50 % / 25 %, dividendes réinvestis, horizon H années
  - rendement total = (1+g)^H × (P/E sortie / P/E NTM) × (1+div)^H − 1
  - P/E de sortie : central → mi-chemin vers 1,5·g si P/E > 1,5·g, mi-chemin vers g si P/E < g, sinon inchangé ;
                    optimiste → même règle avec g_opt, sous g remonte jusqu'à g avec au plus +50 % ;
                    pessimiste → comprimé vers 1,5·max(g,5), baisse comprise entre 20 % et 50 % du P/E actuel ;
                    plafond : jamais au-dessus de max(P/E actuel, plafond propre à la valeur)
  - score Lynch = 50 % rang centile PEG LT (bas = mieux) + 30 % rang rendement espéré + 20 % rang PEG N+1 (2,0 si n.d.)
                  − 5 pts si Zacks Rank 4, − 10 pts si Zacks Rank 5
  - éligibles : non cycliques avec PEG LT ≤ 1,5

Usage : python3 portefeuille.py [--data data.csv] [--hyp hypotheses.csv] [--index index_weights.csv] [--out outputs/]
"""
import argparse
import csv
import itertools
import json
import math
import os
from collections import defaultdict

ANALYSIS_YEAR = 2026
MONTHS_ELAPSED = 9          # analyse au 1er octobre 2026, cours du 30 septembre
HORIZON = 4                 # années (01/10/2026 → 01/10/2030)
WEIGHTS = {"pess": 0.25, "central": 0.50, "opt": 0.25}
SCEN = ["pess", "central", "opt"]
CYCLICAL_MULT = {"pess": 0.35, "central": 0.65, "opt": 1.30}


# ----------------------------------------------------------------------------
# lecture des CSV
# ----------------------------------------------------------------------------
def fnum(x):
    if x is None:
        return None
    x = str(x).strip().replace(",", ".")
    if x in ("", "n.d.", "nd", "NA", "null", "None"):
        return None
    try:
        return float(x)
    except ValueError:
        return None


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ----------------------------------------------------------------------------
# métriques de Lynch
# ----------------------------------------------------------------------------
def calendarise(row):
    """Retourne (BPA CY2026, BPA CY2027, BPA CY2028, notes, fy) à partir des colonnes fy2025..fy2029.
    fyYYYY = BPA de l'exercice clos dans l'année civile YYYY (mois de clôture fy_end_month).
    Règles du cahier : F2 manquant → +10 % (signalé) ; exercice antérieur manquant → rétro-extrapolé ;
    exercice au-delà de F2 nécessaire à la calendarisation → croissance F2 plafonnée à 15 % (signalé)."""
    m = int(fnum(row.get("fy_end_month")) or 12)
    fy = {y: fnum(row.get(f"fy{y}")) for y in range(2025, 2030)}
    notes = []
    known = [y for y in range(2025, 2030) if fy[y] is not None]
    if not known:
        return None, None, None, ["aucun BPA"], fy
    first, last = known[0], known[-1]
    # F2 manquant : +10 % (règle du cahier)
    if last == first:
        fy[first + 1] = fy[first] * 1.10
        notes.append(f"FY{first + 1} extrapolé à +10 % (hyp., un seul exercice disponible)")
        last = first + 1
    # exercices suivants manquants : croissance du dernier exercice connu, bornée entre 0 et 15 %
    g = fy[last] / fy[last - 1] - 1 if fy.get(last - 1) and fy[last - 1] > 0 and fy[last] is not None else 0.10
    g = min(max(g, 0.0), 0.15)
    for y in range(last + 1, 2030):
        if fy[y] is None:
            fy[y] = fy[y - 1] * (1 + g)
            if y <= 2027 or (m != 12 and y == 2028):
                notes.append(f"FY{y} extrapolé à {g * 100:+.0f} % (hyp.)")
    # exercices antérieurs manquants : rétro-extrapolation (BPA FY(n-1) = FY(n) / (FY(n+1)/FY(n)))
    for y in range(first - 1, 2024, -1):
        if fy[y] is None and fy[y + 1] and fy[y + 2] and fy[y + 1] > 0 and fy[y + 2] > 0:
            fy[y] = fy[y + 1] / (fy[y + 2] / fy[y + 1])
            if y >= 2026:
                notes.append(f"FY{y} rétro-extrapolé (hyp.)")

    def cy(year):
        if m == 12:
            return fy[year]
        a, b = fy[year], fy.get(year + 1)
        if a is None or b is None:
            return None
        return (m / 12.0) * a + ((12 - m) / 12.0) * b

    return cy(2026), cy(2027), cy(2028), notes, fy


def lynch_metrics(row, hyp):
    """Calcule la fiche Lynch d'une valeur."""
    price = fnum(row["price"])
    cy26, cy27, cy28, notes, fy = calendarise(row)
    k = MONTHS_ELAPSED
    if cy26 is None or cy27 is None:
        eps_ntm = None
    elif str(row.get("ntm_base", "")).strip() == "cy27":
        eps_ntm = cy27
        notes.append("BPA 2026 non normalisé (élément ponctuel) : BPA NTM = BPA 2027")
    else:
        eps_ntm = (12 - k) / 12.0 * cy26 + k / 12.0 * cy27
    pe_ntm = price / eps_ntm if (eps_ntm and eps_ntm > 0 and price) else None
    pe_n1 = price / cy27 if cy27 and cy27 > 0 else None
    g_n1 = (cy27 / cy26 - 1) * 100 if cy26 and cy26 > 0 and cy27 else None
    g_n2 = (cy28 / cy27 - 1) * 100 if cy27 and cy27 > 0 and cy28 else None
    # la cyclicité est décidée par le fichier d'hypothèses (paramètres cycliques présents) ; le drapeau des données
    # brutes est signalé s'il diverge
    cyclical = hyp.get("cyc_pe_exit", {}).get("central") is not None
    if str(row.get("cyclical", "")).strip().lower() in ("1", "true", "oui", "yes") and not cyclical:
        notes.append("signalée cyclique par la recherche, traitée en croissance avec plafond de P/E bas (hyp.)")
    if cyclical:
        peg_n1 = None
        peg_lt = None
    else:
        peg_n1 = (pe_n1 / min(g_n1, 50)) if (pe_n1 and g_n1 and g_n1 > 0 and str(row.get("ntm_base", "")).strip() != "cy27") else None
        peg_lt = (pe_ntm / hyp["g_central"]) if (pe_ntm and hyp.get("g_central")) else None
    buy_peg1 = hyp["g_central"] * eps_ntm if (not cyclical and eps_ntm and hyp.get("g_central")) else None
    buy_peg08 = 0.8 * buy_peg1 if buy_peg1 else None
    if g_n1 is not None and (g_n1 > 50 or g_n1 < 0):
        notes.append(f"croissance N+1 de {g_n1:.1f} % : aberration à expliquer (effet de base, perte ou élément ponctuel)")
    return {
        "ticker": row["ticker"], "name": row["name"], "region": row.get("region", ""),
        "currency": row.get("currency", ""), "theme": row.get("theme", ""),
        "price": price, "price_date": row.get("price_date", ""),
        "mcap_usd_bn": fnum(row.get("mcap_usd_bn")),
        "fy_end_month": int(fnum(row.get("fy_end_month")) or 12),
        "fy": fy, "cy2026": cy26, "cy2027": cy27, "cy2028": cy28,
        "eps_ntm": eps_ntm, "pe_ntm": pe_ntm, "pe_n1": pe_n1,
        "g_n1": g_n1, "g_n2": g_n2, "peg_n1": peg_n1, "peg_lt": peg_lt,
        "buy_peg1": buy_peg1, "buy_peg08": buy_peg08,
        "ltg_consensus": fnum(row.get("ltg_pct")), "beta": fnum(row.get("beta")),
        "div_yield": fnum(row.get("div_yield_pct")) or 0.0,
        "zacks_rank": fnum(row.get("zacks_rank")),
        "cyclical": cyclical, "notes": notes,
        "hyp": hyp,
    }


# ----------------------------------------------------------------------------
# moteur de scénarios
# ----------------------------------------------------------------------------
def exit_pe(pe, g, scenario, cap):
    """P/E de sortie selon les règles du cahier."""
    if scenario == "central":
        if pe > 1.5 * g:
            px = pe + (1.5 * g - pe) / 2.0
        elif pe < g:
            px = pe + (g - pe) / 2.0
        else:
            px = pe
    elif scenario == "opt":
        if pe > 1.5 * g:
            px = pe + (1.5 * g - pe) / 2.0
        elif pe < g:
            px = min(g, pe * 1.5)
        else:
            px = pe
    else:  # pess
        target = 1.5 * max(g, 5.0)
        px = min(max(target, 0.5 * pe), 0.8 * pe)
    ceiling = max(pe, cap)
    return min(px, ceiling)


def terminal_value(m, scenario, growth_shift=0.0, freeze_multiples=False, peak_eps=False):
    """Valeur terminale (1 € investi) d'une valeur dans un scénario.
    growth_shift : points de croissance ajoutés (−5 pour la sensibilité).
    freeze_multiples : P/E de sortie = P/E actuel.
    peak_eps : pour une cyclique, bénéfices maintenus au pic (multiple de BPA = 1,0)."""
    h = m["hyp"]
    pe = m["pe_ntm"]
    dy = (m["div_yield"] or 0.0) / 100.0
    if m["cyclical"]:
        mult = 1.0 if peak_eps else h["cyc_mult"][scenario]
        eps_end = m["eps_ntm"] * mult
        pe_x = pe if freeze_multiples else h["cyc_pe_exit"][scenario]
        price_end = eps_end * pe_x
        return (price_end / m["price"]) * (1 + dy) ** HORIZON
    g = h["g_" + scenario] + growth_shift
    pe_x = pe if freeze_multiples else exit_pe(pe, max(g, 0.0), scenario, h["pe_cap"])
    return (1 + g / 100.0) ** HORIZON * (pe_x / pe) * (1 + dy) ** HORIZON


def scenario_table(m):
    out = {}
    for s in SCEN:
        tv = terminal_value(m, s)
        h = m["hyp"]
        if m["cyclical"]:
            g = None
            pe_x = h["cyc_pe_exit"][s]
            eps_end = m["eps_ntm"] * h["cyc_mult"][s]
        else:
            g = h["g_" + s]
            pe_x = exit_pe(m["pe_ntm"], max(g, 0.0), s, h["pe_cap"])
            eps_end = m["eps_ntm"] * (1 + g / 100.0) ** HORIZON
        out[s] = {"g": g, "pe_exit": pe_x, "eps_end": eps_end, "price_end": eps_end * pe_x,
                  "tv": tv, "annual": tv ** (1 / HORIZON) - 1}
    exp_tv = sum(WEIGHTS[s] * out[s]["tv"] for s in SCEN)
    out["expected"] = {"tv": exp_tv, "annual": exp_tv ** (1 / HORIZON) - 1}
    return out


def pct_rank(values, lower_is_better):
    """Rang centile 0..100 (100 = le meilleur)."""
    n = len(values)
    out = []
    for v in values:
        better = sum(1 for w in values if (w > v if lower_is_better else w < v))
        out.append(100.0 * better / (n - 1) if n > 1 else 100.0)
    return out


# ----------------------------------------------------------------------------
# portefeuille et indice
# ----------------------------------------------------------------------------
def portfolio_tv(members, weights, scen_map, **kw):
    """members : liste de métriques ; weights : dict ticker→poids ; scen_map : ticker→scénario."""
    return sum(weights[m["ticker"]] * terminal_value(m, scen_map[m["ticker"]], **kw) for m in members)


def uniform_scen(members, s):
    return {m["ticker"]: s for m in members}


def ann(tv):
    return tv ** (1 / HORIZON) - 1


def index_tv(idx_members, idx_weights, scenario, **kw):
    return portfolio_tv(idx_members, idx_weights, uniform_scen(idx_members, scenario), **kw)


def expected_tv(fn):
    return sum(WEIGHTS[s] * fn(s) for s in SCEN)


def probability_analysis(members, weights, index_central_tv):
    """Chaque valeur tire son scénario indépendamment (3^n combinaisons)."""
    below, loss, total = 0.0, 0.0, 0.0
    tvs = {m["ticker"]: {s: terminal_value(m, s) for s in SCEN} for m in members}
    for combo in itertools.product(SCEN, repeat=len(members)):
        p = 1.0
        tv = 0.0
        for m, s in zip(members, combo):
            p *= WEIGHTS[s]
            tv += weights[m["ticker"]] * tvs[m["ticker"]][s]
        total += p
        if tv < index_central_tv:
            below += p
        if tv < 1.0:
            loss += p
    return {"p_below_index_central": below / total, "p_loss": loss / total, "combinations": 3 ** len(members)}


# ----------------------------------------------------------------------------
# programme principal
# ----------------------------------------------------------------------------
def load_hypotheses(path):
    hyp = {}
    for r in read_csv(path):
        t = r["ticker"]
        hyp[t] = {
            "g_pess": fnum(r.get("g_pess")), "g_central": fnum(r.get("g_central")), "g_opt": fnum(r.get("g_opt")),
            "pe_cap": fnum(r.get("pe_cap")) or 32.0,
            "cyc_mult": {"pess": fnum(r.get("cyc_mult_pess")) or CYCLICAL_MULT["pess"],
                         "central": fnum(r.get("cyc_mult_central")) or CYCLICAL_MULT["central"],
                         "opt": fnum(r.get("cyc_mult_opt")) or CYCLICAL_MULT["opt"]},
            "cyc_pe_exit": {"pess": fnum(r.get("cyc_pe_pess")), "central": fnum(r.get("cyc_pe_central")),
                            "opt": fnum(r.get("cyc_pe_opt"))},
            "justification": r.get("justification", ""),
        }
    return hyp


def fmt_pct(x, d=1):
    return "n.d." if x is None else f"{x * 100:+.{d}f} %".replace(".", ",")


def fmtn(x, d=1):
    return "n.d." if x is None else f"{x:.{d}f}".replace(".", ",")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/data.csv")
    ap.add_argument("--hyp", default="data/hypotheses.csv")
    ap.add_argument("--index", default="data/index_weights.csv")
    ap.add_argument("--portfolio", default="data/portfolio.csv")
    ap.add_argument("--out", default="outputs")
    ap.add_argument("--dilution", action="append", help="TICKER:facteur sur le BPA 2030 (ex. NU:0.868 pour Monzo tout en actions)")
    ap.add_argument("--variants", default=None, help="fichier texte : nom|T1:poids,T2:poids,... (une variante par ligne)")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    rows = {r["ticker"]: r for r in read_csv(args.data)}
    hyps = load_hypotheses(args.hyp)
    metrics = {}
    for t, r in rows.items():
        if t not in hyps:
            raise SystemExit(f"hypothèse manquante pour {t}")
        if fnum(r.get("price")) is None:
            print(f"[avert.] {t}: cours indisponible, valeur ignorée")
            continue
        m = lynch_metrics(r, hyps[t])
        if m["pe_ntm"] is None:
            print(f"[avert.] {t}: P/E NTM indisponible (BPA NTM négatif ou manquant), valeur ignorée")
            continue
        m["scen"] = scenario_table(m)
        metrics[t] = m

    # --- indice reconstitué ---
    idx_rows = read_csv(args.index)
    idx_members, raw_w = [], {}
    missing = []
    for r in idx_rows:
        t = r["ticker"]
        w = fnum(r["weight_pct"])
        if t in metrics and w:
            idx_members.append(metrics[t])
            raw_w[t] = w
        else:
            missing.append(t)
    tot = sum(raw_w.values())
    idx_w = {t: w / tot for t, w in raw_w.items()}
    index_res = {s: index_tv(idx_members, idx_w, s) for s in SCEN}
    index_res["expected"] = expected_tv(lambda s: index_res[s])
    index_cov = tot
    # distorsion propre à l'indice : bénéfices des cycliques maintenus au pic
    index_peak = {s: index_tv(idx_members, idx_w, s, peak_eps=True) for s in SCEN}
    index_peak["expected"] = expected_tv(lambda s: index_peak[s])
    # multiples figés / croissance −5
    index_frozen = expected_tv(lambda s: index_tv(idx_members, idx_w, s, freeze_multiples=True))
    index_minus5 = expected_tv(lambda s: index_tv(idx_members, idx_w, s, growth_shift=-5))
    index_both = expected_tv(lambda s: index_tv(idx_members, idx_w, s, growth_shift=-5, freeze_multiples=True))

    # --- classement ---
    eligible = [m for m in metrics.values() if not m["cyclical"] and m["peg_lt"] is not None and m["peg_lt"] <= 1.5]
    excluded = [m for m in metrics.values() if m not in eligible]
    peg_lt = [m["peg_lt"] for m in eligible]
    exp_ret = [m["scen"]["expected"]["annual"] for m in eligible]
    peg_n1 = [m["peg_n1"] if m["peg_n1"] is not None else 2.0 for m in eligible]
    r1, r2, r3 = pct_rank(peg_lt, True), pct_rank(exp_ret, False), pct_rank(peg_n1, True)
    for m, a, b, c in zip(eligible, r1, r2, r3):
        pen = 5 if m["zacks_rank"] == 4 else (10 if m["zacks_rank"] == 5 else 0)
        m["score"] = 0.5 * a + 0.3 * b + 0.2 * c - pen
        m["score_parts"] = (a, b, c, pen)
    eligible.sort(key=lambda m: -m["score"])

    # --- portefeuille retenu ---
    pf_rows = read_csv(args.portfolio)
    pf = [metrics[r["ticker"]] for r in pf_rows]
    pf_w = {r["ticker"]: fnum(r["weight"]) for r in pf_rows}
    wsum = sum(pf_w.values())
    pf_w = {t: w / wsum for t, w in pf_w.items()}
    pf_res = {s: portfolio_tv(pf, pf_w, uniform_scen(pf, s)) for s in SCEN}
    pf_res["expected"] = expected_tv(lambda s: pf_res[s])
    # variantes de pondération : équipondéré
    eq_w = {m["ticker"]: 1.0 / len(pf) for m in pf}
    eq_res = {s: portfolio_tv(pf, eq_w, uniform_scen(pf, s)) for s in SCEN}
    eq_res["expected"] = expected_tv(lambda s: eq_res[s])

    # --- quintets parmi les 10 premiers du classement + valeurs du portefeuille ---
    pool = []
    for m in eligible[:10] + pf:
        if m not in pool:
            pool.append(m)
    quintets = []
    for combo in itertools.combinations(pool, 5):
        w = {m["ticker"]: 0.2 for m in combo}
        res = {s: portfolio_tv(list(combo), w, uniform_scen(combo, s)) for s in SCEN}
        exp = expected_tv(lambda s: res[s])
        worst = portfolio_tv(list(combo), w, uniform_scen(combo, "pess"), growth_shift=-5, freeze_multiples=True)
        themes = defaultdict(int)
        for m in combo:
            themes[m["theme"]] += 1
        dom = max(themes.values())
        quintets.append({
            "tickers": [m["ticker"] for m in combo],
            "pe_ntm": 1.0 / sum(0.2 / m["pe_ntm"] for m in combo),
            "g_n1": sum(0.2 * (m["g_n1"] or 0) for m in combo),
            "peg_lt": sum(0.2 * (m["peg_lt"] or 0) for m in combo),
            "dominant_theme_n": dom,
            "expected": ann(exp), "pess": ann(res["pess"]), "central": ann(res["central"]), "opt": ann(res["opt"]),
            "worst_case": ann(worst),
            "beta": sum(0.2 * (m["beta"] or 1.0) for m in combo),
        })
    quintets.sort(key=lambda q: -q["expected"])

    # --- stress tests ---
    central = uniform_scen(pf, "central")
    stress = {}
    stress["tout en central"] = pf_res["central"]
    for m in pf:
        sm = dict(central)
        sm[m["ticker"]] = "pess"
        stress[f"{m['ticker']} seul en pessimiste"] = portfolio_tv(pf, pf_w, sm)
    top2 = sorted(pf, key=lambda m: -pf_w[m["ticker"]])[:2]
    sm = dict(central)
    for m in top2:
        sm[m["ticker"]] = "pess"
    stress["double choc (2 plus grosses lignes en pessimiste)"] = portfolio_tv(pf, pf_w, sm)
    themes = defaultdict(list)
    for m in pf:
        themes[m["theme"]].append(m["ticker"])
    dom_theme = max(themes.items(), key=lambda kv: len(kv[1]))
    sm = dict(central)
    for t in dom_theme[1]:
        sm[t] = "pess"
    stress[f"krach du thème dominant ({dom_theme[0]} : {', '.join(dom_theme[1])})"] = portfolio_tv(pf, pf_w, sm)
    stress["tout en pessimiste"] = pf_res["pess"]
    stress["tout en optimiste"] = pf_res["opt"]

    sens = {}
    sens["multiples figés"] = expected_tv(lambda s: portfolio_tv(pf, pf_w, uniform_scen(pf, s), freeze_multiples=True))
    sens["croissance −5 pts"] = expected_tv(lambda s: portfolio_tv(pf, pf_w, uniform_scen(pf, s), growth_shift=-5))
    sens["multiples figés et croissance −5 pts"] = expected_tv(
        lambda s: portfolio_tv(pf, pf_w, uniform_scen(pf, s), growth_shift=-5, freeze_multiples=True))
    sens["pire combinaison (tout pessimiste, −5 pts, multiples figés)"] = portfolio_tv(
        pf, pf_w, uniform_scen(pf, "pess"), growth_shift=-5, freeze_multiples=True)
    line_sens = {}
    for m in pf:
        for shift in (-5, 5):
            def f(s, m=m, shift=shift):
                tv = 0.0
                for mm in pf:
                    tv += pf_w[mm["ticker"]] * terminal_value(mm, s, growth_shift=(shift if mm is m else 0.0))
                return tv
            line_sens[f"{m['ticker']} {shift:+d} pts"] = expected_tv(f)

    probs = probability_analysis(pf, pf_w, index_res["central"])

    # --- poche d'ETF Nasdaq 100 à côté du portefeuille ---
    etf = {}
    for share in (0.0, 0.10, 0.20, 1 / 3, 0.50):
        def mix(fn_pf, fn_ix):
            return (1 - share) * fn_pf + share * fn_ix
        exp = expected_tv(lambda s: mix(portfolio_tv(pf, pf_w, uniform_scen(pf, s)), index_tv(idx_members, idx_w, s)))
        sm = dict(central)
        for m in top2:
            sm[m["ticker"]] = "pess"
        double = mix(portfolio_tv(pf, pf_w, sm), index_res["central"])
        allp = mix(pf_res["pess"], index_res["pess"])
        etf[f"{share * 100:.0f} %"] = {"expected": ann(exp), "double_choc": ann(double), "tout_pess": ann(allp)}

    # --- dilution d'une acquisition : BPA de fin d'horizon d'une ligne multiplié par un facteur ---
    dilution = {}
    for spec in (args.dilution or []):
        t, f = spec.split(":")
        f = float(f)
        def tvd(s, t=t, f=f):
            return sum(pf_w[m["ticker"]] * terminal_value(m, s) * (f if m["ticker"] == t else 1.0) for m in pf)
        dilution[spec] = {"expected": ann(expected_tv(tvd)), "central": ann(tvd("central")),
                          "ligne_expected": ann(sum(WEIGHTS[s] * terminal_value(metrics[t], s) * f for s in SCEN))}

    # --- variantes de portefeuille nommées (comparaison) ---
    variants = []
    IA_THEMES = {"IA calcul", "IA fonderie et équipement", "IA mémoire et stockage", "IA réseau et optique", "IA énergie et refroidissement", "Hyperscalers et plateformes"}
    if args.variants and os.path.exists(args.variants):
        for line in open(args.variants, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "|" not in line:
                continue
            name, spec = line.split("|", 1)
            comp = {}
            for part in spec.split(","):
                tk, wv = part.strip().split(":")
                comp[tk.strip()] = float(wv)
            if any(tk not in metrics for tk in comp):
                print(f"[avert.] variante « {name} » : valeur inconnue {[tk for tk in comp if tk not in metrics]}")
                continue
            tot_w = sum(comp.values())
            wv = {tk: v / tot_w for tk, v in comp.items()}
            mem = [metrics[tk] for tk in wv]
            res = {sc: portfolio_tv(mem, wv, uniform_scen(mem, sc)) for sc in SCEN}
            exp = expected_tv(lambda sc: res[sc])
            cen = uniform_scen(mem, "central")
            two = sorted(mem, key=lambda m: -wv[m["ticker"]])[:2]
            sm2 = dict(cen)
            for m in two:
                sm2[m["ticker"]] = "pess"
            smia = dict(cen)
            for m in mem:
                if m["theme"] in IA_THEMES:
                    smia[m["ticker"]] = "pess"
            pr = probability_analysis(mem, wv, index_res["central"])
            worst = portfolio_tv(mem, wv, uniform_scen(mem, "pess"), growth_shift=-5, freeze_multiples=True)
            variants.append({
                "nom": name.strip(), "composition": ", ".join(f"{tk} {v * 100:.0f} %" for tk, v in wv.items()),
                "pe_ntm": 1.0 / sum(wv[m["ticker"]] / m["pe_ntm"] for m in mem),
                "g_n1": sum(wv[m["ticker"]] * (m["g_n1"] or 0) for m in mem),
                "peg_lt": (1.0 / sum(wv[m["ticker"]] / m["pe_ntm"] for m in mem)) / max(1e-9, sum(wv[m["ticker"]] * (m["hyp"]["g_central"] or 0) for m in mem if not m["cyclical"])),
                "part_ia": sum(wv[m["ticker"]] for m in mem if m["theme"] in IA_THEMES),
                "beta": sum(wv[m["ticker"]] * (m["beta"] or 1.0) for m in mem),
                "expected": ann(exp), "pess": ann(res["pess"]), "central": ann(res["central"]), "opt": ann(res["opt"]),
                "double_choc": ann(portfolio_tv(mem, wv, sm2)), "krach_ia": ann(portfolio_tv(mem, wv, smia)),
                "pire_cas": ann(worst), "p_below": pr["p_below_index_central"], "p_loss": pr["p_loss"],
                "regions": ", ".join(sorted({m["region"] for m in mem})),
            })

    # --- cycliques « qui ne le seraient plus » : rendement selon le sort des bénéfices et le P/E de sortie ---
    cyc_table = {}
    for m in metrics.values():
        if not m["cyclical"]:
            continue
        rows_c = []
        for lab, mult, pe in (("−65 %", 0.35, 14), ("−50 %", 0.50, 12), ("−35 %", 0.65, 12), ("stables, au sommet", 1.0, 12), ("+10 % par an", 1.1 ** HORIZON, 12)):
            tv = (m["eps_ntm"] * mult * pe / m["price"]) * (1 + (m["div_yield"] or 0) / 100) ** HORIZON
            rows_c.append({"benefices_2030": lab, "pe_sortie": pe, "annuel": ann(tv), "cours_2030": m["eps_ntm"] * mult * pe})
        cyc_table[m["ticker"]] = rows_c

    # --- coût de la concentration : 3 et 4 lignes (meilleurs sous-ensembles par score) ---
    concentration = {}
    for n in (3, 4, 5):
        sub = pf[:n] if n < len(pf) else pf
        w = {m["ticker"]: 1.0 / len(sub) for m in sub}
        res = {s: portfolio_tv(sub, w, uniform_scen(sub, s)) for s in SCEN}
        pr = probability_analysis(sub, w, index_res["central"])
        concentration[n] = {"tickers": [m["ticker"] for m in sub], "expected": ann(expected_tv(lambda s: res[s])),
                            "pess": ann(res["pess"]), "p_below": pr["p_below_index_central"], "p_loss": pr["p_loss"]}

    # ------------------------------------------------------------------
    # sorties
    # ------------------------------------------------------------------
    def write_csv(name, header, rows_):
        with open(os.path.join(args.out, name), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows_)

    write_csv("resultats_par_valeur.csv",
              ["ticker", "nom", "région", "thème", "devise", "cours", "BPA CY2026", "BPA CY2027", "BPA CY2028", "BPA NTM",
               "P/E NTM", "P/E N+1", "croiss. N+1 %", "croiss. N+2 %", "PEG N+1", "g pess", "g central", "g opt", "PEG LT",
               "zone PEG 1", "zone PEG 0,8", "P/E sortie pess", "P/E sortie central", "P/E sortie opt",
               "cours fin pess", "cours fin central", "cours fin opt", "rdt annuel pess", "rdt annuel central",
               "rdt annuel opt", "rdt annuel espéré", "cyclique", "score Lynch", "notes"],
              [[m["ticker"], m["name"], m["region"], m["theme"], m["currency"], m["price"],
                round(m["cy2026"], 3), round(m["cy2027"], 3), round(m["cy2028"], 3) if m["cy2028"] else "",
                round(m["eps_ntm"], 3), round(m["pe_ntm"], 2), round(m["pe_n1"], 2) if m["pe_n1"] else "",
                round(m["g_n1"], 1) if m["g_n1"] is not None else "", round(m["g_n2"], 1) if m["g_n2"] is not None else "",
                round(m["peg_n1"], 2) if m["peg_n1"] else "", m["hyp"]["g_pess"], m["hyp"]["g_central"], m["hyp"]["g_opt"],
                round(m["peg_lt"], 2) if m["peg_lt"] else "",
                round(m["buy_peg1"], 2) if m["buy_peg1"] else "", round(m["buy_peg08"], 2) if m["buy_peg08"] else "",
                round(m["scen"]["pess"]["pe_exit"], 1), round(m["scen"]["central"]["pe_exit"], 1),
                round(m["scen"]["opt"]["pe_exit"], 1),
                round(m["scen"]["pess"]["price_end"], 2), round(m["scen"]["central"]["price_end"], 2),
                round(m["scen"]["opt"]["price_end"], 2),
                round(m["scen"]["pess"]["annual"] * 100, 2), round(m["scen"]["central"]["annual"] * 100, 2),
                round(m["scen"]["opt"]["annual"] * 100, 2), round(m["scen"]["expected"]["annual"] * 100, 2),
                "oui" if m["cyclical"] else "non", round(m.get("score", 0), 1) if "score" in m else "",
                " ; ".join(m["notes"])]
               for m in sorted(metrics.values(), key=lambda m: -(m.get("score", -1e9)))])

    write_csv("classement.csv", ["rang", "ticker", "nom", "PEG LT", "rdt espéré %", "PEG N+1", "rang PEG LT", "rang rdt",
                                 "rang PEG N+1", "pénalité Zacks", "score"],
              [[i + 1, m["ticker"], m["name"], round(m["peg_lt"], 2), round(m["scen"]["expected"]["annual"] * 100, 2),
                round(m["peg_n1"], 2) if m["peg_n1"] else "n.d. (2,0)", round(m["score_parts"][0], 1),
                round(m["score_parts"][1], 1), round(m["score_parts"][2], 1), m["score_parts"][3], round(m["score"], 1)]
               for i, m in enumerate(eligible)])

    write_csv("exclus.csv", ["ticker", "nom", "raison", "PEG LT", "rdt espéré %"],
              [[m["ticker"], m["name"], "cyclique" if m["cyclical"] else f"PEG LT {m['peg_lt']:.2f} > 1,5",
                round(m["peg_lt"], 2) if m["peg_lt"] else "", round(m["scen"]["expected"]["annual"] * 100, 2)]
               for m in sorted(excluded, key=lambda m: -(m["scen"]["expected"]["annual"]))])

    write_csv("quintets.csv", ["valeurs", "P/E NTM", "croiss. N+1 %", "PEG LT", "n thème dominant", "bêta", "rdt espéré %",
                               "rdt pess %", "rdt central %", "rdt opt %", "pire cas % (pess, −5 pts, multiples figés)"],
              [[" ".join(q["tickers"]), round(q["pe_ntm"], 1), round(q["g_n1"], 1), round(q["peg_lt"], 2),
                q["dominant_theme_n"], round(q["beta"], 2), round(q["expected"] * 100, 2), round(q["pess"] * 100, 2),
                round(q["central"] * 100, 2), round(q["opt"] * 100, 2), round(q["worst_case"] * 100, 2)] for q in quintets])

    write_csv("variantes.csv", ["variante", "composition", "régions", "P/E NTM", "croiss. N+1 %", "PEG LT", "part IA %", "bêta",
                                "rdt espéré %", "rdt pess %", "rdt central %", "rdt opt %", "double choc %", "krach IA %",
                                "pire cas %", "p sous indice %", "p perte %"],
              [[v["nom"], v["composition"], v["regions"], round(v["pe_ntm"], 1), round(v["g_n1"], 1), round(v["peg_lt"], 2),
                round(v["part_ia"] * 100, 0), round(v["beta"], 2), round(v["expected"] * 100, 2), round(v["pess"] * 100, 2),
                round(v["central"] * 100, 2), round(v["opt"] * 100, 2), round(v["double_choc"] * 100, 2), round(v["krach_ia"] * 100, 2),
                round(v["pire_cas"] * 100, 2), round(v["p_below"] * 100, 1), round(v["p_loss"] * 100, 1)] for v in variants])

    write_csv("indice.csv", ["ticker", "nom", "poids brut %", "poids renormalisé %", "P/E NTM", "g central", "PEG LT",
                             "rdt espéré %", "cyclique"],
              [[m["ticker"], m["name"], raw_w[m["ticker"]], round(idx_w[m["ticker"]] * 100, 2), round(m["pe_ntm"], 1),
                m["hyp"]["g_central"], round(m["peg_lt"], 2) if m["peg_lt"] else "",
                round(m["scen"]["expected"]["annual"] * 100, 2), "oui" if m["cyclical"] else "non"]
               for m in sorted(idx_members, key=lambda m: -idx_w[m["ticker"]])])

    summary = {
        "parametres": {"date_analyse": "2026-10-01", "horizon_annees": HORIZON, "mois_ecoules": MONTHS_ELAPSED,
                       "poids_scenarios": WEIGHTS},
        "portefeuille": {
            "lignes": [{"ticker": m["ticker"], "poids": round(pf_w[m["ticker"]], 4)} for m in pf],
            "rendement_annuel": {s: ann(pf_res[s]) for s in SCEN + ["expected"]},
            "valeur_terminale": {s: pf_res[s] for s in SCEN + ["expected"]},
            "equipondere_rendement_annuel": {s: ann(eq_res[s]) for s in SCEN + ["expected"]},
            "pe_ntm": 1.0 / sum(pf_w[m["ticker"]] / m["pe_ntm"] for m in pf),
            "g_n1": sum(pf_w[m["ticker"]] * (m["g_n1"] or 0) for m in pf),
            "peg_lt": sum(pf_w[m["ticker"]] * (m["peg_lt"] or 0) for m in pf),
            "beta": sum(pf_w[m["ticker"]] * (m["beta"] or 1.0) for m in pf),
            "g_central": sum(pf_w[m["ticker"]] * m["hyp"]["g_central"] for m in pf),
        },
        "indice": {
            "couverture_poids_pct": index_cov, "n_lignes": len(idx_members), "manquants": missing,
            "rendement_annuel": {s: ann(index_res[s]) for s in SCEN + ["expected"]},
            "valeur_terminale": {s: index_res[s] for s in SCEN + ["expected"]},
            "pe_ntm": 1.0 / sum(idx_w[m["ticker"]] / m["pe_ntm"] for m in idx_members),
            "g_n1": sum(idx_w[m["ticker"]] * (m["g_n1"] or 0) for m in idx_members),
            "g_central": sum(idx_w[m["ticker"]] * (m["hyp"]["g_central"] or 0) for m in idx_members if not m["cyclical"]) /
                         max(1e-9, sum(idx_w[m["ticker"]] for m in idx_members if not m["cyclical"])),
            "beta": sum(idx_w[m["ticker"]] * (m["beta"] or 1.0) for m in idx_members),
            "sensibilites_rendement_annuel": {
                "benefices cycliques maintenus au pic": ann(index_peak["expected"]),
                "multiples figés": ann(index_frozen), "croissance −5 pts": ann(index_minus5),
                "multiples figés et −5 pts": ann(index_both),
            },
        },
        "stress_tests_rendement_annuel": {k: ann(v) for k, v in stress.items()},
        "sensibilites_rendement_annuel": {k: ann(v) for k, v in sens.items()},
        "sensibilites_par_ligne_rendement_annuel": {k: ann(v) for k, v in line_sens.items()},
        "probabilites": probs,
        "poche_etf": etf,
        "dilution": dilution,
        "cycliques": cyc_table,
        "variantes": variants,
        "concentration": concentration,
        "classement": [{"rang": i + 1, "ticker": m["ticker"], "score": round(m["score"], 1), "peg_lt": round(m["peg_lt"], 2),
                        "rdt_espere": m["scen"]["expected"]["annual"]} for i, m in enumerate(eligible)],
        "exclus": [{"ticker": m["ticker"], "raison": "cyclique" if m["cyclical"] else "PEG LT > 1,5",
                    "peg_lt": m["peg_lt"], "rdt_espere": m["scen"]["expected"]["annual"]} for m in excluded],
        "quintets_top10": quintets[:10],
        "quintet_retenu": next((q for q in quintets if set(q["tickers"]) == set(pf_w)), None),
        "quintet_rang": next((i + 1 for i, q in enumerate(quintets) if set(q["tickers"]) == set(pf_w)), None),
        "valeurs": {t: {k: v for k, v in m.items() if k not in ("hyp", "fy")} | {"hyp": m["hyp"], "fy": m["fy"]}
                    for t, m in metrics.items()},
    }
    with open(os.path.join(args.out, "resume.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=lambda o: None)

    # --- affichage console ---
    print("=" * 78)
    print("PORTEFEUILLE 5 VALEURS — méthode PEG de Lynch — horizon", HORIZON, "ans")
    print("=" * 78)
    for m in pf:
        s = m["scen"]
        print(f"{m['ticker']:<8} poids {pf_w[m['ticker']]*100:4.0f} %  P/E NTM {m['pe_ntm']:5.1f}  g N+1 {fmtn(m['g_n1'])} %"
              f"  PEG LT {fmtn(m['peg_lt'],2)}  rdt espéré {fmt_pct(s['expected']['annual'])}"
              f"  [pess {fmt_pct(s['pess']['annual'])} / central {fmt_pct(s['central']['annual'])} / opt {fmt_pct(s['opt']['annual'])}]")
    print("-" * 78)
    for s in SCEN + ["expected"]:
        print(f"{s:<9} portefeuille {fmt_pct(ann(pf_res[s]))}   indice {fmt_pct(ann(index_res[s]))}")
    print(f"indice couvert à {index_cov:.1f} % du poids sur {len(idx_members)} lignes ; manquants : {missing}")
    print("-" * 78)
    print("Stress tests (rendement annuel du portefeuille) :")
    for k, v in stress.items():
        print(f"  {k:<60} {fmt_pct(ann(v))}")
    print("Sensibilités :")
    for k, v in sens.items():
        print(f"  {k:<60} {fmt_pct(ann(v))}")
    print(f"Probabilité de finir sous l'indice (central) : {probs['p_below_index_central']*100:.1f} % ; "
          f"de perdre de l'argent : {probs['p_loss']*100:.1f} % ({probs['combinations']} combinaisons)")
    print("-" * 78)
    print("Classement (score Lynch) :")
    for i, m in enumerate(eligible[:15]):
        print(f"  {i+1:>2}. {m['ticker']:<8} score {m['score']:5.1f}  PEG LT {m['peg_lt']:.2f}  "
              f"rdt espéré {fmt_pct(m['scen']['expected']['annual'])}")
    print(f"Quintet retenu : rang {summary['quintet_rang']} sur {len(quintets)} quintets")
    print("Sorties écrites dans", args.out)


if __name__ == "__main__":
    main()
