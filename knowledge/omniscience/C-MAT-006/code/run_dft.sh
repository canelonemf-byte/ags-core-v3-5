#!/bin/bash
# C-MAT-006: DFT PBE 650 eV. Rutilo: relax, Γ 650/800, supercelda 2x2x2. Cuarzo: solo si factible (<=6 desplazamientos).
cd /workspace/omniscience_cmat006/code
PY=/workspace/omniscience_cmat005/venv_dft/bin/python; export OMP_NUM_THREADS=1
r() { mpiexec -n 4 $PY cmat006_dft.py --mat $1 --etapa $2 || echo "ERROR $1 $2"; echo "hecho $1 $2 $(date -Iseconds)"; }
r TiO2 relax; r TiO2 gamma; r TiO2 super
$PY cmat006_dft.py --mat SiO2 --etapa factib
N=$(python3 -c "import json;print(json.load(open('../out/dft/SiO2/factib.json'))['n_disp'])")
if [ "$N" -le 6 ]; then r SiO2 relax; r SiO2 super; else echo "cuarzo no factible: n_disp=$N"; fi
echo FIN_DFT
