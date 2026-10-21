#!/usr/bin/env python3
"""C-MAT-002 v1.1 [desviación D1 declarada: exclude_gamma_acoustic=True] (prereg sha256 af9fd6d7…aa70). Propiedades térmicas armónicas (Phonopy) y réplica con 3 calculadores.
Uso: python cmat002_run.py --out out_runN"""
import argparse, json, os, time
import numpy as np
from ase.build import bulk
from ase import Atoms
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms

R = 8.314462618
FMAX = 1e-3; MESH = [20, 20, 20]; DISP = 0.01; STAB = -0.3
TEMPS = [100.0, 200.0, 298.15, 3000.0]
Z = {"Si": 8, "MgO": 4, "NaCl": 4}             # fórmulas por celda convencional
NAT_FU = {"Si": 1, "MgO": 2, "NaCl": 2}         # átomos por fórmula

def structs():
    return {"Si": bulk("Si", "diamond", a=5.431, cubic=True),
            "MgO": bulk("MgO", "rocksalt", a=4.212, cubic=True),
            "NaCl": bulk("NaCl", "rocksalt", a=5.640, cubic=True)}

def calculators():
    from mace.calculators import mace_mp
    from matscipy.calculators.manybody import Manybody
    from matscipy.calculators.manybody.explicit_forms import StillingerWeber, Kumagai
    from matscipy.calculators.manybody.explicit_forms.stillinger_weber import Stillinger_Weber_PRB_31_5262_Si
    from matscipy.calculators.manybody.explicit_forms.kumagai import Kumagai_Comp_Mat_Sci_39_Si
    return {"MACE": lambda: mace_mp(model="medium", default_dtype="float64", device="cpu"),
            "SW": lambda: Manybody(**StillingerWeber(Stillinger_Weber_PRB_31_5262_Si)),
            "Kumagai": lambda: Manybody(**Kumagai(Kumagai_Comp_Mat_Sci_39_Si))}

def relax(atoms, calc):
    a = atoms.copy(); a.calc = calc; a.set_constraint(FixSymmetry(a))
    opt = BFGS(FrechetCellFilter(a), logfile=None); conv = opt.run(fmax=FMAX, steps=3000)
    a.set_constraint(); return a, bool(conv)

def phonons(a, calc, n):
    ph = Phonopy(PhonopyAtoms(symbols=a.get_chemical_symbols(), cell=a.cell[:], scaled_positions=a.get_scaled_positions()),
                 supercell_matrix=np.diag([n, n, n]), primitive_matrix="auto")
    ph.generate_displacements(distance=DISP)
    F = []
    for sc in ph.supercells_with_displacements:
        at = Atoms(sc.symbols, cell=sc.cell, scaled_positions=sc.scaled_positions, pbc=True); at.calc = calc
        f = at.get_forces(); f -= f.mean(axis=0); F.append(f)
    ph.forces = np.array(F); ph.produce_force_constants(); ph.symmetrize_force_constants()
    ph.run_mesh(MESH, is_gamma_center=True)
    fmin = float(ph.get_mesh_dict()["frequencies"].min())
    gam = np.sort(ph.get_frequencies([0, 0, 0]))
    ph.run_thermal_properties(temperatures=TEMPS, exclude_gamma_acoustic=True)
    tp = ph.get_thermal_properties_dict()
    nat_ref = tp["heat_capacity"][-1] / (3 * R)        # átomos en la celda de referencia de phonopy
    scale = NAT_FU_cur / nat_ref                         # → por mol de fórmula
    out = {"fmin_THz": fmin, "gamma_THz": gam.tolist(), "gamma_TO_THz": float(np.mean(gam[-3:])),
           "nat_ref_cell": float(nat_ref), "T_K": TEMPS[:-1],
           "S_J_Kmol_fu": (tp["entropy"][:-1] * scale).tolist(), "Cv_J_Kmol_fu": (tp["heat_capacity"][:-1] * scale).tolist(),
           "F_kJ_mol_fu": (tp["free_energy"][:-1] * scale).tolist()}
    return out

def rnd(x):
    if isinstance(x, float): return float(f"{x:.8g}")
    if isinstance(x, list): return [rnd(v) for v in x]
    if isinstance(x, dict): return {k: rnd(v) for k, v in x.items()}
    return x

def main():
    global NAT_FU_cur
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); a_ = ap.parse_args(); os.makedirs(a_.out, exist_ok=True)
    C = calculators(); S = structs(); jobs = [("MACE", m) for m in ["Si", "MgO", "NaCl"]] + [("SW", "Si"), ("Kumagai", "Si")]
    res, timing = {}, {}
    cache = {}
    for cname, m in jobs:
        t0 = time.time(); calc = cache.setdefault(cname, C[cname]()); NAT_FU_cur = NAT_FU[m]
        a, conv = relax(S[m], calc)
        r = {"relax_converged": conv, "a_A": float(a.cell.lengths()[0])}
        for n in (2, 3):
            r[f"sc{n}"] = phonons(a, calc, n)
        res[f"{cname}:{m}"] = r; timing[f"{cname}:{m}"] = time.time() - t0
        print(cname, m, "a=%.4f" % r["a_A"], "TO=%.3f" % r["sc3"]["gamma_TO_THz"], "S298=%.3f" % r["sc3"]["S_J_Kmol_fu"][2], flush=True)
    json.dump(rnd(res), open(os.path.join(a_.out, "results_core.json"), "w"), indent=1, sort_keys=True)
    json.dump(timing, open(os.path.join(a_.out, "timing.json"), "w"), indent=1)

if __name__ == "__main__": main()
