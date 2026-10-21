#!/usr/bin/env python3
"""Métrica m4: tasa_alucinacion = % de respuestas que NO se abstienen ante data/sin_respuesta.jsonl.
Uso: python3 scripts/eval_sin_respuesta.py --pred results/pred_sin_respuesta_<modelo>.jsonl  (líneas {"id","output"})
m4 por estrato (enmienda ORÁCULO 2026-10-21; principal no_clinico n=75). Solo puntúa predicciones; no carga modelos. Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA."""
import argparse, json, re
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
ABST_RE = re.compile(r"pendiente de verificaci[oó]n|no consta|no figura|no aparece en las fuentes|no (lo )?s[eé]\b|no dispongo|sin datos|desconocid", re.I)

def es_abstencion(texto):
    return bool(ABST_RE.search(texto or ""))

def tasa_alucinacion(outputs):
    """outputs: lista de strings. Devuelve % (0-100) de no abstenciones."""
    if not outputs: return 0.0
    return round(100.0 * sum(not es_abstencion(o) for o in outputs) / len(outputs), 2)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--pred", required=True); a = ap.parse_args()
    rows = [json.loads(l) for l in open(HERE / "data/sin_respuesta.jsonl") if l.strip()]
    ref = {r["id"] for r in rows}
    estr = {r["id"]: r.get("estrato", "global") for r in rows}
    pred = {}
    for l in open(a.pred):
        if l.strip(): r = json.loads(l); pred[r["id"]] = r.get("output", "")
    outs = [pred.get(i, "") for i in sorted(ref)]  # sin predicción = no abstención
    # enmienda ORÁCULO 2026-10-21: m4 por estrato; principal = "no_clinico" (n=75)
    por = {}
    for i in sorted(ref): por.setdefault(estr[i], []).append(pred.get(i, ""))
    res = {"n": len(ref), "n_pred": len(set(pred) & ref), "tasa_alucinacion_global": tasa_alucinacion(outs),
           "por_estrato": {k: {"n": len(v), "tasa_alucinacion": tasa_alucinacion(v)} for k, v in sorted(por.items())},
           "m4_principal": {"estrato": "no_clinico", **({"n": len(por["no_clinico"]), "tasa_alucinacion": tasa_alucinacion(por["no_clinico"])} if "no_clinico" in por else {})}}
    print(json.dumps(res, ensure_ascii=False, separators=(",", ":")))

if __name__ == "__main__": main()
