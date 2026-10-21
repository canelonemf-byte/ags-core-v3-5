---
meta:
  id: C-MAT-003
  fecha: "2026-10-19 (UTC+2)"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
  prereg_sha256: 2d9a125647b675531cdfaa5508687b2b8032ffe78ccce4eb6410f4619b9dfc96
  cronologia: "prereg congelado 09:31:06 · prueba de humo solo con Ge y Cu · hashes de código y checkpoints 09:35:21 · run1 09:35:28 · run2 hasta 09:58:39 · evaluación 09:56–10:00 · exploratorio 09:57–10:02"
  afirmaciones: [UM-07, UM-10, UM-13, UM-14]
objetivo: "Comprobar si MatterSim (potencial universal más reciente) y la corrección cuasiarmónica (Phonopy QHA) llevan S y Cp calculadas desde fonones a ±10 % de NIST-JANAF en 11 sólidos, con MACE-MP-0 como línea base y SevenNet-0 como segundo potencial."
datos_clave:
  materiales: "Si, MgO, NaCl (anclas) + LiF, NaF, KCl, KBr, CaO, CaF2, Al2O3, BeO (n = 11). Referencias JANAF verificadas con una segunda fuente (desviación de S298 ≤ 0.56 %)."
  potenciales: "MatterSim v1.0.0-5M (principal), SevenNet-0 (7net-0, 11-jul-2024), MACE-MP-0 medium (línea base). Phonopy 4.8.3, 0.01 Å, superceldas 2×2×2 (cúbicos y Al2O3) y 3×3×2 (BeO), 10 volúmenes QHA (V/V0 0.96–1.14), EOS Vinet."
  tabla_error_S298_pct: |
    | material | S298 JANAF | MatterSim arm | MatterSim QHA | SevenNet arm | MACE arm | MatterSim arm celda de partida (exploratorio) |
    |---|---|---|---|---|---|---|
    | Si | 18.820 | +3.1 | +3.7 | +12.2 | +27.8 | +1.8 |
    | MgO | 26.924 | +8.1 | +12.1 | +20.4 | +22.2 | +1.3 |
    | NaCl | 72.115 | +6.3 | +10.4 | +4.6 | +5.1 | +2.5 |
    | LiF | 35.660 | +9.7 | +18.3 | +25.0 | +20.1 | +3.8 |
    | NaF | 51.212 | +5.9 | +12.1 | +8.1 | +10.4 | −0.3 |
    | KCl | 82.554 | +6.9 | +17.3 | +18.3 | +4.3 | +1.7 |
    | KBr | 95.939 | +10.5 | +11.2 | +9.9 | +5.3 | +6.3 |
    | CaO | 38.212 | +11.3 | +14.2 | +15.2 | +17.7 | +8.1 |
    | CaF2 | 68.572 | +6.1 | +11.1 | +13.0 | +10.4 | +1.6 |
    | Al2O3 | 50.950 | +8.4 | +11.3 | +12.9 | +13.1 | +2.1 |
    | BeO | 13.770 | +5.4 | +8.5 | +15.1 | +18.0 | +3.1 |
  MARE_S: {MatterSim_arm: {T298: 0.074, T600: 0.028}, MatterSim_QHA: {T298: 0.118}, SevenNet_arm: {T298: 0.141, T600: 0.068}, MACE_arm: {T298: 0.140, T600: 0.067}}
  controles: "C1 PASA (MACE reproduce C-MAT-002: Si −0.15 %, MgO −0.23 %, NaCl −0.05 %). C2: 1 fallo (SevenNet KCl). C3 PASA. C4 y C5 sin incidencias (ningún material inconcluso ni inestable). C6: sin horquilla de volumen a 600 K en MatterSim NaCl, SevenNet KBr y MACE NaF (el mínimo de F(V) se sale del intervalo 0.96–1.14)."
tareas:
  veredictos_criterios_originales:
    H-Q1: "FALSADA. MatterSim + QHA dentro de ±10 % en 2 de 11 (Si, BeO); se pedían ≥ 9."
    H-Q2: "FALSADA. MARE de S298 con MatterSim + QHA = 11.8 % (umbral 5 %)."
    H-Q3: "FALSADA por poco. MARE armónica MatterSim 7.42 % frente a 0.5 × 14.05 % = 7.02 % de MACE (reduce el error un 47 %, no un 50 %)."
    H-Q4: "FALSADA. A 600 K la QHA empeora la entropía de MatterSim: MARE 8.2 % frente a 2.9 % armónica (n = 10)."
    H-Q5: "FALSADA. MARE de Cp_QHA(600 K) 8.1 % frente a 5.9 % de Cv armónica (n = 10)."
    H-Q6: "FALSADA. SevenNet-0 14.08 % frente a MACE 14.05 %: sin mejora."
    H-Q7: "PASA. MACE-MP-0 armónico sobreestima S298 en 11 de 11 (+4.3…+27.8 %)."
    H-REP: "FALSADA. Ningún potencial dio results_core idénticos byte a byte (diferencia relativa máxima en S armónica: MatterSim 1.3e-4, SevenNet 1.1e-4, MACE 0; en MACE solo difieren, en Si, los modos acústicos de Γ y Cp_QHA). Los 8 veredictos salen iguales al evaluar run2 (results_replica_run2.json)."
