#!/bin/bash
# Parte A: dos flujos de 2 procesos MPI; tope 6 h por cálculo; reanudable (salta JSON existentes).
cd /workspace/omniscience_cumf005; V=/workspace/omniscience_cmat003/venv_ms/bin/python
st(){ o=$1; met=$2; mat=$3; c=$4; f=$o/${met}_${mat}_normal_${c}.json; [ -f $f ] && return; echo "INI $o $met $mat $c $(date -Iseconds)"; timeout 21600 $V code/cumf005_cp2k.py --met $met --mat $mat --out $o --cutoff $c >> out/a_stages.log 2>&1 || echo "FALLO/TOPE $o $met $mat $c $(date -Iseconds)"; }
( for m in rutilo anatasa; do st out/a_run1 R2SCAN $m 1000; done; for m in rutilo anatasa; do st out/a_run1 R2SCAN $m 1200; done; echo FIN_S1 $(date -Iseconds) ) > out/s1.log 2>&1 &
( for m in rutilo anatasa; do st out/a_run1 PBE $m 1000; done; for m in rutilo anatasa; do st out/a_run2 R2SCAN $m 1000; done; echo FIN_S2 $(date -Iseconds) ) > out/s2.log 2>&1 &
wait; echo FIN_A $(date -Iseconds)
