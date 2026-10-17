"""Supervisor: descompone una tarea, la reparte por proyecto y la ejecuta con sub-agentes acotados.

Concurrencia: como mucho `max_workers` tareas a la vez (una por proyecto) y, dentro de cada
tarea, `workers_per_project` sub-agentes que revisan trozos distintos de los archivos.
"""
import json
import os
import re
import socket
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from projects.knowledge import get_index, plain
from projects.manifest import get_project, load_manifest
from . import checks
from .queue import TaskQueue

ROOT = Path(__file__).resolve().parents[2]
HARD_MAX_WORKERS, HARD_MAX_SUB = 16, 8
KIND_TITLES = {
    "review_claims": "Afirmaciones sin respaldo",
    "missing_pieces": "Piezas que faltan",
    "license_check": "Originalidad, licencia y atribuciones",
}
_KIND_WORDS = {
    "review_claims": ["afirmacion", "claim", "cifra", "unsupported", "respaldo", "revisa doc", "review doc", "fisica", "dato"],
    "missing_pieces": ["falta", "missing", "pendiente", "pieza", "incomplet"],
    "license_check": ["licen", "copyright", "plagi", "atribuc", "derechos", "original", "attribution"],
}


def _data_dir() -> Path:
    return Path(os.getenv("AGSGPT_DATA_DIR", ROOT / "data"))


def _reports_dir() -> Path:
    return Path(os.getenv("AGS_REPORTS_DIR", ROOT / "reports"))


