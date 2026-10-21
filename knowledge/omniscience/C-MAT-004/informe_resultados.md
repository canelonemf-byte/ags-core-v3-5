---
meta:
  id: C-MAT-004
  fecha: "2026-10-19 (UTC+2)"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
  prereg_sha256: 160ce4b26fe555375174bd01c416e3ffe1e534c5ec43aaad5d211b6055af2363
  cronologia: "refs 11:05 · humo solo con Ge y Cu 11:05 · prereg congelado 11:06:48 · script de evaluación 11:07:32 · code_freeze 11:07:43 · primer resultado del estudio 11:08:04 · run2 MACE terminó 11:51:48 · evaluación 11:52 (hashes verificados, sin cambios)"
  afirmaciones: [UM-07, UM-14, UM-15]
objetivo: "Comprobar si fijar el volumen con el V_exp estructural (presión empírica P_corr antes de la QHA, float64) lleva S y Cp desde fonones a ±10 % (MARE ≤ 5 %) de NIST-JANAF en 17 sólidos (11 anclas + 6 nuevos de validación)."
datos_clave:
  materiales: "Anclas: Si, MgO, NaCl, LiF, NaF, KCl, KBr, CaO, CaF2, Al2O3, BeO. Validación nueva: SrO, MgF2, TiO2 rutilo, SiO2 cuarzo-α, Li2O, MgAl2O4 (n = 17)."
  potenciales: "MatterSim v1.0.0-5M (principal) y MACE-MP-0 medium (línea base), ambos float64 en CPU. SevenNet-0 excluido antes de calcular (no corre en float64), tal como fija el prereg."
  protocolo: "Phonopy 4.8.3, 14 volúmenes V/V_exp 0.94–1.20, EOS Vinet, P_corr por bisección hasta V(298.15 K) = V_exp. Dos ejecuciones completas (run1, run2)."
  tabla_MatterSim_pct: |
    | material | S298 JANAF (J/mol·K) | V0/V_exp | P_corr (GPa) | S298 arm V0 | S298 arm V_exp | S298 QHA corr | S600 corr | Cp298 corr | Cp600 corr | patología |
    |---|---|---|---|---|---|---|---|---|---|---|
    | Si | 18.820 | 1.021 | 2.47 | +3.1 | +1.8 | +2.0 | +0.8 | +0.6 | −1.9 | — |
    | MgO | 26.924 | 1.032 | 7.68 | +8.1 | +1.3 | +1.3 | +1.0 | +0.5 | +0.7 | — |
    | NaCl | 72.115 | 1.032 | 1.75 | +6.3 | +2.5 | +2.2 | +1.3 | −0.2 | −0.8 | — |
    | LiF | 35.660 | 1.032 | 4.85 | +9.7 | +3.8 | +4.0 | +2.9 | +1.8 | +1.6 | — |
    | NaF | 51.212 | 1.043 | 3.89 | +5.9 | −0.3 | −0.2 | +0.3 | +0.1 | +2.0 | — |
    | KCl | 82.554 | 1.038 | 1.60 | +6.9 | +1.7 | — | — | — | — | P4 V(T) no monótono |
    | KBr | 95.939 | 1.048 | 1.16 | +10.5 | +6.3 | +7.6 | +3.6 | −3.7 | −9.5 | — |
    | CaO | 38.212 | 1.019 | 3.63 | +11.3 | +8.0 | +7.9 | +4.2 | +2.3 | −1.2 | — |
    | CaF2 | 68.572 | 1.026 | 4.01 | +6.1 | +1.5 | +1.5 | +0.2 | −1.8 | −0.4 | — |
    | Al2O3 | 50.950 | 1.029 | 9.98 | +8.4 | +2.2 | +2.2 | +1.1 | +0.8 | −0.3 | — |
    | BeO | 13.770 | 1.013 | 6.22 | +5.4 | +3.0 | +3.1 | +1.1 | +1.0 | −0.8 | — |
    | SrO | 55.522 | 1.029 | 3.70 | +4.6 | +0.9 | +0.8 | +0.3 | +1.1 | −2.5 | — |
    | MgF2 | 57.255 | 1.050 | 6.62 | +3.7 | −1.5 | — | — | — | — | P3 V(T) fuera de la rejilla (0.98 inestable) |
    | TiO2 | 50.292 | 1.029 | — | NE | NE | — | — | — | — | P2 inestable en los 14 volúmenes (fmin −1.5…−8.6 THz) |
    | SiO2 | 41.463 | 1.068 | — | NE | NE | — | — | — | — | P2 inestable en los 14 volúmenes (fmin −0.6…−1.8 THz) |
    | Li2O | 37.890 | 1.015 | 3.62 | +0.6 | −2.0 | −2.0 | −1.8 | −1.1 | −2.5 | — |
    | MgAl2O4 | 88.692 | 1.033 | 8.59 | −2.2 | −7.2 | −7.1 | −3.2 | +0.1 | +0.5 | — |
  tabla_MACE_S298_pct: "arm V0 / QHA corr (P_corr GPa): Si +27.8/+27.1 (1.88) · MgO +22.2/+14.7 · NaCl +5.1/+2.2 · LiF +20.1/+9.7 · NaF +10.4/+7.4 · KCl +4.3/+0.9 · KBr +5.3/+1.3 · CaO +17.7/+15.7 · CaF2 +10.4/+6.0 · Al2O3 +13.1/+8.0 · BeO +18.0/+13.4 · SrO +9.7/+6.7 · MgF2 +7.2/+3.1 · TiO2 NE/P2 · SiO2 +9.8/P2 · Li2O +15.7/+10.5 · MgAl2O4 +5.9/+0.1. Patológicos MACE: TiO2, SiO2 (P2)."
  NE: "NE = no evaluable (fmin < −0.3 THz en esa celda)."
