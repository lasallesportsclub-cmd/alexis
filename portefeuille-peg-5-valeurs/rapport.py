#!/usr/bin/env python3
"""
Assemble le rapport Markdown (et le contenu de l'article) à partir des sorties du modèle (outputs/resume.json, CSV)
et d'un gabarit de rédaction contenant des balises {{...}}. Tous les chiffres des tableaux viennent du modèle ;
aucun n'est recopié à la main. Bibliothèque standard uniquement.

Usage : python3 rapport.py --template redaction/RAPPORT_template.md --out RAPPORT.md
"""
import argparse
import csv
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
CUR = {"USD": "$", "EUR": "€", "JPY": "¥", "TWD": "NT$", "KRW": "₩", "HKD": "HK$", "CNY": "CN¥", "INR": "₹", "GBP": "£",
       "GBX": "p", "CHF": "CHF", "SEK": "SEK", "DKK": "DKK", "NOK": "NOK", "BRL": "R$", "MXN": "MX$"}


def fr(x, d=1):
    """Nombre au format français (1 234,5)."""
    if x is None or x == "":
        return "n.d."
    x = float(x)
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s


def pct(x, d=1, sign=True):
    if x is None or x == "":
        return "n.d."
    x = float(x) * 100
    s = f"{x:+.{d}f}" if sign else f"{x:.{d}f}"
    return s.replace(".", ",") + " %"


def pctraw(x, d=1, sign=True):
    """x déjà en pour cent."""
    if x is None or x == "":
        return "n.d."
    x = float(x)
    s = f"{x:+.{d}f}" if sign else f"{x:.{d}f}"
    return s.replace(".", ",") + " %"


def money(x, cur, d=2):
    if x is None or x == "":
        return "n.d."
    sym = CUR.get(cur, cur)
    x = float(x)
    if abs(x) >= 1000:
        d = 0
    return f"{fr(x, d)} {sym}"


def table(header, rows, align=None):
    align = align or ["---"] * len(header)
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(align) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


