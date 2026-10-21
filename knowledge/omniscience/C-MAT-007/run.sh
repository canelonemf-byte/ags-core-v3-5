#!/bin/bash
cd /workspace/omniscience_cmat007/code; V=/workspace/omniscience_cmat003/venv_ms/bin/python
$V cmat007_run.py --out ../out/run1 > ../logs/run1.log 2>&1; echo FIN1 $(date -Iseconds)
$V cmat007_run.py --out ../out/run2 --disp 0.02 > ../logs/run2.log 2>&1; echo FIN2 $(date -Iseconds)
$V cmat007_eval.py > ../logs/eval.log 2>&1; echo FIN_EVAL $(date -Iseconds)
