#!/usr/bin/env bash
# reparar_tras_reinicio.sh — reparación ligera e idempotente tras un reinicio/restauración del box.
# Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia: MIT.
#
# Qué hace (repetible sin efectos dobles; no toca ficheros modificados):
#   1. Restaura desde HEAD SOLO los ficheros con seguimiento en git que han desaparecido
#      (`git ls-files -d`) en ags-core-v3.6. Los ficheros modificados sin commit no se tocan.
#   2. Comprueba ase 3.29.0 en dos destinos: /workspace/omniscience_cmat003/venv_ms (site-packages)
#      y /workspace/omniscience_cvib004/pylib (instalación --target). Un destino es íntegro si
#      todos los ficheros de su RECORD coinciden por sha256. Si a uno le falta ase/build o no es
#      íntegro: (a) copia ase/build desde el otro destino si ese es íntegro y las entradas ase/build/
#      de ambos RECORD coinciden; (b) si no hay origen íntegro o la copia no basta, reinstala
#      ase==3.29.0 --no-deps (--target --upgrade para pylib) con el pip del Python base de venv_ms.
#      Después verifica todo el RECORD por sha256 y `from ase.build import bulk`. En pylib comprueba
#      que la lista de entradas de primer nivel no cambia.
#   3. Comprueba que existen los entornos Python (no los recrea: para eso, recuperar_todo.sh).
# Salida: 0 todo bien; 1 si pip falla, la verificación falla o falta un entorno.
# Uso: scripts/reparar_tras_reinicio.sh [--verificar]   (--verificar: solo comprueba, no cambia nada)
set -uo pipefail

REPO=/workspace/agsgpt/ags-core-v3.6
VENVS=(/workspace/agsgpt/.venv /workspace/agsgpt/NNC/.venv /workspace/omniscience_cmat003/venv_ms)
ASE_VER=3.29.0
MS_PY=/workspace/omniscience_cmat003/venv_ms/bin/python
MS_SP=/workspace/omniscience_cmat003/venv_ms/lib/python3.12/site-packages
PYLIB=/workspace/omniscience_cvib004/pylib
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

