#!/usr/bin/env python3
"""Preflight 7B (P003 AGSGPT-LORA): comprueba GPU/VRAM, disco, RAM, librerías, hashes del dataset y licencias.
NO descarga ni carga pesos; NO entrena. Imprime GO/NO-GO.
Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia MIT."""
import argparse, hashlib, importlib, json, shutil, subprocess, sys
from pathlib import Path

H = Path(__file__).resolve().parents[1]
TEST_SHA256 = "0937f06c329f1744f22570dab347aca26fa487c771356027b9bdead33e6f8ef5"
NEED = {"qlora4": {"vram_gb": 16, "libs": ["torch", "transformers", "peft", "bitsandbytes", "accelerate", "yaml"]},
        "bf16": {"vram_gb": 24, "libs": ["torch", "transformers", "peft", "accelerate", "yaml"]}}  # estimaciones PENDIENTE DE VERIFICACIÓN
DISK_GB, RAM_GB = 40, 16  # 2 modelos 7B ~15 GB c/u en safetensors + margen (PENDIENTE DE VERIFICACIÓN)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mode", choices=list(NEED), default="qlora4"); a = ap.parse_args()
    chk, fallos = [], []
    def add(nombre, ok, detalle, bloquea=True):
        chk.append({"check": nombre, "ok": ok, "detalle": detalle})
        if not ok and bloquea: fallos.append(nombre)
    # librerías
    vers = {}
    for m in NEED[a.mode]["libs"]:
        try: vers[m] = getattr(importlib.import_module(m), "__version__", "instalada")
        except Exception: vers[m] = ""
    add("librerias", all(vers.values()), {k: (v or "AUSENTE") for k, v in vers.items()})
    # GPU
    gpus = []
    try:
        import torch
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                p = torch.cuda.get_device_properties(i); gpus.append({"nombre": p.name, "vram_gb": round(p.total_memory / 2**30, 1)})
            add("bf16_soportado", torch.cuda.is_bf16_supported(), "")
    except Exception: pass
    if not gpus and shutil.which("nvidia-smi"):
        try:
            out = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=10).stdout
            gpus = [{"nombre": n.strip(), "vram_gb": round(float(m) / 1024, 1)} for n, m in (l.split(",") for l in out.strip().splitlines() if l)]
        except Exception: pass
    add("gpu", bool(gpus), gpus or "sin GPU CUDA")
    add("vram", any(g["vram_gb"] >= NEED[a.mode]["vram_gb"] for g in gpus), f">= {NEED[a.mode]['vram_gb']} GB requeridos (estimación PENDIENTE DE VERIFICACIÓN)")
    # disco y RAM
    free = shutil.disk_usage(H).free / 2**30
    add("disco", free >= DISK_GB, f"{free:.0f} GB libres, >= {DISK_GB} GB")
    try:
        mi = {l.split(":")[0]: int(l.split()[1]) for l in open("/proc/meminfo")}
        tot, av = mi["MemTotal"] / 2**20, mi["MemAvailable"] / 2**20
    except Exception: tot = av = 0.0
    add("ram", tot >= RAM_GB, f"total {tot:.1f} GB, disponible {av:.1f} GB, >= {RAM_GB} GB")
    # dataset
    D = H / "data"
    t = D / "test.jsonl"
    add("test_congelado", t.exists() and sha(t) == TEST_SHA256, sha(t) if t.exists() else "falta test.jsonl")
    man = json.loads((D / "manifest.json").read_text()) if (D / "manifest.json").exists() else {}
    hs = man.get("archivos_sha256", {})
    mism = [f for f, h in hs.items() if not (D / f).exists() or sha(D / f) != h]
    add("hashes_manifest", bool(hs) and not mism, {"archivos": len(hs), "discrepancias": mism})
    sp = {s: sum(1 for l in (D / f"{s}.jsonl").read_text().splitlines() if l.strip()) for s in ("train", "val", "test")}
    sim = sum(1 for s in ("train", "val", "test") for l in (D / f"{s}.jsonl").read_text().splitlines() if l.strip() and json.loads(l).get("simulado") is True)
    add("sin_simulados_en_splits", sim == 0, {"splits": sp, "simulados_en_splits": sim})
    add("sin_respuesta", (D / "sin_respuesta.jsonl").exists(), "data/sin_respuesta.jsonl")
    # licencias (notas, no bloquean salvo Qwen ausente)
    lic = json.loads((H / "licencias.json").read_text()) if (H / "licencias.json").exists() else {}
    add("licencias", bool(lic), "Qwen2.5-7B apache-2.0 (LICENSE en repo); Mistral-7B-v0.3 apache-2.0 en ficha, sin LICENSE en repo: texto PENDIENTE DE VERIFICACIÓN", bloquea=False)
    add("aprobacion_lazaro", False, "entrenar 7B requiere aprobación expresa de Lázaro (no comprobable por script)", bloquea=False)
    res = {"modo": a.mode, "veredicto": "GO" if not fallos else "NO-GO", "bloqueos": fallos, "checks": chk,
           "nota": "GO técnico no autoriza entrenar: falta aprobación de Lázaro"}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0 if not fallos else 1

if __name__ == "__main__":
    sys.exit(main())
