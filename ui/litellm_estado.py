"""Criterio de aviso LiteLLM para la UI de estado (sin dependencia de Streamlit)."""


def litellm_estado_sano(estado) -> bool:
    """True si /health reporta LiteLLM operativo ('ready' en la API, o 'ok')."""
    return str(estado or "").strip().lower() in {"ok", "ready"}
