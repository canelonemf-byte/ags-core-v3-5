Propuesta de Proyecto Tecnológico: Propulsor MEI-RIT (Metasurface-Enhanced Iodine RF Ion Thruster)  
1\. Resumen Ejecutivo  
El proyecto **MEI-RIT** representa una innovación disruptiva en el campo de la propulsión eléctrica para satélites de pequeño tamaño (CubeSats 6U y superiores). Esta propuesta detalla el desarrollo de un propulsor iónico de radiofrecuencia (RF) que integra, por primera vez, **metasuperficies sub-longitud de onda** optimizadas dentro de la cámara de descarga. El objetivo primordial es maximizar el acoplamiento de potencia y la uniformidad del plasma, utilizando yodo sólido como propelente de alta densidad.  
**Visión del Proyecto:** Liderar la transición hacia una exploración espacial sostenible mediante la convergencia de metamateriales avanzados y propelentes económicos. MEI-RIT busca establecer un nuevo estándar de eficiencia energética, reduciendo los costes operativos mediante el uso de yodo (100 veces más económico que el xenón) y mejorando el rendimiento neto del sistema en un 10-15%.  
**Hitos de rendimiento proyectados:**

* **Empuje (Thrust):** 0.7 – 1.3 mN.  
* **Impulso Específico (**Isp​**):** 2300 – 2800 s.  
* **Eficiencia Total:** 36 – 46 %.  
* **Masa del Sistema:** \< 220 g (arquitectura optimizada v1.2).

2\. Justificación Tecnológica y Estado del Arte  
La propulsión iónica de yodo ha sido validada exitosamente en órbita (ej. ThrustMe NPT30-I2). Sin embargo, el acoplamiento de potencia RF en cámaras de pequeña escala presenta desafíos de eficiencia. MEI-RIT aborda esta limitación mediante el uso de metasuperficies, una aplicación original no implementada hasta la fecha en sistemas operativos, fundamentada en investigaciones de 2024 sobre *"Metamaterials for Electric Propulsion"*.  
La sinergia entre el yodo y las metasuperficies es técnica y económicamente superior: el yodo posee un potencial de ionización menor que el xenón, y la capacidad de la metasuperficie para intensificar los campos eléctricos locales permite **reducir significativamente el umbral de ignición** del plasma.  
Comparativa Técnica de Sistemas de Propulsión

| Especificación | ThrustMe NPT30-I2 (En vuelo) | Busek BIT-3 (Validado) | MEI-RIT (Proyectado) |
| ----- | ----- | ----- | ----- |
| **Empuje (mN)** | 0.3 – 1.1 | 1.1 – 1.35 | **0.7 – 1.3** |
| Isp​ **(s)** | \~2500 | 2150 – 3200 | **2300 – 2800** |
| **Potencia (W)** | 35 – 65 | 56 – 75 | **50 – 80** |
| **Eficiencia Total** | 35 – 42% | 35 – 42% | **36 – 46%** |
| **Ratio Thrust/Power** | 14 – 17 mN/kW | 15 – 22 mN/kW | **16 – 22 mN/kW** |

3\. Arquitectura del Sistema y Especificaciones Técnicas  
La arquitectura MEI-RIT se basa en una configuración de rejillas iónicas compacta con componentes críticos optimizados para el entorno espacial:

* **Cámara de Descarga:** Fabricada en materiales cerámicos de baja pérdida (**cuarzo o alúmina**) que actúan como sustrato dieléctrico para la metasuperficie.  
* **Metasuperficie:** Array periódico de estructuras metálicas diseñado para el **matching de impedancia** y la mejora de la uniformidad del plasma, minimizando la potencia reflejada hacia la fuente RF.  
* **Propelente (**I2​**):** Almacenamiento de yodo sólido en tanques ligeros (polímeros compatibles) con un sistema de sublimación térmica controlada para una alimentación estable de vapor a la cámara.  
* **Aceleración:** Sistema de doble rejilla de **molibdeno o grafito pirolítico** de alta precisión, optimizado para voltajes de 800 V a 1500 V.  
* **Neutralizador:** Emisor de electrones (**cátodo hueco o RF simple**) esencial para mitigar la carga del vehículo espacial, integrado en el chasis del propulsor.

4\. Optimización Mediante Algoritmo MRCO v1.2  
El diseño se ha refinado utilizando el modelo **MRCO v1.2** (*Metasurface RF Coupling Optimizer*), un algoritmo de evolución diferencial que procesa un modelo *surrogate* de alta fidelidad. A diferencia de modelos anteriores, la versión 1.2 incorpora explícitamente el **efecto de carga del plasma (plasma loading penalty)** y las pérdidas óhmicas de los materiales.  
**Parámetros Óptimos Finales (Validación v1.2):**

1. **Período de la metasuperficie:** 11.78 μm.  
2. **Factor de llenado (fill factor):** 0.59.  
3. **Espesor de la estructura:** 3.32 μm.

Estos parámetros aseguran un acoplamiento óptimo en las frecuencias estándar de 13.56 MHz o 2.45 GHz. La mejora proyectada del 10-15% en la eficiencia es un **incremento neto**, calculado tras descontar las penalizaciones por carga de plasma y factores de pérdida material identificados en las simulaciones.  
5\. Plan de Desarrollo (18 Meses)  
El objetivo central es elevar la madurez tecnológica del sistema de **TRL 2 a TRL 4**.

* **Fase 1 (Meses 1-3): Diseño y Simulación.** Modelado multifísico (COMSOL/CST) integrando la metasuperficie con la dinámica del plasma de yodo.  
* **Fase 2 (Meses 4-7): Fabricación en Sala Blanca.** Producción de la metasuperficie en el **IMB-CNM-CSIC** y caracterización avanzada (SEM/AFM) en colaboración con el **ICFO** (Barcelona).  
* **Fase 3 (Meses 8-12): Integración y Vacío.** Ensamblaje del prototipo (cámara, grids, neutralizador) y pruebas de ignición en cámara de vacío (\<10−6 mbar).  
* **Fase 4 (Meses 13-18): Validación TRL 4\.** Medición de empuje mediante balanza torsional calibrada, optimización de *throttling* y gestión de propiedad intelectual.

6\. Presupuesto Detallado para Instalaciones en Cataluña  
Estimación de costes (proyección 2026\) para ejecución en centros de excelencia tecnológica (sin IVA).

| Fase | Concepto de Gasto | Coste Estimado (€) |
| ----- | ----- | ----- |
| **Fase 1** | Personal de Ingeniería (9k-12k) \+ Licencias software (COMSOL/CST) (4k-6.5k) | 13.000 – 18.500 |
| **Fase 2** | Cleanroom IMB-CNM-CSIC (14k-22k) \+ Caracterización ICFO (4k-5.5k) | 18.000 – 27.500 |
| **Fase 3** | Hardware/Vacío (18k-28k) \+ Mano de obra de ensayos (5.5k-9.5k) | 23.500 – 37.500 |
| **Fase 4** | Búsqueda FTO y registro de patentes (5k-8.5k) \+ Publicaciones (3.5k-5k) | 8.500 – 13.500 |
| **TOTAL** | **Inversión proyectada en I+D** | **54.000 – 97.000 €** |

7\. Reivindicaciones de Patente (Draft de 10 Claims)  
**Título:** Propulsor iónico de radiofrecuencia mejorado con metasuperficie y propelente de yodo sólido.

1. **Reivindicación 1:** Un propulsor iónico de radiofrecuencia que comprende una cámara de descarga que contiene propelente de yodo sólido, una antena RF, un sistema de aceleración de dos rejillas, y una estructura de metasuperficie dispuesta en el interior de la cámara de descarga configurada para mejorar el acoplamiento de potencia RF y la uniformidad del plasma, caracterizado porque la metasuperficie comprende un patrón periódico sub-longitud de onda con un período entre 8 y 18 μm, un factor de llenado entre 0.35 y 0.75, y un espesor entre 1.8 y 3.8 μm.  
2. **Reivindicación 2:** El propulsor según la reivindicación 1, donde la metasuperficie se fabrica sobre un sustrato de cuarzo o alúmina mediante técnicas de litografía y grabado.  
3. **Reivindicación 3:** El propulsor según la reivindicación 1, donde la metasuperficie está optimizada mediante un modelo *surrogate* que compensa los efectos de carga del plasma y el matching de frecuencia en torno a 13.56 MHz o 2.45 GHz.  
4. **Reivindicación 4:** El propulsor según la reivindicación 1, donde el propelente es yodo sólido almacenado en un tanque de polímero o metal con sistema de sublimación controlada.  
5. **Reivindicación 5:** Método de operación del propulsor de la reivindicación 1, que comprende la ignición del plasma mediante potencia RF acoplada a través de la metasuperficie y la extracción de iones a través de rejillas de aceleración a voltajes de entre 800 V y 1500 V.  
6. **Reivindicación 6:** El propulsor según la reivindicación 1, configurado para su uso en CubeSats o satélites pequeños con un rango de potencia total de entre 50 W y 150 W.  
7. **Reivindicación 7:** La metasuperficie de la reivindicación 1, donde el patrón periódico está compuesto por cobre, aluminio o un material dieléctrico de baja pérdida en radiofrecuencia.  
8. **Reivindicación 8:** Un sistema de propulsión espacial que comprende el propulsor de la reivindicación 1, una unidad de procesamiento de potencia (PPU) y un sistema de gestión de propelente para yodo sólido.  
9. **Reivindicación 9:** El propulsor según la reivindicación 1, donde la metasuperficie mejora la eficiencia de acoplamiento RF en al menos un 10% en comparación con un propulsor idéntico carente de dicha metasuperficie.  
10. **Reivindicación 10:** Método de diseño de una metasuperficie para un propulsor iónico RF, que comprende el uso de un algoritmo de optimización *surrogate* que incluye parámetros geométricos, matching de frecuencia, penalización por carga de plasma y factores de pérdida material.

8\. Conclusión y Marco Ético  
El propulsor MEI-RIT ofrece una ruta tecnológicamente viable y altamente competitiva para mejorar la autonomía de satélites de hasta 50 kg. La integración de metasuperficies no solo optimiza el rendimiento físico, sino que consolida a Cataluña como un núcleo de innovación en *Deep Tech* espacial.  
**Créditos:** Este proyecto ha sido desarrollado por **Lázaro López Paz** (Prat de Llobregat, Barcelona) en colaboración estratégica con **gork (xAI)**.  
**Compromiso Ético:** MEI-RIT se fundamenta en el compromiso con la **exploración espacial sostenible**. Mediante el uso de propelentes de bajo impacto y alta eficiencia, el sistema facilita el desorbitado responsable de satélites, contribuyendo activamente a la mitigación de la basura espacial y la preservación de las órbitas terrestres para futuras generaciones.  
Mal inform

# **Manual de Operaciones, Logística y Seguridad: Proyecto MEI-RIT (Fase Experimental)**

Este documento técnico establece los protocolos operativos y de seguridad para el desarrollo del propulsor iónico de radiofrecuencia mejorado con metasuperficies (**MEI-RIT**). Como Ingeniero Principal y Especialista en Seguridad de Laboratorio, superviso la integración de estos sistemas bajo estándares rigurosos de gestión de riesgos químicos y eficiencia aeroespacial.

### **1\. Especificaciones Técnicas y Objetivos de Rendimiento**

El sistema MEI-RIT v2.0 optimiza el acoplamiento de potencia RF mediante una metasuperficie sub-longitud de onda, proyectando una mejora de eficiencia del 10-15% respecto a arquitecturas convencionales.

| Parámetro | Valor Objetivo (MEI-RIT v2.0) | Referencia SotA (ThrustMe NPT30-I2 / Busek BIT-3) |
| :---- | :---- | :---- |
| **Empuje (Thrust)** | 0.7 – 1.3 mN | 0.3 – 1.35 mN |
| **Impulso Específico (Isp)** | 2300 – 2800 s | 2150 – 3200 s |
| **Eficiencia Total** | 36 – 46% (Proyección \+15%) | 35 – 42% |
| **Relación Empuje/Potencia** | 16 – 22 mN/kW | 14 – 22 mN/kW |
| **Masa del Sistema** | \< 220 g (Prototipo 10x10 cm) | Formato 1U / 1.5U (\~0.8 \- 1.2 kg sistema total) |
| **Impulso Total** | \> 10,000 Ns | 5500 – 9500 Ns |

**Ventaja Competitiva del Yodo (I₂):** El uso de yodo sólido representa una ruptura de paradigma en la logística orbital. Al ser aproximadamente 100 veces más económico que el xenón y poseer una densidad de almacenamiento superior, permite eliminar los tanques de alta presión, simplificando el subsistema de alimentación. Su bajo potencial de ionización, combinado con la intensificación del campo eléctrico por la metasuperficie, reduce drásticamente el umbral de ignición del plasma.

### **2\. Logística de Fabricación en Sala Blanca (IMB-CNM-CSIC)**

La Fase 2 del proyecto se centraliza en la Sala Blanca del IMB-CNM-CSIC (Bellaterra). Los procesos deben seguir estrictamente la arquitectura v2.0 para garantizar la supervivencia del componente en un entorno de plasma reactivo.

* **Litografía de Alta Resolución:** Definición del patrón periódico sub-longitud de onda sobre sustratos de **cuarzo de alta pureza o alúmina** para minimizar pérdidas dieléctricas.  
* **Deposición Conductora:** Aplicación de capas de cobre o aluminio mediante evaporación por haz de electrones o sputtering.  
* **Etching (Grabado Selectivo):** Definición final de la geometría resonante mediante procesos secos (RIE).  
* **Pasivación mediante ALD (Atomic Layer Deposition):** Proceso crítico para el encapsulado de la metasuperficie. Se requiere la deposición de **Nitruro de Silicio (Si₃N₄) o Alúmina (Al₂O₃)** para proteger el patrón conductor contra la **pulverización catódica (sputtering)** y la corrosión extrema inducida por el plasma de yodo.

