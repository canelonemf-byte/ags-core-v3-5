#!/usr/bin/env python3
"""C-UMF-004: evaluación literal de los criterios congelados (prereg sha256 845ad29a…). Uso: python cumf004_eval.py
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os, sys
import numpy as np
sys.path.insert(0, "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-UMF-002/code"); import cumf002_eval as e2
H = os.path.dirname(os.path.abspath(__file__)) + "/.."; O = H + "/out"; EXP = 9.0; LAY = ["MgCl2", "CaI2", "MgBr2"]
J = lambda p: json.load(open(p)) if os.path.exists(p) else None
def dE(d, met, k="normal"):
    r, a = J(f"{d}/{met}_rutilo_{k}.json"), J(f"{d}/{met}_anatasa_{k}.json")
    return None if r is None or a is None else (a["E_por_atomo_eV"] - r["E_por_atomo_eV"]) * 1e3
v = lambda c: "NO EVALUABLE" if c is None else ("PASA" if c else "FALLA")
R = {"A": {}, "B": {}, "hipotesis": {}}
A = R["A"]; A["dE_PBE_relaj"] = dE(O + "/a_run1", "PBE"); A["dE_R2SCAN_relaj"] = dE(O + "/a_run1", "R2SCAN"); A["dE_R2SCAN_relaj_run2"] = dE(O + "/a_run2", "R2SCAN")
A["dE_HSE06_reducido"] = dE(O + "/a_run1", "HSE06", "reducido")
vr, va = J(O + "/vib_run1/vib_rutilo.json"), J(O + "/vib_run1/vib_anatasa.json")
A["dH_vib298"] = None if not (vr and va) else (va["Uvib298_eV_at"] - vr["Uvib298_eV_at"]) * 1e3
A["dZPE"] = None if not (vr and va) else (va["ZPE_eV_at"] - vr["ZPE_eV_at"]) * 1e3
A["fmin_THz"] = None if not (vr and va) else min(vr["fmin_THz"], va["fmin_THz"])
A["relax"] = {m: J(f"{O}/a_run1/relax_{m}.json") for m in ("rutilo", "anatasa")}
dH = None if A["dE_R2SCAN_relaj"] is None or A["dH_vib298"] is None else A["dE_R2SCAN_relaj"] + A["dH_vib298"]; A["dH_R2SCAN_vib"] = dH
h = R["hipotesis"]
h["H-A1"] = v(None if dH is None else abs(dH - EXP) <= 10); h["H-A2"] = v(None if dH is None else dH > 0)
h["H-A3"] = v(None if A["dE_R2SCAN_relaj"] is None else abs(A["dE_R2SCAN_relaj"] + 11.665761795512708) <= 5)
h["H-A4"] = v(None if A["dH_vib298"] is None else abs(A["dH_vib298"]) <= 5)
h["H-A5"] = v(None if A["dE_HSE06_reducido"] is None else A["dE_HSE06_reducido"] > 0)
B = R["B"]; runs = {}
for r in ("b_run1", "b_run2"):
    d = f"{O}/{r}/mattersim"
    try: rows, S = e2.evaluate(e2.load(d)); runs[r] = (e2.load(d), S)
    except Exception as ex: B["error_" + r] = repr(ex)
if "b_run1" in runs:
    S = runs["b_run1"][1]; le = S["loocv_err_meV"]
    B.update({"MAE_loocv_D3": S["MAE_loocv_meV"], "MAE_loocv_base": 32.630969408592556, "n": S["n_sin_Ti"], "err_capas_D3": {k: le[k] for k in LAY},
              "MAE_capas_D3": float(np.mean([abs(le[k]) for k in LAY])), "MAE_capas_base": 51.8, "max_abs_D3": float(max(abs(x) for x in le.values())),
              "peor": max(le, key=lambda k: abs(le[k])), "MAE_test_Ti_D3": S["MAE_test_Ti_meV"], "MAE_mp2020_D3": S["MAE_mp2020_meV"], "delta_X_eV": S["delta_X_eV"],
              "C1_convergen": all(x["convergio"] for k in "cem" for x in runs["b_run1"][0][k].values())})
    h["H-B1"] = v(B["MAE_loocv_D3"] <= 32.63); h["H-B2"] = v(B["MAE_capas_D3"] <= 36.3); h["H-B3"] = v(B["max_abs_D3"] <= 150)
else: h["H-B1"] = h["H-B2"] = h["H-B3"] = "NO EVALUABLE"
rep = []
if A["dE_R2SCAN_relaj_run2"] is not None and A["dE_R2SCAN_relaj"] is not None: rep.append(abs(A["dE_R2SCAN_relaj_run2"] - A["dE_R2SCAN_relaj"]) <= 0.01)
v2 = J(O + "/vib_run2/vib_anatasa.json")
if v2 and va: rep.append(abs(v2["Uvib298_eV_at"] - va["Uvib298_eV_at"]) * 1e3 <= 0.01)
if len(runs) == 2:
    a, b = runs["b_run1"][0], runs["b_run2"][0]; dif = max(abs(a[k][n]["E_total_eV"] / b[k][n]["E_total_eV"] - 1) for k in "cem" for n in a[k]); B["rep_max_rel"] = dif; rep.append(dif <= 1e-6)
h["H-REP"] = v(None if len(rep) < 3 else all(rep)); R["rep_checks"] = rep
R["controles"] = {"C1": B.get("C1_convergen"), "C2_dif_PBE_vs_CUMF003": None if A["dE_PBE_relaj"] is None else A["dE_PBE_relaj"] + 29.717882568800036,
                  "C3_sin_imag": None if A["fmin_THz"] is None else A["fmin_THz"] > -0.1}
P = lambda *k: all(h[x] == "PASA" for x in k)
R["nivel_E"] = "E3" if P("H-A1", "H-A2", "H-B1", "H-B2", "H-REP") else ("E2" if P("H-B1", "H-B2") or P("H-A1", "H-A2") else "E1")
json.dump(R, open(H + "/results.json", "w"), indent=1, default=float); print(json.dumps(h), R["nivel_E"]); print(json.dumps({k: A[k] for k in A if k != "relax"}))
print(json.dumps({k: B[k] for k in B if k != "delta_X_eV"}, default=float))
