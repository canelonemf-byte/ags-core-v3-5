#!/bin/bash
# run1 y luego run2 para un potencial (reanudable).
model=$1; py=$2; cd "$(dirname "$0")/.."
for r in run1 run2; do echo "== $r $(date -Iseconds)"; "$py" code/cmat004_run.py --model "$model" --out out/$r 2>&1 | grep --line-buffered -E "^$model |salto|Error|Traceback|line [0-9]"; done
echo "FIN $(date -Iseconds)"