# 2. ase 3.29.0 en venv_ms y pylib
ase_record() {  # $1 = base; verifica sha256 de TODO el RECORD; imprime "ok total"; rc 0 si íntegro
  python3 - "$1" "$ASE_VER" <<'PY'
import base64, hashlib, re, sys
from pathlib import Path
base, ver = Path(sys.argv[1]), sys.argv[2]
rec = base / f"ase-{ver}.dist-info" / "RECORD"
if not rec.is_file():
    print("0 0"); sys.exit(1)
target = "site-packages" not in str(base)  # instalación --target: ../../bin/x -> base/bin/x
n = ok = 0
for line in rec.read_text().splitlines():
    p = line.rsplit(",", 2)
    if len(p) < 3 or not p[1].startswith("sha256="):
        continue
    n += 1
    r = re.sub(r"^(\.\./)+bin/", "bin/", p[0]) if target else p[0]
    f = (base / r).resolve()
    d = base64.urlsafe_b64encode(hashlib.sha256(f.read_bytes()).digest()).rstrip(b"=").decode() if f.is_file() else ""
    ok += d == p[1][7:]
print(f"{ok} {n}"); sys.exit(0 if n and ok == n else 1)
PY
}
ase_build_rec() { grep '^ase/build/' "$1/ase-$ASE_VER.dist-info/RECORD" 2>/dev/null | grep -v __pycache__ | sort; }
ase_import() {  # $1 = nombre; importa ase.build y construye bulk NaCl con el Python de venv_ms
  if [ "$1" = pylib ]; then (cd /tmp && PYTHONPATH="$PYLIB" "$MS_PY" -c "from ase.build import bulk; bulk('NaCl','rocksalt',a=5.64)") 2>/dev/null
  else (cd /tmp && "$MS_PY" -c "from ase.build import bulk; bulk('NaCl','rocksalt',a=5.64)") 2>/dev/null; fi
}
PIP_PY="$(sed -n 's/^home = //p' /workspace/omniscience_cmat003/venv_ms/pyvenv.cfg 2>/dev/null)/python3.12"
ase_pip() {  # $1 = nombre; reinstala ase==ASE_VER sin dependencias
  if [ "$1" = pylib ]; then "$PIP_PY" -m pip install -q --disable-pip-version-check --no-deps --force-reinstall --upgrade --target "$PYLIB" "ase==$ASE_VER"
  else "$PIP_PY" -m pip --python "$MS_PY" install -q --disable-pip-version-check --no-deps --force-reinstall "ase==$ASE_VER"; fi
}
reparar_ase() {  # $1 = nombre, $2 = base destino, $3 = base del otro destino
  local nom=$1 dst=$2 otro=$3 res="" antes=""
  if [ -d "$dst/ase/build" ] && res=$(ase_record "$dst"); then
    log "ase $ASE_VER en $nom íntegro (RECORD ${res% *}/${res#* } sha256)"
  elif [ "$MODO" = "--verificar" ]; then
    log "ase en $nom: falta ase/build o RECORD no conforme (${res:-ase/build ausente}) (sin reparar: --verificar)"; RC=1; return
  else
    log "ase en $nom: falta ase/build o RECORD no conforme (${res:-ase/build ausente}); reparo"
    if [ -d "$otro/ase/build" ] && ase_record "$otro" >/dev/null && [ -d "$dst/ase-$ASE_VER.dist-info" ] \
       && diff -q <(ase_build_rec "$dst") <(ase_build_rec "$otro") >/dev/null; then
      mkdir -p "$dst/ase/build" && cp -p "$otro"/ase/build/*.py "$dst/ase/build/" \
        && log "ase/build copiado a $nom desde un origen íntegro"
    fi
    if ! res=$(ase_record "$dst"); then
      [ "$nom" = pylib ] && antes=$(ls -A "$PYLIB" 2>/dev/null)
      if [ ! -x "$PIP_PY" ]; then log "ERROR: no encuentro el Python base con pip ($PIP_PY)"; RC=1; return; fi
      if ! ase_pip "$nom"; then log "ERROR: pip install ase==$ASE_VER falló en $nom"; RC=1; return; fi
      log "ase==$ASE_VER reinstalado en $nom (--no-deps)"
      if [ "$nom" = pylib ] && [ "$antes" != "$(ls -A "$PYLIB")" ]; then
        log "ERROR: la lista de entradas de pylib ha cambiado tras pip --target"; RC=1; fi
      if ! res=$(ase_record "$dst"); then log "ERROR: RECORD de $nom no conforme tras reinstalar ($res)"; RC=1; return; fi
    fi
    log "ase $ASE_VER en $nom reparado (RECORD ${res% *}/${res#* } sha256)"
  fi
  ase_import "$nom" && log "$nom: from ase.build import bulk ok" || { log "ERROR: $nom no importa ase.build.bulk"; RC=1; }
}
if [ ! -x "$MS_PY" ] || [ ! -d "$MS_SP" ]; then
  log "ERROR: falta venv_ms ($MS_SP)"; RC=1
else
  reparar_ase venv_ms "$MS_SP" "$PYLIB"
  if [ -d "$PYLIB" ]; then reparar_ase pylib "$PYLIB" "$MS_SP"
  else log "ERROR: falta $PYLIB"; RC=1; fi
fi

# 3. entornos Python (solo comprobación; no se reinstala nada pesado)
for v in "${VENVS[@]}"; do
  if [ -x "$v/bin/python" ] && "$v/bin/python" -c "import sys" 2>/dev/null; then log "venv ok: $v"
  else log "FALTA venv: $v (recrear con scripts/recuperar_todo.sh --solo-venvs)"; RC=1; fi
done

log "fin rc=$RC"
exit $RC
