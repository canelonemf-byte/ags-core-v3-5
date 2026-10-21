#!/usr/bin/env python3
"""Evaluador congelado de C-VIB-002 (hipótesis del prereg sha256 c1a20dd5…0b15)."""
import json, glob, sys, numpy as np
from scipy.stats import spearmanr
D = "/workspace/omniscience_cvib002/out"; S = "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-VIB-002"
EXP = {"BN":760,"BP":350,"AlP":90,"AlAs":98,"AlSb":56,"GaP":100,"GaAs":45,"GaSb":40,"InP":93,"InAs":30,"InSb":20,"ZnS":27,"ZnSe":19,"ZnTe":18,"CdTe":7.5}
LDA = {"BN":648,"BP":396,"AlP":83.0,"AlAs":85.6,"AlSb":75.1,"GaP":85.5,"GaAs":31.0,"GaSb":31.8,"InP":73.8,"InAs":20.4,"InSb":12.6,"ZnS":31.0,"ZnSe":14.9,"ZnTe":18.4,"CdTe":6.28}
def load(run, model, mesh=19):
    return {m: json.load(open(f"{D}/{run}/{model}_{m}_m{mesh}.json")) for m in EXP if glob.glob(f"{D}/{run}/{model}_{m}_m{mesh}.json")}
ms, mc, ms2 = load("run1","mattersim"), load("run1","mace"), load("run2","mattersim")
def stats(r):
    ok = {m: v for m, v in r.items() if v["fmin_THz"] > -0.05}
    lr = {m: float(np.log10(v["kappa_300K"]/EXP[m])) for m, v in ok.items()}
    w2 = sum(abs(x) <= np.log10(2) for x in lr.values())
    return ok, lr, int(w2)
ok, lr, w2 = stats(ms); okc, lrc, w2c = stats(mc)
out = {"n_ms": len(ms), "n_mace": len(mc), "C1_excluidos_ms": [m for m in ms if m not in ok], "C1_excluidos_mace": [m for m in mc if m not in okc]}
out["ratio_ms"] = {m: round(10**x, 3) for m, x in lr.items()}; out["ratio_mace"] = {m: round(10**x, 3) for m, x in lrc.items()}
out["kappa_ms"] = {m: round(v["kappa_300K"], 2) for m, v in ms.items()}; out["kappa_mace"] = {m: round(v["kappa_300K"], 2) for m, v in mc.items()}
mal_ms = float(np.mean(np.abs(list(lr.values())))); mal_mc = float(np.mean(np.abs(list(lrc.values()))))
rho = float(spearmanr([ms[m]["kappa_300K"] for m in ok], [EXP[m] for m in ok]).correlation)
lda = float(np.mean([abs(np.log10(ms[m]["kappa_300K"]/LDA[m])) for m in ok]))
rep = max(abs(ms2[m]["kappa_300K"]/ms[m]["kappa_300K"]-1) for m in ms) if len(ms2) == len(ms) == 15 else None
try:
    c25 = json.load(open(f"{D}/ctrl/mattersim_GaAs_m25.json"))["kappa_300K"]; c2 = abs(c25/ms["GaAs"]["kappa_300K"]-1)
except Exception: c2 = None
H = {"H1": {"valor": f"{w2}/15", "pasa": w2 >= 11}, "H2": {"valor": round(mal_ms, 3), "pasa": mal_ms <= 0.20},
     "H3": {"valor": round(rho, 3), "pasa": rho >= 0.85}, "H4": {"valor": [round(mal_ms,3), round(mal_mc,3)], "pasa": mal_ms < mal_mc},
     "H5": {"valor": round(float(np.median([10**x for x in lrc.values()])), 3), "pasa": float(np.median([10**x for x in lrc.values()])) < 1},
     "H6": {"valor": round(lda, 3), "pasa": lda <= 0.20},
     "H_REP": {"valor": rep, "pasa": rep is not None and rep <= 1e-6},
     "C1": {"valor": out["C1_excluidos_ms"], "pasa": len(ok) == 15}, "C2": {"valor": c2, "pasa": c2 is not None and c2 <= 0.05},
     "MACE_dentro_factor2": f"{w2c}/{len(lrc)}"}
core = all(H[k]["pasa"] for k in ["H1","H2","H3","H_REP","C1"])
nivel = "E3" if core else ("E2" if H["H_REP"]["pasa"] and any(H[k]["pasa"] for k in ["H1","H2","H3"]) else "E1")
out["hipotesis"] = H; out["nivel"] = nivel
json.dump(out, open(f"{S}/results.json", "w"), indent=1, ensure_ascii=False); print(json.dumps(out, indent=1, ensure_ascii=False))
