# Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia: CC BY-NC-ND 4.0 (ver LICENSE).
import numpy as np
import pytest
import termometria as t
from termometria.pendientes import cargar, DatoPendiente


def test_antistokes_roundtrip():
    T, nu, nl = 300.0, 1000.0, 18797.0
    r = ((nl + nu) / (nl - nu)) ** 4 * np.exp(-t.HC_K * nu / T)
    assert np.isclose(t.temp_antistokes_stokes(r, nu, nl), T)


def test_figures():
    T = np.linspace(290, 320, 7); X = 100 - 0.02 * T
    f = t.figuras_merito(T, X, 0.002)
    assert np.isclose(f["delta_T_K"], 0.1)


def test_pending():
    with pytest.raises(DatoPendiente):
        t.run(cargar())
