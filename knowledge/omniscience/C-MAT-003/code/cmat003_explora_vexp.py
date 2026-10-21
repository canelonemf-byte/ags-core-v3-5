#!/usr/bin/env python3
"""EXPLORATORIO, NO pre-registrado (sin valor probatorio). C-MAT-003.
Armónico en la celda de partida (parámetros de red experimentales aproximados del prereg, sin relajar la celda;
solo posiciones internas) para ver cuánto del exceso de S viene del volumen de equilibrio del potencial.
Uso: python cmat003_explora_vexp.py --model mattersim --out out/explora_vexp"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import cmat003_run as C
ap = argparse.ArgumentParser(); ap.add_argument("--model", required=True); ap.add_argument("--out", required=True); A = ap.parse_args()
os.makedirs(A.out, exist_ok=True); calc = C.calculator(A.model)
for m in C.MATS:
    p = os.path.join(A.out, f"{A.model}_{m}.json")
    if os.path.exists(p): continue
    a, e, rc = C.relax_pos(C.structure(m), calc)
    ph, fmin, gam, tp, npr, nd = C.phonons(a, calc, C.supercell(m, "base"), C.T_EVAL)
    zp = npr / C.APF.get(m, 2)
    r = {"material": m, "V_A3_por_atomo": a.get_volume() / len(a), "fmin_THz": fmin, "S": (tp["entropy"] / zp).tolist(), "Cv": (tp["heat_capacity"] / zp).tolist()}
    json.dump(C.rnd(r), open(p, "w"), indent=1, sort_keys=True); print(A.model, m, "S298=%.3f" % r["S"][2], flush=True)
