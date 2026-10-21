#!/usr/bin/env python3
"""Diseño de test_ampliado (enmienda ORÁCULO 2026-10-21). NO modifica data/test.jsonl (congelado, 0937f06c...8ef5).
Candidatos: documentos propios (mismas reglas que build_dataset.py) NO usados en train/val/test/simulados/retirados,
excluyendo knowledge/nnc (uso no aprobado) y documentos de incidente; se descartan ítems near-dup (Jaccard >= 0.85) o con
cualquier 13-grama de contenido en común con train/val/test/simulados, y los documentos con algún ítem descartado.
Sin --congelar: escribe data/test_ampliado_reserva.json (documentos reservados; merge_pares no los asigna a train/val).
Con --congelar --n N (solo tras piloto y aprobación de Lázaro): escribe data/test_ampliado.jsonl + test_ampliado_prerregistro.json.
Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia MIT."""
import argparse, collections, hashlib, json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import build_dataset as b, merge_pares as m, contaminacion as c
EXCL = ("knowledge/nnc", "knowledge/RECUPERACION", "knowledge/fusi-n-carpeta")

def candidatos():
    used = {x["source"] for n in ("train", "val", "test", "simulados") for x in m.load(n)} | {x["par"]["source"] for x in m.load("retirados")}
    cands = []
    for base in ("knowledge", "docs"):
        for p in sorted((b.ROOT / base).rglob("*")):
            if not p.is_file() or p.suffix.lower() not in b.EXTS or "fusi-n-carpeta" in p.parts or ".venv" in p.parts: continue
            src = str(p.relative_to(b.ROOT))
            if src in used or src.startswith(EXCL): continue
            t = p.read_text(errors="ignore")
            if not b.authored(p, t): continue
            cs = b.chunks_md(t) if p.suffix == ".md" else ([("archivo", t[:1500])] if len(t) >= 200 else [])
            for title, ch in cs:
                cands.append({"id": hashlib.sha256((src + title + ch).encode()).hexdigest()[:16], "instruction": b.INSTR + ch,
                              "response": json.dumps(b.to_llp(title, ch, src), ensure_ascii=False, separators=(",", ":")), "source": src})
    ref = [x for n in ("train", "val", "test", "simulados") for x in m.load(n)]
    refsh = [m.shingles(x["instruction"], x["response"]) for x in ref]
    refng = set().union(*[c.ngrams_contenido(x, 13) for x in ref])
    motivo = collections.Counter(); malos = set(); ok = []
    for x in cands:
        sh = m.shingles(x["instruction"], x["response"])
        if any(min(len(sh), len(o)) / max(len(sh), len(o)) >= m.NEAR_DUP and m.jaccard(sh, o) >= m.NEAR_DUP for o in refsh):
            motivo["near_dup"] += 1; malos.add(x["source"]); continue
        if c.ngrams_contenido(x, 13) & refng:
            motivo["solape_13gram"] += 1; malos.add(x["source"]); continue
        ok.append(x)
    ok = [x for x in ok if x["source"] not in malos]
    return cands, ok, motivo, malos

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--congelar", action="store_true"); ap.add_argument("--n", type=int, default=0); a = ap.parse_args()
    cands, ok, motivo, malos = candidatos()
    proy = collections.Counter(x["source"].split("/")[1] if x["source"].startswith("knowledge/") else "docs" for x in ok)
    docs = sorted({x["source"] for x in ok})
    if a.congelar:
        if not a.n or a.n > len(ok): sys.exit(f"n inválido: disponibles {len(ok)}")
        sel = sorted(ok, key=lambda x: hashlib.sha256(f"42:{x['id']}".encode()).hexdigest())[:a.n]
        f = m.DATA / "test_ampliado.jsonl"
        if f.exists(): sys.exit("test_ampliado.jsonl ya existe: congelado, no se sobrescribe")
        f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in sel))
        (m.DATA / "test_ampliado_prerregistro.json").write_text(json.dumps({"test_ampliado_sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
            "pares": len(sel), "documentos": len({x["source"] for x in sel}), "fecha": __import__("datetime").date.today().isoformat(), "autor": m.AUTOR}, ensure_ascii=False))
        print("congelado", len(sel)); return
    res = {"meta": {"fecha": "2026-10-21", "autor": m.AUTOR, "licencia": "CC BY 4.0", "estado": "PENDIENTE: diseño, no congelado"},
           "objetivo": "reservar documentos no usados para un test_ampliado prerregistrado tras el piloto",
           "datos_clave": {"items_candidatos_brutos": len(cands), "descartes": dict(motivo), "documentos_descartados": len(malos),
                           "items_disponibles": len(ok), "documentos_disponibles": len(docs), "items_por_proyecto": dict(proy.most_common()),
                           "documentos_reservados": docs},
           "tareas": ["piloto para medir discordancia", "elegir n con scripts/estadistica.py --n-potencia", "aprobación de Lázaro antes de --congelar"],
           "riesgos": ["concentración por proyecto: no representativo del test original"],
           "decisiones": ["merge_pares.py no asigna a train/val pares cuya fuente esté en documentos_reservados"],
           "proximo_paso": "piloto"}
    (m.DATA / "test_ampliado_reserva.json").write_text(json.dumps(res, ensure_ascii=False, separators=(",", ":")))
    print(json.dumps({k: v for k, v in res["datos_clave"].items() if k != "documentos_reservados"}, ensure_ascii=False))

if __name__ == "__main__":
    main()
