> Texto extraído automáticamente del PDF original «Libro_Blanco_Sensores_Cuanticos.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1m97g-wx5ViOwUc1tpnV0Sp_G0Oq8j4Bj/view?usp=drivesdk



Libro Blanco de Sensores Cuánticos,
Biosensores y Simulación Cuántica
para Medicina y Neurociencia
 Lázaro López Paz

El Prat de Llobregat, Barcelona, España
 Julio de 2026

Licencia: Este documento se publica bajo licencia Creative Commons Atribución
4.0 Internacional (CC BY 4.0) . Usted es libre de compartir y adaptar el material para
cualquier propósito, incluso comercialmente, siempre que dé crédito de manera adecuada
a Lázaro López Paz , incluya un enlace a la licencia e indique si se han realizado cambios.
Véase: https://creativecommons.org/licenses/by/4.0/ .

Aviso de autoría: La organización de ideas, la estructura de proyectos, los textos y las
arquitecturas propuestas son obra original de Lázaro López Paz, basados en conocimiento
cientí˝co general y referencias abiertas, sin copiar contenidos literales de proyectos publicados.
 Abstract

Este Libro Blanco presenta un conjunto coherente e interconectado de proyectos orientados
al diseño, desarrollo y validación de sensores cuánticos de campo magnético (centros
NV en diamante, defectos en hBN y magnetómetros ópticamente bombeados OPM),
biosensores avanzados e integración con plataformas organ-on-a-chip para aplicaciones
en neurociencia, cardiología y diagnóstico precoz de enfermedades neurodegenerativas.
Se detallan fundamentos teóricos (efecto Zeeman, dinámica de polarización, modelos de
impedancia y plegamiento proteico), diseños experimentales, protocolos de calibración,
algoritmos de análisis de señales y de detección temprana, así como la integración con
datos clínicos e inteligencia arti˝cial. Todos los proyectos se publican bajo licencia CC
BY 4.0 para fomentar la colaboración abierta y la reproducibilidad cientí˝ca.

Libro Blanco de Sensores Cuánticos Lázaro López Paz

Palabras clave: sensores cuánticos, centros NV, diamante, hBN, OPM-MEG, magnetocardiografía,
organ-on-a-chip, neurodegeneración, Alzheimer, Parkinson, biosensores, simulación cuántica.
 1

Contents

Introducción general 3

1 Proyecto 1  Sensor cuántico de campo magnético (NV, hBN) 4
1.1 Objetivo general . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.2 Fundamento teórico . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.2.1 Espines electrónicos y efecto Zeeman . . . . . . . . . . . . . . . . . 4
1.2.2 Lectura óptica y control por microondas . . . . . . . . . . . . . . . 5
1.3 Diseño experimental . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
1.3.1 Con˝guración del sensor . . . . . . . . . . . . . . . . . . . . . . . . 5
1.3.2 Protocolo de resonancia . . . . . . . . . . . . . . . . . . . . . . . . 5
1.4 Algoritmos de calibración y sensibilidad . . . . . . . . . . . . . . . . . . . . 6
1.4.1 Calibración del campo magnético . . . . . . . . . . . . . . . . . . . 6
1.4.2 Estimación de sensibilidad . . . . . . . . . . . . . . . . . . . . . . . 6
1.5 Adquisición y procesamiento de señales dinámicas . . . . . . . . . . . . . . 6
1.6 Validación experimental . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
1.7 Aplicaciones en neurociencia y cardiología . . . . . . . . . . . . . . . . . . 7

