> Texto extraído automáticamente del PDF original «Ordenador híbrido @.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1s-tFouvGwZ2Tcia3sq3_bA3gX2dzeoGe/view?usp=drivesdk



ORDENADOR NO BINARIO HIBRIDO DE
ULTRA-BAJO CONSUMO

Estudio de viabilidad, arquitectura de referencia y plan de
investigacion

Autor: Lazaro Lopez Paz

Afiliacion: Investigador independiente, Cataluna, Espana

Apoyo tecnico: Sistema de inteligencia artificial

Fecha: 8 de septiembre de 2026

Version: 1.0

INDICE

1. Declaracion de alcance

2. Fundamentos fisicos

3. Tecnologias candidatas

4. Arquitectura de referencia

5. Modelos y metricas

6. Metodologia reproducible

7. Escenarios prospectivos

8. Riesgos y mitigacion

9. Verificacion y falsabilidad

10. Plan de I+D

11. Gobernanza

12. Conclusiones

RESUMEN EJECUTIVO

Este documento analiza la viabilidad de una plataforma computacional no binaria e
hibrida orientada a reducir la energia por tarea y densidad de potencia en cargas de
trabajo especificas. La propuesta no presupone que la logica multinivel sustituya al
CMOS binario universalmente; plantea una arquitectura heterogenea donde cada
dominio fisico se usa donde aporta ventaja verificable.

El principio de Landauer establece que el coste termodinamico minimo de borrar
informacion equivalente a un bit permanece en k_B*T*ln(2), tambien en sistemas
multivaluados. Emplear mas niveles no reduce el limite energetico por bit equivalente.
La ventaja posible esta en reduccion de interconexiones, densidad de informacion por
simbolo, computo en memoria y especializacion de tareas.

Palabras clave: computacion heterogenea, logica multinivel, memristores, computacion
en memoria, fotonica integrada, eficiencia energetica.

1. DECLARACION DE ALCANCE

Este manuscrito es una propuesta tecnico-cientifica y hoja de ruta de investigacion. No
comunica fabricacion, demostracion experimental ni validacion independiente de un
ordenador no binario hibrido. Las cifras prospectivas se separan de limites fisicos
establecidos y resultados que requeririan validacion experimental.

1.1 Pregunta de investigacion

Puede una arquitectura heterogenea, que combine control binario, estados multinivel
locales, computo en memoria e interconexiones fotonico selectivas, mejorar de forma
medible la energia por tarea y densidad de potencia frente a una linea base CMOS
para cargas especificas?

1.2 Hipotesis

H1. La logica multinivel no reduce por si sola la energia minima de borrado por bit
equivalente.

H2. Estados multinivel pueden reducir trafico de datos y area efectiva cuando variabilidad,
retencion y tasa de error son controlables.

H3. El computo en memoria resistiva puede reducir energia de movimiento de datos en
operaciones vector-matriz con tolerancia a precision limitada.

H4. La fotonica integrada puede ser ventajosa en enlaces de alto ancho de banda o entre
chiplets, no necesariamente en distancias cortas.

H5. El sistema hibrido sera competitivo solo si la ganancia de aceleradores supera
sobrecarga de conversion, programacion, calibracion y correccion de errores.

2. FUNDAMENTOS FISICOS

2.1 Limite de Landauer

En proceso irreversible, borrado de un bit: E_Landauer >= k_B*T*ln(2), donde k_B es
constante de Boltzmann y T temperatura absoluta. A temperatura ambiente, limite es
~10^-21 J por bit, muy inferior al consumo practico actual.

Para sistema de base b: E_erase,symbol >= k_B*T*ln(b). Como simbolo de base b
codifica log2(b) bits, limite por bit equivalente es: (k_B*T*ln(b))/log2(b) = k_B*T*ln(2).
Representacion multivaluada no evade limite de Landauer por bit equivalente.

2.2 Computacion reversible y conmutacion adiabatica

Computacion reversible preserva informacion para reconstruir estados de entrada. Evita
borrado logico pero no elimina perdidas por resistencia, fugas, ruido y control. Para carga
adiabatica de capacidad C por resistencia R, en regimen T_sw >> RC: E_adia es
proporcional a (RC/T_sw)*C*V^2. Reducir disipacion exige aumentar tiempo de
conmutacion.

