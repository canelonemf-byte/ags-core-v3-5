"""Índice de conocimiento local por proyecto: trozos de texto + TF-IDF (puro Python).

Si scikit-learn está instalado se usa su TfidfVectorizer; si no, una implementación propia.
El índice se persiste en SQLite (tabla chunks) y se reconstruye si cambian los archivos.
"""
import hashlib
import math
import re
import sqlite3
import threading
import unicodedata
from collections import Counter
from pathlib import Path

from .manifest import knowledge_dir

DOC_EXT = {".md", ".txt", ".tex", ".bib"}
CODE_EXT = {".py", ".sh", ".rs", ".lean", ".ts", ".js", ".html", ".json", ".toml", ".yml", ".yaml"}
_TOK = re.compile(r"[a-z0-9]+(?:[.,][0-9]+)?")


def plain(s: str) -> str:
    s = s.lower()
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def tokens(s: str) -> list[str]:
    return [t for t in _TOK.findall(plain(s)) if len(t) > 2]


def chunk_text(text: str, size: int = 900, overlap: int = 150) -> list[str]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    out, cur = [], ""
    for p in paras:
        if len(cur) + len(p) + 2 <= size:
            cur = f"{cur}\n\n{p}" if cur else p
            continue
        if cur:
            out.append(cur)
        while len(p) > size:
            out.append(p[:size])
            p = p[size - overlap:]
        cur = p
    if cur:
        out.append(cur)
    return out


