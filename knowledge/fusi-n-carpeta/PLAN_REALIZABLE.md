# PLAN_REALIZABLE — fusi-n-carpeta-

Qué se puede hacer **hoy** con la ciencia y la tecnología actuales. Niveles de evidencia: E0 especulativo sin experimento · E1 declarado sin verificar · E2 simulación/cálculo reproducible · E3 medido experimentalmente y publicado con revisión por pares.

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial. ORCID: 0000-0001-8601-1963.

```yaml
meta:
  id: fusi-n-carpeta-
  fecha: "2026-10-24"
  responsable: "Lázaro López Paz"
  licencia: "ver LICENSE"
objetivo: "Carpeta de fusión: reunir las fuentes (Sarfatti citado como obra ajena, literatura revisada) y redirigir el trabajo práctico a pliegue y control-tiempo-gravedad sin duplicar"
datos_clave:
  - "El código de simulación vive en pliegue (warpcalc); aquí no se duplica."
  - "Realizable hoy (E3, por terceros): análogos de horizonte en fibra óptica (Philbin et al. 2008), agua (Weinfurtner et al. 2011) y condensados de Bose-Einstein (Steinhauer 2016); fuerza de Casimir (Lamoreaux 1997) y Casimir dinámico (Wilson et al. 2011); análogos métricos en metamateriales (Smolyaninov y Narimanov 2010)."
  - "Las propuestas de warp de baja energía con metamateriales son de Jack Sarfatti, autoeditadas, nivel E0; se citan y comentan, no se reproducen."
tareas:
  - {id: T1, tarea: "Índice de fuentes con DOI comprobados en REFERENCIAS.md", estado: hecho, evidencia: E1}
  - {id: T2, tarea: "Ficha comparativa: qué afirma Sarfatti (E0) frente a lo que miden los análogos publicados (E3)", estado: pendiente, evidencia: E1}
  - {id: T3, tarea: "Enlazar cada resultado numérico a pliegue/warpcalc en lugar de copiarlo", estado: hecho, evidencia: E1}
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
proximo_paso: "Completar T2: ficha comparativa Sarfatti (E0) frente a análogos medidos (E3)."
```

Referencias completas con DOI: [REFERENCIAS.md](REFERENCIAS.md).
