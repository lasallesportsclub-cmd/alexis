import {evolvePath} from '@remotion/paths';
import React from 'react';
import {COLORS, SAFE, SLASH_TAN} from '../theme';

/** Le trait incliné du monogramme (pente tan = 0,42) qui se dessine de 0 à 1. */
export const Slash: React.FC<{progress: number; y?: number; stroke?: number; color?: string}> = ({
  progress,
  y = 1010,
  stroke = 10,
  color = COLORS.orTaupe,
}) => {
  const width = SAFE.x1 - SAFE.x0;
  const path = `M ${SAFE.x0} ${y} L ${SAFE.x1} ${y - width * SLASH_TAN}`;
  const {strokeDasharray, strokeDashoffset} = evolvePath(Math.min(1, Math.max(0, progress)), path);
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
      <path
        d={path}
        fill="none"
        stroke={color}
        strokeWidth={stroke}
        strokeLinecap="butt"
        strokeDasharray={strokeDasharray}
        strokeDashoffset={strokeDashoffset}
      />
    </svg>
  );
};
