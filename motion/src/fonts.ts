import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

type Face = {family: string; file: string; weight: string; style?: 'normal' | 'italic'};

const FACES: Face[] = [
  {family: 'Barlow Condensed', file: 'barlow-condensed-latin-700-normal', weight: '700'},
  {family: 'Barlow Condensed', file: 'barlow-condensed-latin-800-normal', weight: '800'},
  {family: 'Barlow Condensed', file: 'barlow-condensed-latin-800-italic', weight: '800', style: 'italic'},
  {family: 'Barlow Condensed', file: 'barlow-condensed-latin-900-normal', weight: '900'},
  {family: 'Barlow Condensed', file: 'barlow-condensed-latin-900-italic', weight: '900', style: 'italic'},
  {family: 'DM Sans', file: 'dm-sans-latin-400-normal', weight: '400'},
  {family: 'DM Sans', file: 'dm-sans-latin-500-normal', weight: '500'},
  {family: 'DM Sans', file: 'dm-sans-latin-700-normal', weight: '700'},
  {family: 'Inter', file: 'inter-latin-400-normal', weight: '400'},
  {family: 'Inter', file: 'inter-latin-600-normal', weight: '600'},
  {family: 'Inter', file: 'inter-latin-800-normal', weight: '800'},
  {family: 'Anton', file: 'anton-latin-400-normal', weight: '400'},
  {family: 'Bebas Neue', file: 'bebas-neue-latin-400-normal', weight: '400'},
];

// loadFont() retient le rendu (delayRender) tant que la police n'est pas prête :
// plus de texte rendu avec la police de secours.
export const fontsReady = Promise.all(
  FACES.map((f) =>
    loadFont({
      family: f.family,
      url: staticFile(`fonts/${f.file}.woff2`),
      weight: f.weight,
      style: f.style ?? 'normal',
    }),
  ),
);
