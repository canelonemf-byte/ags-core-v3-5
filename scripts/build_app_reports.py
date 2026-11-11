#!/usr/bin/env python3
"""Genera, por cada app/proyecto, su propia SQLite y su propio Excel.

No mezcla datos entre apps. Salidas:
  <root>/data/<app_id>.db
  <root>/reports/<app_id>.xlsx

Tablas: apps, checks, hallazgos, ecuaciones.
Solo datos reales verificables; lo no confirmado va como pendiente.

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España,
con asistencia de inteligencia artificial.
Licencia: MIT.
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
from zoneinfo import ZoneInfo

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"falta openpyxl: {e}") from e

ZONA = ZoneInfo("Europe/Madrid")
AGS_ROOT = Path(os.environ.get("AGS_ROOT", "/workspace/agsgpt/ags-core-v3.6"))
METRICS_FILE = Path(
    os.environ.get("AGS_MASTER_METRICS_FILE", "/workspace/agsgpt/data/master_metrics.json")
)
API_BASE = os.environ.get("AGS_BASE_URL", "http://127.0.0.1:8000")
# Filas de historial de comprobaciones que se conservan por app (≈ 1 año cada 20 min).
MAX_CHECKS = int(os.environ.get("AGS_APP_REPORTS_MAX_CHECKS", "30000"))
# Filas de 'checks' que se vuelcan al Excel (las más recientes).
XLSX_MAX_CHECKS = int(os.environ.get("AGS_APP_REPORTS_XLSX_CHECKS", "2000"))


@dataclass
class AppSpec:
    app_id: str
    title: str
    root: Path
    port: Optional[int] = None
    tech: str = "unknown"
    url: Optional[str] = None
    knowledge_dirs: List[str] = field(default_factory=list)
    extra_hallazgos: List[Dict[str, Any]] = field(default_factory=list)
    extra_ecuaciones: List[Dict[str, Any]] = field(default_factory=list)


def now_iso() -> str:
    return datetime.now(ZONA).isoformat(timespec="seconds")


def load_metrics() -> Dict[str, Any]:
    if not METRICS_FILE.exists():
        return {"apps": {}}
    try:
        return json.loads(METRICS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"apps": {}}


def http_check(url: str, timeout: float = 3.0) -> Tuple[Optional[int], str]:
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, "ok"
    except urllib.error.HTTPError as e:
        return e.code, f"http_error:{e.code}"
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}"


def app_registry() -> List[AppSpec]:
    return [
        AppSpec(
            app_id="ags_core_ui",
            title="AGs-Core UI",
            root=AGS_ROOT,
            port=8501,
            tech="streamlit",
            url="http://127.0.0.1:8501/",
            knowledge_dirs=[],
            extra_ecuaciones=[
                {
                    "name": "energia_exacta_demo_vqe",
                    "expression": "E0 = -sqrt(1.09)",
                    "latex": r"E_0=-\sqrt{1.09}",
                    "variables": "H = 0.5 ZI + 0.5 IZ + 0.3 XX (2 qubits)",
                    "source": "app/shared/maestro_cuantico.py::crear_hamiltoniano_demo",
                    "status": "verificado",
                },
                {
                    "name": "vqe_expectation",
                    "expression": "E(theta) = <psi(theta)|H|psi(theta)>",
                    "latex": r"E(\theta)=\langle\psi(\theta)|H|\psi(\theta)\rangle",
                    "variables": "theta parametros del ansatz Ry+CNOT; Statevector clasico",
                    "source": "app/shared/maestro_cuantico.py::hacer_funcion_costo",
                    "status": "verificado",
                },
            ],
            extra_hallazgos=[
                {
                    "title": "Maestro Cuantico compartido (simulacion clasica)",
                    "description": (
                        "Modulo shared.maestro_cuantico: VQE + simulated annealing "
                        "sobre Qiskit Statevector. No es hardware cuantico."
                    ),
                    "equations": "E0=-sqrt(1.09); E(theta)=<psi|H|psi>",
                    "evidence": "docs/maestro_cuantico.md; tests/test_maestro_cuantico.py",
                    "feasibility": "alta",
                    "status": "verificado",
                },
                {
                    "title": "Contador de visitas por app",
                    "description": (
                        "shared.metrics cuenta visitas y unicos por app_name; "
                        "sin total global. Endpoints /metrics/visit/{app} y /metrics/badge/{app}."
                    ),
                    "equations": "",
                    "evidence": "app/shared/metrics.py; app/metrics_api.py",
                    "feasibility": "alta",
                    "status": "verificado",
                },
            ],
        ),
        AppSpec(
            app_id="ucs_ui",
            title="UCS Cognitive Stack UI",
            root=AGS_ROOT / "ucs",
            port=8502,
            tech="streamlit",
            url="http://127.0.0.1:8502/",
            extra_hallazgos=[
                {
                    "title": "UI UCS con badge de visitas propio",
                    "description": "track_streamlit_visit('ucs_ui') + render_visit_badge.",
                    "equations": "",
                    "evidence": "ucs/ui_streamlit.py",
                    "feasibility": "alta",
                    "status": "verificado",
                }
            ],
        ),
        AppSpec(
            app_id="matriz_el_prat",
            title="Control ciudadano El Prat",
            root=Path("/workspace/matriz-el-prat"),
            port=8510,
            tech="streamlit",
            url="http://127.0.0.1:8510/",
            knowledge_dirs=["matriz-el-prat"],
            extra_hallazgos=[
                {
                    "title": "Contratos atipicos a revisar (analitica)",
                    "description": (
                        "analitica.py calcula anomalias IQR/z-score/LCSP art. 118 sobre "
                        "contratos unicos desde 2024. Cifra concreta: ver ejecucion local."
                    ),
                    "equations": "IQR fence: [Q1-1.5 IQR, Q3+1.5 IQR] sobre ln(importe)",
                    "evidence": "app/analitica.py; reports/anomalias_*.json",
                    "feasibility": "alta",
                    "status": "verificado",
                }
            ],
            extra_ecuaciones=[
                {
                    "name": "iqr_anomalia_importe",
                    "expression": "ln(importe) fuera de [Q1-1.5*IQR, Q3+1.5*IQR] por tipo",
                    "latex": r"\ln(\mathrm{importe})\notin[Q_1-1{,}5\,\mathrm{IQR},\,Q_3+1{,}5\,\mathrm{IQR}]",
                    "variables": "importe EUR; agrupacion por tipo de contrato",
                    "source": "app/analitica.py::anomalias_contratos",
                    "status": "verificado",
                }
            ],
        ),
        AppSpec(
            app_id="nnc_dashboard",
            title="NNC Dashboard",
            root=Path("/workspace/agsgpt/NNC"),
            port=8080,
            tech="http.server",
            url="http://127.0.0.1:8080/",
            knowledge_dirs=["nnc"],
            extra_hallazgos=[
                {
                    "title": "Badge de visitas en dashboard NNC",
                    "description": "HTML llama a AGs-Core /metrics/visit/nnc_dashboard.",
                    "equations": "",
                    "evidence": "NNC/.../dashboard_server.py (ags-visit-badge)",
                    "feasibility": "alta",
                    "status": "verificado",
                },
                {
                    "title": "Referencias bibliograficas (supervisor)",
                    "description": "Corregido 2026-11-11: README de knowledge/nnc con seccion Referencias "
                                   "(Bowring 1976 doi:10.1179/sre.1976.23.181.323, NGA WGS84, catalogo CRC); "
                                   "SUMMARY.md ya no marca no_references.",
                    "equations": "",
                    "evidence": "ags-core-v3.6/knowledge/nnc/README.md; ags-core-v3.6/reports/SUMMARY.md",
                    "feasibility": "alta",
                    "status": "verificado",
                },
            ],
        ),
        AppSpec(
            app_id="nnc_api",
            title="NNC REST API",
            root=Path("/workspace/agsgpt/NNC"),
            port=8010,
            tech="http.server",
            url="http://127.0.0.1:8010/health",
            knowledge_dirs=["nnc"],
            extra_hallazgos=[
                {
                    "title": "Proxy /visitas y /badge.svg hacia AGs-Core",
                    "description": "service_server proxya contador nnc_api.",
                    "equations": "",
                    "evidence": "NNC/.../service_server.py",
                    "feasibility": "alta",
                    "status": "verificado",
                }
            ],
        ),
        AppSpec(
            app_id="control_de_gastos",
            title="Control de gastos",
            root=Path("/workspace/apps/control-de-gastos"),
            port=5173,
            tech="vite",
            url=None,  # no asumimos que este levantada
            extra_hallazgos=[
                {
                    "title": "Badge de visitas en index.html",
                    "description": "localStorage visitor opaco → /metrics/visit/control_de_gastos",
                    "equations": "",
                    "evidence": "apps/control-de-gastos/index.html",
                    "feasibility": "alta",
                    "status": "verificado",
                }
            ],
        ),
        AppSpec(
            app_id="despensa_inteligente",
            title="Despensa inteligente",
            root=Path("/workspace/apps/despensa-inteligente"),
            port=5174,
            tech="vite",
            url=None,
            extra_hallazgos=[
                {
                    "title": "index.html + badge de visitas",
                    "description": "Entrada Vite creada con contador despensa_inteligente.",
                    "equations": "",
                    "evidence": "apps/despensa-inteligente/index.html",
                    "feasibility": "alta",
                    "status": "verificado",
                }
            ],
        ),
        AppSpec(
            app_id="radar_app",
            title="Radar / AGs local (sin UI HTTP)",
            root=Path("/workspace/agsgpt/radar_app"),
            port=None,
            tech="python_package",
            url=None,
            extra_hallazgos=[
                {
                    "title": "Sin interfaz HTTP activa",
                    "description": (
                        "radar_app contiene ags_core local + checkpoints; no hay servidor "
                        "web en marcha para colgar un badge visible. Contador preparado "
                        "via API AGs-Core si se anade UI."
                    ),
                    "equations": "",
                    "evidence": "radar_app/ags_core/; sin proceso en puertos de app",
                    "feasibility": "media",
                    "status": "pendiente",
                }
            ],
        ),
        AppSpec(
            app_id="ags_core_api",
            title="AGs-Core API",
            root=AGS_ROOT,
            port=8000,
            tech="fastapi",
            url="http://127.0.0.1:8000/health",
            extra_hallazgos=[
                {
                    "title": "API de metricas publicas",
                    "description": "/metrics/{app}, /metrics/visit/{app}, /metrics/badge/{app}",
                    "equations": "",
                    "evidence": "app/metrics_api.py",
                    "feasibility": "alta",
                    "status": "verificado",
                }
            ],
        ),
    ]


def knowledge_specs() -> List[AppSpec]:
    """Un informe por carpeta knowledge/*/maestro_cuantico.yaml (datos solo de ese proyecto)."""
    if yaml is None:
        return []
    out: List[AppSpec] = []
    root = AGS_ROOT / "knowledge"
    if not root.is_dir():
        return out
    for yml in sorted(root.glob("*/maestro_cuantico.yaml")):
        proj = yml.parent.name
        try:
            data = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        mc = data.get("maestro_cuantico") or data
        aplica = bool(mc.get("aplica"))
        uso = mc.get("uso") or ("no_aplica" if not aplica else "pendiente")
        hallazgos = [
            {
                "title": f"Maestro Cuantico: {'aplica' if aplica else 'no_aplica'}",
                "description": (
                    f"uso={uso}; backend={mc.get('backend')}; "
                    f"es_hardware_cuantico={mc.get('es_hardware_cuantico')}; "
                    f"nota={mc.get('nota', '')}"
                ),
                "equations": "",
                "evidence": str(yml.relative_to(AGS_ROOT)),
                "feasibility": "alta" if aplica else "n/a",
                "status": "verificado",
            }
        ]
        ecuaciones: List[Dict[str, Any]] = []
        # VQE I2 scan real si existe en este proyecto
        vqe = yml.parent / "vqe_i2_scan.json"
        if vqe.exists():
            try:
                scan = json.loads(vqe.read_text(encoding="utf-8"))
                proto = scan.get("protocolo") or {}
                ecuaciones.append(
                    {
                        "name": "vqe_i2_De",
                        "expression": (
                            f"De_vqe_eV={scan.get('De_vqe_eV')} ; "
                            f"De_casci_eV={scan.get('De_casci_eV')} ; "
                            f"lit_De_eV={scan.get('lit_De_eV')}"
                        ),
                        "latex": r"D_e^{\mathrm{VQE}}\approx D_e^{\mathrm{CASCI}}",
                        "variables": (
                            f"mol={proto.get('mol')}; basis={proto.get('basis')}; "
                            f"active={proto.get('active')}; backend={proto.get('backend')}"
                        ),
                        "source": str(vqe.relative_to(AGS_ROOT)),
                        "status": "verificado",
                    }
                )
                hallazgos.append(
                    {
                        "title": "Escaneo VQE I2 (simulacion statevector)",
                        "description": (
                            f"Clase {proto.get('clase')}; no es QPU/Maxwell/empuje. "
                            f"De_vqe_eV={scan.get('De_vqe_eV')} vs lit {scan.get('lit_De_eV')}."
                        ),
                        "equations": f"De_vqe_eV={scan.get('De_vqe_eV')}",
                        "evidence": str(vqe.relative_to(AGS_ROOT)),
                        "feasibility": "alta_simulacion",
                        "status": "verificado",
                    }
                )
            except (OSError, json.JSONDecodeError):
                pass
        out.append(
            AppSpec(
                app_id=proj.replace("-", "_")[:64],
                title=proj,
                root=yml.parent,
                tech="knowledge",
                knowledge_dirs=[proj],
                extra_hallazgos=hallazgos,
                extra_ecuaciones=ecuaciones,
            )
        )
    return out


