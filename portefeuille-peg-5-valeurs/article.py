#!/usr/bin/env python3
"""
Génère l'article de journal (HTML autonome, thèmes clair/sombre, lisible sur mobile) à partir de :
  - outputs/resume.json  (sorties du moteur portefeuille.py)
  - article/contenu.md   (texte de l'article en Markdown léger : #, ##, ###, paragraphes, listes, tableaux, **gras**)
Infographies SVG inline : fourchettes de scénarios, barres comparatives, nuage P/E contre croissance.
Bibliothèque standard uniquement.

Usage : python3 article.py --resume outputs/resume.json --content article/contenu.md --out article.html
"""
import argparse
import html
import json
import os
import re

JOURNAL = "La Gazette du PEG"
DISCLAIMER_TITLE = ("Titre de journal fictif : « La Gazette du PEG » ne correspond à aucune publication existante. "
                    "Analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé.")


# ----------------------------------------------------------------------------
# Markdown léger → HTML
# ----------------------------------------------------------------------------
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\[(.+?)\]\((https?://[^\s)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


def md_to_html(md):
    out, i = [], 0
    lines = md.splitlines()
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("<!--"):
            out.append(ln)  # marqueur d'infographie (remplacé plus tard) ou commentaire
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", ln)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            if len(cells) >= 2 and all(re.match(r"^:?-{2,}:?$", c) for c in cells[1]):
                head, body = cells[0], cells[2:]
            else:
                head, body = None, cells
            t = ['<div class="tablewrap"><table>']
            if head:
                t.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead>")
            t.append("<tbody>")
            for r in body:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        if re.match(r"^\s*[-*]\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        if re.match(r"^\s*\d+[.)]\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+[.)]\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+[.)]\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            continue
        if ln.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> "))
                i += 1
            out.append("<blockquote>" + inline(" ".join(quote)) + "</blockquote>")
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|\||\s*[-*]\s|\s*\d+[.)]\s|>|<!--)", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


# ----------------------------------------------------------------------------
# Infographies SVG
# ----------------------------------------------------------------------------
def fr(x, d=1, pct=True):
    s = f"{x * 100:+.{d}f}" if pct else f"{x:.{d}f}"
    return s.replace(".", ",") + (" %" if pct else "")


def svg_ranges(resume):
    """Fourchettes de scénarios : barre pess→opt, repère central, pour chaque ligne, le portefeuille et l'indice."""
    pf = resume["portefeuille"]
    rows = []
    for l in pf["lignes"]:
        v = resume["valeurs"][l["ticker"]]
        s = v["scen"]
        rows.append((l["ticker"], s["pess"]["annual"], s["central"]["annual"], s["opt"]["annual"], "stock"))
    rows.append(("Portefeuille", pf["rendement_annuel"]["pess"], pf["rendement_annuel"]["central"], pf["rendement_annuel"]["opt"], "pf"))
    ix = resume["indice"]["rendement_annuel"]
    rows.append(("Nasdaq 100", ix["pess"], ix["central"], ix["opt"], "idx"))
    lo = min(min(r[1] for r in rows), -0.1)
    hi = max(max(r[3] for r in rows), 0.3)
    lo, hi = lo - 0.03, hi + 0.03
    W, H, left, right, rowh, top = 720, 40 + 34 * len(rows) + 30, 120, 30, 34, 30
    def x(v):
        return left + (v - lo) / (hi - lo) * (W - left - right)
    g = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Fourchette des rendements annuels par scénario">']
    g.append('<style>.lab{font:13px system-ui,sans-serif;fill:var(--fg)}.ax{font:11px system-ui,sans-serif;fill:var(--muted)}.grid{stroke:var(--grid);stroke-width:1}</style>')
    step = 0.1
    v = round(lo / step) * step
    while v <= hi:
        g.append(f'<line class="grid" x1="{x(v):.1f}" y1="{top - 5}" x2="{x(v):.1f}" y2="{H - 25}"/>')
        g.append(f'<text class="ax" x="{x(v):.1f}" y="{H - 10}" text-anchor="middle">{fr(v, 0)}</text>')
        v += step
    g.append(f'<line x1="{x(0):.1f}" y1="{top - 5}" x2="{x(0):.1f}" y2="{H - 25}" stroke="var(--fg)" stroke-width="1.5"/>')
    for i, (name, p, c, o, kind) in enumerate(rows):
        y = top + i * rowh + rowh / 2
        col = {"stock": "var(--c1)", "pf": "var(--c2)", "idx": "var(--c3)"}[kind]
        g.append(f'<text class="lab" x="{left - 8}" y="{y + 4}" text-anchor="end" font-weight="{"700" if kind != "stock" else "400"}">{html.escape(name)}</text>')
        g.append(f'<rect x="{x(p):.1f}" y="{y - 7}" width="{max(1, x(o) - x(p)):.1f}" height="14" rx="7" fill="{col}" opacity="0.35"/>')
        g.append(f'<circle cx="{x(c):.1f}" cy="{y}" r="6" fill="{col}"/>')
        g.append(f'<text class="ax" x="{x(o) + 6:.1f}" y="{y + 4}">{fr(o)}</text>')
        g.append(f'<text class="ax" x="{x(p) - 6:.1f}" y="{y + 4}" text-anchor="end">{fr(p)}</text>')
    g.append(f'<text class="ax" x="{left}" y="{top - 12}">Rendement annuel sur 4 ans : barre = pessimiste → optimiste, point = central</text>')
    g.append("</svg>")
    return "\n".join(g)


