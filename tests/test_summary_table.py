import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))


def test_summary_lists_projects_with_high(tmp_path, monkeypatch):
    from supervisor.supervisor import Supervisor
    from supervisor import checks
    s = Supervisor.__new__(Supervisor)
    s.reports_dir = tmp_path
    monkeypatch.setattr(Supervisor, "projects", lambda self: ["a", "b"])
    k = checks.KINDS[0]
    for pid, sev in (("a", "high"), ("b", "low")):
        (tmp_path / pid).mkdir()
        (tmp_path / pid / f"{k}.json").write_text(json.dumps({"summary": {"project": pid, "counts": {}}, "findings": [{"severity": sev, "kind": "no_code", "file": "-", "line": 0, "message": "m"}]}))
    txt = s.write_summary().read_text()
    tabla = txt.split("severidad alta", 1)[1].split("## Ejemplos")[0]
    assert "| a | 1 |" in tabla and "| b |" not in tabla