tareas:
  veredictos_criterios_originales:
    H-V1: "FALSADA. MatterSim QHA corregida dentro de ±10 % en 13 de 17; se pedían ≥ 15. Los 13 evaluables están todos dentro; los 4 patológicos (KCl, MgF2, TiO2, SiO2) cuentan como fallo según el prereg."
    H-V2: "INCONCLUSA. MARE S298 = 3.23 % (≤ 5 %), pero con 13 evaluables < 14 exigidos."
    H-V3: "FALSADA (validación limpia). 3 de 6 dentro de ±10 % (SrO, Li2O, MgAl2O4); se pedían ≥ 5. MgF2, TiO2 y SiO2 patológicos. MARE descriptiva 3.32 % con n = 3."
    H-V4: "INCONCLUSA. MARE S600 = 1.67 % (≤ 5 %), n = 13 < 14."
    H-V5: "INCONCLUSA. MARE Cp_suave 1.15 % a 298 K y 1.89 % a 600 K (≤ 5 %), n = 13 < 14."
    H-V6: "INCONCLUSA. MACE pasa (8.45 % corr < 12.87 % arm V0, n = 15). MatterSim n = 13 < 14 (descriptivo: 3.23 % < 6.32 %)."
    H-V7: "PASA. MatterSim armónico en V_exp: MARE S298 = 2.94 % (≤ 5 %), n = 15 (TiO2 y SiO2 no evaluables). Repite como prueba pre-registrada el exploratorio de C-MAT-003 (3.0 %)."
    H-V8: "INCONCLUSA. n = 13 < 14 en la intersección. Descriptivo: MACE 9.45 % frente a MatterSim 3.23 % (cociente 2.93; se pedía ≥ 1.5)."
    H-REP: "FALSADA. MatterSim: results_core idénticos byte a byte (sha256 e84ee5f8…). MACE: 16 de 17 materiales idénticos; Si difiere en 64 campos (modos acústicos de Γ ~1e-7 THz y derivados; diferencia relativa máx. en campos no nulos 3.9e-6). Los 9 veredictos son iguales al evaluar run2 (results_replica_run2.json)."
  controles:
    C1: "PASA. MACE armónico en V0 reproduce C-MAT-003 en las 11 anclas (|desviación| ≤ 1.0e-8)."
    C2: "P_corr > 0 en todos los materiales con QHA (MatterSim 1.16–9.98 GPa; MACE 1.32–9.42 GPa): los dos potenciales subenlazan (V0/V_exp 1.013–1.073). Sin veredicto."
    C3: "FALLA. TiO2 en ambos potenciales (Cv(3000 K)/3R·n = 0.945 MatterSim, 0.958 MACE) por sus modos imaginarios. Los otros 16 dentro de [0.99, 1.000001]."
    C4: "Sin incidencias: |ΔS298| supercelda grande frente a base ≤ 1.25 % (MatterSim) y ≤ 1.56 % (MACE), máximo en MgAl2O4; ninguno inconcluso."
    C5_P6: "Sin incidencias: |V(298.15)/V_exp − 1| ≤ 9.4e-7 en todos los materiales con P_corr (umbral 1e-4)."
    C_PAT: "FALLA. MatterSim patológico en 4 de 17 (> 2): se declara que el protocolo QHA no es robusto. Los veredictos no cambian."
  desviaciones: "Ninguna. Código, rejilla, EOS, intervalo y criterios sin cambios tras ver resultados (hashes verificados frente a code_freeze.json al evaluar). Notas de interpretación, sin efecto en los veredictos: N1, el mínimo de 14 evaluables se aplicó también a H-V7 por analogía con la regla de tratamiento (con n = 15 no cambia nada); N2, en H-V3 el recuento ya falla, así que la MARE inconclusa no altera el veredicto; N3, el script de evaluación se escribió 44 s después de congelar el prereg y antes de cualquier cálculo del estudio; N4, la interrupción del trabajador anterior no afectó a los cálculos (el proceso de fondo terminó run2 MACE sin relanzarse)."
  lectura: "En los 13 materiales donde la QHA corregida es estable, MatterSim queda a ±10 % en todos y la MARE de S298 baja de 6.3 % (armónico V0) a 3.2 %. Pero el efecto viene casi entero del volumen: en MatterSim, la QHA corregida y el armónico en V_exp difieren ≤ 1.3 puntos (MACE ≤ 3.2). El protocolo falla por robustez (4 patológicos), sobre todo en la validación nueva: rutilo y cuarzo-α salen dinámicamente inestables en toda la rejilla con los dos potenciales (en rutilo el modo blando es conocido en cálculos; en cuarzo era un aviso a priori) y MgF2 se sale del intervalo de volúmenes a baja T. KBr Cp600 (−9.5 %) es el peor Cp. MACE sigue sobreestimando S298 en 15 de 15 incluso en V_exp (+0.5…+26 %): su error no es solo de volumen."
