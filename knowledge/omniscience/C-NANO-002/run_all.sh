#!/bin/bash
# C-NANO-002: ejecución secuencial (un proceso a la vez, 2 hilos) para no competir en memoria con CP2K.
cd /workspace/omniscience_cnano002; export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
MS=/workspace/omniscience_cmat003/venv_ms/bin/python; MC=/workspace/omniscience_cnano001/venv_mace/bin/python; DF=/workspace/omniscience_cmat005/venv_dft/bin/python
for run in run1 run2; do
  $MS code/nano2_run.py --model mattersim --run $run --out out --parte mono >> logs/ms_${run}.log 2>&1; echo "FIN ms mono $run $?"
  $MS code/nano2_run.py --model mattersim --run $run --out out --parte bulk --d3 1 >> logs/ms_${run}.log 2>&1; echo "FIN ms_d3 bulk $run $?"
  $MS code/nano2_run.py --model mattersim --run $run --out out --parte bulk >> logs/ms_${run}.log 2>&1; echo "FIN ms bulk $run $?"
done
$MC code/nano2_run.py --model mace --run run1 --out out --parte mono >> logs/mace_run1.log 2>&1; echo "FIN mace $?"
$DF code/gpaw_grafeno.py >> logs/gpaw.log 2>&1; echo "FIN gpaw $?"
echo FIN_TODO $(date -Iseconds)
