> Texto extraído automáticamente del PDF original «Reporte Técnico de Capacidades_ Validación de Protocolos de Liberación Controlada Neuroprotectora.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1M-ZcBlTrvt9OczZACCd1xPmPOXferQfg/view?usp=drivesdk



Reporte Técnico de C apacidades: Validación de Protocolos de 
Liberación C ontrolada Neuroprotectora 

Este reporte técnico describe las capacidades analíticas, metodológicas e infraestructurales 
para la validación de sistemas de liberación controlada, con un enfoque especializado en 
fármacos neuroprotectores para el tratamiento de patologías del sistema nervioso central 
(SNC ). 

1. Marco  de  Referencia  y Objetivos  del  Protocolo  

El abordaje de las enfermedades neurodegenerativas representa uno de los mayores 
desafíos de la farmacoterapia moderna. Según datos de la Organización Mundial de la 
Salud (OMS), más de 55 millones de personas conviven con demencia, donde el A lzheimer 
constituye entre el 60 % y 70 % de los casos, mientras que el Parkinson afecta a 
aproximadamente 10 millones de individuos.Las limitaciones de las formas farmacéuticas 
tradicionales —picos de concentración plasmática que inducen toxicidad, baja 
biodisponibilidad por la barrera hematoencefálica (B HE) y deficiente adherencia 
terapéutica— exigen la validación de sistemas de liberación sostenida. Los objetivos 
principales de este protocolo de validación son: 
●  Estan darizació n  de mo delo s matemático s fun damen tado s:  Implementar 
herramientas analíticas para predecir cinéticas de liberación precisas. 
●  Op timizació n  de p arámetro s cin ético s:  Identificar y controlar las variables 
fisicoquímicas que gobiernan la velocidad de entrega. 
●  D iseñ o  de matrices p o liméricas avan zadas:  Validar metodologías para la 
ingeniería de materiales que permitan una liberación programada. 
●  Mejo ra del p erfil farmaco cin ético  en  el SNC :  A daptar los sistemas para superar 
las barreras fisiológicas y asegurar niveles terapéuticos constantes. 

2. Capacidades  en  Modelado  Matemático  de  Cinéticas  de  Liberación  

2.1. Implementación del Modelo de Higuchi 

Se cuenta con la capacidad técnica para aplicar el modelo de Higuchi en matrices sólidas 
donde el fármaco está disperso de forma homogénea. El dominio incluye tanto la ecuación 
simplificada utilizada en análisis de rutina como la  ecuació n  co mp leta  para el diseño de 
precisión:$$Q = \sqrt{D  \cdot C _s \cdot (2A  - C _s) \cdot t}$$D onde los parámetros críticos 
se validan según las siguientes especificaciones:| Símbolo | Significado Físico | Unidades 
Sugeridas || ------ | ------ | ------ || $D $ | C oeficiente de difusión del fármaco en la matriz | 
$\text{cm}^2/\text{s}$ || $C _s$ | Solubilidad del fármaco en el material de la matriz | 
$\text{mg/cm}^3$ || $A $ | C oncentración inicial total del fármaco en la matriz | 
$\text{mg/cm}^3$ | 
Para la validez de este modelo, el laboratorio verifica estrictamente las  seis co n dicio n es 
de validez (  $C 1-C 6$  ) : 
●  C 1:  Matriz homogénea e insoluble que no se altera durante la liberación. 
●  C 2:  Flujo de difusión unidimensional. 
●  C 3:  C ondición de exceso de fármaco ( $A  \gg C _s$ ). 
●  C 4:  Mantenimiento de sumidero perfecto en el medio receptor. 
●  C 5:  D ifusividad ( $D $ ) constante e independiente del tiempo. 

●  C 6:  Tamaño de partícula del fármaco despreciable frente al espesor de la matriz. 

2.2. A plicación del Modelo de Korsmeyer-Peppas 