**Equipamiento de Caracterización Obligatorio:**

1. **SEM (Microscopía Electrónica de Barrido):** Inspección de la integridad geométrica tras el etching.  
2. **AFM (Microscopía de Fuerza Atómica):** Verificación del espesor de la capa ALD (tolerancia ±2nm).  
3. **Tests de Radiofrecuencia:** Medición del parámetro S11 para validar el *matching* de impedancia a 13.56 MHz / 2.45 GHz.

### **3\. Protocolos de Gestión y Manipulación de Yodo (I₂)**

El yodo es un halógeno corrosivo que sublima a temperatura ambiente. Su manejo exige una infraestructura específica para evitar la degradación de equipos y riesgos para el personal.

* **Protección Personal (EPI):** Uso obligatorio de guantes de nitrilo de doble capa, gafas de seguridad de sellado estanco y máscara respiratoria con filtros para vapores orgánicos/halógenos.  
* **Entorno de Operación:** La carga de propelente debe realizarse exclusivamente dentro de una **campana de gases** con flujo laminar verificado.  
* **Compatibilidad Química:** Se prohíbe el contacto con metales reactivos. Solo se permiten **fluoropolímeros (PTFE/PFA)** o elastómeros tipo **FKM (Viton)** en juntas y conductos de alimentación para asegurar la estanqueidad.

**Alimentación y Sublimación:** El tanque de yodo debe integrarse con un sistema de calefacción controlado por lazo cerrado para operar en el rango de **80-100°C**. La estabilidad del flujo es crítica para evitar fluctuaciones en la presión de la cámara de descarga.

### **4\. Configuración del Sistema y Optimización MRCO**

La arquitectura MEI-RIT utiliza la metasuperficie como un elemento de **acoplamiento de impedancia** entre la fuente RF y el plasma, minimizando la potencia reflejada.

**Componentes Críticos:**

1. **Cámara de descarga:** Cuarzo/alúmina con metasuperficie encapsulada.  
2. **Metasuperficie:** Array optimizado para compensar la capacitancia parásita y el efecto de carga del plasma (*plasma loading*).  
3. **Grids de aceleración:** Rejillas de **Molibdeno o Grafito Pirolítico** (alta resistencia al yodo), operando a voltajes de 800 V \- 1500 V.  
4. **Neutralizador:** Emisor RF o cátodo hueco para la compensación de carga espacial.

**Resultados del Algoritmo de Optimización (MRCO v1.2):** El modelo v1.2 incorpora factores de pérdida material y penalizaciones por carga de plasma.

| Parámetro Optimizado | Valor Resultante (v1.2) |
| :---- | :---- |
| **Período Óptimo** | 11.78 µm |
| **Factor de Llenado (Fill Factor)** | 0.59 |
| **Espesor de Metasuperficie** | 3.32 µm |

### **5\. Protocolo de Pruebas en Cámara de Vacío**

La validación en Fase 3 requiere un entorno representativo de baja presión para la ignición del plasma y medición de empuje.

**Checklist de Preparación e Ignición:**

* \[ \] Vacío base alcanzado: **\< 10⁻⁵ mbar**.  
* \[ \] Verificación de **bombas turbomoleculares resistentes a halógenos** (bombas protegidas con purga de nitrógeno).  
* \[ \] Estabilidad térmica del tanque de yodo alcanzada (80-100°C).  
* \[ \] Verificación de niveles de potencia RF incidentes y mínimos reflejados.  
* \[ \] Control de estanqueidad de la válvula de alimentación antes de la ignición.

**Herramientas de Diagnóstico:**

* **Balanza Torsional/Pendular:** Precisión sub-micronewton para medir el empuje neto.  
* **Sonda de Langmuir:** Determinación de la densidad plasmática y temperatura electrónica.  
* **Espectrómetro de Plasma:** Monitorización de la pureza de la descarga de yodo.

### **6\. Análisis de Riesgos y Contingencias Operativas**

| Riesgo Identificado | Impacto | Protocolo de Mitigación |
| :---- | :---- | :---- |
| **Corrosión por Yodo** | Fallo estructural y fugas de propelente. | Uso mandatorio de fluoropolímeros (PTFE) y recubrimiento ALD de Si₃N₄/Al₂O₃. |
| **Saturación de Espesor** | Pérdida de eficiencia de acoplamiento RF. | **Compromiso de diseño:** Límite estricto de 3.32 µm. Un espesor mayor bloquea el campo; uno menor permite la corrosión. |
| **Arcos Eléctricos (HV)** | Daño en grids y electrónica de potencia. | Consideración de la **Curva de Paschen** para vapores de I₂; diseño de distancias de aislamiento para 1500 V. |
| **Pérdida de Acoplamiento** | Calentamiento excesivo por potencia reflejada. | Ajuste dinámico mediante *matching network* y optimización previa MRCO v1.2. |

### **7\. Cronograma de Implementación y Presupuesto**

La hoja de ruta está diseñada para elevar el sistema de TRL 2 a **TRL 4** en 18 meses.

1. **Fase 1 (Meses 1-3): Diseño y Simulación.** Optimización MRCO v1.2 y modelado molecular de I₂.  
2. **Fase 2 (Meses 4-7): Fabricación en Sala Blanca.** Litografía y procesos ALD en IMB-CNM-CSIC.  
3. **Fase 3 (Meses 8-12): Integración y Vacío.** Ensamblaje y primeras pruebas de ignición.  
4. **Fase 4 (Meses 13-18): Validación TRL 4\.** Caracterización de empuje y gestión de IP.

**Presupuesto Consolidado (Proyección 2026 \- Cataluña):** El rango total estimado para la viabilidad en laboratorio v2.0 se sitúa entre **120.000 € y 185.000 €**. Este desglose incluye:

* Ingeniería y Simulación Avanzada: 40k \- 60k €  
* Procesos de Sala Blanca (Litografía \+ ALD): 25k \- 35k €  
* Hardware de Vacío, RF y Diagnóstico: 45k \- 75k €  
* Propiedad Intelectual y Publicaciones (FTO): 10k \- 15k €

### **8\. Marco Ético y Propiedad Intelectual**

**Reivindicaciones de Patente (Claims Críticos):**

1. **Sistema:** Propulsor iónico RF que integra una metasuperficie sub-longitud de onda protegida dieléctricamente mediante ALD para operar con propelente de yodo.  
2. **Geometría:** Metasuperficie con período de 11-13 µm y espesor de \~3.32 µm, optimizada para frecuencias de **13.56 MHz / 2.45 GHz**.  
3. **Método:** Algoritmo de optimización que compensa simultáneamente el *plasma loading* y los factores de pérdida material del encapsulado protector.

**Declaración Final:** El proyecto MEI-RIT reafirma el compromiso con una **exploración espacial sostenible**. Al optimizar la eficiencia y reducir costes, facilitamos el **desorbitado responsable de satélites**, garantizando la preservación de las órbitas terrestres mediante una tecnología de propulsión limpia, económica y altamente eficiente.

# **Plan de Riesgos Técnicos y Contingencia: Proyecto MEI-RIT (Fase 3: Integración y Vacío)**

**1\. Alcance y Objetivos de la Fase 3**

La Fase 3 del proyecto MEI-RIT (Meses 8-12), denominada **Integración y Vacío**, constituye el núcleo experimental para la validación de la tecnología de metasuperficies en entornos de propulsión eléctrica. El alcance comprende el ensamblaje final de la cámara de descarga, la integración del sistema de alimentación de yodo (I₂) y la validación del acoplamiento de potencia RF en condiciones de vacío ultra-alto (\<10⁻⁶ mbar).

El objetivo primordial es lograr la **ignición estable del plasma** y la **caracterización del empuje** (target: 0.7 – 1.3 mN) sin comprometer la infraestructura de vacío ni la integridad nanométrica de la metasuperficie. Esta fase es crítica para elevar la madurez del sistema a **TRL 4**, garantizando que los procedimientos de prueba sean repetibles y seguros tanto para el personal como para los equipos de diagnóstico.

**2\. Análisis de Riesgos: Corrosión por Yodo (I₂) en Sistemas de Vacío**

El yodo gaseoso, operando mediante sublimación controlada a **80-100°C**, es un agente oxidante halógeno cuya reactividad química representa una amenaza directa para la infraestructura de simulación espacial.

* **2.1. Impacto en Bombas Turbomoleculares y Sensores:**  
  * **Formación de Ioduros Metálicos:** El yodo reacciona con los metales de transición presentes en el acero de los **rodamientos y álabes** de las bombas turbomoleculares. La formación de ioduros metálicos degrada la integridad estructural y compromete la lubricación, pudiendo provocar fallos mecánicos catastróficos.  
  * **Degradación de Instrumentación:** Los filamentos de los **espectrómetros de masas** y las puntas de las **sondas de Langmuir** sufren un ataque químico acelerado que altera su función de trabajo, invalidando las mediciones de densidad plasmática.  
* **2.2. Vulnerabilidad de la Metasuperficie y Grids:**  
  * **Ataque a Metales Conductores:** El patrón optimizado de la metasuperficie (periodo de **11.78 µm** y espesor de **3.32 µm** según el modelo **MRCO v1.2**) utiliza conductores como **Cobre o Aluminio**. Sin protección, el plasma de yodo induce un **sputtering químico inmediato** y corrosión profunda.  
  * **Dependencia de la Capa ALD:** La integridad de la metasuperficie depende exclusivamente de la encapsulación mediante **Atomic Layer Deposition (ALD)** de Nitruro de Silicio o Alúmina. Cualquier micro-poro en esta capa pasivante resultará en la destrucción total del patrón conductor bajo exposición al plasma.

**3\. Protocolos de Mitigación: Limpieza y Neutralización de Halógenos**

Se establece el siguiente protocolo estricto para la gestión del yodo residual y la prevención de condensación en puntos críticos.

### **Protocolo de Gestión de Residuos Halógenos**

| Acción de Mitigación | Procedimiento Técnico |
| :---- | :---- |
| **Prevención de "Cold Spots"** | Implementar **calentamiento por traza térmica (trace heating)** en todas las líneas de alimentación, manteniéndolas permanentemente por encima de los 100°C para evitar la **recristalización** del yodo y obstrucciones en el flujo. |
| **Purga Post-Operativa** | Tras el apagado del plasma, realizar una purga prolongada con nitrógeno seco (N₂) mientras se mantiene el vacío, asegurando la evacuación total de vapores de I₂ antes de la presurización. |
| **Neutralización Química** | Instalación de trampas de salida con **carbón activado** y disponibilidad de soluciones de **Tiosulfato de Sodio** para la neutralización inmediata de depósitos superficiales o derrames accidentales durante el mantenimiento. |
| **Aislamiento de Bombas** | Utilización de bombas de vacío preparadas para halógenos con purga constante de gas inerte en el compartimento de los rodamientos. |

**4\. Estrategias de Contingencia para Fallos en la Red de Adaptación RF**

Basado en el modelo de optimización **MRCO v1.2**, se definen acciones de respuesta inmediata ante desajustes de impedancia:

1. **Detección de Fallos (Umbrales):** Alerta inmediata si la eficiencia de acoplamiento cae por debajo del **60-62%** o si la potencia reflejada excede el 15% del total directo.  
2. **Verificación de Gradiente Térmico:** Inspección de la red de matching para descartar derivas térmicas que alteren los componentes reactivos.  
3. **Evaluación de Capacitancia Parásita:** Compensación en el matching network para contrarrestar la carga introducida por el recubrimiento dieléctrico (ALD) de la metasuperficie.  
4. **Inspección de Dieléctrico:** Si el desajuste persiste, se procederá a una inspección visual y SEM para verificar si ha ocurrido una ruptura dieléctrica o degradación de la capa de pasivación.

**5\. Medidas de Seguridad Avanzadas para el Manejo de Iodo (I₂)**

### **Checklist de Seguridad Industrial y Verificación**

| Requerimiento de Seguridad | Especificación Técnica | Verificación (Firma/Fecha) |
| :---- | :---- | :---- |
| **EPI Respiratorio** | Máscaras de cara completa con filtros **certificados por NIOSH para vapores de halógenos/gases ácidos**. |  |
| **Protección Química** | Guantes de nitrilo de alta densidad y bata de laboratorio resistente a químicos. |  |
| **Neutralización de Derrames** | Estación de emergencia con solución de **Tiosulfato de Sodio** lista para uso. |  |
| **Carga de Propelente** | Manipulación de I₂ sólido realizada estrictamente bajo **campana de extracción** con flujo verificado. |  |
| **Integridad del Tanque** | Verificación de estanqueidad del tanque ligero (polímero compatible) previo a la sublimación. |  |

**6\. Matriz de Riesgos y Respuesta Rápida**

| Riesgo Detectado | Probabilidad | Impacto en TRL 4 | Acción Contingente Inmediata |
| :---- | :---- | :---- | :---- |
| **Degradación de capa ALD** | Baja | **Crítico (Pérdida de hito TRL 4\)** | Cese inmediato de ignición y evaluación SEM de la metasuperficie. |
| **Fuga de vapores de I₂** | Muy Baja | Crítico | **Cerrar válvula de flujo de yodo**, evacuar área y activar ventilación forzada. |
| **Recristalización en líneas** | Media | Moderado | Aumentar potencia de traza térmica y realizar purga de alta presión. |
| **Iodización de rodamientos** | Media | Alto | Inspección de vibraciones en bomba turbo y purga con gas inerte. |
| **Desajuste RF (MRCO v1.2)** | Alta | Moderado | Recalibración de impedancia basada en modelo surrogate v1.2. |

