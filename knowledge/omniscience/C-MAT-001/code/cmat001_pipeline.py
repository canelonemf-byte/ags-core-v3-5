#!/usr/bin/env python3
"""C-MAT-001 pipeline (pre-registro congelado sha256 efb5f872…ea90).
MACE-MP-0 medium (float64, CPU) + ASE (relajación con FixSymmetry + FrechetCellFilter) + Phonopy (desplazamientos finitos).
Uso: python cmat001_pipeline.py --out out [--only Si,C]
"""
import argparse, json, os, sys, time, hashlib
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from ase import Atoms
from ase.build import bulk
from ase.spacegroup import crystal
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
from ase.io import write
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from mace.calculators import mace_mp

THZ_PER_CM = 0.0299792458
STAB_TOL_THZ = -0.3       # §4 H-MAT-1
FMAX = 1e-3               # §5.2
MESH = [20, 20, 20]       # §5.3
CONFIGS = [("base_2x2x2_d0.01", 2, 0.01), ("sc_3x3x3_d0.01", 3, 0.01), ("disp_2x2x2_d0.03", 2, 0.03)]
# Referencias verificadas (§8.1); None = no evaluable
REF_CM = {"Si": 520.2, "C": 1332.0, "GaAs": 269.0, "MgO": 396.0, "NaCl": None, "PbTe": 18.0}
REF_SECONDARY_CM = {"NaCl": 164.0}
EXPECT_STABLE = {"Si": True, "C": True, "GaAs": True, "MgO": True, "NaCl": True, "PbTe": True, "SnSe": True, "SrTiO3": False, "BaTiO3": False}

def perovskite(A, B, a):
    return Atoms([A, B, "O", "O", "O"], scaled_positions=[(0,0,0),(.5,.5,.5),(.5,.5,0),(.5,0,.5),(0,.5,.5)], cell=[a,a,a], pbc=True)

def structures():
    return {
     "Si": bulk("Si", "diamond", a=5.431, cubic=True),
     "C": bulk("C", "diamond", a=3.567, cubic=True),
     "GaAs": bulk("GaAs", "zincblende", a=5.653, cubic=True),
     "MgO": bulk("MgO", "rocksalt", a=4.212, cubic=True),
     "NaCl": bulk("NaCl", "rocksalt", a=5.640, cubic=True),
     "PbTe": bulk("PbTe", "rocksalt", a=6.462, cubic=True),
     "SnSe": crystal(["Sn", "Se"], basis=[(0.1185, 0.25, 0.1026), (0.8553, 0.25, 0.4814)], spacegroup=62,
                     cellpar=[11.501, 4.153, 4.445, 90, 90, 90]),
     "SrTiO3": perovskite("Sr", "Ti", 3.905),
     "BaTiO3": perovskite("Ba", "Ti", 4.006),
    }

def relax(atoms, calc, log):
    a = atoms.copy(); a.calc = calc
    a.set_constraint(FixSymmetry(a))
    opt = BFGS(FrechetCellFilter(a), logfile=log)
    conv = opt.run(fmax=FMAX, steps=3000)
    f = np.abs(a.get_forces()).max(); s = a.get_stress(voigt=True)
    a.set_constraint()
    return a, bool(conv), float(f), s.tolist(), opt.get_number_of_steps()

def to_ph(a):
    return PhonopyAtoms(symbols=a.get_chemical_symbols(), cell=a.cell[:], scaled_positions=a.get_scaled_positions())

def run_phonons(a, calc, n, d):
    ph = Phonopy(to_ph(a), supercell_matrix=np.diag([n, n, n]), primitive_matrix="auto")
    ph.generate_displacements(distance=d)
    forces = []
    for sc in ph.supercells_with_displacements:
        at = Atoms(sc.symbols, cell=sc.cell, scaled_positions=sc.scaled_positions, pbc=True); at.calc = calc
        f = at.get_forces(); f -= f.mean(axis=0)  # elimina deriva neta
        forces.append(f)
    ph.forces = np.array(forces)
    ph.produce_force_constants(); ph.symmetrize_force_constants()
    ph.run_mesh(MESH, is_gamma_center=True)
    fmesh = ph.get_mesh_dict()["frequencies"]
    gam = np.sort(ph.get_frequencies([0, 0, 0]))
    return ph, float(fmesh.min()), gam, len(forces), len(ph.supercell)

def figure(ph, name, out):
    ph.auto_band_structure(npoints=81)
    bs = ph.get_band_structure_dict()
    ph.run_mesh(MESH, is_gamma_center=True); ph.run_total_dos()
    dos = ph.get_total_dos_dict()
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [3, 1]}, sharey=True)
    x0 = 0
    for dist, fr in zip(bs["distances"], bs["frequencies"]):
        ax[0].plot(dist, fr, "b-", lw=0.8)
    labels = ph.band_structure.labels if hasattr(ph, "band_structure") else None
    ax[0].axhline(0, c="k", lw=0.5); ax[0].axhline(STAB_TOL_THZ, c="r", ls=":", lw=0.8)
    ax[0].set(title=f"{name}: MACE-MP-0, 2×2×2, 0.01 Å", ylabel="frecuencia [THz]", xlabel="camino de alta simetría (seekpath)")
    ax[1].plot(dos["total_dos"], dos["frequency_points"], "k-", lw=0.8); ax[1].set(xlabel="DOS")
    fig.tight_layout(); fig.savefig(os.path.join(out, f"{name}_bandas_dos.png"), dpi=110, metadata={"Software": None}); plt.close(fig)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--only", default="")
    args = ap.parse_args(); os.makedirs(args.out, exist_ok=True)
    calc = mace_mp(model="medium", default_dtype="float64", device="cpu")
    S = structures(); names = args.only.split(",") if args.only else list(S)
    for name in names:
        t0 = time.time(); res = {"material": name}
        a, conv, fmax, stress, nsteps = relax(S[name], calc, os.path.join(args.out, f"{name}_relax.log"))
        write(os.path.join(args.out, f"{name}_relaxed.vasp"), a, format="vasp", direct=True)
        res["relax"] = {"converged": conv, "max_force_eV_A": fmax, "stress_eV_A3": stress, "steps": nsteps,
                        "cell_lengths_A": a.cell.lengths().tolist(), "cell_angles": a.cell.angles().tolist(),
                        "spacegroup_check": None}
        res["configs"] = {}
        for label, n, d in CONFIGS:
            ph, fmin, gam, ndisp, nat = run_phonons(a, calc, n, d)
            opt = gam[3:6] if len(gam) >= 6 else gam
            res["configs"][label] = {"supercell": n, "disp_A": d, "n_displacements": ndisp, "atoms_supercell": int(nat),
                                     "min_freq_mesh_THz": fmin, "stable": bool(fmin >= STAB_TOL_THZ),
                                     "gamma_freqs_THz": gam.tolist(), "gamma_optical_mean_THz": float(np.mean(opt)) if name in ["Si","C","GaAs","MgO","NaCl","PbTe"] else None}
            if label.startswith("base"):
                ph.save(os.path.join(args.out, f"{name}_phonopy_base.yaml"))
                figure(ph, name, args.out)
            print(name, label, f"fmin={fmin:.3f} THz", "Γ=", np.round(gam, 3).tolist(), flush=True)
        res["time_s"] = time.time() - t0
        json.dump(res, open(os.path.join(args.out, f"{name}.json"), "w"), indent=1)
        print(name, "done", f"{res['time_s']:.0f}s", flush=True)

if __name__ == "__main__": main()
