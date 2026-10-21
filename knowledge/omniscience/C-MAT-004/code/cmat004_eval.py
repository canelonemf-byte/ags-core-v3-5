#!/usr/bin/env python3
"""Evalúa C-MAT-004 con los criterios congelados (prereg sha256 160ce4b2…2363). Uso: python code/cmat004_eval.py [run1|run2]
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os, sys, hashlib
RUN = sys.argv[1] if len(sys.argv) > 1 else "run1"; OTHER = "run2" if RUN == "run1" else "run1"
ANC = ["Si", "MgO", "NaCl", "LiF", "NaF", "KCl", "KBr", "CaO", "CaF2", "Al2O3", "BeO"]; NEW = ["SrO", "MgF2", "TiO2", "SiO2", "Li2O", "MgAl2O4"]
M = ANC + NEW; MODELS = ["mattersim", "mace"]
REF = json.load(open("refs/refs_termo_C-MAT-004.json"))["materiales"]
C3P = "/workspace/omniscience_cmat003/C-MAT-003/out/run1/mace"
def core(run, mod):
    d = {m: json.load(open(f"out/{run}/{mod}/{m}.json")) for m in M if os.path.exists(f"out/{run}/{mod}/{m}.json")}
    s = json.dumps(d, indent=1, sort_keys=True); open(f"out/{run}/results_core_{mod}.json", "w").write(s)
    return d, hashlib.sha256(s.encode()).hexdigest()
rel = lambda a, b: None if a is None else (a - b) / b
def mare(v): v = [abs(x) for x in v if x is not None]; return (sum(v) / len(v)) if v else None
res = {"run_principal": RUN, "por_modelo": {}, "hipotesis": {}, "controles": {}, "sha256_results_core": {}}
D = {}
for mod in MODELS:
    d1, h1 = core(RUN, mod); d2, h2 = core(OTHER, mod); D[mod] = d1
    res["sha256_results_core"][mod] = {RUN: h1, OTHER: h2, "n": [len(d1), len(d2)], "identicos": h1 == h2 and len(d1) == len(d2) == 17}
    P = {}
    for m in M:
        if m not in d1: P[m] = {"estado": "FALTA"}; continue
        r = d1[m]; J = REF[m]; q = r["qha"]; c = q.get("corr", {}); pat = list(c.get("patologias", ["sin_QHA"]))
        if not q["evaluable_estabilidad"]: pat.append("P2_estabilidad")
        if c.get("V_sobre_Vexp") and c["V_sobre_Vexp"][2] is not None and abs(c["V_sobre_Vexp"][2] - 1) > 1e-4: pat.append("P6_ajuste_V")
        if c.get("S") is None or any(x is None for x in c.get("S", [None])[2:]): pat.append("valores_ausentes")
        conv = None; inconc = False
        if m in NEW and "arm_Vexp_grande" in r:
            conv = abs(r["arm_Vexp_grande"]["S"][2] - r["arm_Vexp"]["S"][2]) / r["arm_Vexp"]["S"][2]; inconc = conv > 0.02
        e = {"patologico": bool(pat), "patologias": pat, "inconcluso_C4": inconc, "conv_C4": conv, "V0_sobre_Vexp": r["V0_sobre_Vexp"],
             "c3_norm": r["arm_V0"]["c3_norm"], "arm_V0_ok": r["arm_V0"]["fmin_THz"] >= -0.3, "arm_Vexp_ok": r["arm_Vexp"]["fmin_THz"] >= -0.3,
             "err_S_armV0": [rel(a, b) for a, b in zip(r["arm_V0"]["S"], J["S"])], "err_S_armVexp": [rel(a, b) for a, b in zip(r["arm_Vexp"]["S"], J["S"])],
             "P_GPa": c.get("P_GPa"), "alfa_V_298_1e6K": c.get("alfa_V_298_1e6K")}
        if not pat:
            e["err_S_corr"] = [rel(a, b) for a, b in zip(c["S"], J["S"])]; e["err_Cp_corr"] = [rel(a, b) for a, b in zip(c["Cp_suave"], J["Cp"])]
            e["S_corr"] = c["S"]; e["Cp_suave"] = c["Cp_suave"]; e["Cp_phonopy_polyfit"] = c["Cp_phonopy_polyfit"]
        s0 = q.get("sin_corr", {})
        if s0.get("S") and not s0.get("patologias"): e["err_S_sincorr_desc"] = [rel(a, b) for a, b in zip(s0["S"], J["S"])]
        e["sin_corr_patologias"] = s0.get("patologias")
        P[m] = e
    res["por_modelo"][mod] = P
ok = lambda mod, m: m in D[mod] and not res["por_modelo"][mod][m]["patologico"] and not res["por_modelo"][mod][m]["inconcluso_C4"]
H = res["hipotesis"]; PM = res["por_modelo"]["mattersim"]
def count(mod, mats, key="err_S_corr", i=2): return sum(1 for m in mats if ok(mod, m) and abs(res["por_modelo"][mod][m][key][i]) <= 0.10)
def mare_ok(mod, mats, key, i, nmin):
    v = [res["por_modelo"][mod][m][key][i] for m in mats if ok(mod, m)]; return mare(v), len(v), len(v) < nmin
n1 = count("mattersim", M); H["H-V1"] = {"n_dentro_10pc": n1, "umbral": 15, "veredicto": "PASA" if n1 >= 15 else "FALSADA"}
mv, n, inc = mare_ok("mattersim", M, "err_S_corr", 2, 14); H["H-V2"] = {"MARE": mv, "n": n, "veredicto": "INCONCLUSA" if inc else ("PASA" if mv <= 0.05 else "FALSADA")}
n3 = count("mattersim", NEW); mv3, nn3, inc3 = mare_ok("mattersim", NEW, "err_S_corr", 2, 5)
H["H-V3"] = {"n_dentro_10pc": n3, "MARE": mv3, "n": nn3, "veredicto": "INCONCLUSA" if inc3 and n3 >= 5 else ("PASA" if n3 >= 5 and not inc3 and mv3 <= 0.05 else "FALSADA")}
mv4, n4, inc4 = mare_ok("mattersim", M, "err_S_corr", 3, 14); H["H-V4"] = {"MARE": mv4, "n": n4, "veredicto": "INCONCLUSA" if inc4 else ("PASA" if mv4 <= 0.05 else "FALSADA")}
a5, n5, i5 = mare_ok("mattersim", M, "err_Cp_corr", 2, 14); b5, _, _ = mare_ok("mattersim", M, "err_Cp_corr", 3, 14)
H["H-V5"] = {"MARE_298": a5, "MARE_600": b5, "n": n5, "veredicto": "INCONCLUSA" if i5 else ("PASA" if a5 <= 0.05 and b5 <= 0.05 else "FALSADA")}
h6 = {}
for mod in MODELS:
    com = [m for m in M if ok(mod, m) and res["por_modelo"][mod][m]["arm_V0_ok"]]
    a = mare([res["por_modelo"][mod][m]["err_S_corr"][2] for m in com]); b = mare([res["por_modelo"][mod][m]["err_S_armV0"][2] for m in com])
    h6[mod] = {"n": len(com), "MARE_corr": a, "MARE_armV0": b, "pasa": len(com) >= 14 and a < b}
H["H-V6"] = h6 | {"veredicto": "PASA" if all(h6[m]["pasa"] for m in MODELS) else ("INCONCLUSA" if any(h6[m]["n"] < 14 for m in MODELS) else "FALSADA")}
v7 = [PM[m]["err_S_armVexp"][2] for m in M if m in D["mattersim"] and PM[m]["arm_Vexp_ok"] and not PM[m]["inconcluso_C4"]]
H["H-V7"] = {"MARE": mare(v7), "n": len(v7), "veredicto": "INCONCLUSA" if len(v7) < 14 else ("PASA" if mare(v7) <= 0.05 else "FALSADA")}
com = [m for m in M if ok("mattersim", m) and ok("mace", m)]
a8 = mare([res["por_modelo"]["mace"][m]["err_S_corr"][2] for m in com]); b8 = mare([PM[m]["err_S_corr"][2] for m in com])
H["H-V8"] = {"n": len(com), "MARE_mace": a8, "MARE_mattersim": b8, "veredicto": "INCONCLUSA" if len(com) < 14 else ("PASA" if a8 >= 1.5 * b8 else "FALSADA")}
H["H-REP"] = {m: res["sha256_results_core"][m]["identicos"] for m in MODELS}; H["H-REP"]["veredicto"] = "PASA" if all(H["H-REP"][m] for m in MODELS) else "FALSADA"
C = res["controles"]
c1 = {}
for m in ANC:
    p = f"{C3P}/{m}.json"
    if os.path.exists(p) and m in D["mace"]: c1[m] = rel(D["mace"][m]["arm_V0"]["S"][2], json.load(open(p))["arm_base"]["S"][2])
C["C1"] = {"desv": c1, "pasa": len(c1) == 11 and all(abs(x) <= 0.005 for x in c1.values())}
C["C2_P_corr_GPa"] = {mod: {m: res["por_modelo"][mod][m].get("P_GPa") for m in M if m in D[mod]} for mod in MODELS}
C["C3"] = {"fallos": {mod: [m for m in M if m in D[mod] and not (0.99 <= res["por_modelo"][mod][m]["c3_norm"] <= 1.000001)] for mod in MODELS}}
C["C3"]["pasa"] = not any(C["C3"]["fallos"].values())
C["C4"] = {mod: {m: res["por_modelo"][mod][m]["conv_C4"] for m in NEW if m in D[mod]} for mod in MODELS}
C["C_PAT"] = {mod: {m: res["por_modelo"][mod][m]["patologias"] for m in M if m in D[mod] and res["por_modelo"][mod][m]["patologico"]} for mod in MODELS}
C["C_PAT"]["pasa"] = len(C["C_PAT"]["mattersim"]) <= 2
res["descriptivo"] = {mod: {"MARE_S_armV0": {T: mare([res["por_modelo"][mod][m]["err_S_armV0"][i] for m in M if m in D[mod]]) for T, i in [(100, 0), (200, 1), (298, 2), (600, 3)]},
                            "MARE_S_corr": {T: mare([res["por_modelo"][mod][m]["err_S_corr"][i] for m in M if ok(mod, m)]) for T, i in [(100, 0), (200, 1), (298, 2), (600, 3)]}} for mod in MODELS}
json.dump(res, open("results.json" if RUN == "run1" else "results_replica_run2.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: v["veredicto"] for k, v in H.items()}, indent=0))
for k, v in H.items(): print(k, {a: b for a, b in v.items() if a != "veredicto"})
print("C1", C["C1"]["pasa"], "C3", C["C3"]["pasa"], "C_PAT", C["C_PAT"])
for mod in MODELS:
    for m in M:
        e = res["por_modelo"][mod].get(m, {})
        if "err_S_armV0" in e: print(mod, m, "V0/Vexp %.3f P %s | S298 armV0 %+.3f armVexp %+.3f corr %s | S600 corr %s | Cp298 %s Cp600 %s | pat %s" % (e["V0_sobre_Vexp"], e["P_GPa"], e["err_S_armV0"][2], e["err_S_armVexp"][2], *(("%+.3f" % e["err_S_corr"][2], "%+.3f" % e["err_S_corr"][3], "%+.3f" % e["err_Cp_corr"][2], "%+.3f" % e["err_Cp_corr"][3]) if "err_S_corr" in e else ("-",) * 4), e["patologias"]))
