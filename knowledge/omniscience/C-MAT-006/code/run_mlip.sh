#!/bin/bash
cd /workspace/omniscience_cmat006
MS=/workspace/omniscience_cmat003/venv_ms/bin/python; MC=/workspace/omniscience_cmat001/.venv/bin/python
for run in run1 run2; do
  $MS code/cmat006_run.py --model mattersim --out out/$run > out/${run}_ms.log 2>&1 || echo "ERROR ms $run"
  $MC code/cmat006_run.py --model mace --out out/$run > out/${run}_mace.log 2>&1 || echo "ERROR mace $run"
  echo "FIN $run $(date -Iseconds)"
done
echo FIN_TODO
