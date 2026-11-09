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
- Modelo por defecto: `gemini-4-argon` (variable `GEMINI_MODEL`). Clave: `GEMINI_API_KEY`.
- Verificación 2026-11-09: `client.interactions.create` + `output_text` confirmados; si argon no tiene cuota, usar `GEMINI_MODEL=gemini-3.5-flash`.

```bash
export GEMINI_API_KEY=...   # o cargar .secrets/gemini.env
export GEMINI_MODEL=gemini-3.5-flash   # opcional
python -m pytest test_gemini_meta_agent.py test_genai_fallback.py test_suite.py -q
```
