#!/usr/bin/env python3
"""
Assemble data/data.csv (univers) à partir :
  - du consensus Zacks du dépôt elgateaux/bourse (data/zacks_univers.csv, 29-30/09/2026) ;
  - des screens régionaux de la phase 1 (JSON, recherche web du 01/10/2026) ;
  - des fichiers research/*.json des sessions enfants (Europe, Asie, US, méga-tendances) s'ils existent ;
  - des cours de clôture du 30/09/2026 de Google Finance (gf.csv) lorsque disponibles.
Chaque ligne garde une note de source. Bibliothèque standard uniquement.
"""
import csv
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("PEG_REPO_DATA", os.path.join(ROOT, "sources", "elgateaux-bourse"))
PHASE1 = os.environ.get("PEG_PHASE1", os.path.join(ROOT, "..", "research", "phase1"))
RESEARCH = os.environ.get("PEG_RESEARCH", os.path.join(ROOT, "..", "research"))
GF = os.path.join(ROOT, "gf.csv")
OUT = os.path.join(ROOT, "data", "data.csv")

# Dernier exercice publié (libellé Zacks) pour les exercices non calendaires (repris du dépôt).
FY0_ANNEE = {"NVDA": 2026, "MRVL": 2026, "WMT": 2026, "AVGO": 2025, "AMAT": 2025, "LRCX": 2026, "KLAC": 2026,
             "SNDK": 2026, "LITE": 2026, "COHR": 2026, "MSFT": 2026, "MU": 2025, "COST": 2026, "AAPL": 2025,
             "CRDO": 2026, "CSCO": 2026, "PANW": 2026, "ORCL": 2026, "ATEYY": 2026}
# Micron : exercice clos fin août 2026 → FY2026 publié le 23/09/2026 ; Zacks donne FY0 = 2025 dans le dépôt
# (8,29 $), F1 = FY2026 (73,91 $), F2 = FY2027 (158,45 $) : on garde ce libellé.
GF_TICKER = {  # ticker du modèle → ticker Google Finance
    "NU": "NYSE:NU", "UBER": "NYSE:UBER", "ORCL": "NYSE:ORCL", "ANET": "NYSE:ANET", "CRDO": "NASDAQ:CRDO",
    "COHR": "NYSE:COHR", "VRT": "NYSE:VRT", "TSM": "NYSE:TSM", "RNMBY": "OTCMKTS:RNMBY", "ADYEY": "OTCMKTS:ADYEY",
    "ATEYY": "OTCMKTS:ATEYY", "SKHY": "OTCMKTS:HXSCL", "GRAB": "NASDAQ:GRAB", "SE": "NYSE:SE", "HOOD": "NASDAQ:HOOD",
    "RDDT": "NYSE:RDDT", "LLY": "NYSE:LLY", "CVNA": "NYSE:CVNA", "DUOL": "NASDAQ:DUOL", "SPCX": "NASDAQ:SPCX",
    "EMBJ": "NYSE:EMBJ", "CPA": "NYSE:CPA", "PAM": "NYSE:PAM", "VIST": "NYSE:VIST", "PAC": "NYSE:PAC", "ARCO": "NYSE:ARCO",
    "MELI": "NASDAQ:MELI", "DLO": "NASDAQ:DLO", "VTEX": "NYSE:VTEX", "GLOB": "NYSE:GLOB", "PAX": "NYSE:PAX",
    "BMA": "NYSE:BMA", "GFNORTEO.MX": "BMV:GFNORTEO",
    "2330.TW": "TPE:2330", "2454.TW": "TPE:2454", "2317.TW": "TPE:2317", "2308.TW": "TPE:2308", "6669.TW": "TPE:6669",
    "2382.TW": "TPE:2382", "000660.KS": "KRX:000660", "005930.KS": "KRX:005930",
    "6857.T": "TYO:6857", "8035.T": "TYO:8035", "6146.T": "TYO:6146", "6920.T": "TYO:6920", "7735.T": "TYO:7735",
    "6525.T": "TYO:6525", "4062.T": "TYO:4062", "5803.T": "TYO:5803", "6501.T": "TYO:6501", "7011.T": "TYO:7011",
    "7013.T": "TYO:7013", "6503.T": "TYO:6503", "6504.T": "TYO:6504", "6861.T": "TYO:6861", "6758.T": "TYO:6758",
    "7974.T": "TYO:7974", "8136.T": "TYO:8136", "6098.T": "TYO:6098",
}
THEME_MAP = {  # thème du dépôt → thème du modèle
    "IA calcul": "IA calcul", "IA fonderie et equipement": "IA fonderie et équipement",
    "IA memoire et stockage": "IA mémoire et stockage", "IA reseau et optique": "IA réseau et optique",
    "IA energie et refroidissement": "IA énergie et refroidissement", "Hyperscalers et plateformes": "Hyperscalers et plateformes",
    "Internet et IA applicative": "Internet et IA applicative", "Fintech emergente": "Fintech émergente",
    "Mobilite et robotaxi": "Mobilité et robotaxi", "Defense europeenne": "Défense", "Autres Nasdaq 100": "Autres",
    "Paiements": "Fintech émergente", "IA cloud": "IA calcul",
}
REGION_REPO = {"TSM": "Asie", "ASML": "Europe", "RNMBY": "Europe", "ADYEY": "Europe", "GRAB": "Asie", "ATEYY": "Asie",
               "SKHY": "Asie", "NU": "Amérique du Sud", "MELI": "Amérique du Sud", "SE": "Asie", "PDD": "Asie"}
