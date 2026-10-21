---
meta:
  id: C-MAT-003
  titulo: "Termodinámica de fonones con corrección cuasiarmónica (Phonopy QHA) y tres potenciales universales frente a NIST-JANAF en 11 sólidos"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
  fecha_congelacion: "2026-10-19 (UTC+2), antes de cualquier cálculo con los 11 materiales del estudio"
  afirmaciones_registro: [UM-07, UM-10, UM-13]
  estado: congelado
  antecedente: "C-MAT-002 (prereg sha256 af9fd6d7…aa70): MACE-MP-0 armónico sobreestima S298 +5…+28 % en Si, MgO, NaCl."
objetivo: "Comprobar si un potencial universal más reciente (MatterSim) y la corrección cuasiarmónica de volumen llevan la entropía y la capacidad calorífica calculadas desde fonones a ±10 % de NIST-JANAF en ≥ 8 sólidos, con MACE-MP-0 como línea base y SevenNet-0 como segundo potencial nuevo."
datos_clave:
  materiales:
    anclas: [Si, MgO, NaCl]
    nuevos: [LiF, NaF, KCl, KBr, CaO, CaF2, Al2O3, BeO]
    n: 11
    estructuras_iniciales: "Si diamante a=5.431; MgO a=4.212; NaCl a=5.640; LiF a=4.027; NaF a=4.634; KCl a=6.293; KBr a=6.600; CaO a=4.811 (sal gema); CaF2 fluorita a=5.463; Al2O3 corindón R-3c a=4.759 c=12.991 Al z=0.3522 O x=0.3064 (celda primitiva romboédrica, 10 át.); BeO wurtzita a=2.698 c=4.380 u=0.378 (4 át.). Valores de partida aproximados; todo se relaja con cada potencial."
    seleccion: "Sólidos no metálicos sin transición de fase entre 0 y 600 K con tabla JANAF en fase cr y verificación independiente de S298. Elegidos antes de calcular nada con ellos; ningún material se añade ni se retira después."
  referencias: "refs/refs_C-MAT-003.json (Cp y S a 100, 200, 298.15 y 600 K de NIST-JANAF; tablas .txt guardadas con sha256). Verificación de S298 con una segunda fuente: CODATA Key Values (https://www.codata.info/resources/databases/key1.html) para Si, MgO, CaO, Al2O3, BeO; Robie y Hemingway 1995 (https://doi.org/10.3133/b2131) para Si, MgO, NaCl, NaF, KCl, KBr, CaO, CaF2, Al2O3, BeO; LiF con https://www.osti.gov/biblio/4314983 (S298 = 8.53 cal/(K·mol)). Desviación máxima 0.56 % (NaF). Aviso: Robie y Hemingway citan a JANAF para algunas sales, así que esa comprobación no siempre es independiente."
  potenciales:
    principal: "MatterSim v1.0.0-5M (mattersim 1.2.5), CPU"
    secundario: "SevenNet-0 (7net-0, sevenn 0.13.0), CPU"
    linea_base: "MACE-MP-0 medium (mace-torch 0.3.16, float64, mismo checkpoint que C-MAT-001/002), CPU"
    sha256_checkpoints: "se registran en provenance antes de la primera ejecución del estudio"
  protocolo:
    relajacion_V0: "FixSymmetry + FrechetCellFilter + BFGS, fmax 1e-3 eV/Å, máx. 3000 pasos; si no converge se marca y se informa"
    fonones: "Phonopy 4.8.3, desplazamientos finitos 0.01 Å, fuerzas con media restada, constantes de fuerza simetrizadas, sin NAC, malla por longitud 60 Å centrada en Γ, exclude_gamma_acoustic=True (fijado a priori a partir de la desviación D1 de C-MAT-002)"
    superceldas: "cúbicos: 2×2×2 de la celda convencional (base) y 3×3×3 (convergencia en V0); Al2O3: 2×2×2 de la primitiva (base) y 3×3×3; BeO: 3×3×2 (base) y 4×4×3"
    normalizacion: "por mol de fórmula con el número ENTERO de átomos de la celda primitiva de phonopy (no con Cv(3000 K)/3R)"
    armonico: "S y Cv en V0 (mínimo estático, sin energía de punto cero)"
    qha: "10 volúmenes V/V0 = 0.96, 0.98, …, 1.14 por escalado isótropo de la celda relajada; posiciones internas relajadas a celda fija con FixSymmetry (fmax 1e-3); E(V) estática + F_vib(T,V); PhonopyQHA con EOS Vinet, T = 0…900 K paso 1 K; S_QHA(T) = S_vib(T, V(T)) con ajuste polinómico de grado 3 en V; Cp_QHA = heat_capacity_P_numerical de phonopy; valores a 298.15 K por interpolación lineal entre 298 y 299 K"
    hilos: "torch con 4 hilos; semillas fijas; dos ejecuciones completas independientes (run1, run2)"
  hipotesis:
    H-Q1: "PRINCIPAL. MatterSim + QHA: |S(298.15) − S_JANAF|/S_JANAF ≤ 0.10 en ≥ 9 de 11 materiales."
    H-Q2: "MatterSim + QHA: error relativo absoluto medio (MARE) de S(298.15) en los 11 ≤ 0.05."
    H-Q3: "MARE de S(298.15) armónica de MatterSim ≤ 0.5 × MARE armónica de MACE-MP-0 (el potencial nuevo reduce el error al menos a la mitad)."
    H-Q4: "MatterSim: MARE de S(600 K) con QHA < MARE de S(600 K) armónica."
    H-Q5: "MatterSim: MARE de Cp_QHA(600 K) frente a Cp_JANAF < MARE de Cv armónica(600 K) frente a Cp_JANAF."
    H-Q6: "SevenNet-0: MARE de S(298.15) armónica < MARE armónica de MACE-MP-0."
    H-Q7: "MACE-MP-0 armónico sobreestima S(298.15) (error > 0) en ≥ 9 de 11 materiales (generaliza H-TH-2 de C-MAT-002)."
    H-REP: "Para los tres potenciales, results_core.json de run1 y run2 idénticos byte a byte. Se informa aparte la diferencia relativa máxima."
  controles:
    C1_regresion: "MACE-MP-0 armónico (superceldas base) reproduce S(298.15) de C-MAT-002 v1.1 sc2 dentro de ±1 %: Si 24.097, MgO 32.976, NaCl 75.835 J/(K·mol)."
    C2_signo_qha: "S_QHA(600) ≥ S_arm(600) en cada material y potencial evaluable (expansión térmica positiva). Si falla en > 2 materiales de MatterSim, H-Q4 y H-Q5 pasan a INCONCLUSAS."
    C3_normalizacion: "Cv(3000 K)/(3R·n_at_prim) en V0 entre 0.99 y 1.000001."
    C4_convergencia: "|S298 superceldas grandes − base|/base ≤ 0.02 en V0; si no, el material queda INCONCLUSO para ese potencial."
    C5_estabilidad: "fmin ≥ −0.3 THz en V0. En QHA, los volúmenes con fmin < −0.3 THz solo se excluyen si están en los extremos y quedan ≥ 6 volúmenes contiguos estables que incluyan V0; si no, QHA = NO_EVALUABLE para ese material."
    C6_horquilla: "V(T) a 600 K debe quedar dentro del intervalo de volúmenes estables usado; si no, 600 K = NO_EVALUABLE para ese material."
  reglas_de_evaluacion:
    - "Los materiales INCONCLUSOS o NO_EVALUABLES cuentan como fallo en los criterios de recuento (H-Q1, H-Q7)."
    - "Los criterios MARE se calculan con los materiales evaluables; si quedan < 9, la hipótesis es INCONCLUSA."
    - "Las hipótesis se evalúan con superceldas base; las grandes solo sirven para C4."
    - "Resultados a 100 y 200 K, expansión térmica y frecuencias TO-Γ se dan solo como descripción, sin veredicto."
