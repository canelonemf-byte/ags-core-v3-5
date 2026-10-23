"""union: ocupación de un sitio de unión, theta = L / (L + Kd), con la Kd = 45 nM que declara el documento del autor
(valor declarado, E1: sin medida publicada). Útil para elegir concentraciones de ensayo.
Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
KD_AUTOR_nM = 45.0


def occupancy(L_nM, Kd_nM=KD_AUTOR_nM):
    return L_nM / (L_nM + Kd_nM)


def conc_for_occupancy(theta, Kd_nM=KD_AUTOR_nM):
    return Kd_nM * theta / (1 - theta)
