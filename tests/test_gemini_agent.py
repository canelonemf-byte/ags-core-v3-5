"""Tests del agente gemini_reviewer sin red (mock httpx)."""
import pytest
from registry import get_agent, agents_by_domain

pytestmark = pytest.mark.unit


def test_registered():
    names = {a.name for a in agents_by_domain("validation")}
    assert "gemini_reviewer" in names
    a = get_agent("gemini_reviewer")
    assert a.preferred_model.startswith("gemini")
    assert "Segunda opinión" in a.description or "segunda" in a.description.lower()


@pytest.mark.asyncio
async def test_degraded_when_proxy_down(monkeypatch):
    """Sin LiteLLM / red: no lanza; status=degraded."""
    import agents.gemini_agent as ga
    monkeypatch.setenv("AGS_GEMINI_OFF", "1")
    # Re-instantiate to pick env? Agent already constructed; run checks env each call.
    out = await get_agent("gemini_reviewer").run("contrasta esto")
    assert out["status"] == "degraded"
    assert out["model_used"] == ""
    assert "degradado" in out["output"].lower()


@pytest.mark.asyncio
async def test_ok_with_mocked_litellm(monkeypatch):
    """Con respuesta mock de LiteLLM: status=ok y model_used gemini."""
    import httpx

    class _Resp:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "Hallazgos: ok\nHuecos: ninguno\nConclusión: coherente"}}]}

    class _Client:
        def __init__(self, *a, **k):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def post(self, path, json=None):
            assert path == "/chat/completions"
            assert json["model"].startswith("gemini") or json["model"] == "grok"
            return _Resp()

    monkeypatch.delenv("AGS_GEMINI_OFF", raising=False)
    monkeypatch.setattr(httpx, "AsyncClient", _Client)
    out = await get_agent("gemini_reviewer").run(
        "revisa cifras", context={"resultado_previo": "Grok dice saldo 13 M€"}
    )
    assert out["status"] == "ok"
    assert out["model_used"].startswith("gemini")
    assert "Hallazgos" in out["output"]
    assert out["evidencia"] == "E0_proveedor"


@pytest.mark.asyncio
async def test_degraded_on_http_error(monkeypatch):
    import httpx

    class _Client:
        def __init__(self, *a, **k):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def post(self, path, json=None):
            raise httpx.ConnectError("proxy down")

    monkeypatch.delenv("AGS_GEMINI_OFF", raising=False)
    monkeypatch.setattr(httpx, "AsyncClient", _Client)
    out = await get_agent("gemini_reviewer").run("x")
    assert out["status"] == "degraded"
