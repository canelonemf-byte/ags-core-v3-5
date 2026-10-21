#!/usr/bin/env python3
"""Integra knowledge/*/lora_pares.jsonl en data/ (idempotente, re-ejecutable a diario).
- Esquema: docs/esquema_lora_pares.md
- Control de autoría y de fuente (sin material de terceros ni PDFs) -> data/rechazados.jsonl
- Dedup exacto (id) y normalizado (sha256 de instruction+response normalizados) contra data/ existente
- Nunca mueve items existentes; fuentes nuevas -> split determinista por fuente (seed 42), SOLO train/val
- TEST CONGELADO (Opción A, 2026-10-21): nunca se añade a test; aborta si sha256(test.jsonl) != prerregistrado
- SIMULADOS (Lázaro, 2026-10-21): pares simulado=true -> data/simulados.jsonl (split_origen), nunca a train/val/test
- Reescribe data/*.jsonl solo si hay pares nuevos válidos; manifest siempre actualizado (backup en manifest_prev.json)
Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia MIT."""
import hashlib, json, re, shutil, sys, unicodedata
from datetime import datetime, timezone, timedelta
from pathlib import Path

SEED = 42
HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
DATA = HERE / "data"
AUTOR = "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA"
AUTHOR_RE = re.compile(r"^\s*L[áa]zaro\s+L[óo]pez\s+Paz\b(.*)$", re.I)
REQ_STR = ["instruction", "response", "autor", "fuente", "licencia", "proyecto"]
LIC_OK = {"mit", "cc by 4.0", "cc-by-4.0", "cc by-4.0"}
THIRD = re.compile(r"(\.pdf\b|https?://|doi\.org|arxiv|wikipedia|scholar\.google|terceros|third[_ -]?party)", re.I)
SPLITS = ("train", "val", "test")
TEST_SHA256 = "0937f06c329f1744f22570dab347aca26fa487c771356027b9bdead33e6f8ef5"  # 66 pares prerregistrados

def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    return re.sub(r"\s+", " ", s).strip()

def nhash(ins, out):
    return hashlib.sha256((norm(ins) + "\u241e" + norm(out)).encode()).hexdigest()

def split_for(src):
    h = int(hashlib.sha256(f"{SEED}:{src}".encode()).hexdigest(), 16) % 100
    if h < 80: return "train"
    if h < 90: return "val"
    # antes iba a test; test congelado -> re-hash determinista 8:1 train/val
    return "train" if int(hashlib.sha256(f"{SEED}:trainval:{src}".encode()).hexdigest(), 16) % 9 < 8 else "val"

def validate(r, proyecto_dir):
    if not isinstance(r, dict): return "no_es_objeto_json"
    for es, en in (("instruccion", "instruction"), ("respuesta", "response")):  # alias en español
        if en not in r and es in r: r[en] = r.pop(es)
    falt = [k for k in REQ_STR if not isinstance(r.get(k), str) or not r[k].strip()]
    if not isinstance(r.get("simulado"), bool): falt.append("simulado(bool)")
    if falt: return "campos_obligatorios_ausentes:" + ",".join(falt)
    if any(v is None for v in r.values()): return "contiene_null"
    m = AUTHOR_RE.match(r["autor"])
    if not m: return "autor_no_es_lazaro_lopez_paz"
    resto = m.group(1).strip(" ,;")
    if resto and not re.search(r"asistencia de (ia|inteligencia artificial)|el prat|barcelona|espa", resto, re.I):
        return "autor_con_coautores_no_permitidos"
    if THIRD.search(r["fuente"]): return "fuente_de_terceros_o_pdf"
    fp = ROOT / r["fuente"]
    if not r["fuente"].startswith(("knowledge/", "docs/")) or not fp.is_file(): return "fuente_no_existe_en_ags_core"
    if r["licencia"].strip().lower() not in LIC_OK: return "licencia_no_permitida"
    if r["proyecto"] != proyecto_dir: return "proyecto_no_coincide_con_carpeta"
    return ""

