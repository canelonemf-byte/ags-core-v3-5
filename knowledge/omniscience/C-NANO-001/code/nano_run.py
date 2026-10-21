#!/usr/bin/env python3
"""C-NANO-001: energías superficiales con potenciales universales (MatterSim / MACE-MP-0).
Partes: metales (10 elementos × 3 facetas), TiO2 (rutilo y anatasa, 3 facetas cada uno), fonones Γ de losas (NANO-09).
Uso: python nano_run.py --model {mattersim,mace} --run {run1,run2} --out DIR [--parte metales,tio2,gamma]
run1 = espesor base; run2 = réplica con losas más gruesas. Reanudable (un JSON por losa).
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
import torch
torch.set_num_threads(3); torch.manual_seed(0); np.random.seed(0)
from ase.build import bulk, fcc111, fcc100, fcc110, bcc110, bcc100, bcc111
from ase.constraints import FixSymmetry
from ase.filters import ExpCellFilter as ECF
from ase.optimize import BFGS
from ase import Atoms
EVA2_JM2 = 16.02176634
FCC = ["Ag", "Al", "Au", "Cu", "Ni", "Pd", "Pt"]; BCC = ["Fe", "Mo", "W"]
METALES = sorted(FCC + BCC)
A0 = {"Ag": 4.09, "Al": 4.05, "Au": 4.08, "Cu": 3.61, "Ni": 3.52, "Pd": 3.89, "Pt": 3.92, "Fe": 2.87, "Mo": 3.15, "W": 3.17}  # sólo punto de partida
CAPAS = {"run1": {"fcc": 9, "bcc110": 9, "bcc100": 9, "bcc111": 12}, "run2": {"fcc": 13, "bcc110": 13, "bcc100": 13, "bcc111": 18}}
TIO2_FACETAS = {"rutilo": [(1, 1, 0), (1, 0, 0), (1, 0, 1)], "anatasa": [(1, 0, 1), (0, 0, 1), (1, 0, 0)]}
TIO2_ESP = {"run1": 12.0, "run2": 18.0}; VAC = 15.0

def calculator(model):
    if model == "mattersim":
        from mattersim.forcefield import MatterSimCalculator
        return MatterSimCalculator(load_path="MatterSim-v1.0.0-5M.pth", device="cpu")
    from mace.calculators import mace_mp
    return mace_mp(model="medium", device="cpu", default_dtype="float64")

def relax_bulk(a, calc):
    a = a.copy(); a.calc = calc; a.set_constraint(FixSymmetry(a))
    BFGS(ECF(a), logfile=None).run(fmax=1e-3, steps=500); a.set_constraint(); return a

def relax_slab(s, calc, fmax=0.01, steps=600):
    s.calc = calc; opt = BFGS(s, logfile=None); ok = opt.run(fmax=fmax, steps=steps); return bool(ok), int(opt.nsteps)

def gamma(e_slab, n_unit, e_unit, area): return (e_slab - n_unit * e_unit) / (2 * area) * EVA2_JM2

def metal(m, faceta, calc, run, bdir):
    est = "bcc" if m in BCC else "fcc"
    bf = os.path.join(bdir, f"bulk_{m}.json")
    if os.path.exists(bf): bj = json.load(open(bf))
    else:
        b = relax_bulk(bulk(m, est, a=A0[m], cubic=True), calc); bj = {"a": float(b.cell[0, 0]), "e_atom": float(b.get_potential_energy() / len(b))}
        json.dump(bj, open(bf, "w"))
    f = {"fcc": {"111": fcc111, "100": fcc100, "110": fcc110}, "bcc": {"110": bcc110, "100": bcc100, "111": bcc111}}[est][faceta]
    nl = CAPAS[run]["fcc" if est == "fcc" else est + faceta]
    try: s = f(m, size=(1, 1, nl), a=bj["a"], vacuum=VAC / 2, orthogonal=False, periodic=True)
    except NotImplementedError: s = f(m, size=(1, 1, nl), a=bj["a"], vacuum=VAC / 2, orthogonal=True, periodic=True)  # D1: (100)/(110) solo admiten celda ortogonal
    A = np.linalg.norm(np.cross(s.cell[0], s.cell[1]))
    s.calc = calc; e0 = s.get_potential_energy(); ok, ns = relax_slab(s, calc)
    e = s.get_potential_energy()
    return {"material": m, "estructura": est, "faceta": faceta, "capas": nl, "n": len(s), "area_A2": float(A), "a_bulk": bj["a"],
            "gamma_J_m2": gamma(e, len(s), bj["e_atom"], A), "gamma_sin_relajar_J_m2": gamma(e0, len(s), bj["e_atom"], A), "relax_ok": ok, "pasos": ns}

def tio2_bulk(fase, calc, bdir):
    from ase.io import read
    bf = os.path.join(bdir, f"bulk_{fase}.traj")
    if os.path.exists(bf): return read(bf)
    cif = {"rutilo": "/workspace/omniscience_cmat006/refs/cif/cod_9007531.cif", "anatasa": os.path.join(os.path.dirname(__file__), "..", "refs", "anatasa.cif")}[fase]
    a = relax_bulk(read(cif), calc); a.write(bf); return a

def tio2(fase, hkl, calc, run, bdir):
    from pymatgen.io.ase import AseAtomsAdaptor as AAA
    from pymatgen.core.surface import SlabGenerator
    b = tio2_bulk(fase, calc, bdir); b.calc = calc; e_fu = b.get_potential_energy() / (len(b) / 3)
    g = SlabGenerator(AAA.get_structure(b), hkl, TIO2_ESP[run], VAC, center_slab=True, primitive=True, lll_reduce=True)
    cands = [s for s in g.get_slabs(symmetrize=False) if s.is_symmetric() and not s.is_polar() and abs(s.composition.reduced_composition["O"] / s.composition.reduced_composition["Ti"] - 2) < 1e-6]
    res = []
    for i, sl in enumerate(cands[:3]):
        s = AAA.get_atoms(sl); s.set_constraint(); A = np.linalg.norm(np.cross(s.cell[0], s.cell[1])); nfu = len(s) / 3
        s.calc = calc; e0 = s.get_potential_energy(); ok, ns = relax_slab(s, calc, fmax=0.02, steps=800); e = s.get_potential_energy()
        res.append({"term": i, "n": len(s), "area_A2": float(A), "gamma_J_m2": gamma(e, nfu, e_fu, A), "gamma_sin_relajar_J_m2": gamma(e0, nfu, e_fu, A), "relax_ok": ok, "pasos": ns})
        s.write(os.path.join(bdir, f"slab_{fase}_{''.join(map(str, hkl))}_t{i}.traj"))
    if not res: return {"fase": fase, "hkl": list(hkl), "error": "sin terminación simétrica estequiométrica no polar"}
    best = min(res, key=lambda r: r["gamma_J_m2"])
    return {"fase": fase, "hkl": list(hkl), "n_candidatas": len(cands), "terminaciones": res, "gamma_J_m2": best["gamma_J_m2"], "term_min": best["term"],
            "V_fu_A3": float(b.get_volume() / (len(b) / 3)), "e_fu_eV": float(e_fu)}

def gamma_modes(fase, hkl, calc, bdir):
    """NANO-09: frecuencias en Γ de la losa relajada (diferencias finitas centrales, 0.01 Å, losa completa)."""
    from ase.io import read
    from ase.vibrations import Vibrations
    import glob, shutil
    fs = sorted(glob.glob(os.path.join(bdir, f"slab_{fase}_{''.join(map(str, hkl))}_t*.traj")))
    tj = json.load(open(os.path.join(bdir, f"tio2_{fase}_{''.join(map(str, hkl))}.json")))
    s = read(os.path.join(bdir, f"slab_{fase}_{''.join(map(str, hkl))}_t{tj['term_min']}.traj")); s.calc = calc
    wd = os.path.join(bdir, f"vib_{fase}_{''.join(map(str, hkl))}"); v = Vibrations(s, name=wd, delta=0.01, nfree=2); v.run()
    e = v.get_energies(); thz = np.where(np.iscomplex(e) & (np.abs(e.imag) > 0), -np.abs(e.imag), np.real(e)) / 4.135667696e-3
    return {"fase": fase, "hkl": list(hkl), "n": len(s), "freq_THz": sorted(map(float, thz)), "fmin_THz": float(np.min(thz)), "n_bajo_m0p3": int((thz < -0.3).sum())}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--model", required=True); ap.add_argument("--run", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--parte", default="metales,tio2,gamma"); A = ap.parse_args()
    d = os.path.join(A.out, A.run, A.model); os.makedirs(d, exist_ok=True); calc = calculator(A.model)
    def guarda(nombre, fn):
        f = os.path.join(d, nombre + ".json")
        if os.path.exists(f): return
        t = time.time(); r = fn(); r["t_s"] = round(time.time() - t, 1)
        json.dump(r, open(f + ".tmp", "w"), indent=1, sort_keys=True); os.replace(f + ".tmp", f); print(A.model, A.run, nombre, r.get("gamma_J_m2", r.get("fmin_THz")), flush=True)
    partes = A.parte.split(",")
    if "metales" in partes:
        for m in METALES:
            for fa in (["111", "100", "110"] if m in FCC else ["110", "100", "111"]):
                guarda(f"metal_{m}_{fa}", lambda: metal(m, fa, calc, A.run, d))
    if "tio2" in partes:
        for fase, hs in TIO2_FACETAS.items():
            for h in hs: guarda(f"tio2_{fase}_{''.join(map(str, h))}", lambda: tio2(fase, h, calc, A.run, d))
    if "gamma" in partes and A.run == "run1":
        for fase, h in (("rutilo", (1, 1, 0)), ("anatasa", (1, 0, 1))): guarda(f"gamma_{fase}_{''.join(map(str, h))}", lambda: gamma_modes(fase, h, calc, d))
    print("FIN", A.model, A.run, flush=True)
