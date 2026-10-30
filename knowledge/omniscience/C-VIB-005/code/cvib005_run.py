#!/usr/bin/env python3
"""C-VIB-005 (derivado de C-VIB-004): κL(300 K) RTA con phono3py + MatterSim-v1 en sales de roca, a la constante de red experimental de 300 K (a_exp) en lugar de la relajada.
Uso: python cvib004_run.py --out DIR --mats ... [--aexp] [--sc 2] [--mesh 19] [--disp 0.03] [--threads 4]
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963).
Código original; reutiliza la receta de C-VIB-003 (cvib003_run.py): misma relajación, fc3 compacta simetrizada, malla Γ, isótopos, RTA."""
import argparse, json, os, time, warnings, re, resource
import numpy as np
warnings.filterwarnings("ignore")
p = argparse.ArgumentParser(); p.add_argument("--out", required=True); p.add_argument("--mats", nargs="+", required=True)
p.add_argument("--aexp", action="store_true"); p.add_argument("--scale", type=float, default=1.0); p.add_argument("--sc", type=int, default=2); p.add_argument("--mesh", type=int, default=19)
p.add_argument("--disp", type=float, default=0.03); p.add_argument("--threads", type=int, default=4)
a = p.parse_args()
import torch
torch.set_num_threads(a.threads); torch.manual_seed(0); np.random.seed(0)
from ase.build import bulk
from ase.data import covalent_radii, atomic_numbers
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
from ase import Atoms
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from phono3py import Phono3py
# Constantes de red experimentales a ~300 K (Å). Fuentes en prereg_C-VIB-004.md
AEXP = {"MgO":4.212,"CaO":4.81,"SrO":5.16,"BaO":5.520,"LiF":4.03,"NaF":4.63,"NaCl":5.64,"NaBr":5.97,"NaI":6.47,"KF":5.34,"KCl":6.29,
        "KBr":6.60,"KI":7.07,"RbCl":6.59,"PbS":5.9362,"PbSe":6.1273,"PbTe":6.4620}
def split(m): return re.findall(r"[A-Z][a-z]?", m)
def relax(m, calc):
    A, B = split(m); r = covalent_radii[atomic_numbers[A]] + covalent_radii[atomic_numbers[B]]; a0 = 2*r
    at = bulk(m, "rocksalt", a=a0, cubic=True); at.calc = calc; at.set_constraint(FixSymmetry(at))
    BFGS(FrechetCellFilter(at), logfile=None).run(fmax=1e-3, steps=500)
    at.set_constraint(); return at, a0
def main():
    from mattersim.forcefield import MatterSimCalculator
    calc = MatterSimCalculator(load_path="MatterSim-v1.0.0-5M.pth", device="cpu", dtype="float64")
    os.makedirs(a.out, exist_ok=True); tag = (f"aexp{a.scale:.3f}" if a.aexp else "arel")
    for m in a.mats:
        fn = f"{a.out}/mattersim_{m}_{tag}_sc{a.sc}_m{a.mesh}_d{a.disp:.3f}.json"
        if os.path.exists(fn): continue
        t0 = time.time()
        if a.aexp:
            at = bulk(m, "rocksalt", a=AEXP[m]*a.scale, cubic=True); a0 = AEXP[m]*a.scale   # posiciones fijadas por simetría en Fm-3m
        else:
            at, a0 = relax(m, calc)
        at.calc = calc; stress = (at.get_stress(voigt=True)[:3].mean()*-160.21766208)  # presión en GPa (positiva = compresión)
        uc = PhonopyAtoms(symbols=at.get_chemical_symbols(), cell=at.cell[:], scaled_positions=at.get_scaled_positions())
        S = np.diag([a.sc]*3)
        ph3 = Phono3py(uc, supercell_matrix=S, primitive_matrix="auto", log_level=0)
        ph3.generate_displacements(distance=a.disp); F = []
        for sc in ph3.supercells_with_displacements:
            s = Atoms(sc.symbols, cell=sc.cell, scaled_positions=sc.scaled_positions, pbc=True); s.calc = calc
            f = np.array(s.get_forces(), dtype=np.float64); f -= f.mean(axis=0); F.append(f)
        t_f = time.time()-t0
        ph3.forces = np.array(F); ph3.produce_fc3(symmetrize_fc3r=True, is_compact_fc=True)
        ph = Phonopy(uc, supercell_matrix=S, primitive_matrix="auto"); ph.force_constants = ph3.fc2
        ph.run_mesh([a.mesh]*3, is_gamma_center=True); md = ph.get_mesh_dict(); f = md["frequencies"]; q = md["qpoints"]
        ig = int(np.where(np.all(np.abs(q) < 1e-9, axis=1))[0][0]); mask = np.ones_like(f, bool); mask[ig, np.argsort(np.abs(f[ig]))[:3]] = False
        fmin = float(f[mask].min())
        ph3.mesh_numbers = [a.mesh]*3; ph3.init_phph_interaction()
        ph3.run_thermal_conductivity(temperatures=[300.0], is_isotope=True)
        k = np.array(ph3.thermal_conductivity.kappa)[0, 0]
        res = {"material": m, "model": "mattersim", "red": tag, "sc": a.sc, "mesh": a.mesh, "disp": a.disp, "a0_inicial": float(a0),
               "a_usada": float(at.cell[0,0]), "presion_GPa": float(stress), "n_disp": len(F), "fmin_THz": fmin,
               "kappa_rta_xyz": k.tolist(), "kappa_rta": float(k[:3].mean()), "t_fuerzas_s": t_f, "t_s": time.time()-t0,
               "maxrss_MB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024}
        json.dump(res, open(fn, "w"), indent=1)
        print(m, tag, round(res["a_usada"], 4), round(res["presion_GPa"], 3), round(res["kappa_rta"], 3), round(fmin, 3), len(F), round(res["t_s"]), round(res["maxrss_MB"]), flush=True)
if __name__ == "__main__": main()
