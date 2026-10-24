# Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia: CC BY-NC-SA 4.0 (ver LICENSE).
import pytest
import diagnostico as d
from diagnostico.pendientes import cargar, DatoPendiente


def test_altman_bland_example():
    # Altman y Bland 1994: gammagrafía hepática, VP 231, FP 32, FN 27, VN 54 -> Se 0,895, Sp 0,628
    m = d.metricas(231, 32, 27, 54, prevalencia=258 / 344)
    assert round(m["sensibilidad"], 3) == 0.895 and round(m["especificidad"], 3) == 0.628
    assert round(m["vpp"], 3) == round(231 / 263, 3)
    assert "no es un diagnóstico" in m["aviso"]


def test_pending():
    with pytest.raises(DatoPendiente):
        d.run(cargar())
