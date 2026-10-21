#!/bin/bash
cd /workspace/omniscience_cumf004; MS=/workspace/omniscience_cmat003/venv_ms/bin/python
while pgrep -f cumf004_b.py >/dev/null; do sleep 30; done
for r in run1 run2; do $MS code/cumf004_vib.py --out out/vib_$r > out/vib_$r.log 2>&1; done; echo FIN_VIB
