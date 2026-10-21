# INN-01 — σᴬ(300 K) con MACE-MP-0 como compuerta de validez armónica: resultados confirmatorios
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963).
Fecha: 19-oct-2026 (UTC+2). Texto, código y figura propios; las fuentes se citan solo por DOI.

## Congelación
- Pre-registro con enmiendas A1–A8: `prereg_INN-01_sigmaA.FROZEN.md`, sha256 `180ae31a8e56a653ed389a6fb36c0fb75e48c4f3bf496161ad37e732fcad9663` (el hash se ha vuelto a comprobar).
- Orden temporal: el `.sha256` existe desde ≤ 23:15:23 (UTC+2, 18-oct).
- Fases del cálculo (UTC+2):
  - Hashes del código guardados en `out/code_sha256_pre_run.txt` a las 23:43:39 (`sha256sum -c` OK al evaluar).
  - Cálculo armónico: 23:43:39–23:48:37.
  - MD: 23:49:23–00:53 (19-oct).
- **La congelación es anterior al cálculo.** Las marcas anteriores a 23:15 se perdieron al restaurar la máquina, así que la hora declarada de las enmiendas (22:55) no se puede verificar.

## Referencia
- doi:10.1103/PhysRevMaterials.4.083809 (Knoop, Purcell, Scheffler, Carbogno 2020), comprobado en Crossref.
- σᴬ_OS a 300 K, tomados de la tabla del preprint arXiv 2006.14672v2. NaBr = 0.40 sale del texto principal.
- Los valores se han vuelto a comprobar en la fuente el 19-oct-2026.

## Materiales
- CuCl, CuBr, CuI, AgI y AgBr (zincblenda); AgCl, AgBr, AgI y NaBr (sal gema). Control: Si.
- AgI-RS queda **excluido por A4**: f_min = −0.81 THz (3×3×3) y −0.74 THz (2×2×2). Con eso, **n = 8**.

## Resultados por material (σᴬ, 300 K, muestreo clásico con 24 instantáneas y FC 3×3×3)
| Material | σᴬ MACE [IC95] | σᴬ_OS ref. | Δ |
|---|---|---|---|
| CuCl-ZB | 0.592 [0.578, 0.606] | 0.55 | +0.04 |
| CuBr-ZB | 0.524 [0.507, 0.542] | 0.52 | +0.00 |
| CuI-ZB | 0.438 [0.424, 0.451] | 0.37 | +0.07 |
| AgI-ZB | 0.551 [0.534, 0.568] | 0.41 | +0.14 |
| AgBr-ZB | 0.583 [0.567, 0.598] | 0.68 | −0.10 |
| AgCl-RS | 0.709 [0.689, 0.728] | 0.50 | +0.21 |
| AgBr-RS | 0.883 [0.864, 0.899] | 0.48 | +0.40 |
| AgI-RS | excluido (inestable) | 0.52 | — |
| NaBr-RS | 0.412 [0.389, 0.440] | 0.40 | +0.01 |
| Si (control) | 0.227 [0.220, 0.234] | 0.15 | +0.08 |

## Criterios (tal como están escritos)
| Criterio | Requisito | Valor | Veredicto |
|---|---|---|---|
| H-A1 (original) | ρ ≥ 0.8, n ≥ 10, IC95 sin 0 | n = 8 | **NO EVALUABLE → no superada** |
| H-A1 (enmienda A2/A4) | n ≥ 9 | n = 8 | **NO EVALUABLE → no superada** |
| H-A2 | \|sesgo\| medio ≤ 0.05 (mismo n) | n = 8 | **NO EVALUABLE → no superada** |
| H-A3 | compuerta σᴬ ≥ 0.30 frente a error TO | sin TO verificadas (A5) | **NO EVALUABLE → no superada** |

Valores calculados en el n = 8 disponible (solo informativos, porque el criterio no se puede aplicar):
- ρ de Spearman = 0.50, IC95 bootstrap [−0.42, 0.92]: incluye 0.
- Sesgo absoluto medio 0.122; sesgo con signo +0.098.
- Si se hubieran podido aplicar, H-A1 y H-A2 habrían fallado.

**Veredicto global: NO SUPERADA (no evaluable).** No hay falsación formal, pero los números apuntan en contra.

## Controles
- Trivial (F = F⁽²⁾): σᴬ = 0 en todos los materiales. Pasa.
- Si (positivo armónico): 0.227 frente a 0.15. MACE sobreestima +0.08, el mismo sesgo que en el exploratorio X1.
- Sensibilidad 2×2×2 frente a 3×3×3: |Δσᴬ| máximo 0.056 (AgCl). ρ con FC 2×2×2 = 0.50, igual que con 3×3×3.
- MD Langevin (A7, 300 K, 5 ps, 200 fotogramas tras descartar 1 ps; **completada**):
  - CuI: σᴬ_MD = 0.571 frente a 0.438 con muestreo (aiMD DFT publicado: 0.41).
  - AgCl: σᴬ_MD = 1.085 frente a 0.709 (aiMD DFT publicado: 0.85).
  - La MD con MACE da valores más altos que el muestreo armónico, igual que ocurre en DFT. Es compatible con la formación de defectos intersticiales que describe la referencia (no se analizó la trayectoria).

## Análisis adicional (no pre-registrado; el script se escribió después de ver los resultados)
- El texto original de H-A1 menciona σᴬ «DFT-aiMD», pero la tabla de la enmienda A1 usa σᴬ_OS. La evaluación sigue la enmienda.
- Contra σᴬ_MD (aiMD), n = 7: ρ = −0.04.
- La compuerta σᴬ ≥ 0.30 marca los 8 materiales: con este conjunto, todos anarmónicos, no discrimina nada.
- 3 de 8 materiales (37.5 %) quedan dentro de ±0.05 de la referencia.

## Desviaciones
- Ninguna en los criterios, el conjunto ni los umbrales.
- La exclusión de AgI-RS se aplicó según la regla A4, fijada de antemano.
- La MD terminó completa, así que no hubo que cortarla.

## Nivel E
INN-01 se queda en **E2 (exploratorio)**. El intento confirmatorio no pudo evaluarse (n = 8 < 9, y H-A3 sin datos de TO). La evidencia descriptiva no apoya la hipótesis: ρ = 0.50 con un IC que incluye 0, y MACE-MP-0 sin afinar sobreestima σᴬ de forma sistemática (+0.10; Si +0.08).
Siguiente paso: un prereg nuevo con n ≥ 12 (lista completa de la SM de Knoop), frecuencias TO verificadas para H-A3, y un modelo afinado o DFT para separar el ablandamiento del uMLIP.
