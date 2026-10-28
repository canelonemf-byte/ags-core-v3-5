#!/usr/bin/env python3
"""C-NANO-003: monocapas grafeno, h-BN, MoS2, WS2, MoSe2 (MatterSim) con exponente ZA a 3 amplitudes; masivos con D3(BJ) a 95 bohr.
Uso: python nano3_run.py --run {run1,run2} --out DIR --parte {mono,bulk}
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import guardia
import numpy as np
import base_nano2 as B
from ase import Atoms
RUNS = {"run1": dict(seed=1, amps=[0.005, 0.010, 0.015], mesh_mono=[48, 48, 1], mesh_bulk=[24, 24, 8]),
        "run2": dict(seed=2, amps=[0.007, 0.012, 0.017], mesh_mono=[36, 36, 1], mesh_bulk=[18, 18, 6])}
def mono(name):
    if name in ("grafeno", "hBN", "MoS2"): return B.mono(name)
    a, dz, f = {"WS2": (3.15, 1.57, "WS2"), "MoSe2": (3.29, 1.67, "MoSe2")}[name]; d = dz / B.VAC
    return Atoms(f, cell=B.hexcell(a, B.VAC), scaled_positions=[[1/3, 2/3, .5], [2/3, 1/3, .5 + d], [2/3, 1/3, .5 - d]], pbc=True)
def run_mono(name, calc, R):
    a, conv = B.relax(mono(name), calc, [1, 1, 0, 0, 0, 1], R["seed"]); r = {"material": name, "relax_ok": conv, "a_A": float(a.cell.lengths()[0]), "por_amplitud": {}}
    for i, d in enumerate(R["amps"]):
        ph, nd = B.fonones(a, calc, B.SC_MONO, d)
        x = {"disp_A": d, "n_desplazamientos": nd, "ZA": B.za_exponente(ph, a)}
        if i == 1:
            x.update({"G": B.caracter(ph, [0, 0, 0]), "M": B.caracter(ph, [0.5, 0, 0]), "K": B.caracter(ph, [1/3, 1/3, 0])}); x.update(B.regla_S(ph, R["mesh_mono"], len(a)))
        r["por_amplitud"][str(d)] = x
    return r
def run_bulk(name, calc, R):
    a, conv = B.relax(B.bulk(name), calc, [1, 1, 1, 0, 0, 1], R["seed"]); ph, nd = B.fonones(a, calc, B.SC_BULK[name], R["amps"][1]); l = a.cell.lengths()
    r = {"material": name, "relax_ok": conv, "a_A": float(l[0]), "c_A": float(l[2]), "n_desplazamientos": nd, "disp_A": R["amps"][1], "d3_corte_bohr": B.D3_CUT_BOHR}
    r.update(B.regla_S(ph, R["mesh_bulk"], len(a))); return r
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--run", default="run1"); ap.add_argument("--out", required=True); ap.add_argument("--parte", default="mono")
    A = ap.parse_args(); guardia.activar(); R = RUNS[A.run]; bulk = A.parte == "bulk"; tag = "mattersim_d3_95" if bulk else "mattersim"
    d = os.path.join(A.out, A.run, tag); os.makedirs(d, exist_ok=True); calc = B.calculator("mattersim", bulk)
    mats = ["grafito", "hBN_bulk", "MoS2_2H"] if bulk else ["grafeno", "hBN", "MoS2", "WS2", "MoSe2"]
    for m in mats:
        f = os.path.join(d, m + ".json")
        if os.path.exists(f): continue
        t0 = time.time()
        try: r = run_bulk(m, calc, R) if bulk else run_mono(m, calc, R)
        except Exception as e: r = {"material": m, "error": repr(e)[:400], "clase": "no_evaluable"}
        r.update({"run": A.run, "semilla": R["seed"], "t_s": time.time() - t0}); json.dump(r, open(f + ".tmp", "w"), indent=1); os.replace(f + ".tmp", f)
        print(m, round(r["t_s"], 1), r.get("error", ""), flush=True)
    print("FIN", flush=True)
