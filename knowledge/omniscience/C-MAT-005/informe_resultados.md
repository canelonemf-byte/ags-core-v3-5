# C-MAT-005 — Informe de resultados
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963). Texto, código y figura propios; fuentes citadas solo por DOI.

## 1. Congelación
- `prereg_C-MAT-005.md` (9898 B), sha256 `b6a80ede…c39e`, congelado el 2026-10-19 a las 15:01:17 (UTC+2). `prereg_C-MAT-005.FROZEN.md` (554 B) es un **registro-puntero** (archivo, hash, hora, estado y autoría), no una copia rota. El hash coincide con el prereg actual.
- Ningún archivo de `out/` es anterior a la marca: el primero es de las 15:01:27. Antes solo hubo pruebas de humo con Ge, Cu y Si (`smoke/`). Los 17 hashes de `code_freeze.json` (código, referencias y CIF) coinciden al evaluar. **Congelación válida; resultados confirmatorios.**

## 2. Materiales y métodos
14 sólidos nuevos: AlN, SiC, KF, NaBr, KI, LiCl, CsCl, SrF2, BaF2, Na2O, ZrO2, BeAl2O4, MgTiO3 y ZrSiO4. Si y MgO son controles C1. Se usan MatterSim v1.0.0-5M (principal) y MACE-MP-0 (línea base), ambos en float64, con Phonopy armónico en V0 y en V_exp, comparado con NIST-JANAF. La prueba de artefacto usa rutilo y cuarzo-α en la celda experimental, con GPAW PBE. Se hicieron dos ejecuciones completas: run1 y run2.

## 3. Resultados con los criterios originales (run1; run2 da los mismos veredictos)
| Hipótesis | Resultado | Veredicto |
|---|---|---|
| H1 (principal) | 13/14 dentro de ±10 % (umbral 12). ZrO2 no evaluable (f_min −1.26 THz) | **PASA** |
| H2 | MARE S298 en V_exp = 2.31 % (n = 13; umbral 5 %) | **PASA** |
| H3 | V_exp 2.31 % < V0 5.71 % (n = 13) | **PASA** |
| H4 | MatterSim 2.31 % / MACE 8.04 % = 0.29 (umbral 0.6) | **PASA** |
| H5 | MARE Cv(298) frente a Cp = 3.09 % | **PASA** |
| H6 | MARE S(600 K) = 1.80 % | **PASA** |
| H7 | mediana del error con signo de S298 = +1.29 % (umbral ±3 %) | **PASA** |
| H-REP | MatterSim byte-idéntico; MACE con max_rel 7.2e-10 (tolerancia 1e-6) y no byte-idéntico; misma clase de estabilidad y mismos veredictos y controles | **PASA** |
| H-D1 rutilo | MLIP f_min,conm ≈ 0 en 2×2×1 (clase C). Además, C-DFT1 falla | **INCONCLUSA** |
| H-D2 cuarzo-α | MLIP clase C; DFT PBE no ejecutado (D1) | **INCONCLUSA** |

Controles:
- C1 pasa (desviación 0 en los 4 casos).
- **C2 falla**: KI con MatterSim da Cv(3000 K)/3Rn = 0.9666 < 0.99, porque tiene modos blandos de hasta −0.21 THz, aún dentro del umbral de evaluabilidad.
- C3 pasa: convergencia ≤ 0.62 %, sin inconclusos.
- **C-DFT1 falla en TiO2**: en Γ, la diferencia entre 500 y 650 eV llega a 0.44 THz (> 0.15).
- C-DFT2 pasa en TiO2 (fmax 2.0e-4 eV/Å).

Errores de S298 de MatterSim en V_exp:
AlN +3.9 %, SiC +0.6 %, KF −0.5 %, NaBr +1.0 %, KI +7.7 %, LiCl +5.6 %, CsCl −0.9 %, SrF2 +1.3 %, BaF2 −1.7 %, Na2O +0.5 %, ZrO2 +0.9 % (no evaluable), BeAl2O4 +1.6 %, MgTiO3 +1.4 %, ZrSiO4 +3.3 %.

MACE en V_exp sigue sobreestimando mucho: AlN +25 %, SiC +36 %, MgTiO3 +12 %.

## 4. Prueba de artefacto (descriptiva más allá del veredicto)
- **Rutilo, PBE en 2×2×1 (completo).** Estable en los 4 q conmensurados: el mínimo no acústico es 1.80 THz en (½,½,0), y la malla interpolada no da modos imaginarios. MatterSim y MACE también son estables en esos q. En la supercelda de C-MAT-004, en cambio, dan −3.11 y −2.48 THz en q ≈ (0.43, 0, ½), un punto que la 2×2×1 no muestrea. Esto es coherente con un artefacto, pero no está demostrado: es una clase C.
- **Cuarzo-α.** Con la celda experimental, MatterSim es estable incluso en la supercelda de C-MAT-004 (f_min 0.00 THz) y MACE da −0.11 THz. Es decir, la inestabilidad de C-MAT-004 desaparece en la celda experimental. En la 2×2×1 interpolada ambos dan −3.6 THz, que es solo descriptivo.

## 5. Desviaciones (ninguna cambia un veredicto)
- **D1.** A las 15:24 (UTC+2) se detuvo el bucle DFT antes de SiO2 PBE y de LDA. Con el código congelado, el cuarzo genera 54 desplazamientos (Phonopy no detecta la simetría del CIF) en una supercelda de 36 átomos. A unos 10 min por desplazamiento son más de 9 h, y el prereg prevé que H-D quede INCONCLUSA si la DFT no termina. Además, LDA solo serviría para distinguir B1 de B2, algo irrelevante porque PBE del rutilo es estable. Aunque se hubiera completado, H-D2 seguiría INCONCLUSA, porque los MLIP son clase C.
- **D2 (operativa).** `cmat005_run.py` y `cmat005_art_mlip.py` escriben en `out/<run>/<mod>/<mod>/`, pero `cmat005_eval.py` lee `out/<run>/<mod>/`. Se añadieron enlaces simbólicos (`code/link_paths.sh`) sin tocar datos, código congelado ni criterios.
- **N1.** La figura (`code/cmat005_fig.py`) se escribió tras la congelación y es solo descriptiva.

## 6. Niveles E
- **UM-16** (C-MAT-005) entra en **E2**. La regla congelada para E3 exige H1, H2 y H-REP, más C1 y **C2**. C2 falla (KI), así que no se alcanza E3 aunque pasen las 7 hipótesis y la réplica.
- UM-07 sigue en E1 y UM-15 en E2.

## 7. Originalidad
Baja. Que corregir el volumen reduce el error de los uMLIP ya está publicado (doi:10.1016/j.commatsci.2025.113770; doi:10.1038/s41524-025-01650-1; pshift doi:10.1103/PhysRevB.84.184103). Lo propio es la validación prerregistrada en 14 sólidos nuevos, con réplica por tolerancia y fallos declarados. No se ha hecho revisión sistemática.

## 8. Próximo paso
Proponer C-MAT-006 con estas cuatro líneas:
1. Fijar a priori el tratamiento de los modos blandos en C2 (o excluir de C2 los materiales con f_min < 0), sin reinterpretar C-MAT-005.
2. Repetir la DFT del rutilo en una 2×2×2 que muestree q_z = ½ y con ecut ≥ 650 eV para que C-DFT1 pase.
3. Simetrizar el cuarzo (symprec) para hacer viable su DFT.
4. Ampliar a más de 20 sólidos.
