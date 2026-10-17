> Texto extraído automáticamente del PDF original «OMNISCIENCE_Documento_Maestro_2026.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1qje3TY76kodva2Mleeab0XATIzBi95vt/view?usp=drivesdk



OMNISCIENCE
Universal Autonomous Scientific Discovery Engine

Documento maestro integral de arquitectura, ciencia computacional, IA, cuántica, materiales,

biología, energía, fusión, experimentación y gobernanza

Lázaro López Paz
España

Agosto de 2026

Resumen

OMNISCIENCE es una arquitectura federada para descubrimiento científico asistido por
inteligencia artificial. Su objetivo es convertir problemas abiertos en campañas científicas repro-
ducibles: recuperar evidencia, formular hipótesis falsables, generar predicciones cuantitativas,
ejecutar simulaciones, buscar activamente refutaciones, priorizar experimentos por valor de
información, registrar procedencia y, cuando exista infraestructura autorizada, cerrar el ciclo
mediante experimentación y réplica independiente.
La plataforma integra ciencia de materiales, vibraciones atómicas y fonones, estructura
electrónica, química computacional, metamateriales, fotónica, óptica, superconductividad, sen-
sores cuánticos, dinámica cuántica abierta, computación cuántica híbrida, biología molecular,
biomateriales, descubrimiento terapéutico, energía, almacenamiento, agua, medio ambiente,
agricultura, ingeniería, robótica, gemelos digitales y fusión. La arquitectura no presupone
que una IA, una QPU o un modelo concreto sea superior para todos los problemas: selec-
ciona métodos por complejidad, incertidumbre, coste, reproducibilidad y valor esperado de
información.
El núcleo inicial recomendado es OMNISCIENCE-MV1, Universal Matter + Vibrational
Discovery Platform, seguido por un motor de dinámica cuántica abierta y por diseño inverso
de materiales. El proyecto se diseña alrededor de la separación entre generación y verificación,
la trazabilidad de extremo a extremo y la supervisión humana en actividades físicas de riesgo.

Índice

1. Resumen ejecutivo 2

2. Alcance y límites 2

3. Principios epistemológicos 2

4. Niveles de evidencia 2

5. Arquitectura de alto nivel 3

1

OMNISCIENCE Documento maestro 2026

6. Capa de datos y conocimiento 4

7. Arquitectura multiagente 4

7.1. Agentes generadores . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4

7.2. Agentes verificadores . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4

7.3. Agente de orquestación . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4

8. Universal Matter Engine 4

9. Universal Vibrational and Phonon Engine 5

10.Mapa vibracional universal 5

11.Estructura electrónica y química cuántica 5

12.Quantum Dynamics Engine 5

13.Quantum Computing Engine 6

14.Quantum Sensing Engine 6

15.Metamaterial and Metasurface Engine 6

16.Photonic Engine 6

17.Superconductivity Engine 6

18.Chemical Discovery Engine 7

19.Energy Engine 7

20.Fusion Materials and Digital Twin Engine 7

21.Biology and Biomaterials Engine 7

22.Therapeutic Discovery Engine 7

23.Environmental Engine 8

24.Water Engine 8

25.Agriculture and Food Engine 8

26.Aerospace and Extreme Materials Engine 8

27.AI Scientist Engine 8

28.Innovation Radar 8

29.Diseño inverso universal 8

2

OMNISCIENCE Documento maestro 2026

30.Optimización bayesiana y búsqueda activa 9

31.Valor esperado de información 9

32.Estadística e incertidumbre 9

33.Falsación adversarial 9

34.Réplicas independientes 9

35.Active Experiment Design 10

36.Laboratorio autónomo y robótica 10

37.Digital Twins 10

38.Provenance y reproducibilidad 10

39.Auditoría bibliográfica 10

40.Seguridad y gobernanza 11

40.1. Permitido inicialmente . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11

40.2. Revisión humana obligatoria . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11

41.Arquitectura de software 11

42.Esquema mínimo de una campaña 11

43.Algoritmo maestro 12

44.Plan de implementación 13

44.1. Fase 0: infraestructura . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