sesgos_declarados:
  - "Sin anarmonicidad explícita más allá del volumen (QHA); las sales de K y los haluros pueden necesitar más."
  - "Escalado isótropo en Al2O3 y BeO (sin relajar c/a en cada volumen)."
  - "Sin NAC: afecta solo a la separación LO–TO cerca de Γ; efecto esperado en S < 1 %."
  - "JANAF por debajo de 298 K procede de calorimetría antigua; su incertidumbre no siempre está tabulada."
riesgos:
  - "n = 11: suficiente para una calibración por recuento, no para una estadística fina."
  - "MatterSim y SevenNet-0 pueden mostrar modos imaginarios a volúmenes expandidos."
  - "Las pruebas de humo del código se hacen con Ge y Cu, que NO están en el estudio."
decisiones:
  - "Criterios fijados antes de calcular; cualquier cambio posterior se declara como desviación y no cambia el veredicto original."
  - "Nueva fila del registro para C-MAT-003: E2 si se ejecuta con procedencia; E3 solo si H-Q1, H-Q2 y H-REP pasan y C1–C3 se cumplen."
  - "UM-10: E2 → E3 solo si el mismo flujo corre sin cambios con los tres potenciales en los 11 materiales y H-REP pasa para los tres."
  - "UM-07 sigue en E1 mientras falten E_form, fases competidoras e incertidumbre, sea cual sea el resultado."
proximo_paso: "Prueba de humo con Ge/Cu, congelar hashes del código y ejecutar run1 y run2 en segundo plano, material a material."
---
