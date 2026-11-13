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

## Corrida de supervisión (rutinas 9:00 / 13:00 / 18:00)

```bash
cd /workspace/agsgpt/ags-core-v3.6 && /workspace/agsgpt/.venv/bin/python scripts/maestro_supervision.py --seed 42
```

Ejecuta el agente `maestro_cuantico` (VQE, hamiltoniano demo de 2 qubits) dos veces con la misma semilla y reescribe en sitio `knowledge/ordenador-hibrido-no-binario/maestro_cuantico_ultima_corrida.json` y `knowledge/oraculo-mesoscopico/maestro_cuantico_ultima_corrida.json` (LLP). Evidencia siempre `E2_simulacion_propia` (en la escala de ORDENADOR HÍBRIDO, E3 es literatura citada). La reproducibilidad va en el campo aparte `verificacion_software`: `reproducible_misma_semilla` si las dos corridas coinciden; si no, `no_reproducible` y código de salida 1. El hamiltoniano demo no es un modelo físico de esos proyectos; es simulación clásica, no hardware cuántico.
