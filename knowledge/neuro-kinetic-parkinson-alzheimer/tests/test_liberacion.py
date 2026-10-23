import numpy as np
import liberacion as L


def test_fit_recovers_k():
    t = np.linspace(0, 10, 20)
    assert abs(L.fit_higuchi(t, L.higuchi(t, 0.2)) - 0.2) < 1e-9


def test_t50():
    assert abs(L.time_to_fraction(0.5, "first", np.log(2)) - 1) < 1e-12
    assert abs(L.time_to_fraction(0.5, "higuchi", 0.25) - 4) < 1e-12
