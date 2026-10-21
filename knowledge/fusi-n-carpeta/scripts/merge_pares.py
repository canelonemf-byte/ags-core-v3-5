#!/usr/bin/env python3
"""Integra knowledge/*/lora_pares.jsonl en data/ (idempotente, re-ejecutable a diario).
- Esquema: docs/esquema_lora_pares.md
- Control de autoría y de fuente (sin material de terceros ni PDFs) -> data/rechazados.jsonl
- Dedup exacto (id) y normalizado (sha256 de instruction+response normalizados) contra data/ existente
- Nunca mueve items existentes; fuentes nuevas -> split determinista por fuente (seed 42), SOLO train/val
- TEST CONGELADO (Opción A, 2026-10-21): nunca se añade a test; aborta si sha256(test.jsonl) != prerregistrado
- SIMULADOS (Lázaro, 2026-10-21): pares simulado=true -> data/simulados.jsonl (split_origen), nunca a train/val/test
- NEAR-DUP (2026-10-21): Jaccard de shingles de 5 caracteres (Python puro) >= 0.85 contra train/val/test/simulados -> rechazado near_dup (test siempre)
- RETIRADOS: data/retirados.jsonl (par completo + motivo) se copia a rechazados.jsonl en cada ejecución
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
    if not resolve_fuente(r["fuente"]): return "fuente_no_existe"
    if r["licencia"].strip().lower() not in LIC_OK: return "licencia_no_permitida"
    if r["proyecto"] != proyecto_dir: return "proyecto_no_coincide_con_carpeta"
    return ""

NEAR_DUP = 0.85
SHINGLE_K = 5

def shingles(ins, out, k=SHINGLE_K):
    t = norm(ins) + " \u241e " + norm(out)
    return {t[i:i + k] for i in range(max(1, len(t) - k + 1))}

def jaccard(a, b):
    if not a or not b: return 0.0
    i = len(a & b)
    return i / (len(a) + len(b) - i)

def best_match(sh, index):
    """index: lista de (id, split, shingles). Devuelve (sim, id, split) del más parecido; prefiltro por tamaño."""
    best = (0.0, "", "")
    n = len(sh)
    for pid, sp, other in index:
        m = len(other)
        if min(n, m) / max(n, m) < NEAR_DUP: continue  # cota: J <= min/max
        j = jaccard(sh, other)
        if j > best[0] or (sp == "test" and j >= NEAR_DUP and best[2] != "test"): best = (j, pid, sp)
    return best

WS = Path("/workspace")

def resolve_fuente(f):
    """2026-10-21: quita #fragmento; absoluta -> debe estar bajo /workspace; relativa -> prueba ags-core-v3.6/ y luego /workspace/."""
    f = f.split("#", 1)[0].strip()
    if not f: return None
    p = Path(f)
    cands = [p] if p.is_absolute() else [ROOT / p, WS / p]
    for c in cands:
        try: c = c.resolve()
        except Exception: continue
        if c.is_file() and (c.is_relative_to(WS)): return c
    return None

# 2026-10-21 (Lázaro): rutas alternativas de documentos de test -> se tratan como test (nunca train/val)
ALIAS_TEST = {"knowledge/ordenador-hibrido-no-binario/docs/Estudio_viabilidad_arquitectura_hibrida_revisado.docx.md":
              "knowledge/ordenador-hibrido-no-binario/drive/Estudio_viabilidad_arquitectura_hibrida_revisado.md"}
DOC_DUP = 0.85  # Jaccard de shingles del documento completo frente a documentos fuente de test

def doc_shingles(path):
    p = resolve_fuente(path)
    if not p: return set()
    t = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", p.read_text(errors="ignore")).lower())
    return {t[i:i + 9] for i in range(0, max(1, len(t) - 8))}

