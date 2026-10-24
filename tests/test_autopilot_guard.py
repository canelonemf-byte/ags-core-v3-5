import json, sys
from pathlib import Path
APP = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP))
import autopilot  # noqa: E402


def test_single_instance_lock(tmp_path):
    pf = tmp_path / "ap.pid"
    fd = autopilot.acquire_lock(pf)
    assert fd is not None
    import os
    assert pf.read_text().strip() == str(os.getpid())
    assert autopilot.acquire_lock(pf) is None
    os.close(fd)
    fd2 = autopilot.acquire_lock(pf)
    assert fd2 is not None
    os.close(fd2)


def test_main_refuses_second_instance(tmp_path):
    pf = tmp_path / "ap.pid"
    fd = autopilot.acquire_lock(pf)
    try:
        assert autopilot.main(["--cycles", "1", "--pid-file", str(pf), "--stop-file", str(tmp_path / "S")]) == 2
    finally:
        import os; os.close(fd)


def test_reload_picks_up_new_manifest(tmp_path, monkeypatch):
    m = tmp_path / "projects.json"
    m.write_text(json.dumps({"version": "1", "projects": [{"id": "a"}]}))
    monkeypatch.setenv("AGS_PROJECTS_MANIFEST", str(m))
    autopilot.reload_config()
    import projects.manifest as M
    assert M.project_ids() == ["a"]
    m.write_text(json.dumps({"version": "2", "projects": [{"id": "a"}, {"id": "b"}]}))
    assert M.project_ids() == ["a"]  # caché lru
    autopilot.reload_config()
    import projects.manifest as M2
    assert M2.project_ids() == ["a", "b"]
    monkeypatch.delenv("AGS_PROJECTS_MANIFEST")
    autopilot.reload_config()
