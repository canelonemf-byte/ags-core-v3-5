import pytest
import tamano_muestra as t
from tamano_muestra.pendientes import cargar, DatoPendiente


def test_classic_value():
    # efecto estandarizado 0,5 con alfa 0,05 y potencia 0,8 da 63 por grupo (fórmula normal)
    assert t.n_per_group(0.5, 1.0) == 63


def test_pending():
    with pytest.raises(DatoPendiente, match="diferencia_clinica_relevante"):
        t.run(cargar())
