#!/usr/bin/env bash
# (ORÁCULO) Reproduce C-VIB-001: venv, figuras, animación, tests y checksums. Usa VIBRACIONES_OUT (por defecto out/figs).
# Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, ORCID 0000-0001-8601-1963, con asistencia de IA.
# Licencia: MIT. La IA no es autora.
set -euo pipefail
cd "$(dirname "$0")"
export MPLBACKEND=Agg VIBRACIONES_OUT="${VIBRACIONES_OUT:-out/figs}"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -r requirements.txt
rm -rf "$VIBRACIONES_OUT"
.venv/bin/python simular_vibraciones.py
if command -v ffmpeg >/dev/null; then .venv/bin/python animar_modos.py; else echo "AVISO: sin ffmpeg, no hay mp4"; fi
.venv/bin/python verificacion_frecuencias.py
# los smoke tests heredan el entorno: sin VIBRACIONES_OUT para no mezclar rutas
env -u VIBRACIONES_OUT .venv/bin/python -m pytest -q -rx
sha256sum -c checksums_c_vib_001.sha256  # integridad de fuentes del paquete (no out/figs)
.venv/bin/python gen_rocrate.py
echo "C-VIB-001: TODO OK"