class Supervisor:
    def __init__(self, queue: TaskQueue | None = None, index=None, reports_dir: Path | None = None,
                 max_workers: int | None = None, workers_per_project: int | None = None):
        self.queue = queue or TaskQueue(_data_dir() / "supervisor.sqlite")
        self.index = index or get_index()
        self.reports_dir = Path(reports_dir or _reports_dir())
        self.max_workers = max(1, min(HARD_MAX_WORKERS, int(max_workers or os.getenv("AGS_MAX_WORKERS", 4))))
        self.workers_per_project = max(1, min(HARD_MAX_SUB, int(workers_per_project or os.getenv("AGS_WORKERS_PER_PROJECT", 3))))
        self.worker_id = f"{socket.gethostname()}:{os.getpid()}"
        self._busy: set[str] = set()
        self._blk = threading.Lock()

    # ---------- descomposición ----------
    def projects(self) -> list[str]:
        return [p["id"] for p in load_manifest()["projects"]]

    def decompose(self, task: str, projects: list[str] | None = None, kinds: list[str] | None = None):
        t = plain(task)
        if not kinds:
            kinds = [k for k, ws in _KIND_WORDS.items() if any(w in t for w in ws)] or list(checks.KINDS)
        bad = [k for k in kinds if k not in checks.KINDS]
        if bad:
            raise ValueError(f"tipos desconocidos: {bad}")
        allp = self.projects()
        if projects:
            unknown = [p for p in projects if p not in allp]
            if unknown:
                raise ValueError(f"proyectos desconocidos: {unknown}")
        else:
            projects = [p for p in allp if re.search(r"(?<![a-z0-9])" + re.escape(p) + r"(?![a-z0-9])", t)] or allp
        return projects, kinds

    def submit(self, task: str, projects: list[str] | None = None, kinds: list[str] | None = None, priority: int = 3) -> dict:
        projects, kinds = self.decompose(task, projects, kinds)
        parent = self.queue.add("composite", None, {"task": task, "projects": projects, "kinds": kinds}, priority=priority, status="split")
        ids = [self.queue.add(k, p, {"task": task}, parent_id=parent, priority=priority) for p in projects for k in kinds]
        self.queue.log("info", f"tarea {parent} descompuesta en {len(ids)} subtareas ({len(projects)} proyectos x {len(kinds)} tipos)", parent)
        return {"id": parent, "subtasks": len(ids), "projects": projects, "kinds": kinds}

    def seed(self, reseed_seconds: float = 6 * 3600) -> int:
        """Encola las revisiones estándar de cada proyecto que no tengan una reciente o en curso."""
        n, now = 0, time.time()
        for pid in self.projects():
            for k in checks.KINDS:
                if not self.queue.open_for(pid, k) and now - self.queue.last_done(pid, k) >= reseed_seconds:
                    self.queue.add(k, pid, {"task": "autopilot"}, priority=5)
                    n += 1
        return n

    # ---------- ejecución ----------
    def run_task(self, task: dict) -> dict:
        pid, kind = task["project"], task["kind"]
        project = get_project(pid)
        if project is None:
            raise KeyError(f"proyecto {pid} no está en projects.json")
        if kind not in checks.KINDS:
            raise ValueError(f"tipo {kind} no soportado")
        files = checks.files_for(kind, self.index, pid)
        fn = checks.PER_FILE[kind]
        shards = [files[i::self.workers_per_project] for i in range(self.workers_per_project)]
        shards = [s for s in shards if s]
        base = self.index.root / pid

        def sub_agent(shard):
            out = []
            for p in shard:
                out += fn(str(p.relative_to(base)), self.index.read(p))
            return out

        findings = []
        if shards:
            with ThreadPoolExecutor(max_workers=len(shards), thread_name_prefix=f"sub-{pid[:12]}") as ex:
                for res in ex.map(sub_agent, shards):
                    findings += res
        findings += checks.project_level(kind, self.index, project, findings)
        findings = checks.dedupe(findings)
        summary = {"project": pid, "kind": kind, "files_reviewed": len(files), "sub_agents": len(shards),
                   "counts": checks.score(findings), "findings": len(findings)}
        path = self._write_report(project, kind, findings, summary)
        return {"report_path": str(path), "summary": summary}

    def _write_report(self, project: dict, kind: str, findings: list[dict], summary: dict) -> Path:
        d = self.reports_dir / project["id"]
        d.mkdir(parents=True, exist_ok=True)
        ts = time.strftime("%Y-%m-%d %H:%M:%S %Z")
        (d / f"{kind}.json").write_text(json.dumps({"generated": ts, "summary": summary, "findings": findings}, ensure_ascii=False, indent=1), encoding="utf-8")
        c = summary["counts"]
        lines = [f"# {KIND_TITLES[kind]} — {project['id']}", "",
                 f"Generado: {ts} · archivos revisados: {summary['files_reviewed']} · sub-agentes: {summary['sub_agents']}",
                 f"Repositorio: {project.get('url', '')}", "",
                 f"**Alta: {c['high']} · Media: {c['medium']} · Baja: {c['low']} · Info: {c['info']}**", "",
                 "Revisión automática por reglas (sin LLM). Son indicios a revisar, no veredictos.", ""]
        groups = {}
        for f in findings:
            groups.setdefault(f["severity"], []).append(f)
        for sev in ("high", "medium", "low", "info"):
            fs = groups.get(sev, [])
            if not fs:
                continue
            lines += [f"## {sev.upper()} ({len(fs)})", ""]
            for f in fs[:60]:
                loc = f"`{f['file']}:{f['line']}`" if f["line"] else f"`{f['file']}`"
                q = f" — «{f['quote']}»" if f.get("quote") else ""
                lines.append(f"- {loc} {f['message']}{q}")
                if f.get("tool_output"):
                    lines.append("  ```\n  " + f["tool_output"].replace("\n", "\n  ") + "\n  ```")
            if len(fs) > 60:
                lines.append(f"- … y {len(fs) - 60} más (ver {kind}.json)")
            lines.append("")
        p = d / f"{kind}.md"
        p.write_text("\n".join(lines), encoding="utf-8")
        return p

    def _work(self, task: dict):
        try:
            res = self.run_task(task)
            self.queue.complete(task["id"], res["report_path"], res["summary"])
            return True
        except Exception as exc:
            self.queue.fail(task["id"], f"{type(exc).__name__}: {exc}\n{traceback.format_exc(limit=3)}")
            return False
        finally:
            with self._blk:
                self._busy.discard(task["project"])

    def run_cycle(self, max_tasks: int | None = None) -> dict:
        """Ejecuta hasta max_tasks tareas pendientes con como mucho max_workers en paralelo."""
        limit = max_tasks or self.max_workers * 4
        done = errors = 0
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="ags-worker") as ex:
            futures = []
            claimed = 0
            while claimed < limit:
                with self._blk:
                    task = self.queue.claim(self.worker_id, exclude_projects=set(self._busy))
                    if task:
                        self._busy.add(task["project"])
                if not task:
                    if any(not f.done() for f in futures):
                        time.sleep(0.02)
                        continue
                    break
                claimed += 1
                futures.append(ex.submit(self._work, task))
            for f in futures:
                if f.result():
                    done += 1
                else:
                    errors += 1
        stats = {"ts": time.time(), "tasks": done + errors, "done": done, "errors": errors, "seconds": round(time.time() - t0, 2)}
        cycles = self.queue.kv_get("cycles", 0) + 1
        self.queue.kv_set("cycles", cycles)
        self.queue.kv_set("last_cycle", stats)
        if done:
            self.write_summary()
        return stats

    # ---------- estado y resumen ----------
    def latest_reports(self) -> list[dict]:
        out = []
        for pid in self.projects():
            for k in checks.KINDS:
                p = self.reports_dir / pid / f"{k}.json"
                if p.exists():
                    try:
                        out.append(json.loads(p.read_text(encoding="utf-8")))
                    except json.JSONDecodeError:
                        pass
        return out

    def write_summary(self) -> Path:
        reps = self.latest_reports()
        by_proj, kinds_tot, top = {}, {}, []
        for r in reps:
            s = r["summary"]
            bp = by_proj.setdefault(s["project"], {"high": 0, "medium": 0, "low": 0, "info": 0})
            for k, v in s["counts"].items():
                bp[k] += v
            for f in r["findings"]:
                if f["severity"] in ("high", "medium"):
                    kinds_tot[(f["severity"], f["kind"])] = kinds_tot.get((f["severity"], f["kind"]), 0) + 1
                if f["severity"] == "high":
                    top.append((s["project"], f))
        lines = ["# Resumen del supervisor AGs-Core v3.6", "", f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}",
                 f"Proyectos con informe: {len(by_proj)}", "", "## Problemas más frecuentes (alta/media)", ""]
        for (sev, kind), n in sorted(kinds_tot.items(), key=lambda x: (x[0][0] != "high", -x[1])):
            lines.append(f"- [{sev}] {kind}: {n}")
        lines += ["", "## Proyectos con más hallazgos de severidad alta", "", "| proyecto | alta | media | baja |", "|---|---|---|---|"]
        for pid, c in sorted(by_proj.items(), key=lambda x: (-x[1]["high"], -x[1]["medium"])):
            lines.append(f"| {pid} | {c['high']} | {c['medium']} | {c['low']} |")
        lines += ["", "## Ejemplos de hallazgos de severidad alta", ""]
        for pid, f in top[:40]:
            lines.append(f"- **{pid}** `{f['file']}:{f['line']}` {f['message']}" + (f" — «{f['quote'][:160]}»" if f.get("quote") else ""))
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        p = self.reports_dir / "SUMMARY.md"
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        (self.reports_dir / "summary.json").write_text(json.dumps(
            {"projects": by_proj, "kinds": {f"{a}:{b}": n for (a, b), n in kinds_tot.items()}}, ensure_ascii=False, indent=1), encoding="utf-8")
        return p

    def status(self) -> dict:
        hb = self.queue.kv_get("autopilot_heartbeat")
        alive = bool(hb and not hb.get("stopped") and time.time() - hb.get("ts", 0) < max(120, 3 * hb.get("interval", 30)))
        return {
            "max_workers": self.max_workers, "workers_per_project": self.workers_per_project,
            "projects": len(self.projects()), "queue": self.queue.counts(),
            "cycles": self.queue.kv_get("cycles", 0), "last_cycle": self.queue.kv_get("last_cycle"),
            "autopilot": {"alive": alive, "heartbeat": hb},
            "recent_errors": self.queue.events(10, "error"),
            "reports_dir": str(self.reports_dir),
        }


_SUP: Supervisor | None = None
_SLK = threading.Lock()


def get_supervisor() -> Supervisor:
    global _SUP
    with _SLK:
        if _SUP is None:
            _SUP = Supervisor()
        return _SUP


def reset_supervisor(s: Supervisor | None = None):
    global _SUP
    with _SLK:
        _SUP = s