SCHEMA = """
CREATE TABLE IF NOT EXISTS apps (
  name TEXT PRIMARY KEY,
  title TEXT,
  port INTEGER,
  tech TEXT,
  status TEXT,
  visits INTEGER DEFAULT 0,
  unique_users INTEGER DEFAULT 0,
  last_check TEXT,
  url TEXT
);
CREATE TABLE IF NOT EXISTS checks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  app TEXT NOT NULL,
  http_status INTEGER,
  tests_result TEXT,
  detail TEXT
);
CREATE TABLE IF NOT EXISTS hallazgos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  equations TEXT,
  evidence TEXT,
  feasibility TEXT,
  status TEXT
);
CREATE TABLE IF NOT EXISTS ecuaciones (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project TEXT NOT NULL,
  name TEXT NOT NULL,
  expression TEXT,
  latex TEXT,
  variables TEXT,
  source TEXT,
  status TEXT
);
"""


def write_db(spec: AppSpec, visits: int, unicos: int, http_status: Optional[int],
             http_detail: str, hallazgos: List[Dict[str, Any]],
             ecuaciones: List[Dict[str, Any]]) -> Path:
    data_dir = spec.root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = data_dir / f"{spec.app_id}.db"
    # Historial: la DB de cada app se conserva entre pasadas (antes se borraba en cada una).
    # - apps: una fila por app (estado actual, upsert)
    # - checks: se ACUMULA (serie temporal), recortada a MAX_CHECKS filas
    # - hallazgos/ecuaciones: instantánea de la spec (se reemplaza, no se duplica)
    conn = sqlite3.connect(str(db_path), timeout=30)
    try:
        conn.executescript(SCHEMA)
        conn.execute("DELETE FROM apps WHERE name = ?", (spec.app_id,))
        conn.execute("DELETE FROM hallazgos WHERE project = ?", (spec.app_id,))
        conn.execute("DELETE FROM ecuaciones WHERE project = ?", (spec.app_id,))
        status = "ok" if http_status and 200 <= http_status < 400 else (
            "sin_ui" if spec.url is None and spec.port is None else "down_or_error"
        )
        if spec.tech == "knowledge":
            status = "knowledge"
        elif spec.tech == "vite" and http_status is None:
            status = "codigo_listo_ui_apagada"
        conn.execute(
            "INSERT INTO apps(name,title,port,tech,status,visits,unique_users,last_check,url) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (
                spec.app_id,
                spec.title,
                spec.port,
                spec.tech,
                status,
                visits,
                unicos,
                now_iso(),
                spec.url,
            ),
        )
        conn.execute(
            "INSERT INTO checks(timestamp,app,http_status,tests_result,detail) VALUES (?,?,?,?,?)",
            (now_iso(), spec.app_id, http_status, http_detail, http_detail),
        )
        conn.execute(
            "DELETE FROM checks WHERE app = ? AND id NOT IN "
            "(SELECT id FROM checks WHERE app = ? ORDER BY id DESC LIMIT ?)",
            (spec.app_id, spec.app_id, MAX_CHECKS),
        )
        for h in hallazgos:
            conn.execute(
                "INSERT INTO hallazgos(project,title,description,equations,evidence,feasibility,status) "
                "VALUES (?,?,?,?,?,?,?)",
                (
                    spec.app_id,
                    h.get("title", ""),
                    h.get("description", ""),
                    h.get("equations", ""),
                    h.get("evidence", ""),
                    h.get("feasibility", ""),
                    h.get("status", "pendiente"),
                ),
            )
        for e in ecuaciones:
            conn.execute(
                "INSERT INTO ecuaciones(project,name,expression,latex,variables,source,status) "
                "VALUES (?,?,?,?,?,?,?)",
                (
                    spec.app_id,
                    e.get("name", ""),
                    e.get("expression", ""),
                    e.get("latex", ""),
                    e.get("variables", ""),
                    e.get("source", ""),
                    e.get("status", "pendiente"),
                ),
            )
        conn.commit()
    finally:
        conn.close()
    return db_path


