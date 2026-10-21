---
meta:
  id: C-MAT-005
  titulo: "Fonones armónicos en el volumen experimental (V_exp) frente a NIST-JANAF en 14 sólidos nuevos, float64, con prueba DFT de artefacto en rutilo y cuarzo-α"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
  fecha_congelacion: "2026-10-19 (UTC+2), antes de cualquier cálculo con los materiales del estudio"
  afirmaciones_registro: [UM-07, UM-15, UM-16]
  estado: congelado
  antecedente: "C-MAT-004 (prereg 160ce4b2…2363): H-V7 PASA (MatterSim armónico en V_exp, MARE S298 2.94 %, n = 15), pero la QHA corregida no fue robusta; rutilo y cuarzo-α salieron inestables con MatterSim y MACE en toda la rejilla."
objetivo: "Comprobar, con materiales nuevos, si el armónico en V_exp con MatterSim da S y Cv desde fonones a ±10 % (MARE ≤ 5 %) de NIST-JANAF; y decidir con DFT (GPAW, CPU) si las inestabilidades de rutilo y cuarzo-α son un artefacto del potencial."
datos_clave:
  materiales:
    estudio: [AlN, SiC, KF, NaBr, KI, LiCl, CsCl, SrF2, BaF2, Na2O, ZrO2, BeAl2O4, MgTiO3, ZrSiO4]
    n: 14
    estructuras: "AlN wurtzita; SiC 3C (β); KF, NaBr, KI, LiCl tipo NaCl; CsCl tipo B2; SrF2, BaF2 fluorita; Na2O antifluorita; ZrO2 baddeleyita P2_1/c (COD 9016714); BeAl2O4 crisoberilo Pnma (COD 2100925); MgTiO3 geikielita R-3 (COD 9011261, celda primitiva); ZrSiO4 circón I4_1/amd (COD 9005518, celda primitiva)"
    disjuncion: "Ninguno está en C-MAT-001, -002, -003 ni -004 (ni en sus pruebas de humo)."
    excluidos_a_priori: "Mg2SiO4 (S298 de Robie y Hemingway difiere 1.09 % de JANAF, > 1 %); MgCl2 (fuentes de volumen discrepan ~3 %; capas con van der Waals); K2O (JANAF sin datos por debajo de 298 K); diamante (sin tabla JANAF); SnO2 (tipo rutilo, se mezclaría con la pregunta de artefacto)."
    controles_C1: "Si y MgO (de C-MAT-004), solo para regresión de código; no cuentan en ningún criterio."
    avisos_a_priori: "LiCl, KF, NaBr, KI, CsCl: haluros blandos y algo anarmónicos a 600 K; CsCl tiene transición B2→B1 a 743 K (fuera del rango); ZrO2 monoclínica de baja simetría; Cv armónica < Cp experimental por construcción (Cp − Cv = α²BVT, ~1–3 % a 298 K, más a 600 K), y S(600 K) en V_exp(298 K) ignora la expansión térmica entre 298 y 600 K."
  referencias_termicas: "refs/refs_termo_C-MAT-005.json: Cp y S de NIST-JANAF (14 tablas) a 100, 200, 298.15 y 600 K. Verificación de S298 con Robie y Hemingway 1995 (https://doi.org/10.3133/b2131) para Na2O, ZrO2, BeAl2O4, MgTiO3 y ZrSiO4, y con las tablas NBS de Wagman et al. 1982 (J. Phys. Chem. Ref. Data 11, supl. 2; leídas por OCR) para los otros 9. Desviación máxima 0.34 % (Na2O). Aviso: NBS 1982 y JANAF no son del todo independientes (ambas evaluaciones NBS/NIST)."
  referencias_volumen: "refs/vexp_C-MAT-005.json: V_exp a ~298 K por fórmula. Principal con DOI: Robie y Hemingway 1995 (5 minerales), NBS Circular 539 (Swanson et al. 1953–1955; DOI 10.6028/NBS.CIRC.539v1, v2, v3 y v5) para KF, NaBr, KI, LiCl, CsCl, SrF2 y BaF2, https://doi.org/10.3390/ma15186229 para SiC y https://doi.org/10.1007/BF01328124 para AlN. Verificación con una segunda medida experimental (COD con DOI o valor tabulado con su cita original; kX convertidos a Å): desviación máxima 0.55 % (Na2O), umbral 0.6 %."
  potenciales:
    principal: "MatterSim v1.0.0-5M, dtype=float64 (mattersim 1.2.5), CPU"
    linea_base: "MACE-MP-0 medium, default_dtype=float64 (mace-torch 0.3.16), CPU"
    excluido: "SevenNet-0 (no corre en float64; igual que en C-MAT-004)"
  protocolo:
    relajacion_V0: "FixSymmetry + FrechetCellFilter + BFGS, fmax 1e-3 eV/Å"
    celda_Vexp: "escalado isótropo de la celda relajada hasta V_exp (forma de celda del potencial) y relajación de posiciones con FixSymmetry"
    fonones: "Phonopy 4.8.3, 0.01 Å, malla 60 Å, exclude_gamma_acoustic=True, sin NAC. Superceldas base: 2×2×2 (convencional cúbica, o primitiva en MgTiO3 y ZrSiO4; ZrO2 2×2×2), CsCl 4×4×4, AlN 3×3×2, BeAl2O4 1×2×2. Grandes (solo en V_exp, para C3): 3×3×3, CsCl 5×5×5, AlN 4×4×3, BeAl2O4 2×2×3."
    magnitudes: "S(T) y Cv(T) armónicas en V0 y en V_exp, a 100, 200, 298.15 y 600 K, por mol de fórmula. Sin QHA (no hay rejilla de volúmenes; si en el futuro se usa QHA, la rejilla empezaría en 0.90)."
    determinismo: "float64, torch.use_deterministic_algorithms(True), 4 hilos, semillas fijas, redondeo a 10 cifras significativas; dos ejecuciones completas (run1, run2)."
  prueba_artefacto:
    materiales: "TiO2 rutilo (COD 9007531, Baur y Khan 1971, https://doi.org/10.1107/S0567740871005466) y SiO2 cuarzo-α (COD 9013321, https://doi.org/10.3749/canmin.46.5.1501), en la celda experimental de esos CIF (a, c fijos)."
    dft: "GPAW 25.1.0 (ondas planas, PAW de gpaw-data), 500 eV, FermiDirac 0.01 eV, convergencia de densidad 1e-6 y de fuerzas 1e-4 eV/Å. Posiciones relajadas con FixSymmetry + BFGS (fmax 2e-3 eV/Å) en la celda primitiva con k 4×4×6 (rutilo) y 3×3×3 (cuarzo). Fonones Phonopy 0.01 Å en supercelda 2×2×1 (k 2×2×6 y 2×2×3). Funcional principal PBE (el de entrenamiento de los uMLIP); LDA como secundario."
    mlip: "MatterSim y MACE en la misma celda experimental, con posiciones relajadas por cada potencial; fonones en la misma supercelda 2×2×1 y, como descriptivo, en la supercelda base de C-MAT-004 (2×2×3 rutilo, 2×2×2 cuarzo) con el q del mínimo."
    magnitud: "f_min,conm = frecuencia mínima en los q conmensurados de la supercelda 2×2×1 (Γ, (½,0,0), (0,½,0), (½,½,0)), sin interpolación."
    clasificacion: "Para cada potencial: A = artefacto del potencial si f_min,conm(uMLIP) < −0.3 THz y f_min,conm(PBE) ≥ −0.3 THz; B = heredada de PBE si ambos < −0.3 THz (B1 si LDA ≥ −0.3 THz, B2 si no o sin dato); C = no reproducida en q conmensurados si f_min,conm(uMLIP) ≥ −0.3 THz; INCONCLUSA_DFT si falla C-DFT1 o C-DFT2 o falta el cálculo PBE."
  hipotesis:
    H1: "PRINCIPAL. MatterSim armónico en V_exp: |S(298.15) − S_JANAF|/S_JANAF ≤ 0.10 en ≥ 12 de 14. Un material no evaluable (f_min < −0.3 THz en V_exp) o inconcluso por C3 cuenta como fallo."
    H2: "MatterSim armónico en V_exp: MARE de S(298.15) ≤ 0.05 (sobre los evaluables; INCONCLUSA si hay menos de 12)."
    H3: "MatterSim: MARE S298 en V_exp < MARE S298 en V0 (intersección de evaluables en ambas celdas; INCONCLUSA si n < 12)."
    H4: "MARE S298 en V_exp de MatterSim ≤ 0.6 × la de MACE (intersección de evaluables; INCONCLUSA si n < 12)."
    H5: "MatterSim en V_exp: MARE de Cv(298.15) frente a Cp_JANAF(298.15) ≤ 0.05 (INCONCLUSA si n < 12)."
    H6: "MatterSim en V_exp: MARE de S(600 K) ≤ 0.05 (INCONCLUSA si n < 12)."
    H7: "Sin sesgo sistemático: |mediana del error con signo de S298 de MatterSim en V_exp| ≤ 0.03 (INCONCLUSA si n < 12)."
    H-REP: "Réplica con tolerancia numérica fijada a priori: para los dos potenciales y los 16 materiales (14 + Si, MgO), |X_run1 − X_run2|/|X_run1| ≤ 1e-6 para S y Cv a las 4 T en V0, V_exp y supercelda grande; la clase de estabilidad (f_min ≥ −0.3 THz) igual; y los veredictos de H1–H7 iguales al evaluar run2. La identidad byte a byte se informa, sin veredicto."
    H-D1: "Rutilo: la inestabilidad de MatterSim es un artefacto del potencial. CONFIRMADA si la clase de MatterSim es A; REFUTADA si es B1 o B2; INCONCLUSA si es C o INCONCLUSA_DFT. MACE: solo descriptivo."
    H-D2: "Cuarzo-α: igual que H-D1."
  controles:
    C1_regresion: "MatterSim y MACE en Si y MgO: S298 armónica en V_exp dentro de ±1e-4 (relativo) de C-MAT-004 run1 (arm_Vexp)."
    C2_normalizacion: "Cv(3000 K)/(3R·n_at_prim) en V_exp entre 0.99 y 1.000001 para todos los materiales evaluables."
    C3_convergencia: "|S298 en V_exp con supercelda grande − base|/base ≤ 0.02; si no, el material es INCONCLUSO (fallo en H1, fuera de las MARE)."
    C-DFT1: "PBE, celda primitiva: frecuencias de Γ con 500 y 650 eV difieren ≤ 0.15 THz en todos los modos."
    C-DFT2: "Relajación DFT PBE convergida (fmax ≤ 2e-3 eV/Å)."
  reglas_de_evaluacion:
    - "Estabilidad: evaluable si f_min ≥ −0.3 THz en la malla de la supercelda base de esa celda."
    - "Las MARE se calculan solo sobre materiales evaluables y no inconclusos; las comparaciones entre celdas o potenciales usan la intersección."
    - "Resultados a 100 y 200 K, en V0 (salvo H3), de MACE (salvo H4) y los mínimos interpolados de la prueba de artefacto: solo descriptivos."
    - "Si el cálculo LDA no termina, se informa como sin dato (B2 por defecto si PBE es inestable); no cambia H-D1/H-D2 salvo para distinguir B1 de B2."