44.2. Fase 1: MV1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

44.3. Fase 2: Quantum Dynamics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

44.4. Fase 3: diseño inverso . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

44.5. Fase 4: multiagente . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

44.6. Fase 5: radar interdisciplinario . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

44.7. Fase 6: experimentación autorizada . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

44.8. Fase 7: gemelos digitales . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

45.Métricas de éxito 13

46.Riesgos científicos 14

47.Mitigaciones 14

3

OMNISCIENCE Documento maestro 2026

48.Ejemplos de campañas científicas 14

48.1. Material térmico . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14

48.2. Material fotónico . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14

48.3. Catalizador . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14

48.4. Sensor cuántico . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15

48.5. Fusión . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15

48.6. Biomaterial . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15

49.Principio de descubrimiento universal 15

50.Conclusión general 15

4

OMNISCIENCE Documento maestro 2026

1. Resumen ejecutivo

La hipótesis arquitectónica de OMNISCIENCE es que el mayor potencial no procede de un

único modelo de inteligencia artificial, sino de una red de modelos especializados coordinados por

un protocolo científico común. El sistema debe ser capaz de preguntar qué se sabe, qué no se sabe,
qué predicción discrimina entre hipótesis, qué simulación es suficiente, qué experimento aporta

más información y qué resultado podría demostrar que la hipótesis es incorrecta.

La unidad de trabajo es una campaña:

P → H → M → S → F → E → R → K → H ′

con P problema, H hipótesis, M modelo, S simulación, F falsación, E experimento autorizado, R

réplica y K conocimiento actualizado.

2. Alcance y límites

OMNISCIENCE pretende abarcar cualquier rama científica en la medida en que pueda forma-

lizarse como problema de conocimiento, modelado, observación, optimización o experimentación.
Esto no significa que todo problema sea resoluble, ni que exista una representación única de la

realidad, ni que la IA pueda sustituir la validación humana.

El sistema debe distinguir entre: idea, hipótesis, predicción, simulación, observación, réplica y

conocimiento consolidado. Una salida de IA no constituye por sí misma evidencia científica.

3. Principios epistemológicos

1. Toda hipótesis importante debe ser falsable.

2. Los criterios de falsación se fijan antes de observar el resultado siempre que sea posible.

3. Generación y verificación deben estar separadas.

4. Las incertidumbres deben acompañar a los resultados.

5. La reproducibilidad forma parte del resultado, no es un añadido posterior.

6. Las afirmaciones científicas deben vincularse a evidencia identificable.

7. Las predicciones computacionales no se presentan como hechos experimentales.

8. Las decisiones de alto impacto requieren revisión humana.

4. Niveles de evidencia

Nivel Estado Definición

0 Idea Concepto sin evaluación formal.

5

OMNISCIENCE Documento maestro 2026

1 Hipótesis Propuesta explícita y falsable.

2 Predicción Resultado derivado de un modelo o algoritmo.

3 Simulación reproducible Resultado que puede repetirse bajo condiciones docu-

mentadas.

4 Observación experimen-

tal
 Medición documentada con incertidumbre.

5 Réplica independiente Confirmación mediante una ruta metodológica inde-

pendiente.

6 Evidencia convergente Varias líneas independientes apuntan al mismo resul-

tado.

7 Conocimiento consolida-

do
 Resultado robusto, replicado y con límites conocidos.

5. Arquitectura de alto nivel

OMNISCIENCE

|

+---------------+---------------+

| |

META-CIENCIA GOBERNANZA

| |

+---------+---------+ Etica / Seguridad

| | | Auditoria / Humanos

Evidencia Modelos Datos Acceso / Trazabilidad

| | |

+---------+---------+

|

ORQUESTADOR CIENTIFICO

|

+------+------+------+------+------+------+------+------+

| | | | | | | | |

Materia Fonon Quantum Quimica Bio Meta Energia Fusion IA

| | | | | | | | |

+------+------+------+------+------+------+------+------+

|

SIMULACION / OPTIMIZACION

|

FALSACION ADVERSARIAL

|

EXPERIMENTO AUTORIZADO

|

