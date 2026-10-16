"""Memoria sqlite. La semejanza es solape de palabras, no un embedding."""
import sqlite3
import threading
import time
from pathlib import Path


class Memory:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False)  # v3.5: uso desde hilos de FastAPI
        self._lk = threading.Lock()
        self._x(
            "create table if not exists exp (id integer primary key, ts real, role text, project text, text text)"
        )
        self._x("create table if not exists meta (k text primary key, v text)")
        self._c()

    def _x(self, *a):
        with self._lk:
            return self.db.execute(*a)

    def _c(self):
        with self._lk:
            self.db.commit()

    def add(self, text: str, role: str = "user", project: str = "general") -> None:
        self._x(
            "insert into exp (ts, role, project, text) values (?, ?, ?, ?)",
            (time.time(), role, project, text),
        )
        self._c()

    def count(self) -> int:
        return int(self._x("select count(*) from exp").fetchone()[0])

    def corpus(self, limite: int = 400) -> str:
        rows = self._x("select text from exp order by id desc limit ?", (limite,)).fetchall()
        return "\n".join(r[0] for r in reversed(rows))

    def similar(self, consulta: str, n: int = 3) -> list[str]:
        palabras = {w for w in consulta.lower().split() if len(w) > 2}
        if not palabras:
            return []
        rows = self._x("select text from exp order by id desc limit 500").fetchall()
        puntuados = []
        for (texto,) in rows:
            toks = set(texto.lower().split())
            s = len(palabras & toks)
            if s:
                puntuados.append((s, texto))
        puntuados.sort(key=lambda x: -x[0])
        return [t for _, t in puntuados[:n]]

    def meta_get(self, k: str, defecto: str = "0") -> str:
        row = self._x("select v from meta where k = ?", (k,)).fetchone()
        return row[0] if row else defecto

    def meta_set(self, k: str, v: str) -> None:
        self._x("insert into meta (k, v) values (?, ?) on conflict(k) do update set v = excluded.v", (k, v))
        self._c()
