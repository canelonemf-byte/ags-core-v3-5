# Correcciones para los PDFs de AGs-Core

Archivos afectados:
- **R** = `Reporte_Tecnico_Consolidado_AGs_Core.pdf`
- **Z** = `Zenodo_AGs_Core_v3_Complete_Specification.pdf`

Referencia: el código real (`ags_core` 3.0.0 / AGs-Core v3.5, `app/ags_local/`), verificado con tests el 16/10/2026.

## 1. Número de parámetros de AGsGPT y porcentaje LoRA (R §4, Z §3 y Figura 1)
- **Dice:** "~196.000 parámetros entrenables (3,9 % del total)"; "Modelo base congelado (96,1 %) vs adaptadores LoRA (3,9 %)"; README antiguo: "~10M params".
- **Debe decir:** "Con la configuración por defecto (d=128, h=4, 4 capas, ctx=128, r=8, α=8) y un vocabulario de ~50 caracteres, AGsGPT tiene **≈0,82 M parámetros** (822.578 medidos con vocabulario 50). Los adaptadores LoRA suman **65.536 parámetros entrenables (≈8 %)**." Añadir: "La cifra total varía ligeramente con el tamaño del vocabulario."
- **Dice (R §4):** LoRA "únicamente en las matrices de proyección (W_q, W_k, W_v, W_o)".
- **Debe decir:** "LoRA se aplica a la proyección conjunta qkv, a la proyección de salida y a las dos capas lineales de la red feed-forward de cada bloque."
- **Añadir:** "La red base se inicializa aleatoriamente (semilla propia) y queda congelada **sin preentrenar**. Por eso la generación de texto no es útil todavía y no constituye una medida."
- **Dice (Z §4):** "motor de recuperación semántica RAG".
- **Debe decir:** "recuperación por coincidencia de palabras (no usa embeddings) sobre SQLite".

## 2. Cifra de amoniaco (R §3, tabla de co-simulación, fila zero_a)
- **Dice:** "400 MW eléctricos → 72.000,0 kg NH₃/h | 1.179.446,4 t CO₂ evitado/año"; subproductos "113.760 L/h H₂O | 101.018,9 kg/h O₂".
- **Debe decir:** el código usa 9,52 kWh/kg NH₃ (50 kWh/kg H₂ · 3/17 kg H₂/kg NH₃ + 0,7 kWh/kg de síntesis). Por tanto **400 MW → ≈42.008 kg NH₃/h** (25 MW → 2.625,1 kg/h, valor verificado en tests). CO₂ evitado: 1,6 kg CO₂/kg NH₃ (supuesto) → ≈67.213 kg/h ≈ **≈588.800 t/año** a 8.760 h. Recalcular también el agua y el oxígeno de los subproductos con la nueva producción, o retirarlos si no tienen herramienta en el código.
- La "métrica de salida garantizada" debe pasar a ser "estimación con los supuestos indicados".

## 3. Potencia de fusión de 961 MW (R §3, fila d3he_tokamak; Z §5)
- **Dice:** "600 MW inyectados (150 keV) → Potencia de fusión: 961,68 MW (cría autoprovista ³He)".
- **Debe decir:** "La herramienta `balance_fusion` calcula la energía por reacción D-³He (18,3 MeV = 2,93·10⁻¹² J). **No calcula la potencia** si no se dan la densidad (m⁻³) y la reactividad <σv> (m³/s), y no inventa <σv>." Eliminar la cifra de 961,68 MW y la "cría autoprovista de ³He", o presentarlas como hipótesis sin respaldo en el código.
- Revisar igualmente las demás cifras de la tabla presentadas como "garantizadas": Isp 6.885,8 s (el código da 6.887 s ideal, sin divergencia), 81,06 mN (el código necesita la corriente) y 22,32 nT/√Hz.

## 4. Cláusula de derechos frente a la licencia (R final; Z cabecera)
- **Dice (R):** "Todos los derechos de arquitectura, algoritmos variacionales, cortacircuitos y formulación cuántica quedan preservados…".
- **Dice (Z):** licencia "Creative Commons Attribution 4.0 (CC BY 4.0)".
- **Debe decir:**
  - Documentos: "Este documento se publica bajo CC BY 4.0."
  - Código: "El código de AGs-Core se publica bajo licencia MIT (ver LICENSE y NOTICE)."
  - Suprimir "todos los derechos… quedan preservados", porque contradice ambas licencias y reclama como propios elementos de terceros (Transformer, LoRA).

## 5. Atribuciones a añadir (sección "Referencias" en R y Z)
- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS 2017. (Arquitectura Transformer.)
- Hu, E. J. et al. (2022). *LoRA: Low-Rank Adaptation of Large Language Models*. ICLR 2022. arXiv:2106.09685.
- Karpathy, A. *minGPT* (2020) y *nanoGPT* (2022), licencia MIT. https://github.com/karpathy/minGPT · https://github.com/karpathy/nanoGPT. AGsGPT sigue su diseño (atención causal, bloques, generate con top-k, inicialización std 0,02).
- Microsoft, *loralib* (LoRA), licencia MIT. https://github.com/microsoft/LoRA. LoRALinear sigue su inicialización (B=0, Kaiming a=√5, escala α/r).
- En Z §2 y §3, frases como "construida desde cero" deben pasar a decir "implementación propia basada en el diseño de minGPT/nanoGPT y en LoRA (Hu et al., 2022)".

## 6. Autoría asistida por IA (cabeceras de R y Z)
- **Dice:** "Autores: Lázaro López Paz & Inteligencia Artificial".
- **Debe decir:** "Autor: Lázaro López Paz." Añadir una declaración: "En la redacción de este documento y en partes del código se utilizaron herramientas de inteligencia artificial generativa. El autor ha revisado el contenido y es responsable del mismo." (La IA no puede figurar como autora en Zenodo ni en la mayoría de repositorios y revistas.)

## 7. Otras precisiones recomendadas
- La versión documentada es la 3.0. La 3.5 añade 6 agentes de herramientas deterministas, el agente local `agsgpt` y un orquestador "reglas primero" (38 agentes en total).
- Sustituir "autoaprendizaje" por "ajuste periódico de adaptadores LoRA sobre la memoria local".
- Los "cortacircuitos de seguridad" (3 kV, 0,12 mA/cm², 150 keV, 5 MHz) no aparecen como tales en el código actual: implementarlos o describirlos como pendientes.
