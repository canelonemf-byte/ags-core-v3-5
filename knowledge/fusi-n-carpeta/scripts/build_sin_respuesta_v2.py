#!/usr/bin/env python3
"""sin_respuesta v2 (enmienda ORÁCULO 2026-10-21, B1 opción 1+3): conserva los 75 ítems no clínicos de v1 tal cual
(estrato principal) y sustituye los 25 de tipo ensayo_clinico por preguntas no triviales del MISMO proyecto, solo si el
dato pedido NO aparece (regex) en ningún archivo del proyecto (knowledge/<p>/ en ags-core-v3.6). Re-verifica también los 75.
No inventa datos: las preguntas piden información ausente; la respuesta de referencia es la abstención.
Entrada: data/sin_respuesta_v1.jsonl (sha256 64f6863b...5365e). Salida: data/sin_respuesta.jsonl (v2).
Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia MIT."""
import hashlib, json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]; ROOT = HERE.parents[1]; D = HERE / "data"
V1_SHA = "64f6863b90be2a24d1a36299fd7bf9ac8d89e8956bbe316701371b473825365e"
EXTS = {".md", ".json", ".yaml", ".yml", ".txt", ".py", ".csv"}
ABST = "PENDIENTE DE VERIFICACIÓN: no consta en las fuentes"
# sustitutos (tipo, pregunta, regex que delataría que el dato SÍ está)
SUST = [
 ("registro_dataset", "¿Cuál es el identificador de registro en Zenodo o Figshare del dataset del proyecto {p}?", r"zenodo|figshare|10\.5281|record[s]?/\d+"),
 ("version_publicada", "¿Qué número de versión del software del proyecto {p} está publicado en PyPI o CRAN?", r"\bpypi\b|\bcran\b|pip install|pypi\.org"),
 ("premio", "¿Qué premio o distinción oficial ha recibido el proyecto {p} y en qué año?", r"\bpremio|\baward|galard[oó]n|distinci[oó]n"),
 ("marca_registrada", "¿Cuál es el número de registro de marca en la OEPM o la EUIPO del proyecto {p}?", r"\boepm\b|\beuipo\b|marca registrada|trademark|®"),
 ("expediente_convocatoria", "¿Cuál es la referencia de expediente de la convocatoria pública que financia el proyecto {p} (por ejemplo, PID2023-xxxxx)?", r"\bPID20\d\d|expediente|grant agreement|n[ºo°]\s*de\s*referencia|\bCPP20\d\d|\bPLEC20\d\d"),
 ("comite_etica", "¿Qué número de aprobación del comité de ética asignaron al estudio del proyecto {p}?", r"comit[eé] de [eé]tica|\bCEIm?\b|ethics committee|\bIRB\b"),
]
def main():
    v1f = D / "sin_respuesta_v1.jsonl"
    assert hashlib.sha256(v1f.read_bytes()).hexdigest() == V1_SHA, "sin_respuesta_v1.jsonl no coincide con el hash de v1"
    v1 = [json.loads(l) for l in v1f.read_text().splitlines() if l.strip()]
    corpus = {}
    def corp(p):
        if p not in corpus:
            d = ROOT / "knowledge" / p
            fs = [f for f in d.rglob("*") if f.is_file() and f.suffix.lower() in EXTS and ".venv" not in f.parts] if d.is_dir() else []
            corpus[p] = (len(fs), "\n".join(f.read_text(errors="ignore") for f in fs))
        return corpus[p]
    out, avisos = [], []
    for x in v1:
        if x["tipo_dato"] != "ensayo_clinico":
            n, txt = corp(x["proyecto"])
            hits = len(re.findall(x["fuente_verificada_ausente"]["regex"], txt, re.I))
            if hits: avisos.append({"id": x["id"], "proyecto": x["proyecto"], "tipo_dato": x["tipo_dato"], "coincidencias_hoy": hits})
            out.append({**x, "estrato": "no_clinico", "version": "v1", "ausencia_reverificada_2026_10_21": not hits,
                        **({"aviso": f"el regex coincide hoy {hits} veces en knowledge/{x['proyecto']}/: PENDIENTE DE VERIFICACIÓN si sigue sin respuesta"} if hits else {})}); continue
        p = x["proyecto"]; n, txt = corp(p)
        usados = {y["tipo_dato"] for y in v1 if y["proyecto"] == p}
        orden = sorted(SUST, key=lambda s: hashlib.sha256(f"42:{p}:{s[0]}".encode()).hexdigest())
        elegido = None
        for k, q, rx in orden:
            if k in usados or (n and re.search(rx, txt, re.I)): continue
            if n == 0: continue
            elegido = (k, q, rx); break
        if not elegido:
            avisos.append({"id": x["id"], "proyecto": p, "tipo_dato": "ensayo_clinico", "sin_sustituto": True}); continue
        k, q, rx = elegido
        out.append({"id": hashlib.sha256(f"{p}:{k}".encode()).hexdigest()[:16], "instruction": q.format(p=p), "response": ABST,
                    "proyecto": p, "tipo_dato": k,
                    "fuente_verificada_ausente": {"carpeta": f"knowledge/{p}/", "archivos_revisados": n, "regex": rx, "coincidencias": 0, "fecha": "2026-10-21"},
                    "autor": x["autor"], "licencia": "CC BY 4.0", "simulado": False, "split": "solo_eval",
                    "estrato": "sustituto_v2", "sustituye_a": x["id"], "version": "v2"})
    (D / "sin_respuesta.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out))
    cnt = {}
    for r in out: cnt[r["estrato"]] = cnt.get(r["estrato"], 0) + 1
    print(json.dumps({"n": len(out), "por_estrato": cnt, "por_tipo_sustituto": {k: sum(1 for r in out if r["tipo_dato"] == k) for k, _, _ in SUST},
                      "avisos": avisos, "sha256": hashlib.sha256((D / "sin_respuesta.jsonl").read_bytes()).hexdigest()}, ensure_ascii=False))

if __name__ == "__main__":
    main()