def svg_bars(resume):
    """Barres comparatives : rendement espéré annuel et pire cas, portefeuille, équipondéré, indice, 3 et 4 lignes."""
    pf = resume["portefeuille"]
    items = [("Portefeuille 5 valeurs", pf["rendement_annuel"]["expected"], resume["sensibilites_rendement_annuel"].get("pire combinaison (tout pessimiste, −5 pts, multiples figés)")),
             ("Équipondéré 20 %", pf["equipondere_rendement_annuel"]["expected"], None)]
    for n in ("4", "3"):
        c = resume["concentration"].get(n)
        if c:
            items.append((f"{n} lignes ({', '.join(c['tickers'])})", c["expected"], c["pess"]))
    ix = resume["indice"]
    items.append(("Nasdaq 100 reconstitué", ix["rendement_annuel"]["expected"], ix["rendement_annuel"]["pess"]))
    W, left, barh, gap = 720, 230, 22, 14
    H = 40 + len(items) * (2 * barh + gap) + 30
    lo = min(0, min(v for _, _, v in items if v is not None)) - 0.02
    hi = max(e for _, e, _ in items) + 0.05
    def x(v):
        return left + (v - lo) / (hi - lo) * (W - left - 60)
    g = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Rendement espéré et pire cas">']
    g.append('<style>.lab{font:13px system-ui,sans-serif;fill:var(--fg)}.ax{font:11px system-ui,sans-serif;fill:var(--muted)}</style>')
    g.append(f'<line x1="{x(0):.1f}" y1="30" x2="{x(0):.1f}" y2="{H - 25}" stroke="var(--fg)"/>')
    y = 40
    for name, e, w in items:
        g.append(f'<text class="lab" x="{left - 8}" y="{y + barh}" text-anchor="end">{html.escape(name)}</text>')
        g.append(f'<rect x="{min(x(0), x(e)):.1f}" y="{y}" width="{abs(x(e) - x(0)):.1f}" height="{barh}" fill="var(--c2)" rx="4"/>')
        g.append(f'<text class="ax" x="{x(e) + 5:.1f}" y="{y + 15}">espéré {fr(e)}</text>')
        if w is not None:
            g.append(f'<rect x="{min(x(0), x(w)):.1f}" y="{y + barh + 2}" width="{abs(x(w) - x(0)):.1f}" height="{barh - 6}" fill="var(--c3)" rx="4" opacity="0.8"/>')
            g.append(f'<text class="ax" x="{(x(w) + 5 if w >= 0 else x(0) + 5):.1f}" y="{y + barh + 13}">pire cas {fr(w)}</text>')
        y += 2 * barh + gap
    g.append(f'<text class="ax" x="{left}" y="22">Rendement annuel : espéré (25/50/25) et pire cas (pessimiste, croissance −5 pts, multiples figés)</text>')
    g.append("</svg>")
    return "\n".join(g)


