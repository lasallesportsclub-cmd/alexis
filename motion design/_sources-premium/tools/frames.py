"""Cadres du kit Option Premium LA SALLE (esquisses statiques = mise en page figée du build). v2

Chaque fonction renvoie le HTML intérieur d'un cadre .fr (1080×1920 ou 1080×1350).
Coordonnées en px. Pente du trait : 0,42 (dx par dy), penchée à droite.
"""
NB = " "  # espace insécable
SLOPE = 0.42
GOLD, CANVAS, SURFACE = "#B8A07E", "#0D0D0D", "#222222"

FONTAINE = "FONTAINE À BOISSON SPORTIVE"
QUAL_PASTILLE = "EN CE MOMENT · EN PLUS DE VOTRE ABONNEMENT"
MENTION_TXT = (f"Option 2{NB}€ TTC/sem. (8{NB}€/4{NB}sem.) en plus de l'abonnement. "
               f"1{NB}boisson/30{NB}min. 1{NB}analyse 3D/sem. Sans engagement sur l'option.")
RAPPEL = "FONTAINE · ANALYSE 3D · POSING (BIENTÔT)"
LCARN = '<span style="white-space:nowrap">L-carnitine</span>'
BOISSONS = f"Collagène, multivitamines, {LCARN}, booster… ou simplement de l'eau."

# « + » : barre à plat 22 % ; barre penchée à 0,42, épaisseur perpendiculaire 22 %
PLUS_PTS = '<polygon points="8.6,39 100.6,39 91.4,61 -0.6,61"/><polygon points="59.05,0 82.95,0 40.95,100 17.05,100"/>'


def plus(x, y, size, color=GOLD, cls=""):
    return (f'<svg class="a plus {cls}" style="left:{x}px;top:{y}px;width:{size*1.04:.0f}px;height:{size}px;fill:{color}" '
            f'viewBox="-2 0 104 100">{PLUS_PTS}</svg>')


def plus_inline(size, color=CANVAS):
    return (f'<svg style="display:inline-block;width:{size*1.04:.0f}px;height:{size}px;fill:{color};vertical-align:-3px;margin:0 3px 0 8px" '
            f'viewBox="-2 0 104 100">{PLUS_PTS}</svg>')


def pastille(x=108, y=300, cls=""):
    """Pastille or (version courte du §4) avec le « + » en négatif, et sa ligne de qualificatif dans le même bloc."""
    txt = f"4 SEMAINES OFFERTES, PUIS {plus_inline(26)}2{NB}€ TTC/SEM."
    return (f'<div class="a pastille {cls}" style="left:{x}px;top:{y}px">{txt}</div>'
            f'<div class="a qual {cls}" style="left:{x}px;top:{y + 76}px;font-size:32px">{QUAL_PASTILLE}</div>')


def bande(x, y, w, h, num, name, extra="", cls="", label_size=None, filet=True):
    d = SLOPE * h
    ls = f'font-size:{label_size}px;' if label_size else ''
    out = (f'<div class="a bande {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{d:.1f}px">'
           f'<div class="label" style="{ls}"><span class="gold">{num}</span>{NB}{NB}{name}{extra}</div></div>')
    if filet:
        out += f'<div class="a filet {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{d:.1f}px"></div>'
    return out


def panel(x=72, y=460, w=936, h=530, cls=""):
    """Bande ouverte (preuve), extrémité droite coupée à 0,42, filet or sur le bord."""
    d = SLOPE * h
    return (f'<div class="a bande {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{d:.1f}px"></div>'
            f'<div class="a filet {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{d:.1f}px"></div>')


def mention(y=1040, cls=""):
    return f'<div class="a mention {cls}" style="top:{y}px">{MENTION_TXT}</div>'


def trait(x, y, w, thick=6, cls=""):
    d = SLOPE * thick
    return (f'<div class="a {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{thick}px;background:var(--gold);'
            f'clip-path:polygon({d:.1f}px 0,100% 0,calc(100% - {d:.1f}px) 100%,0 100%)"></div>')


