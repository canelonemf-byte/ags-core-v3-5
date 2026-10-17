> Texto extraído automáticamente del PDF original «Proyecto número 4_30_07_2026.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1ic8WsvbTy8mw-bjuW-qILxHVlSbg3Fba/view?usp=drivesdk



 
 
# PROYECTO 4   
**Título:** Biosensores cuánticos y ópticos para biomarcadores neurodegenerativos en 
sangre y fluidos   
**Autor:** Lázaro López Paz   
**Lugar:** El Prat de Llobregat, Barcelona, España   
**Fecha:**30 Julio de 2026   
 
*** 
 
## 1. Objetivo general 
 
Desarrollar una plataforma de **biosensores avanzados** (ópticos, nanoplasmónicos y 
cuánticos basados en NV) para la detección ultrasensible de biomarcadores 
neurodegenerativos (beta-amiloide, alfa-sinucleína, tau fosforilada, etc.) en sangre y fluidos, 
orientada a diagnóstico temprano de Alzheimer, Parkinson y otras enfermedades.\[] 
[nature](https://www.nature.com/articles/s44328-025-00040-3) 
 
*** 
 
## 2. Fundamento científico 
 
### 2.1. Biomarcadores clave 
 
En neurodegeneración se usan biomarcadores como:\[][][] 
 
- **Amyloid-β (Aβ)**: asociación con placas en Alzheimer.   
- **α-synuclein (α-Syn)**: asociada a Parkinson y sinucleinopatías.   
- **Tau fosforilada (p-tau)**: daños neurofibrilares.   
 
No solo importa la concentración, sino también el **estado de plegamiento** (misfolding) de 
estas proteínas, que puede reflejar procesos patológicos años antes de los síntomas.\[] 
[azosensors](https://www.azosensors.com/news.aspx?newsID=16876) 
 
### 2.2. Biosensores ópticos y cuánticos 
 
Plataformas relevantes:\[][][][][][][] 
 
- **Sensores inmuno-infrarrojos (iRS)**: usan anticuerpos específicos y espectroscopia 
infrarroja para detectar cambios de estructura secundaria (Amide I) en proteínas de interés.   
- **Nanoplasmonic infrared metasurface sensors**: metasuperficies que amplifican señales 
infrarrojas, capaces de detectar proteínas como α-Syn con alta especificidad.\[]   
- **NV-based quantum biosensors**: sensores basados en centros NV en nanodiamantes 
funcionalizados con anticuerpos, que leen cambios magnéticos o de entorno mediante espín 
cuántico.\[][][][]   
 

Estos sistemas ofrecen límites de detección en el rango femtomolar y capacidad de 
distinguir estados estructurales patológicos.\[] 
[accscience](https://accscience.com/journal/JCTR/articles/online_first/8138) 
 
*** 
 
## 3. Objetivos específicos 
 
1. Diseñar un biosensor híbrido que combine:   
   - reconocimiento biomolecular por anticuerpos/nanostructuras,   
   - lectura óptica infrarroja o cuántica (NV). \[][][]   
2. Implementar modelos matemáticos de respuesta del sensor (curvas de calibración, 
estado de plegamiento). \[] 
[pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC8278381/)   
3. Definir protocolos de análisis de sangre y fluidos (plasma, CSF). \[][][]   
4. Integrar resultados con proyectos de neuroimagen cuántica (Proyecto 2) y OoC (Proyecto 
3). 
 
*** 
 
## 4. Diseño del biosensor híbrido 
 
### 4.1. Componente de captura biomolecular 
 
- **Superficie funcionalizada** con anticuerpos específicos para Aβ, α-Syn, p-tau, etc.\[] 
[accscience](https://accscience.com/journal/JCTR/articles/online_first/8138)   
- Opciones:   
  - capas de grafeno, nanoplata, oro, nanodiamantes, metasuperficies. \[][][][]   
- Química de superficie diseñada para:   
  - alta afinidad,   
  - baja adsorción inespecífica (capas de bloqueo). 
 
### 4.2. Componente de lectura 
 
- **Lectura infrarroja** (iRS, metasuperficie): analiza banda Amide I para determinar estado 
de plegamiento de proteínas.\[] 
[azosensors](https://www.azosensors.com/news.aspx?newsID=16876)   
- **Lectura cuántica NV**:   
  - nanodiamantes con centros NV cercanos a proteínas capturadas,   
  - cambios en entorno magnético/eléctrico/viscoelástico se traducen en cambios en 
frecuencia de resonancia y contraste de espín.\[][][][]   
 
*** 
 
## 5. Modelos matemáticos 
 
### 5.1. Curvas de calibración concentración–señal 
 

Para cada biomarcador, se desarrolla una curva \(S(C)\):\[] 
[nature](https://www.nature.com/articles/s44328-025-00040-3) 
 
1. Modelo logarítmico: 
 
\[ 
S(C) = a \log(C) + b 
\] 
 
2. Modelo tipo Langmuir (unión anticuerpo–antígeno): 
 
\[ 
S(C) = S_{\max} \frac{C}{K_d + C} 
\] 
 
donde: 
 
- \(S_{\max}\): señal máxima,   
- \(K_d\): constante de disociación,   
- \(a, b\): parámetros de ajuste. 
 
Se ajustan estos modelos con soluciones estándar de concentración conocida y se obtiene 
la función inversa: 
 
\[ 
C_{\text{estimada}} = f^{-1}(S_{\text{medido}}) 
\] 
 
### 5.2. Modelo de estado de plegamiento (iRS) 
 
Para sensores inmuno-infrarrojos:\[][][] 
 
La banda Amide I refleja la proporción de estructuras beta plegadas patológicas. 
 
Definimos: 
 
- \(S_{\text{IR}}\): intensidad o parámetro derivado de la banda Amide I.   
- \(\theta_{\beta}\): fracción de conformación beta patológica. 
 
Modelo lineal simple: 
 
\[ 
S_{\text{IR}} = S_0 + \Delta S \cdot \theta_{\beta} 
\] 
 
donde: 
 
- \(S_0\): señal basal (estado sano),   

- \(\Delta S\): cambio máximo entre estado sano y patológico. 
 
La calibración se consigue comparando muestras de controles y pacientes, construyendo 
distribuciones de \(\theta_{\beta}\) y definiendo umbrales de riesgo. 
 
### 5.3. Modelo de lectura NV para biosensado 
 
En sensores NV funcionalizados con biomoléculas:\[] 
[accscience](https://accscience.com/journal/JCTR/articles/online_first/8138) 
 
El campo magnético local \(B_{\text{loc}}\) o la variación en entorno se traduce en cambios 
de frecuencia: 
 
\[ 
f(B_{\text{loc}}) = f_0 + \gamma B_{\text{loc}} 
\] 
 
Se pueden usar protocolos de ODMR (optically detected magnetic resonance) para medir: 
 
- frecuencia de resonancia,   
- contraste \(C\),   
- ancho de línea \(\Delta \nu\). 
 
La sensibilidad teórica: 
 
\[ 
\eta_{\text{NV}} \approx \frac{\Delta \nu}{\gamma C \sqrt{R}} 
\] 
 
donde \(R\) es la tasa de fotones.\[][] 
 
Cambios en biomarcadores (unión, agregación, cambios de plegamiento) afectan 
\(B_{\text{loc}}\) y otras propiedades, produciendo cambios medibles en \(f\) y otros 
parámetros. Estos se relacionan con \(C\) (concentración) y \(\theta_{\beta}\) (estado) 
mediante curvas empíricas. 
 
*** 
 
## 6. Protocolos de análisis 
 
### 6.1. Preparación de muestras 
 
- Fluido a analizar: sangre, plasma, suero, CSF. \[] 
[azosensors](https://www.azosensors.com/news.aspx?newsID=16876)   
- Preprocesamiento:   
  - dilución controlada,   
  - filtrado,   
  - separación de fracciones si es necesario. 

 
### 6.2. Protocolo con sensor inmuno-infrarrojo (iRS) 
 
1. Inmovilizar anticuerpos específicos en la superficie del sensor. \[][]   
2. Incubar muestra para capturar proteínas objetivo (Aβ, α-Syn).   
3. Lavar para eliminar material no unido.   
4. Medir espectro infrarrojo, especialmente banda Amide I.   
5. Extraer \(S_{\text{IR}}\) y estimar \(\theta_{\beta}\).   
6. Comparar con distribuciones de controles y pacientes para obtener probabilidad de 
estado preclínico. 
 
### 6.3. Protocolo con sensor NV híbrido 
 
1. Funcionalizar nanodiamantes con anticuerpos. \[] 
[iopscience.iop](https://iopscience.iop.org/article/10.1088/2515-7647/ae46fe)   
2. Mezclar con muestra para capturar biomarcadores cerca de NV.   
3. Ubicar nanodiamantes en entorno controlado (solución, gel, chip).   
4. Iluminar con láser y aplicar microondas para ODMR. \[][]   
5. Medir frecuencia de resonancia \(f\) y parámetros de línea.   
6. Convertir cambios en \(f\) y otros parámetros en estimaciones de concentración y/o 
estado estructural usando curvas de calibración. 
 
*** 
 
## 7. Estructuras de datos y análisis 
 
### 7.1. Datos por muestra 
 
Para cada muestra: 
 
- `ID_muestra`, `tipo_fluido`, `paciente/control`.   
- `S_IR`, `theta_beta` para cada proteína (Aβ, α-Syn). \[] 
[azosensors](https://www.azosensors.com/news.aspx?newsID=16876)   
- `C_estimada` (concentración) vía iRS, NV u otros sensores. \[][][]   
- Datos clínicos asociados (diagnóstico, puntuaciones cognitivas, etc.). \[] 
[azosensors](https://www.azosensors.com/news.aspx?newsID=16876) 
 
### 7.2. Algoritmos de clasificación 
 
Usando vectores: 
 
\[ 
\mathbf{v} = \bigl( C_{Aβ}, C_{\alpha\text{-Syn}}, C_{\text{tau}}, \theta_{\beta,\text{Aβ}}, 
\theta_{\beta,\alpha\text{-Syn}}, \dots \bigr) 
\] 
 
se entrenan modelos (regresión logística, redes, etc.) para: 
 

- clasificar estado: sano / riesgo alto / enfermedad establecida,   
- predecir probabilidad de desarrollar enfermedad en un periodo dado (años). \[][][] 
 
*** 
 
## 8. Validación y desempeño 
 
### 8.1. Métricas 
 
Estudios recientes muestran: \[] 
[azosensors](https://www.azosensors.com/news.aspx?newsID=16876) 
 
- iRS puede predecir Alzheimer hasta 17 años antes del diagnóstico clínico convencional, 
con AUC ~0.82.   
- Sensores para Parkinson basados en misfolding de α-Syn alcanzan sensibilidades y 
especificidades >90%, AUC ~0.90.   
- Sistemas cuánticos híbridos NV alcanzan límites de detección de orden femtomolar, 
150–300 veces mejores que ELISA para algunos biomarcadores.   
 
Las métricas clave: 
 
- Límite de detección (LOD).   
- Precisión, sensibilidad, especificidad, AUC.   
- Reproducibilidad (CV intra/interensayo). \[][][][] 
 
*** 
 
## 9. Integración con otros proyectos 
 
- Con **Proyecto 2** (OPMs y neurodegeneración):   
  - señales neuromagnéticas + biomarcadores sanguíneos → diagnóstico multimodal. \[] 
[physicsworld](https://physicsworld.com/a/quantum-sensor-could-help-detect-dementia/)   
- Con **Proyecto 3** (OoC):   
  - OoC simula procesos de plegamiento y respuesta a fármacos; biosensores miden esos 
cambios en tiempo real. \[][][][]   
- Con proyectos futuros de IA:   
  - datos de biosensores y neuroimagen cuántica se integran en modelos predictivos. \[] 
[pmc.ncbi.nlm.nih](https://pmc.ncbi.nlm.nih.gov/articles/PMC12431406/) 
 
*** 
 
## 10. Licencia y autoría 
 
Este proyecto se publica bajo licencia **Creative Commons Atribución 4.0 Internacional (CC 
BY 4.0)**, igual que los anteriores.\[][][] 
 
Autor: **Lázaro López Paz**   
El Prat de Llobregat, Barcelona, España   

30 Julio de 2026   
