"""lubricacion: espesor mínimo de película en contacto blando isoviscoso-elástico, H_min = 7,43(1 − 0,85 e^(−0,31k)) U^0,65 W^(−0,21) con h = H·Rx (Hamrock y Dowson 1978), y razón lambda = h/sqrt(Rq1² + Rq2²) para identificar el régimen de lubricación. Modelo de ingeniería que no sustituye ensayos en cartílago.

Referencias (verificadas):
Hamrock B.J., Dowson D. (1978) Elastohydrodynamic Lubrication of Elliptical Contacts for Materials of Low Elastic Modulus I—Fully Flooded Conjunction. J. Lubr. Technol. 100, 236. doi:10.1115/1.3453152

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia: Todos los derechos reservados. Confidencial (ver LICENSE).
"""
import numpy as np
from .pendientes import cargar, dato


def e_reducido(E1, nu1, E2, nu2):
    """E' = 2 / ((1-nu1^2)/E1 + (1-nu2^2)/E2)."""
    return 2 / ((1 - nu1**2) / E1 + (1 - nu2**2) / E2)


def h_min_soft(eta0, u, w, Rx, Ep, k=1.0):
    U = eta0 * u / (Ep * Rx); W = w / (Ep * Rx**2)
    return 7.43 * (1 - 0.85 * np.exp(-0.31 * k)) * U**0.65 * W**-0.21 * Rx


def lambda_ratio(h, rq1, rq2):
    return h / np.hypot(rq1, rq2)


def regimen(lam):
    return "límite" if lam < 1 else ("mixto" if lam < 3 else "película completa")


def run(cfg=None):
    cfg = cfg or cargar()
    g = lambda k: float(dato(cfg, k)[0])
    Ep = e_reducido(g("modulo_e1_pa"), g("poisson_1"), g("modulo_e2_pa"), g("poisson_2"))
    h = h_min_soft(g("viscosidad_pa_s"), g("velocidad_m_s"), g("carga_n"), g("radio_rx_m"), Ep, g("elipticidad_k"))
    lam = lambda_ratio(h, g("rugosidad_rq1_m"), g("rugosidad_rq2_m"))
    return {"h_min_m": float(h), "lambda": float(lam), "regimen": regimen(lam)}