2 Proyecto 2  Sensores OPM-MEG para detección precoz de neurodegeneración 8
2.1 Objetivo general . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
2.2 Fundamento cientí˝co . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
2.2.1 Campos magnéticos cerebrales y neurodegeneración . . . . . . . . . 8
2.2.2 Funcionamiento de los OPM . . . . . . . . . . . . . . . . . . . . . . 8
2.2.3 Sensibilidad de OPM . . . . . . . . . . . . . . . . . . . . . . . . . . 9
2.3 Diseño experimental . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
2.3.1 Con˝guración de medición . . . . . . . . . . . . . . . . . . . . . . . 10
2.3.2 Estructuras de datos . . . . . . . . . . . . . . . . . . . . . . . . . . 10
2.4 Algoritmos y procedimientos . . . . . . . . . . . . . . . . . . . . . . . . . . 10
2.4.1 Análisis de velocidad de propagación . . . . . . . . . . . . . . . . . 10
2.4.2 Análisis espectral y de conectividad . . . . . . . . . . . . . . . . . . 11
2.4.3 Algoritmo de detección precoz . . . . . . . . . . . . . . . . . . . . . 11
2.5 Integración con biomarcadores moleculares y organ-on-a-chip . . . . . . . . 12
 2

Libro Blanco de Sensores Cuánticos Lázaro López Paz

3 Proyecto 3  Organ-on-a-chip con biosensores cuánticos 13
3.1 Objetivo general . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
3.2 Fundamento cientí˝co . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
3.2.1 Organ-on-a-chip y micro˝siología . . . . . . . . . . . . . . . . . . . 13
3.2.2 Sensores integrados en OoC . . . . . . . . . . . . . . . . . . . . . . 13
3.3 Diseño del dispositivo OoC . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
3.3.1 Arquitectura física . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
3.4 Modelos matemáticos . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
3.4.1 Dinámica de concentración de especies . . . . . . . . . . . . . . . . 14
3.4.2 Modelo de sensor eléctrico FG-FET . . . . . . . . . . . . . . . . . . 14
3.4.3 Modelo de TEER e impedancia de monocapa . . . . . . . . . . . . 15
3.4.4 Biosensores cuánticos de plegamiento de proteínas . . . . . . . . . . 15
3.5 Protocolos de adquisición de datos . . . . . . . . . . . . . . . . . . . . . . 15
3.5.1 Estructura de datos . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
3.5.2 Protocolo típico . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
3.6 Validación y perspectivas . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16

4 Conclusiones y hoja de ruta 17

3

Introducción general

La física cuántica ha pasado de ser un campo fundamental a sostener tecnologías de uso
cotidiano como el láser, la resonancia magnética y la ˝bra óptica. Entre las tecnologías
emergentes más prometedoras se encuentran los sensores cuánticos, capaces de medir con
precisión sin precedentes magnitudes físicas como campos magnéticos, campos eléctricos
y propiedades químicas de muestras muy pequeñas [2, 3].
En neurociencia y cardiología, los campos magnéticos generados por neuronas y células
del miocardio son extremadamente débiles y difíciles de medir con sensores convencionales.
Los dispositivos basados en centros NV en diamante, defectos cuánticos en materiales
bidimensionales y magnetómetros ópticamente bombeados (OPM) han demostrado ser
capaces de detectar campos en el rango de picotesla y por debajo, abriendo la posibilidad
de registrar actividad neuronal y cardíaca con mayor resolución y menor invasividad [4,
5, 6]. Este libro blanco presenta un conjunto coherente de proyectos para:

‹ diseñar y desplegar sensores cuánticos de campo magnético para neurociencia y
cardiología,

‹ desarrollar biosensores avanzados para biomarcadores neurodegenerativos,

‹ integrar organ-on-a-chip con sensores cuánticos,

‹ usar simulación cuántica de moléculas en el diseño de fármacos,

‹ integrar todo en una plataforma de IA y datos clínicos,

‹ acompañar esta evolución con un marco ético, social y teológico robusto.

Todos los proyectos se publican bajo licencia CC BY 4.0, para que cualquier equipo del
mundo pueda usarlos, adaptarlos y mejorarlos, reconociendo la autoría de Lázaro López
Paz.
 4

Chapter 1

Proyecto 1  Sensor cuántico de campo
magnético (NV, hBN)

1.1 Objetivo general

Diseñar e implementar un sensor cuántico de campo magnético basado en defectos de espín
en sólidos (centros NV en diamante y defectos en materiales 2D como hBN) para medir
campos magnéticos débiles en entornos de laboratorio, con aplicaciones en neurociencia y
cardiología.

1.2 Fundamento teórico

1.2.1 Espines electrónicos y efecto Zeeman

