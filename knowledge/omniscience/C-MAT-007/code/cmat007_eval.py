#!/usr/bin/env python3
"""C-MAT-007: evaluación tal cual. Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os, glob
import numpy as np
S = "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience"; H = os.path.dirname(os.path.abspath(__file__)) + "/.."
REF = {}
for f in (f"{S}/C-MAT-004/refs/refs_termo_C-MAT-004.json", f"{S}/C-MAT-005/refs/refs_termo_C-MAT-005.json", f"{H}/refs/refs_termo_C-MAT-007.json"):
    for m, v in json.load(open(f))["materiales"].items():
        i, j = v["T_K"].index(298.15), v["T_K"].index(600.0); REF[m] = {"S": [v["S"][i], v["S"][j]], "Cp": [v["Cp"][i], v["Cp"][j]]}
def load(run): return {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(f"{H}/out/{run}/mattersim/*.json")}
def ev(d):
    rows = {}
    for m, r in d.items():
        if m not in REF: continue
        e = r.get("clase") != "no_evaluable" and "S_form" in r
        row = {"clase": r.get("clase"), "f_imag": r.get("f_imag"), "nuevo": r.get("nuevo")}
        if e:
            for k, (x, y) in (("S298", (r["S_form"][0], REF[m]["S"][0])), ("S600", (r["S_form"][1], REF[m]["S"][1])), ("Cp298", (r["Cv_form"][0], REF[m]["Cp"][0])), ("Cp600", (r["Cv_form"][1], REF[m]["Cp"][1]))):
                row[k] = {"calc": x, "ref": y, "err_rel": (x - y) / y}
        rows[m] = row
    return rows
def mare(rows, k): v = [abs(r[k]["err_rel"]) for r in rows.values() if k in r]; return (float(np.mean(v)) if v else -1, len(v))
def hip(rows):
    n = len(rows); ok10 = sum(1 for r in rows.values() if "S298" in r and abs(r["S298"]["err_rel"]) <= 0.10)
    m2, ne = mare(rows, "S298"); m3, _ = mare(rows, "S600"); m4, _ = mare(rows, "Cp298")
    neg = [r["Cp600"]["err_rel"] < 0 for r in rows.values() if "Cp600" in r]
    nu = [r for r in rows.values() if r.get("nuevo")]; nu_ok = sum(1 for r in nu if "S298" in r and abs(r["S298"]["err_rel"]) <= 0.10)
    return {"n": n, "n_evaluables": ne, "n_S298_10pc": ok10, "H1": "PASA" if (n == 44 and ok10 >= 37) else ("FALLA" if n == 44 else "NO EVALUABLE"),
            "MARE_S298": m2, "H2": ("PASA" if m2 <= 0.05 else "FALLA") if ne >= 30 else "INCONCLUSA",
            "MARE_S600": m3, "H3": ("PASA" if m3 <= 0.05 else "FALLA") if ne >= 30 else "INCONCLUSA",
            "MARE_Cp298": m4, "H4": ("PASA" if m4 <= 0.05 else "FALLA") if ne >= 30 else "INCONCLUSA",
            "frac_Cv600_bajo_Cp": float(np.mean(neg)) if neg else -1, "MARE_Cp600": mare(rows, "Cp600")[0], "H5": ("PASA" if np.mean(neg) >= 0.75 else "FALLA") if len(neg) >= 30 else "INCONCLUSA",
            "n_nuevos": len(nu), "n_nuevos_10pc": nu_ok, "H6": "PASA" if (len(nu) == 13 and nu_ok >= 10) else ("FALLA" if len(nu) == 13 else "NO EVALUABLE")}
r1, r2 = ev(load("run1")), ev(load("run2")); h1, h2 = hip(r1), hip(r2)
dif = {m: abs(r2[m]["S298"]["calc"] - r1[m]["S298"]["calc"]) / r1[m]["S298"]["calc"] for m in r1 if m in r2 and "S298" in r1[m] and "S298" in r2[m]}
same = all(h1[k] == h2[k] for k in ("H1", "H2", "H3", "H4", "H5", "H6"))
rep = {"n_comparados": len(dif), "n_dentro_1pc": sum(v <= 0.01 for v in dif.values()), "max": max(dif.values()) if dif else -1, "veredictos_iguales": same}
rep["veredicto"] = "PASA" if (len(dif) >= 0.9 * h1["n_evaluables"] and rep["n_dentro_1pc"] >= 0.9 * len(dif) and same) else "FALLA"
nivel = "E3" if rep["veredicto"] == "PASA" else "E2"
out = {"run1": {"filas": r1, "hip": h1}, "run2_disp0p02": {"hip": h2}, "H_REP": rep, "nivel_E": nivel}
json.dump(out, open(f"{H}/results.json", "w"), indent=1, ensure_ascii=False); print(json.dumps({"hip_run1": h1, "hip_run2": h2, "H_REP": rep, "nivel": nivel}, indent=1))
