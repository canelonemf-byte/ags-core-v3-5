#!/usr/bin/env python3
"""Control de contaminación (enmienda ORÁCULO 2026-10-21): solapamiento de n-gramas de palabras (n=13 por defecto)
entre conjuntos de evaluación (test, test_ampliado, sin_respuesta) y entrenamiento (train, val).
Se informa en bruto y "sin plantilla": se quita la instrucción fija, la autoría y las claves LLP (con cortes para que no haya
n-gramas a caballo) y además los n-gramas presentes en >= --umbral-plantilla de los ítems de train+val.
Solo lectura de data/; escribe results/contaminacion.json. No compara con datos de preentrenamiento (PENDIENTE DE VERIFICACIÓN).
Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia MIT."""
import argparse, collections, hashlib, json, re, unicodedata
from pathlib import Path
H = Path(__file__).resolve().parents[1]; D = H / "data"

def toks(s):
    s = unicodedata.normalize("NFKC", s).lower()
    return re.findall(r"\w+", s)

def ngrams(t, n):
    return {" ".join(t[i:i + n]) for i in range(len(t) - n + 1)}

AUTOR = "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA"
LLP_KEYS = re.compile(r'"(meta|fuente|seccion|autor|evidencia|objetivo|datos_clave|tareas|riesgos|decisiones|proximo_paso)"\s*:')

def contenido(x):
    """Texto sin plantilla: la nota tras 'NOTA:' y la respuesta sin autoría ni claves LLP; los cortes impiden n-gramas a caballo."""
    ins = x["instruction"].split("NOTA:", 1)[-1]
    resp = LLP_KEYS.sub(" \x00 ", x.get("response", "").replace(AUTOR, " \x00 "))
    return [seg for seg in (ins + " \x00 " + resp).split("\x00") if seg.strip()]

def ngrams_contenido(x, n):
    return set().union(*[ngrams(toks(seg), n) for seg in contenido(x)] or [set()])

def load(name):
    f = D / f"{name}.jsonl"
    return [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=13); ap.add_argument("--umbral-plantilla", type=float, default=0.01)
    a = ap.parse_args(); n = a.n
    ref_rows = load("train") + load("val")
    ref_ng = [ngrams(toks(x["instruction"] + " " + x["response"]), n) for x in ref_rows]
    df = collections.Counter(g for s in ref_ng for g in s)
    plantilla = {g for g, c in df.items() if c >= a.umbral_plantilla * len(ref_rows)}
    allref = set(df)
    ref_c = set().union(*[ngrams_contenido(x, n) for x in ref_rows])
    out = {"meta": {"fecha": "2026-10-21", "autor": "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA",
                    "licencia": "CC BY 4.0", "metodo": f"{n}-gramas de palabras (NFKC, minúsculas)", "referencia": "train+val",
                    "n_referencia": len(ref_rows), "ngramas_plantilla_excluidos": len(plantilla), "umbral_plantilla": a.umbral_plantilla,
                    "sha256": {f: hashlib.sha256((D / f).read_bytes()).hexdigest() for f in ("train.jsonl", "val.jsonl")}},
           "objetivo": "detectar solapamiento literal entre evaluación y entrenamiento", "datos_clave": {}, "tareas": [],
           "riesgos": ["no detecta paráfrasis ni contaminación del preentrenamiento de Qwen/Mistral (PENDIENTE DE VERIFICACIÓN)"],
           "decisiones": ["solo informe; no se mueve ningún ítem"], "proximo_paso": "revisar ítems con solapamiento sin plantilla > 0"}
    for name in ("test", "test_ampliado", "sin_respuesta"):
        rows = load(name)
        if not rows: continue
        res = []
        for x in rows:
            g = ngrams(toks(x["instruction"] + " " + x.get("response", "")), n)
            bruto = g & allref; gc = ngrams_contenido(x, n); neto = (gc & ref_c) - plantilla
            res.append({"id": x["id"], "fuente": x.get("source", x.get("proyecto", "")), "ngramas": len(g), "comunes_bruto": len(bruto),
                        "ngramas_contenido": len(gc), "comunes_sin_plantilla": len(neto),
                        "frac_sin_plantilla": round(len(neto) / len(gc), 4) if gc else 0.0})
        con = [r for r in res if r["comunes_sin_plantilla"] > 0]
        out["datos_clave"][name] = {"n": len(rows), "items_con_solape_bruto": sum(r["comunes_bruto"] > 0 for r in res),
                                    "items_con_solape_sin_plantilla": len(con),
                                    "items_frac_sin_plantilla_ge_0_5": sum(r["frac_sin_plantilla"] >= 0.5 for r in res),
                                    "max_frac_sin_plantilla": max((r["frac_sin_plantilla"] for r in res), default=0.0),
                                    "detalle_con_solape": sorted(con, key=lambda r: -r["frac_sin_plantilla"])[:20]}
    (H / "results" / "contaminacion.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "detalle_con_solape"} for k, v in out["datos_clave"].items()}, ensure_ascii=False))

if __name__ == "__main__":
    main()
