// Avatar scanné de la story Visbody (scène « UN SCAN À 360° ») : silhouette humaine grise (femme athlétique, cheveux
// en chignon, comme les avatars de la référence fournie), vue de dos, bras le long du corps, debout sur le plateau. Surface lisse d'un seul tenant : distance signée à des formes simples fusionnées en
// douceur aux articulations, polygonisée par marching cubes (Three.js). Aucun modèle téléchargé.
// Rendu image par image depuis le temps de la scène (seek déterministe) : creer() renvoie rendre(t).
//
// Déroulé (instants fournis par tools/build.py, en secondes depuis le début de la scène) :
//   plateau  : le plateau et son filet or s'ouvrent
//   montee   : l'avatar sort du plateau (glissement masqué par le dessus du plateau)
//   descente : le scan passe de la tête aux pieds et trace les tours (lignes horizontales)
//   remontee : il remonte et trace les lignes verticales : l'avatar finit maillé en 3D
import * as THREE from "../vendor/three.module.min.js";
import { MarchingCubes } from "../vendor/MarchingCubes.js";

const OR = new THREE.Color("#B8A07E");
const HAUT = 1.78;           // au-dessus du chignon
const BAS = -0.01;           // sous les pieds

const lisse = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
const sinus = (x) => 0.5 - 0.5 * Math.cos(Math.PI * Math.min(1, Math.max(0, x)));
const sortie = (x) => 1 - Math.pow(1 - Math.min(1, Math.max(0, x)), 3);

// ---------- corps : distance signée à une silhouette faite de formes simples fusionnées en douceur ----------
function smin(a, b, k) { const h = Math.max(k - Math.abs(a - b), 0) / k; return Math.min(a, b) - h * h * k * 0.25; }

function ellipsoide(px, py, pz, cx, cy, cz, rx, ry, rz) {
  const x = (px - cx) / rx, y = (py - cy) / ry, z = (pz - cz) / rz;
  const k0 = Math.hypot(x, y, z);
  const k1 = Math.hypot(x / rx, y / ry, z / rz);
  return k1 > 0 ? k0 * (k0 - 1) / k1 : -Math.min(rx, ry, rz);
}

function cone(px, py, pz, a, b, r1, r2) {
  // Cône arrondi entre deux sphères (formule d'Inigo Quilez)
  const bx = b[0] - a[0], by = b[1] - a[1], bz = b[2] - a[2];
  const l2 = bx * bx + by * by + bz * bz, rr = r1 - r2, a2 = l2 - rr * rr, il2 = 1 / l2;
  const qx = px - a[0], qy = py - a[1], qz = pz - a[2];
  const y = qx * bx + qy * by + qz * bz, z = y - l2;
  const cx = qx * l2 - bx * y, cy = qy * l2 - by * y, cz = qz * l2 - bz * y;
  const x2 = cx * cx + cy * cy + cz * cz, y2 = y * y * l2, z2 = z * z * l2;
  const k = Math.sign(rr) * rr * rr * x2;
  if (Math.sign(z) * a2 * z2 > k) return Math.sqrt(x2 + z2) * il2 - r2;
  if (Math.sign(y) * a2 * y2 < k) return Math.sqrt(x2 + y2) * il2 - r1;
  return (Math.sqrt(x2 * a2 * il2) + y * rr) * il2 - r1;
}

function smax(a, b, k) { return -smin(-a, -b, k); }

