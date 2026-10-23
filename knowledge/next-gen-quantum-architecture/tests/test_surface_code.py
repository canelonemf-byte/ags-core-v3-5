import pytest
import surface_code as s
from surface_code.pendientes import cargar, DatoPendiente


def test_scaling():
    assert s.logical_error(0.001, 5) < s.logical_error(0.001, 3)
    d = s.distance_for_target(0.001, 1e-12)
    assert s.logical_error(0.001, d) <= 1e-12 < s.logical_error(0.001, d - 2)
    assert s.physical_qubits(3, 1) == 17


def test_above_threshold():
    with pytest.raises(ValueError):
        s.distance_for_target(0.01, 1e-9)


def test_pending():
    with pytest.raises(DatoPendiente, match="error_fisico_por_ciclo"):
        s.run(cargar())