2.3 Ruido termico y discriminacion de niveles

Ruido termico en nodo capacitivo ideal: sigma_V = sqrt(k_B*T/C). Para T=300K y C=1fF:
sigma_V ~= 2.0mV. Si rango de tension es V_DD y se representan b niveles
equiespaciados, separacion ideal es: Delta_V = V_DD/(b-1).

Base (b) Bits/simbolo Delta_V (mV) Delta_V/sigma

2 1.00 500 250

3 1.58 250 125

4 2.00 167 83

8 3.00 71 36

16 4.00 33 17

Tabla es cota idealizada. Diseno real debe incorporar ruido de alimentacion, interferencia,
1/f, acoplo, dispersion de umbrales, deriva, variabilidad proceso-voltaje-temperatura y
errores de lectura.

2.4 Capacidad de canal y coste de conversion

Canal gaussiano ideal: C_canal = B*log2(1+SNR), donde B es ancho de banda y SNR
relacion senal-ruido. Incrementar niveles discretos no mejora automaticamente eficiencia
energetica.

Energia total operacion multinivel: E_total = E_conmutacion + E_lectura + E_escritura +
E_DAC/ADC + E_calibracion + E_ECC + E_interconexion. Base optima debe
determinarse mediante simulacion y caracterizacion de arquitectura concreta.

3. TECNOLOGIAS CANDIDATAS

3.1 CMOS binario como linea base

CMOS binario se adopta como referencia por madurez, escalabilidad industrial, robustez,
ecosistema de herramientas, integracion y compatibilidad de software. Toda afirmacion de
mejora debe compararse con nodo tecnologico, biblioteca estandar, proceso de
fabricacion y carga de trabajo explicitos.

3.2 Dispositivos resistivos y memoria multinivel

Dispositivos resistivos basados en oxidos de hafnio pueden exhibir multiplos estados de
conductancia. Utilidad a escala de sistema depende de retencion, endurance, dispersion,
linealidad, deriva y coste de programacion. Oportunidad principal es memoria no volatil y
operaciones analogicas o mixtas de multiplicacion vector-matriz dentro o cerca de
memoria.

3.3 Materiales bidimensionales

Dicalcogenuros de metales de transicion, como MoS2, ofrecen interes por espesor
atomico, banda prohibida e integracion heterogenea. Contactos, movilidad efectiva,
defectos, uniformidad de oblea y encapsulado son limitaciones criticas. Grafeno ofrece
alta movilidad para interconexion, RF y optoelectronica, pero ausencia de banda prohibida
intrinseca limita uso como transistor logico digital.

3.4 TFET y operacion de bajo voltaje

Transistores de efecto tunel de campo se investigan para reducir tension de alimentacion y
consumo dinamico. Reto es alcanzar corrientes de conduccion, uniformidad y
manufacturabilidad suficientes sin perder ventaja teorica de pendiente subumbral.

3.5 Fotonica integrada

Interconexion fotonica integrada puede disminuir energia por bit en comunicaciones de
alto ancho de banda, especialmente en enlaces de mayor alcance fisico o entre chiplets.
Beneficios deben incluir laseres, moduladores, detectores, control termico, perdidas
opticas y conversion electrooptica.

3.6 Computacion cuantica

Coprocesadores cuanticos no son via general para reducir consumo de computo clasico.
Interes se limita a problemas concretos con ventaja algoritmica y relacion favorable entre
coste de preparacion, ejecucion, correccion de errores y lectura. VQE es relevante como
linea exploratoria de quimica cuantica, pero no sustituye calculo clasico exacto en
Hamiltonianos pequenos.

4. ARQUITECTURA DE REFERENCIA

4.1 Principio de heterogeneidad

Arquitectura propuesta reserva control secuencial, sistema operativo, seguridad y tareas
de precision para dominios binarios convencionales. Bloques no binarios se introducen
solo donde demuestren mejora neta de energia, latencia o ancho de banda.

Componentes principales:

* CPU y control binario: Gestion de SO, seguridad, logica secuencial y alta precision.

