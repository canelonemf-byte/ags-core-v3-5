#!/bin/bash
cd /workspace/omniscience_cumf003; MS=/workspace/omniscience_cmat003/venv_ms/bin/python
for r in run1 run2; do $MS code/cumf003_mlip.py --out out/mlip_$r > out/mlip_$r.log 2>&1; done; echo FIN_MLIP >> out/mlip_run2.log
