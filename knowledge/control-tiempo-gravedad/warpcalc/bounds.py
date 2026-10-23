"""Cotas y efectos medibles.

- Pfenning & Ford (1997), doi:10.1088/0264-9381/14/7/011: las desigualdades cuánticas obligan a que
  la pared de una burbuja de Alcubierre tenga un grosor del orden de ~10^2 longitudes de Planck
  (para v ~ c). Aquí se usa como estimación de orden de magnitud: Delta <~ 1e2 * (v/c) * l_P.
- Chou et al. (2010), doi:10.1126/science.1192720: corrimiento gravitacional entre relojes ópticos
  separados ~33 cm; df/f = g*dh/c^2 (aprox. de campo débil), medido hoy en laboratorio.
"""
import math

C = 299_792_458.0
G = 6.67430e-11
HBAR = 1.054571817e-34


def planck_length():
    return math.sqrt(HBAR * G / C**3)


def pfenning_ford_wall_bound(v_over_c):
    """Grosor máximo aproximado de la pared (m). Orden de magnitud, no valor exacto."""
    return 1e2 * v_over_c * planck_length()


def gravitational_redshift(dh, g=9.80665):
    """Desplazamiento fraccional de frecuencia entre dos relojes separados dh metros en vertical."""
    return g * dh / C**2