*  Planificador y compilador con IA: Asignacion dinamica de tareas y calibracion
adaptativa.

*  Acelerador CIM memristivo multinivel: Operaciones vector-matriz de baja precision
con alta reutilizacion de datos.

*  Memoria no volatil multinivel: Almacenamiento denso con multiplos estados de
resistencia.

*  Interconexion fotonica selectiva: Enlaces de alto ancho de banda entre chiplets o
dominios especificos.

4.2 Bloques funcionales

Bloque Funcion primaria Riesgo dominante

CPU binaria Control, software, precision Energia de movimiento de datos

Memoria multinivel Mayor densidad local Retencion, dispersion y errores

CIM memristivo Operaciones vector-matriz ADC/DAC, no linealidad

Fotonica integrada Comunicacion alto ancho de banda Coste electrooptico, perdidas

IA de control Asignacion, calibracion Validacion, explicabilidad

4.3 Flujo de datos

Optimizacion principal es evitar desplazamientos innecesarios de matrices y activaciones.
Operaciones densas compatibles con precision reducida se envian al acelerador CIM;
operaciones de control, ramificacion, criptografia, precision elevada y gestion de memoria
permanecen en dominio binario. Fotonica se justifica solo cuando energia de
comunicacion electrica, congestion o distancia exceden umbral cuantificado.

5. MODELOS Y METRICAS

5.1 Energia dinamica

Aproximacion inicial: E_dyn = alpha * C_eff * V_DD^2, donde alpha es factor de actividad
y C_eff capacidad efectiva conmutada. Reduccion de tension puede disminuir fuertemente
energia dinamica, pero queda limitada por ruido, velocidad, variabilidad y fugas.

5.2 Modelo termico de primer orden

Comportamiento termico: C_th * dT/dt = P_dis - (T - T_amb)/R_th, donde C_th es
capacidad termica, R_th resistencia termica, P_dis potencia disipada y T_amb
temperatura ambiente. Para potencia constante: T_inf = T_amb + P_dis * R_th. Modelo
debera extenderse a mallas termicas distribuidas, puntos calientes, encapsulado,
apilamiento 3D y variacion temporal de carga.

5.3 Metricas de evaluacion

Metrica Definicion operativa

Energia por tarea Energia total incluyendo memoria, conversion y comunicacion.

Rendimiento por vatio Operaciones utiles por segundo / potencia total.

Latencia extremo a extremo Tiempo desde entrada hasta salida verificable.

Precision o calidad Error numerico, exactitud inferencia, SNR o BER.

Densidad de potencia Potencia por area y distribucion puntos calientes.

Fiabilidad Retencion, endurance, tasa de fallos, deriva.

Coste integracion Area, rendimiento fabricacion, encapsulado, test.

6. METODOLOGIA REPRODUCIBLE

6.1 Jerarquia de simulacion

* Materiales y dispositivos: DFT, modelos atomicos, medidas I-V, modelos compactos.

* Circuito: SPICE, Monte Carlo proceso-voltaje-temperatura, extraccion de parasitos.

* Arquitectura: simulacion memoria, red en chip, ancho de banda, ADC/DAC.

* Sistema: cargas reales, modelo energetico completo, perfiles software.

* Termomecanica y fiabilidad: modelos distribuidos, envejecimiento, sensibilidad.

6.2 Descubrimiento de materiales

Seleccion de materiales comenzara con metodos clasicos establecidos. Para cada
candidato se calcularan o mediran banda prohibida, alineamiento de bandas, movilidad
efectiva, contactos, estabilidad, defectos y fabricabilidad. Algoritmos variacionales
cuanticos se mantendran como linea exploratoria.

6.3 Diseno de circuitos

Algoritmos evolutivos exploran topologias, tamanos y niveles de cuantizacion. Funcion
objetivo: L = w_E*E + w_D*D + w_A*A + w_BER*BER + w_T*Delta_T + w_V*V_var +
w_C*C_cal, donde E es energia, D retardo, A area, BER tasa de error, Delta_T incremento
termico, V_var penalizacion por variabilidad y C_cal coste de calibracion.

6.4 Modelado computo en memoria

