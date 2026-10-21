---
meta:
  id: C-MAT-006
  titulo: "Regla de modos blandos fijada a priori, S(298) y S(600) armónicas en V_exp para 31 sólidos frente a NIST-JANAF (MatterSim vs MACE) y prueba DFT PBE de rutilo en supercelda 2×2×2 a 650 eV"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
  fecha_congelacion: "2026-10-20 (UTC+2), antes de cualquier cálculo de esta campaña"
  afirmaciones_registro: [UM-15, UM-16, UM-19]
  estado: congelado
  antecedente: "C-MAT-005: MatterSim en V_exp 13/14 a ±10 % (MARE S298 2.31 %), pero el control C2 falló (modos blandos de KI) y la prueba DFT de rutilo (2×2×1, 500 eV) y de cuarzo quedó INCONCLUSA. C-MAT-004: rutilo y cuarzo inestables con ambos uMLIP; el mínimo de MatterSim en rutilo está cerca de q = (0.43, 0, 0.5)."
objetivo: "Fijar una regla única para modos imaginarios, aplicarla a 31 sólidos (C-MAT-004 + C-MAT-005, incluidos rutilo y cuarzo) y decidir con DFT si la inestabilidad de rutilo cerca de (½, 0, ½) es un artefacto del potencial."
datos_clave:
  materiales: "31 = 17 de C-MAT-004 [Si, MgO, NaCl, LiF, NaF, KCl, KBr, CaO, CaF2, Al2O3, BeO, SrO, MgF2, TiO2, SiO2, Li2O, MgAl2O4] + 14 de C-MAT-005 [AlN, SiC, KF, NaBr, KI, LiCl, CsCl, SrF2, BaF2, Na2O, ZrO2, BeAl2O4, MgTiO3, ZrSiO4]. Estructuras, V_exp y S de JANAF ya verificados y con hash en C-MAT-004/refs y C-MAT-005/refs (sin cambios)."
  protocolo_mlip: "Igual que C-MAT-005 en V_exp: relajación completa con simetría, escalado isótropo a V_exp, relajación de posiciones, Phonopy 0.01 Å en la supercelda base de C-MAT-004/005, malla 60 Å centrada en Γ. float64, CPU, 4 hilos, semilla 0."
  regla_modos_blandos:
    R0: "Se usan todas las frecuencias de la malla con sus pesos. Un modo es imaginario si ν < −0.05 THz; los 3 acústicos de Γ se excluyen siempre."
    R1: "f_imag = fracción ponderada de modos imaginarios (sobre los 3·N_prim·N_q modos menos los acústicos de Γ)."
    R2: "Si f_imag = 0: S(T) armónica normal sobre los modos con ν > 0.05 THz (implementación propia; control C1 frente a Phonopy)."
    R3: "Si 0 < f_imag ≤ 0.02: los modos imaginarios se excluyen y S se reescala por 1/(1 − f_imag) (cada modo excluido aporta la entropía media de los reales). Material 'evaluable_con_regla'."
    R4: "Si f_imag > 0.02: NO evaluable; cuenta como fallo en H1 y queda fuera de las MARE."
  referencias: "S° NIST-JANAF a 298.15 y 600 K (Chase 1998, https://doi.org/10.18434/T42S31) desde refs_termo_C-MAT-004.json y refs_termo_C-MAT-005.json."
  dft_rutilo:
    celda: "Celda experimental fija de COD 9007531 (Baur y Khan 1971, https://doi.org/10.1107/S0567740871005466)."
    metodo: "GPAW (PW), PBE, ecut 650 eV, FermiDirac 0.01 eV, densidad 1e-6, fuerzas 1e-4 eV/Å. Relajación de posiciones (FixSymmetry, BFGS, fmax 2e-3) en celda primitiva con k 4×4×6 a 650 eV."
    supercelda: "2×2×2 (48 átomos), k 2×2×3, Phonopy 0.01 Å. q conmensurados: incluyen (½,0,½), (0,½,½), (½,½,½), (½,0,0), (0,0,½), Γ, etc. Se informa ν_min en todos y en particular en (½,0,½), el q conmensurado más próximo al mínimo de MatterSim."
    mlip_misma_celda: "MatterSim y MACE en la misma celda experimental, posiciones relajadas por cada potencial, misma supercelda 2×2×2."
    clases: "A = artefacto del potencial si ν_min,conm(uMLIP) < −0.3 THz y ν_min,conm(PBE) ≥ −0.3 THz; B = heredada de PBE si ambos < −0.3 THz; C = no reproducida si ν_min,conm(uMLIP) ≥ −0.3 THz; INCONCLUSA_DFT si falla C-DFT1 o C-DFT2 o no termina."
  dft_cuarzo_factibilidad: "Cuarzo-α (COD 9013321) se simetriza con spglib (symprec 1e-3). Se ejecuta PBE 650 eV en 2×2×1 (36 átomos, k 2×2×3) SOLO si el rutilo ha terminado y Phonopy da ≤ 6 desplazamientos. Si no, o si no termina antes de 2026-10-21 12:00 (UTC+2), H-D2 = INCONCLUSA (no es desviación)."
