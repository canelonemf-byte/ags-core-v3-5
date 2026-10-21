# Pre-registro (BORRADOR) — C-MAT-001 «Estabilidad y fonones cristalinos»
**Estado:** propuesto, NO ejecutado · **Paso:** E1 → E2 (predicción de modelo) · **Redactado:** 18-oct-2026 (UTC+2) · **Requiere:** aprobación del autor (Lázaro López Paz) antes de calcular. Una vez aprobado, este documento se congela (hash SHA-256 en log_avances.md) y los criterios no se modifican.

## 1. Pregunta
¿Puede el pipeline MV1 (relajación → fonones armónicos por desplazamientos finitos → modos imaginarios) clasificar correctamente la estabilidad dinámica y predecir las frecuencias ópticas de Γ de materiales conocidos con un error acotado, antes de aplicarlo a candidatos nuevos?

## 2. Paso concreto propuesto (E1→E2)
Ejecutar, en la caja y solo en CPU, **Phonopy + un potencial interatómico universal de ML** (p. ej. MACE-MP-0 vía ASE; alternativa: CHGNet) sobre un conjunto de referencia de 9 materiales. Es un nivel E2 porque produce *predicciones de un modelo*; no es E3 hasta repetirse con DFT (QE) bajo condiciones documentadas, ni E5 hasta coincidir por otra ruta.

## 3. Conjunto de referencia (fijado antes de calcular)
| Material | Estructura | Papel | Expectativa |
|---|---|---|---|
| Si | diamante | control positivo | estable; óptico Γ ≈ 520 cm⁻¹ (Raman) |
| C | diamante | control positivo, alta frecuencia | estable; óptico Γ ≈ 1332 cm⁻¹ |
| GaAs | zincblenda | polar (LO–TO) | estable; TO ≈ 268, LO ≈ 292 cm⁻¹ |
| MgO | sal gema | polar | estable; TO ≈ 401 cm⁻¹ |
| NaCl | sal gema | iónico blando | estable; TO ≈ 164 cm⁻¹ |
| PbTe | sal gema | κL baja, anarmónico | estable (modos TO blandos) |
| SnSe | Pnma | κL baja | estable a 0 K |
| SrTiO₃ | perovskita cúbica | **control negativo** | modos imaginarios (inestabilidad antiferrodistorsiva, R) a 0 K |
| BaTiO₃ | perovskita cúbica | **control negativo** | modo ferroeléctrico imaginario en Γ a 0 K |

Los valores experimentales de referencia (y su incertidumbre) deben **verificarse y citarse con DOI antes de ejecutar** (auditoría de citas); las cifras de la tabla son orientativas y no se usan para evaluar hasta estar verificadas.

## 4. Hipótesis y criterios de falsación (declarados antes)
- **H-MAT-1 (clasificación):** el pipeline clasifica correctamente la estabilidad dinámica de ≥8/9 materiales (estable = sin frecuencias < −0.3 THz en la malla de q; inestable = al menos una). *Falsada* si <8/9, o si falla cualquiera de los dos controles negativos.
- **H-MAT-2 (frecuencias):** error relativo |ω_pred − ω_exp|/ω_exp ≤ 10 % en el óptico de Γ (TO para polares) en ≥5/6 de {Si, C, GaAs, MgO, NaCl, PbTe}. *Falsada* si no se cumple. Criterio z>3 cuando haya σ experimental.
- **H-MAT-3 (convergencia):** el veredicto de estabilidad no cambia al pasar de supercelda 2×2×2 a 3×3×3 ni al variar el desplazamiento 0.01 → 0.03 Å. *Si cambia*, ese material se registra como «inconcluso», no como estable/inestable.

## 5. Protocolo fijo
1. Estructuras iniciales: prototipos cristalográficos estándar (sin CIF experimental propietario); hash de cada archivo de entrada.
2. Relajación: fmax ≤ 1e-3 eV/Å, celda incluida (filtro de celda de ASE).
3. Phonopy: supercelda 2×2×2 (y 3×3×3 para H-MAT-3), desplazamiento 0.01 Å, malla de q 20×20×20; NAC (corrección no analítica) para polares solo si se dispone de cargas de Born; si no, comparar TO y declararlo.
4. Semillas y versiones fijadas; registro PROV en JSON + SHA-256 de entradas/salidas, como en C-VIB-001.
5. E_hull: fuera del alcance de este paso (requiere datos de Materials Project con clave de API). Se registra como siguiente paso.

## 6. Resultados posibles y nivel
- Todas las H pasan → C-MAT-001 sube a **E2** (predicción de modelo validada frente a referencias).
- Falla alguna → se registra como falsada/inconclusa; el motor no se usa con candidatos nuevos hasta corregirlo.
- Siguiente paso (E2→E3): repetir los 9 materiales con DFT (Quantum ESPRESSO, PBEsol), pruebas de convergencia documentadas, y añadir E_hull.

## 7. Recursos y riesgos
Solo CPU, ~horas en la caja; instalar `phonopy`, `ase`, `mace-torch` (o `chgnet`) en un venv propio. Riesgos: los potenciales universales suelen ablandar frecuencias (sesgo sistemático, a declarar); materiales polares sin NAC; los controles negativos son sensibles a la convergencia.

---
## 8. Enmiendas pre-ejecución (18-oct-2026, 21:16 UTC+2) — antes de cualquier cálculo
Aprobado por el autor (vía agente OMNISCIENCE) el 18-oct-2026. Las secciones 1–7 no se modifican; estas enmiendas solo (a) fijan las referencias verificadas y (b) precisan ambigüedades de implementación. Criterios H-MAT-1/2/3 **sin cambios**.