def svg_scatter(resume):
    """Nuage P/E NTM contre croissance centrale, droites PEG = 1 et 1,5."""
    vals = [v for v in resume["valeurs"].values() if not v["cyclical"] and v["pe_ntm"] and v["hyp"]["g_central"]]
    pf = {l["ticker"] for l in resume["portefeuille"]["lignes"]}
    W, H, left, bottom = 720, 420, 50, 40
    gmax = max(max(v["hyp"]["g_central"] for v in vals) + 5, 40)
    pmax = min(max(v["pe_ntm"] for v in vals) + 5, 80)
    def x(gv):
        return left + gv / gmax * (W - left - 20)
    def y(pe):
        return H - bottom - min(pe, pmax) / pmax * (H - bottom - 20)
    g = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="P/E contre croissance">']
    g.append('<style>.lab{font:11px system-ui,sans-serif;fill:var(--fg)}.ax{font:11px system-ui,sans-serif;fill:var(--muted)}.grid{stroke:var(--grid)}</style>')
    for gv in range(0, int(gmax) + 1, 10):
        g.append(f'<line class="grid" x1="{x(gv):.1f}" y1="20" x2="{x(gv):.1f}" y2="{H - bottom}"/>')
        g.append(f'<text class="ax" x="{x(gv):.1f}" y="{H - bottom + 15}" text-anchor="middle">{gv} %</text>')
    for pe in range(0, int(pmax) + 1, 10):
        g.append(f'<line class="grid" x1="{left}" y1="{y(pe):.1f}" x2="{W - 20}" y2="{y(pe):.1f}"/>')
        g.append(f'<text class="ax" x="{left - 5}" y="{y(pe) + 4:.1f}" text-anchor="end">{pe}x</text>')
    for peg, lab in ((1.0, "PEG = 1"), (1.5, "PEG = 1,5")):
        gend = min(gmax, pmax / peg)
        g.append(f'<line x1="{x(0):.1f}" y1="{y(0):.1f}" x2="{x(gend):.1f}" y2="{y(gend * peg):.1f}" stroke="var(--c3)" stroke-dasharray="6 4"/>')
        g.append(f'<text class="ax" x="{x(gend) - 50:.1f}" y="{y(gend * peg) - 6:.1f}">{lab}</text>')
    for v in vals:
        px, py = x(v["hyp"]["g_central"]), y(v["pe_ntm"])
        inpf = v["ticker"] in pf
        g.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{7 if inpf else 4}" fill="{"var(--c2)" if inpf else "var(--c1)"}" opacity="{1 if inpf else 0.55}"/>')
        if inpf or v.get("score", 0) > 60 or v["pe_ntm"] > 45:
            g.append(f'<text class="lab" x="{px + 8:.1f}" y="{py + 4:.1f}" font-weight="{"700" if inpf else "400"}">{html.escape(v["ticker"])}</text>')
    g.append(f'<text class="ax" x="{W / 2:.0f}" y="{H - 5}" text-anchor="middle">croissance centrale retenue du BPA (hyp.), % par an</text>')
    g.append(f'<text class="ax" x="14" y="{H / 2:.0f}" transform="rotate(-90 14 {H / 2:.0f})" text-anchor="middle">P/E NTM</text>')
    g.append("</svg>")
    return "\n".join(g)


def svg_hist(h, cur):
    """Petits multiples : chiffre d'affaires (barres) et BPA (barres), même échelle de temps, une mesure par graphique."""
    fin = [f for f in h.get("financials", []) if f.get("year")]
    if not fin:
        return ""
    unit = {"USD": "Md$", "EUR": "Md€", "TWD": "Md NT$"}.get(fin[0].get("revenue_currency") or cur, cur)
    rc0 = fin[0].get("revenue_currency") or cur
    panels = [("Chiffre d'affaires, " + unit, [f.get("revenue") for f in fin]), ("BPA, " + ({"USD": "$", "EUR": "€", "TWD": "NT$"}.get(rc0, rc0)), [f.get("eps") for f in fin])]
    W, H, left, bottom, top = 720, 230, 60, 30, 28
    pw = (W - 30) / 2
    g = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Historique du chiffre d\'affaires et du BPA">']
    g.append('<style>.lab{font:11px system-ui,sans-serif;fill:var(--fg)}.ax{font:11px system-ui,sans-serif;fill:var(--muted)}.grid{stroke:var(--grid)}</style>')
    for pi, (title, vals) in enumerate(panels):
        x0 = 10 + pi * pw
        nums = [v for v in vals if v is not None]
        if not nums:
            continue
        vmax = max(max(nums), 0) * 1.12 or 1
        vmin = min(min(nums), 0)
        def y(v):
            return top + (vmax - v) / (vmax - vmin) * (H - top - bottom)
        g.append(f'<text class="lab" x="{x0 + left}" y="{top - 10}" font-weight="700">{html.escape(title)}</text>')
        step = 10 ** max(0, len(str(int(vmax))) - 1)
        if vmax / step < 3:
            step /= 2
        v = 0
        while v <= vmax:
            g.append(f'<line class="grid" x1="{x0 + left}" y1="{y(v):.1f}" x2="{x0 + pw - 10}" y2="{y(v):.1f}"/>')
            g.append(f'<text class="ax" x="{x0 + left - 4}" y="{y(v) + 4:.1f}" text-anchor="end">{fr(v, 0, False) if v >= 10 else fr(v, 1, False)}</text>')
            v += step
        n = len(fin)
        bw = (pw - left - 10) / n
        for i, (f, val) in enumerate(zip(fin, vals)):
            bx = x0 + left + i * bw + bw * 0.15
            g.append(f'<text class="ax" x="{bx + bw * 0.35:.1f}" y="{H - 10}" text-anchor="middle">{f["year"]}</text>')
            if val is None:
                continue
            yb, y0 = y(val), y(0)
            top_y, hgt = (min(yb, y0), abs(y0 - yb))
            g.append(f'<rect x="{bx:.1f}" y="{top_y:.1f}" width="{bw * 0.7:.1f}" height="{hgt:.1f}" rx="3" fill="var(--c1)"><title>{f["year"]} : {fr(val, 2, False)}</title></rect>')
            if i == n - 1 or i == 0:
                g.append(f'<text class="ax" x="{bx + bw * 0.35:.1f}" y="{top_y - 4:.1f}" text-anchor="middle">{fr(val, 1 if abs(val) < 100 else 0, False)}</text>')
    g.append("</svg>")
    return "\n".join(g)


