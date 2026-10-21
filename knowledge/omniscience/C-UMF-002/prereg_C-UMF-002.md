---
meta:
  id: C-UMF-002
  titulo: "Entalpías de formación con uMLIP (MatterSim, MACE) en 42 sólidos frente a NIST-JANAF, con corrección de Ti fijada a priori y estabilidad frente a fases competidoras"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
  fecha_congelacion: "2026-10-20 (UTC+2), antes de cualquier cálculo con los 13 compuestos nuevos y antes de cualquier ajuste de δ_Ti"
  afirmaciones_registro: [UM-07, UM-17, UM-18]
  estado: congelado
  antecedente: "C-UMF-001 (29 sólidos): MAE LOOCV MatterSim 46 meV/átomo; TiO2 rutilo 195 meV/átomo (> 150) y δ_F a 0.17 eV de MP2020 (> 0.15). Se conocen los errores de TiO2 y MgTiO3 de C-UMF-001; por eso el conjunto de entrenamiento de Ti NO los incluye."
objetivo: "Probar si una corrección por átomo de Ti, ajustada SOLO con TiN y Ti2O3, corrige el error de los óxidos de Ti (rutilo, anatasa, MgTiO3), y si las energías de MatterSim ordenan bien la estabilidad frente a fases competidoras."
datos_clave:
  compuestos:
    de_C-UMF-001: [MgO, CaO, SrO, BeO, Al2O3, Li2O, Na2O, SiO2, TiO2, ZrO2, MgAl2O4, BeAl2O4, MgTiO3, ZrSiO4, LiF, NaF, KF, CaF2, SrF2, BaF2, MgF2, NaCl, KCl, LiCl, CsCl, KBr, NaBr, KI, AlN]
    nuevos: [NaI, SrCl2, BaO, TiN, Ti2O3, TiO2_anatasa, MgCl2, ZrN, CaI2, LiBr, LiI, CsF, MgBr2]
    n: 42
    estructuras_nuevas: "Celdas iniciales de prototipos estándar, después relajación completa: NaI, BaO, CsF, LiBr, LiI, TiN, ZrN tipo NaCl; SrCl2 fluorita; Ti2O3 corindón (R-3c); anatasa I4_1/amd; MgCl2 tipo CdCl2 (R-3m); CaI2 y MgBr2 tipo CdI2 (P-3m1)."
    tablas_JANAF_nuevas: "https://janaf.nist.gov/tables/<id>.txt: I-015, Cl-119, Ba-034, N-014, O-059, O-042, Cl-093, N-019, Ca-023, Br-019, I-008, Cs-008, Br-057 (sha256 en refs/sha256_janaf.txt). Fuente: Chase 1998, NIST-JANAF 4.ª ed., https://doi.org/10.18434/T42S31"
    referencia_exp: "ΔfH°(0 K). Regla fijada: si la tabla no da valor a 0 K (LiBr, LiI, CsF, MgBr2) se usa ΔfH°(298.15 K) y el compuesto se marca 'ref_298'."
  modelos: "MatterSim-v1.0.0-5M (principal), MACE-MP-0 medium (línea base); float64, CPU, 4 hilos, semilla 0; mismo protocolo, referencias elementales (Ti, Zr hcp, etc.) y moléculas (O2, N2, F2, Cl2, Br2, I2 en caja de 20 Å) que C-UMF-001."
  correccion_anion: "δ_X por mínimos cuadrados (error por átomo, peso x_X) con los 37 compuestos sin Ti."
  correccion_Ti_fijada:
    entrenamiento: [TiN, Ti2O3]
    prueba: [TiO2, TiO2_anatasa, MgTiO3]
    formula: "r_i = exp_i − (raw_i + δ_X·x_X,i); δ_Ti = Σ x_Ti,i·r_i / Σ x_Ti,i² (i ∈ entrenamiento); pred_j = raw_j + δ_X·x_X,j + δ_Ti·x_Ti,j"
    nota: "δ_X sale de los 37 sin Ti. δ_Ti no se reajusta tras ver la prueba."
  loocv: "Para cada uno de los 37 sin Ti: δ_X reajustado sin ese compuesto (todos los aniones tienen ≥ 2 compuestos)."
  mp2020: "O −0.687, F −0.462, Cl −0.614, Br −0.534, I −0.379, N −0.361 eV/átomo de anión (Wang et al. 2021, https://doi.org/10.1038/s41598-021-94550-5). Sin término de Ti."
  reacciones_JANAF_0K:
    R1: "MgO + Al2O3 → MgAl2O4"
    R2: "BeO + Al2O3 → BeAl2O4"
    R3: "MgO + TiO2(rutilo) → MgTiO3"
    R4: "ZrO2 + SiO2 → ZrSiO4"
    R5: "TiO2(anatasa) → TiO2(rutilo)"
    R6: "Ti + 3 TiO2(rutilo) → 2 Ti2O3"
    unidad: "eV por átomo de productos; las correcciones δ se cancelan (mismos átomos a cada lado)."
  E_hull: "pymatgen PhaseDiagram por sistema químico con todas las fases calculadas (elementos, moléculas como referencia del anión, 42 compuestos), energías MatterSim con δ_X y δ_Ti aplicados."
