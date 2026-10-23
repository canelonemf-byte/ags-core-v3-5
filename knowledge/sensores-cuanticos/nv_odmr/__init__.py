"""nv_odmr: magnetometría con centros NV en diamante (modelo de referencia público, no datos del autor).
D = 2,87 GHz, gamma_e = 28 GHz/T: Doherty M.W. et al. (2013) Physics Reports 528, 1-45, doi:10.1016/j.physrep.2013.02.001.
Incluye la ecuación del documento del autor f(B) = f0 + gamma B_loc para la lectura de campo.
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

NV = dict(D=2.87e9, E=0.0, gamma_e=28e9)


def field_from_splitting(df_hz, gamma_e=28e9):
    """Campo axial (T) a partir de la separación entre las dos líneas: df = 2 gamma B."""
    return df_hz / (2 * gamma_e)
