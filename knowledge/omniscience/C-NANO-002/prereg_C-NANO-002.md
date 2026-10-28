# Prerregistro C-NANO-002 — Fonones de monocapas 2D (grafeno, h-BN, MoS2) con potenciales universales y entropía vibracional monocapa vs. masivo
meta:
  id: C-NANO-002
  proyecto: omniscience
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963"
  fecha: "2026-10-22 (Europe/Madrid)"
  licencia: "CC BY 4.0"
  registro_origen: "NANO-04 (E1), NANO-05 (E0) en evidence_register.csv"
objetivo: "Medir con MatterSim (principal) las frecuencias de fonones en Γ, M y K de grafeno, h-BN y MoS2-1H monocapa frente a referencias DFT y Raman verificadas, la ley ZA ω∝q^n, y la diferencia de entropía vibracional S(298) monocapa − masivo con y sin D3(BJ) en el masivo."
datos_clave:
  codigo: "code/nano2_run.py, code/nano2_eval.py, code/gpaw_grafeno.py, code/guardia.py (sha256 en code_freeze.sha256)"
  potenciales: "MatterSim-v1.0.0-5M float64 (venv_ms, mattersim 1.2.5); contraste MACE-MP-0 medium float64 (venv_mace, mace 0.3.16); D3(BJ, parámetros PBE) con torch_dftd 0.5.3 (Grimme 2010 https://doi.org/10.1063/1.3382344; BJ 2011 https://doi.org/10.1002/jcc.21759). CPU, 2 hilos."
  monocapas: "Celda hexagonal, vacío c = 20 Å; relajación de a y posiciones con FixSymmetry (c fijo), BFGS fmax 0.002 eV/Å. Phonopy 4.8.3, supercelda 6×6×1, fuerzas con deriva restada, symmetrize_force_constants (solo regla de suma traslacional; no hay regla rotacional disponible en el entorno: se declara)."
  masivos: "Grafito AB (4 át.), h-BN AA' (4 át.), 2H-MoS2 (6 át.); relajación completa (FrechetCellFilter) con MatterSim+D3 y, por separado, con MatterSim solo. Superceldas 3×3×2, 3×3×2 y 3×3×1 (reducidas por memoria; ver smoke/smoke_mem.log)."
  modos: "Γ: 3 acústicos = |ν| mínimos. Grafeno/h-BN: ZO = óptico con fracción z > 0.5; LO/TO = media de los 2 ópticos en el plano. MoS2: fuera de plano ópticos → A1' (menor peso de Mo), A2'' (otro); en el plano ópticos → E'' (2 de menor peso Mo, media), E' (otros 2, media). M/K (grafeno): fuera de plano ZA (menor), ZO (mayor); en plano ordenados TA<LA<LO<TO en M; en K TA, LA/LO (media del 2.º y 3.º), TO."
  ZA: "ν_ZA a lo largo de Γ–M en q = (0.04…0.15)·|ΓM| (12 puntos); exponente n = pendiente log-log; si algún ν_ZA ≤ 0 en la ventana, no evaluable (cuenta como fallo)."
  entropia: "S_vib(298.15 K) por átomo en k_B con la regla de modos blandos R0–R4 de C-MAT-006 (ν_imag < −0.05 THz, f_imag ≤ 0.02 evaluable con reescalado, > 0.02 no evaluable); contraste Phonopy con exclude_gamma_acoustic=True. Mallas q run1: monocapa 48×48×1, masivo 24×24×8."
  run1: "semilla 1 (escala inicial de celda aleatoria ±1 %), desplazamiento 0.010 Å, mallas 48×48×1 / 24×24×8"
  run2_replica: "semilla 2, desplazamiento 0.015 Å, mallas 36×36×1 / 18×18×6"
  referencias_DFT_monocapa:
    grafeno: "Mounet y Marzari 2005, https://doi.org/10.1103/PhysRevB.71.205214 (tabla IV, columna grafeno GGA, texto arXiv cond-mat/0412643v1): Γ ZO 881, Γ LO/TO 1554, M ZA 471, M TA 626, M ZO 635, M LA 1328, M LO 1340, M TO 1390, K ZA 535, K ZO 535, K TA 997, K LA/LO 1213, K TO 1288 cm⁻¹"
    hBN: "D'Souza y Mukherjee 2017, https://doi.org/10.1103/PhysRevB.96.205422 (tabla I, SLBN, texto arXiv 1711.02366v1): Γ ZO (A2u) 819.37, Γ LO/TO (E2g/E1u) 1363.88 cm⁻¹"
    MoS2: "Molina-Sánchez y Wirtz 2011, https://doi.org/10.1103/PhysRevB.84.155413 (tabla II, monocapa LDA, texto arXiv 1109.5499v1): E'' 289.2, E' 391.7, A1' 410.3, A2'' 476.0 cm⁻¹"
  referencias_experimentales:
    grafeno_G: "≈1580 cm⁻¹ (Ferrari et al. 2006, https://doi.org/10.1103/PhysRevLett.97.187401)"
    hBN_E2g_monocapa: "1366 cm⁻¹ en cristal masivo + desplazamiento hasta +4 cm⁻¹ en monocapa → se usa 1368 (Gorbachev et al. 2011, https://doi.org/10.1002/smll.201001628)"
    MoS2_E_prima: "≈384 cm⁻¹ monocapa (Lee et al. 2010, https://doi.org/10.1021/nn1003937). El A1' monocapa (~403) solo aparece en figura; no se usa."
    S298_JANAF: "NIST-JANAF (Chase 1998, https://doi.org/10.18434/T42S31): C(ref, grafito) 5.740 J/(K·mol) = 0.6904 k_B/át; BN(cr) 14.795 J/(K·mol) = 0.8897 k_B/át. MoS2 no está en JANAF."
  humo_previo_declarado: "Solo tiempos y memoria de fuerzas (smoke/smoke_tiempo.log, smoke_mem.log); ninguna frecuencia ni entropía calculada antes de congelar. Un primer humo con D3 a 95 bohr en supercelda 4×4×2 agotó la RAM (OOM) — de ahí la reducción."
