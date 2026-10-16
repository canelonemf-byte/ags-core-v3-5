# AGs-Core v3.5

38 agentes: 31 por LLM (vía LiteLLM, de la v3.4) + 6 agentes de herramientas físicas
deterministas (`tool_<proyecto>`) + 1 agente local `agsgpt` (PyTorch + LoRA).
La salida de un LLM o de AGsGPT **no** es evidencia; la de las herramientas sí indica supuestos.

## Novedades v3.5
- `app/ags_local/`: motor local (herramientas, enrutado, planificador, memoria SQLite, AGsGPT/LoRA),
  portado de ags_core 3.0 sin el acoplamiento a la app radar.
- Orquestador **reglas primero**: si una herramienta local resuelve la tarea, no se llama a ningún LLM.
- Endpoints nuevos (requieren `X-API-Key`):
  - `POST /run/tool/{project}` `{"task": "..."}`
  - `GET  /agsgpt/status`
  - `POST /agsgpt/train` `{"steps": 1-200, "text": "corpus opcional"}`

## Uso
    pip install -r requirements-dev.txt     # torch CPU: ver requirements.txt
    cd app && AGS_API_KEY=xxx uvicorn main:app --port 8000
    pytest -m unit

## Límites
- AGsGPT: ~0,8 M parámetros, base aleatoria congelada **sin preentrenar**; solo se entrena LoRA.
  Genera texto sin sentido hasta que se preentrene la base (fuera de alcance de v3.5).
- Docker/litellm_config/docker-compose: el original no se pudo leer desde Drive; Dockerfile reconstruido sin probar.
- Licencia: MIT (ver LICENSE). Atribuciones de terceros en NOTICE.
