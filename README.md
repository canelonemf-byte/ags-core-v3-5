# ags-core-v3-5

# AGs-Core v3.6 — 121 agentes (verificado con `GET /health` el 11-11-2026): 53 agentes de proyecto (uno por proyecto de `projects.json`) + 38 de la v3.5 (31 por LLM vía LiteLLM, 6 herramientas físicas deterministas `tool_<proyecto>` y 1 agente local `agsgpt` PyTorch) + 7 sub-agentes locales (`app/agents/subagents.py`) + 23 de matriz_el_prat, gemini_reviewer y maestro_cuantico.

## Autoría

- **Autor:** Lázaro López Paz, El Prat de Llobregat, Barcelona, España
- **ORCID:** [0000-0001-8601-1963](https://orcid.org/0000-0001-8601-1963)
- Elaborado con asistencia de inteligencia artificial
- Sin afiliaciones institucionales

## Estado

Proyecto en desarrollo / documentación. No afirmar validación experimental salvo que el código o los informes del propio repositorio lo demuestren.

## Contenido (raíz)

```
.env.example
app/
config/
Dockerfile
docs/
integration_manifest.json
knowledge/
LICENSE
manifiesto/
NOTICE
projects.json
pytest.ini
README.md
requirements-dev.txt
requirements.txt
scripts/
tests/
tools/
ucs/
ui/
```

## Instalación

```bash
pip install -r requirements.txt          # pruebas: pip install -r requirements-dev.txt
```

## Operación (puertos y recuperación)

| servicio | puerto | log |
|---|---|---|
| API FastAPI | 8000 (`/health`) | `/workspace/agsgpt/api.log` |
| UI de estado (Streamlit) | 8501 | `/workspace/agsgpt/ui.log` |
| UI UCS (Streamlit) | 8502 | `/workspace/agsgpt/ucs_ui.log` |
| matriz_el_prat (Streamlit, repo aparte) | 8510 | `/workspace/agsgpt/matriz_ui.log` |
| HYBRIX API + capa L5 (FastAPI, `knowledge/hybrix/paquete`) | 8520 (`/api/v1/hybrix/l5/status`) | `/workspace/agsgpt/hybrix.log` |
| NNC dashboard / API (repo aparte) | 8080 / 8010 | `/workspace/agsgpt/NNC/logs/` |
| LiteLLM (opcional) | 4000 (`/health/readiness`) | `/workspace/agsgpt/litellm.log` |
| Autopilot | — | `/workspace/agsgpt/autopilot.log` |

Tras una restauración del equipo (venvs perdidos, servicios caídos):

```bash
scripts/recuperar_todo.sh               # recrea venvs, limpia .pid obsoletos, arranca todo y verifica HTTP
scripts/recuperar_todo.sh --verificar   # solo comprobación
```

El autopilot genera los informes por app (`scripts/build_app_reports.py --apps-only`) cada 20 min
(`AGS_APP_REPORTS_INTERVAL`, límite `AGS_APP_REPORTS_TIMEOUT`=300 s) y registra la duración en el log.
Cada app conserva su propia DB (`data/<app>.db`, historial de comprobaciones) y su propio Excel; no se mezclan.


## Uso

Archivos Python principales (revisar cada uno antes de ejecutar):
- `app/__init__.py`
- `app/agents/__init__.py`
- `app/agents/agsgpt_agent.py`
- `app/agents/compute.py`
- `app/agents/domain.py`
- `app/agents/gemini_agent.py`
- `app/agents/lab.py`
- `app/agents/matriz_el_prat_agents.py`
- `app/agents/multimodal.py`
- `app/agents/orchestration.py`
- `app/agents/physics_tools.py`
- `app/agents/project_agents.py`


## Licencia

Ver archivo `LICENSE` (o `LICENSE.md`) en la raíz. Documentación bajo CC BY 4.0 cuando aplique; código habitualmente MIT, salvo indicación contraria.
