---
meta:
  campana: C-VIB-005
  titulo: "Diagnóstico de la subestimación residual de κL en haluros alcalinos pesados con MatterSim-v1: barrido de red ±1 % alrededor de a_exp(300 K)"
  fecha: "2026-10-30"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial"
  orcid: "0000-0001-8601-1963"
  afirmaciones: [UM-25, "UM-26 (nueva)"]
  campana_previa: "C-VIB-004 (prereg sha256 901c5eec…3193; UM-25 E2; fuera de factor 2: NaI 0.454, KBr 0.41, KI 0.006, RbCl 0.319)"
objetivo: "Separar si la subestimación residual de κL en NaI, KBr y RbCl (y la inestabilidad de KI) a a_exp se debe a sensibilidad volumétrica (se arreglaría con ≤1 % de compresión de red) o a ablandamiento intrínseco de la superficie de energía de MatterSim-v1"
datos_clave:
  metodo: "Receta idéntica a C-VIB-004 (MatterSim-v1.0.0-5M float64 CPU, phono3py RTA, 2×2×2 convencional, d=0.03 Å, malla 19³, isótopos, 300 K, sin NAC ni 4 fonones) con a = a_exp × s, s ∈ {0.99, 1.01}; el punto s=1.00 se toma de C-VIB-004/results.json"
  materiales: [KBr, KI, RbCl, NaI, NaBr, BaO, PbS, PbSe, PbTe, NaCl, MgO]
  magnitudes: {g: "−dlnκ/dlnV por diferencia central entre s=0.99 y s=1.01 (parámetro tipo Bridgman del modelo)", da_needed_pct: "compresión de red que llevaría κ a κexp, por ajuste lineal de lnκ frente a ln a con los 3 puntos"}
  kappa_exp: "Xia et al., PRX 10, 041029 (2020), tabla I (las de C-VIB-004)"
  referencias_experimentales_presion: ["Andersson y Bäckström, J. Phys. C 18, 3943 (1985), https://doi.org/10.1088/0022-3719/18/20/020 (κ(P) de KCl, KBr, KI, RbCl…)", "NaCl y NaI bajo presión, J. Phys. Chem. Solids (1986), https://doi.org/10.1016/0022-3697(86)90025-9"]
hipotesis:
  H1: "Dirección física: κ(0.99) > κ(1.00) > κ(1.01) en ≥10/11"
  H2_KI: "A 0.99·a_exp KI es estable (ν_min > −0.05 THz con d=0.03 y d=0.01), |κ(d0.01)/κ(d0.03) − 1| ≤ 0.10 y κ/κexp ≥ 0.25"
  H3: "Diagnóstico: en ≥2/3 de NaI, KBr, RbCl la compresión necesaria para alcanzar κexp supera el 1 % de red (da_needed_pct < −1.0) → ablandamiento intrínseco; si falla, el residuo es volumétrico"
  H4: "Plausibilidad: g ∈ [2, 20] en ≥80 % de las sales estables en los 3 puntos (≥6 sales); cota amplia fijada a priori por el autor, no tomada de literatura"
controles:
  CA: "NaCl a s=1.00 recalculado hoy reproduce C-VIB-004 en |cociente − 1| ≤ 1e-3"
  C1: "ν_min > −0.05 THz se registra para cada punto; las sales no estables en los 3 puntos se excluyen de H4"
  ausentes: "Topes: 30 min por barrido, 6 min CA y B; lo ausente cuenta como fallo"
regla_decision:
  UM-26: "E2 si CA, H1 y H4 pasan; el enunciado (a: ablandamiento intrínseco / b: dominado por volumen) lo elige H3. E1 en otro caso. E3 exigirá confirmación independiente (otro uMLIP o DFT, o κ(P) experimental de Andersson y Bäckström)."
  UM-25: "Sin cambio de nivel (E2); se anota H2_KI"
riesgos: ["Ajuste lineal en lnκ–ln a con solo 3 puntos; extrapolar más allá de ±1 % es aproximado", "KI puede seguir inestable", "Memoria libre ≈2.3 GB"]
decisiones: ["Ningún parámetro se ajusta tras ver resultados", "Evaluador y runner congelados con sha256 antes de calcular", "Nada se sube a repositorios"]
proximo_paso: "Congelar y lanzar run_all.sh"
---
