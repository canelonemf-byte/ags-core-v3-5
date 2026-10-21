#!/usr/bin/env python3
"""C-UMF-001: energías totales relajadas (compuestos, elementos, moléculas) con uMLIP en float64.
Uso: python cumf001_run.py --model {mattersim,mace} --out DIR
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
import torch
torch.set_num_threads(4); torch.manual_seed(0); np.random.seed(0); torch.use_deterministic_algorithms(True)
from ase import Atoms
from ase.build import bulk
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
STORE = "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience"
sys.path.insert(0, f"{STORE}/C-MAT-004/code"); import cmat004_run as c4
sys.path.insert(0, f"{STORE}/C-MAT-005/code"); import cmat005_run as c5
FMAX = 1e-3
C4 = ["MgO", "CaO", "SrO", "BeO", "Al2O3", "Li2O", "SiO2", "TiO2", "MgAl2O4", "LiF", "NaF", "CaF2", "MgF2", "NaCl", "KCl", "KBr"]
C5 = ["Na2O", "ZrO2", "BeAl2O4", "MgTiO3", "KF", "SrF2", "BaF2", "LiCl", "CsCl", "NaBr", "KI", "AlN"]
ELEM = {"Mg": "hcp", "Be": "hcp", "Ti": "hcp", "Zr": "hcp", "Al": "fcc", "Ca": "fcc", "Sr": "fcc",
        "Li": "bcc", "Na": "bcc", "K": "bcc", "Cs": "bcc", "Ba": "bcc", "Si": "diamond"}
MOL = {"O2": 1.21, "N2": 1.10, "F2": 1.42, "Cl2": 1.99, "Br2": 2.28, "I2": 2.67}

def comp_structure(m):
    if m in C4: return c4.structure(m)
    if m == "ZrSiO4" or m in C5: return c5.structure(m)
    raise KeyError(m)

def relax_full(a, calc, steps=3000):
    a = a.copy(); a.calc = calc; a.set_constraint(FixSymmetry(a))
    conv = BFGS(FrechetCellFilter(a), logfile=None).run(fmax=FMAX, steps=steps)
    e = float(a.get_potential_energy()); a.set_constraint(); return a, e, bool(conv)

def relax_mol(name, d, calc):
    sym = name[:-1]
    a = Atoms(sym + "2", positions=[[10, 10, 10 - d / 2], [10, 10, 10 + d / 2]], cell=[20, 20, 20], pbc=True); a.calc = calc
    conv = BFGS(a, logfile=None).run(fmax=FMAX, steps=500)
    return a, float(a.get_potential_energy()), bool(conv)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--model", required=True); ap.add_argument("--out", required=True)
    ar = ap.parse_args(); os.makedirs(ar.out, exist_ok=True)
    calc = c4.calculator(ar.model); res = {"model": ar.model, "compuestos": {}, "elementos": {}, "moleculas": {}, "control_C3": {}}
    for m in C4 + C5 + ["ZrSiO4"]:
        t = time.time(); a0 = comp_structure(m); a, e, cv = relax_full(a0, calc)
        res["compuestos"][m] = {"formula": a.get_chemical_formula(mode="metal"), "n_atomos": len(a), "E_total_eV": e,
                                "V0_A3": float(a0.get_volume()), "V_A3": float(a.get_volume()), "convergio": cv, "t_s": round(time.time() - t, 1)}
        print(m, e, cv, flush=True)
    for el, st in ELEM.items():
        a0 = bulk(el, st, cubic=(st == "diamond")); a, e, cv = relax_full(a0, calc)
        res["elementos"][el] = {"estructura": st, "n_atomos": len(a), "E_total_eV": e, "E_por_atomo_eV": e / len(a), "V_A3": float(a.get_volume()), "convergio": cv}
        print(el, e / len(a), cv, flush=True)
    for mol, d in MOL.items():
        a, e, cv = relax_mol(mol, d, calc)
        res["moleculas"][mol] = {"E_total_eV": e, "E_por_atomo_eV": e / 2, "d_A": float(a.get_distance(0, 1)), "convergio": cv}
        print(mol, e, cv, flush=True)
    a, e, cv = relax_full(bulk("Mg", "fcc", a=4.52), calc)
    res["control_C3"] = {"Mg_fcc_E_por_atomo_eV": e / len(a), "convergio": cv}
    json.dump(res, open(os.path.join(ar.out, f"{ar.model}.json"), "w"), indent=1)

if __name__ == "__main__": main()
