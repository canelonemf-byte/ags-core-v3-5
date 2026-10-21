#!/bin/bash
# C-NANO-001: runs reanudables. MatterSim run1 -> run2; MACE run1 en paralelo; GPAW tras run1 MatterSim.
cd /workspace/omniscience_cnano001; MS=/workspace/omniscience_cmat003/venv_ms/bin/python; MC=/workspace/omniscience_cnano001/venv_mace/bin/python
( $MS code/nano_run.py --model mattersim --run run1 --out out > logs/ms_run1.log 2>&1; echo FIN_MS1 $(date -Iseconds)
  $MS code/nano_run.py --model mattersim --run run2 --out out --parte metales,tio2 > logs/ms_run2.log 2>&1; echo FIN_MS2 $(date -Iseconds) ) &
( $MC code/nano_run.py --model mace --run run1 --out out --parte metales,tio2 > logs/mace_run1.log 2>&1; echo FIN_MACE $(date -Iseconds) ) &
wait; echo FIN_TODO $(date -Iseconds)