hipotesis:
  H1: "PRINCIPAL. MatterSim en V_exp con la regla: |S298 − S_JANAF|/S_JANAF ≤ 0.10 en ≥ 26 de 31 (no evaluables cuentan como fallo)."
  H2: "PRINCIPAL. MatterSim: MARE S298 ≤ 0.05 sobre evaluables (INCONCLUSA si n < 21)."
  H3: "MatterSim: MARE S600 ≤ 0.06 sobre evaluables (INCONCLUSA si n < 21)."
  H4: "MARE S298 MatterSim ≤ 0.6 × MARE S298 MACE (intersección de evaluables; INCONCLUSA si n < 21)."
  H5: "Regla R3: en los materiales 'evaluable_con_regla' de MatterSim, |error S298| ≤ 0.10 en al menos 2/3 de ellos (INCONCLUSA si hay < 3)."
  H6: "MatterSim: n.º de no evaluables (R4) ≤ 3 de 31."
  H-D1: "Rutilo: la inestabilidad de MatterSim es artefacto. CONFIRMADA si clase A; REFUTADA si B; INCONCLUSA si C o INCONCLUSA_DFT. MACE: descriptivo."
  H-D2: "Cuarzo-α: igual que H-D1, sujeto a la regla de factibilidad."
  H-REP: "run2 completo de los MLIP: |S_run1 − S_run2|/|S_run1| ≤ 1e-6 a 298.15 y 600 K, f_imag igual y veredictos de H1–H6 iguales. La DFT no se replica (coste), se declara."
controles:
  C1: "Para los materiales con f_imag = 0, la S propia coincide con la S de Phonopy a ≤ 1e-4 relativo (298.15 K)."
  C2: "Regresión: S298 MatterSim en V_exp de los 14 materiales de C-MAT-005 a ≤ 1e-4 relativo de C-MAT-005 run1 cuando f_imag = 0."
  C-DFT1: "Rutilo, celda primitiva, PBE: frecuencias de Γ a 650 y 800 eV difieren ≤ 0.15 THz en todos los modos."
  C-DFT2: "Relajación PBE convergida (fmax ≤ 2e-3 eV/Å)."
sesgos_declarados:
  - "V_exp es dato de entrada; sin anarmonicidad ni expansión entre 298 y 600 K (sesgo negativo en S600)."
  - "R3 supone que los modos excluidos aportan la entropía media; es una convención, no física."
  - "La supercelda 2×2×2 solo explora q conmensurados; (0.43, 0, 0.5) no es conmensurado y se usa (½, 0, ½)."
riesgos:
  - "DFT en CPU con 48 átomos a 650 eV: horas; memoria del equipo limitada (~3 GB libres)."
  - "Las celdas de C-MAT-004/005 ya se usaron; la novedad es la regla y la DFT, no los materiales."
decisiones:
  - "Criterios fijados antes de calcular; desviaciones como D1, D2… sin cambiar el veredicto."
  - "Nueva fila UM-19: E3 solo si H1, H2 y H-REP pasan y C1 se cumple; si no, E2. H-D1 se registra aparte en UM-15/UM-16 como nota."
proximo_paso: "Congelar (sha256 + .FROZEN.md), congelar código, lanzar DFT y MLIP en segundo plano, evaluar."
---
