#!/bin/bash
# Busca un python con gpaw; si no hay, C1 = NO EVALUABLE
for P in /workspace/omniscience_cmat005/venv_dft/bin/python /usr/bin/python3; do $P -c "import gpaw" 2>/dev/null && { OMP_NUM_THREADS=2 timeout 14400 $P /workspace/omniscience_cnano003/code/gpaw_ws2.py; exit $?; }; done; echo "GPAW no disponible: C1 NO EVALUABLE"
