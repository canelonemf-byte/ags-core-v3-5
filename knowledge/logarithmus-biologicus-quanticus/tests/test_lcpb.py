import numpy as np
import lcpb


def test_formula_and_planet_sensitivity():
    assert np.isclose(lcpb.lcpb([10, 10], [1], S=1, m=0.5), 2.0)
    assert lcpb.lcpb([10, 10], [1]) > lcpb.lcpb([1, 1], [10])


def test_original_gamma_is_circular():
    a = lcpb.circular_lambda([10, 10], [1], 1, 0.3, 0.42)
    b = lcpb.circular_lambda([1, 2], [50], 3, 0.8, 0.42)
    assert np.isclose(a, 0.42) and np.isclose(b, 0.42)


def test_metropolis_recovers_mean():
    c = lcpb.metropolis_gaussian(-1.0, 0.5)[2000:]
    assert abs(c.mean() + 1.0) < 0.1
