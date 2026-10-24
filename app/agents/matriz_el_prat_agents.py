"""matriz_el_prat en AGs-Core: 5 agentes principales + 15 sub-agentes registrados y ejecutados por el autopilot.
Objetivo: mejorar la vida de la ciudadanía del Prat de Llobregat. Solo fuentes públicas; solo BORRADORES.
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. MIT."""
import asyncio, json, os, time
from pathlib import Path

from base_agent import BaseAgent
from registry import register
from matriz_el_prat import OBJETIVO, agentes as MA
from matriz_el_prat.store import Store

ROOT = Path(__file__).resolve().parents[2]
DB = Path(os.getenv("MATRIZ_DB", ROOT / "data" / "matriz_el_prat.sqlite"))
STATUS = ROOT / "data" / "subagentes" / "matriz_el_prat.json"
INTERVAL = float(os.getenv("MATRIZ_INTERVAL", 86400))  # ingesta diaria
_store = None


def store():
    global _store
    _store = _store or Store(DB)
    return _store


class MatrizAgent(BaseAgent):
    domain = "matriz_el_prat"
    preferred_model = "local_check"
    fallback_models: list = []
    clave = ""

    @property
    def system_prompt(self):
        return (f"{self.description}. Objetivo: {OBJETIVO} Cada hallazgo debe decir el beneficio ciudadano, "
                "a quién beneficia y su impacto solo con datos reales. Nunca presenta ni envía documentos.")

    def execute(self):
        s = store()
        subs = [c for c in MA.SUBAGENTES if c.nombre == self.clave or c.agente == self.clave]
        res = [c(s).ejecutar() for c in subs]
        out = {"agente": self.name, "objetivo": OBJETIVO, "subagentes": res}
        if self.clave == "fiscal_prat":
            out["analisis"] = MA.analizar_propuestas()
        return out

    async def run(self, task, context=None):
        out = await asyncio.to_thread(self.execute)
        return {"agent": self.name, "domain": self.domain, "model_used": "local_check",
                "output": json.dumps(out, ensure_ascii=False, default=str)[:20000], "evidencia": "E3_software", "es_evidencia": False}


for _k, _n in MA.AGENTES.items():
    register(type(f"Matriz_{_k}", (MatrizAgent,), {"name": f"matriz_{_k}", "clave": _k, "description": _n}))
for _c in MA.SUBAGENTES:
    register(type(f"Matriz_{_c.nombre}", (MatrizAgent,), {"name": f"matriz_{_c.nombre}", "clave": _c.nombre,
                                                          "description": f"Sub-agente {_c.nombre} de {_c.agente}"}))


def run_due(state: dict, now=None) -> bool:
    now = now or time.time()
    if now - state.get("matriz_last", 0) < INTERVAL:
        return False
    state["matriz_last"] = now
    res = MA.ciclo(store())
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return True
