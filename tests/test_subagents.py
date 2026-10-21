import json, pytest
from registry import get_agent, agents_by_domain
from agents import subagents as sa
pytestmark = pytest.mark.unit

def test_registered():
    assert {a.name for a in agents_by_domain("subagentes")} == {c.name for c in sa.WORKERS} and len(sa.WORKERS) == 7

def test_llp_validator():
    v = sa.ValidadorEsquemaLLP.validate
    assert v({k: "" for k in sa.LLP_KEYS}) == []
    assert any("null" in e for e in v({"meta": None}))
    assert any("snake_case" in e for e in v({"nivelE": 1}))

def test_clean_no_null():
    assert sa._clean({"a": None, "b": [None]}) == {"a": "", "b": [""]}

@pytest.mark.parametrize("name", ["verificador_licencias", "revisor_evidencia_e0_e6", "validador_esquema_llp", "preflight_7b"])
def test_execute_real(name):
    out = get_agent(name).execute(write=False)
    assert out["estado"] in ("ok", "aviso") and "null" not in json.dumps(out)

def test_preflight_never_trains():
    out = get_agent("preflight_7b").execute(write=False)
    assert out["entrena"] is False and out["descarga_pesos"] is False and out["test_congelado_ok"] is True

def test_generador_no_toca_test(tmp_path, monkeypatch):
    before = sa._sha_file(sa.DATA / "test.jsonl")
    monkeypatch.setattr(sa, "ROOT", tmp_path)
    out = get_agent("generador_pares_lora").execute(write=False)
    assert out["toca_test"] is False and sa._sha_file(sa.DATA / "test.jsonl") == before == sa.TEST_SHA

def test_run_due_intervals(monkeypatch):
    calls = []
    for c in sa.WORKERS:
        monkeypatch.setattr(get_agent(c.name), "execute", lambda write=True, n=c.name: calls.append(n) or {})
    st = {}
    assert len(sa.run_due(st, now=10_000)) == 7
    assert sa.run_due(st, now=10_001) == []
