#!/usr/bin/env bash
# Arranca Ollama en 127.0.0.1:11434 (solo localhost). Sin systemd.
# Pesos en /workspace/ollama/models (fuera del repo; no versionar).
# Binario de usuario: /workspace/tools/ollama (tarball oficial v0.40.16).
set -euo pipefail
umask 077

OLLAMA_ROOT="${OLLAMA_ROOT:-/workspace/tools/ollama}"
BIN="${OLLAMA_BIN:-$OLLAMA_ROOT/bin/ollama}"
export OLLAMA_HOST="${OLLAMA_HOST:-127.0.0.1:11434}"
export OLLAMA_MODELS="${OLLAMA_MODELS:-/workspace/ollama/models}"
LOGF="${OLLAMA_LOG_FILE:-/workspace/logs/ollama.log}"
PIDF="${OLLAMA_PID_FILE:-/workspace/logs/ollama.pid}"

if [ ! -x "$BIN" ]; then
  echo "ERROR: no encuentro el binario de Ollama: $BIN" >&2
  exit 1
fi

mkdir -p "$(dirname "$LOGF")" "$(dirname "$PIDF")" "$OLLAMA_MODELS"

if [ -f "$PIDF" ] && kill -0 "$(cat "$PIDF")" 2>/dev/null; then
  echo "Ollama ya en marcha: pid $(cat "$PIDF") $OLLAMA_HOST"
  exit 0
fi

# Evitar arrancar un segundo serve si el puerto ya está ocupado
if command -v ss >/dev/null 2>&1; then
  if ss -lptn 2>/dev/null | grep -q ':11434'; then
    echo "ERROR: el puerto 11434 ya está ocupado y no es este pidfile" >&2
    exit 1
  fi
fi

# El binario busca ../lib/ollama respecto a bin/
export PATH="$(dirname "$BIN"):$PATH"

nohup "$BIN" serve >> "$LOGF" 2>&1 &
echo $! > "$PIDF"
echo "Ollama pid $(cat "$PIDF") → http://${OLLAMA_HOST}  modelos=${OLLAMA_MODELS}"
