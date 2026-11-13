import pytest
from fastapi.testclient import TestClient
from main import app
from agents.project_agents import PROJECT_AGENTS
from agents.subagents import WORKERS
TOTAL = 38 + len(PROJECT_AGENTS) + len(WORKERS) + 23  # matriz_el_prat (20 + actualizar_todo) + gemini_reviewer + maestro_cuantico
pytestmark = pytest.mark.unit
client = TestClient(app, client=("127.0.0.1", 50000))  # las lecturas de inventario sin clave exigen localhost

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["agents"] == TOTAL

def test_request_id():
    r = client.get("/health", headers={"X-Request-ID": "test-123"})
    assert r.headers["X-Request-ID"] == "test-123"

def test_agents():
    r = client.get("/agents")
    assert r.status_code == 200 and r.json()["total"] == TOTAL

def test_auth():
    assert client.post("/run/agent/searcher", json={"task": "x"}).status_code == 401

def test_unknown_agent_with_auth():
    r = client.post("/run/agent/nope", headers={"X-API-Key": "test-key"}, json={"task": "x"})
    assert r.status_code == 404

def test_unknown_domain():
    assert client.get("/agents/domain/nope").status_code == 404

def test_integrations_configurable():
    r = client.get("/integrations", headers={"X-API-Key": "test-key"})
    assert r.status_code == 200

def test_health_reports_litellm_state():
    j = client.get("/health").json()
    assert j["version"] == "3.6.0" and j["litellm"] in {"ready", "unreachable"} or j["litellm"].startswith("http_")
    assert "docker" not in j


# ---- auditoría REA M08: inventario sin clave solo desde localhost; esquema declarado ----
def test_inventory_remote_requires_key():
    remote = TestClient(app, client=("10.1.2.3", 50000))
    for path in ("/agents", "/projects", "/agents/domain/nope"):
        assert remote.get(path).status_code == 403
    assert remote.get("/agents", headers={"X-API-Key": "test-key"}).status_code == 200
    assert remote.get("/agents", headers={"X-API-Key": "mala"}).status_code == 403
    assert remote.get("/health").status_code == 200

def test_openapi_declares_security():
    spec = client.get("/openapi.json").json()
    schemes = spec["components"]["securitySchemes"]
    assert any(v.get("type") == "apiKey" and v.get("name") == "X-API-Key" for v in schemes.values())
    assert spec["paths"]["/tasks"]["get"].get("security")
    assert spec["paths"]["/agents"]["get"].get("security")
    assert "security" not in spec["paths"]["/health"]["get"]
