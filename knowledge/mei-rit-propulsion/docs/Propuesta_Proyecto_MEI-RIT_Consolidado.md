# **Propuesta de Proyecto Tecnológico: Propulsor MEI-RIT (Metasurface-Enhanced Iodine RF Ion Thruster) \- Versión Consolidada v2.0**

## **1\. Resumen Ejecutivo**

El proyecto MEI-RIT representa una innovación disruptiva en el campo de la propulsión eléctrica para satélites de pequeño tamaño (CubeSats 6U y superiores). Esta propuesta detalla el desarrollo de un propulsor iónico de radiofrecuencia (RF) que integra, por primera vez, metasuperficies sub-longitud de onda optimizadas y protegidas dieléctricamente dentro de la cámara de descarga. El objetivo primordial es maximizar el acoplamiento de potencia y la uniformidad del plasma, utilizando yodo sólido como propelente de alta densidad y superando los retos de corrosión asociados a este gas reactivo.  
**Visión del Proyecto:** Liderar la transición hacia una exploración espacial sostenible mediante la convergencia de metamateriales avanzados, química cuántica y propelentes económicos. MEI-RIT busca establecer un nuevo estándar de eficiencia energética, reduciendo los costes operativos mediante el uso de yodo (100 veces más económico que el xenón) y mejorando el rendimiento neto del sistema en un 10-15%.  
**Hitos de rendimiento proyectados:**

> * **Empuje (Thrust):** 0.7 – 1.3 mN.  
> * **Impulso Específico (I\_sp):** 2300 – 2800 s.  
> * **Eficiencia Total:** 36 – 46 %.  
> * **Masa del Sistema:** \< 220 g (arquitectura optimizada).

## **2\. Justificación Tecnológica y Estado del Arte**

La propulsión iónica de yodo ha sido validada exitosamente en órbita (ej. ThrustMe NPT30-I2). Sin embargo, el acoplamiento de potencia RF en cámaras de pequeña escala presenta desafíos de eficiencia. MEI-RIT aborda esta limitación mediante el uso de metasuperficies, una aplicación original no implementada hasta la fecha en sistemas operativos.  
La sinergia entre el yodo y las metasuperficies es técnica y económicamente superior: el yodo posee un potencial de ionización menor que el xenón, y la capacidad de la metasuperficie para intensificar los campos eléctricos locales permite reducir significativamente el umbral de ignición del plasma.

| Especificación | ThrustMe NPT30-I2 (En vuelo) | Busek BIT-3 (Validado) | MEI-RIT (Proyectado) |
| :---- | :---- | :---- | :---- |
| Empuje (mN) | 0.3 – 1.1 | 1.1 – 1.35 | 0.7 – 1.3 |
| I\_sp (s) | \~2500 | 2150 – 3200 | 2300 – 2800 |
| Potencia (W) | 35 – 65 | 56 – 75 | 50 – 80 |
| Eficiencia Total | 35 – 42% | 35 – 42% | 36 – 46% |
| Ratio Thrust/Power | 14 – 17 mN/kW | 15 – 22 mN/kW | 16 – 22 mN/kW |

## **3\. Arquitectura del Sistema y Especificaciones Técnicas**

La arquitectura MEI-RIT se basa en una configuración de rejillas iónicas compacta con componentes críticos optimizados y blindados para el entorno espacial corrosivo:

