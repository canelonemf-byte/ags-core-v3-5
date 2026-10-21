# Pre-registro (borrador) INN-01 — σᴬ con uMLIP como compuerta de validez armónica
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963).
Estado: BORRADOR, no congelado ni ejecutado. Redactado el 18-oct-2026 (UTC+2) **después** de ver el exploratorio X1; por eso la prueba confirmatoria usa materiales que no aparecen en X1.

**Hipótesis**
- H-A1: σᴬ(300 K) calculado con MACE-MP-0 (one-shot, armónico) ordena los materiales igual que σᴬ DFT-aiMD publicado (Knoop et al., PRMaterials 4, 083809). Criterio: ρ de Spearman ≥ 0.8, con n ≥ 10.
- H-A2: el sesgo absoluto medio |σᴬ_MACE − σᴬ_DFT| es ≤ 0.05.
- H-A3 (compuerta): con el umbral fijado de antemano σᴬ ≥ 0.30, todos los materiales con error armónico en el TO de Γ > 50 % quedan marcados, y se marca ≤ 30 % de los que tienen error ≤ 15 %.

**Método**
- Conjunto: ≥ 10 sólidos binarios con σᴬ DFT publicado en la SM de Knoop 2020, excluidos los 6 de X1. La lista y los valores se fijan y verifican antes de ejecutar.
- Estructura de partida: experimental; relajación como en C-MAT-001.
- Constantes de fuerza: 3×3×3, 0.01 Å.
- Muestreo: 24 instantáneas armónicas a 300 K (Phonopy, semilla 20261018).
- σᴬ = √(Σ⟨(F−F⁽²⁾)²⟩/Σ⟨F²⟩); IC95 por bootstrap.
- Control de método: MD Langevin de 5 ps a 300 K en 2 materiales.

**Controles**
- Positivo armónico: Si (DFT 0.15).
- Positivos anarmónicos: según la lista verificada.
- Control trivial: con fuerzas sustituidas por F⁽²⁾ debe salir σᴬ = 0.
- Sensibilidad: FC 2×2×2 frente a 3×3×3.

**Falsación**: H-A1 se rechaza si ρ < 0.8 o si el IC95 de ρ incluye 0. H-A2 y H-A3 se rechazan según los criterios anteriores.
**Coste estimado**: ~30–60 min de CPU.

## Enmiendas pre-ejecución (18-oct-2026, 22:55 UTC+2; antes de cualquier cálculo sobre este conjunto)
**A1. Referencias σᴬ DFT verificadas en fuente primaria.** Knoop, Purcell, Scheffler, Carbogno, Phys. Rev. Materials 4, 083809 (2020), doi:10.1103/PhysRevMaterials.4.083809. Los valores se han leído en el código fuente arXiv 2006.14672v2 (CC BY), tabla «tab:nmh_md_comps» (σᴬ_OS a 300 K) y texto principal.

| Material | Estructura | σᴬ ref. | Método de la referencia |
|---|---|---|---|
| AgBr | ZB (216) | 0.68 | one-shot |
| AgI | ZB (216) | 0.41 | one-shot |
| CuCl | ZB (216) | 0.55 | one-shot |
| CuBr | ZB (216) | 0.52 | one-shot |
| CuI | ZB (216) | 0.37 | one-shot |
| AgCl | RS (225) | 0.50 | one-shot |
| AgBr | RS (225) | 0.48 | one-shot |
| AgI | RS (225) | 0.52 | one-shot |
| NaBr | RS (225) | 0.40 | no especificado en el texto principal |

- Control positivo (fuera del conjunto evaluado): Si, 0.15.
- La SM con la lista completa (figshare doi:10.6084/m9.figshare.12783395) no se pudo descargar desde la caja (HTTP 403).

**A2. Tamaño del conjunto.** El conjunto verificable y disjunto del exploratorio X1 tiene **n = 9**, por debajo del n ≥ 10 pre-registrado.
- Criterio enmendado: n ≥ 9.
- Según el criterio original, H-A1 se declara **no evaluable (n < 10)**; ambos resultados se reportan.

**A3. Muestreo.** Para coincidir con la definición de la referencia (límite clásico), se usa distribución **clásica** de Phonopy (RandomDisplacements, dist_func="classical"), 24 instantáneas, semilla 20261018, 300 K. La referencia usa one-shot con amplitudes clásicas; nuestra versión es muestreo canónico armónico (diferencia metodológica declarada).

**A4. Exclusión por inestabilidad.** Un material con f_min < −0.3 THz en la malla 20³ (FC 3×3×3) no admite muestreo armónico.
- Se excluye y cuenta en contra de n.
- Si n cae por debajo de 9, H-A1 y H-A2 son no evaluables.

**A5. H-A3 no evaluable.** No se han verificado frecuencias TO experimentales en fuente primaria para este conjunto, así que H-A3 se declara no evaluable y cuenta como no superada.

**A6. Estructuras de partida.** Parámetros de red aproximados: CuCl 5.42, CuBr 5.69, CuI 6.05, AgI-ZB 6.50, AgBr-ZB 6.20, AgCl 5.55, AgBr-RS 5.77, AgI-RS 6.07, NaBr 5.97 Å. La relajación (FixSymmetry + FrechetCellFilter, fmax 1e-3) fija el valor del modelo.

**A7. Control MD.** Langevin a 300 K, paso de 4 fs, 5 ps (descartando 1 ps), en la supercelda 3×3×3 de CuI y AgCl. Semilla 20261018.

**A8. IC95 de ρ.** Bootstrap sobre materiales: 5000 remuestreos, semilla 20261018, percentiles 2.5/97.5.