def write_xlsx(spec: AppSpec, db_path: Path) -> Path:
    reports = spec.root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    xlsx_path = reports / f"{spec.app_id}.xlsx"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    wb = Workbook()
    # remove default
    default = wb.active
    wb.remove(default)
    header_fill = PatternFill("solid", fgColor="1B5E20")
    header_font = Font(color="FFFFFF", bold=True)
    for table in ("apps", "checks", "hallazgos", "ecuaciones"):
        ws = wb.create_sheet(table)
        if table == "checks":
            cur = conn.execute(
                "SELECT * FROM (SELECT * FROM checks WHERE app = ? ORDER BY id DESC LIMIT ?) ORDER BY id",
                (spec.app_id, XLSX_MAX_CHECKS),
            )
        else:
            cur = conn.execute(f"SELECT * FROM {table}")
        cols = [d[0] for d in cur.description]
        ws.append(cols)
        for col_i, _ in enumerate(cols, 1):
            cell = ws.cell(1, col_i)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center")
        for row in cur.fetchall():
            ws.append([row[c] for c in cols])
        ws.auto_filter.ref = ws.dimensions
        for i, col in enumerate(cols, 1):
            width = 14
            for cell in ws[get_column_letter(i)]:
                width = max(width, min(60, len(str(cell.value or "")) + 2))
            ws.column_dimensions[get_column_letter(i)].width = width
    conn.close()
    # hoja meta
    meta = wb.create_sheet("meta", 0)
    meta.append(["campo", "valor"])
    meta["A1"].fill = header_fill
    meta["B1"].fill = header_fill
    meta["A1"].font = header_font
    meta["B1"].font = header_font
    for k, v in [
        ("app_id", spec.app_id),
        ("title", spec.title),
        ("generado", now_iso()),
        ("zona", "Europe/Madrid"),
        ("db", str(db_path)),
        ("autoria", "Lázaro López Paz, El Prat de Llobregat, Barcelona, España; asistencia IA"),
        ("nota", "Solo datos de ESTA app/proyecto. No hay totales globales cruzados."),
    ]:
        meta.append([k, v])
    meta.column_dimensions["A"].width = 16
    meta.column_dimensions["B"].width = 80
    wb.save(xlsx_path)
    return xlsx_path


