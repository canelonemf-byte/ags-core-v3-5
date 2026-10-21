#!/usr/bin/env python3
"""C-NANO-001: evaluación tal cual del prerregistro congelado. Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os, glob
import numpy as np
from pymatgen.analysis.wulff import WulffShape
from pymatgen.core import Lattice
H = os.path.dirname(os.path.abspath(__file__)) + "/.."
REF = json.load(open(f"{H}/refs/refs_gamma_metales.json"))["metales"]
FCC = ["Ag", "Al", "Au", "Cu", "Ni", "Pd", "Pt"]; TRAIN = ["Ag", "Al", "Au", "Cu", "Fe"]; TEST = ["Mo", "Ni", "Pd", "Pt", "W"]
DH = 0.027  # eV/TiO2
def L(run, model, pat): return {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(f"{H}/out/{run}/{model}/{pat}.json")}
def wulff_cubic(gs):  # gs: {'111':γ,...}
    m = [tuple(int(c) for c in k) for k in gs]; return WulffShape(Lattice.cubic(1.0), m, list(gs.values())).weighted_surface_energy
def metales(run, model):
    d = L(run, model, "metal_*"); out = {}
    for m in REF:
        gs = {v["faceta"]: v["gamma_J_m2"] for v in d.values() if v["material"] == m}
        if len(gs) == 3: out[m] = {"facetas": gs, "gamma_w": wulff_cubic(gs), "ref": REF[m]["gamma_w_J_m2"], "relax_ok": all(v["relax_ok"] for v in d.values() if v["material"] == m)}
    return out
def h1h2(mt):
    if len(mt) < 10: return {"H1": "NO EVALUABLE", "H2": "NO EVALUABLE"}
    n_sub = sum(mt[m]["gamma_w"] < mt[m]["ref"] for m in mt)
    x = np.array([mt[m]["gamma_w"] for m in TRAIN]); y = np.array([mt[m]["ref"] for m in TRAIN]); a = float((x * y).sum() / (x * x).sum())
    mae_test = float(np.mean([abs(a * mt[m]["gamma_w"] - mt[m]["ref"]) for m in TEST])); mae_raw = float(np.mean([abs(mt[m]["gamma_w"] - mt[m]["ref"]) for m in mt]))
    return {"n_subestima": int(n_sub), "H1": "PASA" if n_sub >= 8 else "FALLA", "a": a, "MAE_test_corr": mae_test, "MAE_bruto_10": mae_raw,
            "MAE_test_bruto": float(np.mean([abs(mt[m]["gamma_w"] - mt[m]["ref"]) for m in TEST])),
            "H2": "PASA" if (mae_test < 0.10 and 1.05 <= a <= 1.5) else "FALLA"}
def tio2(run, model):
    d = L(run, model, "tio2_*"); r = {}
    for fase, hs, lat in (("rutilo", ["110", "100", "101"], None), ("anatasa", ["101", "001", "100"], None)):
        g = {h: d[f"tio2_{fase}_{h}"]["gamma_J_m2"] for h in hs if f"tio2_{fase}_{h}" in d and "gamma_J_m2" in d[f"tio2_{fase}_{h}"]}
        if len(g) < 3: return None
        from ase.io import read
        b = read(f"{H}/out/{run}/{model}/bulk_{fase}.traj"); p = b.cell.cellpar(); latt = Lattice.tetragonal((p[0] + p[1]) / 2, p[2])
        w = WulffShape(latt, [tuple(int(c) for c in h) for h in g], list(g.values()))
        r[fase] = {"facetas": g, "gamma_w": w.weighted_surface_energy, "V_fu": d[f"tio2_{fase}_{hs[0]}"]["V_fu_A3"], "fraccion_area": {str(k): v for k, v in w.area_fraction_dict.items()}}
    gR, gA = r["rutilo"]["gamma_w"] / 16.02176634, r["anatasa"]["gamma_w"] / 16.02176634
    dstar = 6 * (gR * r["rutilo"]["V_fu"] - gA * r["anatasa"]["V_fu"]) / DH / 10  # nm
    dg = r["rutilo"]["gamma_w"] - r["anatasa"]["gamma_w"]; a101 = r["anatasa"]["facetas"]["101"]
    r.update({"d_estrella_nm": dstar, "delta_gamma": dg, "anatasa101": a101,
              "H4": "PASA" if 0.308 <= a101 <= 0.572 else "FALLA", "H5": "PASA" if 5 <= dstar <= 40 else "FALLA", "H6": "PASA" if 0.9 <= dg <= 2.7 else "FALLA"})
    return r
R = {}
for run, model in (("run1", "mattersim"), ("run1", "mace"), ("run2", "mattersim")):
    mt = metales(run, model); R[f"{run}_{model}"] = {"metales": mt, "hip_metales": h1h2(mt), "tio2": tio2(run, model)}
g = L("run1", "mattersim", "gamma_*")
R["H7"] = {k: {"fmin_THz": v["fmin_THz"], "n_bajo_m0p3": v["n_bajo_m0p3"]} for k, v in g.items()}
R["H7"]["veredicto"] = ("PASA" if all(v["n_bajo_m0p3"] == 0 for v in g.values()) else "FALLA") if len(g) == 2 else "NO EVALUABLE"
# réplica
a1 = {**L("run1", "mattersim", "metal_*"), **L("run1", "mattersim", "tio2_*")}; a2 = {**L("run2", "mattersim", "metal_*"), **L("run2", "mattersim", "tio2_*")}
dif = {k: abs(a2[k]["gamma_J_m2"] - a1[k]["gamma_J_m2"]) for k in a1 if k in a2 and "gamma_J_m2" in a1[k] and "gamma_J_m2" in a2[k]}
ok = sum(v <= 0.05 for v in dif.values()); r1, r2 = R["run1_mattersim"], R["run2_mattersim"]
same = r1["hip_metales"].get("H1") == r2["hip_metales"].get("H1") and r1["hip_metales"].get("H2") == r2["hip_metales"].get("H2") and (r1["tio2"] and r2["tio2"] and all(r1["tio2"][h] == r2["tio2"][h] for h in ("H4", "H5", "H6")))
R["H_REP"] = {"n_losas_comparadas": len(dif), "n_dentro_0p05": ok, "max_dif": max(dif.values()) if dif else -1, "veredictos_iguales": bool(same),
              "veredicto": "PASA" if (len(dif) == 36 and ok >= 0.9 * 36 and same) else ("FALLA" if len(dif) == 36 else "NO EVALUABLE")}
gp = f"{H}/out/gpaw/gpaw_anatasa101.json"
if os.path.exists(gp) and r1["tio2"]:
    gj = json.load(open(gp)); rel = abs(r1["tio2"]["anatasa101"] - gj["gamma_PBE_J_m2"]) / gj["gamma_PBE_J_m2"]
    R["C1"] = {"gamma_PBE_geomMS": gj["gamma_PBE_J_m2"], "gamma_MS": r1["tio2"]["anatasa101"], "rel": rel, "veredicto": "PASA" if rel <= 0.30 else "FALLA"}
else: R["C1"] = {"veredicto": "NO EVALUABLE"}
rep, c1 = R["H_REP"]["veredicto"], R["C1"]["veredicto"]
R["nivel_E"] = "E3" if (rep == "PASA" and c1 == "PASA") else ("E2" if rep == "PASA" else "E1")
json.dump(R, open(f"{H}/results.json", "w"), indent=1, ensure_ascii=False, default=float)
print(json.dumps({k: R[k] for k in ("H7", "H_REP", "C1", "nivel_E")}, indent=1, default=float)); print("H1/H2", {k: R[k]["hip_metales"] for k in R if k.startswith("run")})
for k in R:
    if k.startswith("run") and R[k]["tio2"]: print(k, {x: R[k]["tio2"][x] for x in ("anatasa101", "d_estrella_nm", "delta_gamma", "H4", "H5", "H6")})
