#!/usr/bin/env bash
# Arranca LiteLLM en 127.0.0.1:4000 con Grok y Gemini. Carga secretos sin mostrarlos.
set -euo pipefail
umask 077
REPO="$(cd "$(dirname "$0")/.." && pwd)"
PIDF="${LITELLM_PID_FILE:-/workspace/agsgpt/litellm.pid}"
LOGF="${LITELLM_LOG_FILE:-/workspace/agsgpt/litellm.log}"
VENV="${AGS_VENV:-/workspace/agsgpt/.venv}"
PORT="${LITELLM_PORT:-4000}"

if [ -f "$PIDF" ] && kill -0 "$(cat "$PIDF")" 2>/dev/null; then
  echo "LiteLLM ya en marcha: pid $(cat "$PIDF") puerto $PORT"
  exit 0
fi

# Cargar claves sin echo (set -a exporta; set +a deja de exportar)
set -a
[ -f "${HOME}/.secrets/xai.env" ] && . "${HOME}/.secrets/xai.env"
[ -f "${HOME}/.secrets/gemini.env" ] && . "${HOME}/.secrets/gemini.env"
[ -f "${REPO}/.env" ] && . "${REPO}/.env"
set +a

: "${LITELLM_MASTER_KEY:=local-dev-key}"
export LITELLM_MASTER_KEY

missing=()
[ -z "${GROK_API_KEY:-}" ] && missing+=(GROK_API_KEY)
[ -z "${GEMINI_API_KEY:-}" ] && missing+=(GEMINI_API_KEY)
if [ "${#missing[@]}" -gt 0 ]; then
  echo "AVISO: faltan en el entorno: ${missing[*]} (el proxy arranca; esos modelos fallarán)"
fi

cd "$REPO"
nohup "$VENV/bin/litellm" --config config/litellm.yaml --host 127.0.0.1 --port "$PORT" \
  >> "$LOGF" 2>&1 &
echo $! > "$PIDF"
echo "LiteLLM pid $(cat "$PIDF") → http://127.0.0.1:${PORT}"
