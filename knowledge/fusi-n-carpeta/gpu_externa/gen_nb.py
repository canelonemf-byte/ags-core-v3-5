# Genera piloto_qlora.ipynb. Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. MIT.
import nbformat as nbf
nb = nbf.v4.new_notebook(); C=[]
md=lambda s:C.append(nbf.v4.new_markdown_cell(s)); code=lambda s:C.append(nbf.v4.new_code_cell(s))
md("""# P003 AGSGPT-LORA · Piloto QLoRA 4-bit (Kaggle / Colab, GPU gratuita)
Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Código MIT, texto CC BY 4.0.
Evidencia: E1 (preparado, **no ejecutado**). Protocolo prerregistrado: `protocolo_comparacion.json` (McNemar exacto + Holm, IC95 Agresti-Min, semillas 42/43/44).
Modelos base: Qwen/Qwen2.5-7B y mistralai/Mistral-7B-v0.3 (Apache-2.0 según Hugging Face).
**Notas:** T4/P100 no soportan bf16 → compute en float16. Ejecuta primero con `MODO_PILOTO=True`.""")
code("""# 0. Configuración
import os, sys, json, hashlib, glob, time
MODO_PILOTO = True          # True: 1 semilla, 1 modelo, subconjunto; False: protocolo completo
MODELOS = ["Qwen/Qwen2.5-7B", "mistralai/Mistral-7B-v0.3"]
SEMILLAS = [42, 43, 44]
TEST_SHA256 = "0937f06c329f1744f22570dab347aca26fa487c771356027b9bdead33e6f8ef5"
LORA = dict(r=16, lora_alpha=32, lora_dropout=0.05, target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"])
LR, EPOCHS, BATCH_EFECTIVO, MAX_LEN, MAX_NEW_TOKENS = 1e-4, 3, 4, 1024, 400
if MODO_PILOTO: MODELOS, SEMILLAS, EPOCHS = MODELOS[:1], [42], 1""")
code("""# 1. Localizar el paquete (Kaggle Dataset, Drive en Colab, o carpeta local)
CANDIDATOS = glob.glob("/kaggle/input/*/SHA256SUMS") + glob.glob("/kaggle/input/*/*/SHA256SUMS") + glob.glob("/content/drive/MyDrive/agsgpt_lora_pkg/SHA256SUMS") + glob.glob("/content/agsgpt_lora_pkg/SHA256SUMS") + glob.glob(os.environ.get("PKG_DIR", "./pkg") + "/SHA256SUMS")
if not CANDIDATOS and os.path.exists("/content") and not os.environ.get("PKG_DIR"):
    from google.colab import drive; drive.mount("/content/drive")  # solo Colab
    CANDIDATOS = glob.glob("/content/drive/MyDrive/agsgpt_lora_pkg/SHA256SUMS")
assert CANDIDATOS, "No encuentro el paquete (SHA256SUMS). Revisa el README."
PKG = os.path.dirname(CANDIDATOS[0]); print("Paquete:", PKG)
OUT = "/kaggle/working/resultados" if os.path.exists("/kaggle/working") else os.path.join(os.getcwd(), "resultados")
os.makedirs(OUT, exist_ok=True); sys.path.insert(0, os.path.join(PKG, "scripts"))""")
code("""# 2. Verificar integridad (SHA256SUMS y test congelado)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
for line in open(os.path.join(PKG, "SHA256SUMS")):
    h, f = line.split(maxsplit=1); f = f.strip().lstrip("*")
    assert sha(os.path.join(PKG, f)) == h, f"Hash distinto: {f}"
assert sha(os.path.join(PKG, "data/test.jsonl")) == TEST_SHA256, "TEST ALTERADO: no evaluar"
print("Integridad OK; test congelado OK")""")
code("""# 3. Cargar datos
from common import is_valid_llp, KEYS
from estadistica import comparar, resumen_semillas
load = lambda n: [json.loads(l) for l in open(os.path.join(PKG, "data", n))]
train, val, test = load("train.jsonl"), load("val.jsonl"), load("test.jsonl")
print({"train": len(train), "val": len(val), "test": len(test)})
assert (len(train), len(val), len(test)) == (889, 200, 66)
if MODO_PILOTO: train, val = train[:200], val[:40]""")
code("""# 4. Dependencias (solo en GPU)
import subprocess
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "transformers>=4.44", "peft>=0.12", "bitsandbytes>=0.43", "accelerate>=0.33"], check=True)
import torch; assert torch.cuda.is_available(), "Activa la GPU (T4/P100) antes de seguir"
print(torch.cuda.get_device_name(0))""")
code("""# 5. Funciones de entrenamiento y evaluación (QLoRA 4-bit, fp16)
import random, gc, numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, get_linear_schedule_with_warmup
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
BNB = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.float16)
def fijar(s): random.seed(s); np.random.seed(s); torch.manual_seed(s); torch.cuda.manual_seed_all(s)
def cargar(m):
    tok = AutoTokenizer.from_pretrained(m)
    if tok.pad_token is None: tok.pad_token = tok.eos_token
    if tok.chat_template is None:  # modelos base sin plantilla: formato simple documentado
        tok.chat_template = "{% for m in messages %}### Instrucción:\\n{{ m['content'] }}\\n\\n{% endfor %}{% if add_generation_prompt %}### Respuesta:\\n{% endif %}"
    mod = AutoModelForCausalLM.from_pretrained(m, quantization_config=BNB, device_map="auto")
    return tok, mod
def prompt(tok, ins): return tok.apply_chat_template([{"role": "user", "content": ins}], tokenize=False, add_generation_prompt=True)
def enc(tok, r):
    p = tok(prompt(tok, r["instruction"]), add_special_tokens=False)["input_ids"]
    a = tok(r["response"] + tok.eos_token, add_special_tokens=False)["input_ids"]
    ids = (p + a)[:MAX_LEN]; lab = ([-100] * len(p) + a)[:MAX_LEN]
    return torch.tensor([ids]), torch.tensor([lab])
def entrenar(tok, mod, seed):
    fijar(seed); mod = prepare_model_for_kbit_training(mod); mod = get_peft_model(mod, LoraConfig(task_type="CAUSAL_LM", **LORA))
    opt = torch.optim.AdamW([p for p in mod.parameters() if p.requires_grad], lr=LR)
    pasos = EPOCHS * len(train) // BATCH_EFECTIVO; sch = get_linear_schedule_with_warmup(opt, int(0.03 * pasos), pasos)
    mod.train(); hist = []
    for ep in range(EPOCHS):
        orden = list(range(len(train))); random.Random(seed + ep).shuffle(orden)
        for i, j in enumerate(orden):
            ids, lab = enc(tok, train[j]); out = mod(input_ids=ids.cuda(), labels=lab.cuda())
            (out.loss / BATCH_EFECTIVO).backward()
            if (i + 1) % BATCH_EFECTIVO == 0: opt.step(); sch.step(); opt.zero_grad()
            if i % 50 == 0: print(ep, i, round(out.loss.item(), 4), flush=True); hist.append(out.loss.item())
    mod.eval(); return mod, hist
@torch.no_grad()
def evaluar(tok, mod, filas):
    assert sha(os.path.join(PKG, "data/test.jsonl")) == TEST_SHA256  # re-verificación antes de evaluar
    res = []
    for r in filas:
        ids = tok(prompt(tok, r["instruction"]), return_tensors="pt", add_special_tokens=False).to("cuda")
        o = mod.generate(**ids, max_new_tokens=MAX_NEW_TOKENS, do_sample=False, pad_token_id=tok.pad_token_id)
        t = tok.decode(o[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)
        res.append({"id": r["id"], "estricto": is_valid_llp(t, True), "laxo": is_valid_llp(t, False), "salida": t})
    return res""")