El sensor se basa en defectos de espín en sólidos, como centros NV en diamante o vacantes
de boro en nitruro de boro hexagonal (hBN), que poseen niveles de energía dependientes
del campo magnético. La separación de estos niveles se describe mediante el efecto
Zeeman:
 ∆E = gµBB (1.1)

y la frecuencia de resonancia asociada es:
 f = ∆E
h = gµB
h B (1.2)

donde g es el factor g, µB el magnetón de Bohr y h la constante de Planck. Para
centros NV en diamante, el factor giromagnético es γ ≈ 2.8 × 10
10 Hz/T, y la frecuencia
de transición se puede aproximar como:
 f (B) ≈ f0 + γB (1.3)

5

Libro Blanco de Sensores Cuánticos Lázaro López Paz

1.2.2 Lectura óptica y control por microondas

La lectura del estado de espín se realiza mediante ˛uorescencia inducida por un láser
(típicamente verde, ∼ 532 nm) que excita el defecto cuántico. La aplicación de microondas
permite resonar entre niveles de espín, produciendo cambios característicos en la intensidad
de la luz roja emitida al retornar al estado fundamental. Escaneando la frecuencia de
microondas y registrando la ˛uorescencia se obtiene un espectro de resonancia sensible al
campo magnético externo.

1.3 Diseño experimental

1.3.1 Con˝guración del sensor

El sistema se compone de:

‹ Muestra sólida (diamante con centros NV o hBN con defectos cuánticos).

‹ Fuente de láser verde para excitación óptica.

‹ Óptica de enfoque y colección (objetivos, lentes).

‹ Generador de microondas y antena próxima a la muestra.

‹ Fotodetector o cámara para lectura de ˛uorescencia.

‹ Bobinas o imanes para generar campos de referencia en calibraje.

‹ Electrónica de adquisición y control.

1.3.2 Protocolo de resonancia

El procedimiento básico para encontrar la frecuencia de resonancia consiste en:

1. Aplicar un campo magnético de referencia Bref.

2. Barrer la frecuencia de microondas en un rango adecuado.

3. Registrar la ˛uorescencia I(f ).

4. Identi˝car el mínimo o máximo en I(f ) correspondiente a la resonancia f0.

Este protocolo se repite para distintos valores de Bref durante la fase de calibración.

6

Libro Blanco de Sensores Cuánticos Lázaro López Paz

1.4 Algoritmos de calibración y sensibilidad

1.4.1 Calibración del campo magnético

Con las medidas de ˛uorescencia I(f ) y los campos de referencia, se obtiene una relación
práctica entre la frecuencia de resonancia y el campo efectivo:

1. Detección de f0 mediante búsqueda de extremos en I(f ).

2. Relación teórica: Bterico = h
gµB f0 (1.4)

3. Ajuste lineal con los campos de referencia:
 Bmedido = αBref + β (1.5)

para corregir desviaciones experimentales.

4. Uso posterior:
 Bestimado = α h
gµB f0 + β (1.6)

La calidad de la calibración se evalúa comparando Bestimado con Bref y analizando el
error relativo y la desviación estándar.

1.4.2 Estimación de sensibilidad

La sensibilidad η se de˝ne como:
 η = σB√T (1.7)

donde σB es la desviación estándar en la medición de un campo constante durante un
tiempo T . Esta magnitud se expresa frecuentemente en unidades de T/
√
Hz y se compara
en escala logarítmica:
 Lη = log10(η) (1.8)

lo que facilita evaluar mejoras sucesivas del sensor.

1.5 Adquisición y procesamiento de señales dinámicas

Para medir actividad neuronal o cardíaca, la frecuencia de microondas se ˝ja en una
condición óptima de sensibilidad y se registra la ˛uorescencia I(t) a lo largo del tiempo.

7

Libro Blanco de Sensores Cuánticos Lázaro López Paz

Usando la relación de calibración, se convierte I(t) en una señal de campo magnético
B(t).
El procesamiento incluye:

1. Preprocesamiento: eliminación de tendencia y ˝ltrado pasa-banda según banda de
interés.

2. Transformada de Fourier para obtener el espectro X(f ).

