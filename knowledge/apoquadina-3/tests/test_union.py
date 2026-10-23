import union as u


def test_half_at_kd_and_inverse():
    assert u.occupancy(45.0) == 0.5
    assert abs(u.conc_for_occupancy(0.9) - 405.0) < 1e-9
