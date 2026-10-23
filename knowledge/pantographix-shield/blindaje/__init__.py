"""blindaje: eficacia de blindaje electromagnético de campo lejano de una lámina, SE = A + R (Schelkunoff 1938). SUPUESTO: Pantographix Shield es un blindaje EM. El autor debe confirmarlo, porque los documentos fuente están en Drive y no se han podido leer.

Referencias (verificadas):
Schelkunoff S.A. (1938) The Impedance Concept and Its Application to Problems of Reflection, Refraction, Shielding and Power Absorption. Bell System Technical Journal 17, 17-48. doi:10.1002/j.1538-7305.1938.tb00774.x

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np
from .pendientes import cargar, dato

MU0 = 4e-7 * np.pi
SIGMA_CU = 5.8e7


def skin_depth(f, sigma, mu_r=1.0):
    return 1 / np.sqrt(np.pi * f * MU0 * mu_r * sigma)


def shielding_db(f, t, sigma, mu_r=1.0):
    A = 8.686 * t / skin_depth(f, sigma, mu_r)
    R = 168 + 10 * np.log10((sigma / SIGMA_CU) / (mu_r * f))
    return {"absorcion_db": float(A), "reflexion_db": float(R), "total_db": float(A + R)}


def run(cfg=None):
    cfg = cfg or cargar()
    f = float(dato(cfg, "frecuencia_hz")[0]); t = float(dato(cfg, "espesor_m")[0])
    s, o = dato(cfg, "conductividad_s_m"); mu, o2 = dato(cfg, "mu_r")
    r = shielding_db(f, t, float(s), float(mu)); r["origen_material"] = [o, o2]; return r
