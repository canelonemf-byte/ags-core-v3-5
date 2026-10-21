# Pre-registro (borrador) INN-03 — Profundidad del doble pozo (uMLIP) frente a Tc en perovskitas
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
