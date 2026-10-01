#!/usr/bin/env python3
"""
Scénarios d'acquisition pour une ligne du portefeuille (ex. Nu rachetant Monzo) :
effet sur le BPA, dilution, rendement de la ligne et du portefeuille. Bibliothèque standard uniquement.
Lit data/acquisition.csv (un scénario par ligne), outputs/resume.json et data/data.csv ;
écrit outputs/acquisition.csv, outputs/acquisition.json et redaction/ACQUISITION_TABLE.md (tableau généré).
Usage : python3 acquisition.py --ticker NU
"""
import argparse
import csv
import json
import os

import portefeuille as P

ROOT = os.path.dirname(os.path.abspath(__file__))


def fr(x, d=1):
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s


def pct(x, d=1, sign=True):
    s = f"{x * 100:+.{d}f}" if sign else f"{x * 100:.{d}f}"
    return s.replace(".", ",") + " %"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", default="NU")
    ap.add_argument("--scenarios", default=os.path.join(ROOT, "data", "acquisition.csv"))
    ap.add_argument("--out", default=os.path.join(ROOT, "outputs"))
    args = ap.parse_args()
    R = json.load(open(os.path.join(args.out, "resume.json"), encoding="utf-8"))
    data = {r["ticker"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data", "data.csv"), encoding="utf-8"))}
    hyp = P.load_hypotheses(os.path.join(ROOT, "data", "hypotheses.csv"))
    t = args.ticker
    # métriques recalculées (mêmes fonctions que le modèle)
    pf_rows = [l["ticker"] for l in R["portefeuille"]["lignes"]]
    weights = {l["ticker"]: l["poids"] for l in R["portefeuille"]["lignes"]}
    metrics = {x: P.lynch_metrics(data[x], hyp[x]) for x in pf_rows}
    m = metrics[t]
    price = m["price"]
    shares_bn = float(data[t]["mcap_usd_bn"]) / price  # milliards d'actions (capitalisation / cours)
    eps_ntm = m["eps_ntm"]
    H = P.HORIZON
    rows, out = [], {}
    for sc in csv.DictReader(open(args.scenarios, encoding="utf-8")):
        if sc.get("ticker", t) != t:
            continue
        prix_gbp = float(sc["prix_md_gbp"]); fx = float(sc["gbpusd"]); part = float(sc["part_actions"])
        emission = float(sc["cours_emission_usd"]); cible_pretax = float(sc["resultat_cible_m_gbp"]) / 1000.0  # Md£
        g_cible = float(sc["croissance_cible_pct"]) / 100.0; taux = float(sc["taux_impot_pct"]) / 100.0
        r_dette = float(sc["cout_dette_pct"]) / 100.0; dg = float(sc.get("delta_g_central", 0) or 0)
        prix_usd = prix_gbp * fx
        new_shares = prix_usd * part / emission  # milliards
        cash_part = prix_usd * (1 - part)
        interest_at = cash_part * r_dette * (1 - taux)  # Md$ par an, après impôt
        cible_ni_2026 = cible_pretax * fx * (1 - taux)  # Md$
        res = {}
        for s in P.SCEN:
            g = (hyp[t]["g_" + s] + (dg if s == "central" else 0.0)) / 100.0
            eps_end = eps_ntm * (1 + g) ** H
            ni_end = eps_end * shares_bn
            cible_end = cible_ni_2026 * (1 + g_cible) ** H
            eps_pf = (ni_end + cible_end - interest_at) / (shares_bn + new_shares)
            f = eps_pf / eps_end
            # BPA 2027 (année pleine) : dilution immédiate
            eps27 = m["cy2027"]; ni27 = eps27 * shares_bn
            eps27_pf = (ni27 + cible_ni_2026 * (1 + g_cible) - interest_at) / (shares_bn + new_shares)
            res[s] = {"f": f, "accretion_2027": eps27_pf / eps27 - 1}
        # rendements : valeur terminale de la ligne × facteur du scénario (multiple de sortie inchangé)
        def tv_line(s):
            return P.terminal_value(m, s, growth_shift=(dg if s == "central" else 0.0)) * res[s]["f"]
        line_exp = P.ann(sum(P.WEIGHTS[s] * tv_line(s) for s in P.SCEN))
        def tv_pf(s):
            return sum(weights[x] * (tv_line(s) if x == t else P.terminal_value(metrics[x], s)) for x in pf_rows)
        pf_exp = P.ann(P.expected_tv(tv_pf)); pf_cen = P.ann(tv_pf("central")); pf_pess = P.ann(tv_pf("pess"))
        row = {"scenario": sc["nom"], "prix_md_gbp": prix_gbp, "prix_md_usd": prix_usd, "part_actions": part,
               "actions_nouvelles_md": new_shares, "dilution_pct": new_shares / (shares_bn + new_shares),
               "prix_sur_resultat_cible": prix_gbp / cible_pretax if cible_pretax else None,
               "prix_sur_capi_nu": prix_usd / (shares_bn * price),
               "accretion_bpa_2027": res["central"]["accretion_2027"], "facteur_bpa_2030_central": res["central"]["f"],
               "ligne_expected": line_exp, "ligne_expected_base": m["scen"]["expected"]["annual"] if "scen" in m else None,
               "pf_expected": pf_exp, "pf_central": pf_cen, "pf_pess": pf_pess, "delta_g_central": dg, "source": sc.get("source", "")}
        rows.append(row); out[sc["nom"]] = row
    base_line = P.ann(sum(P.WEIGHTS[s] * P.terminal_value(m, s) for s in P.SCEN))
    base_pf = R["portefeuille"]["rendement_annuel"]["expected"]
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "acquisition.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    json.dump({"ticker": t, "base_line_expected": base_line, "base_pf_expected": base_pf, "shares_bn": shares_bn, "scenarios": out},
              open(os.path.join(args.out, "acquisition.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # tableau Markdown généré
    lines = ["| Scénario | Prix | Payé en actions | Actions nouvelles | Dilution | Prix / résultat avant impôt de la cible | BPA 2027 pro forma | BPA 2030 pro forma (central) | Espéré de la ligne | Espéré du portefeuille | Central du portefeuille |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['scenario']} | {fr(r['prix_md_gbp'], 1)} Md£ ({fr(r['prix_md_usd'], 1)} Md$) | {pct(r['part_actions'], 0, False)} | {fr(r['actions_nouvelles_md'] * 1000, 0)} M | {pct(r['dilution_pct'], 1, False)} | {fr(r['prix_sur_resultat_cible'], 0)}x | {pct(r['accretion_bpa_2027'])} | {pct(r['facteur_bpa_2030_central'] - 1)} | {pct(r['ligne_expected'])} | {pct(r['pf_expected'])} | {pct(r['pf_central'])} |")
    lines.append(f"| **Sans acquisition (référence)** | — | — | — | — | — | — | — | **{pct(base_line)}** | **{pct(base_pf)}** | {pct(R['portefeuille']['rendement_annuel']['central'])} |")
    open(os.path.join(ROOT, "redaction", "ACQUISITION_TABLE.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    for r in rows:
        print(f"{r['scenario'][:50]:50s} dilution {r['dilution_pct']*100:5.1f} %  BPA27 {r['accretion_bpa_2027']*100:+6.1f} %  BPA30 {100*(r['facteur_bpa_2030_central']-1):+6.1f} %  ligne {r['ligne_expected']*100:5.1f} %  pf {r['pf_expected']*100:5.1f} %")
    print("écrit outputs/acquisition.csv, outputs/acquisition.json, redaction/ACQUISITION_TABLE.md")


if __name__ == "__main__":
    main()
