#!/bin/bash
cd /workspace/omniscience_ctio2hse; V=/workspace/omniscience_cmat003/venv_ms/bin/python
while pgrep -f "nano_run.py|cmat007_run.py|vib_tio2.py" >/dev/null; do sleep 60; done
st(){ met=$1; mat=$2; f=out/${met}_${mat}_base_600${3}.json; [ -f $f ] && return; echo "INI $met $mat $3 $(date -Iseconds)"; timeout 18000 $V code/hse_cp2k.py --met $met --mat $mat --sc base --out out --np 6 >> a_stages.log 2>&1 || echo "FALLO/TOPE $met $mat $3 $(date -Iseconds)"; }
for m in anatasa rutilo; do st PBE $m ""; done
for m in anatasa rutilo; do st PBE0TC $m ""; done
export RC_TC=3.0; for m in anatasa rutilo; do st PBE0TC $m _rc3; done
$V code/eval_umf006.py > eval.log 2>&1; echo FIN_A $(date -Iseconds)
