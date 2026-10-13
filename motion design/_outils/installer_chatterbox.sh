#!/usr/bin/env bash
# Installe Chatterbox (Resemble AI, licence MIT) pour cloner une voix à partir d'un enregistrement de référence.
# Environnement Python séparé : chatterbox-tts fixe torch 2.6 et transformers 5.2, incompatibles avec celui de
# installer_audio_local.sh (Kokoro, MusicGen).
# Les modèles (≈ 3 Go) se téléchargent depuis huggingface.co au premier usage, puis restent en cache.
# Les fichiers générés portent un filigrane inaudible (PerTh) qui les signale comme audio de synthèse.
# Usage : bash "motion design/_outils/installer_chatterbox.sh"   (≈ 10 min, ≈ 5 Go)
set -euo pipefail

VENV="${HOME}/.venvs/chatterbox"
log() { printf '\n== %s\n' "$*"; }

log "Environnement Python dédié"
command -v uv >/dev/null || python3 -m pip install -q --user uv
[ -x "$VENV/bin/python" ] || uv venv -q --python 3.12 "$VENV" || uv venv -q "$VENV"
uv pip install -q --python "$VENV/bin/python" chatterbox-tts soundfile
"$VENV/bin/python" -c "import torch, chatterbox; from chatterbox.mtl_tts import ChatterboxMultilingualTTS; print('chatterbox', 'torch', torch.__version__, ': OK')"

for rc in "${HOME}/.bashrc" "${HOME}/.profile"; do
  grep -q 'CHATTERBOX_PYTHON=' "$rc" 2>/dev/null || echo "export CHATTERBOX_PYTHON=\"$VENV/bin/python\"" >> "$rc"
done
echo "CHATTERBOX_PYTHON=$VENV/bin/python"
echo "Terminé. Générer : \$CHATTERBOX_PYTHON \"motion design/_outils/voix_clone.py\" --ref ref.wav --texte \"...\" -o sortie.wav"