3. Detección de picos y cálculo de potencia en diferentes bandas de frecuencia.

4. Compresión logarítmica de amplitudes:
 Alog(f ) = log(1 + |X(f )|
) (1.9)

para visualizar y comparar señales débiles y fuertes.

1.6 Validación experimental

La validación inicial incluye:

‹ Medición de campos generados por bobinas calibradas.

‹ Comparación del campo estimado con el valor teórico.

‹ Evaluación de linealidad, ruido y sensibilidad global.

‹ Comparación con magnetómetros clásicos y técnicas existentes.

1.7 Aplicaciones en neurociencia y cardiología

En neurociencia, los sensores cuánticos permiten medir campos magnéticos producidos
por neuronas individuales o pequeñas poblaciones, lo que podría facilitar la detección de
cambios funcionales antes de que se mani˝esten clínicamente. En cardiología, registrar el
campo magnético del corazón complementa la electrocardiografía clásica, proporcionando
información adicional sobre la dinámica eléctrica del miocardio.
 8

Chapter 2

Proyecto 2  Sensores OPM-MEG para
detección precoz de neurodegeneración

2.1 Objetivo general

Desarrollar un sistema basado en magnetómetros ópticamente bombeados (OPM)
capaz de detectar cambios tempranos en la actividad cerebral asociados a enfermedades
neurodegenerativas (Alzheimer, Parkinson, demencia, ELA), mejorando la sensibilidad y
precisión respecto a técnicas clásicas como EEG y fMRI.

2.2 Fundamento cientí˝co

2.2.1 Campos magnéticos cerebrales y neurodegeneración

Cuando las neuronas disparan, generan corrientes eléctricas que producen campos magnéticos
muy débiles, que pueden medirse con técnicas como magnetoencefalografía (MEG). Sensores
cuánticos basados en OPM pueden acercarse más al cráneo y ofrecer mediciones con alta
resolución temporal y espacial.
En enfermedades neurodegenerativas, se observa a menudo una ralentización en
la velocidad de propagación de las señales y cambios en patrones de actividad y
conectividad, incluso antes de la aparición de síntomas clínicos claros.

2.2.2 Funcionamiento de los OPM

Un OPM se puede modelar como un sistema donde el estado de polarización del
vapor responde al campo magnético externo y esa respuesta se observa como cambio en
la intensidad de luz medida por el fotodiodo.
De˝nimos:

‹ P (t): grado de polarización del vapor (entre 0 y 1).
 9

Libro Blanco de Sensores Cuánticos Lázaro López Paz

‹ B(t): campo magnético externo (neuromagnético + ruido).

‹ I(t): intensidad de luz en el fotodiodo.

Modelo cualitativo:

1. Dinámica de polarización:
 dP
dt = Rpump(1 − P ) − Γ(B)P (2.1)

donde Rpump es la tasa de bombeo óptico y Γ(B) la tasa de despolarización dependiente
del campo magnético.

2. Intensidad de luz: I(t) = I0(1 − αP (t)
) (2.2)

donde I0 es la intensidad máxima (vapor transparente) y α un coe˝ciente que
relaciona polarización con absorción.

En régimen estacionario ( dP
dt = 0
)
, para un campo B aproximadamente constante:

Peq(B) = Rpump
Rpump + Γ(B) (2.3)

Ieq(B) = I0
 (
1 − α Rpump
Rpump + Γ(B)
) (2.4)

De forma práctica, alrededor de un punto de operación se linealiza:
 I(B) ≈ I(B0) + kB(B − B0) (2.5)

donde kB es la sensibilidad local (derivada de I respecto a B en B0).

2.2.3 Sensibilidad de OPM

La sensibilidad magnética de un sensor cuántico se puede expresar en términos de parámetros
experimentales como contraste, ancho de línea y tasa de detección de fotones. Para OPM:
 ηOPM ≈ σB√T (2.6)

donde σB es la desviación estándar de mediciones de campo en tiempo T y la sensibilidad
se expresa habitualmente en fT/
√Hz.
 10

Libro Blanco de Sensores Cuánticos Lázaro López Paz

2.3 Diseño experimental

2.3.1 Con˝guración de medición

