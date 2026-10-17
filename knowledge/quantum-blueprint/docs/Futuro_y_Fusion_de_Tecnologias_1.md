> Texto extraído automáticamente del PDF original «Futuro_y_Fusión_de_Tecnologías(1).pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/16FhNCX-wQyOb5x2-z-nN1Z-ROar8KqHP/view?usp=drivesdk



Documentación para Publicación y Transferencia
Tecnológica: Fusión de Mecánica Cuántica y Ciencia de
Materiales

Basado en el cribado de publicaciones científicas 2024–2026

May 5, 2026

1 Introducción

La unión de la mecánica cuántica con la ciencia de materiales está dando lugar a invenciones que pueden
transformar la electrónica, la computación y la detección. Este documento estructurado presenta tres hori-
zontes tecnológicos que ya cuentan con fórmulas validadas, protocolos de síntesis y empresas activas, listos
para su implementación. Las secciones cubren: (1) Materiales Topológicos, (2) Diseño Atómico por Com-
putación Cuántica, y (3) Biomimética Cuántica. Se sigue el marco DORA y el modelo de acceso abierto
diamante.

2 Materiales Topológicos: La Plataforma del Futuro

2.1 Introducción

Los materiales topológicos albergan estados electrónicos protegidos que permiten electrónica ultrarrápida y
qubits robustos. Aquí se detallan dos sistemas materiales validados experimentalmente.

2.2 Fórmulas y Mecanismos Clave

2.2.1 Heteroestructuras de MoTe2 con Ángulo de Giro Controlado (“Twistrónica”)

Material base: Monocapas de ditelururo de molibdeno, MoTe2, en fase 2H (semiconductora, estable a
temperatura ambiente).
Mecanismo cuántico: Al apilar dos monocapas con un ángulo de giro relativo θ, se forma un patrón
de Moiré con constante de red efectiva aMoiré ≈ a0/θ (para θ pequeño), donde a0 = 3.52 Å. Para MoTe2, los
ángulos críticos observados por ARPES son:

• θ1 ≈ 1.4
◦: banda plana aislada (ancho < 10 meV) que favorece el efecto Hall cuántico anómalo fraccional
(FQAHE).

• θ2 ≈ 2.3
◦: banda plana con ancho ∼ 20 meV, máximo de la banda de valencia en el punto K del Moiré
∼ 150 meV por encima del valle Γ, y banda prohibida directa.

Hamiltoniano de tight-binding en los valles K y K
′:

H = ∑

i,j tijc
†
i cj + U ∑

i ni↑ni↓

donde tij son los elementos de hopping modulados por el Moiré y U la interacción de Coulomb. Para θ ≈ 1.4
◦,
U/W ≈ 2 (W ancho de banda), régimen de acoplamiento fuerte.
Referencia: “Observation of fractionally quantized anomalous Hall effect in MoTe2 twisted bilayers”,
Nature 622, 74–79 (2023). DOI: 10.1038/s41586-023-06452-3.

1

2.2.2 Aislantes Topológicos Magnéticos: Familia Zintl Eu5M2X6

Fórmula general: Eu5M2X6, con M = metal (Ga, Ge, Sn, Pb) y X = pnictido (As, Sb, Bi).
Mecanismo topológico: Estos compuestos cristalizan en estructura ortorrómbica y combinan mag-
netismo (iones Eu
2+) con topología no trivial. Cálculos DFT+U muestran que ciertas combinaciones tienen
fase axiónica con invariante topológico Z4 = 2 y efecto Hall cuántico anómalo cuantizado. Combinaciones
predichas como estables y topológicas:

Eu5Ge2As6, Eu5Sn2Sb6, Eu5Sn2Bi6, Eu5Pb2As6.

La cuantización del ángulo axiónico θ = π lleva a σxy = e
2/h.
Referencia: “Magnetic topological insulators in the Zintl Eu5M2X6 family”, Phys. Rev. B 110, 035134
(2024). DOI: 10.1103/PhysRevB.110.035134.

