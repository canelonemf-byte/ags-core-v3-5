---
meta:
  campana: C-VIB-004
  titulo: "κL(300 K) de 17 sales de roca con MatterSim-v1 y phono3py RTA a la constante de red experimental de 300 K: ¿corrige la sobreexpansión del modelo la subestimación de κ bajo?"
  fecha: "2026-10-29"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial"
  orcid: "0000-0001-8601-1963"
  afirmaciones: [UM-25, UM-12, VP-05]
  campana_previa: "C-VIB-003 (prereg sha256 66275ff6…ac1f; UM-25 E2)"
objetivo: "Comprobar si fijar la red de MatterSim-v1 en a_exp(300 K) (en vez de la red relajada del modelo, 0.6–1.8 % mayor) basta para que κL RTA de 17 sales de roca quede dentro de factor 2 del experimento, sobre todo en las 9 de κ bajo, y separar este efecto de artefactos numéricos (amplitud de desplazamiento, malla, réplica)"
datos_clave:
  motivacion: "En C-VIB-003 MatterSim relajado subestima κ bajo (mediana κ/κexp 0.239) y queda muy por debajo incluso de PBE-HA de Xia et al. 2020 (p. ej. KBr 0.217 frente a 2.2). En la tabla I de Xia et al. la suma SCPH+4 fonones queda cerca de HA+3 fonones en sales (p. ej. KBr 2.2→2.0, PbTe 1.6→1.7), así que añadir 4 fonones/SCPH no explicaría un factor 4–15; la hipótesis de trabajo es el ablandamiento de la superficie de energía del modelo, en parte por red sobreexpandida (a_rel − a_exp: NaCl +1.1 %, KBr +1.6 %, PbTe +1.6 %)."
  modelo: "MatterSim-v1.0.0-5M (float64, CPU); entorno /workspace/omniscience_cmat003/venv_ms (phono3py 4.8.2, phonopy 4.8.3, torch 2.14.1) con ase 3.29.0 reinstalado en /workspace/omniscience_cvib004/pylib (PYTHONPATH) porque ase/build falta en el venv compartido (D1)"
  metodo: "Celda convencional de sal de roca construida directamente con a = a_exp (posiciones fijadas por simetría Fm-3m, sin relajar). Supercelda 2×2×2 (64 át., 146 desplazamientos), desplazamiento 0.03 Å, fc3 compacta simetrizada, malla 19³ centrada en Γ, isótopos naturales, T=300 K, RTA, κ = traza/3, 4 hilos, un proceso a la vez. Misma receta que C-VIB-003 salvo red fija y sin LBTE. Se registra la presión MatterSim a a_exp."
  materiales: [MgO, CaO, SrO, BaO, LiF, NaF, NaCl, NaBr, NaI, KF, KCl, KBr, KI, RbCl, PbS, PbSe, PbTe]
  subconjunto_kappa_bajo: [BaO, NaBr, NaI, KBr, KI, RbCl, PbS, PbSe, PbTe]
  a_exp_300K_A: {MgO: 4.212, CaO: 4.81, SrO: 5.16, BaO: 5.520, LiF: 4.03, NaF: 4.63, NaCl: 5.64, NaBr: 5.97, NaI: 6.47, KF: 5.34, KCl: 6.29, KBr: 6.60, KI: 7.07, RbCl: 6.59, PbS: 5.9362, PbSe: 6.1273, PbTe: 6.4620}
  fuentes_a_exp: ["Haluros alcalinos, MgO, PbS, PbTe: tabla «Lattice constants for various materials at 300 K», https://en.wikipedia.org/wiki/Lattice_constant (MgO, PbS, PbTe con referencias APS/SPI; haluros sin referencia individual: riesgo declarado)", "CaO 4.81, SrO 5.16, BaO 5.520: tabla 1 (columna Expt.) de Roshan et al., arXiv:2110.13857, https://arxiv.org/html/2110.13857v1", "PbSe 6.127348 Å a 300.0 K: tabla 1 de Mater. Adv. 2022, DOI 10.1039/D1MA01093J, https://pubs.rsc.org/en/content/articlehtml/2022/ma/d1ma01093j"]
  kappa_exp_W_mK: "las mismas 17 de C-VIB-003 (Xia et al., PRX 10, 041029 (2020), tabla I, https://doi.org/10.1103/PhysRevX.10.041029)"
  kappa_pbe_ha3ph_xia: "las mismas de C-VIB-003"
  base_relajada: "C-VIB-003/out/rs/mattersim_*_sc2_m19.json (κ RTA a red relajada, mismo modelo)"
  no_incluido: {NAC: "MatterSim no da cargas de Born ni ε∞ y hoy no se ha abierto una fuente única verificada de Z* y ε∞ para las 17 sales; se aplaza", cuatro_fonones_SCPH: "phono3py no calcula 4 fonones; SCPH/TDEP con MD no cabe en ≈2 GB de RAM libre con el presupuesto de hoy; además Xia et al. muestran compensación parcial SCPH↔4ph en sales", LBTE: "omitida: en C-VIB-003 LBTE/RTA mediana 1.07 en sales"}
