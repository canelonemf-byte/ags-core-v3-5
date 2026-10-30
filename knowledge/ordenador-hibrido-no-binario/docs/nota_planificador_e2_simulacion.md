# Nota UCS — planificador E2 (simulación, no experimento)

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España + asistencia IA. Licencia CC BY 4.0. Fecha: 2026-10-30.

Esta nota documenta la **simulación** `sim/planificador.py` del proyecto ordenador-hibrido-no-binario.

- Tipo: **simulación** (nivel E2). **No es un experimento** ni una medida de hardware.
- Compara HEFT con un planificador consciente de error y coste de conversión ADC/DAC sobre un DAG sintético.
- El modelo de coste usa tablas de `sim/sim_mvm.py`, cuyos parámetros en `parametros.yaml` son **supuestos**.
- En la corrida con semilla 20261030, el planificador consciente respeta umbrales de error y puede gastar más energía modelada que HEFT al forzar CMOS.
- Propuesta de diseño del planificador: E0 (adaptación sobre literatura HEFT/CIM). Prototipo: E2 simulación.

No ingerir `sim/salidas/*.json` como experimento.
