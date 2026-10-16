"""ags_local: motor local de AGs-Core (herramientas físicas deterministas + AGsGPT/LoRA).

Procede de ags_core 3.0.0 (Lázaro López Paz). Se eliminó el acoplamiento con la
app radar (ciclo/_mejoras/_digest). Ver NOTICE para atribuciones de model.py.
"""
from .engine import LocalEngine, get_engine

__all__ = ["LocalEngine", "get_engine"]