* Distribucion de conductancias y estados multinivel.

* No linealidad de programacion y lectura.

* Resistencia de lineas y caida de tension en arrays.

* Ruido de lectura, deriva y retencion.

* Coste energetico y latencia de ADC, DAC y amplificadores.

* Cuantizacion de pesos, activaciones y acumulaciones.

* Correccion digital posterior y recalibracion.

6.5 Modelado fotonico

Cada enlace fotonico se evaluara mediante: E_link = E_laser + E_mod + E_driver +
E_detector + E_TIA + E_control, incluyendo perdidas de acoplamiento, control de longitud
de onda, estabilizacion termica y tasa de error. Solo se seleccionaran enlaces con
beneficio neto positivo respecto a alternativa electrica.

6.6 PINNs y modelos sustitutos

Redes neuronales informadas por fisica pueden acelerar exploracion de parametros si
respetan ecuaciones de conservacion y validacion frente a simuladores de referencia. No
deben reemplazar mediciones fisicas ni emplearse como unica fuente de evidencia.

7. ESCENARIOS PROSPECTIVOS

7.1 Definicion

Valores de esta seccion son objetivos de diseno y no resultados demostrados. Carga de
trabajo de referencia es inferencia de redes neuronales de precision reducida y
operaciones vector-matriz con alta reutilizacion local de pesos.

7.2 Objetivos de sistema

Metrica Linea base CMOS Objetivo hibrido

Energia por tarea 1.0 (normalizada) <= 0.4

Rendimiento por vatio 1.0 (normalizado) >= 2.0

Latencia extremo a extremo 1.0 (normalizada) <= 1.2

Precision de aplicacion Referencia Diferencia <= 1%

Incremento de temperatura Referencia Reduccion >= 20%

Disponibilidad funcional Referencia >= 99.9%

Objetivos no incluyen superioridad universal. CMOS puede conservar ventajas en
densidad, fiabilidad, coste, compatibilidad y programabilidad.

7.3 Ejemplo termico ilustrativo

Si dos bloques tienen misma resistencia termica efectiva R_th, disminucion de potencia de
P_1 a P_2 reduce idealmente temperatura estacionaria en: Delta_T_reducida = (P_1 -
P_2) * R_th. Resultado no permite asignar temperaturas absolutas sin conocer
encapsulado, area, distribucion de potencia, ventilacion y condiciones ambientales.

8. RIESGOS Y MITIGACION

Riesgo Consecuencia Mitigacion

Variabilidad memristiva Errores, recalibracion Caracterizacion estadistica, ECC, codificacion diferencial

ADC/DAC dominante Pierde ventaja CIM Co-diseno precision, conversion compartida

Deriva y retencion Degradacion datos Monitorizacion, recalibracion, refresco selectivo

Fotonica no rentable Energia excesiva Usar solo sobre umbrales validados

Puntos calientes Menor fiabilidad Modelado termico distribuido, floorplanning

Complejidad software Baja adopcion Compilador con particion automatica

Falta manufacturabilidad Coste, bajo rendimiento Seleccion temprana procesos CMOS

9. VERIFICACION Y FALSABILIDAD

9.1 Criterios de comparacion

* Nodo CMOS, biblioteca, tension, frecuencia y memoria de linea base.

* Aplicacion, conjunto de datos, tamano de lote y precision.

* Definicion exacta de operacion y frontera de medicion energetica.

* Area, potencia estatica, dinamica, temperatura y rendimiento.

* Numero de muestras, dispersion, intervalos de confianza.

* Versiones de codigo, modelos, configuracion y semillas.

9.2 Verificacion formal

Verificacion formal se aplicara a propiedades finitas de control, protocolos, gestion de
errores y seguridad mediante SAT/SMT, model checking y pruebas exhaustivas acotadas.
Algoritmo de Grover puede considerarse solo en estudio teorico sobre espacios finitos con
oraculos definidos; no como evidencia de ausencia de contraejemplos fisicos.

9.3 Criterios de abandono

* Energia total no mejora al menos 20% frente a linea base.

* Precision se degrada mas del umbral definido.

* Tasa de error o deriva anulan mejora energetica.

