#!/usr/bin/env python3
"""
Dossier de transfert : assemble en un seul HTML (puis PDF via Chromium) l'ensemble des analyses, de la méthode,
des recherches et des données du portefeuille PEG. Réutilise le convertisseur Markdown et les infographies d'article.py.
Usage : python3 compendium.py --out DOSSIER_COMPLET.html
"""
import argparse
import csv
import glob
import html
import json
import os
import re

import article as A

ROOT = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(ROOT, "..", "research")


def md(path):
    return open(path, encoding="utf-8").read()


def strip_h1(text):
    return re.sub(r"^# .*\n", "", text, count=1)


def demote(text, n=1):
    """Abaisse les titres Markdown de n niveaux (# -> ##) pour les imbriquer sous un chapitre."""
    def rep(m):
        return "#" * min(6, len(m.group(1)) + n) + " "
    return re.sub(r"^(#{1,5}) ", rep, text, flags=re.M)


def megatrends_md():
    d = json.load(open(os.path.join(RES, "megatrends", "megatrends.json"), encoding="utf-8"))
    out = [f"*Recherche du {d.get('as_of', '')}. Contexte macro au 30/09/2026 : 10 ans américain {d['macro'].get('us10y_pct')} %, Brent {d['macro'].get('brent_usd')} $, EUR/USD {d['macro'].get('eurusd')}, USD/BRL {d['macro'].get('usdbrl')}, USD/TWD {d['macro'].get('usdtwd')}, USD/JPY {d['macro'].get('usdjpy')}.*", ""]
    for t in d["trends"]:
        out.append(f"### {t['name']}")
        out.append(t.get("summary", ""))
        for k, lab in (("market_size_now", "Taille du marché aujourd'hui"), ("market_size_2030", "Taille attendue vers 2030"), ("cagr_pct", "Croissance annuelle"), ("who_captures_value", "Qui capte la valeur")):
            if t.get(k):
                out.append(f"**{lab}.** {t[k]}")
        if t.get("bottlenecks"):
            out.append("**Goulots d'étranglement.** " + " ; ".join(t["bottlenecks"]))
        if t.get("leaders"):
            out.append("| Société | Ticker | Cotation | Pourquoi |\n|---|---|---|---|")
            for l in t["leaders"]:
                out.append(f"| {l.get('company', '')} | {l.get('ticker', '')} | {l.get('listing', '')} | {l.get('why', '')} |")
        for q in t.get("quotes", []):
            out.append(f"> « {q.get('french', '')} » — {q.get('speaker', '')}, {q.get('company', '')}, {q.get('date', '')}. Original : « {q.get('original', '')} » ({q.get('source', '')})")
        if t.get("key_documents"):
            out.append("**Documents clés.** " + " ; ".join(f"{k.get('title', '')} ({k.get('date', '')}, {k.get('source', '')})" for k in t["key_documents"]))
        if t.get("risks"):
            out.append("**Risques.** " + " ; ".join(t["risks"]))
        if t.get("sources"):
            out.append("**Sources.** " + " ; ".join(f"{s.get('what', '')} ({s.get('url', '')}, {s.get('date', '')})" for s in t["sources"]))
        out.append("")
    return "\n\n".join(out)


