import json
import httpx
from config import settings
from registry import all_agents, get_agent
from ags_local import get_engine
import asyncio

class Orchestrator:
    def _catalog(self):
        return "\n".join(f"- {n} [{a.domain}] {a.description}" for n, a in all_agents().items())

    async def plan(self, task):
        prompt = (
            "Selecciona agentes SOLO del catalogo. Responde SOLO JSON "
            '{"agents":["nombre"]}. No inventes nombres. Maximo 8.'
            f"\n\nCATALOGO:\n{self._catalog()}\n\nOBJETIVO:\n{task}"
        )
        try:
            async with httpx.AsyncClient(base_url=settings.LITELLM_BASE_URL, headers={"Authorization": f"Bearer {settings.LITELLM_API_KEY}"}, timeout=90.0) as client:
                r = await client.post("/chat/completions", json={"model": "claude-primary", "messages": [{"role": "user", "content": prompt}], "response_format": {"type": "json_object"}})
                r.raise_for_status()
                payload = r.json()
            chosen = json.loads(payload["choices"][0]["message"]["content"]).get("agents", [])
            if not isinstance(chosen, list):
                chosen = []
        except (httpx.HTTPError, KeyError, TypeError, IndexError, json.JSONDecodeError):
            chosen = []
        return [x for x in chosen if x in all_agents()][:8] or ["searcher", "summarizer", "critic"]

    async def execute(self, task, plan=None, allow_llm=True):
        # Reglas primero: si las herramientas locales resuelven, no se llama a ningun LLM.
        if plan is None:
            eng = get_engine()
            if eng.can_solve_locally(task):
                texto = await asyncio.to_thread(eng.planner.plan, task)
                ok = "Plan completado" in texto
                return {"status": "completed" if ok else "partial", "mode": "local_rules",
                        "plan": ["ags_local.planner"], "errors": 0 if ok else 1,
                        "results": [{"agent": "ags_local", "status": "ok", "output": texto,
                                     "es_evidencia": True}], "escribe_ciencia": False}
            if not allow_llm:
                return {"status": "failed", "mode": "local_rules", "plan": [], "errors": 1,
                        "results": [{"agent": "ags_local", "status": "error",
                                     "error": "ninguna herramienta local encaja y LLM desactivado"}],
                        "escribe_ciencia": False}
        plan = plan or await self.plan(task)
        results, context = [], {"objetivo": task}
        for name in plan:
            try:
                out = await get_agent(name).run(task, context)
                context[f"resultado_{name}"] = out["output"][:2000]
                results.append(out)
            except Exception as exc:
                results.append({"agent": name, "status": "error", "error": str(exc)[:200]})
        errors = sum(1 for x in results if x.get("status") == "error")
        status = "completed" if errors == 0 else ("failed" if errors == len(results) else "partial")
        return {"status": status, "mode": "llm", "plan": plan, "errors": errors, "results": results, "escribe_ciencia": False}

orchestrator = Orchestrator()