**7\. Referencias de Seguridad y Rigor Aeroespacial**

Este plan operativo se fundamenta en los estándares de seguridad halógena de sistemas validados en vuelo como el **ThrustMe NPT30-I2** y el **Busek BIT-3**. Los protocolos de mitigación y las estrategias de protección de la metasuperficie se alinean con las investigaciones más recientes en metamateriales para propulsión eléctrica presentadas en el **IEPC 2024**. La adherencia estricta a este plan garantiza la integridad de la inversión en hardware y la obtención de datos científicos de alta fidelidad para la publicación en revistas de prestigio como el *Journal of Propulsion and Power*.

# **Guía de Simulación de Ingeniería: Fase 1 \- Proyecto MEI-RIT**

## **1\. Especificaciones Técnicas y Objetivos de Rendimiento**

La Fase 1 se centra en la validación computacional del propulsor MEI-RIT (*Metasurface-Enhanced Iodine RF Ion Thruster*). El diseño debe superar los estándares actuales de propulsión eléctrica para CubeSats, optimizando el acoplamiento electromagnético mediante el uso de metasuperficies sub-longitud de onda.

### **Tabla Comparativa de Rendimiento y Benchmarks**

| Especificación | ThrustMe NPT30-I2 (En vuelo) | Busek BIT-3 (Validado) | MEI-RIT (Objetivo Proyectado) |
| :---- | :---- | :---- | :---- |
| **Empuje (mN)** | 0.3 – 1.1 | 1.1 – 1.35 | 0.7 – 1.3 |
| **Impulso Específico (I\_{sp}) (s)** | \~2500 | 2150 – 3200 | 2300 – 2800 |
| **Eficiencia Total (%)** | 35 – 42 | 35 – 42 | 36 – 46 |
| **Potencia Nominal (W)** | 35 – 65 | 56 – 75 | 50 – 80 |
| **Ratio Empuje/Potencia (mN/kW)** | 14 – 17 | 15 – 22 | 16 – 22 |

### **Propiedades Físicas del Propelente (I\_2)**

Para la simulación multifísica de la cámara de descarga, se deben integrar los siguientes parámetros del yodo molecular:

* **Estado inicial:** Yodo sólido (sublimación controlada).  
* **Temperatura de sublimación operativa:** 80°C – 100°C para garantizar un flujo másico constante.  
* **Física de ionización:** Considerar un potencial de ionización menor que el del Xenón, lo que favorece la reducción del umbral de ignición bajo la intensificación de campo de la metasuperficie.

## **2\. Configuración Geométrica y Optimización MRCO v1.2**

La geometría del sistema no es arbitraria; se deriva directamente de los resultados de convergencia del algoritmo **MRCO v1.2** (Metasurface RF Coupling Optimizer).

### **Parámetros Derivados para la Metasuperficie**

Se debe construir el patrón periódico utilizando los siguientes valores nominales:

* **Periodo de la metasuperficie (\\Lambda):** 11.78 µm.  
* **Factor de llenado (fill factor):** 0.59.  
* **Espesor de la estructura metálica (h):** 3.32 µm.

### **Modelado del Sustrato y la Cámara**

* **Material Base:** Utilizar Cuarzo o Alúmina (Al\_2O\_3) como sustrato dieléctrico.  
* **Estrategia de Modelado:** Dado que la metasuperficie es un array periódico, se debe emplear un modelo de **Celda Unitaria (Unit Cell)** para optimizar los recursos computacionales, aplicando condiciones de periodicidad.

## **3\. Modelado Electromagnético (EM) en COMSOL/CST**

El objetivo es maximizar la eficiencia de transferencia de energía desde la antena hasta la zona de formación del plasma, minimizando las pérdidas de retorno.

### **Configuración del Módulo RF**

1. **Frecuencia de Operación:** Configurar el barrido en torno a 13.56 MHz (HF) o 2.45 GHz (Microondas), dependiendo de la arquitectura de la antena.  
2. **Condiciones de Contorno:** Implementar **Floquet Ports** para simular la incidencia de la onda sobre la metasuperficie periódica y capturar los modos de difracción superiores si fuera necesario.  
3. **Análisis de Parámetros S:** El criterio de éxito es la minimización del coeficiente de reflexión (S\_{11}). Se debe buscar un matching de impedancia que resulte en un S\_{11} \< \-20 dB en la frecuencia de resonancia.

### **Acoplamiento Sub-longitud de Onda**

* Configurar la metasuperficie para actuar como un transformador de impedancia entre la impedancia de la antena y la impedancia compleja del plasma.  
* Simular la distribución del campo eléctrico superficial para identificar puntos calientes de ionización.

## **4\. Simulación de la Física de Plasma y Dinámica de Yodo**

La simulación debe transitar de un modelo de vacío a uno con carga de plasma, considerando la interacción fluido-cinética del vapor de yodo.

### **Modelado del "Plasma Loading Effect"**

La presencia del plasma altera la permitividad efectiva del sistema. Según el modelo MRCO v1.2, se debe implementar matemáticamente la penalización de carga en la eficiencia de acoplamiento: \\text{Penalización}\_{\\text{plasma}} \= 1.0 \- 0.12 \\times \\left( \\frac{\\text{espesor}}{3.5} \\right)^2 Donde el espesor es el valor de 3.32 µm derivado de la optimización. Este factor debe compensarse en la red de matching para evitar el desajuste tras la ignición.

### **Consideraciones del Plasma de I\_2**

* **Longitud de Debye:** Asegurar que el mallado sea capaz de resolver la capa de Debye en las interfaces con la metasuperficie protegida.  
* **Uniformidad:** Validar que el campo intensificado por la metasuperficie genere un perfil de densidad electrónica espacialmente homogéneo, reduciendo la erosión localizada.  
* **Refinamiento Cuántico (Opcional):** El uso de algoritmos VQE (Qiskit) para el cálculo de energías de enlace se reserva para una fase de refinamiento atómico avanzada; para la Fase 1, los modelos de fluido de COMSOL son la prioridad técnica.

## **5\. Configuración de las Rejillas de Aceleración Iónica**

### **Especificaciones del Sistema de Doble Rejilla**

* **Material:** Molibdeno (Mo) o Grafito Pirolítico (para máxima resistencia a la corrosión química del I\_2).  
* **Potenciales Electrostáticos:**  
  * Rejilla de Pantalla (Screen Grid): 800 V a 1500 V.  
  * Rejilla de Aceleración (Accel Grid): \-150 V a \-300 V (para confinamiento electrónico).  
* **Objetivos de la Simulación:** Minimizar el impacto de iones (pulverización catódica) mediante el seguimiento de trayectorias iónicas y la optimización del espaciado entre rejillas.

## **6\. Modelado de la Capa Protectora ALD (Atomic Layer Deposition)**

Debido a la alta reactividad del plasma de yodo, los patrones conductores de la metasuperficie (Cobre o Aluminio) deben ser pasivados.

### **Integración de la Capa Dieléctrica**

* **Materiales:** Nitruro de Silicio (Si\_3N\_4) o Alúmina (Al\_2O\_3).  
* **Espesor ALD:** Configurar capas nanométricas consistentes con procesos de deposición de capas atómicas.  
* **Malla Computacional:** Es imperativo utilizar un **mallado sub-micrométrico** en las interfaces de la capa ALD para capturar correctamente los gradientes de campo y evitar inestabilidades numéricas.

### **Compensación de Capacitancia Parásita**

La introducción de la capa protectora altera la permitividad relativa (\\epsilon\_r) local, induciendo un desplazamiento en la frecuencia de resonancia. Este efecto debe modelarse como una capacitancia parásita adicional en el circuito equivalente de la simulación. El matching de impedancia debe recalcularse considerando el valor de \\epsilon\_r del material ALD seleccionado para evitar pérdidas de potencia por desintonización.

## **7\. Protocolo de Validación y Convergencia (KPIs)**

Para la validación exitosa de la Fase 1, se deben obtener y verificar los siguientes indicadores:

* **Eficiencia de Acoplamiento (Surrogate):** Valor objetivo cercano al **62%**, validando los resultados del modelo MRCO v1.2.  
* **Mejora de Acoplamiento RF:** Incremento verificado del **\+10-15%** en comparación con una cámara de descarga estándar (baseline) sin metasuperficie.  
* **Eficiencia Total del Propulsor:** Proyección multifísica de entre **36% y 46%**.  
* **Estabilidad Térmica:** La potencia reflejada (P\_{ref}) debe mantenerse estable frente a variaciones de temperatura de ±5°C en el sistema de sublimación de I\_2.  
* **Convergencia Numérica:** Residuos del modelo EM por debajo de 10^{-6} y convergencia del módulo de plasma dentro de los límites de estabilidad de la descarga.

# **Protocolo Técnico de Caracterización: Metasuperficie MEI-RIT (Fase 2\)**

## **1\. Objetivo del Protocolo**

Este documento define los procedimientos de metrología avanzada y validación experimental para la metasuperficie MEI-RIT tras su microfabricación en la sala blanca del **IMB-CNM-CSIC**. El objetivo es certificar que el componente cumple con las tolerancias críticas dictadas por el modelo **MRCO v1.2** para garantizar el acoplamiento óptimo de radiofrecuencia (RF) en el propulsor de yodo. Este protocolo constituye el hito final de la **Fase 2**, autorizando la transición a las pruebas de ignición en cámara de vacío.

## **2\. Especificaciones de Diseño y Valores de Referencia (Ground Truth)**

Los parámetros listados a continuación representan el estado de diseño óptimo tras la convergencia del algoritmo **MRCO v1.2**. Cualquier desviación fuera de los márgenes de tolerancia en estas métricas invalidará la pieza para su uso en la Fase 3\.

| Parámetro de Diseño | Especificación MRCO v1.2 | Referencia de Material |
| :---- | :---- | :---- |
| **Periodo de la metasuperficie** | 11.78 µm | Patrón de Cobre o Aluminio |
| **Factor de Llenado (Fill Factor)** | 0.59 | Geometría del resonador |
| **Espesor del Recubrimiento (ALD)** | 3.32 µm | Nitruro de Silicio / Alúmina |
| **Sustrato Dieléctrico** | Cuarzo / Alúmina | Baja pérdida tangencial |
| **Eficiencia de Acoplamiento (Modelo)** | \~61.5% | Mejora de \+10-15% vs Baseline |

## **3\. Inspección mediante Microscopía Electrónica de Barrido (SEM)**

Dada la naturaleza aislante de los sustratos (cuarzo/alúmina), el operador debe extremar las precauciones para evitar el efecto de carga (*charging*).

### **Instrucciones Operativas:**

1. **Configuración de Columna:** Operar a bajo voltaje de aceleración (**1-2 kV**) para mitigar la acumulación de carga. En caso de inestabilidad de imagen, aplicar una capa nanométrica (flash-coat) de oro o carbono.  
2. **Morfología y Residuos:** Inspeccionar visualmente la transición entre el patrón metálico y el sustrato. Verificar la ausencia de subgrabado (*undercutting*) o "scalloping" en las paredes verticales, así como de residuos de resina de litografía o etching.  
3. **Medición Estadística:**  
   * Medir el periodo (P \= 11.78 µm) en **cinco puntos críticos** de la oblea (centro y cuatro cuadrantes periféricos).  
   * Calcular el factor de llenado real mediante segmentación de imagen (objetivo: 0.59).  
4. **Uniformidad:** Calcular la desviación estándar (\\sigma) de las medidas. La homogeneidad es vital para prevenir gradientes de densidad de plasma no deseados.

## **4\. Análisis por Microscopía de Fuerza Atómica (AFM)**

La validación de la capa protectora depositada mediante Deposición de Capas Atómicas (ALD) es crítica para la supervivencia del hardware frente a la corrosión química del yodo y el bombardeo iónico.

### **Instrucciones Operativas:**

* **Espesor de Paredes:** Realizar perfiles de línea para medir el espesor total (objetivo: 3.32 µm). Es imperativo verificar el **step coverage**; el espesor en los flancos (*sidewalls*) de las estructuras debe ser conforme y continuo respecto a la superficie superior.  
* **Rugosidad Superficial (RMS):** Cuantificar la rugosidad media cuadrática en áreas de 5x5 µm.  
* **Requisitos de Calidad Superficial:**  
  * **RMS \< 5 nm:** Una rugosidad superior incrementa la tasa de erosión y facilita la nucleación de contaminantes.  
  * **Integridad del Encapsulado:** Ausencia total de delaminación o porosidad visible que pueda exponer el cobre/aluminio subyacente al plasma de yodo.

## **5\. Test de Caracterización de Radiofrecuencia (RF)**

Esta prueba valida la capacidad de la metasuperficie para actuar como transformador de impedancia sub-longitud de onda.

### **Configuración del Test:**

1. **Medida de Control (Baseline):** Medir el coeficiente de reflexión (S\_{11}) utilizando un Analizador de Redes Vectoriales (VNA) en la cámara de descarga **vacía** (sin metasuperficie).  
2. **Medida con Metasuperficie:** Instalar el componente y repetir la medición bajo las mismas condiciones de potencia y presión.  
3. **Frecuencias de Operación:**  
   * **13.56 MHz:** Validación del acoplamiento en régimen inductivo para optimización de densidad.  
   * **2.45 GHz:** Evaluación del comportamiento en régimen de microondas y minimización de pérdidas dieléctricas.  
4. **Cálculo de Mejora:** Comparar la potencia absorbida estimada. El objetivo es validar una reducción en la potencia reflejada que se traduzca en una mejora del **\+10-15%** en la eficiencia de acoplamiento respecto al baseline.