def data_md():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "data.csv"), encoding="utf-8")))
    out = ["Univers tel que lu par le modèle (`data/data.csv`, 159 lignes) : cours du 30/09/2026, BPA par exercice (base indiquée), bêta, dividende, source.", "",
           "| Ticker | Nom | Région | Thème | Devise | Cours | FY2025 | FY2026 | FY2027 | FY2028 | FY2029 | Bêta | Div. % | Base du BPA |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append("| " + " | ".join([r["ticker"], r["name"], r["region"], r["theme"], r["currency"], r["price"], r["fy2025"], r["fy2026"], r["fy2027"], r["fy2028"], r["fy2029"], r["beta"], r["div_yield_pct"], r["eps_basis"][:60]]) + " |")
    hyp = list(csv.DictReader(open(os.path.join(ROOT, "data", "hypotheses.csv"), encoding="utf-8")))
    out += ["", "### Hypothèses éditoriales (`data/hypotheses.csv`)", "", "| Ticker | Pess. / central / opt. (%) | Plafond P/E | Cycliques (multiples, P/E) | Justification |", "|---|---|---|---|---|"]
    for h in hyp:
        cyc = f"{h['cyc_mult_pess']}/{h['cyc_mult_central']}/{h['cyc_mult_opt']} ; P/E {h['cyc_pe_pess']}/{h['cyc_pe_central']}/{h['cyc_pe_opt']}" if h["cyc_mult_central"] else ""
        out.append(f"| {h['ticker']} | {h['g_pess']} / {h['g_central']} / {h['g_opt']} | {h['pe_cap']} | {cyc} | {h['justification']} |")
    fx = list(csv.DictReader(open(os.path.join(ROOT, "fx.csv"), encoding="utf-8")))
    out += ["", "### Taux de change (`fx.csv`)", "", "| Paire | Taux | Source |", "|---|---|---|"] + [f"| {f['pair']} | {f['rate']} | {f['source']} |" for f in fx]
    acq = list(csv.DictReader(open(os.path.join(ROOT, "data", "acquisition.csv"), encoding="utf-8")))
    out += ["", "### Scénarios d'acquisition (`data/acquisition.csv`)", "", "| Scénario | Prix (Md£) | GBP/USD | Part actions | Cours d'émission | Résultat cible (M£) | Croissance cible | Impôt | Coût dette | Δ croissance centrale | Source |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for a in acq:
        out.append(f"| {a['nom']} | {a['prix_md_gbp']} | {a['gbpusd']} | {a['part_actions']} | {a['cours_emission_usd']} | {a['resultat_cible_m_gbp']} | {a['croissance_cible_pct']} % | {a['taux_impot_pct']} % | {a['cout_dette_pct']} % | {a['delta_g_central']} | {a['source']} |")
    return "\n".join(out)


def files_md():
    out = ["| Chemin | Contenu |", "|---|---|"]
    desc = {"portefeuille.py": "Moteur du modèle (calendarisation, PEG, scénarios, indice, classement, quintets, variantes, stress tests, probabilités, ETF, dilution, cycliques)",
            "build_data.py": "Assemblage de l'univers depuis sources/, research/ et gf.csv", "build_hypotheses.py": "Écriture des hypothèses éditoriales justifiées",
            "acquisition.py": "Scénarios d'acquisition (Monzo)", "news.py": "Tableaux de la revue de presse", "rapport.py": "Rendu des gabarits (balises {{...}})",
            "article.py": "HTML autonome et infographies SVG", "compendium.py": "Ce dossier de transfert"}
    for f in sorted(glob.glob(os.path.join(ROOT, "*.py")) + glob.glob(os.path.join(ROOT, "*.csv")) + glob.glob(os.path.join(ROOT, "*.md")) + glob.glob(os.path.join(ROOT, "data", "*")) + glob.glob(os.path.join(ROOT, "outputs", "*")) + glob.glob(os.path.join(ROOT, "sources", "**", "*"), recursive=True) + glob.glob(os.path.join(RES, "**", "*"), recursive=True)):
        if os.path.isdir(f):
            continue
        rel = os.path.relpath(f, os.path.join(ROOT, ".."))
        out.append(f"| `{rel}` | {desc.get(os.path.basename(f), '')} |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "DOSSIER_COMPLET.html"))
    ap.add_argument("--date", default="7 octobre 2026")
    args = ap.parse_args()
    resume = json.load(open(os.path.join(ROOT, "outputs", "resume.json"), encoding="utf-8"))
    hist = {h["ticker"]: h for h in json.load(open(os.path.join(RES, "histoire", "histoire.json"), encoding="utf-8"))}

    parts = []  # (titre de partie, [(titre de chapitre, markdown)])
    parts.append(("Partie I. Lire d'abord", [
        ("La demande et la méthode de travail", md(os.path.join(RES, "prompts", "00-demande-initiale.md")).replace("# ", "### ", 1) + "\n\n" + md(os.path.join(ROOT, "redaction", "METHODE_PROCESSUS.md")).replace("## ", "### ", 1)),
        ("Le rapport complet (1er octobre 2026)", demote(strip_h1(md(os.path.join(ROOT, "RAPPORT.md"))), 0)),
    ]))
    parts.append(("Partie II. Les articles", [
        ("L'enquête complète : histoire, chiffres et « pourquoi » de chaque valeur", demote(strip_h1(md(os.path.join(ROOT, "article", "contenu_long.md"))), 1)),
        ("L'article court", demote(strip_h1(md(os.path.join(ROOT, "article", "contenu.md"))), 1)),
        ("Revue de presse, édition du 5 octobre 2026", demote(strip_h1(md(os.path.join(ROOT, "article", "contenu_news_2026-10-05.md"))), 1)),
        ("Revue de presse, édition du 6 octobre 2026", demote(strip_h1(md(os.path.join(ROOT, "article", "contenu_news_2026-10-06.md"))), 1)),
    ]))
    dd = []
    for t in ["NU", "RHM", "AVGO", "UBER", "TSM", "LLY", "ENR", "ALNY", "3661_TW"]:
        p = os.path.join(RES, "deepdives", f"{t}.md")
        if os.path.exists(p):
            txt = md(p)
            title = re.match(r"# (.*)", txt).group(1) if re.match(r"# (.*)", txt) else t
            dd.append((title, demote(strip_h1(txt), 1)))
    parts.append(("Partie III. Les deep dives (01/10/2026)", dd))
    hh = []
    for t in ["NU", "RHM", "AVGO", "UBER", "TSM"]:
        txt = md(os.path.join(RES, "histoire", f"{t}.md"))
        title = re.match(r"# (.*)", txt).group(1)
        hh.append((title, demote(strip_h1(txt), 1)))
    parts.append(("Partie IV. Les histoires d'entreprises", hh))
    parts.append(("Partie V. Le scénario Monzo", [("Rumeur, chiffres, analyse, alternatives, réglementation", demote(strip_h1(md(os.path.join(RES, "monzo", "MONZO.md"))), 1))]))
    parts.append(("Partie VI. Les méga-tendances", [("Huit courants documentés", megatrends_md())]))
    news = []
    for p in sorted(glob.glob(os.path.join(RES, "news", "2026-*.md"))):
        txt = md(p)
        title = re.match(r"# (.*)", txt).group(1) if re.match(r"# (.*)", txt) else os.path.basename(p)
        news.append((title, demote(strip_h1(txt), 1)))
    parts.append(("Partie VII. Les revues de presse sourcées", news))
    parts.append(("Partie VIII. Les données et les prompts", [
        ("Univers, hypothèses, change, scénarios", data_md()),
        ("Le cahier PEG d'origine (version trois valeurs)", demote(strip_h1(md(os.path.join(ROOT, "sources", "cahier-peg-3-valeurs.md"))), 1)),
        ("Les prompts des sessions de recherche", "\n\n".join(demote(md(p), 1) for p in sorted(glob.glob(os.path.join(RES, "prompts", "0[1-9]-*.md"))))),
        ("Index des fichiers du dépôt", files_md()),
    ]))

    figs = {"ranges": A.svg_ranges(resume), "bars": A.svg_bars(resume), "scatter": A.svg_scatter(resume)}
    body, toc = [], []
    n = 0
    for pi, (ptitle, chapters) in enumerate(parts, 1):
        body.append(f'<h1 class="part" id="p{pi}">{html.escape(ptitle)}</h1>')
        toc.append(f'<li class="part"><a href="#p{pi}">{html.escape(ptitle)}</a><ol>')
        for ctitle, text in chapters:
            n += 1
            h = A.md_to_html(f"## {ctitle}\n\n" + text)
            h = re.sub(r"<h2>", f'<h2 class="chapter" id="c{n}">', h, count=1)
            for key, svg in figs.items():
                h = h.replace(f"<!--infographic:{key}-->", f"<figure>{svg}<figcaption>Calculs du modèle portefeuille.py, cours du 30/09/2026.</figcaption></figure>")
            def rep_hist(m):
                hh = hist.get(m.group(1))
                cur = resume["valeurs"].get(m.group(1), {}).get("currency", "USD")
                return f"<figure>{A.svg_hist(hh, cur)}</figure>" if hh else ""
            h = re.sub(r"<!--infographic:hist:([A-Za-z0-9.\-]+)-->", rep_hist, h)
            h = re.sub(r"<!--.*?-->", "", h)
            body.append(h)
            toc.append(f'<li><a href="#c{n}">{html.escape(ctitle)}</a></li>')
        toc.append("</ol></li>")
    cover = f"""<section class="cover">
<div class="kicker">Dossier de transfert</div>
<h1>Portefeuille PEG à cinq valeurs pour battre le Nasdaq 100</h1>
<p class="sub">Nu Holdings 25 % · Rheinmetall 20 % · Broadcom 20 % · Uber 20 % · TSMC 15 %</p>
<p class="sub">Analyse du 1er octobre 2026, histoires, scénario Monzo, revues de presse des 5 et 6 octobre, méthode, données et prompts. Document compilé le {args.date}.</p>
<p class="small">Méthode PEG de Peter Lynch sur un univers de 159 valeurs (États-Unis, Europe, Asie, Amérique latine). Tous les chiffres de valorisation sont générés par le modèle depuis les fichiers CSV ; les faits datés viennent des sources citées dans chaque dossier. Analyse quantitative et datée : elle ne constitue pas un conseil en investissement personnalisé.</p>
</section>
<nav class="toc"><div class="toc-title">Sommaire</div><ol>{''.join(toc)}</ol></nav>"""
    css = A.CSS + """
.cover{min-height:70vh;display:flex;flex-direction:column;justify-content:center;border-bottom:1px solid var(--rule);margin-bottom:24px}
.cover h1{font-size:38px;line-height:1.1}.cover .kicker{font:600 14px system-ui,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
.cover .sub{font-size:18px}.cover .small{font:13px/1.5 system-ui,sans-serif;color:var(--muted)}
h1.part{font-size:30px;margin-top:40px;border-bottom:2px solid var(--rule);padding-bottom:6px}
.toc{columns:1}.toc ol ol{padding-left:16px;margin:2px 0 8px}.toc li.part{font-weight:700;margin-top:6px}.toc li.part li{font-weight:400}
@media print{.cover{break-after:page;min-height:auto;padding-top:120px}nav.toc{break-after:page}h1.part{break-before:page}h2.chapter{break-before:page}}
"""
    page = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dossier complet — Portefeuille PEG cinq valeurs</title><style>{css}</style></head><body><div class="wrap">
<header class="masthead"><div class="title">{A.JOURNAL}</div><div class="meta">Dossier de transfert · {args.date} · <button class="theme" onclick="toggleTheme()">Thème clair / sombre</button></div></header>
<div class="disclaimer">{A.DISCLAIMER_TITLE}</div>
{cover}
{''.join(body)}
<footer>{A.DISCLAIMER_TITLE} Dossier compilé par compendium.py depuis le dépôt ; chaque chapitre conserve ses sources.</footer>
</div>
<script>
function toggleTheme(){{var r=document.documentElement;var cur=r.getAttribute('data-theme');var dark=window.matchMedia('(prefers-color-scheme: dark)').matches;var now=cur?cur:(dark?'dark':'light');var nxt=now==='dark'?'light':'dark';r.setAttribute('data-theme',nxt);try{{localStorage.setItem('theme',nxt)}}catch(e){{}}}}
try{{var t=localStorage.getItem('theme');if(t){{document.documentElement.setAttribute('data-theme',t)}}}}catch(e){{}}
</script></body></html>"""
    open(args.out, "w", encoding="utf-8").write(page)
    print(f"écrit {args.out} ({len(page)} caractères, {n} chapitres)")


if __name__ == "__main__":
    main()
