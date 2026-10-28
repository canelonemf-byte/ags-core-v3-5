# Resultados C-NANO-002 — Fonones de monocapas 2D con MatterSim y S_vib monocapa vs. masivo
meta:
  id: C-NANO-002
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963"
  fecha: "2026-10-22 (Europe/Madrid)"
  prerregistro: "prereg_C-NANO-002.FROZEN.md, sha256 3f4ceeaa7e8693029e13e16a964382da74f85da83351387eec15f47e496cdc46, congelado 2026-10-22 09:15:25 CEST, antes de cualquier cálculo de frecuencias o entropías"
  codigo: "code_freeze.sha256 (nano2_run.py, nano2_eval.py, gpaw_grafeno.py, guardia.py); fig.py escrito después (solo dibujo; code_freeze_fig_posterior.sha256)"
  salidas: "out/run1, out/run2 (mattersim, mattersim_d3), out/run1/mace, out/gpaw; results.json (sha256 3a43e88f…8328); eval.log"
  licencia: "CC BY 4.0"
objetivo: "Avanzar NANO-04 (frecuencias Γ/M/K de monocapas con MatterSim) y NANO-05 (S_vib(298) monocapa − masivo, efecto D3) con hipótesis cuantitativas prerregistradas."
datos_clave:
  H1_gamma_DFT: "PASA (run1 y run2). 1/8 fuera de ±5 %: h-BN ZO 772.2 vs 819.37 cm⁻¹ (−5.8 %). Resto: grafeno ZO 871.4/881 (−1.1 %), LO/TO 1564.5/1554 (+0.7 %); h-BN LO/TO 1335.7/1363.88 (−2.1 %); MoS2 E'' 276.0/289.2 (−4.6 %), E' 372.7/391.7 (−4.9 %), A1' 392.4/410.3 (−4.4 %), A2'' 458.7/476.0 (−3.6 %). MoS2 sistemáticamente blando ~4 %."
  H2_grafeno_MK: "FALLA (run1 y run2). 3/9 fuera de ±5 %: M ZA 407.5/471 (−13.5 %), M TA 667.9/626 (+6.7 %), K ZA 506.6/535 (−5.3 %). Dentro: M ZO −3.4 %, M LA +0.3 %, M LO +1.2 %, M TO +0.9 %, K TA +2.9 %, K LA/LO +1.7 %. Informativo K TO 1385.4 vs 1288 (+7.6 %): MatterSim no reproduce el ablandamiento por anomalía de Kohn."
  H3_raman_exp: "PASA. G grafeno 1564.5 vs 1580 (−1.0 %); E2g h-BN 1335.7 vs 1368 (−2.4 %); E' MoS2 372.7 vs 384 (−2.9 %)."
  H4_ZA: "PASA. n = 2.04 (grafeno), 2.07 (h-BN), 1.82 (MoS2) en run1; run2 2.11, 2.18, 1.82. Sin regla de suma rotacional y sin modos imaginarios en la ventana."
  H5_dS: "PASA. ΔS = S_mono − S_masivo(MS+D3) = 0.092 (grafeno/grafito), 0.096 (h-BN), 0.117 (MoS2) k_B/át (run2: 0.098, 0.088, 0.113). Todas en el extremo bajo de la banda 0.05–0.6."
  H6_efecto_D3: "FALLA. |ΔS(MS+D3) − ΔS(MS)| = 0.079 (grafeno), 0.092 (h-BN), 0.107 (MoS2) k_B/át; MoS2 ≥ 0.1 (run2 0.104). Sin D3, MatterSim casi no liga las capas (c: grafito 8.39 vs 6.82 Å con D3; h-BN 8.22 vs 6.45; 2H-MoS2 15.23 vs 12.15) y ΔS colapsa a ~0.00–0.02: el D3 es el que crea la diferencia monocapa/masivo."
  H_REP: "FALLA (por un componente). Frecuencias run2 vs run1: máx 0.075 % (≤1 %); entropías máx 0.007 k_B/át (≤0.02); veredictos H1–H6 idénticos; pero |Δn_ZA| máx = 0.104 (h-BN 2.07→2.18) > 0.10."
  C1_GPAW: "PASA. GPAW PBE Γ grafeno en la red MS: ZO 868.2, LO/TO 1560.8 cm⁻¹ (media 1551.0/1570.6, sin simetrizar); MatterSim −0.4 %/+0.2 % de diferencia. Acústico ZA de GPAW −71 cm⁻¹ (ruido de rejilla, excluido como acústico)."
  C2_MACE: "Informativo: MACE-MP-0 medium sistemáticamente blando ~20–30 % (grafeno ZO −24 %, LO/TO −20 %; h-BN −25 %; MoS2 E' −25 %); H1–H4 FALLAN; ZA de MoS2 imaginaria en la ventana."
  C3_JANAF: "PASA. S298 MS+D3: grafito 0.7034 vs 0.6904 k_B/át (+1.9 %); h-BN 0.9171 vs 0.8897 (+3.1 %)."
  nivel_regla_literal: "NANO-04: H_REP FALLA → E1 (sin cambio). NANO-05: H_REP FALLA → E1 (E0→E1)."
  analisis_posterior_no_registrado: "Si se excluyera el exponente ZA de H_REP, la réplica pasaría y la regla daría E3 a ambas (C1 y C3 pasan). No se aplica: queda como motivo para C-NANO-003 con criterio de ajuste ZA más robusto."
originalidad:
  clasificacion: "parcial"
  hallazgos: ["Loew et al. 2025, npj Comput. Mater. 11, 178, https://doi.org/10.1038/s41524-025-01650-1 (≈10 000 fonones de cristales masivos, 7 uMLIP; MatterSim entre los mejores)", "Anam et al. 2025, https://arxiv.org/abs/2509.03401 (2429 cristales OQMD, IFC y conductividad)", "Uni2D, https://arxiv.org/abs/2506.07043 (potencial específico 2D con fonones C2DB/MC2D)", "https://arxiv.org/html/2508.15614 (uMLIP en sistemas 0D–3D: energías y geometrías)", "https://arxiv.org/html/2606.22234v1 (MLIP afinados para 2D retorcidos)"]
  conclusion: "Los benchmarks de fonones con uMLIP ya existen (masivos) y hay potenciales 2D dedicados; no hallé un contraste prerregistrado de MatterSim/MACE para modos ZA/M/K de grafeno, h-BN y MoS2 monocapa con control DFT y réplica, ni la prueba ΔS monocapa−masivo con/sin D3. Búsqueda de patentes sin resultado relevante."
tareas: ["C-NANO-003: criterio ZA robusto (regla rotacional o ajuste en ventana fija con varios desplazamientos)", "Dispersiones completas con referencia IXS", "MoS2 masivo vs referencia entrópica medida"]
riesgos: ["Referencias DFT con funcionales distintos (GGA/LDA)", "Superceldas masivas 3×3×2/3×3×1", "D3 con corte 40 bohr", "S° JANAF vs armónica a volumen fijo"]
decisiones: ["Evaluación tal cual el prerregistro; niveles por regla literal", "Desviaciones en desviaciones.md"]
proximo_paso: "Prerregistrar C-NANO-003: misma batería con regla de suma rotacional (o ajuste ZA con 3 amplitudes) y tolerancia ZA declarada; añadir WS2/MoSe2 y referencia IXS de grafito M/K."
