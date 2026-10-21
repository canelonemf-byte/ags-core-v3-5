# C-NANO-001 — Energías superficiales con potenciales universales (OMNISCIENCE)

- **Nivel de evidencia:** E3, simulación computacional (no experimento). **PENDIENTE DE VERIFICACIÓN independiente.**
- **Prerregistro congelado:** `prereg_C-NANO-001.FROZEN.md`, sello `2026-10-21 11:52:25 CEST` (`freeze_stamp.txt`); sha256 en `prereg_C-NANO-001.sha256` (comprobado OK al integrar).
- **Resultados** (`resultados_C-NANO-001.md`, `results.json`):
  - H1 **PASA**: MatterSim subestima la energía superficial en 10/10 metales (MACE 9/10); MAE 0.143 J/m² frente a PBE de Tran 2016 (NANO-11).
  - H2 **FALLA**: la corrección lineal de un parámetro no alcanza el criterio.
  - H5 **FALSADA** (d* = −2.9 nm: el modelo no predice el cruce anatasa/rutilo) y H6 **FALSADA** (Δγ̄ R−A −0.022 J/m²) (NANO-12).
  - H7 (NANO-13): las losas relajadas de rutilo(110) y anatasa(101) no tienen modos < −0.3 THz en Γ.
  - Resto de hipótesis y desviaciones: ver `resultados_C-NANO-001.md` y `desviaciones.md`.
- `lora_C-NANO-001.jsonl`: 6 pares LLP derivados de esta campaña (no se han añadido al dataset de FUSIÓN IA).
- Excluido de la copia: `refs/` (datos de terceros), entornos virtuales, logs de instalación, `out/`, `smoke/`.

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Código MIT, documentos CC BY 4.0. Ver `NOTICE`.
