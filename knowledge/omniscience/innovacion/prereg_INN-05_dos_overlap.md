# Pre-registro (borrador) INN-05 — Solapamiento de DOS fonónica (uMLIP) como prefiltro de conductancia térmica de interfaz
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
