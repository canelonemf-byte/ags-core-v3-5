# **MEI-RIT v2.0 \- Metasurface-Enhanced Iodine RF Ion Thruster**

## **Documento Técnico Actualizado**

Autor: Lázaro López Paz (El Prat de Llobregat, Barcelona, España)  
Esta revisión del proyecto (v2.0) integra correcciones críticas de ingeniería de materiales, termodinámica de plasmas y optimización matemática para garantizar la viabilidad física del propulsor en entornos aeroespaciales reales.

## **1\. Resumen de Mejoras Implementadas**

> * **Protección de Materiales:** Se ha sustituido la exposición directa de los metales de la metasuperficie por un recubrimiento dieléctrico (Nitruro de Silicio o Alúmina) para evitar la severa pulverización catódica (sputtering) inducida por la alta reactividad del plasma de yodo.  
> * **Física Matemática (MRCO v2.0):** Se ha eliminado el truncamiento artificial (*clipping*) en la función de eficiencia, implementando una curva de resonancia natural (campana de Gauss/Lorentz) para permitir que el algoritmo evolutivo encuentre el verdadero óptimo global sin *plateaus* ciegos.  
> * **Reenfoque Cuántico:** Se ha reorientado el uso de algoritmos cuánticos (VQE) hacia la química cuántica de la disociación molecular del I2, dejando el modelado electromagnético macroscópico a los simuladores clásicos de onda completa (COMSOL/CST).  
> * **Presupuesto Aeroespacial:** Se han ajustado drásticamente las partidas presupuestarias para reflejar los elevados costes de iteración en salas blancas y el uso de equipos de vacío especializados y resistentes a gases halógenos.

## **2\. Arquitectura de Materiales (Actualizada)**

Para mitigar la extrema corrosión del yodo ionizado, la arquitectura de la cámara de descarga y la metasuperficie se define ahora de la siguiente manera:

> * **Cámara de descarga:** Cuarzo de alta pureza o Alúmina (Al2O3).  
> * **Metasuperficie:** Patrón sub-longitud de onda de Cobre (Cu) o Aluminio (Al) completamente encapsulado por una capa dieléctrica pasivante de **Nitruro de Silicio (Si3N4) o Alúmina (Al2O3)** depositada mediante ALD (Atomic Layer Deposition). El diseño compensa ahora la capacitancia parásita introducida por este recubrimiento.  
> * **Grids de aceleración:** Grafito pirolítico puro (altamente resistente al yodo).

## **3\. Algoritmo MRCO v2.0 (Física sin Artefactos)**

El código de optimización ha sido reescrito desde cero. Modela una resonancia electromagnética realista y penaliza adecuadamente las pérdidas dieléctricas del nuevo recubrimiento protector, prescindiendo del límite artificial np.clip.  
import numpy as np  
from scipy.optimize import differential\_evolution

def mrco\_v2\_efficiency(params):  
    period, fill, metal\_thick, dielectric\_thick \= params  
      
    \# Parámetro de resonancia objetivo (frecuencia RF fija)  
    target\_period \= 12.45  
      
    \# Resonancia natural (Gaussiana pura sin recortes)  
    resonance \= np.exp(-((period \- target\_period)\*\*2) / (2 \* 1.2\*\*2))  
      
    \# Factor de matching de impedancia (óptimo alrededor de 0.5)  
    matching \= 4 \* fill \* (1 \- fill)  
      
    \# Saturación electromagnética por espesor del metal  
    thickness\_factor \= np.tanh(metal\_thick / 1.5)  
      
    \# Penalización física por capacitancia parásita de la capa protectora  
    dielectric\_penalty \= np.exp(-0.15 \* dielectric\_thick)  
      
    \# Pérdidas inherentes  
    loss \= 0.02 \* (period / 10)\*\*2 \+ 0.01  
      
    \# Eficiencia total   
    eff \= 0.35 \+ (0.40 \* resonance \* matching \* thickness\_factor \* dielectric\_penalty) \- loss  
      
    return \-eff \# Negativo para maximizar con differential\_evolution