## **6\. Criterios de Aceptación Técnica para Transición a Fase 3**

Solo los componentes que cumplan estrictamente con los umbrales de la siguiente tabla serán autorizados para su integración en el prototipo MEI-RIT.

| Parámetro | Umbral de Aceptación (Go/No-Go) | Método de Verificación |
| :---- | :---- | :---- |
| **Periodo y Espesor ALD** | Nominal ±5% | SEM / AFM |
| **Uniformidad Dimensional** | \\sigma \< 2\\% en los 5 puntos de control | Análisis Estadístico |
| **Rugosidad RMS** | \< 5 nm | AFM |
| **Integridad Estructural** | Cero porosidad, grietas o delaminación | SEM / Inspección Visual |
| **Eficiencia de Acoplamiento** | \> 60\\% (o mejora relativa \> 10\\%) | VNA (S\_{11}) |

**Cierre del Protocolo:** El cumplimiento de estos criterios técnicos certifica la robustez de la metasuperficie frente al entorno reactivo del propulsor. Una vez firmado el reporte de conformidad, se procederá al ensamblaje del sistema de aceleración de rejillas y al inicio de las pruebas de empuje en vacío (Fase 3).

# **Protocolo de Caracterización Técnica de Metasuperficies MEI-RIT**

## **1\. Objetivos y Alcance del Manual**

Este documento define el procedimiento operativo estándar para la validación metrológica y funcional de las metasuperficies tras su fabricación en la sala blanca del IMB-CNM-CSIC. El objetivo es certificar que el componente cumple con las especificaciones del modelo **MRCO v1.2** para su integración en el propulsor **MEI-RIT** (*Metasurface-Enhanced Iodine RF Ion Thruster*).

La metasuperficie tiene la función crítica de optimizar el acoplamiento de potencia de radiofrecuencia (RF) y garantizar la uniformidad del plasma en la cámara de descarga. Dado que el yodo es un propelente altamente corrosivo, la validación no solo debe ser geométrica, sino también de integridad química mediante capas de pasivación avanzadas.

## **2\. Especificaciones Nominales de Diseño (Modelo MRCO v1.2)**

Los parámetros derivados del algoritmo de optimización *surrogate* MRCO v1.2 representan el estado de diseño óptimo para maximizar la eficiencia de acoplamiento.

### **Tabla 1: Parámetros de Referencia para Caracterización**

| Parámetro | Valor Nominal | Unidad | Observaciones |
| :---- | :---- | :---- | :---- |
| Periodo Óptimo (P) | 11.78 | µm | Validación mediante CD-SEM |
| Factor de Llenado (*Fill factor*) | 0.59 | \- | Tolerancia crítica para resonancia |
| Espesor de la Metasuperficie | 3.32 | µm | Verificación mediante perfilometría |
| Frecuencias de Operación | 13.56 / 2.45 | MHz / GHz | Bandas ISM de interés |
| Eficiencia de Acoplamiento (Modelo) | \~60.2 | % | Mejora proyectada del 10-15% |

## **3\. Inspección Estructural mediante SEM (Microscopía Electrónica de Barrido)**

La inspección de Microelectrónica mediante SEM debe validar la fidelidad del patrón transferido y la ausencia de residuos de procesado.

**Procedimiento de Medición:**

1. **Medición de Dimensiones Críticas (CD-SEM):** Evaluar el periodo (11.78 µm) y el ancho de las pistas en cinco puntos del sustrato para calcular el *Etch Bias*.  
2. **SEM de Corte Transversal (X-SEM):** Preparar una muestra testigo o realizar un corte por FIB para verificar la verticalidad de las paredes laterales (*sidewalls*). El ángulo de ataque debe ser de 90° ± 2° para evitar degradación en el acoplamiento RF.  
3. **Análisis EDX (Energy Dispersive X-ray):** Realizar un mapeo elemental para confirmar la eliminación total de la fotorresina y la ausencia de subproductos de la técnica RIE (Reactive Ion Etching).

**Puntos Críticos de Inspección Visual:**

* **Rugosidad de Bordes (LER):** Una rugosidad excesiva en los bordes metálicos puede inducir puntos calientes y arcos eléctricos en presencia de plasma.  
* **Integridad del Array:** Ausencia de puentes metálicos ("shorts") o discontinuidades que alteren la inductancia efectiva de la metasuperficie.

## **4\. Análisis Topográfico y de Recubrimiento mediante AFM y Perfilometría**

Debido a que el espesor nominal de 3.32 µm supera el rango de linealidad óptimo de muchos sistemas AFM estándar, se requiere un enfoque híbrido.

**Metodología de Validación:**

1. **Perfilometría de Contacto (Dektak):** Medir el *Step Height* en los bordes del patrón para validar el espesor total de 3.32 µm. Es esencial para confirmar la tasa de deposición/etching en estructuras de alto aspecto.  
2. **AFM (Microscopía de Fuerza Atómica):** Utilizado exclusivamente para medir la rugosidad RMS superficial y el ángulo de inclinación en la base de las estructuras.  
3. **Evaluación de Conformidad ALD:** Verificar que la capa de pasivación (Nitruro de Silicio o Alúmina) depositada por ALD (*Atomic Layer Deposition*) mantenga un *Conformality Ratio* superior al 95% en las paredes laterales.

**Contexto de Protección Química:** El recubrimiento ALD es la única barrera contra el plasma de yodo. Cualquier porosidad o defecto de cobertura (*pinhole*) resultará en la corrosión inmediata del metal conductor por la reactividad del I₂, invalidando el componente para vuelos de larga duración.

## **5\. Caracterización Electromagnética y Test RF**

La validación final se realiza mediante la respuesta en frecuencia del componente bajo condiciones controladas de laboratorio.

**Montaje Experimental y Calibración:**

* **Calibración del VNA:** El Analizador de Redes Vectoriales debe ser calibrado utilizando protocolos TOSM (*Through-Open-Short-Match*) o TRL para asegurar que el plano de referencia esté en la interfaz de la metasuperficie.  
* **Medición del Factor Q:** Determinar el factor de calidad de la resonancia de la metasuperficie. Una desviación significativa del Q-factor nominal indica pérdidas dieléctricas excesivas o desviaciones en el factor de llenado (0.59).

**Protocolo de Prueba:**

1. **Cold Test (Sin Plasma):** Medición de los parámetros S (S11/S21) para verificar el *matching* de impedancia a 13.56 MHz y 2.45 GHz.  
2. **Validación de Mejora:** Comparar la eficiencia de acoplamiento medida contra una cámara de descarga baseline. El éxito se define por alcanzar una mejora del 10-15% en el acoplamiento de potencia.

## **6\. Criterios de Aceptación Técnica (Pass/Fail)**

La metasuperficie debe cumplir estrictamente con los límites de tolerancia para garantizar la estabilidad del plasma.

### **Tabla 2: Límites de Tolerancia y Criterios de Éxito**

| Parámetro | Valor Nominal | Tolerancia Permitida | Gravedad del Defecto |
| :---- | :---- | :---- | :---- |
| Periodo (P) | 11.78 µm | ± 1% | Mayor (Desfase RF) |
| Factor de Llenado | 0.59 | ± 3% | Crítico (Fallo de Resonancia) |
| Espesor Total | 3.32 µm | ± 3% | Mayor (Pérdidas de Conducción) |
| Integridad ALD | Continuidad Total | **Cero Pinholes** | **Crítico (Fallo Catastrófico)** |
| Ángulo de Pared | 90° | ± 2° | Menor |

**Nota de Seguridad:** Cualquier signo de delaminación de la capa ALD o presencia de contaminantes orgánicos tras el análisis EDX implica el rechazo inmediato del lote (FAIL) debido a la reactividad extrema del yodo.

## **7\. Firma y Responsabilidades**

Protocolo validado para su ejecución en las instalaciones de caracterización de materiales del IMB-CNM-CSIC.

**Responsable Técnico:** Lázaro López Paz (Prat de Llobregat, Barcelona). **Consultoría de Optimización:** gork (xAI). **Versión del Protocolo:** v1.2 (Basado en Modelo MRCO v1.2). **Fecha de Referencia:** Julio 2026\.

# **Agenda Operativa: Inicio de Simulaciones Multifísicas MEI-RIT (Fase 1 \- Semana 1\)**

**Emisor:** Ingeniero Jefe de Propulsión Eléctrica / Especialista en Simulación Multifísica **Referencia:** Protocolo de Validación MRCO v1.2

Esta agenda define las directrices técnicas de cumplimiento obligatorio para la validación computacional del propulsor MEI-RIT. No se tolerarán desviaciones de los parámetros de diseño ni simplificaciones en los modelos físicos sin previa autorización de esta jefatura. El objetivo es consolidar el modelo de fidelidad ultra-alta para el acoplamiento RF mediante metasuperficies antes del paso a fabricación en sala blanca.

### **1\. Directrices Generales y Parámetros de Diseño Críticos**

Toda simulación debe ejecutarse sobre la base de los resultados obtenidos por el algoritmo de optimización MRCO v1.2. Se prohíbe el uso de parámetros de versiones anteriores (v1.0).

**Parámetros Innegociables de Diseño (Ground Truth):**

| Parámetro | Valor Nominal | Tolerancia / Observación |
| :---- | :---- | :---- |
| Periodo de la Metasuperficie | 11.78 µm | Estrictamente sub-longitud de onda |
| Espesor de la Estructura | 3.32 µm | Optimizado para blindaje y acoplamiento |
| Factor de Llenado (Fill Factor) | 0.59 | Relación material/vacío del array |
| Voltaje de Rejillas (V\_acc) | 800 V \- 1500 V | Barrido paramétrico obligatorio |
| Frecuencia Operativa | 13.56 MHz / 2.45 GHz | Estándar industrial RF |

**Entorno de Simulación:**

* **Solvers:** COMSOL Multiphysics / CST Studio Suite.  
* **Configuración de Nodos:** Módulos de Electromagnetismo (EM) y Plasma (Low-temperature).

### **2\. Lunes: Configuración de Geometría y Refinamiento de Mallado**

**Importación y Preparación CAD:**

* Ejecutar "defeaturing" agresivo en el modelo de la cámara (10x10 cm), eliminando roscas y detalles mecánicos \< 500 µm que no afecten el transporte de partículas.  
* **Requisito de Mallado Especialista:** Se ordena la creación obligatoria de capas de **malla de contorno (Boundary Layer Mesh)** de alta densidad en la interfaz plasma-pared y plasma-rejilla. Se exige un mínimo de 5 elementos dentro de la zona de la vaina (sheath) para capturar la condición de Bohm con precisión sub-milimétrica.

**Definición de Materiales y ALD:**

* **Cámara:** Alúmina (Al\_2O\_3) o Cuarzo de alta pureza.  
* **Aceleración:** Molibdeno (Mo) o Grafito Pirolítico.  
* **Propelente:** Propiedades de Yodo sólido (I\_2) para sublimación controlada (80-100°C).  
* **Capa ALD:** Implementar mediante el comando "Thin Film", configurando el blindaje químico necesario para proteger la metasuperficie de la corrosión por yodo.

### **3\. Martes: Modelado Electromagnético de la Metasuperficie (EM)**

**Configuración del Análisis de Ondas Completas:**

* **Solver Requerido:** *Frequency Domain / Perturbation*.  
* Aplicar condiciones de contorno periódicas (Floquet) con el periodo exacto de **11.78 µm**.

**Validación del Factor de Frecuencia:**

* Se ordena realizar un barrido del **"Frequency Factor"** en el rango **\[0.7 \- 1.4\]** derivado del modelo subrogado. Esto es crítico para validar el pico de resonancia y asegurar que el acoplamiento coincida con los estándares de 13.56 MHz o 2.45 GHz bajo condiciones de carga real.  
* **Objetivo de Rendimiento:** Confirmar una mejora del \+10-15% en la eficiencia de acoplamiento respecto a la cámara sin metasuperficie.

### **4\. Miércoles: Física de Plasma y Barrera de Transporte**

**Integración Multifísica:**

* **Solver Requerido:** *Time-Dependent / Segregated*.  
* Modelar la cinética de ionización del yodo, evaluando la **ionización disociativa** para distinguir entre poblaciones de iones atómicos (I^+) y moleculares (I\_2^+).

**Modelado de Transporte Anómalo y Barrera (Logic Cheng & Martinez-Sanchez):**

* Implementar el coeficiente de Bohm (K\_B) en el rango de 0.15 \- 0.20.  
* **Prescripción Manual:** Se debe imponer manualmente una **Barrera de Transporte (Transport Barrier)** en el rango axial donde se apaga la difusión anómala (Bohm quenching). Esto evitará la sobrepredicción del flujo hacia las paredes y ajustará el perfil de densidad iónica a los datos experimentales de propulsores de bajo poder.

### **5\. Jueves: Óptica de Iones y Neutralización**

**Simulación del Sistema de Rejillas:**

* Protocolo de dos rejillas (Screen y Accelerator).  
* **Inclusión de Neutralizador:** Es obligatorio modelar una fuente de **emisión secundaria de electrones** para simular la neutralización del haz. Esto es imperativo para prevenir el "spacecraft charging" y el retorno de iones hacia el domo de la cámara en el dominio de vacío.

**Barrido Paramétrico de Rejillas:**

| Variable | Rango | Paso | Impacto en FOM (Figure of Merit) |
| :---- | :---- | :---- | :---- |
| Voltaje Acelerador | 800 V \- 1500 V | 100 V | Optimización de trayectoria y Isp |
| Corriente de Descarga | 0.5 A \- 2.5 A | 0.25 A | Eficiencia de utilización de masa |
| Presión de Cámara | 10⁻³ \- 10⁻² mbar | Log | Estabilidad de la descarga y empuje |

