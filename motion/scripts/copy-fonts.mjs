// Copie les polices (woff2, sous-ensemble latin) de @fontsource vers public/fonts.
// Remotion les charge ensuite avec staticFile() → rendu 100 % hors-ligne.
import {cpSync, existsSync, mkdirSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const out = join(root, 'public', 'fonts');
const FILES = {
  'barlow-condensed': ['700-normal', '800-normal', '800-italic', '900-normal', '900-italic'],
  'dm-sans': ['400-normal', '500-normal', '700-normal'],
  inter: ['400-normal', '600-normal', '800-normal'],
  anton: ['400-normal'],
  'bebas-neue': ['400-normal'],
};

mkdirSync(out, {recursive: true});
let copied = 0;
for (const [pkg, variants] of Object.entries(FILES)) {
  for (const v of variants) {
    const name = `${pkg}-latin-${v}.woff2`;
    const src = join(root, 'node_modules', '@fontsource', pkg, 'files', name);
    if (!existsSync(src)) {
      console.warn(`[fonts] introuvable : ${name}`);
      continue;
    }
    cpSync(src, join(out, name));
    copied++;
  }
}
console.log(`[fonts] ${copied} fichiers copiés dans public/fonts`);