def clock(cx, cy, r, cls=""):
    """Horloge tracée par le trait : cercle filet, demi-tour or (30 min), aiguille or."""
    s = 2 * r + 40
    return (f'<svg class="a {cls}" style="left:{cx - s/2:.0f}px;top:{cy - s/2:.0f}px;width:{s}px;height:{s}px" viewBox="0 0 {s} {s}">'
            f'<circle cx="{s/2}" cy="{s/2}" r="{r}" fill="none" stroke="rgba(244,241,236,0.18)" stroke-width="4"/>'
            f'<path d="M {s/2} {s/2 - r} A {r} {r} 0 0 1 {s/2} {s/2 + r}" fill="none" stroke="{GOLD}" stroke-width="{max(8, r*0.16):.0f}"/>'
            f'<line x1="{s/2}" y1="{s/2}" x2="{s/2}" y2="{s/2 + r - r*0.28:.0f}" stroke="{GOLD}" stroke-width="{max(6, r*0.1):.0f}"/>'
            f'<circle cx="{s/2}" cy="{s/2}" r="{max(6, r*0.12):.0f}" fill="{GOLD}"/></svg>')


def relief(x, y, size, txt="3D", angle=-22, layers=12, depth_color=SURFACE, cls=""):
    """Relief typographique (règle 3d-text-depth-layers) : couches opaques d'une seule couleur déclarée, face blanc cassé."""
    lay = "".join(
        f'<div aria-hidden="true" data-layout-ignore style="position:absolute;left:0;top:0;transform:translateZ({-i*3.5:.1f}px);color:{depth_color}">{txt}</div>'
        for i in range(layers, 0, -1))
    return (f'<div class="a {cls}" style="left:{x}px;top:{y}px;perspective:1600px">'
            f'<div style="position:relative;transform-style:preserve-3d;transform:rotateY({angle}deg) rotateX(6deg);'
            f'font-weight:900;font-size:{size}px;line-height:.86;letter-spacing:-.02em">{lay}'
            f'<div style="position:relative;transform:translateZ(0)">{txt}</div></div></div>')


def reflet(x, y, txt, cls="h1", line_w=640):
    """Reflet de miroir à plat, sans dégradé : filet, puis le texte retourné en or fantôme."""
    return (f'<div class="a" style="left:{x}px;top:{y}px;width:{line_w}px;height:3px;background:rgba(244,241,236,0.18)"></div>'
            f'<div class="a {cls}" aria-hidden="true" data-layout-ignore style="left:{x}px;top:{y + 9}px;color:rgba(184,160,126,0.16);transform:scaleY(-1)">{txt}</div>')


def logo(x, y, w, cls=""):
    """⚠ Logo provisoire : signature 170 px du Drive, à remplacer par mono.png + word.png du kit du PC."""
    return (f'<img class="a {cls}" src="assets/img/logo-negatif-provisoire.png" style="left:{x}px;top:{y}px;width:{w}px" alt="LA SALLE">')


def grain():
    return ''  # grain porté par .fr::after (premium.css) : décor hors audit, jamais un calque sur le texte


def ghost(x, y, txt, size, cls=""):
    return (f'<div class="a {cls}" aria-hidden="true" data-layout-ignore style="left:{x}px;top:{y}px;font-weight:900;font-size:{size}px;line-height:.8;'
            f'letter-spacing:-.03em;color:rgba(184,160,126,0.16)">{txt}</div>')


def lines(x, y, rows, cls=""):
    """rows = [(classe, texte, style)] empilées à partir de y."""
    return (f'<div class="a {cls}" style="left:{x}px;top:{y}px">' +
            "".join(f'<div class="{c}" style="{st}">{t}</div>' for c, t, st in rows) + "</div>")


def lab(x, y, html, size=None, cls="label"):
    s = f"font-size:{size}px;" if size else ""
    return f'<div class="a {cls}" style="left:{x}px;top:{y}px;{s}">{html}</div>'


def num(n, name):
    return f'<span class="gold">{n}</span>{NB}{NB}{name}'


def CTA(y, x=108, size=44):
    return plus(x, y - 6, size + 12) + lab(x + size + 34, y, "ACTIVEZ-LA À L'ACCUEIL", size)


def gold_fill(txt, pct=0.6):
    """Mot qui se remplit d'or de bas en haut, bord net (pas de dégradé)."""
    return (f'<span style="position:relative;display:inline-block">{txt}'
            f'<span style="position:absolute;left:0;top:0;color:var(--gold);clip-path:inset({(1-pct)*100:.0f}% 0 0 0)">{txt}</span></span>')