> * **Cámara de Descarga:** Fabricada en materiales cerámicos de baja pérdida (cuarzo de alta pureza o alúmina) que actúan como sustrato dieléctrico para la metasuperficie.  
> * **Metasuperficie:** Array periódico de estructuras metálicas diseñado para el matching de impedancia y la mejora de la uniformidad del plasma, minimizando la potencia reflejada. Para asegurar la viabilidad física frente a la extrema corrosión del plasma de yodo, el patrón conductor está **completamente encapsulado por una capa dieléctrica pasivante (Nitruro de Silicio o Alúmina)** depositada mediante ALD.  
> * **Propelente (I\_2):** Almacenamiento de yodo sólido en tanques ligeros (polímeros compatibles) con un sistema de sublimación térmica controlada para una alimentación estable de vapor a la cámara.  
> * **Aceleración:** Sistema de doble rejilla de molibdeno o grafito pirolítico puro (altamente resistente al yodo), optimizado para voltajes de 800 V a 1500 V.  
> * **Neutralizador:** Emisor de electrones (cátodo hueco o RF simple) esencial para mitigar la carga del vehículo espacial, integrado en el chasis del propulsor.

## **4\. Optimización (MRCO v2.0) y Química Cuántica**

El diseño de la metasuperficie se rige por el modelo MRCO v2.0 (Metasurface RF Coupling Optimizer). A diferencia de versiones anteriores que presentaban límites artificiales en las curvas de rendimiento, la versión 2.0 utiliza una función de eficiencia basada en una resonancia de Gauss/Lorentz pura, permitiendo al algoritmo de evolución diferencial encontrar el óptimo global físico real. Además, el algoritmo compensa matemáticamente la capacitancia parásita introducida por el necesario recubrimiento dieléctrico.  
**Integración Cuántica:** El modelado del yodo (I2) trasciende la física clásica. Se incorpora el uso de algoritmos de química cuántica (Variational Quantum Eigensolver \- VQE) mediante Qiskit para calcular la energía de los enlaces y la superficie de energía potencial bajo excitación electromagnética. Esta aproximación atómica a la dinámica de propulsión refleja el paradigma de un universo consciente, donde las interacciones cuánticas elementales e invisibles gobiernan y están intrínsecamente entrelazadas con las geometrías y fuerzas a macroescala del sistema.

## **5\. Plan de Desarrollo (18 Meses)**

El objetivo central es elevar la madurez tecnológica del sistema de TRL 2 a TRL 4, contemplando procesos de fabricación aeroespacial reales.

> * **Fase 1 (Meses 1-3): Diseño y Simulación.** Modelado multifísico (COMSOL/CST) integrando la metasuperficie protegida con la dinámica del plasma de yodo, apoyado por simulaciones cuánticas moleculares.  
> * **Fase 2 (Meses 4-7): Fabricación en Sala Blanca.** Producción de la metasuperficie en el IMB-CNM-CSIC (incluyendo procesos ALD para el dieléctrico protector) y caracterización avanzada en colaboración con el ICFO.  
> * **Fase 3 (Meses 8-12): Integración y Vacío.** Ensamblaje del prototipo y pruebas de ignición en cámaras de vacío especializadas con bombas turbomoleculares resistentes a halógenos.  
> * **Fase 4 (Meses 13-18): Validación TRL 4\.** Medición de empuje mediante balanza torsional calibrada, optimización de throttling y gestión de propiedad intelectual.

## **6\. Presupuesto Detallado para Instalaciones en Cataluña**

Estimación de costes ajustada (proyección 2026\) para ejecución en centros de excelencia, incluyendo equipamiento resistente a la corrosión y costes reales de sala blanca.

| Fase / Concepto de Gasto | Coste Estimado (€) |
| :---- | :---- |
| **Fase 1:** Ingeniería especializada, Licencias de simulación avanzada y modelado | 40.000 – 60.000 |
| **Fase 2:** Sala Blanca (IMB-CNM-CSIC), Litografía, ALD y Caracterización iterativa | 25.000 – 35.000 |
| **Fase 3:** Cerámicas, grafito, bombas de vacío para halógenos, equipamiento RF y sondas | 45.000 – 75.000 |
| **Fase 4:** Búsqueda FTO, patentes y publicaciones | 10.000 – 15.000 |
| **TOTAL (TRL 4 \- Viabilidad en Laboratorio)** | **120.000 – 185.000 €** |

