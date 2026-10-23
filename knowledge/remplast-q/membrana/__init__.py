"""membrana: dimensionado de la etapa de membrana del expediente REMPLAST-Q v2.1 (Q = 5 m³/h, recuperación 90 %, J = 200 LMH, así que A = 22,5 m²) y flujo por solución-difusión, J = Lp·(ΔP − Δπ).

Referencias (verificadas):
Wijmans J.G., Baker R.W. (1995) The solution-diffusion model: a review. J. Membrane Sci. 107, 1-21. doi:10.1016/0376-7388(95)00102-I

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
from .pendientes import cargar, dato


def membrane_area(q_feed_m3h, recovery, flux_lmh, margin=0.10):
    q_perm = q_feed_m3h * recovery
    A = q_perm * 1000 / flux_lmh
    return {"q_permeado_m3h": q_perm, "q_retenido_m3h": q_feed_m3h - q_perm, "area_m2": A, "area_instalada_m2": A * (1 + margin)}


def solution_diffusion_flux(lp_lmh_bar, dp_bar, dpi_bar):
    return lp_lmh_bar * (dp_bar - dpi_bar)


def run(cfg=None):
    cfg = cfg or cargar()
    r = membrane_area(float(dato(cfg, "caudal_alimentacion_m3h")[0]), float(dato(cfg, "recuperacion")[0]), float(dato(cfg, "flujo_diseno_lmh")[0]))
    try:
        r["flujo_solucion_difusion_lmh"] = solution_diffusion_flux(float(dato(cfg, "permeabilidad_lmh_bar")[0]), float(dato(cfg, "presion_transmembrana_bar")[0]), float(dato(cfg, "presion_osmotica_bar")[0]))
    except Exception as e:
        r["flujo_solucion_difusion_lmh"] = str(e)
    return r
