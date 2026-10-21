---
base_model: HuggingFaceTB/SmolLM2-135M-Instruct
library_name: peft
tags: [lora, smoke]
---
# AGsGPT+LoRA smoke_lowmem (adaptador de prueba)

- autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA
- licencia: MIT (código/adaptador propio); modelo base de terceros con su propia licencia (PENDIENTE DE VERIFICACIÓN en su ficha de Hugging Face)
- evidencia: E2_smoke_minimo (135M, CPU, 60 pasos, n_test=20); sin mejora medible (0 % baseline y LoRA)
- uso: solo prueba de pipeline; no publicar ni usar como modelo
- resultados: ../../results/resumen_smoke.json
