#!/usr/bin/env python3
"""C-MAT-005, prueba de artefacto: fonones DFT (GPAW, ondas planas) de rutilo y cuarzo-α en la celda experimental.
Uso: gpaw -P 4 python cmat005_dft.py --mat {TiO2,SiO2,Si_humo} --xc {PBE,LDA} [--etapa {relax,gamma650,super}]
Reanudable: cada cálculo de fuerzas se guarda en out/dft/<mat>_<xc>/.
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os
import numpy as np
from ase import Atoms
from ase.io import read
from ase.build import bulk
from ase.constraints import FixSymmetry
from ase.optimize import BFGS
from ase.parallel import world, parprint
from gpaw import GPAW, PW, FermiDirac

HERE = os.path.dirname(os.path.abspath(__file__)); REFS = os.path.join(HERE, "..", "refs", "cif")
ECUT = 500.0; ECUT_TEST = 650.0; DISP = 0.01; FMAX = 2e-3
K_PRIM = {"TiO2": (4, 4, 6), "SiO2": (3, 3, 3), "Si_humo": (4, 4, 4)}
SC = {"TiO2": (2, 2, 1), "SiO2": (2, 2, 1), "Si_humo": (1, 1, 1)}

def structure(m):
    if m == "TiO2": return read(os.path.join(REFS, "cod_9007531.cif"))
    if m == "SiO2": return read(os.path.join(REFS, "cod_9013321.cif"))
    if m == "Si_humo": return bulk("Si", "diamond", a=5.431)
    raise KeyError(m)

def calc(xc, kpts, ecut, txt):
    return GPAW(mode=PW(ecut), xc=xc, kpts={"size": kpts, "gamma": True}, occupations=FermiDirac(0.01),
                convergence={"density": 1e-6, "forces": 1e-4}, symmetry={"point_group": True, "time_reversal": True}, txt=txt)

def save(path, obj):
    if world.rank == 0:
        json.dump(obj, open(path + ".tmp", "w"), indent=1); os.replace(path + ".tmp", path)
    world.barrier()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mat", required=True); ap.add_argument("--xc", required=True)
    ap.add_argument("--etapa", default="relax"); A = ap.parse_args()
    d = os.path.join(HERE, "..", "out", "dft", f"{A.mat}_{A.xc}"); os.makedirs(d, exist_ok=True)
    fr = os.path.join(d, "relax.json")
    if A.etapa == "relax":
        if os.path.exists(fr): parprint("relax ya hecho"); return
        a = structure(A.mat); a.calc = calc(A.xc, K_PRIM[A.mat], ECUT, os.path.join(d, "relax.txt")); a.set_constraint(FixSymmetry(a))
        conv = BFGS(a, logfile=os.path.join(d, "relax_bfgs.log") if world.rank == 0 else None).run(fmax=FMAX, steps=200)
        fmax = float(np.abs(a.get_forces()).max()); a.set_constraint()
        save(fr, {"cell": a.cell[:].tolist(), "symbols": a.get_chemical_symbols(), "scaled_positions": a.get_scaled_positions().tolist(),
                  "converged": bool(conv), "fmax_eV_A": fmax, "energy_eV": float(a.get_potential_energy()), "ecut": ECUT, "kpts": K_PRIM[A.mat]})
        parprint("relax OK", conv, fmax); return
    r = json.load(open(fr)); a0 = Atoms(r["symbols"], cell=r["cell"], scaled_positions=r["scaled_positions"], pbc=True)
    from phonopy import Phonopy
    from phonopy.structure.atoms import PhonopyAtoms
    if A.etapa == "gamma650":           # control C-DFT: fuerzas en Γ (celda primitiva) a 500 y 650 eV
        n = (1, 1, 1); stages = [(ECUT, "g500"), (ECUT_TEST, "g650")]; kp = K_PRIM[A.mat]
    else:
        n = SC[A.mat]; stages = [(ECUT, "sc")]; kp = tuple(int(np.ceil(k / s)) for k, s in zip(K_PRIM[A.mat], n))
    ph = Phonopy(PhonopyAtoms(symbols=a0.get_chemical_symbols(), cell=a0.cell[:], scaled_positions=a0.get_scaled_positions()),
                 supercell_matrix=np.diag(n), primitive_matrix="auto")
    ph.generate_displacements(distance=DISP); scs = ph.supercells_with_displacements
    for ecut, tag in stages:
        F = []
        for i, sc in enumerate(scs):
            fi = os.path.join(d, f"{tag}_disp{i:03d}.json")
            if not os.path.exists(fi):
                at = Atoms(sc.symbols, cell=sc.cell, scaled_positions=sc.scaled_positions, pbc=True)
                at.calc = calc(A.xc, kp, ecut, os.path.join(d, f"{tag}_disp{i:03d}.txt"))
                save(fi, {"forces": at.get_forces().tolist(), "ecut": ecut, "kpts": kp, "n": n})
            f = np.array(json.load(open(fi))["forces"]); f -= f.mean(axis=0); F.append(f)
        ph.forces = np.array(F); ph.produce_force_constants(); ph.symmetrize_force_constants()
        from phonopy.harmonic.dynmat_to_fc import get_commensurate_points
        qs = get_commensurate_points(ph.supercell_matrix)
        fq = {",".join("%.3f" % x for x in q): np.sort(ph.get_frequencies(q)).tolist() for q in qs}
        ph.run_mesh(30.0, is_gamma_center=True); fmesh = float(ph.get_mesh_dict()["frequencies"].min())
        save(os.path.join(d, f"{tag}_result.json"), {"supercell": n, "kpts": kp, "ecut": ecut, "n_disp": len(scs), "freq_commensurate_THz": fq,
             "fmin_commensurate_THz": float(min(min(v) for v in fq.values())), "fmin_mesh_interp_THz": fmesh, "relax": {k: r[k] for k in ("converged", "fmax_eV_A")}})
        parprint(tag, "fmin_comm", min(min(v) for v in fq.values()))

if __name__ == "__main__":
    main()
