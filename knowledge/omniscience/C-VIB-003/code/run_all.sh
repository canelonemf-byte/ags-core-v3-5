#!/bin/bash
# C-VIB-003: un cálculo a la vez, 6 hilos, topes de tiempo. Autoría: Lázaro López Paz (ORCID 0000-0001-8601-1963), con asistencia de IA.
cd /workspace/omniscience_cvib003; PY=/workspace/omniscience_cmat003/venv_ms/bin/python; C=code/cvib003_run.py
export OMP_NUM_THREADS=6; mkdir -p out
RS="MgO CaO SrO BaO LiF NaF NaCl NaBr NaI KF KCl KBr KI RbCl PbS PbSe PbTe"
ZB="BN BP AlP AlAs AlSb GaP GaAs GaSb InP InAs InSb ZnS ZnSe ZnTe CdTe"
timeout 90m  $PY $C --struct rocksalt --out out/rs --mats $RS > out/rs.log 2>&1; echo FIN_rs $(date -Iseconds)
timeout 20m  $PY $C --struct rocksalt --out out/rs_rep --mats PbTe NaCl KBr > out/rs_rep.log 2>&1; echo FIN_rs_rep $(date -Iseconds)
timeout 20m  $PY $C --struct rocksalt --out out/rs_ctrl --mats PbTe --mesh 25 > out/rs_ctrl.log 2>&1; echo FIN_rs_ctrl $(date -Iseconds)
timeout 100m $PY $C --struct zincblende --out out/zb2 --mats $ZB > out/zb2.log 2>&1; echo FIN_zb2 $(date -Iseconds)
for m in BP BN ZnS GaSb InSb; do
  timeout 100m $PY $C --struct zincblende --out out/zb3 --sc 3 --mats $m >> out/zb3.log 2>&1; echo FIN_zb3_$m $(date -Iseconds)
done
echo FIN_TODO $(date -Iseconds)