* Ganancia optica no compensa transceptores y control.

* Complejidad de software impide reproducibilidad practica.

10. PLAN DE INVESTIGACION Y DESARROLLO

Fase I: modelado y seleccion (12-24 meses)

* Construir repositorio reproducible de modelos y benchmarks.

* Seleccionar materiales, dispositivos y configuraciones de memoria.

* Definir lineas base CMOS y cargas representativas.

* Implementar modelos de energia, rendimiento, ruido y termica.

Entregable: informe reproducible con modelos versionados, parametros, hipotesis y
criterios de seleccion.

Fase II: dispositivos elementales (18-36 meses)

* Fabricar o acceder a dispositivos memristivos y transistores.

* Medir curvas I-V, estados multinivel, retencion, endurance.

* Extraer modelos compactos para SPICE y arrays.

* Validar estabilidad termica y compatibilidad de proceso.

Entregable: datos experimentales, modelos validados y evaluacion de madurez
tecnologica.

Fase III: circuitos y acelerador CIM (18-30 meses)

* Disenar circuitos de lectura, programacion, calibracion.

* Evaluar arrays pequenos y medianos con modelos no ideales.

* Implementar flujo compilador-hardware para vector-matriz.

* Medir energia total, precision, latencia y degradacion.

Entregable: prototipo funcional de acelerador y comparacion con linea base.

Fase IV: integracion fotonica y chiplets (24-36 meses)

* Evaluar enlaces electricos y opticos equivalentes.

* Disenar interfaces electroopticas y protocolos.

* Integrar sensores termicos y control adaptativo.

* Cuantificar coste energetico por bit y BER.

Entregable: demostrador de interconexion heterogenea con balance energetico.

Fase V: sistema integrado (24-36 meses)

* Integrar CPU, memoria, CIM y enlaces selectivos.

* Ejecutar benchmarks de inferencia y algebra lineal.

* Validar fiabilidad, termica, software y seguridad.

* Publicar datos, codigo y protocolos de evaluacion.

Entregable: prototipo de sistema, informe comparativo y decision de escalado.

11. GOBERNANZA Y REPRODUCIBILIDAD

11.1 Repositorio cientifico

* Codigo fuente y entornos reproducibles.

* Parametros de simulacion y configuracion.

* Datos experimentales con metadatos.

* Modelos compactos, netlists y scripts.

* Registro de cambios, incidencias y limitaciones.

11.2 Separacion de evidencia

Todo resultado se etiquetara como: limite fisico establecido (teoria/literatura), resultado
simulado (reproducible con codigo),  resultado experimental (instrumentacion
documentada) o proyeccion (estimacion no validada).

11.3 Uso responsable de IA

Inteligencia artificial puede apoyar busqueda bibliografica, generacion de hipotesis,
optimizacion y automatizacion documental. No sustituye revision por especialistas,
validacion experimental ni trazabilidad de resultados.

12. CONCLUSIONES

No existe fundamento fisico para afirmar que logica multivaluada sea universalmente
superior a binaria. Limite de Landauer por bit equivalente se mantiene y niveles
adicionales introducen costes de margen de ruido, conversion, calibracion y tolerancia a
variabilidad.

Direccion tecnicamente mas defendible es plataforma heterogenea: control binario para
proposito general, memoria multinivel donde aporte densidad, computo en memoria para
operaciones vector-matriz compatibles y fotonica solo donde balance de comunicacion
sea favorable.

Viabilidad dependera de demostrar mejora extremo a extremo en energia por tarea,
rendimiento por vatio y densidad de potencia sin deterioro inaceptable de precision,
fiabilidad, coste o programabilidad.

AUTORES Y CONTRIBUCIONES

Lazaro Lopez Paz - concepcion del proyecto, definicion de objetivos, direccion de
investigacion y revision final.

Apoyo tecnico documental mediante IA - estructuracion, revision de consistencia,
formulacion de modelos y organizacion documental.

Aviso: este documento es propuesta conceptual de investigacion. No constituye
evidencia de fabricacion, rendimiento experimental, disponibilidad comercial ni
superioridad demostrada sobre sistemas CMOS existentes.