originalidad: "Baja. La corrección empírica por presión constante ('pshift') antes de la QHA está publicada para DFT (Otero-de-la-Roza y Luaña 2011, https://doi.org/10.1103/PhysRevB.84.184103) y la sensibilidad al volumen de los uMLIP ya se ha descrito (https://doi.org/10.1016/j.commatsci.2025.113770 ; https://doi.org/10.1038/s41524-025-01650-1). Lo propio es solo la prueba pre-registrada con uMLIP, float64, validación nueva y fallos declarados. Texto, código y figura son propios; las fuentes se citan por DOI o URL."
riesgos:
  - "n = 17 (6 de validación, solo 3 evaluables): calibración por recuento."
  - "P_corr absorbe errores del potencial, punto cero y expansión 0–298 K; con V_exp como dato de entrada no es una predicción ab initio del volumen."
  - "Sin NAC ni anarmonicidad explícita; escalado isótropo en no cúbicos."
decisiones:
  - "UM-15 (C-MAT-004) entra en E2. No E3: H-V1 y H-V3 falsadas, H-V2 inconclusa, H-REP falsada y C3 falla."
  - "UM-14 sigue en E2; UM-07 sigue en E1 (faltan E_form, fases competidoras e incertidumbre)."
proximo_paso: "Prereg C-MAT-005: (1) armónico en V_exp como método principal (es lo que funciona: H-V7) con un conjunto nuevo ≥ 12 sólidos sin modos blandos conocidos; (2) para rutilo y cuarzo, comprobar antes con DFT (PBEsol) o MatterSim afinado si la inestabilidad es del potencial; (3) rejilla de volumen que empiece en 0.90 para que V(T) a baja T no se salga; (4) investigar la no determinación de MACE en Si (modos acústicos de Γ) o fijar el criterio de réplica a una tolerancia numérica declarada a priori."
archivos: "prereg_C-MAT-004.md/.FROZEN.md/.sha256, code_freeze.json, code/ (cmat004_run.py, cmat004_eval.py, run_all.sh congelados; diff_runs.py y cmat004_fig.py posteriores, descriptivos), refs/, out/run1, out/run2, results.json, results_replica_run2.json, diff_runs.json, provenance_C-MAT-004.json, figs/fig_S298_err_JANAF.png, logs/."
---
