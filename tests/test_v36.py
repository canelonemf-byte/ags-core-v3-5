"""Tests v3.6: manifiesto, conocimiento, ProjectAgents, checks, cola, supervisor, autopilot y API."""
import asyncio
import json
import time

import os
import pytest
from fastapi.testclient import TestClient

from agents.project_agents import PROJECT_AGENTS, agent_name
from main import app
from projects import load_manifest
from projects.knowledge import KnowledgeIndex, ProjectKnowledge, _Tfidf, chunk_text, tokens
from registry import agents_by_domain, get_agent
from supervisor import Supervisor, TaskQueue, checks

pytestmark = pytest.mark.unit
H = {"X-API-Key": "test-key"}


# ---------- manifiesto y agentes ----------
def test_manifest_and_agents():
    ps = load_manifest()["projects"]
    ids = [p["id"] for p in ps]
    assert len(ids) >= 46 and len(set(ids)) == len(ids)
    assert len(PROJECT_AGENTS) == len(ids) == len(agents_by_domain("project"))
    assert "atlas0-ordenador2-6-x-10" in ids and "fusi-n-carpeta" in ids
    for p in ps:
        a = get_agent(agent_name(p["id"]))
        assert a.project["id"] == p["id"] and a.description and a.system_prompt


def test_project_agent_retrieval_and_tool():
    a = get_agent("proj_cero_a_amoniaco")
    out = asyncio.run(a.run("produccion de amoniaco con 400 MW de electrolisis"))
    assert out["status"] == "ok" and out["tool"].startswith("zero_a.")
    assert out["sources"] and out["es_evidencia"] is True
    b = get_agent("proj_neuroglyq")
    out = asyncio.run(b.run("neuromodulacion inhibitoria"))
    assert out["sources"] and out["evidencia"] in ("E0_documental", "E1_calculo_local")


def test_project_agent_runs_check():
    out = asyncio.run(get_agent("proj_helioatlas_helio3").run("revisa la licencia y el copyright"))
    assert "license_check" in out["output"] and out["report"].endswith("license_check.md")


# ---------- conocimiento ----------
def test_chunk_and_tokens():
    cs = chunk_text("a" * 2000 + "\n\nhola mundo", size=900, overlap=100)
    assert len(cs) >= 3 and all(len(c) <= 900 for c in cs)
    assert tokens("Fusión D-He³ a 70 keV") == ["fusion", "kev"]


@pytest.mark.parametrize("sk", [True, False])
def test_tfidf_ranking(sk):
    rows = [("a.md", "reactor de fusion con helio tres y plasma"), ("b.md", "peptidos terapeuticos para cancer"),
            ("c.md", "receta de cocina")]
    pk = ProjectKnowledge("x", rows, prefer_sklearn=sk)
    r = pk.search("plasma de fusion")
    assert r[0]["file"] == "a.md"
    assert pk.search("") == []


def test_tfidf_fallback_scores():
    t = _Tfidf(["uno dos tres", "cuatro cinco seis"])
    s = t.scores("dos")
    assert s[0] > 0 and s[1] == 0


def test_index_persistence_and_rebuild(tmp_path):
    root = tmp_path / "k"
    (root / "p1").mkdir(parents=True)
    (root / "p1" / "README.md").write_text("# p1\n\nsensor de glucosa cuantico", encoding="utf-8")
    db = tmp_path / "k.sqlite"
    idx = KnowledgeIndex(root, db, prefer_sklearn=False)
    assert idx.search("p1", "glucosa")[0]["file"] == "README.md"
    idx2 = KnowledgeIndex(root, db, prefer_sklearn=False)  # lee de sqlite
    assert idx2.stats("p1")["chunks"] == 1
    time.sleep(1.1)
    (root / "p1" / "notas.txt").write_text("membrana de grafeno", encoding="utf-8")
    assert idx2.search("p1", "grafeno")[0]["file"] == "notas.txt"
    assert idx2.search("nope", "x") == []


# ---------- checks ----------
def test_license_checks():
    txt = ("© 2026 Lázaro López Paz. Todos los derechos reservados.\n"
           "Basado en https://github.com/karpathy/nanoGPT\n"
           "Licencia CC BY-NC-SA 4.0\nCopyright 2020 Andrej Karpathy\n"
           "Aquí tienes el documento completo que pediste\nver https://drive.google.com/x\n")
    fs = checks.license_in_file("doc.md", txt)
    kinds = {f["kind"] for f in fs}
    assert {"reserved_clause", "derived", "third_party", "ai_text", "foreign_copyright"} <= kinds
    names = {f.get("name") for f in fs if f["kind"] == "third_party"}
    assert "karpathy" in names and "google" not in names  # las URL no cuentan como mención
    owner = [f for f in fs if f["kind"] == "foreign_copyright"]
    assert len(owner) == 1 and "Karpathy" in owner[0]["quote"]  # el copyright propio no se marca