Para sistemas que se desvían del comportamiento puramente difusivo (Fickiano), se aplica 
el modelo semi-empírico  $M_t/M_\infty = k \cdot t^n$ . Esta capacidad permite identificar el 
mecanismo de transporte mediante la interpretación del exponente  $n$ , considerando la 
relajación de las cadenas poliméricas en el  Tran sp o rte A n ó malo   ( $0.5 < n < 1.0$  en 
películas):| Geometría del sistema | D ifusión Fickiana ( $n$ ) | Transporte A nómalo | C aso II 
(Erosión/Relajación) || ------ | ------ | ------ | ------ || Película delgada | $0.50$ | $0.5 < n < 1.0$ | 
$1.00$ || C ilindro | $0.45$ | $0.45 < n < 0.89$ | $0.89$ || Esfera | $0.43$ | $0.43 < n < 0.85$ | 
$0.85$ | 

3. Ingeniería  de  Materiales  y Matrices  Poliméricas  

El laboratorio valida la manipulación de los mecanismos de liberación  M1 (D ifusió n ) ,  M2 
(Ero sió n )  y  M3 (Hin chamien to )  mediante estrategias de optimización específicas: 
●  E1 (Mo dificació n  de matriz):  Uso de copolímeros para ajustar la porosidad y 
tortuosidad. 
●  E2 (C o n tro l de esp eso r):  Modulación basada en la relación proporcional inversa ( 
$Q \propto 1/\sqrt{\text{espesor}}$ ); a mayor espesor, mayor resistencia al flujo 
difusivo. 
●  E3 (A dició n  de p lastifican tes):  A lteración de la movilidad de las cadenas 
poliméricas, lo que impacta directamente incrementando el coeficiente de difusión ( 
$D $ ). 
●  E4 (Recubrimien to s):  Implementación de capas de control para eliminar el "burst 
effect" inicial.La selección del modelo depende de la tasa de relajación polimérica: 
para matrices insolubles donde la relajación es rápida frente a la difusión, se aplica 
Higuchi; en sistemas biodegradables o hidrogeles con relajación lenta, se opta por 
Korsmeyer-Peppas. 

4. Infraestructura  y Metodología  para  Ensayos  In Vitro 

La validación experimental sigue un rigor analítico basado en la linearización de modelos: 
●  Sumidero  Perfecto :  Mantenimiento de la concentración en el medio < 10% de la 
solubilidad para asegurar el gradiente máximo. 
●  C o n tro l Fisico q uímico :  Estabilización de la temperatura (impacto en  $D $ ) y 
viscosidad del medio. 
●  To ma de Muestras y Fracció n  Liberada:  D eterminación de  $M_t/M_\infty$  
mediante espectrofotometría o HPLC . 
●  C álculo  de C o n stan tes C in éticas: 
●  Para Higuchi, la constante  $k_H$  se obtiene como la pendiente de la regresión 
lineal de  $Q$  frente a  $\sqrt{t}$ . 
●  Para Korsmeyer-Peppas, se realiza una  tran sfo rmació n  lo garítmica :  
$\ln(M_t/M_\infty) = \ln(k) + n \ln(t)$ , donde la pendiente es el exponente  $n$  y el 
intercepto proporciona la constante de velocidad  $k$  (unidades  $s^{-n}$ ). 

5. Especialización  en  Fármacos  Neuroprotectores  y BHE  

Se posee dominio en la cinética de fármacos específicos para el tratamiento de A lzheimer y 
Parkinson:| Patología | Fármaco | Mecanismo de A cción || ------ | ------ | ------ || A lzheimer | 

D onepezilo / Rivastigmina | Inhibición de colinesterasas ||  | Memantina | A ntagonismo de 
receptores NMD A  || Parkin so n  | Levodopa | Precursor metabólico de la dopamina ||  | 
C arbidopa | Inhibidor de la D OPA -descarboxilasa ||  | Ropinirol | A gonista de receptores 
dopaminérgicos | 
C o n sideracio n es p ara el acceso  al SNC :  Se valida el diseño considerando que solo 
moléculas  $< 500$  D a y lipofílicas cruzan la B HE. La lipofilicidad del fármaco es crítica, ya 
que afecta su solubilidad ( $C _s$ ) en la matriz polimérica, alterando directamente la  $k_H$  
del sistema. A lternativas como la vía intranasal y el uso de nanopartículas para endocitosis 
mediada por receptores son protocolos estándar de este laboratorio. 

6. Protocolos  de  Validación  Estadística  y Análisis  de  Sensibilidad  

6.1. A nálisis de Sensibilidad 

