#!/bin/bash
cd /workspace/omniscience_cumf005; V=/workspace/omniscience_cmat003/venv_ms/bin/python; ST=/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-UMF-005
while pgrep -f "omniscience_cumf005/run_a.sh|cumf005_cp2k.py" >/dev/null; do sleep 120; done
$V code/cumf005_eval.py > out/eval.log 2>&1
mkdir -p $ST; cp -r --no-preserve=mode prereg_* freeze_stamp.txt code_freeze.sha256 code refs run_*.sh finisher.sh results.json resultados_C-UMF-005.md figs $ST/ 2>>out/eval.log
mkdir -p $ST/out; cp -r --no-preserve=mode out/*.log out/*.json $ST/out/ 2>>out/eval.log
for r in a_run1 a_run2 smoke; do mkdir -p $ST/out/$r; cp --no-preserve=mode out/$r/*.json $ST/out/$r/ 2>/dev/null; for d in out/$r/*/; do mkdir -p $ST/$d; cp --no-preserve=mode $d/in.inp $d/out.log $ST/$d/ 2>/dev/null; done; done
echo FINISHER_OK $(date -Iseconds) >> out/eval.log
