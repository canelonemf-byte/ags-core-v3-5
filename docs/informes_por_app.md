# Informes por app (DB + Excel)

**Autoría:** Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA.  
**Licencia:** MIT.

Cada app/proyecto tiene **su propia** base SQLite y **su propio** Excel. No hay un fichero combinado.

## Generador

```bash
python scripts/build_app_reports.py           # apps + knowledge
python scripts/build_app_reports.py --apps-only
```

Salidas típicas:

| app_id | DB | Excel |
|--------|----|-------|
| ags_core_ui | `data/ags_core_ui.db` | `reports/ags_core_ui.xlsx` |
| ucs_ui | `ucs/data/ucs_ui.db` | `ucs/reports/ucs_ui.xlsx` |
| matriz_el_prat | `/workspace/matriz-el-prat/data/…` | `…/reports/…` |
| nnc_dashboard / nnc_api | `/workspace/agsgpt/NNC/data/…` | `…/reports/…` |
| knowledge/\<proy\> | `knowledge/<proy>/data/<id>.db` | `knowledge/<proy>/reports/<id>.xlsx` |

Tablas: `apps`, `checks`, `hallazgos`, `ecuaciones` (+ hoja `meta` en el xlsx).

El autopilot ejecuta `--apps-only` al final de cada ciclo (mejor esfuerzo).

## Métricas HTTP

- `GET/POST /metrics/visit/{app}` — cuenta visita de esa app
- `GET /metrics/{app}` — lee contadores de esa app
- `GET /metrics/badge/{app}.svg` — badge SVG
