"""Cadres du kit Option Premium LA SALLE (esquisses statiques = mise en page figée du build).

Chaque fonction renvoie le HTML intérieur d'un cadre .fr (1080×1920 ou 1080×1350).
Coordonnées en px. Pente du trait : 0,42 (dx par dy), penchée à droite.
"""
NB = " "  # espace insécable
SLOPE = 0.42

PASTILLE_TXT = f"4 SEMAINES OFFERTES, PUIS 2{NB}€ TTC/SEM."
MENTION_TXT = (f"Option 2{NB}€ TTC/sem. (8{NB}€/4{NB}sem.) en plus de l'abonnement. "
               f"1{NB}boisson/30{NB}min. 1{NB}analyse 3D/sem. Sans engagement sur l'option.")
FONTAINE = "FONTAINE À BOISSON SPORTIVE"


def plus(x, y, size, cls=""):
    return (f'<svg class="a plus {cls}" style="left:{x}px;top:{y}px;width:{size*1.04:.0f}px;height:{size}px" '
            f'viewBox="-2 0 104 100"><polygon points="8.6,39 100.6,39 91.4,61 -0.6,61"/>'
            f'<polygon points="60,0 82,0 40,100 18,100"/></svg>')


def pastille(x=108, y=300, txt=PASTILLE_TXT, cls=""):
    return f'<div class="a pastille {cls}" style="left:{x}px;top:{y}px">{txt}</div>'


def bande(x, y, w, h, num, name, extra="", cls="", label_size=None):
    d = SLOPE * h
    ls = f'font-size:{label_size}px;' if label_size else ''
    return (f'<div class="a bande {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{d:.1f}px">'
            f'<div class="label" style="{ls}"><span class="gold">{num}</span>{NB}{NB}{name}{extra}</div></div>'
            f'<div class="a filet {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{d:.1f}px"></div>')


def panel(x, y, w, h, cls=""):
    """Bande ouverte plein cadre (preuve), extrémité droite coupée."""
    d = SLOPE * h
    return (f'<div class="a bande {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{d:.1f}px"></div>'
            f'<div class="a filet {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{d:.1f}px"></div>')


def mention(y=1040, txt=MENTION_TXT, cls=""):
    return f'<div class="a mention {cls}" style="top:{y}px">{txt}</div>'


def trait(x, y, w, thick=6, cls=""):
    """Filet or horizontal aux extrémités coupées à 0,42."""
    d = SLOPE * thick
    return (f'<div class="a {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{thick}px;background:var(--gold);'
            f'clip-path:polygon({d:.1f}px 0,100% 0,calc(100% - {d:.1f}px) 100%,0 100%)"></div>')


def clock(cx, cy, r, cls=""):
    """Horloge tracée par le trait : cercle filet, secteur or de 30 min (demi-tour), aiguille or."""
    s = 2 * r + 40
    return (f'<svg class="a {cls}" style="left:{cx - s/2:.0f}px;top:{cy - s/2:.0f}px;width:{s}px;height:{s}px" viewBox="0 0 {s} {s}">'
            f'<circle cx="{s/2}" cy="{s/2}" r="{r}" fill="none" stroke="rgba(244,241,236,0.18)" stroke-width="4"/>'
            f'<path d="M {s/2} {s/2 - r} A {r} {r} 0 0 1 {s/2} {s/2 + r}" fill="none" stroke="#B8A07E" stroke-width="16"/>'
            f'<line x1="{s/2}" y1="{s/2}" x2="{s/2}" y2="{s/2 + r - 26}" stroke="#B8A07E" stroke-width="10"/>'
            f'<circle cx="{s/2}" cy="{s/2}" r="12" fill="#B8A07E"/></svg>')


def relief(x, y, size, txt="3D", angle=-22, layers=16, cls=""):
    """Relief typographique : couches empilées en or fantôme, face avant blanc cassé."""
    lay = "".join(
        f'<div style="position:absolute;left:0;top:0;transform:translateZ({-i*4}px);color:rgba(184,160,126,0.16)">{txt}</div>'
        for i in range(layers, 0, -1))
    return (f'<div class="a {cls}" style="left:{x}px;top:{y}px;perspective:1600px">'
            f'<div style="position:relative;transform-style:preserve-3d;transform:rotateY({angle}deg) rotateX(6deg);'
            f'font-weight:900;font-size:{size}px;line-height:.86;letter-spacing:-.02em">{lay}'
            f'<div style="position:relative;transform:translateZ(0)">{txt}</div></div></div>')


