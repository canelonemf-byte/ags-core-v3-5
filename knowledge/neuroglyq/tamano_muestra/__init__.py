"""tamano_muestra: tamaño muestral de un ensayo de dos grupos con resultado continuo, n = 2(z_{1-α/2} + z_{1-β})² σ²/Δ² por grupo. Sirve para planificar la validación clínica que NeuroGlyQ aún no tiene. α = 0,05 y potencia 0,80 son las convenciones de la referencia.

Referencias (verificadas):
Noordzij M. et al. (2010) Sample size calculations: basic principles and common pitfalls. Nephrol. Dial. Transplant. 25, 1388-1393. doi:10.1093/ndt/gfp732

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import math
from statistics import NormalDist
from .pendientes import cargar, dato


def n_per_group(delta, sd, alpha=0.05, power=0.80, dropout=0.0):
    if delta <= 0 or sd <= 0:
        raise ValueError("delta y sd deben ser > 0")
    z = NormalDist().inv_cdf
    n = 2 * (z(1 - alpha / 2) + z(power)) ** 2 * sd**2 / delta**2
    return math.ceil(math.ceil(n) / (1 - dropout))


def run(cfg=None):
    cfg = cfg or cargar()
    d = float(dato(cfg, "diferencia_clinica_relevante")[0]); s = float(dato(cfg, "desviacion_estandar")[0])
    a, oa = dato(cfg, "alfa"); p, op = dato(cfg, "potencia"); dr = float(dato(cfg, "abandono")[0])
    return {"n_por_grupo": n_per_group(d, s, float(a), float(p), dr), "origen_alfa_potencia": [oa, op]}