‹ Sensores OPM dispuestos en casco o arreglo cercano al cráneo.

‹ Sistema de registro de señales: adquisición continua de campos magnéticos B(t, r)
en varias posiciones r.

‹ Protocolo de estimulación: estímulos sensoriales (visuales, auditivos) o tareas cognitivas
para provocar respuestas reproducibles.

2.3.2 Estructuras de datos

Sea N el número de canales (sensores) y M el número de muestras (instantes de tiempo
o mapas de campo). De˝nimos:
 X ∈ R
N ×M , Xi,k = Bi(tk) (2.7)

donde i = 1, . . . , N (canal) y k = 1, . . . , M (instante).
A partir de X, se construyen:

‹ Media por canal:
 ¯Xi = 1
M
 M∑

k=1 Xi,k (2.8)

‹ Covarianza entre canales i y j:

Kij = 1
M
 M∑

k=1
(Xi,k − ¯Xi)(Xj,k − ¯Xj) (2.9)

‹ Correlación normalizada: Cij = Kij
σiσj (2.10)

donde σi es la desviación estándar del canal i.

2.4 Algoritmos y procedimientos

2.4.1 Análisis de velocidad de propagación

La idea central es medir cómo la señal se desplaza entre regiones cerebrales y si se ralentiza
con el tiempo.

1. Identi˝car eventos de disparo (picos o cambios rápidos) en una región de referencia.
 11

Libro Blanco de Sensores Cuánticos Lázaro López Paz

2. Medir tiempos de llegada de eventos correlacionados en otras regiones.

3. Calcular velocidad efectiva de propagación:
 vefectiva = d
∆t (2.11)

donde d es la distancia entre regiones y ∆t el retraso medio observado.

4. Repetir mediciones en distintas sesiones (por ejemplo, cada varios meses).

5. Analizar tendencia: si vefectiva disminuye signi˝cativamente con el tiempo, puede
indicar procesos neurodegenerativos tempranos.

2.4.2 Análisis espectral y de conectividad

1. Calcular espectros de potencia para cada región.

2. Evaluar cambios en bandas (theta, alpha, beta, gamma), que pueden asociarse a
estados cognitivos y patológicos.

3. Calcular medidas de conectividad funcional (coherencia, correlaciones cruzadas)
entre regiones.

4. Observar patrones de desconexión o reorganización asociados a enfermedad.

2.4.3 Algoritmo de detección precoz

Entrada: vectores de características para cada sesión (velocidad de propagación, parámetros
espectrales, conectividad).Procedimiento:

1. Construir un modelo de progresión normal (a partir de sujetos sanos o simulaciones).

2. Comparar el per˝l de cada sujeto con el modelo normal.

3. Calcular índices de desviación (por ejemplo, z-scores para velocidad, potencia en
bandas).

4. De˝nir umbrales para posible neurodegeneración temprana basados en desviaciones
signi˝cativas.

Con IA, se puede entrenar un clasi˝cador que combine todos estos indicadores para
emitir una señal de alerta temprana.
 12

Libro Blanco de Sensores Cuánticos Lázaro López Paz

2.5 Integración con biomarcadores moleculares y organ-

on-a-chip

La convergencia de biosensores cuánticos y organ-on-a-chip está emergiendo como frontera
en diagnóstico avanzado. Se propone:

‹ integrar datos de OPM-MEG con biomarcadores de proteínas mal plegadas (beta-
amiloide, alfa-sinucleína),

‹ usar organ-on-a-chip que reproduzca funciones cerebrales o barrera hematoencefálica,

‹ combinar datos de chip y de cerebro real para entender y validar mecanismos de
enfermedad.
 13

Chapter 3

Proyecto 3  Organ-on-a-chip con
biosensores cuánticos

3.1 Objetivo general

Diseñar y validar un sistema organ-on-a-chip (OoC) que integre biosensores (eléctricos,
ópticos y cuánticos) para monitorizar en tiempo real procesos celulares y moleculares
relevantes en enfermedades (incluidas neurodegenerativas y cardiovasculares), facilitando
diagnóstico avanzado y estudio de fármacos.

3.2 Fundamento cientí˝co

