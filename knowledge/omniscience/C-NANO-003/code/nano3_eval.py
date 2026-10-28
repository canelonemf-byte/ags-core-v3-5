#!/usr/bin/env python3
"""C-NANO-003: evaluación tal cual el prerregistro (escribe ../results.json). Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA (ORCID 0000-0001-8601-1963)."""
import json, os, numpy as np
H = os.path.dirname(os.path.abspath(__file__)) + "/.."; MEV = 8.065544; TOL = 0.05
MONO = ["grafeno", "hBN", "MoS2", "WS2", "MoSe2"]; PAR = {"grafeno": "grafito", "hBN": "hBN_bulk", "MoS2": "MoS2_2H"}
REF_RAMAN = {("WS2", "E'"): 356.0, ("WS2", "A1'"): 418.0, ("MoSe2", "E'"): 288.0, ("MoSe2", "A1'"): 242.0}
REF_IXS = {"M_ZA": 60.0 * MEV, "M_TA/ZO_bajo": 77.8 * MEV, "M_TA/ZO_alto": 78.1 * MEV, "M_LA": 160.0 * MEV, "M_LO": 166.2 * MEV, "M_TO": 173.4 * MEV,
           "K_ZA": 67.2 * MEV, "K_ZO": 67.2 * MEV, "K_TA": 124.9 * MEV, "K_LA/LO": 151.0 * MEV}
JANAF = {"grafito": 5.740 / 8.314462618, "hBN_bulk": 14.795 / 8.314462618 / 2}
def L(p):
    f = f"{H}/{p}"; return json.load(open(f)) if os.path.exists(f) else None
def mid(r): return list(r["por_amplitud"].values())[1]
def gam_tmd(x):
    G = sorted(x["G"], key=lambda y: abs(y["nu_cm"]))[3:]; z = sorted([y for y in G if y["frac_z"] > 0.5], key=lambda y: y["peso_Mo"]); p = sorted([y for y in G if y["frac_z"] <= 0.5], key=lambda y: y["peso_Mo"])
    return {"A1'": z[0]["nu_cm"], "A2''": z[1]["nu_cm"], "E''": float(np.mean([y["nu_cm"] for y in p[:2]])), "E'": float(np.mean([y["nu_cm"] for y in p[2:]]))}
def mk(x):
    o = {}
    for P in "MK":
        z = sorted(y["nu_cm"] for y in x[P] if y["frac_z"] > 0.5); p = sorted(y["nu_cm"] for y in x[P] if y["frac_z"] <= 0.5)
        o[f"{P}_ZA"], o[f"{P}_ZO"], o[f"{P}_TA"] = z[0], z[-1], p[0]
        if P == "M": o["M_LA"], o["M_LO"], o["M_TO"] = p[1], p[2], p[3]
        else: o["K_LA/LO"] = float(np.mean(p[1:3])); o["K_TO"] = p[3]
    tz = sorted([o["M_TA"], o["M_ZO"]]); o["M_TA/ZO_bajo"], o["M_TA/ZO_alto"] = tz; return o
def comp(c, ref):
    t = {(f"{k[0]}|{k[1]}" if isinstance(k, tuple) else k): {"calc": c[k], "ref": v, "err_rel": (c[k] - v) / v, "dentro": abs(c[k] - v) / v <= TOL} for k, v in ref.items()}
    return t, sum(not y["dentro"] for y in t.values())
def evalua(run):
    R = {}; mo = {m: L(f"out/{run}/mattersim/{m}.json") for m in MONO}; bk = {b: L(f"out/{run}/mattersim_d3_95/{b}.json") for b in PAR.values()}
    za = {}
    for m in MONO:
        ns = [v["ZA"]["exponente"] for v in mo[m]["por_amplitud"].values()]; ok = all(n is not None for n in ns)
        za[m] = {"n_por_amp": ns, "n_med": float(np.median(ns)) if ok else None, "dispersion": float(max(ns) - min(ns)) if ok else None}
    R["ZA"] = za; R["H1"] = all(v["n_med"] is not None and 1.8 <= v["n_med"] <= 2.2 and v["dispersion"] <= 0.10 for v in za.values())
    g = {}; [g.update({(m, k): v for k, v in gam_tmd(mid(mo[m])).items()}) for m in ("WS2", "MoSe2", "MoS2")]
    R["gamma_tmd"] = {f"{k[0]}|{k[1]}": v for k, v in g.items()}; R["H2_tabla"], n2 = comp(g, REF_RAMAN); R["H2"] = n2 == 0; R["H2_n_fuera"] = n2
    m_ = mk(mid(mo["grafeno"])); R["MK_grafeno"] = m_; R["H3_tabla"], n3 = comp(m_, REF_IXS); R["H3"] = n3 <= 2; R["H3_n_fuera"] = n3
    R["inf_K_TO_vs_MS"] = m_["K_TO"]
    n2r = L("../omniscience_cnano002/results.json") or {}; S = {}
    for m, b in PAR.items():
        sm, sb = mid(mo[m]), bk[b]; ok = sb and sb.get("clase") in ("normal", "evaluable_con_regla") and sm.get("clase") in ("normal", "evaluable_con_regla")
        d95 = sm["S298_kB_at"] - sb["S298_kB_at"] if ok else None; d40 = n2r.get(run, {}).get("S", {}).get(m, {}).get("dS")
        S[m] = {"S_mono": sm["S298_kB_at"], "S_bulk_d3_95": sb["S298_kB_at"] if sb else None, "clase_bulk": sb.get("clase") if sb else None, "c_bulk_95": sb.get("c_A") if sb else None,
                "dS_95": d95, "dS_40_CNANO002": d40, "dif_95_40": None if (d95 is None or d40 is None) else abs(d95 - d40)}
    R["S"] = S; R["H4"] = all(v["dif_95_40"] is not None and v["dif_95_40"] <= 0.02 for v in S.values()); R["H5"] = all(v["dS_95"] is not None and 0.05 <= v["dS_95"] <= 0.6 for v in S.values())
    R["C3_tabla"] = {b: {"S_calc": bk[b]["S298_kB_at"], "S_janaf": s, "err_rel": (bk[b]["S298_kB_at"] - s) / s} for b, s in JANAF.items() if bk[b] and "S298_kB_at" in bk[b]}
    R["C3"] = len(R["C3_tabla"]) == 2 and all(abs(v["err_rel"]) <= 0.10 for v in R["C3_tabla"].values())
    return R, g, m_