# Directorios de entorno/caché que no son obra del proyecto (no se escanean).
SKIP_DIRS = frozenset({".venv", "venv", ".hf_cache", "node_modules", "__pycache__", ".git",
                       ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache", ".ipynb_checkpoints", ".tox"})


class _Tfidf:
    """TF-IDF mínimo con normalización L2 (fallback sin scikit-learn)."""

    def __init__(self, docs: list[str]):
        self.toks = [Counter(tokens(d)) for d in docs]
        n = len(docs)
        df = Counter()
        for c in self.toks:
            df.update(c.keys())
        self.idf = {t: math.log((1 + n) / (1 + f)) + 1 for t, f in df.items()}
        self.vecs = [self._vec(c) for c in self.toks]

    def _vec(self, c: Counter) -> dict:
        v = {t: (1 + math.log(f)) * self.idf.get(t, 0.0) for t, f in c.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {t: x / norm for t, x in v.items()}

    def scores(self, query: str) -> list[float]:
        q = self._vec(Counter(tokens(query)))
        return [sum(w * v.get(t, 0.0) for t, w in q.items()) for v in self.vecs]


class _SkTfidf:
    def __init__(self, docs):
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vz = TfidfVectorizer(tokenizer=tokens, lowercase=False, sublinear_tf=True, token_pattern=None)
        self.m = self.vz.fit_transform(docs)

    def scores(self, query):
        q = self.vz.transform([query])
        return (self.m @ q.T).toarray().ravel().tolist()


def _make_tfidf(docs, prefer_sklearn=True):
    if prefer_sklearn:
        try:
            return _SkTfidf(docs)
        except Exception:  # sklearn ausente o vocabulario vacío
            pass
    return _Tfidf(docs)


class ProjectKnowledge:
    def __init__(self, pid: str, rows: list[tuple[str, str]], prefer_sklearn=True):
        self.pid = pid
        self.rows = rows  # (archivo, texto)
        self._tf = _make_tfidf([t for _, t in rows], prefer_sklearn) if rows else None

    def search(self, query: str, k: int = 4) -> list[dict]:
        if not self._tf or not query.strip():
            return []
        sc = self._tf.scores(query)
        qt = set(tokens(query))
        ranked = []
        for i, s in enumerate(sc):
            kw = len(qt & set(tokens(self.rows[i][1])))  # componente de palabras clave
            total = s + 0.05 * kw
            if total > 0:
                ranked.append((total, i))
        ranked.sort(reverse=True)
        return [{"file": self.rows[i][0], "score": round(s, 4), "text": self.rows[i][1]} for s, i in ranked[:k]]


class KnowledgeIndex:
    def __init__(self, root: Path | None = None, db_path: Path | None = None, prefer_sklearn=True):
        self.root = Path(root or knowledge_dir())
        self.db_path = db_path
        self.prefer_sklearn = prefer_sklearn
        self._lk = threading.Lock()
        self._cache: dict[str, tuple[str, ProjectKnowledge]] = {}
        self.db = None
        if db_path:
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            self.db = sqlite3.connect(str(db_path), check_same_thread=False)
            self.db.execute("create table if not exists chunks (project text, sig text, file text, n integer, text text)")
            self.db.execute("create index if not exists ix_chunks on chunks(project)")
            self.db.commit()

    def files(self, pid: str) -> list[Path]:
        base = self.root / pid
        if not base.exists():
            return []
        return sorted(p for p in base.rglob("*")
                      if p.is_file() and not (set(p.relative_to(base).parts[:-1]) & SKIP_DIRS))

    def doc_files(self, pid: str) -> list[Path]:
        return [p for p in self.files(pid) if p.suffix.lower() in DOC_EXT or p.name in ("LICENSE", "NOTICE")]

    def code_files(self, pid: str) -> list[Path]:
        return [p for p in self.files(pid) if p.suffix.lower() in CODE_EXT]

    def read(self, p: Path) -> str:
        try:
            return p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return ""

    def _sig(self, pid: str) -> str:
        h = hashlib.sha1()
        for p in self.files(pid):
            st = p.stat()
            h.update(f"{p.relative_to(self.root)}:{st.st_size}:{int(st.st_mtime)}".encode())
        return h.hexdigest()

    def _rows(self, pid: str, sig: str) -> list[tuple[str, str]]:
        if self.db is not None:
            with self._lk:
                got = self.db.execute("select file, text from chunks where project=? and sig=? order by rowid", (pid, sig)).fetchall()
            if got:
                return [(f, t) for f, t in got]
        rows = []
        for p in self.doc_files(pid) + self.code_files(pid):
            rel = str(p.relative_to(self.root / pid))
            for c in chunk_text(self.read(p)):
                rows.append((rel, c))
        if self.db is not None:
            with self._lk:
                self.db.execute("delete from chunks where project=?", (pid,))
                self.db.executemany("insert into chunks values (?,?,?,?,?)", [(pid, sig, f, i, t) for i, (f, t) in enumerate(rows)])
                self.db.commit()
        return rows

    def project(self, pid: str) -> ProjectKnowledge:
        sig = self._sig(pid)
        hit = self._cache.get(pid)
        if hit and hit[0] == sig:
            return hit[1]
        pk = ProjectKnowledge(pid, self._rows(pid, sig), self.prefer_sklearn)
        self._cache[pid] = (sig, pk)
        return pk

    def search(self, pid: str, query: str, k: int = 4) -> list[dict]:
        return self.project(pid).search(query, k)

    def stats(self, pid: str) -> dict:
        pk = self.project(pid)
        return {"chunks": len(pk.rows), "files": len(self.files(pid)), "docs": len(self.doc_files(pid)), "code": len(self.code_files(pid))}


_INDEX: KnowledgeIndex | None = None
_ILK = threading.Lock()


def get_index() -> KnowledgeIndex:
    global _INDEX
    with _ILK:
        if _INDEX is None:
            import os
            data = Path(os.getenv("AGSGPT_DATA_DIR", Path(__file__).resolve().parents[2] / "data"))
            _INDEX = KnowledgeIndex(db_path=data / "knowledge.sqlite")
        return _INDEX


def reset_index(idx: KnowledgeIndex | None = None):
    global _INDEX
    with _ILK:
        _INDEX = idx