# ─────────────────────────── Vidéos 9:16 ───────────────────────────
# Zone : pastille + qualificatif y 300–409 ; contenu y 460–1020 ; mentions y 1040+ (à partir de 9,375 s)

def A1():  # Accroche A — image 0
    return (pastille() +
            lines(108, 470, [("disp", "PASSEZ EN", ""), ("disp", "VERSION", ""), ("disp", "PREMIUM.", "")]) +
            plus(745, 640, 230) + trait(108, 925, 600) + grain())


def A2():  # 1er temps du plan 01 : les 3 bandes
    return (pastille() +
            bande(72, 460, 936, 160, "01", FONTAINE) +
            bande(72, 644, 936, 160, "02", "ANALYSE 3D") +
            bande(72, 828, 936, 160, "03", "SALLE DE POSING", f' <span class="muted">· BIENTÔT</span>') + grain())


def A3(n="01"):  # 01 fontaine (même mise en page pour B·03)
    return (pastille() + panel() + lab(108, 498, num(n, FONTAINE)) +
            clock(760, 640, 92) +
            lines(108, 740, [("h1", "TOUTES LES", ""), ("disp", '<span class="gold">30 MINUTES.</span>', "font-size:140px")]) + grain())


def A4(n="02"):  # 02 analyse 3D (même mise en page pour C·01)
    return (pastille() + panel() + lab(108, 498, num(n, "ANALYSE 3D")) +
            f'<div class="a body muted" style="left:108px;top:558px;font-size:32px">Analyse de composition corporelle</div>' +
            relief(540, 590, 240, depth_color=CANVAS) +
            lines(108, 770, [("h1", "CHAQUE", ""), ("h1", "SEMAINE.", "")]) +
            lab(108, 1012, '<span class="gold">1</span> ANALYSE 3D PAR SEMAINE') + grain())


def A5(n="03"):  # 03 salle de posing : citée, jamais montrée
    return (pastille() + panel() + lab(108, 498, num(n, "SALLE DE POSING")) +
            lines(108, 600, [("h1", "ARRIVE", ""), ("h1", '<span class="gold">TRÈS BIENTÔT.</span>', "margin-top:16px")]) +
            reflet(108, 834, "TRÈS BIENTÔT.") +
            lab(108, 1012, "MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES", 36, "label muted") + grain())


def F6a():  # Cassure 0,47 s
    return lines(108, 600, [("disp", "ET EN CE", ""), ("disp", "MOMENT…", "")]) + grain()


def F6b():  # Offre au drop (8,44 s) : 1er groupe de la 25
    return (lab(108, 420, "EN CE MOMENT", 44, "label muted") +
            lines(108, 560, [("h1", "LES 4 PREMIÈRES", ""), ("disp", "SEMAINES", "")]) + grain())


def F6():  # Offre quand la voix dit « offertes » : le mot et sa condition dans la même image
    return (lab(108, 420, "EN CE MOMENT", 44, "label muted") +
            lines(108, 520, [("h1", "SONT", ""), ("disp", '<span class="gold">OFFERTES.</span>', "")]) +
            trait(108, 785, 650) +
            lines(108, 815, [("qual", "LES 4 PREMIÈRES SEMAINES DE L'OPTION", "font-size:40px"),
                             ("qual", f"PUIS 2{NB}€ TTC/SEM. (8{NB}€ TOUTES LES 4{NB}SEM.)", "font-size:40px"),
                             ("qual", "EN PLUS DE VOTRE ABONNEMENT", "font-size:40px")]) +
            mention() + grain())


def F7():  # Prix : le prix et ses qualificatifs dans la même image
    return (lab(108, 440, "PUIS", None, "h2 muted") +
            plus(108, 548, 190) +
            f'<div class="a disp num" style="left:330px;top:514px;font-size:250px">2{NB}€</div>' +
            lab(108, 752, "TTC PAR SEMAINE", None, "h2") +
            lines(108, 846, [("qual", f"SOIT 8{NB}€ TOUTES LES 4{NB}SEM.", "font-size:40px"), ("qual", "EN PLUS DE VOTRE ABONNEMENT", "font-size:40px")]) +
            lab(108, 960, RAPPEL, 38, "label muted") +
            mention() + grain())


