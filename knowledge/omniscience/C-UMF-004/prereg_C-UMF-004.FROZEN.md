# FROZEN 2026-10-20T17:09:44+02:00 sha256 845ad29a942e6bf6d8704e12a0da8e79a2a5ba030de107d8541c5b444392be31
# Prerregistro C-UMF-004 — Orden anatasa/rutilo (r2SCAN relajado + vibración) y D3 en ΔfH
meta: {campaña: C-UMF-004, version: 1, fecha: 2026-10-20, autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial", orcid: 0000-0001-8601-1963, antecedentes: [C-UMF-002, C-UMF-003]}
objetivo: "A) ¿r2SCAN con geometría relajada más corrección vibracional reproduce ΔH(A−R)=+9.0±1.4 meV/át? B) ¿D3(BJ) sobre MatterSim mejora ΔfH de haluros en capas y el MAE global de C-UMF-002?"

## Factibilidad (decidida antes de calcular)
- F1 setups r2SCAN consistentes: probado 20-oct 17:09 UTC+2: `gpaw.atom.generator2.generate(xc=r2SCAN)` → NotImplementedError; no hay setups MGGA en /usr/share/gpaw-setups. Se usan setups PAW-PBE (misma limitación que C-UMF-003), declarada; no es desviación.
- F2 relajación: celda+posiciones con PBE (filtro de celda ASE, fmax 0.01 eV/Å, presión 0); r2SCAN y PBE en un punto sobre geometría PBE relajada. Ecut 600 eV, k como C-UMF-003 "normal", 2 procesos MPI (memoria libre ~2 GB; trabajo C-MAT-006 en curso no se toca).
- F3 HSE06 (opcional): un smoke de ≤20 min (k reducido, ecut 500); si no converge o falla, H-A5 = NO EVALUABLE.
- Tope 8 h por etapa DFT; si se supera, la hipótesis afectada = NO EVALUABLE.
- Vibración: MatterSim armónica (phonopy, supercelda rutilo 3×3×4, anatasa 3×3×1 de celda convencional ≈ 108–144 át., desplazamiento 0.01 Å, malla 20³) en la geometría experimental. ΔH_vib(298) = (ZPE + U_term(298)) anatasa − rutilo, meV/át.

## Hipótesis (umbrales fijos)
| id | enunciado | criterio PASA |
|---|---|---|
| H-A1 | r2SCAN@PBE-relajada + ΔH_vib reproduce el experimento | |ΔH − 9.0| ≤ 10 meV/át |
| H-A2 | signo correcto (rutilo más estable) con r2SCAN + ΔH_vib | ΔH > 0 |
| H-A3 | la relajación no es la causa del error de r2SCAN | |ΔE_r2SCAN(relaj) − ΔE_r2SCAN(exp, C-UMF-003 = −11.67)| ≤ 5 meV/át |
| H-A4 | la vibración es pequeña | |ΔH_vib(298)| ≤ 5 meV/át |
| H-A5 | HSE06 (geom. PBE relajada) da signo correcto | ΔE_HSE > 0 (NO EVALUABLE si F3 falla) |
| H-B1 | D3 no empeora el MAE LOOCV sin Ti (n=37, protocolo C-UMF-002 idéntico) | MAE_D3 ≤ 32.63 meV/át |
| H-B2 | D3 reduce el error medio absoluto LOOCV de MgCl2, CaI2, MgBr2 | ≤ 0.7 × 51.8 = 36.3 meV/át |
| H-B3 | ningún compuesto sin Ti empeora mucho | max |err_LOOCV,D3| ≤ 150 meV/át |
| H-REP | réplica run2 (A: DFT r2SCAN de ambas fases repetido; B: todo repetido) | dif. ≤ 1e-6 relativa / ≤ 0.01 meV/át |
Controles: C1 todas las relajaciones convergen; C2 PBE relajado reproduce ΔE PBE de C-UMF-003 ±10 meV/át (descriptivo); C3 phonons sin modos imaginarios < −0.1 THz.
D3: TorchDFTD3 (BJ, xc=pbe, cutoff 95 bohr), aplicada a compuestos, elementos y moléculas por igual, como C-UMF-003.

## Decisión
E3 si pasan H-A1, H-A2, H-B1, H-B2 y H-REP; E2 si pasa B (H-B1, H-B2) o A (H-A1, H-A2) por separado; si no, E1. Reglas aplicadas literalmente; desviaciones en sección aparte del informe.

## Referencias (verificadas por DOI en Crossref 20-oct-2026)
https://doi.org/10.1073/pnas.251534898 (calorimetría TiO2) ; https://doi.org/10.1021/acs.jpclett.0c02405 (r2SCAN) ; https://doi.org/10.1002/jcc.21759 (D3-BJ) ; https://doi.org/10.1063/1.2204597 (HSE06) ; https://doi.org/10.1016/j.scriptamat.2015.07.021 (phonopy) ; https://doi.org/10.18434/T42S31 (JANAF)
riesgos: [setups PBE con r2SCAN, memoria limitada, HSE costoso]
