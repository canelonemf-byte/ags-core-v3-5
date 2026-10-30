# Resultados C-VIB-004 — κL de 17 sales de roca con MatterSim a la red experimental
```yaml
meta: {campana: C-VIB-004, fecha: "2026-10-29", zona: Europe/Madrid, autor: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial", orcid: 0000-0001-8601-1963, prereg_sha256: 901c5eecf74920ec17e655403153c5ed6426179e3486b6806fc60f4cdbc63193, evaluador_sha256: 132b65f131871d55532669ba563e5b21df65e6df0397df0e1ac02a38350f5a1f, runner_sha256: 05516214860b62b89d484a5e3a58e2c23395b37020277d4a6a0eba905629165e, congelado: "2026-10-29T09:06:58+01:00", ejecucion: "09:07–09:35", resultados: results.json}
objetivo: "Comprobar si evaluar κL(300 K) en a_exp (en vez de la red relajada por MatterSim, 0.6–1.8 % mayor) corrige la subestimación de κ bajo de UM-25"
metodo: "MatterSim-v1.0.0-5M float64 CPU; phono3py 4.8.2 RTA; 2×2×2 convencional (64 át., 146 desplazamientos, 0.03 Å); malla 19³; isótopos naturales; 300 K; sin NAC ni 4 fonones"
datos_clave:
  presion_a_aexp_GPa: "0.41–5.08"
  kappa_aexp_vs_arel: "16/17 aumentan, mediana ×1.551 (KBr ×6.4, PbTe ×3.6, PbSe ×3.6; KI ×0.043)"
  H1: "13/17 dentro de factor 2 — PASA (antes 9/17)"
  H2: "media |log10| 0.276 > 0.20 — FALLA (antes 0.388)"
  H3: "Spearman 0.888 ≥ 0.85 — PASA (antes 0.904)"
  H4: "κ bajo 5/9 y media 0.439 — FALLA (antes 2/9, 0.595)"
  H5: "16/17 > 1, mediana 1.551 — PASA"
  H6: "mediana κ/κexp κ bajo 0.696 ≥ 0.50 — PASA (antes 0.239)"
  H7: "frente a PBE-HA de Xia 0.233 > 0.20 — FALLA (antes 0.29)"
  B_H1: "d 0.01/0.03 en ±10 % en 4/5 — PASA (KI ×2.0 falla)"
  H_REP: "réplica PbTe/NaCl/KBr idéntica (0.0) — PASA"
  C1: "sin ν_min < −0.05 THz a d=0.03 — PASA (KI +0.022, marginal)"
  C2: "PbTe 25³/19³ +1.55 % — PASA (antes +5.65 %)"
  CA: "NaCl/KBr relajados reproducen C-VIB-003 (2.9e-4, 0) — PASA"
  fuera_factor2: {NaI: 0.454, KBr: 0.41, KI: 0.006, RbCl: 0.319}
  exploratorio_sin_KI: "media |log10| 0.156, 13/16 (post hoc, no decisorio)"
tareas: []
riesgos: ["KI inestable marginalmente en MatterSim (ν_min −0.355 THz con d=0.01)", "a_exp de 300 K mezcla dilatación térmica real con error del modelo; no separa ambos", "sin NAC ni 4 fonones"]
decisiones: ["Regla prerregistrada: H_REP y H1/H3 pasan pero H2 y H4 fallan → UM-25 sigue E2", "UM-12 sin cambio (CA pasa)", "VP-05 sigue E6 con nota de sensibilidad al volumen"]
originalidad: {grado: parcial, fuentes: ["https://arxiv.org/abs/2509.03401", "https://arxiv.org/abs/2408.00755", "https://www.nature.com/articles/s41524-024-01500-6", "https://arxiv.org/html/2110.13857v1", "https://doi.org/10.1103/PhysRevX.10.041029"]}
proximo_paso: "C-VIB-005: diagnosticar KI/KBr/RbCl (fonones TA en X/L frente a INS, barrido de volumen ±1 %) y probar corrección de ablandamiento (escalado lineal de fuerzas o ajuste fino con pocos puntos DFT) frente a a_exp"
```