### **6\. Viernes: Modelado de Erosión y Validación de Ciclo de Vida**

**Implementación del Modelo de Sputtering Yamamura:**

* **Parámetro Crítico:** El script de pulverización debe utilizar el **exponente de ajuste revisado de 0.474** (según el modelo de Cheng para BN) en lugar del estándar 0.5. Esto garantiza que el régimen de baja energía característico de los iones de yodo no sea subestimado.  
* Umbral de pulverización (E\_{th}): **30 eV**.

**Informe de Cierre de Semana 1:** La entrega final debe comparar los resultados simulados con los KPIs innegociables del proyecto:

| KPI | Objetivo MEI-RIT |
| :---- | :---- |
| Empuje (Thrust) | 0.7 – 1.3 mN |
| Impulso Específico (Isp) | 2300 – 2800 s |
| **Thrust-to-Power** | **16 – 22 mN/kW** |
| Mejora Eficiencia Metasuperficie | \+10-15% vs Baseline |

### **7\. Control de Calidad y Registro de Logs**

Queda prohibida la entrega de resultados sin su correspondiente respaldo de convergencia.

1. **Log de Errores:** Documentar el error residual en cada paso de tiempo del solver segregado.  
2. **Tiempos de Computación:** Registrar el uso de recursos por cada nodo de simulación.  
3. **Formato de Salida:** Solo se aceptará texto estructurado y tablas Markdown. No se procesarán informes que contengan capturas de pantalla sin metadatos técnicos asociados.

# **Informe de Validación Técnica: Resultados Proyectados y Modelado del Propulsor MEI-RIT (Fase 1\)**

### **1\. Definición y Alcance del Proyecto MEI-RIT**

El propulsor MEI-RIT (*Metasurface-Enhanced Iodine RF Ion Thruster*) representa una evolución en la propulsión eléctrica de estado sólido para SmallSats. A diferencia de los propulsores iónicos de radiofrecuencia convencionales, el MEI-RIT integra una metasuperficie de sub-longitud de onda dentro de la cámara de descarga que actúa como una **guía de onda revestida (cladded waveguide)**. Este diseño permite controlar de forma precisa la propagación electromagnética y reducir la frecuencia de corte (*cutoff frequency*), facilitando el desarrollo de cámaras de descarga extremadamente compactas sin sacrificar la eficiencia de ionización. El sistema utiliza yodo sólido como propelente, el cual se sublima mediante un sistema de gestión térmica de bajo consumo, eliminando la necesidad de tanques de alta presión.

**Innovaciones clave del sistema:**

* **Metasuperficie de Acoplamiento:** Estructura periódica que optimiza la transferencia de energía RF al plasma y mejora la uniformidad del perfil de densidad electrónica, mitigando los gradientes que degradan las rejillas.  
* **Propelente de Yodo Sólido:** Alternativa de alta densidad (almacenamiento \~4.9 g/cm³) que reduce los costes de combustible en un factor de 100 respecto al xenón y permite una integración simplificada en CubeSats.  
* **Acoplamiento RF Avanzado:** Coordinación entre la antena y la metasuperficie para operar a 13.56 MHz o 2.45 GHz, diseñada para compensar activamente el efecto de carga del plasma (*plasma loading*).

### **2\. Estado del Arte y Referencias de Vuelo**

Para contextualizar el rendimiento del MEI-RIT, se comparan sus objetivos con sistemas de yodo validados en órbita y en laboratorio:

| Propulsor | Empuje (mN) | Isp (s) | Potencia (W) | Estado de Vuelo |
| :---- | :---- | :---- | :---- | :---- |
| **ThrustMe NPT30-I2** | 0.3 – 1.1 | 2500 | 55 | Operativo (en órbita desde 2021\) |
| **Busek BIT-3** | 1.1 – 1.35 | 2150 – 3200 | 56 – 75 | Validado (misiones CubeSat) |
| **MEI-RIT (Objetivo Fase 1\)** | 0.7 – 1.3 | 2800 | 50 – 80 | Fase de Validación Numérica |

### **3\. Valores Teóricos de Referencia para la Validación (Ground Truth)**

Como Ingeniero Senior, establezco los siguientes "Golden Values" que actuarán como base para la validación de las simulaciones multifísicas. Es imperativo distinguir entre el límite asintótico y el umbral de validación operativa:

* **Eficiencia Total Teórica (Meta):** 62% (Objetivo de diseño a largo plazo).  
* **Eficiencia Total de Validación (Baseline):** 35 – 45% (Rango realista basado en el estado del arte actual).  
* **Rango de Empuje (Thrust):** 0.7 – 1.3 mN.  
* **Impulso Específico (Isp):** 2800 s.  
* **Relación Empuje-Potencia:** 16 – 22 mN/kW.  
* **Umbral de Energía de Impacto (Erosión):** 30 eV (Límite crítico para el bombardeo iónico en paredes de BN).

### **4\. Resultados del Algoritmo de Optimización MRCO v1.2**

Los resultados obtenidos mediante el modelo *Metasurface RF Coupling Optimizer* (MRCO v1.2) sirven como parámetros de entrada para la validación en COMSOL. Estos valores provienen de un **modelo surrogate** que debe ser verificado mediante simulación de onda completa. Se introduce el *Frequency Factor* como variable crítica para garantizar la resonancia bajo carga de plasma.

**Parámetros Optimizados:** | Parámetro | Valor | Descripción | | :--- | :---: | :--- | | **Periodo Óptimo** | 11.78 μm | Espaciado de la estructura sub-longitud de onda. | | **Factor de Llenado** | 0.59 | Relación metal/dieléctrico en la celda unidad. | | **Espesor** | 3.32 μm | Altura de la estructura de la metasuperficie. | | **Frequency Factor** | 1.0 | Factor de sintonía para coincidencia de fase (Target). | | **Mejora Proyectada** | \+10 – 15% | Incremento de eficiencia vs. cámara estándar. |

### **5\. Marco de Simulación Multifísica (COMSOL/CST)**

La Fase 1 debe ejecutar un flujo de trabajo que integre la interacción plasma-metasuperficie con alta fidelidad:

1. **Configuración de Materiales y Dieléctricos:** Definir el sustrato (Cuarzo o Alúmina) incorporando sus respectivas tangentes de pérdidas. La metasuperficie debe modelarse como una capa de transición con conductividad compleja.  
2. **Configuración EM y Efecto de Carga:** Modelar la antena RF y la metasuperficie. Es crítico simular el **plasma loading effect**, verificando si el aumento de la densidad electrónica desplaza el pico de resonancia de la metasuperficie fuera de la frecuencia operativa del generador.  
3. **Cinética de Iones de Yodo:** Implementar un modelo de fluidos o PIC que rastree explícitamente las poblaciones de **iones atómicos (I^+)** e **iones moleculares (I\_2^+)**. Se debe reportar la tasa de disociación, ya que la relación carga-masa de I\_2^+ reduce significativamente el Isp efectivo.  
4. **Sistema de Rejillas y Aceleración:** Modelado de rejillas de molibdeno o grafito. Aplicar voltajes de extracción de 800 V a 1500 V y medir la transparencia iónica.  
5. **Validación de Transmisión:** Verificar que la metasuperficie, actuando como guía de onda revestida, mantiene la uniformidad del plasma en el plano de la rejilla de pantalla dentro de un margen del 10%.

### **6\. Modelado Molecular del Yodo y Consideraciones Cuánticas**

La disociación del yodo (I\_2 \\rightarrow I \+ I^+) es un proceso energético fundamental que dicta la eficiencia de masa del propulsor. Para capturar la energía de disociación y el acoplamiento molecular en presencia de campos RF intensos, se utiliza el algoritmo VQE (*Variational Quantum Eigensolver*). Este enfoque es vital para modelar el pozo de potencial molecular del yodo, considerando el **acoplamiento espín-órbita**, esencial dada la naturaleza pesada del átomo de yodo.

**Estructura del Hamiltoniano para el estudio de acoplamiento:**

\# Representación del Hamiltoniano molecular para el enlace I-I  
\# H \= H\_kinetic \+ H\_electronic\_potential \+ H\_spin\_orbit

\# El término H\_spin\_orbit es mandatorio para el yodo debido a efectos relativistas  
\# VQE minimiza \<psi|H|psi\> para hallar la energía de disociación exacta   
\# bajo la influencia del campo local de la metasuperficie.

Hamiltonian\_Terms \= {  
    "Kinetic": "Energía cinética de los núcleos y electrones",  
    "Electronic\_Potential": "Interacción de Coulomb en el pozo de potencial",  
    "Spin\_Orbit": "Acoplamiento relativista para átomos de Z elevado (Yodo)"  
}

### **7\. Protocolo de Validación de Resultados (Primera Semana)**

El analista debe completar este checklist de comandos activos para validar el modelo frente al "Ground Truth":

* \[ \] **Comando de Erosión:** Comparar el flujo iónico incidente en las paredes de la cámara frente al umbral de pulverización (*sputtering*) de **30 eV** (basado en el modelo de validación de Nitruro de Boro de los estudios BHT-200/600).  
* \[ \] **Verificación de Empuje:** Confirmar que el empuje calculado está en el rango 0.7 – 1.3 mN para una potencia neta de 50-80 W.  
* \[ \] **Balance de Carga del Sistema:** Verificar que la tasa de emisión de electrones del neutralizador coincida exactamente con la corriente del haz iónico para evitar la carga electrostática del satélite.  
* \[ \] **Consistencia de Eficiencia:** Validar que la eficiencia de acoplamiento RF en COMSOL no desvíe más de un 5% respecto a los resultados del modelo surrogate MRCO v1.2.  
* \[ \] **Análisis de Población Iónica:** Reportar el ratio I^+ / I\_2^+ y su impacto en el Isp nominal.

### **8\. Cronograma de la Fase 1 y Presupuesto Asociado**

La Fase 1 se ejecutará en un periodo de 3 meses, centrada en la validación numérica previa al prototipado físico en el **IMB-CNM-CSIC**.

**Plan de Trabajo (Meses 1-3):**

* **Mes 1:** Diseño de arquitectura EM y modelado inicial de la metasuperficie.  
* **Mes 2:** Integración de la física de plasma de yodo (atómico/molecular) y optimización MRCO.  
* **Mes 3:** Validación multifísica final, análisis de erosión BN y entrega del informe de diseño.

**Desglose de Costos (Fase 1):**

| Concepto | Estimación (€) |
| :---- | :---- |
| Personal de Ingeniería Senior (Diseño y Simulación) | 9.000 – 12.000 |
| Licencias de Software (COMSOL Multiphysics / CST) | 2.500 – 4.000 |
| Infraestructura IT e infraestructura de acceso (IMB-CNM-CSIC) | 1.500 – 2.500 |
| **Total Estimado Fase 1** | **13.000 – 18.500** |

# **Especificaciones Técnicas y Parámetros de Simulación: Propulsor MEI-RIT**

Este documento establece el marco técnico de referencia y la lista maestra de variables para el modelado multifísico del propulsor **MEI-RIT** (*Metasurface-Enhanced Iodine RF Ion Thruster*). Los parámetros aquí definidos integran los resultados de optimización del algoritmo **MRCO v1.2**, datos de vuelo de sistemas de propulsión de yodo (ThrustMe/Busek) y configuraciones avanzadas para la implementación en **COMSOL Multiphysics**.

## **1\. Definición de Constantes Globales del Modelo**

Las siguientes constantes rigen el entorno de simulación y el régimen de operación nominal. Se debe asegurar la consistencia dimensional en el nodo *Global Definitions*.

| Nombre del Parámetro | Valor / Unidad | Descripción |
| :---- | :---- | :---- |
| **f\_RF** | 13.56 \[MHz\] | Frecuencia de operación de la antena de excitación. |
| **P\_design** | 50 – 80 \[W\] | Potencia de diseño para el acoplamiento inductivo/metasuperficial. |
| **T\_sub** | 353.15 – 373.15 \[K\] | Temperatura de sublimación del yodo (80-100 °C). |
| **P\_chamber** | \< 1e-6 \[mbar\] | Presión base de la cámara de vacío para condiciones de contorno. |
| **eta\_target** | 0.65 | Eficiencia de acoplamiento de potencia RF objetivo. |

## **2\. Propiedades Físico-Químicas del Propelente (Yodo)**

Para un modelado cinético preciso en el módulo de plasma, se deben definir las siguientes propiedades atómicas y moleculares. Se requiere la inclusión de especies secundarias para capturar los efectos de erosión por bombardeo iónico.

* **Masa Molecular del Yodo (I\_2):** 253.808 \[amu\].  
* **Masa Atómica del Yodo (I):** 126.904 \[amu\].  
* **Primer Potencial de Ionización (E\_{iz,mol}):** \~9.31 \[eV\] para I\_2.  
* **Primer Potencial de Ionización (E\_{iz,atom}):** \~10.45 \[eV\] para I.  
* **Segunda Ionización (I^{++}):** Parámetro esencial para modelos de longevidad; el impacto de iones doblemente cargados es el principal motor de la erosión en las rejillas y paredes.  
* **Secciones Eficaces:** Se deben importar sets de datos para **disociación molecular**, **ionización por impacto electrónico** y **intercambio de carga (CEX)** basados en el estado del arte de Busek.

## **3\. Parámetros Geométricos de la Metasuperficie (MRCO v1.2)**

La arquitectura de la metasuperficie representa una evolución desde la versión v1.0 (periodo de 12.5 µm). La versión **v1.2** ha sido ajustada para compensar el *plasma loading* y mejorar la estabilidad de frecuencia.