COUNTRY_REPO = {"TSM": "Taïwan", "ASML": "Pays-Bas", "RNMBY": "Allemagne", "ADYEY": "Pays-Bas", "GRAB": "Singapour",
                "ATEYY": "Japon", "SKHY": "Corée du Sud", "NU": "Brésil", "MELI": "Uruguay/Argentine", "SE": "Singapour"}


def fnum(x):
    if x is None:
        return None
    s = str(x).strip().replace(" ", "").replace(" ", "")
    if s in ("", "na", "n.d.", "None", "null", "#N/A"):
        return None
    # format français 1234,5
    if re.match(r"^-?\d+,\d+$", s):
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def load_gf():
    gf = {}
    if not os.path.exists(GF):
        return gf
    with open(GF, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            gf[r["ticker"]] = {k: fnum(v) if k not in ("ticker", "currency", "name") else v for k, v in r.items()}
    return gf


def year_from_label(label, default=None):
    m = re.search(r"(20\d\d)", label or "")
    return int(m.group(1)) if m else default


rows = []
notes_global = []


def add(row):
    rows.append(row)


def base_row(ticker):
    return {"ticker": ticker, "name": "", "region": "", "country": "", "currency": "", "listing": "", "pea": "",
            "theme": "", "price": None, "price_date": "", "price_source": "", "mcap_usd_bn": None, "fy_end_month": 12,
            "eps_basis": "", "fy2025": None, "fy2026": None, "fy2027": None, "fy2028": None, "fy2029": None,
            "ltg_pct": None, "beta": None, "div_yield_pct": None, "zacks_rank": None, "w52_low": None, "w52_high": None,
            "target": None, "cyclical": 0, "ntm_base": "", "source_note": ""}


gf = load_gf()
SUFFIX = {".TWO": "TPE:", ".TW": "TPE:", ".KS": "KRX:", ".KQ": "KOSDAQ:", ".T": "TYO:", ".HK": "HKG:", ".SZ": "SHE:", ".SS": "SHA:",
          ".NS": "NSE:", ".SI": "SGX:", ".SA": "BVMF:", ".MX": "BMV:", ".AS": "AMS:", ".DE": "ETR:", ".PA": "EPA:", ".MI": "BIT:",
          ".L": "LON:", ".ST": "STO:", ".CO": "CPH:", ".SW": "SWX:", ".BR": "EBR:", ".HE": "HEL:", ".OL": "OSL:", ".MC": "MAD:", ".VI": "VIE:"}


def gf_ticker_for(t):
    if t in GF_TICKER:
        return GF_TICKER[t]
    for suf, pre in SUFFIX.items():
        if t.endswith(suf):
            base = t[: -len(suf)]
            if suf == ".HK":
                base = base.zfill(4)
            return pre + base
    return "NASDAQ:" + t
FX_PATH = os.path.join(ROOT, "fx.csv")   # pair,rate (USD par unité : USDCNY = CNY pour 1 USD)
FX = {}
if os.path.exists(FX_PATH):
    for r in csv.DictReader(open(FX_PATH, encoding="utf-8")):
        FX[r["pair"]] = fnum(r["rate"])


def to_usd(amount, ccy):
    """Convertit un montant d'une devise en USD avec les taux du 30/09/2026."""
    ccy = (ccy or "").upper()
    if ccy == "USD" or amount is None:
        return amount
    if ccy == "EUR" and FX.get("EURUSD"):
        return amount * FX["EURUSD"]
    if ccy == "GBP" and FX.get("GBPUSD"):
        return amount * FX["GBPUSD"]
    if ccy == "GBX" and FX.get("GBPUSD"):
        return amount / 100 * FX["GBPUSD"]
    r = FX.get("USD" + ccy)
    return amount / r if r else None


def convert(amount, from_ccy, to_ccy):
    if amount is None or from_ccy == to_ccy:
        return amount
    usd = to_usd(amount, from_ccy)
    if usd is None:
        return None
    if to_ccy == "USD":
        return usd
    back = to_usd(1.0, to_ccy)  # USD par unité de to_ccy
    return usd / back if back else None


def apply_gf(row, gf_ticker):
    g = gf.get(gf_ticker)
    if not g:
        return
    if g.get("close_2026_09_30") is not None:
        row["price"] = g["close_2026_09_30"]
        row["price_date"] = "2026-09-30"
        row["price_source"] = f"Google Finance ({gf_ticker}), clôture 30/09/2026"
    if row.get("mcap_usd_bn") is None and g.get("mcap") is not None and (g.get("currency") == "USD"):
        row["mcap_usd_bn"] = round(g["mcap"] / 1e9, 2)
    if row.get("beta") is None and g.get("beta") is not None:
        row["beta"] = g["beta"]
    if row.get("w52_high") is None and g.get("high52") is not None:
        row["w52_high"], row["w52_low"] = g["high52"], g["low52"]


# ----------------------------------------------------------------------------
# 1. Univers Zacks du dépôt (29-30/09/2026)
# ----------------------------------------------------------------------------
with open(os.path.join(REPO, "zacks_univers.csv"), newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        t = r["ticker"]
        row = base_row(t)
        row.update(name=r["nom"], region=REGION_REPO.get(t, "États-Unis"), country=COUNTRY_REPO.get(t, "États-Unis"),
                   currency="USD", listing=("ADR " + t if t in ("RNMBY", "ADYEY", "ATEYY", "SKHY") else t),
                   pea=("Non" if t not in ("ASML",) else "Oui via Euronext Amsterdam (ASML, EUR)"),
                   theme=THEME_MAP.get(r["theme"], r["theme"]), price=fnum(r["prix"]), price_date="2026-09-29",
                   price_source="Zacks via elgateaux/bourse (zacks_univers.csv), cours du 29/09/2026",
                   mcap_usd_bn=(fnum(r["cap_musd"]) or 0) / 1000 or None, fy_end_month=int(r["fye"]),
                   eps_basis="BPA non-GAAP consensus Zacks", ltg_pct=fnum(r["ltg"]), beta=fnum(r["beta"]),
                   div_yield_pct=fnum(r["div_yield"]), zacks_rank=fnum(r["zacks_rank"]), w52_low=fnum(r["low_52w"]),
                   w52_high=fnum(r["high_52w"]), target=fnum(r["target_zacks"]),
                   source_note=f"Zacks ({r['source']}) au 30/09/2026 via dépôt elgateaux/bourse")
        fy0 = FY0_ANNEE.get(t, 2025)
        row[f"fy{fy0}"] = fnum(r["eps_fy0"])
        row[f"fy{fy0 + 1}"] = fnum(r["eps_f1"])
        row[f"fy{fy0 + 2}"] = fnum(r["eps_f2"])
        apply_gf(row, GF_TICKER.get(t, "NASDAQ:" + t))
        add(row)

# cycliques et bases NTM ajustées (reprises des hypothèses du dépôt)
with open(os.path.join(REPO, "hypotheses.csv"), newline="", encoding="utf-8") as f:
    hyp_repo = {h["ticker"]: h for h in csv.DictReader(f)}
for row in rows:
    h = hyp_repo.get(row["ticker"])
    if h:
        row["cyclical"] = 1 if h["cyclique"] == "1" else 0
        row["ntm_base"] = h.get("ntm_ajuste", "")

# ----------------------------------------------------------------------------
# 2. Screens de la phase 1 (recherche web, 01/10/2026)
# ----------------------------------------------------------------------------
REGION_SCREEN = {"screen_asia-japan.json": ("Asie", "Japon"), "screen_asia-taiwan-korea.json": ("Asie", None),
                 "screen_latam-fintech-platforms.json": ("Amérique du Sud", None),
                 "screen_latam-industrials-energy-consumer.json": ("Amérique du Sud", None),
                 "screen_us-software-consumer-health.json": ("États-Unis", "États-Unis")}
THEME_GUESS = [("defen", "Défense"), ("semiconductor equipment", "IA fonderie et équipement"), ("test", "IA fonderie et équipement"),
               ("packaging", "IA fonderie et équipement"), ("EUV", "IA fonderie et équipement"), ("foundry", "IA fonderie et équipement"),
               ("memory", "IA mémoire et stockage"), ("HBM", "IA mémoire et stockage"), ("server", "IA calcul"), ("ASIC", "IA calcul"),
               ("optical", "IA réseau et optique"), ("PCB", "IA réseau et optique"), ("CCL", "IA réseau et optique"),
               ("power", "IA énergie et refroidissement"), ("cooling", "IA énergie et refroidissement"), ("grid", "IA énergie et refroidissement"),
               ("electrif", "IA énergie et refroidissement"), ("bank", "Fintech émergente"), ("fintech", "Fintech émergente"),
               ("payment", "Fintech émergente"), ("financial", "Fintech émergente"), ("GLP", "Santé"), ("obesity", "Santé"),
               ("health", "Santé"), ("insulin", "Santé"), ("RNAi", "Santé"), ("aero", "Aéronautique"), ("airline", "Aéronautique"),
               ("airport", "Infrastructures"), ("IP", "Consommation et divertissement"), ("character", "Consommation et divertissement"),
               ("entertainment", "Consommation et divertissement"), ("gaming", "Consommation et divertissement"),
               ("streaming", "Consommation et divertissement"), ("education", "Internet et IA applicative"),
               ("e-commerce", "Internet et IA applicative"), ("commerce", "Internet et IA applicative"), ("retail investing", "Fintech émergente"),
               ("training-data", "Internet et IA applicative"), ("used", "Consommation et divertissement"), ("shale", "Énergie"),
               ("oil", "Énergie"), ("gas", "Énergie"), ("automation", "Industrie"), ("hiring", "Internet et IA applicative")]


def guess_theme(text):
    for k, v in THEME_GUESS:
        if k.lower() in (text or "").lower():
            return v
    return "Autres"


existing = {r["ticker"] for r in rows}
SKIP_SCREEN = {"NU", "MELI", "HOOD", "NFLX", "2330.TW", "6857.T"}
SKIP_CHILD = {"2330.TW", "6857.T", "SE", "GRAB", "PDD"}  # doublons de lignes Zacks (TSM, ATEYY, SE, GRAB, PDD si présent)  # déjà dans l'univers Zacks (TSM, ATEYY) ou doublons
for fname, (region, country_default) in REGION_SCREEN.items():
    path = os.path.join(PHASE1, fname)
    if not os.path.exists(path):
        continue
    d = json.load(open(path, encoding="utf-8"))
    for c in d["candidates"]:
        t = c["ticker"]
        if t in existing or t in SKIP_SCREEN:
            continue
        if c.get("eps_f1") is None:
            continue  # pas de consensus : inutilisable pour le PEG
        cur = (c.get("currency") or "").split()[0].strip("(),")
        if "BRL" in (c.get("currency") or "") and cur == "USD":
            continue  # consensus en BRL face à un cours en USD : exclu (change non sourcé)
        row = base_row(t)
        m = c.get("fy_end_month") or 12
        row.update(name=c["name"], region=region, country=(c.get("country") or country_default or ""), currency=cur,
                   listing=f"{c.get('exchange', '')} {t}".strip(), pea="Non", theme=guess_theme(c.get("megatrend", "") + " " + c.get("sector", "")),
                   price=c.get("price"), price_date=(c.get("price_date") or "")[:10], price_source="recherche web (voir sources JSON)",
                   mcap_usd_bn=c.get("market_cap_usd_bn"), fy_end_month=int(m), eps_basis=(c.get("eps_basis") or "")[:80],
                   ltg_pct=c.get("ltg_pct"), beta=c.get("beta"), div_yield_pct=c.get("dividend_yield_pct"),
                   zacks_rank=c.get("zacks_rank"), w52_low=c.get("w52_low"), w52_high=c.get("w52_high"), target=c.get("price_target"),
                   cyclical=1 if c.get("cyclical") else 0,
                   source_note=f"recherche web 01/10/2026 ({fname}) : " + "; ".join(s.get("url", "")[:60] for s in c.get("sources", [])[:3]))
        for key, lab in (("eps_fy0", "eps_fy0_label"), ("eps_f1", "eps_f1_label"), ("eps_f2", "eps_f2_label"), ("eps_f3", "eps_f3_label")):
            v = c.get(key)
            if v is None:
                continue
            y = year_from_label(c.get(lab, ""))
            if y is None:
                continue
            row[f"fy{y}"] = v
        apply_gf(row, gf_ticker_for(t))
        add(row)
        existing.add(t)

# ----------------------------------------------------------------------------
# 3. Sessions enfants (research/*/screen_*.json), si disponibles
# ----------------------------------------------------------------------------
for path in sorted(glob.glob(os.path.join(RESEARCH, "*", "screen_*.json"))):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as e:  # noqa
        notes_global.append(f"{path}: illisible ({e})")
        continue
    region = {"Europe": "Europe", "Asia": "Asie", "US": "États-Unis"}.get(d.get("region", ""), d.get("region", ""))
    for c in d.get("candidates", []):
        t = c.get("ticker")
        if not t:
            continue
        if t in SKIP_CHILD:
            continue
        m_end = int(c.get("fy_end_month") or 12)
        # complet = deux exercices à venir (déc. : fy2026+fy2027 ; mars/juin : fy2027+fy2028)
        need = ("fy2026", "fy2027") if m_end == 12 else ("fy2027", "fy2028")
        if any(c.get(k) is None for k in need):
            continue
        # devise du cours et devise du BPA (ex. « HKD (price); EPS consensus in RMB »)
        cur_field = (c.get("currency") or "")
        price_ccy = cur_field.split()[0].strip("(),;") if cur_field else ""
        eps_ccy = price_ccy
        for tag, code in (("RMB", "CNY"), ("CNY", "CNY"), ("HKD", "HKD"), ("TWD", "TWD"), ("JPY", "JPY"), ("KRW", "KRW"), ("INR", "INR"), ("EUR", "EUR"), ("GBP", "GBP"), ("GBX", "GBX"), ("CHF", "CHF"), ("SEK", "SEK"), ("DKK", "DKK"), ("NOK", "NOK"), ("USD", "USD"), ("BRL", "BRL"), ("MXN", "MXN"), ("SGD", "SGD")):
            if ("EPS" in cur_field or "consensus" in cur_field) and tag in cur_field.split("EPS")[-1] if "EPS" in cur_field else False:
                eps_ccy = code
                break
        conv_note = ""
        if eps_ccy != price_ccy:
            for y in ("fy2025", "fy2026", "fy2027", "fy2028", "fy2029"):
                if c.get(y) is not None:
                    c[y] = convert(float(c[y]), eps_ccy, price_ccy)
            conv_note = f" ; BPA convertis de {eps_ccy} en {price_ccy} au change du 30/09/2026"
            if any(c.get(y) is None for y in need):
                continue
        c["currency"] = price_ccy
        # corrections de devise documentées
        if t == "SPOT":
            # consensus en EUR face à un cours NYSE en USD : on retient les équivalents USD cités par la même source
            c.update(fy2026=14.29, fy2027=15.95, fy2028=19.81)
            conv_note = " ; consensus USD (2026 14,29 $, 2027 15,95 $, 2028 19,81 $) retenu à la place du consensus en EUR"
        if t == "ALC":
            # BPA core en USD (devise de publication) face à un cours SIX en CHF
            for y in ("fy2025", "fy2026", "fy2027", "fy2028", "fy2029"):
                if c.get(y) is not None:
                    c[y] = convert(float(c[y]), "USD", "CHF")
            conv_note = " ; BPA convertis de USD en CHF au change du 30/09/2026"
        row = base_row(t)
        row.update(name=c.get("name", ""), region=region, country=c.get("country", ""), currency=c.get("currency", ""),
                   listing=c.get("listing_to_buy") or c.get("exchange", ""), pea=c.get("pea_eligible", ""),
                   theme=guess_theme((c.get("megatrend") or "") + " " + (c.get("sector") or "")), price=c.get("price"),
                   price_date=(c.get("price_date") or "")[:10], price_source="recherche web session enfant (voir research/)",
                   mcap_usd_bn=c.get("market_cap_usd_bn"), fy_end_month=int(c.get("fy_end_month") or 12),
                   eps_basis=(c.get("eps_basis") or "")[:80], fy2025=c.get("fy2025"), fy2026=c.get("fy2026"),
                   fy2027=c.get("fy2027"), fy2028=c.get("fy2028"), fy2029=c.get("fy2029"), ltg_pct=c.get("ltg_pct"),
                   beta=c.get("beta"), div_yield_pct=c.get("dividend_yield_pct"), zacks_rank=c.get("zacks_rank"),
                   w52_low=c.get("w52_low"), w52_high=c.get("w52_high"), target=c.get("price_target"),
                   cyclical=1 if c.get("cyclical") else 0,
                   source_note=f"session enfant {os.path.basename(os.path.dirname(path))} : " + "; ".join(s.get("url", "")[:60] for s in c.get("sources", [])[:3]) + conv_note)
        if row["price"] is None:
            apply_gf(row, gf_ticker_for(t))
        else:
            g_ = gf.get(gf_ticker_for(t))
            if g_:
                if row.get("beta") is None and g_.get("beta") is not None:
                    row["beta"] = g_["beta"]
                if row.get("w52_high") is None and g_.get("high52") is not None:
                    row["w52_high"], row["w52_low"] = g_["high52"], g_["low52"]
                if row.get("mcap_usd_bn") is None and g_.get("mcap") is not None and g_.get("currency"):
                    usd = to_usd(g_["mcap"], g_["currency"])
                    row["mcap_usd_bn"] = round(usd / 1e9, 2) if usd else None
        if t in existing:
            old = next(r for r in rows if r["ticker"] == t)
            if "Zacks" in old.get("source_note", ""):
                # ligne Zacks : on ne fait que compléter les champs manquants, jamais des montants d'une autre devise
                monetary = {"price", "fy2025", "fy2026", "fy2027", "fy2028", "fy2029", "w52_low", "w52_high", "target", "currency", "price_date", "price_source"}
                for k, v in row.items():
                    if k in monetary and row.get("currency") != old.get("currency"):
                        continue
                    if old.get(k) in (None, "", 0) and v not in (None, ""):
                        old[k] = v
            else:
                # ligne de la phase 1 (recherche plus mince) : les données de la session enfant priment
                for k, v in row.items():
                    if v not in (None, ""):
                        old[k] = v
            continue
        add(row)
        existing.add(t)

# ----------------------------------------------------------------------------
# 4. Deep dives (research/deepdives/summary_*.json, 01/10/2026) : chiffres recoupés sur deux sources ou plus.
#    Règle : pour les valeurs couvertes par Zacks (États-Unis, ADR), on garde F1/F2 Zacks (base du cahier) et on
#    complète les exercices manquants (réalisé 2025 non-GAAP, 2028, 2029) ; pour les lignes locales (Xetra),
#    le deep dive remplace le consensus de la phase 1 ; bêta, 52 semaines, objectif et dividende sont mis à jour.
# ----------------------------------------------------------------------------
DEEPDIVE_FULL = {"RHM", "ENR", "3661.TW"}  # lignes non couvertes par Zacks : le deep dive fait foi (Alchip : médiane FactSet, 18 analystes, au lieu de Stockopedia, 3-4 analystes)
for path in sorted(glob.glob(os.path.join(RESEARCH, "deepdives", "summary_*.json"))):
    try:
        dd = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        notes_global.append(f"deep dive illisible : {path} ({e})")
        continue
    comps = dd["companies"] if isinstance(dd, dict) else dd
    for c in comps:
        t = c.get("ticker")
        row = next((r for r in rows if r["ticker"] == t), None)
        if row is None:
            continue
        full = t in DEEPDIVE_FULL
        for fy in ("fy2025", "fy2026", "fy2027", "fy2028", "fy2029"):
            v = c.get(fy)
            if v in (None, ""):
                continue
            if full or fy == "fy2025" or row.get(fy) in (None, ""):
                row[fy] = v
        for k_src, k_dst in (("beta", "beta"), ("w52_low", "w52_low"), ("w52_high", "w52_high"),
                             ("price_target", "target"), ("dividend_yield_pct", "div_yield_pct")):
            v = c.get(k_src)
            if v not in (None, "") and (full or row.get(k_dst) in (None, "") or k_dst in ("target", "w52_low", "w52_high")):
                row[k_dst] = v
        if full and c.get("price") not in (None, ""):
            row["price"] = c["price"]
            row["price_date"] = c.get("price_date", row.get("price_date"))
            row["price_source"] = "deep dive du 01/10/2026 (clôture du 30/09/2026)"
        if c.get("eps_basis"):
            row["eps_basis"] = (c["eps_basis"][:160])
        row["source_note"] = (row.get("source_note") or "") + f" ; deep dive 01/10/2026 (research/deepdives/{t}.md)"

THEME_OVERRIDE = {"ENR": "Électrification et réseaux", "SU": "Électrification et réseaux", "PRY": "Électrification et réseaux", "LR": "Électrification et réseaux",
                  "267260.KS": "Électrification et réseaux", "6501.T": "Électrification et réseaux", "POLYCAB.NS": "Électrification et réseaux",
                  "RHM": "Défense", "LDO": "Défense", "HAG": "Défense", "SAAB B": "Défense", "KOG": "Défense", "012450.KS": "Défense", "079550.KS": "Défense",
                  "S63.SI": "Défense", "7011.T": "Défense", "7013.T": "Défense", "6503.T": "Défense",
                  "SAF": "Aéronautique", "AIR": "Aéronautique", "RR.": "Aéronautique", "ADYEN": "Fintech émergente", "SPOT": "Consommation et divertissement",
                  "FLUT": "Consommation et divertissement", "LSEG": "Autres", "PGHN": "Autres", "ARGX": "Santé", "LONN": "Santé", "GALD": "Santé", "UCB": "Santé",
                  "ALC": "Santé", "SRT3": "Santé", "RMS": "Consommation et divertissement", "RACE": "Consommation et divertissement", "BC": "Consommation et divertissement",
                  "ASM": "IA fonderie et équipement", "BESI": "IA fonderie et équipement", "IFX": "IA énergie et refroidissement", "VACN": "IA fonderie et équipement",
                  "3661.TW": "IA calcul", "3017.TW": "IA énergie et refroidissement", "5274.TWO": "IA calcul", "2383.TW": "IA réseau et optique",
                  "0700.HK": "Internet et IA applicative", "PDD": "Internet et IA applicative", "NTES": "Consommation et divertissement", "1810.HK": "Consommation et divertissement",
                  "300750.SZ": "Électrification et réseaux", "9992.HK": "Consommation et divertissement", "BHARTIARTL.NS": "Autres", "TRENT.NS": "Consommation et divertissement",
                  "COFORGE.NS": "Services IT", "PERSISTENT.NS": "Services IT", "207940.KS": "Santé", "6861.T": "Industrie", "8136.T": "Consommation et divertissement",
                  "SE": "Fintech émergente", "GRAB": "Mobilité et robotaxi", "UBER": "Mobilité et robotaxi","VIST": "Énergie", "PAM": "Énergie", "TGS": "Énergie", "CPA": "Aéronautique", "LTM": "Aéronautique",
                  "EMBJ": "Aéronautique et défense", "PAC": "Infrastructures", "ASR": "Infrastructures", "OMAB": "Infrastructures",
                  "GLOB": "Services IT", "AFYA": "Santé", "DUOL": "Internet et IA applicative", "LLY": "Santé (GLP-1)",
                  "6758.T": "Consommation et divertissement", "8136.T": "Consommation et divertissement", "7974.T": "Consommation et divertissement",
                  "6861.T": "Industrie", "6098.T": "Internet et IA applicative", "4062.T": "IA fonderie et équipement",
                  "2317.TW": "IA calcul", "2382.TW": "IA calcul", "6669.TW": "IA calcul", "2454.TW": "IA calcul", "2308.TW": "IA énergie et refroidissement",
                  "DLO": "Fintech émergente", "VTEX": "Internet et IA applicative", "PAX": "Fintech émergente", "BMA": "Fintech émergente",
                  "GFNORTEO.MX": "Fintech émergente", "ARCO": "Consommation et divertissement", "CVNA": "Internet et IA applicative"}
for row in rows:
    if row["ticker"] in THEME_OVERRIDE:
        row["theme"] = THEME_OVERRIDE[row["ticker"]]

# doublons ADR / action locale : SK hynix via 000660.KS ; Rheinmetall via RHM (Xetra, PEA) ; Adyen via ADYEN (Amsterdam, PEA)
tick_set = {r["ticker"] for r in rows}
DROP = {"SKHY"}
if "RHM" in tick_set:
    DROP.add("RNMBY")
if "ADYEN" in tick_set:
    DROP.add("ADYEY")
rows = [r for r in rows if r["ticker"] not in DROP]

# ----------------------------------------------------------------------------
# poids de l'indice (QQQ au 30/09/2026, dépôt elgateaux/bourse) : GOOG fusionné dans GOOGL
# ----------------------------------------------------------------------------
w = {}
names = {}
with open(os.path.join(REPO, "qqq_holdings.csv"), newline="", encoding="utf-8") as f:
    for q in csv.DictReader(f):
        t = "GOOGL" if q["ticker"] == "GOOG" else q["ticker"]
        w[t] = w.get(t, 0.0) + float(q["poids_pct"])
        names[t] = q["nom"]
with open(os.path.join(ROOT, "data", "index_weights.csv"), "w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f)
    wr.writerow(["ticker", "name", "weight_pct"])
    for t, p in sorted(w.items(), key=lambda kv: -kv[1]):
        wr.writerow([t, names[t], round(p, 2)])

# ----------------------------------------------------------------------------
# écriture
# ----------------------------------------------------------------------------
os.makedirs(os.path.dirname(OUT), exist_ok=True)
cols = list(base_row("x").keys())
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})
print(f"{len(rows)} lignes écrites dans {OUT}")
for n in notes_global:
    print("note:", n)
