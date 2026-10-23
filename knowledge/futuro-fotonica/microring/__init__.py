"""microring: transmisión de un microanillo all-pass, FSR, finesa y Q (Bogaerts et al. 2012). Modelo de referencia público; todos los parámetros del dispositivo están pendientes.

Referencias (verificadas):
Bogaerts W. et al. (2012) Silicon microring resonators. Laser & Photonics Reviews 6, 47-73. doi:10.1002/lpor.201100017

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np
from .pendientes import cargar, dato


def allpass_transmission(lam, radius, n_eff, r, a):
    phi = 2 * np.pi * n_eff * 2 * np.pi * radius / np.asarray(lam, float)
    return (a**2 - 2 * r * a * np.cos(phi) + r**2) / (1 - 2 * a * r * np.cos(phi) + (r * a) ** 2)


def fsr(lam, radius, n_g):
    return lam**2 / (n_g * 2 * np.pi * radius)


def loaded_q(lam, radius, n_g, r, a):
    return np.pi * n_g * 2 * np.pi * radius * np.sqrt(r * a) / (lam * (1 - r * a))


def run(cfg=None):
    cfg = cfg or cargar()
    v = {k: float(dato(cfg, k)[0]) for k in ("longitud_onda_m", "radio_m", "n_eff", "n_g", "r_acoplo", "a_perdidas")}
    for k in ("r_acoplo", "a_perdidas"):
        if not 0 < v[k] <= 1:
            raise ValueError(f"{k} debe estar en (0, 1]")
    return {"fsr_m": fsr(v["longitud_onda_m"], v["radio_m"], v["n_g"]), "q_cargado": loaded_q(v["longitud_onda_m"], v["radio_m"], v["n_g"], v["r_acoplo"], v["a_perdidas"]), "origen": "dato_usuario"}
