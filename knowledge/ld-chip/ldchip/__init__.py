"""ldchip: modelos del documento LD-Chip del autor: absorbente saturable T(I) = exp(-alpha L / (1 + I/I_sat))
y eficiencia de memoria/detección eta = eta_abs * eta_hs * eta_read. Modelos estándar, parámetros a fijar con medidas.
Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np


def saturable_transmission(I, alpha_L, I_sat):
    return np.exp(-alpha_L / (1 + np.asarray(I, float) / I_sat))


def efficiency_chain(*etas):
    out = 1.0
    for e in etas:
        if not 0 <= e <= 1:
            raise ValueError("cada eficiencia debe estar entre 0 y 1")
        out *= e
    return out
