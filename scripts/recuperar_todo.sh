#!/usr/bin/env bash
# recuperar_todo.sh — recuperación idempotente del ecosistema AGs-Core tras una restauración del box.
# Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia: MIT.
#
# Qué hace (cada paso se puede repetir sin efectos dobles):
#   1. Recrea los entornos Python si faltan o si cambian sus requirements (huella sha256):
#        /workspace/agsgpt/.venv            (AGs-Core + UCS + matriz + HYBRIX L5 + LiteLLM)
#        /workspace/agsgpt/NNC/.venv        (NNC dashboard/servicio + Ojo de Dios)
#        /workspace/gh_verify/clones/nnc/.venv (solo pruebas del clon nnc, si existe el clon)
#   2. Borra archivos .pid obsoletos (proceso muerto o que no es el servicio esperado).
#   3. Arranca en segundo plano (nohup, logs en /workspace/agsgpt): LiteLLM :4000, API :8000,
#      UI :8501, UCS :8502, NNC :8080/:8010, matriz Streamlit :8510 y el autopilot.
#   4. Comprueba HTTP de cada servicio y el primer ciclo del autopilot.
# Nunca imprime claves: se cargan con `set -a; . archivo` solo dentro de los procesos que las usan.
# Uso: scripts/recuperar_todo.sh [--solo-venvs | --solo-servicios | --verificar]
set -euo pipefail

ROOT=/workspace/agsgpt
REPO=$ROOT/ags-core-v3.6
VENV=$ROOT/.venv
NNC_DIR=$ROOT/NNC
NNC_VENV=$NNC_DIR/.venv
NNC_CLONE=/workspace/gh_verify/clones/nnc
MATRIZ=/workspace/matriz-el-prat
PYBIN="${PYBIN:-python3}"
TORCH_INDEX="${TORCH_INDEX:-https://download.pytorch.org/whl/cpu}"
MODO="${1:-todo}"

log() { printf '[recuperar %s] %s\n' "$(date '+%F %T')" "$*"; }

have_uv() { command -v uv >/dev/null 2>&1; }

mk_venv() {  # mk_venv <dir>
  local d=$1
  if [ ! -x "$d/bin/python" ]; then
    log "creando venv $d"
    if have_uv; then uv venv -q --python "$PYBIN" "$d"; else "$PYBIN" -m venv "$d"; fi
  fi
}

pip_in() {  # pip_in <venv> <args...>
  local d=$1; shift
  if have_uv; then VIRTUAL_ENV="$d" uv pip install -q "$@"; else "$d/bin/python" -m pip install -q "$@"; fi
}

huella() { cat "$@" 2>/dev/null | sha256sum | cut -c1-16; }

ensure_venv() {  # ensure_venv <dir> <archivo_huella> <requirements...> -- <paquetes extra...>
  local d=$1; shift
  local reqs=() extra=() sep=0
  for a in "$@"; do
    if [ "$a" = "--" ]; then sep=1; continue; fi
    if [ $sep -eq 0 ]; then [ -f "$a" ] && reqs+=("$a"); else extra+=("$a"); fi
  done
  mk_venv "$d"
  local h; h="$(huella "${reqs[@]}"; printf '%s' "${extra[*]}")"
  if [ -f "$d/.recuperar_huella" ] && [ "$(cat "$d/.recuperar_huella")" = "$h" ]; then
    log "venv $d al día"; return 0
  fi
  local rargs=(); for r in "${reqs[@]}"; do rargs+=(-r "$r"); done
  log "instalando dependencias en $d (${#reqs[@]} requirements)"
  pip_in "$d" "${rargs[@]}" "${extra[@]}"
  echo "$h" > "$d/.recuperar_huella"
}