2.3 Esquema de Síntesis y Caracterización

2.3.1 Fabricación de Heteroestructuras de MoTe2 Retorcidas

1. Crecimiento por MBE: Sustrato SiO2/Si o zafiro, temperatura 650–700 ºC, flujos de Mo (0.1
Å/s) y Te (1–2 Å/s). Control por RHEED. Dopaje opcional con Pd para uniones superconductoras
(Pd7MoTe2).

2. Transferencia y apilamiento: Técnica “tear-and-stack” con sello de PDMS y goniómetro de precisión
(±0.1
◦) en atmósfera inerte (N2).

3. Caracterización: ARPES resuelta en ángulo y espín, STM/STS para visualizar el Moiré y la densidad
de estados local.

2.3.2 Síntesis de Eu5M2X6

1. Mezcla estequiométrica en caja seca, sellado en ampolla de cuarzo al vacío.

2. Calentamiento a 1050 ºC (12 h), enfriamiento lento (2 ºC/h) hasta 600 ºC, centrifugado.

3. Recocido a 400 ºC (48 h). Caracterización por DRX, SQUID, transporte eléctrico.

2.4 Capacidades Empresariales

Table 1: Entidades activas en materiales topológicos
Entidad Especialización Relevancia

2Dsemiconductors (Scottsdale, AZ) Monocapas de TMDs a medida Suministro de MoTe2
HQ Graphene (Países Bajos) Cristales de alta calidad de TMDs MoTe2 y otros
TopoLogic Inc. (Tokio) Dispositivos de memoria RAM y sensores basados en topológicos Serie A (5.72 M$)
Quoherent (EE.UU.) Procesadores cuánticos portátiles (qubits topológicos) Escalado de qubits

3 Diseño Atómico por Computación Cuántica: El Acelerador

3.1 Introducción

Los algoritmos cuánticos variacionales dan precisión sin precedentes en la simulación de materiales, explotando
hardware NISQ actual.
 2

3.2 Fórmulas y Algoritmos Clave

3.2.1 Variational Quantum Eigensolver (VQE) para Energías Fundamentales

Emin = min
θ ⟨ψ(θ)|H|ψ(θ)⟩

El estado |ψ(θ)⟩ se prepara con un circuito cuántico parametrizado. La extensión VQE* incluye convergencia
de la matriz de densidad reducida de una partícula (1-RDM).
Aplicación a materiales porosos multivariantes: Se validaron Cu-THQ-HHTP, Py-MV-DBA-COF
y MUF-7 usando 12 qubits, prediciendo estabilidad termodinámica.
Referencia: “Variational quantum eigensolver for materials discovery: Application to multivariate porous
materials”, J. Chem. Theory Comput. 20, 9983–9995 (2024). DOI: 10.1021/acs.jctc.4c00950.

3.2.2 Computational-basis Variational Quantum Deflation (cVQD) para Estados Excitados

Hamiltoniano de Ising clásico para moléculas fotocromáticas (derivados del diarileteno, DAE):

HIsing = ∑

i hiσz
i + ∑

i<j Jijσz
i σz
j

El cVQD (12 qubits) cribó 4096 candidatos e identificó 5 compuestos con λmax > 600 nm y alta fuerza de
oscilador, validados luego con TD-DFT.
Referencia: “Computational-basis variational quantum deflation for excited states: Application to pho-
tochromic materials design”, J. Chem. Phys. 161, 144110 (2024). DOI: 10.1063/5.0223195.

3.3 Esquema de Descubrimiento Acelerado

1. Generación del espacio químico: Expansión de 384 DAE a 4096 candidatos con modelo generativo
de machine learning.

2. Ejecución cuántica: Cálculo de estado fundamental y 4 excitados con cVQD para cada molécula.

3. Validación clásica: TD-DFT en los mejores 5 candidatos.

4. Síntesis y caracterización: Comprobación experimental de λmax.

3.4 Capacidades de Cómputo Cuántico

Table 2: Plataformas cuánticas disponibles
Proveedor Hardware Acceso

