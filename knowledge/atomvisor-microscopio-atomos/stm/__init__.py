"""stm: corriente túnel en el modelo de barrera rectangular, I ∝ V exp(-2 kappa d), kappa = sqrt(2 m phi)/hbar.
Base física del microscopio de efecto túnel (Binnig et al. 1982, doi:10.1103/PhysRevLett.49.57). Modelo de referencia público.
Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np
HBAR = 1.054571817e-34; ME = 9.1093837015e-31; EV = 1.602176634e-19


def kappa(phi_eV):
    return np.sqrt(2 * ME * phi_eV * EV) / HBAR


def current_ratio(dd_m, phi_eV=4.5):
    """Factor de cambio de la corriente cuando la distancia punta-muestra aumenta dd metros."""
    return np.exp(-2 * kappa(phi_eV) * dd_m)


def gap_change_for_ratio(ratio, phi_eV=4.5):
    return -np.log(ratio) / (2 * kappa(phi_eV))
