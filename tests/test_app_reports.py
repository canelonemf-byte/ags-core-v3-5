"""Tests de los informes por app (build_app_reports) y de su programación en el autopilot.

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia: MIT.
"""
import importlib.util
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit
ROOT = Path(__file__).resolve().parents[1]


def _bar():
    spec = importlib.util.spec_from_file_location("build_app_reports", ROOT / "scripts" / "build_app_reports.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["build_app_reports"] = mod  # dataclasses necesita el módulo registrado
    spec.loader.exec_module(mod)
    return mod


def test_write_db_conserva_historial_y_no_duplica(tmp_path):
    bar = _bar()
    s = bar.AppSpec(app_id="app_a", title="A", root=tmp_path / "a", port=1, tech="streamlit",
                    url="http://x", extra_hallazgos=[{"title": "h1"}])
    for code in (200, 500, 200):
        db = bar.write_db(s, 1, 1, code, "ok", s.extra_hallazgos, [])
    c = sqlite3.connect(db)
    assert [r[0] for r in c.execute("SELECT http_status FROM checks ORDER BY id")] == [200, 500, 200]
    assert c.execute("SELECT COUNT(*) FROM apps").fetchone()[0] == 1
    assert c.execute("SELECT COUNT(*) FROM hallazgos").fetchone()[0] == 1
    c.close()
    assert bar.write_xlsx(s, db).is_file()


def test_write_db_no_mezcla_apps(tmp_path):
    bar = _bar()
    a = bar.AppSpec(app_id="app_a", title="A", root=tmp_path / "a")
    b = bar.AppSpec(app_id="app_b", title="B", root=tmp_path / "b")
    da = bar.write_db(a, 5, 2, None, "no_url", [], [])
    db = bar.write_db(b, 7, 3, None, "no_url", [], [])
    assert da != db
    for path, name, visits in ((da, "app_a", 5), (db, "app_b", 7)):
        c = sqlite3.connect(path)
        assert c.execute("SELECT name, visits FROM apps").fetchall() == [(name, visits)]
        assert {r[0] for r in c.execute("SELECT app FROM checks")} == {name}
        c.close()


def test_write_db_recorta_historial(tmp_path, monkeypatch):
    bar = _bar()
    monkeypatch.setattr(bar, "MAX_CHECKS", 3)
    s = bar.AppSpec(app_id="app_c", title="C", root=tmp_path / "c")
    for _ in range(5):
        db = bar.write_db(s, 0, 0, None, "no_url", [], [])
    c = sqlite3.connect(db)
    assert c.execute("SELECT COUNT(*) FROM checks").fetchone()[0] == 3
    c.close()


def test_autopilot_build_app_reports_espaciado_y_duracion():
    import autopilot  # app/ está en sys.path vía conftest/pythonpath
    llamadas = []

    class R:
        returncode = 0

    def runner(cmd, **kw):
        llamadas.append(kw["timeout"])
        return R()

    st = {}
    r1 = autopilot.maybe_build_app_reports(st, now=10_000.0, runner=runner)
    assert r1 and r1["rc"] == 0 and r1["timeout"] is False and "segundos" in r1
    assert autopilot.maybe_build_app_reports(st, now=10_060.0, runner=runner) is None  # siguiente ciclo: no toca
    assert autopilot.maybe_build_app_reports(st, now=10_000.0 + autopilot.APP_REPORTS_INTERVAL, runner=runner)
    assert len(llamadas) == 2 and all(t == autopilot.APP_REPORTS_TIMEOUT for t in llamadas)
    assert 15 * 60 <= autopilot.APP_REPORTS_INTERVAL <= 30 * 60 and autopilot.APP_REPORTS_TIMEOUT >= 300


def test_autopilot_build_app_reports_timeout_no_rompe():
    import autopilot

    def runner(cmd, **kw):
        raise subprocess.TimeoutExpired(cmd, kw["timeout"])

    r = autopilot.maybe_build_app_reports({}, now=1e9, runner=runner)
    assert r["timeout"] is True and r["rc"] is None


def test_monitor_servicios_vigila_matriz_8510():
    from agents.subagents import MonitorServicios
    assert MonitorServicios.URLS.get("matriz_8510") == "http://127.0.0.1:8510/"


def test_monitor_servicios_vigila_hybrix_8520():
    from agents.subagents import MonitorServicios
    assert MonitorServicios.URLS.get("hybrix_8520") == "http://127.0.0.1:8520/api/v1/hybrix/l5/status"
