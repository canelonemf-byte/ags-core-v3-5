#!/bin/bash
# C-NANO-003: secuencial, 2 hilos. Autoría: Lázaro López Paz ... con asistencia de IA.
cd /workspace/omniscience_cnano003; export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
MS=/workspace/omniscience_cmat003/venv_ms/bin/python
for run in run1 run2; do
  $MS code/nano3_run.py --run $run --out out --parte mono >> logs/ms_${run}.log 2>&1; echo "FIN mono $run $?"
  $MS code/nano3_run.py --run $run --out out --parte bulk >> logs/ms_${run}_bulk.log 2>&1; echo "FIN bulk $run $?"
done
[ -x code/gpaw_c1.sh ] && bash code/gpaw_c1.sh >> logs/gpaw.log 2>&1; echo "FIN gpaw $?"
$MS code/nano3_eval.py > eval.log 2>&1; echo FIN_TODO $(date -Iseconds)
