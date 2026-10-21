#!/usr/bin/env python3
"""C-UMF-003 parte B: volúmenes relajados MatterSim sin y con D3(BJ, PBE). Uso: python cumf003_mlip.py --out DIR (reanudable)
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, sys, time, warnings
warnings.filterwarnings("ignore")
import numpy as np, torch
torch.set_num_threads(1); torch.manual_seed(0); np.random.seed(0)
from ase.calculators.mixing import SumCalculator
from torch_dftd.torch_dftd3_calculator import TorchDFTD3Calculator
sys.path.insert(0, "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-UMF-002/code"); import cumf002_run as u2
u1 = u2.u1; torch.set_num_threads(1)
MATS = ["MgCl2", "CaI2", "MgBr2", "NaCl", "KCl", "MgO", "CaF2", "LiF", "TiO2"]
ap = argparse.ArgumentParser(); ap.add_argument("--out"); A = ap.parse_args(); os.makedirs(A.out, exist_ok=True)
ms = u2.c4.calculator("mattersim")
d3 = TorchDFTD3Calculator(xc="pbe", damping="bj", device="cpu", dtype=torch.float64, cutoff=95 * 0.52917721)
for var, calc in [("ms", ms), ("ms_d3", SumCalculator([ms, d3]))]:
    for m in MATS:
        f = os.path.join(A.out, f"{var}_{m}.json")
        if os.path.exists(f): continue
        t = time.time(); a0 = u2.structure(m); a, e, cv = u1.relax_full(a0.copy(), calc)
        v0, v = float(a0.get_volume()), float(a.get_volume())
        json.dump({"var": var, "mat": m, "V_exp_A3": v0, "V_A3": v, "dV_rel": (v - v0) / v0, "E_eV": float(e), "convergio": bool(cv), "t_s": round(time.time() - t, 1)},
                  open(f + ".tmp", "w"), indent=1); os.replace(f + ".tmp", f); print(var, m, (v - v0) / v0, cv, flush=True)
print("FIN", flush=True)
