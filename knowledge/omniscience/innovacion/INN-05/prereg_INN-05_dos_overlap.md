# Pre-registro (borrador) INN-05 — Solapamiento de DOS fonónica (uMLIP) como prefiltro de conductancia térmica de interfaz
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963).
Estado: BORRADOR, no congelado. X3 solo calculó solapamientos, sin compararlos con medidas; la comparación con TBC no se ha visto.

**Hipótesis**
- H-T1: en ≥ 8 pares de interfaz con TBC experimental a ~300 K (lista verificada antes de ejecutar; p. ej. metal/dieléctrico y semiconductor/semiconductor), el solapamiento O = ∫min(g₁,g₂)dω de las DOS normalizadas MACE-MP-0 correlaciona con la TBC. Criterio: ρ de Spearman ≥ 0.6.
- H-T2: O mejora a la línea base de desajuste acústico (cociente de impedancias acústicas Z₁/Z₂, con velocidades de sonido de las propias curvas MACE). Criterio: Δρ ≥ 0.10.
- H-T3: el ablandamiento no domina el resultado: |O_MACE − O_DFT| ≤ 0.05 en ≥ 3 pares con DOS DFT de PhononDB.

**Método**: `x3_dos_overlap.py` (malla 20³, σ = 0.1 THz). Los metales requieren comprobar que MACE da fonones razonables.
**Controles**
- Par idéntico (O = 1).
- Par de ensanchamiento extremo (C|Pb).
- Permutación aleatoria de las TBC (1000 permutaciones, semilla 20261018) para obtener la distribución nula de ρ.

**Falsación**: ρ < 0.6, o Δρ < 0.10 frente a la línea base, o fallo de H-T3.
**Advertencia física**: el solapamiento ignora la velocidad de grupo, la dispersión inelástica y la calidad de la interfaz, factores que en la práctica pueden dominar.

## Enmiendas pre-ejecución (18-oct-2026, 22:55 UTC+2; antes de cualquier cálculo sobre este conjunto)
**C1. TBC experimentales verificadas en fuente primaria** (pares disjuntos de los materiales del exploratorio X3: Si, C, GaAs, MgO, NaCl, PbTe).

| Par | TBC (MW m⁻² K⁻¹) | T | Fuente |
|---|---|---|---|
| Al/Al2O3(0001) | 350 ± 60 | ambiente | Koh et al., PRB 102, 205304 (2020), doi:10.1103/PhysRevB.102.205304 (texto) |
| Co/Al2O3(0001) | 350 ± 60 | ambiente | ídem |
| Ru/Al2O3(0001) | 350 ± 60 | ambiente | ídem |
| TiN/Al2O3(0001) | ≈ 700 | ~294 K | Costescu, Wall, Cahill, PRB 67, 054302 (2003), doi:10.1103/PhysRevB.67.054302 (resumen) |

**Descartados por falta de verificación:**
- Stevens et al. 2005 (solo se da el rango, cerrado).
- Al/GaN (el resumen no da el número).
- Al/SiC (fuente inaccesible).
- GaN/ZnO (solo fuente secundaria).
- SrRuO3/SrTiO3 (solo cota inferior > 800, y la estructura cúbica MACE de SrTiO3 es inestable).

**C2. Consecuencia.** n = 4 < 8.
- Según los criterios pre-registrados, **H-T1 y H-T2 son no evaluables** y cuentan como no superadas.
- Se calculan O y la línea base AMM como análisis descriptivo (no confirmatorio).

**C3. H-T3 no evaluable.** PhononDB no respondió desde la caja (timeout), así que no hay DOS DFT disponibles.

**C4. Controles.**
- Par idéntico (Al|Al; debe dar O = 1).
- C|Pb: ensanchamiento extremo; C es control de método, no par evaluado.
- La permutación nula no se aplica con n = 4.

**C5. Línea base AMM.**
- Transmisión t = 4Z₁Z₂/(Z₁+Z₂)², con Z = ρ·v_D.
- v_D es la velocidad de Debye promedio de las ramas acústicas MACE (pendientes a |q| = 0.02 en 26 direcciones).

**C6. Estructuras.**
- Al fcc 4.05; Pb fcc 4.95; Co hcp 2.507/4.07; Ru hcp 2.706/4.282; TiN rocksalt 4.24 Å.
- Al2O3 corindón (R-3c): a = 4.759, c = 12.991 Å; Al (0, 0, 0.3522), O (0.3064, 0, 0.25).
- Supercelda 2×2×2 de la celda primitiva/convencional; fonones como en C-MAT-001.
