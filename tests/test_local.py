import pytest
from fastapi.testclient import TestClient
from main import app
from orchestrator import orchestrator
from registry import get_agent
pytestmark = pytest.mark.unit
c = TestClient(app); H = {"X-API-Key": "test-key"}

async def test_orchestrator_rules_first_no_llm():
    r = await orchestrator.execute("amoniaco con 10 MW y luego fusion a 100 keV", allow_llm=False)
    assert r["mode"] == "local_rules" and r["status"] == "completed"
    assert "produccion_amoniaco" in r["results"][0]["output"]

async def test_orchestrator_no_match_no_llm():
    r = await orchestrator.execute("escribe un poema", allow_llm=False)
    assert r["status"] == "failed"

async def test_tool_agent():
    r = await get_agent("tool_zero_a").run("amoniaco 25 MW")
    assert r["tool"] == "produccion_amoniaco" and r["es_evidencia"]

def test_run_tool_endpoint():
    r = c.post("/run/tool/mei_rit", headers=H, json={"task": "empuje yodo 3 kV"})
    assert r.status_code == 200 and r.json()["tool"] == "empuje_yodo"

def test_run_tool_unknown_project():
    assert c.post("/run/tool/nope", headers=H, json={"task": "x"}).status_code == 404

def test_run_tool_requires_auth():
    assert c.post("/run/tool/zero_a", json={"task": "x"}).status_code == 401

def test_orchestrated_endpoint_local():
    r = c.post("/run/orchestrated", headers=H, json={"task": "calcula amoniaco con 25 MW"})
    assert r.status_code == 200 and r.json()["mode"] == "local_rules"

def test_train_validation():
    assert c.post("/agsgpt/train", headers=H, json={"steps": 10000}).status_code == 422

def test_train_smoke_and_status():
    pytest.importorskip("torch")
    r = c.post("/agsgpt/train", headers=H, json={"steps": 5, "text": "AGs-Core prueba local " * 20})
    assert r.status_code == 200 and r.json()["trainable_lora_params"] > 0
    s = c.get("/agsgpt/status", headers=H).json()
    assert s["weights"] and 0 < s["params_lora"] < s["params_total"]
    g = c.post("/run/agent/agsgpt", headers=H, json={"task": "hola"}).json()
    assert g["weights"] and "[AGsGPT]" in g["output"]
