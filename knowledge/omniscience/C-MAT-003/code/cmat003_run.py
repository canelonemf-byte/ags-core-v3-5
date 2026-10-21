#!/usr/bin/env python3
"""C-MAT-003 (prereg sha256 2d9a1256…fc96). Fonones armónicos + QHA (Phonopy) con un potencial universal.
Uso: python cmat003_run.py --model {mattersim,sevenn,mace} --out DIR [--mats Si,MgO,...]
Guarda un JSON por material en DIR/<model>/<mat>.json y se salta los que ya existen (reanudable).
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
import torch
torch.set_num_threads(4); torch.manual_seed(0); np.random.seed(0)
from ase import Atoms
from ase.build import bulk
from ase.spacegroup import crystal
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
from phonopy import Phonopy, PhonopyQHA
from phonopy.structure.atoms import PhonopyAtoms

R = 8.314462618; FMAX = 1e-3; DISP = 0.01; MESH = 60.0; STAB = -0.3
T_EVAL = [100.0, 200.0, 298.15, 600.0]
T_GRID = np.arange(0.0, 901.0, 1.0)
VFAC = [round(0.96 + 0.02 * i, 2) for i in range(10)]          # 0.96 … 1.14
MATS = ["Si", "MgO", "NaCl", "LiF", "NaF", "KCl", "KBr", "CaO", "CaF2", "Al2O3", "BeO"]
APF = {"Si": 1, "CaF2": 3, "Al2O3": 5}                           # átomos por fórmula (resto: 2)
SC = {"base": {"cub": (2, 2, 2), "Al2O3": (2, 2, 2), "BeO": (3, 3, 2)},
      "grande": {"cub": (3, 3, 3), "Al2O3": (3, 3, 3), "BeO": (4, 4, 3)}}

def structure(m):
    rs = {"MgO": 4.212, "NaCl": 5.640, "LiF": 4.027, "NaF": 4.634, "KCl": 6.293, "KBr": 6.600, "CaO": 4.811}
    if m == "Si": return bulk("Si", "diamond", a=5.431, cubic=True)
    if m == "Ge": return bulk("Ge", "diamond", a=5.658, cubic=True)      # solo prueba de humo (fuera del estudio)
    if m == "Cu": return bulk("Cu", "fcc", a=3.615, cubic=True)          # solo prueba de humo (fuera del estudio)
    if m in rs: return bulk(m, "rocksalt", a=rs[m], cubic=True)
    if m == "CaF2": return bulk("CaF2", "fluorite", a=5.463, cubic=True)
    if m == "BeO": return bulk("BeO", "wurtzite", a=2.698, c=4.380, u=0.378)
    if m == "Al2O3": return crystal(["Al", "O"], basis=[(0, 0, 0.3522), (0.3064, 0, 0.25)], spacegroup=167,
                                    cellpar=[4.759, 4.759, 12.991, 90, 90, 120], primitive_cell=True)
    raise KeyError(m)

def supercell(m, kind):
    return SC[kind]["Al2O3" if m == "Al2O3" else "BeO" if m == "BeO" else "cub"]

def calculator(model):
    if model == "mattersim":
        from mattersim.forcefield import MatterSimCalculator
        return MatterSimCalculator(load_path="MatterSim-v1.0.0-5M.pth", device="cpu")
    if model == "sevenn":
        from sevenn.calculator import SevenNetCalculator
        return SevenNetCalculator(model="7net-0", device="cpu")
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
    e = float(a.get_potential_energy()); a.set_constraint(); return a, e, bool(conv)

def phonons(a, calc, n, temps):
    ph = Phonopy(PhonopyAtoms(symbols=a.get_chemical_symbols(), cell=a.cell[:], scaled_positions=a.get_scaled_positions()),
                 supercell_matrix=np.diag(n), primitive_matrix="auto")
    ph.generate_displacements(distance=DISP)
    F = []
    for sc in ph.supercells_with_displacements:
        at = Atoms(sc.symbols, cell=sc.cell, scaled_positions=sc.scaled_positions, pbc=True); at.calc = calc
        f = np.array(at.get_forces(), dtype=float); f -= f.mean(axis=0); F.append(f)
    ph.forces = np.array(F); ph.produce_force_constants(); ph.symmetrize_force_constants()
    ph.run_mesh(MESH, is_gamma_center=True)
    fmin = float(ph.get_mesh_dict()["frequencies"].min())
    gam = np.sort(ph.get_frequencies([0, 0, 0]))
    ph.run_thermal_properties(temperatures=temps, exclude_gamma_acoustic=True)
    tp = ph.get_thermal_properties_dict()
    return ph, fmin, gam, tp, len(ph.primitive), len(ph.supercells_with_displacements)

def run_material(m, calc):
    t0 = time.time(); s0 = structure(m); a0, conv = relax_full(s0, calc)
    apf = APF.get(m, 2); nin = len(a0)
    out = {"material": m, "relax_converged": conv, "cell_par_V0": [float(x) for x in a0.cell.cellpar()],
           "V0_A3_por_atomo": float(a0.get_volume() / nin)}
    # armónico en V0, superceldas base y grande
    for kind in ("base", "grande"):
        ph, fmin, gam, tp, npr, nd = phonons(a0, calc, supercell(m, kind), T_EVAL + [3000.0])
        zp = npr / apf
        out[f"arm_{kind}"] = {"fmin_THz": fmin, "n_desplaz": nd, "n_at_prim": npr,
                               "c3_norm": float(tp["heat_capacity"][-1] / (3 * R * npr)),
                               "S": (tp["entropy"][:-1] / zp).tolist(), "Cv": (tp["heat_capacity"][:-1] / zp).tolist()}
        if kind == "base": out["gamma_THz"] = gam.tolist()
    # QHA
    vols, ens, fe, cv, en, fmins, rconv = [], [], [], [], [], [], []
    cell0 = a0.cell[:].copy()
    for f in VFAC:
        a = a0.copy(); a.set_cell(cell0 * f ** (1 / 3), scale_atoms=True)
        a, e, rc = relax_pos(a, calc)
        ph, fmin, _, tp, npr, _ = phonons(a, calc, supercell(m, "base"), T_GRID)
        k = npr / nin
        vols.append(a.get_volume() * k); ens.append(e * k); fmins.append(fmin); rconv.append(rc)
        fe.append(tp["free_energy"]); cv.append(tp["heat_capacity"]); en.append(tp["entropy"])
    out["qha_input"] = {"vfac": VFAC, "fmin_THz": fmins, "relax_pos_converged": rconv}
    stable = [x >= STAB for x in fmins]; i0 = VFAC.index(1.0)
    lo = i0; hi = i0
    while lo - 1 >= 0 and stable[lo - 1]: lo -= 1
    while hi + 1 < len(VFAC) and stable[hi + 1]: hi += 1
    ok_contig = all(stable[lo:hi + 1]) and stable[i0]
    excl_only_ends = (not any(stable[:lo])) and (not any(stable[hi + 1:]))   # solo se excluyen inestables de los extremos
    use = list(range(lo, hi + 1))
    q = {"usados": [VFAC[i] for i in use], "evaluable": bool(ok_contig and excl_only_ends and len(use) >= 6)}
    if q["evaluable"]:
        zp = npr / apf
        V = np.array(vols)[use]; E = np.array(ens)[use]
        FE = np.array(fe)[use].T; CV = np.array(cv)[use].T; EN = np.array(en)[use].T
        qha = PhonopyQHA(volumes=V, electronic_energies=E, temperatures=T_GRID, free_energy=FE, cv=CV, entropy=EN, eos="vinet", t_max=float(T_GRID[-1]) - 10)
        vt = np.array(qha.volume_temperature); cp = np.array(qha.heat_capacity_P_numerical)
        nt = min(len(vt), len(cp)); Tq = T_GRID[:nt]
        S_T = np.array([np.polyval(np.polyfit(V, EN[i], 3), vt[i]) for i in range(nt)])
        try: S_ph = np.array(qha.entropy_temperature)[:nt]
        except Exception: S_ph = np.full(nt, np.nan)
        def at(arr, T): return float(np.interp(T, Tq, arr))
        V0p = float(np.array(vols)[i0])
        q.update({"T_max_K": float(Tq[-1]),
                  "S": [at(S_T, T) / zp if T <= Tq[-1] else None for T in T_EVAL],
                  "S_phonopy": [at(S_ph, T) / zp if T <= Tq[-1] else None for T in T_EVAL],
                  "Cp": [at(cp, T) / zp if T <= Tq[-1] else None for T in T_EVAL],
                  "V_sobre_V0": [at(vt, T) / V0p if T <= Tq[-1] else None for T in T_EVAL],
                  "alfa_V_298_1e6K": float(np.interp(298.15, Tq[:len(qha.thermal_expansion)], np.array(qha.thermal_expansion)) * 1e6),
                  "horquilla_600": bool(600.0 <= Tq[-1] and V.min() < at(vt, 600.0) < V.max())})
    out["qha"] = q; out["t_s"] = time.time() - t0
    return out

def rnd(x):
    if isinstance(x, (float, np.floating)): return float(f"{float(x):.8g}")
    if isinstance(x, (list, tuple)): return [rnd(v) for v in x]
    if isinstance(x, dict): return {k: rnd(v) for k, v in x.items()}
    return x

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--model", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--mats", default=",".join(MATS)); A = ap.parse_args()
    d = os.path.join(A.out, A.model); os.makedirs(d, exist_ok=True); calc = calculator(A.model)
    for m in A.mats.split(","):
        p = os.path.join(d, f"{m}.json")
        if os.path.exists(p): print("salto", m, flush=True); continue
        r = run_material(m, calc); t = r.pop("t_s")
        json.dump(rnd(r), open(p + ".tmp", "w"), indent=1, sort_keys=True); os.replace(p + ".tmp", p)
        print(A.model, m, "S298 arm=%.3f qha=%s t=%.0fs" % (r["arm_base"]["S"][2], r["qha"].get("S", [None]*3)[2], t), flush=True)

if __name__ == "__main__": main()
