#!/usr/bin/env python3
"""Evaluador congelado C-VIB-005 (barrido ±1 % de a_exp). Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA (ORCID 0000-0001-8601-1963)."""
import json, glob, math, numpy as np
B4 = json.load(open("/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-VIB-004/results.json"))["A_kappa"]
M = "KBr KI RbCl NaI NaBr BaO PbS PbSe PbTe NaCl MgO".split()
def ld(d, m, s, disp=0.03):
    f = glob.glob(f"out/{d}/mattersim_{m}_aexp{s:.3f}_sc2_m19_d{disp:.3f}.json"); return json.load(open(f[0])) if f else None
R = {}; TH = -0.05
for m in M:
    lo, hi = ld("V099", m, 0.99), ld("V101", m, 1.01); k0 = B4[m]["k_aexp"]; f0 = B4[m]["fmin"]; ex = B4[m]["exp"]
    r = {"exp": ex, "k100": k0, "fmin100": f0}
    if lo: r.update(k099=lo["kappa_rta"], fmin099=lo["fmin_THz"], P099=lo["presion_GPa"])
    if hi: r.update(k101=hi["kappa_rta"], fmin101=hi["fmin_THz"], P101=hi["presion_GPa"])
    if lo and hi:
        r["monotono"] = bool(lo["kappa_rta"] > k0 > hi["kappa_rta"])
        r["g"] = -(math.log(hi["kappa_rta"]) - math.log(lo["kappa_rta"])) / (3*(math.log(1.01) - math.log(0.99)))
        r["estable_3"] = bool(min(lo["fmin_THz"], f0, hi["fmin_THz"]) > TH)
        x = np.log([0.99, 1.0, 1.01]); y = np.log([lo["kappa_rta"], k0, hi["kappa_rta"]]); c1, c0 = np.polyfit(x, y, 1)
        r["dlnk_dlna"] = float(c1); r["da_needed_pct"] = float(100*(math.exp((math.log(ex) - c0)/c1) - 1)) if c1 != 0 else None
    R[m] = r
out = {"materiales": R}
n_mono = sum(1 for m in M if R[m].get("monotono")); out["H1"] = {"n": n_mono, "de": len(M), "pasa": n_mono >= 10}
G = [R[m]["g"] for m in M if R[m].get("estable_3") and "g" in R[m]]
nG = sum(1 for g in G if 2 <= g <= 20); out["H4"] = {"n_en_rango": nG, "de": len(G), "pasa": len(G) >= 6 and nG >= math.ceil(0.8*len(G)), "g_mediana": float(np.median(G)) if G else None}
H3 = {m: R[m].get("da_needed_pct") for m in ["NaI", "KBr", "RbCl"]}
nH3 = sum(1 for v in H3.values() if v is not None and v < -1.0); out["H3"] = {"da_needed_pct": H3, "n_mas_de_1pct": nH3, "pasa": nH3 >= 2}
ki, kib = ld("V099", "KI", 0.99), ld("B", "KI", 0.99, 0.01)
if ki and kib:
    rr = kib["kappa_rta"]/ki["kappa_rta"]
    ok = ki["fmin_THz"] > TH and kib["fmin_THz"] > TH and abs(rr-1) <= 0.10 and ki["kappa_rta"]/B4["KI"]["exp"] >= 0.25
    out["H2_KI"] = {"fmin_d003": ki["fmin_THz"], "fmin_d001": kib["fmin_THz"], "ratio_d": rr, "k_sobre_exp": ki["kappa_rta"]/B4["KI"]["exp"], "pasa": bool(ok)}
else: out["H2_KI"] = {"pasa": False, "nota": "ausente"}
ca = ld("CA", "NaCl", 1.0)
out["CA"] = {"ratio_m1": (ca["kappa_rta"]/B4["NaCl"]["k_aexp"] - 1) if ca else None, "pasa": bool(ca and abs(ca["kappa_rta"]/B4["NaCl"]["k_aexp"] - 1) <= 1e-3)}
e2 = out["CA"]["pasa"] and out["H1"]["pasa"] and out["H4"]["pasa"]
out["UM-26"] = {"nivel": "E2" if e2 else "E1", "enunciado": ("a: con MatterSim-v1 la subestimación residual de κL en NaI/KBr/RbCl a a_exp NO se corrige con ≤1 % de compresión de red (ablandamiento intrínseco)" if out["H3"]["pasa"] else "b: la subestimación residual de κL en NaI/KBr/RbCl a a_exp se corrige con ≤1 % de compresión de red (dominada por volumen)")}
json.dump(out, open("results.json", "w"), indent=1, ensure_ascii=False); print(json.dumps(out, indent=1, ensure_ascii=False))
