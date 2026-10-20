import uuid
import httpx
from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field
import agents  # noqa: F401
from config import settings
from registry import all_agents, get_agent, agents_by_domain
from orchestrator import orchestrator
import asyncio
from ags_local import get_engine
from supervisor import get_supervisor
from projects import load_manifest, get_index

VERSION = "3.6.0"
app = FastAPI(title="AGs-Core", version=VERSION)

class TrainRequest(BaseModel):
    steps: int = Field(default=40, ge=1, le=200)
    text: str = Field(default="", max_length=200000)

class SupervisorTask(BaseModel):
    task: str = Field(min_length=1, max_length=5000)
    projects: list[str] | None = Field(default=None, max_length=100)
    kinds: list[str] | None = Field(default=None, max_length=10)
    run_now: bool = False

class TaskRequest(BaseModel):
    task: str = Field(min_length=1, max_length=20000)
    context: dict | None = None

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response

def auth(x_api_key: str | None):
    if not settings.AGS_API_KEY:
        raise HTTPException(503, "AGS_API_KEY no configurada")
    if x_api_key != settings.AGS_API_KEY:
        raise HTTPException(401, "API key invalida")

async def litellm_state():
    try:
        async with httpx.AsyncClient(base_url=settings.LITELLM_BASE_URL, timeout=settings.HEALTH_TIMEOUT) as client:
            r = await client.get("/health/liveliness")
        return "ok" if r.status_code == 200 else f"http_{r.status_code}"
    except httpx.HTTPError:
        return "unreachable"

@app.get("/health")
async def health():
    return {"status": "ok", "agents": len(all_agents()), "version": VERSION, "litellm": await litellm_state()}

@app.get("/agents")
def list_agents():
    return {"total": len(all_agents()), "agents": [{"name": a.name, "domain": a.domain, "description": a.description, "model": a.preferred_model} for a in all_agents().values()]}

@app.get("/models")
async def models(x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    try:
        async with httpx.AsyncClient(base_url=settings.LITELLM_BASE_URL, headers={"Authorization": f"Bearer {settings.LITELLM_API_KEY}"}, timeout=15) as client:
            r = await client.get("/v1/models")
            r.raise_for_status()
            return r.json()
    except httpx.HTTPError as exc:
        raise HTTPException(502, f"LiteLLM no disponible: {type(exc).__name__}")

@app.get("/integrations")
def integrations(x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    return {"integrations": {k: ("configured" if v else "not_configured") for k, v in settings.INTEGRATIONS.items()}}

@app.get("/agents/domain/{domain}")
def by_domain(domain: str):
    xs = agents_by_domain(domain)
    if not xs:
        raise HTTPException(404, f"Sin agentes en {domain}")
    return {"domain": domain, "agents": [a.name for a in xs]}

@app.post("/run/agent/{name}")
async def run_single(name: str, req: TaskRequest, x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    try:
        agent = get_agent(name)
    except KeyError:
        raise HTTPException(404, f"Agente {name} no existe")
    try:
        return await agent.run(req.task, req.context)
    except RuntimeError as exc:
        raise HTTPException(502, str(exc)[:300])

@app.post("/run/orchestrated")
async def run_orch(req: TaskRequest, x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    return await orchestrator.execute(req.task)

@app.post("/run/tool/{project}")
async def run_tool(project: str, req: TaskRequest, x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    try:
        return await asyncio.to_thread(get_engine().run_tool, project, req.task)
    except KeyError:
        raise HTTPException(404, f"Proyecto {project} no existe")

@app.get("/agsgpt/status")
def agsgpt_status(x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    return get_engine().status()

@app.post("/agsgpt/train")
async def agsgpt_train(req: TrainRequest, x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    try:
        return await asyncio.to_thread(get_engine().train, req.steps, req.text)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc))


# ---------------- v3.6: proyectos, supervisor y cola de tareas ----------------
@app.get("/projects")
def list_projects():
    ps = load_manifest()["projects"]
    return {"total": len(ps), "projects": [{"id": p["id"], "agent": "proj_" + p["id"].replace("-", "_"), "url": p.get("url"),
            "tools": p.get("tools", []), "license": p.get("license"), "files": p.get("files")} for p in ps]}

@app.get("/projects/{pid}/search")
def project_search(pid: str, q: str, k: int = 4, x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    if pid not in {p["id"] for p in load_manifest()["projects"]}:
        raise HTTPException(404, f"Proyecto {pid} no existe")
    return {"project": pid, "results": get_index().search(pid, q, max(1, min(k, 20)))}

@app.post("/tasks", status_code=201)
async def create_task(req: SupervisorTask, x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    sup = get_supervisor()
    try:
        res = sup.submit(req.task, req.projects, req.kinds)
    except ValueError as exc:
        raise HTTPException(422, str(exc))
    if req.run_now:
        res["cycle"] = await asyncio.to_thread(sup.run_cycle, res["subtasks"])
    return res

@app.get("/tasks")
def get_tasks(status: str | None = None, project: str | None = None, parent_id: int | None = None, limit: int = 50,
              x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    q = get_supervisor().queue
    return {"counts": q.counts(), "tasks": q.list_tasks(status, project, max(1, min(limit, 500)), parent_id)}

@app.get("/tasks/{tid}")
def get_task(tid: int, x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    t = get_supervisor().queue.get(tid)
    if not t:
        raise HTTPException(404, f"Tarea {tid} no existe")
    return t

@app.get("/supervisor/status")
def supervisor_status(x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    return get_supervisor().status()


# ---------------- Unified Cognitive Stack: memoria ----------------
import memory_store

class MemoryNote(BaseModel):
    subject: str = Field(min_length=1, max_length=500)
    fact_contents: str = Field(min_length=1, max_length=20000)
    keywords: list[str] = Field(default_factory=list, max_length=50)
    importance_score: float = Field(default=0.6, ge=0.0, le=1.0)
    pinned: bool = False

class IngestRequest(BaseModel):
    action: str = "ADD"
    memory_note: MemoryNote

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
    top_k: int = Field(default=5, ge=1, le=50)

@app.post("/ingest", status_code=201)
def ingest(req: IngestRequest, x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    if req.action.upper() != "ADD":
        raise HTTPException(400, "solo se admite action=ADD")
    n = req.memory_note
    mid = memory_store.add(n.subject, n.fact_contents, n.keywords, n.importance_score, n.pinned)
    return {"id": mid, "status": "added"}

@app.post("/chat")
def chat(req: ChatRequest, x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    hits = memory_store.search(req.message, req.top_k)
    if not hits:
        answer = "No hay memorias relevantes. (Sin LLM: LiteLLM PENDIENTE de configurar.)"
    else:
        answer = "Memorias recuperadas (sin LLM; LiteLLM PENDIENTE):\n" + "\n".join(
            f"- [{m.subject}] (S={s:.2f}) {m.fact_contents[:300]}" for m, _, s in hits)
    return {"answer": answer, "used_memory_ids": [m.id for m, _, _ in hits]}

@app.get("/memory/stats")
def memory_stats(x_api_key: str | None = Header(default=None)):
    auth(x_api_key)
    return memory_store.stats()
