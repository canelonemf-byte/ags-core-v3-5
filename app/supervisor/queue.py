"""Cola de tareas persistente (SQLite). Segura entre hilos y entre procesos (API + autopilot)."""
import json
import sqlite3
import threading
import time
from pathlib import Path

SCHEMA = """
create table if not exists tasks (
  id integer primary key autoincrement,
  parent_id integer,
  project text,
  kind text not null,
  payload text default '{}',
  status text not null default 'pending',   -- pending | running | done | error | split
  priority integer default 5,
  attempts integer default 0,
  max_attempts integer default 3,
  not_before real default 0,
  created real, started real, finished real,
  worker text, report_path text, summary text, error text
);
create index if not exists ix_tasks_status on tasks(status, priority, id);
create index if not exists ix_tasks_proj on tasks(project, kind, status);
create table if not exists events (id integer primary key autoincrement, ts real, level text, task_id integer, message text);
create table if not exists kv (k text primary key, v text);
"""
COLS = ["id", "parent_id", "project", "kind", "payload", "status", "priority", "attempts", "max_attempts",
        "not_before", "created", "started", "finished", "worker", "report_path", "summary", "error"]


class TaskQueue:
    def __init__(self, path: Path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.db = sqlite3.connect(str(path), check_same_thread=False, timeout=30, isolation_level=None)
        self.db.execute("pragma journal_mode=wal")
        self.db.execute("pragma busy_timeout=30000")
        self._lk = threading.RLock()
        with self._lk:
            self.db.executescript(SCHEMA)

    def _row(self, r):
        if r is None:
            return None
        d = dict(zip(COLS, r))
        d["payload"] = json.loads(d["payload"] or "{}")
        d["summary"] = json.loads(d["summary"]) if d["summary"] else None
        return d

    def add(self, kind: str, project: str | None = None, payload: dict | None = None, parent_id: int | None = None,
            priority: int = 5, max_attempts: int = 3, status: str = "pending") -> int:
        with self._lk:
            cur = self.db.execute(
                "insert into tasks (parent_id, project, kind, payload, status, priority, max_attempts, created) values (?,?,?,?,?,?,?,?)",
                (parent_id, project, kind, json.dumps(payload or {}, ensure_ascii=False), status, priority, max_attempts, time.time()))
            return cur.lastrowid

    def claim(self, worker: str, exclude_projects: set | None = None) -> dict | None:
        """Toma atómicamente la siguiente tarea pendiente (por prioridad), opcionalmente evitando proyectos ocupados."""
        now = time.time()
        with self._lk:
            self.db.execute("begin immediate")
            try:
                rows = self.db.execute(
                    "select id, project from tasks where status='pending' and not_before<=? order by priority, id limit 200", (now,)).fetchall()
                pick = next((i for i, p in rows if not exclude_projects or p not in exclude_projects), None)
                if pick is None:
                    self.db.execute("commit")
                    return None
                self.db.execute("update tasks set status='running', started=?, worker=?, attempts=attempts+1 where id=?", (now, worker, pick))
                self.db.execute("commit")
            except Exception:
                self.db.execute("rollback")
                raise
            return self.get(pick)

    def complete(self, tid: int, report_path: str, summary: dict):
        with self._lk:
            self.db.execute("update tasks set status='done', finished=?, report_path=?, summary=?, error=null where id=?",
                            (time.time(), report_path, json.dumps(summary, ensure_ascii=False), tid))
        self._close_parent(tid)

    def fail(self, tid: int, error: str, backoff: float = 60.0):
        t = self.get(tid)
        with self._lk:
            if t and t["attempts"] < t["max_attempts"]:
                self.db.execute("update tasks set status='pending', error=?, not_before=? where id=?",
                                (error[:2000], time.time() + backoff * t["attempts"], tid))
            else:
                self.db.execute("update tasks set status='error', error=?, finished=? where id=?", (error[:2000], time.time(), tid))
        self.log("error", f"tarea {tid}: {error[:300]}", tid)
        self._close_parent(tid)

    def _close_parent(self, tid: int):
        t = self.get(tid)
        if not t or not t["parent_id"]:
            return
        with self._lk:
            left = self.db.execute("select count(*) from tasks where parent_id=? and status in ('pending','running')", (t["parent_id"],)).fetchone()[0]
            if left == 0:
                errs = self.db.execute("select count(*) from tasks where parent_id=? and status='error'", (t["parent_id"],)).fetchone()[0]
                self.db.execute("update tasks set status=?, finished=? where id=?", ("error" if errs else "done", time.time(), t["parent_id"]))

    def requeue_stale(self, older_than: float = 1800.0) -> int:
        with self._lk:
            cur = self.db.execute("update tasks set status='pending' where status='running' and started < ?", (time.time() - older_than,))
            return cur.rowcount

    def get(self, tid: int) -> dict | None:
        with self._lk:
            return self._row(self.db.execute(f"select {','.join(COLS)} from tasks where id=?", (tid,)).fetchone())

    def list_tasks(self, status: str | None = None, project: str | None = None, limit: int = 100, parent_id: int | None = None) -> list[dict]:
        q, a = f"select {','.join(COLS)} from tasks where 1=1", []
        if status:
            q += " and status=?"; a.append(status)
        if project:
            q += " and project=?"; a.append(project)
        if parent_id is not None:
            q += " and parent_id=?"; a.append(parent_id)
        q += " order by id desc limit ?"; a.append(limit)
        with self._lk:
            return [self._row(r) for r in self.db.execute(q, a).fetchall()]

    def counts(self) -> dict:
        with self._lk:
            return {s: n for s, n in self.db.execute("select status, count(*) from tasks group by status").fetchall()}

    def open_for(self, project: str, kind: str) -> bool:
        with self._lk:
            return self.db.execute("select 1 from tasks where project=? and kind=? and status in ('pending','running') limit 1", (project, kind)).fetchone() is not None

    def last_done(self, project: str, kind: str) -> float:
        with self._lk:
            r = self.db.execute("select max(finished) from tasks where project=? and kind=? and status in ('done','error')", (project, kind)).fetchone()
            return r[0] or 0.0

    def log(self, level: str, message: str, task_id: int | None = None):
        with self._lk:
            self.db.execute("insert into events (ts, level, task_id, message) values (?,?,?,?)", (time.time(), level, task_id, message[:2000]))

    def events(self, limit: int = 20, level: str | None = None) -> list[dict]:
        q, a = "select ts, level, task_id, message from events", []
        if level:
            q += " where level=?"; a.append(level)
        q += " order by id desc limit ?"; a.append(limit)
        with self._lk:
            return [dict(zip(("ts", "level", "task_id", "message"), r)) for r in self.db.execute(q, a).fetchall()]

    def kv_get(self, k: str, default=None):
        with self._lk:
            r = self.db.execute("select v from kv where k=?", (k,)).fetchone()
        return json.loads(r[0]) if r else default

    def kv_set(self, k: str, v):
        with self._lk:
            self.db.execute("insert into kv (k, v) values (?, ?) on conflict(k) do update set v=excluded.v", (k, json.dumps(v, ensure_ascii=False)))