def mirror(x, y, txt, size, cls=""):
    """Reflet de miroir à plat (sans dégradé) : texte fantôme et son reflet sous un filet."""
    return (f'<div class="a {cls}" style="left:{x}px;top:{y}px;font-weight:900;font-size:{size}px;line-height:.86;'
            f'letter-spacing:-.01em;color:rgba(184,160,126,0.16)">{txt}</div>'
            f'<div class="a" style="left:{x - 36}px;top:{y + size*0.86 + 14:.0f}px;width:{size*3.2:.0f}px;height:3px;background:rgba(244,241,236,0.18)"></div>'
            f'<div class="a {cls}" style="left:{x}px;top:{y + size*0.86 + 30:.0f}px;font-weight:900;font-size:{size}px;line-height:.86;'
            f'letter-spacing:-.01em;color:rgba(184,160,126,0.16);transform:scaleY(-1);transform-origin:50% 0;opacity:.55;'
            f'clip-path:inset(0 0 0 0)">{txt}</div>')


def logo(x, y, w, cls=""):
    """⚠ Logo provisoire : signature 170 px du Drive, à remplacer par mono.png + word.png du kit du PC."""
    return (f'<img class="a {cls}" src="assets/img/logo-provisoire.png" style="left:{x}px;top:{y}px;width:{w}px;'
            f'filter:invert(1);mix-blend-mode:screen" alt="LA SALLE">')


def grain():
    return '<div class="grain"></div>'


def ghost(x, y, txt, size, cls=""):
    return (f'<div class="a {cls}" style="left:{x}px;top:{y}px;font-weight:900;font-size:{size}px;line-height:.8;'
            f'letter-spacing:-.03em;color:rgba(184,160,126,0.16)">{txt}</div>')


def lines(x, y, rows, cls=""):
    """rows = [(classe, texte, extra_style)] empilées à partir de y."""
    out = []
    for c, t, st in rows:
        out.append(f'<div class="{c}" style="{st}">{t}</div>')
    return f'<div class="a {cls}" style="left:{x}px;top:{y}px">' + "".join(out) + "</div>"


# ─────────────────────────── Vidéos 9:16 ───────────────────────────

def A1():  # Accroche A
    return (pastille() +
            lines(108, 470, [("disp", "PASSEZ EN", ""), ("disp", "VERSION", ""), ("disp", "PREMIUM.", "")]) +
            plus(738, 640, 230) +
            trait(108, 925, 600) + grain())


def A2():  # Les 3 bandes
    return (pastille() +
            bande(72, 440, 936, 170, "01", FONTAINE) +
            bande(72, 640, 936, 170, "02", "ANALYSE 3D") +
            bande(72, 840, 936, 170, "03", "SALLE DE POSING", f' <span class="muted">· BIENTÔT</span>') + grain())


def A3():  # 01 fontaine
    return (pastille() + panel(72, 410, 936, 530) +
            f'<div class="a label" style="left:108px;top:448px"><span class="gold">01</span>{NB}{NB}{FONTAINE}</div>' +
            clock(806, 600, 92) +
            lines(108, 690, [("h1", "TOUTES LES", ""), ("disp", '<span class="gold">30 MINUTES.</span>', "font-size:140px")]) + grain())

def A4():  # 02 analyse 3D
    return (pastille() + panel(72, 410, 936, 530) +
            f'<div class="a label" style="left:108px;top:448px"><span class="gold">02</span>{NB}{NB}ANALYSE 3D</div>' +
            f'<div class="a body muted" style="left:108px;top:508px;font-size:32px">Analyse de composition corporelle</div>' +
            relief(560, 540, 250) +
            lines(108, 700, [("h1", "CHAQUE", ""), ("h1", "SEMAINE.", "")]) +
            f'<div class="a label" style="left:108px;top:975px"><span class="gold">1</span> ANALYSE 3D PAR SEMAINE</div>' + grain())

