---
meta:
  id: C-MAT-002
  titulo: "Termodinámica armónica (Phonopy) frente a NIST-JANAF y réplica del flujo de fonones con tres calculadores para Si"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
  fecha_congelacion: "2026-10-19 (UTC+2), antes de cualquier cálculo de fonones o propiedades térmicas"
  afirmaciones_registro: [UM-07, UM-10]
  estado: congelado
objetivo: "UM-07: añadir y verificar el paso 'propiedad térmica' del flujo MV1 (Cv, S) frente a datos experimentales evaluados. UM-10: demostrar que el mismo flujo corre sin cambios con calculadores independientes (uMLIP y potenciales empíricos) y cuantificar la dispersión entre modelos."
datos_clave:
  referencias_experimentales:
    fuente: "NIST-JANAF Thermochemical Tables (Chase 1998), tablas descargadas 2026-10-19"
    Si: {url: "https://janaf.nist.gov/tables/Si-001.txt", Cp: {T100: 7.268, T200: 15.636, T298.15: 20.000}, S: {T100: 3.833, T200: 11.665, T298.15: 18.820}}
    MgO: {url: "https://janaf.nist.gov/tables/Mg-008.txt", Cp: {T100: 7.802, T200: 26.681, T298.15: 37.106}, S: {T100: 2.548, T200: 14.096, T298.15: 26.924}}
    NaCl: {url: "https://janaf.nist.gov/tables/Cl-053.txt", Cp: {T100: 34.932, T200: 46.873, T298.15: 50.509}, S: {T100: 23.723, T200: 52.605, T298.15: 72.115}}
    unidades: "J/(K·mol de fórmula)"
    Si_TO_Gamma: "520.2 cm-1 = 15.595 THz (Parker, Feldman, Ashkin, Phys. Rev. 155, 712, 1967; ya usada en C-MAT-001)"
  sesgo_declarado: "Se compara Cv armónico con Cp experimental (Cp−Cv ≥ 0, ~1–3 % a 298 K) y S armónica a volumen de 0 K con S experimental (sin expansión térmica ni anarmonicidad). Ambos sesgos hacen que el modelo tienda a quedar POR DEBAJO del experimento."
  calculadores:
    - "MACE-MP-0 medium (mace-torch 0.3.16, float64, CPU), mismo checkpoint que C-MAT-001"
    - "Stillinger–Weber, PRB 31, 5262 (1985), parámetros Stillinger_Weber_PRB_31_5262_Si de matscipy 1.3.1"
    - "Kumagai et al., Comput. Mater. Sci. 39, 457 (2007), parámetros Kumagai_Comp_Mat_Sci_39_Si de matscipy 1.3.1"
  protocolo:
    estructuras_iniciales: "las de C-MAT-001 (Si a=5.431, MgO a=4.212, NaCl a=5.640, celdas cúbicas convencionales)"
    relajacion: "FixSymmetry + FrechetCellFilter + BFGS, fmax 1e-3 eV/Å (igual que C-MAT-001)"
    fonones: "Phonopy 4.8.3, desplazamientos finitos 0.01 Å, supercelda 2×2×2 (base) y 3×3×3 (convergencia), malla 20×20×20 centrada en Γ, sin NAC"
    termicas: "phonopy run_thermal_properties a T = 100, 200, 298.15 K; normalización a mol de fórmula usando Cv(3000 K)/(3R) = átomos por celda de referencia de phonopy"
    tolerancia_estabilidad: "fmin ≥ −0.3 THz (como C-MAT-001)"
  predicciones_a_priori:
    fuente: "estimación de ablandamiento uniforme ΔS ≈ −3nR·ln(ω_MACE/ω_exp) con el error TO-Γ de C-MAT-001"
    Si: {ratio_TO: 0.7171, dS_pred: 8.29}
    MgO: {ratio_TO: 0.8399, dS_pred: 8.70}
    NaCl: "no evaluable (referencia TO solo secundaria en C-MAT-001)"
    literatura: "MACE-MP-0 sobreestima S y Cv frente a PBE (Loew et al., npj Comput. Mater. 2025, https://www.nature.com/articles/s41524-025-01650-1); SW original sobreestima TO-Γ de Si (~595 vs 518 cm-1, https://utw10370.utweb.utexas.edu/publications/P116.pdf)"
tareas:
  hipotesis:
    H-TH-1: "MACE: |S(298.15) − S_JANAF|/S_JANAF ≤ 0.10 para Si, MgO y NaCl (los tres). Si falla uno → FALSADA."
    H-TH-2: "MACE: S(298.15) − S_JANAF > 0 en los tres materiales (firma del ablandamiento pese a los sesgos declarados que empujan en sentido contrario)."
    H-TH-3: "MACE: |error relativo de Cv(100 K) frente a Cp_JANAF(100 K)| > |error relativo a 298.15 K| en los tres materiales."
    H-TH-4: "MACE, Si y MgO: el cociente ΔS_obs/ΔS_pred (ΔS_pred de arriba) está en [0.5, 1.5] en ambos."
    H-X-1: "Si con los tres calculadores: relajación convergida y estable (fmin ≥ −0.3 THz) en 2×2×2 y 3×3×3."
    H-X-2: "Al menos uno de los dos potenciales empíricos (SW, Kumagai) cumple a la vez |error S(298.15)| ≤ 0.10 y |error TO-Γ| ≤ 0.10 frente a 15.595 THz."
    H-X-3: "S_JANAF(298.15) de Si queda dentro del intervalo [mín, máx] de S(298.15) de los tres calculadores (horquillado)."
    H-X-4: "Reproducibilidad: una segunda ejecución completa produce results_core.json idéntico byte a byte."
  convergencia: "Si |S_3×3×3 − S_2×2×2|/S_2×2×2 > 0.02 a 298.15 K en un material/calculador, sus hipótesis se marcan INCONCLUSAS. Las hipótesis se evalúan con 3×3×3."
riesgos:
  - "n = 3 materiales: es calibración, no estadística."
  - "Cp vs Cv y S armónica vs real: sesgos de 1–5 % declarados arriba."
  - "Los potenciales empíricos solo existen para Si en este entorno; UM-10 se demuestra solo en Si."
decisiones:
  - "Criterios fijados antes de ejecutar; cualquier cambio posterior se declarará como desviación y no cambiará el veredicto original."
  - "Niveles: UM-07 y UM-10 suben a E2 si el cálculo se ejecuta con procedencia; E3 solo si TODAS sus hipótesis pasan y H-X-4 pasa."
proximo_paso: "Ejecutar code/cmat002_run.py dos veces y evaluar con code/cmat002_eval.py."
---