def load(sp):
    f = DATA / f"{sp}.jsonl"
    return [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []

def check_test():
    got = hashlib.sha256((DATA / "test.jsonl").read_bytes()).hexdigest()
    if got != TEST_SHA256:
        sys.exit(f"ABORTADO: sha256 de test.jsonl {got} != prerregistrado {TEST_SHA256}")

def main():
    check_test()
    now = datetime.now(timezone(timedelta(hours=2))).isoformat(timespec="minutes")
    data = {sp: load(sp) for sp in SPLITS}
    ids, hashes, src_split = set(), set(), {}
    for sp, rows in data.items():
        for x in rows:
            ids.add(x["id"]); hashes.add(nhash(x["instruction"], x["response"]))
            src_split.setdefault(x["source"], sp)
    for x in load("simulados"):  # dedup contra simulados ya apartados
        ids.add(x["id"]); hashes.add(nhash(x["instruction"], x["response"]))
    files = sorted((ROOT / "knowledge").glob("*/lora_pares.jsonl"))
    files = [f for f in files if f.parent.name != HERE.name]
    nuevos = {sp: [] for sp in SPLITS}; sim_new = []; rech = []; dup = 0; leidos = 0
    for f in files:
        proy = f.parent.name
        for i, l in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            if not l.strip(): continue
            leidos += 1
            ref = {"archivo": str(f.relative_to(ROOT)), "linea": i}
            try: r = json.loads(l)
            except Exception: rech.append({**ref, "motivo": "json_invalido"}); continue
            why = validate(r, proy)
            if why: rech.append({**ref, "motivo": why, "id_origen": str(r.get("id", "")) if isinstance(r, dict) else ""}); continue
            h = nhash(r["instruction"], r["response"])
            pid = hashlib.sha256((r["fuente"] + h).encode()).hexdigest()[:16]
            if pid in ids or h in hashes: dup += 1; continue
            sp = src_split.get(r["fuente"]) or split_for(r["fuente"])
            if sp == "test": dup += 1; continue  # fuente ya presente en test: no se añade (test congelado, sin fuga)
            row = {"id": pid, "instruction": r["instruction"], "response": r["response"], "source": r["fuente"],
                   "autor": AUTOR, "licencia": r["licencia"], "proyecto": proy, "simulado": r["simulado"], "origen": "lora_pares"}
            ids.add(pid); hashes.add(h)
            if r["simulado"] is True:
                sim_new.append({**row, "split_origen": sp}); continue
            src_split.setdefault(r["fuente"], sp)
            nuevos[sp].append(row)
    assert not nuevos["test"]
    assert all(r["simulado"] is False for v in nuevos.values() for r in v)
    n_new = sum(len(v) for v in nuevos.values())
    (DATA / "rechazados.jsonl").write_text("".join(json.dumps({**x, "fecha": now}, ensure_ascii=False) + "\n" for x in rech))
    if sim_new:
        with open(DATA / "simulados.jsonl", "a") as fh:
            fh.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in sim_new))
    if n_new:
        for sp in SPLITS:
            if nuevos[sp]:
                with open(DATA / f"{sp}.jsonl", "a") as fh:
                    fh.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in nuevos[sp]))
    man_f = DATA / "manifest.json"
    man = json.loads(man_f.read_text()) if man_f.exists() else {"meta": {"seed": SEED, "autor": AUTOR}}
    if man_f.exists(): shutil.copy2(man_f, DATA / "manifest_prev.json")
    data = {sp: load(sp) for sp in SPLITS}
    por_fuente = {}
    for sp, rows in data.items():
        for x in rows:
            d = por_fuente.setdefault(x["source"], {"split": sp, "pares": 0})
            d["pares"] += 1
    for sp in SPLITS:
        f = DATA / f"{sp}.jsonl"
        man["splits"][sp].update({"pares": len(data[sp]), "documentos": sum(1 for v in por_fuente.values() if v["split"] == sp),
                                  "sha256": hashlib.sha256(f.read_bytes()).hexdigest()})
    sim_f = DATA / "simulados.jsonl"
    sims = load("simulados")
    man["simulados"] = {"pares": len(sims), "documentos": len({x["source"] for x in sims}),
                        "sha256": hashlib.sha256(sim_f.read_bytes()).hexdigest() if sim_f.exists() else "",
                        "por_split_origen": {s: sum(1 for x in sims if x.get("split_origen") == s) for s in ("train", "val")},
                        "decision": "excluir simulados de train/val/test (Lázaro, 2026-10-21)"}
    man["archivos_sha256"] = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(DATA.glob("*.jsonl"))}
    man["total_pares"] = sum(len(v) for v in data.values())
    man["por_fuente"] = dict(sorted(por_fuente.items()))
    man["fecha"] = now
    man["ultima_fusion"] = {"fecha": now, "archivos_encontrados": [str(f.relative_to(ROOT)) for f in files],
                            "pares_leidos": leidos, "pares_nuevos": n_new, "nuevos_por_split": {k: len(v) for k, v in nuevos.items()},
                            "simulados_nuevos": len(sim_new), "duplicados": dup, "rechazados": len(rech), "datos_reescritos": bool(n_new or sim_new)}
    check_test()
    man["test_prerregistrado"] = {"sha256": TEST_SHA256, "coincide": True, "congelado": True}
    man_f.write_text(json.dumps(man, ensure_ascii=False, indent=1))
    print(json.dumps(man["ultima_fusion"], ensure_ascii=False, separators=(",", ":")))

if __name__ == "__main__":
    sys.exit(main())