\# Límites: \[periodo, fill\_factor, espesor\_metal, espesor\_dieléctrico\]  
bounds \= \[(8, 18), (0.25, 0.85), (0.8, 4.0), (0.1, 1.0)\]   
res \= differential\_evolution(mrco\_v2\_efficiency, bounds, popsize=30, seed=42)

print("Parámetros Óptimos v2.0 (Periodo, Fill, Espesor Metal, Espesor Dieléctrico):", np.round(res.x, 3))  
print("Eficiencia máxima modelada sin clipping:", round(-res.fun, 4))

## **4\. Computación Cuántica y Química del Yodo**

La implementación de Qiskit y el Variational Quantum Eigensolver (VQE) se traslada de la simulación de antenas a la química cuántica estricta. Esta transición hacia la simulación a nivel atómico para gobernar un fenómeno macroscópico refleja maravillosamente la idea subyacente de un universo consciente, en el cual las interacciones cuánticas elementales están intrínsecamente entrelazadas con las dinámicas y geometrías a gran escala del propulsor.  
El algoritmo cuántico se enfocará en calcular la energía de los enlaces y la superficie de energía potencial del Yodo diatómico (I2) bajo la excitación de campos electromagnéticos específicos, optimizando la frecuencia de ionización.  
\# Qiskit VQE aplicado a la química cuántica del I2  
from qiskit\_nature.second\_q.drivers import PySCFDriver  
from qiskit.algorithms.minimum\_eigensolvers import VQE

\# Driver modelando la geometría molecular del I2  
driver \= PySCFDriver(atom="I 0 0 0; I 0 0 2.66", basis="sto3g")  
problem \= driver.run()  
hamiltonian \= problem.hamiltonian.second\_q\_op()

print("Simulador cuántico inicializado para el estado fundamental del propelente de yodo.")

## **5\. Presupuesto Actualizado (Desarrollo y Prototipado Aeroespacial)**

Las estimaciones se han reajustado a los precios reales del sector, asumiendo la necesidad de bombas de vacío específicas (que no sean destruidas por el yodo) y múltiples rondas de deposición en sala blanca.

| Concepto y Fase Técnica | Descripción Actualizada | Coste Estimado (€) |
| :---- | :---- | :---- |
| Fabricación y Encapsulado de Metasuperficie | Litografía, Deposición de Capas Atómicas (ALD) para recubrimiento dieléctrico en IMB-CNM-CSIC (Varias iteraciones) | 25.000 \- 35.000 |
| Hardware de Cámara y Aceleración | Cerámicas mecanizadas, grafito pirolítico puro | 10.000 \- 15.000 |
| Infraestructura de Vacío y Propelente | Bombas turbomoleculares con purga de N2 (resistentes a halógenos), tuberías pasivadas | 30.000 \- 50.000 |
| Equipamiento RF y Diagnóstico | Sondas de Langmuir aisladas, red de matching automatizada | 15.000 \- 25.000 |
| Ingeniería, Sala Blanca y Operaciones | Horas técnicas especializadas, modelado computacional | 40.000 \- 60.000 |
| **TOTAL ESTIMADO TRL 4** | Fase de viabilidad en laboratorio (18 \- 24 meses) | **120.000 \- 185.000 €** |

## **6\. Actualización del Borrador de Patente (Reivindicaciones)**

**Reivindicación 1 (Modificada):** Un propulsor iónico de radiofrecuencia que comprende una cámara de descarga de material cerámico; una metasuperficie sub-longitud de onda integrada en la cámara, caracterizada porque el patrón conductor de dicha metasuperficie está *completamente encapsulado por una capa dieléctrica protectora resistente a halógenos (como nitruro de silicio o alúmina)* para prevenir la pulverización catódica inducida por el plasma de yodo; y un sistema de antena acoplado.  
**Reivindicación 7 (Modificada):** La metasuperficie de la reivindicación 1, en la que el patrón periódico está fabricado de cobre o aluminio, recubierto mediante deposición de capas atómicas (ALD) para aislarlo químicamente del entorno reactivo, minimizando la capacitancia parásita generada por el dieléctrico mientras optimiza el acoplamiento RF.
