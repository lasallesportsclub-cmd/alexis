#!/usr/bin/env python3
"""
Revue de presse : génère depuis research/news/news.json les tableaux de l'article d'actualité
(cours et variations depuis le 30/09, effet mécanique sur le P/E et le PEG des lignes, calendrier),
dans redaction/NEWS_PRICES.md, redaction/NEWS_CALENDAR.md et outputs/news_prices.csv. Bibliothèque standard uniquement.
Usage : python3 news.py --json ../research/news/news.json
"""
import argparse
import csv
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


def fr(x, d=1):
    return f"{x:,.{d}f}".replace(",", " ").replace(".", ",")


def pct(x, d=1, sign=True):
    s = f"{x:+.{d}f}" if sign else f"{x:.{d}f}"
    return s.replace(".", ",") + " %"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=os.path.join(ROOT, "..", "research", "news", "news.json"))
    args = ap.parse_args()
    N = json.load(open(args.json, encoding="utf-8"))
    R = json.load(open(os.path.join(ROOT, "outputs", "resume.json"), encoding="utf-8"))
    V = R["valeurs"]
    data = {r["ticker"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data", "data.csv"), encoding="utf-8"))}
    weights = {l["ticker"]: l["poids"] for l in R["portefeuille"]["lignes"]}
    sym = {"USD": "$", "EUR": "€", "TWD": "NT$"}
    rows, out = [], []
    pf_move = 0.0
    for p in N.get("prices", []):
        t = p["ticker"]
        c0, c1 = p.get("close_2026_09_30"), p.get("close_latest")
        chg = p.get("change_pct")
        if chg is None and c0 and c1:
            chg = (c1 / c0 - 1) * 100
        v = V.get(t)
        cur = sym.get(data[t]["currency"], "") if t in data else ("$" if t == "QQQ" else "")
        pe_new = peg_new = None
        if v and c1 and v.get("eps_ntm"):
            pe_new = c1 / v["eps_ntm"]
            g = v["hyp"]["g_central"]
            peg_new = pe_new / g if g else None
        if t in weights and chg is not None:
            pf_move += weights[t] * chg
        rows.append([f"**{t}**" if t in weights else t, f"{fr(c0, 2)} {cur}" if c0 else "n.d.", f"{fr(c1, 2)} {cur}" if c1 else "n.d.",
                     p.get("date_latest", ""), pct(chg) if chg is not None else "n.d.",
                     f"{fr(v['pe_ntm'])} → {fr(pe_new)}" if pe_new else "—", f"{fr(v['peg_lt'], 2)} → {fr(peg_new, 2)}" if peg_new else "—"])
        out.append({"ticker": t, "close_2026_09_30": c0, "close_latest": c1, "date_latest": p.get("date_latest"), "change_pct": chg,
                    "pe_ntm_new": pe_new, "peg_lt_new": peg_new, "source": p.get("source", "")})
    qqq = next((p for p in N.get("prices", []) if p["ticker"] == "QQQ"), None)
    qchg = qqq.get("change_pct") if qqq else None
    if qchg is None and qqq and qqq.get("close_2026_09_30") and qqq.get("close_latest"):
        qchg = (qqq["close_latest"] / qqq["close_2026_09_30"] - 1) * 100
    rows.append(["**Portefeuille (poids retenus)**", "", "", "", pct(pf_move), "", ""])
    tab = ["| Valeur | Clôture 30/09 | Dernière clôture | Date | Variation | P/E NTM (30/09 → aujourd'hui) | PEG LT (30/09 → aujourd'hui) |", "|---|---|---|---|---|---|---|"]
    tab += ["| " + " | ".join(r) + " |" for r in rows]
    open(os.path.join(ROOT, "redaction", "NEWS_PRICES.md"), "w", encoding="utf-8").write("\n".join(tab) + "\n")
    cal = ["| Date | Événement | Ligne |", "|---|---|---|"] + [f"| {c.get('date', '')} | {c.get('event', '')} | {c.get('ticker', '')} |" for c in N.get("calendar", [])]
    open(os.path.join(ROOT, "redaction", "NEWS_CALENDAR.md"), "w", encoding="utf-8").write("\n".join(cal) + "\n")
    with open(os.path.join(ROOT, "outputs", "news_prices.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    json.dump({"as_of": N.get("as_of"), "pf_move_pct": pf_move, "qqq_move_pct": qchg, "prices": out},
              open(os.path.join(ROOT, "outputs", "news.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"portefeuille {pf_move:+.2f} % ; QQQ {qchg if qchg is not None else 'n.d.'} ; {len(N.get('items', []))} nouvelles ; {len(N.get('calendar', []))} dates")


if __name__ == "__main__":
    main()