REPLICA

|
 6

OMNISCIENCE Documento maestro 2026

GRAFO DE CONOCIMIENTO

|

NUEVA CAMPAÑA

6. Capa de datos y conocimiento

El sistema debe mantener un grafo de conocimiento que conecte entidades científicas, fuentes,

modelos, simulaciones, experimentos y resultados. La procedencia puede representarse mediante

W3C PROV/PROV-O y empaquetarse mediante RO-Crate, que permite describir datos, software,

equipos, personas, workflows y contexto de producción. [1, 2, 3]
Cada afirmación tendrá un registro mínimo: identificador, texto, dominio, fuente, fecha de
recuperación, identificador persistente, evidencia asociada, nivel de evidencia, incertidumbre y

estado de revisión.

7. Arquitectura multiagente

7.1. Agentes generadores

Físicos, químicos, materiales, matemáticos, biólogos, ingenieros, especialistas en IA y agentes

de síntesis interdisciplinaria.

7.2. Agentes verificadores

Un verificador independiente reconstruye el cálculo; un falsador intenta producir contraejemplos;

un agente estadístico revisa incertidumbres; un agente bibliográfico busca literatura contradictoria;

un agente experimental diseña pruebas discriminantes.

7.3. Agente de orquestación

El orquestador decide qué agente debe intervenir, con qué datos, qué método debe utilizarse y

cuándo un resultado puede avanzar de nivel de evidencia.

8. Universal Matter Engine

Este motor representa composición, estructura, energía, estabilidad, defectos, superficies,

interfaces y propiedades.
 Eform = Etotal − ∑

i niµi

Ehull = Eform − Econvex hull.

Debe incorporar estructuras cristalinas, amorfas, nanoestructuras y fases metastables cuando los

modelos utilizados sean adecuados.
 7

OMNISCIENCE Documento maestro 2026

9. Universal Vibrational and Phonon Engine

La vibración de una especie atómica no es una propiedad aislada: depende del entorno, enlace,

masa, simetría, temperatura, presión y estado electrónico. Por ello el sistema debe explorar modos

normales y colectivos, no una supuesta frecuencia única de cada elemento.

Dij
αβ(q) = 1
√mimj
 ∑

R Φij
αβ(R)eiq·R

D(q)eν(q) = ω2
ν(q)eν(q).

El flujo de fonones puede implementarse mediante desplazamientos finitos o constantes de fuerza,

tal como documenta Phonopy. [4]

Se estudiarán densidad de estados fonónica, dispersión, velocidades de grupo, tiempos de vida,

anharmonicidad, fonón-fonón, electrón-fonón, espín-fonón, transporte térmico y modos localizados.

κL = 1
3
 ∑

ν Cνv2
ντν.

10. Mapa vibracional universal

Para cada estructura se almacenará una firma:

V = {ω, e, q, τ, C, v, S, g, T, P }

que permita buscar materiales con patrones vibracionales similares o propiedades objetivo.
Se explorarán relaciones entre vibración y estabilidad, transporte térmico, movilidad iónica,

catálisis, óptica, magnetismo, superconductividad, respuesta mecánica y propiedades emergentes.

11. Estructura electrónica y química cuántica

El sistema podrá combinar DFT, métodos post-DFT y aproximaciones específicas según el

problema. Ningún funcional será considerado universal. Las convergencias deberán tratar energía

de corte, malla de puntos k, tamaño de celda, tolerancias de fuerza, magnetismo y otros parámetros

relevantes.
Para problemas adecuados se podrá utilizar Quantum ESPRESSO y otras herramientas

especializadas; la arquitectura debe conservar independencia respecto de un único código. [5]

12. Quantum Dynamics Engine

Para sistemas cuánticos abiertos:

dρ
dt = − i
ℏ [H, ρ] + ∑

k
 (LkρL
†
k − 1
2 {L†
kLk, ρ}
) .

Se estudiarán coherencia, decoherencia, transporte excitónico, captura, ruido y dinámica de

sistemas abiertos.
 8

OMNISCIENCE Documento maestro 2026

13. Quantum Computing Engine

