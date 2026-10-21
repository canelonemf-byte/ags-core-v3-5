#!/usr/bin/env python3
"""C-MAT-007: S(298), S(600) y Cv armónica (≈Cp) en V_exp para 44 sólidos con la regla de modos blandos R0–R4 de C-MAT-006.
Uso: python cmat007_run.py --model mattersim --out DIR [--disp 0.01] [--mats ...]   (reanudable, un JSON por material)
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, "/workspace/omniscience_cmat006/code"); import cmat006_run as c6
from ase.build import bulk
H = os.path.dirname(os.path.abspath(__file__)) + "/.."
COD = json.load(open(f"{H}/refs/cod_cmat007.json"))
NUEVOS = {"LiBr": ("rocksalt", 2), "NaI": ("rocksalt", 2), "LiH": ("rocksalt", 2), "NaH": ("rocksalt", 2), "BaO": ("rocksalt", 2), "MgS": ("rocksalt", 2),
          "CaS": ("rocksalt", 2), "CsF": ("rocksalt", 2), "Na2S": ("antifluorite", 3), "K2O": ("antifluorite", 3), "Mg2Si": ("antifluorite", 3), "Al": ("fcc", 1), "Cu": ("fcc", 1)}
FORM = {"Na2S": "SNa2", "K2O": "OK2", "Mg2Si": "SiMg2"}
SC_NUEVOS = {"Al": (3, 3, 3), "Cu": (3, 3, 3)}
MATS = c6.MATS + list(NUEVOS)
T = np.array([298.15, 600.0]); KB, HP, R = c6.KB, c6.H, c6.R

def cv_modos(nu, wt, temps):
    out = []
    for t in temps:
        x = HP * nu * 1e12 / (KB * t); out.append(float(R * (wt * x * x * np.exp(x) / np.expm1(x) ** 2).sum()))
    return np.array(out)

def regla_cv(ph):
    r = c6.regla(ph); md = ph.get_mesh_dict(); q = md["qpoints"]; w = md["weights"].astype(float); f = md["frequencies"]
    W = np.repeat(w[:, None], f.shape[1], axis=1) / w.sum(); acu = np.zeros_like(f, bool); ig = int(np.where(np.all(np.abs(q) < 1e-9, axis=1))[0][0])
    acu[ig, np.argsort(np.abs(f[ig]))[:3]] = True; real = (f > c6.NU_CUT) & ~acu
    cv = cv_modos(f[real], W[real], T) / (1 - r["f_imag"]); r["Cv_prim"] = cv.tolist(); return r

def estructura(m):
    est, apf = NUEVOS[m]; a = COD[m]["a_mediana"]
    if est == "fcc": return bulk(m, "fcc", a=a, cubic=True)
    if est == "rocksalt": return bulk(m, "rocksalt", a=a, cubic=True)
    return bulk(FORM[m], "fluorite", a=a, cubic=True)

def run(m, calc, disp):
    c6.c5.DISP = disp
    if m in NUEVOS:
        t0 = time.time(); a0, conv = c6.c5.relax_full(estructura(m), calc); apf = NUEVOS[m][1]; nfu = len(a0) / apf
        Vc = COD[m]["a_mediana"] ** 3 / 4 * nfu; a = a0.copy(); a.set_cell(a0.cell[:] * (Vc / a0.get_volume()) ** (1 / 3), scale_atoms=True)
        a, rc = c6.c5.relax_pos(a, calc); n = SC_NUEVOS.get(m, (2, 2, 2))
    else:
        M = c6.mod(m); a0, conv = c6.c5.relax_full(M.structure(m), calc); apf = c6.apf(m); nfu = len(a0) / apf; Vc = c6.vexp(m) * nfu
        a = a0.copy(); a.set_cell(a0.cell[:] * (Vc / a0.get_volume()) ** (1 / 3), scale_atoms=True); a, rc = c6.c5.relax_pos(a, calc); n = M.supercell(m, "base")
    ph = c6.fonones(a, calc, n); r = regla_cv(ph); zp = r["n_prim"] / apf
    r.update({"material": m, "nuevo": m in NUEVOS, "relax_ok": conv, "relax_pos_ok": rc, "V_sobre_Vexp": float(a.get_volume() / Vc), "supercelda": list(n), "disp_A": disp,
              "S_form": [s / zp for s in r["S_prim"]], "Cv_form": [c / zp for c in r["Cv_prim"]]})
    return r

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--model", default="mattersim"); ap.add_argument("--out", required=True); ap.add_argument("--disp", type=float, default=0.01)
    ap.add_argument("--mats", default=",".join(MATS)); A = ap.parse_args()
    calc = c6.c5.calculator(A.model); d = os.path.join(A.out, A.model); os.makedirs(d, exist_ok=True)
    for m in A.mats.split(","):
        f = os.path.join(d, m + ".json")
        if os.path.exists(f): continue
        try: r = run(m, calc, A.disp)
        except Exception as e: r = {"material": m, "error": repr(e)[:300], "clase": "no_evaluable"}
        json.dump(c6.rnd(r), open(f + ".tmp", "w"), indent=1, sort_keys=True); os.replace(f + ".tmp", f)
        print(m, r.get("clase"), r.get("f_imag"), (r.get("S_form") or [0])[0], (r.get("Cv_form") or [0])[0], flush=True)
    print("FIN", flush=True)
