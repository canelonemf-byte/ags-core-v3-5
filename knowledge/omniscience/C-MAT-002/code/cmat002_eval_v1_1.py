#!/usr/bin/env python3
"""Evalúa C-MAT-002 con los criterios congelados (prereg sha256 af9fd6d7…aa70)."""
import json, sys, hashlib
r1 = json.load(open("out/v11_run1/results_core.json"))
J = {"Si": {"Cp": [7.268, 15.636, 20.000], "S": [3.833, 11.665, 18.820]},
     "MgO": {"Cp": [7.802, 26.681, 37.106], "S": [2.548, 14.096, 26.924]},
     "NaCl": {"Cp": [34.932, 46.873, 50.509], "S": [23.723, 52.605, 72.115]}}
DS_PRED = {"Si": 8.29, "MgO": 8.70}; TO_EXP = 15.595
out = {"por_calc_material": {}, "hipotesis": {}}
inconcl = set()
for k, v in r1.items():
    c, m = k.split(":"); s2, s3 = v["sc2"], v["sc3"]
    conv = abs(s3["S_J_Kmol_fu"][2] - s2["S_J_Kmol_fu"][2]) / s2["S_J_Kmol_fu"][2]
    if conv > 0.02: inconcl.add(k)
    d = {"a_A": v["a_A"], "relax_converged": v["relax_converged"], "fmin_sc2": s2["fmin_THz"], "fmin_sc3": s3["fmin_THz"],
         "TO_THz": s3["gamma_TO_THz"], "conv_S298_rel": conv, "S": s3["S_J_Kmol_fu"], "Cv": s3["Cv_J_Kmol_fu"],
         "S_ref": J[m]["S"], "Cp_ref": J[m]["Cp"],
         "err_S": [(a - b) / b for a, b in zip(s3["S_J_Kmol_fu"], J[m]["S"])],
         "err_Cv": [(a - b) / b for a, b in zip(s3["Cv_J_Kmol_fu"], J[m]["Cp"])],
         "dS298": s3["S_J_Kmol_fu"][2] - J[m]["S"][2]}
    if m == "Si": d["err_TO"] = (s3["gamma_TO_THz"] - TO_EXP) / TO_EXP
    out["por_calc_material"][k] = d
P = out["por_calc_material"]; mats = ["Si", "MgO", "NaCl"]; M = {m: P[f"MACE:{m}"] for m in mats}
def verdict(ok, keys): return "INCONCLUSA" if any(k in inconcl for k in keys) else ("PASA" if ok else "FALSADA")
mk = [f"MACE:{m}" for m in mats]
out["hipotesis"]["H-TH-1"] = verdict(all(abs(M[m]["err_S"][2]) <= 0.10 for m in mats), mk)
out["hipotesis"]["H-TH-2"] = verdict(all(M[m]["dS298"] > 0 for m in mats), mk)
out["hipotesis"]["H-TH-3"] = verdict(all(abs(M[m]["err_Cv"][0]) > abs(M[m]["err_Cv"][2]) for m in mats), mk)
ratios = {m: M[m]["dS298"] / DS_PRED[m] for m in ["Si", "MgO"]}; out["ratio_dS_obs_pred"] = ratios
out["hipotesis"]["H-TH-4"] = verdict(all(0.5 <= x <= 1.5 for x in ratios.values()), ["MACE:Si", "MACE:MgO"])
sk = ["MACE:Si", "SW:Si", "Kumagai:Si"]
out["hipotesis"]["H-X-1"] = verdict(all(P[k]["relax_converged"] and P[k]["fmin_sc2"] >= -0.3 and P[k]["fmin_sc3"] >= -0.3 for k in sk), [])
out["hipotesis"]["H-X-2"] = verdict(any(abs(P[k]["err_S"][2]) <= 0.10 and abs(P[k]["err_TO"]) <= 0.10 for k in ["SW:Si", "Kumagai:Si"]), ["SW:Si", "Kumagai:Si"])
Ss = [P[k]["S"][2] for k in sk]; out["S298_Si_tres_calc"] = dict(zip(sk, Ss))
out["hipotesis"]["H-X-3"] = verdict(min(Ss) <= 18.820 <= max(Ss), sk)
h = [hashlib.sha256(open(f"out/v11_run{i}/results_core.json", "rb").read()).hexdigest() for i in (1, 2)]
out["sha256_results_core"] = h; out["hipotesis"]["H-X-4"] = "PASA" if h[0] == h[1] else "FALSADA"
out["inconclusos"] = sorted(inconcl)
json.dump(out, open("results_sensibilidad_v1_1.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out["hipotesis"], indent=1)); print("ratios", ratios); print("S298 Si", out["S298_Si_tres_calc"])
for k, d in P.items(): print(k, "a=%.4f TO=%.3f errS=%s errCv=%s conv=%.4f fmin=%.3g" % (d["a_A"], d["TO_THz"], [round(x,3) for x in d["err_S"]], [round(x,3) for x in d["err_Cv"]], d["conv_S298_rel"], d["fmin_sc3"]))
