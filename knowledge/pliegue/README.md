# PLIEGUE (P001)

Laboratorio de simulación de métricas warp (ficha P001, 2026-09-15, en knowledge/llp_pack/proyectos/P001.json de AGs-Core).

- Objetivo declarado: rayo NEC, toro T00 y desigualdad de Ford-Roman; métricas de Alcubierre, Natario y White.
- Datos clave declarados: ANEC en la pared -0,08 (viola), T00 nulo en el eje del toro, QI de Alcubierre ~10^50, Casimir ~10^60, violación de NEC/WEC/DEC, geodésica nula k=0 con Δ≪R.
- Riesgo anotado: el empuje transversal es invisible si Δ≪R.
- Evidencia: E2 para lo que calcula `warpcalc` (con tests); E1 para las cifras de P001 que aún no reproduce el código.
- Teoría de terceros: métricas de Alcubierre, Natario y White; desigualdades cuánticas de Ford-Roman (referencias exactas con DOI en [REFERENCIAS.md](REFERENCIAS.md)).
- Licencia: MIT (ver LICENSE).

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial. ORCID: 0000-0001-8601-1963.

## Estado científico
- Establecido (teoría revisada por pares): métricas de Alcubierre (1994) y Natário (2002); desigualdades cuánticas de Ford-Roman (1995, 1996). Indican que una burbuja warp exige energía negativa en cantidades enormes.
- Especulativo (E0): propuestas de Jack Sarfatti de «warp de baja energía» con metamateriales (2014, 2020). Son obra de Sarfatti, no de este proyecto; ver REFERENCIAS.md.

## Código
`warpcalc/`: densidad de energía euleriana de Alcubierre (analítica y numérica) y Natário, energía total, cota de Pfenning-Ford. `pip install -e .[test] && pytest`; ejemplo: `python examples/energia_burbuja.py`. Plan: [PLAN_REALIZABLE.md](PLAN_REALIZABLE.md).
