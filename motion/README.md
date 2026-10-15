# Studio vidéo / motion design – LA SALLE / LE CUBE

Remotion 4 (vidéo en React) + outils de montage, son, sous-titres et vectorisation.
Tout s'installe avec `bash scripts/setup-video-tools.sh` (à la racine du dépôt, idempotent).
Le conteneur cloud étant éphémère, **relancer ce script au début de chaque session**.

## Commandes

```bash
cd motion
npm run studio          # éditeur Remotion (prévisualisation, timeline)
npm run compositions    # liste des compositions
npm run render:test     # rend out/brand-intro.mp4 (démo 9:16, 4,5 s, ~25 s)
npm run still           # rend out/poster.png
npx remotion render src/index.ts <Id> out/<fichier>.mp4
```

## Ce qui est installé

**Remotion** (tous les `@remotion/*` sont en version exacte 4.0.535 : ne jamais les faire diverger)

| Besoin | Module |
|---|---|
| Transitions entre plans | `@remotion/transitions` (slide, wipe, fade…) |
| Flou de mouvement | `@remotion/motion-blur` |
| Trait qui se dessine, formes | `@remotion/paths`, `@remotion/shapes` |
| Fond organique / grain | `@remotion/noise` |
| Texte qui tient dans une largeur | `@remotion/layout-utils` (`fitText`) |
| Animations After Effects | `@remotion/lottie` (+ `lottie-web`) |
| 3D | `@remotion/three` (+ `three`, `@react-three/fiber`) |
| Audio / vidéo, spectre, durée | `@remotion/media`, `@remotion/media-utils` |
| Sous-titres (format) | `@remotion/captions` |
| GIF, fuites de lumière, easing | `@remotion/gif`, `@remotion/light-leaks`, `@remotion/animation-utils` |
| Polices locales, Tailwind 4 | `@remotion/fonts`, `@remotion/tailwind-v4` |

**Polices** (`@fontsource`, copiées dans `public/fonts` au `npm install`) : Barlow Condensed 700–900 (+ italiques),
DM Sans, Inter, Anton, Bebas Neue. Charge via `src/fonts.ts` : le rendu attend les polices.

**Système** : ffmpeg 6.1 (x264/x265/VP9/AV1/ProRes, libass, vidstab, loudnorm), sox, mediainfo, exiftool,
gifsicle, potrace (vectorisation), librsvg, ImageMagick, polices emoji.

**Python** : Pillow 12 + RAQM (crénage), fonttools + brotli (woff2 → ttf), OpenCV (headless), librosa
(battements), PySceneDetect (détection de plans), pydub, soundfile, **faster-whisper** (sous-titres).

## Charte et réglages de rendu

- `src/theme.ts` : couleurs « Le Trait Oblique », pente du trait (tan 0,42), 30 i/s, 120 BPM = 15 images/battement,
  zones de sécurité Reels (y 290–1250, x 72–1008).
- Export : H.264, `yuv420p`, `bt709`, CRF 19 (≈ 22 Mo pour 15 s). Vérifié par `ffprobe`.
- `src/compositions/BrandIntro.tsx` est une démo : texte « slam » posé dès la frame 0, trait or, coupes calées
  sur le battement, pastille d'offre permanente. À dupliquer, pas à livrer telle quelle.

## Sous-titres automatiques (faster-whisper)

```python
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")   # téléchargé depuis huggingface.co
segments, _ = m.transcribe("voix.wav", language="fr", word_timestamps=True)
```

## Caler les coupes sur la musique (librosa)

Utiliser les **positions** de battement (`librosa.beat.beat_track` → `librosa.frames_to_time`), pas la valeur de
tempo seule : sur des clics exacts à 120 BPM, l'estimation sort ≈ 117,5.

## Limites de ce conteneur (testées)

- **Chrome Headless Shell ne se télécharge pas** (storage.googleapis.com bloqué) : `remotion.config.ts` utilise
  le Chromium déjà présent (`/opt/pw-browsers`) ; surcharge possible avec `BROWSER_EXECUTABLE`.
- **GitHub, remotion.media, Google Fonts inaccessibles** : pas de `@remotion/install-whisper-cpp` (compile depuis
  GitHub), pas de `@remotion/sfx` (sons distants), pas de `@remotion/google-fonts`. D'où les polices locales.
- **Ne pas installer moviepy** : il impose Pillow < 12 (a déjà cassé `pdfplumber` et le crénage du kit pub).
- `pip check` signale `scenedetect requires opencv-python` : sans conséquence, `cv2` vient du paquet headless.
- Non installés volontairement : Blender (3D lourd, `@remotion/three` couvre l'essentiel), Whisper.cpp.
