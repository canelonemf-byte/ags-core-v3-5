# Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia: Todos los derechos reservados. Patente en trámite (ver LICENSE). Prohibido reproducir, distribuir o modificar sin permiso escrito del autor.
import pytest
import he3
from he3.pendientes import cargar, DatoPendiente


def test_energy_per_kg():
    # ~5,9e14 J/kg (~19 GWe·año térmicos por tonelada)
    assert 5.8e14 < he3.energia_por_kg_he3() < 5.9e14


def test_regolith_linear():
    assert he3.regolito_necesario_kg(1.0, 10, 1.0) == pytest.approx(1e8)
    assert he3.regolito_necesario_kg(1.0, 10, 0.5) == pytest.approx(2e8)


def test_pending():
    with pytest.raises(DatoPendiente, match="masa_he3_objetivo_kg"):
        he3.run(cargar())
