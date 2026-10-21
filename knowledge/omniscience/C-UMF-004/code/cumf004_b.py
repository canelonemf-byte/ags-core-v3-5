#!/usr/bin/env python3
"""C-UMF-004 parte B: energías relajadas MatterSim+D3(BJ) de todas las fases de C-UMF-002 (reanudable).
Uso: python cumf004_b.py --out DIR
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, sys, time, warnings
warnings.filterwarnings("ignore")
import torch
sys.path.insert(0, "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-UMF-002/code"); import cumf002_run as u2
from ase.build import bulk
from ase.calculators.mixing import SumCalculator
from torch_dftd.torch_dftd3_calculator import TorchDFTD3Calculator
torch.set_num_threads(2); u1 = u2.u1
ap = argparse.ArgumentParser(); ap.add_argument("--out"); A = ap.parse_args(); d = os.path.join(A.out, "mattersim"); os.makedirs(d, exist_ok=True)
d3 = TorchDFTD3Calculator(xc="pbe", damping="bj", device="cpu", dtype=torch.float64, cutoff=95 * 0.52917721)
calc = SumCalculator([u2.c4.calculator("mattersim"), d3])
for m in u2.TODOS:
    f = os.path.join(d, "c_" + m + ".json")
    if os.path.exists(f): continue
    t = time.time(); a0 = u2.structure(m); a, e, cv = u1.relax_full(a0, calc)
    u2.dump(f, {"formula": a.get_chemical_formula(mode="metal"), "n_atomos": len(a), "E_total_eV": e, "V0_A3": float(a0.get_volume()),
                "V_A3": float(a.get_volume()), "convergio": cv, "t_s": round(time.time() - t, 1)}); print(m, e, cv, flush=True)
for el, st in u1.ELEM.items():
    f = os.path.join(d, "e_" + el + ".json")
    if os.path.exists(f): continue
    a, e, cv = u1.relax_full(bulk(el, st, cubic=(st == "diamond")), calc)
    u2.dump(f, {"estructura": st, "n_atomos": len(a), "E_total_eV": e, "E_por_atomo_eV": e / len(a), "convergio": cv}); print(el, e / len(a), cv, flush=True)
for mol, dd in u1.MOL.items():
    f = os.path.join(d, "m_" + mol + ".json")
    if os.path.exists(f): continue
    a, e, cv = u1.relax_mol(mol, dd, calc)
    u2.dump(f, {"E_total_eV": e, "E_por_atomo_eV": e / 2, "d_A": float(a.get_distance(0, 1)), "convergio": cv}); print(mol, e, cv, flush=True)
print("FIN", flush=True)
