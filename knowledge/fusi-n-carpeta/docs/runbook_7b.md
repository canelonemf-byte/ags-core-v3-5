# Runbook 7B — P003 AGSGPT-LORA (Qwen2.5-7B → Mistral-7B-v0.3)

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia CC BY 4.0.
Fecha: 2026-10-21. LoRA = Low-Rank Adaptation (no los canales de radio simulados de NNC).

> **El entrenamiento 7B requiere aprobación expresa de Lázaro. Nada de este runbook se ha ejecutado.**

## Estimaciones (PENDIENTE DE VERIFICACIÓN)
| Perfil | VRAM | Tiempo (3 épocas, ~856 pares, max_len 1024) |
|---|---|---|
| QLoRA 4-bit (`*_qlora4`) | 12–16 GB | PENDIENTE DE VERIFICACIÓN |
| bf16 (`*_bf16`) | ~24 GB | PENDIENTE DE VERIFICACIÓN |
Disco: ~15 GB por modelo base en safetensors + adaptadores (PENDIENTE DE VERIFICACIÓN).

## 0. Entorno (máquina con GPU CUDA)
```bash
cd knowledge/fusi-n-carpeta
python3 -m venv .venv && . .venv/bin/activate
pip install torch transformers peft accelerate bitsandbytes pyyaml
export HF_HOME=$PWD/.hf_cache
```
## 1. Preflight (sin pesos)
```bash
python scripts/preflight_7b.py --mode qlora4   # o --mode bf16; debe decir GO
sha256sum data/test.jsonl   # 0937f06c329f1744f22570dab347aca26fa487c771356027b9bdead33e6f8ef5
```
## 2. Qwen2.5-7B (primero)
```bash
P=target_7b_qwen_qlora4        # o target_7b_qwen_bf16
python scripts/eval.py --profile $P --mode baseline
python scripts/train_lora.py --profile $P
python scripts/eval.py --profile $P --mode lora
```
## 3. Mistral-7B-v0.3 (después, mismo pipeline)
Antes: verificar el texto completo de la licencia (el repo no tiene archivo LICENSE; ficha: apache-2.0).
```bash
P=target_7b_mistral_qlora4     # o target_7b_mistral_bf16
python scripts/eval.py --profile $P --mode baseline
python scripts/train_lora.py --profile $P
python scripts/eval.py --profile $P --mode lora
```
## 4. Alucinación (m4)
`python scripts/eval_sin_respuesta.py --pred <predicciones.jsonl>` sobre `data/sin_respuesta.jsonl`.

## Criterio
Protocolo en `protocolo_comparacion.json`: m1 validez LLP estricta (principal); H0 se mantiene si ningún modelo mejora m1 ≥ 10 puntos sobre su base. La enmienda ORÁCULO (McNemar, semillas, estratos m4) **no está aprobada**.
