#!/bin/bash
# C-VIB-004: un cálculo a la vez, 4 hilos, topes de tiempo. Autoría: Lázaro López Paz (ORCID 0000-0001-8601-1963), con asistencia de IA.
cd /workspace/omniscience_cvib004; PY=/workspace/omniscience_cmat003/venv_ms/bin/python; C=code/cvib004_run.py
export OMP_NUM_THREADS=4 PYTHONPATH=/workspace/omniscience_cvib004/pylib; mkdir -p out
RS="MgO CaO SrO BaO LiF NaF NaCl NaBr NaI KF KCl KBr KI RbCl PbS PbSe PbTe"
timeout 80m $PY $C --aexp --out out/A --mats $RS > out/A.log 2>&1; echo FIN_A $(date -Iseconds)
timeout 15m $PY $C --aexp --out out/REP --mats PbTe NaCl KBr > out/REP.log 2>&1; echo FIN_REP $(date -Iseconds)
timeout 15m $PY $C --aexp --out out/C2 --mats PbTe --mesh 25 > out/C2.log 2>&1; echo FIN_C2 $(date -Iseconds)
timeout 15m $PY $C --out out/CA --mats NaCl KBr > out/CA.log 2>&1; echo FIN_CA $(date -Iseconds)
timeout 25m $PY $C --aexp --out out/B --mats KBr KI RbCl NaI PbTe --disp 0.01 > out/B.log 2>&1; echo FIN_B $(date -Iseconds)
$PY code/cvib004_eval.py > out/eval.log 2>&1; echo FIN_EVAL $(date -Iseconds)
echo FIN_TODO $(date -Iseconds)
