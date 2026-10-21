#!/bin/bash
# Etapas con tope 8 h (timeout 28800 s). Reanudable: salta JSON ya existentes.
cd /workspace/omniscience_cumf004; P="mpiexec -n 2 /workspace/omniscience_cmat005/venv_dft/bin/python code/cumf004_dft.py"
st(){ f=$1; shift; [ -f "$f" ] && return; echo "INI $* $(date -Iseconds)"; timeout 28800 $P "$@" >> out/a_stages.log 2>&1 || echo "FALLO/TOPE $* $(date -Iseconds)"; }
for m in rutilo anatasa; do st out/a_run1/relax_$m.json --etapa relax --met PBE --mat $m --out out/a_run1; done
for r in run1 run2; do for m in rutilo anatasa; do cp -n out/a_run1/relax_$m.traj out/a_$r/ 2>/dev/null || { mkdir -p out/a_$r; cp -n out/a_run1/relax_$m.traj out/a_$r/; }
  for x in PBE R2SCAN; do [ $r = run2 ] && [ $x = PBE ] && continue; st out/a_$r/${x}_${m}_normal.json --etapa sp --met $x --mat $m --out out/a_$r; done; done; done
# F3 smoke HSE06 (tope 20 min por fase); si ambos terminan, HSE06 k normal no se intenta (coste), se usa k reducido como estimación declarada en prereg F3
for m in rutilo anatasa; do f=out/a_run1/HSE06_${m}_reducido.json; [ -f $f ] || { echo "INI HSE $m $(date -Iseconds)"; timeout 1200 $P --etapa sp --met HSE06 --mat $m --out out/a_run1 --k reducido --ecut 500 >> out/a_stages.log 2>&1 || echo "FALLO/TOPE HSE $m"; }; done
echo FIN_A $(date -Iseconds)