def load(sp):
    f = DATA / f"{sp}.jsonl"
    return [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []

def check_test():
    got = hashlib.sha256((DATA / "test.jsonl").read_bytes()).hexdigest()
    if got != TEST_SHA256:
        sys.exit(f"ABORTADO: sha256 de test.jsonl {got} != prerregistrado {TEST_SHA256}")

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="no escribe nada; solo cuenta")
    ap.add_argument("--input", action="append", default=[], help="lora_pares.jsonl extra (proyecto = carpeta padre); implica revisión")
    a = ap.parse_args()
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
    rf = DATA / "test_ampliado_reserva.json"  # enmienda ORÁCULO 2026-10-21: documentos reservados para test_ampliado
    reservados = set(json.loads(rf.read_text())["datos_clave"]["documentos_reservados"]) if rf.exists() else set()
    test_docs = {s for s, sp in src_split.items() if sp == "test"}
    _tdsh = {}
    _cache = {}
    def es_doc_de_test(fuente):
        """True si la fuente es alias de un documento de test o su contenido coincide (Jaccard >= DOC_DUP) con uno."""
        f = fuente.split("#", 1)[0]
        if f in test_docs or ALIAS_TEST.get(f) in test_docs: return True
        if f not in _cache:
            sh = doc_shingles(f); _cache[f] = False
            if sh:
                for td in test_docs:
                    if td not in _tdsh: _tdsh[td] = doc_shingles(td)
                    o = _tdsh[td]
                    if o and min(len(sh), len(o)) / max(len(sh), len(o)) >= DOC_DUP and jaccard(sh, o) >= DOC_DUP:
                        _cache[f] = True; break
        return _cache[f]
    for x in load("test_ampliado"):
        ids.add(x["id"]); hashes.add(nhash(x["instruction"], x["response"])); src_split.setdefault(x["source"], "test")
    index = [(x["id"], "test_ampliado", shingles(x["instruction"], x["response"])) for x in load("test_ampliado")]
    index += [(x["id"], sp, shingles(x["instruction"], x["response"])) for sp, rows in data.items() for x in rows]
    index += [(x["id"], "simulados", shingles(x["instruction"], x["response"])) for x in load("simulados")]
    orig = {}
    files = sorted((ROOT / "knowledge").glob("*/lora_pares.jsonl"))
    files = [f for f in files if f.parent.name != HERE.name]
    if a.input: files = [Path(x).resolve() for x in a.input]
    rel = lambda f: str(f.relative_to(ROOT)) if f.is_relative_to(ROOT) else str(f)
    nuevos = {sp: [] for sp in SPLITS}; sim_new = []; rech = []; dup = 0; leidos = 0
    for f in files:
        proy = f.parent.name
        o = orig.setdefault(proy, {"leidos": 0, "aceptados": 0, "simulados": 0, "dup_exacto": 0, "near_dup": 0, "rechazados_esquema": 0})
        for i, l in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            if not l.strip(): continue
            leidos += 1; o["leidos"] += 1
            ref = {"archivo": rel(f), "linea": i}
            try: r = json.loads(l)
            except Exception: rech.append({**ref, "motivo": "json_invalido"}); o["rechazados_esquema"] += 1; continue
            why = validate(r, proy)
            if why: o["rechazados_esquema"] += 1; rech.append({**ref, "motivo": why, "id_origen": str(r.get("id", "")) if isinstance(r, dict) else ""}); continue
            if r["fuente"].split("#", 1)[0] not in src_split and es_doc_de_test(r["fuente"]):
                o["rechazados_esquema"] += 1
                rech.append({**ref, "motivo": "fuente_es_documento_de_test", "id_origen": str(r.get("id", ""))}); continue
            if r["fuente"].split("#", 1)[0] in reservados:
                o["rechazados_esquema"] += 1
                rech.append({**ref, "motivo": "fuente_reservada_test_ampliado", "id_origen": str(r.get("id", ""))}); continue
            h = nhash(r["instruction"], r["response"])
            pid = hashlib.sha256((r["fuente"] + h).encode()).hexdigest()[:16]
            if pid in ids or h in hashes: dup += 1; o["dup_exacto"] += 1; continue
            sh = shingles(r["instruction"], r["response"])
            j, mid, msp = best_match(sh, index)
            if j >= NEAR_DUP:  # incluye siempre near-dups de test
                o["near_dup"] += 1
                rech.append({**ref, "motivo": "near_dup", "id_origen": str(r.get("id", "")), "id_coincidente": mid,
                             "split_coincidente": msp, "jaccard": round(j, 4)}); continue
            sp = src_split.get(r["fuente"]) or split_for(r["fuente"])
            if sp == "test": dup += 1; o["dup_exacto"] += 1; continue  # fuente ya presente en test: no se añade (test congelado, sin fuga)
            row = {"id": pid, "instruction": r["instruction"], "response": r["response"], "source": r["fuente"],
                   "autor": AUTOR, "licencia": r["licencia"], "proyecto": proy, "simulado": r["simulado"], "origen": "lora_pares"}
            ids.add(pid); hashes.add(h)
            if r["simulado"] is True:
                index.append((pid, "simulados", sh)); o["simulados"] += 1
                sim_new.append({**row, "split_origen": sp}); continue
            index.append((pid, sp, sh)); o["aceptados"] += 1
            src_split.setdefault(r["fuente"], sp)
            nuevos[sp].append(row)
    assert not nuevos["test"]
    assert all(r["simulado"] is False for v in nuevos.values() for r in v)
    n_new = sum(len(v) for v in nuevos.values())
    if a.dry_run:
        print(json.dumps({"dry_run": True, "archivos": [rel(f) for f in files], "por_agente": orig,
                          "aceptarian_por_split": {k: len(v) for k, v in nuevos.items()}, "simulados": len(sim_new),
                          "rechazos": [{k: x[k] for k in x if k != "fecha"} for x in rech]}, ensure_ascii=False, indent=1))
        return 0
    # retirados manuales aprobados (p. ej. near_dup_cross_split 2026-10-21) se conservan en rechazados en cada ejecución
    ret = [{k: v for k, v in x.items() if k != "par"} for x in load("retirados")]
    (DATA / "rechazados.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in ret + rech))
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
    for extra in ("test_prerregistro.json", "test_ampliado_reserva.json", "test_ampliado_prerregistro.json"):
        if (DATA / extra).exists(): man["archivos_sha256"][extra] = hashlib.sha256((DATA / extra).read_bytes()).hexdigest()
    sr = load("sin_respuesta")
    man["sin_respuesta"] = {"version": "v2" if any(x.get("version") == "v2" for x in sr) else "v1", "n": len(sr),
                            "por_estrato": {k: sum(1 for x in sr if x.get("estrato", "global") == k) for k in sorted({x.get("estrato", "global") for x in sr})},
                            "v1_sha256": "64f6863b90be2a24d1a36299fd7bf9ac8d89e8956bbe316701371b473825365e"}
    man["total_pares"] = sum(len(v) for v in data.values())
    man["por_fuente"] = dict(sorted(por_fuente.items()))
    man["fecha"] = now
    man["ultima_fusion"] = {"fecha": now, "archivos_encontrados": [rel(f) for f in files],
                            "pares_leidos": leidos, "pares_nuevos": n_new, "nuevos_por_split": {k: len(v) for k, v in nuevos.items()},
                            "simulados_nuevos": len(sim_new), "duplicados": dup, "rechazados": len(rech), "datos_reescritos": bool(n_new or sim_new)}
    check_test()
    man["test_prerregistrado"] = {"sha256": TEST_SHA256, "coincide": True, "congelado": True}
    tot = {k: sum(v[k] for v in orig.values()) for k in ("leidos", "aceptados", "simulados", "dup_exacto", "near_dup", "rechazados_esquema")}
    (DATA / "originalidad.json").write_text(json.dumps({
        "meta": {"fecha": now[:10], "autor": AUTOR, "licencia": "CC BY 4.0", "metodo": f"jaccard_shingles_{SHINGLE_K}_caracteres_python_puro", "umbral": NEAR_DUP},
        "objetivo": "medir originalidad de pares de agentes frente a train/val/test/simulados",
        "datos_clave": {"por_agente": dict(sorted(orig.items())), "total": tot},
        "tareas": [], "riesgos": ["shingles de caracteres no detectan paráfrasis semánticas"],
        "decisiones": ["near_dup >= 0.85 -> rechazados.jsonl con id_coincidente; near-dup de test siempre rechazado"],
        "proximo_paso": "revisar rechazados near_dup con cada agente"}, ensure_ascii=False, separators=(",", ":")))
    man_f.write_text(json.dumps(man, ensure_ascii=False, indent=1))
    print(json.dumps(man["ultima_fusion"], ensure_ascii=False, separators=(",", ":")))

if __name__ == "__main__":
    sys.exit(main())
