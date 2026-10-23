"""Desigualdad cuántica de Ford-Roman (1997) para un campo escalar sin masa en Minkowski 4D, con muestreo lorentziano:
<rho>_tau >= -3 hbar / (32 pi^2 c^3 tau^4). Ford L.H., Roman T.A. (1997) Phys. Rev. D 55, 2082, doi:10.1103/PhysRevD.55.2082.
Sirve para reproducir la cifra "QI 1e50" de P001 cuando se declaren tau y la densidad comparada (datos_pendientes.yaml).
Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. MIT.
"""
import numpy as np
from .pendientes import cargar, dato
HBAR = 1.054571817e-34; C = 299792458.0


def ford_roman_bound(tau_s):
    return -3 * HBAR / (32 * np.pi**2 * C**3 * tau_s**4)


def violation_factor(rho_j_m3, tau_s):
    return abs(rho_j_m3) / abs(ford_roman_bound(tau_s))


def reproducir_p001(cfg=None):
    cfg = cfg or cargar()
    tau = float(dato(cfg, "tau_muestreo_s")[0]); rho = float(dato(cfg, "densidad_negativa_j_m3")[0])
    return {"cota_J_m3": ford_roman_bound(tau), "factor_violacion": violation_factor(rho, tau)}
