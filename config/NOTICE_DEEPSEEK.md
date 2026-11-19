# NOTICE — DeepSeek-R1 destilado (uso local)

Este servicio usa pesos oficiales publicados de forma gratuita, ejecutados en
local con Ollama. No se incluyen los pesos en el repositorio (están en
`/workspace/ollama/models`, fuera de git).

## Modelos

- DeepSeek-R1-Distill-Qwen-1.5B (etiqueta Ollama `deepseek-r1:1.5b`, alias LiteLLM `deepseek-local-small`)
- DeepSeek-R1-Distill-Qwen-7B (etiqueta Ollama `deepseek-r1:7b`, alias LiteLLM `deepseek-local`)

Cuantización GGUF Q4_K_M procedente de Hugging Face
(`unsloth/DeepSeek-R1-Distill-Qwen-1.5B-GGUF` y
`unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF`), derivada de los pesos oficiales
de DeepSeek. Plantilla de chat, parámetros `stop` y texto MIT tomados de las
capas oficiales de la biblioteca Ollama (`registry.ollama.ai/library/deepseek-r1`).

## Atribución

- DeepSeek-R1 / DeepSeek-R1-Distill / DeepSeek-R1-0528  
  Copyright (c) 2023–2025 DeepSeek  
  Licencia MIT  
  https://github.com/deepseek-ai/DeepSeek-R1/blob/main/LICENSE  
  https://huggingface.co/deepseek-ai/DeepSeek-R1  
  https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B  
  https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B  
  Copia local: `config/licenses/LICENSE_DEEPSEEK_MIT.txt`

- Modelos base Qwen2.5-Math-1.5B y Qwen2.5-Math-7B  
  Copyright 2024 Alibaba Cloud  
  Licencia Apache License 2.0  
  https://huggingface.co/Qwen/Qwen2.5-Math-1.5B/blob/main/LICENSE  
  https://huggingface.co/Qwen/Qwen2.5-Math-7B/blob/main/LICENSE  
  Copia local: `config/licenses/LICENSE_QWEN_APACHE-2.0.txt`

No son obra original de Lázaro López Paz, El Prat de Llobregat, Barcelona, España.
Se usan tal cual, con asistencia de IA, sin presentarlos como autoría propia.
La cuantización GGUF/Ollama es un derivado de esos pesos oficiales.

Cualquier texto generado con estos modelos debe declararse como asistencia de IA
conforme a la regla de autoría del propietario.
