import json
import os
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def manifest_path() -> Path:
    return Path(os.getenv("AGS_PROJECTS_MANIFEST", ROOT / "projects.json"))


def knowledge_dir() -> Path:
    return Path(os.getenv("AGS_KNOWLEDGE_DIR", ROOT / "knowledge"))


@lru_cache(maxsize=4)
def _load(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        return {"version": "0", "projects": []}
    return json.loads(p.read_text(encoding="utf-8"))


def load_manifest() -> dict:
    return _load(str(manifest_path()))


def project_ids() -> list[str]:
    return [p["id"] for p in load_manifest()["projects"]]


def get_project(pid: str) -> dict | None:
    for p in load_manifest()["projects"]:
        if p["id"] == pid:
            return p
    return None