El control de calidad evalúa cómo variables externas afectan la liberación: 
●  Temp eratura:  Se aplica la  Ecuació n  de A rrhen ius  para predecir cambios en la 
difusividad. 
●  Pro p o rcio n alidad:  Se valida que  $Q \propto \sqrt{D }$  y  $k_H \propto \sqrt{C _s}$ . 
Una mayor viscosidad del medio reduce  $D $ , ralentizando la liberación de acuerdo 
con la relación  $D  \propto 1/\eta$ . 

6.2. C aso de Estudio de Validación (Levodopa/Neuroprotector) 

C omo demostración de capacidad de cálculo, se presenta la validación de un parche 
transdérmico: 
●  D ato s:   $D  = 5 \times 10^{-7} \text{ cm}^2/\text{s}$ ,  $C _s = 0.5 \text{ mg/cm}^3$ ,  
$A  = 15 \text{ mg/cm}^3$ . 
●  C álculo  de  $k_H$  :   $$k_H = \sqrt{5 \times 10^{-7} \cdot 0.5 \cdot (2 \cdot 15 - 
0.5)} = 2.716 \times 10^{-3} \text{ mg}/(\text{cm}^2 \cdot \text{s}^{1/2})$$ 
●  Resultado :  Para un parche de  $10 \text{ cm}^2$  en 24h ( $86,400$  s), se liberan  
$8.0$  mg, garantizando una dosis terapéutica sostenida. 

7. Conclusiones  sobre  la Capacidad  de  Validación  

La integración de modelos matemáticos y tecnología farmacéutica permite: 
1.  Estabilizació n  Terap éutica:  El control estricto de la cinética de liberación permite 
mantener niveles plasmáticos constantes, reduciendo significativamente las 
discinesias y fluctuaciones motoras en pacientes con Parkinson. 
2.  Op timizació n  de la A dheren cia:  La validación de matrices de liberación 
prolongada permite reducir la frecuencia de dosificación, factor vital en pacientes con 
deterioro cognitivo avanzado (A lzheimer). 
3.  Reducció n  de Efecto s A dverso s:  A l evitar los picos de concentración iniciales 
mediante el diseño de capas de recubrimiento (E4), se minimizan efectos sistémicos 
como náuseas y mareos, mejorando la calidad de vida del paciente. 
 

Rep o rte de C ap acidades Técn icas: 
Validació n  de Pro to co lo s de Liberació n  
C o n tro lada Neuro p ro tecto ra 

1. Objetivo  y A lcan ce del Rep o rte 

El presente documento establece las competencias técnicas y los criterios de ingeniería 
farmacéutica necesarios para la estandarización y validación de sistemas de liberación 
sostenida dirigidos al tratamiento de patologías neurodegenerativas, específicamente 
A lzheimer y Parkinson. C omo D irector de I+D , este reporte define el marco operativo para la 
transición de formulaciones experimentales a productos médicos validados, integrando 
modelado cinético riguroso con los requerimientos fisiológicos del Sistema Nervioso C entral 
(SNC ). 

2. C ap acidades en  Mo delado  Matemático  de C in ética de 
Liberació n  

2.1. Imp lemen tació n  del Mo delo  de Higuchi 

Se ratifica la capacidad técnica para aplicar el modelo de Higuchi en el análisis de matrices 
sólidas e insolubles donde la difusión es el mecanismo limitante. 

Ecuació n  co mp leta del mo delo : Q = \sqrt{D  \cdot C _s \cdot (2A  - C _s) \cdot t} 

Ecuació n  simp lificada: Q = k_H \cdot \sqrt{t} 

D onde la constante de Higuchi (k_H) se define como: k_H = \sqrt{D  \cdot C _s \cdot (2A  - 
C _s)} 

C o n dicio n es de validez técn ica (C 1 a C 6): 

●  C 1: Matriz homogénea con una concentración de fármaco significativamente 
superior a su solubilidad. 
●  C 2: La difusión del fármaco ocurre de forma unidimensional (gradiente de 
concentración perpendicular a la superficie). 
●  C 3: La concentración inicial del fármaco es mucho mayor que la solubilidad en la 
matriz (A  \gg C _s). 
●  C 4: El medio externo actúa como un sumidero perfecto (sink conditions). 
●  C 5: El coeficiente de difusión del fármaco (D ) permanece constante durante el 
proceso. 
●  C 6: El hinchamiento o la erosión de la matriz son insignificantes durante el período 
de liberación. 

