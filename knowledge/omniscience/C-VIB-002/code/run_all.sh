#!/bin/bash
cd /workspace/omniscience_cvib002; MS=/workspace/omniscience_cmat003/venv_ms/bin/python; MC=/workspace/omniscience_cmat001/.venv/bin/python; C=/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-VIB-002/code/cvib002_run.py
export OMP_NUM_THREADS=4
$MS $C --model mattersim --out out/run1 > out/run1_ms.log 2>&1 &
$MC $C --model mace --out out/run1 > out/run1_mace.log 2>&1 &
wait; echo FIN_run1 $(date -Iseconds)
$MS $C --model mattersim --out out/run2 > out/run2_ms.log 2>&1 &
$MS $C --model mattersim --out out/ctrl --mats GaAs --mesh 25 > out/ctrl.log 2>&1 &
wait; echo FIN_TODO $(date -Iseconds)
