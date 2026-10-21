# Prerregistro C-UMF-006 — TiO2 anatasa−rutilo: corrección híbrida (sustituye a HSE06) + corrección vibracional en V_exp con la regla de C-MAT-006
meta:
  id: C-UMF-006
  proyecto: omniscience
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963"
  fecha: "2026-10-21 (Europe/Madrid)"
  licencia: "CC BY 4.0"
  antecedentes: "C-UMF-004: PBE −30.5, r2SCAN −11.8 meV/át, ΔH_vib −47.9 con modos imaginarios, HSE06 sin terminar. C-UMF-005: r2SCAN CP2K −13.7, PBE CP2K −30.7 meV/át (k convergida). Experimento +9.0±1.4 meV/át (https://doi.org/10.1073/pnas.251534898)."
objetivo: "Retomar lo pendiente de C-UMF-004: (A) estimar el desplazamiento híbrido δ_hyb de ΔE(A−R) y (B) una corrección vibracional sin artefactos de modos blandos, y comprobar si PBE + δ_hyb + ΔH_vib reproduce el signo y la magnitud experimental."
datos_clave:
  inviabilidad_hse06_declarada: "Antes de congelar: HSE06 (ω = 0.11 bohr⁻¹) con RI-HFX en puntos k en CP2K 2026.2 fue terminado por falta de memoria (señal 9, 15 GB) con k 2×2×2 en la celda primitiva de anatasa, y CP2K advierte que el alcance del término de corto alcance (15.9 Å) exige una supercelda de Born–von Kármán ≥ 32 Å. HSE06 queda fuera de alcance en esta máquina (desviación de alcance respecto al encargo)."
  sustituto_A: "PBE0 truncado (25 % HF, potencial TRUNCATED, R_c = 3.5 Å, corrección PBE_HOLE_T_C_LR) con ADMM (admm-dzp), base DZVP-MOLOPT-PBE0 y GTH-PBE0, solo Γ, superceldas rutilo 2×2×3 (72 át.) y anatasa 2×2×1 convencional (48 át.), geometrías PBE de C-UMF-004 (a_run1). En las mismas superceldas: PBE con DZVP-MOLOPT-PBE/GTH-PBE. δ_hyb = ΔE_hyb,Γ − ΔE_PBE,Γ (meV/át). E_hyb = −30.7 + δ_hyb (PBE CP2K k-convergido de C-UMF-005). Humo de tiempo previo: el primer paso SCF híbrido no terminó en ~15 min con 4 procesos MPI y CPU compartida; se mató."
  limite_computo: "Cada cálculo híbrido tiene un tope de 5 h (timeout). Si alguno no termina, HA1–HA3 = NO EVALUABLE."
  parte_B: "MatterSim (principal) y MACE-MP-0 medium (réplica): relajación completa con simetría, escalado isótropo a V_exp (rutilo COD 9007531 https://doi.org/10.1107/S0567740871005466; anatasa COD 9015929 https://doi.org/10.1107/S010876819100335X), relajación de posiciones, Phonopy 0.01 Å, superceldas rutilo 2×2×3 y anatasa 3×3×1 convencional, malla 60, regla R0–R4 de C-MAT-006. Se informan ΔZPE, ΔU_vib(298) y ΔF_vib(298) por átomo (A − R)."
  codigo: "code/hse_cp2k.py, code/vib_tio2.py, code/eval_umf006.py (sha256 en code_freeze.sha256)"
hipotesis:
  HA1: "δ_hyb > 0 (el híbrido desplaza ΔE(A−R) hacia valores positivos)."
  HA2: "E_hyb + ΔU_vib(298, MatterSim) ∈ [−1.0, 19.0] meV/át (experimento ± 10)."
  HA3: "E_hyb tiene el signo experimental (> 0)."
  HB1: "Rutilo y anatasa son 'normal' o 'evaluable_con_regla' con MatterSim (f_imag ≤ 0.02)."
  HB2: "|ΔU_vib(298)| MatterSim ≤ 5 meV/át (la corrección vibracional es pequeña; el −47.9 de C-UMF-004 era artefacto)."
  H_REP: "Réplica: (i) |ΔU_vib MACE − ΔU_vib MatterSim| ≤ 3 meV/át; (ii) δ_hyb con R_c = 3.0 Å difiere ≤ 5 meV/át del de R_c = 3.5 Å (solo si hay cómputo; si no, (ii) NO EVALUABLE y H_REP se decide por (i))."
regla_nivel_E: "E2 si HA evaluable y H_REP PASA; E1 si H_REP falla o la parte A no es evaluable."
tareas: ["congelar", "parte B MatterSim y MACE", "parte A PBE Γ (2) + PBE0-TC Γ (2) [+ R_c 3.0 (2)]", "evaluación", "figura", "registro + LoRA"]
riesgos: ["PBE0 truncado a 3.5 Å no es HSE06; con R_c pequeño el intercambio de largo alcance se trata con el agujero LR de PBE", "Superceldas Γ pequeñas: se mitiga usando diferencias Δ_hyb − Δ_PBE en la misma supercelda"]
decisiones: ["HSE06 → PBE0-TC (desviación de alcance declarada antes de calcular)"]
proximo_paso: "Lanzar parte B ya; parte A cuando terminen C-NANO-001 y C-MAT-007 (CPU)."
