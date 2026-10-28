#!/bin/bash
# Reanudación (guardia abortó run1 MS+D3 masivo tras grafito por MemAvailable<700 MB); el script es reanudable y no recalcula lo existente.
cd /workspace/omniscience_cnano002; export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
while pgrep -f run_all.sh >/dev/null; do sleep 10; done
for i in 1 2 3 4 5 6; do
  /workspace/omniscience_cmat003/venv_ms/bin/python code/nano2_run.py --model mattersim --run run1 --out out --parte bulk --d3 1 >> logs/ms_run1_resume.log 2>&1 && break
  echo "reintento $i $(date -Iseconds)"; sleep 120
done
echo FIN_RESUME $(date -Iseconds)
