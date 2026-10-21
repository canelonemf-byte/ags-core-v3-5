# Prerregistro C-UMF-005: orden anatasa/rutilo con r2SCAN y pseudopotenciales meta-GGA coherentes (CP2K), y D3 solo en compuestos de baja dimensionalidad con regla fijada a priori
meta: {campaña: C-UMF-005, version: 1, fecha: 2026-10-20, autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial", orcid: 0000-0001-8601-1963, antecedentes: [C-UMF-002, C-UMF-003, C-UMF-004]}
objetivo: "A) ¿r2SCAN con pseudopotenciales y bases optimizados para meta-GGA (GTH-SCAN + MOLOPT-SCAN, CP2K) corrige el signo de ΔE(anatasa−rutilo) que con setups PAW-PBE (GPAW) salía −11.8 meV/át frente a +9.0±1.4 exp? B) ¿Aplicar D3(BJ) solo a los compuestos que una regla estructural fija clasifica como de baja dimensionalidad (y a toda su reacción de formación) conserva la mejora en haluros en capas sin el empeoramiento global de C-UMF-004?"

## Factibilidad (decidida antes de calcular)
- F-A0 herramientas: CP2K 2026.2 (conda-forge, libxc) instalado 20-oct 20:40 UTC+2 en /workspace/tools/env_cp2k. Pseudopotenciales GTH-SCAN-q12 (Ti) y GTH-SCAN-q6 (O) en POTENTIAL_UZH_2026.2 y bases TZV2P-MOLOPT-SCAN-GTH en BASIS_MOLOPT_UZH_2026.2 (repositorio cp2k/cp2k, sha256 de los ficheros descargados 8ab49093… y dd2a387f…). Son pseudopotenciales SCAN, no r2SCAN: misma familia meta-GGA; se declara (no es desviación).
- F-A1 smoke (tras congelar este documento, ≤30 min): rutilo, r2SCAN (libxc MGGA_X_R2SCAN + MGGA_C_R2SCAN), k 2×2×3, cutoff 600 Ry. Si CP2K no admite meta-GGA con puntos k o el SCF no converge, la parte A = NO EVALUABLE (no es desviación). El smoke solo verifica que corre; no produce ΔE. El código de A se congela (sha256) después del smoke y antes de cualquier cálculo de producción; el de B se congela antes de evaluar.
- Geometrías: las PBE relajadas de C-UMF-004 (out/a_run1/relax_{rutilo,anatasa}.traj), sin re-relajar.
- Producción: GPW, CUTOFF 1000 Ry, REL_CUTOFF 70 Ry, EPS_SCF 1e-8, Monkhorst-Pack rutilo 5×5×8, anatasa (celda primitiva) 6×6×6 (mismas densidades que C-UMF-004), Fermi-Dirac 300 K, 2 procesos MPI, 1 hilo. Tope 6 h por cálculo; si se supera, hipótesis afectada NO EVALUABLE.
- Parte B no requiere cálculos nuevos: reutiliza energías relajadas MatterSim sin D3 (C-UMF-002 out/run1 y run2) y MatterSim+D3 (C-UMF-004 out/b_run1 y b_run2), protocolo de evaluación C-UMF-002 idéntico (LOOCV de corrección por anión, n=37 sin Ti).

## Regla R-dim (fijada antes de mirarla aplicada)
Para cada compuesto, la estructura experimental de entrada (cumf002_run.structure, antes de relajar) se analiza con ase.geometry.dimensionality.analyze_dimensionality(atoms, method="RDA") (ASE 3.29.0, parámetros por defecto). Se toma el intervalo de mayor puntuación. El compuesto se marca «baja dimensionalidad» si su tipo de dimensionalidad h no es exactamente "3D" (contiene algún componente 0D, 1D o 2D). Para los marcados, su ΔfH bruto se calcula con energías D3 en compuesto, elementos y moléculas de referencia; para el resto, sin D3. Equivalente aplicado: E_c' = E_c(D3) − (n_at/n_fórmula)·Σ n_i·[μ_i(D3) − μ_i(base)], resto de referencias base.

## Hipótesis (umbrales fijos)
| id | enunciado | criterio PASA |
|---|---|---|
| H-A1 | r2SCAN con pseudopotenciales meta-GGA da el signo correcto | ΔE_r2SCAN,CP2K(A−R) > 0 |
| H-A2 | y la magnitud es compatible con el experimento (solo electrónica) | |ΔE − 9.0| ≤ 10 meV/át |
| H-A3 | la incoherencia de setups explica parte del error de C-UMF-004 | ΔE_CP2K − (−11.76) ≥ +5 meV/át; solo evaluable si C-A1 se cumple |
| H-B1 | D3 selectivo no empeora el MAE LOOCV base | MAE_sel ≤ 32.63 meV/át |
| H-B2 | conserva la mejora en MgCl2, CaI2, MgBr2 | MAE_sel(capas) ≤ 36.3 meV/át |
| H-B3 | ningún compuesto sin Ti empeora mucho | max |err_LOOCV,sel| ≤ 150 meV/át |
| H-B4 | mejora frente a D3 global (C-UMF-004) | MAE_sel ≤ 38.01 − 2 = 36.01 meV/át |
| H-REP | réplica: A r2SCAN de ambas fases repetido; B evaluado con run2 de ambas fuentes | A ≤ 0.01 meV/át; B dif. MAE ≤ 1e-6 relativa y mismas marcas |
Controles: C-A1 PBE en CP2K (GTH-PBE + TZV2P-MOLOPT-PBE) reproduce ΔE PBE de GPAW en la misma geometría (−30.51) ±10 meV/át; C-A2 convergencia: r2SCAN a 1200 Ry cambia ΔE ≤ 2 meV/át; C-R descriptivo: lista de compuestos marcados por R-dim y si incluye MgCl2, CaI2, MgBr2.

## Decisión
E3 si pasan H-A1, H-A2, H-B1, H-B2, H-REP y se cumplen C-A1 y C-A2. E2 si pasa A (H-A1, H-A2 con C-A1) o B (H-B1, H-B2, H-REP) por separado; si no, E1. Limitación declarada: B es dentro de muestra y los errores por compuesto con D3 global ya se conocían (C-UMF-004); por eso B por sí solo no puede dar más de E2. Reglas aplicadas literalmente; desviaciones en sección aparte.

## Referencias (DOI verificados en Crossref 20-oct-2026)
https://doi.org/10.1073/pnas.251534898 (calorimetría TiO2) ; https://doi.org/10.1021/acs.jpclett.0c02405 (r2SCAN) ; https://doi.org/10.1063/5.0007045 (CP2K) ; https://doi.org/10.1103/PhysRevB.54.1703 (GTH) ; https://doi.org/10.1063/1.2770708 (MOLOPT) ; https://doi.org/10.1103/PhysRevMaterials.3.034003 (dimensionalidad RDA) ; https://doi.org/10.1002/jcc.21759 (D3-BJ) ; https://doi.org/10.18434/T42S31 (JANAF)
riesgos: [pseudopotenciales SCAN usados con r2SCAN, meta-GGA en GPW sensible al cutoff, CPU compartida con C-MAT-006, B dentro de muestra]