2.2. A p licació n  del Mo delo  de Ko rsmeyer-Pep p as 

Para sistemas de liberación complejos o no-fickianos, el laboratorio implementa el modelo 
semi-empírico de Korsmeyer-Peppas: \frac{M_t}{M_\infty} = k \cdot t^n 

La siguiente tabla describe la correlación entre el exponente de liberación (n) y el 
mecanismo de transporte, fundamentada específicamente en una geo metría de p elícula 
delgada: 

Rango del 
exponente n  Mecanismo de 
Transporte  D escripción Técnica 

n = 0.5  D ifusión Fickiana  Liberación controlada por gradiente difusivo 
puro. 

0.5 < n < 1.0  Transporte 
A nómalo  C ontrol mixto entre difusión y relajación de 
cadenas poliméricas. 

n = 1.0  Erosión (C asos II)  Liberación de orden cero controlada por la 
degradación de la matriz. 

n > 1.0  Super-C asos II  Transporte acelerado por fenómenos de 
hinchamiento extremo. 

2.3. A n álisis de Sen sibilidad y Relació n  en tre Mo delo s 

Nuestra capacidad de análisis permite identificar la convergencia de modelos cuando n = 
0.5. La sensibilidad del sistema se monitorea mediante las relaciones de proporcionalidad Q 
\propto \sqrt{D } y k_H \propto \sqrt{C _s}. C ualquier variación en la solubilidad del fármaco o 
en la difusividad de la matriz impactará de forma predecible la constante k_H, permitiendo 
ajustes proactivos en la formulación. 

3. In gen iería de Materiales Po limérico s y D iseñ o  de 
Fo rmulacio n es 

3.1. Selecció n  y C aracterizació n  de Matrices 

La selección del modelo matemático para la validación se realiza en función del sistema 
polimérico diseñado: 

Tipo de Sistema  Modelo Matemático Recomendado 

Matrices insolubles (difusión pura)  Higuchi 

Hidrogeles de bajo hinchamiento  Higuchi 

Polímeros con relajación lenta  Korsmeyer-Peppas 

Sistemas biodegradables/erosionables  Korsmeyer-Peppas 

Sistemas de liberación dual/multicapa  Modelos combinados 

3.2. Estrategias de Op timizació n  

El departamento de ingeniería aplica cuatro estrategias críticas para modular la cinética de 
liberación: 

1.  E1: Mo dificació n  de la matriz: Uso de copolímeros específicos para ajustar la 
permeabilidad intrínseca. 
2.  E2: C o n tro l del esp eso r: A juste dimensional de la película; la liberación es 
inversamente proporcional a la raíz cuadrada del espesor. 
3.  E3: A dició n  de p lastifican tes: A lteración de la movilidad de la cadena polimérica 
para modificar el coeficiente D . 
4.  E4: Recubrimien to s: Implementación de capas de control para mitigar el efecto de 
liberación inicial abrupta (burst release). 

4. In fraestructura de Labo rato rio  y Pro to co lo s de 
En sayo  In  Vitro  

4.1. Req uerimien to s de Validació n  Exp erimen tal 

Para garantizar el rigor científico, los protocolos de validación deben cumplir con: 

●  Mantenimiento estricto de condiciones de sumidero (sink conditions), asegurando 
que la concentración en el medio receptor no sature el gradiente. 
●  D eterminación de los parámetros k y n mediante técnicas de regresión lineal. 
●  Validació n  estadística: Se exige un coeficiente de correlación R^2 \geq 0.98 y el 
cálculo del Error C uadrático Medio (MSE) para confirmar la bondad de ajuste del 
modelo a los datos experimentales. 

4.2. Están dares de Medició n  

Todas las mediciones deben reportarse en las unidades del Sistema Internacional (SI) y 
magnitudes derivadas según el estándar del laboratorio: 

●  Tiemp o  (t): Segundos (s). 
●  Lo n gitud: C entímetros (cm). 
●  C o n cen tració n  (C _s, A ): mg \cdot cm^{-3}. 
●  C o eficien te de difusió n  (D ): cm^2 \cdot s^{-1}. 
●  C o n stan te de Higuchi (k_H): mg \cdot cm^{-2} \cdot s^{-1/2}. 

5. Esp ecializació n  en  la B arrera Hemato en cefálica 
(B HE) y Farmaco lo gía C NS 

