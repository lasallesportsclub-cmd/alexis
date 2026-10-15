import {existsSync} from 'node:fs';
import {Config} from '@remotion/cli/config';
import {enableTailwind} from '@remotion/tailwind-v4';

// Chromium : on réutilise celui déjà présent dans le conteneur (le téléchargement
// de Chrome Headless Shell passe par storage.googleapis.com, bloqué ici).
const LOCAL_HEADLESS_SHELL = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
const browserExecutable =
  process.env.BROWSER_EXECUTABLE ?? (existsSync(LOCAL_HEADLESS_SHELL) ? LOCAL_HEADLESS_SHELL : null);
if (browserExecutable) {
  Config.setBrowserExecutable(browserExecutable);
  Config.setChromeMode('headless-shell');
}

Config.overrideWebpackConfig(enableTailwind);
Config.setOverwriteOutput(true);
Config.setVideoImageFormat('jpeg'); // plus rapide ; les stills PNG gardent le PNG
Config.setCodec('h264');
Config.setPixelFormat('yuv420p'); // compatibilité Meta / Instagram / TikTok
Config.setColorSpace('bt709'); // HD standard : évite le décalage de couleurs au réencodage
Config.setCrf(19); // même cible que la méthode « pub motion » (≈ 22 Mo pour 15 s)
Config.setX264Preset('medium');
Config.setEnforceAudioTrack(true);