function silhouette(x, y, z) {
  // Femme athlétique, vue de dos (comme les avatars de la référence) : elle regarde vers +z, la caméra est derrière.
  // Mètres, pieds à y = 0, 1,72 m chignon compris. X = |x| : les deux côtés sont symétriques.
  if (Math.abs(x) > 0.34 || Math.abs(z) > 0.22 || y > 1.8 || y < -0.01) return 0.05;
  const X = Math.abs(x);
  // Tête : crâne, occiput, mâchoire, oreilles, cheveux tirés en chignon
  let t = ellipsoide(x, y, z, 0, 1.615, 0, 0.078, 0.092, 0.095);
  t = smin(t, ellipsoide(x, y, z, 0, 1.6, -0.025, 0.07, 0.075, 0.07), 0.03);
  t = smin(t, ellipsoide(x, y, z, 0, 1.535, 0.035, 0.06, 0.06, 0.065), 0.04);
  t = smin(t, ellipsoide(X, y, z, 0.077, 1.585, 0.01, 0.013, 0.03, 0.02), 0.008);
  t = smin(t, smax(ellipsoide(x, y, z, 0, 1.625, -0.006, 0.083, 0.096, 0.1), 1.556 - y, 0.012), 0.006);
  t = smin(t, ellipsoide(x, y, z, 0, 1.655, -0.098, 0.046, 0.043, 0.041), 0.02);
  // Cou et trapèzes
  t = smin(t, cone(x, y, z, [0, 1.37, -0.005], [0, 1.53, 0.005], 0.052, 0.046), 0.03);
  t = smin(t, cone(X, y, z, [0, 1.465, -0.022], [0.14, 1.4, -0.012], 0.036, 0.03), 0.05);
  // Tronc : épaules, cage thoracique, poitrine, omoplates, dorsaux, taille, bassin, fessiers
  t = smin(t, ellipsoide(X, y, z, 0.165, 1.365, 0, 0.05, 0.06, 0.055), 0.035);
  t = smin(t, ellipsoide(x, y, z, 0, 1.25, 0.005, 0.135, 0.15, 0.095), 0.06);
  t = smin(t, ellipsoide(X, y, z, 0.056, 1.245, 0.07, 0.055, 0.05, 0.045), 0.03);
  t = smin(t, ellipsoide(X, y, z, 0.075, 1.29, -0.07, 0.06, 0.075, 0.03), 0.04);
  t = smin(t, ellipsoide(X, y, z, 0.082, 1.17, -0.03, 0.05, 0.1, 0.05), 0.05);
  t = smin(t, ellipsoide(x, y, z, 0, 1.06, 0, 0.11, 0.11, 0.08), 0.07);
  t = smin(t, ellipsoide(x, y, z, 0, 0.92, 0, 0.15, 0.12, 0.1), 0.07);
  t = smin(t, ellipsoide(X, y, z, 0.065, 0.885, -0.04, 0.078, 0.085, 0.07), 0.035);
  // Sillon de la colonne et pli fessier, en creux
  t = smax(t, -cone(x, y, z, [0, 1.36, -0.104], [0, 1.0, -0.088], 0.011, 0.011), 0.02);
  t = smax(t, -cone(x, y, z, [0, 0.95, -0.118], [0, 0.82, -0.1], 0.009, 0.009), 0.015);
  // Jambes : cuisse, ischios, genou, mollet, tibia, tendon, malléole, talon, pied
  let j = cone(X, y, z, [0.085, 0.86, 0], [0.075, 0.5, 0.005], 0.078, 0.048);
  j = smin(j, ellipsoide(X, y, z, 0.08, 0.68, -0.03, 0.06, 0.13, 0.055), 0.03);
  j = smin(j, ellipsoide(X, y, z, 0.075, 0.48, 0.01, 0.045, 0.04, 0.045), 0.02);
  j = smin(j, ellipsoide(X, y, z, 0.078, 0.36, -0.03, 0.05, 0.09, 0.048), 0.03);
  j = smin(j, cone(X, y, z, [0.075, 0.47, 0.005], [0.078, 0.08, 0], 0.045, 0.026), 0.025);
  j = smin(j, cone(X, y, z, [0.078, 0.2, -0.02], [0.078, 0.06, -0.025], 0.03, 0.025), 0.02);
  j = smin(j, ellipsoide(X, y, z, 0.078, 0.035, -0.03, 0.032, 0.032, 0.04), 0.02);
  j = smin(j, ellipsoide(X, y, z, 0.082, 0.03, 0.06, 0.04, 0.03, 0.1), 0.02);
  t = smin(t, j, 0.04);
  t = smin(t, cone(-X, y, z, [0.085, 0.86, 0], [0.075, 0.5, 0.005], 0.078, 0.048), 0.03);   // cuisse opposée
  // Bras détendus le long du corps : épaule, biceps/triceps, coude, avant-bras, main, pouce
  let b = cone(X, y, z, [0.175, 1.35, 0], [0.215, 1.08, -0.015], 0.045, 0.034);
  b = smin(b, ellipsoide(X, y, z, 0.198, 1.22, -0.01, 0.042, 0.09, 0.044), 0.03);
  b = smin(b, ellipsoide(X, y, z, 0.217, 1.075, -0.025, 0.03, 0.03, 0.03), 0.02);
  b = smin(b, cone(X, y, z, [0.217, 1.075, -0.01], [0.237, 0.84, 0.02], 0.036, 0.024), 0.02);
  b = smin(b, ellipsoide(X, y, z, 0.222, 1.01, 0, 0.036, 0.065, 0.038), 0.03);
  b = smin(b, ellipsoide(X, y, z, 0.242, 0.77, 0.028, 0.022, 0.07, 0.04), 0.015);
  b = smin(b, cone(X, y, z, [0.234, 0.8, 0.05], [0.227, 0.75, 0.062], 0.012, 0.01), 0.008);
  return smin(t, b, 0.012);
}

