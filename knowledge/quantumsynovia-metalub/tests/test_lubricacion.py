# Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia: Todos los derechos reservados. Confidencial (ver LICENSE).
import numpy as np
import pytest
import lubricacion as l
from lubricacion.pendientes import cargar, DatoPendiente


def test_scaling_exponents():
    a = l.h_min_soft(0.01, 0.1, 100, 0.05, 1e7)
    assert np.isclose(l.h_min_soft(0.02, 0.1, 100, 0.05, 1e7) / a, 2**0.65)
    assert np.isclose(l.h_min_soft(0.01, 0.1, 200, 0.05, 1e7) / a, 2**-0.21)


def test_regimes_and_ereduced():
    assert l.regimen(0.5) == "límite" and l.regimen(2) == "mixto" and l.regimen(5) == "película completa"
    assert np.isclose(l.e_reducido(1e7, 0, 1e7, 0), 1e7)


def test_pending():
    with pytest.raises(DatoPendiente):
        l.run(cargar())
