import pytest
import g4
from g4.pendientes import cargar, DatoPendiente


def test_telomeric():
    h = g4.find_g4("AGGGTTAGGGTTAGGGTTAGGG")
    assert any(x[0] == "+" for x in h)
    assert g4.find_g4("ATATATATATAT") == []


def test_minus_strand():
    assert any(x[0] == "-" for x in g4.find_g4(g4.revcomp("AGGGTTAGGGTTAGGGTTAGGG")))


def test_example_and_pending():
    assert g4.run()["origen"].startswith("ejemplo_publico")
    c = cargar(); c["secuencia_diana"]["ejemplo_publico"] = ""
    with pytest.raises(DatoPendiente):
        g4.run(c)