function corps(mat, resolution = 160) {
  // Boîte de calcul : x ±0,38 m, y −0,02 à 1,84 m, z ±0,24 m, remplie puis polygonisée (marching cubes)
  const EX = 0.38, EY = 0.93, CY = 0.91, EZ = 0.24;
  const mc = new MarchingCubes(resolution, mat, false, false, 400000);
  const n = resolution, h = n / 2, f = mc.field, iso = mc.isolation;
  for (let k = 0; k < n; k++) {
    const z = ((k - h) / h) * EZ;
    for (let j = 0; j < n; j++) {
      const y = ((j - h) / h) * EY + CY;
      for (let i = 0; i < n; i++) {
        const x = ((i - h) / h) * EX;
        f[i + j * n + k * n * n] = iso - 2000 * silhouette(x, y, z);
      }
    }
  }
  mc.update();
  mc.scale.set(EX, EY, EZ);
  mc.position.y = CY;
  const g = new THREE.Group();
  g.add(mc);
  return g;
}

export function creer(canvas, R) {
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(R.largeur, R.hauteur, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.localClippingEnabled = true;
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(25, R.largeur / R.hauteur, 0.1, 50);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x262626, 1.15));
  const cle = new THREE.DirectionalLight(0xffffff, 1.7);
  cle.position.set(-2.2, 3.2, -3.5);                 // côté caméra, en hauteur : éclaire le dos
  scene.add(cle);
  const contre = new THREE.DirectionalLight(0xffffff, 1.4);
  contre.position.set(2.5, 2.0, 3.0);                // en face de l'avatar : liseré sur les contours
  scene.add(contre);

  // Matière grise ; le scan y ajoute ses lignes or (repère monde)
  const u = { uScanY: { value: -10 }, uActif: { value: 0 }, uTours: { value: -10 }, uMaille: { value: -10 }, uLevee: { value: 0 }, uOr: { value: OR } };
  const peau = new THREE.MeshStandardMaterial({ color: 0xb4b4b4, roughness: 0.55, metalness: 0 });
  const sol = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);   // l'avatar sort du plateau : rien sous y = 0
  peau.clippingPlanes = [sol];
  peau.onBeforeCompile = (s) => {
    Object.assign(s.uniforms, u);
    s.vertexShader = s.vertexShader
      .replace("#include <common>", "#include <common>\nvarying vec3 vMonde;")
      .replace("#include <project_vertex>", "#include <project_vertex>\nvMonde = (modelMatrix * vec4(transformed, 1.0)).xyz;");
    s.fragmentShader = s.fragmentShader
      .replace("#include <common>", `#include <common>
varying vec3 vMonde;
uniform float uScanY, uActif, uTours, uMaille, uLevee;
uniform vec3 uOr;
float trait(float f, float epaisseur) {
  float w = max(fwidth(f), 1e-4);
  return 1.0 - clamp((abs(fract(f - 0.5) - 0.5) / w - epaisseur * 0.5) , 0.0, 1.0);
}`)
      .replace("#include <color_fragment>", `#include <color_fragment>
diffuseColor.rgb *= 1.0 - 0.5 * smoothstep(1.552, 1.566, vMonde.y - uLevee);   // cheveux : gris plus soutenu`)
      .replace("#include <dithering_fragment>", `#include <dithering_fragment>
float y = vMonde.y;
float tours = trait(y / 0.04, 1.6) * step(uTours, y);                 // tracés au-dessus du front de descente
float maille = trait(vMonde.x / 0.045, 1.4) * step(y, uMaille);         // tracés sous le front de remontée
float bande = (1.0 - smoothstep(0.004, 0.014, abs(y - uScanY))) * uActif;
vec3 c = gl_FragColor.rgb;
c = mix(c, uOr, 0.85 * tours);
c = mix(c, uOr, 0.7 * maille);
c = mix(c, vec3(0.96, 0.93, 0.88), bande);
gl_FragColor.rgb = c;`);
  };
  const avatar = corps(peau);
  scene.add(avatar);

  // Plateau : disque sombre, filet or sur le pourtour
  const plateau = new THREE.Group();
  const disque = new THREE.Mesh(new THREE.CylinderGeometry(0.47, 0.47, 0.05, 128),
                                new THREE.MeshStandardMaterial({ color: 0x1f1f1f, roughness: 0.8 }));
  disque.position.y = -0.025;
  const pourtour = new THREE.Mesh(new THREE.TorusGeometry(0.47, 0.007, 12, 192), new THREE.MeshBasicMaterial({ color: OR }));
  pourtour.rotation.x = Math.PI / 2;
  plateau.add(disque, pourtour);
  scene.add(plateau);

  // Plan du scan : anneau or et voile or translucide, à plat
  const plan = new THREE.Group();
  const anneau = new THREE.Mesh(new THREE.RingGeometry(0.43, 0.437, 192),
                                new THREE.MeshBasicMaterial({ color: OR, side: THREE.DoubleSide }));
  const voile = new THREE.Mesh(new THREE.CircleGeometry(0.43, 192),
                               new THREE.MeshBasicMaterial({ color: OR, transparent: true, opacity: 0.12, side: THREE.DoubleSide, depthWrite: false }));
  for (const m of [anneau, voile]) { m.rotation.x = -Math.PI / 2; plan.add(m); }
  scene.add(plan);

  return function rendre(t) {
    // Caméra : derrière l'avatar, un peu au-dessus, lente avancée
    const d = 4.2 - 0.25 * lisse(0, R.fin, t);
    camera.position.set(0.18 * (1 - lisse(0, R.fin, t)), 1.05, -d);
    camera.lookAt(0, 0.9, 0);

    const p = sortie((t - R.plateau[0]) / R.plateau[1]);
    plateau.scale.set(Math.max(p, 1e-3), 1, Math.max(p, 1e-3));
    plateau.visible = p > 0;

    const m = sortie((t - R.montee[0]) / R.montee[1]);
    avatar.position.y = -1.9 * (1 - m);
    u.uLevee.value = avatar.position.y;
    avatar.visible = m > 0;

    const a = (t - R.descente[0]) / R.descente[1];
    const b = (t - R.remontee[0]) / R.remontee[1];
    let y = -10, actif = 0;
    if (a >= 0 && a <= 1) { y = HAUT + (BAS - HAUT) * sinus(a); actif = 1; }
    else if (b >= 0 && b <= 1) { y = BAS + (HAUT - BAS) * sinus(b); actif = 1; }
    u.uScanY.value = y;
    u.uActif.value = actif;
    u.uTours.value = a < 0 ? 10 : a <= 1 ? y : -10;             // tours : au-dessus du front, puis partout
    u.uMaille.value = b < 0 ? -10 : b <= 1 ? y : 10;            // maille : sous le front, puis partout
    plan.visible = actif > 0;
    plan.position.y = y;
    const r = 1 + 0.06 * Math.sin(Math.PI * Math.min(1, Math.max(0, a >= 0 && a <= 1 ? a : b)));
    plan.scale.set(r, 1, r);

    renderer.render(scene, camera);
  };
}
