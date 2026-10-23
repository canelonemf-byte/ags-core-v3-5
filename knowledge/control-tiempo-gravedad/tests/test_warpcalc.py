import numpy as np
import warpcalc as w


def test_shape_limits():
    assert abs(w.alcubierre_shape(np.array(0.0), 1.0, 8.0) - 1) < 1e-6
    assert w.alcubierre_shape(np.array(5.0), 1.0, 8.0) < 1e-10


def test_alcubierre_numeric_matches_analytic():
    x, y, z, h = w.grid(2.0, 81)
    v, R, s = 1e3, 1.0, 4.0
    num = w.eulerian_energy_density(w.alcubierre_shift(x, y, z, v, R, s), h)
    ana = w.alcubierre_rho_analytic(x, y, z, v, R, s)
    m = np.abs(ana) > 0.05 * np.abs(ana).max()
    rel = np.abs(num[m] - ana[m]) / np.abs(ana[m])
    assert np.median(rel) < 0.02


def test_energy_density_negative():
    x, y, z, h = w.grid(2.0, 41)
    ana = w.alcubierre_rho_analytic(x, y, z, 1e3, 1.0, 4.0)
    assert ana.max() <= 0 and ana.min() < 0
    assert w.total_energy(ana, h) < 0


def test_natario_zero_expansion_and_negative():
    x, y, z, h = w.grid(2.0, 61)
    X = w.natario_shift(x, y, z, 1e3, 1.0, 4.0, h)
    div = sum(np.gradient(X[i], h, axis=i) for i in range(3))
    inner = (slice(5, -5),) * 3
    assert np.abs(div[inner]).max() < 1e-2 * np.abs(X).max()
    assert abs(X[0][30, 30, 30] - 1e3) < 1.0  # dentro de la burbuja se mueve a v
    rho = w.eulerian_energy_density(X, h)
    assert w.total_energy(rho[inner], h) < 0


def test_planck_and_wall_bound():
    assert abs(w.planck_length() - 1.616e-35) < 1e-38
    assert w.pfenning_ford_wall_bound(1.0) < 1e-32


def test_redshift_chou2010_order():
    # Chou et al. 2010 midieron (4.1 ± 1.6)e-17 para ~33 cm
    assert 2.5e-17 < w.gravitational_redshift(0.33) < 5.7e-17