La computación cuántica será un recurso especializado. Un selector de hardware decidirá entre
CPU, GPU, HPC, simuladores y QPU según complejidad, tamaño, precisión, disponibilidad y

coste.

El sistema utilizará QPU únicamente cuando el problema y la evidencia de ventaja lo justifiquen.
Los resultados cuánticos deberán verificarse mediante simulación clásica, métodos analíticos o

réplicas cuando sea posible.

14. Quantum Sensing Engine

El motor estudiará sensibilidad, ruido, contraste, ancho de línea y límites de detección. Un

modelo idealizado puede escribirse:
 η ∝ ∆ν
C√R .

La expresión no se utilizará fuera de su régimen de validez y cada sensor tendrá un modelo

específico de ruido y medición.

15. Metamaterial and Metasurface Engine

El diseño inverso será:
 x∗ = arg m´ın
x L[F(x), yobjetivo].

Se podrán explorar metamateriales electromagnéticos, acústicos, mecánicos, fotónicos, fonónicos,

metasuperficies, estructuras topológicas y sistemas reconfigurables.

16. Photonic Engine

Se estudiarán interacción luz-materia, fotónica integrada, materiales ópticos, metasuperfi-
cies, óptica no lineal, excitones, polaritones y dispositivos optoelectrónicos. El motor buscará

combinaciones funcionales entre fotones, fonones, electrones y geometría.

17. Superconductivity Engine

El flujo será:
 estructura → electrones → fonones → acoplamiento → Tc.

Se analizarán estabilidad, densidad de estados, acoplamiento electrón-fonón, presión y compo-
sición. Ninguna predicción será etiquetada como superconductividad demostrada sin validación

experimental.
 9

OMNISCIENCE Documento maestro 2026

18. Chemical Discovery Engine

Se explorarán moléculas, reacciones, catalizadores, electrolitos, materiales funcionales y rutas

químicas. La optimización multiobjetivo será:

m´ax{A, S, St, E} − {C, T ox, Env}

donde A es actividad, S selectividad, St estabilidad y E eficiencia.

19. Energy Engine

Se investigarán baterías, almacenamiento térmico, hidrógeno, amoníaco, combustibles sintéti-
cos, termoeléctricos, fotovoltaica, catalizadores y sistemas electroquímicos. La función objetivo

combinará eficiencia, densidad energética, vida útil, coste, disponibilidad de materiales, seguridad

e impacto ambiental.

20. Fusion Materials and Digital Twin Engine

El motor integrará plasma, materiales, neutrones, refrigeración, superconductores, control,
mantenimiento y gemelos digitales. La estrategia de UKAEA 2026–2030 identifica computación
avanzada, gemelos digitales, materiales, robótica y control como capacidades relevantes para el

ciclo de vida de sistemas de fusión. [6]
Toda actividad con tritio, radiación, plasma de alta energía o instalaciones reales requerirá

autorización y supervisión especializada.

21. Biology and Biomaterials Engine

La arquitectura conectará moléculas, proteínas, complejos, células, tejidos y sistemas. Las

herramientas de IA podrán proponer hipótesis estructurales o funcionales, pero cada predicción

deberá distinguirse de la validación experimental. Los avances recientes en predicción de interac-

ciones biomoleculares muestran el potencial de integrar estructura y aprendizaje automático, pero

no eliminan la necesidad de validación. [7]

22. Therapeutic Discovery Engine

La cadena de evidencia será:

hipótesis → modelo → validación molecular → celular → preclínica → clínica.

El sistema no deberá presentar un candidato computacional como tratamiento ni generar instruc-

ciones clínicas sin evaluación regulatoria y profesional.

10

OMNISCIENCE Documento maestro 2026

23. Environmental Engine

Se investigarán captura y transformación de CO2, tratamiento de agua, descontaminación,

reciclaje, recuperación de materiales, eficiencia energética y reducción de residuos. La optimización

considerará ciclo de vida completo y posibles efectos secundarios.

24. Water Engine

Se estudiarán membranas, adsorbentes, catalizadores, sistemas electroquímicos y materiales

