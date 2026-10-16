"""Registro de proyectos y enrutado por palabras."""
import json
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from .tools import CATALOGO


def _llano(s: str) -> str:
    s = s.lower().replace("µ", "u").replace("μ", "u")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


@dataclass
class Project:
    id: str
    name: str
    domain: str
    status: str
    summary: str
    keywords: list[str]
    tools: dict = field(default_factory=dict)


class Registry:
    def __init__(self, path: Path):
        raw = json.loads(path.read_text(encoding="utf-8"))
        self.projects = {
            p["id"]: Project(
                id=p["id"],
                name=p["name"],
                domain=p["domain"],
                status=p["status"],
                summary=p["summary"],
                keywords=p["keywords"],
            )
            for p in raw["projects"]
        }
        for pid, nombre, _claves, fn in CATALOGO:
            self.projects[pid].tools[nombre] = fn

    def get(self, pid: str):
        return self.projects.get(pid)

    def route(self, texto: str):
        t = _llano(texto)
        mejor, puntos = None, 0
        for p in self.projects.values():
            n = sum(1 for k in p.keywords if _llano(k) in t)
            if n > puntos:
                mejor, puntos = p, n
        return mejor

    def match_tool(self, pid: str, texto: str):
        proj = self.get(pid)
        if not proj:
            return None
        t = _llano(texto)
        for p, nombre, claves, fn in CATALOGO:
            if p != pid:
                continue
            if any(_llano(c) in t for c in claves):
                return nombre, fn
        return None
