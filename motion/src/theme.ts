// Charte « Le Trait Oblique » – LA SALLE / LE CUBE
export const COLORS = {
  noir: '#0D0D0D',
  blancCasse: '#F4F1EC',
  orTaupe: '#B8A07E',
  anthracite: '#222222',
} as const;

// Pente du trait incliné du monogramme : tan(θ) = 0,42
export const SLASH_TAN = 0.42;
export const SLASH_ANGLE_DEG = (Math.atan(SLASH_TAN) * 180) / Math.PI; // ≈ 22,8°

// Tempo des coupes (une coupe toutes les 0,5 à 1 s à 120 BPM)
export const BPM = 120;
export const FPS = 30;
export const FRAMES_PER_BEAT = (FPS * 60) / BPM; // 15 images

// Zones de sécurité Reels / Stories 1080×1920
export const SAFE = {x0: 72, x1: 1008, y0: 290, y1: 1250} as const;

export const FONT = {
  titre: '"Barlow Condensed", sans-serif', // 800–900, capitales
  texte: '"DM Sans", sans-serif',
} as const;