sesgos_declarados:
  - "V_exp es un dato de entrada: el método no predice el volumen."
  - "Cv armónica frente a Cp experimental: sesgo negativo esperado de ~1–3 % a 298 K y mayor a 600 K."
  - "S(600 K) en V_exp(298 K): sesgo negativo esperado por no incluir la expansión térmica."
  - "Escalado isótropo en no cúbicos; sin NAC; sin anarmonicidad."
  - "DFT en supercelda 2×2×1: solo explora 4 q conmensurados; una inestabilidad en otro q queda como clase C."
riesgos:
  - "n = 14: calibración por recuento, no estadística fina."
  - "Haluros alcalinos pesados (KI, CsCl) y ZrO2 pueden ser difíciles para los uMLIP."
  - "La DFT en CPU puede tardar horas; si no termina, H-D1/H-D2 quedan INCONCLUSAS."
decisiones:
  - "Criterios fijados antes de calcular; cualquier cambio posterior es una desviación declarada y no cambia el veredicto original."
  - "Nueva fila UM-16 (C-MAT-005): E2 si se ejecuta con procedencia; E3 solo si H1, H2 y H-REP pasan y C1 y C2 se cumplen."
  - "UM-07 sigue en E1 mientras falten E_form, fases competidoras e incertidumbre."
proximo_paso: "Congelar prereg y código (sha256), prueba de humo solo con Ge, Cu y Si (fuera del estudio), y ejecutar run1 y run2 en segundo plano junto con la DFT."
---
