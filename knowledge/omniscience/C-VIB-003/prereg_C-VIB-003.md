---
meta:
  campana: C-VIB-003
  titulo: "κL(300 K) con MatterSim-v1 y phono3py: RTA frente a LBTE (solución directa) en 15 blendas, convergencia 3×3×3 en BN/BP y atípicos, y benchmark de κ bajo en 17 sales de roca frente a experimento"
  fecha: "2026-10-27"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial"
  orcid: "0000-0001-8601-1963"
  afirmaciones: [UM-25, UM-12, VP-05, UM-07]
  campana_previa: "C-VIB-002 (prereg sha256 c1a20dd5…0b15; E3 en UM-12)"
objetivo: "Comprobar (A) si la LBTE corrige la subestimación RTA de MatterSim en blendas y si reproduce la razón LBTE/RTA de LDA de Togo et al.; (B) si la supercelda 2×2×2 está convergida para BN, BP y los atípicos ZnS/GaSb/InSb; (C) si MatterSim sin ajuste predice κL experimental en sales de roca, en particular en compuestos de κ bajo (≤3.5 W/mK)"
datos_clave:
  modelo: "MatterSim-v1.0.0-5M (float64, CPU); mismo entorno que C-VIB-002 (/workspace/omniscience_cmat003/venv_ms; ase 3.29.0, phono3py 4.8.2)"
  metodo: "Relajación con el propio modelo (FixSymmetry + FrechetCellFilter, fmax 1e-3, a0 desde radios covalentes: blenda 4/√3·Σr, sal de roca 2·Σr). Celda convencional; supercelda n×n×n (n=2 salvo parte B, n=3), desplazamiento 0.03 Å, sin corte de vecinos, fc3 compacta simetrizada. Malla 19³ centrada en Γ, isótopos naturales, T=300 K. κ = traza/3. RTA y LBTE (solución directa de phono3py) en la misma interacción. Sin corrección no analítica (NAC) ni coherencias (Wigner), igual que C-VIB-002."
  parte_A: {materiales: [BN, BP, AlP, AlAs, AlSb, GaP, GaAs, GaSb, InP, InAs, InSb, ZnS, ZnSe, ZnTe, CdTe], supercelda: "2×2×2 (64 át.)"}
  parte_B: {materiales: [BP, BN, ZnS, GaSb, InSb], supercelda: "3×3×3 (216 át., 716 desplazamientos en blenda)", orden: "BP, BN, ZnS, GaSb, InSb"}
  parte_C: {materiales: [MgO, CaO, SrO, BaO, LiF, NaF, NaCl, NaBr, NaI, KF, KCl, KBr, KI, RbCl, PbS, PbSe, PbTe], supercelda: "2×2×2 (64 át., 146 desplazamientos)", subconjunto_kappa_bajo: [BaO, NaBr, NaI, KBr, KI, RbCl, PbS, PbSe, PbTe], excluidos: {LiH: "efectos cuánticos del H y dilatación térmica grande", AgCl: "modos imaginarios armónicos en DFT", SnSe: "ortorrómbico Pnma de baja simetría: miles de desplazamientos fc3 y κ anisótropo con valores experimentales discutidos; no cabe en el presupuesto de hoy (≈5 GB RAM libres, 1 cálculo a la vez)"}}
  kappa_exp_blendas_W_mK: {BN: 760, BP: 350, AlP: 90, AlAs: 98, AlSb: 56, GaP: 100, GaAs: 45, GaSb: 40, InP: 93, InAs: 30, InSb: 20, ZnS: 27, ZnSe: 19, ZnTe: 18, CdTe: 7.5}
  fuente_exp_blendas: "Togo, Chaput, Tanaka, PRB 91, 094306 (2015), tabla IV, https://doi.org/10.1103/PhysRevB.91.094306 (misma que C-VIB-002)"
  razon_lbte_rta_lda_togo: {BN: 1.120, BP: 1.061, AlP: 1.012, AlAs: 1.014, AlSb: 1.031, GaP: 1.216, GaAs: 1.035, GaSb: 1.022, InP: 1.154, InAs: 1.235, InSb: 1.095, ZnS: 1.177, ZnSe: 1.047, ZnTe: 1.027, CdTe: 1.062}
  nota_razon: "Cociente LBTE/RTA con isótopos de la tabla IV de Togo et al. 2015 (p. ej. BN 726/648)"
  kappa_exp_sales_W_mK: {MgO: 52, CaO: 30, SrO: 10, BaO: 3, LiF: 16.1, NaF: 18.5, NaCl: 7.2, NaBr: 2.9, NaI: 1.9, KF: 7.8, KCl: 7.2, KBr: 3.4, KI: 2.8, RbCl: 2.9, PbS: 2.5, PbSe: 1.6, PbTe: 2.2}
  kappa_pbe_ha3ph_xia: {MgO: 52.1, CaO: 21.3, SrO: 9.0, BaO: 2.8, LiF: 11.3, NaF: 20.6, NaCl: 7.2, NaBr: 2.9, NaI: 1.7, KF: 5.9, KCl: 6.6, KBr: 2.2, KI: 1.3, RbCl: 1.7, PbS: 1.3, PbSe: 1.1, PbTe: 1.6}
  fuente_exp_sales: "Xia et al., Phys. Rev. X 10, 041029 (2020), tabla I (fila κL^exp y fila κ_HA^3ph PBE), https://doi.org/10.1103/PhysRevX.10.041029 (CC BY 4.0; que a su vez cita Landolt-Börnstein, Håkansson, Pettersson, El-Sharkawy, Akhmedova y otros)"
