import React from 'react';
import {AbsoluteFill} from 'remotion';
import {NoiseField} from '../components/NoiseField';
import {Pastille} from '../components/Pastille';
import {Slash} from '../components/Slash';
import {COLORS, FONT, SAFE} from '../theme';
import {useFittedFontSize} from '../useFit';

export const Poster: React.FC = () => {
  const size = useFittedFontSize({
    text: 'ÇA COMMENCE ICI',
    width: SAFE.x1 - SAFE.x0,
    fontFamily: 'Barlow Condensed',
    fontWeight: '900',
    maxSize: 260,
  });
  return (
    <AbsoluteFill style={{background: COLORS.noir}}>
      <NoiseField />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div style={{fontFamily: FONT.titre, fontWeight: 900, fontSize: size, lineHeight: 0.95, color: COLORS.blancCasse, whiteSpace: 'nowrap'}}>
          ÇA COMMENCE ICI
        </div>
      </AbsoluteFill>
      <Slash progress={1} y={820} />
      <Pastille label="Offre limitée" />
    </AbsoluteFill>
  );
};
