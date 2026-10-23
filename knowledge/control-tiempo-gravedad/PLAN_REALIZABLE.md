# PLAN_REALIZABLE — control-tiempo-gravedad

Qué se puede hacer **hoy** con la ciencia y la tecnología actuales. Niveles de evidencia: E0 especulativo sin experimento · E1 declarado sin verificar · E2 simulación/cálculo reproducible · E3 medido experimentalmente y publicado con revisión por pares.

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial. ORCID: 0000-0001-8601-1963.

```yaml
meta:
  id: control-tiempo-gravedad
  fecha: "2026-10-24"
  responsable: "Lázaro López Paz"
  licencia: "ver LICENSE"
objetivo: "Medir y simular hoy los efectos reales del tiempo y la gravedad (dilatación temporal gravitacional) y cuantificar por qué el «control del tiempo» (hipótesis E0) no es realizable"
datos_clave:
  - "Realizable hoy (E3): la dilatación temporal gravitacional se mide en laboratorio con relojes ópticos: 33 cm (Chou et al. 2010, doi:10.1126/science.1192720) y escala milimétrica (Bothwell et al. 2022, doi:10.1038/s41586-021-04349-7)."
  - "Realizable hoy (E2, simulación): warpcalc calcula la energía negativa de Alcubierre y Natário; con v=0,1c y R=100 m sale del orden de -10^43 a -10^44 J (examples/energia_burbuja.py)."
  - "No realizable hoy (E0): «control del tiempo», retrocausalidad e información del futuro; las desigualdades cuánticas (Ford y Roman 1995; Pfenning y Ford 1997) lo impiden con la física conocida."
tareas:
  - {id: T1, tarea: "Paquete warpcalc con tests (densidad de energía euleriana, cota de Pfenning-Ford, corrimiento gravitacional)", estado: hecho, evidencia: E2}
  - {id: T2, tarea: "Calculadora de dilatación temporal: GPS, relojes ópticos a distintas alturas, comparar con Chou 2010", estado: en_curso, evidencia: E2}
  - {id: T3, tarea: "Barrido de parámetros (v, R, sigma) y gráfica energía vs grosor de pared frente a la cota cuántica", estado: pendiente, evidencia: E2}
  - {id: T4, tarea: "Reescribir el informe como divulgación: qué es medible (E3), qué es simulación (E2) y qué es hipótesis (E0)", estado: hecho, evidencia: E1}
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
proximo_paso: "Completar T2: calculadora de dilatación temporal comparada con Chou 2010."
```

Referencias completas con DOI: [REFERENCIAS.md](REFERENCIAS.md).