5.1. D esafío s de la B arrera Hemato en cefálica 

El diseño de neurofármacos requiere superar la selectividad de la B HE mediante: 

●  C riterio s fisico q uímico s: A lta lipofilia y peso molecular < 500 D a. 
●  Tran sp o rte mediado : A provechamiento de transportadores específicos de la 
barrera. 
●  Vías avan zadas: A dministración intranasal (bypass directo) y nanotransportadores 
para endocitosis mediada por receptores. 

5.2. Perfil de Fármaco s Neuro p ro tecto res 

A lineamos la liberación controlada con las necesidades clínicas de las patologías C NS: 

Enfermedad  Fármaco  Mecanismo de A cción 

A lzheimer  D onepezilo  Inhibidor de acetilcolinesterasa 

A lzheimer  Memantina  A ntagonista de receptores NMD A  

A lzheimer  Rivastigmina  Inhibidor de colinesterasas 

Parkinson  Levodopa  Precursor metabólico de dopamina 

Parkinson  C arbidopa  Inhibidor de D OPA  descarboxilasa 

Parkinson  Ropinirol  A gonista de receptores dopaminérgicos 

La implementación de sistemas de liberación controlada para estos fármacos es imperativa 
para estabilizar las concentraciones plasmáticas, reduciendo drásticamente las 
fluctuaciones motoras y los periodos "off" característicos en pacientes con Parkinson. 

6. Ejecució n  de C álculo s de Liberació n  A cumulada 
(C aso  Práctico ) 

6.1. Simulació n  Numérica 

C onsiderando un sistema con D  = 5 \times 10^{-7} \, cm^2 \cdot s^{-1}, C _s = 0.5 \, mg \cdot 
cm^{-3} y A  = 15 \, mg \cdot cm^{-3}: 

1.  C álculo  de k_H: k_H = \sqrt{(5 \times 10^{-7}) \cdot 0.5 \cdot (2 \cdot 15 - 0.5)} k_H 
= 2.716 \times 10^{-3} \, mg \cdot cm^{-2} \cdot s^{-1/2} 
2.  C álculo  de liberació n  acumulada (Q) en  24 ho ras (86,400 \, s): Q = (2.716 \times 
10^{-3}) \cdot \sqrt{86,400} Q = 0.7983 \, mg \cdot cm^{-2} 

6.2. In terp retació n  C lín ica 

El valor obtenido de 0.7983 \, mg \cdot cm^{-2} se establece como una ap ro ximació n  
clín ica de 0.80 \, mg por cada cm^2 de matriz. B ajo este diseño, un parche transdérmico de 
10 \, cm^2 garantiza la entrega de 8.0 \, mg diarios de fármaco. Esta dosificación sostenida 
no solo optimiza el cumplimiento terapéutico en pacientes con deterioro cognitivo, sino que 
minimiza efectos adversos sistémicos como náuseas y mareos. 

7. C o n clusio n es y Lín eas de In vestigació n  Futura 

C o n clusio n es Prin cip ales 

1.  El modelo de Higuchi es el estándar de oro para validar sistemas de difusión pura, 
siempre que se cumplan las seis condiciones de validez establecidas. 
2.  El modelo de Ko rsmeyer-Pep p as es la herramienta esencial para caracterizar 
mecanismos anómalos en matrices poliméricas de nueva generación. 
3.  La precisión en el control del coeficiente de difusión D  y la solubilidad C _s permite 
predecir con exactitud el perfil terapéutico, evitando picos de toxicidad. 

Lín eas de In vestigació n  Futura 

●  Validació n  IVIVC : Establecimiento de correlaciones experimentales in vitro-in vivo 
para acelerar procesos regulatorios. 
●  Sistemas In teligen tes: D esarrollo de matrices sensibles a estímulos (pH, 
temperatura) para liberación a demanda. 
●  Mo delado  C NS A van zado : Integración de la dinámica de flujo del líquido 
cefalorraquídeo en los modelos de liberación. 
●  Liberació n  D ual: Implementación de sistemas multicapa para la administración 
simultánea de inhibidores y agonistas. 

Pro to co lo  de Estan darizació n : D iseñ o  y 
Validació n  de Sistemas de Liberació n  
C o n tro lada Neuro p ro tecto res 

