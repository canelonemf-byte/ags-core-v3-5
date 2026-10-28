#!/usr/bin/env python3
"""C-NANO-002: fonones de monocapas (grafeno, h-BN, MoS2-1H) y masivos (grafito AB, h-BN AA', 2H-MoS2) con potenciales universales.
Uso: python nano2_run.py --model {mattersim,mace} --run {run1,run2} --out DIR [--parte mono,bulk] [--d3 0/1]
run1: semilla 1, desplazamiento 0.010 Å, mallas q mono 48x48x1 / bulk 24x24x8.
run2: semilla 2, desplazamiento 0.015 Å, mallas q mono 36x36x1 / bulk 18x18x6.
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import guardia
import numpy as np, torch
torch.set_num_threads(2); torch.set_default_dtype(torch.float64)
from ase import Atoms
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms

THZ2CM = 33.35641; KB = 8.617333262e-5; R = 8.314462618
NU_IMAG, NU_CUT, F_MAX = -0.05, 0.05, 0.02           # regla R0–R4 de C-MAT-006 (THz)
RUNS = {"run1": dict(seed=1, disp=0.010, mesh_mono=[48, 48, 1], mesh_bulk=[24, 24, 8]),
        "run2": dict(seed=2, disp=0.015, mesh_mono=[36, 36, 1], mesh_bulk=[18, 18, 6])}
VAC = 20.0
SC_MONO = [[6, 0, 0], [0, 6, 0], [0, 0, 1]]
SC_BULK = {"grafito": [[3, 0, 0], [0, 3, 0], [0, 0, 2]], "hBN_bulk": [[3, 0, 0], [0, 3, 0], [0, 0, 2]], "MoS2_2H": [[3, 0, 0], [0, 3, 0], [0, 0, 1]]}   # reducido por memoria (smoke/smoke_mem.log)
D3_CUT_BOHR = 40.0   # C-UMF-003 usó 95 bohr; reducido por memoria (desviación declarada antes de calcular)

def hexcell(a, c): return [[a, 0, 0], [-a / 2, a * np.sqrt(3) / 2, 0], [0, 0, c]]

def mono(name):
    if name == "grafeno": return Atoms("C2", cell=hexcell(2.46, VAC), scaled_positions=[[1/3, 2/3, .5], [2/3, 1/3, .5]], pbc=True)
    if name == "hBN": return Atoms("BN", cell=hexcell(2.50, VAC), scaled_positions=[[1/3, 2/3, .5], [2/3, 1/3, .5]], pbc=True)
    if name == "MoS2": dz = 1.56 / VAC; return Atoms("MoS2", cell=hexcell(3.16, VAC), scaled_positions=[[1/3, 2/3, .5], [2/3, 1/3, .5 + dz], [2/3, 1/3, .5 - dz]], pbc=True)

def bulk(name):   # geometrías iniciales aproximadas; se relajan completas
    if name == "grafito": return Atoms("C4", cell=hexcell(2.46, 6.70), scaled_positions=[[0, 0, .25], [0, 0, .75], [1/3, 2/3, .25], [2/3, 1/3, .75]], pbc=True)
    if name == "hBN_bulk": return Atoms("B2N2", cell=hexcell(2.50, 6.66), scaled_positions=[[1/3, 2/3, .25], [2/3, 1/3, .75], [2/3, 1/3, .25], [1/3, 2/3, .75]], pbc=True)
    if name == "MoS2_2H":
        z = 0.621; return Atoms("Mo2S4", cell=hexcell(3.16, 12.29), scaled_positions=[[1/3, 2/3, .25], [2/3, 1/3, .75], [1/3, 2/3, z], [1/3, 2/3, .5 - z],
                                                                                    [2/3, 1/3, .5 + z], [2/3, 1/3, 1 - z]], pbc=True)

def calculator(model, d3=False):
    if model == "mattersim":
        from mattersim.forcefield import MatterSimCalculator
        c = MatterSimCalculator(load_path="MatterSim-v1.0.0-5M.pth", device="cpu", dtype="float64")
    else:
        from mace.calculators import mace_mp
        c = mace_mp(model="medium", default_dtype="float64", device="cpu")
    if not d3: return c
    from ase.calculators.mixing import SumCalculator
    from torch_dftd.torch_dftd3_calculator import TorchDFTD3Calculator
    return SumCalculator([c, TorchDFTD3Calculator(xc="pbe", damping="bj", device="cpu", dtype=torch.float64, cutoff=D3_CUT_BOHR * 0.52917721)])

def relax(a, calc, mask, seed):
    """Semilla: escala isótropa aleatoria de la celda inicial (±1 %, normal σ=0.5 %), conserva la simetría; FixSymmetry durante la relajación."""
    a = a.copy(); rng = np.random.default_rng(seed); a.set_cell(a.cell[:] * (1 + float(np.clip(rng.normal(0, 0.005), -0.01, 0.01))), scale_atoms=True)
    a.calc = calc; a.set_constraint(FixSymmetry(a, symprec=0.01))
    opt = BFGS(FrechetCellFilter(a, mask=mask), logfile=None); conv = opt.run(fmax=0.002, steps=800)
    a.set_constraint(); return a, bool(conv)

def fonones(a, calc, sc, disp):
    u = PhonopyAtoms(symbols=a.get_chemical_symbols(), cell=a.cell[:], scaled_positions=a.get_scaled_positions())
    ph = Phonopy(u, supercell_matrix=sc, primitive_matrix=None); ph.generate_displacements(distance=disp)
    F = []
    for s in ph.supercells_with_displacements:
        x = Atoms(s.symbols, cell=s.cell, scaled_positions=s.scaled_positions, pbc=True); x.calc = calc
        f = x.get_forces(); F.append(f - f.mean(axis=0))
    ph.forces = np.array(F); ph.produce_force_constants(); ph.symmetrize_force_constants()
    return ph, len(F)

def caracter(ph, q):
    fr, ev = ph.get_frequencies_with_eigenvectors(q); n = len(ph.primitive); sy = ph.primitive.symbols; out = []
    for j in range(3 * n):
        e = np.abs(ev[:, j].reshape(n, 3)) ** 2
        out.append({"nu_THz": float(fr[j]), "nu_cm": float(fr[j] * THZ2CM), "frac_z": float(e[:, 2].sum()),
                    "peso_Mo": float(sum(e[i].sum() for i in range(n) if sy[i] == "Mo"))})
    return out

def regla_S(ph, mesh, natom):
    ph.run_mesh(mesh, is_gamma_center=True); md = ph.get_mesh_dict(); q = md["qpoints"]; w = md["weights"].astype(float); f = md["frequencies"]
    W = np.repeat(w[:, None], f.shape[1], axis=1) / w.sum(); acu = np.zeros_like(f, bool)
    ig = int(np.where(np.all(np.abs(q) < 1e-9, axis=1))[0][0]); acu[ig, np.argsort(np.abs(f[ig]))[:3]] = True
    imag = (f < NU_IMAG) & ~acu; real = (f > NU_CUT) & ~acu; f_imag = float(W[imag].sum() / W[~acu].sum())
    T = 298.15; x = 6.62607015e-34 * f[real] * 1e12 / (1.380649e-23 * T)
    s = (W[real] * (x / np.expm1(x) - np.log1p(-np.exp(-x)))).sum()           # k_B por celda primitiva (modos reales)
    clase = "normal" if f_imag == 0 else ("evaluable_con_regla" if f_imag <= F_MAX else "no_evaluable")
    S = s / (1 - f_imag) / natom
    ph.run_thermal_properties(temperatures=[T], cutoff_frequency=NU_CUT, exclude_gamma_acoustic=True)
    S_ph = float(ph.get_thermal_properties_dict()["entropy"][0]) / R / natom
    return {"S298_kB_at": float(S), "S298_phonopy_kB_at": S_ph, "f_imag": f_imag, "clase": clase, "fmin_THz": float(f.min()), "malla_q": list(mesh)}

def za_exponente(ph, a):
    rec = np.linalg.inv(a.cell[:]).T; gm = np.linalg.norm(0.5 * rec[0]); fr = np.linspace(0.04, 0.15, 12); nu = []
    for t in fr:
        f = ph.get_frequencies([0.5 * t, 0, 0]); nu.append(f[0])           # ZA = rama más baja
    nu = np.array(nu); ok = bool(np.all(nu > 0))
    p = float(np.polyfit(np.log(fr * gm), np.log(nu), 1)[0]) if ok else None
    return {"q_frac_GM": fr.tolist(), "nu_ZA_THz": nu.tolist(), "exponente": p, "evaluable": ok}

def run_mono(name, calc, R_):
    a, conv = relax(mono(name), calc, [1, 1, 0, 0, 0, 1], R_["seed"])
    ph, nd = fonones(a, calc, SC_MONO, R_["disp"]); n = len(a)
    r = {"material": name, "relax_ok": conv, "a_A": float(a.cell.lengths()[0]), "n_desplazamientos": nd, "supercelda": SC_MONO,
         "G": caracter(ph, [0, 0, 0]), "M": caracter(ph, [0.5, 0, 0]), "K": caracter(ph, [1/3, 1/3, 0]), "ZA": za_exponente(ph, a)}
    r.update(regla_S(ph, R_["mesh_mono"], n)); return r

def run_bulk(name, calc, R_):
    a, conv = relax(bulk(name), calc, [1, 1, 1, 0, 0, 1], R_["seed"])
    ph, nd = fonones(a, calc, SC_BULK[name], R_["disp"]); n = len(a); l = a.cell.lengths()
    r = {"material": name, "relax_ok": conv, "a_A": float(l[0]), "c_A": float(l[2]), "n_desplazamientos": nd, "supercelda": SC_BULK[name], "G": caracter(ph, [0, 0, 0])}
    r.update(regla_S(ph, R_["mesh_bulk"], n)); return r

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--model", default="mattersim"); ap.add_argument("--run", default="run1"); ap.add_argument("--out", required=True)
    ap.add_argument("--parte", default="mono,bulk"); ap.add_argument("--d3", type=int, default=0); ap.add_argument("--mats", default="")
    A = ap.parse_args(); guardia.activar(); R_ = RUNS[A.run]; tag = A.model + ("_d3" if A.d3 else ""); d = os.path.join(A.out, A.run, tag); os.makedirs(d, exist_ok=True)
    calc = calculator(A.model, bool(A.d3))
    tareas = [("mono", m) for m in ["grafeno", "hBN", "MoS2"]] * ("mono" in A.parte) + [("bulk", m) for m in ["grafito", "hBN_bulk", "MoS2_2H"]] * ("bulk" in A.parte)
    for tipo, m in tareas:
        if A.mats and m not in A.mats.split(","): continue
        f = os.path.join(d, m + ".json")
        if os.path.exists(f): continue
        t0 = time.time()
        try: r = run_mono(m, calc, R_) if tipo == "mono" else run_bulk(m, calc, R_)
        except Exception as e: r = {"material": m, "error": repr(e)[:400], "clase": "no_evaluable"}
        r.update({"modelo": tag, "run": A.run, "semilla": R_["seed"], "disp_A": R_["disp"], "t_s": time.time() - t0})
        json.dump(r, open(f + ".tmp", "w"), indent=1); os.replace(f + ".tmp", f)
        print(m, r.get("clase"), r.get("S298_kB_at"), r.get("f_imag"), round(r["t_s"], 1), flush=True)
    print("FIN", flush=True)