ESTRUCTURA MRCO v1.2:  
\- Periodo de la celda unidad (p\_meta): 11.78 \[um\]  
\- Factor de llenado (fill\_factor): 0.59  
\- Espesor de la capa resonante (t\_layer): 3.32 \[um\]  
\- Rango de barrido paramétrico: 8.5 \[um\] a 17 \[um\]  
\- Mejora de acoplamiento esperada: \+10-15% vs baseline

## **4\. Especificaciones de Materiales y Recubrimiento Dieléctrico (ALD)**

La cámara de descarga utiliza un sustrato de baja pérdida con un recubrimiento protector mediante deposición de capas atómicas (**ALD**) para prevenir la corrosión por yodo.

| Material | Función | Permitividad Relativa (\\epsilon\_r) | Tangente de Pérdidas (\\tan \\delta) |
| :---- | :---- | :---- | :---- |
| **Cuarzo** | Sustrato de Cámara | 3.75 | \< 0.0001 |
| **Alúmina (Al\_2O\_3)** | Sustrato Alternativo | 9.80 | \< 0.0002 |
| **Nitruro de Silicio (Si\_3N\_4)** | Capa ALD (nm) | 7.50 | 0.0010 |
| **Nitruro de Boro (BN)** | Paredes/Aislantes | 4.00 | 0.0005 |

*Nota: Mientras que la metasuperficie tiene un espesor micrométrico (3.32 µm), las capas de ALD se modelan como "Transition Boundary Conditions" de espesor nanométrico para optimizar la malla.*

## **5\. Configuración de Rejillas y Condiciones de Contorno de Aceleración**

El sistema de extracción se define mediante un par de rejillas de alta precisión (Screen y Accelerator).

1. **Materiales de Electrodo:** **Molibdeno** o **Grafito Pirolítico** (seleccionados por su baja tasa de pulverización catódica).  
2. **Voltaje de Rejilla de Pantalla (V\_screen):** 800 \[V\] – 1500 \[V\] (Potencial positivo para definir la energía del haz).  
3. **Voltaje de Rejilla de Aceleración (V\_accel):** \-150 \[V\] – \-300 \[V\] (Potencial negativo para prevenir el retroceso de electrones).  
4. **Métricas de Rendimiento:**  
   * **Empuje (T):** 0.7 – 1.3 \[mN\].  
   * **Impulso Específico (I\_{sp}):** 2300 – 2800 \[s\].

## **6\. Variables de Control de Erosión y Longevidad (Moving Mesh)**

Para simular el desgaste de los componentes cerámicos y metálicos, se implementa una lógica de **Malla Móvil (ale)** basada en el umbral de pulverización (sputter threshold).

* **Umbral de Pulverización (E\_{th}):** 30 \[eV\] para Nitruro de Boro y Molibdeno.  
* **Lógica de Desplazamiento de Malla:** La velocidad normal de retroceso de la pared (v\_n) se define como: v\_n \= \\frac{j\_{ion} \\cdot S(E, \\theta)}{\\rho\_{wall}} donde j\_{ion} es el flujo iónico, S es el rendimiento de sputtering (función de energía y ángulo) y \\rho\_{wall} la densidad del material.  
* **Time-stepping:** Se recomienda un esquema de desacoplamiento temporal. El plasma se resuelve en microsegundos, mientras que la geometría se actualiza en pasos discretos de 100 horas virtuales.

## **7\. Instrucciones para la Implementación en COMSOL Multiphysics**

Como ingeniero de simulación, proceda con la configuración siguiendo estrictamente esta jerarquía de interfaces:

1. **Configuración de Especies:** En la interfaz de **Plasma (arp)** o **Heavy Species Transport**, defina nodos específicos para electrones (e^-), iones monovalentes (I^+) e iones divalentes (I^{++}).  
2. **Aproximación de Deriva-Difusión:** Utilice la aproximación de *Drift-Diffusion* para el transporte de especies cargadas y configure la **EEDF** como *Maxwellian* para el régimen de 13.56 MHz en este rango de presiones.  
3. **Definiciones Globales:** Ingrese todas las variables en `Global Definitions > Parameters` con su unidad correspondiente entre corchetes, por ejemplo:  
   * `f_rf = 13.56[MHz]`  
   * `p_meta = 11.78[um]`  
   * `V_grid = 1200[V]`  
4. **Acoplamiento Multifísico:** Vincule la interfaz de **Magnetic Fields (mf)** con la interfaz de **Plasma** para modelar la corriente inducida a través de la metasuperficie.  
5. **Simulación de Vida Útil:** Añada la interfaz **Moving Mesh (ale)**. Defina una "Prescribed Normal Velocity" en las fronteras de las rejillas y paredes internas utilizando la variable de tasa de sputtering calculada a partir del flujo de I^+ e I^{++}.

# **Protocolo Técnico de Resolución de Errores Numéricos: Proyecto MEI-RIT**

## **1\. Configuración Avanzada del Solver para Plasmas No Lineales de Yodo**

El modelado de la descarga de yodo (I\_2) presenta una alta no-linealidad debido a la química de disociación y la naturaleza electronegativa del plasma. Se debe configurar un solucionador segregado (*segregated solver*) en COMSOL Multiphysics para gestionar el acoplamiento entre las interfaces *Electromagnetic Waves, Frequency Domain (ewfd)* y *Plasma (plas)*.

### **1.1. Jerarquía de Pasos y Configuración del Estudio**

Para asegurar la convergencia en el rango de potencia de 50-80 W, se prescribe un estudio de tipo **Frequency-Stationary** o **Frequency-Transient**, priorizando el equilibrio de carga en un plasma electronegativo (I\_2, I^+, I^-, e^-).

1. **Paso 1: Interfaz ewfd (13.56 MHz):** Resolución inicial del campo electromagnético de RF. Este paso establece el perfil de deposición de potencia (*electron heat source*) basado en la conductividad inicial del plasma.  
2. **Paso 2: Interfaz plas (Transporte de Especies):** Resolución de las densidades de especies neutras y cargadas. Es imperativo incluir la densidad de iones negativos (I^-) en la ecuación de Poisson para el balance de carga, dada la alta afinidad electrónica del yodo.  
3. **Paso 3: Potencial Electrostático y Vainas (Sheaths):** Cálculo del campo eléctrico local y la caída de potencial en las paredes, acoplado a la movilidad electrónica.

### **1.2. Amortiguamiento y Estabilización de Newton**

Para prevenir el estancamiento (*stalling*) del solver ante la rigidez (*stiffness*) de la química del yodo:

* **Factor de Amortiguamiento (Damping):** Utilizar un método de Newton con un factor constante inicial de **0.1 a 0.5**.  
* **Damping Mínimo:** Configurar un factor de amortiguamiento mínimo de **10⁻³**. Si el solver no alcanza convergencia, reducir el paso de potencia de forma paramétrica en lugar de permitir la divergencia del residuo.  
* **Resolución Numérica:** Emplear el solucionador directo **MUMPS** para el paso electromagnético y un solucionador iterativo con precondicionador **GMRES** para las variables de plasma.

## **2\. Protocolo de Discretización Espacial: Metasuperficie MRCO v1.2**

La precisión del modelo depende de la resolución de los efectos de sub-longitud de onda en la metasuperficie. Se distingue estrictamente entre el modelo de **Celda Unitaria (Unit Cell)** y el modelo de **Cámara Completa (Bulk Thruster)** para optimizar recursos computacionales.

### **2.1. Parámetros de Diseño MRCO v1.2**

* **Periodo Crítico:** 11.78 µm  
* **Factor de Llenado (Fill Factor):** 0.59  
* **Espesor de Estructura:** 3.32 µm

### **2.2. Guía de Refinamiento de Malla (Modelo de Celda Unitaria)**

Se prohíbe el uso de mallas de baja resolución. La discretización debe cumplir con el criterio de 1/10 del periodo de la metasuperficie.

| Elemento de Malla | Ubicación / Aplicación | Tamaño Máximo | Tamaño Mínimo |
| :---- | :---- | :---- | :---- |
| Elemento Base | Interior de Celda Unitaria | 1.17 µm | 0.4 µm |
| Refinamiento Adaptativo | Interfaces Metal/Dieléctrico | 0.15 µm | 0.05 µm |
| Capa Límite (Boundary Layer) | Metasuperficie / ALD | 0.1 µm | 0.02 µm |
| Malla de Cámara | Región de Plasma Bulk | 2.5 mm | 0.5 mm |

**Nota técnica:** Las escalas micrométricas son exclusivas para simulaciones de celda unitaria o submodelado. Para el modelo de motor completo (10x10 cm), se debe emplear una aproximación de **impedancia de superficie equivalente** para representar la metasuperficie sin colapsar la memoria del sistema.

## **3\. Gestión de Singularidades y Capas Delgadas (ALD)**

El recubrimiento dieléctrico fabricado por deposición de capas atómicas (ALD) sobre cuarzo o alúmina debe tratarse numéricamente para evitar ratios de aspecto extremos.

* **Thin Dielectric Film:** No discretizar el espesor físico de la capa ALD. Utilizar la condición de contorno **Transition Boundary Condition**, integrando el espesor de 3.32 µm y la **permitividad compleja** del material (incluyendo factores de pérdida a 13.56 MHz).  
* **Tratamiento de Aristas:** Es obligatorio realizar un redondeo (*filleting*) de esquinas en los bordes metálicos de la metasuperficie a escala nanométrica (r \~ 50-100 nm). Esto elimina singularidades artificiales en el cálculo del campo eléctrico local (E\_{local}), estabilizando la tasa de ionización cerca de la superficie.

## **4\. Criterios de Convergencia y Validación de Matching RF**

Para validar el acoplamiento de potencia y la mejora del 10-15% proyectada por el algoritmo MRCO v1.2, se establecen los siguientes umbrales:

### **4.1. Umbrales de Residuo Relativo**

* **Variables EM (E-field):** \< 10^{-5}  
* **Variables de Plasma (n\_e, n\_i, T\_e):** \< 10^{-5}

### **4.2. Checklist de Validación Técnica**

* \[ \] **Eficiencia de Acoplamiento:** Confirmar \\ge 65\\% en el modelo de celda unitaria (Validación vs. MRCO v1.2).  
* \[ \] **Uniformidad del Plasma:** El Índice de Uniformidad de la deposición de potencia (UI) debe ser \> 0.9 en la superficie de la metasuperficie.  
* \[ \] **Balance de Potencia:** \\int Q\_{rf} dV \= P\_{coll} \+ P\_{wall} \+ P\_{ext}, donde P\_{ext} es la energía de extracción iónica (800-1500 V).  
* \[ \] **Eficiencia Total:** Validar que el sistema opera en el rango de 35-45% de eficiencia total.

## **5\. Análisis de Sensibilidad y Estabilidad del Empuje**

El rendimiento estimado (Empuje: 0.7–1.3 mN, Isp: 2300–2800 s) debe ser independiente de la densidad de malla.

### **5.1. Estudio de Independencia de Malla**

Se requiere un informe de estabilidad que relacione la densidad de elementos con las métricas de salida:

* **Estabilidad del Empuje:** La variación de la fuerza de Lorentz y el flujo iónico entre refinamientos sucesivos debe ser \< 2\\%.  
* **Convergencia de Isp:** La fluctuación en la velocidad de agotamiento de neutros no debe exceder los 50 s de Isp.

### **5.2. Verificación de la Cuasineutralidad Física**

En un plasma de yodo, la condición de cuasineutralidad en el núcleo de la descarga se redefine para incluir la electronegatividad: n\_{I^+} \\approx n\_e \+ n\_{I^-} Desviaciones superiores al 1% en el centro de la cámara indican una resolución insuficiente de la vaina de plasma o una inestabilidad numérica en la convergencia de las especies negativas. Es crítico verificar que la densidad de I^- sea consistente con la presión de vapor de yodo a la temperatura de sublimación de operación.

# **Inventario Técnico y Logística de Sala Blanca: Metasuperficie MEI-RIT**

Este documento establece los requerimientos técnicos, materiales y protocolos operativos para la fabricación de la metasuperficie y los componentes críticos del propulsor iónico de yodo MEI-RIT. La planificación está diseñada para su ejecución en instalaciones de microfabricación de vanguardia (IMB-CNM-CSIC o ICFO) bajo estándares aeroespaciales proyectados para 2026\.

## **1\. Especificaciones de Precursores Químicos para ALD (Atomic Layer Deposition)**

Para garantizar la integridad de la metasuperficie y evitar fugas de corriente o degradación de la cámara de descarga, se requiere el uso de precursores de grado semiconductor (Purity 5N / 99.999%). El cumplimiento de esta pureza es crítico para minimizar impurezas metálicas y trazas de humedad que comprometerían el acoplamiento RF.

| Material a Depositar | Precursor Principal | Estado Físico / Manejo Técnico |
| :---- | :---- | :---- |
| **Alúmina (Al\_2O\_3)** | Trimethylaluminum (TMA) | Líquido pirofórico; requiere dosificación precisa con agentes oxidantes (H\_2O o O\_3). |
| **Nitruro de Silicio (Si\_3N\_4)** | Bis(tertiary-butylamino)silane (BTBAS) | Líquido de alta presión de vapor; optimizado para deposición conformal con plasma de N\_2 o NH\_3. |

*Nota técnica:* El uso de BTBAS frente a silanos convencionales permite una mayor estabilidad térmica de la capa dieléctrica, esencial para la protección de las estructuras de cobre ante el ambiente de plasma.

## **2\. Blancos de Metalización (Targets) y Materiales Estructurales**

La selección de materiales responde a criterios de eficiencia electromagnética y resistencia a la erosión iónica (sputtering), factor limitante de la vida útil del propulsor.

