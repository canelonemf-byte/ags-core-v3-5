# Pre-registro (borrador) INN-03 — Profundidad del doble pozo (uMLIP) frente a Tc en perovskitas
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963).
Estado: BORRADOR, no congelado. Redactado después del exploratorio X2 (n = 5); la prueba confirmatoria excluye PbTiO3, KNbO3, BaTiO3, SrTiO3 y KTaO3.

**Hipótesis**
- H-F1: la profundidad del pozo con relajación libre ΔE_rel (MACE-MP-0, meV/f.u.) ordena la Tc experimental de la transición paraeléctrica→ferroeléctrica, asignando Tc = 0 a los no ferroeléctricos. Criterio: ρ de Spearman ≥ 0.7, con n ≥ 8.
- H-F2: clasificación FE / no FE con un umbral fijado ahora (|ΔE_rel| ≥ 10 meV/f.u. ⇒ FE). Criterio: ≥ 80 % de aciertos.

**Método** (idéntico a X2, código `x2_ferro_wells.py`)
- Celda cúbica de 5 átomos relajada con FixSymmetry.
- Phonopy 2×2×2 a 0.01 Å; se toma el modo más blando de Γ.
- Barrido de 0 a 0.35 Å y relajación libre (celda incluida, fmax 1e-3), con perturbación de semilla 7.
- Conjunto candidato, que se fijará con Tc verificadas en fuentes primarias antes de ejecutar: LiNbO3*, LiTaO3*, NaNbO3, KTa0.5Nb0.5O3, BiFeO3*, CaTiO3 (no FE), BaZrO3 (no FE), PbZrO3 (antiferroeléctrico, control), etc.
  - *Los marcados con asterisco no son cúbicos simples: se reportarán aparte.

**Controles**
- Negativos: BaZrO3 y CaTiO3 (inestabilidad de giros, no FE). Deben quedar por debajo del umbral en el canal polar.
- Sensibilidad: supercelda 3×3×3 para el modo de Γ.

**Falsación**: ρ < 0.7, o < 80 % de aciertos en H-F2, o fallo de cualquiera de los dos controles negativos.
**Coste estimado**: ~15 min por material en CPU.

## Enmiendas pre-ejecución (18-oct-2026, 22:55 UTC+2; antes de cualquier cálculo sobre este conjunto)
**B1. Conjunto y referencias verificadas en fuente primaria.** Tc = transición paraeléctrica→ferroeléctrica; 0 = sin fase ferroeléctrica.

| Material | Tc (K) | Clase | Fuente |
|---|---|---|---|
| BiFeO3 | 1098 | FE (α R3c → β Pbnm, 820–830 °C, primer orden) | Arnold et al., PRL 102, 027602 (2009), doi:10.1103/PhysRevLett.102.027602 |
| CsGeCl3 | 428 | FE (R3m polar → cúbica; 155 °C) | Thiele, Rotter, Schmidt, Z. Anorg. Allg. Chem. 545, 148 (1987), doi:10.1002/zaac.19875450217 |
| CsGeBr3 | 511 | FE (R3m; 238 °C) | ídem |
| CsGeI3 | 550 | FE (R3m; 277 °C) | ídem |
| PbZrO3 | 0 | antiferroeléctrico | Sawaguchi, Shirane, Takagi, JPSJ 6, 333 (1951), doi:10.1143/JPSJ.6.333 |
| PbHfO3 | 0 | antiferroeléctrico | Shirane, Pepinsky, Phys. Rev. 91, 812 (1953), doi:10.1103/PhysRev.91.812 |
| CaTiO3 | 0 | ferroeléctrico incipiente; control negativo | Lemanov et al., Solid State Commun. 110, 611 (1999), doi:10.1016/S0038-1098(99)00153-2 |
| BaZrO3 | 0 | cúbico paraeléctrico hasta 2 K; control negativo | Akbarzadeh et al., PRB 72, 205104 (2005), doi:10.1103/PhysRevB.72.205104 |
| SrZrO3 | 0 | secuencia Pnma→Imma→I4/mcm→Pm-3m, toda centrosimétrica | Howard, Knight, Kennedy, Kisi, J. Phys.: Condens. Matter 12, L677 (2000), doi:10.1088/0953-8984/12/45/101; Kennedy, Howard, Chakoumakos, PRB 59, 4023 (1999) |
| BaSnO3 | 0 | cúbico hasta 10 K | Bévillon et al., J. Phys.: Condens. Matter 20, 145217 (2008), doi:10.1088/0953-8984/20/14/145217 |

- n = 10, disjunto del exploratorio X2.
- Se retira NaTaO3: no se verificó en fuente primaria la ausencia de fase polar a baja T.
- Se retiran LiNbO3 y LiTaO3: no tienen fase madre perovskita cúbica.
- El título pasa a «perovskitas ABX3» por la inclusión de los haluros CsGeX3.

**B2. Selección del modo.** Se toma el modo **óptico** más blando de Γ (se excluyen los 3 modos acústicos de menor |f|). En X2 se tomaba el mínimo absoluto, que coincidía con un modo óptico porque todos eran inestables.

**B3. Parámetros iniciales aproximados (Å).** BiFeO3 3.96, CsGeCl3 5.43, CsGeBr3 5.64, CsGeI3 6.05, PbZrO3 4.16, PbHfO3 4.14, CaTiO3 3.84, BaZrO3 4.19, SrZrO3 4.10, BaSnO3 4.12. Sin espín explícito (MACE-MP-0 no lo modela; limitación para BiFeO3).

**B4. ρ con empates.** Se usa Spearman con rangos promedio (scipy).
