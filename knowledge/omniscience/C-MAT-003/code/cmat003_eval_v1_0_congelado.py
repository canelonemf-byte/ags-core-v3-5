#!/usr/bin/env python3
"""Evalúa C-MAT-003 con los criterios congelados (prereg sha256 2d9a1256…fc96).
Reglas de interpretación escritas ANTES de ver resultados del estudio (no figuran literalmente en el prereg):
 R1. Si fmin(V0, base) < −0.3 THz (C5), el material es NO_EVALUABLE para ese potencial en todas las hipótesis.
 R2. Las comparaciones de MARE entre dos potenciales (H-Q3, H-Q6) usan la intersección de materiales evaluables de ambos.
 R3. En H-Q4/H-Q5 solo entran materiales con QHA evaluable y horquilla a 600 K (C6).
Uso: python cmat003_eval.py  (desde C-MAT-003/)"""
import json, os, glob, hashlib
M = ["Si", "MgO", "NaCl", "LiF", "NaF", "KCl", "KBr", "CaO", "CaF2", "Al2O3", "BeO"]
MODELS = ["mattersim", "sevenn", "mace"]
REF = json.load(open("refs/refs_C-MAT-003.json"))["materiales"]
C1_REF = {"Si": 24.096729, "MgO": 32.97637, "NaCl": 75.834819}
iT = {100: 0, 200: 1, 298: 2, 600: 3}

def core(run, model):
    d = {}
    for m in M:
        p = f"out/{run}/{model}/{m}.json"
        if os.path.exists(p): d[m] = json.load(open(p))
    s = json.dumps(d, indent=1, sort_keys=True); os.makedirs(f"out/{run}", exist_ok=True)
    open(f"out/{run}/results_core_{model}.json", "w").write(s)
    return d, hashlib.sha256(s.encode()).hexdigest()

def rel(a, b): return None if a is None else (a - b) / b
def mare(v): v = [abs(x) for x in v if x is not None]; return sum(v) / len(v) if v else None

res = {"por_modelo": {}, "hipotesis": {}, "controles": {}, "sha256_results_core": {}}
D = {}
for mod in MODELS:
    d1, h1 = core("run1", mod); d2, h2 = core("run2", mod); D[mod] = d1
    maxd = 0.0
    def walk(a, b):
        global maxd
    def diff(a, b):
        if isinstance(a, dict): return max([diff(a[k], b.get(k)) for k in a] + [0.0])
        if isinstance(a, list): return max([diff(x, y) for x, y in zip(a, b)] + [0.0])
        if isinstance(a, float) and isinstance(b, float): return abs(a - b) / max(abs(a), 1e-12)
        return 0.0 if a == b else float("inf")
    res["sha256_results_core"][mod] = {"run1": h1, "run2": h2, "identicos": h1 == h2 and len(d1) == 11,
                                       "dif_rel_max": diff(d1, d2) if d2 else None, "n_run1": len(d1), "n_run2": len(d2)}
    P = {}
    for m in M:
        if m not in d1: P[m] = {"estado": "FALTA"}; continue
        r = d1[m]; J = REF[m]; ab, ag = r["arm_base"], r["arm_grande"]; q = r["qha"]
        conv = abs(ag["S"][2] - ab["S"][2]) / ab["S"][2]
        st = "OK"
        if ab["fmin_THz"] < -0.3: st = "NO_EVALUABLE_V0"
        elif conv > 0.02: st = "INCONCLUSO"
        e = {"estado": st, "relax_converged": r["relax_converged"], "fmin_V0": ab["fmin_THz"], "conv_S298": conv, "c3_norm": ab["c3_norm"],
             "S_arm": ab["S"], "Cv_arm": ab["Cv"], "err_S_arm": [rel(a, b) for a, b in zip(ab["S"], J["S"])],
             "err_Cv_arm": [rel(a, b) for a, b in zip(ab["Cv"], J["Cp"])], "qha_evaluable": q["evaluable"], "qha_usados": q["usados"]}
        if q["evaluable"]:
            e.update({"S_qha": q["S"], "Cp_qha": q["Cp"], "V_sobre_V0": q["V_sobre_V0"], "alfa_V_298_1e6K": q["alfa_V_298_1e6K"],
                      "horquilla_600": q["horquilla_600"], "err_S_qha": [rel(a, b) for a, b in zip(q["S"], J["S"])],
                      "err_Cp_qha": [rel(a, b) for a, b in zip(q["Cp"], J["Cp"])],
                      "dS_qha_arm_600": None if q["S"][3] is None else q["S"][3] - ab["S"][3],
                      "S_qha_vs_phonopy_298": None if q["S_phonopy"][2] is None else q["S"][2] - q["S_phonopy"][2]})
        e["TO_gamma_THz"] = r["gamma_THz"][-1]
        P[m] = e
    res["por_modelo"][mod] = P

