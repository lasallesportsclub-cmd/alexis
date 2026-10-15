#!/usr/bin/env bash
# Installe tout le studio vidéo / motion design : paquets système, Python, Remotion.
# Idempotent. Pensé pour le conteneur cloud (éphémère) : relancer à chaque nouvelle session.
set -euo pipefail
cd "$(dirname "$0")/.."

PIP_FLAGS="${PIP_FLAGS:---break-system-packages}"   # conteneur jetable ; PIP_FLAGS="" dans un venv

echo "==> 1/3 Paquets système (sox, mediainfo, exiftool, gifsicle, potrace, rsvg, emoji, ffmpeg)"
if command -v apt-get >/dev/null && [ "$(id -u)" = 0 ]; then
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get install -y -qq --no-install-recommends \
    ffmpeg sox libsox-fmt-all mediainfo libimage-exiftool-perl gifsicle potrace \
    librsvg2-bin fonts-noto-color-emoji fontconfig
else
  echo "   (apt non disponible ou pas root : étape ignorée)"
fi

echo "==> 2/3 Python (fonttools, OpenCV, librosa, PySceneDetect, faster-whisper…)"
# shellcheck disable=SC2086
pip install $PIP_FLAGS --no-input -q -r motion/requirements.txt
# shellcheck disable=SC2086
pip install $PIP_FLAGS --no-input -q --no-deps scenedetect

echo "==> 3/3 Remotion (npm ci depuis le lockfile)"
( cd motion && npm ci --no-audit --no-fund )

echo "==> Terminé. Studio : cd motion && npm run studio   |   Test : npm run render:test"
