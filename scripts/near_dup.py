"""Detector de duplicados exactos y casi-duplicados (TF-IDF de 5-gramas de caracteres, coseno).

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia MIT.
Evidencia: E3 software (herramienta probada); los hallazgos son E1 (análisis textual), no prueban plagio.

    python scripts/near_dup.py [--threshold 0.85] [--quarantine] [--out reports/near_dup_FECHA]
"""
import argparse, hashlib, json, re, sys, unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "knowledge/fusi-n-carpeta/data"
TEST_SHA = "0937f06c329f1744f22570dab347aca26fa487c771356027b9bdead33e6f8ef5"
EXTRA = [Path("/workspace/p003/pares_lora.jsonl")]


def norm(t: str) -> str:
    t = unicodedata.normalize("NFKC", t).lower()
    return re.sub(r"\s+", " ", t).strip()


def sha(t: str) -> str:
    return hashlib.sha256(t.encode()).hexdigest()


def load_pairs():
    items = []
    srcs = [("train", DATA / "train.jsonl"), ("val", DATA / "val.jsonl"), ("test", DATA / "test.jsonl")]
    for p in sorted((ROOT / "knowledge").rglob("*.jsonl")):
        if DATA in p.parents:
            continue
        srcs.append(("agente", p))
    srcs += [("p003", p) for p in EXTRA if p.exists()]
    for split, p in srcs:
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines()):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "instruction" not in r:
                continue
            txt = norm(f"{r.get('instruction','')} {r.get('response','')}")
            items.append({"split": split, "file": str(p.relative_to(ROOT)) if ROOT in p.parents else str(p),
                          "line": i + 1, "id": str(r.get("id", "")), "text": txt, "sha": sha(txt)})
    return items


def cosine_pairs(texts, threshold):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    if len(texts) < 2:
        return []
    X = TfidfVectorizer(analyzer="char_wb", ngram_range=(5, 5), sublinear_tf=True, min_df=1).fit_transform(texts)
    out = []
    step = 500
    for a in range(0, X.shape[0], step):
        S = cosine_similarity(X[a:a + step], X)
        for r, row in enumerate(S):
            i = a + r
            for j in (row > threshold - 1e-9).nonzero()[0]:
                if j > i:
                    out.append((i, int(j), float(row[j])))
    return out


def analyse_pairs(items, threshold):
    exact, near = [], []
    by = {}
    for k, it in enumerate(items):
        by.setdefault(it["sha"], []).append(k)
    for h, ks in by.items():
        if len(ks) > 1:
            exact.append({"sha256": h, "items": [{k2: items[k][k2] for k2 in ("split", "file", "line", "id")} for k in ks]})
    for i, j, s in cosine_pairs([it["text"] for it in items], threshold):
        if items[i]["sha"] == items[j]["sha"]:
            continue
        near.append({"similitud": round(s, 4),
                     "a": {k: items[i][k] for k in ("split", "file", "line", "id")},
                     "b": {k: items[j][k] for k in ("split", "file", "line", "id")}})
    return exact, near


def leaks(exact, near, items):
    """Pares de train/val/agente/p003 que coinciden (exacto o >=umbral) con test."""
    out = []
    for e in exact:
        sp = {x["split"] for x in e["items"]}
        if "test" in sp and len(sp) > 1:
            for x in e["items"]:
                if x["split"] != "test":
                    out.append({"tipo": "exacto", "similitud": 1.0, **x})
    for n in near:
        a, b = n["a"], n["b"]
        if (a["split"] == "test") != (b["split"] == "test"):
            other = b if a["split"] == "test" else a
            test = a if a["split"] == "test" else b
            out.append({"tipo": "casi", "similitud": n["similitud"], **other, "test_id": test["id"], "test_line": test["line"]})
    return out


def analyse_docs(threshold):
    docs = []
    for p in sorted((ROOT / "knowledge").rglob("*.md")):
        t = norm(p.read_text(encoding="utf-8", errors="ignore"))
        if len(t) >= 200:
            docs.append((str(p.relative_to(ROOT)), t))
    by = {}
    for f, t in docs:
        by.setdefault(sha(t), []).append(f)
    exact = [{"sha256": h, "files": fs} for h, fs in by.items() if len(fs) > 1]
    near = [{"similitud": round(s, 4), "a": docs[i][0], "b": docs[j][0]}
            for i, j, s in cosine_pairs([t for _, t in docs], threshold) if sha(docs[i][1]) != sha(docs[j][1])]
    return len(docs), exact, near


