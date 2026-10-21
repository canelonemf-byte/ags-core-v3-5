#!/usr/bin/env python3
"""C-UMF-002: energías totales relajadas de 42 sólidos, elementos y moléculas con uMLIP (float64).
Uso: python cumf002_run.py --model {mattersim,mace} --out DIR   (un JSON por fase, reanudable)
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
import torch
torch.set_num_threads(4); torch.manual_seed(0); np.random.seed(0); torch.use_deterministic_algorithms(True)
from ase.build import bulk
from ase.spacegroup import crystal
sys.path.insert(0, "/workspace/omniscience_cumf001/code"); import cumf001_run as u1
c4 = u1.c4
NUEVOS = ["NaI", "SrCl2", "BaO", "TiN", "Ti2O3", "TiO2_anatasa", "MgCl2", "ZrN", "CaI2", "LiBr", "LiI", "CsF", "MgBr2"]
TODOS = u1.C4 + u1.C5 + ["ZrSiO4"] + NUEVOS

def structure(m):
    rs = {"NaI": 6.47, "BaO": 5.52, "CsF": 6.01, "LiBr": 5.50, "LiI": 6.00, "TiN": 4.24, "ZrN": 4.58}
    if m in rs: return bulk(m, "rocksalt", a=rs[m], cubic=True)
    if m == "SrCl2": return bulk("SrCl2", "fluorite", a=6.98, cubic=True)
    if m == "Ti2O3": return crystal(["Ti", "O"], basis=[(0, 0, 0.3447), (0.3101, 0, 0.25)], spacegroup=167,
                                    cellpar=[5.157, 5.157, 13.61, 90, 90, 120], primitive_cell=True)
    if m == "TiO2_anatasa": return crystal(["Ti", "O"], basis=[(0, 0, 0), (0, 0, 0.2081)], spacegroup=141, setting=1,
                                           cellpar=[3.785, 3.785, 9.514, 90, 90, 90], primitive_cell=True)
    if m == "MgCl2": return crystal(["Mg", "Cl"], basis=[(0, 0, 0), (0, 0, 0.2578)], spacegroup=166,
                                    cellpar=[3.641, 3.641, 17.67, 90, 90, 120], primitive_cell=True)
    if m == "CaI2": return crystal(["Ca", "I"], basis=[(0, 0, 0), (1 / 3, 2 / 3, 0.25)], spacegroup=164, cellpar=[4.48, 4.48, 6.96, 90, 90, 120])
    if m == "MgBr2": return crystal(["Mg", "Br"], basis=[(0, 0, 0), (1 / 3, 2 / 3, 0.25)], spacegroup=164, cellpar=[3.81, 3.81, 6.26, 90, 90, 120])
    return u1.comp_structure(m)

def dump(f, obj):
    json.dump(obj, open(f + ".tmp", "w"), indent=1); os.replace(f + ".tmp", f)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--model", required=True); ap.add_argument("--out", required=True)
    A = ap.parse_args(); d = os.path.join(A.out, A.model); os.makedirs(d, exist_ok=True); calc = c4.calculator(A.model)
    for m in TODOS:
        f = os.path.join(d, "c_" + m + ".json")
        if os.path.exists(f): continue
        t = time.time(); a0 = structure(m); a, e, cv = u1.relax_full(a0, calc)
        dump(f, {"formula": a.get_chemical_formula(mode="metal"), "n_atomos": len(a), "E_total_eV": e, "V0_A3": float(a0.get_volume()),
                 "V_A3": float(a.get_volume()), "convergio": cv, "t_s": round(time.time() - t, 1)}); print(m, e, cv, flush=True)
    for el, st in u1.ELEM.items():
        f = os.path.join(d, "e_" + el + ".json")
        if os.path.exists(f): continue
        a, e, cv = u1.relax_full(bulk(el, st, cubic=(st == "diamond")), calc)
        dump(f, {"estructura": st, "n_atomos": len(a), "E_total_eV": e, "E_por_atomo_eV": e / len(a), "convergio": cv}); print(el, e / len(a), cv, flush=True)
    for mol, dd in u1.MOL.items():
        f = os.path.join(d, "m_" + mol + ".json")
        if os.path.exists(f): continue
        a, e, cv = u1.relax_mol(mol, dd, calc)
        dump(f, {"E_total_eV": e, "E_por_atomo_eV": e / 2, "d_A": float(a.get_distance(0, 1)), "convergio": cv}); print(mol, e, cv, flush=True)
    print("FIN", A.model, flush=True)

if __name__ == "__main__": main()
