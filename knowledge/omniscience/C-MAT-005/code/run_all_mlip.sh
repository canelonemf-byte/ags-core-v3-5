#!/bin/bash
# C-MAT-005: ejecuciones MLIP (run1, run2) y prueba de artefacto MLIP; secuencial para no saturar la CPU.
cd /workspace/omniscience_cmat005/C-MAT-005
MS=/workspace/omniscience_cmat003/venv_ms/bin/python; MC=/workspace/omniscience_cmat001/.venv/bin/python
for run in run1 run2; do
  $MS code/cmat005_run.py --model mattersim --out out/$run/mattersim || echo "ERROR ms $run"
  $MC code/cmat005_run.py --model mace --out out/$run/mace || echo "ERROR mace $run"
  $MS code/cmat005_art_mlip.py --model mattersim --out out/$run/artefacto/mattersim || echo "ERROR art ms $run"
  $MC code/cmat005_art_mlip.py --model mace --out out/$run/artefacto/mace || echo "ERROR art mace $run"
  echo "FIN $run $(date)"
done
echo FIN_MLIP