selectivos para desalación, purificación y recuperación de recursos.

25. Agriculture and Food Engine

Podrá investigar sensores, materiales biodegradables, eficiencia hídrica, conservación de ali-
mentos y optimización de procesos. Toda aplicación biológica o alimentaria deberá incorporar

validación de seguridad apropiada.

26. Aerospace and Extreme Materials Engine

Se analizarán materiales sometidos a temperatura, presión, radiación, vacío, ciclos térmicos y

cargas extremas. Se priorizarán ligereza, resistencia, estabilidad y manufacturabilidad.

27. AI Scientist Engine

OMNISCIENCE podrá utilizar IA para investigar nuevos algoritmos, arquitecturas, agentes y
métodos científicos. La evaluación deberá separar mejoras de benchmark de mejoras científicas

reales.

28. Innovation Radar

El radar convierte problemas en oportunidades de investigación:

S = wI I + wF F + wN N + wRR + wEE − wCC − wQQ.

La función podrá adaptarse a cada dominio y deberá mostrar los pesos utilizados.

29. Diseño inverso universal

propiedad objetivo → estructura → composición → fabricación → validación.

El motor generará candidatos, pero deberá filtrarlos mediante restricciones físicas, químicas,

económicas, ambientales y de fabricación.
 11

OMNISCIENCE Documento maestro 2026

30. Optimización bayesiana y búsqueda activa

x∗ = arg m´ax
x a(x)

EI(x) = E[m´ax(0, f (x) − f +)].

También se podrán utilizar optimización evolutiva, aprendizaje por refuerzo, modelos generativos,

búsqueda multiobjetivo y optimización restringida.

31. Valor esperado de información

U (e) = E[∆I(e)]Pdisc(e)Vimpacto
C(e)R(e) .

Esta métrica prioriza acciones que puedan reducir incertidumbre y modificar decisiones científicas

importantes.

32. Estadística e incertidumbre

p(x) = 1
√2πσ2 e−(x−µ)2/(2σ2)

P (H|D) = P (D|H)P (H)
P (D)

H(X) = − ∑

i p(xi) log p(xi).

La plataforma debe utilizar métodos apropiados al tipo de dato; las expresiones anteriores son

componentes generales y no sustituyen modelos estadísticos específicos.

33. Falsación adversarial
z = |y − ˆy|
√
σ2
pred + σ2
ref .

Un valor elevado puede activar revisión, pero no constituye por sí mismo una regla universal de

falsación. Los criterios deben definirse para cada problema.

34. Réplicas independientes

Una réplica puede cambiar código, funcional, pseudopotenciales, tamaño de supercelda, malla

k, hardware, modelo de IA, semilla, instrumento, operador o método experimental. El objetivo es

comprobar que el resultado no depende de un único camino de cálculo.

12

OMNISCIENCE Documento maestro 2026

35. Active Experiment Design

Cuando exista laboratorio autorizado, el sistema propondrá el experimento que mejor discrimine

entre hipótesis. El experimento debe tener:

1. objetivo;

2. hipótesis comparadas;

3. variable discriminante;

4. protocolo aprobado;

5. criterios de éxito y fracaso;

6. incertidumbre esperada;

7. condiciones de seguridad;

8. registro de procedencia.

36. Laboratorio autónomo y robótica

La arquitectura podrá conectarse a equipos de caracterización y plataformas robóticas. El

ciclo será:
 predicción → fabricación → medición → análisis → nueva predicción.

Las acciones físicas de riesgo no serán autónomas por defecto.

37. Digital Twins

Los gemelos digitales representarán materiales, dispositivos, procesos, laboratorios y sistemas
energéticos. Cada gemelo deberá tener un dominio de validez explícito y diferenciar estado

observado de estado inferido.

38. Provenance y reproducibilidad

Cada ejecución debe almacenar código, versión, entorno, datos de entrada, parámetros, hard-

ware, software, resultados, logs y hashes. RO-Crate ofrece un mecanismo de empaquetado de datos

y metadatos que puede complementar W3C PROV. [3]

39. Auditoría bibliográfica