venvs() {
  # torch CPU primero (evita varios GB de CUDA); si falla, sigue: torch es opcional en AGs-Core.
  mk_venv "$VENV"
  if ! "$VENV/bin/python" -c "import torch" 2>/dev/null; then
    log "instalando torch CPU"
    pip_in "$VENV" --index-url "$TORCH_INDEX" torch || log "AVISO: torch no instalado (opcional)"
  fi
  ensure_venv "$VENV" \
    "$REPO/requirements-dev.txt" "$REPO/requirements.txt" "$MATRIZ/requirements.txt" \
    "$REPO/knowledge/hybrix/paquete/requirements-l5.txt" \
    -- backoff pytest-timeout
  ensure_venv "$NNC_VENV" \
    "$NNC_DIR/NNC/sistema-nnc-ags-core-corregido-1.0.0/nnc_system/requirements.txt" \
    "$NNC_DIR/ojo_de_dios/requirements.txt" -- numpy
  if [ -d "$NNC_CLONE" ]; then
    ensure_venv "$NNC_CLONE/.venv" "$NNC_CLONE/ojo_de_dios/requirements.txt" -- pytest
  fi
}

# ---------- pids ----------
pid_vivo_de() {  # pid_vivo_de <pidfile> <patron_cmdline>
  local f=$1 pat=$2 p
  [ -f "$f" ] || return 1
  p="$(cat "$f" 2>/dev/null || true)"
  [ -n "$p" ] && kill -0 "$p" 2>/dev/null && tr '\0' ' ' < "/proc/$p/cmdline" 2>/dev/null | grep -q -- "$pat"
}

limpiar_pid() {  # limpiar_pid <pidfile> <patron>
  local f=$1 pat=$2
  if [ -f "$f" ] && ! pid_vivo_de "$f" "$pat"; then log "pid obsoleto: $f"; rm -f "$f"; fi
}

puerto_ocupado() { ss -ltn 2>/dev/null | awk '{print $4}' | grep -qE "[:.]$1\$"; }

arrancar() {  # arrancar <nombre> <pidfile> <patron> <puerto|-> <log> <dir> <cmd...>
  local n=$1 f=$2 pat=$3 port=$4 lg=$5 dir=$6; shift 6
  limpiar_pid "$f" "$pat"
  if pid_vivo_de "$f" "$pat"; then log "$n ya en marcha (pid $(cat "$f"))"; return 0; fi
  if [ "$port" != "-" ] && puerto_ocupado "$port"; then log "$n: puerto $port ya ocupado por otro proceso; no arranco"; return 0; fi
  (
    cd "$dir"
    # clave de la API por entorno (nunca por argv, no aparece en `ps`)
    if [ "${CON_CLAVE:-0}" = 1 ] && [ -f "$REPO/data/api_key" ]; then AGS_API_KEY="$(cat "$REPO/data/api_key")"; export AGS_API_KEY; fi
    [ -n "${API_URL_ENV:-}" ] && export API_URL="$API_URL_ENV"
    nohup "$@" >> "$lg" 2>&1 < /dev/null &
    echo $! > "$f"
  )
  log "$n arrancado (pid $(cat "$f"))"
}

