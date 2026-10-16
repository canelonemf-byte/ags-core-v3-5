"""Agente AGsGPT local (PyTorch + LoRA). Sin pesos responde 'sin pesos'; no inventa fisica."""
import asyncio

from ags_local import get_engine
from base_agent import BaseAgent
from registry import register


@register
class AGsGPTAgent(BaseAgent):
    name = "agsgpt"
    domain = "local"
    description = "Red neuronal propia AGsGPT con adaptadores LoRA (CPU, local)"
    preferred_model = "agsgpt-local"
    fallback_models: list = []

    @property
    def system_prompt(self):
        return "AGsGPT local. Generacion por caracteres; no es evidencia."

    async def run(self, task, context=None):
        eng = get_engine()
        out = await asyncio.to_thread(eng.gpt_or_gap, task, "agsgpt")
        return {"agent": self.name, "domain": self.domain, "model_used": "agsgpt-local",
                "output": out, "status": "ok", "weights": eng.model is not None,
                "evidencia": "E0_generativo", "es_evidencia": False}
