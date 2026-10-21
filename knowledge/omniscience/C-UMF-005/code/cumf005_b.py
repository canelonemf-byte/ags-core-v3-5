#!/usr/bin/env python3
"""C-UMF-005 parte B: D3(BJ) solo en compuestos de baja dimensionalidad (regla R-dim fija) y en toda su reacción de formación.
Reutiliza energías MatterSim (C-UMF-002) y MatterSim+D3 (C-UMF-004). Uso: python cumf005_b.py --run {run1,run2} --out FICHERO.json
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, copy, json, sys, warnings
warnings.filterwarnings("ignore")
import numpy as np
ST = "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience"
sys.path.insert(0, ST + "/C-UMF-002/code"); import cumf002_eval as e2, cumf002_run as u2
from ase.geometry.dimensionality import analyze_dimensionality
ap = argparse.ArgumentParser(); ap.add_argument("--run"); ap.add_argument("--out"); A = ap.parse_args()
base = e2.load(f"{ST}/C-UMF-002/out/{A.run}/mattersim"); d3 = e2.load(f"/workspace/omniscience_cumf004/out/b_{A.run}/mattersim")
LAY = ["MgCl2", "CaI2", "MgBr2"]; marca, dim = {}, {}
for m in e2.JAN:
    iv = analyze_dimensionality(u2.structure(m), method="RDA")[0]; dim[m] = iv.dimtype; marca[m] = iv.dimtype != "3D"
def ref(r, el): return r["m"][e2.MOLREF[el]]["E_por_atomo_eV"] if el in e2.ANION else r["e"][el]["E_por_atomo_eV"]
sel = copy.deepcopy(base)
for m in e2.JAN:
    if not marca[m]: continue
    f = e2.formula(m); nat = sum(f.values()); c = d3["c"][m]; nf = c["n_atomos"] / nat
    sel["c"][m] = dict(c, E_total_eV=c["E_total_eV"] - nf * sum(n * (ref(d3, el) - ref(base, el)) for el, n in f.items()))
rows, S = e2.evaluate(sel); le = S["loocv_err_meV"]
out = {"run": A.run, "dimtype": dim, "marcados": sorted(k for k in marca if marca[k]), "capas_marcadas": {k: marca[k] for k in LAY},
       "MAE_loocv_sel": S["MAE_loocv_meV"], "n": S["n_sin_Ti"], "err_loocv_sel": le, "err_capas_sel": {k: le[k] for k in LAY},
       "MAE_capas_sel": float(np.mean([abs(le[k]) for k in LAY])), "max_abs_sel": float(max(abs(x) for x in le.values())),
       "peor": max(le, key=lambda k: abs(le[k])), "MAE_test_Ti_sel": S["MAE_test_Ti_meV"], "convergen": all(x["convergio"] for k in "cem" for x in sel[k].values())}
json.dump(out, open(A.out, "w"), indent=1, default=float); print(json.dumps({k: out[k] for k in ("marcados", "MAE_loocv_sel", "MAE_capas_sel", "max_abs_sel", "peor")}, default=float))
