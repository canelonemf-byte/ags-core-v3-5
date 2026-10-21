---
meta:
  id: C-MAT-002
  fecha: "2026-10-19 (UTC+2)"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
  prereg_sha256: af9fd6d7e39a00bef5082bf8cfe47a35064e70dec189096606889bbda332aa70
  cronologia: "prereg congelado 09:10:31 · run.py 09:10:56 · eval.py escrito 09:11:19 sin haber leído resultados · run1 09:11:30 · run2 09:11:54 · v1.1 (D1) 09:13:03 y 09:13:24"
  afirmaciones: [UM-07, UM-10, UM-13]
objetivo: "Verificar el paso de propiedades térmicas del flujo MV1 frente a NIST-JANAF (UM-07) y ejecutar el mismo flujo con tres calculadores independientes en Si (UM-10)."
datos_clave:
  S298_J_Kmol:
    Si: {JANAF: 18.820, MACE: 24.120, SW: 16.502, Kumagai: 14.966}
    MgO: {JANAF: 26.924, MACE: 32.866}
    NaCl: {JANAF: 72.115, MACE: 75.774}
  error_rel_S298: {MACE_Si: "+28.2 %", MACE_MgO: "+22.1 %", MACE_NaCl: "+5.1 %", SW_Si: "−12.3 %", Kumagai_Si: "−20.5 %"}
  error_rel_Cv_vs_Cp: {MACE_Si: {T100: "+40.6 %", T298: "+8.7 %"}, MACE_MgO: {T100: "+44.7 %", T298: "+7.2 %"}, MACE_NaCl: {T100: "+5.8 %", T298: "−4.7 %"}}
  TO_Gamma_Si_THz: {exp: 15.595, MACE: 11.184, SW: 17.832, Kumagai: 18.400}
  comprobacion_externa: "SW da 17.832 THz = 594.8 cm-1; la literatura publica 594.76 cm-1 para SW original (https://utw10370.utweb.utexas.edu/publications/P116.pdf). El flujo reproduce un valor publicado con un calculador distinto."
  convergencia_2x2x2_vs_3x3x3: "|ΔS298| ≤ 0.33 %; ningún caso inconcluso"
  ratio_dS_obs_pred: {Si: 0.64, MgO: 0.68}
tareas:
  veredictos_criterios_originales:
    H-TH-1: "FALSADA (Si +28 %, MgO +22 % > 10 %; NaCl +5 % pasa)"
    H-TH-2: "PASA (MACE sobreestima S en los 3 pese a sesgos que empujan hacia abajo)"
    H-TH-3: "PASA (el error de Cv a 100 K supera al de 298 K en los 3)"
    H-TH-4: "PASA (0.64 y 0.68 dentro de [0.5, 1.5]; el ablandamiento medio del espectro es ~2/3 del de la rama TO)"
    H-X-1: "PASA (3 calculadores, relajación convergida, fmin ≥ −6e-7 THz)"
    H-X-2: "FALSADA (SW: S −12 %, TO +14 %; Kumagai: S −20 %, TO +18 %)"
    H-X-3: "PASA (MACE 24.1 > JANAF 18.8 > SW 16.5 > Kumagai 15.0: los modelos horquillan el experimento)"
    H-X-4: "FALSADA en v1.0 (MACE Si S298 24.147 vs 24.120 entre ejecuciones)"
riesgos:
  - "D1 (desviación declarada, post hoc): la no reproducibilidad de v1.0 viene de los 3 modos acústicos en Γ (~1e-7 THz, ruido numérico de MACE en CPU) que entran en las sumas térmicas; phonopy avisa con GammaAcousticWarning. v1.1 con exclude_gamma_acoustic=True da results_core.json idénticos byte a byte (sha256 b82bd5ad…cdbb). Efecto ≤ 0.11 % en S298; ningún veredicto H-TH/H-X-1..3 cambia. El veredicto original de H-X-4 sigue siendo FALSADA."
  - "D2 (sesgo detectado): la normalización por Cv(3000 K)/3R da 1.993–1.999 átomos en lugar de 2 (corrección cuántica residual), lo que infla S y Cv ≤ 0.36 %. No cambia ningún veredicto."
  - "n = 3 materiales y 1 solo material para 3 calculadores: calibración, no estadística."
  - "S armónica a volumen de 0 K y Cv frente a Cp: sesgos de 1–5 % declarados en el prereg."
decisiones:
  - "UM-13 (nueva fila, campaña C-MAT-002): E2. No E3 porque H-TH-1, H-X-2 y H-X-4 (original) fallan."
  - "UM-10: E0 → E2. El flujo corre sin cambios con 3 calculadores independientes y reproduce un valor publicado (SW), pero los resultados no coinciden entre calculadores."
  - "UM-07: se queda en E1 (faltan E_form, fases competidoras e incertidumbre); el paso térmico ya está ejecutado y verificado frente a JANAF."
  - "Exploratorio no pre-registrado, sin valor probatorio: con SW y Kumagai el cociente ΔS_obs/ΔS_pred(TO) es 0.70 y 0.93."
proximo_paso: "Nuevo prereg C-MAT-003 con n ≥ 8 sólidos JANAF, un uMLIP más reciente (MatterSim o SevenNet, que en Loew et al. 2025 tienen MAE(S) 15 y 48 J/K/mol frente a 60 de MACE-MP-0) y corrección cuasiarmónica de volumen. Mantener exclude_gamma_acoustic=True y normalización entera."
---
