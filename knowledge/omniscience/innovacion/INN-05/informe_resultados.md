# INN-05 — Solapamiento de DOS fonónica (MACE-MP-0) como prefiltro de conductancia térmica de interfaz: resultados confirmatorios
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963).
Fecha: 19-oct-2026 (UTC+2). Texto, código y figura propios; las fuentes se citan solo por DOI.

## Congelación
- Pre-registro con enmiendas C1–C6: `prereg_INN-05_dos_overlap.FROZEN.md`, sha256 `4d8f3ba147a2f501b42fc1ca4b7820a78bef8941db983c62cb767a601f05e4d2` (`sha256sum` vuelve a coincidir el 19-oct-2026).
- Orden temporal: el `.sha256` y el prereg existen desde ≤ 23:15:23 (UTC+2, 18-oct). La ejecución confirmatoria (`out/run.log`) empezó a las 23:34:51 y terminó a las 23:36:34. **La congelación es anterior al cálculo.**
- Limitación: las marcas anteriores a 23:15 se perdieron al restaurar la máquina; la hora de enmienda declarada (22:55) no se puede verificar en el sistema de archivos.
- La cabecera del texto congelado aún dice «BORRADOR, no congelado»; no se editó para no romper el hash.

## Referencias (comprobadas en Crossref el 19-oct-2026)
- doi:10.1103/PhysRevB.102.205304 (Koh et al. 2020): Al, Co y Ru sobre Al2O3(0001), 350 ± 60 MW m⁻² K⁻¹.
- doi:10.1103/PhysRevB.67.054302 (Costescu, Wall, Cahill 2003): TiN/Al2O3(0001), ≈ 700 MW m⁻² K⁻¹.
- Los valores numéricos se toman de la enmienda C1; esta vez no se releyeron en el texto.

## Materiales
Al, Co, Ru, TiN, Al2O3 (corindón), y Pb y C como controles de método. Pares evaluables: Al|Al2O3, Co|Al2O3, Ru|Al2O3 y TiN|Al2O3 (n = 4).

## Criterios (tal como están escritos)
| Criterio | Requisito | Resultado | Veredicto |
|---|---|---|---|
| H-T1 | ρ ≥ 0.6 con n ≥ 8 | n = 4 | **NO EVALUABLE → no superada** (C2) |
| H-T2 | Δρ(O − AMM) ≥ 0.10 con n ≥ 8 | n = 4 | **NO EVALUABLE → no superada** (C2) |
| H-T3 | \|O_MACE − O_DFT\| ≤ 0.05 en ≥ 3 pares | sin DOS DFT (PhononDB, timeout) | **NO EVALUABLE → no superada** (C3) |
| Control idéntico | O(Al\|Al) = 1 | 1.000000 | pasa |
| Control extremo | O(C\|Pb) ≈ 0 | 3.1×10⁻⁵ | pasa |
| Permutación nula | — | no aplica con n = 4 (C4) | — |

**Veredicto global: NO SUPERADA por no evaluable.** No está falsada: ningún umbral se pudo comparar con datos.

## Descriptivo (no confirmatorio)
| Par | TBC exp | O (MACE) | t_AMM |
|---|---|---|---|
| Al\|Al2O3 | 350 | 0.047 | 0.686 |
| Co\|Al2O3 | 350 | 0.112 | 0.9999 |
| Ru\|Al2O3 | 350 | 0.013 | 0.878 |
| TiN\|Al2O3 | 700 | 0.329 | 0.9999 |

- ρ(O, TBC) = 0.77 y ρ(t_AMM, TBC) = 0.77 (n = 4, con tres empates). Δρ = 0: O no mejora a la línea base acústica.
- Con la TBC igual dentro del error, O varía unas 9 veces (Al, Co, Ru). O, por sí solo, no explica la TBC medida.
- v_D de Ru (1044 m/s) parece anómalamente bajo; puede ser un artefacto de MACE o de la estimación por pendientes. No está verificado.
- Ningún material tiene modos imaginarios: f_min ≥ −2.4×10⁻⁷ THz.

## Desviaciones y notas de procedencia
- D1 (procedimiento, no afecta al resultado): existía una ejecución previa, anterior a la restauración de las 23:15:23. Se apartó en `/workspace/inn05_results_prereset.json` y no se puede situar respecto a la congelación. La ejecución confirmatoria de 23:34 la reproduce con diferencias ≤ 10⁻⁹. Los veredictos dependen solo del n de referencias verificadas (C2–C3), no de los valores calculados.
- No se cambiaron criterios, conjunto ni umbrales después de ver los resultados.

## Nivel E
INN-05 se queda en **E2 (exploratorio)**. El intento confirmatorio no pudo evaluarse (n = 4 < 8 y sin DOS DFT). El descriptivo no apoya que O aporte algo sobre la línea base AMM.
Siguiente paso: ≥ 8 TBC verificadas en fuente primaria (p. ej., series metal/diamante o metal/Si de una misma fuente) y DOS DFT locales para H-T3, con un prereg nuevo.
