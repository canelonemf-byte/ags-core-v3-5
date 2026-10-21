import importlib.util, pathlib, pytest
pytestmark = pytest.mark.unit
spec = importlib.util.spec_from_file_location("sim", pathlib.Path(__file__).parents[1] / "scripts/sim_subagentes.py")
sim = importlib.util.module_from_spec(spec); spec.loader.exec_module(sim)

def test_sim_labelled_and_scales():
    a = sim.simular(n=10, tareas=2000); b = sim.simular(n=1000, tareas=2000)
    assert a["simulacion"] is True and a["resultado"]["completadas"] == 2000
    assert b["resultado"]["latencia_p50_s"] < a["resultado"]["latencia_p50_s"]
