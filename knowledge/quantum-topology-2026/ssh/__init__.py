"""ssh: número de winding del modelo SSH (Su, Schrieffer y Heeger 1979, doi:10.1103/PhysRevLett.42.1698), calculado
numéricamente; nu = 1 si |w| > |v| (fase topológica) y 0 si |w| < |v|. Incluye espectro de cadena abierta con estados de borde.
Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np


def winding_number(v, w, nk=2001):
    k = np.linspace(-np.pi, np.pi, nk)
    h = v + w * np.exp(1j * k)
    ph = np.unwrap(np.angle(h))
    return int(round((ph[-1] - ph[0]) / (2 * np.pi)))


def open_chain_spectrum(v, w, cells=40):
    n = 2 * cells
    H = np.zeros((n, n))
    for i in range(n - 1):
        H[i, i + 1] = H[i + 1, i] = v if i % 2 == 0 else w
    return np.linalg.eigvalsh(H)