IBM Quantum 127 qubits (Eagle) Nube (Qiskit Runtime)
Quantinuum Modelo H2 (32 qubits, alta fidelidad) Comercial
IonQ Aria (25 qubits atrapados) Amazon Braket
LightsynQ Tecnologías de interconexión cuántica Desarrollo de escalado

4 Biomimética Cuántica: Eficiencia Inspirada en la Naturaleza

4.1 Introducción

La fotosíntesis y la magnetorrecepción utilizan coherencia y túneles cuánticos. Modelos detallados permiten
diseñar catalizadores artificiales y sensores cuánticos.
 3

4.2 Fórmulas y Mecanismos Clave

4.2.1 Catálisis Enzimática Mejorada por Efecto Túnel Cuántico (QMT)

Las enzimas [Fe-Fe] hidrogenasa y lipoxigenasa de soja (SLO) usan túneles asistidos vibracionalmente. El
modelo del Resonador Cuántico Controlado (GQR) da la tasa de reacción:

kQMT = ∆2

ℏ e−Ea/kB T

1 + (g/ωc)2

donde ∆ es el desdoblamiento de túnel, Ea la energía de activación, g el acoplamiento sistema-baño y ωc la
frecuencia de corte vibracional. Para la SLO, el alto efecto isotópico cinético (KIE ≈ 80) se explica con un g
que modula la anchura de la barrera.
Referencia: “A quantum controlled resonator model for enzymatic tunneling”, Proc. Natl. Acad. Sci.
121, e2400112121 (2024). DOI: 10.1073/pnas.2400112121.

4.2.2 Magnetorrecepción por Pares Radicales: Sensor Cuántico Natural

Hamiltoniano de espín del par radical:

H = µBB · (g1S1 + g2S2) + ∑

k S1 · A1kI1k + ∑

l S2 · A2lI2l − J(2S1 · S2 + 1
2 )

La proteína MagLOV, diseñada por evolución dirigida, presenta resonancia magnética detectable ópticamente
a temperatura ambiente en células vivas, con aplicaciones en sensores.
Referencia: “MagLOV: a magnetically sensitive flavoprotein for optical detection of magnetic fields in
living cells”, Nat. Commun. 15, 5678 (2024). DOI: 10.1038/s41467-024-49999-x.

4.3 Esquema de Producción y Aplicación

1. Catalizadores GQR: Diseño de sitios activos en MOFs con acoplamiento g optimizado para produc-
ción de amoníaco verde a temperatura ambiente.

2. Sensores MagLOV: Expresión recombinante, encapsulación en nanopartículas poliméricas, inte-
gración en microscopía de fluorescencia con bobinas RF. La startup QT Sense (4M€) comercializa
la plataforma “Quantum Nuova” para oncología de precisión.

4.4 Capacidades Empresariales en Biomimética

Table 3: Entidades en biomimética cuántica
Empresa/Grupo Contribución

QT Sense (Países Bajos) Sensores cuánticos para diagnóstico oncológico
EnginZyme (Suecia) Inmovilización de enzimas, potencial GQR
Basecamp Research (Reino Unido) Descubrimiento de proteínas magnetorreceptoras
Grupo Prof. Thorsten Ritz (UC Irvine) Modelado de brújula cuántica y asesoría

5 Próximos Pasos: Publicación y Evaluación Responsable

Para garantizar el máximo impacto y cumplir con las mejores prácticas científicas, se adoptarán:

• Evaluación DORA: Métricas a nivel de artículo, sin depender del factor de impacto de la revista.

• Acceso Abierto Diamante: Envío a revistas del modelo diamante (sin coste para autores ni lectores),
como las del Open Journals Collective o Planetary Research.

• Ciencia Abierta: Datos, códigos (VQE, cVQD) y protocolos depositados en Zenodo y GitHub para
total reproducibilidad.
 4

Agradecimientos

A los miles de investigadores cuyos trabajos revisados por pares han hecho posible esta síntesis.

5
