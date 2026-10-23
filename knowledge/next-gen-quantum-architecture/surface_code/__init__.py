"""surface_code: estimación de recursos del código de superficie, p_L ≈ A (p/p_th)^((d+1)/2), con 2d²−1 qubits físicos por qubit lógico (Fowler et al. 2012). Los valores A=0,03 y p_th=0,0057 son el ejemplo público del artículo.

Referencias (verificadas):
Fowler A.G., Mariantoni M., Martinis J.M., Cleland A.N. (2012) Surface codes: Towards practical large-scale quantum computation. Phys. Rev. A 86, 032324. doi:10.1103/PhysRevA.86.032324

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
from .pendientes import cargar, dato


def logical_error(p, d, A=0.03, p_th=0.0057):
    return A * (p / p_th) ** ((d + 1) / 2)


def distance_for_target(p, target, A=0.03, p_th=0.0057, d_max=201):
    if p >= p_th:
        raise ValueError("la tasa física está por encima del umbral: el código no corrige")
    for d in range(3, d_max + 1, 2):
        if logical_error(p, d, A, p_th) <= target:
            return d
    raise ValueError("no se alcanza el objetivo con d <= d_max")


def physical_qubits(d, n_logical):
    return n_logical * (2 * d * d - 1)


def run(cfg=None):
    cfg = cfg or cargar()
    p = float(dato(cfg, "error_fisico_por_ciclo")[0]); t = float(dato(cfg, "error_logico_objetivo")[0]); n = int(dato(cfg, "qubits_logicos")[0])
    A, oa = dato(cfg, "prefactor_A"); pth, op = dato(cfg, "umbral_p_th")
    d = distance_for_target(p, t, float(A), float(pth))
    return {"distancia": d, "qubits_fisicos": physical_qubits(d, n), "origen_A_pth": [oa, op]}
