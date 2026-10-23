import numpy as np
import nv_odmr as n


def test_nv_lines_and_inverse():
    B = 1e-3
    f = n.odmr_frequencies(n.NV["D"], 0.0, n.NV["gamma_e"], B)
    assert np.allclose(f, [2.87e9 - 28e6, 2.87e9 + 28e6])
    assert abs(n.field_from_splitting(f[1] - f[0]) - B) < 1e-12
