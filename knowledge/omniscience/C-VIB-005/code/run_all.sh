#!/bin/bash
# C-VIB-005: barrido de volumen ±1 % en a_exp. Un cálculo a la vez, 4 hilos. Autoría: Lázaro López Paz (ORCID 0000-0001-8601-1963), con asistencia de IA.
cd /workspace/omniscience_cvib005; PY=/workspace/omniscience_cmat003/venv_ms/bin/python; C=code/cvib005_run.py
export OMP_NUM_THREADS=4 PYTHONPATH=/workspace/omniscience_cvib004/pylib; mkdir -p out
M="KBr KI RbCl NaI NaBr BaO PbS PbSe PbTe NaCl MgO"
timeout 30m $PY $C --aexp --scale 0.99 --out out/V099 --mats $M > out/V099.log 2>&1; echo FIN_V099 $(date -Iseconds)
timeout 30m $PY $C --aexp --scale 1.01 --out out/V101 --mats $M > out/V101.log 2>&1; echo FIN_V101 $(date -Iseconds)
timeout 6m $PY $C --aexp --scale 1.00 --out out/CA --mats NaCl > out/CA.log 2>&1; echo FIN_CA $(date -Iseconds)
timeout 6m $PY $C --aexp --scale 0.99 --out out/B --mats KI --disp 0.01 > out/B.log 2>&1; echo FIN_B $(date -Iseconds)
$PY code/cvib005_eval.py > out/eval.log 2>&1; echo FIN_EVAL $(date -Iseconds)
echo FIN_TODO $(date -Iseconds)