def ok(mod, m): return res["por_modelo"][mod][m].get("estado") == "OK"
def qok(mod, m): return ok(mod, m) and res["por_modelo"][mod][m]["qha_evaluable"]
H = res["hipotesis"]; C = res["controles"]; PM = res["por_modelo"]["mattersim"]
# controles
C["C1_regresion"] = {m: rel(PM_m["arm_base"]["S"][2], C1_REF[m]) for m, PM_m in [(m, D["mace"][m]) for m in C1_REF if m in D["mace"]]}
C["C1_pasa"] = len(C["C1_regresion"]) == 3 and all(abs(x) <= 0.01 for x in C["C1_regresion"].values())
C["C2_fallos"] = {mod: [m for m in M if m in D[mod] and qok(mod, m) and res["por_modelo"][mod][m]["dS_qha_arm_600"] is not None and res["por_modelo"][mod][m]["dS_qha_arm_600"] < 0] for mod in MODELS}
C["C3_fallos"] = {mod: [m for m in M if m in D[mod] and not (0.99 <= res["por_modelo"][mod][m]["c3_norm"] <= 1.000001)] for mod in MODELS}
C["C3_pasa"] = all(not v for v in C["C3_fallos"].values())
C["C4_C5_no_ok"] = {mod: {m: res["por_modelo"][mod][m]["estado"] for m in M if res["por_modelo"][mod][m]["estado"] != "OK"} for mod in MODELS}
C["C5_qha_no_evaluable"] = {mod: [m for m in M if m in D[mod] and not res["por_modelo"][mod][m]["qha_evaluable"]] for mod in MODELS}
C["C6_sin_horquilla_600"] = {mod: [m for m in M if qok(mod, m) and not res["por_modelo"][mod][m]["horquilla_600"]] for mod in MODELS}
# H-Q1/H-Q2
n1 = sum(1 for m in M if qok("mattersim", m) and abs(PM[m]["err_S_qha"][2]) <= 0.10)
H["H-Q1"] = {"n_dentro_10pc": n1, "umbral": 9, "veredicto": "PASA" if n1 >= 9 else "FALSADA"}
ev = [PM[m]["err_S_qha"][2] for m in M if qok("mattersim", m)]
H["H-Q2"] = {"n": len(ev), "MARE": mare(ev), "veredicto": "INCONCLUSA" if len(ev) < 9 else ("PASA" if mare(ev) <= 0.05 else "FALSADA")}
def cmp(a, b, f):
    common = [m for m in M if m in D[a] and m in D[b] and ok(a, m) and ok(b, m)]
    ma = mare([res["por_modelo"][a][m]["err_S_arm"][2] for m in common]); mb = mare([res["por_modelo"][b][m]["err_S_arm"][2] for m in common])
    v = "INCONCLUSA" if len(common) < 9 else ("PASA" if f(ma, mb) else "FALSADA")
    return {"n": len(common), f"MARE_{a}": ma, f"MARE_{b}": mb, "veredicto": v}
H["H-Q3"] = cmp("mattersim", "mace", lambda a, b: a <= 0.5 * b)
H["H-Q6"] = cmp("sevenn", "mace", lambda a, b: a < b)
s600 = [m for m in M if qok("mattersim", m) and PM[m]["horquilla_600"]]
c2bad = len(C["C2_fallos"]["mattersim"]) > 2
for hk, kq, ka in [("H-Q4", "err_S_qha", "err_S_arm"), ("H-Q5", "err_Cp_qha", "err_Cv_arm")]:
    mq = mare([PM[m][kq][3] for m in s600]); ma = mare([PM[m][ka][3] for m in s600])
    v = "INCONCLUSA" if (len(s600) < 9 or c2bad) else ("PASA" if mq < ma else "FALSADA")
    H[hk] = {"n": len(s600), "MARE_qha": mq, "MARE_arm": ma, "veredicto": v}
n7 = sum(1 for m in M if ok("mace", m) and res["por_modelo"]["mace"][m]["err_S_arm"][2] > 0)
H["H-Q7"] = {"n_sobreestima": n7, "umbral": 9, "veredicto": "PASA" if n7 >= 9 else "FALSADA"}
H["H-REP"] = {mod: res["sha256_results_core"][mod]["identicos"] for mod in MODELS}
H["H-REP"]["veredicto"] = "PASA" if all(H["H-REP"][m] for m in MODELS) else "FALSADA"
# descriptivo
res["descriptivo"] = {mod: {"MARE_S_arm": {T: mare([res["por_modelo"][mod][m]["err_S_arm"][i] for m in M if ok(mod, m)]) for T, i in iT.items()},
                            "MARE_S_qha": {T: mare([res["por_modelo"][mod][m]["err_S_qha"][i] for m in M if qok(mod, m)]) for T, i in iT.items()},
                            "n_S298_qha_10pc": sum(1 for m in M if qok(mod, m) and abs(res["por_modelo"][mod][m]["err_S_qha"][2]) <= 0.10)} for mod in MODELS}
json.dump(res, open("results.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: v.get("veredicto") if isinstance(v, dict) else v for k, v in H.items()}, indent=1))
print("C1", C["C1_pasa"], C["C1_regresion"], "C2", C["C2_fallos"], "C3", C["C3_pasa"], "C4C5", C["C4_C5_no_ok"], "C5q", C["C5_qha_no_evaluable"], "C6", C["C6_sin_horquilla_600"])
for mod in MODELS:
    for m in M:
        e = res["por_modelo"][mod][m]
        if "S_arm" in e: print(mod, m, e["estado"], "S298 arm %+.3f qha %s | S600 arm %+.3f qha %s" % (e["err_S_arm"][2], None if "err_S_qha" not in e else "%+.3f" % e["err_S_qha"][2], e["err_S_arm"][3], None if "err_S_qha" not in e or e["err_S_qha"][3] is None else "%+.3f" % e["err_S_qha"][3]))