CSS = """
:root{--bg:#f7f5ef;--fg:#1b1b1b;--muted:#5c5c5c;--card:#ffffff;--grid:#d9d6cc;--rule:#1b1b1b;--c1:#2a78d6;--c2:#eb6834;--c3:#1baf7a;--accent:#8a1c1c}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#121416;--fg:#ececec;--muted:#a5a5a5;--card:#1c1f23;--grid:#33383d;--rule:#ececec;--c1:#3987e5;--c2:#d95926;--c3:#199e70;--accent:#f0a5a5}}
:root[data-theme="dark"]{--bg:#121416;--fg:#ececec;--muted:#a5a5a5;--card:#1c1f23;--grid:#33383d;--rule:#ececec;--c1:#3987e5;--c2:#d95926;--c3:#199e70;--accent:#f0a5a5}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,"Times New Roman",serif}
.wrap{max-width:900px;margin:0 auto;padding:16px}
header.masthead{border-top:4px solid var(--rule);border-bottom:1px solid var(--rule);padding:12px 0;margin-bottom:8px;display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px}
.masthead .title{font:700 34px/1 Georgia,serif;letter-spacing:-.5px}
.masthead .meta{font:13px system-ui,sans-serif;color:var(--muted)}
.disclaimer{font:12px/1.4 system-ui,sans-serif;color:var(--muted);border:1px dashed var(--grid);padding:8px 10px;margin:8px 0 18px}
h1{font:700 30px/1.15 Georgia,serif;margin:14px 0 8px}
h2{font:700 22px/1.2 Georgia,serif;margin:28px 0 8px;border-bottom:1px solid var(--grid);padding-bottom:4px}
h3{font:700 17px/1.25 system-ui,sans-serif;margin:20px 0 6px}
h4{font:600 15px/1.25 system-ui,sans-serif;margin:14px 0 4px;color:var(--muted)}
p{margin:0 0 12px}
.lead{font-size:19px;line-height:1.5;color:var(--fg)}
.box{background:var(--card);border-left:4px solid var(--c2);padding:12px 16px;margin:16px 0;font-family:system-ui,sans-serif;font-size:15px}
.tablewrap{overflow-x:auto;margin:10px 0 16px}
table{border-collapse:collapse;width:100%;font:13.5px/1.35 system-ui,sans-serif}
th,td{padding:6px 8px;border-bottom:1px solid var(--grid);text-align:left;vertical-align:top;white-space:nowrap}
td:first-child,th:first-child{white-space:normal}
th{background:var(--card);font-weight:600}
blockquote{margin:12px 0;padding:8px 14px;border-left:3px solid var(--c1);color:var(--muted);font-style:italic}
code{font:13px ui-monospace,monospace;background:var(--card);padding:1px 4px;border-radius:3px}
.chart{width:100%;height:auto;background:var(--card);border:1px solid var(--grid);border-radius:6px;margin:8px 0 18px}
figure{margin:16px 0}figcaption{font:12px system-ui,sans-serif;color:var(--muted);margin-top:-12px}
button.theme{font:13px system-ui,sans-serif;background:var(--card);color:var(--fg);border:1px solid var(--grid);border-radius:6px;padding:4px 10px;cursor:pointer}
.toc{font:14px/1.6 system-ui,sans-serif;background:var(--card);border:1px solid var(--grid);border-radius:6px;padding:10px 16px;margin:12px 0 18px;columns:2;column-gap:24px}.toc-title{font-weight:700;margin-bottom:4px;column-span:all}.toc ol{margin:0;padding-left:18px}.toc a{text-decoration:none}
footer{font:12px/1.5 system-ui,sans-serif;color:var(--muted);border-top:1px solid var(--rule);margin-top:30px;padding-top:10px}
a{color:var(--c1)}
@media print{button.theme{display:none}.chart{break-inside:avoid}h2{break-after:avoid}table{font-size:10px}th,td{white-space:normal;padding:4px 5px}.tablewrap{overflow:visible}body{font-size:13px;line-height:1.5}figure,blockquote,.box{break-inside:avoid}h3{break-after:avoid}}
@media print{.long h2.chapter{break-before:page}}
@page{size:A4;margin:14mm 12mm}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", default="outputs/resume.json")
    ap.add_argument("--content", default="article/contenu.md")
    ap.add_argument("--out", default="article.html")
    ap.add_argument("--date", default="1er octobre 2026")
    ap.add_argument("--hist", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "research", "histoire", "histoire.json"))
    ap.add_argument("--long", action="store_true", help="mise en page longue : saut de page avant chaque chapitre à l'impression")
    args = ap.parse_args()
    resume = json.load(open(args.resume, encoding="utf-8"))
    md = open(args.content, encoding="utf-8").read()
    body = md_to_html(md)
    figs = {
        "ranges": ("Fourchettes de scénarios", svg_ranges(resume)),
        "bars": ("Barres comparatives", svg_bars(resume)),
        "scatter": ("Nuage P/E contre croissance", svg_scatter(resume)),
    }
    for key, (cap, svg) in figs.items():
        body = body.replace(f"<!--infographic:{key}-->", f"<figure>{svg}<figcaption>{cap} — calculs du modèle portefeuille.py, {args.date}.</figcaption></figure>")
    # historiques par valeur : <!--infographic:hist:TICKER-->
    hist = {}
    if args.hist and os.path.exists(args.hist):
        for h in json.load(open(args.hist, encoding="utf-8")):
            hist[h["ticker"]] = h
    def rep_hist(m):
        t = m.group(1)
        h = hist.get(t)
        if not h:
            return ""
        cur = resume["valeurs"].get(t, {}).get("currency", "USD")
        src = h.get("financials_source") or "rapports annuels et communiqués cités dans research/histoire/"
        return f"<figure>{svg_hist(h, cur)}<figcaption>Historique {html.escape(t)} — {html.escape(src)}.</figcaption></figure>"
    body = re.sub(r"<!--infographic:hist:([A-Za-z0-9.\-]+)-->", rep_hist, body)
    if args.long:
        # sommaire : ancres sur les chapitres, liste insérée après le premier h1
        heads = re.findall(r"<h2>(.*?)</h2>", body)
        n = [0]
        def anchor(m):
            n[0] += 1
            return f'<h2 class="chapter" id="ch{n[0]}">{m.group(1)}</h2>'
        body = re.sub(r"<h2>(.*?)</h2>", anchor, body)
        toc = '<nav class="toc"><div class="toc-title">Sommaire</div><ol>' + "".join(
            f'<li><a href="#ch{i + 1}">{re.sub("<.*?>", "", h)}</a></li>' for i, h in enumerate(heads)) + "</ol></nav>"
        body = re.sub(r"(</h1>)", r"\1" + toc.replace("\\", "\\\\"), body, count=1)
    title = re.search(r"<h1>(.*?)</h1>", body)
    title = re.sub("<.*?>", "", title.group(1)) if title else "Portefeuille PEG"
    page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — {JOURNAL}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap{" long" if args.long else ""}">
<header class="masthead"><div class="title">{JOURNAL}</div><div class="meta">Édition du {args.date} · <button class="theme" onclick="toggleTheme()">Thème clair / sombre</button></div></header>
<div class="disclaimer">{DISCLAIMER_TITLE}</div>
{body}
<footer>{DISCLAIMER_TITLE} Chiffres générés depuis les CSV du modèle (portefeuille.py) ; sources citées avec leur date dans le rapport complet.</footer>
</div>
<script>
function toggleTheme(){{var r=document.documentElement;var cur=r.getAttribute('data-theme');var dark=window.matchMedia('(prefers-color-scheme: dark)').matches;var now=cur?cur:(dark?'dark':'light');var nxt=now==='dark'?'light':'dark';r.setAttribute('data-theme',nxt);try{{localStorage.setItem('theme',nxt)}}catch(e){{}}}}
try{{var t=localStorage.getItem('theme');if(t){{document.documentElement.setAttribute('data-theme',t)}}}}catch(e){{}}
</script>
</body></html>"""
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(page)
    print("article écrit :", args.out, f"({len(page)} caractères)")


if __name__ == "__main__":
    main()
