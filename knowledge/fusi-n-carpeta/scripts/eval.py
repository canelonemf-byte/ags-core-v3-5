#!/usr/bin/env python3
"""Métrica: % de salidas que son LLP JSON válido (common.is_valid_llp). baseline vs lora."""
import argparse, json, time, sys
from pathlib import Path
import torch, yaml
from transformers import AutoTokenizer, AutoModelForCausalLM
sys.path.insert(0, str(Path(__file__).parent)); from common import prompt, is_valid_llp
H = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser(); ap.add_argument("--profile", default="smoke")
ap.add_argument("--mode", choices=["baseline", "lora"], required=True); a = ap.parse_args()
cfg = yaml.safe_load(open(H / "configs/lora.yaml")); c = cfg[a.profile]
torch.manual_seed(cfg["seed"]); torch.set_num_threads(int(__import__("os").environ.get("NUM_THREADS", "2")))
tok = AutoTokenizer.from_pretrained(c["base_model"])
_kw = {"dtype": getattr(torch, c.get("dtype", "float32"))}  # 2026-10-21: perfiles 7B bf16/QLoRA
if c.get("quantization"):
    from transformers import BitsAndBytesConfig
    _q = dict(c["quantization"]); _q["bnb_4bit_compute_dtype"] = getattr(torch, _q.get("bnb_4bit_compute_dtype", "bfloat16"))
    _kw = {"quantization_config": BitsAndBytesConfig(**_q), "device_map": "auto"}
model = AutoModelForCausalLM.from_pretrained(c["base_model"], **_kw)
if a.mode == "lora":
    from peft import PeftModel; model = PeftModel.from_pretrained(model, H / f"adapters/{a.profile}")
model.eval()
rows = [json.loads(l) for l in open(H / "data/test.jsonl")][: c["eval_max_samples"]]
res, t0 = [], time.time()
for r in rows:
    ids = tok(prompt(tok, r["instruction"]), return_tensors="pt", add_special_tokens=False)
    with torch.no_grad():
        o = model.generate(**ids, max_new_tokens=c["max_new_tokens"], do_sample=False, pad_token_id=tok.pad_token_id)
    txt = tok.decode(o[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)
    print(len(res)+1, round(time.time()-t0), flush=True)
    res.append({"id": r["id"], "valido_estricto": is_valid_llp(txt, True), "valido_laxo": is_valid_llp(txt, False), "salida": txt})
n = len(res)
summ = {"profile": a.profile, "modo": a.mode, "base_model": c["base_model"], "n_test": n,
        "pct_llp_valido_estricto": round(100 * sum(x["valido_estricto"] for x in res) / n, 1),
        "pct_llp_valido_laxo": round(100 * sum(x["valido_laxo"] for x in res) / n, 1),
        "decodificacion": "greedy", "max_new_tokens": c["max_new_tokens"], "segundos": round(time.time() - t0),
        "nota": "smoke test en modelo pequeño (E2 candidato), no es el objetivo 7B" if a.profile.startswith("smoke") else ""}
json.dump({**summ, "muestras": res}, open(H / f"results/eval_{a.profile}_{a.mode}.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(summ, ensure_ascii=False))
