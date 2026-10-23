import numpy as np
import vb_spin as v
P = v.PARAMS_AUTOR


def test_zero_field_lines_D_pm_E():
    f = v.odmr_frequencies(P["D"], P["E"], P["gamma_e"], 0.0)
    assert np.allclose(f, [P["D"] - P["E"], P["D"] + P["E"]], rtol=1e-9)


def test_zeeman_slope_high_field():
    f1 = v.odmr_frequencies(P["D"], P["E"], P["gamma_e"], 0.05)
    f2 = v.odmr_frequencies(P["D"], P["E"], P["gamma_e"], 0.06)
    assert abs((f2[1] - f1[1]) / 0.01 - P["gamma_e"]) / P["gamma_e"] < 0.01


def test_spectrum_dips():
    f = np.linspace(3.3e9, 3.65e9, 4001)
    s = v.odmr_spectrum(f, P["D"], P["E"], P["gamma_e"], P["B"], 50e6)
    assert s.min() < 0.99 and s.max() <= 1
