import importlib.util, pathlib, pytest
pytestmark = pytest.mark.unit
spec = importlib.util.spec_from_file_location("near_dup", pathlib.Path(__file__).parents[1] / "scripts/near_dup.py")
nd = importlib.util.module_from_spec(spec); spec.loader.exec_module(nd)

def test_norm_and_cosine():
    assert nd.norm("  Hola\n MUNDO ") == "hola mundo"
    p = nd.cosine_pairs(["el gato come pescado azul en la cocina de la casa grande", "el gato come pescado azul en la cocina de la casa grande hoy", "teoría cuántica de campos"], 0.85)
    assert [(i, j) for i, j, _ in p] == [(0, 1)]

def test_leaks_detects_cross_split():
    a = {"split": "train", "file": "t", "line": 1, "id": "x"}; b = {"split": "test", "file": "s", "line": 2, "id": "y"}
    assert len(nd.leaks([], [{"similitud": 0.9, "a": a, "b": b}], [])) == 1
    assert nd.leaks([], [{"similitud": 0.9, "a": a, "b": dict(a, line=3)}], []) == []