def A5():  # 03 salle de posing : le texte et son reflet de miroir
    return (pastille() + panel(72, 410, 936, 530) +
            f'<div class="a label" style="left:108px;top:448px"><span class="gold">03</span>{NB}{NB}SALLE DE POSING</div>' +
            lines(108, 560, [("h1", "ARRIVE", ""), ("h1", '<span class="gold">TRÈS BIENTÔT.</span>', "")]) +
            f'<div class="a" style="left:108px;top:772px;width:640px;height:3px;background:rgba(244,241,236,0.18)"></div>' +
            f'<div class="a h1" style="left:108px;top:781px;color:rgba(184,160,126,0.16);transform:scaleY(-1);transform-origin:50% 50%">TRÈS BIENTÔT.</div>' +
            f'<div class="a label muted" style="left:108px;top:975px;font-size:36px">MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES</div>' + grain())

def F6():  # Cassure puis offre (fin commune)
    return (f'<div class="a h2 muted" style="left:108px;top:400px">DE L\'OPTION PREMIUM</div>' +
            lines(108, 520, [("disp", "4 SEMAINES", ""), ("disp", '<span class="gold">OFFERTES</span>', "")]) +
            trait(108, 822, 560) +
            lines(108, 852, [("qual", f"PUIS 2{NB}€ TTC/SEM.", "font-size:40px"), ("qual", f"(8{NB}€ TOUTES LES 4{NB}SEM.)", "font-size:40px")]) + grain())

def F6a():  # La cassure 0,47 s
    return (lines(108, 600, [("disp", "ET EN CE", ""), ("disp", "MOMENT…", "")]) + grain())

def F7():  # Prix (fin commune)
    return (pastille() +
            f'<div class="a h2" style="left:108px;top:400px">SONT <span class="gold">OFFERTES.</span></div>' +
            plus(108, 548, 190) +
            f'<div class="a disp num" style="left:330px;top:518px;font-size:250px">2{NB}€</div>' +
            f'<div class="a h2" style="left:108px;top:760px">TTC PAR SEMAINE</div>' +
            lines(108, 850, [("qual", f"SOIT 8{NB}€ TOUTES LES 4{NB}SEM.", ""), ("qual", "EN PLUS DE VOTRE ABONNEMENT", "")]) +
            f'<div class="a label muted" style="left:108px;top:962px;font-size:38px">FONTAINE · ANALYSE 3D · POSING</div>' +
            mention() + grain())


def F8():  # Carte finale (fin commune)
    return (logo(372, 330, 336) +
            f'<div class="a label muted" style="left:0;width:1080px;text-align:center;top:560px;font-size:38px">OPTION PREMIUM</div>' +
            lines(108, 690, [("h1", "EN QUELQUES", ""), ("h1", "SECONDES.", "")]) +
            plus(108, 924, 76) +
            f'<div class="a label" style="left:204px;top:938px">ACTIVEZ-LA À L\'ACCUEIL</div>' +
            mention() + grain())


def B1():  # Accroche B
    return (pastille() + plus(108, 430, 150) +
            lines(108, 640, [("disp", "VOTRE BOISSON", "font-size:126px"), ("disp", "VOUS ATTEND.", "font-size:126px")]) +
            _jauge(900, 300, 92, 700, 0.62) + grain())

def _jauge(x, y, w, h, level):
    d = SLOPE * w * 0.0  # bords verticaux nets ; coupes haute et basse à 0,42
    cut = SLOPE * 40
    fill_h = h * level
    return (f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:3px solid rgba(244,241,236,0.18)"></div>'
            f'<div class="a" style="left:{x+10}px;top:{y + h - fill_h + 10:.0f}px;width:{w-20}px;height:{fill_h - 20:.0f}px;background:var(--gold);'
            f'clip-path:polygon(0 {cut:.0f}px,100% 0,100% 100%,0 100%)"></div>')


def B2():  # 01 les boissons
    return (pastille() +
            f'<div class="a label" style="left:108px;top:420px"><span class="gold">01</span>{NB}{NB}{FONTAINE}</div>' +
            lines(108, 520, [("h1", "COLLAGÈNE,", ""), ("h1", "MULTIVITAMINES,", ""), ("h1", "L-CARNITINE,", ""), ("h1", "BOOSTER…", "")]) +
            _ticker(924, 420, 600) + grain())


def _ticker(x, y, h):
    txt = " · ".join(["PASSION", "PASTÈQUE", "ICE TEA", "ANANAS", "MULTIFRUIT"])
    return (f'<div class="a label muted" style="left:{x}px;top:{y}px;font-size:36px;writing-mode:vertical-rl;'
            f'height:{h}px;overflow:hidden;white-space:nowrap">{txt} · {txt}</div>')


