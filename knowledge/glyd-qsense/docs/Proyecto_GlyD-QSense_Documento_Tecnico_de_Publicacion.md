# **GlyD-QSense: Sensor Cuántico de Temperatura Orgánico basado en nanocristales de glicina deuterada y lectura mediante IA**

**Autor:** Lázaro López Paz  
**Fecha:** 18 de junio de 2026  
**Licencia:** CC BY-NC-ND 4.0

## **1\. Resumen Ejecutivo**

GlyD-QSense es el primer sensor térmico cuántico orgánico, biocompatible y biodegradable. Utiliza nanocristales de glicina deuterada en fase \$\\gamma\$ para medir temperatura mediante espectroscopía Raman decodificada por una 1D-CNN, alcanzando una precisión de 0.08°C en el rango fisiológico \[cite: 6, 12\].

## **2\. Metodología y Síntesis**

| Fase | Parámetros Clave |
| :---- | :---- |
| **Síntesis** | Microfluídica con etanol deuterado (0.8 \$\\mu L/min\$) y glicina-ds (0.5 \$\\mu L/min\$) en atmósfera de Argón \[cite: 27, 28\]. |
| **Caracterización** | DRX (fase \$\\gamma\$ pura), SEM (\$220 \\pm 45\$ nm), Raman (ventana silente 2100-2300 \$cm^{-1}\$) \[cite: 31, 32, 33\]. |
| **IA (1D-CNN)** | 18,300 espectros sintéticos, arquitectura con 3 bloques convolucionales, optimizador AdamW \[cite: 34, 39\]. |

## **3\. Protocolos de Implementación**

> * **Síntesis:** Disolver 50 mg de glicina-ds en 125 \$\\mu L\$ de \$D\_2O\$ a 45°C, filtrar y mezclar en chip microfluídico añadiendo 0.1% \$p/p\$ de semillas \[cite: 27, 29\].  
> * **Validación Biológica:** Recubrimiento con DSPE-PEG(2000)-amina para internalización en células HeLa; monitorización térmica con láser IR (1450 nm) \[cite: 42, 50\].

## **4\. Resultados y Aplicaciones**

El sensor presenta un \$R^2\$ de 0.9992 y una viabilidad celular del 92% a las 24 horas \[cite: 45, 50\]. Las aplicaciones incluyen oncología (mapeo térmico), neurociencia (termogénesis) y agricultura (estrés hídrico) \[cite: 52, 53, 56\].

## **5\. Protección Intelectual y Recursos**

El proyecto cuenta con registro en Safe Creative (SAFE-20260618-GLYD-001) y sellado de tiempo blockchain \[cite: 63\]. El corpus de datos y el modelo de IA están disponibles bajo licencias abiertas para facilitar la implementación física estimada en 72,000 € \[cite: 67, 68\].