El sistema debe recuperar fuentes desde registros identificables y verificar DOI, PMID, arXiv

ID u otros identificadores persistentes. Una referencia no debe generarse desde memoria del modelo.

La evidencia debe quedar vinculada a la afirmación.

13

OMNISCIENCE Documento maestro 2026

40. Seguridad y gobernanza

40.1. Permitido inicialmente

Simulación, análisis de datos públicos, análisis bibliográfico, generación de hipótesis, optimiza-

ción computacional y elaboración de informes.

40.2. Revisión humana obligatoria

Síntesis química, modificación biológica, trabajo con células, tejidos o animales, aplicaciones
médicas, materiales radiactivos, tritio, fusión, plasma de alta energía y experimentos físicos

potencialmente peligrosos.

41. Arquitectura de software

omniscience/

README.md

LICENSE

pyproject.toml

configs/

docs/

knowledge/

ontology/

references/

agents/

physics/ chemistry/ materials/ biology/

quantum/ fusion/ mathematics/ verification/

engines/

matter/ vibrations/ phonons/ quantum/

metamaterials/ photonics/ chemistry/

biology/ energy/ fusion/ environment/

water/ innovation/

campaigns/

simulations/

experiments/

data/

notebooks/

reports/

tests/

audit/

42. Esquema mínimo de una campaña

CampaignID
 14

OMNISCIENCE Documento maestro 2026

Problem

Question

Hypotheses[]

Predictions[]

Models[]

Datasets[]

ComputationalRuns[]

FalsificationTests[]

Experiments[]

Replications[]

EvidenceLevel

Uncertainty

Provenance

Decision

NextAction

43. Algoritmo maestro

Algorithm 1 Ciclo universal de descubrimiento OMNISCIENCE
Require: Problema, datos, restricciones, presupuesto, riesgo

1: Definir pregunta científica

2: Recuperar y verificar evidencia

3: Construir grafo de conocimiento

4: Generar hipótesis alternativas

5: Formular predicciones cuantitativas

6: Definir criterios de falsación

7: Filtrar restricciones físicas, éticas y de seguridad

8: Seleccionar modelos y hardware

9: Ejecutar simulaciones

10: Ejecutar verificación independiente

11: Buscar contradicciones

12: Cuantificar incertidumbre

13: Diseñar experimento discriminante si procede

14: Solicitar autorización humana si procede

15: Ejecutar experimento autorizado

16: Comparar predicción y observación

17: Ejecutar réplica

18: Actualizar evidencia y grafo

19: Clasificar resultado

20: Seleccionar siguiente acción por valor esperado de información

15

OMNISCIENCE Documento maestro 2026

44. Plan de implementación

44.1. Fase 0: infraestructura

Python, contenedores, control de versiones, base de datos, almacenamiento de artefactos,

registro de procedencia y pruebas automáticas.

44.2. Fase 1: MV1

Materiales, estructuras, relajación, energías, fuerzas, fonones y estabilidad dinámica. Phonopy

documenta un flujo basado en celdas, superceldas, desplazamientos, fuerzas y constantes de fuerza.

[4]

44.3. Fase 2: Quantum Dynamics

Hamiltonianos, Lindblad, ruido, coherencia y transporte.

44.4. Fase 3: diseño inverso

Generación de estructuras y materiales candidatos y filtrado mediante cálculos de alta fidelidad.

44.5. Fase 4: multiagente

Agentes generadores, verificadores y falsadores.

44.6. Fase 5: radar interdisciplinario

Conectar materiales, química, energía, biología, medio ambiente y dispositivos.

44.7. Fase 6: experimentación autorizada

Integración con laboratorios y robótica bajo supervisión.

44.8. Fase 7: gemelos digitales

Modelado continuo de sistemas complejos.

45. Métricas de éxito

porcentaje de resultados reproducibles;

tasa de falsación de hipótesis;

reducción de coste computacional por descubrimiento;

tiempo desde problema hasta predicción verificable;

valor esperado de información por campaña;

diversidad de métodos independientes;
 16

OMNISCIENCE Documento maestro 2026

cobertura de procedencia;

número de predicciones experimentalmente verificadas;