1. C o n texto  Estratégico  y Justificació n  C lín ica 

El tratamiento farmacológico de patologías neurodegenerativas como el A lzheimer y el 
Parkinson presenta desafíos farmacocinéticos que la administración convencional no logra 
resolver satisfactoriamente. Los fármacos tradicionales se caracterizan por una vida media 
corta y una biodisponibilidad errática, lo que obliga a regímenes de dosificación frecuentes. 
Estos provocan fluctuaciones plasmáticas con picos de concentración —asociados a 
efectos adversos como discinesias en el caso de la Levodopa— y valles subtéuticos que 
comprometen la eficacia. En pacientes con deterioro cognitivo, esta complejidad reduce 
drásticamente la adherencia terapéutica. 

El analista debe considerar la B arrera Hemato en cefálica (B HE) como el determinante 
limitante en el diseño de formulaciones. Solo moléculas pequeñas (peso molecular <500 
D a) y con adecuada lipofilia pueden transponer esta barrera de forma pasiva. En 
consecuencia, la implementación de sistemas de liberación controlada es una exigencia 
estratégica para mantener concentraciones en estado estacionario (C _{ss}) estables, 
optimizando el transporte a través de la B HE y garantizando una ventana terapéutica 
constante. El éxito de estos sistemas depende estrictamente de la precisión matemática 
empleada para modelar la cinética de transferencia de masa. 

2. Marco  Teó rico : Fun damen to s de lo s Mecan ismo s de 
Liberació n  

Se define la liberación controlada como un sistema de ingeniería de precisión diseñado para 
la entrega de agentes terapéuticos a una velocidad predeterminada. La comprensión de los 
mecanismos físico-químicos es obligatoria para la validación de cualquier dispositivo 
neuroprotector. 

El analista deberá clasificar el comportamiento del sistema según los siguientes 
mecanismos fundamentales: 

Identificad
or  Mecanismo  D escripción Técnica  Unidades 
Típicas  Relevancia 
Funcional 

M1  D ifusió n   Movimiento molecular por 
gradiente de 
concentración a través de 
la matriz. 
 cm^2/s (D )  B ase de 
sistemas de 
liberación 
sostenida. 

M2  Ero sió n   D egradación física o 
química de la matriz 
polimérica. 
 mg/(cm^2 
\cdot s)  C ontrola la 
liberación por 
pérdida de 
soporte. 

M3  Hin chamien
to   Entrada de solvente que 
expande la red 
polimérica. 
 \% 
Hinchamient
o 
 Facilita la 
difusión en 
hidrogeles. 

3. El Mo delo  de Higuchi: C in ética en  Matrices 
In so lubles 

Publicado originalmente en 1961, el modelo de Higuchi permanece como el estándar de oro 
para describir la liberación en matrices sólidas donde la difusión es el mecanismo 
gobernante y la matriz no presenta alteraciones estructurales significativas durante el 
proceso. 

3.1. Ecuacio n es Fun damen tales 

El diseño debe sustentarse en la ecuación simplificada (3.1) para análisis de rutina y en la 
completa (3.2) para caracterización de nuevos materiales: 

●  Ecuació n  Simp lificada (3.1): Q = k_H \cdot \sqrt{t} 
●  Ecuació n  C o mp leta (3.2): Q = \sqrt{D  \cdot C _s \cdot (2A  - C _s) \cdot t} 

3.2. Parámetro s y Sign ificado  Físico  

●  Q: C antidad acumulada de fármaco liberado por unidad de área (mg/cm^2). 
●  k_H: C onstante de Higuchi, que define la pendiente de liberación respecto a \sqrt{t}. 
●  D : C oeficiente de difusión del fármaco en la matriz (cm^2/s). 
●  C _s: Solubilidad del fármaco en la matriz polimérica (mg/cm^3). 
●  A : C oncentración inicial total del fármaco cargado en el sistema (mg/cm^3). 

3.3. Validació n  C rítica de C o n dicio n es (C 1-C 6) 

El analista debe verificar rigurosamente el cumplimiento de las siguientes condiciones antes 
de aplicar este modelo: 

