---
meta:
  campana: C-VIB-002
  titulo: "κL(300 K) en RTA con phono3py y potenciales universales (MatterSim, MACE-MP-0) frente a experimento en 15 compuestos tipo blenda"
  fecha: "2026-10-21"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial"
  orcid: "0000-0001-8601-1963"
  afirmaciones: [UM-12, VP-05, UM-07]
objetivo: "Primer paso de transporte térmico del Phonon Engine (paso «propiedad térmica» de MV1): ¿predice un uMLIP sin ajuste el κL experimental a 300 K?"
datos_clave:
  materiales: [BN, BP, AlP, AlAs, AlSb, GaP, GaAs, GaSb, InP, InAs, InSb, ZnS, ZnSe, ZnTe, CdTe]
  kappa_exp_W_mK: {BN: 760, BP: 350, AlP: 90, AlAs: 98, AlSb: 56, GaP: 100, GaAs: 45, GaSb: 40, InP: 93, InAs: 30, InSb: 20, ZnS: 27, ZnSe: 19, ZnTe: 18, CdTe: 7.5}
  fuente_exp: "Tabla IV de Togo, Chaput, Tanaka, PRB 91, 094306 (2015), https://doi.org/10.1103/PhysRevB.91.094306 (arXiv:1501.00691), que cita Shindé y Goela 2006 y Steigmeier y Kudman 1966 (AlP)"
  kappa_lda_rta_togo: {BN: 648, BP: 396, AlP: 83.0, AlAs: 85.6, AlSb: 75.1, GaP: 85.5, GaAs: 31.0, GaSb: 31.8, InP: 73.8, InAs: 20.4, InSb: 12.6, ZnS: 31.0, ZnSe: 14.9, ZnTe: 18.4, CdTe: 6.28}
  metodo: "Estructura blenda (F-43m) con a inicial 5.6 Å relajada con el propio modelo (FixSymmetry + FrechetCellFilter, fmax 1e-3 eV/Å, float64). Celda convencional 8 átomos; fc2 y fc3 en supercelda 2×2×2 (64 átomos), desplazamiento 0.03 Å, sin corte de vecinos. RTA, malla 19×19×19, isótopos naturales, T=300 K. κ = traza/3."
  modelos: {principal: MatterSim-v1.0.0-5M, secundario: MACE-MP-0 medium}
hipotesis:
  H1: "MatterSim: |κ/κexp| dentro de un factor 2 en ≥11/15"
  H2: "MatterSim: media de |log10(κ/κexp)| ≤ 0.20"
  H3: "MatterSim: Spearman ρ(κ, κexp) ≥ 0.85"
  H4: "MatterSim tiene menor media |log10| que MACE-MP-0"
  H5: "MACE-MP-0: mediana de κ/κexp < 1 (subestimación por ablandamiento)"
  H6: "MatterSim frente a LDA-RTA de Togo: media |log10| ≤ 0.20"
  H_REP: "Réplica completa con MatterSim: κ idéntico (diferencia relativa ≤ 1e-6)"
controles:
  C1: "Sin modos imaginarios: ν_min > −0.05 THz en malla 19³ (excluidos los 3 acústicos en Γ); un material que falle se excluye de H1–H3 y cuenta como fallo en H1"
  C2: "Convergencia de malla en GaAs (MatterSim): |κ(25³)/κ(19³) − 1| ≤ 0.05"
regla_decision:
  E3: "H1, H2, H3, H_REP y C1 pasan"
  E2: "H_REP pasa y al menos una de H1–H3"
  E1: "resto"
riesgos: ["Valores experimentales de manual sin incertidumbre; muestras con defectos pueden bajar κexp", "2×2×2 puede ser corta para fc3 en compuestos de alto κ (BN, BP)", "RTA subestima frente a LBTE en BN/BP"]
decisiones: ["Sin LBTE ni términos de coherencia (Wigner) en esta campaña", "Ningún parámetro se ajusta tras ver resultados"]
proximo_paso: "Ejecutar run1 (MatterSim, MACE) y run2 (MatterSim) y evaluar con el evaluador congelado"
---
