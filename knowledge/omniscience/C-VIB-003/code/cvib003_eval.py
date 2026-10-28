#!/usr/bin/env python3
"""Evaluador congelado de C-VIB-003 (prereg sha256 66275ff6…ac1f). Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA (ORCID 0000-0001-8601-1963)."""
import json, os, numpy as np
from scipy.stats import spearmanr
D = "/workspace/omniscience_cvib003/out"; P = "/workspace/omniscience_cvib003/out_cvib002_run1"
S = "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-VIB-003"
EZB = {"BN":760,"BP":350,"AlP":90,"AlAs":98,"AlSb":56,"GaP":100,"GaAs":45,"GaSb":40,"InP":93,"InAs":30,"InSb":20,"ZnS":27,"ZnSe":19,"ZnTe":18,"CdTe":7.5}
RT = {"BN":1.120,"BP":1.061,"AlP":1.012,"AlAs":1.014,"AlSb":1.031,"GaP":1.216,"GaAs":1.035,"GaSb":1.022,"InP":1.154,"InAs":1.235,"InSb":1.095,"ZnS":1.177,"ZnSe":1.047,"ZnTe":1.027,"CdTe":1.062}
ERS = {"MgO":52,"CaO":30,"SrO":10,"BaO":3,"LiF":16.1,"NaF":18.5,"NaCl":7.2,"NaBr":2.9,"NaI":1.9,"KF":7.8,"KCl":7.2,"KBr":3.4,"KI":2.8,"RbCl":2.9,"PbS":2.5,"PbSe":1.6,"PbTe":2.2}
XIA = {"MgO":52.1,"CaO":21.3,"SrO":9.0,"BaO":2.8,"LiF":11.3,"NaF":20.6,"NaCl":7.2,"NaBr":2.9,"NaI":1.7,"KF":5.9,"KCl":6.6,"KBr":2.2,"KI":1.3,"RbCl":1.7,"PbS":1.3,"PbSe":1.1,"PbTe":1.6}
LOW = ["BaO","NaBr","NaI","KBr","KI","RbCl","PbS","PbSe","PbTe"]; L2 = np.log10(2)
def load(sub, mats, sc=2, mesh=19):
    r = {}
    for m in mats:
        f = f"{D}/{sub}/mattersim_{m}_sc{sc}_m{mesh}.json"
        if os.path.exists(f): r[m] = json.load(open(f))
    return r
def lg(x, y): return float(np.log10(x/y))
def H(v, p): return {"valor": v, "pasa": bool(p)}
out = {"prereg_sha256": "66275ff6e4483b5b28e0ffd6b0c502396c6e8271dc45c5f83f6588e1f8bbac1f"}
# Parte A
A = load("zb2", EZB); n = len(A); out["A_n"] = n
if n:
    out["A_kappa"] = {m: {"rta": round(v["kappa_rta"],2), "lbte": round(v["kappa_lbte"],2), "r": round(v["kappa_lbte"]/v["kappa_rta"],3), "fmin": round(v["fmin_THz"],3)} for m, v in A.items()}
    half = n >= 8
    h1 = sum(v["kappa_lbte"] >= v["kappa_rta"] for v in A.values())
    h2 = sum(abs(v["kappa_lbte"]/v["kappa_rta"] - RT[m]) <= 0.10 for m, v in A.items())
    mr = float(np.mean([abs(lg(v["kappa_rta"], EZB[m])) for m, v in A.items()])); ml = float(np.mean([abs(lg(v["kappa_lbte"], EZB[m])) for m, v in A.items()]))
    h4 = sum(abs(lg(v["kappa_lbte"], EZB[m])) <= L2 for m, v in A.items())
    out["A_H1"] = H(f"{h1}/15", h1 == 15); out["A_H2"] = H(f"{h2}/15", h2 >= 12)
    out["A_H3"] = H([round(ml,3), round(mr,3)], half and ml < mr); out["A_H4"] = H(f"{h4}/15", h4 >= 12)
    out["A_fuera_factor2_lbte"] = [m for m, v in A.items() if abs(lg(v["kappa_lbte"], EZB[m])) > L2]
    ca = []
    for m, v in A.items():
        f = f"{P}/mattersim_{m}_m19.json"
        if os.path.exists(f): ca.append(abs(v["kappa_rta"]/json.load(open(f))["kappa_300K"] - 1))
    out["CA"] = H(max(ca) if ca else None, len(ca) == 15 and max(ca) <= 1e-3)
