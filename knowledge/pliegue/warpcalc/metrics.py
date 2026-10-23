"""Densidad de energía medida por observadores eulerianos en métricas tipo warp.

Métrica (lapso 1, cortes planos):  ds^2 = -c^2 dt^2 + sum_i (dx^i - X^i dt)^2.
Con la ligadura hamiltoniana (R=0):  rho = c^4/(16 pi G) * (K^2 - K_ij K^ij)   [J/m^3],
con K_ij = (d_i X_j + d_j X_i)/(2c) (Natário 2002, ec. de la sección 2).
Para Alcubierre: rho = -(c^4/(32 pi G)) * (v/c)^2 * (y^2+z^2)/r^2 * (df/dr)^2 (Alcubierre 1994, ec. 19).
"""
import numpy as np

C = 299_792_458.0
G = 6.67430e-11


def grid(L, n):
    """Malla cúbica [-L, L]^3 con n puntos por eje. Devuelve (x, y, z, h)."""
    a = np.linspace(-L, L, n)
    x, y, z = np.meshgrid(a, a, a, indexing="ij")
    return x, y, z, a[1] - a[0]


def alcubierre_shape(r, R, sigma):
    return (np.tanh(sigma * (r + R)) - np.tanh(sigma * (r - R))) / (2 * np.tanh(sigma * R))


def _dshape(r, R, sigma):
    sech2 = lambda u: 1.0 / np.cosh(u) ** 2
    return sigma * (sech2(sigma * (r + R)) - sech2(sigma * (r - R))) / (2 * np.tanh(sigma * R))


def alcubierre_rho_analytic(x, y, z, v, R, sigma):
    """Densidad de energía euleriana analítica (burbuja centrada en el origen), J/m^3."""
    r = np.sqrt(x**2 + y**2 + z**2)
    rho2 = y**2 + z**2
    with np.errstate(invalid="ignore", divide="ignore"):
        q = np.where(r > 0, rho2 / r**2, 0.0)
    return -(C**4 / (32 * np.pi * G)) * (v / C) ** 2 * q * _dshape(r, R, sigma) ** 2


def alcubierre_shift(x, y, z, v, R, sigma):
    r = np.sqrt(x**2 + y**2 + z**2)
    f = alcubierre_shape(r, R, sigma)
    return np.stack([v * f, 0 * f, 0 * f])


def natario_shift(x, y, z, v, R, sigma, h):
    """Campo de desplazamiento de divergencia nula: X = v * rot(n(r)/2 * (0, -z, y)),
    con n = forma de Alcubierre (n=1 dentro, 0 fuera). Derivadas por diferencias finitas."""
    r = np.sqrt(x**2 + y**2 + z**2)
    n = alcubierre_shape(r, R, sigma)
    A = np.stack([0 * n, -0.5 * n * z, 0.5 * n * y])
    d = lambda F, ax: np.gradient(F, h, axis=ax)
    return v * np.stack([d(A[2], 1) - d(A[1], 2), d(A[0], 2) - d(A[2], 0), d(A[1], 0) - d(A[0], 1)])


def eulerian_energy_density(X, h):
    """rho = c^4/(16 pi G) (K^2 - K_ij K^ij) para un desplazamiento X (3, n, n, n) en m/s."""
    D = [[np.gradient(X[j], h, axis=i) for j in range(3)] for i in range(3)]
    K = [[(D[i][j] + D[j][i]) / (2 * C) for j in range(3)] for i in range(3)]
    tr = K[0][0] + K[1][1] + K[2][2]
    kk = sum(K[i][j] ** 2 for i in range(3) for j in range(3))
    return C**4 / (16 * np.pi * G) * (tr**2 - kk)


def total_energy(rho, h):
    """Energía total (J) integrando rho en la malla; E/c^2 da la masa equivalente."""
    return float(np.sum(rho) * h**3)
