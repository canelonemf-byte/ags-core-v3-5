import pytest
import casimir as c
from casimir.pendientes import cargar


def test_lamoreaux_scale():
    # a 1 µm la presión ideal es ~1,3 mPa
    assert abs(c.casimir_pressure(1e-6) - 1.3e-3) < 0.05e-3


def test_author_example():
    r = c.run(cargar())
    assert r["origen"] == "dato_usuario" and r["delta_F_N"] > 0