code("""# 6. Ejecutar: base y LoRA por modelo y semilla; guarda métricas en OUT
metricas = {}
for m in MODELOS:
    tok, mod = cargar(m); tag = m.split("/")[-1]
    base = evaluar(tok, mod, test); json.dump(base, open(f"{OUT}/eval_{tag}_base.json", "w"), ensure_ascii=False)
    metricas[m] = {"base": [int(x["estricto"]) for x in base], "lora": {}}
    for s in SEMILLAS:
        mod, hist = entrenar(tok, mod, s); lora = evaluar(tok, mod, test)
        json.dump({"semilla": s, "loss": hist, "muestras": lora}, open(f"{OUT}/eval_{tag}_lora_s{s}.json", "w"), ensure_ascii=False)
        mod.save_pretrained(f"{OUT}/adaptador_{tag}_s{s}")
        metricas[m]["lora"][s] = [int(x["estricto"]) for x in lora]
        mod = mod.unload(); gc.collect(); torch.cuda.empty_cache()  # quita LoRA para la siguiente semilla
    del mod; gc.collect(); torch.cuda.empty_cache()
json.dump(metricas, open(f"{OUT}/metricas_brutas.json", "w"))""")
code("""# 7. Análisis prerregistrado: McNemar exacto + Holm (por semilla), IC95 Agresti-Min, resumen entre semillas
informe = {"evidencia": "E3 candidato" if not MODO_PILOTO else "E2 piloto (no confirmatorio)", "test_sha256": TEST_SHA256, "por_semilla": {}, "resumen": {}}
for s in SEMILLAS:
    informe["por_semilla"][s] = comparar({m: {"base": d["base"], "lora": d["lora"][s]} for m, d in metricas.items()})
for m in metricas:
    informe["resumen"][m] = resumen_semillas({s: informe["por_semilla"][s][m]["diferencia_pts"] for s in SEMILLAS})
json.dump(informe, open(f"{OUT}/informe_estadistico.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(informe["resumen"], indent=1))""")
nb.cells = C; nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, "piloto_qlora.ipynb")
