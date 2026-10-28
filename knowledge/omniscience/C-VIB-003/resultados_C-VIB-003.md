# Resultados C-VIB-003
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963

```yaml
meta: {campana: C-VIB-003, prereg_sha256: "66275ff6e4483b5b28e0ffd6b0c502396c6e8271dc45c5f83f6588e1f8bbac1f", evaluador_sha256: "2da18e72ca6fc5b766382bddfe9077e0d17acd1334f68a77852d8b1a3955f7ee", calculo_fin: "2026-10-27T17:27+01:00", evaluado: "2026-10-27T17:29+01:00", cerrado_registro: "2026-10-28 09:15 UTC+1", datos: "results_final.json, eval_final.log"}
objetivo: "RTA frente a LBTE en 15 blendas, convergencia 3×3×3 y benchmark κ en 17 sales de roca con MatterSim-v1"
datos_clave:
  parte_A: {A_H1: "14/15 FALLA (GaSb LBTE/RTA 0.986)", A_H2: "12/15 PASA", A_H3: "0.134 < 0.149 PASA", A_H4: "13/15 PASA", fuera_factor2_lbte: [GaSb, ZnS], CA: "6.6e-4 PASA"}
  parte_B: {B_H1: "4/5 PASA (ZnS 0.823)", B_H2: "PASA (BN 686/760, BP 375/350)", B_H3: "PASA (ZnS, InSb)"}
  parte_C: {C_H1: "9/17 FALLA", C_H2: "0.388 FALLA", C_H3: "0.904 PASA", C_H4: "2/9, 0.595 FALLA", C_H5: "0.29 FALLA", C_H6: "0.239 PASA", C_H7: "1.07 PASA", fuera_factor2: {NaI: 0.223, KCl: 0.309, KBr: 0.064, RbCl: 0.151, PbS: 0.446, PbSe: 0.256, PbTe: 0.216}}
  controles: {H_REP: "0.0 PASA", C1: "FALLA (KI ν_min −0.079 THz)", C2: "FALLA (PbTe malla +5.65 %)"}
  niveles: {UM-25: "nueva E2", UM-12: "E3 (sin cambio)", VP-05: "E6 externo + nota interna", UM-07: "E1"}
tareas: ["Registro y log actualizados 28-oct", "LoRA +4 (C-VIB-003_01..04)"]
riesgos: ["Sin NAC en sales iónicas", "κexp sin incertidumbre", "C1 falla en KI: según el prereg, KI debería excluirse de C_H1–C_H5; el evaluador congelado no lo excluyó en C_H2–C_H5, lo que solo puede mejorar ligeramente esas cifras y no cambia el nivel (D2)"]
decisiones: ["Evaluador congelado sin cambios", "Nada subido a repositorios"]
originalidad: {grado: "parcial, alto solapamiento en parte C", fuentes: ["arXiv:2509.03401, https://arxiv.org/abs/2509.03401 (benchmark de modelos fundacionales para fonones, incluye MatterSim-V1-5M y κL de haluros alcalinos; valores de MatterSim para NaBr, NaI y KBr similares a los nuestros según el resumen consultado, no verificado tabla a tabla)", "Xia et al., PRX 10, 041029 (2020), https://doi.org/10.1103/PhysRevX.10.041029", "Togo et al., PRB 91, 094306 (2015), https://doi.org/10.1103/PhysRevB.91.094306"], nota: "Lo propio es el prerregistro con hipótesis falsables, la comparación RTA/LBTE con la razón LDA y la réplica byte a byte"}
proximo_paso: "Prerregistrar C-VIB-004: κ bajo (KBr, KI, RbCl, PbTe, NaI) con 4 fonones o SCPH, dilatación térmica y NAC, y comparación con PBE"
```
