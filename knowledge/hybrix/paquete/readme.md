# HYBRIX Orchestration System (v1.9.0)

Sistema de orquestación, telemetría biológica, monitor de deriva estadística y exportación de datos.

## Componentes del Paquete

- : API FastAPI v1.9.0 con almacenamiento síncrono en disco, alertas automáticas de viabilidad (< 70%) y exportación preventiva.
- : Pruebas de integración y unitarias completas.
- : Script de exportación preventiva periódica a CSV.
- : Benchmark de carga y rendimiento.

## Ejecución


## Capa L5 (Gemini)

- `gemini_meta_agent.py` — `GeminiMetaAgent` (estigmergia + JSON de hiperparámetros).
- `hybrix_phero_bus.py` — bus de feromonas in-memory (`sniff` / `deposit` con TTL).
- `hybrix_genai_l5.py` — `GenAIMetaAgent` con fallback heurístico local.
- Modelo por defecto: `gemini-3.5-flash` (desde 2026-11-11); `GEMINI_MODEL=gemini-4-argon` para usar argon (existe, pero dio 429 por cuota el 2026-11-09). Clave: `GEMINI_API_KEY`.
- Verificación 2026-11-09: `client.interactions.create` + `output_text` confirmados.
- Integrado en `main.py` (2026-11-11): cada predicción recibida (`POST /api/v1/hybrix/predictions` y `/batch`) se deposita como
  feromona `prediccion_final` y avanza un ciclo del agente en segundo plano; cada `HYBRIX_L5_INTERVAL` ciclos (50) con 10 ensayos
  pide a Gemini un JSON y lo deposita en `gemini_hyperparameters_update`. Estado: `GET /api/v1/hybrix/l5/status`.
  Desactivar con `HYBRIX_L5_ENABLED=0`. Sin `GEMINI_API_KEY` el agente queda `pending` (no llama a la red).
- Estado de la API fuera del directorio de trabajo: `HYBRIX_DB_PATH`, o `HYBRIX_DATA_DIR`, o `~/.local/share/hybrix/hybrix_api_state.json`.

```bash
export GEMINI_API_KEY=...   # o cargar .secrets/gemini.env
export GEMINI_MODEL=gemini-4-argon     # opcional (por defecto gemini-3.5-flash)
python -m pytest test_gemini_meta_agent.py test_genai_fallback.py test_suite.py test_l5_integracion.py -q
```
