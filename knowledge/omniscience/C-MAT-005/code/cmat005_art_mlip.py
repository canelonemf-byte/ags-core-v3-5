#!/usr/bin/env python3
"""C-MAT-005, prueba de artefacto (lado uMLIP): rutilo y cuarzo-α en la celda experimental (misma que la DFT),
posiciones relajadas con el potencial; fonones en la supercelda de la DFT (frecuencias exactas en q conmensurados)
y en la supercelda base de C-MAT-004 (descriptivo, con el q del mínimo).
Uso: python cmat005_art_mlip.py --model {mattersim,mace} --out DIR
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cmat005_run import calculator, rnd, DISP, FMAX
from ase import Atoms
from ase.io import read
from ase.constraints import FixSymmetry
from ase.optimize import BFGS
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from phonopy.harmonic.dynmat_to_fc import get_commensurate_points
REFS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "refs", "cif")
CIF = {"TiO2": "cod_9007531.cif", "SiO2": "cod_9013321.cif"}
SC_DFT = {"TiO2": (2, 2, 1), "SiO2": (2, 2, 1), "Si_humo": (1, 1, 1)}; SC_C4 = {"TiO2": (2, 2, 3), "SiO2": (2, 2, 2), "Si_humo": (2, 2, 2)}

def ph_run(a, calc, n):
    ph = Phonopy(PhonopyAtoms(symbols=a.get_chemical_symbols(), cell=a.cell[:], scaled_positions=a.get_scaled_positions()),
                 supercell_matrix=np.diag(n), primitive_matrix="auto")
    ph.generate_displacements(distance=DISP); F = []
    for sc in ph.supercells_with_displacements:
        at = Atoms(sc.symbols, cell=sc.cell, scaled_positions=sc.scaled_positions, pbc=True); at.calc = calc
        f = np.array(at.get_forces(), dtype=np.float64); f -= f.mean(axis=0); F.append(f)
    ph.forces = np.array(F); ph.produce_force_constants(); ph.symmetrize_force_constants()
    qs = get_commensurate_points(ph.supercell_matrix)
    fq = {",".join("%.3f" % x for x in q): np.sort(ph.get_frequencies(q)).tolist() for q in qs}
    ph.run_mesh(30.0, is_gamma_center=True); md = ph.get_mesh_dict(); i = int(np.argmin(md["frequencies"].min(axis=1)))
    return {"supercell": list(n), "n_disp": len(ph.supercells_with_displacements), "freq_commensurate_THz": fq,
            "fmin_commensurate_THz": float(min(min(v) for v in fq.values())), "fmin_mesh_interp_THz": float(md["frequencies"].min()),
            "q_fmin_mesh": md["qpoints"][i].tolist()}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--model", required=True); ap.add_argument("--out", required=True); ap.add_argument("--mats", default="TiO2,SiO2"); A = ap.parse_args()
    calc = calculator(A.model); d = os.path.join(A.out, "artefacto", A.model); os.makedirs(d, exist_ok=True)
    for m in A.mats.split(","):
        f = os.path.join(d, m + ".json")
        if os.path.exists(f): print(A.model, m, "salto (existe)", flush=True); continue
        if m == "Si_humo":
            from ase.build import bulk; a = bulk("Si", "diamond", a=5.431)
        else: a = read(os.path.join(REFS, CIF[m]))
        a.calc = calc; a.set_constraint(FixSymmetry(a))
        conv = BFGS(a, logfile=None).run(fmax=FMAX, steps=1000); a.set_constraint()
        r = {"material": m, "relax_pos_converged": bool(conv), "scaled_positions": a.get_scaled_positions().tolist(),
             "sc_dft": ph_run(a, calc, SC_DFT[m]), "sc_c4": ph_run(a, calc, SC_C4[m])}
        json.dump(rnd(r), open(f + ".tmp", "w"), indent=1, sort_keys=True); os.replace(f + ".tmp", f)
        print(A.model, m, "fmin_comm=%.3f fmin_mesh_c4=%.3f" % (r["sc_dft"]["fmin_commensurate_THz"], r["sc_c4"]["fmin_mesh_interp_THz"]), flush=True)
