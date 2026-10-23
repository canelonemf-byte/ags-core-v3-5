# ORÁCULO MESOSCÓPICO

**PENDIENTE DE VERIFICACIÓN: sin documentos fuente.**

Nivel de evidencia: **E0** (solo nombre y alcance declarado; no hay documentos, código, datos ni referencias).

## Alcance declarado (por el usuario, 2026-10-18)
Agente de predicción probabilística y simulación mesoscópica.
Toda salida debe indicar siempre su incertidumbre, sus supuestos y sus límites.

## Estado
- Repositorio en GitHub (canelonemf-byte): no existe.
- Google Drive: no se encontró ningún documento propio de este proyecto (búsquedas «oráculo», «oraculo», «mesoscópico», «mesoscopico»; solo aparecen menciones incidentales de «oráculo» en documentos de OMNISCIENCE y HelioAtlas).
- Ordenador de trabajo: sin material fuente.

Este archivo es un marcador de posición. No contiene modelos, resultados, datos, DOI ni referencias,
y no debe citarse como evidencia. Añadir aquí los documentos fuente cuando existan.

## Módulo funcional `oraculo` (esperando datos)

oraculo: conductancia mesoscópica de Landauer, G = (2e²/h)·Σ T_n, con propagación Monte Carlo de la incertidumbre. Cada salida da media, intervalo del 95 %, supuestos y límites, que es lo que pide el alcance declarado.

`pip install -r requirements.txt && python -m pytest -q`. Los datos que faltan están en [DATOS_PENDIENTES.md](DATOS_PENDIENTES.md).
