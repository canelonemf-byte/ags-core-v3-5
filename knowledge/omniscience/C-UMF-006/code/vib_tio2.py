#!/usr/bin/env python3
"""C-TIO2-HSE parte B: ΔU_vib, ΔF_vib y ΔZPE (anatasa − rutilo) por átomo en V_exp con la regla R0–R4 de C-MAT-006.
Uso: python vib_tio2.py --model {mattersim,mace} --out DIR. Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, "/workspace/omniscience_cmat006/code"); import cmat006_run as c6
from ase import Atoms
from ase.io import read
import spglib
CIF = {"rutilo": "/workspace/omniscience_cmat006/refs/cif/cod_9007531.cif", "anatasa": "/workspace/omniscience_cnano001/refs/anatasa.cif"}
SC = {"rutilo": (2, 2, 3), "anatasa": (3, 3, 1)}
T = 298.15; KB, HP = c6.KB, c6.H
def calc_of(model):
    if model == "mattersim": return c6.c5.calculator("mattersim")
    from mace.calculators import mace_mp; return mace_mp(model="medium", device="cpu", default_dtype="float64")
def termo(ph):
    r = c6.regla(ph); md = ph.get_mesh_dict(); q = md["qpoints"]; w = md["weights"].astype(float); f = md["frequencies"]
    W = np.repeat(w[:, None], f.shape[1], axis=1) / w.sum(); acu = np.zeros_like(f, bool); ig = int(np.where(np.all(np.abs(q) < 1e-9, axis=1))[0][0])
    acu[ig, np.argsort(np.abs(f[ig]))[:3]] = True; real = (f > c6.NU_CUT) & ~acu; nu = f[real]; wt = W[real]; e = HP * nu * 1e12; x = e / (KB * T); s = 1 / (1 - r["f_imag"])
    zpe = float((wt * e / 2).sum()) * s; u = zpe + float((wt * e / np.expm1(x)).sum()) * s; fv = zpe + float((wt * KB * T * np.log1p(-np.exp(-x))).sum()) * s
    n = r["n_prim"]; r.update({"ZPE_eV_at": zpe / n, "U_vib_eV_at": u / n, "F_vib_eV_at": fv / n}); return r
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--model"); ap.add_argument("--out"); A = ap.parse_args(); os.makedirs(A.out, exist_ok=True); calc = calc_of(A.model); R = {}
    for fase in ("rutilo", "anatasa"):
        a = read(CIF[fase]); c, p, z = spglib.standardize_cell((a.cell[:], a.get_scaled_positions(), a.numbers), to_primitive=False, symprec=1e-3)
        a = Atoms(numbers=z, cell=c, scaled_positions=p, pbc=True); V = a.get_volume()
        a0, conv = c6.c5.relax_full(a, calc); b = a0.copy(); b.set_cell(a0.cell[:] * (V / a0.get_volume()) ** (1 / 3), scale_atoms=True); b, rc = c6.c5.relax_pos(b, calc)
        ph = c6.fonones(b, calc, SC[fase]); r = termo(ph); r.update({"relax_ok": conv, "relax_pos_ok": rc, "V0_sobre_Vexp": float(a0.get_volume() / V), "supercelda": list(SC[fase])}); R[fase] = c6.rnd(r)
        print(A.model, fase, r["clase"], r["f_imag"], r["fmin_THz"], r["U_vib_eV_at"], flush=True)
    d = {k: 1000 * (R["anatasa"][k] - R["rutilo"][k]) for k in ("ZPE_eV_at", "U_vib_eV_at", "F_vib_eV_at")}
    R["delta_A_menos_R_meV_at"] = d; json.dump(R, open(os.path.join(A.out, f"vib_{A.model}.json"), "w"), indent=1); print("FIN", d, flush=True)
