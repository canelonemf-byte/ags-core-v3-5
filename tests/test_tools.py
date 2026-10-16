import pytest
from ags_local.project_registry import Registry
from ags_local import tools
from pathlib import Path
import ags_local
pytestmark = pytest.mark.unit
R = Registry(Path(ags_local.__file__).parent / "projects.json")

def test_amoniaco_25mw():
    assert "kg_NH3/h 2625.1" in tools.produccion_amoniaco("calcula amoniaco con 25 MW")

def test_isp_yodo_3kv():
    assert "Isp 6887 s" in tools.empuje_yodo("empuje yodo 3 kV")

def test_fusion_no_inventa_sigma_v():
    out = tools.balance_fusion("fusion a 100 keV")
    assert "MeV 18.3" in out and "No se inventa" in out

def test_falta_dato():
    assert "falta" in tools.produccion_amoniaco("amoniaco")

@pytest.mark.parametrize("txt,pid", [("amoniaco 10 MW", "zero_a"), ("tokamak fusion 100 keV", "d3he_tokamak"),
                                     ("isp del propulsor de yodo", "mei_rit"), ("odmr zeeman nv", "q_matrix"),
                                     ("tdcs electrodo 35 cm2", "neuroglyq")])
def test_routing(txt, pid):
    assert R.route(txt).id == pid
