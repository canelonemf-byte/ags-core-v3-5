import numpy as np
import pytest
import blindaje as b
from blindaje.pendientes import cargar, DatoPendiente


def test_copper_skin_depth_1mhz():
    assert abs(b.skin_depth(1e6, 5.8e7) - 66e-6) < 2e-6


def test_absorption_one_skin_depth():
    d = b.skin_depth(1e6, 5.8e7)
    assert abs(b.shielding_db(1e6, d, 5.8e7)["absorcion_db"] - 8.686) < 1e-9


def test_pending():
    with pytest.raises(DatoPendiente, match="frecuencia_hz"):
        b.run(cargar())
