#!/usr/bin/env python3
"""C-MAT-004: QHA con corrección empírica de presión (V_QHA(298.15 K) = V_exp) en float64.
Uso: python cmat004_run.py --model {mattersim,mace} --out DIR [--mats Si,...]
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
from phonopy import Phonopy, PhonopyQHA
from phonopy.structure.atoms import PhonopyAtoms

HERE = os.path.dirname(os.path.abspath(__file__))
R = 8.314462618; FMAX = 1e-3; DISP = 0.01; MESH = 60.0; STAB = -0.3
T_EVAL = [100.0, 200.0, 298.15, 600.0]
T_GRID = np.arange(0.0, 901.0, 1.0)
VFAC = [round(0.94 + 0.02 * i, 2) for i in range(14)]           # V/V_exp = 0.94 … 1.20
ANCLAS = ["Si", "MgO", "NaCl", "LiF", "NaF", "KCl", "KBr", "CaO", "CaF2", "Al2O3", "BeO"]
NUEVOS = ["SrO", "MgF2", "TiO2", "SiO2", "Li2O", "MgAl2O4"]
MATS = ANCLAS + NUEVOS
APF = {"Si": 1, "Ge": 1, "Cu": 1, "CaF2": 3, "Al2O3": 5, "MgF2": 3, "TiO2": 3, "SiO2": 3, "Li2O": 3, "MgAl2O4": 7}
VEXP = json.load(open(os.path.join(HERE, "..", "refs", "vexp_C-MAT-004.json")))["V_exp_A3_por_formula"] if os.path.exists(os.path.join(HERE, "..", "refs", "vexp_C-MAT-004.json")) else {}
VEXP_SMOKE = {"Ge": 22.635, "Cu": 11.81}                          # solo prueba de humo, fuera del estudio

def structure(m):
    rs = {"MgO": 4.212, "NaCl": 5.640, "LiF": 4.027, "NaF": 4.634, "KCl": 6.293, "KBr": 6.600, "CaO": 4.811, "SrO": 5.160}
    if m == "Si": return bulk("Si", "diamond", a=5.431, cubic=True)
    if m == "Ge": return bulk("Ge", "diamond", a=5.658, cubic=True)
    if m == "Cu": return bulk("Cu", "fcc", a=3.615, cubic=True)
    if m in rs: return bulk(m, "rocksalt", a=rs[m], cubic=True)
    if m == "CaF2": return bulk("CaF2", "fluorite", a=5.463, cubic=True)
    if m == "Li2O": return bulk("OLi2", "fluorite", a=4.61, cubic=True)
    if m == "BeO": return bulk("BeO", "wurtzite", a=2.698, c=4.380, u=0.378)
    if m == "Al2O3": return crystal(["Al", "O"], basis=[(0, 0, 0.3522), (0.3064, 0, 0.25)], spacegroup=167,
                                    cellpar=[4.759, 4.759, 12.991, 90, 90, 120], primitive_cell=True)
    if m == "MgF2": return crystal(["Mg", "F"], basis=[(0, 0, 0), (0.303, 0.303, 0)], spacegroup=136, cellpar=[4.62, 4.62, 3.05, 90, 90, 90])
    if m == "TiO2": return crystal(["Ti", "O"], basis=[(0, 0, 0), (0.305, 0.305, 0)], spacegroup=136, cellpar=[4.594, 4.594, 2.959, 90, 90, 90])
    if m == "SiO2": return read(os.path.join(HERE, "..", "refs", "cod_9013321.cif"))
    if m == "MgAl2O4": return crystal(["Mg", "Al", "O"], basis=[(0.125, 0.125, 0.125), (0.5, 0.5, 0.5), (0.2615, 0.2615, 0.2615)],
                                      spacegroup=227, setting=2, cellpar=[8.0801] * 3 + [90] * 3)
    raise KeyError(m)

def supercell(m, kind):
    base = {"Al2O3": (2, 2, 2), "BeO": (3, 3, 2), "MgF2": (2, 2, 3), "TiO2": (2, 2, 3), "SiO2": (2, 2, 2), "MgAl2O4": (1, 1, 1)}
    big = {"Al2O3": (3, 3, 3), "BeO": (4, 4, 3), "MgF2": (3, 3, 4), "TiO2": (3, 3, 4), "SiO2": (3, 3, 3), "MgAl2O4": (2, 2, 2)}
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
    e = float(a.get_potential_energy()); a.set_constraint(); return a, e, bool(conv)

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
    ph.run_thermal_properties(temperatures=temps, exclude_gamma_acoustic=True)
    tp = ph.get_thermal_properties_dict()
    return fmin, gam, tp, len(ph.primitive), len(ph.supercells_with_displacements)

def qha_at(V, E, FE, CV, EN, P, Tg):
    q = PhonopyQHA(volumes=V, electronic_energies=E, temperatures=Tg, free_energy=FE[:len(Tg)], cv=CV[:len(Tg)], entropy=EN[:len(Tg)],
                   pressure=P, eos="vinet", t_max=float(Tg[-1]) - 10)
    return q, np.array(q.volume_temperature)

def analyse(V, E, FE, CV, EN, P, V_target_prim, zp):
    """QHA a presión P: S, Cp suave, V(T), alfa y banderas de patología (decididas en el prereg)."""
    q, vt = qha_at(V, E, FE, CV, EN, P, T_GRID)
    nt = len(vt); Tq = T_GRID[:nt]; flags = []
    if Tq[-1] < 600.0: flags.append("t_max<600")
    vt6 = vt[Tq <= 600.0]
    if vt6.size and (vt6.min() <= V.min() or vt6.max() >= V.max()): flags.append("V_fuera_de_rango")
    sel = (Tq >= 150.0) & (Tq <= 600.0)
    if sel.sum() > 1 and np.any(np.diff(vt[sel]) < -1e-6 * vt[sel][:-1]): flags.append("V_no_monotono")
    def dvdt(T):
        w = (Tq >= T - 20) & (Tq <= T + 20)
        c = np.polyfit(Tq[w] - T, vt[w], 2); return float(c[1]), float(c[2])
    out = {"S": [], "Cp_suave": [], "Cv_VT": [], "V_sobre_Vexp": [], "S_phonopy": [], "Cp_phonopy_polyfit": []}
    try: Sph = np.array(q.entropy_temperature)
    except Exception: Sph = None
    try: Cpp = np.array(q.heat_capacity_P_polyfit)
    except Exception: Cpp = None
    for T in T_EVAL:
        if T > Tq[-1] - 20: [out[k].append(None) for k in out]; continue
        i0 = int(np.floor(T)); i1 = i0 + 1; w1 = T - i0
        def at_T(fun):
            return (1 - w1) * fun(i0) + w1 * fun(i1)
        dv, vT = dvdt(T)
        S = at_T(lambda i: np.polyval(np.polyfit(V, EN[i], 3), vt[i]))
        dSdV = at_T(lambda i: np.polyval(np.polyder(np.polyfit(V, EN[i], 3)), vt[i]))
        Cv = at_T(lambda i: np.polyval(np.polyfit(V, CV[i], 3), vt[i]))
        out["S"].append(S / zp); out["Cv_VT"].append(Cv / zp); out["Cp_suave"].append((Cv + T * dSdV * dv) / zp)
        out["V_sobre_Vexp"].append(vT / V_target_prim)
        out["S_phonopy"].append(None if Sph is None else float(np.interp(T, Tq[:len(Sph)], Sph)) / zp)
        out["Cp_phonopy_polyfit"].append(None if Cpp is None else float(np.interp(T, Tq[:len(Cpp)], Cpp)) / zp)
    dv, vT = dvdt(298.15) if Tq[-1] > 320 else (np.nan, np.nan)
    alfa = dv / vT if vT == vT else None
    if alfa is None or not (0.0 <= alfa <= 3e-4): flags.append("alfa_fuera_[0,3e-4]")
    out.update({"P_GPa": P, "alfa_V_298_1e6K": None if alfa is None else alfa * 1e6, "T_max_K": float(Tq[-1]), "patologias": flags})
    return out

def solve_P(V, E, FE, CV, EN, Vt):
    Tg = T_GRID[T_GRID <= 330.0]
    def f(P):
        try:
            _, vt = qha_at(V, E, FE, CV, EN, P, Tg)
            if len(vt) < 300: return None
            return float(np.interp(298.15, Tg[:len(vt)], vt)) - Vt
        except Exception: return None
    lo, hi = -5.0, 30.0; flo, fhi = f(lo), f(hi)
    if flo is None or fhi is None or flo * fhi > 0: return None, "P_sin_horquilla"
    for _ in range(60):
        mid = 0.5 * (lo + hi); fm = f(mid)
        if fm is None: return None, "P_fallo_QHA"
        if abs(fm) / Vt <= 1e-6: break
        if flo * fm <= 0: hi, fhi = mid, fm
        else: lo, flo = mid, fm
    return mid, None

def run_material(m, calc):
    t0 = time.time(); a0, conv = relax_full(structure(m), calc)
    apf = APF.get(m, 2); nin = len(a0); nfu_in = nin / apf
    vexp_fu = VEXP.get(m, VEXP_SMOKE.get(m)); Vexp_in = vexp_fu * nfu_in
    out = {"material": m, "relax_converged": conv, "cell_par_V0": [float(x) for x in a0.cell.cellpar()],
           "V0_sobre_Vexp": float(a0.get_volume() / Vexp_in)}
    fmin, gam, tp, npr, nd = phonons(a0, calc, supercell(m, "base"), T_EVAL + [3000.0]); zp = npr / apf
    out["arm_V0"] = {"fmin_THz": fmin, "c3_norm": float(tp["heat_capacity"][-1] / (3 * R * npr)),
                     "S": (tp["entropy"][:-1] / zp).tolist(), "Cv": (tp["heat_capacity"][:-1] / zp).tolist()}
    vols, ens, fe, cv, en, fmins, rconv, cells = [], [], [], [], [], [], [], []
    cell0 = a0.cell[:].copy(); s0 = (Vexp_in / a0.get_volume()) ** (1 / 3)
    for fv in VFAC:
        a = a0.copy(); a.set_cell(cell0 * s0 * fv ** (1 / 3), scale_atoms=True)
        a, e, rc = relax_pos(a, calc)
        fm, g, tq, npr, _ = phonons(a, calc, supercell(m, "base"), T_GRID); k = npr / nin
        vols.append(a.get_volume() * k); ens.append(e * k); fmins.append(fm); rconv.append(rc)
        fe.append(tq["free_energy"]); cv.append(tq["heat_capacity"]); en.append(tq["entropy"])
        if fv == 1.0:
            ftmp, gx, tpx, _, _ = phonons(a, calc, supercell(m, "base"), T_EVAL)
            out["arm_Vexp"] = {"fmin_THz": ftmp, "S": (tpx["entropy"] / zp).tolist(), "Cv": (tpx["heat_capacity"] / zp).tolist(), "gamma_THz": gx.tolist()}
            if m in NUEVOS:
                fb, _, tb, nb, _ = phonons(a, calc, supercell(m, "grande"), T_EVAL); out["arm_Vexp_grande"] = {"fmin_THz": fb, "S": (tb["entropy"] / (nb / apf)).tolist()}
    out["qha_input"] = {"vfac": VFAC, "fmin_THz": fmins, "relax_pos_converged": rconv}
    stable = [x >= STAB for x in fmins]; i0 = VFAC.index(1.0); lo = hi = i0
    while lo - 1 >= 0 and stable[lo - 1]: lo -= 1
    while hi + 1 < len(VFAC) and stable[hi + 1]: hi += 1
    ok = stable[i0] and not any(stable[:lo]) and not any(stable[hi + 1:]) and (hi - lo + 1) >= 8
    use = list(range(lo, hi + 1)); res = {"usados": [VFAC[i] for i in use], "evaluable_estabilidad": bool(ok)}
    if ok:
        V = np.array(vols)[use]; E = np.array(ens)[use]
        FE = np.array(fe)[use].T; CV = np.array(cv)[use].T; EN = np.array(en)[use].T
        Vt = vols[i0]
        P, why = solve_P(V, E, FE, CV, EN, Vt)
        res["corr"] = analyse(V, E, FE, CV, EN, P, Vt, zp) if P is not None else {"patologias": [why]}
        try: res["sin_corr"] = analyse(V, E, FE, CV, EN, 0.0, Vt, zp)
        except Exception as ex: res["sin_corr"] = {"patologias": ["fallo_QHA_P0"]}
    out["qha"] = res; out["t_s"] = time.time() - t0
    return out

def rnd(x):
    if isinstance(x, (float, np.floating)): return float(f"{float(x):.10g}")
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
        c = r["qha"].get("corr", {}); print(A.model, m, "P=%s S298=%s pat=%s t=%.0fs" % (c.get("P_GPa"), (c.get("S") or [None]*3)[2], c.get("patologias"), t), flush=True)

if __name__ == "__main__": main()
