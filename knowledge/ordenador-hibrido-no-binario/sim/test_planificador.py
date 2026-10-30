"""Test mínimo del planificador: reproducibilidad y coherencia (E2, no física)."""
import json, shutil, subprocess, sys, pathlib

def _run(tmp):
    src = pathlib.Path(__file__).parent
    for f in ("planificador.py", "sim_mvm.py", "parametros.yaml"):
        shutil.copy(src / f, tmp / f)
    # necesita resultados MVM
    subprocess.run([sys.executable, str(tmp / "sim_mvm.py")], check=True, cwd=tmp)
    subprocess.run([sys.executable, str(tmp / "planificador.py")], check=True, cwd=tmp)
    return json.load(open(tmp / "salidas" / "planificador_resultados.json"))

def test_planificador_reproducible(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(); b.mkdir()
    ra, rb = _run(a), _run(b)
    assert ra["comparacion"] == rb["comparacion"]
    assert ra["tipo"] == "simulacion" and ra["nivel_evidencia"] == "E2"
    assert "supuestos" in ra and len(ra["supuestos"]) >= 3
    # el consciente de error no debe asignar CIM a tareas con error_max < error del destino
    for t, a in ra["resultados"]["error_coste_aware"]["asignacion"].items():
        assert a["error_rel_modelo"] <= a["error_max_tarea"] + 1e-12
    # HEFT y aware producen makespan finito y energía > 0
    for alg in ("HEFT", "error_coste_aware"):
        assert ra["resultados"][alg]["makespan"] > 0
        assert ra["resultados"][alg]["energia_total_pj"] > 0
