import numpy as np
import liberacion as L


def test_fit_and_mechanism():
    t = np.linspace(0.1, 5, 30)
    k, n = L.fit_korsmeyer_peppas(t, L.korsmeyer_peppas(t, 0.1, 0.7))
    assert abs(n - 0.7) < 1e-6 and abs(k - 0.1) < 1e-6
    assert L.mechanism(0.5) == "fickiana" and L.mechanism(0.7).startswith("anómala") and L.mechanism(1.0).startswith("caso II")


def test_higuchi_and_arrhenius():
    assert np.isclose(L.higuchi_q(1e-6, 1.0, 2.0, 4.0), np.sqrt(1e-6 * 3 * 4))
    assert L.arrhenius(1e10, 5e4, 310) > L.arrhenius(1e10, 5e4, 298)

