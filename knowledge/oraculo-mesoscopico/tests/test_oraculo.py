import numpy as np
import pytest
import oraculo as o
from oraculo.pendientes import cargar, DatoPendiente


def test_quantized():
    assert np.isclose(o.landauer([1, 1, 1]) / o.G0, 3)
    assert abs(o.G0 - 7.748e-5) < 1e-8


def test_uncertainty_contains_mean():
    r = o.predecir([1.0, 0.5], [0.0, 0.1])
    assert r["ic95_S"][0] < r["G_media_S"] < r["ic95_S"][1]


def test_pending():
    with pytest.raises(DatoPendiente):
        o.run(cargar())
