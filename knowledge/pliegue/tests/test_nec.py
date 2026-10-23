import numpy as np
import warpcalc as w
from warpcalc.nec import _einstein
import warpcalc.metrics as m


def test_einstein_tensor_matches_alcubierre_eq19():
    _, ff = _einstein()
    xx, yy = 0.6, 0.7
    f = float(ff(0, xx, yy, 0, 0.5, 1, 8))
    num = w.T_kk(0, xx, yy, 0, 0.5, 1, 8, (1, 0.5 * f, 0, 0))
    r = np.hypot(xx, yy)
    ana = -(0.5**2 / (32 * np.pi)) * (yy**2 / r**2) * m._dshape(r, 1, 8) ** 2
    assert abs(num - ana) < 1e-9


def test_anec_negative_through_wall():
    assert w.anec_x_ray(0.5, vv=0.5, RR=1.0, ss=8.0, n=301) < 0


def test_energy_approx_matches_grid():
    x, y, z, h = w.grid(2.0, 81)
    num = w.total_energy(w.alcubierre_rho_analytic(x, y, z, 1e3, 1, 8), h)
    assert abs(num / w.energia_total_aprox(1e3, 1, 8) - 1) < 0.05


def test_casimir_1um():
    assert abs(w.casimir_energy_density(1e-6) + 4.33e-4) < 1e-6