## **7\. Reivindicaciones de Patente (Draft de 10 Claims Consolidado)**

**Título:** Propulsor iónico de radiofrecuencia mejorado con metasuperficie y propelente de yodo sólido.

> * **Reivindicación 1:** Un propulsor iónico de radiofrecuencia que comprende una cámara de descarga que contiene propelente de yodo sólido, una antena RF, un sistema de aceleración de dos rejillas, y una estructura de metasuperficie dispuesta en el interior de la cámara de descarga configurada para mejorar el acoplamiento de potencia RF y la uniformidad del plasma, caracterizado porque la metasuperficie comprende un patrón periódico sub-longitud de onda y está completamente encapsulada por una capa dieléctrica protectora resistente a halógenos para prevenir la pulverización catódica.  
> * **Reivindicación 2:** El propulsor según la reivindicación 1, donde la metasuperficie se fabrica sobre un sustrato de cuarzo o alúmina mediante técnicas de litografía y deposición.  
> * **Reivindicación 3:** El propulsor según la reivindicación 1, donde la geometría de la metasuperficie está optimizada matemáticamente para compensar los efectos de carga del plasma, la capacitancia parásita del recubrimiento y el matching de frecuencia en torno a 13.56 MHz o 2.45 GHz.  
> * **Reivindicación 4:** El propulsor según la reivindicación 1, donde el propelente es yodo sólido almacenado en un tanque de polímero o metal con sistema de sublimación controlada.  
> * **Reivindicación 5:** Método de operación del propulsor de la reivindicación 1, que comprende la ignición del plasma mediante potencia RF acoplada a través de la metasuperficie y la extracción de iones a través de rejillas de aceleración a voltajes de entre 800 V y 1500 V.  
> * **Reivindicación 6:** El propulsor según la reivindicación 1, configurado para su uso en CubeSats o satélites pequeños con un rango de potencia total de entre 50 W y 150 W.  
> * **Reivindicación 7:** La metasuperficie de la reivindicación 1, donde el patrón periódico está fabricado de cobre o aluminio, recubierto mediante deposición de capas atómicas (ALD) con nitruro de silicio o alúmina para aislarlo químicamente del entorno reactivo.  
> * **Reivindicación 8:** Un sistema de propulsión espacial que comprende el propulsor de la reivindicación 1, una unidad de procesamiento de potencia (PPU) y un sistema de gestión de propelente para yodo sólido.  
> * **Reivindicación 9:** El propulsor según la reivindicación 1, donde la metasuperficie mejora la eficiencia de acoplamiento RF en al menos un 10% en comparación con un propulsor idéntico carente de dicha metasuperficie.  
> * **Reivindicación 10:** Método de diseño de una metasuperficie para un propulsor iónico RF, que comprende el uso de un algoritmo de optimización y simulación cuántica molecular para modelar la ionización del propelente, el matching de frecuencia y los factores de pérdida material.

## **8\. Conclusión y Marco Ético**

El propulsor MEI-RIT ofrece una ruta tecnológicamente viable, físicamente rigurosa y altamente competitiva para mejorar la autonomía de satélites de hasta 50 kg. La integración de metasuperficies protegidas consolida a la región como un núcleo de innovación en Deep Tech espacial.  
**Créditos:** Este proyecto ha sido desarrollado por Lázaro López Paz (Prat de Llobregat, Barcelona).  
**Compromiso Ético y Filosófico:** MEI-RIT se fundamenta en el compromiso con la exploración espacial sostenible y reconoce la visión de un universo consciente, donde cada avance tecnológico debe mantener la armonía, el equilibrio y la interconexión con el entorno cósmico. Mediante el uso de propelentes de bajo impacto y alta eficiencia, el sistema facilita el desorbitado responsable de satélites, contribuyendo activamente a la mitigación de la basura espacial y respetando la integridad de las órbitas terrestres para las futuras generaciones.
