# C-MAT-006: resultados (2026-10-20, UTC+2)
autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
congelacion: "prereg sha256 33b60529bef1a813d7a3603acafc3cdc48c07da13d076973cdb0977139e919ba, 13:43:40 UTC+2; codigo congelado 13:44-13:48; primer calculo 13:45. Sin desviacion de congelacion."
hipotesis:
  H1: "PASA 29/31 dentro de ±10 % (umbral 26). Fuera: TiO2 (+11.0 %), KI (no evaluable, f_imag 0.032)"
  H2: "PASA MARE S298 MatterSim 2.69 % (n 30)"
  H3: "PASA MARE S600 1.76 % (n 30)"
  H4: "PASA MACE MARE 8.90 %; cociente 0.30 ≤ 0.6"
  H5: "PASA 3/4 con regla R3 (MgF2, SiO2, ZrO2 ok; TiO2 +11 %)"
  H6: "PASA 1 no evaluable (KI)"
  H-REP: "PASA run2 identico (max dif rel 0), f_imag y veredictos iguales"
  C1: "OK max 2.4e-6"
  C2: "OK max 2.3e-6"
  C-DFT1: "OK Γ 650 vs 800 eV max 0.089 THz"
  C-DFT2: "OK relax fmax 1.9e-4 eV/Å"
  H-D1: "INCONCLUSA (clase C): en la celda experimental fija MatterSim no da modos imaginarios en ningun q conmensurado 2×2×2 (ν_min ≈ 0 en Γ; en (½,0,½) 1.98 THz); MACE igual. La inestabilidad de C-MAT-004 no se reproduce en celda experimental, asi que la DFT ya no decide el veredicto. Supercelda PBE 2×2×2 aun en curso (descriptiva)."
  H-D2: "INCONCLUSA: cuarzo pendiente de la regla de factibilidad (rutilo no ha terminado); MatterSim y MACE sin modos imaginarios conmensurados."
nivel: "UM-19 E3 (H1, H2, H-REP y C1 cumplen la regla de la decision del prereg)"
desviaciones: "D1: script de evaluacion re-ejecutado manualmente tras terminar run2 (el finalizador lo repetira al acabar la DFT); no cambia veredictos."
figura: figs/err_S298.png
referencias: ["https://doi.org/10.18434/T42S31", "https://doi.org/10.1107/S0567740871005466"]
originalidad: "Regla R0-R4 y codigo propios; comparar entropias armonicas uMLIP con JANAF es practica conocida, la novedad es solo la regla prerregistrada y el benchmark concreto."
