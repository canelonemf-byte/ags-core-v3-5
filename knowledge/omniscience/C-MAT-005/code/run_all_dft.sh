#!/bin/bash
# C-MAT-005: DFT GPAW (PBE y luego LDA) para TiO2 rutilo y SiO2 cuarzo-α.
cd /workspace/omniscience_cmat005/C-MAT-005/code
PY=/workspace/omniscience_cmat005/venv_dft/bin/python; export OMP_NUM_THREADS=1
r() { mpiexec -n 4 $PY cmat005_dft.py --mat $1 --xc $2 --etapa $3 || echo "ERROR $1 $2 $3"; echo "hecho $1 $2 $3 $(date)"; }
for m in TiO2 SiO2; do r $m PBE relax; r $m PBE gamma650; r $m PBE super; done
for m in TiO2 SiO2; do r $m LDA relax; r $m LDA super; done
echo FIN_DFT
