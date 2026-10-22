// Versement de la boisson sous la buse : jet, remplissage de la gourde, bulles, gouttes, vaguelettes.
// Dessin à plat (charte « Le Trait Oblique » : aplats, aucun dégradé, aucune ombre). Recopié tel quel dans la
// composition du versement par tools/build.py. Rendu déterministe : rendre(t) ne dépend que de t (secondes, temps
// local de la scène), jamais de l'image précédente, pour que le rendu image par image et les retours en arrière
// donnent la même image. R : géométrie et instants posés par build.py (coordonnées de la scène, px et s).
function versement(canvas, R) {
  const ctx = canvas.getContext("2d");
  const OR = "#B8A07E", BLANC = "rgba(244,241,236,", G = R.g;
  const cx = R.cx, yn = R.buse, w0 = R.jet, v0 = R.v0;
  const g = R.gourde;                       // { col, epaule, corps, bas, rayon, demiCol, demi }
  const yFond = g.bas - 4, yPlein = R.plein;
  const lisse = (a, b, x) => { const u = Math.min(1, Math.max(0, (x - a) / (b - a))); return u * u * (3 - 2 * u); };
  // Hasard reproductible : valeur dans [0, 1) pour un entier et un canal
  const h = (i, k) => { const s = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return s - Math.floor(s); };

  const tAtteint = R.ouvre + chute(yn, yFond);           // la tête du jet touche le fond
  function chute(y0, y1) { const d = y1 - y0; return (-v0 + Math.sqrt(v0 * v0 + 2 * G * d)) / G; }
  function niveau(t) {                                    // fraction remplie, débit constant, fin adoucie
    const u = Math.min(1, Math.max(0, (t - tAtteint) / (R.ferme + chute(yn, yPlein) - tAtteint)));
    return u < 0.92 ? u : 0.92 + 0.08 * Math.sin((u - 0.92) / 0.08 * Math.PI / 2);
  }
  const surface = (t) => yFond - (yFond - yPlein) * niveau(t);

  function contour(dedans) {                              // gourde vue de face, à large goulot
    const e = dedans ? 0 : 3, c = g.demiCol + e, d = g.demi + e, r = g.rayon;
    ctx.beginPath();
    ctx.moveTo(cx - c, g.col);
    ctx.lineTo(cx - c, g.epaule);
    ctx.bezierCurveTo(cx - c, g.epaule + 40, cx - d, g.corps - 40, cx - d, g.corps);
    ctx.lineTo(cx - d, g.bas - r);
    ctx.quadraticCurveTo(cx - d, g.bas + e, cx - d + r, g.bas + e);
    ctx.lineTo(cx + d - r, g.bas + e);
    ctx.quadraticCurveTo(cx + d, g.bas + e, cx + d, g.bas - r);
    ctx.lineTo(cx + d, g.corps);
    ctx.bezierCurveTo(cx + d, g.corps - 40, cx + c, g.epaule + 40, cx + c, g.epaule);
    ctx.lineTo(cx + c, g.col);
  }

  function largeur(y) {                                   // le jet s'affine en accélérant (débit conservé)
    const v = Math.sqrt(v0 * v0 + 2 * G * Math.max(0, y - yn));
    return w0 * Math.sqrt(v0 / v);
  }

  function jet(t, yS) {
    if (t < R.ouvre) return;
    const tau = t - R.ouvre;
    const tete = Math.min(yS, yn + v0 * tau + 0.5 * G * tau * tau);
    let queue = yn;
    if (t > R.ferme) { const k = t - R.ferme; queue = yn + v0 * 0.4 * k + 0.5 * G * k * k; }
    if (queue >= tete - 1) return;
    const gauche = [], droite = [], reflet = [];
    for (let y = queue; ; y = Math.min(tete, y + 5)) {
      const f = (y - yn) / (yFond - yn);
      const a = 0.5 + 2.4 * f;
      const x = cx + a * Math.sin(0.045 * y - 24 * t) + 0.5 * a * Math.sin(0.11 * y - 43 * t + 1.3);
      let w = largeur(y) * (1 + 0.1 * f * Math.sin(0.07 * y - 58 * t));
      if (t > R.ferme) w *= lisse(queue, queue + 40, y);  // la queue du jet s'effile
      w *= lisse(tete + 2, tete - 14, y) * 0.35 + 0.65;   // tête arrondie
      gauche.push([x - w / 2, y]); droite.push([x + w / 2, y]); reflet.push([x - 0.3 * w, x - 0.12 * w, y]);
      if (y >= tete) break;
    }
    ctx.fillStyle = OR;
    ctx.beginPath();
    gauche.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
    for (let i = droite.length - 1; i >= 0; i--) ctx.lineTo(droite[i][0], droite[i][1]);
    ctx.closePath(); ctx.fill();
    if (tete < yS - 2) { const w = largeur(tete) * 0.6; ctx.beginPath(); ctx.arc(gauche[gauche.length - 1][0] + w / 2 + 1, tete, w / 2 + 1, 0, 7); ctx.fill(); }
    ctx.fillStyle = BLANC + "0.42)";
    ctx.beginPath();
    reflet.forEach(([a], i) => (i ? ctx.lineTo(a, reflet[i][2]) : ctx.moveTo(a, reflet[i][2])));
    for (let i = reflet.length - 1; i >= 0; i--) ctx.lineTo(reflet[i][1], reflet[i][2]);
    ctx.closePath(); ctx.fill();
  }

  function onde(x, t, yS, actif) {                         // surface : houle, cratère sous le jet, anneaux, ballottement
    const dx = x - cx, ad = Math.abs(dx);
    let y = yS + actif * (1.6 * Math.sin(0.05 * x - 9 * t) + 1.0 * Math.sin(0.09 * x + 13 * t + 0.7));
    y += actif * (5 * Math.exp(-((dx / 16) ** 2)) + 2.6 * Math.sin(0.12 * ad - 26 * t) * Math.exp(-ad / 90));
    const apres = t - R.ferme - 0.25;
    if (apres > 0) y += 5 * Math.exp(-apres / 0.55) * Math.cos(2 * Math.PI * 1.7 * apres) * (dx / g.demi);
    return y;
  }

  function rendre(t) {
    ctx.setTransform(1, 0, 0, 1, -R.ox, -R.oy);
    ctx.clearRect(R.ox, R.oy, canvas.width, canvas.height);
    const yS = surface(t);
    const touche = t >= tAtteint && t < R.ferme + chute(yn, yS) + 0.02;
    const actif = touche ? 1 : t > tAtteint ? Math.exp(-(t - R.ferme - chute(yn, yS)) / 0.3) : 0;

    // Corps de la gourde (paroi translucide à plat)
    contour(true); ctx.closePath(); ctx.fillStyle = BLANC + "0.05)"; ctx.fill();

    // Liquide, découpé dans la gourde
    ctx.save();
    contour(true); ctx.closePath(); ctx.clip();
    if (t >= tAtteint) {
      const x0 = cx - g.demi - 6, x1 = cx + g.demi + 6;
      ctx.beginPath(); ctx.moveTo(x0, onde(x0, t, yS, actif));
      for (let x = x0; x <= x1; x += 4) ctx.lineTo(x, onde(x, t, yS, actif));
      ctx.lineTo(x1, g.bas + 10); ctx.lineTo(x0, g.bas + 10); ctx.closePath();
      ctx.fillStyle = OR; ctx.fill();
      // Bulles entraînées sous le jet, puis bulles qui remontent de tout le volume
      ctx.lineWidth = 1.6;
      for (let i = 0; i < 260; i++) {
        const ti = tAtteint + i / 70;
        if (ti > Math.min(t, R.ferme + 0.15)) break;
        const age = t - ti, prof = 14 + 80 * h(i, 1) * (0.4 + 0.6 * (1 - niveau(ti)));
        const x = cx + (h(i, 2) - 0.5) * 70 + (h(i, 3) - 0.5) * 60 * age + 3 * Math.sin(9 * age + i);
        const y = surface(ti) + prof * (1 - Math.exp(-age / 0.07)) - (150 + 110 * h(i, 4)) * Math.max(0, age - 0.06);
        if (y <= onde(x, t, yS, actif) + 3 || age > 2.5) continue;
        const r = 1.6 + 4 * h(i, 5) ** 2;
        ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.strokeStyle = BLANC + "0.6)"; ctx.stroke();
      }
      for (let i = 0; i < 90; i++) {
        const ti = tAtteint + 0.3 + i / 18;
        if (ti > t) break;
        const age = t - ti, x0 = cx - g.demi + 18 + (2 * g.demi - 36) * h(i, 6);
        const x = x0 + 4 * Math.sin(6 * age + 7 * h(i, 7));
        const y = g.bas - 10 - (110 + 140 * h(i, 8)) * age;
        if (y <= onde(x, t, yS, actif) + 3) continue;
        ctx.beginPath(); ctx.arc(x, y, 1.3 + 2.2 * h(i, 9), 0, 7); ctx.strokeStyle = BLANC + "0.45)"; ctx.stroke();
      }
      // Ménisque
      ctx.beginPath(); ctx.moveTo(x0, onde(x0, t, yS, actif));
      for (let x = x0; x <= x1; x += 4) ctx.lineTo(x, onde(x, t, yS, actif));
      ctx.lineWidth = 3; ctx.strokeStyle = BLANC + "0.55)"; ctx.stroke();
      // Écume au point d'impact
      if (actif > 0.05) {
        ctx.fillStyle = BLANC + (0.5 * actif).toFixed(3) + ")";
        for (let k = 0; k < 4; k++) {
          const ph = Math.floor(t * 30) + k * 17;
          ctx.beginPath();
          ctx.ellipse(cx + (h(ph, 10) - 0.5) * 26, yS + 2 + (h(ph, 11) - 0.5) * 3, 10 + 14 * h(ph, 12), 3 + 3 * h(ph, 13), 0, 0, 7);
          ctx.fill();
        }
      }
    }
    ctx.restore();

    jet(t, yS);

    // Gouttes projetées à l'impact (balistiques) et gouttes qui tombent de la buse après la fermeture
    ctx.fillStyle = OR;
    for (let i = 0; i < 140; i++) {
      const ti = tAtteint + 0.02 + i / 30;
      if (ti > Math.min(t, R.ferme)) break;
      const age = t - ti, vx = (h(i, 14) - 0.5) * 520, vy = -(700 + 800 * h(i, 15));
      const y0 = surface(ti), x = cx + (h(i, 16) - 0.5) * 16 + vx * age, y = y0 + vy * age + 0.5 * G * age * age;
      if (age > 0.3 || (age > 0.02 && y > surface(t))) continue;
      ctx.beginPath(); ctx.arc(x, y, 1.8 + 2.4 * h(i, 17), 0, 7); ctx.fill();
    }
    for (const td of R.gouttes) {                          // la goutte grossit 0,12 s au bout de la buse, puis tombe
      if (t < td) continue;
      const age = t - td;
      if (age < 0.12) { const c = age / 0.12; ctx.beginPath(); ctx.ellipse(cx, yn + 4 * c, 4 * c, 5 * c, 0, 0, 7); ctx.fill(); continue; }
      const y = yn + 4 + 0.5 * G * (age - 0.12) ** 2;
      if (y > surface(t)) continue;
      ctx.beginPath(); ctx.ellipse(cx, y, 4, 6, 0, 0, 7); ctx.fill();
    }

    // Paroi : contour, reflet vertical, lèvre du goulot, graduation de la contenance servie
    ctx.lineJoin = "round";
    contour(false); ctx.lineWidth = 6; ctx.strokeStyle = BLANC + "0.92)"; ctx.stroke();
    ctx.fillStyle = BLANC + "0.16)";
    ctx.fillRect(cx - g.demi + 20, g.corps + 30, 9, g.bas - g.corps - 80);
    ctx.fillStyle = BLANC + "0.92)";
    ctx.fillRect(cx - g.demiCol - 12, g.col - 6, 2 * g.demiCol + 24, 10);
    ctx.fillStyle = OR;
    ctx.fillRect(cx + g.demi - 34, yPlein - 2, 34, 4);
    for (let k = 1; k < 7; k++) {
      const y = yFond - (yFond - yPlein) * k / 7;
      ctx.fillStyle = BLANC + "0.35)"; ctx.fillRect(cx + g.demi - 18, y - 1, 18, 2);
    }
  }
  rendre.niveau = niveau;                                 // le compteur de contenance suit le même niveau
  return rendre;
}
