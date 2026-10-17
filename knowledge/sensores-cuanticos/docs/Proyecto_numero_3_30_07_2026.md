> Texto extraído automáticamente del PDF original « Proyecto número 3_30_07_2026.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1qqUVTAFd3Q53ZWxHr-k60Zf424ZqS896/view?usp=drivesdk



 
 
# PROYECTO 3   
**Título:** Organ-on-a-chip con biosensores cuánticos para diagnóstico avanzado   
**Autor:** Lázaro López Paz   
**Lugar:** El Prat de Llobregat, Barcelona, España   
**Fecha:**30 Julio de 2026   
 
*** 
 
## 1. Objetivo general 
 
Diseñar y validar un sistema **organ-on-a-chip (OoC)** que integre biosensores (eléctricos, 
ópticos y cuánticos) para monitorizar en tiempo real procesos celulares y moleculares 
relevantes en enfermedades (incluidas neurodegenerativas y cardiovasculares), facilitando 
diagnóstico avanzado y estudio de fármacos. \[] 
[mps.amegroups](https://mps.amegroups.org/article/view/4689/html) 
 
*** 
 
## 2. Fundamento científico 
 
### 2.1. Organ-on-a-chip y microfisiología 
 
Los OoC son sistemas microfluídicos que replican funciones de órganos humanos (pulmón, 
hígado, corazón, cerebro, barrera hematoencefálica) mediante células humanas en 
entornos controlados. \[][] Permiten: 
 
- recrear condiciones mecánicas (flujo, presión, deformación),   
- estudiar respuesta a fármacos, toxinas, inflamación,   
- reducir dependencia de modelos animales. 
 
### 2.2. Sensores integrados en OoC 
 
Los sensores en OoC se integran para monitorizar: \[] 
[re.public.polimi](https://re.public.polimi.it/retrieve/handle/11311/1154772/565740/biosensors-
10-00110%20(1).pdf) 
 
- variables **físicas**: presión, flujo, deformación, potencial eléctrico.   
- variables **químicas**: pH, oxígeno, metabolitos, iones.   
- variables **bioquímicas**: biomarcadores de proteínas, estados de plegamiento, actividad 
enzimática. 
 
Se clasifican en: 
 
- sensores **eléctricos**,   
- **electroquímicos**,   
- **ópticos**,   

- y, en proyectos avanzados, **cuánticos** (como NV, OPMs, sensores infrarrojos láser). 
 
*** 
 
## 3. Objetivos específicos 
 
1. Diseñar un OoC híbrido (por ejemplo, modelo de tejido cerebral o cardíaco) con 
integración de biosensores. \[][][]   
2. Implementar modelos matemáticos de:   
   - dinámica de concentraciones de metabolitos/fármacos,   
   - respuesta de sensores (corriente, voltaje, intensidad óptica) a cambios de carga y 
concentración. \[] [nature](https://www.nature.com/articles/s41598-023-34786-5)   
3. Integrar sensores cuánticos (NV, infrarrojo láser de cascada) para medir biomarcadores 
de plegamiento de proteínas o campos electromagnéticos locales. \[][]   
4. Definir protocolos de adquisición, análisis y verificación. 
 
*** 
 
## 4. Diseño del dispositivo OoC 
 
### 4.1. Arquitectura física 
 
Un diseño típico incluye: \[] 
[mps.amegroups](https://mps.amegroups.org/article/view/4689/html) 
 
- **Canales microfluídicos** para flujo de medios y fármacos.   
- **Cámara de tejido** donde se cultivan células (ej. neuronas, cardiomiocitos, células 
epiteliales).   
- **Sensores integrados** en paredes o superficie:   
  - electrodos TEER y de impedancia (estado de barrera o monocapa),   
  - microelectrodos para potencial de acción,   
  - sensores de pH/oxígeno,   
  - interfaces para sensores cuánticos (ej. nanodiamantes NV cerca de células, sensores 
infrarrojos láser para plegamiento de proteínas). \[][][][] 
 
### 4.2. Integración de biosensores 
 
Ejemplo de combinación: 
 
- un **sensor eléctrico** basado en transistor de puerta flotante (FG-FET) para medir carga 
y potencial de acción, \[]   
- sensores ópticos o infrarrojos para estado de plegamiento de proteínas en el medio. \[]   
- nanodiamantes NV introducidos en células para medir campos y procesos inflamatorios 
internos. \[] 
[um](https://www.um.es/web/otri/actualidad/noticias/-/asset_publisher/LFx92NCkGzLx/conte
nt/el-grupo-quantum-technologies-de-la-umu-logra-introducir-nanodiamantes-con-sensores-
cu%C3%A1nticos-en-las-c%C3%A9lulas-que-act%C3%BAan-como-chivatos-de-enfermeda
des-antes-de-mostrar-s%C3%ADntomas) 

 
*** 
 
## 5. Modelos matemáticos 
 
### 5.1. Dinámica de concentración de especies 
 
Para cualquier metabolito o fármaco \(C(t)\) en la cámara: 
 
\[ 
\frac{dC}{dt} = -k C + F(t) 
\] 
 
donde: \[][] 
 
- \(k\): tasa de eliminación (metabolismo, degradación, salida por flujo).   
- \(F(t)\): función fuente (entrada por perfusión, liberación desde células). 
 
Si el flujo es constante y \(F(t) = F_0\): 
 
\[ 
C(t) = C_{\text{eq}} + (C_0 - C_{\text{eq}}) e^{-kt}, \quad C_{\text{eq}} = \frac{F_0}{k} 
\] 
 
Este modelo se usa para simular la evolución de concentración de fármaco y su relación 
con respuesta celular medida por sensores. 
 
### 5.2. Modelo de sensor eléctrico FG-FET 
 
El sensor de puerta flotante responde a cambios de carga cerca del electrodo. \[] 
 
- Carga total en la superficie: \(Q_S\).   
- Capacitancia total relevante: \(C_{\text{tot}}\).   
- Umbral de tensión: 
 
\[ 
V_{\text{th}} = V_{\text{th},0} + \frac{Q_S}{C_{\text{tot}}} 
\] 
 
La corriente de drenador (régimen simplificado, lineal): 
 
\[ 
I_D \approx \mu C_{\text{ox}} \frac{W}{L} (V_G - V_{\text{th}}) V_D 
\] 
 
donde: \[] 
 
- \(\mu\): movilidad,   

- \(C_{\text{ox}}\): capacitancia por unidad de área del óxido,   
- \(W/L\): geometría del transistor,   
- \(V_G\): tensión de puerta,   
- \(V_D\): tensión de drenador. 
 
Cambios en \(Q_S\) debido a biomoléculas (proteínas, iones) o actividad celular → cambios 
en \(V_{\text{th}}\) → cambios medibles en \(I_D\). 
 
### 5.3. Modelo de TEER e impedancia de monocapa 
 
La **trans-epithelial/endothelial electrical resistance (TEER)** es un indicador del estado de 
una barrera de células epiteliales o endoteliales. \[] 
 
Se mide la resistencia \(R_{\text{TEER}}\) a través de la monocapa: 
 
\[ 
R_{\text{TEER}} = \frac{V}{I} 
\] 
 
Los sensores TEER integrados (electrodos Ag/AgCl, etc.) permiten monitorizar integridad de 
la barrera intestinal, renal, etc., lo que es clave para estudiar la permeabilidad y efecto de 
fármacos. \[] 
 
### 5.4. Biosensores cuánticos de plegamiento de proteínas 
 
Como en el sensor inmuno-infrarrojo para beta-amiloide y alfa-sinucleína: \[] 
 
La señal espectroscópica \(S\) depende del estado de plegamiento de la proteína: 
 
- Se captura proteína específica mediante anticuerpos en la superficie del sensor.   
- Se mide espectro infrarrojo con láser de cascada cuántica.   
- La señal \(S\) refleja la proporción de estructuras beta plegadas, asociadas a estados 
patológicos. 
 
Modelo simplificado: 
 
\[ 
S = S_0 + \Delta S \cdot \theta_{\beta} 
\] 
 
donde: 
 
- \(\theta_{\beta}\): fracción de proteína en configuración beta patológica,   
- \(S_0\): señal basal,   
- \(\Delta S\): contribución máxima de estructuras patológicas. 
 
La calibración relaciona \(\theta_{\beta}\) con riesgo de enfermedad, y se puede integrar con 
el OoC para estudiar cómo fármacos modifican el plegamiento. 

 
*** 
 
## 6. Protocolos de adquisición de datos 
 
### 6.1. Estructura de datos 
 
Para cada experimento en OoC: 
 
- `ID_experimento`, `Fecha_hora`.   
- `Configuracion_chip` (tipo de tejido, flujo, sensores activos).   
- `C(t)` para cada especie importante (registro o simulación).   
- `I_D(t)` y `V_{\text{th}}(t)` para sensores eléctricos.   
- `R_{\text{TEER}}(t)` para barrera.   
- `S(t)` espectroscópico para plegamiento de proteínas.   
- `B(t)` si se usan sensores cuánticos NV u OPM para campos. \[][][][] 
 
### 6.2. Protocolo típico 
 
1. Preparar chip con células y sensores integrados.   
2. Establecer flujo basal de medio.   
3. Introducir fármaco o estímulo (entrada \(F(t)\)).   
4. Registrar continuamente: 
 
   - concentraciones (si se mide),   
   - señales eléctricas (FG-FET, TEER, potencial de acción),   
   - señales ópticas/cuánticas (espectros, campos).   
 
5. Repetir para distintos concentraciones y condiciones.   
6. Calibrar modelos: 
 
   - ajustar parámetros \(k, F_0, C_{\text{tot}}, \mu\), etc.,   
   - establecer curvas de respuesta. 
 
*** 
 
## 7. Algoritmos de análisis 
 
### 7.1. Ajuste de modelos dinámicos 
 
Para cada especie \(C(t)\): 
 
1. Ajustar \(k\) y \(F_0\) a datos experimentales.   
2. Usar modelo para predecir \(C(t)\) bajo nuevas condiciones. \[] 
[re.public.polimi](https://re.public.polimi.it/retrieve/handle/11311/1154772/565740/biosensors-
10-00110%20(1).pdf) 
 
### 7.2. Inferencia de estados celulares 

 
A partir de: 
 
- \(I_D(t)\): actividad eléctrica,   
- \(R_{\text{TEER}}(t)\): integridad de la barrera,   
- \(S(t)\): estado de plegamiento de proteínas, 
 
se define un vector de características \(\mathbf{v}(t)\) que describe el estado del tejido: 
 
\[ 
\mathbf{v}(t) = \bigl( C(t), I_D(t), R_{\text{TEER}}(t), S(t), B(t) \bigr) 
\] 
 
Con IA, se entrenan modelos para: 
 
- clasificar estados (sano vs inflamado vs degenerativo),   
- predecir respuesta a fármacos,   
- detectar señales tempranas de toxicidad o efectividad. \[][][] 
 
*** 
 
## 8. Verificación y validación 
 
### 8.1. Comparación con datos in vivo y clínicos 
 
- Comparar respuesta del OoC con datos de pacientes o modelos animales. \[] 
[mps.amegroups](https://mps.amegroups.org/article/view/4689/html)   
- Validar que cambios en \(C(t), I_D, R_{\text{TEER}}, S\) se correlacionan con marcadores 
clínicos (biomarcadores en sangre, imagen, etc.). \[][] 
 
### 8.2. Reproducibilidad 
 
- Repetir experimentos con chips distintos y lotes de células.   
- Verificar que modelos y parámetros se mantienen dentro de rangos aceptables. 
 
*** 
 
## 9. Integración con proyectos 1 y 2 
 
El OoC con biosensores cuánticos se integra directamente con: 
 
- **Proyecto 1:** sensores NV para campos magnéticos locales en el chip, estudiando 
procesos inflamatorios y actividad eléctrica a escala celular. \[] 
[um](https://www.um.es/web/otri/actualidad/noticias/-/asset_publisher/LFx92NCkGzLx/conte
nt/el-grupo-quantum-technologies-de-la-umu-logra-introducir-nanodiamantes-con-sensores-
cu%C3%A1nticos-en-las-c%C3%A9lulas-que-act%C3%BAan-como-chivatos-de-enfermeda
des-antes-de-mostrar-s%C3%ADntomas)   

- **Proyecto 2:** OPMs y lectura de actividad cerebral macro; los datos de OoC sirven como 
modelo para interpretar señales cerebrales y validar mecanismos. \[][][] 
 
*** 
 
## 10. Licencia y autoría 
 
Este proyecto se publica bajo la misma licencia **Creative Commons Atribución 4.0 
Internacional (CC BY 4.0)** que los anteriores.\[] 
[creativecommons](https://creativecommons.org/licenses/by/4.0/deed.es) 
 
Autor: **Lázaro López Paz**   
El Prat de Llobregat, Barcelona, España   
30 Julio de 2026 
