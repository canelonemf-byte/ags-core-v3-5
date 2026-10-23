import numpy as np
from canelone_sim import Circuit


def test_bell():
    p = Circuit(2).h(0).cx(0, 1).probabilities()
    assert np.allclose(p, [0.5, 0, 0, 0.5])


def test_ghz3():
    p = Circuit(3).h(0).cx(0, 1).cx(1, 2).probabilities()
    assert np.isclose(p[0], 0.5) and np.isclose(p[7], 0.5)


def test_norm_and_x():
    c = Circuit(3).x(2)
    assert np.isclose(c.probabilities().sum(), 1) and np.isclose(c.probabilities()[1], 1)
