#!/usr/bin/env python3
"""C-UMF-003: evaluación literal de las hipótesis del prerregistro congelado. Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os, glob
O = "/workspace/omniscience_cumf003/out"; EXP = 9.0
def L(p): return json.load(open(p)) if os.path.exists(p) else None
def dE(run, met):
    r, a = L(f"{O}/dft_{run}/{met}_rutilo.json"), L(f"{O}/dft_{run}/{met}_anatasa.json")
    return None if r is None or a is None else 1000 * (a["E_por_atomo_eV"] - r["E_por_atomo_eV"])
R = {"dE_AR_meV_at": {run: {m: dE(run, m) for m in ["PBE", "PBEU", "R2SCAN"]} for run in ["run1", "run2"]}}
d = R["dE_AR_meV_at"]["run1"]; ok = lambda x: x is not None
H = {}
H["H-A1"] = ok(d["PBE"]) and d["PBE"] < 0
H["H-A2"] = ok(d["R2SCAN"]) and d["R2SCAN"] > 0
H["H-A3"] = ok(d["PBEU"]) and d["PBEU"] > 0
H["H-A4"] = any(ok(d[m]) and abs(d[m] - EXP) <= 10 for m in ["PBEU", "R2SCAN"])
H["H-A5"] = ok(d["R2SCAN"]) and abs(d["R2SCAN"] - EXP) <= 10
CAP, DEN = ["MgCl2", "CaI2", "MgBr2"], ["NaCl", "KCl", "MgO", "CaF2", "LiF", "TiO2"]
def V(run, var, m): return L(f"{O}/mlip_{run}/{var}_{m}.json")
mean = lambda xs: sum(xs) / len(xs)
B = {run: {var: {m: V(run, var, m)["dV_rel"] for m in CAP + DEN} for var in ["ms", "ms_d3"]} for run in ["run1", "run2"]}
R["dV_rel"] = B; b = B["run1"]
capd3 = [abs(b["ms_d3"][m]) for m in CAP]; cap0 = [abs(b["ms"][m]) for m in CAP]
den3 = mean([abs(b["ms_d3"][m]) for m in DEN]); den0 = mean([abs(b["ms"][m]) for m in DEN])
R["resumen_B"] = {"cap_mean_ms": mean(cap0), "cap_mean_d3": mean(capd3), "den_mean_ms": den0, "den_mean_d3": den3}
H["H-B1"] = all(x <= 0.05 for x in capd3)
H["H-B2"] = mean(capd3) <= 0.5 * mean(cap0)
H["H-B3"] = den3 <= 0.03 and (den3 - den0) <= 0.02
rep_A = [abs(R["dE_AR_meV_at"]["run1"][m] - R["dE_AR_meV_at"]["run2"][m]) for m in ["PBE", "PBEU"] if ok(R["dE_AR_meV_at"]["run2"][m])]
rep_B = [abs((1 + B["run1"][v][m]) / (1 + B["run2"][v][m]) - 1) for v in B["run1"] for m in CAP + DEN]
R["replica"] = {"max_dif_A_meV": max(rep_A) if len(rep_A) == 2 else None, "max_dif_V_rel": max(rep_B),
                "r2scan_run2": R["dE_AR_meV_at"]["run2"]["R2SCAN"]}
H["H-REP"] = len(rep_A) == 2 and max(rep_A) <= 1 and max(rep_B) <= 1e-3
R["hipotesis"] = H
pr = ["H-A2", "H-A4", "H-B1", "H-B3"]
if all(H[h] for h in pr) and H["H-REP"]: E = "E3"
elif ((H["H-A2"] or H["H-A4"]) and (H["H-B1"] or H["H-B3"])) or all(H[h] for h in ["H-A1","H-A2","H-A3","H-A4","H-A5"]) or all(H[h] for h in ["H-B1","H-B2","H-B3"]): E = "E2"
else: E = "E1"
R["nivel_E"] = E
json.dump(R, open("/workspace/omniscience_cumf003/results.json", "w"), indent=1); print(json.dumps(R, indent=1))
