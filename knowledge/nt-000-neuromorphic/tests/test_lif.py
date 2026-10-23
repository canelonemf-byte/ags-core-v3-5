import numpy as np
import lif


def test_subthreshold_no_spikes():
    _, s = lif.simulate(np.full(5000, 1e-9))
    assert s == []


def test_rate_matches_theory():
    I = 3e-9
    _, s = lif.simulate(np.full(20000, I), dt=1e-5)
    rate = len(s) / 0.2
    assert abs(rate - lif.rate_theory(I)) / lif.rate_theory(I) < 0.05
