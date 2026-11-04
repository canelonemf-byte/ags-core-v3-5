# Entrenar el piloto con GPU gratuita (Kaggle o Colab)

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA.
Textos CC BY 4.0 · Código MIT. Estado: **preparado, no ejecutado** (evidencia E1).

## Qué es esto
Un "cuaderno" (piloto_qlora.ipynb) que, en un ordenador de internet con tarjeta gráfica gratuita, enseña a dos modelos (Qwen2.5-7B y Mistral-7B-v0.3) con tus fichas y luego les pone el examen bloqueado de 66 preguntas. Antes de corregir comprueba la huella digital del examen; si alguien lo hubiera cambiado, se para.

## Qué necesitas subir
Un solo archivo: `agsgpt_lora_pkg.zip` (está en `/workspace/gpu_externa_pkg/`). Contiene las fichas (estudio 889, repaso 200, examen 66, preguntas sin respuesta 100), dos programas pequeños de corrección y estadística, el protocolo y las licencias. No lleva contraseñas, claves ni fichas simuladas.
Huella del zip (SHA256): ver `agsgpt_lora_pkg.zip.sha256`.

## Opción A: Kaggle (recomendada)
1. Entra en kaggle.com con tu cuenta (si no tienes, la creas tú; hace falta verificar el teléfono para usar GPU — PENDIENTE DE VERIFICACIÓN).
2. Datasets → New Dataset → sube el zip → **Visibilidad: Private** → Create.
3. Code → New Notebook → File → Import Notebook → `piloto_qlora.ipynb`.
4. Panel derecho: Add Input → tu dataset privado. Accelerator → GPU (P100 o T4 x2). Internet: activado (para descargar los modelos).
5. Deja `MODO_PILOTO = True` y pulsa **Save Version → Save & Run All** (así sigue aunque cierres el navegador).
6. Al terminar, en la pestaña Output estarán los resultados (carpeta `resultados/`). Descárgalos y pásamelos.

## Opción B: Google Colab
1. Sube la carpeta descomprimida `agsgpt_lora_pkg` a tu Drive, en `Mi unidad/agsgpt_lora_pkg`.
2. colab.research.google.com → Subir cuaderno → `piloto_qlora.ipynb`.
3. Entorno de ejecución → Cambiar tipo → GPU T4. Ejecutar todo. Te pedirá permiso para ver tu Drive.
4. **No cierres la pestaña**: Colab gratis se apaga si estás inactivo. Copia `resultados/` a Drive al acabar.

## Límites gratuitos (comprobados en la documentación oficial el 05-11-2026)
| | Kaggle (kaggle.com/docs/notebooks) | Colab (research.google.com/colaboratory/faq.html) |
|---|---|---|
| GPU | 1×P100 o 2×T4, 29 GB RAM, 4 CPU | "Varía con el tiempo" (habitualmente T4: PENDIENTE DE VERIFICACIÓN) |
| Duración máx. sesión | 12 h | "como mucho 12 h", según disponibilidad |
| Inactividad | 20 min en modo interactivo (Save & Run All no se corta) | se corta si estás inactivo; tiempo no publicado |
| Cuota semanal | PENDIENTE DE VERIFICACIÓN (se suele citar ~30 h/semana; no aparece en la página oficial consultada) | no publicada; Google dice que fluctúa |
| Disco guardado | 20 GB en /kaggle/working | — |
| Garantía | En horas punta puede haber cola | Recursos no garantizados |

## Cuánto tarda (ESTIMACIÓN, no medida)
- Modo piloto (1 modelo, 1 semilla, 200 fichas, 1 vuelta, examen base + LoRA): **≈1–2 h** en T4/P100. ESTIMACIÓN.
- Protocolo completo (2 modelos × 3 semillas × 3 vueltas × 889 fichas + exámenes): **≈20–40 h** en total. ESTIMACIÓN. No cabe en una sesión de 12 h: habría que hacerlo por partes (un modelo/semilla por sesión, cambiando `MODELOS` y `SEMILLAS`).
- Con el piloto mediremos el tiempo real y corregiremos esta estimación.

## Detalles técnicos que conviene saber
- QLoRA 4-bit (NF4) con cálculo en float16, porque T4 y P100 no tienen bf16. En P100 bitsandbytes podría dar problemas: PENDIENTE DE VERIFICACIÓN; si falla, usar T4.
- Configuración LoRA del protocolo: r 16, alpha 32, dropout 0.05, lr 1e-4, 3 vueltas, lote efectivo 4, longitud 1024, decodificación greedy 400 tokens.
- Estadística prerregistrada: McNemar exacto + corrección de Holm, intervalo Agresti-Min, semillas 42/43/44 (reutiliza `scripts/estadistica.py`).
- Los modelos base (Qwen2.5-7B, Mistral-7B-v0.3) son modelos sin plantilla de chat; el cuaderno usa la del modelo si existe y si no un formato simple "### Instrucción / ### Respuesta" (desviación menor respecto al protocolo, a anotar).
- El piloto es **E2 (no confirmatorio)**. Solo el protocolo completo cuenta como resultado.

## Licencias de los modelos (Hugging Face, consultado 05-11-2026)
- Qwen/Qwen2.5-7B: Apache-2.0 (etiqueta de la API de HF, no restringido).
- mistralai/Mistral-7B-v0.3: Apache-2.0 (etiqueta de la API de HF, no restringido). El archivo LICENSE del repo daba 404 antes: el texto completo sigue PENDIENTE DE VERIFICACIÓN.

## Reglas
Nada de esto se ejecuta sin tu permiso expreso. No se publica nada: dataset y cuaderno privados.