riesgos:
  - "D1 (código, sin cambio de criterios): cmat003_eval.py v1.0 fallaba cuando aún faltaba un material en run2; v1.1 solo corrige ese caso. La v1.0 congelada se conserva (sha256 2674af40…)."
  - "D2 (interpretación declarada): las reglas R1–R3 del script de evaluación (inestabilidad en V0, intersección de materiales y horquilla a 600 K) se escribieron antes de ver resultados del estudio, pero no aparecen literalmente en el prereg. En este caso ninguna cambió nada, porque no hubo materiales inestables ni inconclusos."
  - "D3 (detectado después): el prereg no fijó la precisión numérica. MatterSim y SevenNet corren en float32, y eso basta para meter ruido en E(V). Hay QHA patológicas: α_V negativo en MatterSim KBr, V(T) disparado en SevenNet KBr y MACE NaF. Las diferencias de hasta un 6 % entre ejecuciones vienen de esos casos."
  - "D4 (instrumento): Cp_QHA, que phonopy calcula como derivada segunda numérica con paso de 1 K, cambia hasta un 46 % entre ejecuciones en casos sueltos (MACE Si a 600 K). La MARE de H-Q5 solo varía un 1 % (8.09 frente a 8.17 %) y el veredicto se mantiene, pero Cp_QHA por material no es fiable."
  - "Exploratorio NO pre-registrado (sin valor probatorio): los potenciales relajan volúmenes entre un 1.3 y un 4.8 % mayores que las celdas de partida (parámetros de red experimentales aproximados, a temperatura ambiente y sin verificar). En esas celdas, la MARE armónica de S298 baja de 7.4 a 3.0 % con MatterSim (11 de 11 dentro de ±10 %) y de 14.1 a 9.7 % con MACE. Esto apunta a que buena parte del exceso de entropía viene de un volumen de equilibrio demasiado grande (subenlace de tipo PBE), y a que la QHA lo agrava porque expande todavía más."
  - "n = 11 sin metales ni materiales anarmónicos fuertes; JANAF por debajo de 298 K se basa en calorimetría antigua."
decisiones:
  - "Nueva fila UM-14 (C-MAT-003): E2. No llega a E3 porque H-Q1, H-Q2 y H-REP fallan."
  - "UM-10 se queda en E2. El mismo flujo corrió sin cambios con 3 potenciales universales en 11 materiales, pero la regla de E3 exigía H-REP para los tres, y H-REP falla."
  - "UM-07 se queda en E1 (faltan E_form, fases competidoras e incertidumbre). El paso cuasiarmónico ya está implementado y probado, y en este régimen empeora el resultado."
  - "UM-13 se queda en E2. H-Q7 confirma en 11 materiales el sesgo positivo de MACE que vio C-MAT-002."
  - "Originalidad: ya conocido. Fromsejer et al. 2025 (https://doi.org/10.1016/j.commatsci.2025.113770) compararon armónico, QHA y MLIP con datos experimentales (JANAF/NBS) en hasta 784 compuestos, y vieron que la armónica rinde como la QHA hasta temperaturas moderadas. Loew et al. 2025 (https://doi.org/10.1038/s41524-025-01650-1) ya situaban a MatterSim por delante de SevenNet-0 y MACE-MP-0 frente a PBE. La sobreexpansión térmica de PBE con QHA en haluros alcalinos también es conocida. Aportación propia, solo en su alcance: una calibración pre-registrada, reproducible y con fallos declarados, frente al experimento y no frente a DFT."
proximo_paso: "Pre-registrar C-MAT-004: armónico y QHA con corrección de volumen fijada a priori (presión empírica que lleve V0 al volumen experimental de 0 K con referencias verificadas, o volumen experimental directo), float64 donde sea posible y Cp por ajuste suave en lugar de la derivada segunda numérica. Hipótesis: con esa corrección, MatterSim queda dentro de ±10 % en ≥ 9 de 11. Mismos 11 materiales y otros 6 nuevos como conjunto de validación."
---
