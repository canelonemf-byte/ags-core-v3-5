# fusi-n-carpeta-
proyecto 

## Glosario: dos "LoRA" distintos
- **LoRA (Low-Rank Adaptation)**: técnica de ajuste fino con adaptadores de bajo rango (PEFT). Es lo que entrena `scripts/train_lora.py` y se guarda en `adapters/`.
- **LoRA en NNC**: canales de radio *simulados* (Air/Water/Land/Space/Fauna, `SIMULADO_NO_CONECTADO`) en `ags_core_lora_agents.py`. No son adaptadores, no tienen pesos ni torch/peft.
- `scripts/build_nnc_dataset.py` es solo diseño: no se ha ejecutado (falta aprobación para usar datos NNC).
