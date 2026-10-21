#!/usr/bin/env python3
"""C-MAT-005: fonones armónicos en el volumen experimental (V_exp) frente a NIST-JANAF, float64.
Uso: python cmat005_run.py --model {mattersim,mace} --out DIR [--mats AlN,...]
Un JSON por material en DIR/<model>/<mat>.json; reanudable (salta los existentes).
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
import torch
torch.set_num_threads(4); torch.manual_seed(0); np.random.seed(0); torch.use_deterministic_algorithms(True)
from ase import Atoms
from ase.build import bulk
from ase.io import read
from ase.spacegroup import crystal
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms

HERE = os.path.dirname(os.path.abspath(__file__)); REFS = os.path.join(HERE, "..", "refs")
R = 8.314462618; FMAX = 1e-3; DISP = 0.01; MESH = 60.0
T_EVAL = [100.0, 200.0, 298.15, 600.0]
MATS = ["AlN", "SiC", "KF", "NaBr", "KI", "LiCl", "CsCl", "SrF2", "BaF2", "Na2O", "ZrO2", "BeAl2O4", "MgTiO3", "ZrSiO4"]
CONTROL = ["Si", "MgO"]                                             # C1: regresión frente a C-MAT-004 (arm_Vexp)
APF = {"Si": 1, "Ge": 1, "Cu": 1, "SrF2": 3, "BaF2": 3, "Na2O": 3, "ZrO2": 3, "BeAl2O4": 7, "MgTiO3": 5, "ZrSiO4": 6}
VEXP = json.load(open(os.path.join(REFS, "vexp_C-MAT-005.json")))["V_exp_A3_por_formula"] if os.path.exists(os.path.join(REFS, "vexp_C-MAT-005.json")) else {}
VEXP_OTROS = {"Ge": 22.635, "Cu": 11.81, "Si": 20.0195, "MgO": 18.6811}   # humo (Ge, Cu) y C1 (Si, MgO: V_exp de C-MAT-004)

def structure(m):
    rs = {"KF": 5.347, "NaBr": 5.973, "KI": 7.066, "LiCl": 5.130, "MgO": 4.212}
    if m in rs: return bulk(m, "rocksalt", a=rs[m], cubic=True)
    if m == "Si": return bulk("Si", "diamond", a=5.431, cubic=True)
    if m == "Ge": return bulk("Ge", "diamond", a=5.658, cubic=True)
    if m == "Cu": return bulk("Cu", "fcc", a=3.615, cubic=True)
    if m == "SiC": return bulk("SiC", "zincblende", a=4.3596, cubic=True)
    if m == "AlN": return bulk("AlN", "wurtzite", a=3.111, c=4.979, u=0.382)
    if m == "CsCl": return bulk("CsCl", "cesiumchloride", a=4.123)
    if m == "SrF2": return bulk("SrF2", "fluorite", a=5.800, cubic=True)
    if m == "BaF2": return bulk("BaF2", "fluorite", a=6.200, cubic=True)
    if m == "Na2O": return bulk("ONa2", "fluorite", a=5.55, cubic=True)
    cif = {"ZrO2": "cod_9016714.cif", "BeAl2O4": "cod_2100925.cif", "MgTiO3": "cod_MgTiO3.cif", "ZrSiO4": "cod_ZrSiO4.cif"}
    if m in cif:
        a = read(os.path.join(REFS, "cif", cif[m]))
        if m in ("MgTiO3", "ZrSiO4"):                                   # celda primitiva (romboédrica / tetragonal centrada)
            import spglib
            c, p, z = spglib.standardize_cell((a.cell[:], a.get_scaled_positions(), a.numbers), to_primitive=True, symprec=1e-3)
            a = Atoms(numbers=z, cell=c, scaled_positions=p, pbc=True)
        return a
    raise KeyError(m)

def supercell(m, kind):
    base = {"CsCl": (4, 4, 4), "AlN": (3, 3, 2), "ZrO2": (2, 2, 2), "BeAl2O4": (1, 2, 2), "MgTiO3": (2, 2, 2), "ZrSiO4": (2, 2, 2)}
    big = {"CsCl": (5, 5, 5), "AlN": (4, 4, 3), "ZrO2": (3, 3, 3), "BeAl2O4": (2, 2, 3), "MgTiO3": (3, 3, 3), "ZrSiO4": (3, 3, 3)}
    return (base if kind == "base" else big).get(m, (2, 2, 2) if kind == "base" else (3, 3, 3))

def calculator(model):
    if model == "mattersim":
        from mattersim.forcefield import MatterSimCalculator
        return MatterSimCalculator(load_path="MatterSim-v1.0.0-5M.pth", device="cpu", dtype="float64")
    if model == "mace":
        from mace.calculators import mace_mp
        return mace_mp(model="medium", default_dtype="float64", device="cpu")
    raise KeyError(model)

def relax_full(atoms, calc):
    a = atoms.copy(); a.calc = calc; a.set_constraint(FixSymmetry(a))
    conv = BFGS(FrechetCellFilter(a), logfile=None).run(fmax=FMAX, steps=3000)
    a.set_constraint(); return a, bool(conv)

def relax_pos(atoms, calc):
    a = atoms.copy(); a.calc = calc; a.set_constraint(FixSymmetry(a))
    conv = BFGS(a, logfile=None).run(fmax=FMAX, steps=1000)
    a.set_constraint(); return a, bool(conv)

def phonons(a, calc, n, temps):
    ph = Phonopy(PhonopyAtoms(symbols=a.get_chemical_symbols(), cell=a.cell[:], scaled_positions=a.get_scaled_positions()),
                 supercell_matrix=np.diag(n), primitive_matrix="auto")
    ph.generate_displacements(distance=DISP)
    F = []
    for sc in ph.supercells_with_displacements:
        at = Atoms(sc.symbols, cell=sc.cell, scaled_positions=sc.scaled_positions, pbc=True); at.calc = calc
        f = np.array(at.get_forces(), dtype=np.float64); f -= f.mean(axis=0); F.append(f)
    ph.forces = np.array(F); ph.produce_force_constants(); ph.symmetrize_force_constants()
    ph.run_mesh(MESH, is_gamma_center=True)
    fmin = float(ph.get_mesh_dict()["frequencies"].min())
    gam = np.sort(ph.get_frequencies([0, 0, 0]))
    ph.run_thermal_properties(temperatures=list(temps) + [3000.0], exclude_gamma_acoustic=True)
    tp = ph.get_thermal_properties_dict(); npr = len(ph.primitive)
    return {"fmin_THz": fmin, "gamma_THz": gam.tolist(), "S_raw": tp["entropy"][:-1], "Cv_raw": tp["heat_capacity"][:-1],
            "c3_norm": float(tp["heat_capacity"][-1] / (3 * R * npr)), "n_prim": npr, "n_disp": len(ph.supercells_with_displacements)}

def pack(p, apf):
    zp = p["n_prim"] / apf
    return {"fmin_THz": p["fmin_THz"], "c3_norm": p["c3_norm"], "S": (p["S_raw"] / zp).tolist(), "Cv": (p["Cv_raw"] / zp).tolist(),
            "gamma_THz": p["gamma_THz"], "n_disp": p["n_disp"]}

def run_material(m, calc):
    t0 = time.time(); a_in = structure(m); a0, conv = relax_full(a_in, calc)
    apf = APF.get(m, 2); nfu = len(a0) / apf
    vexp = VEXP.get(m, VEXP_OTROS.get(m)); Vexp_cell = vexp * nfu
    out = {"material": m, "relax_converged": conv, "cell_par_V0": [float(x) for x in a0.cell.cellpar()],
           "V0_sobre_Vexp": float(a0.get_volume() / Vexp_cell), "n_atoms_celda": len(a0)}
    out["arm_V0"] = pack(phonons(a0, calc, supercell(m, "base"), T_EVAL), apf)
    a = a0.copy(); a.set_cell(a0.cell[:] * (Vexp_cell / a0.get_volume()) ** (1 / 3), scale_atoms=True)
    a, rc = relax_pos(a, calc); out["relax_pos_Vexp_converged"] = rc
    out["V_celda_sobre_Vexp"] = float(a.get_volume() / Vexp_cell)
    out["arm_Vexp"] = pack(phonons(a, calc, supercell(m, "base"), T_EVAL), apf)
    if m in MATS: out["arm_Vexp_grande"] = pack(phonons(a, calc, supercell(m, "grande"), T_EVAL), apf)
    out["t_s"] = time.time() - t0
    return out

def rnd(x):
    if isinstance(x, dict): return {k: rnd(v) for k, v in x.items() if k != "t_s"}
    if isinstance(x, (list, tuple)): return [rnd(v) for v in x]
    if isinstance(x, (float, np.floating)): return float("%.10g" % x)
    if isinstance(x, (np.integer,)): return int(x)
    return x

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--model", required=True); ap.add_argument("--out", required=True); ap.add_argument("--mats", default=",".join(MATS + CONTROL))
    A = ap.parse_args(); calc = calculator(A.model); d = os.path.join(A.out, A.model); os.makedirs(d, exist_ok=True)
    for m in A.mats.split(","):
        f = os.path.join(d, m + ".json")
        if os.path.exists(f): print(A.model, m, "salto (existe)", flush=True); continue
        r = run_material(m, calc); t = r["t_s"]
        json.dump(rnd(r), open(f + ".tmp", "w"), indent=1, sort_keys=True); os.replace(f + ".tmp", f)
        print(A.model, m, "V0/Vexp=%.4f fmin_Vexp=%.3f S298_Vexp=%.4f t=%.0fs" % (r["V0_sobre_Vexp"], r["arm_Vexp"]["fmin_THz"], r["arm_Vexp"]["S"][2], t), flush=True)
