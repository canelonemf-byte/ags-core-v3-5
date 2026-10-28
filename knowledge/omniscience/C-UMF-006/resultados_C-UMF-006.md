# Resultados C-UMF-006 (prereg sha256 82efeb0c…a2, congelado 2026-10-21 12:07:02 UTC+2) — CERRADA 22-oct-2026
autoria: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963
meta: {campana: C-UMF-006, nivel_E: E1, estado: cerrada; parte A NO EVALUABLE (tope 5 h y memoria)}
datos_clave:
  B_MatterSim: "rutilo evaluable_con_regla (f_imag 0.0093), anatasa normal; ΔZPE +2.66, ΔU_vib(298) +1.71, ΔF_vib(298) +5.44 meV/át (A−R)"
  B_MACE: "ΔZPE +3.75, ΔU_vib +2.35, ΔF_vib +6.71 meV/át"
  HB1: PASA · HB2: "PASA (|1.71| ≤ 5): el −47.9 de C-UMF-004 era artefacto de modos imaginarios"
  H_REP_i: "PASA (|2.35 − 1.71| = 0.64 ≤ 3)"
  A_PBE_gamma: "ΔE Γ-supercelda PBE −58.2 meV/át (k-convergido −30.7): error de tamaño grande, se usa solo como diferencia"
  A_hibrido: "PBE0-TC anatasa en curso: 1.er paso SCF 928 s con 6 MPI; previsiblemente supera el tope de 5 h → HA1–HA3 NO EVALUABLE si no termina"
desviaciones: ["HSE06 inviable (OOM con RI-HFXk; requisito BvK ≥ 32 Å) → PBE0-TC, declarado antes de calcular"]
proximo_paso: "run_a.sh sigue en nohup y reevalúa al terminar; si HA no es evaluable, HSE06 requiere cluster"
figura: figs/C-UMF-006_vib.png