def F8():  # Carte finale
    return (logo(108, 330, 280) +
            lab(108, 626, "OPTION PREMIUM", 40, "label muted") +
            plus(108, 726, 84) +
            lab(216, 734, "ACTIVEZ-LA À L'ACCUEIL", 68) +
            lab(108, 856, "EN QUELQUES SECONDES.", None, "h2") +
            mention() + grain())


def B1():  # Accroche B — image 0
    return (pastille() + plus(790, 450, 170) +
            lines(108, 660, [("disp", f"VOTRE {gold_fill('BOISSON')}", "font-size:126px"), ("disp", "VOUS ATTEND.", "font-size:126px")]) + grain())


def B2():  # 01 les boissons, plan 1 (plan 2 identique : « L-CARNITINE, » « BOOSTER… »)
    return (pastille() + panel() + lab(108, 498, num("01", FONTAINE)) +
            lines(108, 600, [("h1", "COLLAGÈNE,", ""), ("h1", "MULTIVITAMINES,", "")]) +
            ghost(560, 790, "01", 220) + grain())


def B2b():  # « ou simplement de l'eau. » et les saveurs, une à la fois
    return (pastille() + panel() + lab(108, 498, num("01", FONTAINE)) +
            lines(108, 600, [("h1", "OU SIMPLEMENT", ""), ("disp", "DE L'EAU.", "")]) +
            f'<div class="a" style="left:108px;top:888px;width:560px;height:52px;overflow:hidden">'
            f'<div class="label muted">SAVEUR · <span style="color:var(--text)">PASSION</span></div></div>' + grain())


def B3():  # 30 minutes, puis 02 et 03 en un temps chacun sous la voix
    return (pastille() + panel(72, 460, 936, 400) + lab(108, 498, num("01", FONTAINE)) +
            clock(790, 640, 80) +
            lines(108, 620, [("h1", "TOUTES LES", ""), ("disp", '<span class="gold">30 MINUTES.</span>', "font-size:132px")]) +
            bande(72, 880, 936, 64, "02", "ANALYSE 3D", ' <span class="muted">· 1 PAR SEMAINE</span>', label_size=36, filet=False) +
            bande(72, 954, 936, 64, "03", "SALLE DE POSING", ' <span class="muted">· BIENTÔT</span>', label_size=36, filet=False) + grain())


def C1():  # Accroche C — image 0
    return (pastille() + relief(108, 450, 330) + plus(790, 470, 170) +
            lines(108, 770, [("disp", "VOS PROGRÈS,", "font-size:140px"), ("disp", "EN 3D.", "font-size:140px")]) + grain())


def C2():
    return A4("01")


def C3():
    return A5("02")


def C4():  # 03 fontaine en deux temps
    return (pastille() + bande(72, 600, 936, 190, "03", FONTAINE) +
            lab(108, 868, '<span class="gold">1</span> BOISSON TOUTES LES 30' + NB + 'MIN') +
            clock(880, 890, 66) + grain())


# ─────────────────────────── Images story 9:16 ───────────────────────────
# Zone : y 290–1240 ; mentions y 1080–1238 ; zone sticker 1320–1540 vide

def S1():  # visuel clé A
    return (pastille() +
            lines(108, 450, [("disp", "PASSEZ EN", "font-size:118px"), ("disp", "VERSION", "font-size:118px"), ("disp", "PREMIUM.", "font-size:118px")]) +
            plus(778, 560, 170) +
            bande(72, 778, 936, 62, "01", FONTAINE, label_size=36, filet=False) +
            bande(72, 848, 936, 62, "02", "ANALYSE 3D", ' <span class="muted">· 1 PAR SEMAINE</span>', label_size=36, filet=False) +
            bande(72, 918, 936, 62, "03", "SALLE DE POSING", ' <span class="muted">· BIENTÔT</span>', label_size=36, filet=False) +
            CTA(1010, size=40) + mention(1080) + grain())


def S2():  # visuel clé B
    return (pastille() + clock(890, 530, 64) +
            lines(108, 440, [("disp", "VOTRE BOISSON", "font-size:112px"), ("disp", "VOUS ATTEND.", "font-size:112px")]) +
            lab(108, 664, num("01", FONTAINE), 38) +
            f'<div class="a body" style="left:108px;top:716px;width:860px;font-size:34px">{BOISSONS}</div>' +
            lab(108, 826, "PASSION · PASTÈQUE · ICE TEA · ANANAS · MULTIFRUIT", 36, "label muted") +
            lab(108, 886, '<span class="gold">1</span> BOISSON TOUTES LES 30' + NB + 'MIN', 40) +
            lab(108, 948, "AUSSI : ANALYSE 3D · SALLE DE POSING (BIENTÔT)", 32, "label muted") +
            CTA(1010, size=40) + mention(1080) + grain())


