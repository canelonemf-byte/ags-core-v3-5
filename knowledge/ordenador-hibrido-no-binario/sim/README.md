# sim/ — MVM y planificador (E2 simulación, no experimento)

**Nivel de evidencia: E2 (simulación propia, no experimento, no reproducida por terceros).**

## MVM (`sim_mvm.py`)
- `parametros.yaml`: todos los parámetros siguen marcados `supuesto` tras intento t6 (2026-10-30): Horowitz doi:10.1109/isscc.2014.6757323 y Andrulis arXiv:2404.06553 verificados en existencia, sin valor sustituible limpio.
- Ejecutar: `python3 sim_mvm.py` (numpy, pyyaml). Semilla 20261020.
- `salidas/resultados.csv|json`: error relativo y energía por configuración.

## Planificador (`planificador.py`) — t7
- Prototipo mínimo: HEFT clásico vs planificador consciente de error + coste de conversión, usando las tablas de `salidas/resultados.csv` como modelo de coste sobre un DAG sintético.
- Semilla fija; salidas en `salidas/planificador_*.json|csv`. Test: `test_planificador.py`.
- La **propuesta de diseño** sigue E0; esta corrida es **E2 simulación** con supuestos explícitos (DAG sintético, latencias supuestos, tablas MVM con parámetros supuestos).

## Limitaciones del modelo MVM
Sin no linealidades del dispositivo, IR-drop, deriva, variabilidad ciclo a ciclo, ni tiling; ADC lineal en bits; el ahorro energético es consecuencia de los supuestos, no una predicción.
