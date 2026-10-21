# C-UMF-002: informe de resultados
autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
fecha: 2026-10-20 (UTC+2)
prereg: prereg_C-UMF-002.md, sha256 be01fb96…09fd (congelado 13:43:40, antes de cualquier cálculo). Código hasheado antes de ejecutar y evaluador hasheado antes de ver resultados (code_freeze.sha256).

## Resultados (MatterSim-v1.0.0-5M, 42 sólidos, run1 = run2)
| hip | resultado | veredicto |
|---|---|---|
| H-U1 (principal) | δ_Ti = +0.403 eV/Ti (solo TiN, Ti2O3). Errores en la prueba: rutilo −70, anatasa −121, MgTiO3 −29 meV/át | **FALLA** (anatasa > 100) |
| H-U2 | MAE de la prueba Ti: 73 con δ_Ti frente a 190 sin él (cociente 0.39) | **PASA** |
| H-U3 (principal) | MAE LOOCV de 37 compuestos sin Ti = 32.6 meV/át | **PASA** |
| H-U4 | máx. \|err\| 121 meV/át (anatasa) | **PASA** |
| H-U5 | MACE LOOCV 33.8 frente a 32.6 de MatterSim | **PASA** |
| H-U6 | MP2020 fijo con n = 34 compuestos de O, F, Cl y N: MAE 84.9 meV/át | **FALLA** (ver D1) |
| H-U7 | signo correcto en 5 de 6 reacciones (falla R5: anatasa sale 31 meV/át más estable que rutilo; JANAF dice −21) | **PASA** |
| H-U8 | MAE ΔrH 25.1 meV/át | **FALLA** (por 0.1) |
| H-U9 (principal) | E_hull del rutilo 30.8 meV/át (sobre la anatasa); los demás 0 | **FALLA** |
| H-REP | diferencia relativa máx. 2.2e-16; veredictos iguales | **PASA** |

Controles: C1 pasa (todas las relajaciones convergen). C2 (descriptivo): MgCl2 +11 %, CaI2 +16 %, MgBr2 +20 % de volumen, son capas con van der Waals. C3 pasa (29 compuestos idénticos a C-UMF-001, ≤2e-14).
MACE: mismo patrón (δ_Ti +0.400; anatasa −138; R5 también al revés).
δ_X ajustados a los 37 compuestos sin Ti (MatterSim): O −0.590, F −0.637, Cl −0.607, Br −0.396, I −0.235, N −0.366 eV.

## Desviaciones
- D1: el prereg dice n = 33 para H-U6, pero la definición (compuestos de O, F, Cl y N) da 34 (fue un error de recuento). Se evalúa con la definición, n = 34. El veredicto es sensible: quitando la anatasa, el MAE sería 77.8.
- Prueba de humo: no hubo.

## Lectura
Una δ_Ti de compuestos de entrenamiento independientes reduce el error de los óxidos de Ti a menos de la mitad, pero no lo arregla en la anatasa. El fallo de estabilidad (anatasa por debajo de rutilo) viene de PBE (es conocido) y una corrección por átomo no puede cambiarlo, porque se cancela entre polimorfos. E2.
figura: figs/fig_cumf002_paridad.png