# Parte B
B = load("zb3", ["BP","BN","ZnS","GaSb","InSb"], sc=3); out["B_n"] = len(B)
if B:
    out["B_kappa"] = {m: {"rta": round(v["kappa_rta"],2), "lbte": round(v["kappa_lbte"],2), "rta_3_sobre_2": round(v["kappa_rta"]/A[m]["kappa_rta"],3) if m in A else None, "fmin": round(v["fmin_THz"],3)} for m, v in B.items()}
b1 = sum(1 for m, v in B.items() if m in A and 0.85 <= v["kappa_rta"]/A[m]["kappa_rta"] <= 1.15)
out["B_H1"] = H(f"{b1}/5 (presentes {len(B)})", b1 >= 4)
b2 = [m for m in ["BN","BP"] if m in B and abs(B[m]["kappa_lbte"]/EZB[m]-1) <= 0.25]
out["B_H2"] = H(b2, len(b2) == 2)
b3 = [m for m in ["ZnS","GaSb","InSb"] if m in B and abs(lg(B[m]["kappa_lbte"], EZB[m])) <= L2]
out["B_H3"] = H(b3, len(b3) >= 2)
# Parte C
C = load("rs", ERS); out["C_n"] = len(C)
ok = {m: v for m, v in C.items() if v["fmin_THz"] > -0.05}
out["C1"] = H([m for m in ERS if m not in ok], len(ok) == 17)
if ok:
    out["C_kappa"] = {m: {"rta": round(v["kappa_rta"],3), "lbte": round(v["kappa_lbte"],3), "exp": ERS[m], "ratio_rta": round(v["kappa_rta"]/ERS[m],3), "a": round(v["a_relajada"],4), "fmin": round(v["fmin_THz"],3)} for m, v in C.items()}
    lr = {m: lg(v["kappa_rta"], ERS[m]) for m, v in ok.items()}
    c1 = sum(abs(x) <= L2 for x in lr.values()); out["C_H1"] = H(f"{c1}/17", c1 >= 12)
    c2 = float(np.mean(np.abs(list(lr.values())))); out["C_H2"] = H(round(c2,3), len(ok) >= 9 and c2 <= 0.20)
    rho = float(spearmanr([ok[m]["kappa_rta"] for m in ok], [ERS[m] for m in ok]).correlation); out["C_H3"] = H(round(rho,3), len(ok) >= 9 and rho >= 0.85)
    lo = [m for m in LOW if m in ok]; w = sum(abs(lr[m]) <= L2 for m in lo); ml = float(np.mean([abs(lr[m]) for m in lo])) if lo else None
    out["C_H4"] = H({"factor2": f"{w}/9", "media_log10": round(ml,3) if ml is not None else None}, w >= 6 and ml is not None and ml <= 0.25)
    c5 = float(np.mean([abs(lg(v["kappa_rta"], XIA[m])) for m, v in ok.items()])); out["C_H5"] = H(round(c5,3), len(ok) >= 9 and c5 <= 0.20)
    med = float(np.median([10**lr[m] for m in lo])) if lo else None; out["C_H6"] = H(round(med,3) if med else None, med is not None and len(lo) >= 5 and med < 1)
    c7 = float(np.median([v["kappa_lbte"]/v["kappa_rta"] for v in ok.values()])); out["C_H7"] = H(round(c7,3), len(ok) >= 9 and c7 <= 1.10)
    out["C_fuera_factor2"] = {m: round(10**x,3) for m, x in lr.items() if abs(x) > L2}
R = load("rs_rep", ["PbTe","NaCl","KBr"]); rep = []
for m, v in R.items():
    if m in C: rep += [abs(v["kappa_rta"]/C[m]["kappa_rta"]-1), abs(v["kappa_lbte"]/C[m]["kappa_lbte"]-1)]
out["H_REP"] = H(max(rep) if rep else None, len(R) == 3 and len(rep) == 6 and max(rep) <= 1e-6)
try:
    c25 = load("rs_ctrl", ["PbTe"], mesh=25)["PbTe"]["kappa_rta"]; cc = abs(c25/C["PbTe"]["kappa_rta"]-1); out["C2"] = H(round(cc,4), cc <= 0.05)
except Exception: out["C2"] = H(None, False)
g = lambda k: out.get(k, {}).get("pasa", False)
core = all(g(k) for k in ["C_H1","C_H2","C_H3","C_H4","H_REP","C1"])
out["nivel_UM-25"] = "E3" if core else ("E2" if g("H_REP") and any(g(k) for k in ["C_H1","C_H2","C_H3","C_H4"]) else "E1")
out["nivel_UM-12"] = "E3" if g("CA") else "E3 en revisión"
os.makedirs(S, exist_ok=True)
json.dump(out, open(f"{S}/results.json", "w"), indent=1, ensure_ascii=False); print(json.dumps(out, indent=1, ensure_ascii=False))