def S3():  # visuel clé C
    return (pastille() + relief(650, 408, 210) +
            lines(108, 619, [("disp", "VOS PROGRÈS,", "font-size:116px"), ("disp", "EN 3D.", "font-size:116px")]) +
            lab(108, 832, num("01", 'ANALYSE 3D · <span class="gold">1</span> PAR SEMAINE'), 40) +
            f'<div class="a body muted" style="left:108px;top:885px;font-size:32px">Analyse de composition corporelle.</div>' +
            lab(108, 948, "AUSSI : FONTAINE · SALLE DE POSING (BIENTÔT)", 32, "label muted") +
            CTA(1010, size=40) + mention(1080) + grain())


def S4():  # carte offre
    return (logo(108, 300, 170) + lab(330, 334, "OPTION PREMIUM", 40, "label muted") + plus(812, 300, 150) +
            lab(108, 466, "ET EN CE MOMENT…", None, "h2 muted") +
            lines(108, 556, [("disp", "4 SEMAINES", ""), ("disp", '<span class="gold">OFFERTES</span>', "")]) +
            trait(108, 862, 650) +
            lines(108, 888, [("qual", f"PUIS 2{NB}€ TTC/SEM. (8{NB}€ TOUTES LES 4{NB}SEM.)", "font-size:40px"), ("qual", "EN PLUS DE VOTRE ABONNEMENT", "font-size:40px")]) +
            CTA(1004, size=44) + mention(1080) + grain())


# ─────────────────────────── Images post 4:5 ───────────────────────────
# Zone : y 135–1215 ; pastille + qualificatif y 150–259 ; mentions y 1015–1173

def P1():
    return (pastille(y=150) +
            lines(108, 300, [("disp", "PASSEZ EN", "font-size:118px"), ("disp", "VERSION", "font-size:118px"), ("disp", "PREMIUM.", "font-size:118px")]) +
            plus(778, 410, 170) +
            bande(72, 640, 936, 62, "01", FONTAINE, label_size=36, filet=False) +
            bande(72, 710, 936, 62, "02", "ANALYSE 3D", ' <span class="muted">· 1 PAR SEMAINE</span>', label_size=36, filet=False) +
            bande(72, 780, 936, 62, "03", "SALLE DE POSING", ' <span class="muted">· BIENTÔT</span>', label_size=36, filet=False) +
            CTA(890, size=40) + mention(1015) + grain())


def P2():
    return (pastille(y=150) + clock(890, 380, 64) +
            lines(108, 290, [("disp", "VOTRE BOISSON", "font-size:112px"), ("disp", "VOUS ATTEND.", "font-size:112px")]) +
            lab(108, 516, num("01", FONTAINE), 38) +
            f'<div class="a body" style="left:108px;top:568px;width:860px;font-size:34px">{BOISSONS}</div>' +
            lab(108, 674, "PASSION · PASTÈQUE · ICE TEA · ANANAS · MULTIFRUIT", 36, "label muted") +
            lab(108, 736, '<span class="gold">1</span> BOISSON TOUTES LES 30' + NB + 'MIN', 40) +
            lab(108, 796, "AUSSI : ANALYSE 3D · SALLE DE POSING (BIENTÔT)", 32, "label muted") +
            CTA(880, size=40) + mention(1015) + grain())


def P3():
    return (pastille(y=150) + relief(650, 290, 230) +
            lines(108, 500, [("disp", "VOS PROGRÈS,", "font-size:116px"), ("disp", "EN 3D.", "font-size:116px")]) +
            lab(108, 720, num("01", 'ANALYSE 3D · <span class="gold">1</span> PAR SEMAINE'), 40) +
            f'<div class="a body muted" style="left:108px;top:770px;font-size:32px">Analyse de composition corporelle.</div>' +
            lab(108, 820, "AUSSI : FONTAINE · SALLE DE POSING (BIENTÔT)", 32, "label muted") +
            CTA(890, size=40) + mention(1015) + grain())


