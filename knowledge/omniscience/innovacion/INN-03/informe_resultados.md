# INN-03 — Profundidad del doble pozo (MACE-MP-0) frente a Tc en perovskitas ABX3: resultados confirmatorios
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963).
Fecha: 18-oct-2026 (UTC+2). Texto, código y figura propios; las fuentes se citan solo por DOI.

## Congelación
- Pre-registro con enmiendas B1–B4 (añadidas antes de calcular sobre este conjunto): `prereg_INN-03_pozos_ferro.FROZEN.md`, sha256 `839eeaec1697c226fdfff7449cbdbfcae61f8c8b2aca8b918030e313d99d728a`.
- Evidencia de orden temporal en la máquina: el archivo `.sha256` existe desde 23:15:23 (UTC+2); la salida del cálculo (`out/run.log`, `out/inn03_raw.json`) se creó a partir de 23:34:51. El hash se volvió a comprobar (`sha256sum -c` OK) antes de la réplica.
- Limitación: las marcas de tiempo anteriores a 23:15 se perdieron al restaurar el directorio de trabajo; la enmienda declara 22:55, pero eso no se puede verificar en el sistema de archivos.

## Verificación de referencias (comprobado de nuevo el 18-oct-2026)
- Los 9 DOI de B1 resuelven en Crossref con el título, los autores, la revista, el volumen y las páginas citados.
- Valores numéricos comprobados en el resumen de la fuente primaria: BiFeO3, 820–830 °C (coexistencia a 825 °C ⇒ 1098 K), doi:10.1103/PhysRevLett.102.027602; CsGeCl3 155 °C, CsGeBr3 238 °C y CsGeI3 277 °C (428/511/550 K), doi:10.1002/zaac.19875450217.
- Para los no ferroeléctricos (Tc = 0), la clasificación se apoya en el título o tema de cada fuente (antiferroeléctrico, ferroeléctrico incipiente, cúbico a baja T, secuencia centrosimétrica); no se leyó el texto completo de todas.
- No hubo nuevas enmiendas de referencia.

## Conjunto (n = 10, disjunto del exploratorio X2 {PbTiO3, KNbO3, BaTiO3, SrTiO3, KTaO3})
BiFeO3, CsGeCl3, CsGeBr3, CsGeI3 (FE); PbZrO3, PbHfO3 (AFE, Tc = 0); CaTiO3, BaZrO3 (controles negativos); SrZrO3, BaSnO3.

## Resultados (criterios originales, tal como están escritos)
| Material | Tc exp (K) | ΔE_rel (meV/f.u.) | Pred. FE | Acierto | Grupo relajado | f_opt,Γ 2×2×2 / 3×3×3 (THz) |
|---|---|---|---|---|---|---|
| BiFeO3 | 1098 | −870.7 | sí | ✓ | Pm | −5.943 / −5.943 |
| CsGeCl3 | 428 | −152.9 | sí | ✓ | R3m | −4.432 / −4.432 |
| CsGeBr3 | 511 | −58.8 | sí | ✓ | R3m | −2.406 / −2.406 |
| CsGeI3 | 550 | −27.0 | sí | ✓ | R3m | −1.752 / −1.752 |
| PbZrO3 | 0 | −216.2 | sí | ✗ | R3m | −3.316 / −3.316 |
| PbHfO3 | 0 | −114.0 | sí | ✗ | R3m | −2.755 / −2.755 |
| CaTiO3 | 0 | −97.7 | sí | ✗ | P4mm | −3.558 / −3.558 |
| BaZrO3 | 0 | 0.0 | no | ✓ | Pm-3m | +2.639 / +2.639 |
| SrZrO3 | 0 | −15.3 | sí | ✗ | P4mm | −2.073 / −2.073 |
| BaSnO3 | 0 | 0.0 | no | ✓ | Pm-3m | +3.117 / +3.117 |

- **H-F1 (ρ ≥ 0.7, n ≥ 8): FALSADA.** ρ de Spearman = 0.376 (p = 0.28, n = 10).
- **H-F2 (≥ 80 % de aciertos con |ΔE_rel| ≥ 10 meV/f.u.): FALSADA.** 6/10 = 60 %.
- **Controles negativos:** BaZrO3 pasa (por debajo del umbral) y CaTiO3 falla (−97.7 meV/f.u.).
- **Sensibilidad 3×3×3:** el modo de Γ cambia menos de 0.001 THz en todos los materiales, así que no afecta al resultado.
- **Veredicto global: FALSADA.**

## Análisis adicional (no pre-registrado; solo informativo)
- La frase del borrador «*no cúbicos simples: se reportarán aparte» marcaba a BiFeO3. Sin BiFeO3 (n = 9): ρ = 0.10 y 5/9 aciertos. Sigue falsada.
- Solo entre los FE (n = 4): ρ = 0.20. En CsGeX3 la profundidad decrece Cl > Br > I, mientras que la Tc crece Cl < Br < I: orden invertido.
- Profundidad del barrido congelado en lugar de la relajada: ρ = 0.25.
- Lectura física: la celda de 5 átomos no permite giros de octaedros ni orden antipolar. Por eso los antiferroeléctricos (PbZrO3, PbHfO3) y los materiales dominados por giros (CaTiO3, SrZrO3) caen en un mínimo polar ficticio. Es la limitación conocida del enfoque, y el pre-registro la ponía a prueba precisamente con estos controles.
- En BiFeO3 el barrido congelado llega al límite de 0.35 Å, y MACE-MP-0 no incluye el espín.

## Réplica
- Segunda ejecución completa (23:39–23:41 UTC+2, `rep/`): ΔE_rel coincide hasta 0.0016 meV/f.u. y los criterios no cambian.
- ΔE congelado difiere hasta 4.2 meV/f.u. y algunos grupos espaciales cambian (CaTiO3 Pm, SrZrO3 Cm). Se debe a que el modo blando es triplemente degenerado y Phonopy elige un autovector arbitrario dentro del subespacio. No afecta a los criterios, que usan ΔE_rel.

## Desviaciones
Ninguna. No se cambiaron criterios, conjunto ni umbrales después de ver los resultados.

## Nivel E
INN-03 queda **E2 confirmatorio negativo**: es una predicción de modelo contrastada con criterios congelados y resulta falsada. La hipótesis «ΔE_rel de 5 átomos ordena Tc» queda refutada para perovskitas ABX3 generales. El ρ = 0.97 del exploratorio X2 no se generaliza.
