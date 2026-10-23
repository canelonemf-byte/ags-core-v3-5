"""warpcalc: cálculos numéricos reproducibles sobre métricas warp y relojes relativistas.

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA.
ORCID 0000-0001-8601-1963. Licencia MIT.

Teoría de terceros (no es obra de este proyecto):
- Alcubierre M. (1994) Class. Quantum Grav. 11 L73, doi:10.1088/0264-9381/11/5/001
- Natário J. (2002) Class. Quantum Grav. 19 1157, doi:10.1088/0264-9381/19/6/308
- Pfenning M.J., Ford L.H. (1997) Class. Quantum Grav. 14 1743, doi:10.1088/0264-9381/14/7/011
- Chou C.W. et al. (2010) Science 329 1630, doi:10.1126/science.1192720
"""
from .metrics import (alcubierre_shape, alcubierre_rho_analytic, alcubierre_shift,
                      natario_shift, eulerian_energy_density, total_energy, grid)
from .bounds import planck_length, pfenning_ford_wall_bound, gravitational_redshift
__all__ = [n for n in dir() if not n.startswith("_")]
