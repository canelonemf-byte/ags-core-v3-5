#!/usr/bin/env python3
"""C-MAT-006: evaluación con los criterios congelados (prereg sha256 33b60529…).
Uso: python cmat006_eval.py   (lee out/run1, out/run2, out/dft)
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "out")
STORE = "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience"
REF = {**json.load(open(f"{STORE}/C-MAT-004/refs/refs_termo_C-MAT-004.json"))["materiales"], **json.load(open(f"{STORE}/C-MAT-005/refs/refs_termo_C-MAT-005.json"))["materiales"]}
M4 = ["Si", "MgO", "NaCl", "LiF", "NaF", "KCl", "KBr", "CaO", "CaF2", "Al2O3", "BeO", "SrO", "MgF2", "TiO2", "SiO2", "Li2O", "MgAl2O4"]
M5 = ["AlN", "SiC", "KF", "NaBr", "KI", "LiCl", "CsCl", "SrF2", "BaF2", "Na2O", "ZrO2", "BeAl2O4", "MgTiO3", "ZrSiO4"]; MATS = M4 + M5
v = lambda c: "PASA" if c else "FALLA"

def modelo(run, mdl):
    out = {}
    for m in MATS:
        f = os.path.join(OUT, run, mdl, m + ".json")
        if not os.path.exists(f): continue
        r = json.load(open(f)); S = REF[m]["S"]; T = REF[m]["T_K"]; i298, i600 = T.index(298.15), T.index(600.0)
        out[m] = {"clase": r["clase"], "f_imag": r["f_imag"], "fmin_THz": r["fmin_THz"], "S298": r["S_form"][0], "S600": r["S_form"][1],
                  "err298": r["S_form"][0] / S[i298] - 1, "err600": r["S_form"][1] / S[i600] - 1,
                  "c1": abs(r["S_form"][0] / r["S_phonopy_form"][0] - 1) if r["clase"] == "normal" else None}
    return out

def hip(ms, mc):
    ev = [m for m in ms if ms[m]["clase"] != "no_evaluable"]; n = len(ev)
    mare = lambda d, ks, k: float(np.mean([abs(d[m][k]) for m in ks])) if ks else None
    H = {"n_calculados": len(ms), "evaluables": n, "no_evaluables": [m for m in ms if m not in ev], "con_regla": [m for m in ev if ms[m]["clase"] == "evaluable_con_regla"]}
    k10 = sum(1 for m in ev if abs(ms[m]["err298"]) <= 0.10)
    H["H1"] = {"n_dentro_10pc": k10, "de": 31, "umbral": 26, "veredicto": v(k10 >= 26 and len(ms) == 31)}
    m2 = mare(ms, ev, "err298"); H["H2"] = {"MARE": m2, "n": n, "veredicto": "INCONCLUSA" if n < 21 else v(m2 <= 0.05)}
    m3 = mare(ms, ev, "err600"); H["H3"] = {"MARE": m3, "n": n, "veredicto": "INCONCLUSA" if n < 21 else v(m3 <= 0.06)}
    inter = [m for m in ev if m in mc and mc[m]["clase"] != "no_evaluable"]
    a, b = mare(ms, inter, "err298"), mare(mc, inter, "err298")
    H["H4"] = {"MARE_ms": a, "MARE_mace": b, "cociente": a / b if b else None, "n": len(inter), "veredicto": "INCONCLUSA" if len(inter) < 21 else v(a <= 0.6 * b)}
    cr = H["con_regla"]; ok = sum(1 for m in cr if abs(ms[m]["err298"]) <= 0.10)
    H["H5"] = {"n_con_regla": len(cr), "ok": ok, "veredicto": "INCONCLUSA" if len(cr) < 3 else v(ok >= 2 * len(cr) / 3)}
    H["H6"] = {"n_no_evaluables": len(H["no_evaluables"]), "veredicto": v(len(H["no_evaluables"]) <= 3)}
    return H

def dft(mat):
    d = os.path.join(OUT, "dft", mat); g = lambda f: json.load(open(os.path.join(d, f))) if os.path.exists(os.path.join(d, f)) else None
    rel, g6, g8, sc, fa = g("relax.json"), g("g650_result.json"), g("g800_result.json"), g("sc_result.json"), g("factib.json")
    res = {"factib": fa, "relax_ok": bool(rel and rel["converged"] and rel["fmax_eV_A"] <= 2e-3)}
    if g6 and g8:
        a, b = np.array(g6["freq_commensurate_THz"]["0.000,0.000,0.000"]), np.array(g8["freq_commensurate_THz"]["0.000,0.000,0.000"])
        res["C_DFT1_max_dif_THz"] = float(np.abs(a - b).max()); res["C_DFT1"] = res["C_DFT1_max_dif_THz"] <= 0.15
    else: res["C_DFT1"] = None
    res["PBE_fmin_comm"] = sc["fmin_commensurate_THz"] if sc else None
    res["PBE_freq_q"] = {q: f[:3] for q, f in sc["freq_commensurate_THz"].items()} if sc else None
    for mdl in ("mattersim", "mace"):
        f = os.path.join(OUT, "run1", mdl, f"DFT_{mat}.json")
        u = json.load(open(f)) if os.path.exists(f) else None; fm = u["fmin_commensurate_THz"] if u else None
        if u is None or not res["relax_ok"] or not res["C_DFT1"] or sc is None: cl = "INCONCLUSA_DFT"
        elif fm >= -0.3: cl = "C"
        elif res["PBE_fmin_comm"] >= -0.3: cl = "A"
        else: cl = "B"
        res[mdl] = {"fmin_comm": fm, "freq_q_min3": {q: x[:3] for q, x in u["freq_commensurate_THz"].items()} if u else None, "clase": cl}
    c = res["mattersim"]["clase"]; res["veredicto"] = {"A": "CONFIRMADA", "B": "REFUTADA"}.get(c, "INCONCLUSA"); return res

def main():
    out = {}
    for run in ("run1", "run2"):
        ms, mc = modelo(run, "mattersim"), modelo(run, "mace")
        if ms: out[run] = {"mattersim": ms, "mace": mc, "hipotesis": hip(ms, mc)}
    r1 = out["run1"]; c1 = [x["c1"] for x in r1["mattersim"].values() if x["c1"] is not None] + [x["c1"] for x in r1["mace"].values() if x["c1"] is not None]
    old = {m: json.load(open(f"{STORE}/C-MAT-005/out/run1/mattersim/{m}.json"))["arm_Vexp"]["S"][2] for m in M5}
    c2 = {m: r1["mattersim"][m]["S298"] / old[m] - 1 for m in M5 if m in r1["mattersim"] and r1["mattersim"][m]["clase"] == "normal"}
    out["controles"] = {"C1_max_rel": max(c1) if c1 else None, "C1": bool(c1) and max(c1) <= 1e-4, "C2_dif": c2, "C2": all(abs(x) <= 1e-4 for x in c2.values())}
    out["H-D1"] = dft("TiO2"); out["H-D2"] = dft("SiO2")
    if "run2" in out:
        d = 0.0; same = True
        for mdl in ("mattersim", "mace"):
            for m, x in out["run1"][mdl].items():
                y = out["run2"][mdl].get(m)
                if y is None: same = False; continue
                d = max(d, abs(y["S298"] / x["S298"] - 1), abs(y["S600"] / x["S600"] - 1)); same &= x["f_imag"] == y["f_imag"]
        vv = lambda r: {k: out[r]["hipotesis"][k]["veredicto"] for k in ("H1", "H2", "H3", "H4", "H5", "H6")}
        out["H-REP"] = {"max_dif_rel": d, "f_imag_igual": same, "veredictos_iguales": vv("run1") == vv("run2"),
                        "veredicto": v(d <= 1e-6 and same and vv("run1") == vv("run2"))}
    json.dump(out, open(os.path.join(HERE, "..", "results.json"), "w"), indent=1)
    H = out["run1"]["hipotesis"]; print(json.dumps(H, indent=0)); print(json.dumps(out["controles"]), json.dumps(out.get("H-REP")))
    for k in ("H-D1", "H-D2"): print(k, json.dumps(out[k])[:800])

if __name__ == "__main__": main()