3.2.1 Organ-on-a-chip y micro˝siología

Los OoC son sistemas micro˛uídicos que replican funciones de órganos humanos (pulmón,
hígado, corazón, cerebro, barrera hematoencefálica) mediante células humanas en entornos
controlados. Permiten recrear condiciones mecánicas (˛ujo, presión, deformación), estudiar
respuesta a fármacos, toxinas, in˛amación, y reducir dependencia de modelos animales.

3.2.2 Sensores integrados en OoC

Los sensores en OoC se integran para monitorizar variables físicas (presión, ˛ujo, potencial
eléctrico), químicas (pH, oxígeno, metabolitos) y bioquímicas (biomarcadores de proteínas,
estados de plegamiento). Se clasi˝can en sensores eléctricos, electroquímicos, ópticos y,
en proyectos avanzados, cuánticos (como NV, OPMs, sensores infrarrojos láser).
 14

Libro Blanco de Sensores Cuánticos Lázaro López Paz

3.3 Diseño del dispositivo OoC

3.3.1 Arquitectura física

Un diseño típico incluye:

‹ Canales micro˛uídicos para ˛ujo de medios y fármacos.

‹ Cámara de tejido donde se cultivan células (ej. neuronas, cardiomiocitos, células
epiteliales).

‹ Sensores integrados en paredes o super˝cie:

 electrodos TEER y de impedancia,

 microelectrodos para potencial de acción,

 sensores de pH/oxígeno,

 interfaces para sensores cuánticos (nanodiamantes NV, sensores infrarrojos
láser).

3.4 Modelos matemáticos

3.4.1 Dinámica de concentración de especies

Para cualquier metabolito o fármaco C(t) en la cámara:

dC
dt = −kC + F (t) (3.1)

donde k es la tasa de eliminación y F (t) la función fuente (entrada por perfusión,
liberación desde células). Si el ˛ujo es constante y F (t) = F0:

C(t) = Ceq + (C0 − Ceq)e−kt, Ceq = F0
k (3.2)

3.4.2 Modelo de sensor eléctrico FG-FET

El sensor de puerta ˛otante responde a cambios de carga cerca del electrodo.

‹ Carga total en la super˝cie: QS.

‹ Capacitancia total relevante: Ctot.

‹ Umbral de tensión: Vth = Vth,0 + QS
Ctot (3.3)

15

Libro Blanco de Sensores Cuánticos Lázaro López Paz

‹ Corriente de drenador (régimen simpli˝cado, lineal):
 ID ≈ µCox W
L (VG − Vth)VD (3.4)

Cambios en QS debido a biomoléculas o actividad celular producen cambios medibles
en ID.

3.4.3 Modelo de TEER e impedancia de monocapa

La trans-epithelial/endothelial electrical resistance (TEER) es un indicador del
estado de una barrera de células epiteliales o endoteliales. Se mide la resistencia RTEER a
través de la monocapa:
 RTEER = V
I (3.5)

3.4.4 Biosensores cuánticos de plegamiento de proteínas

La señal espectroscópica S depende del estado de plegamiento de la proteína:

S = S0 + ∆S · θβ (3.6)

donde θβ es la fracción de proteína en con˝guración beta patológica, S0 la señal basal
y ∆S la contribución máxima de estructuras patológicas.

3.5 Protocolos de adquisición de datos

3.5.1 Estructura de datos

Para cada experimento en OoC:

‹ ID_experimento, Fecha_hora.

‹ Con˝guracion_chip (tipo de tejido, ˛ujo, sensores activos).

‹ C(t) para cada especie importante (registro o simulación).

‹ ID(t) y Vth(t) para sensores eléctricos.

‹ RTEER(t) para barrera.

‹ S(t) espectroscópico para plegamiento de proteínas.

‹ B(t) si se usan sensores cuánticos NV u OPM para campos.
 16

Libro Blanco de Sensores Cuánticos Lázaro López Paz

3.5.2 Protocolo típico

1. Preparar chip: esterilización, recubrimiento de super˝cie (matriz extracelular, poli-
L-lisina, etc.) y montaje en el sistema de ˛ujo.

