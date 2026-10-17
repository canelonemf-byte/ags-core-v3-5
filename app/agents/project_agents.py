"""Un ProjectAgent por repositorio, generado desde projects.json (no hay un archivo por agente).

Conocimiento: README/docs/código del repo indexados en local (TF-IDF + palabras clave).
Herramientas: las físicas de ags_local que encajan con el proyecto (campo "tools").
No usa LLM: devuelve pasajes con su archivo de origen y, si aplica, un cálculo local.
"""
import asyncio

from base_agent import BaseAgent
from projects.knowledge import get_index, plain
from projects.manifest import load_manifest
from registry import register

_CHECK_WORDS = {
    "license_check": ("licencia", "copyright", "plagio", "atribucion", "derechos"),
    "missing_pieces": ("que falta", "falta", "pendiente", "missing"),
    "review_claims": ("afirmaciones", "sin respaldo", "unsupported", "revisa"),
}


class ProjectAgent(BaseAgent):
    domain = "project"
    preferred_model = "local_knowledge"
    fallback_models: list = []
    project: dict = {}

    @property
    def system_prompt(self):
        return (f"Agente especializado del proyecto {self.project['id']} ({self.project.get('url', '')}). "
                "Responde solo con pasajes de sus documentos y cálculos locales; no inventa.")

    def _check_kind(self, task: str):
        t = plain(task)
        for k, ws in _CHECK_WORDS.items():
            if any(w in t for w in ws):
                return k
        return None

    def answer(self, task: str, k: int = 4) -> dict:
        pid = self.project["id"]
        kind = self._check_kind(task)
        if kind:
            from supervisor import get_supervisor
            res = get_supervisor().run_task({"id": 0, "project": pid, "kind": kind})
            s = res["summary"]
            out = (f"[{pid}] revisión {kind}: {s['findings']} hallazgos "
                   f"(alta {s['counts']['high']}, media {s['counts']['medium']}). Informe: {res['report_path']}")
            return {"output": out, "status": "ok", "report": res["report_path"], "sources": [], "tool": None}
        hits = get_index().search(pid, task, k)
        parts, tool = [], None
        if self.project.get("tools"):
            from ags_local import get_engine
            eng = get_engine()
            for tid in self.project["tools"]:
                hit = eng.registry.match_tool(tid, task)
                if hit:
                    tool = f"{tid}.{hit[0]}"
                    parts.append(f"[cálculo local {tool}]\n{hit[1](task)}")
                    break
        for h in hits:
            parts.append(f"[{h['file']} · score {h['score']}]\n{h['text'][:700]}")
        if not parts:
            parts.append(f"[{pid}] no hay pasajes relevantes en la documentación del proyecto.")
        return {"output": "\n\n".join(parts), "status": "ok" if hits or tool else "no_match",
                "sources": [h["file"] for h in hits], "tool": tool}

    async def run(self, task, context=None):
        res = await asyncio.to_thread(self.answer, task)
        return {"agent": self.name, "domain": self.domain, "model_used": "local_knowledge",
                "project": self.project["id"], **res,
                "evidencia": "E1_calculo_local" if res.get("tool") else "E0_documental", "es_evidencia": bool(res.get("tool"))}


def agent_name(pid: str) -> str:
    return "proj_" + pid.replace("-", "_")


def build_agents(manifest: dict | None = None) -> list[str]:
    names = []
    for p in (manifest or load_manifest())["projects"]:
        desc = (p.get("description") or p.get("name") or p["id"])[:160]
        cls = type(f"Project_{p['id'].replace('-', '_')}", (ProjectAgent,), {
            "name": agent_name(p["id"]), "project": p, "description": f"Proyecto {p['id']}: {desc}"})
        register(cls)
        names.append(cls.name)
    return names


PROJECT_AGENTS = build_agents()
