# C-UMF-001 — Informe de resultados

meta:
  campana: C-UMF-001
  fecha: 2026-10-20
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
  prereg_sha256: c646ab82ab875b036c0d06e97e8f9695f14ff7993309d96fc1e94358b27ab83a
  congelacion: "prereg 09:09:48 (UTC+2), código de ejecución hasheado y lanzado después; evaluador hasheado antes de ver ninguna entalpía"

## objetivo
Añadir E_form al flujo MV1 (UM-07) y comprobar si MatterSim-v1.0.0-5M y MACE-MP-0 dan ΔfH°(0 K) experimental (NIST-JANAF) en 29 sólidos iónicos: en bruto, con MP2020 fijo y con δ por anión reajustado (LOOCV).

## datos_clave
| hipótesis | criterio | resultado MatterSim | veredicto |
|---|---|---|---|
| H-F1 | bruto, óxidos: ≥12/14 positivos y media en [0.40, 1.00] eV/O | 14/14, +0.561 eV/O | PASA |
| H-F2 | MAE LOOCV ≤ 60 meV/át (n=27) | 45.9 | PASA |
| H-F3 | máx. LOOCV ≤ 150 meV/át | 194.8 (TiO2) | FALSADA |
| H-F4 | MAE MatterSim ≤ MACE | 45.9 frente a 47.6 | PASA |
| H-F5 | δ_O, δ_F, δ_Cl a ≤0.15 eV de MP2020 | +0.140 / −0.174 / −0.035 | FALSADA (F) |
| H-F6 | MP2020 fijo, MAE ≤ 80 meV/át (n=26, O/F/Cl/N) | 73.3 (máx. 269, TiO2) | PASA |
| H-F7 | Spearman LOOCV ≥ 0.95 | 0.983 | PASA |
| H-REP | dif. rel. energía ≤ 1e-6, ambos modelos | 0 (byte-idéntico en energías) | PASA |
| C1 / C2 / C3 | convergencia / volumen ±8 % / Mg hcp < fcc | todo converge / 0 fuera / −1.8 meV | pasan |

- MACE-MP-0: MAE LOOCV 47.6, máx. 198 (TiO2); MP2020 fijo 75.4; bruto 291 meV/át.
- MatterSim bruto (O/F/Cl/N): MAE 323 meV/át. El uMLIP hereda el error de PBE con la molécula de O2 (los 14 óxidos salen menos estables que el experimento).
- Br y I con MP2020 (descriptivo, referencia molecular): 70 meV/át MatterSim, 119 MACE.
- 298.15 K (descriptivo): MAE LOOCV MatterSim 50.4 meV/át.
- Exploratorio, NO prerregistrado: sin los dos compuestos con Ti, la MAE LOOCV baja a 38.2 meV/át y el máximo a 96 meV/át (BeAl2O4). TiO2 (−195) y MgTiO3 (−90) salen sobrestabilizados con ambos modelos, coherente con el error conocido de PBE en óxidos de Ti sin +U.

## riesgos
- Energía de punto cero despreciada; moléculas aisladas sin espín fuera del dominio de entrenamiento.
- n pequeño por anión (Br n=2) y un solo compuesto con N e I.
- El ajuste por anión no corrige errores catiónicos (Ti).

## decisiones
- Según la regla del prerregistro, la fila queda en **E2** (H-F3 falla). Sin desviaciones.
- Originalidad: parcial. Las correcciones aniónicas (FERE, MP2020) y la comparación de uMLIP con JANAF ya existen; lo nuevo es la prueba prerregistrada de trasladar MP2020 a uMLIP con referencias moleculares, con LOOCV y réplica.

## proximo_paso
C-UMF-002: añadir una corrección catiónica para Ti (y metales de transición d0) fijada a priori, o ruta DFT+U de control para TiO2; ampliar a ≥40 compuestos (sulfuros, nitruros) y calcular E_hull con fases competidoras para cerrar UM-07.
