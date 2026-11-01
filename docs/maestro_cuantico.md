# Maestro Cuántico (módulo compartido)

**Autoría:** Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA.  
**Licencia:** MIT.

## Qué es

Simulación **clásica** de circuitos cuánticos con Qiskit `Statevector` + optimizador de *simulated annealing* (`OptimizadorModular`). **No** usa hardware cuántico real ni afirma ventaja cuántica.

## Dónde vive

- Código: `app/shared/maestro_cuantico.py`
- Agente: `maestro_cuantico` (`app/agents/maestro_cuantico_agent.py`)
- Tests: `tests/test_maestro_cuantico.py`
- Aplicabilidad por proyecto: `knowledge/<proyecto>/maestro_cuantico.yaml`

## Cómo lo usan los proyectos

```python
from shared.maestro_cuantico import OptimizadorModular, optimizar_vqe, ejecutar_paralelo

# Annealing sobre cualquier función de coste
opt = OptimizadorModular({"x": (-1, 1)}, seed=1)
pos, costo = opt.optimizar(lambda p: p["x"] ** 2, max_iter=200)

# VQE con H y n_qubits arbitrarios (simulación clásica)
pos, E, opt, H = optimizar_vqe(n_qubits=2, hamiltoniano=[("ZI", 0.5), ("IZ", 0.5), ("XX", 0.3)])
```

O vía agente registrado: `maestro_cuantico` (modos `vqe` / `paralelo` / `anneal` / `info`).

## Honestidad

Cada `maestro_cuantico.yaml` indica `aplica` + `uso` o `uso: no_aplica`. Solo aplica donde VQE/annealing tienen sentido real (p. ej. ordenador híbrido, oráculo mesoscópico, cero-a, proyectos cuánticos de modelado).
