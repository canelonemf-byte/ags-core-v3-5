#!/usr/bin/env python3
"""Corrección aprobada por Lázaro (2026-10-21): retira de sin_respuesta v2 el ítem dd86ea20047a5c33 (DOI de remplast-q;
su regex coincide hoy en knowledge/remplast-q/) y lo sustituye por la plantilla v1 'isbn' del mismo proyecto (estrato no_clinico)
solo si su regex v1 no coincide en ningún archivo de knowledge/remplast-q/ (extensiones v1 y v2). Idempotente.
Nota de retirada en data/sin_respuesta_retirados.jsonl.
Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia MIT."""
import hashlib, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import build_sin_respuesta as v1
HERE = Path(__file__).resolve().parents[1]; D = HERE / "data"
RET_ID, PROY, TIPO = "dd86ea20047a5c33", "remplast-q", "isbn"
EXTS = v1.EXTS | {".csv", ".txt"}

def main():
    f = D / "sin_respuesta.jsonl"; rows = [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
    retf = D / "sin_respuesta_retirados.jsonl"
    ret = [json.loads(l) for l in retf.read_text().splitlines() if l.strip()] if retf.exists() else []
    out = [r for r in rows if r["id"] != RET_ID]; viejo = [r for r in rows if r["id"] == RET_ID]
    if viejo and not any(x["id"] == RET_ID for x in ret):
        ret.append({"id": RET_ID, "motivo": "dato_presente_en_fuentes", "fecha": "2026-10-21",
                    "detalle": "regex doi coincide 189 veces en knowledge/remplast-q/ (fuentes_cc_by)", "decision": "Lázaro 2026-10-21", "item": viejo[0]})
    k, q, rx = next(t for t in v1.PLANT if t[0] == TIPO)
    d = v1.ROOT / "knowledge" / PROY
    fs = [p for p in d.rglob("*") if p.is_file() and p.suffix.lower() in EXTS and ".venv" not in p.parts]
    hits = len(re.findall(rx, "\n".join(p.read_text(errors="ignore") for p in fs), re.I))
    nid = hashlib.sha256(f"{PROY}:{k}".encode()).hexdigest()[:16]
    añadido = False
    if hits == 0 and not any(r["id"] == nid for r in out):
        out.append({"id": nid, "instruction": q.format(p=PROY), "response": v1.ABST, "proyecto": PROY, "tipo_dato": k,
                    "fuente_verificada_ausente": {"carpeta": f"knowledge/{PROY}/", "archivos_revisados": len(fs), "regex": rx, "coincidencias": 0, "fecha": "2026-10-21"},
                    "autor": v1.AUTOR, "licencia": "CC BY 4.0", "simulado": False, "split": "solo_eval",
                    "estrato": "no_clinico", "version": "v2", "sustituye_a": RET_ID, "ausencia_reverificada_2026_10_21": True}); añadido = True
    out.sort(key=lambda r: (r["proyecto"], r["id"]))
    f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    retf.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in ret))
    cnt = {}
    for r in out: cnt[r["estrato"]] = cnt.get(r["estrato"], 0) + 1
    print(json.dumps({"n": len(out), "por_estrato": cnt, "sustituto": nid if hits == 0 else "", "coincidencias_regex": hits, "archivos": len(fs),
                      "añadido_en_esta_ejecucion": añadido, "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}, ensure_ascii=False))

if __name__ == "__main__":
    main()
