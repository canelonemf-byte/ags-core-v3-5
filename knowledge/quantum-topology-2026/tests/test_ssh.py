import numpy as np
import ssh


def test_phases():
    assert ssh.winding_number(0.5, 1.0) == 1 and ssh.winding_number(1.0, 0.5) == 0


def test_edge_modes():
    e = ssh.open_chain_spectrum(0.3, 1.0)
    assert np.sum(np.abs(e) < 1e-3) == 2
    assert np.sum(np.abs(ssh.open_chain_spectrum(1.0, 0.3)) < 1e-3) == 0
