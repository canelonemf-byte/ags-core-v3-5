"""Pruebas del criterio de aviso LiteLLM en la UI (sin arrancar Streamlit)."""
import pytest
from ui.litellm_estado import litellm_estado_sano

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "estado,sano",
    [
        ("ready", True),
        ("ok", True),
        ("READY", True),
        ("  ok  ", True),
        ("unreachable", False),
        ("http_500", False),
        ("", False),
        (None, False),
    ],
)
def test_litellm_estado_sano(estado, sano):
    assert litellm_estado_sano(estado) is sano
