import pytest
import eurostat_es as e
from eurostat_es.pendientes import cargar, DatoPendiente


def test_cached_real_data():
    d = e.leer()
    assert "2024" in d["series"]["petroleo_gae_ktep"]["valores"]
    c = e.cuota_petroleo(d, "2024")
    assert 0.3 < c < 0.7


def test_trajectory():
    t = e.trayectoria(e.leer(), "2024", 2050, 0.0)
    assert t["2050"] == 0 and t["2024"] > t["2037"] > 0


def test_pending():
    with pytest.raises(DatoPendiente, match="anio_objetivo"):
        e.run(cargar())
