import numpy as np
import pytest
import breit_rabi as b
from breit_rabi.pendientes import cargar, DatoPendiente


def test_zero_field_splitting_hydrogen_like():
    lv = b.breit_rabi(0.0, 1.420405751e9, 0.5)
    E = sorted(set(round(e, 3) for _, _, e in lv))
    assert np.isclose(E[-1] - E[0], 1.420405751e9)
    assert len(lv) == 4


def test_stretched_state_linear():
    dE = 1e9; B = 1e-3
    e0 = [e for F, m, e in b.breit_rabi(0, dE, 0.5) if m == 1][0]
    e1 = [e for F, m, e in b.breit_rabi(B, dE, 0.5) if m == 1][0]
    assert np.isclose(e1 - e0, 2.00231930436 * b.MU_B * B / b.H / 2, rtol=1e-6)


def test_pending():
    with pytest.raises(DatoPendiente):
        b.run(cargar())
