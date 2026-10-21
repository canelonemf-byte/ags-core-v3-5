# C-MAT-001 — Informe de resultados (ejecución 18-oct-2026, ~21:20 UTC+2)

Pre-registro congelado: `prereg_C-MAT-001.md` sha256 `efb5f872cd581a88626cb9b3dbc2cb7b9e4f547c1bc1d1ec850de958c583ea90` (21:16 UTC+2, antes del primer cálculo; sin cambios posteriores).
Modelo: **MACE-MP-0 medium** (checkpoint 2023-12-03 `128L1_epoch199`, sha256 `01bfe221…5845`), float64, CPU. CHGNet **no** usado.
Pila: ASE 3.29.0 · Phonopy 4.8.3 · mace-torch 0.3.16 · torch 2.14.1+cpu. Sin aleatoriedad (sin semillas).

## Tabla por material (configuración base 2×2×2, 0.01 Å; malla 20³)
| Material | Esperado | Veredicto (3 config.) | f_min (THz) | ω_pred TO Γ (cm⁻¹) | ω_exp (cm⁻¹) | Error |
|---|---|---|---|---|---|---|
| Si | estable | estable ✔ | 0.000 | 373.0 | 520.2 | −28.3 % |
| C | estable | estable ✔ | 0.000 | 1172.0 | 1332 | −12.0 % |
| GaAs | estable | estable ✔ | 0.000 | 212.6 | 269 | −21.0 % |
| MgO | estable | estable ✔ | 0.000 | 332.6 | 396 | −16.0 % |
| NaCl | estable | estable ✔ | 0.000 | 147.8 | no verificada (164 secundaria) | (−9.9 % secundario, no cuenta) |
| PbTe | estable | estable ✔ | 0.000 | 52.8 | 18.0 | +193.6 % |
| SnSe | estable | estable ✔ (⚠ relajó a Fm-3m) | 0.000 | — | — | — |
| SrTiO3 (control −) | inestable | inestable ✔ | −2.357 | — | — | — |
| BaTiO3 (control −) | inestable | inestable ✔ | −6.412 | — | — | — |

## Criterios (exactamente como se pre-registraron)
- **H-MAT-1: PASA** — 9/9 correctos (umbral ≥ 8/9); ambos controles negativos correctos.
- **H-MAT-2: FALSADA** — 0/6 dentro de ±10 % (umbral ≥ 5/6).
- **H-MAT-3: PASA** — ningún veredicto cambia entre 2×2×2/3×3×3 ni entre 0.01/0.03 Å (ω_TO varía ≤ 1.1 %).

## Desviaciones y observaciones
- No hay desviaciones de criterios ni de protocolo.
- NAC no aplicado (no hay cargas de Born): se compara TO, como estaba previsto.
- ⚠ SnSe: con FixSymmetry(Pnma), la relajación de MACE convergió a una estructura de mayor simetría, Fm-3m tipo NaCl (a ≈ 6.05 Å). El veredicto «estable» se refiere a esa fase y no a la fase Pnma experimental. Análisis de sensibilidad (no pre-registrado): con SnSe contado como incorrecto quedan 8/9 y H-MAT-1 sigue pasando.
- Análisis exploratorio (no pre-registrado): el error firmado medio en Si, C, GaAs y MgO es −19.3 %. Es coherente con el ablandamiento sistemático descrito para MACE-MP-0 (Deng et al., npj Comput. Mater. 2025, doi:10.1038/s41524-024-01500-6). El caso de PbTe es distinto: modo TO muy anarmónico, con un valor experimental a baja T de 18 cm⁻¹; un cálculo armónico no puede reproducirlo.

## Nivel de evidencia
UM-08 pasa de E1 a **E2 (Predicción)**: hay predicciones calculadas evaluadas contra criterios pre-registrados. No sube a E3, porque H-MAT-2 está falsada y no hay réplica independiente. Lo que queda respaldado: clasificación de estabilidad dinámica robusta. Lo que queda falsado: frecuencias Γ con MACE-MP-0 sin ajuste dentro del ±10 %.