tasa de falsos positivos;

impacto científico o tecnológico validado.

46. Riesgos científicos

alucinaciones bibliográficas;

sesgo de datos;

fuga de información entre entrenamiento y evaluación;

sobreajuste;

errores numéricos;

extrapolación fuera del dominio de validez;

optimización de métricas equivocadas;

correlación interpretada como causalidad;

consenso artificial entre modelos similares.

47. Mitigaciones

Se utilizarán fuentes verificadas, conjuntos de prueba independientes, múltiples modelos,

cálculos de referencia, pruebas de convergencia, validación cruzada, agentes adversariales y revisión

humana.

48. Ejemplos de campañas científicas

48.1. Material térmico

Buscar un material con baja conductividad térmica y estabilidad dinámica. Flujo: generación

de candidatos, relajación, estabilidad, fonones, transporte, réplica.

48.2. Material fotónico

Definir respuesta óptica objetivo y realizar diseño inverso de geometría y composición, seguido

de simulación electromagnética y fabricación experimental si procede.

48.3. Catalizador

Optimizar actividad, selectividad, estabilidad, disponibilidad y toxicidad mediante modelos

moleculares y validación experimental.
 17

OMNISCIENCE Documento maestro 2026

48.4. Sensor cuántico

Optimizar sensibilidad frente a ruido y temperatura, y diseñar una prueba experimental

discriminante.

48.5. Fusión

Explorar materiales y arquitecturas térmicas mediante simulación multi-física y gemelo digital;

la validación física requiere instalaciones especializadas.

48.6. Biomaterial

Generar candidatos, evaluar propiedades fisicoquímicas, estudiar interacciones biológicas y

avanzar solo mediante validación progresiva autorizada.

49. Principio de descubrimiento universal

La plataforma debe buscar no solo mejores soluciones dentro de categorías existentes, sino

cambios de representación. En términos generales:

nuevo material + nueva geometría + nuevo régimen físico + nuevo algoritmo

pueden abrir espacios de diseño que no aparecen al optimizar una sola variable.

50. Conclusión general

OMNISCIENCE es concebido como una infraestructura científica interoperable y verificable.
El proyecto no promete descubrir cualquier cosa ni presupone que todas las disciplinas puedan
reducirse a un mismo modelo. Su objetivo es construir un sistema capaz de coordinar múltiples

métodos, representar explícitamente la incertidumbre, buscar refutaciones y utilizar computación

avanzada allí donde aporte valor.

El núcleo inicial recomendado es el motor universal de materia y vibraciones, porque permite

conectar composición, estructura, fuerzas, fonones, propiedades térmicas y diseño inverso con datos
y software reproducibles. Sobre este núcleo se incorporarán dinámica cuántica, metamateriales,

fotónica, química, biología, energía, fusión y experimentación autónoma.

La arquitectura final puede expresarse como:

Problema → Conocimiento → Hipótesis → Predicción → Simulación → Falsación → Experimento → Réplica → Conocimiento

La condición de éxito no será producir muchas hipótesis, sino producir hipótesis útiles que
sobrevivan a pruebas independientes y puedan convertirse en conocimiento reproducible o en

decisiones experimentales racionales.
 18

OMNISCIENCE Documento maestro 2026

Referencias

[1] W3C. PROV-Overview. https://www.w3.org/TR/prov-overview/

[2] W3C. PROV-O: The PROV Ontology. https://www.w3.org/TR/prov-o/

[3] Research Object Crate. RO-Crate Specification. https://www.researchobject.org/

ro-crate/specification/1.3/

[4] Phonopy Project. Workflow. https://phonopy.github.io/phonopy/workflow.html

[5] Quantum ESPRESSO. Official documentation. https://www.quantum-espresso.org/

[6] UK Atomic Energy Authority. UK Atomic Energy Authority strategy 2026 to
2030. 2026. https://www.gov.uk/government/publications/ukaea-strategy/

uk-atomic-energy-authority-strategy-2026-to-2030

[7] Abramson et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3.

Nature, 2024. https://www.nature.com/articles/s41586-024-07487-w

19
