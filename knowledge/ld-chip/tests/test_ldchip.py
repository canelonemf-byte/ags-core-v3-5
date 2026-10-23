import numpy as np
import ldchip as l


def test_saturable_limits():
    assert np.isclose(l.saturable_transmission(0, 2.0, 1.0), np.exp(-2))
    assert l.saturable_transmission(1e6, 2.0, 1.0) > 0.999


def test_chain():
    assert np.isclose(l.efficiency_chain(0.9, 0.8, 0.5), 0.36)
