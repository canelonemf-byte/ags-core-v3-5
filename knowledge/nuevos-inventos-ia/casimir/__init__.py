"""casimir: presión de Casimir entre placas ideales, P = π²ħc/(240 d⁴), y la fuerza del sensor A2 del documento del autor (d = 50 nm, A = 1e-4 m², eps 55 y 57). AVISO: el factor (eps−1)/(eps+1) del autor es una aproximación heurística, no la teoría de Lifshitz. Por debajo de unos 100 nm tampoco valen las placas ideales.

Referencias (verificadas):
Lamoreaux S.K. (1997) Demonstration of the Casimir Force in the 0.6 to 6 µm Range. Phys. Rev. Lett. 78, 5. doi:10.1103/PhysRevLett.78.5

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np
from .pendientes import cargar, dato

HBAR = 1.054571817e-34; C = 299792458.0


def casimir_pressure(d):
    return np.pi**2 * HBAR * C / (240 * d**4)


def autor_force(d, eps, A):
    """Fórmula del autor (heurística): F = P(d) * (eps-1)/(eps+1) * A."""
    return casimir_pressure(d) * (eps - 1) / (eps + 1) * A


def run(cfg=None):
    cfg = cfg or cargar()
    d, o = dato(cfg, "distancia_m"); A, _ = dato(cfg, "area_m2"); e1, _ = dato(cfg, "eps_estado_1"); e2, _ = dato(cfg, "eps_estado_2")
    F1, F2 = autor_force(float(d), float(e1), float(A)), autor_force(float(d), float(e2), float(A))
    return {"F1_N": F1, "F2_N": F2, "delta_F_N": F2 - F1, "origen": o, "aviso": "factor dieléctrico heurístico"}
