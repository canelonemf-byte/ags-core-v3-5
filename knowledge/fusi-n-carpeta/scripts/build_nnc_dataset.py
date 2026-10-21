#!/usr/bin/env python3
"""SOLO DISEÑO - NO EJECUTAR sin aprobación explícita de Lázaro para usar datos de NNC.
Convertiría salidas JSON de NNC (solo lectura) en pares instrucción/LLP JSON marcados simulado=true.
Salida prevista: data/nnc_{train,val,test}.jsonl + data/nnc_manifest.json (split por archivo fuente, seed 42).
No modifica NNC. El test actual (data/test.jsonl) queda congelado y no se toca."""
import argparse, hashlib, json, random, sys
from pathlib import Path
H = Path(__file__).resolve().parents[1]
NNC_DB = Path("/workspace/agsgpt/NNC/NNC/sistema-nnc-ags-core-corregido-1.0.0/nnc_system/db")
AUTOR = "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA"
GLOSARIO = "LoRA aquí = canal de radio simulado de NNC (SIMULADO_NO_CONECTADO), no Low-Rank Adaptation"

def pair(src, obj):
    datos = [f"{k}: {json.dumps(v, ensure_ascii=False)[:200]}" for k, v in list(obj.items())[:8]] if isinstance(obj, dict) else [str(obj)[:200]]
    resp = {"meta": {"proyecto": "nnc", "fuente": src.name, "autor": AUTOR, "evidencia": "E1_simulado", "simulado": True},
            "objetivo": f"Resumir estado NNC desde {src.name}", "datos_clave": datos,
            "tareas": ["revisar con datos reales antes de cualquier afirmación física"],
            "riesgos": ["datos simulados, no medidos", GLOSARIO], "decisiones": ["solo lectura de NNC"],
            "proximo_paso": "validar con fuente real"}
    return {"id": hashlib.sha256((src.name + json.dumps(obj, sort_keys=True, default=str)).encode()).hexdigest()[:16],
            "instruction": f"Genera un informe LLP JSON compacto del estado NNC (datos SIMULADOS) a partir de: {json.dumps(obj, ensure_ascii=False, default=str)[:1500]}",
            "response": json.dumps(resp, ensure_ascii=False), "simulado": True, "fuente": str(src)}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--i-have-approval", action="store_true"); a = ap.parse_args()
    if not a.i_have_approval:
        sys.exit("Bloqueado: falta aprobación del usuario para usar datos de NNC (diseño solamente).")
    files = sorted(NNC_DB.glob("*.json")); random.Random(42).shuffle(files)
    n = len(files); cut = {"train": files[: int(.8 * n)], "val": files[int(.8 * n): int(.9 * n)], "test": files[int(.9 * n):]}
    man = {"seed": 42, "simulado": True, "fuente": str(NNC_DB), "splits": {}}
    for sp, fs in cut.items():
        rows = [pair(f, json.load(open(f))) for f in fs]
        out = H / f"data/nnc_{sp}.jsonl"; txt = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
        out.write_text(txt); man["splits"][sp] = {"pares": len(rows), "archivos": [f.name for f in fs], "sha256": hashlib.sha256(txt.encode()).hexdigest()}
    json.dump(man, open(H / "data/nnc_manifest.json", "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__": main()
