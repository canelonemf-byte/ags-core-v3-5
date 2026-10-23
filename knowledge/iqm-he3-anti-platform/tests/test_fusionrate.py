import numpy as np
import pytest
import fusionrate as f


def test_dt_10keV_bosch_hale_table():
    # Bosch y Hale 1992, tabla VIII: D-T a 10 keV = 1.136e-16 cm^3/s
    assert abs(f.reactivity(10.0, "DT") / 1.136e-22 - 1) < 0.01


def test_dhe3_much_lower_than_dt_at_10keV():
    assert f.reactivity(10.0, "DHe3") < 0.01 * f.reactivity(10.0, "DT")


def test_dhe3_increases_with_T():
    T = np.array([10, 50, 100, 150])
    assert np.all(np.diff(f.reactivity(T, "DHe3")) > 0)


def test_range_check():
    with pytest.raises(ValueError):
        f.reactivity(500.0, "DT")


def test_power_density_positive():
    assert f.fusion_power_density(5e19, 5e19, 15.0) > 0
