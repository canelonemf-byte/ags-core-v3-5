"""Memoria cognitiva (Unified Cognitive Stack) para AGs-Core.

El decaimiento se importa de ucs/memory_decay.py: servidor y simulación usan
la MISMA función (fuente única). /chat no usa LLM: devuelve las memorias
recuperadas (LiteLLM aún no configurado).
"""
import json, math, os, re, sqlite3, sys, threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

UCS_DIR = Path(__file__).resolve().parent.parent / "ucs"
if str(UCS_DIR) not in sys.path:
    sys.path.insert(0, str(UCS_DIR))
import memory_decay  # noqa: E402

DB_PATH = Path(os.getenv("UCS_MEMORY_DB", Path(__file__).resolve().parent.parent / "data" / "ucs_memory.sqlite3"))
_lock = threading.Lock()


@dataclass
class Mem:
    id: int
    subject: str
    fact_contents: str
    keywords: list
    importance_score: float
    access_count: int
    last_access: datetime | None
    pinned: bool


def _conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.execute("""CREATE TABLE IF NOT EXISTS memories(
        id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, fact_contents TEXT,
        keywords TEXT, importance_score REAL, access_count INTEGER DEFAULT 0,
        created_at TEXT, last_access TEXT, pinned INTEGER DEFAULT 0)""")
    return c


def _row(r) -> Mem:
    la = datetime.fromisoformat(r[7]) if r[7] else None
    return Mem(r[0], r[1], r[2], json.loads(r[3] or "[]"), r[4], r[5], la, bool(r[8]))


def add(subject: str, fact: str, keywords: list, importance: float, pinned: bool = False) -> int:
    importance = min(max(float(importance), 0.0), 1.0)
    pinned = pinned or importance >= memory_decay.PIN_IMPORTANCE
    now = datetime.now(timezone.utc).isoformat()
    with _lock, _conn() as c:
        cur = c.execute("INSERT INTO memories(subject,fact_contents,keywords,importance_score,"
                        "access_count,created_at,last_access,pinned) VALUES(?,?,?,?,0,?,?,?)",
                        (subject, fact, json.dumps(keywords, ensure_ascii=False), importance, now, now, int(pinned)))
        return cur.lastrowid


def all_memories() -> list[Mem]:
    with _conn() as c:
        return [_row(r) for r in c.execute("SELECT * FROM memories")]


def retention(m: Mem) -> float:
    return memory_decay._decay_score(m)


def _tokens(t: str) -> set:
    return {w for w in re.findall(r"\w+", t.lower()) if len(w) > 2}


def search(query: str, top_k: int = 5) -> list[tuple[Mem, float, float]]:
    q = _tokens(query)
    scored = []
    for m in all_memories():
        if memory_decay.should_forget(m):
            continue
        doc = _tokens(m.subject + " " + m.fact_contents) | {k.lower() for k in m.keywords}
        overlap = len(q & doc)
        if not overlap:
            continue
        s = retention(m)
        scored.append((m, overlap / math.sqrt(len(doc) or 1) * s, s))
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:top_k]
    now = datetime.now(timezone.utc).isoformat()
    with _lock, _conn() as c:
        for m, _, _ in top:
            c.execute("UPDATE memories SET access_count=access_count+1, last_access=? WHERE id=?", (now, m.id))
    return top


def stats() -> dict:
    ms = all_memories()
    return {"total": len(ms), "pinned": sum(memory_decay.is_pinned(m) for m in ms),
            "forgettable": sum(memory_decay.should_forget(m) for m in ms),
            "params": {"tau0_days": memory_decay.TAU0_DAYS, "alpha": memory_decay.ALPHA_IMPORTANCE,
                       "beta": memory_decay.BETA_USE, "forget_threshold": memory_decay.FORGET_THRESHOLD,
                       "pin_importance": memory_decay.PIN_IMPORTANCE}}
