# Sub-agentes especializados — 2026-10-21

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Software MIT; documento CC BY 4.0.

## Número real
- **7 sub-agentes reales** (E3 software, CPU, sin LLM, con tests en `tests/test_subagentes.py`), dominio `subagentes`, registrados en la API: `/health` pasa de 88 a **95 agentes**.
- **50.000 sub-agentes: no existen.** Solo hay un diseño (E1) y una simulación de colas (E2, `scripts/sim_subagentes.py`) con workers simulados.

| Sub-agente | Comprobación real | Intervalo |
|---|---|---|
| verificador_licencias | LICENSE/NOTICE por proyecto; licencias PENDIENTE en `licencias.json` | 1 h |
| detector_duplicados | `scripts/near_dup.py`: exactos, casi ≥0,85, filtraciones a test | 1 h |
| revisor_evidencia_e0_e6 | líneas con E4–E6 sin marca de verificación | 1 h |
| validador_esquema_llp | respuestas LLP JSON: claves, snake_case, sin null | 30 min |
| monitor_servicios | HTTP localhost: API, UIs, NNC, LiteLLM | 5 min |
| preflight_7b | sha256/esquema de splits vs manifest, test congelado, lora.yaml, licencias, GPU/RAM/disco, estimación VRAM (E0). **No entrena ni descarga pesos.** | 1 h |
| generador_pares_lora | recoge pares de agentes, deduplica contra train/val/test, escribe `data/staging/` (simulados aparte, nunca a train). **No toca test.** | 30 min |

Se ejecutan dentro del bucle del autopilot (`run_due`), y cada uno escribe su estado en `data/subagentes/<nombre>.json`.

## Primera ejecución (14:1x Madrid)
- verificador_licencias: 1 proyecto sin LICENSE/NOTICE (`llp_pack`), 6 licencias de modelos PENDIENTE DE VERIFICACIÓN.
- detector_duplicados: 0 filtraciones a test.
- revisor_evidencia_e0_e6: 32 líneas con E4–E6 que hay que revisar a mano.
- validador_esquema_llp: 50 respuestas con la clave `nivel_E` (no es snake_case estricto), en las líneas 807+ de train (añadidas a las 14:08).
- monitor_servicios: LiteLLM caído.
- preflight_7b: sin GPU, 7B bloqueado; RAM ~15 GB total.
- generador_pares_lora: 41 pares nuevos en staging, 159 simulados fuera de train, 38 líneas inválidas.

## Simulación del diseño de 50k (E2, simulación; NO agentes reales)
Supuestos: servicio exp(30 s), 1000 tareas/s, 100 coordinadores, 2 % de fallos con reintento, seed 42, 100.000 tareas.

| N workers simulados | throughput (tareas/s) | p50 (s) | p95 (s) | utilización |
|---|---|---|---|---|
| 7 | 0,23 | 218 695 | 416 253 | 1,00 |
| 1 000 | 30,9 | 1 485 | 2 906 | 0,95 |
| 50 000 | 221,1 | 21,3 | 91,8 | 0,14 |

Lectura: con estos supuestos, 50 000 workers quedarían infrautilizados (14 %). La escala real está limitada por CPU/RAM del box y por los costes de LLM. Son resultados de modelo, PENDIENTES DE VERIFICACIÓN con carga real.

## Integración de pares 14:1x (Madrid)
- ORÁCULO: 42 pares matemáticos verificados con sympy (`aprobado=true`), convertidos al esquema en `knowledge/oraculo-mesoscopico/lora_pares.jsonl` y unidos con `merge_pares.py`: 42 aceptados, 0 duplicados exactos, 0 casi-duplicados (Jaccard ≥0,85 contra train/val/test/simulados); 35 a train y 7 a val. Evidencia E1 (verificación simbólica).
- GRAVEDAD: los 12 pares provisionales de `/workspace/p003/pares_lora.jsonl` (2 marcados simulado) van a `data/staging/gravedad_provisional.jsonl`, no a train. Además citan trabajos de terceros (DOI), y merge_pares rechaza esas fuentes.
- Recuentos: train 891, val 193, test 66 (sha256 0937f06c…f8ef5 intacto). 0 filtraciones a test (near_dup).
