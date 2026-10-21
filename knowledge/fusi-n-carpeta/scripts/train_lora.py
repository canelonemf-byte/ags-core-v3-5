#!/usr/bin/env python3
import argparse, json, random, time, sys
from pathlib import Path
import torch, yaml
from transformers import AutoTokenizer, AutoModelForCausalLM, get_linear_schedule_with_warmup
from peft import LoraConfig, get_peft_model
sys.path.insert(0, str(Path(__file__).parent)); from common import prompt
H = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser(); ap.add_argument("--profile", default="smoke")
ap.add_argument("--seed", type=int, default=None, help="enmienda ORÁCULO 2026-10-21: una ejecución por semilla de c['seeds']")
a = ap.parse_args()
cfg_all = yaml.safe_load(open(H / "configs/lora.yaml")); c = cfg_all[a.profile]; seed = cfg_all["seed"] if a.seed is None else a.seed
TAG = a.profile if a.seed is None else f"{a.profile}_s{a.seed}"
random.seed(seed); torch.manual_seed(seed); torch.set_num_threads(int(c.get("num_threads", __import__("os").environ.get("NUM_THREADS", "2"))))
tok = AutoTokenizer.from_pretrained(c["base_model"])
_kw = {"dtype": getattr(torch, c.get("dtype", "float32"))}  # 2026-10-21: perfiles 7B bf16/QLoRA
if c.get("quantization"):
    from transformers import BitsAndBytesConfig
    _q = dict(c["quantization"]); _q["bnb_4bit_compute_dtype"] = getattr(torch, _q.get("bnb_4bit_compute_dtype", "bfloat16"))
    _kw = {"quantization_config": BitsAndBytesConfig(**_q), "device_map": "auto"}
model = AutoModelForCausalLM.from_pretrained(c["base_model"], **_kw)
if c.get("quantization"):
    from peft import prepare_model_for_kbit_training
    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=bool(c.get("gradient_checkpointing")))
model = get_peft_model(model, LoraConfig(r=c["r"], lora_alpha=c["alpha"], lora_dropout=c["dropout"],
                       target_modules=c["target_modules"], task_type="CAUSAL_LM"))
GA = c.get("grad_accum", 1)
if c.get("gradient_checkpointing"):
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False}); model.enable_input_require_grads()
    model.config.use_cache = False
rows = [json.loads(l) for l in open(H / "data/train.jsonl")]; random.Random(seed).shuffle(rows)
def enc(r):
    p = tok(prompt(tok, r["instruction"]), add_special_tokens=False)["input_ids"]
    y = tok(r["response"] + tok.eos_token, add_special_tokens=False)["input_ids"]
    p = p[: max(0, c["max_len"] - len(y))]
    return p + y, [-100] * len(p) + y
data = [enc(r) for r in rows]
vrows = [json.loads(l) for l in open(H / "data/val.jsonl")][: c.get("val_max_samples", 0)]
vdata = [enc(r) for r in vrows]
def val_loss():
    if not vdata: return None
    model.eval(); tot = 0.0
    with torch.no_grad():
        for x, y in vdata:
            tot += model(input_ids=torch.tensor([x]), labels=torch.tensor([y])).loss.item()
    model.train(); return round(tot / len(vdata), 4)
vlog = []
steps = c["max_steps"] if c["max_steps"] > 0 else c["epochs"] * (len(data) // c["batch_size"])
opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=c["lr"])
sch = get_linear_schedule_with_warmup(opt, max(1, steps // 10), steps)
model.train(); log = []; t0 = time.time(); i = 0
if vdata: v = val_loss(); vlog.append({"step": 0, "val_loss": v}); print(f"val step 0 {v}", flush=True)
for step in range(steps):
    acc = 0.0
    for _ in range(GA):
        batch = [data[(i + k) % len(data)] for k in range(c["batch_size"])]; i += c["batch_size"]
        L = max(len(x) for x, _ in batch)
        ids = torch.tensor([x + [tok.pad_token_id] * (L - len(x)) for x, _ in batch])
        lab = torch.tensor([y + [-100] * (L - len(y)) for _, y in batch])
        att = torch.tensor([[1] * len(x) + [0] * (L - len(x)) for x, _ in batch])
        loss = model(input_ids=ids, attention_mask=att, labels=lab).loss / GA
        loss.backward(); acc += loss.item(); del loss
    opt.step(); sch.step(); opt.zero_grad()
    log.append(round(acc, 4)); print(f"step {step+1}/{steps} loss {acc:.4f} {time.time()-t0:.0f}s", flush=True)
    if vdata and c.get("val_every") and ((step + 1) % c["val_every"] == 0 or step + 1 == steps):
        v = val_loss(); vlog.append({"step": step + 1, "val_loss": v}); print(f"val step {step+1} {v}", flush=True)
out = H / f"adapters/{TAG}"; model.save_pretrained(out)
json.dump({"profile": a.profile, "base_model": c["base_model"], "steps": steps, "ejemplos_vistos": i,
           "train_pares": len(data), "loss_inicial": log[0], "loss_final": log[-1], "loss": log, "val_loss": vlog, "grad_accum": GA, "max_len": c["max_len"],
           "segundos": round(time.time() - t0), "dispositivo": "cpu", "seed": seed,
           "nota": "smoke test en modelo pequeño, no es el objetivo 7B" if a.profile.startswith("smoke") else ""},
          open(H / f"results/train_{TAG}.json", "w"), indent=1)