def quarantine(leak_list):
    """Mueve a data/cuarentena_leak.jsonl las copias de train/val que filtran a test. Nunca toca test."""
    targets = {}
    for l in leak_list:
        if l["split"] in ("train", "val"):
            targets.setdefault(l["split"], set()).add(l["line"])
    moved = []
    for split, lines in targets.items():
        p = DATA / f"{split}.jsonl"
        rows = p.read_text(encoding="utf-8").splitlines()
        keep = [r for i, r in enumerate(rows) if i + 1 not in lines]
        q = [r for i, r in enumerate(rows) if i + 1 in lines]
        with (DATA / "cuarentena_leak.jsonl").open("a", encoding="utf-8") as fh:
            for r in q:
                fh.write(json.dumps({"split_origen": split, "motivo": "filtracion_a_test", "par": json.loads(r)}, ensure_ascii=False) + "\n")
        p.write_text("\n".join(keep) + "\n", encoding="utf-8")
        moved.append({"split": split, "movidos": len(q)})
    return moved


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.85)
    ap.add_argument("--quarantine", action="store_true")
    ap.add_argument("--out", default=str(ROOT / f"reports/near_dup_{date.today().isoformat()}"))
    a = ap.parse_args(argv)
    test_sha = hashlib.sha256((DATA / "test.jsonl").read_bytes()).hexdigest()
    items = load_pairs()
    exact, near = analyse_pairs(items, a.threshold)
    lk = leaks(exact, near, items)
    ndocs, dexact, dnear = analyse_docs(a.threshold)
    within = lambda xs: sum(1 for n in xs if n["a"]["split"] == n["b"]["split"])
    counts = {}
    for it in items:
        counts[it["split"]] = counts.get(it["split"], 0) + 1
    moved = quarantine(lk) if a.quarantine and lk else []
    rep = {
        "meta": {"fecha": date.today().isoformat(), "autor": "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA",
                 "licencia": "CC BY 4.0", "metodo": "sha256 de texto normalizado + coseno TF-IDF char 5-gramas",
                 "umbral": a.threshold, "evidencia": "E1_analisis_textual", "herramienta": "scripts/near_dup.py (E3 software)"},
        "test_sha256": test_sha, "test_intacto": test_sha == TEST_SHA,
        "pares_por_split": counts,
        "pares": {"exactos_grupos": len(exact), "casi_total": len(near), "casi_mismo_split": within(near),
                  "casi_entre_splits": len(near) - within(near), "filtraciones_a_test": len(lk)},
        "filtraciones_a_test": lk, "cuarentena": moved,
        "docs": {"analizados": ndocs, "exactos_grupos": len(dexact), "casi": len(dnear)},
        "pares_exactos": exact, "pares_casi": near[:500], "docs_exactos": dexact, "docs_casi": dnear[:500],
    }
    Path(a.out + ".json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    md = [f"# Casi-duplicados y originalidad — {rep['meta']['fecha']}", "",
          f"Autoría: {rep['meta']['autor']}. Licencia CC BY 4.0. Evidencia de los hallazgos: E1 (análisis textual).", "",
          f"- Método: {rep['meta']['metodo']}, umbral {a.threshold}",
          f"- test.jsonl sha256 `{test_sha[:8]}…{test_sha[-5:]}` intacto: {rep['test_intacto']}",
          f"- Pares por fuente: {counts}",
          f"- Pares: grupos exactos {len(exact)}, casi-duplicados {len(near)} (mismo split {within(near)}, entre splits {len(near)-within(near)})",
          f"- **Filtraciones a test: {len(lk)}**; cuarentena: {moved or 'ninguna'}",
          f"- Docs knowledge (*.md ≥200 car.): {ndocs}; grupos exactos {len(dexact)}; casi {len(dnear)}", "",
          "## Filtraciones a test"] + [f"- {l['tipo']} {l['similitud']} {l['file']}:{l['line']}" for l in lk[:100]] + \
         ["", "## Docs casi-duplicados (top 50)"] + [f"- {d['similitud']} `{d['a']}` ~ `{d['b']}`" for d in sorted(dnear, key=lambda d: -d['similitud'])[:50]] + \
         ["", "## Docs exactos"] + [f"- {', '.join(d['files'])}" for d in dexact] + \
         ["", "Nota: similitud alta indica texto repetido (plantillas, copias internas), no plagio de terceros; revisión humana PENDIENTE DE VERIFICACIÓN."]
    Path(a.out + ".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"pares": rep["pares"], "docs": rep["docs"], "test_intacto": rep["test_intacto"], "cuarentena": moved}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
