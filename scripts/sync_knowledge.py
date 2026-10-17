"""Copia los textos (README, docs, código pequeño) de los repos de proyecto a knowledge/<id>/
y genera projects.json. Solo lee de los origenes; no modifica ningun repo.

Uso:
    python scripts/sync_knowledge.py --src /ruta/repos [--src /otra/ruta] [--github owner/repo ...]
"""
import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_EXT = {".md", ".txt", ".tex", ".bib", ".py", ".sh", ".json", ".rs", ".lean", ".ts", ".js", ".html", ".toml", ".yml", ".yaml", ".log"}
MAX_BYTES = 400_000

# proyecto -> herramientas físicas locales (ids de app/ags_local/projects.json)
TOOLS = {
    "cero-a-amoniaco": ["zero_a"],
    "espana-sin-petroleo": ["zero_a"],
    "helio3-fusion-qmc-h3": ["d3he_tokamak"],
    "helioatlas-helio3": ["d3he_tokamak"],
    "iqm-he3-anti-platform": ["d3he_tokamak"],
    "mei-rit-propulsion": ["mei_rit"],
    "q-matrix-autonomous-control": ["q_matrix"],
    "sensores-cuanticos": ["q_matrix"],
    "glyd-qsense": ["q_matrix"],
    "neuroglyq": ["neuroglyq"],
    "neuro-kinetic-parkinson-alzheimer": ["neuroglyq"],
    "ecosistema-cuantico-fractal": ["ecosistema"],
}
STOP = set("de la el en y a los las del un una para por con que se su al es lo como mas o sus the of and to in for on with is are an by this be from at or as que ia ai v2 v3 copia".split())


def slug(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "proyecto"


def is_text(p: Path) -> bool:
    if p.name in ("LICENSE", "NOTICE", "Makefile") or p.suffix.lower() in TEXT_EXT:
        try:
            p.read_text(encoding="utf-8")
            return True
        except (UnicodeDecodeError, OSError):
            return False
    return False


def describe(readme: str, pid: str):
    title, desc = pid, ""
    for line in readme.splitlines():
        s = line.strip()
        if s.startswith("# ") and title == pid:
            title = s[2:].strip()
        elif s and not s.startswith(("#", "**", "-", "|", "`", "!")) and not desc:
            desc = s[:300]
    return title, desc


def keywords(pid: str, title: str) -> list[str]:
    toks = re.findall(r"[a-záéíóúñü0-9³]+", f"{pid.replace('-', ' ')} {title}".lower())
    out = []
    for t in toks:
        if len(t) > 2 and t not in STOP and t not in out:
            out.append(t)
    return out[:12]


def copy_repo(src: Path, pid: str, repo: str, source: str) -> dict:
    dst = ROOT / "knowledge" / pid
    if dst.exists():
        shutil.rmtree(dst)
    files, skipped = [], []
    for p in sorted(src.rglob("*")):
        if not p.is_file() or ".git" in p.parts:
            continue
        rel = p.relative_to(src)
        if len(str(rel)) > 200:  # nombres rotos (p. ej. contenido pegado en el nombre)
            skipped.append(str(rel)[:80] + "…")
            continue
        if p.stat().st_size <= MAX_BYTES and is_text(p):
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst / rel)
            files.append(str(rel))
        else:
            skipped.append(str(rel))
    readme = (dst / "README.md").read_text(encoding="utf-8") if (dst / "README.md").exists() else ""
    title, desc = describe(readme, pid)
    lic = "none"
    if (dst / "LICENSE").exists():
        t = (dst / "LICENSE").read_text(encoding="utf-8")
        lic = "MIT" if "MIT License" in t or "Permission is hereby granted" in t else "other"
    return {
        "id": pid, "name": title, "repo": repo, "source": source,
        "url": f"https://github.com/{repo}", "description": desc,
        "keywords": keywords(pid, title), "tools": TOOLS.get(pid, []),
        "license": lic, "files": len(files), "binaries_or_skipped": skipped,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", action="append", default=[], help="carpeta con un subdirectorio por repo")
    ap.add_argument("--github", action="append", default=[], help="owner/repo a leer con git archive (solo lectura)")
    ap.add_argument("--owner", default="canelonemf-byte")
    a = ap.parse_args()
    projects = []
    for s in a.src:
        for d in sorted(Path(s).iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                projects.append(copy_repo(d, slug(d.name), f"{a.owner}/{d.name}", "local"))
    for full in a.github:
        name = full.split("/")[-1]
        with tempfile.TemporaryDirectory() as tmp:
            bare = Path(tmp) / "r.git"
            subprocess.run(["git", "clone", "-q", "--bare", "--depth", "1", f"https://github.com/{full}.git", str(bare)], check=True)
            names = subprocess.run(["git", "-C", str(bare), "ls-tree", "-r", "--name-only", "-z", "HEAD"], check=True, capture_output=True).stdout.decode().split("\0")
            work = Path(tmp) / "w"
            broken = []
            for n in filter(None, names):
                if len(n) > 200 or "\n" in n:
                    broken.append(n)
                    continue
                out = work / n
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(subprocess.run(["git", "-C", str(bare), "show", f"HEAD:{n}"], check=True, capture_output=True).stdout)
            p = copy_repo(work, slug(name), full, "github")
            p["broken_paths"] = [b.split("\n")[0][:80] + " (nombre de archivo roto: contiene el contenido)" for b in broken]
            projects.append(p)
    projects.sort(key=lambda p: p["id"])
    manifest = {"version": "3.6.0", "owner": a.owner, "projects": projects}
    (ROOT / "projects.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(projects)} proyectos -> projects.json; knowledge/ actualizado")


if __name__ == "__main__":
    main()
