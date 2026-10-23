import stm


def test_order_of_magnitude_per_angstrom():
    # con phi ~4-5 eV la corriente cae ~un orden de magnitud por ångström
    r = stm.current_ratio(1e-10, 4.5)
    assert 0.05 < r < 0.2


def test_inverse():
    assert abs(stm.gap_change_for_ratio(stm.current_ratio(2e-10)) - 2e-10) < 1e-15