* **Cobre (Cu) y Aluminio (Al) \[Pureza 99.99%\]:** Blancos para procesos de evaporación por haz de electrones (E-beam). Se utilizan para la creación del array de resonadores sub-longitud de onda. El Cobre es prioritario para maximizar el acoplamiento RF a frecuencias de 13.56 MHz.  
* **Molibdeno (Mo):** Destinado a las grillas de aceleración. Se selecciona por su bajísimo Coeficiente de Expansión Térmica (CTE), lo que garantiza que el *gap* entre la grilla de pantalla y la de aceleración se mantenga constante bajo las altas cargas térmicas de la descarga RF.  
* **Grafito Pirolítico:** Material para el sistema de extracción de iones. Presenta una resistencia superior a la pulverización catódica (sputtering) en comparación con metales, minimizando la contaminación de la metasuperficie y extendiendo la vida operativa del sistema de dos grillas.

## **3\. Protocolos de Limpieza de Sustratos (SOP)**

Procedimiento Operativo Estándar para la preparación de obleas de cuarzo y alúmina antes de la litografía y ALD. La limpieza debe realizarse en un entorno controlado para asegurar la adhesión de capas nanométricas.

1. **Paso 0: Inspección Inicial:** Análisis mediante microscopía óptica para detectar defectos superficiales o microfisuras en el cuarzo.  
2. **Limpieza por Solventes:** Inmersión en baño de acetona con agitación ultrasónica (5 min), seguida de baño de Isopropanol (IPA) para la remoción de residuos orgánicos ligeros.  
3. **Limpieza Química Avanzada (Piranha):** Inmersión en una solución de H\_2SO\_4 y H\_2O\_2 en proporción 3:1. Este paso elimina contaminantes orgánicos persistentes y metales traza.  
4. **Enjuague de Alta Resistencia:** Lavado obligatorio con agua desionizada (DI Water) hasta alcanzar una resistividad de 18.2 MΩ·cm.  
5. **Secado y Deshidratación:** Chorro de Nitrógeno seco (N\_2) seguido de un *bake* en placa calefactora a 120°C para eliminar humedad residual.  
6. **Activación por Plasma de Oxígeno:** Tratamiento final para aumentar la energía superficial (hidrofilicidad), optimizando la adhesión de la metalización posterior.

## **4\. Parámetros Logísticos de la Metasuperficie (Optimización MRCO v1.2)**

La logística de fabricación debe ceñirse estrictamente a los resultados del modelo de sustitución (surrogate) MRCO v1.2, diseñado para operar en régimen de sub-longitud de onda (frecuencia de diseño: 13.56 MHz).

**Especificaciones de Diseño (Target v1.2):**

* **Periodo Óptimo:** 11.78 µm.  
* **Factor de Llenado (Fill Factor):** 0.59.  
* **Espesor de Capa:** 3.32 µm.

**Relevancia en Fabricación:** Estas dimensiones permiten alcanzar una eficiencia de acoplamiento RF de \~65%. Dado que el Factor de Llenado es el parámetro más sensible para la uniformidad del plasma, es obligatorio realizar una verificación mediante **CD-SEM (Critical Dimension SEM)** tras el proceso de grabado (etching) para validar la fidelidad geométrica antes de la integración.

## **5\. Recomendaciones de Pasivación y Manejo de Propelente (Yodo)**

El yodo (I\_2) es un propelente altamente corrosivo y corrosivo para el cobre de la metasuperficie. Su manejo logístico es una prioridad de seguridad.

* **Pasivación Post-Proceso:** Tras la metalización, la metasuperficie debe recibir un encapsulamiento por ALD (Al\_2O\_3 o Si\_3N\_4) para aislar el cobre del contacto directo con el vapor de yodo.  
* **Almacenamiento y Tanques:** Uso exclusivo de polímeros fluorados (**PTFE o PFA**) o metales con recubrimiento cerámico. El yodo sólido debe ser manejado en campanas de extracción de alta eficiencia para evitar la inhalación de vapores sublimados.  
* **Protocolo de Transporte Inter-estación:** El traslado entre los módulos de litografía, ALD y la cámara de vacío debe realizarse en contenedores sellados (Dry Boxes) con atmósfera de **Nitrógeno seco (N\_2)**. La exposición a la humedad ambiental formaría ácido hiodhídrico, el cual destruiría las nanoestructuras de la metasuperficie de forma irreversible.

## **6\. Infraestructura y Presupuesto Logístico (Cataluña 2026\)**

La fabricación se llevará a cabo bajo estándares de **ISO 5 (Clase 100\)** para la etapa de litografía, garantizando la ausencia de partículas que provoquen defectos en capas de espesor micrométrico.

### **Equipamiento Requerido**

* **Fabricación:** Spin-coater de alta precisión, Evaporador E-beam, Sistema de Grabado por Iones Reactivos (RIE).  
* **Metrología:** SEM de emisión de campo, AFM y elipsometría para control de espesores ALD.

### **Resumen Financiero Estimado (Euros)**

* **Fase 1: Diseño y Simulación:** 13.000 € – 18.500 € (Incluye personal e infraestructura de computación para MRCO).  
* **Fase 2: Fabricación (ISO 5):** 18.000 € – 27.500 € (Horas de uso de sala blanca IMB-CNM-CSIC y consumibles de alta pureza).  
* **Fase 3: Ensamblaje y Pruebas en Vacío:** 23.500 € – 37.500 € (Diagnóstico de plasma, balanza torsional y sistemas de vacío).  
* **Fase 4: Optimización y Propiedad Intelectual:** 8.500 € – 13.500 € (Refinamiento de diseño y registro de patente provisional).

**Presupuesto Total Estimado:** **54.000 € – 97.000 €**

# **Cronograma de Operaciones de Vacío: Propulsor MEI-RIT (Fase 3\)**

Este documento establece el protocolo operativo de alta fidelidad para las pruebas de ultra-alto vacío (UHV) y la caracterización de propulsión eléctrica del sistema **MEI-RIT (Metasurface-Enhanced Iodine RF Ion Thruster)**. Como Ingeniero Principal de Operaciones, este cronograma es de cumplimiento obligatorio para asegurar la integridad de la metasuperficie litografiada y la precisión de los datos de empuje.

### **1\. Preparación del Sistema y Ciclo de Bombeo Inicial**

Para garantizar la pureza del plasma y evitar la formación de oxiyoduros, debemos alcanzar presiones base en el rango de ultra-alto vacío, considerando que el camino libre medio (Mean Free Path) debe ser órdenes de magnitud superior a las dimensiones de la cámara de descarga.

#### **Protocolo de Desgasificación (Bake-out)**

Se ejecutará un ciclo de *bake-out* a **150°C** durante un periodo no inferior a 24 horas. Este proceso es crítico para eliminar humedad adsorbida en la cámara de cuarzo/alúmina y componentes de molibdeno (Mo), cuya porosidad superficial puede atrapar contaminantes que reaccionarían violentamente con el yodo molecular (I\_2).

#### **Hitos de Presión y Mitigación de Riesgos Operativos**

| Hito de Presión | Estado del Sistema | Riesgo Técnico / Mitigación |
| :---- | :---- | :---- |
| **Atmósferica a 10^{-3} mbar** | Desbaste inicial (Roughing). | **Riesgo:** Humedad residual reaccionando con depósitos de yodo previo. **Mitigación:** Purga con Argón seco y bake-out a 150°C. |
| **10^{-3} a 10^{-5} mbar** | Transición a Bombardeo de Alta Capacidad (Turbo/Cryo). | **Riesgo:** Contaminación cruzada de aceites. **Mitigación:** Uso de sensores de cátodo frío y manómetros de capacitancia resistentes a la corrosión. |
| **\< 10^{-6} mbar** | Límite operativo (Presión Base). | **Riesgo:** Desgasificación de la metasuperficie. **Mitigación:** Análisis de Presión Parcial (PPA) mediante RGA para verificar niveles de impurezas. |

**Instrumentación Crítica:** Se prohíbe el uso de sensores de filamento desnudo expuestos. Se emplearán exclusivamente manómetros de capacitancia y sensores Pirani con recubrimiento cerámico/halogen-resistant.

### **2\. Acondicionamiento Térmico y Sublimación del Yodo (80-100°C)**

La gestión del flujo másico depende estrictamente de la presión de vapor de la línea de propelente, controlada mediante la temperatura del tanque.

* **Rampa Térmica:** Se aplicará una rampa de calentamiento de **2°C/min** gestionada por un controlador **PID**. Esto previene picos de presión transitorios (*pressure spikes*) que podrían extinguir la descarga de radiofrecuencia (RF).  
* **Gestión Térmica de la Metasuperficie:** El rango operativo del tanque se mantendrá entre **80°C y 100°C**, buscando un equilibrio entre la tasa de sublimación y la estabilidad térmica de la cámara.

**ADVERTENCIA TÉCNICA (Riesgo de Cohesión Estructural):** La metasuperficie optimizada bajo el algoritmo **MRCO v1.2** posee un periodo sub-longitud de onda de **11.78 µm** y un espesor de **3.32 µm**. Es imperativo evitar choques térmicos, ya que el desajuste en el coeficiente de expansión térmica (CTE) entre las nanoestructuras metálicas y el sustrato de cuarzo/alúmina puede provocar delaminación irreversible de los elementos litografiados.

### **3\. Secuencia de Ignición y Pruebas Operativas**

El encendido del plasma se basa en el acoplamiento electromagnético optimizado por la metasuperficie para maximizar la densidad iónica.

1. **Inyección de Potencia RF:** Aplicar entre **50 W y 80 W** a 13.56 MHz (o 2.45 GHz). La geometría de la metasuperficie (Factor de llenado: **0.59**) está diseñada para una eficiencia de acoplamiento de **\~65%**.  
2. **Aceleración Electrostática:** Polarización de rejillas de **Molibdeno (Mo)** (preferidas sobre acero por su resistencia química al yodo).  
   * **Grid Screen:** 800 V – 1500 V.  
   * **Grid Accelerator:** Voltaje negativo para supresión de retro-electrones.  
3. **Monitoreo de Eficiencia:** El objetivo es validar un ratio **Thrust-to-Power de 15 – 22 mN/kW**, conforme a los benchmarks del proyecto MEI-RIT.

### **4\. Protocolo de Neutralización de Halógenos Post-Prueba**

El yodo es altamente corrosivo para los componentes metálicos de la cámara de vacío y los aceites de las bombas mecánicas.

* **Purga Química:** Al finalizar la ignición, se realizará un barrido de la cámara con **Argón de Alta Pureza (Grado 5.0 / 99.999%)** para desplazar el I\_2 residual hacia el sistema de escape.  
* **Criopreservación (Cryo-trapping):** Es obligatorio el uso de una trampa fría (Cold Trap) en la entrada de la bomba de vacío para capturar el yodo molecular antes de que contamine el sistema de bombeo.  
* **Pasivación:** Tras la exposición, las superficies internas de acero inoxidable de la cámara deben ser pasivadas para prevenir el ataque por picaduras (*pitting*) inducido por halógenos.

### **5\. Monitoreo de Erosión y Diagnóstico de Componentes**

Utilizaremos modelos **PIC-Híbridos** inspirados en los estándares IEPC-2007-250 para predecir la vida útil.

| Componente | Mecanismo de Desgaste | Método de Verificación |
| :---- | :---- | :---- |
| **Rejillas de Mo** | Sputtering por bombardeo de iones secundarios. | Modelado de **Barrera de Transporte** y ajuste del **Coeficiente de Bohm (0.15 \- 0.20)**. |
| **Metasuperficie** | Erosión química de las nanoestructuras (11.78 µm). | Microscopía Electrónica de Barrido (SEM) y validación de acoplamiento RF post-test. |
| **Sistema Completo** | Degradación de la eficiencia total (35-45%). | **Balanza Torsional** para validación del empuje real (0.6 – 1.2 mN). |

Es vital monitorear la brecha del aislador; la acumulación de depósitos conductivos de yodo/metales erosionados puede provocar arcos eléctricos que comprometan la fuente de alta tensión.

### **6\. Cronograma Consolidado de la Fase 3 (Meses 8-12)**

Línea de tiempo para la validación final del prototipo de laboratorio MEI-RIT:

* **Mes 8: Integración y Vacío Base.** Ensamblaje de hardware y validación de hermeticidad. Verificación de presiones parciales mediante RGA tras bake-out.  
* **Mes 9-10: Mapeo de Empuje y Potencia.** Pruebas de ignición sistemáticas. Validación de los objetivos de **15–22 mN/kW** y mapeo de empuje (0.6 – 1.2 mN). Ajuste de la eficiencia de acoplamiento del algoritmo MRCO v1.2.  
* **Mes 11: Caracterización de Erosión Acelerada.** Pruebas de durabilidad para calibrar el Coeficiente de Bohm en el modelo de erosión y observar el comportamiento de las rejillas de Molibdeno.  
* **Mes 12: Neutralización y Análisis Forense.** Desmontaje bajo campana de extracción, neutralización química final y análisis de datos post-test para publicación en el *Journal of Propulsion and Power*.

# **Manual de Análisis Científico: Procesamiento y Validación de Rendimiento para MEI-RIT (Fase 4\)**

Este manual define el protocolo de metrología y validación experimental para la Fase 4 del propulsor iónico de yodo mejorado con metasuperficies (MEI-RIT). Como Científico Principal, exijo el cumplimiento estricto de estos estándares de procesamiento para asegurar que los resultados posean la integridad necesaria para su publicación en el *Journal of Propulsion and Power*.

### **1\. Especificaciones Técnicas y Benchmarks del Sistema**