class Rapport:
    def __init__(self, outdir, datadir):
        self.R = json.load(open(os.path.join(outdir, "resume.json"), encoding="utf-8"))
        self.data = {r["ticker"]: r for r in csv.DictReader(open(os.path.join(datadir, "data.csv"), encoding="utf-8"))}
        self.hyp = {r["ticker"]: r for r in csv.DictReader(open(os.path.join(datadir, "hypotheses.csv"), encoding="utf-8"))}
        self.quintets = list(csv.DictReader(open(os.path.join(outdir, "quintets.csv"), encoding="utf-8")))
        self.classement = list(csv.DictReader(open(os.path.join(outdir, "classement.csv"), encoding="utf-8")))
        self.exclus = list(csv.DictReader(open(os.path.join(outdir, "exclus.csv"), encoding="utf-8")))
        self.indice = list(csv.DictReader(open(os.path.join(outdir, "indice.csv"), encoding="utf-8")))
        self.V = self.R["valeurs"]
        self.pf = self.R["portefeuille"]
        self.ix = self.R["indice"]
        self.weights = {l["ticker"]: l["poids"] for l in self.pf["lignes"]}
        # historiques (research/histoire/histoire.json), facultatif
        self.hist = {}
        hp = os.environ.get("PEG_HISTOIRE", os.path.join(ROOT, "..", "research", "histoire", "histoire.json"))
        if os.path.exists(hp):
            try:
                for h in json.load(open(hp, encoding="utf-8")):
                    self.hist[h["ticker"]] = h
            except Exception as e:
                print("histoire.json illisible :", e)

    # ------------------------------------------------------------------
    def v(self, t):
        return self.V[t]

    def cur(self, t):
        return self.data[t]["currency"]

    def name(self, t):
        return self.data[t]["name"]

    def tab_verdict(self):
        rows = []
        for t, w in self.weights.items():
            v, s = self.v(t), self.v(t)["scen"]
            rows.append([f"**{self.name(t)}** ({t})", self.data[t]["theme"], pct(w, 0, False), money(v["price"], self.cur(t)),
                         fr(v["pe_ntm"]), pctraw(v["g_n1"], 0), fr(v["peg_n1"], 2) if v["peg_n1"] else "n.d.",
                         f"{self.hyp[t]['g_central']} %", fr(v["peg_lt"], 2),
                         f"**{pct(s['expected']['annual'])}**", f"{pct(s['pess']['annual'])} / {pct(s['central']['annual'])} / {pct(s['opt']['annual'])}",
                         money(s["central"]["price_end"], self.cur(t)), money(v["buy_peg1"], self.cur(t))])
        return table(["Valeur", "Thème", "Poids", "Cours 30/09", "P/E NTM", "Croiss. BPA 2027", "PEG 2027", "Croiss. retenue (hyp.)",
                      "PEG LT", "Rendement annuel espéré", "Pess. / central / opt.", "Cours 2030 (central)", "Zone d'achat (PEG 1)"], rows)

    def tab_verdict_court(self):
        rows = []
        for t, w in self.weights.items():
            v, s = self.v(t), self.v(t)["scen"]
            rows.append([f"**{self.name(t)}**", self.data[t]["theme"], pct(w, 0, False), money(v["price"], self.cur(t)), fr(v["pe_ntm"]),
                         pctraw(v["g_n1"], 0), fr(v["peg_lt"], 2), f"**{pct(s['expected']['annual'])}**", money(s["central"]["price_end"], self.cur(t)),
                         money(v["buy_peg1"], self.cur(t))])
        rows.append(["**Portefeuille**", "", "100 %", "", fr(self.pf["pe_ntm"]), pctraw(self.pf["g_n1"], 0), fr(self.pf["peg_lt"], 2),
                     f"**{pct(self.pf['rendement_annuel']['expected'])}**", "", ""])
        rows.append(["Nasdaq 100 reconstitué", "", "", "", fr(self.ix["pe_ntm"]), pctraw(self.ix["g_n1"], 0),
                     fr(self.ix["pe_ntm"] / max(self.ix["g_central"], 0.01), 2), pct(self.ix["rendement_annuel"]["expected"]), "", ""])
        return table(["Valeur", "Thème", "Poids", "Cours 30/09", "P/E 12 mois", "BPA 2027", "PEG long terme", "Espéré", "Cours 2030 (central)", "Zone d'achat"], rows)

    def tab_vs_indice(self):
        pf, ix = self.pf, self.ix
        eq = pf["equipondere_rendement_annuel"]
        rows = [
            ["P/E des 12 prochains mois", fr(pf["pe_ntm"]), fr(ix["pe_ntm"]), "—"],
            ["Croissance du BPA 2027 (consensus, pondérée)", pctraw(pf["g_n1"], 0), pctraw(ix["g_n1"], 0), "—"],
            ["Croissance retenue 2027-2031 (hyp., pondérée)", pctraw(pf["g_central"], 1), pctraw(ix["g_central"], 1), "—"],
            ["PEG long terme", fr(pf["peg_lt"], 2), fr(ix["pe_ntm"] / max(ix["g_central"], 0.01), 2), "—"],
            ["Bêta", fr(pf["beta"], 2), fr(ix["beta"], 2), "—"],
            ["Rendement annuel, scénario pessimiste", pct(pf["rendement_annuel"]["pess"]), pct(ix["rendement_annuel"]["pess"]), pct(eq["pess"])],
            ["Rendement annuel, scénario central", pct(pf["rendement_annuel"]["central"]), pct(ix["rendement_annuel"]["central"]), pct(eq["central"])],
            ["Rendement annuel, scénario optimiste", pct(pf["rendement_annuel"]["opt"]), pct(ix["rendement_annuel"]["opt"]), pct(eq["opt"])],
            ["**Rendement annuel espéré (25/50/25)**", f"**{pct(pf['rendement_annuel']['expected'])}**", f"**{pct(ix['rendement_annuel']['expected'])}**", pct(eq["expected"])],
            ["Valeur de 100 investis en 2030 (espérance)", fr(100 * pf["valeur_terminale"]["expected"], 0), fr(100 * ix["valeur_terminale"]["expected"], 0), "—"],
        ]
        return table(["", "Portefeuille", f"Nasdaq 100 reconstitué ({ix['n_lignes']} lignes, {fr(ix['couverture_poids_pct'])} % du poids)", "Portefeuille équipondéré"], rows)

    def tab_classement(self, n=25):
        rows = []
        for r in self.classement[:n]:
            t = r["ticker"]
            v = self.v(t)
            rows.append([r["rang"], f"{self.name(t)} ({t})", self.data[t]["region"], fr(v["pe_ntm"]), pctraw(v["g_n1"], 0),
                         fr(v["peg_n1"], 2) if v["peg_n1"] else "n.d.", f"{self.hyp[t]['g_central']} %", fr(v["peg_lt"], 2),
                         pct(v["scen"]["expected"]["annual"]), pct(v["scen"]["pess"]["annual"]), fr(float(r["score"]), 0)])
        return table(["Rang", "Valeur", "Région", "P/E NTM", "Croiss. 2027", "PEG 2027", "Croiss. retenue", "PEG LT", "Espéré", "Pessimiste", "Score"], rows)

    def tab_exclus(self):
        rows = []
        for r in sorted(self.exclus, key=lambda r: -float(r["rdt espéré %"])):
            t = r["ticker"]
            rows.append([f"{self.name(t)} ({t})", self.data[t]["region"], r["raison"], fr(self.v(t)["pe_ntm"]),
                         pctraw(r["rdt espéré %"])])
        return table(["Valeur", "Région", "Raison", "P/E NTM", "Rendement espéré"], rows)

    def tab_quintets(self, n=12):
        rows = []
        ret = set(self.weights)
        for i, q in enumerate(self.quintets[:n], 1):
            tick = q["valeurs"].split()
            mark = "**" if set(tick) == ret else ""
            rows.append([i, f"{mark}{' + '.join(tick)}{mark}", q["P/E NTM"].replace(".", ","), pctraw(q["croiss. N+1 %"], 0),
                         q["PEG LT"].replace(".", ","), q["n thème dominant"], pctraw(q["rdt espéré %"]), pctraw(q["rdt pess %"]),
                         pctraw(q["rdt central %"]), pctraw(q["rdt opt %"]), pctraw(q["pire cas % (pess, −5 pts, multiples figés)"])])
        if self.R.get("quintet_rang") and self.R["quintet_rang"] > n:
            q = self.R["quintet_retenu"]
            rows.append([self.R["quintet_rang"], f"**{' + '.join(q['tickers'])}** (retenu)", fr(q["pe_ntm"]), pctraw(q["g_n1"], 0),
                         fr(q["peg_lt"], 2), q["dominant_theme_n"], pct(q["expected"]), pct(q["pess"]), pct(q["central"]), pct(q["opt"]), pct(q["worst_case"])])
        return table(["Rang", "Quintet (poids égaux)", "P/E NTM", "Croiss. 2027", "PEG LT", "Thème dominant (n)", "Espéré", "Pess.", "Central", "Opt.", "Pire cas*"], rows)

    def tab_stress(self):
        ixc = self.ix["rendement_annuel"]["central"]
        rows = []
        for k, val in self.R["stress_tests_rendement_annuel"].items():
            rows.append([k, pct(val), pct(ixc), pctraw((val - ixc) * 100, 1).replace(" %", " pt")])
        return table(["Scénario (valeurs visées en pessimiste, le reste en central)", "Portefeuille", "Nasdaq 100 (central)", "Écart"], rows)

    def tab_sens(self):
        rows = []
        ixs = self.ix["sensibilites_rendement_annuel"]
        mp = {"multiples figés": "multiples figés", "croissance −5 pts": "croissance −5 pts", "multiples figés et croissance −5 pts": "multiples figés et −5 pts"}
        for k, val in self.R["sensibilites_rendement_annuel"].items():
            iv = ixs.get(mp.get(k, ""), None)
            rows.append([k, pct(val), pct(iv) if iv is not None else pct(self.ix["rendement_annuel"]["expected"]) + " (espérance)"])
        rows.append(["Indice : bénéfices des cycliques (mémoire) maintenus au pic", "—", pct(ixs["benefices cycliques maintenus au pic"])])
        return table(["Sensibilité (rendement annuel espéré)", "Portefeuille", "Nasdaq 100"], rows)

    def tab_lignes(self):
        rows = []
        base = self.pf["rendement_annuel"]["expected"]
        d = self.R["sensibilites_par_ligne_rendement_annuel"]
        for t in self.weights:
            rows.append([f"{self.name(t)} ({t})", pct(d.get(f"{t} -5 pts")), pct(d.get(f"{t} +5 pts")),
                         pctraw((d.get(f"{t} +5 pts") - d.get(f"{t} -5 pts")) * 100, 1).replace(" %", " pt")])
        return table(["Ligne", "Croissance retenue −5 pts", "Croissance retenue +5 pts", "Amplitude"], rows) + f"\n\nEspérance de référence : {pct(base)}."

    def tab_proba(self):
        p = self.R["probabilites"]
        c = self.R["concentration"]
        rows = [["Portefeuille retenu (5 lignes, poids retenus)", pct(self.pf["rendement_annuel"]["expected"]), pct(self.pf["rendement_annuel"]["pess"]),
                 pct(p["p_below_index_central"], 1, False), pct(p["p_loss"], 1, False)]]
        for n in ("3", "4", "5"):
            k = c.get(n)
            if k:
                rows.append([f"{n} lignes à poids égaux ({', '.join(k['tickers'])})", pct(k["expected"]), pct(k["pess"]), pct(k["p_below"], 1, False), pct(k["p_loss"], 1, False)])
        return table(["Composition", "Espéré", "Tout en pessimiste", "Probabilité de finir sous l'indice*", "Probabilité de perdre de l'argent*"], rows)

    def fiche(self, t):
        v, d, h = self.v(t), self.data[t], self.hyp[t]
        cur = self.cur(t)
        fy = v["fy"]
        rows = [
            ["Cours (clôture du 30/09/2026) / capitalisation", f"{money(v['price'], cur)} / {fr(v['mcap_usd_bn'], 1)} Md$" if v.get("mcap_usd_bn") else money(v["price"], cur)],
            ["Cotation à utiliser / PEA", f"{d['listing']} / {d['pea'] or 'n.d.'}"],
            ["Exercice clos en", f"mois {v['fy_end_month']}"],
            ["BPA non-GAAP par exercice (consensus)", " → ".join(f"FY{y} : {fr(fy[str(y)], 2)}" for y in (2025, 2026, 2027, 2028) if fy.get(str(y)) is not None)],
            ["BPA années civiles 2026 → 2027", f"{fr(v['cy2026'], 2)} → {fr(v['cy2027'], 2)} ({pctraw(v['g_n1'], 0)})"],
            ["BPA des 12 prochains mois (NTM)", fr(v["eps_ntm"], 2)],
            ["P/E NTM / P/E 2027", f"{fr(v['pe_ntm'])} / {fr(v['pe_n1'])}"],
            ["PEG 2027 / PEG long terme", f"{fr(v['peg_n1'], 2) if v['peg_n1'] else 'n.d.'} / {fr(v['peg_lt'], 2)}"],
            ["Croissance retenue 2027-2031 (hyp.) pess. / central / opt.", f"{h['g_pess']} % / {h['g_central']} % / {h['g_opt']} %"],
            ["Plafond de P/E de sortie", h["pe_cap"]],
            ["Croissance de long terme du consensus (LTG)", f"{fr(v['ltg_consensus'], 1)} %" if v.get("ltg_consensus") else "n.d."],
            ["Bêta / rendement du dividende", f"{fr(v['beta'], 2) if v.get('beta') else 'n.d.'} / {fr(v['div_yield'], 2)} %"],
            ["Plus bas / plus haut 52 semaines", f"{money(d['w52_low'], cur)} / {money(d['w52_high'], cur)}" if d.get("w52_low") else "n.d."],
            ["Objectif de cours moyen (analystes)", money(d["target"], cur) if d.get("target") else "n.d."],
            ["Zacks Rank", str(d["zacks_rank"]).replace(".0", "") if d["zacks_rank"] else "n.d."],
            ["Zone d'achat de Lynch (PEG LT = 1) / forte sécurité (PEG 0,8)", f"{money(v['buy_peg1'], cur)} / {money(v['buy_peg08'], cur)}"],
            ["Source des données", d["source_note"][:160]],
        ]
        return table(["", ""], rows)

    def scen(self, t):
        v = self.v(t)
        cur = self.cur(t)
        rows = []
        for s, lab in (("pess", "Pessimiste"), ("central", "Central"), ("opt", "Optimiste")):
            x = v["scen"][s]
            rows.append([lab, f"{x['g']} %" if x["g"] is not None else "multiple de BPA", fr(x["pe_exit"]), money(x["eps_end"], cur),
                         money(x["price_end"], cur), pct(x["annual"])])
        e = v["scen"]["expected"]
        rows.append(["**Espéré (25/50/25)**", "", "", "", "", f"**{pct(e['annual'])}**"])
        return table(["Scénario", "Croissance BPA/an", "P/E de sortie", "BPA 2030", "Cours 2030", "Rendement annuel"], rows)

    def tab_etf(self):
        rows = []
        for k, v in self.R["poche_etf"].items():
            rows.append([k, pct(v["expected"]), pct(v["double_choc"]), pct(v["tout_pess"])])
        return table(["Part de l'ETF Nasdaq 100", "Espéré", "Double choc (deux plus grosses lignes en pessimiste)", "Tout en pessimiste"], rows)

    def tab_variantes(self):
        rows = []
        for v in self.R["variantes"]:
            rows.append([v["nom"], fr(v["pe_ntm"]), pctraw(v["g_n1"], 0), fr(v["peg_lt"], 2), pct(v["part_ia"], 0, False), fr(v["beta"], 2),
                         f"**{pct(v['expected'])}**", pct(v["pess"]), pct(v["double_choc"]), pct(v["krach_ia"]), pct(v["pire_cas"]),
                         pct(v["p_below"], 1, False)])
        return table(["Variante", "P/E NTM", "Croiss. 2027", "PEG LT", "Part IA", "Bêta", "Espéré", "Tout pess.", "Double choc", "Krach IA", "Pire cas*", "P(sous l'indice)"], rows)

    def tab_cycliques(self, tickers=("MU", "000660.KS")):
        rows = []
        labels = None
        cols = []
        for t in tickers:
            c = self.R["cycliques"].get(t)
            if not c:
                continue
            cols.append(t)
            if labels is None:
                labels = [(r["benefices_2030"], r["pe_sortie"]) for r in c]
        if not cols:
            return ""
        for i, (lab, pe) in enumerate(labels):
            rows.append([lab, pe] + [pct(self.R["cycliques"][t][i]["annuel"]) for t in cols])
        return table(["Bénéfices 2030 vs aujourd'hui", "P/E de sortie"] + [f"{self.name(t)} ({t})" for t in cols], rows)

    def tab_dilution(self):
        rows = []
        for k, v in self.R["dilution"].items():
            t, f = k.split(":")
            rows.append([f"{self.name(t)} : BPA 2030 × {fr(float(f), 3)}", pct(v["ligne_expected"]), pct(v["expected"]), pct(v["central"])])
        return table(["Cas", "Espéré de la ligne", "Espéré du portefeuille", "Central du portefeuille"], rows)

    def tab_indice(self, n=20):
        rows = []
        for r in self.indice[:n]:
            t = r["ticker"]
            rows.append([f"{self.name(t)} ({t})", r["poids brut %"].replace(".", ","), r["poids renormalisé %"].replace(".", ","),
                         r["P/E NTM"].replace(".", ","), f"{r['g central']} %" if r["g central"] else "cyclique", r["PEG LT"].replace(".", ",") or "—",
                         pctraw(r["rdt espéré %"])])
        return table(["Composant", "Poids QQQ", "Poids renormalisé", "P/E NTM", "Croiss. retenue", "PEG LT", "Espéré"], rows)

    def tab_univers(self):
        rows = []
        order = sorted(self.V.values(), key=lambda m: -(m.get("score") if m.get("score") is not None else -999))
        for v in order:
            t = v["ticker"]
            d = self.data[t]
            rows.append([f"{self.name(t)} ({t})", d["region"], d["theme"], money(v["price"], d["currency"]), fr(v["pe_ntm"]),
                         pctraw(v["g_n1"], 0) if v["g_n1"] is not None else "n.d.", f"{self.hyp[t]['g_central']} %" if not v["cyclical"] else "cyclique",
                         fr(v["peg_lt"], 2) if v["peg_lt"] else "—", pct(v["scen"]["expected"]["annual"]), fr(v["score"], 0) if v.get("score") is not None else "exclu"])
        return table(["Valeur", "Région", "Thème", "Cours", "P/E NTM", "Croiss. 2027", "Croiss. retenue", "PEG LT", "Espéré", "Score"], rows)

    def tab_hypotheses(self):
        rows = []
        for t, h in self.hyp.items():
            if t not in self.V:
                continue
            if h["g_central"]:
                rows.append([f"{self.name(t)} ({t})", f"{h['g_pess']} / {h['g_central']} / {h['g_opt']}", h["pe_cap"], h["justification"]])
            else:
                rows.append([f"{self.name(t)} ({t})", f"cyclique : BPA 2030 = {h['cyc_mult_pess']} / {h['cyc_mult_central']} / {h['cyc_mult_opt']} × NTM",
                             f"P/E {h['cyc_pe_pess']} / {h['cyc_pe_central']} / {h['cyc_pe_opt']}", h["justification"]])
        return table(["Valeur", "Croissance pess. / central / opt. (%)", "Plafond P/E", "Justification"], rows)

    def tab_sources(self):
        rows = []
        for t, d in self.data.items():
            if t in self.V:
                rows.append([f"{self.name(t)} ({t})", d["price_source"], d["source_note"]])
        return table(["Valeur", "Cours", "Consensus et données"], rows)

    def tab_hist(self, t):
        h = self.hist.get(t)
        if not h or not h.get("financials"):
            return f"<!-- historique manquant : {t} -->"
        cur = self.cur(t)
        rows = []
        for f in h["financials"]:
            rev = f.get("revenue")
            rc = f.get("revenue_currency") or cur
            unit = {"USD": "Md$", "EUR": "Md€", "TWD": "Md NT$"}.get(rc, rc)
            rows.append([f.get("year"), f"{fr(rev, 1)} {unit}" if rev is not None else "n.d.",
                         pctraw(f["revenue_growth_pct"], 0) if f.get("revenue_growth_pct") is not None else "n.d.",
                         (fr(f["op_margin_pct"], 1) + " %") if f.get("op_margin_pct") is not None else "n.d.",
                         fr(f["eps"], 2) if f.get("eps") is not None else "n.d.",
                         (fr(f["fcf"], 1) + " " + unit) if f.get("fcf") is not None else "n.d.",
                         fr(f["shares_m"], 0) if f.get("shares_m") is not None else "n.d."])
        basis = next((f.get("eps_basis") for f in h["financials"] if f.get("eps_basis")), "")
        rc0 = h["financials"][0].get("revenue_currency") or cur
        sym = {"USD": "$", "EUR": "€", "TWD": "NT$"}.get(rc0, rc0)
        return table(["Exercice", "Chiffre d'affaires", "Croissance", "Marge opérationnelle", f"BPA en {sym} ({basis})" if basis else f"BPA en {sym}", "Flux de trésorerie libre", "Actions (M)"], rows)

    def timeline(self, t):
        h = self.hist.get(t)
        if not h or not h.get("milestones"):
            return f"<!-- chronologie manquante : {t} -->"
        out = []
        for m in h["milestones"]:
            amt = f" ({m['amount']})" if m.get("amount") else ""
            out.append(f"- **{m.get('date', '')}** : {m.get('event', '')}{amt}")
        return "\n".join(out)

    def render(self, template):
        out = template
        # inclusions de fichiers de rédaction : {{include:chemin}} (relatif au dossier redaction/)
        def inc(m):
            path = os.path.join(ROOT, "redaction", m.group(1))
            return open(path, encoding="utf-8").read().strip() if os.path.exists(path) else f"<!-- manquant : {m.group(1)} -->"
        for _ in range(3):
            out = re.sub(r"\{\{include:([^}]+)\}\}", inc, out)
        simple = {"tab_verdict": self.tab_verdict, "tab_verdict_court": self.tab_verdict_court, "tab_vs_indice": self.tab_vs_indice, "tab_classement": self.tab_classement,
                  "tab_exclus": self.tab_exclus, "tab_quintets": self.tab_quintets, "tab_stress": self.tab_stress,
                  "tab_sens": self.tab_sens, "tab_lignes": self.tab_lignes, "tab_proba": self.tab_proba, "tab_indice": self.tab_indice,
                  "tab_univers": self.tab_univers, "tab_hypotheses": self.tab_hypotheses, "tab_sources": self.tab_sources,
                  "tab_etf": self.tab_etf, "tab_variantes": self.tab_variantes, "tab_cycliques": self.tab_cycliques, "tab_dilution": self.tab_dilution}
        for k, fn in simple.items():
            out = out.replace("{{" + k + "}}", fn())
        out = out.replace("{{nb_quintets}}", str(len(self.quintets)))
        out = out.replace("{{nb_univers}}", str(len(self.V)))
        for m in re.findall(r"\{\{(fiche|scen|hist|timeline):([A-Za-z0-9.\-]+)\}\}", out):
            kind, t = m
            fn = {"fiche": self.fiche, "scen": self.scen, "hist": self.tab_hist, "timeline": self.timeline}[kind]
            out = out.replace("{{" + kind + ":" + t + "}}", fn(t))
        # scalaires d'historique : {{hs:TICKER:champ}} (champs de premier niveau ou de stock)
        def hscalar(m):
            t, field = m.group(1), m.group(2)
            h = self.hist.get(t)
            if not h:
                return "n.d."
            v = h.get(field, (h.get("stock") or {}).get(field))
            if v is None:
                return "n.d."
            if field.endswith("_pct"):
                return pctraw(v, 0)
            if isinstance(v, float):
                return fr(v, 2)
            return str(v)
        out = re.sub(r"\{\{hs:([A-Za-z0-9.\-]+):([a-z_0-9]+)\}\}", hscalar, out)
        # valeurs scalaires : {{v:TICKER:champ}} et {{pf:champ}} / {{ix:champ}}
        def scalar(m):
            kind, t, field = m.group(1), m.group(2), m.group(3)
            if kind == "v":
                v = self.v(t)
                if field == "price":
                    return money(v["price"], self.cur(t))
                if field in ("pe_ntm", "pe_n1"):
                    return fr(v[field])
                if field in ("peg_lt", "peg_n1"):
                    return fr(v[field], 2)
                if field == "g_n1":
                    return pctraw(v["g_n1"], 0)
                if field in ("expected", "pess", "central", "opt"):
                    return pct(v["scen"][field]["annual"])
                if field in ("price_central", "price_pess", "price_opt"):
                    return money(v["scen"][field.split("_")[1]]["price_end"], self.cur(t))
                if field in ("buy_peg1", "buy_peg08"):
                    return money(v[field], self.cur(t))
                if field == "eps_ntm":
                    return fr(v["eps_ntm"], 2)
                if field == "weight":
                    return pct(self.weights.get(t, 0), 0, False)
                if field in ("g_pess", "g_central", "g_opt", "pe_cap"):
                    return str(self.hyp[t][field]).replace(".0", "")
                if field in ("w52_low", "w52_high", "target"):
                    return money(self.data[t][field], self.cur(t)) if self.data[t].get(field) else "n.d."
                if field.startswith("pe_exit_"):
                    return fr(v["scen"][field[8:]]["pe_exit"])
                if field.startswith("eps_end_"):
                    return money(v["scen"][field[8:]]["eps_end"], self.cur(t))
                if field in ("cy2026", "cy2027", "cy2028"):
                    return fr(v[field], 2)
                if field == "g_n2":
                    return pctraw(v["g_n2"], 0)
                if field == "mcap":
                    return fr(v["mcap_usd_bn"], 0) + " Md$"
                if field == "ltg":
                    return (fr(v["ltg_consensus"], 1) + " %") if v.get("ltg_consensus") else "n.d."
                return str(v.get(field, "n.d."))
            if kind == "pf":
                if field in ("expected", "pess", "central", "opt"):
                    return pct(self.pf["rendement_annuel"][field])
                if field == "pe_ntm":
                    return fr(self.pf["pe_ntm"])
                if field == "peg_lt":
                    return fr(self.pf["peg_lt"], 2)
                if field == "g_n1":
                    return pctraw(self.pf["g_n1"], 0)
                if field == "beta":
                    return fr(self.pf["beta"], 2)
                if field == "p_below":
                    return pct(self.R["probabilites"]["p_below_index_central"], 1, False)
                if field == "p_loss":
                    return pct(self.R["probabilites"]["p_loss"], 1, False)
                if field == "worst":
                    return pct(self.R["sensibilites_rendement_annuel"]["pire combinaison (tout pessimiste, −5 pts, multiples figés)"])
                if field == "double":
                    return pct(self.R["stress_tests_rendement_annuel"]["double choc (2 plus grosses lignes en pessimiste)"])
                if field == "tv":
                    return fr(100 * self.pf["valeur_terminale"]["expected"], 0)
                if field == "g_central":
                    return pctraw(self.pf["g_central"], 1)
                if field == "eq_expected":
                    return pct(self.pf["equipondere_rendement_annuel"]["expected"])
            if kind == "ix":
                if field in ("expected", "pess", "central", "opt"):
                    return pct(self.ix["rendement_annuel"][field])
                if field == "pe_ntm":
                    return fr(self.ix["pe_ntm"])
                if field == "g_n1":
                    return pctraw(self.ix["g_n1"], 0)
                if field == "couverture":
                    return fr(self.ix["couverture_poids_pct"]) + " %"
                if field == "n":
                    return str(self.ix["n_lignes"])
                if field == "peak":
                    return pct(self.ix["sensibilites_rendement_annuel"]["benefices cycliques maintenus au pic"])
                if field == "peg_lt":
                    return fr(self.ix["pe_ntm"] / max(self.ix["g_central"], 0.01), 2)
                if field == "g_central":
                    return pctraw(self.ix["g_central"], 1)
                if field == "beta":
                    return fr(self.ix["beta"], 2)
                if field == "tv":
                    return fr(100 * self.ix["valeur_terminale"]["expected"], 0)
            return m.group(0)
        out = re.sub(r"\{\{(v|pf|ix):(?:([A-Za-z0-9.\-]+):)?([a-z_0-9]+)\}\}", scalar, out)

        # stress tests et sensibilités : {{stress:clé}} / {{sens:clé}} (clés telles qu'écrites dans resume.json)
        def keyed(m):
            kind, key = m.group(1), m.group(2).strip()
            src = self.R["stress_tests_rendement_annuel"] if kind == "stress" else self.R["sensibilites_rendement_annuel"]
            return pct(src[key]) if key in src else m.group(0)
        out = re.sub(r"\{\{(stress|sens):([^}]+)\}\}", keyed, out)

        # variantes, poche d'ETF, concentration, dilution : {{var:Y:expected}}, {{etf:10 %:expected}}, {{conc:3:p_below}}, {{dil:NU:0.868:expected}}
        def multi(m):
            kind, key, field = m.group(1), m.group(2).strip(), m.group(3)
            if kind == "var":
                v = next((x for x in self.R["variantes"] if x["nom"].startswith(key)), None)
                if not v:
                    return m.group(0)
                if field in ("expected", "pess", "central", "opt", "double_choc", "krach_ia", "pire_cas"):
                    return pct(v[field])
                if field == "p_below":
                    return pct(v["p_below"], 1, False)
                if field == "part_ia":
                    return pct(v["part_ia"], 0, False)
                if field in ("peg_lt", "beta"):
                    return fr(v[field], 2)
                if field == "pe_ntm":
                    return fr(v["pe_ntm"])
                return str(v.get(field, m.group(0)))
            if kind == "etf":
                v = self.R["poche_etf"].get(key)
                return pct(v[field]) if v and field in v else m.group(0)
            if kind == "conc":
                v = self.R["concentration"].get(key)
                if not v:
                    return m.group(0)
                if field in ("p_below", "p_loss"):
                    return pct(v[field], 1, False)
                return pct(v[field]) if field in v else m.group(0)
            if kind == "dil":
                v = self.R["dilution"].get(key)
                return pct(v[field]) if v and field in v else m.group(0)
            return m.group(0)
        out = re.sub(r"\{\{(var|etf|conc|dil):([^}]+?):([a-z_]+)\}\}", multi, out)

        # scénarios d'acquisition (outputs/acquisition.json) : {{acq:A:dilution_pct}} (lettre = début du nom du scénario)
        acq_path = os.path.join(os.path.dirname(self.R_path) if hasattr(self, "R_path") else os.path.join(ROOT, "outputs"), "acquisition.json")
        acq = json.load(open(acq_path, encoding="utf-8")) if os.path.exists(acq_path) else None
        def acqf(m):
            key, field = m.group(1).strip(), m.group(2)
            if not acq:
                return m.group(0)
            if key == "base":
                v = {"line_expected": acq["base_line_expected"], "pf_expected": acq["base_pf_expected"]}.get(field)
                return pct(v) if v is not None else m.group(0)
            sc = next((v for k, v in acq["scenarios"].items() if k.startswith(key)), None)
            if not sc or field not in sc:
                return m.group(0)
            v = sc[field]
            if field in ("dilution_pct", "part_actions"):
                return pct(v, 1, False)
            if field in ("accretion_bpa_2027", "ligne_expected", "pf_expected", "pf_central", "pf_pess"):
                return pct(v)
            if field == "facteur_bpa_2030_central":
                return pct(v - 1)
            if field == "prix_sur_resultat_cible":
                return fr(v, 0) + "x"
            if field == "prix_sur_capi_nu":
                return pct(v, 0, False)
            if field == "actions_nouvelles_md":
                return fr(v * 1000, 0) + " M"
            if field in ("prix_md_gbp", "prix_md_usd"):
                return fr(v, 1)
            return str(v)
        out = re.sub(r"\{\{acq:([^}]+?):([a-z_0-9]+)\}\}", acqf, out)

        # revue de presse (outputs/news.json) : {{news:pf_move}}, {{news:qqq_move}}, {{news:NU:change_pct}}
        news_path = os.path.join(ROOT, "outputs", "news.json")
        news = json.load(open(news_path, encoding="utf-8")) if os.path.exists(news_path) else None
        def newsf(m):
            a, b = m.group(1), m.group(2)
            if not news:
                return m.group(0)
            if b is None:
                v = {"pf_move": news.get("pf_move_pct"), "qqq_move": news.get("qqq_move_pct"), "as_of": news.get("as_of")}.get(a)
                if a == "as_of":
                    return str(v)
                return (pctraw(v, 1) if v is not None else "n.d.")
            p = next((x for x in news["prices"] if x["ticker"] == a), None)
            if not p or p.get(b) is None:
                return "n.d."
            v = p[b]
            if b == "change_pct":
                return pctraw(v, 1)
            if b in ("pe_ntm_new",):
                return fr(v, 1)
            if b in ("peg_lt_new",):
                return fr(v, 2)
            if b in ("close_latest", "close_2026_09_30"):
                return money(v, self.cur(a)) if a in self.data else fr(v, 2) + " $"
            return str(v)
        out = re.sub(r"\{\{news:([A-Za-z0-9.\-_]+)(?::([a-z_0-9]+))?\}\}", newsf, out)
        return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--outputs", default=os.path.join(ROOT, "outputs"))
    ap.add_argument("--data", default=os.path.join(ROOT, "data"))
    a = ap.parse_args()
    r = Rapport(a.outputs, a.data)
    tpl = open(a.template, encoding="utf-8").read()
    txt = r.render(tpl)
    left = re.findall(r"\{\{[^}]+\}\}", txt)
    if left:
        print("balises non résolues :", sorted(set(left))[:20])
    open(a.out, "w", encoding="utf-8").write(txt)
    print("écrit", a.out, len(txt), "caractères")


if __name__ == "__main__":
    main()
