# Revisión de pares MEDIUM (FUSIÓN IA) y afirmaciones MEDIUM (ORDENADOR HÍBRIDO) — 2026-10-21

**Autoría:** Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. CC BY 4.0.

## 1. FUSIÓN IA: 7 pares MEDIUM (license_check)
Ningún par se ha puesto en cuarentena: los 7 se pudieron arreglar con honestidad añadiendo el campo `revision_licencia` (fecha, hallazgo, nota, atribucion, decision="mantener_con_atribucion"). No se ha cambiado `instruction` ni `response`. El split de test NO se ha tocado (sha256 `0937f06c…6f8ef5`, idéntico).

| split:línea | id | hallazgo | resolución |
|---|---|---|---|
| train:139 | e012d6b61859bc62 | ai_text | "Aqui tienes…" es el nombre de un archivo del usuario (salida previa de IA). Declarado como redactado con asistencia de IA. |
| train:154 | 76b128b3a6aae154 | derived | Falso positivo: "basado en guías PPLN" es descripción técnica. |
| train:364 | ce6be246bdd5f25f | derived | "basado en literatura": referencias concretas PENDIENTE DE VERIFICACIÓN. |
| train:515 | 4b127944380f880b | derived | Síntesis propia a partir de cribado 2024–2026; publicaciones PENDIENTE DE VERIFICACIÓN. |
| train:611 | 3d66b0a206325d3f | derived | Atribuida la noticia de la Universidad de Murcia (OTRI) citada; licencia del texto PENDIENTE DE VERIFICACIÓN. |
| train:681 | 7ac818424d336f3b | derived | Atribuidas physicsworld.com y dicardiology.com; contenido de terceros, no investigación propia; licencia PENDIENTE DE VERIFICACIÓN. |
| val:46 | e6c8d7d87ff63195 | derived | "basado en" descriptivo; marcas `[cite: 1]` de salida de IA, fuente PENDIENTE DE VERIFICACIÓN. |

`data/` está en `.gitignore`: los cambios en `train.jsonl`/`val.jsonl` y los nuevos sha256 de `manifest.json` son locales (train/val siguen con 806/186 pares).

`app/supervisor/checks.py`: un par con `revision_licencia` pasa de MEDIUM a INFO (`derived_reviewed`/`ai_text_reviewed`); no se oculta.

## 2. ORDENADOR HÍBRIDO: 34 afirmaciones MEDIUM (review_claims)
- **Corregidas (3 líneas en 3 archivos):**
  - "garantizando BER < 10^-18" → "en este cálculo teórico (E1, PENDIENTE DE VERIFICACIÓN; solo ruido térmico kT/C) correspondería a…", en `docs/Manual_de_Fabricacion…md` y en `drive/Manual_Fabricacion…md`.
  - "Se ha demostrado inferencia precisa en PCM [R9]" → marcado como resultado de terceros; R9 PENDIENTE DE VERIFICACIÓN (`docs/algoritmos_hibridos.md`).
- **Falsos positivos (ya son cautos o niegan la validación):** 26. Incluyen "objetivos de diseño y no resultados demostrados", "usar solo sobre umbrales validados", entregables futuros ("demostrador", "modelos validados"), "Thesis B (E1 propuesta, no validada)", "scripts no validados (E2…)", "que no garantizan el margen", "distinguiendo lo demostrado en laboratorio" y "La ventaja debe provenir de".
- **Transcripciones OCR de PDFs del usuario (no se editan para no alterar el original):** 4 de "Garantiza BER < 10^-18" en `drive/Ultra-Low Power Hybrid Architectures(.pdf).ocr.md`. Se etiquetan aquí como E1 teórico, PENDIENTE DE VERIFICACIÓN.
- Los pares `lora_pares.jsonl` no contienen "garantiz/validad/demostrad".

## 3. Recuento tras volver a ejecutar las comprobaciones (13:59, hora de Madrid)
| proyecto | comprobación | antes (high/medium) | después (high/medium/low/info) |
|---|---|---|---|
| fusi-n-carpeta | license_check | 0/7 | 0/0/0/39 |
| fusi-n-carpeta | review_claims | — | 0/2/2/0 (aprobacion_smoke: "Aprobado…/NO aprobado", falso positivo) |
| ordenador-hibrido-no-binario | review_claims | 0/34 | 0/32/83/0 (quedan los 26 falsos positivos, las 4 líneas OCR y 2 copias) |
| ordenador-hibrido-no-binario | license_check | — | 0/11/0/8 (10 falsos positivos: OCR "©" y la clave JSON "copyright" en revision_llp.json; 1 cita Tossoun et al. ya atribuida en registro_evidencia.json) |