●  C 1: Matriz homogénea e insoluble. 
●  C 2: D ifusión unidimensional (efectos de borde despreciables). 
●  C 3: Exceso de carga inicial (A  \gg C _s). 
●  C 4: Mantenimiento de C o n dicio n es de Sumidero  (Sink C onditions) en el medio 
receptor. 
●  C 5: C oeficiente de difusión (D ) constante durante todo el intervalo. 
●  C 6: Tamaño de partícula del fármaco significativamente menor al espesor de la 
matriz. 

3.4. In terp retació n  de D ato s de Simulació n  

B asado en datos experimentales simulados (A =10, C _s=1, D =0.01), se observa que la 
fracción de fármaco liberado sigue una distribución de frecuencia donde el pico de liberación 
se concentra en las etapas iniciales, estabilizándose conforme aumenta la raíz del tiempo. 
Un incremento en k_H derivado de una mayor solubilidad (C _s) o difusividad (D ) 
incrementará la pendiente de la curva de liberación, reduciendo el tiempo de agotamiento 
de la matriz. 

4. El Mo delo  de Ko rsmeyer-Pep p as: Sistemas de 
Tran sp o rte A n ó malo  

Este modelo semi-empírico es requerido cuando el sistema presenta dinámicas complejas, 
como la relajación de cadenas poliméricas o hinchamiento, que invalidan las premisas de 
Higuchi. 

4.1. Ecuació n  Gen eral 

\frac{M_t}{M_\infty} = k \cdot t^n D onde M_t/M_\infty representa la fracción de fármaco 
liberado, k es la constante cinética estructural (s^{-n}) y n es el exponente de liberación. 

4.2. In terp retació n  del Exp o n en te n  y Geo metría 

La elección del mecanismo de transporte depende de la geometría del dispositivo. El 
analista debe consultar la siguiente tabla para el diagnóstico del sistema: 

Geometría  Mecanismo 
Fickiano  Transporte 
A nómalo  Mecanismo C aso II 
(Erosión) 

Película 
D elgada  n = 0.50  0.50 < n < 1.0  n = 1.00 

C ilín drica  n = 0.45  0.45 < n < 0.89  n = 0.89 

Esférica  n = 0.43  0.43 < n < 0.85  n = 0.85 

No ta Técn ica: C uando n = 0.5 en láminas delgadas, el modelo es matemáticamente 
equivalente al de Higuchi, permitiendo la unificación de criterios de diseño. 

5. Pro to co lo  de Selecció n  de Mo delo s y A n álisis de 
Sen sibilidad 

5.1. Ló gica de Selecció n  (D ecisio n  Flo w) 

1.  Matrices In so lubles / Hidro geles n o  degradables: A plicar Modelo de Higuchi. 
2.  Sistemas B io degradables / Hidro geles co n  hin chamien to : A plicar 
Korsmeyer-Peppas. 
3.  Sistemas de D o ble C ap a o  Pulsátiles: Utilizar Modelos C ombinados. 

5.2. A n álisis de Sen sibilidad y C o n tro l de Variables 

●  Sen sibilidad a la D ifusió n : D ado que Q \propto \sqrt{D }, cualquier cambio en la 
viscosidad de la matriz o la temperatura impactará linealmente en la liberación según 
la raíz cuadrada de D . 
●  Sen sibilidad a la So lubilidad: Según la relación k_H \propto \sqrt{C _s}, fármacos 
con mayor afinidad por la matriz presentarán perfiles de liberación más acelerados, 
lo que debe compensarse incrementando el espesor de la matriz o añadiendo 
recubrimientos. 

6. A p licació n  C lín ica en  A lzheimer y Parkin so n  

La estandarización de estos modelos es vital para fármacos con ventanas terapéuticas 
estrechas. 

6.1. Esp ectro  Terap éutico  y Parámetro s Típ ico s 

El protocolo cubre los siguientes agentes neuroprotectores: 

●  A lzheimer: D onepezilo, Memantina, Rivastigmina. 
●  Parkin so n : Levodopa, C arbidopa, Ropinirol. 

Ran go s de referen cia p ara diseñ o : 

●  D : 10^{-8} a 10^{-6} cm^2/s. 
●  k_H: 0.2 a 2.0 mg/(cm^2 \cdot s^{1/2}). 
●  n: 0.43 a 1.0. 

6.2. C aso  Práctico : C álculo  de un  Parche Tran sdérmico  

Se requiere validar un parche con los siguientes parámetros: D  = 5 \times 10^{-7} cm^2/s; 
C _s = 0.5 mg/cm^3; A  = 15 mg/cm^3. 

