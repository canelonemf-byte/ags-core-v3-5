# PLAN_REALIZABLE — pliegue

Qué se puede hacer **hoy** con la ciencia y la tecnología actuales. Niveles de evidencia: E0 especulativo sin experimento · E1 declarado sin verificar · E2 simulación/cálculo reproducible · E3 medido experimentalmente y publicado con revisión por pares.

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial. ORCID: 0000-0001-8601-1963.

```yaml
meta:
  id: pliegue
  fecha: "2026-10-24"
  responsable: "Lázaro López Paz"
  licencia: "ver LICENSE"
objetivo: "Laboratorio numérico verificable de métricas warp: reproducir con código y tests la energía negativa, la condición NEC y las cotas cuánticas"
datos_clave:
  - "Realizable hoy (E2): warpcalc reproduce la densidad de energía analítica de Alcubierre (1994, ec. 19) con error mediano <2 % en la malla de test, y la de Natário (2002) con divergencia nula."
  - "Los datos declarados en P001 (ANEC -0,08, QI ~10^50, Casimir ~10^60) siguen sin código que los genere: se marcan E1 hasta reproducirlos."
  - "No realizable hoy (E0): construir una burbuja; exige energía negativa ~10^43 J o más y paredes de ~10^2 longitudes de Planck (Pfenning y Ford 1997)."
tareas:
  - {id: T1, tarea: "Paquete warpcalc (Alcubierre, Natário, cota Pfenning-Ford) con 6 tests", estado: hecho, evidencia: E2}
  - {id: T2, tarea: "Integral ANEC y verificación de las cifras de P001 (examples/verificar_p001.py, results/verificacion_p001.json)", estado: hecho, evidencia: E2}
  - {id: T3, tarea: "Añadir métrica de White (2011, informe técnico NASA) solo si se encuentra la forma funcional publicada", estado: pendiente, evidencia: E0}
  - {id: T4, tarea: "Comparar con análogos de laboratorio publicados (Barceló et al. 2011; Philbin 2008; Steinhauer 2016)", estado: pendiente, evidencia: E3}
riesgos:
  - id: R1
    riesgo: "confundir un análogo de laboratorio con un motor warp real"
    mitigacion: "todo análogo se describe como modelo matemático equivalente, no como curvatura real del espacio-tiempo"
  - id: R2
    riesgo: "atribuir ideas de Sarfatti como propias"
    mitigacion: "toda idea de Sarfatti se cita en REFERENCIAS.md y NOTICE.md como obra suya, nivel E0"
  - id: R3
    riesgo: "cifras de costes o materiales inventadas"
    mitigacion: "no se dan costes sin fuente; se añadirán solo con presupuesto o cita verificable"
decisiones:
  - "Las afirmaciones extraordinarias no se borran: se etiquetan como hipótesis E0 con su cita."
  - "No se suben PDF de terceros; solo citas y resúmenes propios."
  - "Costes y materiales: solo con fuente; de momento el trabajo realizable es computacional (ordenador personal, Python + numpy)."
proximo_paso: "Pedir al autor los parámetros (v, R, sigma, rayo, separación de placas) usados para ANEC -0,08, QI 1e50 y Casimir 1e60."
```

Referencias completas con DOI: [REFERENCIAS.md](REFERENCIAS.md).
