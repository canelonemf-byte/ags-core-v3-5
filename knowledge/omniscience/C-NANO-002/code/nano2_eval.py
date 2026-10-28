#!/usr/bin/env python3
"""C-NANO-002: evaluación tal cual el prerregistro. Uso: python nano2_eval.py > ../eval.log   (escribe ../results.json)
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA (ORCID 0000-0001-8601-1963)."""
import json, os, numpy as np
H = os.path.dirname(os.path.abspath(__file__)) + "/.."; KB = 1.0
REF_G = {("grafeno", "ZO"): 881, ("grafeno", "LO/TO"): 1554, ("hBN", "ZO"): 819.37, ("hBN", "LO/TO"): 1363.88,
         ("MoS2", "E''"): 289.2, ("MoS2", "E'"): 391.7, ("MoS2", "A1'"): 410.3, ("MoS2", "A2''"): 476.0}
REF_MK = {"M_ZA": 471, "M_TA": 626, "M_ZO": 635, "M_LA": 1328, "M_LO": 1340, "M_TO": 1390, "K_ZA": 535, "K_TA": 997, "K_LA/LO": 1213}
REF_INF = {"K_TO": 1288}
REF_EXP = {("grafeno", "LO/TO"): 1580, ("hBN", "LO/TO"): 1368, ("MoS2", "E'"): 384}
JANAF = {"grafito": 5.740 / 8.314462618, "hBN_bulk": 14.795 / 8.314462618 / 2}
PAR = {"grafeno": "grafito", "hBN": "hBN_bulk", "MoS2": "MoS2_2H"}
TOL = 0.05

def load(run, tag, m):
    f = f"{H}/out/{run}/{tag}/{m}.json"; return json.load(open(f)) if os.path.exists(f) else None

def gamma_modos(r):
    G = sorted(r["G"], key=lambda x: abs(x["nu_cm"])); opt = sorted(G[3:], key=lambda x: x["nu_cm"]); out = {}
    if r["material"] in ("grafeno", "hBN"):
        z = [x for x in opt if x["frac_z"] > 0.5]; p = [x for x in opt if x["frac_z"] <= 0.5]
        out["ZO"] = z[0]["nu_cm"]; out["LO/TO"] = float(np.mean([x["nu_cm"] for x in p]))
    else:
        z = sorted([x for x in opt if x["frac_z"] > 0.5], key=lambda x: x["peso_Mo"]); p = sorted([x for x in opt if x["frac_z"] <= 0.5], key=lambda x: x["peso_Mo"])
        out["A1'"] = z[0]["nu_cm"]; out["A2''"] = z[1]["nu_cm"]
        out["E''"] = float(np.mean([x["nu_cm"] for x in p[:2]])); out["E'"] = float(np.mean([x["nu_cm"] for x in p[2:]]))
    return out

def mk_modos(r):
    o = {}
    for P in ["M", "K"]:
        L = r[P]; z = sorted([x["nu_cm"] for x in L if x["frac_z"] > 0.5]); p = sorted([x["nu_cm"] for x in L if x["frac_z"] <= 0.5])
        o[f"{P}_ZA"] = z[0]; o[f"{P}_ZO"] = z[-1]; o[f"{P}_TA"] = p[0]
        if P == "M": o["M_LA"], o["M_LO"], o["M_TO"] = p[1], p[2], p[3]
        else: o["K_LA/LO"] = float(np.mean(p[1:3])); o["K_TO"] = p[3]
    return o

def comp(calc, ref):
    rows = {f"{k[0]}|{k[1]}" if isinstance(k, tuple) else k: {"calc": calc[k], "ref": v, "err_rel": (calc[k] - v) / v, "dentro": abs(calc[k] - v) / v <= TOL} for k, v in ref.items()}
    return rows, sum(not x["dentro"] for x in rows.values())

