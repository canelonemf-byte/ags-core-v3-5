"""Test mínimo de sim_mvm.py: ejecuta en una copia temporal y comprueba salidas coherentes.
No valida el modelo físico (E2: supuestos), solo que la simulación es reproducible y consistente."""
import csv, shutil, subprocess, sys, pathlib

def _run(tmp):
    src = pathlib.Path(__file__).parent
    for f in ("sim_mvm.py", "parametros.yaml"):
        shutil.copy(src / f, tmp / f)
    subprocess.run([sys.executable, str(tmp / "sim_mvm.py")], check=True, cwd=tmp)
    return list(csv.DictReader(open(tmp / "salidas" / "resultados.csv")))

def test_sim_mvm_reproducible(tmp_path):
    a = tmp_path / "a"; b = tmp_path / "b"; a.mkdir(); b.mkdir()
    ra, rb = _run(a), _run(b)
    assert ra == rb  # semilla fija
    assert ra[0]["config"] == "cmos_digital" and float(ra[0]["ahorro_vs_cmos"]) == 0.0
    assert float(ra[0]["error_rel"]) < 0.05  # CMOS 8 bits ~ exacto
    for r in ra:
        assert float(r["error_rel"]) >= 0.0  # algunas configs CIM de pocos niveles/bits superan 1.0 (salida inútil): es un resultado, no un fallo
        assert float(r["energia_total_pj"]) > 0
        assert 0.0 <= float(r["frac_adc_dac"]) <= 1.0
