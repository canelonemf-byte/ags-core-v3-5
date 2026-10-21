#!/usr/bin/env python3
"""Genera data/sin_respuesta.jsonl: preguntas sobre proyectos LLP cuya respuesta NO está en las fuentes.
Cada pregunta solo se incluye si el patrón del dato pedido NO aparece (grep regex) en ningún archivo del proyecto.
No va a train. Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA."""
import hashlib, json, re
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]; ROOT = HERE.parents[1]
AUTOR = "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA"
ABST = "PENDIENTE DE VERIFICACIÓN: no consta en las fuentes"
EXTS = {".md", ".json", ".yaml", ".yml", ".txt", ".py"}
# (clave, plantilla de pregunta, regex que delataría que el dato SÍ está)
PLANT = [
 ("doi", "¿Cuál es el DOI de la publicación del proyecto {p}?", r"\b10\.\d{4,9}/\S+|\bdoi\b"),
 ("isbn", "¿Cuál es el ISBN del libro sobre el proyecto {p}?", r"\bisbn\b"),
 ("patente", "¿Cuál es el número de patente concedida al proyecto {p}?", r"\b(ES|EP|US|WO)\s?\d{4,}|n[úu]mero de patente|patent number"),
 ("financiacion", "¿Cuántos euros de financiación pública ha recibido el proyecto {p}?", r"\d[\d.,]*\s?(€|eur\b|euros|millones de euros)"),
 ("revista", "¿En qué revista con revisión por pares se publicó el proyecto {p} y en qué volumen?", r"\b(volumen|vol\.|journal of|physical review|nature\b|ieee trans)"),
 ("citas", "¿Cuántas citas en Google Scholar tiene el artículo del proyecto {p}?", r"\bcitas\b|\bcitations?\b|google scholar"),
 ("ensayo_clinico", "¿Cuál es el identificador NCT del ensayo clínico del proyecto {p}?", r"\bNCT\d{6,}"),
]
def main():
    out = []
    for d in sorted((ROOT / "knowledge").iterdir()):
        if not d.is_dir() or d.name in ("fusi-n-carpeta",): continue
        files = [f for f in d.rglob("*") if f.is_file() and f.suffix.lower() in EXTS and ".venv" not in f.parts]
        if not files: continue
        corpus = "\n".join(f.read_text(errors="ignore") for f in files)
        for k, q, rx in PLANT:
            if re.search(rx, corpus, re.I): continue  # el dato podría estar: no se pregunta
            pr = d.name
            out.append({"id": hashlib.sha256(f"{pr}:{k}".encode()).hexdigest()[:16], "instruction": q.format(p=pr),
                        "response": ABST, "proyecto": pr, "tipo_dato": k,
                        "fuente_verificada_ausente": {"carpeta": f"knowledge/{pr}/", "archivos_revisados": len(files),
                                                      "regex": rx, "coincidencias": 0},
                        "autor": AUTOR, "licencia": "CC BY 4.0", "simulado": False, "split": "solo_eval"})
    # máx. 2 por proyecto (objetivo 50-100), elección determinista con seed 42
    por = {}
    for x in sorted(out, key=lambda x: hashlib.sha256(f"42:{x['proyecto']}:{x['tipo_dato']}".encode()).hexdigest()):
        por.setdefault(x["proyecto"], []).append(x)
    out = [x for pr in sorted(por) for x in por[pr][:2]]
    (HERE / "data" / "sin_respuesta.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out))
    print(len(out))
if __name__ == "__main__": main()
