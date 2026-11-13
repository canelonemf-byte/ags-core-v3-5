#!/usr/bin/env python3
"""Corrida de supervisión del Maestro Cuántico (punto de entrada para rutinas 9:00 / 13:00 / 18:00).

Ejecuta el agente registrado ``maestro_cuantico`` (app/agents/maestro_cuantico_agent.py,
que usa app/shared/maestro_cuantico.py) en modo VQE con semilla fija, DOS veces, comprueba
reproducibilidad y reescribe en sitio knowledge/<proyecto>/maestro_cuantico_ultima_corrida.json
(formato LLP, snake_case, sin null).

Honestidad:
- Simulación CLÁSICA (Qiskit Statevector). No es hardware cuántico ni prueba ventaja cuántica.
- El único hamiltoniano que el código soporta hoy sin datos externos es el demo de 2 qubits
  (0.5·ZI + 0.5·IZ + 0.3·XX). No es un modelo físico de ORDENADOR HÍBRIDO ni de ORÁCULO;
  la corrida verifica que el optimizador compartido funciona y es reproducible.
- Evidencia: siempre E2_simulacion_propia (simulación propia; en la escala de ORDENADOR HÍBRIDO
  E3 es literatura citada). La reproducibilidad va aparte en verificacion_software:
  "reproducible_misma_semilla" o "no_reproducible" (código de salida 1). Nunca E4+.

Uso:
    /workspace/agsgpt/.venv/bin/python scripts/maestro_supervision.py \
        --proyecto ordenador-hibrido-no-binario --proyecto oraculo-mesoscopico --seed 42

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA.
Licencia: MIT.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
PROYECTOS = ("ordenador-hibrido-no-binario", "oraculo-mesoscopico")
SALIDA = "maestro_cuantico_ultima_corrida.json"
AUTORIA = "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA"
EVIDENCIA = "E2_simulacion_propia"
BACKEND_TXT = "qiskit Statevector (simulación clásica, no hardware cuántico)"
CODIGO = (
    "app/shared/maestro_cuantico.py",
    "app/agents/maestro_cuantico_agent.py",
    "scripts/maestro_supervision.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sin_null(obj: Any) -> Any:
    """LLP: nunca null (dict/list vacíos se mantienen; None -> "")."""
    if obj is None:
        return ""
    if isinstance(obj, dict):
        return {k: _sin_null(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sin_null(v) for v in obj]
    return obj


def _leer_aplicabilidad(proyecto: str) -> dict:
    import yaml  # pyyaml está en requirements.txt

    yml = ROOT / "knowledge" / proyecto / "maestro_cuantico.yaml"
    if not yml.is_file():
        raise FileNotFoundError(f"falta {yml.relative_to(ROOT)}")
    data = (yaml.safe_load(yml.read_text(encoding="utf-8")) or {}).get("maestro_cuantico", {})
    if data.get("aplica") is not True:
        raise ValueError(f"{proyecto}: maestro_cuantico.yaml no declara aplica: true")
    if data.get("es_hardware_cuantico") is not False:
        raise ValueError(f"{proyecto}: maestro_cuantico.yaml debe declarar es_hardware_cuantico: false")
    return data


def ejecutar_agente(seed: int, max_iter: int) -> dict:
    """Una corrida VQE vía el agente registrado (sin LLM)."""
    if str(APP) not in sys.path:
        sys.path.insert(0, str(APP))
    import agents  # noqa: F401  registra maestro_cuantico
    from registry import get_agent

    out = asyncio.run(
        get_agent("maestro_cuantico").run(
            "vqe supervision", context={"modo": "vqe", "seed": seed, "max_iter": max_iter}
        )
    )
    if out.get("status") != "ok":
        raise RuntimeError(str(out.get("output")))
    return out["data"]


def construir_llp(proyecto: str, uso: str, seed: int, max_iter: int,
                  r1: dict, r2: dict, fecha: str) -> dict:
    reproducible = (
        r1["energia"] == r2["energia"]
        and r1["params"] == r2["params"]
        and r1["iteraciones"] == r2["iteraciones"]
    )
    evidencia = EVIDENCIA
    verificacion = "reproducible_misma_semilla" if reproducible else "no_reproducible"
    shas = {c: _sha256(ROOT / c) for c in CODIGO}
    return _sin_null({
        "meta": {
            "proyecto": proyecto,
            "fecha": fecha,
            "zona": "Europe/Madrid",
            "autoria": AUTORIA,
            "licencia": "MIT (código); CC BY 4.0 (este registro)",
            "agente": "maestro_cuantico",
            "script": "scripts/maestro_supervision.py",
            "backend": BACKEND_TXT,
            "es_hardware_cuantico": False,
            "evidencia": evidencia,
            "verificacion_software": verificacion,
            "sha256_codigo": shas,
        },
        "objetivo": (
            "Verificar en cada supervisión que el optimizador compartido (VQE + simulated "
            "annealing) funciona y es reproducible con semilla fija, como optimizador de "
            f"parámetros declarado para este proyecto (uso: {uso})."
        ),
        "datos_clave": {
            "caso": "hamiltoniano_demo_2q",
            "hamiltoniano": [["ZI", 0.5], ["IZ", 0.5], ["XX", 0.3]],
            "caso_nota": "hamiltoniano de demostración; no es un modelo físico del proyecto",
            "semilla": seed,
            "max_iter": max_iter,
            "n_qubits": r1["n_qubits"],
            "energia_obtenida": r1["energia"],
            "energia_referencia_exacta": r1["energia_exacta"],
            "metodo_referencia": "diagonalización densa numpy.linalg.eigvalsh",
            "energia_referencia_analitica": -math.sqrt(1.09),
            "error_abs": r1["error_abs"],
            "iteraciones": r1["iteraciones"],
            "parametros": r1["params"],
            "reproducible_semilla": reproducible,
            "corrida_2_energia": r2["energia"],
            "corrida_2_iteraciones": r2["iteraciones"],
        },
        "tareas": [],
        "riesgos": [
            "simulación clásica statevector: no es hardware cuántico ni demuestra ventaja cuántica",
            "el caso es el hamiltoniano demo de 2 qubits; falta un hamiltoniano o función de coste "
            "del proyecto con fuente verificable",
        ],
        "decisiones": [
            f"evidencia {evidencia} (simulación propia); verificacion_software {verificacion}: "
            + ("dos corridas con la misma semilla dan resultado idéntico" if reproducible
               else "las dos corridas no coinciden; código de salida 1"),
            "no se marca como resultado del proyecto ni E4+",
        ],
        "proximo_paso": (
            "Sustituir el hamiltoniano demo por una función de coste del proyecto cuando exista "
            "con fuente verificable (decisión de Lázaro)."
        ),
    })


def escribir_en_sitio(destino: Path, data: dict) -> None:
    """Reescribe el fichero en el mismo sitio (escritura atómica, sin copias ni .bak)."""
    texto = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(dir=destino.parent, prefix=f".{destino.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(texto)
        os.chmod(tmp, 0o644)
        os.replace(tmp, destino)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--proyecto", action="append", choices=PROYECTOS,
                    help="repetible; por defecto ambos")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--max-iter", type=int, default=800)
    ap.add_argument("--no-escribir", action="store_true", help="solo imprime el resultado")
    args = ap.parse_args(argv)
    proyectos = args.proyecto or list(PROYECTOS)

    usos = {p: str(_leer_aplicabilidad(p).get("uso", "")) for p in proyectos}
    r1 = ejecutar_agente(args.seed, args.max_iter)
    r2 = ejecutar_agente(args.seed, args.max_iter)
    fecha = datetime.now(ZoneInfo("Europe/Madrid")).isoformat(timespec="seconds")

    ok = True
    for p in proyectos:
        llp = construir_llp(p, usos[p], args.seed, args.max_iter, r1, r2, fecha)
        dk = llp["datos_clave"]
        ok = ok and dk["reproducible_semilla"]
        destino = ROOT / "knowledge" / p / SALIDA
        if not args.no_escribir:
            escribir_en_sitio(destino, llp)
        print(json.dumps({
            "proyecto": p,
            "energia": dk["energia_obtenida"],
            "referencia_exacta": dk["energia_referencia_exacta"],
            "error_abs": dk["error_abs"],
            "iteraciones": dk["iteraciones"],
            "reproducible": dk["reproducible_semilla"],
            "evidencia": llp["meta"]["evidencia"],
            "verificacion_software": llp["meta"]["verificacion_software"],
            "fichero": "" if args.no_escribir else str(destino.relative_to(ROOT)),
        }, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
