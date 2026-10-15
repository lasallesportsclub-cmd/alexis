import {noise2D} from '@remotion/noise';
import React from 'react';
import {useCurrentFrame} from 'remotion';
import {COLORS, SLASH_ANGLE_DEG} from '../theme';

const COLS = 14;
const ROWS = 26;

/** Champ de petits traits dorés orientés par un bruit de Perlin animé (fond vivant, discret). */
export const NoiseField: React.FC<{opacity?: number}> = ({opacity = 0.16}) => {
  const frame = useCurrentFrame();
  const cells: React.ReactNode[] = [];
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const n = noise2D('trait', c * 0.18 + frame * 0.012, r * 0.18);
      cells.push(
        <div
          key={`${r}-${c}`}
          style={{
            position: 'absolute',
            left: (c + 0.5) * (1080 / COLS),
            top: (r + 0.5) * (1920 / ROWS),
            width: 34,
            height: 3,
            marginLeft: -17,
            background: COLORS.orTaupe,
            transform: `rotate(${-SLASH_ANGLE_DEG + n * 55}deg)`,
          }}
        />,
      );
    }
  }
  return <div style={{position: 'absolute', inset: 0, opacity}}>{cells}</div>;
};
