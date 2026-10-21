#!/bin/bash
cd /workspace/omniscience_cumf004; V=/workspace/omniscience_cmat003/venv_ms/bin/python; ST=/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-UMF-004
while pgrep -f "run_a.sh|run_b.sh|run_vib.sh" >/dev/null; do sleep 60; done
$V code/cumf004_eval.py > out/eval.log 2>&1; $V code/cumf004_fig.py >> out/eval.log 2>&1; $V code/cumf004_report.py >> out/eval.log 2>&1
mkdir -p $ST; cp -r prereg_* freeze_stamp.txt code_freeze.sha256 code run_*.sh finisher.sh results.json resultados_C-UMF-004.md figs $ST/ 2>/dev/null
mkdir -p $ST/out; cp -r out/*.log out/*.nohup out/b_run1 out/b_run2 out/vib_run1 out/vib_run2 $ST/out/ 2>/dev/null
for r in a_run1 a_run2; do mkdir -p $ST/out/$r; cp out/$r/*.json out/$r/*.log out/$r/*.traj $ST/out/$r/ 2>/dev/null; done
echo FINISHER_OK $(date -Iseconds) >> out/eval.log
