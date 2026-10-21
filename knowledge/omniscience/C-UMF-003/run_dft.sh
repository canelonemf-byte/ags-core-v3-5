#!/bin/bash
cd /workspace/omniscience_cumf003; P=/workspace/omniscience_cmat005/venv_dft/bin/python
for met in PBE PBEU R2SCAN; do for mat in rutilo anatasa; do
 [ -f out/dft_run1/${met}_${mat}.json ] || mpiexec -n 3 $P code/cumf003_dft.py --met $met --mat $mat --out out/dft_run1 >> out/dft_run1.log 2>&1; done; done
for met in PBE PBEU R2SCAN; do for mat in rutilo anatasa; do
 [ -f out/dft_run2/${met}_${mat}.json ] || mpiexec -n 2 $P code/cumf003_dft.py --met $met --mat $mat --out out/dft_run2 >> out/dft_run2.log 2>&1; done; done
echo FIN_DFT >> out/dft_run2.log