def build_one(spec: AppSpec, metrics: Dict[str, Any]) -> Dict[str, Any]:
    bucket = (metrics.get("apps") or {}).get(spec.app_id) or {}
    visits = int(bucket.get("total_visits") or 0)
    unicos = int(bucket.get("unique_users") or 0)
    http_status: Optional[int] = None
    http_detail = "no_url"
    if spec.url:
        http_status, http_detail = http_check(spec.url)
    hallazgos = list(spec.extra_hallazgos)
    ecuaciones = list(spec.extra_ecuaciones)
    db_path = write_db(spec, visits, unicos, http_status, http_detail, hallazgos, ecuaciones)
    xlsx_path = write_xlsx(spec, db_path)
    return {
        "app_id": spec.app_id,
        "db": str(db_path),
        "xlsx": str(xlsx_path),
        "visits": visits,
        "unique_users": unicos,
        "http_status": http_status,
        "http_detail": http_detail,
        "n_hallazgos": len(hallazgos),
        "n_ecuaciones": len(ecuaciones),
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    only_apps = "--apps-only" in argv
    metrics = load_metrics()
    specs = app_registry()
    if not only_apps:
        specs = specs + knowledge_specs()
    results = []
    for spec in specs:
        try:
            results.append(build_one(spec, metrics))
        except Exception as exc:  # noqa: BLE001
            results.append({"app_id": spec.app_id, "error": f"{type(exc).__name__}: {exc}"})
    summary = AGS_ROOT / "reports" / "app_reports_index.json"
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(
        json.dumps({"generado": now_iso(), "resultados": results}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"ok": True, "n": len(results), "index": str(summary)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