def B3():  # 30 minutes
    return (pastille() +
            f'<div class="a label" style="left:108px;top:420px"><span class="gold">01</span>{NB}{NB}{FONTAINE}</div>' +
            clock(760, 640, 150) +
            lines(108, 800, [("h1", "TOUTES LES", ""), ("disp", '<span class="gold">30 MINUTES.</span>', "")]) + grain())


def B4():  # 02 puis 03, un temps chacun
    return (pastille() +
            bande(72, 520, 936, 190, "02", "ANALYSE 3D", f' <span class="muted">· 1 PAR SEMAINE</span>') +
            bande(72, 740, 936, 190, "03", "SALLE DE POSING", f' <span class="muted">· BIENTÔT</span>') + grain())


def C1():  # Accroche C
    return (pastille() + relief(300, 420, 430) +
            lines(108, 800, [("h1", "VOS PROGRÈS,", ""), ("h1", "EN 3D.", "")]) +
            plus(520, 905, 96) + grain())


def C2():  # 02 analyse 3D (version longue)
    return (pastille() +
            f'<div class="a label" style="left:108px;top:420px"><span class="gold">02</span>{NB}{NB}ANALYSE 3D</div>' +
            f'<div class="a body muted" style="left:108px;top:480px;font-size:32px">Analyse de composition corporelle</div>' +
            relief(600, 520, 260, angle=18) +
            lines(108, 760, [("h1", "CHAQUE", ""), ("h1", "SEMAINE.", "")]) +
            f'<div class="a label" style="left:108px;top:985px"><span class="gold">1</span> ANALYSE 3D PAR SEMAINE</div>' + grain())

def C4():  # 01 fontaine en deux temps
    return (pastille() +
            bande(72, 560, 936, 190, "01", FONTAINE) +
            clock(860, 860, 70) +
            f'<div class="a label" style="left:108px;top:800px"><span class="gold">1</span> BOISSON TOUTES LES 30{NB}MIN</div>' + grain())


# ─────────────────────────── Images story 9:16 ───────────────────────────

def CTA(y, x=108, size=44):
    return (plus(x, y - 6, size + 12) +
            f'<div class="a label" style="left:{x + size + 34}px;top:{y}px;font-size:{size}px">ACTIVEZ-LA À L\'ACCUEIL</div>')


def S1():  # visuel clé A
    return (pastille() +
            lines(108, 400, [("disp", "PASSEZ EN", "font-size:124px"), ("disp", "VERSION", "font-size:124px"), ("disp", "PREMIUM.", "font-size:124px")]) +
            plus(760, 520, 190) +
            bande(72, 750, 936, 56, "01", FONTAINE, label_size=32) +
            bande(72, 816, 936, 56, "02", "ANALYSE 3D", f' <span class="muted">· 1 PAR SEMAINE</span>', label_size=32) +
            bande(72, 882, 936, 56, "03", "SALLE DE POSING", f' <span class="muted">· BIENTÔT</span>', label_size=32) +
            CTA(966, size=40) + mention() + grain())

def S2():  # visuel clé B
    return (pastille() +
            lines(108, 410, [("disp", "VOTRE BOISSON", "font-size:128px"), ("disp", "VOUS ATTEND.", "font-size:128px")]) +
            f'<div class="a label" style="left:108px;top:650px;font-size:38px"><span class="gold">01</span>{NB}{NB}{FONTAINE}</div>' +
            f'<div class="a body" style="left:108px;top:712px;width:620px;font-size:34px">Collagène, multivitamines, L-carnitine, booster… ou simplement de l\'eau.</div>' +
            f'<div class="a label muted" style="left:108px;top:836px;font-size:32px">PASSION · PASTÈQUE · ICE TEA · ANANAS · MULTIFRUIT</div>' +
            clock(866, 770, 84) +
            f'<div class="a label" style="left:108px;top:900px;font-size:40px"><span class="gold">1</span> BOISSON TOUTES LES 30{NB}MIN</div>' +
            CTA(978, size=40) + mention() + grain())


def S3():  # visuel clé C
    return (pastille() + relief(640, 380, 280) +
            lines(108, 640, [("disp", "VOS PROGRÈS,", "font-size:128px"), ("disp", "EN 3D.", "font-size:128px")]) +
            f'<div class="a label" style="left:108px;top:880px;font-size:40px"><span class="gold">02</span>{NB}{NB}ANALYSE 3D · <span class="gold">1</span> PAR SEMAINE</div>' +
            f'<div class="a body muted" style="left:108px;top:930px;font-size:32px">Analyse de composition corporelle.</div>' +
            CTA(984, size=40) + mention() + grain())