def test_claim_checks():
    txt = ("El sistema logra antigravedad estable.\nEs revolucionario y 100% seguro.\n"
           "Produce 72.000 kg/h de amoniaco.\nProduce 5 MW [1].\n"
           "Eleva la barrera de energía libre de Gibbs.\nEsta validado en laboratorio.\n")
    fs = checks.claims_in_file("d.md", txt)
    by = {}
    for f in fs:
        by.setdefault(f["kind"], []).append(f["line"])
    assert by["physics"] == [1] and 2 in by["hype"] and 3 in by["number"] and 4 not in by["number"] and 5 not in by.get("physics", []) and by["validation"] == [6]


def test_project_level_missing_and_collapse(tmp_path):
    root = tmp_path / "k"
    (root / "solo").mkdir(parents=True)
    (root / "solo" / "README.md").write_text("# solo\n\nidea breve\n\n- x · pendiente: en Drive · link", encoding="utf-8")
    idx = KnowledgeIndex(root, None, prefer_sklearn=False)
    proj = {"id": "solo", "license": "none", "tools": [], "broken_paths": ["Makefile (roto)"]}
    per = checks.missing_in_file("README.md", idx.read(root / "solo" / "README.md"))
    extra = {f["kind"] for f in checks.project_level("missing_pieces", idx, proj, per)}
    assert {"no_license", "no_code", "no_references", "thin_docs", "broken_path"} <= extra
    assert per[0]["kind"] == "drive_pending"
    lic = {f["kind"] for f in checks.project_level("license_check", idx, proj, [])}
    assert "no_mit" in lic
    tp = [checks._f("third_party", "info", f"f{i}.md", i, "m", name="grok") for i in range(3)]
    col = checks.dedupe(tp)
    assert len(col) == 1 and col[0]["count"] == 3 and len(col[0]["files"]) == 3


# ---------- cola ----------
def test_queue_lifecycle(tmp_path):
    q = TaskQueue(tmp_path / "q.sqlite")
    parent = q.add("composite", status="split")
    a = q.add("license_check", "p1", parent_id=parent, max_attempts=2)
    b = q.add("license_check", "p2", parent_id=parent, priority=1)
    t = q.claim("w")
    assert t["id"] == b and t["status"] == "running"  # prioridad
    assert q.claim("w", exclude_projects={"p1"}) is None
    q.complete(b, "r.md", {"ok": 1})
    t = q.claim("w")
    q.fail(t["id"], "boom", backoff=0)
    assert q.get(a)["status"] == "pending"
    q.claim("w")
    q.fail(a, "boom2", backoff=0)
    assert q.get(a)["status"] == "error" and q.get(parent)["status"] == "error"
    assert q.events(5, "error")
    c = q.add("x", "p3")
    q.claim("w")
    q.db.execute("update tasks set started=0 where id=?", (c,))
    assert q.requeue_stale(10) == 1 and q.get(c)["status"] == "pending"
    q.kv_set("k", {"a": 1})
    assert q.kv_get("k") == {"a": 1} and q.kv_get("nope", 7) == 7


# ---------- supervisor ----------
def _sup(tmp_path, **kw):
    return Supervisor(queue=TaskQueue(tmp_path / "s.sqlite"), reports_dir=tmp_path / "reports", **kw)


def test_supervisor_decompose(tmp_path):
    s = _sup(tmp_path)
    ps, ks = s.decompose("revisa la licencia de neuroglyq")
    assert ps == ["neuroglyq"] and ks == ["license_check"]
    ps, ks = s.decompose("revisa todo")
    assert len(ps) == len(s.projects()) and ks == list(checks.KINDS)
    with pytest.raises(ValueError):
        s.decompose("x", kinds=["nope"])
    with pytest.raises(ValueError):
        s.decompose("x", projects=["nope"])


def test_supervisor_bounds(tmp_path):
    s = _sup(tmp_path, max_workers=999, workers_per_project=999)
    assert s.max_workers == 16 and s.workers_per_project == 8
    assert _sup(tmp_path, max_workers=0, workers_per_project=0).max_workers >= 1


def test_supervisor_cycle_writes_reports(tmp_path):
    s = _sup(tmp_path, max_workers=3, workers_per_project=2)
    r = s.submit("x", projects=["helioatlas-helio3", "neuroglyq"], kinds=list(checks.KINDS))
    assert r["subtasks"] == 6
    st = s.run_cycle()
    assert st["done"] == 6 and st["errors"] == 0
    rep = json.loads((tmp_path / "reports" / "helioatlas-helio3" / "license_check.json").read_text())
    assert rep["summary"]["sub_agents"] == 2
    # helioatlas: MIT (código) + CC BY 4.0 (documentos) por decisión del autor (2026-10-18);
    # avisos de reserva sustituidos -> sin hallazgos altos (las menciones de patente quedan en medium)
    assert not any(f["severity"] == "high" for f in rep["findings"])
    assert not any(f["kind"] == "no_mit" for f in rep["findings"])
    assert (tmp_path / "reports" / "neuroglyq" / "missing_pieces.md").exists()
    assert "Resumen" in (tmp_path / "reports" / "SUMMARY.md").read_text()
    assert s.queue.get(r["id"])["status"] == "done"
    status = s.status()
    assert status["queue"]["done"] == 7 and status["cycles"] == 1 and status["autopilot"]["alive"] is False


