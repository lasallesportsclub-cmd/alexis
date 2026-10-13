#!/usr/bin/env bash
# Installe les outils audio locaux et gratuits de HyperFrames dans une session cloud :
#   - whisper.cpp  (transcription, `npx hyperframes transcribe`)  — licence MIT
#   - Kokoro       (voix de synthèse, `npx hyperframes tts`)       — licence Apache-2.0
#   - MusicGen     (musique générée, repli BGM de media-use)        — poids CC-BY-NC 4.0 : usage NON commercial
# Le conteneur cloud est effacé entre les sessions : relancer ce script au début d'une nouvelle session.
# Réseau requis : github.com, huggingface.co, *.hf.co, pypi.org, archive.ubuntu.com (environnement « a », accès Custom).
# Usage : bash "motion design/_outils/installer_audio_local.sh"   (≈ 10 min, ≈ 6 Go : PyTorch vient de PyPI)
# Tests du 13/10/2026 : Kokoro ff_siwis 8,3 s de voix en 30 s ; whisper small (fr) 8,4 s en 19 s ;
# MusicGen small 10 s de musique en 46 s (CPU 4 cœurs).
set -euo pipefail

VENV="${HOME}/.venvs/hyperframes-audio"
WHISPER_SRC="${HOME}/.local/src/whisper.cpp"
log() { printf '\n== %s\n' "$*"; }

log "Paquets système (espeak-ng pour le français de Kokoro, cmake pour whisper.cpp)"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq espeak-ng libsndfile1 cmake build-essential >/dev/null

log "whisper.cpp : compilation (whisper-cli)"
if ! command -v whisper-cli >/dev/null; then
  rm -rf "$WHISPER_SRC"
  git clone --depth 1 -q https://github.com/ggml-org/whisper.cpp.git "$WHISPER_SRC"
  cmake -S "$WHISPER_SRC" -B "$WHISPER_SRC/build" -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DWHISPER_BUILD_TESTS=OFF >/dev/null
  cmake --build "$WHISPER_SRC/build" -j"$(nproc)" --config Release --target whisper-cli >/dev/null
  install -m 0755 "$WHISPER_SRC/build/bin/whisper-cli" /usr/local/bin/whisper-cli
fi
whisper-cli --help >/dev/null 2>&1 && echo "whisper-cli : OK ($(command -v whisper-cli))"

log "Python : environnement dédié avec Kokoro et MusicGen"
command -v uv >/dev/null || python3 -m pip install -q --user uv
[ -x "$VENV/bin/python" ] || uv venv -q "$VENV"
uv pip install -q --python "$VENV/bin/python" kokoro-onnx soundfile numpy transformers torch
"$VENV/bin/python" -c "import kokoro_onnx, soundfile, transformers, torch; print('kokoro-onnx', 'torch', torch.__version__, 'transformers', transformers.__version__, ': OK')"

log "HyperFrames utilisera ce Python (HYPERFRAMES_PYTHON) et le proxy pour ses téléchargements Node (NODE_USE_ENV_PROXY)"
for rc in "${HOME}/.bashrc" "${HOME}/.profile"; do
  grep -q 'HYPERFRAMES_PYTHON=' "$rc" 2>/dev/null || echo "export HYPERFRAMES_PYTHON=\"$VENV/bin/python\"" >> "$rc"
  # sans cette variable, `hyperframes transcribe` échoue au téléchargement du modèle Whisper (getaddrinfo ENOTFOUND)
  grep -q 'NODE_USE_ENV_PROXY=' "$rc" 2>/dev/null || echo "export NODE_USE_ENV_PROXY=1" >> "$rc"
done
export HYPERFRAMES_PYTHON="$VENV/bin/python" NODE_USE_ENV_PROXY=1
echo "HYPERFRAMES_PYTHON=$HYPERFRAMES_PYTHON"
echo "Terminé. Vérifier avec : npx hyperframes doctor"