if __name__ == "__main__":
    out = {}; r1, g1, m1 = evalua("run1"); r2, g2, m2 = evalua("run2"); out["run1"], out["run2"] = r1, r2
    fr = [abs(g2[k] - g1[k]) / abs(g1[k]) for k in g1] + [abs(m2[k] - m1[k]) / abs(m1[k]) for k in m1]
    dn = [abs(r2["ZA"][m]["n_med"] - r1["ZA"][m]["n_med"]) for m in MONO if r1["ZA"][m]["n_med"] is not None and r2["ZA"][m]["n_med"] is not None]
    dS = [abs(r2["S"][m]["dS_95"] - r1["S"][m]["dS_95"]) for m in PAR if r1["S"][m]["dS_95"] is not None and r2["S"][m]["dS_95"] is not None]
    ver = all(r1[h] == r2[h] for h in ["H1", "H2", "H3", "H4", "H5"])
    out["H_REP"] = {"max_dfrec_rel": max(fr), "max_dn_med": max(dn) if dn else None, "n_eval": len(dn), "max_d_dS": max(dS) if dS else None, "dS_eval": len(dS), "veredictos_iguales": ver,
                    "pasa": max(fr) <= 0.01 and len(dn) == 5 and max(dn) <= 0.10 and len(dS) == 3 and max(dS) <= 0.02 and ver}
    gp = L("out/gpaw/gpaw_WS2_gamma.json")
    if gp:
        G = sorted(gp["modos"], key=lambda y: abs(y["nu_cm"]))[3:]; z = sorted([y for y in G if y["frac_z"] > 0.5], key=lambda y: y["peso_Mo"]); p = sorted([y for y in G if y["frac_z"] <= 0.5], key=lambda y: y["peso_Mo"])
        gw = {"A1'": z[0]["nu_cm"], "E'": float(np.mean([y["nu_cm"] for y in p[2:]]))}
        c1 = {k: {"gpaw": gw[k], "ms": g1[("WS2", k)], "err_rel": (g1[("WS2", k)] - gw[k]) / gw[k]} for k in gw}
        out["C1"] = {"tabla": c1, "pasa": all(abs(v["err_rel"]) <= 0.05 for v in c1.values())}
    else: out["C1"] = {"pasa": None, "nota": "NO EVALUABLE"}
    old = (L("../omniscience_cnano002/out/run1/mattersim/MoS2.json") or {})
    if old:
        o = gam_tmd(old); c2 = {k: abs(g1[("MoS2", k)] - o[k]) / o[k] for k in o}; out["C2"] = {"dif_rel": c2, "pasa": max(c2.values()) <= 0.005}
    rep = out["H_REP"]["pasa"]
    out["nivel_NANO_04"] = "E3" if rep and out["C1"]["pasa"] else ("E2" if rep else "E1")
    out["nivel_NANO_05"] = "E3" if rep and r1["C3"] else ("E2" if rep else "E1")
    json.dump(out, open(f"{H}/results.json", "w"), indent=1, default=str)
    for h in ["H1", "H2", "H3", "H4", "H5", "C3"]: print(h, "PASA" if r1[h] else "FALLA", "| run2:", "PASA" if r2[h] else "FALLA")
    print("H_REP", out["H_REP"]); print("C1", out["C1"]); print("C2", out.get("C2")); print("niveles", out["nivel_NANO_04"], out["nivel_NANO_05"])
