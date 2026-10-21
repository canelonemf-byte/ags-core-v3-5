#!/usr/bin/env python3
"""C-VIB-002: κL(300 K) RTA con phono3py y uMLIP en 15 compuestos blenda.
Uso: python cvib002_run.py --model {mattersim,mace} --out DIR [--mats ...] [--mesh 19]
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
import torch
torch.set_num_threads(4); torch.manual_seed(0); np.random.seed(0)
from ase.build import bulk
from ase.data import covalent_radii, atomic_numbers
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
from ase import Atoms
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from phono3py import Phono3py
MATS = ["BN","BP","AlP","AlAs","AlSb","GaP","GaAs","GaSb","InP","InAs","InSb","ZnS","ZnSe","ZnTe","CdTe"]
def split(m):
    import re; return re.findall(r"[A-Z][a-z]?", m)
def calculator(model):
    if model == "mattersim":
        from mattersim.forcefield import MatterSimCalculator
        return MatterSimCalculator(load_path="MatterSim-v1.0.0-5M.pth", device="cpu", dtype="float64")
    from mace.calculators import mace_mp
    return mace_mp(model="medium", default_dtype="float64", device="cpu")
def relax(m, calc):
    A, B = split(m); a0 = 4/np.sqrt(3)*(covalent_radii[atomic_numbers[A]]+covalent_radii[atomic_numbers[B]])  # D1
    at = bulk(m, "zincblende", a=a0, cubic=True); at.calc = calc; at.set_constraint(FixSymmetry(at))
    BFGS(FrechetCellFilter(at), logfile=None).run(fmax=1e-3, steps=500)
    at.set_constraint(); return at, a0
def main():
    p = argparse.ArgumentParser(); p.add_argument("--model", required=True); p.add_argument("--out", required=True)
    p.add_argument("--mats", nargs="*", default=MATS); p.add_argument("--mesh", type=int, default=19); a = p.parse_args()
    os.makedirs(a.out, exist_ok=True); calc = calculator(a.model)
    for m in a.mats:
        fn = f"{a.out}/{a.model}_{m}_m{a.mesh}.json"
        if os.path.exists(fn): continue
        t0 = time.time(); at, a0 = relax(m, calc)
        uc = PhonopyAtoms(symbols=at.get_chemical_symbols(), cell=at.cell[:], scaled_positions=at.get_scaled_positions())
        ph3 = Phono3py(uc, supercell_matrix=np.diag([2,2,2]), primitive_matrix="auto", log_level=0)
        ph3.generate_displacements(distance=0.03); F = []
        for sc in ph3.supercells_with_displacements:
            s = Atoms(sc.symbols, cell=sc.cell, scaled_positions=sc.scaled_positions, pbc=True); s.calc = calc
            f = np.array(s.get_forces(), dtype=np.float64); f -= f.mean(axis=0); F.append(f)
        ph3.forces = np.array(F); ph3.produce_fc3(symmetrize_fc3r=True)
        ph = Phonopy(uc, supercell_matrix=np.diag([2,2,2]), primitive_matrix="auto"); ph.force_constants = ph3.fc2
        ph.run_mesh([a.mesh]*3, is_gamma_center=True); md = ph.get_mesh_dict(); f = md["frequencies"]; q = md["qpoints"]
        ig = int(np.where(np.all(np.abs(q) < 1e-9, axis=1))[0][0]); mask = np.ones_like(f, bool); mask[ig, np.argsort(np.abs(f[ig]))[:3]] = False
        fmin = float(f[mask].min())
        ph3.mesh_numbers = [a.mesh]*3; ph3.init_phph_interaction()
        ph3.run_thermal_conductivity(temperatures=[300.0], is_isotope=True)
        k = np.array(ph3.thermal_conductivity.kappa)[0, 0]
        res = {"material": m, "model": a.model, "mesh": a.mesh, "a0_inicial": float(a0), "a_relajada": float(at.cell[0,0]),
               "n_disp": len(F), "fmin_THz": fmin, "kappa_xyz": k.tolist(), "kappa_300K": float(k[:3].mean()), "t_s": time.time()-t0}
        json.dump(res, open(fn, "w"), indent=1); print(m, res["a_relajada"], res["kappa_300K"], fmin, len(F), round(res["t_s"]), flush=True)
if __name__ == "__main__": main()
