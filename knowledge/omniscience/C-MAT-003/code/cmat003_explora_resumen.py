"""EXPLORATORIO, NO pre-registrado: resume el armónico en la celda de partida frente a V0 relajado."""
import json, os
R = json.load(open("refs/refs_C-MAT-003.json"))["materiales"]
M = ["Si", "MgO", "NaCl", "LiF", "NaF", "KCl", "KBr", "CaO", "CaF2", "Al2O3", "BeO"]; out = {}
for mod in ["mattersim", "mace"]:
    for m in M:
        p = f"out/explora_vexp/{mod}_{m}.json"
        if not os.path.exists(p): continue
        e = json.load(open(p)); r1 = json.load(open(f"out/run1/{mod}/{m}.json")); S = R[m]["S"]
        out[f"{mod}:{m}"] = {"V0_relajado_sobre_V_partida": round(r1["V0_A3_por_atomo"] / e["V_A3_por_atomo"], 4),
            "err_S298_V0": round((r1["arm_base"]["S"][2] - S[2]) / S[2], 4), "err_S298_Vpartida": round((e["S"][2] - S[2]) / S[2], 4),
            "err_S600_Vpartida": round((e["S"][3] - S[3]) / S[3], 4), "fmin_Vpartida": e["fmin_THz"]}
        print(mod, m, out[f"{mod}:{m}"])
    v = [x for k, x in out.items() if k.startswith(mod)]
    if v: out[f"MARE_{mod}"] = {k: round(sum(abs(x[k]) for x in v) / len(v), 4) for k in ["err_S298_V0", "err_S298_Vpartida", "err_S600_Vpartida"]} | {"n": len(v)}; print(mod, out[f"MARE_{mod}"])
json.dump(out, open("results_exploratorio_vexp.json", "w"), indent=1)
