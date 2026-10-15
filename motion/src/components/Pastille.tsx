import React from 'react';
import {COLORS, FONT, SAFE} from '../theme';

/** Pastille or, visible pendant tout le montage (règle n°4 de la méthode pub). */
export const Pastille: React.FC<{label: string}> = ({label}) => (
  <div
    className="absolute rounded-full px-8 py-3 tracking-widest"
    style={{
      left: SAFE.x0,
      top: SAFE.y0 + 10,
      background: COLORS.orTaupe,
      color: COLORS.noir,
      fontFamily: FONT.titre,
      fontWeight: 800,
      fontStyle: 'italic',
      fontSize: 40,
      textTransform: 'uppercase',
    }}
  >
    {label}
  </div>
);
