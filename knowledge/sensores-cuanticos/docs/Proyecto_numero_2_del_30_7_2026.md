> Texto extraído automáticamente del PDF original «Proyecto número 2_del 30_7_2026.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1zyvhCcwppU3k0smeUWntup3JvdsTQdnV/view?usp=drivesdk



 
 
## A. Matemática y protocolos para OPMs (Proyecto 2) 
 
### A.1. Modelo simplificado del OPM 
 
Un OPM se puede modelar como un sistema donde el **estado de polarización del vapor** 
responde al campo magnético externo y esa respuesta se observa como cambio en la 
intensidad de luz medida por el fotodiodo.\[] 
[cell](https://www.cell.com/trends/neurosciences/fulltext/S0166-2236(22)00102-3) 
 
Definimos: 
 
- \(P(t)\): grado de polarización del vapor (entre 0 y 1).   
- \(B(t)\): campo magnético externo (neuromagnético + ruido).   
- \(I(t)\): intensidad de luz en el fotodiodo. 
 
Modelo cualitativo: 
 
1. Dinámica de polarización: 
 
\[ 
\frac{dP}{dt} = R_{\text{pump}} (1 - P) - \Gamma(B) P 
\] 
 
donde: 
 
- \(R_{\text{pump}}\): tasa de bombeo óptico por el láser,   
- \(\Gamma(B)\): tasa de despolarización dependiente del campo magnético (mayor \(B\) → 
mayor despolarización).   
 
2. Intensidad de luz: 
 
\[ 
I(t) = I_0 \bigl(1 - \alpha P(t)\bigr) 
\] 
 
donde: 
 
- \(I_0\): intensidad máxima (vapor transparente),   
- \(\alpha\): coeficiente que relaciona polarización con absorción. 
 
En régimen estacionario (\(\frac{dP}{dt}=0\)), para un campo \(B\) aproximadamente 
constante: 
 
\[ 
P_{\text{eq}}(B) = \frac{R_{\text{pump}}}{R_{\text{pump}} + \Gamma(B)} 
\] 

 
\[ 
I_{\text{eq}}(B) = I_0 \left(1 - \alpha \frac{R_{\text{pump}}}{R_{\text{pump}} + 
\Gamma(B)}\right) 
\] 
 
De forma práctica, alrededor de un punto de operación se linealiza: 
 
\[ 
I(B) \approx I(B_0) + k_B (B - B_0) 
\] 
 
donde \(k_B\) es la sensibilidad local (derivada de \(I\) respecto a \(B\) en \(B_0\)). Esa 
relación lineal es la base para convertir cambios de intensidad en cambios de campo en el 
rango neuromagnético.\[][] 
 
*** 
 
### A.2. Fórmula de sensibilidad para magnetometría 
 
La sensibilidad magnética de un sensor cuántico se puede expresar en términos de 
parámetros experimentales como contraste, ancho de línea y tasa de detección de 
fotones.\[] [qzabre](https://www.qzabre.com/how-it-works) 
 
Para NV en cw-ODMR, una forma típica es: 
 
\[ 
\eta_{\text{cw}} \approx \frac{\Delta \nu}{\gamma C \sqrt{R}} 
\] 
 
donde: 
 
- \(\Delta \nu\): ancho de línea (MHz),   
- \(\gamma\): factor de conversión frecuencia–campo (Hz/T),   
- \(C\): contraste de la señal (0–1),   
- \(R\): tasa de fotones detectados (cuentas/s).\[] 
 
Para OPMs, se usan expresiones análogas, con parámetros específicos de la célula y el 
láser:\[] 
[macqsimal](https://www.macqsimal.eu/macqsimal/optically-pumped-magnetometers/) 
 
\[ 
\eta_{\text{OPM}} \approx \frac{\delta B_{\text{min}}}{\sqrt{T}} = \frac{\sigma_B}{\sqrt{T}} 
\] 
 
donde \(\sigma_B\) es la desviación estándar de mediciones de campo en tiempo \(T\) y la 
sensibilidad se expresa en fT/√Hz.\[][][] 
 

En la práctica, para cada configuración: 
 
1. Se mide \(B(t)\) durante un intervalo con campo constante.   
2. Se calcula \(\sigma_B\).   
3. Se define: 
 
\[ 
\eta = \frac{\sigma_B}{\sqrt{T}} 
\] 
 
y, para comparar sensores o mejoras: 
 
\[ 
L_{\eta} = \log_{10}(\eta) 
\] 
 
Esta fórmula de sensibilidad la reutilizamos en todos los proyectos de magnetometría (NV, 
OPM, hBN). \[] [qzabre](https://www.qzabre.com/how-it-works) 
 
*** 
 
### A.3. Estructuras de datos y matrices para OPM-MEG 
 
Para trabajar con arrays de OPMs en MEG, se modelan las mediciones como matrices:\[][][] 
 
- \(N\): número de canales (sensores).   
- \(M\): número de muestras (instantes de tiempo o mapas de campo). 
 
Definimos: 
 
\[ 
X \in \mathbb{R}^{N \times M}, \quad X_{i,k} = B_i(t_k) 
\] 
 
donde: 
 
- \(i = 1,\dots,N\) (canal),   
- \(k = 1,\dots,M\) (instante). 
 
A partir de \(X\), se construyen: 
 
1. **Media por canal:** 
 
\[ 
\bar{X}_i = \frac{1}{M} \sum_{k=1}^M X_{i,k} 
\] 
 
2. **Covarianza entre canales \(i\) y \(j\):** 

 
\[ 
K_{ij} = \frac{1}{M} \sum_{k=1}^M \bigl(X_{i,k} - \bar{X}_i\bigr)\bigl(X_{j,k} - \bar{X}_j\bigr) 
\] 
 
3. **Correlación normalizada:** 
 
\[ 
C_{ij} = \frac{K_{ij}}{\sigma_i \sigma_j} 
\] 
 
donde \(\sigma_i\) es la desviación estándar de canal \(i\).\[] 
 
Estas matrices se usan para: 
 
- Optimizar el layout de sensores (seleccionar los canales más informativos).   
- Inferir campos en canales no medidos a partir de los medidos, mediante matrices de 
transformación.\[] 
 
*** 
 
### A.4. Modelo de velocidad de propagación y conectividad 
 
Para analizar neurodegeneración: 
 
1. Se definen regiones cerebrales \(R_a, R_b\) asociadas a grupos de canales.   
2. Se identifican eventos de disparo en \(R_a\) y se mide el retraso \(\Delta t\) hasta eventos 
correlacionados en \(R_b\).   
3. Se calcula la **velocidad efectiva**: 
 
\[ 
v_{\text{efectiva}} = \frac{d_{ab}}{\Delta t_{ab}} 
\] 
 
donde \(d_{ab}\) es la distancia (aproximada) entre regiones.\[] 
[physicsworld](https://physicsworld.com/a/quantum-sensor-could-help-detect-dementia/) 
 
Conectividad funcional: 
 
- A partir de \(X\), se calcula coherencia o correlación cruzada entre canales/regiones.   
- Se construye una matriz de conectividad \(G\), donde cada elemento resume la fuerza de 
conexión entre pares de regiones. 
 
Con IA, se usan vectores de características derivados de \(v_{\text{efectiva}}\), espectros de 
potencia y conectividad para clasificar estados (normal vs patológico).\[][] 
 
*** 
 

## B. Bloques matemáticos reutilizables para otros proyectos 
 
### B.1. NV centers y Zeeman (Proyecto 1 y más) 
 
Los NV centers se modelan con un Hamiltoniano que incluye término de Zeeman:\[] 
[qzabre](https://www.qzabre.com/how-it-works) 
 
\[ 
\hat{H} = \hat{H}_0 + \gamma B \hat{S}_z 
\] 
 
donde: 
 
- \(\hat{H}_0\): Hamiltoniano sin campo,   
- \(\gamma\): factor giromagnético del NV (\(\approx 2.8 \times 10^{10}\ \text{Hz/T}\)),   
- \(B\): campo externo,   
- \(\hat{S}_z\): operador de espín. 
 
La frecuencia de transición depende de \(B\): 
 
\[ 
f(B) \approx f_0 + \gamma B 
\] 
 
y el campo se obtiene de la desviación de frecuencia: 
 
\[ 
B = \frac{f(B) - f_0}{\gamma} 
\] 
 
Esta relación se usa en todos los protocolos de magnetometría NV (sensor general, RMN 
mejorada, biomarcadores magnéticos, etc.). \[][][] 
 
*** 
 
### B.2. Modelos para organ-on-a-chip y biosensores 
 
En organ-on-a-chip, los sensores integrados (eléctricos, electroquímicos, ópticos) siguen 
principios generales:\[] 
[re.public.polimi](https://re.public.polimi.it/retrieve/handle/11311/1154772/565740/biosensors-
10-00110%20(1).pdf) 
 
1. **Modelo de concentración de metabolitos o fármacos:** 
 
\[ 
\frac{dC}{dt} = -k C + F(t) 
\] 
 

donde: 
 
- \(C(t)\): concentración de especie,   
- \(k\): tasa de eliminación/degradación,   
- \(F(t)\): entrada (flujo, liberación desde el tejido). 
 
2. **Respuesta del sensor eléctrico (ej. transistor de puerta flotante):**\[] 
 
El cambio de carga en la superficie de un sensor se traduce en cambio de tensión de 
umbral: 
 
\[ 
V_{\text{th}} = V_{\text{th},0} + \frac{Q_S}{C_{\text{tot}}} 
\] 
 
donde: 
 
- \(V_{\text{th},0}\): umbral inicial,   
- \(Q_S\): carga neta en la superficie o en la zona de detección,   
- \(C_{\text{tot}}\): capacitancia total relevante. 
 
La corriente de drenador \(I_D\) de un transistor se modela típicamente como: 
 
\[ 
I_D \approx \mu C_{\text{ox}} \frac{W}{L} (V_G - V_{\text{th}}) V_D 
\] 
 
(en régimen lineal), de forma que cambios en \(Q_S\) → cambios en \(V_{\text{th}}\) → 
cambios en \(I_D\).\[] 
 
Estos modelos se usarán en el Proyecto organ-on-a-chip y biosensores, con sensores 
eléctricos, electroquímicos y ópticos integrados en el chip.\[][][] 
 
*** 
 
### B.3. Sensores de biomarcadores y curvas de calibración 
 
Para biosensores de biomarcadores (proteínas mal plegadas, etc.):\[] 
[pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC8278381/) 
 
Se mide una señal \(S\) (intensidad óptica, corriente, frecuencia de resonancia) en función 
de concentración \(C\). Una relación típica: 
 
\[ 
S(C) = a \log(C) + b 
\] 
 
o modelos tipo Langmuir: 

 
\[ 
S(C) = S_{\max} \frac{C}{K_d + C} 
\] 
 
donde: 
 
- \(S_{\max}\): señal máxima,   
- \(K_d\): constante de disociación. 
 
Se ajustan los parámetros con datos experimentales y se invertirá la relación para estimar 
concentración a partir de la señal: 
 
\[ 
C_{\text{estimada}} = f^{-1}(S_{\text{medido}}) 
\] 
 
Esto se aplicará en el Proyecto de biomarcadores para neurodegeneración (beta-amiloide, 
alfa-sinucleína, etc.). \[][] 
 
*** 
 
### B.4. Bloque de simulación cuántica (Proyecto de fármacos) 
 
Para simulación cuántica de moléculas (VQE y similares):\[] 
[campushealthtech](https://campushealthtech.com/blog/ventajas-de-la-computacion-cuantic
a-en-medicina/) 
 
1. Hamiltoniano molecular: 
 
\[ 
\hat{H} = \sum_{ij} h_{ij} a_i^\dagger a_j + \sum_{ijkl} g_{ijkl} a_i^\dagger a_j^\dagger a_k a_l 
\] 
 
donde \(a_i^\dagger, a_i\) son operadores de creación/aniquilación, y \(h_{ij}, g_{ijkl}\) 
integrales de una base electrónica. 
 
2. Ansätz variacional \(|\psi(\theta)\rangle\).   
3. Energía: 
 
\[ 
E(\theta) = \langle \psi(\theta) | \hat{H} | \psi(\theta) \rangle 
\] 
 
4. Optimización: 
 
\[ 
\theta^* = \arg\min_{\theta} E(\theta) 

\] 
 
Estos bloques se implementarán en el Proyecto de simulación cuántica para diseño de 
fármacos. 
 
*** 
 
## C. Protocolos generales y esquemas 
 
En todos los proyectos usaremos una estructura común de protocolo: 
 
1. **Definición de variables y parámetros.**   
2. **Modelo físico/matemático.**   
3. **Esquema de adquisición de datos** (matrices \(X\), señales \(B(t)\), concentraciones 
\(C(t)\)).   
4. **Algoritmos de análisis** (calibración, sensibilidad, transformación, clasificación).   
5. **Verificación** (comparación con referencia, error, reproducibilidad).   
 
Estos bloques matemáticos que acabo de añadir se integran en: 
 
- Proyecto 1 (NV y sensor general).   
- Proyecto 2 (OPMs y neurodegeneración).   
- Próximos proyectos: organ-on-a-chip, biomarcadores, simulación cuántica, 
metamateriales. 
 