def S4():  # carte offre
    return (logo(108, 300, 170) +
            f'<div class="a h2 muted" style="left:108px;top:440px">ET EN CE MOMENT…</div>' +
            lines(108, 530, [("disp", "4 SEMAINES", ""), ("disp", '<span class="gold">OFFERTES</span>', "")]) +
            trait(108, 830, 520) +
            lines(108, 856, [("qual", f"PUIS 2{NB}€ TTC/SEM. (8{NB}€ TOUTES LES 4{NB}SEM.)", ""), ("qual", "EN PLUS DE VOTRE ABONNEMENT", "")]) +
            CTA(966, size=44) + plus(790, 330, 180) + mention() + grain())


# ─────────────────────────── Images post 4:5 ───────────────────────────

def P1():
    return (pastille(y=150) +
            lines(108, 260, [("disp", "PASSEZ EN", "font-size:132px"), ("disp", "VERSION", "font-size:132px"), ("disp", "PREMIUM.", "font-size:132px")]) +
            plus(752, 410, 200) +
            bande(72, 620, 936, 60, "01", FONTAINE, label_size=34) +
            bande(72, 690, 936, 60, "02", "ANALYSE 3D", f' <span class="muted">· 1 PAR SEMAINE</span>', label_size=34) +
            bande(72, 760, 936, 60, "03", "SALLE DE POSING", f' <span class="muted">· BIENTÔT</span>', label_size=34) +
            CTA(856, size=40) + mention(y=1015) + grain())


def P2():
    return (pastille(y=150) +
            lines(108, 260, [("disp", "VOTRE BOISSON", "font-size:128px"), ("disp", "VOUS ATTEND.", "font-size:128px")]) +
            f'<div class="a label" style="left:108px;top:500px;font-size:38px"><span class="gold">01</span>{NB}{NB}{FONTAINE}</div>' +
            f'<div class="a body" style="left:108px;top:562px;width:620px;font-size:34px">Collagène, multivitamines, L-carnitine, booster… ou simplement de l\'eau.</div>' +
            f'<div class="a label muted" style="left:108px;top:688px;font-size:32px">PASSION · PASTÈQUE · ICE TEA · ANANAS · MULTIFRUIT</div>' +
            clock(866, 620, 84) +
            f'<div class="a label" style="left:108px;top:760px;font-size:40px"><span class="gold">1</span> BOISSON TOUTES LES 30{NB}MIN</div>' +
            CTA(856, size=40) + mention(y=1015) + grain())


def P3():
    return (pastille(y=150) + relief(640, 230, 280) +
            lines(108, 490, [("disp", "VOS PROGRÈS,", "font-size:128px"), ("disp", "EN 3D.", "font-size:128px")]) +
            f'<div class="a label" style="left:108px;top:730px;font-size:40px"><span class="gold">02</span>{NB}{NB}ANALYSE 3D · <span class="gold">1</span> PAR SEMAINE</div>' +
            f'<div class="a body muted" style="left:108px;top:780px;font-size:32px">Analyse de composition corporelle, pour suivre votre progression.</div>' +
            CTA(880, size=40) + mention(y=1015) + grain())

# Carrousel : un seul trait or continu sur 5 × 1080 px (coordonnées globales)
CAR_W = 1080
CAR_PATH = [  # (x, y) globaux. Le trait monte vers la droite et descend vers la gauche (pente 0,42)
    (0, 720), (640, 720), (640 + SLOPE * 380, 340),            # slide 1 : souligne le titre, puis monte
    (1080 + 700, 340), (1080 + 700 + SLOPE * 200, 140),         # slide 2 : file au-dessus du titre, monte en haut
    (3240 + 1060, 140), (3240 + 1060 - SLOPE * 850, 990),       # slides 3-4 : file en haut, redescend à droite du texte de la slide 4
    (4320 + 1080, 990),                                          # slide 5 : file sous le CTA, au-dessus des mentions
]


