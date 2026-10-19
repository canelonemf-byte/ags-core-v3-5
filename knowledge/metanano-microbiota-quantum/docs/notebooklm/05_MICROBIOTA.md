<!-- Fuente: Drive NotebookLM_Fuentes_2026-08-30 · https://docs.google.com/document/d/1NguoCttBUuUROG1OepSeOb8L0lQY5TjmYxHD6ZwKVHU/edit · copia de texto, sin cambios de contenido -->

# Fuente NotebookLM — MetaNanoMicrobiota Quantum

**Inventor:** Lázaro López Paz, Barcelona, 2026.
**Estado de evidencia:** plataforma conceptual + protocolo de CQDs + modelo gLV + borrador de claims.
**Los PDFs cortos de «Clinical Pilot / GMP DoE / Patent v2» en Drive pesan 3–6 KB: son índices o stubs; la sustancia está en el PDF de plataforma (~206 KB) y en scripts no siempre presentes como texto plano.**

## Ficha de gobernanza

```
Estado: concepto + protocolo de síntesis de CQDs + modelo ecológico gLV
Pregunta técnica: ¿se puede personalizar un delivery colon-específico (alginato–quitosano–Eudragit + tributirina + Zn/Mg/Se + cepas) con un modelo gLV de 7 grupos y, a medio plazo, sensores/CQDs?
Limitaciones: CQDs a 250 °C y umbral 0,5 mg/mL son protocolo de lab, no producto aprobado. Biología cuántica (entrelazamiento en H-bonds) es marco teórico, no medida en heces.
Próximo hito verificable: lote de microgeles con release pH y un gLV reproducible con parámetros publicados (r_i, α_ij).
```

No es suplemento comercial ni ensayo clínico autorizado. CQDs y cápsulas: solo laboratorio.

## Núcleo material

**CQDs hidrotermales (protocolo del informe):**

- 5 g D-glucosa + 5 g glicina en 50 mL agua.
- Autoclave 250 °C, 3 h.
- 8000 r/min 20 min; diálisis MWCO 3500 Da, 72 h; 0,22 µm.
- Tamaño declarado 2,29 ± 0,31 nm; λ_ex 370 nm / λ_em 440 nm.

**Cápsula:**

- Alginato 1,5 % + quitosano 0,5 %.
- Tributirina 300–500 mg.
- Probióticos según diagnóstico.
- Zn, Mg, Se.
- Eudragit colon-específico.

Umbral de citotoxicidad citado para CQDs: 0,5 mg/mL (LDH, ROS, MDA por encima).

## Modelo gLV

$$\frac{dx_i}{dt} = x_i \left( r_i + \sum_{j=1}^{n} \alpha_{ij} x_j \right)$$

Hasta 7 grupos funcionales (p. ej. productores de butirato vs competidores).
Software nombrado: `enhanced_microbiome_simulation.py`, `ai_personalization_recommender.py`, más `project_integrator.py` en la carpeta.

## Biología cuántica (marco, no dato clínico)

- Estado de enlace covalente en superposición de configuraciones iónicas.
- Tunelamiento de protones en H-bonds.
- Discriminación de ligandos 3ⁿ − 1 con n H-bonds (cita arXiv:1807.00647v1).
- Nanocables Geobacter / Shewanella y «química de espín» como horizonte de sensores.

NotebookLM no debe presentar esto como mecanismo demostrado del producto.

## Claims de borrador (no patente concedida)

1. Delivery alginato–quitosano + recubrimiento pH.
2. Composición tributirina + Zn/Mg/Se.
3. Software gLV de 7 grupos.
4. Uso para carga alostática / sincronización de redes (muy amplio; FTO crítico).
5. Dispositivo de monitoreo por química de espín.

## Roadmap

1. Suplementación tributirina + minerales.
2. Tests 16S + script de personalización.
3. Cápsulas nano GMP.
4. Sensores metamaterial / capa cuántica.

## Cómo debe responder NotebookLM

- Fase 1 es nutrición/postbiótico conocido; las fases 3–4 no están fabricadas.
- Preferir la carpeta `MetaNanoMicrobiota_Quantum` (30 ago) frente a `Meta Nano Microbiota_Quantum` (julio).
- Primers RT-qPCR del PDF son de referencia de lab; no un kit clínico.