servicios() {
  [ -x "$VENV/bin/python" ] || { log "falta $VENV: ejecuta primero sin --solo-servicios"; exit 1; }
  # LiteLLM (opcional; usa su propio script, que carga las claves sin mostrarlas)
  limpiar_pid "$ROOT/litellm.pid" "litellm"
  if [ -x "$VENV/bin/litellm" ] && [ -f "$REPO/config/litellm.yaml" ]; then
    if ! puerto_ocupado 4000; then bash "$REPO/scripts/start_litellm.sh" | sed 's/^/[litellm] /'; else log "LiteLLM: :4000 ya ocupado"; fi
  else
    log "LiteLLM no disponible (sin binario o config); la API funciona sin él"
  fi
  # API :8000 — la clave se pasa por entorno, nunca por argv
  CON_CLAVE=1 arrancar api "$ROOT/api.pid" "uvicorn main:app" 8000 "$ROOT/api.log" "$REPO/app" \
    "$VENV/bin/uvicorn" main:app --host 127.0.0.1 --port 8000
  arrancar ui "$ROOT/ui.pid" "ui/app.py" 8501 "$ROOT/ui.log" "$REPO" \
    "$VENV/bin/streamlit" run ui/app.py --server.address 127.0.0.1 --server.port 8501 \
    --server.headless true --browser.gatherUsageStats false
  CON_CLAVE=1 API_URL_ENV=http://localhost:8000 arrancar ucs_ui "$ROOT/ucs_ui.pid" "ui_streamlit.py" 8502 "$ROOT/ucs_ui.log" "$REPO/ucs" \
    "$VENV/bin/streamlit" run ui_streamlit.py \
    --server.address 127.0.0.1 --server.port 8502 --server.headless true --browser.gatherUsageStats false
  # matriz_el_prat :8510 (su propia DB/Excel/contador)
  if [ -f "$MATRIZ/app/main.py" ]; then
    arrancar matriz "$ROOT/matriz_ui.pid" "app/main.py" 8510 "$ROOT/matriz_ui.log" "$MATRIZ" \
      "$VENV/bin/streamlit" run app/main.py --server.address 127.0.0.1 --server.port 8510 \
      --server.headless true --browser.gatherUsageStats false
  fi
  # NNC :8080/:8010 con su script (usa $NNC_DIR/.venv)
  if [ -x "$NNC_VENV/bin/python" ] && [ -f "$NNC_DIR/start_nnc.sh" ]; then
    limpiar_pid "$NNC_DIR/dashboard.pid" "dashboard_server.py"
    limpiar_pid "$NNC_DIR/service.pid" "service_server.py"
    bash "$NNC_DIR/start_nnc.sh" | sed 's/^/[nnc] /'
  fi
  # Autopilot (respeta data/STOP)
  if [ -f "$REPO/data/STOP" ]; then
    log "autopilot NO arrancado: existe $REPO/data/STOP (bórralo si quieres que corra)"
  else
    limpiar_pid "$ROOT/autopilot.pid" "app.autopilot"
    if pid_vivo_de "$ROOT/autopilot.pid" "app.autopilot"; then log "autopilot ya en marcha (pid $(cat "$ROOT/autopilot.pid"))"
    else
      # ojo: `cd X && cmd &` pondría en segundo plano un subshell (el pid sería el de bash, no el de python)
      ( cd "$REPO"; nohup "$VENV/bin/python" -m app.autopilot --interval 60 >> "$ROOT/autopilot.log" 2>&1 < /dev/null &
        echo $! > "$ROOT/autopilot.pid" )
      log "autopilot arrancado (pid $(cat "$ROOT/autopilot.pid"))"
    fi
  fi
}

verificar() {
  local fallos=0 url code i
  for url in http://127.0.0.1:8000/health http://127.0.0.1:8501/ http://127.0.0.1:8502/ \
             http://127.0.0.1:8080/ http://127.0.0.1:8010/health http://127.0.0.1:8510/ http://127.0.0.1:4000/health/readiness; do
    code=000
    for i in $(seq 1 30); do
      code="$(curl -s -o /dev/null -m 5 -w '%{http_code}' "$url" || true)"
      [ "$code" = "200" ] && break; sleep 2
    done
    log "HTTP $code $url"
    case "$url" in *:4000*) ;; *) [ "$code" = "200" ] || fallos=$((fallos+1));; esac
  done
  if pid_vivo_de "$ROOT/autopilot.pid" "app.autopilot"; then log "autopilot vivo (pid $(cat "$ROOT/autopilot.pid"))"; else log "autopilot NO vivo"; fallos=$((fallos+1)); fi
  log "fallos: $fallos"
  return $fallos
}

case "$MODO" in
  --solo-venvs) venvs ;;
  --solo-servicios) servicios; verificar ;;
  --verificar) verificar ;;
  *) venvs; servicios; verificar ;;
esac
