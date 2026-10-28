#!/usr/bin/env python3
"""Automatización supervisada AGs-Core. Ciclos finitos, no bucle infinito.
Registra progreso. Para cuando no hay tareas pendientes o alcanza max_ciclos.
"""
import json
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ags_core.orchestrator import Orchestrator

MAX_CICLOS = 20
LOG = Path(__file__).parent / "auto_log.jsonl"
TAREAS = [
    "estado de proyectos",
    "produccion amoniaco 10 MW",
    "balance fusion densidad 1e20 m-3 <σv> 1e-22",
    "zeeman ODMR 10 µT",
    "ZNE 1.2 0.8 0.5",
    "plan: revisar ecosistema y proponer siguiente paso verificable",
]

def main():
    o = Orchestrator()
    log_path = LOG
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"evento": "inicio", "estado": o.estado()}, ensure_ascii=False) + "\n")
    for i in range(MAX_CICLOS):
        tarea = TAREAS[i % len(TAREAS)]
        try:
            salida = o.handle(tarea)
            entrada = {"ciclo": i, "tarea": tarea, "salida": salida[:800], "ok": True}
        except Exception as e:
            entrada = {"ciclo": i, "tarea": tarea, "error": str(e), "ok": False}
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entrada, ensure_ascii=False) + "\n")
        time.sleep(1)  # ritmo controlado
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"evento": "fin", "ciclos": MAX_CICLOS}, ensure_ascii=False) + "\n")
    print(f"Automatización terminada. Log: {log_path}")

if __name__ == "__main__":
    main()
