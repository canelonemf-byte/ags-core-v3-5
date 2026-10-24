"""he3: balance de masas y energía del helio-3 lunar. Calcula el regolito a procesar para una masa de He-3, dada la concentración y la eficiencia de extracción, y la energía de fusión D-He3 (18,35 MeV por reacción, Q de la reacción D + 3He -> 4He + p) por kg de He-3 (Wittenberg et al. 1986). La concentración y la eficiencia del emplazamiento son datos pendientes.

Referencias (verificadas):
Wittenberg L.J., Santarius J.F., Kulcinski G.L. (1986) Lunar Source of 3He for Commercial Fusion Power. Fusion Technology 10, 167-178. doi:10.13182/FST86-A24972

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia: Todos los derechos reservados. Patente en trámite (ver LICENSE). Prohibido reproducir, distribuir o modificar sin permiso escrito del autor.
"""
from .pendientes import cargar, dato

MEV = 1.602176634e-13; NA = 6.02214076e23; M_HE3 = 3.0160293e-3
Q_DHE3_MEV = 18.35


def energia_por_kg_he3():
    return NA / M_HE3 * Q_DHE3_MEV * MEV


def regolito_necesario_kg(masa_he3_kg, conc_ppb_masa, eficiencia):
    if not (0 < eficiencia <= 1) or conc_ppb_masa <= 0:
        raise ValueError("eficiencia en (0,1] y concentración > 0")
    return masa_he3_kg / (conc_ppb_masa * 1e-9 * eficiencia)


def run(cfg=None):
    cfg = cfg or cargar()
    m = float(dato(cfg, "masa_he3_objetivo_kg")[0]); c = float(dato(cfg, "concentracion_he3_ppb_masa")[0]); e = float(dato(cfg, "eficiencia_extraccion")[0])
    return {"regolito_kg": regolito_necesario_kg(m, c, e), "energia_fusion_J": m * energia_por_kg_he3()}
