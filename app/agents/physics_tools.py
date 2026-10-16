"""Agentes deterministas por proyecto: usan las herramientas físicas locales, sin LLM."""
import asyncio

from ags_local import get_engine
from base_agent import BaseAgent
from registry import register

_DESCR = {
    "zero_a": "Amoniaco verde (NH3): produccion, energia Haber-Bosch, MW para objetivo",
    "neuroglyq": "Neuromodulacion tDCS: densidad de corriente y protocolo",
    "d3he_tokamak": "Fusion D-He3: energia por reaccion, producto triple, densidad objetivo",
    "mei_rit": "Propulsor de yodo: Isp/empuje, corrosion Faraday, empuje objetivo",
    "q_matrix": "Sensores NV/ODMR: Zeeman, contraste, sensibilidad magnetica",
    "ecosistema": "Balance energetico del ecosistema integrado",
}


class ToolAgent(BaseAgent):
    domain = "tools"
    preferred_model = "local_tools"
    fallback_models: list = []
    project = ""

    @property
    def system_prompt(self):
        return f"Herramientas fisicas deterministas del proyecto {self.project}. No usa LLM."

    async def run(self, task, context=None):
        eng = get_engine()
        res = await asyncio.to_thread(eng.run_tool, self.project, task)
        if res["tool"] is None:
            out = (f"[{self.project}] ninguna herramienta encaja. Disponibles: "
                   f"{', '.join(res['available_tools'])}")
            ok = False
        else:
            out, ok = f"[{res['tool']}]\n{res['output']}", True
        return {"agent": self.name, "domain": self.domain, "model_used": "local_tools",
                "tool": res["tool"], "output": out, "status": "ok" if ok else "no_tool",
                "evidencia": "E1_calculo_local" if ok else "E0_sin_calculo", "es_evidencia": ok}


def _make(pid):
    cls = type(f"Tool_{pid}", (ToolAgent,), {
        "name": f"tool_{pid}", "project": pid, "description": _DESCR[pid]})
    return register(cls)


for _pid in _DESCR:
    _make(_pid)
