# Prerregistro C-MAT-007 — S(298), S(600) y Cp armónica en V_exp para 44 sólidos (31 de C-MAT-006 + 13 nuevos) con la regla de modos blandos de C-MAT-006
meta:
  id: C-MAT-007
  proyecto: omniscience
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963"
  fecha: "2026-10-21 (Europe/Madrid)"
  licencia: "CC BY 4.0"
objetivo: "Ampliar la prueba de entropía armónica de MatterSim en volumen experimental a ≥40 sólidos y añadir Cp, sin cambiar la regla de modos blandos (R0–R4) fijada en C-MAT-006."
datos_clave:
  materiales: "31 de C-MAT-006 (mismas celdas, V_exp y supercelda base) + 13 nuevos cúbicos: LiBr, NaI, LiH, NaH, BaO, MgS, CaS, CsF (sal gema), Na2S, K2O, Mg2Si (antifluorita), Al, Cu (fcc). LiI se descarta antes de calcular: la consulta COD no devolvió entradas Fm-3m (declarado)."
  v_exp_nuevos: "a = mediana de las entradas COD Fm-3m sin presión declarada y T no especificada o 280–305 K (refs/cod_cmat007.json, consulta 2026-10-21). Riesgo: algunas entradas COD (p. ej. Cu de 10.1021/ic026022z) son de nanopartículas o síntesis especiales; se acepta la mediana tal cual."
  referencias: "NIST-JANAF (Chase 1998, https://doi.org/10.18434/T42S31): C-MAT-004/005 (ya verificados) y refs/refs_termo_C-MAT-007.json (13 tablas nuevas descargadas 2026-10-21 con sha256; sin segunda fuente: declarado)."
  protocolo: "Idéntico a C-MAT-006 (MatterSim v1.0.0-5M, relajación completa con simetría, escalado isótropo a V_exp, relajación de posiciones, Phonopy 0.01 Å, malla 60, regla R0–R4). Nuevos: celda cúbica convencional, supercelda 2×2×2 (Al, Cu: 3×3×3). Cv armónica con los mismos modos y el mismo reescalado 1/(1−f_imag) que S; se compara con Cp de JANAF (Cv ≤ Cp esperado)."
  humo_previo_declarado: "Humo de tiempo antes de congelar: MgS S298 = 49.38 J/(K·mol) (JANAF 50.33), Cv298 = 44.67 (JANAF Cp 45.56)."
  codigo: "code/cmat007_run.py, code/cmat007_eval.py (sha256 en code_freeze.sha256)"
hipotesis:
  H1: "PRINCIPAL. |S298 − S_JANAF|/S_JANAF ≤ 0.10 en ≥ 37 de 44 (no evaluables cuentan como fallo)."
  H2: "MARE S298 ≤ 0.05 sobre evaluables (INCONCLUSA si n < 30)."
  H3: "MARE S600 ≤ 0.05 sobre evaluables."
  H4: "MARE (Cv298 frente a Cp298 JANAF) ≤ 0.05 sobre evaluables."
  H5: "Cv(600) < Cp_JANAF(600) en ≥ 75 % de los evaluables (falta de dilatación/anarmonicidad)."
  H6: "Generalización: ≥ 10 de los 13 nuevos con |error S298| ≤ 0.10."
  H_REP: "Réplica run2 con desplazamiento Phonopy 0.02 Å: |ΔS298|/S298 ≤ 0.01 en ≥ 90 % de los comparados y mismos veredictos H1–H6."
regla_nivel_E: "E3 si H_REP PASA (simulación verificada frente a dato experimental); E2 si falla."
tareas: ["congelar", "run1", "run2 (0.02 Å)", "evaluación", "figura", "registro + LoRA"]
riesgos: ["Hidruros (LiH, NaH): efectos cuánticos nucleares y anarmonicidad fuertes", "Metales: S electrónica no incluida (pequeña a 298 K)", "Cv frente a Cp: diferencia sistemática esperada a 600 K"]
decisiones: ["Regla R0–R4 sin cambios", "Sin MACE en esta campaña (alcance)"]
proximo_paso: "Lanzar run1 y run2 en segundo plano y evaluar con el código congelado."
