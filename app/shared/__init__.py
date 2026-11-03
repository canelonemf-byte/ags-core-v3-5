"""Módulos compartidos de AGs-Core (reutilizables por todos los proyectos)."""

from . import metrics

try:
    from .maestro_cuantico import (
        OptimizadorModular,
        crear_ansatz,
        crear_hamiltoniano_demo,
        hacer_funcion_costo,
        energia_exacta,
        optimizar_vqe,
        worker_vqe,
        ejecutar_paralelo,
    )
except ImportError:  # qiskit/numpy no siempre están en el venv de cada app
    OptimizadorModular = None  # type: ignore
    crear_ansatz = None  # type: ignore
    crear_hamiltoniano_demo = None  # type: ignore
    hacer_funcion_costo = None  # type: ignore
    energia_exacta = None  # type: ignore
    optimizar_vqe = None  # type: ignore
    worker_vqe = None  # type: ignore
    ejecutar_paralelo = None  # type: ignore

__all__ = [
    "OptimizadorModular",
    "crear_ansatz",
    "crear_hamiltoniano_demo",
    "hacer_funcion_costo",
    "energia_exacta",
    "optimizar_vqe",
    "worker_vqe",
    "ejecutar_paralelo",
    "metrics",
]
