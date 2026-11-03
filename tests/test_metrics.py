"""Tests del contador de visitas por aplicación (módulo compartido)."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit


@pytest.fixture()
def metrics_env(tmp_path, monkeypatch):
    """Aísla el JSON/sal/lock en un directorio temporal."""
    monkeypatch.setenv("AGS_METRICS_DIR", str(tmp_path))
    monkeypatch.setenv("AGS_MASTER_METRICS_FILE", str(tmp_path / "master_metrics.json"))
    monkeypatch.setenv("AGS_METRICS_LOCK_FILE", str(tmp_path / "master_metrics.lock"))
    monkeypatch.setenv("AGS_METRICS_SALT_FILE", str(tmp_path / "metrics_salt"))
    # Recargar el módulo para que tome las rutas del env.
    import importlib
    import shared.metrics as m

    importlib.reload(m)
    return m, tmp_path


def test_arranca_en_cero(metrics_env):
    m, _ = metrics_env
    data = m.get_app_metrics("demo_app")
    assert data["total_visits"] == 0
    assert data["unique_users"] == 0


def test_update_incrementa_solo_esa_app(metrics_env):
    m, tmp = metrics_env
    h1 = m.make_user_hash("sesion-a")
    h2 = m.make_user_hash("sesion-b")
    assert m.update_metrics("app_a", user_hash=h1) == 1
    assert m.update_metrics("app_a", user_hash=h1) == 2  # misma persona
    assert m.update_metrics("app_a", user_hash=h2) == 3
    assert m.update_metrics("app_b", user_hash=h1) == 1

    a = m.get_app_metrics("app_a")
    b = m.get_app_metrics("app_b")
    assert a["total_visits"] == 3
    assert a["unique_users"] == 2
    assert b["total_visits"] == 1
    assert b["unique_users"] == 1

    raw = json.loads((tmp / "master_metrics.json").read_text(encoding="utf-8"))
    assert "total_visits_global" not in raw
    assert "global_hashes" not in raw
    assert set(raw["apps"]) == {"app_a", "app_b"}


def test_hash_con_sal_no_es_texto_plano(metrics_env):
    m, tmp = metrics_env
    h = m.make_user_hash("token-opaco-123")
    assert "token-opaco" not in h
    assert len(h) == 32
    assert (tmp / "metrics_salt").exists()
    # misma entrada → mismo hash
    assert m.make_user_hash("token-opaco-123") == h


def test_ciudad_por_defecto(metrics_env):
    m, _ = metrics_env
    h = m.make_user_hash("x")
    m.update_metrics("app_c", user_hash=h)  # city default
    cities = m.get_app_metrics("app_c")["cities"]
    assert cities.get("desconocida") == 1


def test_escritura_atomica_y_lock(metrics_env):
    m, tmp = metrics_env
    h = m.make_user_hash("z")
    m.update_metrics("app_d", user_hash=h)
    path = tmp / "master_metrics.json"
    assert path.exists()
    # no deben quedar temporales
    leftovers = list(tmp.glob(".metrics_*.tmp"))
    assert leftovers == []


def test_tope_hashes_no_infla_unicos(metrics_env, monkeypatch):
    m, _ = metrics_env
    monkeypatch.setattr(m, "MAX_HASHES_PER_APP", 2)
    t1 = m.update_metrics("capped", user_hash=m.make_user_hash("u1"))
    t2 = m.update_metrics("capped", user_hash=m.make_user_hash("u2"))
    t3 = m.update_metrics("capped", user_hash=m.make_user_hash("u3"))
    assert (t1, t2, t3) == (1, 2, 3)
    data = m.get_app_metrics("capped")
    assert data["total_visits"] == 3
    assert data["unique_users"] == 2  # no crece al superar el tope


def test_requiere_user_hash(metrics_env):
    m, _ = metrics_env
    with pytest.raises(ValueError):
        m.update_metrics("app", user_hash="")


def test_render_app_metrics_solo_esta_app(metrics_env, monkeypatch):
    """render_app_metrics no debe hablar de totales globales ni otras apps."""
    m, _ = metrics_env
    h = m.make_user_hash("r1")
    m.update_metrics("sola", user_hash=h)
    m.update_metrics("otra", user_hash=h)

    calls = {"markdown": [], "metric": []}

    class FakeSt:
        def markdown(self, body, unsafe_allow_html=False):
            calls["markdown"].append(body)

        def metric(self, *a, **k):
            calls["metric"].append((a, k))

        def info(self, *a, **k):
            pass

    import sys
    import types

    fake = types.ModuleType("streamlit")
    fake_obj = FakeSt()
    for name in ("markdown", "metric", "info"):
        setattr(fake, name, getattr(fake_obj, name))
    monkeypatch.setitem(sys.modules, "streamlit", fake)

    m.render_app_metrics("sola")
    joined = "\n".join(calls["markdown"])
    assert "Visitas de Sola" in joined or "Visitas de sola" in joined or "Sola" in joined
    assert "Ecosistema" not in joined
    assert "Totales" not in joined or "Históricas Totales" not in joined
    assert "otra" not in joined.lower()
    assert "1" in joined  # visitas de sola


def test_render_visit_badge_solo_esta_app(metrics_env, monkeypatch):
    m, _ = metrics_env
    m.update_metrics("badge_app", user_hash=m.make_user_hash("b1"))
    m.update_metrics("otra_app", user_hash=m.make_user_hash("b1"))
    m.update_metrics("otra_app", user_hash=m.make_user_hash("b2"))

    calls = []

    class FakeSt:
        def markdown(self, body, unsafe_allow_html=False):
            calls.append(body)

    import sys, types
    fake = types.ModuleType("streamlit")
    fake.markdown = FakeSt().markdown
    monkeypatch.setitem(sys.modules, "streamlit", fake)

    m.render_visit_badge("badge_app")
    assert len(calls) == 1
    body = calls[0]
    assert "visitas" in body
    assert "👀" in body
    assert "1" in body  # solo badge_app tiene 1 visita
    assert "Ecosistema" not in body
    assert "otra_app" not in body
    # formato español de miles en helper
    assert m._format_es(1234) == "1.234"