2. Sembrar células humanas (neuronas, cardiomiocitos, células endoteliales o modelos
iPSC) a la densidad adecuada.

3. Equilibrar el cultivo bajo ˛ujo controlado durante 2472 h hasta alcanzar con˛uencia
o madurez funcional (evaluada por TEER o potencial de acción).

4. Introducir estímulos o fármacos según el diseño experimental (concentración, tiempo
de exposición).

5. Adquirir de forma continua o periódica las señales de todos los sensores integrados
( ID, RTEER, S, B, etc.).

6. Al ˝nalizar, realizar análisis de viabilidad celular, ˝jación o extracción de muestras
para validación ortogonal (ELISA, inmunocitoquímica, transcriptómica).

7. Procesar y almacenar los datos en formato estructurado para posterior análisis con
modelos matemáticos e IA.

3.6 Validación y perspectivas

La validación del sistema OoC incluye la comparación de respuestas farmacológicas con
datos de literatura y modelos animales, la evaluación de la reproducibilidad entre chips y
lotes, y la demostración de que los sensores cuánticos aportan información complementaria
(por ejemplo, campos locales o estados de plegamiento) no accesible con sensores clásicos.
A largo plazo, estos sistemas pueden reducirse de tamaño, automatizarse e integrarse en
plataformas de alto rendimiento para screening de fármacos y medicina personalizada.
 17

Chapter 4

Conclusiones y hoja de ruta

Los tres proyectos presentados forman un continuum tecnológico: desde sensores cuánticos
de campo magnético de alta sensibilidad (Proyecto 1), pasando por sistemas OPM-MEG
orientados a la detección precoz de neurodegeneración (Proyecto 2), hasta la integración
de dichos sensores en plataformas organ-on-a-chip que permiten estudiar mecanismos
celulares y moleculares en condiciones ˝siológicamente relevantes (Proyecto 3).
Las siguientes etapas prioritarias incluyen:

‹ prototipado experimental de los sensores NV/hBN y OPM en entornos de laboratorio
controlado;

‹ desarrollo de software de adquisición, calibración y análisis de señales en tiempo
real;

‹ fabricación de chips micro˛uídicos con interfaces cuánticas y validación biológica;

‹ estudios piloto con muestras clínicas o modelos de enfermedad;

‹ elaboración de protocolos de ética, privacidad de datos y gobernanza de IA médica;

‹ publicación de resultados intermedios bajo la misma licencia abierta CC BY 4.0.

Este Libro Blanco se ofrece como base abierta, reproducible y mejorable por la comunidad
cientí˝ca internacional. Cualquier contribución, crítica o extensión será bienvenida, siempre
que se respete la autoría original y la licencia de uso.

Autor: Lázaro López Paz
El Prat de Llobregat, Barcelona, España
Julio de 2026
 18

Bibliography

[1] Creative Commons. Creative Commons Attribution 4.0 International License . https:
//creativecommons.org/licenses/by/4.0/ , 2013.

[2] Aslam, N. et al. Quantum sensors for biomedical applications. Nature Reviews
Physics , 5:157169, 2023. https://doi.org/10.1038/s42254-023-00558-3 .

[3] Lo Fiego, A. et al. How quantum biosensing is transforming healthcare.
Nature Reviews Physics , 7:672674, 2025. https://doi.org/10.1038/
s42254-025-00890-w .

[4] Barry, J. F. et al. Optical magnetic detection of single-neuron action potentials
using quantum defects in diamond. Proceedings of the National Academy of Sciences ,
113(49):1413314138, 2016. Véase también revisiones posteriores sobre NV-diamond
en neuroimagen.

[5] Boto, E. et al. / Brookes, M. J. et al. Magnetoencephalography with optically pumped
magnetometers (OPM-MEG): the next generation of functional neuroimaging.
Revisiones en Trends in Neurosciences y NeuroImage , 20222024. PMCID:
PMC10465236.

[6] Zhang, Y. et al. Noninvasive magnetocardiography of a living rat based on a diamond
quantum sensor. Physical Review Applied , 21:064028, 2024. Véase también sistemas
OPM-MCG de sobremesa.
 19
