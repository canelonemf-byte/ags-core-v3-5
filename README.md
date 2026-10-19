# AGs-Core v3.6

84 agentes: 46 agentes de proyecto (v3.6, uno por repositorio) + los 38 de la v3.5: 31 por LLM (vía LiteLLM, de la v3.4) + 6 agentes de herramientas físicas
deterministas (`tool_<proyecto>`) + 1 agente local `agsgpt` (PyTorch + LoRA).
La salida de un LLM o de AGsGPT **no** es evidencia; la de las herramientas sí indica supuestos.

## Novedades v3.6
- **46 ProjectAgents** (`proj_<proyecto>`), generados desde `projects.json` (no hay un archivo por agente).
  Conocimiento: README/docs/código de cada repo copiados en `knowledge/<proyecto>/` e indexados en local
  (TF-IDF + palabras clave; usa scikit-learn si está instalado). Los proyectos con física asociada
  usan además las herramientas de `ags_local` (amoniaco, fusión D-He3, MEI-RIT, NV/ODMR, tDCS, ecosistema).
  Regenerar: `python scripts/sync_knowledge.py --src /ruta/repos --github owner/repo`.
- **Supervisor** (`app/supervisor/`): descompone una tarea en subtareas por proyecto y tipo, las guarda en
  una cola SQLite persistente (`data/supervisor.sqlite`) y las ejecuta con como mucho `AGS_MAX_WORKERS`
  tareas en paralelo (def. 4, máx. 16) y `AGS_WORKERS_PER_PROJECT` sub-agentes por tarea (def. 3, máx. 8),
  con reintentos y registro de errores.
- Tipos de tarea (deterministas, sin LLM): `review_claims` (afirmaciones sin respaldo, física
  extraordinaria, cifras sin fuente, recálculo con herramientas locales), `missing_pieces` (código, tests,
  referencias, validación, archivos que siguen en Drive) y `license_check` (originalidad y licencias:
  «todos los derechos reservados»/CC BY-NC/patente frente a MIT, nombres de terceros, copyright ajeno,
  contenido derivado sin NOTICE, texto con huella de asistente de IA).
- **Autopilot**: `python -m app.autopilot [--cycles N] [--interval s] [--reseed s]`. Cada ciclo siembra las
  revisiones que tocan (por defecto cada 6 h por proyecto y tipo), las ejecuta y escribe
  `reports/<proyecto>/<tipo>.md|json` y `reports/SUMMARY.md`. Para pararlo: `kill <pid>` o crear `data/STOP`.
- Endpoints nuevos (con `X-API-Key`): `POST /tasks` `{"task", "projects"?, "kinds"?, "run_now"?}`,
  `GET /tasks`, `GET /tasks/{id}`, `GET /supervisor/status`, `GET /projects/{id}/search?q=`; y `GET /projects`.
- Los informes son **indicios a revisar, no veredictos**: las reglas no comprueban plagio contra fuentes
  externas (no hay acceso a internet en la revisión), solo señales internas.

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
    python -m app.autopilot --cycles 3 --interval 2   # desde la raíz del repo

## UI de estado (Streamlit, opcional)
    streamlit run ui/app.py --server.address 127.0.0.1 --server.port 8501
Solo lectura: muestra `/health`, `/supervisor/status`, los proyectos con el recuento de hallazgos
(high/medium/low/info) de `reports/<proyecto>/*.json` y `reports/SUMMARY.md`. La clave `X-API-Key`
se lee en el servidor desde `data/api_key` (o `AGS_API_KEY`) y no llega al navegador.
API base configurable con `AGS_BASE_URL` (def. `http://127.0.0.1:8000`).

## Límites
- AGsGPT: ~0,8 M parámetros, base aleatoria congelada **sin preentrenar**; solo se entrena LoRA.
  Genera texto sin sentido hasta que se preentrene la base (fuera de alcance de v3.5).
- Docker/litellm_config/docker-compose: el original no se pudo leer desde Drive; Dockerfile reconstruido sin probar.
- Licencia: MIT (ver LICENSE). Atribuciones de terceros en NOTICE.

## Fuentes NotebookLM

Textos del paquete NotebookLM (Drive `NotebookLM_Fuentes_2026-08-30`) que no existían en este repositorio:

- [docs/notebooklm/00_GUIA_NOTEBOOKLM.md](docs/notebooklm/00_GUIA_NOTEBOOKLM.md)
- [docs/notebooklm/99_MAPA_CARGAS.md](docs/notebooklm/99_MAPA_CARGAS.md)
- [docs/notebooklm/ATLAS_INTEGRADO_PORTFOLIO.md](docs/notebooklm/ATLAS_INTEGRADO_PORTFOLIO.md)