hipotesis:
  H-U1: "PRINCIPAL. MatterSim + δ_X + δ_Ti: |pred − exp| ≤ 100 meV/átomo en los 3 compuestos de prueba de Ti."
  H-U2: "MAE en la prueba de Ti con δ_Ti ≤ 0.5 × MAE sin δ_Ti (solo δ_X)."
  H-U3: "PRINCIPAL. MAE LOOCV MatterSim (37 sin Ti) ≤ 60 meV/átomo."
  H-U4: "max |error| (LOOCV de los 37 + prueba de Ti) ≤ 150 meV/átomo, MatterSim."
  H-U5: "MAE LOOCV MatterSim ≤ MAE LOOCV MACE."
  H-U6: "MatterSim + MP2020 fijo (sin Ti), compuestos de O, F, Cl y N (n = 33): MAE ≤ 80 meV/átomo."
  H-U7: "Signo de ΔrH de MatterSim igual al de JANAF (0 K) en ≥ 5 de 6 reacciones."
  H-U8: "MAE de ΔrH MatterSim frente a JANAF ≤ 25 meV/átomo (6 reacciones)."
  H-U9: "PRINCIPAL. E_hull MatterSim ≤ 25 meV/átomo en los 41 compuestos estables (todos menos anatasa) y E_hull(anatasa) ≤ 50 meV/átomo."
  H-REP: "Segunda ejecución completa (run2): |E_run1 − E_run2|/|E_run1| ≤ 1e-6 en todas las energías totales y veredictos iguales."
controles:
  C1: "Todas las relajaciones convergen (fmax 1e-3 eV/Å)."
  C2: "Volumen relajado a ±8 % del inicial (descriptivo)."
  C3: "Los 29 compuestos comunes reproducen las energías de C-UMF-001 run1 a ≤ 1e-6 relativo."
riesgos:
  - "Solo 2 compuestos de entrenamiento de Ti; TiN es metálico y Ti2O3 tiene Ti3+ (sin espín en los uMLIP)."
  - "Los valores a 298.15 K en 4 compuestos introducen ≤ ~5 meV/átomo de sesgo."
  - "E_hull solo frente a fases calculadas aquí (no la base completa de Materials Project)."
decisiones:
  - "Criterios fijados antes de calcular; desviaciones como D1, D2… sin cambiar el veredicto."
  - "Nueva fila UM-18: E3 solo si H-U1, H-U3, H-U9 y H-REP pasan; en otro caso E2. UM-07 sigue en E1."
proximo_paso: "Congelar (sha256 + .FROZEN.md), congelar código, ejecutar run1 y run2 en segundo plano, evaluar."
---