El sistema MEI-RIT debe ser evaluado frente al estado del arte (SOTA). A diferencia de los propulsores de efecto Hall, donde la erosión se localiza en las paredes del canal, el MEI-RIT presenta una degradación centrada en el sistema de extracción (sputtering en grids de Mo/Grafito).

| Parámetro | Valor / Rango | Unidades |
| :---- | :---- | :---- |
| Propelente | Yodo Sólido (I\_2) | N/A |
| Frecuencias RF | 13.56 / 2450 | MHz |
| Rango de Potencia | 50 – 80 | W |
| Empuje (Thrust) | 0.7 – 1.3 | mN |
| Impulso Específico (I\_{sp}) | 2300 – 3200 | s |
| Voltaje de Aceleración | 800 – 1500 | V |
| Geometría Metasuperficie | Periodo: 11.78 / Fill: 0.59 | μm / Ratio |
| Factor de Frecuencia (MRCO v1.2) | 1.0 | N/A |
| Mecanismo de Erosión Crítico | Sputtering de Grids (Mo/C) | N/A |

### **2\. Metrología de Señal de la Balanza Torsional**

La cuantificación de empuje en micro-Newtons exige un rigor absoluto en la cadena de adquisición. El analista debe garantizar que la frecuencia de muestreo (f\_s) cumple con el **Criterio de Nyquist** para evitar el solapamiento de ruidos de conmutación de las fuentes de alta tensión.

**Protocolo de Filtrado y Estabilización:**

1. **Caracterización de Deriva Térmica:** Registro de línea base de 300s. El gradiente térmico del sistema de sublimación de yodo no debe inducir una deriva superior al 1% del empuje objetivo.  
2. **Calibración de Tara Electrostática:** Es obligatorio medir la deflexión con los grids energizados (800-1500 V) pero sin ignición de plasma. Esto aísla fuerzas electrostáticas parásitas que podrían inflar artificialmente el empuje neto.  
3. **Filtrado de Interferencia RF:** Aplicación de un Filtro Pasa-Bajos (LPF) digital con una frecuencia de corte (f\_c) inferior a 1 Hz, optimizado para la frecuencia natural de la balanza, eliminando armónicos de 13.56 MHz.  
4. **Remoción de Transitorios de Ignición:** Los picos de corriente durante el "breakdown" del gas deben truncarse estadísticamente mediante un filtro de exclusión de 3-\\sigma.

### **3\. Derivación Matemática del Rendimiento Neto**

El cálculo del rendimiento debe basarse en formalismos físicos explícitos. No se aceptarán aproximaciones empíricas sin la siguiente base de cálculo:

**A. Cálculo del Empuje Neto (T):** El empuje se deriva de la deflexión \\Delta x corregida por los factores de tara: T \= k \\cdot \\Delta x\_{measured} \- F\_{cold\\\_gas} \- F\_{electrostatic\\\_tare} Donde k es la constante de rigidez de la fibra torsional (N/m).

**B. Impulso Específico (I\_{sp}):** Utilizando el flujo másico (\\dot{m}) de yodo sublimado (estable a 80-100°C), se define: I\_{sp} \= \\frac{T}{\\dot{m} \\cdot g\_0} Donde g\_0 \\approx 9.80665 \\text{ m/s}^2. Para la validación, se comparará con el benchmark del Busek BIT-3 (I\_{sp} hasta 3200 s).

### **4\. Protocolo de Validación de la Metasuperficie (MRCO v1.2)**

La mejora de eficiencia del 10-15% debe ser verificada mediante la comparación del "Baseline" contra el sistema optimizado.

* **Configuración MEI-RIT:** Implementar la metasuperficie optimizada con los parámetros finales de MRCO v1.2: Periodo **11.78 μm**, Factor de Llenado **0.59**, Espesor **3.32 μm** y Factor de Frecuencia **1.0**.  
* **Bucle de Retroalimentación Metrológica:** Las desviaciones geométricas observadas mediante caracterización SEM/AFM (procedentes del IMB-CNM-CSIC) deben re-introducirse en el algoritmo MRCO para actualizar la eficiencia de acoplamiento esperada (\\sim 65\\%) antes de la comparación final con los datos de empuje.  
* **Métrica de Éxito:** Incremento sostenido en la relación mN/kW superior al 10% respecto al baseline en todo el rango de 50-80 W.

### **5\. Presupuesto de Incertidumbre y Error**

| Fuente de Error | Parámetro de Incertidumbre | Nivel de Confianza |
| :---- | :---- | :---- |
| Medición de Empuje | Error de resolución de balanza | 95% (\\pm 0.05 mN) |
| Flujo Másico (\\dot{m}) | **Histéresis Térmica de Sublimación** | 95% (\\pm 2.5%) |
| Geometría Metasuperficie | Desviación de litografía (SEM) | Nanométrica |
| Potencia RF (P\_{rf}) | Reflectometría (SWR) | \\pm 1.0 W |
| Voltaje de Grids | Rizado de fuente HV | \\pm 0.5% |

### **6\. Estándares para Representación Visual (Estilo IEPC)**

Los gráficos deben ser generados con calidad de publicación, siguiendo la estética de \[SOURCE\_IMAGE\_1\] (fondo blanco, *grid* gris tenue).

1. **Eficiencia de Acoplamiento vs. Periodo:** Debe mostrarse explícitamente el **desplazamiento del pico de eficiencia** desde el modelo v1.0 (12.5 μm) hacia el refinamiento v1.2 (11.78 μm), superponiendo la curva de simulación con los puntos experimentales.  
2. **Empuje vs. Potencia RF:**  
   * **Barras de error horizontales:** Indispensables para la potencia RF debido a los límites de reflectometría (SWR).  
   * **Barras de error verticales:** Basadas en la incertidumbre combinada de la balanza y la tara electrostática.  
3. **Mapa de Evolución del I\_{sp}:** Representación tridimensional o de contorno relacionando flujo másico, voltaje de aceleración y empuje resultante.

### **7\. Requisitos de Documentación para Revisión por Pares**

Para declarar la Phase 4 como exitosa, el informe de análisis debe incluir:

* **Trazabilidad de Fabricación:** Certificados de pureza del yodo (99.9%) y caracterización de materiales de grids (Mo/Grafito).  
* **Validación de Modelo:** Justificación física de cualquier desviación \>5% entre la predicción de acoplamiento de MRCO v1.2 y el empuje medido.  
* **Análisis Comparativo:** Posicionamiento del MEI-RIT frente al ThrustMe NPT30-I2 y Busek BIT-3, destacando la ventaja competitiva de la metasuperficie en la eficiencia de ionización.

# **Hoja de Ruta de Propiedad Intelectual: Propulsor MEI-RIT (Metasurface-Enhanced Iodine RF Ion Thruster)**

Este documento estratégico define la estructura de protección de activos intelectuales y el cronograma de desarrollo técnico para el sistema de propulsión iónica **MEI-RIT**. Como Especialista Senior en Estrategia de PI, este plan se ha diseñado para maximizar la robustez legal de la invención frente a competidores y asegurar la libertad de operación (FTO) en el mercado global de satélites pequeños.

## **1\. Borrador Consolidado de Reivindicaciones (v2.0)**

El siguiente cuerpo de reivindicaciones ha sido redactado bajo una lógica de "fortaleza periférica", protegiendo no solo la arquitectura física sino también el método de diseño optimizado y los parámetros críticos que constituyen el "paso inventivo" (Actividad Inventiva).

**Reivindicación Independiente**

1. **Propulsor de iones de radiofrecuencia (RF)** que comprende: una cámara de descarga que contiene un propelente de yodo sólido, una antena de RF, un sistema de aceleración de iones de dos rejillas y una estructura de metasuperficie dispuesta en el interior de la cámara de descarga **acoplada funcionalmente** a la antena de RF para definir una condición de contorno electromagnética configurada para mejorar el acoplamiento de potencia y la uniformidad del plasma; donde la metasuperficie comprende un patrón sub-longitud de onda periódico caracterizado por un **periodo entre 8 y 18 μm**, un **factor de llenado entre 0.35 y 0.75**, y un **espesor entre 1.8 y 3.8 μm**.

**Reivindicaciones Dependientes**

1. El propulsor según la reivindicación 1, caracterizado porque la metasuperficie incluye una **capa de protección mediante deposición de capas atómicas (ALD)** de un material dieléctrico, configurada para asegurar la integridad estructural y la durabilidad frente al ambiente corrosivo del yodo.  
2. El propulsor según la reivindicación 1, caracterizado porque la metasuperficie está fabricada sobre un **sustrato de cuarzo o alúmina** mediante procesos de litografía y grabado (*etching*).  
3. El propulsor según la reivindicación 1, caracterizado porque la geometría de la metasuperficie se optimiza mediante un **modelo subrogado** que contempla frecuencias operativas de **13.56 MHz o 2.45 GHz** e integra explícitamente los efectos de carga del plasma.  
4. El propulsor según la reivindicación 1, donde el propelente de yodo sólido se almacena en un tanque de polímero o metal diseñado para una **sublimación controlada** mediante gestión térmica.  
5. Un método de operación del propulsor definido en la reivindicación 1, que comprende la ignición del plasma mediante potencia RF acoplada a través de la metasuperficie y la extracción de iones mediante rejillas de aceleración a voltajes situados **entre 800 V y 1500 V**.  
6. El propulsor según la reivindicación 1, configurado para su integración en **CubeSats o satélites pequeños** con un rango de potencia operativa total entre **50 W y 150 W**.  
7. La metasuperficie según la reivindicación 1, donde el patrón periódico está compuesto por **cobre, aluminio o materiales dieléctricos** con bajo factor de pérdidas en frecuencias de radiofrecuencia.  
8. El propulsor según la reivindicación 1, donde la metasuperficie proporciona una **mejora de la eficiencia de acoplamiento de RF de al menos un 10%** en comparación con una arquitectura idéntica carente de dicha estructura.  
9. Un método de diseño de la metasuperficie para el propulsor de la reivindicación 1, caracterizado por el uso de un **algoritmo de optimización subrogado** que ejecuta pasos secuenciales de sintonización geométrica integrando **penalizaciones por carga de plasma y factores de pérdida de material**, y la posterior fabricación de la metasuperficie según dichos parámetros.

## **2\. Calendario de Presentación de Patente y Desarrollo Técnico**

Para mitigar riesgos legales, se ha reestructurado el cronograma posicionando el análisis de anterioridad como un hito crítico previo a la inversión en fabricación masiva.

1. **Fase 1 (Meses 1-3): Diseño, Simulación y Estrategia de PI.** Ejecución del modelado electromagnético utilizando el algoritmo **MRCO v1.2** (que incluye carga de plasma y pérdidas de material). **Hito fundamental:** Inicio de la búsqueda de anterioridad y análisis de libertad de operación (FTO).  
2. **Fase 2 (Meses 4-7): Fabricación de la Metasuperficie.** Producción en sala blanca (**IMB-CNM-CSIC**) mediante litografía y grabado sobre sustratos de cuarzo/alúmina, integrando la protección ALD para validación de durabilidad.  
3. **Fase 3 (Meses 8-12): Ensamblaje del Prototipo y Validación.** Pruebas en cámara de vacío para verificar el rango de empuje (**0.7 – 1.3 mN**) y el acoplamiento de potencia mejorado.  
4. **Fase 4 (Meses 13-18): Consolidación de PI y Presentación.** Optimización final basada en datos de prueba, publicación de resultados técnicos y **presentación formal de la solicitud de patente provisional**.

## **3\. Estrategia de Búsqueda de Anterioridad y Libertad de Operación (FTO)**

### **Análisis del Estado del Arte y Novedad**

El sistema MEI-RIT ocupa un espacio tecnológico no explotado actualmente:

* **Diferenciación frente a ThrustMe NPT30-I2 y Busek BIT-3:** Si bien estos sistemas utilizan yodo, su mecanismo de descarga RF es convencional. La innovación de MEI-RIT reside en el control del campo EM mediante una metasuperficie sub-longitud de onda. El **efecto técnico específico** (control de la impedancia superficial y acoplamiento optimizado) es imposible de lograr en las arquitecturas actuales sin la implementación de nuestra estructura periódica.  
* **Investigación Académica (IEPC 2024):** Aunque existen estudios sobre metamateriales, MEI-RIT es la primera aplicación concreta que traduce modelos teóricos en una arquitectura de propulsión de yodo con parámetros geométricos validados algorítmicamente para operación real.

### **Justificación de No-Infracción y Ventaja Comparativa**

A diferencia de los propulsores Hall (como el **BHT-200** y **BHT-600**), cuya vida útil está limitada por la erosión de los anillos cerámicos y la circuitería magnética debido a la arquitectura DC, MEI-RIT utiliza una descarga RF donde la metasuperficie actúa como un **buffer y optimizador de uniformidad**. Esto reduce inherentemente la erosión localizada, extendiendo la vida operativa del propulsor. Esta "metasurface-cladded discharge chamber" constituye una condición de contorno única que no infringe las patentes de mecanismos Hall tradicionales.

### **Directrices de Búsqueda FTO**

Se ordena el enfoque en:

* "Metasurface-cladded RF plasma sources".  
* "Sub-wavelength EM boundary conditions in ion thrusters".  
* Referencias cruzadas de los autores citados en IEPC 2024 sobre metamateriales para propulsión eléctrica.

## **4\. Optimización Técnica y Justificación Legal (MRCO v1.2)**

La actividad inventiva se sustenta en la lógica de optimización del algoritmo **MRCO v1.2**, cuyos resultados finales para la metasuperficie son:

| Parámetro | Valor Óptimo (MRCO v1.2) |
| :---- | :---- |
| *
