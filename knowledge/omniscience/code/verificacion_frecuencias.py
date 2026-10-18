"""ADICIÓN NUEVA (ORÁCULO, 2026-10-18), no forma parte del código original de C-VIB-001.
Comprobación analítica independiente de H3: frecuencias de una cuerda fija-fija
f_n = n·c/(2L), con c = sqrt(T/mu). No altera simular_vibraciones.py (allí sigue el xfail).
Método: autovalores de la discretización por diferencias finitas de u_tt = c² u_xx."""
import numpy as np
from scipy.linalg import eigh_tridiagonal

def frecuencias_cuerda(L=1.0, T=1.0, mu=1.0, N=2000, n_modos=6):
    c = np.sqrt(T / mu); h = L / (N + 1)
    d = np.full(N, 2.0) * c**2 / h**2; e = np.full(N - 1, -1.0) * c**2 / h**2
    w2 = eigh_tridiagonal(d, e, select="i", select_range=(0, n_modos - 1))[0]
    return np.sqrt(w2) / (2 * np.pi), c / (2 * L)

if __name__ == "__main__":
    f, f1 = frecuencias_cuerda()
    for n, fn in enumerate(f, 1):
        print(f"n={n}: f_num={fn:.6f}  n·f1={n*f1:.6f}  err_rel={abs(fn-n*f1)/(n*f1):.2e}")