hipotesis:
  H1: "A a_exp, κRTA dentro de factor 2 de κexp en ≥12/17"
  H2: "Media |log10(κRTA/κexp)| ≤ 0.20 (17 sales)"
  H3: "Spearman ρ(κRTA, κexp) ≥ 0.85"
  H4: "Subconjunto κ bajo (9): dentro de factor 2 en ≥6/9 y media |log10| ≤ 0.25"
  H5: "Dirección física: κ(a_exp)/κ(a_rel) > 1 en ≥15/17 y mediana > 1.2"
  H6: "Subconjunto κ bajo: mediana κ(a_exp)/κexp ≥ 0.50 (frente a 0.239 en C-VIB-003)"
  H7: "Frente a κ_HA^3ph PBE de Xia: media |log10| ≤ 0.20"
  B_H1: "Robustez numérica en KBr, KI, RbCl, NaI, PbTe a a_exp: |κ(d=0.01 Å)/κ(d=0.03 Å) − 1| ≤ 0.10 en ≥4/5"
controles:
  C1: "Sin modos imaginarios (ν_min > −0.05 THz en malla 19³, sin los 3 acústicos de Γ) a a_exp; una sal que falle se EXCLUYE de H1–H4, H6, H7 (el evaluador lo aplica) y cuenta como fallo en H1"
  C2: "Malla PbTe a a_exp: |κ(25³)/κ(19³) − 1| ≤ 0.05 (repite el control fallido de C-VIB-003)"
  H_REP: "Réplica de PbTe, NaCl y KBr a a_exp en proceso aparte: |Δκ/κ| ≤ 1e-6"
  CA: "Reproducción entre días a red relajada (NaCl, KBr) frente a C-VIB-003/out/rs: |cociente − 1| ≤ 1e-3 en 2/2 (cambian hilos y ase reinstalado)"
  ausentes: "Presupuesto ≈2.5 h; todo lo que no termine cuenta como ausente; una hipótesis con más de la mitad de datos ausentes queda NO EVALUABLE y falla"
regla_decision:
  UM-25: {E3: "H1, H2, H3, H4, H_REP, C1 y CA pasan → E3 para la afirmación reformulada «MatterSim-v1 a a_exp(300 K) con RTA phono3py 2×2×2 predice κL de sales de roca»; la variante a red relajada queda documentada como E2", E2: "H_REP pasa y al menos una de H1–H4", E1: "resto"}
  UM-12: "Sin cambio (blendas); se anota si CA falla"
  VP-05: "Sigue E6 [externo]; se anota la sensibilidad de κ RTA al volumen"
riesgos: ["a_exp de haluros alcalinos con 2–3 cifras y sin referencia primaria individual en la tabla usada", "Fijar a_exp introduce un dato experimental: deja de ser predicción pura del modelo", "Sin NAC ni 4 fonones", "La prueba de humo de NaCl (malla 7³) ya indicó un aumento de κ a a_exp: declarado en D1"]
decisiones: ["Ningún parámetro se ajusta tras ver resultados", "Evaluador congelado (sha256) antes de calcular", "Orden: A (17 sales a_exp) → REP → C2 → CA → B"]
proximo_paso: "Congelar prereg, código y evaluador con sha256 y lanzar run_all.sh con nohup"
---
