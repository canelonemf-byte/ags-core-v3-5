#!/bin/bash
cd /workspace/omniscience_cumf004; MS=/workspace/omniscience_cmat003/venv_ms/bin/python
for r in run1 run2; do $MS code/cumf004_b.py --out out/b_$r > out/b_$r.log 2>&1; echo "FIN $r $(date -Iseconds)"; done; echo FIN_TODO