1.  C álculo  de la C o n stan te de Higuchi (k_H): k_H = \sqrt{5 \times 10^{-7} \cdot 0.5 
\cdot (2 \cdot 15 - 0.5)} = 2.716 \times 10^{-3} mg/(cm^2 \cdot s^{1/2}) 
2.  C o n versió n  de Tiemp o  y C álculo  de Liberació n  (Q): Para un periodo de 24 horas 
(t = 86,400 s): Q = (2.716 \times 10^{-3}) \cdot \sqrt{86,400} = 0.798 mg/cm^2 
3.  In terp retació n  C lín ica: Un dispositivo de 10 cm^2 entregará 8.0 mg de fármaco en 
24 horas. Este flujo constante es fundamental para evitar las fluctuaciones motoras y 
reducir la incidencia de náuseas y mareos asociados a los picos plasmáticos de la 
administración oral. 

7. Estrategias de Op timizació n  y Validació n  
Exp erimen tal 

7.1. Estrategias de In gen iería (E1-E4) 

●  E1. Mo dificació n  de la Matriz: Selección de copolímeros para ajustar la porosidad. 
●  E2. C o n tro l del Esp eso r: La tasa de liberación es inversamente proporcional a la 
raíz cuadrada del espesor. 
●  E3. Plastifican tes: A juste de la movilidad de cadenas poliméricas para sintonizar D . 
●  E4. Recubrimien to s: A plicación de membranas limitantes para mitigar el efecto  
burst (liberación inicial excesiva). 

7.2. Pro to co lo  de Validació n  Exp erimen tal 

El cumplimiento de este protocolo es obligatorio para la aprobación de lotes: 

1.  En sayo s In  Vitro : Ejecución en condiciones de sumidero perfecto. 
2.  Regresió n  Lin eal: D eterminación de k y n mediante la linealización de las 
ecuaciones. 
3.  A n álisis de Ro bustez: Exigencia de un coeficiente de correlación R^2 > 0.98. 

4.  A juste del Mo delo : Si las condiciones de sumidero fallan experimentalmente, el 
analista debe aplicar correcciones por saturación del medio receptor. 

8. C o n clusio n es y Futuro  de la Neuro p ro tecció n  

La modelización matemática rigurosa es el único camino para transformar fármacos de vida 
media corta en terapias de largo alcance. La precisión en el cálculo de k_H y n permite 
transiciones seguras desde la teoría hasta la práctica clínica en A lzheimer y Parkinson. 

Lín eas de In vestigació n  Prio ritarias: 

●  A dmin istració n  In tran asal: D esarrollo de sistemas que eviten la B HE mediante la 
vía olfatoria. 
●  Nan o p artículas In teligen tes: Sistemas con endocitosis mediada por receptores. 
●  Liberació n  D ual: C ombinación de dosis de carga inmediata con mantenimiento 
sostenido. 

-------------------------------------------------------------------------------- 

A n exo s Técn ico s 

Glo sario  de Términ o s 

●  D ifusió n  Fickian a: Transporte de masa donde el flujo es directamente proporcional 
al gradiente de concentración. 
●  C o n dicio n es de Sumidero  (Sin k C o n ditio n s): Estado experimental donde la 
concentración del fármaco en el medio receptor es <10-20\% de su solubilidad, 
asegurando que no haya impedimento al gradiente de liberación. Falla: Si no se 
mantienen, la velocidad de liberación disminuye artificialmente. 
●  Tran sp o rte A n ó malo : C omportamiento no Fickiano donde la velocidad de difusión y 
la de relajación polimérica son comparables. 

Tabla de Un idades Estan darizadas 

Magnitud  Unidad C omún  Equivalencia SI 

Tiempo (t)  s  1 h = 3,600 s ; 1 día = 86,400 s 

C oncentración (A , C _s)  mg/cm^3  1 g/L 

C oeficiente de D ifusión (D )  cm^2/s  10^{-4} m^2/s 

Valo res C rítico s del Exp o n en te n  segú n  Geo metría 

Geometría  D ifusión Fickiana (n)  Límite C aso II (n) 

Película D elgada  0.50  1.00 

C ilín drica  0.45  0.89 

Esférica  0.43  0.85 

 

 