hipotesis:
  H1: "NANO-04a. 8 frecuencias ópticas Γ (MatterSim) vs DFT monocapa: PASA si ≤ 2 de 8 fuera de ±5 %."
  H2: "NANO-04b. Grafeno M/K: 9 frecuencias (M ZA, TA, ZO, LA, LO, TO; K ZA, TA, LA/LO) vs Mounet GGA: PASA si ≤ 2 de 9 fuera de ±5 %. K TO (anomalía de Kohn) solo informativo."
  H3: "NANO-04c. Raman experimental (G grafeno 1580, E2g h-BN 1368, E' MoS2 384): PASA si 3/3 dentro de ±5 %."
  H4: "NANO-04d. Exponente ZA n ∈ [1.8, 2.2] en las 3 monocapas."
  H5: "NANO-05a. ΔS = S_mono(MS) − S_masivo(MS+D3) ∈ [0.05, 0.6] k_B/át en las 3 parejas."
  H6: "NANO-05b. |ΔS(masivo MS+D3) − ΔS(masivo MS sin D3, relajado sin D3)| < 0.1 k_B/át en las 3 parejas."
  H_REP: "run2 vs run1 (MatterSim): todas las frecuencias de H1–H3 y M/K cambian ≤ 1 %, |Δn_ZA| ≤ 0.1 (evaluable en las 3), |ΔS| ≤ 0.02 k_B/át en las 9 entropías, y veredictos H1–H6 iguales."
controles:
  C1: "GPAW PBE (PW 500 eV, k 18×18×1) Γ de grafeno en la red MatterSim run1: |ν_MS − ν_PBE|/ν_PBE ≤ 5 % para ZO y LO/TO. Si GPAW no cabe en memoria o no termina, NO EVALUABLE."
  C2: "MACE-MP-0: H1–H4 informativas (no cambian nivel)."
  C3: "S298 masivo MS+D3 de grafito y h-BN dentro de ±10 % de NIST-JANAF."
regla_nivel_E:
  NANO_04: "E3 si H_REP PASA y C1 PASA (sea cual sea el veredicto H1–H4); E2 si H_REP PASA y C1 falla o no evaluable; E1 si H_REP FALLA."
  NANO_05: "E3 si H_REP PASA y C3 PASA; E2 si H_REP PASA y C3 falla; E1 si H_REP FALLA."
tareas: ["congelar", "run1 MS mono", "run1 MS+D3 y MS masivo", "run2 réplica", "MACE run1 mono", "GPAW grafeno Γ", "evaluación tal cual", "figura", "registro + LoRA"]
riesgos: ["Referencias DFT con funcionales distintos (GGA grafeno, LDA h-BN y MoS2): ±5 % mezcla error de método", "Sin regla de suma rotacional: ZA puede salir lineal o imaginaria cerca de Γ", "Masivos con superceldas pequeñas", "S° JANAF incluye expansión térmica y anarmonía; la armónica a volumen fijo no", "Cálculo CP2K ajeno en curso: memoria limitada (guardia oom_score_adj=1000 + MemAvailable < 700 MB aborta)"]
decisiones: ["D3 con corte 40 bohr (C-UMF-003 usó 95) por memoria", "A1' monocapa experimental descartado por no tener valor textual verificable", "Superceldas masivas 3×3×2 / 3×3×1 en lugar de 4×4×2"]
proximo_paso: "Ejecutar run1, run2, MACE y GPAW con memoria vigilada; evaluar con code/nano2_eval.py congelado."
