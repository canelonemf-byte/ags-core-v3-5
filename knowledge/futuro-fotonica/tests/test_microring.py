import numpy as np
import pytest
import microring as m
from microring.pendientes import cargar, DatoPendiente


def test_critical_coupling_zero_on_resonance():
    R, n = 5e-6, 2.4
    lam = n * 2 * np.pi * R / 20
    assert m.allpass_transmission(lam, R, n, 0.95, 0.95) < 1e-12


def test_lossless_unity():
    assert np.allclose(m.allpass_transmission(np.linspace(1.5e-6, 1.6e-6, 50), 5e-6, 2.4, 0.9, 1.0), 1)


def test_pending():
    with pytest.raises(DatoPendiente, match="PENDIENTE"):
        m.run(cargar())
