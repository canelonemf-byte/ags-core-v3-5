import numpy as np
import pytest
import chladni as c
from chladni.pendientes import cargar, DatoPendiente

AL = dict(E=69e9, nu=0.33, rho=2700)


def test_scaling_with_thickness_and_mode():
    f1 = c.mode_frequency(1, 1, 0.3, 0.3, 1e-3, **AL)
    assert np.isclose(c.mode_frequency(1, 1, 0.3, 0.3, 2e-3, **AL), 2 * f1)
    assert np.isclose(c.mode_frequency(2, 2, 0.3, 0.3, 1e-3, **AL), 4 * f1)


def test_nodal_zero_on_edges():
    p = c.nodal_pattern(2, 3, 1, 1)
    assert np.allclose(p[0], 0) and np.allclose(p[:, 0], 0)


def test_pending_geometry():
    with pytest.raises(DatoPendiente, match="lado_a_m"):
        c.run(cargar())