def _car_trait(k):
    pts = " ".join(f"{x - k*CAR_W:.1f},{y:.1f}" for x, y in CAR_PATH)
    return (f'<svg class="a" style="left:0;top:0;width:{CAR_W}px;height:1350px;overflow:visible" viewBox="0 0 {CAR_W} 1350">'
            f'<polyline points="{pts}" fill="none" stroke="#B8A07E" stroke-width="6" stroke-linejoin="miter" stroke-miterlimit="10"/></svg>')


def K1():
    return (_car_trait(0) + pastille(y=150) +
            lines(108, 300, [("disp", "PASSEZ EN", "font-size:150px"), ("disp", "VERSION", "font-size:150px"), ("disp", "PREMIUM.", "font-size:150px")]) +
            plus(760, 470, 200) +
            f'<div class="a label muted" style="left:108px;top:760px;font-size:38px">FONTAINE · ANALYSE 3D · POSING</div>' +
            mention(y=1015) + grain())

def K2():
    return (_car_trait(1) +
            f'<div class="a label" style="left:108px;top:180px"><span class="gold">01</span>{NB}{NB}{FONTAINE}</div>' +
            lines(108, 390, [("disp", "VOTRE BOISSON", "font-size:128px"), ("disp", "VOUS ATTEND.", "font-size:128px")]) +
            f'<div class="a body" style="left:108px;top:640px;width:600px;font-size:36px">Collagène, multivitamines, L-carnitine, booster… ou simplement de l\'eau.</div>' +
            f'<div class="a label muted" style="left:108px;top:800px;font-size:34px">PASSION · PASTÈQUE · ICE TEA · ANANAS · MULTIFRUIT</div>' +
            clock(860, 700, 96) +
            f'<div class="a label" style="left:108px;top:890px;font-size:44px"><span class="gold">1</span> BOISSON TOUTES LES 30{NB}MIN</div>' + grain())

def K3():
    return (_car_trait(2) +
            f'<div class="a label" style="left:108px;top:180px"><span class="gold">02</span>{NB}{NB}ANALYSE 3D</div>' +
            relief(620, 250, 280, angle=18) +
            lines(108, 560, [("disp", "VOS PROGRÈS,", "font-size:128px"), ("disp", "EN 3D.", "font-size:128px")]) +
            f'<div class="a label" style="left:108px;top:800px;font-size:44px"><span class="gold">1</span> ANALYSE 3D PAR SEMAINE</div>' +
            f'<div class="a body muted" style="left:108px;top:870px;width:760px;font-size:34px">Analyse de composition corporelle, pour suivre votre progression.</div>' + grain())

def K4():
    return (_car_trait(3) +
            f'<div class="a label" style="left:108px;top:180px"><span class="gold">03</span>{NB}{NB}SALLE DE POSING</div>' +
            ghost(108, 300, "POSING", 200) +
            lines(108, 560, [("h1", "ARRIVE", ""), ("h1", "TRÈS", ""), ("h1", '<span class="gold">BIENTÔT.</span>', "")]) +
            f'<div class="a" style="left:108px;top:868px;width:420px;height:3px;background:rgba(244,241,236,0.18)"></div>' +
            f'<div class="a h1" style="left:108px;top:877px;color:rgba(184,160,126,0.16);transform:scaleY(-1);transform-origin:50% 50%">BIENTÔT.</div>' +
            f'<div class="a label muted" style="left:108px;top:1060px;font-size:36px">MIROIRS · ÉCLAIRAGE LED · MURS SOMBRES</div>' + grain())

def K5():
    return (_car_trait(4) +
            f'<div class="a h2 muted" style="left:108px;top:160px;font-size:60px">ET EN CE MOMENT…</div>' +
            lines(108, 240, [("disp", "4 SEMAINES", "font-size:132px"), ("disp", '<span class="gold">OFFERTES</span>', "font-size:132px")]) +
            lines(108, 476, [("qual", f"PUIS 2{NB}€ TTC/SEM. (8{NB}€ TOUTES LES 4{NB}SEM.)", "")]) +
            plus(108, 570, 120) +
            f'<div class="a disp num" style="left:250px;top:548px;font-size:160px">2{NB}€</div>' +
            f'<div class="a h2" style="left:470px;top:566px;font-size:64px;line-height:1">TTC PAR<br>SEMAINE</div>' +
            lines(108, 712, [("qual", f"SOIT 8{NB}€ TOUTES LES 4{NB}SEM. · EN PLUS DE VOTRE ABONNEMENT", "")]) +
            CTA(860, size=44) + logo(852, 820, 120) +
            mention(y=1015) + grain())