def test_supervisor_logs_errors(tmp_path):
    s = _sup(tmp_path)
    s.queue.add("license_check", "no-existe", max_attempts=1)
    st = s.run_cycle()
    assert st["errors"] == 1 and s.status()["recent_errors"][0]["message"].startswith("tarea")


def test_seed_respects_reseed(tmp_path):
    s = _sup(tmp_path)
    n = s.seed()
    assert n == len(s.projects()) * len(checks.KINDS)
    assert s.seed() == 0  # ya hay pendientes


@pytest.mark.skipif(not os.getenv("AGS_RUN_SLOW"), reason="lento (~4.5 min): ejecuta checks reales sobre todo el manifiesto; AGS_RUN_SLOW=1 para correrlo")
@pytest.mark.timeout(900)
def test_autopilot_cycles(tmp_path, monkeypatch):
    import importlib
    monkeypatch.setenv("AGSGPT_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("AGS_REPORTS_DIR", str(tmp_path / "reports"))
    ap = importlib.import_module("autopilot")
    assert ap.main(["--cycles", "2", "--interval", "0", "--stop-file", str(tmp_path / "STOP")]) == 0
    q = TaskQueue(tmp_path / "data" / "supervisor.sqlite")
    assert q.kv_get("cycles") == 2 and q.kv_get("autopilot_heartbeat")["cycle"] == 2
    assert q.counts().get("done", 0) == len(load_manifest()["projects"]) * 3
    (tmp_path / "STOP").write_text("")
    assert ap.main(["--cycles", "0", "--interval", "0", "--stop-file", str(tmp_path / "STOP")]) == 0


# ---------- API ----------
client = TestClient(app)


def test_api_projects():
    r = client.get("/projects")
    assert r.status_code == 200 and r.json()["total"] == len(PROJECT_AGENTS)
    assert client.get("/projects/neuroglyq/search", params={"q": "tDCS"}).status_code == 401
    r = client.get("/projects/neuroglyq/search", params={"q": "neuromodulacion"}, headers=H)
    assert r.status_code == 200 and r.json()["results"]
    assert client.get("/projects/nope/search", params={"q": "x"}, headers=H).status_code == 404


def test_api_tasks_and_status():
    assert client.post("/tasks", json={"task": "x"}).status_code == 401
    assert client.post("/tasks", json={"task": "x", "kinds": ["nope"]}, headers=H).status_code == 422
    r = client.post("/tasks", json={"task": "licencia", "projects": ["neuroglyq"], "run_now": True}, headers=H)
    assert r.status_code == 201
    j = r.json()
    assert j["kinds"] == ["license_check"] and j["cycle"]["done"] >= 1
    r = client.get("/tasks", params={"parent_id": j["id"]}, headers=H)
    assert r.status_code == 200 and r.json()["tasks"][0]["status"] == "done"
    assert client.get(f"/tasks/{j['id']}", headers=H).json()["status"] == "done"
    assert client.get("/tasks/999999", headers=H).status_code == 404
    s = client.get("/supervisor/status", headers=H)
    assert s.status_code == 200 and s.json()["projects"] == len(PROJECT_AGENTS)
    assert client.get("/supervisor/status").status_code == 401


def test_declared_license_not_flagged():
    from app.supervisor import checks as c
    fs = c.license_in_file("doc.md", "Patente en trámite – Todos los derechos reservados")
    assert any(f["kind"] == "reserved_clause" for f in fs)

    class Idx:
        root = __import__("pathlib").Path("/nonexistent")
        def files(self, pid): return []
        def doc_files(self, pid): return []
        def code_files(self, pid): return []
        def read(self, p): return ""
    proj = {"id": "x", "license": "All-Rights-Reserved", "license_declared_by_author": True, "tools": []}
    extra = c.project_level("license_check", Idx(), proj, fs)
    kinds = {f["kind"] for f in fs + extra}
    assert "reserved_clause" not in kinds and "no_mit" not in kinds and "declared_license" in kinds


def test_index_skips_cache_dirs(tmp_path):
    from projects.knowledge import SKIP_DIRS
    assert {".venv", ".hf_cache", "node_modules", "__pycache__", ".git"} <= SKIP_DIRS
