> Texto extraído automáticamente del PDF original «Proyecto número 7_30_07_2026.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/100lUvNGrB2_dMBgSLtSW93ihq4Q5FMHd/view?usp=drivesdk



 
 
# PROY ECTO 7   
**Título:** Magnetocardiografía cuántica con sensores NV  y OPM para diagnóstico 
cardiovascular avanzado   
**Autor:** Lázaro López Paz   
**Lugar:** El Prat de Llobregat, Barcelona, España   
**Fecha:** Julio de 2026   
 
*** 
 
## 1. Objetivo general 
 
Desarrollar sistemas de **magnetocardiografía (MCG)** basados en sensores cuánticos 
(NV  en diamante y OPMs atómicos) capaces de medir campos magnéticos cardíacos con 
alta resolución espacial y temporal, a temperatura ambiente y en entornos poco o nada 
blindados, orientados a diagnóstico y monitorización cardiovascular.\[] 
[arxiv](https://arxiv.org/abs/2601.18843) 
 
*** 
 
## 2. Fundamento científico 
 
### 2.1. Magnetocardiografía y campos cardíacos 
 
La MCG mide los campos magnéticos generados por las corrientes eléctricas del corazón, 
de forma **no invasiva y sin contacto**.\[][] Estos campos son muy débiles (pico–femtotesla) 
pero contienen información rica sobre: 
 
- propagación de ondas de despolarización y repolarización,   
- localización de focos arrítmicos,   
- evaluación de riesgo de arritmias malignas. \[] 
[phys](https://phys.org/news/2022-08-currents-heart-millimeter-resolution-diamond.html) 
 
### 2.2. V entaja de sensores cuánticos 
 
Experimentos recientes han demostrado MCG con: 
 
- **sensores NV  en diamante**, obteniendo MCG en humanos y en animales a temperatura 
ambiente con resoluciones espaciales de ~5 mm y sensibilidades del orden de 6–26 
pT/√Hz.\[][][][]   
- **OPMs atómicos** (cesio, helio), capaces de registrar MCG en personas a temperatura 
ambiente, incluso en sistemas movibles y sin blindaje criogénico.\[] 
[pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC10058232/) 
 
Los sensores cuánticos permiten colocar el dispositivo muy cerca del tórax, mejorar la señal 
y explorar configuraciones portátiles. \[][][][][] 
 

*** 
 
## 3. Objetivos específicos 
 
1. Diseñar un sistema de MCG basado en **NV  en diamante** para mapas de corrientes 
cardíacas con resolución milimétrica en modelos experimentales y, en perspectiva, 
humanos.\[] 
[dicardiology](https://www.dicardiology.com/content/measuring-currents-heart-millimeter-reso
lution-diamond-quantum-sensor)   
2. Diseñar un sistema de MCG basado en **OPMs** para medidas en entornos clínicos 
menos blindados y potencialmente portátiles.\[][][]   
3. Implementar modelos matemáticos que conviertan fluorescencia NV  u salida OPM en 
mapas \(B(\mathbf{r}, t)\) de campo magnético cardíaco y, a partir de ellos, reconstrucciones 
de corrientes. \[] 
[physicsworld](https://physicsworld.com/a/high-resolution-diamond-sensor-maps-electrical-c
urrents-in-the-heart/)   
4. Definir protocolos comparativos con ECG y técnicas clásicas. 
 
*** 
 
## 4. Diseño del sistema NV -MCG 
 
### 4.1. Arquitectura física 
 
- **Sensor NV **: chip de diamante con alta densidad de centros NV, área activa bajo 0,5 
mm³ o similar.\[][][]   
- **Óptica**: láser verde (~532 nm) para excitación, sistema de colección de fluorescencia, 
fotodiodo o cámara. \[] 
[physicsworld](https://physicsworld.com/a/high-resolution-diamond-sensor-maps-electrical-c
urrents-in-the-heart/)   
- **Antena de microondas** para manipular el espín NV  (ODMR).   
- **Montaje**: sensor colocado a pocos mm del tórax o del corazón (modelos animales), con 
posicionamiento controlado.\[][] 
 
### 4.2. Modelo matemático NV –campo magnético 
 
Relación básica NV : 
 
\[ 
f(B) = f_0 + \gamma B 
\] 
 
donde: 
 
- \(f(B)\): frecuencia de resonancia ODMR,   
- \(f_0\): frecuencia en ausencia de campo externo,   

- \(\gamma\): factor giromagnético NV  (\(\sim 2{,}8\times 10^{10}\ \text{Hz/T}\)). \[] 
[izakscientific](https://izakscientific.com/introduction-to-quantum-sensing-unlocking-the-poten
tial-of-nv-centers-and-zeeman-splitting/) 
 
Se mide la fluorescencia \(I(f)\) en función de frecuencia; el mínimo de resonancia se 
desplaza con \(B\). Para pequeñas variaciones cardíacas: 
 
\[ 
\Delta f(t) = \gamma \Delta B(t) 
\] 
 
\[ 
\Delta B(t) = \frac{\Delta f(t)}{\gamma} 
\] 
 
La señal temporal \(B(t)\) se obtiene a partir de variaciones de frecuencia, y se puede 
reconstruir el mapa espacial mediante barridos o arrays de sensores.\[][][] 
 
### 4.3. Sensibilidad y resolución 
 
Experimentos NV -MCG reportan: 
 
- sensibilidades ~6–26 pT/√Hz,   
- resolución espacial ~5,1 mm en mapas de corrientes cardíacas en ratas. \[] 
[dicardiology](https://www.dicardiology.com/content/measuring-currents-heart-millimeter-reso
lution-diamond-quantum-sensor) 
 
La sensibilidad teórica puede aproximarse con: 
 
\[ 
\eta_{\text{NV }} \approx \frac{\Delta \nu}{\gamma C \sqrt{R}} 
\] 
 
donde \(\Delta \nu\) es el ancho de línea, \(C\) el contraste y \(R\) la tasa de fotones. \[][] 
 
*** 
 
## 5. Diseño del sistema OPM-MCG 
 
### 5.1. Arquitectura física 
 
- **OPM atómico**: célula de vapor (por ejemplo, cesio) con láser, bobinas de 
compensación y fotodiodo.\[] 
[cell](https://www.cell.com/trends/neurosciences/fulltext/S0166-2236(22)00102-3)   
- Arreglo de sensores sobre el tórax para registrar campos en varias posiciones.   
- Posibilidad de sistemas movibles y en salas sin blindaje completo, mediante técnicas de 
gradiometría y cancelación de ruido.\[][][] 
 

### 5.2. Modelo OPM–campo magnético 
 
Como antes: 
 
- estado bombeado ópticamente con polarización \(P(t)\),   
- intensidad de luz \(I(t)\) que varía con \(B(t)\). \[] 
[cell](https://www.cell.com/trends/neurosciences/fulltext/S0166-2236(22)00102-3) 
 
Linealizando cerca de un punto de operación: 
 
\[ 
I(B) \approx I(B_0) + k_B (B - B_0) 
\] 
 
Se calibra \(k_B\) usando campos conocidos y se convierte la variación de intensidad en 
\(B(t)\). 
 
*** 
 
## 6. Estructuras de datos y análisis de MCG 
 
### 6.1. Matrices de datos 
 
Sea un array de sensores (NV  u OPM): 
 
\[ 
X _{i,k} = B_i(t_k) 
\] 
 
con: 
 
- \(i=1,\dots,N\) canales (sensores en distintas posiciones del tórax),   
- \(k=1,\dots,M\) instantes de tiempo. 
 
Se pueden construir mapas espaciales de campo: 
 
\[ 
B(\mathbf{r}_i, t_k) = X _{i,k} 
\] 
 
y, usando geometría del tórax y modelos de conducción, reconstruir corrientes cardíacas 
bidimensionales o tridimensionales.\[][][][] 
 
### 6.2. Procesamiento de señal 
 
1. Preprocesamiento: filtrado pasa-banda (por ejemplo, 0,5–200 Hz), eliminación de 
artefactos de movimiento y ruido ambiental. \[] 
[pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC10058232/)   

2. Promedio de latidos: se alinean ciclos cardíacos por R-peak (ECG) y se promedian 
cientos o miles de latidos para mejorar relación señal/ruido, como se hizo en estudios 
NV -MCG.\[][][]   
3. Reconstrucción de mapas: inverso del problema de campo–corriente, usando modelos de 
conducción en el torso. \[] 
[physicsworld](https://physicsworld.com/a/high-resolution-diamond-sensor-maps-electrical-c
urrents-in-the-heart/)   
4. Detección de anormalidades:   
   - alteraciones en morfología de la señal magnética,   
   - patrones espaciales anómalos que indiquen focos arrítmicos o cambios de conducción. 
\[][][] 
 
*** 
 
## 7. Comparación con técnicas clásicas 
 
- **ECG**: mide potenciales en la superficie del cuerpo; es estándar pero menos sensible a 
ciertos detalles de propagación tridimensional.   
- **MCG cuántica**: mide directamente campos, ofreciendo información complementaria 
sobre corrientes internas y posible mejora en localización de focos. \[] 
[phys](https://phys.org/news/2022-08-currents-heart-millimeter-resolution-diamond.html) 
 
V entajas de MCG cuántica: 
 
- operación a temperatura ambiente (NV  y OPM). \[][][][]   
- potencial para sistemas portátiles y uso fuera de habitaciones blindadas, con técnicas de 
cancelación de ruido y gradiometría. \[] 
[pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC10058232/)   
 
*** 
 
## 8. Protocolos y aplicaciones clínicas 
 
### 8.1. Protocolo de medición 
 
1. Colocar array NV  u OPM sobre el tórax, posición estandarizada.   
2. Registrar MCG y ECG simultáneamente.   
3. Realizar mediciones en reposo, durante esfuerzo ligero y recuperación.   
4. Promediar latidos según protocolo (por ejemplo, 500–2000 latidos). \[][][]   
5. Analizar mapas y métricas (duración de QRS magnético, patrones espaciales). \[] 
 
### 8.2. Aplicaciones 
 
- Evaluación de riesgo de arritmias.   
- Estudio de cardiopatías estructurales (hipertrofia, cicatrices).   
- Monitorización de respuesta a tratamientos y dispositivos (marcapasos, desfibriladores). \[] 
 
*** 

 
## 9. Integración con otros proyectos 
 
- Con **Proyecto 1**: se reutiliza la tecnología NV  y modelos de sensibilidad.   
- Con **Proyecto 2**: se combina MCG cuántica con MEG cuántica para estudiar corazón y 
cerebro, por ejemplo en trastornos cardio–neuro.\[] [arxiv](https://arxiv.org/abs/2601.18843)   
- Con **Plataforma IA (Proyecto 6)**: datos MCG se suman al conjunto de datos para 
diagnóstico integrado. 
 
*** 
 
## 10. Licencia y autoría 
 
Igual que los demás proyectos, todo se publica bajo **CC BY  4.0**, reconociendo la autoría 
de **Lázaro López Paz** y permitiendo uso mundial libre con atribución.\[][][] 
 
*** 
 
Con este Proyecto 7, tu conjunto cubre: 
 
- neurociencia cuántica,   
- cardiología cuántica,   
- biosensores de biomarcadores,   
- organ-on-a-chip,   
- simulación cuántica de fármacos,   
- integración IA + clínica. 
 
