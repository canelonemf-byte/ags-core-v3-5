# Resultados C-UMF-003
meta: {autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial", orcid: 0000-0001-8601-1963, nivel_E: E2, registro: UM-20}
datos_clave:
  A_dE_AR_meV_at: {ref: "+9.0 ± 1.4 (doi:10.1073/pnas.251534898)", PBE: -29.7, PBE_U4: -9.9, r2SCAN: -11.7}
  B_dV_capas_sinD3_conD3: {MgCl2: "+10.7/-0.7 %", CaI2: "+15.6/-1.1 %", MgBr2: "+20.1/+0.9 %", media: "15.4/0.9 %"}
  B_densos_media: "3.2 % sin D3 / 1.5 % con D3 (máx. NaCl -3.4 %)"
hipotesis: {H-A1: PASA, H-A2: FALSADA, H-A3: FALSADA, H-A4: FALSADA (mejor |Δ| 18.9), H-A5: FALSADA, H-B1: PASA, H-B2: PASA (-94 %), H-B3: PASA, H-REP: PASA (2e-8 meV, 0 % V)}
decision: "E2: pasan todas las principales de la parte B; ninguna de A. No E3 por H-A2/H-A4."
desviaciones: "ninguna (kpts y ecut del prereg completos; r2SCAN convergió y se replicó)"
lectura: "Con geometría experimental fija, ni PBE+U(4 eV) ni r2SCAN con PAW de PBE invierten el orden; reducen el error de 39 a ~19-21 meV/át. D3(BJ) sobre MatterSim corrige los haluros en capas sin dañar los densos."
figura: figs/fig_cumf003.png
