#!/usr/bin/env python3
"""Construye pares instrucción/respuesta (nota de texto -> LLP JSON) SOLO desde
documentos propios de Lázaro López Paz en ags-core-v3.6 (knowledge/, docs/).
Determinista: semilla fija, hashes SHA256 en data/manifest.json."""
import hashlib, json, random, re, sys
from pathlib import Path

SEED = 42
HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]  # ags-core-v3.6
OUT = HERE / "data"
AUTHOR_RE = re.compile(r"L[áa]zaro\s+L[óo]pez\s+Paz", re.I)
AUTOR = "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA"
EXTS = {".md", ".json", ".yaml", ".yml"}
INSTR = ("Convierte la siguiente nota en LLP JSON compacto con claves exactas "
         "meta, objetivo, datos_clave, tareas, riesgos, decisiones, proximo_paso "
         "(snake_case, sin null; vacíos como \"\" o []). Responde solo con el JSON.\n\nNOTA:\n")
KW_T = re.compile(r"\b(tarea|pendiente|implementar|desarrollar|crear|validar|todo|fase|sprint)\b", re.I)
KW_R = re.compile(r"\b(riesgo|limitaci[oó]n|advertencia|peligro|incertidumbre|no verificad)", re.I)
KW_D = re.compile(r"\b(decisi[oó]n|se decide|se elige|elegido|aprobado)\b", re.I)
KW_P = re.compile(r"\b(pr[oó]ximo paso|siguiente paso|next step)", re.I)

def authored(p: Path, text: str) -> bool:
    if AUTHOR_RE.search(text):
        return True
    rel = p.relative_to(ROOT).parts
    if rel[0] == "knowledge" and len(rel) > 2:  # README del proyecto lo atribuye
        rd = ROOT / "knowledge" / rel[1] / "README.md"
        return rd.exists() and bool(AUTHOR_RE.search(rd.read_text(errors="ignore")))
    return False

def clean(s):
    s = re.sub(r"[`*_>#|]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def lines_of(chunk):
    return [clean(l) for l in chunk.splitlines() if len(clean(l)) > 15]

def to_llp(title, chunk, src):
    ls = lines_of(chunk)
    sent = re.split(r"(?<=[.!?])\s", " ".join(ls))
    bullets = [clean(l) for l in chunk.splitlines() if re.match(r"\s*([-*+]|\d+[.)])\s+", l) and len(clean(l)) > 10]
    def pick(rx): return [l[:160] for l in ls if rx.search(l)][:4]
    prox = pick(KW_P)
    return {"meta": {"fuente": src, "seccion": title[:80], "autor": AUTOR, "evidencia": "E1"},
            "objetivo": (sent[0] if sent else title)[:200],
            "datos_clave": [b[:160] for b in bullets[:5]] or [s[:160] for s in sent[1:4]],
            "tareas": pick(KW_T), "riesgos": pick(KW_R), "decisiones": pick(KW_D),
            "proximo_paso": prox[0] if prox else ""}

def chunks_md(text):
    parts = re.split(r"(?m)^(#{1,4} .+)$", text)
    title, out = "inicio", []
    for part in parts:
        if re.match(r"^#{1,4} ", part):
            title = clean(part)
        elif len(clean(part)) >= 200:
            out.append((title, part.strip()[:1500]))
    return out

def main():
    files, skipped = [], []
    for base in ("knowledge", "docs"):
        for p in sorted((ROOT / base).rglob("*")):
            if not p.is_file() or p.suffix.lower() not in EXTS: continue
            if "fusi-n-carpeta" in p.parts or ".venv" in p.parts: continue
            t = p.read_text(errors="ignore")
            (files if authored(p, t) else skipped).append((p, t))
    pairs = []
    for p, t in files:
        src = str(p.relative_to(ROOT))
        if p.suffix == ".md":
            cs = chunks_md(t)
        else:  # json/yaml: texto plano como nota
            cs = [("archivo", t[:1500])] if len(t) >= 200 else []
        for title, c in cs:
            out = to_llp(title, c, src)
            pairs.append({"id": hashlib.sha256((src + title + c).encode()).hexdigest()[:16],
                          "instruction": INSTR + c, "response": json.dumps(out, ensure_ascii=False, separators=(",", ":")),
                          "source": src})
    seen, uniq = set(), []
    for x in pairs:
        if x["id"] not in seen: seen.add(x["id"]); uniq.append(x)
    # split por documento fuente para evitar fuga train/test
    srcs = sorted({x["source"] for x in uniq}); random.Random(SEED).shuffle(srcs)
    n = len(srcs); a, b = int(n * .8), int(n * .9)
    assign = {s: ("train" if i < a else "val" if i < b else "test") for i, s in enumerate(srcs)}
    OUT.mkdir(exist_ok=True)
    man = {"meta": {"seed": SEED, "autor": AUTOR, "licencia": "CC BY 4.0", "split": "80/10/10 por documento fuente"},
           "archivos_incluidos": len(files), "archivos_excluidos": len(skipped),
           "excluidos": [str(p.relative_to(ROOT)) for p, _ in skipped], "splits": {}}
    for sp in ("train", "val", "test"):
        rows = [x for x in uniq if assign[x["source"]] == sp]
        f = OUT / f"{sp}.jsonl"
        f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        man["splits"][sp] = {"pares": len(rows), "documentos": sum(1 for s in srcs if assign[s] == sp),
                             "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
    man["total_pares"] = len(uniq)
    (OUT / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1))
    print(json.dumps({k: man[k] for k in ("archivos_incluidos", "archivos_excluidos", "total_pares", "splits")}, indent=1))

if __name__ == "__main__":
    main()
