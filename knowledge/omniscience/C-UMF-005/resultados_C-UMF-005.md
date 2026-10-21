# Resultados C-UMF-005 (prereg sha256 9bcb51e0…6121, congelado 20-oct-2026 20:40:14 UTC+2)
autoria: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963
## A. ΔE(anatasa−rutilo) meV/át, CP2K GTH-SCAN + TZV2P-MOLOPT-SCAN (experimento +9.0±1.4)
r2SCAN 1000 Ry -13.7 (réplica -13.7; 1200 Ry -13.3) · PBE CP2K -30.7 (GPAW −30.5) · GPAW r2SCAN con PAW-PBE −11.8
## B. D3 selectivo (regla R-dim)
marcados: ['CaI2', 'MgBr2', 'MgCl2'] · MAE LOOCV 53.1 (base 32.6, D3 global 38.0) · capas 190.9 (base 51.8) · máx 225.1 (CaI2) · test Ti 73.3
## Hipótesis
{"H-A1": "FALLA", "H-A2": "FALLA", "H-A3": "FALLA", "H-B1": "FALLA", "H-B2": "FALLA", "H-B3": "FALLA", "H-B4": "FALLA", "H-REP": "PASA"}
controles: C-A1 True · C-A2 True
nivel: **E1**
## Desviaciones y notas
- Antes de congelar el código, el smoke F-A1 falló dos veces por sintaxis del input (anidado &XC; en CP2K 2026 los funcionales libxc van como subsecciones MGGA_X_R2SCAN/MGGA_C_R2SCAN); corregido, el smoke convergió en 22 pasos (20:45 UTC+2).
- El fichero BASIS_MOLOPT_UZH_2026.2 instalado (sha256 8ca61714…) difiere del descargado (dd2a387f…), pero las entradas Ti y O TZV2P-MOLOPT-SCAN/PBE son idénticas; se usa el instalado.
- R-dim usa el atributo dimtype del intervalo de mayor puntuación de ASE (marca si dimtype ≠ "3D").
figura: figs/C-UMF-005_resumen.png · referencias: ver prereg (DOI)
