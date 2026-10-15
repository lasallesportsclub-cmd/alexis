import React from 'react';
import {Composition, Still} from 'remotion';
import './fonts';
import {BRAND_INTRO_DURATION, BrandIntro} from './compositions/BrandIntro';
import {Poster} from './compositions/Poster';
import {FPS} from './theme';

export const RemotionRoot: React.FC = () => (
  <>
    {/* 9:16 – Reels / Stories / TikTok */}
    <Composition id="BrandIntro" component={BrandIntro} durationInFrames={BRAND_INTRO_DURATION} fps={FPS} width={1080} height={1920} />
    <Still id="Poster" component={Poster} width={1080} height={1920} />
  </>
);
