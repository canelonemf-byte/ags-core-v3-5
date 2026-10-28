# review_claims — agsgpt-lora (Drive 2026-10-27)

Generado: 2026-10-28 13:40 CET · archivos revisados: 6
Fuente: drive_imports/2026-10-27 (subido por el autor a Drive 2026-10-27 20:37-20:46 Europe/Madrid)

**Alta: 0 · Media: 2 · Baja: 10 · Info: 0**

Revisión automática por reglas (sin LLM). Indicios a revisar, no veredictos. Afirmaciones de cifras/arquitectura: PENDIENTE DE VERIFICACIÓN.

## MEDIUM (2)

- `drive/agsgpt_lora.json:49` [hype] superlativo / afirmación absoluta ('infinit') — «"tarea": "Automatización supervisada finita con log (no bucle infinito)",»
- `drive/agsgpt_lora.json:66` [hype] superlativo / afirmación absoluta ('infinit') — «"La flota se detiene; no hay bucle infinito",»

## LOW (10)

- `drive/AGsGPT_LoRA.json:62` [number] cifra cuantitativa sin fuente ni cálculo enlazado — «"Escalabilidad: 50k agentes concurrentes no es viable en hardware local típico; usar jerarquía + pooling",»
- `drive/AGsGPT_LoRA.md:12` [number] cifra cuantitativa sin fuente ni cálculo enlazado — «- Núcleo AGsGPT (~10M params, base frozen) + LoRA (rank 8, ~196k trainable, ~3.9 %) + RAG + REST + planner multi-step + auto-learn SQLite.»
- `drive/auto_log.jsonl:3` [number] cifra cuantitativa sin fuente ni cálculo enlazado — «{"ciclo": 1, "tarea": "produccion amoniaco 10 MW", "salida": "[produccion_amoniaco]\n  [produccion_amoniaco] potencia 10 MW\n  kg_NH3/h 1050.0\n  CO2_evitado_kg/h 1680.0 (1,6 kg CO2/kg NH3 de gas, supuesto)\n  kWh/kg 9.52 (50 kWh/kg H2 · 3/»
- `drive/auto_log.jsonl:4` [number] cifra cuantitativa sin fuente ni cálculo enlazado — «{"ciclo": 2, "tarea": "balance fusion densidad 1e20 m-3 <σv> 1e-22", "salida": "[balance_fusion]\n  [balance_fusion] reaccion D + He3 → α (3,6 MeV) + p (14,7 MeV)\n  MeV 18.3\n  J/reaccion 2.931983e-12\n  potencia no calculada: faltan densi»
- `drive/auto_log.jsonl:5` [number] cifra cuantitativa sin fuente ni cálculo enlazado — «{"ciclo": 3, "tarea": "zeeman ODMR 10 µT", "salida": "[zeeman_odmr]\n  [zeeman_odmr] D 2.87 GHz\n  f+ 2.870280 GHz\n  f- 2.869720 GHz\n  split 0.560 MHz (γ = 28,025 GHz/T)", "ok": true}»
- `drive/auto_log.jsonl:9` [number] cifra cuantitativa sin fuente ni cálculo enlazado — «{"ciclo": 7, "tarea": "produccion amoniaco 10 MW", "salida": "[produccion_amoniaco]\n  [produccion_amoniaco] potencia 10 MW\n  kg_NH3/h 1050.0\n  CO2_evitado_kg/h 1680.0 (1,6 kg CO2/kg NH3 de gas, supuesto)\n  kWh/kg 9.52 (50 kWh/kg H2 · 3/»
- `drive/auto_log.jsonl:10` [number] cifra cuantitativa sin fuente ni cálculo enlazado — «{"ciclo": 8, "tarea": "balance fusion densidad 1e20 m-3 <σv> 1e-22", "salida": "[balance_fusion]\n  [balance_fusion] reaccion D + He3 → α (3,6 MeV) + p (14,7 MeV)\n  MeV 18.3\n  J/reaccion 2.931983e-12\n  potencia no calculada: faltan densi»
- `drive/auto_log.jsonl:11` [number] cifra cuantitativa sin fuente ni cálculo enlazado — «{"ciclo": 9, "tarea": "zeeman ODMR 10 µT", "salida": "[zeeman_odmr]\n  [zeeman_odmr] D 2.87 GHz\n  f+ 2.870280 GHz\n  f- 2.869720 GHz\n  split 0.560 MHz (γ = 28,025 GHz/T)", "ok": true}»
- `drive/auto_log.jsonl:15` [number] cifra cuantitativa sin fuente ni cálculo enlazado — «{"ciclo": 13, "tarea": "produccion amoniaco 10 MW", "salida": "[produccion_amoniaco]\n  [produccion_amoniaco] potencia 10 MW\n  kg_NH3/h 1050.0\n  CO2_evitado_kg/h 1680.0 (1,6 kg CO2/kg NH3 de gas, supuesto)\n  kWh/kg 9.52 (50 kWh/kg H2 · 3»
- `drive/auto_log.jsonl:16` [number] cifra cuantitativa sin fuente ni cálculo enlazado — «{"ciclo": 14, "tarea": "balance fusion densidad 1e20 m-3 <σv> 1e-22", "salida": "[balance_fusion]\n  [balance_fusion] reaccion D + He3 → α (3,6 MeV) + p (14,7 MeV)\n  MeV 18.3\n  J/reaccion 2.931983e-12\n  potencia no calculada: faltan dens»
