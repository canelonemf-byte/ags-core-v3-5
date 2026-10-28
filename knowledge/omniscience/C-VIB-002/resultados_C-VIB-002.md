# Resultados C-VIB-002 · κL(300 K) RTA, 15 blendas
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963
Fecha: 2026-10-26 13:40 (UTC+1). Prereg sha256 c1a20dd5…0b15 (sin cambios). Evaluador cvib002_eval.py sha256 5dd768aa…2875 verificado, ejecutado sin cambios con venv_ms. Datos: results.json, eval.log. Desviaciones D1–D6 en desviaciones.md.

## Veredicto: **E3** (H1, H2, H3, H_REP y C1 pasan)
| Hipótesis | Valor | Pasa |
|---|---|---|
| H1 MatterSim dentro de factor 2 (≥11/15) | 12/15 | sí |
| H2 media \|log10(κ/κexp)\| ≤ 0.20 | 0.149 | sí |
| H3 Spearman ≥ 0.85 | 0.889 | sí |
| H4 MatterSim mejor que MACE | 0.149 vs 0.227 | sí |
| H5 MACE mediana κ/κexp < 1 | 0.578 | sí |
| H6 MatterSim vs LDA-RTA Togo ≤ 0.20 | 0.131 | sí |
| H_REP réplica (≤1e-6) | 0.0 | sí |
| C1 sin modos imaginarios | 0 excluidos | sí |
| C2 malla 25³ GaAs (≤5 %) | 4.16 % | sí |
MACE-MP-0 dentro de factor 2: 11/15.

## κ (W/mK) MatterSim / MACE / exp
BN 585.9/319.1/760 · BP 338.9/202.2/350 · AlP 91.8/27.8/90 · AlAs 98.6/102.4/98 · AlSb 34.5/42.3/56 · GaP 86.0/125.6/100 · GaAs 29.0/23.6/45 · GaSb 17.0/19.5/40 · InP 52.9/88.4/93 · InAs 30.2/15.2/30 · InSb 9.6/7.0/20 · ZnS 54.6/36.6/27 · ZnSe 20.1/16.3/19 · ZnTe 12.9/28.4/18 · CdTe 4.6/3.9/7.5
Fuera de factor 2 (MatterSim): ZnS ×2.02, GaSb ×0.43, InSb ×0.48. Tendencia general a subestimar en compuestos pesados (Ga/In–Sb, CdTe).

## Registro
UM-12 E0→E3 (alcance: benchmark en materiales conocidos). UM-07 sigue E1 con nota «paso κL verificado E3» (D6). VP-05 anota implementación interna. Backups *_C-VIB-002_20261026_1340.

## Límites
RTA sin LBTE ni coherencias; supercelda 2×2×2 (corta para BN/BP); κexp de manual sin incertidumbre.

## Originalidad: parcial
El benchmark de κ con uMLIP frente a DFT ya está publicado: Póta, Ahlawat, Csányi, Simoncelli, arXiv:2408.00755 (https://arxiv.org/abs/2408.00755). κexp y LDA-RTA de referencia: Togo, Chaput, Tanaka, PRB 91, 094306 (2015), https://doi.org/10.1103/PhysRevB.91.094306. Aporte propio: MatterSim-v1 frente a κ experimental con prerregistro, réplica idéntica y control de malla.
