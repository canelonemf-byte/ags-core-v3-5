---
meta:
  id: C-MAT-004
  titulo: "Corrección empírica de volumen (presión) antes de la QHA, en float64, frente a NIST-JANAF en 17 sólidos (11 de C-MAT-003 + 6 de validación)"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
  fecha_congelacion: "2026-10-19 (UTC+2), antes de cualquier cálculo con los 17 materiales del estudio"
  afirmaciones_registro: [UM-07, UM-14]
  estado: congelado
  antecedente: "C-MAT-003 (prereg 2d9a1256…fc96): la QHA sin corregir empeora S; en un exploratorio no pre-registrado, el armónico en la celda experimental bajó la MARE de S298 de MatterSim de 7.4 a 3.0 %."
objetivo: "Comprobar si fijar el volumen con datos estructurales experimentales (no térmicos) mediante una presión empírica lleva S y Cp desde fonones a ±10 % (MARE ≤ 5 %) de NIST-JANAF, también en 6 sólidos nuevos que no se han usado para nada antes."
datos_clave:
  materiales:
    anclas_C-MAT-003: [Si, MgO, NaCl, LiF, NaF, KCl, KBr, CaO, CaF2, Al2O3, BeO]
    validacion_nuevos: [SrO, MgF2, TiO2 rutilo, SiO2 cuarzo-α, Li2O, MgAl2O4 espinela]
    n: 17
    seleccion: "Nuevos elegidos antes de calcular: tabla JANAF en fase cr sin transición entre 0 y 600 K, S298 verificada con una 2.ª fuente y volumen verificado con una 2.ª fuente primaria. BaO se descartó ANTES de calcular porque su volumen de Robie y Hemingway no coincidía con otras fuentes (≈0.9 %)."
    avisos_a_priori: "Cuarzo: Cp de JANAF a 600 K ya muestra la subida previa a la transición α–β (847 K), que la QHA no puede reproducir. Espinela: se modela la espinela normal; la inversión catiónica parcial y su entropía configuracional no se incluyen."
  referencias_termicas: "refs/refs_termo_C-MAT-004.json: Cp y S de NIST-JANAF a 100, 200, 298.15 y 600 K. Verificación de S298 con CODATA (https://www.codata.info/resources/databases/key1.html), Robie y Hemingway 1995 (https://doi.org/10.3133/b2131) y OSTI 4314983 (LiF). Desviación máxima: 0.77 % (Li2O)."
  referencias_volumen: "refs/vexp_C-MAT-004.json: V_exp a ~298 K por fórmula. Principal: V°298.15 de Robie y Hemingway 1995 (16 materiales) y NBS Circular 539 vol. 1, Swanson y Tatge 1953 (https://nvlpubs.nist.gov/nistpubs/Legacy/circ/nbscircular539v1.pdf) para LiF. Verificación con una 2.ª fuente primaria (artículo cristalográfico con DOI vía COD, o NBS 539). Desviación máxima: 0.24 % (MgF2). Aviso: algunas entradas de COD no declaran la temperatura."
  potenciales:
    principal: "MatterSim v1.0.0-5M, dtype=float64 (mattersim 1.2.5), CPU"
    linea_base: "MACE-MP-0 medium, default_dtype=float64 (mace-torch 0.3.16), CPU"
    excluido: "SevenNet-0: no corre en float64 en este entorno (las capas e3nn compiladas mantienen constantes en float32; error 'both inputs should have same dtype', probado solo con Ge). Se excluye antes de calcular, como exige la regla de float64 para todos los potenciales."
  protocolo:
    relajacion_V0: "FixSymmetry + FrechetCellFilter + BFGS, fmax 1e-3 eV/Å (igual que C-MAT-003)"
    rejilla_QHA: "14 volúmenes V/V_exp = 0.94, 0.96, …, 1.20, por escalado isótropo de la celda relajada (la forma de la celda la da el potencial) y relajación de posiciones con FixSymmetry"
    fonones: "Phonopy 4.8.3, 0.01 Å, malla 60 Å, exclude_gamma_acoustic=True, sin NAC. Superceldas base: cúbicos 2×2×2 de la convencional; Al2O3 2×2×2 de la primitiva; BeO 3×3×2; MgF2 y TiO2 2×2×3; SiO2 2×2×2; MgAl2O4 1×1×1 de la convencional (56 át.). Grandes, solo para C4 en los 6 nuevos: 3×3×3, 3×3×4 o 2×2×2 (espinela)."
    correccion_presion: "P_corr = presión externa tal que V_QHA(298.15 K; P_corr) = V_exp. Se busca por bisección en [−5, 30] GPa hasta |ΔV/V| ≤ 1e-6 (máx. 60 iteraciones), con PhonopyQHA (EOS Vinet) y G = F + PV. La misma P_corr se usa para todas las T."
    entropia: "S(T) = S_vib(T, V(T)) con ajuste cúbico de S(V) a cada T; 298.15 K por interpolación lineal entre 298 y 299 K"
    Cp_suave: "Cp(T) = Cv(T,V(T)) + T·(∂S/∂V)_T·dV/dT; Cv y (∂S/∂V) por ajuste cúbico en V; dV/dT por ajuste cuadrático local de V(T) en T ± 20 K. NO se usa la derivada segunda numérica. Como contraste descriptivo se da heat_capacity_P_polyfit de phonopy."
    armonico_V0: "S y Cv armónicas en el mínimo estático V0 del potencial (sin corrección), como en C-MAT-003"
    armonico_Vexp: "S y Cv armónicas en la celda escalada a V_exp (punto 1.00 de la rejilla)"
    sin_corr: "QHA con P = 0 en la misma rejilla; solo descriptivo"
    determinismo: "float64, torch.use_deterministic_algorithms(True), 4 hilos, semillas fijas, redondeo a 10 cifras significativas; dos ejecuciones completas (run1, run2). Prueba de humo previa con Ge: dos procesos dieron JSON idénticos byte a byte."
  patologias_QHA_decididas_a_priori:
    definicion: "La QHA corregida de un material es PATOLOGICA si ocurre cualquiera de estas cosas:"
    P1: "no se encuentra P_corr en [−5, 30] GPa, o falla la QHA durante la bisección"
    P2: "menos de 8 volúmenes contiguos estables (fmin ≥ −0.3 THz) que incluyan V_exp; solo se excluyen volúmenes inestables de los extremos"
    P3: "t_max de phonopy < 600 K, o V(T) sale del intervalo de volúmenes usado para algún T ≤ 600 K"
    P4: "V(T) no monótono: V(T+1) − V(T) < −1e-6·V en algún T entre 150 y 600 K"
    P5: "α_V(298.15 K) fuera de [0, 3e-4] K⁻¹"
    P6: "|V(298.15)/V_exp − 1| > 1e-4 tras la bisección (control C5)"
    tratamiento: "Un material PATOLOGICO cuenta como fallo en los criterios de recuento y se excluye de las MARE. Si quedan menos de 14 de 17 evaluables (o menos de 5 de 6 en la validación), la MARE correspondiente es INCONCLUSA. No hay plan B silencioso: no se cambia la rejilla, el EOS ni el intervalo después de ver resultados."
  hipotesis:
    H-V1: "PRINCIPAL. MatterSim con QHA corregida: |S(298.15) − S_JANAF|/S_JANAF ≤ 0.10 en ≥ 15 de 17."
    H-V2: "MatterSim con QHA corregida: MARE de S(298.15) ≤ 0.05."
    H-V3: "VALIDACIÓN LIMPIA (solo los 6 nuevos), MatterSim con QHA corregida: ≥ 5 de 6 dentro de ±10 % a 298.15 K Y MARE ≤ 0.05."
    H-V4: "MatterSim con QHA corregida: MARE de S(600 K) ≤ 0.05."
    H-V5: "MatterSim con QHA corregida: MARE de Cp_suave frente a Cp_JANAF ≤ 0.05 a 298.15 K Y ≤ 0.05 a 600 K."
    H-V6: "Para cada potencial (MatterSim y MACE): MARE de S(298.15) con QHA corregida < MARE armónica en V0 sin corregir."
    H-V7: "MatterSim armónico en V_exp: MARE de S(298.15) ≤ 0.05 (repite como prueba pre-registrada el exploratorio de C-MAT-003)."
    H-V8: "Error intrínseco residual: MARE de S(298.15) con QHA corregida de MACE ≥ 1.5 × la de MatterSim."
    H-REP: "results_core de run1 y run2 idénticos byte a byte para los dos potenciales."
  controles:
    C1_regresion: "MACE armónico en V0, 11 anclas: S(298.15) dentro de ±0.5 % de C-MAT-003 run1 (arm_base)."
    C2_signo_presion: "Se informa el signo de P_corr. Se espera P_corr > 0 (subenlace); sin veredicto."
    C3_normalizacion: "Cv(3000 K)/(3R·n_at_prim) en V0 entre 0.99 y 1.000001 para todos."
    C4_convergencia: "Solo en los 6 nuevos: |S298 armónica en V_exp, supercelda grande − base|/base ≤ 0.02; si no, INCONCLUSO (fallo en los recuentos, fuera de las MARE)."
    C5_ajuste_volumen: "ver P6"
    C_PAT: "MatterSim PATOLOGICO en ≤ 2 de 17. Si se supera, se declara que el protocolo QHA no es robusto; los veredictos no cambian."
  reglas_de_evaluacion:
    - "Las comparaciones entre métodos o potenciales (H-V6, H-V8) usan la intersección de materiales evaluables."
    - "El armónico (V0, V_exp) es evaluable si fmin ≥ −0.3 THz en esa celda; si no, NO_EVALUABLE."
    - "Resultados a 100 y 200 K, α_V, P_corr, QHA sin corregir y el contraste de phonopy: solo descriptivos."
sesgos_declarados:
  - "V_exp a ~298 K: la corrección absorbe errores del potencial, de punto cero y de la expansión de 0 a 298 K en una sola presión."
  - "El volumen se fija con datos estructurales, independientes de los térmicos; pero en las anclas ya se vio en C-MAT-003 que el volumen importa, así que H-V3 es la prueba limpia."
  - "Escalado isótropo en los no cúbicos; sin NAC; sin anarmonicidad explícita más allá del volumen."
riesgos:
  - "n = 17 (6 de validación): calibración por recuento, no estadística fina."
  - "Cuarzo y espinela son casos difíciles por los motivos declarados arriba."
decisiones:
  - "Criterios fijados antes de calcular; cualquier cambio posterior es una desviación declarada y no cambia el veredicto original."
  - "Nueva fila UM-15 (C-MAT-004): E2 si se ejecuta con procedencia; E3 solo si H-V1, H-V2, H-V3 y H-REP pasan y C1 y C3 se cumplen."
  - "UM-07 sigue en E1 mientras falten E_form, fases competidoras e incertidumbre."
proximo_paso: "Escribir y hashear el script de evaluación, ejecutar run1 y run2 en segundo plano, material a material, y evaluar."
---
