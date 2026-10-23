"""fusionrate: reactividad térmica <sigma v> de D-T y D-3He con el ajuste de Bosch y Hale (1992).

Fuente (teoría de terceros): Bosch H.-S., Hale G.M. (1992), Improved formulas for fusion cross-sections
and thermal reactivities, Nuclear Fusion 32, 611-631, doi:10.1088/0029-5515/32/4/I07.
Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA.
ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np

# Tabla VII de Bosch y Hale (1992): BG [keV^0.5], mrc2 [keV], C1..C7; rango de validez [keV]
COEF = {
    "DT": dict(BG=34.3827, mrc2=1124656.0, C=(1.17302e-9, 1.51361e-2, 7.51886e-2, 4.60643e-3, 1.35e-2, -1.0675e-4, 1.366e-5), rango=(0.2, 100.0), energia_MeV=17.59),
    "DHe3": dict(BG=68.7508, mrc2=1124572.0, C=(5.51036e-10, 6.41918e-3, -2.02896e-3, -1.91080e-5, 1.35776e-4, 0.0, 0.0), rango=(0.5, 190.0), energia_MeV=18.35),
}


def reactivity(T_keV, reaccion="DT"):
    """<sigma v> en m^3/s para temperatura iónica T (keV), dentro del rango de validez del ajuste."""
    k = COEF[reaccion]
    T = np.asarray(T_keV, dtype=float)
    lo, hi = k["rango"]
    if np.any((T < lo) | (T > hi)):
        raise ValueError(f"T fuera del rango de validez {lo}-{hi} keV para {reaccion}")
    C1, C2, C3, C4, C5, C6, C7 = k["C"]
    theta = T / (1 - T * (C2 + T * (C4 + T * C6)) / (1 + T * (C3 + T * (C5 + T * C7))))
    xi = (k["BG"] ** 2 / (4 * theta)) ** (1 / 3)
    sv_cm3 = C1 * theta * np.sqrt(xi / (k["mrc2"] * T**3)) * np.exp(-3 * xi)
    return sv_cm3 * 1e-6


def fusion_power_density(n1, n2, T_keV, reaccion="DT"):
    """Potencia de fusión por unidad de volumen (W/m^3) para densidades n1, n2 (m^-3) de especies distintas."""
    return n1 * n2 * reactivity(T_keV, reaccion) * COEF[reaccion]["energia_MeV"] * 1.602176634e-13
