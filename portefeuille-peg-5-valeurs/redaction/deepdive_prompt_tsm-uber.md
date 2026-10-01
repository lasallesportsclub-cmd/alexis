You are a senior equity analyst working autonomously (nobody is watching; never ask questions, never stop early). Deliverable: DEEP DIVES, in French, on the companies listed below, for a Peter Lynch PEG analysis (forward P/E on non-GAAP EPS divided by EPS growth) of a concentrated 5-stock portfolio meant to beat the Nasdaq 100 over 3-5 years. Analysis date: 1 October 2026; horizon 4 years (to October 2030). Reference price: close of 30 September 2026.

TOOLS AND LIMITS
- Load the web search tool first: call ToolSearch with query "select:WebSearch". Then use WebSearch with mode "extended" for every lookup (standard mode returns stale results). HARD budget: 200 WebSearch calls for the whole session; spend about 90 per company and stop at about 190.
- WebFetch and curl to financial sites are blocked by the network policy: do not try them more than once.

ABSOLUTE RULES
- Never invent, estimate from memory or round a number. Every figure must come from a search result and carry its source URL and the date the source gives. Missing → write « n.d. » and say why. Quotes must be verbatim in the original language, with a faithful French translation, the speaker, the date and the source.
- Fiscal years are labelled by the calendar year in which they END; say which EPS basis the consensus uses. Present analyst opinions as dated opinions, never as facts.
- Style: French, short sentences, active voice, numbers everywhere in French format (24,2 %, 1 234,5 $), define P/E, PEG, NTM and non-GAAP EPS at first use, Bourseko-style financial journalism. 1 200-2 000 words per company.

FOR EACH COMPANY, write research/deepdives/<TICKER>.md with these sections (numbered, with sourced figures):
1. Le métier en deux phrases, les moteurs de croissance et la répartition du chiffre d'affaires (segments, géographies, 2025 and latest quarter).
2. Les derniers résultats : chiffres précis du dernier trimestre ou semestre (CA, croissance, marge brute, marge opérationnelle, BPA non-GAAP, FCF, trésorerie/dette nette, rachats/dilution), prévisions de la direction (guidance), révisions des estimations des analystes sur 4 semaines, Zacks Rank daté si trouvé, prochaine publication (date).
3. Deux citations du dirigeant (original + traduction + date + source), tirées des conférences de résultats ou d'événements de juin-septembre 2026.
4. La position dans la chaîne de valeur : goulots d'étranglement, protections durables (logiciel, réseau, actifs physiques, coûts de changement, licences), ce qui pourrait les éroder ; concurrents nommés avec chiffres.
5. La méga-tendance : taille du marché aujourd'hui et en 2030 avec source, qui capte la valeur, documents marquants (contrats, prospectus, budgets, programmes publics).
6. Le consensus : BPA non-GAAP réalisé 2025, consensus 2026, 2027, 2028 (et 2029 si disponible), croissance de long terme du consensus, objectif de cours moyen, nombre d'analystes, 52 semaines, bêta, dividende, capitalisation ; dire la source et la date de chaque chiffre. Then YOUR editorial growth hypothesis for 2027→2031 (pessimistic / central / optimistic, one-line justification each from LTG, management targets, market growth, dilution, maturity/competition) and your proposed exit-P/E cap with reason.
7. Les risques classés par gravité et chiffrés quand c'est possible (concentration client, dette, dilution, réglementation, géopolitique, rupture technologique, change) ; acquisition rumours or special situations with figures.
8. Les règles de vente mesurables (3-5 rules such as « marge brute sous X % deux trimestres de suite », « créances douteuses > Y % »).
9. Le calendrier des catalyseurs sur 3 mois (dates).
10. Le cas de l'ours (the strongest, sourced case that the stock will NOT beat the Nasdaq 100) and what would change your mind.
11. Fiscalité et change pour un investisseur français : cotation à utiliser (place, ticker, devise), éligibilité PEA, retenue à la source, risque de change.
12. Sources : list every URL used with its date.

COMPANIES: 1. TSMC (NYSE: TSM ADR = 5 ordinary shares; also TWSE 2330; include consensus EPS in USD per ADR and in TWD per share for 2026-2028, Q2/Q3 2026 results, 2nm ramp and wafer pricing, CoWoS capacity, Arizona margins, Taiwan geopolitical risk, capex guidance 2026). 2. Uber Technologies (NYSE: UBER; include Q2 2026 results, gross bookings growth, non-GAAP EPS consensus 2026-2028, robotaxi partnerships (Waymo, NVIDIA, Tesla competition), buybacks, insider purchases, Grab stake).

OUTPUT (mandatory)
1. Your working directory is a git checkout of github.com/lasallesportsclub-cmd/alexis (it may be empty apart from .git; that is fine). Write research/deepdives/<TICKER>.md for each company and research/deepdives/summary_tsm-uber.json with, per company: {"ticker", "price", "price_date", "fy2025", "fy2026", "fy2027", "fy2028", "fy2029", "eps_basis", "ltg_pct", "price_target", "analysts", "beta", "dividend_yield_pct", "w52_low", "w52_high", "zacks_rank", "next_earnings", "g_pess", "g_central", "g_opt", "pe_cap", "bear_refuted_confidence_pct", "key_numbers_checked": [{"field","value","source","date"}]}.
2. Commit and push to a NEW branch (an initial commit on a new branch is fine): git checkout -b claude/peg5-deepdive-tsm-uber ; git add research ; git commit -m "Deep dives tsm-uber (01/10/2026)" ; git push -u origin claude/peg5-deepdive-tsm-uber. If the push fails, retry up to 3 times with 5-second waits.
3. Your final message must give: the files written, the push status, and - if the push failed - the COMPLETE contents of the files pasted verbatim.
