import numpy as np
import pytest
from warpcalc import qi
from warpcalc.pendientes import cargar, DatoPendiente


def test_bound_scaling():
    assert np.isclose(qi.ford_roman_bound(1e-9) / qi.ford_roman_bound(2e-9), 16)
    assert qi.ford_roman_bound(1.0) < 0


def test_p001_pending():
    with pytest.raises(DatoPendiente, match="tau_muestreo_s"):
        qi.reproducir_p001(cargar())
