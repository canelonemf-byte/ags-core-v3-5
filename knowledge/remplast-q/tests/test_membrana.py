import pytest
import membrana as m
from membrana.pendientes import cargar


def test_author_area():
    r = m.run(cargar())
    assert abs(r["area_m2"] - 22.5) < 1e-9 and abs(r["q_permeado_m3h"] - 4.5) < 1e-9
    assert r["flujo_solucion_difusion_lmh"].startswith("PENDIENTE")


def test_sd_flux():
    assert m.solution_diffusion_flux(2.0, 10, 4) == 12
