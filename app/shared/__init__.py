"""Módulos compartidos de AGs-Core (reutilizables por todos los proyectos)."""

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

__all__ = [
    "OptimizadorModular",
    "crear_ansatz",
    "crear_hamiltoniano_demo",
    "hacer_funcion_costo",
    "energia_exacta",
    "optimizar_vqe",
    "worker_vqe",
    "ejecutar_paralelo",
]
