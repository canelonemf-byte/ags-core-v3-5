# Desviaciones C-NANO-002
- D0 (declarada antes de congelar): superceldas masivas 3×3×2/3×3×1, D3 con corte 40 bohr, sin regla de suma rotacional.
- D1 (incidente, antes de congelar): el primer humo de tiempos (MatterSim+D3 a 95 bohr en grafito 4×4×2, ~10 GB) provocó un OOM global a las ~09:10 CEST. El OOM mató un proceso cp2k.psmp de la etapa PBE0TC rutilo de run_a.sh (C-UMF-006, ajena) y luego el propio humo. La etapa terminó como FALLO/TOPE a las 09:10:18 (≈1 h 14 min antes de su tope de 5 h; iba en el paso SCF 6, ~54 min/paso, sin converger). run_a.sh siguió sola con la etapa PBE0TC anatasa _rc3. Desde entonces todos los procesos de esta campaña corren con oom_score_adj=1000 y vigilante MemAvailable<700 MB (code/guardia.py).
- D2: el vigilante abortó run1 MatterSim+D3 masivo tras grafito (MemAvailable<700 MB); se reanudó con el mismo código congelado (resume_d3.sh) tras GPAW; h-BN y 2H-MoS2 de run1 se calcularon después de run2. Sin efecto en el método.
- D3: code/fig.py escrito tras congelar (solo dibujo).
- D4: GPAW con symmetry="off": LO/TO salen desdobladas 1551.0/1570.6 cm⁻¹; se usa la media, como prevé la regla de asignación.
