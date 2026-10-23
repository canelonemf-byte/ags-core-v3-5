import swcnt as s


def test_10_10_armchair():
    assert abs(s.diameter_nm(10, 10) - 1.356) < 0.01
    assert s.is_metallic(10, 10) and s.kind(10, 10) == "armchair"
    assert abs(s.chiral_angle_deg(10, 10) - 30) < 1e-9


def test_6_5_semiconducting():
    assert abs(s.diameter_nm(6, 5) - 0.747) < 0.01 and not s.is_metallic(6, 5)


def test_candidates():
    c = s.candidates(0.7, 0.8)
    assert {"n": 6, "m": 5} in [{"n": x["n"], "m": x["m"]} for x in c]
