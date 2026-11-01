"""Agente Maestro Cuántico: VQE / annealing compartido para todos los proyectos.

Ejecuta simulación CLÁSICA (Qiskit Statevector), no hardware cuántico.
Sin LLM: resultados numéricos reales o estado degradado si falta qiskit.

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España,
con asistencia de inteligencia artificial. MIT.
"""
from __future__ import annotations

import asyncio
import math
from typing import Any, Optional

from base_agent import BaseAgent
from registry import register

_IMPORT_ERROR: Optional[str] = None
try:
    from shared.maestro_cuantico import (
        NOTA_HARDWARE,
        BACKEND,
        ES_SIMULACION_CLASICA,
        OptimizadorModular,
        crear_hamiltoniano_demo,
        energia_exacta,
        optimizar_vqe,
        ejecutar_paralelo,
    )
except ImportError as exc:  # pragma: no cover
    _IMPORT_ERROR = str(exc)
    NOTA_HARDWARE = "dependencia no disponible"
    BACKEND = ""
    ES_SIMULACION_CLASICA = True
    OptimizadorModular = None  # type: ignore
    crear_hamiltoniano_demo = None  # type: ignore
    energia_exacta = None  # type: ignore
    optimizar_vqe = None  # type: ignore
    ejecutar_paralelo = None  # type: ignore


def _parse_int(context: dict, key: str, default: int) -> int:
    v = context.get(key, default)
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _run_sync(task: str, context: dict[str, Any]) -> dict[str, Any]:
    """Ejecución síncrona: vqe | paralelo | anneal | info."""
    modo = str(context.get("modo") or context.get("mode") or "").lower()
    task_l = (task or "").lower()
    if not modo:
        if "paralelo" in task_l or "parallel" in task_l:
            modo = "paralelo"
        elif "anneal" in task_l or "optimiza" in task_l or "coste" in task_l:
            modo = "anneal"
        else:
            modo = "vqe"

    if modo == "info":
        return {
            "modo": "info",
            "backend": BACKEND,
            "es_simulacion_clasica": ES_SIMULACION_CLASICA,
            "nota": NOTA_HARDWARE,
        }

    if modo == "anneal":
        # Función de coste de prueba acotada (no inventa resultados de proyectos).
        # El llamador puede pasar context["funcion_coste_nombre"]="esfera" únicamente.
        seed = _parse_int(context, "seed", 7)
        max_iter = _parse_int(context, "max_iter", 200)

        def esfera(p: dict) -> float:
            return sum(v * v for v in p.values())

        lim = {"x": (-2.0, 2.0), "y": (-2.0, 2.0)}
        opt = OptimizadorModular(lim, seed=seed, patience=40, t0=0.4, cooling=0.96)
        pos, costo = opt.optimizar(esfera, max_iter=max_iter)
        return {
            "modo": "anneal",
            "funcion_coste": "esfera_demo",
            "mejor_posicion": pos,
            "mejor_costo": costo,
            "iteraciones": opt.iteracion,
            "nota": "demo OptimizadorModular; pasa tu propia función desde código Python",
        }

    if modo == "paralelo":
        semillas = context.get("semillas") or [42, 123, 777, 999, 1024]
        if isinstance(semillas, str):
            semillas = [int(x) for x in semillas.replace(";", ",").split(",") if x.strip()]
        max_iter = _parse_int(context, "max_iter", 400)
        out = ejecutar_paralelo(semillas=list(semillas), max_iter=max_iter)
        return out

    # modo vqe (default)
    seed = _parse_int(context, "seed", 42)
    max_iter = _parse_int(context, "max_iter", 800)
    n_qubits = context.get("n_qubits")
    n_qubits_i = int(n_qubits) if n_qubits is not None else None
    reps = _parse_int(context, "reps", 1)
    # Hamiltoniano arbitrario: lista de [pauli, coef] en context["hamiltoniano"]
    H = None
    raw_h = context.get("hamiltoniano")
    if isinstance(raw_h, list) and raw_h:
        H = [(str(t[0]), float(t[1])) for t in raw_h]
    pos, E, opt, H_obj = optimizar_vqe(
        seed=seed,
        max_iter=max_iter,
        n_qubits=n_qubits_i,
        hamiltoniano=H,
        reps=reps,
    )
    e_ex = energia_exacta(H_obj)
    return {
        "modo": "vqe",
        "energia": E,
        "energia_exacta": e_ex,
        "error_abs": abs(E - e_ex),
        "n_qubits": H_obj.num_qubits,
        "iteraciones": opt.iteracion,
        "params": pos,
        "backend": BACKEND,
        "es_simulacion_clasica": ES_SIMULACION_CLASICA,
        "nota": NOTA_HARDWARE,
        "demo_esperado_2q": -math.sqrt(1.09) if H_obj.num_qubits == 2 and H is None else None,
    }


@register
class MaestroCuanticoAgent(BaseAgent):
    """VQE / simulated annealing compartido (simulación clásica statevector)."""

    name = "maestro_cuantico"
    domain = "compute"
    description = (
        "Maestro Cuántico compartido: VQE (statevector) y OptimizadorModular "
        "(simulated annealing). Simulación clásica, no hardware cuántico."
    )
    preferred_model = "local_tools"
    fallback_models: list = []

    @property
    def system_prompt(self) -> str:
        return (
            "Agente determinista Maestro Cuántico. "
            "Simulación clásica Qiskit Statevector; no finge hardware cuántico."
        )

    async def run(self, task: str, context: dict[str, Any] | None = None):
        ctx = dict(context or {})
        if _IMPORT_ERROR:
            return {
                "agent": self.name,
                "domain": self.domain,
                "model_used": "",
                "output": f"[maestro_cuantico degradado: {_IMPORT_ERROR}]",
                "status": "degraded",
                "evidencia": "E0_degradado",
                "es_evidencia": False,
            }
        try:
            data = await asyncio.to_thread(_run_sync, task, ctx)
            # Texto legible sin inventar cifras
            if data.get("modo") == "vqe":
                out = (
                    f"VQE simulación clásica ({data['backend']}): "
                    f"E={data['energia']:+.6f} exacta={data['energia_exacta']:+.6f} "
                    f"error={data['error_abs']:.6f} qubits={data['n_qubits']} "
                    f"iter={data['iteraciones']}. {data['nota']}"
                )
            elif data.get("modo") == "paralelo":
                m = data["mejor"]
                out = (
                    f"Paralelo {data['n_workers']} semillas en {data['tiempo_total_s']:.2f}s; "
                    f"mejor seed={m['semilla']} E={m['energia']:+.6f} "
                    f"exacta={m['energia_exacta']:+.6f} error={m['error']:.6f}. {data['nota']}"
                )
            elif data.get("modo") == "anneal":
                out = (
                    f"Annealing demo esfera: costo={data['mejor_costo']:.6f} "
                    f"iter={data['iteraciones']} pos={data['mejor_posicion']}"
                )
            else:
                out = str(data.get("nota") or data)
            return {
                "agent": self.name,
                "domain": self.domain,
                "model_used": "maestro_cuantico_local",
                "output": out,
                "data": data,
                "status": "ok",
                "evidencia": "E2_simulacion_propia",
                "es_evidencia": True,
                "es_simulacion_clasica": True,
            }
        except Exception as exc:  # noqa: BLE001
            return {
                "agent": self.name,
                "domain": self.domain,
                "model_used": "",
                "output": f"[maestro_cuantico error: {type(exc).__name__}: {exc}]",
                "status": "error",
                "evidencia": "E0_error",
                "es_evidencia": False,
            }
