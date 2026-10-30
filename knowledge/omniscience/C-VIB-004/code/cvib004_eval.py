#!/usr/bin/env python3
"""Evaluador congelado de C-VIB-004. Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA (ORCID 0000-0001-8601-1963)."""
import json, os, sys, hashlib, numpy as np
from scipy.stats import spearmanr
D = "/workspace/omniscience_cvib004/out"; S = "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience"
P3 = f"{S}/C-VIB-003/out/rs"; PR = f"{S}/C-VIB-004/prereg_C-VIB-004.md"
ERS = {"MgO":52,"CaO":30,"SrO":10,"BaO":3,"LiF":16.1,"NaF":18.5,"NaCl":7.2,"NaBr":2.9,"NaI":1.9,"KF":7.8,"KCl":7.2,"KBr":3.4,"KI":2.8,"RbCl":2.9,"PbS":2.5,"PbSe":1.6,"PbTe":2.2}
XIA = {"MgO":52.1,"CaO":21.3,"SrO":9.0,"BaO":2.8,"LiF":11.3,"NaF":20.6,"NaCl":7.2,"NaBr":2.9,"NaI":1.7,"KF":5.9,"KCl":6.6,"KBr":2.2,"KI":1.3,"RbCl":1.7,"PbS":1.3,"PbSe":1.1,"PbTe":1.6}
LOW = ["BaO","NaBr","NaI","KBr","KI","RbCl","PbS","PbSe","PbTe"]; L2 = np.log10(2); N = len(ERS)
def ld(sub, m, tag="aexp", mesh=19, d=0.03):
    f = f"{D}/{sub}/mattersim_{m}_{tag}_sc2_m{mesh}_d{d:.3f}.json"
    return json.load(open(f)) if os.path.exists(f) else None
def lg(x, y): return float(np.log10(x/y))
def H(v, p): return {"valor": v, "pasa": bool(p)}
out = {"prereg_sha256": hashlib.sha256(open(PR,"rb").read()).hexdigest()}
A = {m: v for m in ERS if (v := ld("A", m)) is not None}; out["A_n"] = len(A)
R3 = {m: json.load(open(f"{P3}/mattersim_{m}_sc2_m19.json")) for m in ERS}
out["A_kappa"] = {m: {"k_aexp": round(v["kappa_rta"],3), "k_arel_cvib003": round(R3[m]["kappa_rta"],3), "exp": ERS[m], "ratio_exp": round(v["kappa_rta"]/ERS[m],3),
                      "ratio_aexp_arel": round(v["kappa_rta"]/R3[m]["kappa_rta"],3), "a_exp": v["a_usada"], "a_rel": round(R3[m]["a_relajada"],4), "P_GPa": round(v["presion_GPa"],3), "fmin": round(v["fmin_THz"],3)} for m, v in A.items()}
ok = {m: v for m, v in A.items() if v["fmin_THz"] > -0.05}
out["C1"] = H({"fallan_o_ausentes": [m for m in ERS if m not in ok]}, len(ok) == N)
half = len(ok) > N/2
lr = {m: lg(v["kappa_rta"], ERS[m]) for m, v in ok.items()}
h1 = sum(abs(x) <= L2 for x in lr.values()); out["H1"] = H(f"{h1}/17", h1 >= 12)
h2 = float(np.mean(np.abs(list(lr.values())))) if lr else None; out["H2"] = H(round(h2,3) if h2 is not None else None, half and h2 <= 0.20)
rho = float(spearmanr([ok[m]["kappa_rta"] for m in ok], [ERS[m] for m in ok]).correlation) if len(ok) > 2 else None
out["H3"] = H(round(rho,3) if rho is not None else None, half and rho >= 0.85)
lo = [m for m in LOW if m in ok]; w = sum(abs(lr[m]) <= L2 for m in lo); ml = float(np.mean([abs(lr[m]) for m in lo])) if lo else None
out["H4"] = H({"factor2": f"{w}/9", "media_log10": round(ml,3) if ml is not None else None}, len(lo) > 4 and w >= 6 and ml <= 0.25)
rr = [A[m]["kappa_rta"]/R3[m]["kappa_rta"] for m in A]; n5 = sum(x > 1 for x in rr); med5 = float(np.median(rr)) if rr else None
out["H5"] = H({"mayor_que_1": f"{n5}/17", "mediana": round(med5,3) if med5 else None}, len(A) > N/2 and n5 >= 15 and med5 > 1.2)
med6 = float(np.median([10**lr[m] for m in lo])) if lo else None; out["H6"] = H(round(med6,3) if med6 else None, len(lo) > 4 and med6 >= 0.50)
c7 = float(np.mean([abs(lg(v["kappa_rta"], XIA[m])) for m, v in ok.items()])) if ok else None; out["H7"] = H(round(c7,3) if c7 is not None else None, half and c7 <= 0.20)
out["fuera_factor2"] = {m: round(10**x,3) for m, x in lr.items() if abs(x) > L2}
bl = ["KBr","KI","RbCl","NaI","PbTe"]; bv = {}
for m in bl:
    v = ld("B", m, d=0.01)
    if v is not None and m in A: bv[m] = round(v["kappa_rta"]/A[m]["kappa_rta"], 4)
nb = sum(abs(x-1) <= 0.10 for x in bv.values()); out["B_H1"] = H({"cocientes": bv, "pasan": f"{nb}/5"}, len(bv) >= 3 and nb >= 4)
rep = []
for m in ["PbTe","NaCl","KBr"]:
    v = ld("REP", m)
    if v is not None and m in A: rep.append(abs(v["kappa_rta"]/A[m]["kappa_rta"]-1))
out["H_REP"] = H(max(rep) if rep else None, len(rep) == 3 and max(rep) <= 1e-6)
v25 = ld("C2", "PbTe", mesh=25)
out["C2"] = H(round(v25["kappa_rta"]/A["PbTe"]["kappa_rta"]-1, 4) if (v25 and "PbTe" in A) else None, bool(v25 and "PbTe" in A and abs(v25["kappa_rta"]/A["PbTe"]["kappa_rta"]-1) <= 0.05))
ca = {}
for m in ["NaCl","KBr"]:
    v = ld("CA", m, tag="arel")
    if v is not None: ca[m] = abs(v["kappa_rta"]/R3[m]["kappa_rta"]-1)
out["CA"] = H(ca, len(ca) == 2 and max(ca.values()) <= 1e-3)
g = lambda k: out[k]["pasa"]
if all(g(k) for k in ["H1","H2","H3","H4","H_REP","C1","CA"]): lvl = "E3"
elif g("H_REP") and any(g(k) for k in ["H1","H2","H3","H4"]): lvl = "E2"
else: lvl = "E1"
out["nivel_UM-25"] = lvl
dst = sys.argv[1] if len(sys.argv) > 1 else f"{S}/C-VIB-004/results.json"
json.dump(out, open(dst, "w"), indent=1, ensure_ascii=False); print(json.dumps(out, indent=1, ensure_ascii=False))