# Carrousel : un seul trait or continu sur 5 × 1080 px (coordonnées globales),
# ancré sous le « P » de la couverture, terminé sous le CTA de la slide 5.
CAR_W = 1080
CAR_PATH = [  # le trait monte vers la droite et descend vers la gauche (pente 0,42)
    (108, 720), (640, 720), (640 + SLOPE * 380, 340),           # slide 1 : souligne le titre, puis monte
    (1080 + 820, 340), (1080 + 820 + SLOPE * 200, 140),          # slide 2 : file au-dessus du titre, monte en haut
    (3240 + 1000, 140), (3240 + 1000 - SLOPE * 832, 972),        # slides 3-4 : file en haut, redescend à droite du texte
    (4320 + 610, 972),                                            # slide 5 : finit sous le CTA
]


def _car_trait(k):
    pts = " ".join(f"{x - k*CAR_W:.1f},{y:.1f}" for x, y in CAR_PATH)
    return (f'<svg class="a" style="left:0;top:0;width:{CAR_W}px;height:1350px;overflow:visible" viewBox="0 0 {CAR_W} 1350">'
            f'<polyline points="{pts}" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linejoin="miter" stroke-miterlimit="10"/></svg>')


def K1():
    return (_car_trait(0) + pastille(y=150) +
            lines(108, 300, [("disp", "PASSEZ EN", "font-size:150px"), ("disp", "VERSION", "font-size:150px"), ("disp", "PREMIUM.", "font-size:150px")]) +
            plus(800, 470, 180) +
            lab(108, 760, RAPPEL, 38, "label muted") +
            mention(1015) + grain())


def K2():
    return (_car_trait(1) + lab(108, 180, num("01", FONTAINE)) +
            lines(108, 390, [("disp", "VOTRE BOISSON", "font-size:128px"), ("disp", "VOUS ATTEND.", "font-size:128px")]) +
            f'<div class="a body" style="left:108px;top:640px;width:640px;font-size:36px">{BOISSONS}</div>' +
            clock(890, 700, 70) +
            lab(108, 812, "PASSION · PASTÈQUE · ICE TEA · ANANAS · MULTIFRUIT", 36, "label muted") +
            lab(108, 890, '<span class="gold">1</span> BOISSON TOUTES LES 30' + NB + 'MIN', 44) + grain())


def K3():
    return (_car_trait(2) + lab(108, 180, num("02", "ANALYSE 3D")) +
            relief(650, 250, 250, angle=18) +
            lines(108, 560, [("disp", "VOS PROGRÈS,", "font-size:128px"), ("disp", "EN 3D.", "font-size:128px")]) +
            lab(108, 806, '<span class="gold">1</span> ANALYSE 3D PAR SEMAINE', 44) +
            f'<div class="a body muted" style="left:108px;top:874px;width:760px;font-size:34px">Analyse de composition corporelle, pour suivre votre progression.</div>' + grain())


def K4():
    return (_car_trait(3) + lab(108, 180, num("03", "SALLE DE POSING")) +
            ghost(108, 300, "POSING", 200) +
            lines(108, 560, [("h1", "ARRIVE", ""), ("h1", "TRÈS", "margin-top:16px"), ("h1", '<span class="gold">BIENTÔT.</span>', "")]) +
            reflet(108, 894, '<span>BIENTÔT.</span>', line_w=420) +
            lab(108, 1060, "MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES", 36, "label muted") + grain())


def K5():
    return (_car_trait(4) +
            lab(108, 160, "ET EN CE MOMENT…", 60, "h2 muted") +
            lines(108, 240, [("disp", "4 SEMAINES", "font-size:132px"), ("disp", '<span class="gold">OFFERTES</span>', "font-size:132px")]) +
            lab(108, 480, "DE L'OPTION PREMIUM", 38, "label muted") +
            lab(108, 560, "PUIS", 60, "h2 muted") +
            plus(108, 652, 104) +
            f'<div class="a disp num" style="left:236px;top:636px;font-size:132px">2{NB}€</div>' +
            lab(430, 640, "TTC PAR<br>SEMAINE", 60, "h2") +
            lines(108, 778, [("qual", f"SOIT 8{NB}€ TOUTES LES 4{NB}SEM.", ""), ("qual", "EN PLUS DE VOTRE ABONNEMENT", "")]) +
            CTA(888, size=44) + logo(852, 862, 120) +
            mention(1015) + grain())
