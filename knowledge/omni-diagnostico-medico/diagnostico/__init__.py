"""diagnostico: métricas de evaluación de una prueba diagnóstica a partir de la tabla 2×2: sensibilidad, especificidad, valores predictivos según la prevalencia (Bayes), razones de verosimilitud e intervalos de Wilson al 95 % (Altman y Bland 1994).

AVISO MÉDICO: herramienta estadística de investigación. NO diagnostica, NO es un producto sanitario, NO sustituye el juicio clínico y NO está validada clínicamente. Cualquier uso clínico requiere estudios de validación y marcado CE conforme al Reglamento (UE) 2017/745.

Referencias (verificadas):
Altman D.G., Bland J.M. (1994) Diagnostic tests 1: sensitivity and specificity. BMJ 308, 1552. doi:10.1136/bmj.308.6943.1552
Altman D.G., Bland J.M. (1994) Diagnostic tests 2: predictive values. BMJ 309, 102. doi:10.1136/bmj.309.6947.102

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia: CC BY-NC-SA 4.0 (ver LICENSE).
"""
import math
from .pendientes import cargar, dato


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def metricas(vp, fp, fn, vn, prevalencia=None):
    se = vp / (vp + fn); sp = vn / (vn + fp)
    out = {"sensibilidad": se, "ic95_sensibilidad": wilson(vp, vp + fn), "especificidad": sp, "ic95_especificidad": wilson(vn, vn + fp),
           "lr_positiva": se / (1 - sp) if sp < 1 else float("inf"), "lr_negativa": (1 - se) / sp if sp > 0 else float("inf")}
    if prevalencia is not None:
        p = prevalencia
        out["vpp"] = se * p / (se * p + (1 - sp) * (1 - p)); out["vpn"] = sp * (1 - p) / (sp * (1 - p) + (1 - se) * p)
    out["aviso"] = "Uso de investigación; no es un diagnóstico."
    return out


def run(cfg=None):
    cfg = cfg or cargar()
    v = [int(dato(cfg, k)[0]) for k in ("verdaderos_positivos", "falsos_positivos", "falsos_negativos", "verdaderos_negativos")]
    return metricas(*v, prevalencia=float(dato(cfg, "prevalencia")[0]))
