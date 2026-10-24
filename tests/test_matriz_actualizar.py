import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "app"))

def test_registrado_y_programado(monkeypatch):
    import agents.matriz_el_prat_agents as mx
    monkeypatch.setattr(mx, "actualizar_todo", lambda: {"estado": "ok"})
    st = {}
    assert mx.run_weekly_due(st, now=1e9) and not mx.run_weekly_due(st, now=1e9 + 3600)
    assert mx.MatrizActualizarTodo.name == "matriz_actualizar_todo"
