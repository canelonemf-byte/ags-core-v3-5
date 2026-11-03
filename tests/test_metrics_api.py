"""Tests de endpoints /metrics (contador por app + badge SVG)."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.unit


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("AGS_METRICS_DIR", str(tmp_path))
    monkeypatch.setenv("AGS_MASTER_METRICS_FILE", str(tmp_path / "master_metrics.json"))
    monkeypatch.setenv("AGS_METRICS_LOCK_FILE", str(tmp_path / "master_metrics.lock"))
    monkeypatch.setenv("AGS_METRICS_SALT_FILE", str(tmp_path / "metrics_salt"))
    monkeypatch.delenv("AGS_METRICS_DISABLE", raising=False)
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)

    import importlib
    import shared.metrics as metrics
    importlib.reload(metrics)
    import metrics_api
    importlib.reload(metrics_api)
    import main
    importlib.reload(main)
    return TestClient(main.app)


def test_visit_counts_per_app(client):
    r1 = client.get("/metrics/visit/demo_x", params={"visitor_id": "aaa"})
    assert r1.status_code == 200
    assert r1.json()["total_visits"] == 1
    r2 = client.get("/metrics/visit/demo_x", params={"visitor_id": "aaa"})
    assert r2.json()["total_visits"] == 2
    assert r2.json()["unique_users"] == 1
    r3 = client.get("/metrics/visit/demo_y", params={"visitor_id": "aaa"})
    assert r3.json()["total_visits"] == 1
    # no global
    gx = client.get("/metrics/demo_x").json()
    gy = client.get("/metrics/demo_y").json()
    assert gx["total_visits"] == 2
    assert gy["total_visits"] == 1


def test_badge_svg(client):
    client.get("/metrics/visit/badge_app", params={"visitor_id": "z"})
    r = client.get("/metrics/badge/badge_app.svg")
    assert r.status_code == 200
    assert "image/svg+xml" in r.headers.get("content-type", "")
    assert b"<svg" in r.content
    assert b"visitas" in r.content


def test_invalid_app_name(client):
    r = client.get("/metrics/visit/bad name!")
    assert r.status_code == 400
    r2 = client.get("/metrics/visit/has/slash")
    assert r2.status_code in (400, 404)
