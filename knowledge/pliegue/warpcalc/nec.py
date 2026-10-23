"""Tensor de Einstein simbólico de la métrica de Alcubierre y verificación de NEC/ANEC.

Unidades geométricas G = c = 1 (longitudes en unidades de R si R = 1). T_ab = G_ab / (8 pi).
Métrica (Alcubierre 1994, doi:10.1088/0264-9381/11/5/001):
  ds^2 = -dt^2 + (dx - v f(r_s) dt)^2 + dy^2 + dz^2,  r_s = sqrt((x - v t)^2 + y^2 + z^2).
"""
from functools import lru_cache
import numpy as np
import sympy as sp

t, x, y, z = sp.symbols("t x y z", real=True)
v, R, s = sp.symbols("v R sigma", positive=True)


@lru_cache(maxsize=1)
def _einstein():
    rs = sp.sqrt((x - v * t) ** 2 + y**2 + z**2)
    f = (sp.tanh(s * (rs + R)) - sp.tanh(s * (rs - R))) / (2 * sp.tanh(s * R))
    X = [t, x, y, z]
    g = sp.Matrix([[-1 + v**2 * f**2, -v * f, 0, 0], [-v * f, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    gi = sp.simplify(g.inv())
    Gam = [[[sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(4)) / 2
             for c in range(4)] for b in range(4)] for a in range(4)]
    def Ric(b, c):
        return sum(sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c])
                   + sum(Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a] for d in range(4)) for a in range(4))
    Rm = sp.Matrix(4, 4, lambda b, c: Ric(b, c))
    Rs = sum(gi[a, b] * Rm[a, b] for a in range(4) for b in range(4))
    Gm = Rm - g * Rs / 2
    return sp.lambdify((t, x, y, z, v, R, s), Gm, "numpy"), sp.lambdify((t, x, y, z, v, R, s), f, "numpy")


def T_kk(tt, xx, yy, zz, vv, RR, ss, k):
    """T_ab k^a k^b en un punto (unidades geométricas)."""
    Gf, _ = _einstein()
    G = np.array(Gf(tt, xx, yy, zz, vv, RR, ss), dtype=float)
    k = np.asarray(k, float)
    return float(k @ G @ k) / (8 * np.pi)


def anec_x_ray(b, vv=0.5, RR=1.0, ss=8.0, L=3.0, n=4001, sentido=+1):
    """Integral de T_ab k^a k^b a lo largo de la curva nula en t=0 que cruza la burbuja paralela a x
    con parámetro de impacto b (en y). k = (1, v f + sentido, 0, 0) es nulo exactamente; se integra en x
    (aproximación de rayo recto: ignora la desviación transversal, que P001 anota como riesgo)."""
    _, ff = _einstein()
    xs = np.linspace(-L, L, n)
    vals = []
    for xx in xs:
        f = float(ff(0.0, xx, b, 0.0, vv, RR, ss))
        k = (1.0, vv * f + sentido, 0.0, 0.0)
        vals.append(T_kk(0.0, xx, b, 0.0, vv, RR, ss, k) / abs(k[1]))  # dλ ∝ dx/|k^x|
    return float(np.trapezoid(vals, xs))


def energia_total_aprox(v_m_s, R_m, sigma_1_m):
    """E ≈ -c^2 v^2 R^2 sigma / (36 G) para pared fina (sigma R >> 1), en julios (deducida de Alcubierre ec. 19)."""
    from .metrics import C, G
    return -(C**2) * v_m_s**2 * R_m**2 * sigma_1_m / (36 * G)


def casimir_energy_density(a_m):
    """Densidad de energía de Casimir entre placas ideales: -pi^2 hbar c / (720 a^4), J/m^3."""
    from .bounds import HBAR, C
    return -np.pi**2 * HBAR * C / (720 * a_m**4)
