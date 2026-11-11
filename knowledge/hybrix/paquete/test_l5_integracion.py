"""Integración de la capa L5 (PheromoneBus + GeminiMetaAgent) en la API HYBRIX (main.py).

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia: MIT.
"""
import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import gemini_meta_agent
import main

KEY = "l5-test-key"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "")  # sin red: el agente queda 'pending'
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "estado.json")
    monkeypatch.setattr(main, "API_KEY", KEY)
    with TestClient(main.app) as c:
        main.app.state.db = {"projects_meta": {}, "telemetry": [], "predictions": []}
        yield c


def _preds(n):
    return [{"trial_id": i, "node_id": "n1", "label": 1, "prediction": 1, "probability": 0.9} for i in range(n)]


def test_modelo_por_defecto_y_override(monkeypatch):
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    assert gemini_meta_agent.DEFAULT_GEMINI_MODEL == "gemini-3.5-flash"
    a = gemini_meta_agent.GeminiMetaAgent(MagicMock(), None, api_key="")
    assert a.model_name == "gemini-3.5-flash"
    monkeypatch.setenv("GEMINI_MODEL", "gemini-4-argon")
    assert gemini_meta_agent.GeminiMetaAgent(MagicMock(), None, api_key="").model_name == "gemini-4-argon"


def test_estado_por_defecto_fuera_del_cwd(monkeypatch, tmp_path):
    monkeypatch.delenv("HYBRIX_DB_PATH", raising=False)
    monkeypatch.setenv("HYBRIX_DATA_DIR", str(tmp_path / "datos"))
    p = main._default_db_path()
    assert p == tmp_path / "datos" / "hybrix_api_state.json"
    monkeypatch.delenv("HYBRIX_DATA_DIR")
    assert main._default_db_path().parent != Path.cwd()


def test_predicciones_alimentan_l5(client):
    r = client.post("/api/v1/hybrix/predictions/batch", json={"items": _preds(10)}, headers={"X-API-Key": KEY})
    assert r.status_code == 201
    st = client.get("/api/v1/hybrix/l5/status", headers={"X-API-Key": KEY}).json()
    assert st["enabled"] is True and st["status"] == "pending"
    assert st["model"] == "gemini-3.5-flash" and st["cycle_count"] == 10 and st["buffer"] == 10
    assert "key" not in str(st).lower() or st.get("last_error") is None


def test_l5_deposita_directriz_json(client):
    agent = main.app.state.l5
    agent.analysis_interval = 10
    fake = MagicMock()
    fake.interactions.create.return_value = SimpleNamespace(output_text='{"beta_ridge": 0.02}')
    agent.client, agent.status, agent._use_interactions = fake, "ready", True
    for p in _preds(10):
        assert client.post("/api/v1/hybrix/predictions", json=p, headers={"X-API-Key": KEY}).status_code == 201
    st = client.get("/api/v1/hybrix/l5/status", headers={"X-API-Key": KEY}).json()
    assert st["ultima_directriz"] == {"beta_ridge": 0.02} and st["buffer"] == 0
    assert fake.interactions.create.call_args.kwargs["model"] == "gemini-3.5-flash"


def test_l5_desactivable(monkeypatch, tmp_path):
    monkeypatch.setattr(main, "L5_ENABLED", False)
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "e.json")
    monkeypatch.setattr(main, "API_KEY", KEY)
    with TestClient(main.app) as c:
        assert c.get("/api/v1/hybrix/l5/status", headers={"X-API-Key": KEY}).json() == {"enabled": False, "status": "disabled"}
