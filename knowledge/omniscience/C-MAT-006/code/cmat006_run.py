#!/usr/bin/env python3
"""C-MAT-006: fonones armónicos en V_exp con regla de modos blandos fijada (R0–R4), 31 sólidos, y rutilo/cuarzo en la celda DFT.
Uso: python cmat006_run.py --model {mattersim,mace} --out DIR [--mats ...]   (un JSON por material; reanudable)
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
import torch
torch.set_num_threads(4); torch.manual_seed(0); np.random.seed(0); torch.use_deterministic_algorithms(True)
from ase import Atoms
from ase.constraints import FixSymmetry
from ase.optimize import BFGS
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
STORE = "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience"
sys.path.insert(0, f"{STORE}/C-MAT-004/code"); import cmat004_run as c4
sys.path.insert(0, f"{STORE}/C-MAT-005/code"); import cmat005_run as c5
HERE = os.path.dirname(os.path.abspath(__file__))
M4 = ["Si", "MgO", "NaCl", "LiF", "NaF", "KCl", "KBr", "CaO", "CaF2", "Al2O3", "BeO", "SrO", "MgF2", "TiO2", "SiO2", "Li2O", "MgAl2O4"]
M5 = list(c5.MATS); MATS = M4 + M5
T = np.array([298.15, 600.0]); NU_IMAG = -0.05; NU_CUT = 0.05; F_MAX_REGLA = 0.02
KB = 8.617333262e-5; H = 4.135667696e-15; R = 8.314462618   # eV/K, eV·s, J/(mol·K)

def mod(m): return c4 if m in M4 else c5
def vexp(m): return c4.VEXP[m] if m in M4 else c5.VEXP[m]
def apf(m): return (c4.APF if m in M4 else c5.APF).get(m, 2)

def s_modos(nu_THz, wt, temps):
    out = []
    for t in temps:
        x = H * nu_THz * 1e12 / (KB * t)
        s = x / np.expm1(x) - np.log1p(-np.exp(-x))
        out.append(float(R * (wt * s).sum()))
    return np.array(out)

def fonones(a, calc, n):
    ph = Phonopy(PhonopyAtoms(symbols=a.get_chemical_symbols(), cell=a.cell[:], scaled_positions=a.get_scaled_positions()),
                 supercell_matrix=np.diag(n), primitive_matrix="auto")
    ph.generate_displacements(distance=c5.DISP); F = []
    for sc in ph.supercells_with_displacements:
        at = Atoms(sc.symbols, cell=sc.cell, scaled_positions=sc.scaled_positions, pbc=True); at.calc = calc
        f = np.array(at.get_forces(), dtype=np.float64); f -= f.mean(axis=0); F.append(f)
    ph.forces = np.array(F); ph.produce_force_constants(); ph.symmetrize_force_constants(); return ph

def regla(ph):
    ph.run_mesh(c5.MESH, is_gamma_center=True); md = ph.get_mesh_dict()
    q = md["qpoints"]; w = md["weights"].astype(float); f = md["frequencies"]
    nq = w.sum(); W = np.repeat(w[:, None], f.shape[1], axis=1) / nq          # peso por modo (suma = 3N)
    acu = np.zeros_like(f, bool); ig = int(np.where(np.all(np.abs(q) < 1e-9, axis=1))[0][0])
    acu[ig, np.argsort(np.abs(f[ig]))[:3]] = True                               # R0: 3 acústicos de Γ fuera
    imag = (f < NU_IMAG) & ~acu; real = (f > NU_CUT) & ~acu
    tot = W[~acu].sum(); f_imag = float(W[imag].sum() / tot)
    S_real = s_modos(f[real], W[real], T)
    if f_imag == 0: clase, S = "normal", S_real
    elif f_imag <= F_MAX_REGLA: clase, S = "evaluable_con_regla", S_real / (1 - f_imag)
    else: clase, S = "no_evaluable", S_real / (1 - f_imag)
    ph.run_thermal_properties(temperatures=list(T), cutoff_frequency=NU_CUT)
    S_ph = ph.get_thermal_properties_dict()["entropy"]
    return {"f_imag": f_imag, "clase": clase, "fmin_THz": float(f.min()), "S_prim": S.tolist(), "S_phonopy_prim": [float(x) for x in S_ph],
            "n_prim": len(ph.primitive)}

def run_material(m, calc):
    M = mod(m); t0 = time.time(); a0, conv = c5.relax_full(M.structure(m), calc)
    nfu = len(a0) / apf(m); Vc = vexp(m) * nfu
    a = a0.copy(); a.set_cell(a0.cell[:] * (Vc / a0.get_volume()) ** (1 / 3), scale_atoms=True); a, rc = c5.relax_pos(a, calc)
    ph = fonones(a, calc, M.supercell(m, "base")); r = regla(ph); zp = r["n_prim"] / apf(m)
    r.update({"material": m, "relax_ok": conv, "relax_pos_ok": rc, "V_sobre_Vexp": float(a.get_volume() / Vc), "supercelda": list(M.supercell(m, "base")),
              "S_form": [s / zp for s in r["S_prim"]], "S_phonopy_form": [s / zp for s in r["S_phonopy_prim"]], "t_s": round(time.time() - t0, 1)})
    return r

def run_celda_dft(m, calc):
    """Rutilo/cuarzo en la celda experimental del CIF (igual que la DFT), posiciones relajadas por el uMLIP; q conmensurados."""
    sys.path.insert(0, HERE); import importlib; from phonopy.harmonic.dynmat_to_fc import get_commensurate_points
    from ase.io import read
    import spglib
    a = read(os.path.join(HERE, "..", "refs", "cif", {"TiO2": "cod_9007531.cif", "SiO2": "cod_9013321.cif"}[m]))
    c, p, z = spglib.standardize_cell((a.cell[:], a.get_scaled_positions(), a.numbers), to_primitive=True, symprec=1e-3)
    a = Atoms(numbers=z, cell=c, scaled_positions=p, pbc=True); a.calc = calc; a.set_constraint(FixSymmetry(a, symprec=1e-3))
    BFGS(a, logfile=None).run(fmax=2e-3, steps=500); a.set_constraint()
    n = {"TiO2": (2, 2, 2), "SiO2": (2, 2, 1)}[m]; ph = fonones(a, calc, n)
    qs = get_commensurate_points(ph.supercell_matrix)
    fq = {",".join("%.3f" % x for x in q): np.sort(ph.get_frequencies(q)).tolist() for q in qs}
    return {"material": m, "supercelda": n, "freq_commensurate_THz": fq, "fmin_commensurate_THz": float(min(min(v) for v in fq.values()))}

def rnd(x):
    if isinstance(x, dict): return {k: rnd(v) for k, v in x.items() if k != "t_s"}
    if isinstance(x, (list, tuple)): return [rnd(v) for v in x]
    if isinstance(x, (float, np.floating)): return float("%.10g" % x)
    if isinstance(x, np.integer): return int(x)
    return x

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--model", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--mats", default=",".join(MATS + ["DFT_TiO2", "DFT_SiO2"])); A = ap.parse_args()
    calc = c5.calculator(A.model); d = os.path.join(A.out, A.model); os.makedirs(d, exist_ok=True)
    for m in A.mats.split(","):
        f = os.path.join(d, m + ".json")
        if os.path.exists(f): continue
        r = run_celda_dft(m[4:], calc) if m.startswith("DFT_") else run_material(m, calc)
        json.dump(rnd(r), open(f + ".tmp", "w"), indent=1, sort_keys=True); os.replace(f + ".tmp", f)
        print(A.model, m, r.get("clase", ""), r.get("f_imag", ""), r.get("fmin_commensurate_THz", ""), (r.get("S_form") or [0])[0], flush=True)
    print("FIN", A.model, flush=True)
