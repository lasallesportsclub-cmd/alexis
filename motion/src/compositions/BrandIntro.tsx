import {linearTiming, TransitionSeries} from '@remotion/transitions';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
import {CameraMotionBlur} from '@remotion/motion-blur';
import {Rect} from '@remotion/shapes';
import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {NoiseField} from '../components/NoiseField';
import {Pastille} from '../components/Pastille';
import {Slash} from '../components/Slash';
import {COLORS, FONT, FRAMES_PER_BEAT, SAFE} from '../theme';
import {useFittedFontSize} from '../useFit';

const SCENE = 75;
const TRANSITION = 15;
export const BRAND_INTRO_DURATION = SCENE * 2 - TRANSITION;

// Règle n°1 : la promesse est déjà à l'écran à la frame 0. L'animation « slam » démarre
// 0,12 s (≈ 4 images) avant t0, donc le texte est net dès la première image.
const SLAM_LEAD = 4;

const Hook: React.FC = () => {
  const frame = useCurrentFrame() + SLAM_LEAD;
  const {fps} = useVideoConfig();
  const size = useFittedFontSize({
    text: 'ÇA COMMENCE ICI',
    width: SAFE.x1 - SAFE.x0,
    fontFamily: 'Barlow Condensed',
    fontWeight: '900',
    maxSize: 260,
  });
  const slam = spring({frame, fps, config: {damping: 11, stiffness: 190, mass: 0.7}});
  const scale = interpolate(slam, [0, 1], [1.45, 1]);
  const sub = interpolate(frame, [10, 24], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});

  return (
    <AbsoluteFill style={{background: COLORS.noir}}>
      <NoiseField />
      <CameraMotionBlur samples={8} shutterAngle={140}>
        <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
          <div
            style={{
              fontFamily: FONT.titre,
              fontWeight: 900,
              fontSize: size,
              lineHeight: 0.95,
              color: COLORS.blancCasse,
              transform: `scale(${scale})`,
              opacity: interpolate(slam, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'}),
              whiteSpace: 'nowrap',
            }}
          >
            ÇA COMMENCE ICI
          </div>
        </AbsoluteFill>
      </CameraMotionBlur>
      <Slash progress={interpolate(frame, [4, 26], [0, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)})} y={820} />
      <div
        style={{
          position: 'absolute',
          left: SAFE.x0,
          right: 1080 - SAFE.x1,
          top: 1090,
          fontFamily: FONT.texte,
          fontWeight: 500,
          fontSize: 44,
          color: COLORS.blancCasse,
          opacity: sub,
          transform: `translateY(${(1 - sub) * 24}px)`,
        }}
      >
        Démo motion · Remotion 4 × Le Trait Oblique
      </div>
    </AbsoluteFill>
  );
};

const Montage: React.FC = () => {
  const frame = useCurrentFrame();
  const beat = Math.floor(frame / FRAMES_PER_BEAT);
  const idx = Math.min(4, (beat % 4) + 1);
  const inBeat = frame % FRAMES_PER_BEAT;
  const zoom = interpolate(frame, [0, SCENE], [1.0, 1.12]);
  const bar = interpolate(frame, [0, SCENE], [0, 1], {extrapolateRight: 'clamp'});
  const w = SAFE.x1 - SAFE.x0;

  return (
    <AbsoluteFill style={{background: COLORS.anthracite}}>
      {/* Emplacement d'un plan vidéo : zoom lent permanent (règle n°2) */}
      <AbsoluteFill style={{transform: `scale(${zoom})`}}>
        <div
          style={{
            position: 'absolute',
            left: SAFE.x0,
            top: SAFE.y0 + 160,
            width: w,
            height: 560,
            background: `linear-gradient(135deg, ${COLORS.noir}, ${COLORS.anthracite} 60%)`,
            border: `2px solid ${COLORS.orTaupe}`,
          }}
        />
      </AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          left: SAFE.x0,
          top: SAFE.y0 + 760,
          fontFamily: FONT.titre,
          fontWeight: 800,
          fontStyle: 'italic',
          fontSize: 120,
          color: COLORS.blancCasse,
          transform: `translateX(${interpolate(inBeat, [0, 5], [-60, 0], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)})}px)`,
          opacity: interpolate(inBeat, [0, 4], [0, 1], {extrapolateRight: 'clamp'}),
        }}
      >
        {String(idx).padStart(2, '0')} PLAN
      </div>
      {/* Barre de progression « Visite express » */}
      <div style={{position: 'absolute', left: SAFE.x0, top: SAFE.y1 - 20}}>
        <Rect width={w} height={8} fill="rgba(244,241,236,0.18)" />
      </div>
      <div style={{position: 'absolute', left: SAFE.x0, top: SAFE.y1 - 20}}>
        <Rect width={Math.max(1, w * bar)} height={8} fill={COLORS.orTaupe} />
      </div>
    </AbsoluteFill>
  );
};

export const BrandIntro: React.FC = () => (
  <AbsoluteFill style={{background: COLORS.noir}}>
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={SCENE}>
        <Hook />
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition presentation={wipe({direction: 'from-left'})} timing={linearTiming({durationInFrames: TRANSITION})} />
      <TransitionSeries.Sequence durationInFrames={SCENE}>
        <Montage />
      </TransitionSeries.Sequence>
    </TransitionSeries>
    <Pastille label="Offre limitée" />
  </AbsoluteFill>
);

// `slide` est ré-exporté pour les compositions futures (autre style de transition).
export {slide};
