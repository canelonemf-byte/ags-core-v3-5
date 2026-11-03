# Contador de visitas por aplicación

**Autoría:** Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA.  
**Licencia:** MIT.

## Qué es

Módulo compartido que cuenta visitas **por aplicación**. Cada UI solo muestra
sus propias visitas y usuarios únicos. **No** hay banner ni cifra de total
global en pantalla.

## Dónde vive

- Código: `app/shared/metrics.py`
- JSON maestro: `/workspace/agsgpt/data/master_metrics.json` (o `AGS_MASTER_METRICS_FILE`)
- Sal de hash: `/workspace/agsgpt/data/metrics_salt` (chmod 600)
- Tests: `tests/test_metrics.py`

## Uso en una UI Streamlit

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("/workspace/agsgpt/ags-core-v3.6/app")))
from shared.metrics import track_streamlit_visit, render_app_metrics

APP = "ags_core_ui"
track_streamlit_visit(APP)          # una vez por sesión
render_visit_badge(APP)             # badge visible (sidebar/cabecera)
render_app_metrics(APP)             # bloque detalle opcional
```

## Privacidad

- Identificador = hash SHA-256 con sal de un token de sesión opaco.
- No se guardan IP ni datos personales.
- Lista de hashes por app acotada (`MAX_HASHES_PER_APP`, por defecto 50 000).

## Apps cableadas

| App | Puerto | `app_name` |
|-----|--------|------------|
| AGs-Core estado | 8501 | `ags_core_ui` |
| UCS Cognitive Stack | 8502 | `ucs_ui` |
| Matriz El Prat | 8510 | `matriz_el_prat` |

NNC en 8080/8010 no es Streamlit: no usa este render.
