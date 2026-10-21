#!/usr/bin/env python3
"""C-MAT-004: diferencias run1 frente a run2 (descriptivo de H-REP). Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os
M = ["Si","MgO","NaCl","LiF","NaF","KCl","KBr","CaO","CaF2","Al2O3","BeO","SrO","MgF2","TiO2","SiO2","Li2O","MgAl2O4"]
def leaves(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items(): yield from leaves(v, p + "/" + k)
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from leaves(v, f"{p}[{i}]")
    else: yield p, x
out = {}
for mod in ["mattersim", "mace"]:
    o = {}
    for m in M:
        a, b = (f"out/{r}/{mod}/{m}.json" for r in ("run1", "run2"))
        if not (os.path.exists(a) and os.path.exists(b)): o[m] = "FALTA"; continue
        A = dict(leaves(json.load(open(a)))); B = dict(leaves(json.load(open(b))))
        A.pop("/t_s", None); B.pop("/t_s", None)
        dif = [(k, A[k], B.get(k)) for k in A if A[k] != B.get(k)]
        rel = [abs(x - y) / max(abs(x), abs(y)) for _, x, y in dif if isinstance(x, float) and isinstance(y, float) and max(abs(x), abs(y)) > 1e-3]
        o[m] = {"n_campos_distintos": len(dif), "max_rel_campos_no_nulos": max(rel) if rel else 0.0, "campos": sorted({k.split("[")[0] for k, _, _ in dif})}
    out[mod] = o
json.dump(out, open("diff_runs.json", "w"), indent=1); print(json.dumps(out, indent=0))
