"""vb_spin: Hamiltoniano de espín S=1 del defecto V_B^- en hBN, con los parámetros del documento Q-MATRIX del autor
(D = 3,47 GHz, E = 60 MHz, gamma_e = 28 GHz/T, B = 5 mT, T1 = 20 µs, T2 = 3 µs), reescrito en numpy sin QuTiP.
Valor de D coherente con Gottscholl A. et al. (2020) Nature Materials 19, 540, doi:10.1038/s41563-020-0619-6.
Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np

SZ = np.diag([1.0, 0.0, -1.0])
SX = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) / np.sqrt(2)
SY = np.array([[0, -1j, 0], [1j, 0, -1j], [0, 1j, 0]]) / np.sqrt(2)


def hamiltonian(D, E, gamma_e, B):
    """H/h (Hz) = D (Sz^2 - 2/3) + E (Sx^2 - Sy^2) + gamma_e B Sz, campo B (T) a lo largo del eje del defecto."""
    return D * (SZ @ SZ - 2 / 3 * np.eye(3)) + E * (SX @ SX - SY @ SY).real + gamma_e * B * SZ


def odmr_frequencies(D, E, gamma_e, B):
    """Frecuencias de transición desde el estado de menor energía (Hz), ordenadas."""
    e = np.linalg.eigvalsh(hamiltonian(D, E, gamma_e, B))
    return np.sort(e[1:] - e[0])


def odmr_spectrum(f, D, E, gamma_e, B, linewidth, contrast=0.02):
    """Fluorescencia normalizada con dos caídas lorentzianas (modelo estándar de ODMR de onda continua)."""
    s = np.ones_like(f, dtype=float)
    for f0 in odmr_frequencies(D, E, gamma_e, B):
        s -= contrast * (linewidth / 2) ** 2 / ((f - f0) ** 2 + (linewidth / 2) ** 2)
    return s


def coherence_decay(t, T2):
    return np.exp(-np.asarray(t, float) / T2)

PARAMS_AUTOR = dict(D=3.47e9, E=60e6, gamma_e=28e9, B=0.005, T1=20e-6, T2=3e-6)
