import {fitText} from '@remotion/layout-utils';
import {useEffect, useState} from 'react';
import {continueRender, delayRender} from 'remotion';
import {fontsReady} from './fonts';

/** Taille de police maximale qui fait tenir `text` dans `width` px (mesurée une fois les polices chargées). */
export const useFittedFontSize = (opts: {
  text: string;
  width: number;
  fontFamily: string;
  fontWeight: string;
  maxSize?: number;
}) => {
  const [handle] = useState(() => delayRender(`fit "${opts.text}"`));
  const [size, setSize] = useState(opts.maxSize ?? 200);

  useEffect(() => {
    fontsReady.then(() => {
      const {fontSize} = fitText({
        text: opts.text,
        withinWidth: opts.width,
        fontFamily: opts.fontFamily,
        fontWeight: opts.fontWeight,
      });
      setSize(Math.min(fontSize, opts.maxSize ?? Infinity));
      continueRender(handle);
    });
  }, [handle, opts.text, opts.width, opts.fontFamily, opts.fontWeight, opts.maxSize]);

  return size;
};
