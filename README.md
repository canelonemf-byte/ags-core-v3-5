# ags-core-v3-5

# AGs-Core v3.6  84 agentes: 46 agentes de proyecto (v3.6, uno por repositorio) + los 38 de la v3.5: 31 por LLM (vía LiteLLM, de la v3.4) + 6 agentes de herramientas físicas deterministas (`tool_<proyecto>`) + 1 agente local `agsgpt` (PyTor

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
pip install -r requirements.txt
```


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