hipotesis:
  A_H1: "LBTE ≥ RTA en 15/15 blendas"
  A_H2: "|r_MS − r_Togo| ≤ 0.10 en ≥12/15, con r = κLBTE/κRTA"
  A_H3: "media |log10(κLBTE/κexp)| < media |log10(κRTA/κexp)| (misma ejecución)"
  A_H4: "LBTE dentro de factor 2 de κexp en ≥12/15"
  B_H1: "κRTA(3×3×3)/κRTA(2×2×2) en [0.85, 1.15] en ≥4/5"
  B_H2: "κLBTE(3×3×3) dentro de ±25 % de κexp en BN (760) y en BP (350), ambos"
  B_H3: "≥2 de {ZnS, GaSb, InSb} quedan dentro de factor 2 con κLBTE(3×3×3)"
  C_H1: "Sales de roca, MatterSim RTA dentro de factor 2 de κexp en ≥12/17"
  C_H2: "media |log10(κRTA/κexp)| ≤ 0.20 (17 sales)"
  C_H3: "Spearman ρ(κRTA, κexp) ≥ 0.85 (17 sales)"
  C_H4: "Subconjunto κ bajo (9): dentro de factor 2 en ≥6/9 y media |log10| ≤ 0.25"
  C_H5: "MatterSim RTA frente a κ_HA^3ph PBE de Xia: media |log10| ≤ 0.20"
  C_H6: "Subconjunto κ bajo: mediana κRTA/κexp < 1 (subestimación sin términos de 4 fonones ni dilatación)"
  C_H7: "Sales de roca: mediana κLBTE/κRTA ≤ 1.10"
controles:
  CA: "Réplica entre días: κRTA parte A frente a C-VIB-002 run1: |cociente − 1| ≤ 1e-3 en 15/15 (cambian hilos y fc3 compacta)"
  C1: "Sin modos imaginarios (ν_min > −0.05 THz en malla 19³, sin los 3 acústicos de Γ) en las 17 sales; una sal que falle se excluye de C_H1–C_H5 y cuenta como fallo en C_H1"
  C2: "Malla PbTe: |κRTA(25³)/κRTA(19³) − 1| ≤ 0.05"
  H_REP: "Réplica de PbTe, NaCl y KBr (parte C): |Δκ/κ| ≤ 1e-6 en RTA y LBTE"
  ausentes: "Todo resultado que no termine dentro del presupuesto (≈5 h de cálculo, un proceso a la vez) cuenta como ausente; una hipótesis con datos ausentes FALLA o queda NO EVALUABLE si le falta más de la mitad"
regla_decision:
  UM-25_nueva: {E3: "C_H1, C_H2, C_H3, C_H4, H_REP y C1 pasan", E2: "H_REP pasa y al menos una de C_H1–C_H4", E1: "resto"}
  UM-12: "Sigue E3 si CA pasa; si CA falla, E3 queda «en revisión». Partes A y B se anotan como alcance (no cambian el nivel)"
  VP-05: "Sigue E6 [externo]; se anota la comparación interna RTA/LBTE (era su siguiente paso)"
  UM-07: "Sigue E1: esta campaña no cubre E_form, fases competidoras ni flujo de extremo a extremo (misma convención que D6 de C-VIB-002)"
riesgos: ["Sin NAC: en sales iónicas el desdoblamiento LO-TO no se trata", "Valores experimentales de manual sin incertidumbre; PbS/PbSe son policristalinos", "3×3×3 BN ≈ 5 s por fuerza → ≈1 h solo en fuerzas", "PbTe es anarmónico (4 fonones y dilatación no incluidos)"]
decisiones: ["Ningún parámetro se ajusta tras ver resultados", "Sin MACE en esta campaña (ya se comparó en C-VIB-002)", "SnSe excluido por coste (declarado antes de calcular)"]
proximo_paso: "Congelar código y evaluador (sha256), lanzar run_all.sh en segundo plano y evaluar"
---