### 8.1 Referencias experimentales verificadas (DOI resueltos en Crossref)
Regla fijada antes de ejecutar: se usa el valor que figura textualmente en una fuente primaria identificada; si esa fuente da un valor a baja temperatura, se usa ese (el modelo es armónico a 0 K); si un valor no puede leerse en una fuente primaria, **no se usa para evaluar** (§3) y el material cuenta como *no superado* en H-MAT-2 (criterio conservador).

| Material | Valor usado | Unidades / ≈THz | T | Fuente (DOI) | Grado de verificación | Cambio vs §3 |
|---|---|---|---|---|---|---|
| Si | 520.2 ± 0.5 | cm⁻¹ / 15.60 | 300 K | Parker, Feldman, Ashkin, Phys. Rev. 155, 712 (1967), 10.1103/PhysRev.155.712 | Valor textual en el abstract | 520 → 520.2 ± 0.5 |
| C (diamante) | 1332 | cm⁻¹ / 39.93 | ambiente (también 77 K y 4 K en el artículo) | Solin & Ramdas, Phys. Rev. B 1, 1687 (1970), 10.1103/PhysRevB.1.1687 | Valor textual en el abstract | sin cambio |
| GaAs (TO) | 269 | cm⁻¹ / 8.06 | ambiente | Holtz, Zallen, Brafman, Phys. Rev. B 38, 6097 (1988), 10.1103/PhysRevB.38.6097 (texto: «weak TO line at 269 cm⁻¹», LO 292 cm⁻¹) | Valor textual en el cuerpo del artículo | 268 → 269. (Strauch & Dorner, J. Phys. Condens. Matter 2, 1457 (1990), 10.1088/0953-8984/2/6/006, neutrones a 12 K: TO ≈ 8.02 THz según compilaciones; valor no leído en la fuente, solo informativo) |
| MgO (TO) | 396 | cm⁻¹ / 11.87 | 300 K | Komandin et al., Phys. Solid State 51, 2045 (2009), 10.1134/S1063783409100096 (texto: «at room temperature, the TO phonon has a frequency ν = 396 cm⁻¹») | Valor textual en el cuerpo | 401 → 396. (Jasperse et al., Phys. Rev. 146, 526 (1966), 10.1103/PhysRev.146.526: medidas 8–1950 K; valor numérico no legible en el abstract) |
| NaCl (TO) | — (164 orientativo) | cm⁻¹ / 4.92 | 300 K | Raunio, Almqvist, Stedman, Phys. Rev. 178, 1496 (1969), 10.1103/PhysRev.178.1496 (neutrones, 80 K y 300 K) | **NO verificado**: el valor numérico no aparece en abstract accesible; 164 cm⁻¹ procede de una compilación secundaria que también menciona 178 | 164 → no evaluable; cuenta como no superado en H-MAT-2; se informa como análisis secundario |
| PbTe (TO) | 18.0 ± 1.0 | cm⁻¹ / 0.540 | baja T (He líquido) | Kinch & Buss, Solid State Commun. 11, 319 (1972), 10.1016/0038-1098(72)90241-4 | Valor textual en el abstract | **nuevo** (§3 no daba valor). A 300 K el modo endurece (~32 cm⁻¹, Burkhard et al., JOSA 67, 943 (1977), 10.1364/JOSA.67.000943; valor no leído en el abstract) |
| SnSe, SrTiO₃, BaTiO₃ | — | — | — | Solo veredicto de estabilidad (§3) | — | sin cambio |

Advertencia: los modos TO de PbTe y, en menor medida, de NaCl son fuertemente anarmónicos/dependientes de T; un cálculo armónico a 0 K no está diseñado para reproducirlos. Esto se declara ahora y no modifica el criterio.

### 8.2 Precisiones de implementación (ambigüedades de §5)
1. **Modelo:** MACE-MP-0 «medium» (checkpoint oficial), `default_dtype=float64`, CPU. Respaldo solo si MACE no se instala: CHGNet (se declararía como desviación).
2. **Celda de la supercelda:** 2×2×2 / 3×3×3 se aplican a la celda convencional: cúbica de 8 átomos (Si, C, GaAs, MgO, NaCl, PbTe), perovskita cúbica de 5 átomos (SrTiO₃, BaTiO₃), celda Pnma de 8 átomos (SnSe).
3. **Relajación:** con celda (FrechetCellFilter) y **conservando la simetría del prototipo** (FixSymmetry); sin ello los controles cúbicos podrían distorsionarse y dejar de ser el objeto del test.
4. **Veredicto de estabilidad:** frecuencia mínima sobre la malla 20×20×20 centrada en Γ (incluye Γ, X, M, R para los cúbicos simples); «inestable» si mín < −0.3 THz. Las bandas de alta simetría se calculan solo como figura.
5. **«Óptico de Γ»:** sin NAC (no hay cargas de Born del modelo), los tres modos ópticos de Γ de los compuestos binarios son el TO; para Si y C, el triplete óptico. Se compara con TO experimental.
6. **H-MAT-3:** configuración base = 2×2×2, 0.01 Å; variantes = 3×3×3, 0.01 Å y 2×2×2, 0.03 Å. Un material cuyo veredicto cambie se registra «inconcluso» y **cuenta como no clasificado correctamente en H-MAT-1**.
7. Estructuras iniciales: prototipos con parámetros de red experimentales aproximados (solo punto de partida; se relajan). Semillas: no hay muestreo aleatorio (desplazamientos deterministas de Phonopy).
