# Resultados C-VIB-005 — barrido de red ±1 % alrededor de a_exp con MatterSim-v1
```yaml
meta: {campana: C-VIB-005, fecha: "2026-10-30", zona: Europe/Madrid, autor: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial", orcid: 0000-0001-8601-1963, prereg_sha256: 32f5607798a22b8686089ce7be9c08916e813a52e32e50e5e9d716b6b2f0b215, evaluador_sha256: fe470166ca2e919812ef4b1ba105056cd7c3cef86dbf47e5079b120ca78c40ab, runner_sha256: 9dfd5e82d66a6757d19716e1325f954cf8a997db38041cfeb8f2c009eef1af4a, congelado: "2026-10-30T09:05:37+01:00", ejecucion: "09:11–09:35 (tras D1)", resultados: results.json}
objetivo: "Separar si la subestimación residual de κL en NaI/KBr/RbCl a a_exp es volumétrica o ablandamiento intrínseco de MatterSim-v1"
metodo: "Receta de C-VIB-004 con a = a_exp × {0.99, 1.01}; 11 sales; s=1.00 de C-VIB-004"
datos_clave:
  H1: "monotonía κ(0.99)>κ(1.00)>κ(1.01) en 9/11 — FALLA (KBr no monótono: 0.976 / 1.395 / 0.319; KI inestable a 1.01)"
  H2_KI: "a 0.99·a_exp KI es estable (ν_min +0.145/+0.145 THz con d 0.03/0.01) y robusto (×0.964), pero κ 0.283 = 0.10·κexp — FALLA"
  H3: "compresión necesaria para κexp: KBr −2.66 %, RbCl −1.81 %, NaI −0.86 % → 2/3 > 1 % — PASA (enunciado a)"
  H4: "g = −dlnκ/dlnV en [2,20] en 7/10 — FALLA; mediana 15.7; NaI 31.6, PbSe 24.4, PbTe 20.6"
  CA: "NaCl a_exp reproduce C-VIB-004 (−8.7e-5) — PASA"
  g_por_sal: {MgO: 7.3, BaO: 8.8, NaCl: 9.9, PbS: 11.8, NaBr: 12.9, RbCl: 18.5, KBr: 18.7, PbTe: 20.6, PbSe: 24.4, NaI: 31.6}
  lectura: "El κL RTA de MatterSim en sales pesadas es extremadamente sensible al volumen: ±1 % de red cambia κ entre ×2 y ×4 (PbSe ×4.3). Por eso el acierto de C-VIB-004 a a_exp no es robusto: depende de un dato de red con 2–3 cifras. KI solo es estable comprimido y aun así queda en 0.10·κexp: ablandamiento intrínseco, no volumen."
tareas: []
riesgos: ["Ajuste lnκ–ln a con 3 puntos; KBr no monótono invalida su extrapolación", "Sin comparación cuantitativa aún con κ(P) experimental (Andersson y Bäckström 1985)", "Sin NAC ni 4 fonones"]
decisiones: ["Regla prerregistrada: H1 y H4 fallan → UM-26 E1 (enunciado a)", "UM-25 sigue E2 con nota de fragilidad volumétrica", "Nada subido a repositorios"]
originalidad: {grado: parcial, fuentes: ["https://www.osti.gov/biblio/2528028", "https://arxiv.org/html/2610.29634", "https://arxiv.org/abs/2509.03401", "https://doi.org/10.1103/physrevb.110.035205", "https://ar5iv.labs.arxiv.org/html/2110.13857", "https://doi.org/10.1088/0022-3719/18/20/020"], nota: "El ablandamiento de uMLIP y la sensibilidad de κ a la red son conocidos; no se encontró la medida prerregistrada del parámetro tipo Bridgman de MatterSim ni de la compresión necesaria en estas sales"}
proximo_paso: "C-VIB-006: comparar g del modelo con κ(P) experimental de Andersson y Bäckström (KBr, KI, RbCl) y probar un escalado de fc2/fc3 o ajuste fino ligero con pocos puntos DFT"
```
