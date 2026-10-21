#!/bin/bash
cd /workspace/omniscience_ctio2hse
[ -f out/vib_mattersim.json ] || /workspace/omniscience_cmat003/venv_ms/bin/python code/vib_tio2.py --model mattersim --out out > logs_vib_ms.log 2>&1
[ -f out/vib_mace.json ] || /workspace/omniscience_cnano001/venv_mace/bin/python code/vib_tio2.py --model mace --out out > logs_vib_mace.log 2>&1
echo FIN_B $(date -Iseconds)
