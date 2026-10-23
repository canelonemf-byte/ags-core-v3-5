import numpy as np
import pytest
from fractal import box_counting_dimension, sierpinski_carpet, run
from fractal.pendientes import cargar, DatoPendiente


def test_sierpinski_exact():
    D = box_counting_dimension(sierpinski_carpet(5), sizes=[1, 3, 9, 27, 81])
    assert abs(D - np.log(8) / np.log(3)) < 0.01


def test_line_and_square():
    sq = np.ones((256, 256), bool); ln = np.zeros((256, 256), bool); ln[128] = True
    assert abs(box_counting_dimension(sq) - 2) < 0.01 and abs(box_counting_dimension(ln) - 1) < 0.01


def test_example_runs_labelled():
    r = run(); assert r["origen"].startswith("ejemplo_publico")


def test_pending_without_example():
    cfg = cargar(); cfg["ruta_patron"]["ejemplo_publico"] = ""
    with pytest.raises(DatoPendiente, match="PENDIENTE: falta dato ruta_patron"):
        run(cfg)