def evalua(run, tag="mattersim"):
    R = {}; mono = {m: load(run, tag, m) for m in PAR}; bD3 = {b: load(run, "mattersim_d3", b) for b in PAR.values()}; b0 = {b: load(run, "mattersim", b) for b in PAR.values()}
    g = {}; [g.update({(m, k): v for k, v in gamma_modos(mono[m]).items()}) for m in PAR]
    R["H1_tabla"], n1 = comp(g, REF_G); R["H1"] = n1 <= 2; R["H1_n_fuera"] = n1
    mk = mk_modos(mono["grafeno"]); R["H2_tabla"], n2 = comp(mk, REF_MK); R["H2"] = n2 <= 2; R["H2_n_fuera"] = n2
    R["inf_K_TO"] = comp(mk, REF_INF)[0]
    R["H3_tabla"], n3 = comp(g, REF_EXP); R["H3"] = n3 == 0; R["H3_n_fuera"] = n3
    R["ZA"] = {m: mono[m]["ZA"]["exponente"] for m in PAR}; R["H4"] = all(e is not None and 1.8 <= e <= 2.2 for e in R["ZA"].values())
    if tag != "mattersim": return R, g, mk
    S = {}
    for m, b in PAR.items():
        sm, sb, s0 = mono[m], bD3[b], b0[b]
        ok = all(x and x.get("clase") in ("normal", "evaluable_con_regla") for x in (sm, sb, s0))
        dS = sm["S298_kB_at"] - sb["S298_kB_at"] if ok else None; dS0 = sm["S298_kB_at"] - s0["S298_kB_at"] if ok else None
        S[m] = {"S_mono": sm["S298_kB_at"], "clase_mono": sm["clase"], "f_imag_mono": sm["f_imag"], "S_bulk_d3": sb["S298_kB_at"], "clase_bulk_d3": sb["clase"],
                "S_bulk_sinD3": s0["S298_kB_at"], "clase_bulk_sinD3": s0["clase"], "c_bulk_d3": sb["c_A"], "c_bulk_sinD3": s0["c_A"],
                "dS": dS, "dS_sinD3": dS0, "efecto_D3": None if dS is None else abs(dS - dS0)}
    R["S"] = S; R["H5"] = all(v["dS"] is not None and 0.05 <= v["dS"] <= 0.6 for v in S.values())
    R["H6"] = all(v["efecto_D3"] is not None and v["efecto_D3"] < 0.1 for v in S.values())
    R["C3_tabla"] = {b: {"S_calc": bD3[b]["S298_kB_at"], "S_janaf": s, "err_rel": (bD3[b]["S298_kB_at"] - s) / s} for b, s in JANAF.items()}
    R["C3"] = all(abs(v["err_rel"]) <= 0.10 for v in R["C3_tabla"].values())
    return R, g, mk

if __name__ == "__main__":
    out = {}; r1, g1, mk1 = evalua("run1"); r2, g2, mk2 = evalua("run2"); out["run1"] = r1; out["run2"] = r2
    fr = [abs(g2[k] - g1[k]) / abs(g1[k]) for k in g1] + [abs(mk2[k] - mk1[k]) / abs(mk1[k]) for k in mk1]
    dza = [abs(r2["ZA"][m] - r1["ZA"][m]) for m in PAR if r1["ZA"][m] is not None and r2["ZA"][m] is not None]
    dS = [abs(r2["S"][m][k] - r1["S"][m][k]) for m in PAR for k in ("S_mono", "S_bulk_d3", "S_bulk_sinD3")]
    ver = all(r1[h] == r2[h] for h in ["H1", "H2", "H3", "H4", "H5", "H6"])
    out["H_REP"] = {"max_dfrec_rel": max(fr), "max_dZA": max(dza) if dza else None, "za_ok": len(dza) == 3, "max_dS": max(dS), "veredictos_iguales": ver,
                    "pasa": max(fr) <= 0.01 and len(dza) == 3 and max(dza) <= 0.1 and max(dS) <= 0.02 and ver}
    if os.path.exists(f"{H}/out/run1/mace/MoS2.json"):
        rm, gm, mkm = evalua("run1", "mace"); out["C2_mace"] = rm
    gp = f"{H}/out/gpaw/gpaw_grafeno_gamma.json"
    if os.path.exists(gp):
        G = json.load(open(gp))["modos"]; Gs = sorted(G, key=lambda x: abs(x["nu_cm"]))[3:]
        zo = [x["nu_cm"] for x in Gs if x["frac_z"] > 0.5][0]; lt = float(np.mean([x["nu_cm"] for x in Gs if x["frac_z"] <= 0.5]))
        c1 = {"ZO": {"gpaw": zo, "ms": g1[("grafeno", "ZO")]}, "LO/TO": {"gpaw": lt, "ms": g1[("grafeno", "LO/TO")]}}
        for v in c1.values(): v["err_rel"] = (v["ms"] - v["gpaw"]) / v["gpaw"]
        out["C1"] = {"tabla": c1, "pasa": all(abs(v["err_rel"]) <= 0.05 for v in c1.values())}
    else: out["C1"] = {"pasa": None, "nota": "NO EVALUABLE"}
    rep, c1, c3 = out["H_REP"]["pasa"], out["C1"]["pasa"], r1["C3"]
    out["nivel_NANO_04"] = "E3" if rep and c1 else ("E2" if rep else "E1")
    out["nivel_NANO_05"] = "E3" if rep and c3 else ("E2" if rep else "E1")
    json.dump(out, open(f"{H}/results.json", "w"), indent=1, default=str)
    for h in ["H1", "H2", "H3", "H4", "H5", "H6", "C3"]: print(h, "PASA" if r1[h] else "FALLA", "| run2:", "PASA" if r2[h] else "FALLA")
    print("H_REP", out["H_REP"]); print("C1", out["C1"]); print("niveles", out["nivel_NANO_04"], out["nivel_NANO_05"])
