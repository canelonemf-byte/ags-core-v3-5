#!/usr/bin/env bash
# reparar_tras_reinicio.sh — reparación ligera e idempotente tras un reinicio/restauración del box.
# Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia: MIT.
#
# Qué hace (repetible sin efectos dobles; no instala paquetes ni toca ficheros modificados):
#   1. Restaura desde HEAD SOLO los ficheros con seguimiento en git que han desaparecido
#      (`git ls-files -d`) en ags-core-v3.6. Los ficheros modificados sin commit no se tocan.
#   2. Repone ase/build en /workspace/omniscience_cmat003/venv_ms copiándolo desde
#      /workspace/omniscience_cvib004/pylib/ase/build, solo si ambos son ase 3.29.0 y las
#      entradas ase/build/ de sus RECORD coinciden; después verifica cada sha256 del RECORD.
#   3. Comprueba que existen los entornos Python (no los recrea: para eso, recuperar_todo.sh).
# Salida: 0 todo bien; 1 algo no se pudo reparar o falta un entorno.
# Uso: scripts/reparar_tras_reinicio.sh [--verificar]   (--verificar: no cambia nada)
set -uo pipefail

REPO=/workspace/agsgpt/ags-core-v3.6
VENVS=(/workspace/agsgpt/.venv /workspace/agsgpt/NNC/.venv /workspace/omniscience_cmat003/venv_ms)
ASE_VER=3.29.0
MS_SP=/workspace/omniscience_cmat003/venv_ms/lib/python3.12/site-packages
SRC_PYLIB=/workspace/omniscience_cvib004/pylib
MODO="${1:-reparar}"
RC=0

log() { printf '[reparar %s] %s\n' "$(date '+%F %T %Z')" "$*"; }

exec 9>/tmp/reparar_tras_reinicio.lock
flock -n 9 || { log "otra instancia en marcha; salgo"; exit 0; }

# 1. ficheros borrados con seguimiento en git
cd "$REPO" || { log "ERROR: no existe $REPO"; exit 1; }
mapfile -t BORRADOS < <(git ls-files -d)
if [ "${#BORRADOS[@]}" -eq 0 ]; then
  log "git: 0 ficheros borrados con seguimiento"
elif [ "$MODO" = "--verificar" ]; then
  log "git: ${#BORRADOS[@]} ficheros borrados con seguimiento (sin restaurar: --verificar)"; RC=1
else
  printf '%s\n' "${BORRADOS[@]}" | git checkout HEAD --pathspec-from-file=- \
    && log "git: restaurados ${#BORRADOS[@]} ficheros borrados desde HEAD" \
    || { log "ERROR: git checkout falló"; RC=1; }
  quedan=$(git ls-files -d | wc -l)
  [ "$quedan" -eq 0 ] || { log "ERROR: siguen borrados $quedan"; RC=1; }
fi

# 2. ase/build en venv_ms
ase_check() {  # verifica sha256 de ase/build/*.py contra el RECORD de venv_ms
  python3 - "$MS_SP" <<'PY'
import base64, hashlib, sys
from pathlib import Path
sp = Path(sys.argv[1]); mal = 0; n = 0
for line in (sp / "ase-3.29.0.dist-info" / "RECORD").read_text().splitlines():
    ruta, h, *_ = line.split(",")
    if not ruta.startswith("ase/build/") or not h.startswith("sha256="):
        continue
    n += 1; f = sp / ruta
    d = base64.urlsafe_b64encode(hashlib.sha256(f.read_bytes()).digest()).rstrip(b"=").decode() if f.is_file() else ""
    mal += d != h[7:]
print(f"{n} {mal}"); sys.exit(0 if n and not mal else 1)
PY
}
if [ ! -d "$MS_SP" ]; then
  log "ERROR: falta $MS_SP"; RC=1
elif [ -d "$MS_SP/ase/build" ] && res=$(ase_check); then
  log "ase/build en venv_ms presente y conforme al RECORD (${res%% *} ficheros)"
elif [ "$MODO" = "--verificar" ]; then
  log "ase/build en venv_ms falta o no coincide (sin reparar: --verificar)"; RC=1
elif [ ! -d "$MS_SP/ase-$ASE_VER.dist-info" ] || [ ! -d "$SRC_PYLIB/ase-$ASE_VER.dist-info" ]; then
  log "ERROR: versión de ase distinta de $ASE_VER en venv_ms o en pylib; no copio"; RC=1
elif ! diff -q <(grep '^ase/build/' "$MS_SP/ase-$ASE_VER.dist-info/RECORD" | grep -v __pycache__ | sort) \
               <(grep '^ase/build/' "$SRC_PYLIB/ase-$ASE_VER.dist-info/RECORD" | grep -v __pycache__ | sort) >/dev/null; then
  log "ERROR: RECORD de ase/build distinto entre venv_ms y pylib; no copio"; RC=1
else
  mkdir -p "$MS_SP/ase/build"
  cp -p "$SRC_PYLIB"/ase/build/*.py "$MS_SP/ase/build/"
  if res=$(ase_check); then log "ase/build repuesto en venv_ms (${res%% *} ficheros, sha256 conforme al RECORD)"
  else log "ERROR: ase/build copiado pero no coincide con el RECORD ($res)"; RC=1; fi
fi
if [ -x /workspace/omniscience_cmat003/venv_ms/bin/python ]; then
  /workspace/omniscience_cmat003/venv_ms/bin/python -c "import ase.build" 2>/dev/null \
    && log "venv_ms: import ase.build ok" || { log "ERROR: venv_ms no importa ase.build"; RC=1; }
fi

# 3. entornos Python (solo comprobación; no se reinstala nada pesado)
for v in "${VENVS[@]}"; do
  if [ -x "$v/bin/python" ] && "$v/bin/python" -c "import sys" 2>/dev/null; then log "venv ok: $v"
  else log "FALTA venv: $v (recrear con scripts/recuperar_todo.sh --solo-venvs)"; RC=1; fi
done

log "fin rc=$RC"
exit $RC
