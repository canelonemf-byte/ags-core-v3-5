#!/usr/bin/env python3
"""C-UMF-001: evaluación frente a NIST-JANAF ΔfH°(0 K) con los criterios del prerregistro (sha256 c646ab82…b83a).
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os, re, sys, hashlib
import numpy as np
from scipy.stats import spearmanr
STORE = "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience"
KJ = 96.4853
JANAF = {"MgO": "C-MAT-003/refs/Mg-008.txt", "CaO": "C-MAT-003/refs/Ca-027.txt", "SrO": "C-MAT-004/refs/O-013.txt", "BeO": "C-MAT-003/refs/Be-044.txt",
 "Al2O3": "C-MAT-003/refs/Al-096.txt", "Li2O": "C-MAT-004/refs/Li-014.txt", "Na2O": "C-MAT-005/refs/Na-012.txt", "SiO2": "C-MAT-004/refs/O-037.txt",
 "TiO2": "C-MAT-004/refs/O-043.txt", "ZrO2": "C-MAT-005/refs/O-052.txt", "MgAl2O4": "C-MAT-004/refs/Al-089.txt", "BeAl2O4": "C-MAT-005/refs/Al-081.txt",
 "MgTiO3": "C-MAT-005/refs/Mg-015.txt", "ZrSiO4": "C-MAT-005/refs/O-072.txt", "LiF": "C-MAT-003/refs/F-021.txt", "NaF": "C-MAT-003/refs/F-033.txt",
 "KF": "C-MAT-005/refs/F-017.txt", "CaF2": "C-MAT-003/refs/Ca-014.txt", "SrF2": "C-MAT-005/refs/F-102.txt", "BaF2": "C-MAT-005/refs/Ba-019.txt",
 "MgF2": "C-MAT-004/refs/F-072.txt", "NaCl": "C-MAT-003/refs/Cl-053.txt", "KCl": "C-MAT-003/refs/Cl-036.txt", "LiCl": "C-MAT-005/refs/Cl-041.txt",
 "CsCl": "C-MAT-005/refs/Cl-005.txt", "KBr": "C-MAT-003/refs/Br-015.txt", "NaBr": "C-MAT-005/refs/Br-027.txt", "KI": "C-MAT-005/refs/I-004.txt",
 "AlN": "C-MAT-005/refs/Al-071.txt"}
MP2020 = {"O": -0.687, "F": -0.462, "Cl": -0.614, "Br": -0.534, "I": -0.379, "N": -0.361}
ANION = set(MP2020); MOLREF = {"O": "O2", "N": "N2", "F": "F2", "Cl": "Cl2", "Br": "Br2", "I": "I2"}

def comp(f):
    d = {}
    for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", f): d[el] = d.get(el, 0) + (int(n) if n else 1)
    return d

def janaf(m):
    p = os.path.join(STORE, JANAF[m]); txt = open(p).read(); h0 = h298 = None
    for ln in txt.splitlines():
        c = ln.split("\t")
        if c[0] == "0": h0 = float(c[5])
        if c[0] == "298.15": h298 = float(c[5])
    return h0, h298, hashlib.sha256(txt.encode()).hexdigest()

def dHf_model(r, m):
    c = r["compuestos"][m]; f = comp(m); nat = sum(f.values()); scale = c["n_atomos"] / nat
    e = c["E_total_eV"] / scale
    for el, n in f.items():
        e -= n * (r["moleculas"][MOLREF[el]]["E_por_atomo_eV"] if el in ANION else r["elementos"][el]["E_por_atomo_eV"])
    return e / nat, f, nat

def table(r):
    rows = {}
    for m in JANAF:
        h0, h298, sh = janaf(m); raw, f, nat = dHf_model(r, m)
        an = [el for el in f if el in ANION][0]; xa = f[an] / nat
        rows[m] = {"anion": an, "x_anion": xa, "exp0_eV_at": h0 / KJ / nat, "exp298_eV_at": h298 / KJ / nat, "raw_eV_at": raw,
                   "mp2020_eV_at": raw + MP2020[an] * xa, "sha256_janaf": sh}
    return rows

def fit(rows, keys):
    # mínimos cuadrados por anión: δ_X = media ponderada; error_i = raw_i + δ x_i − exp_i  → δ = Σ x(exp−raw)/Σ x²
    out = {}
    for an in {rows[k]["anion"] for k in keys}:
        ks = [k for k in keys if rows[k]["anion"] == an]
        x = np.array([rows[k]["x_anion"] for k in ks]); y = np.array([rows[k]["exp0_eV_at"] - rows[k]["raw_eV_at"] for k in ks])
        out[an] = float((x * y).sum() / (x * x).sum())
    return out

def evaluate(r):
    rows = table(r); loo_set = [k for k in rows if rows[k]["anion"] in ("O", "F", "Cl", "Br")]
    for k in loo_set:
        d = fit(rows, [j for j in loo_set if j != k]); rows[k]["loocv_eV_at"] = rows[k]["raw_eV_at"] + d[rows[k]["anion"]] * rows[k]["x_anion"]
    full = fit(rows, loo_set)
    err = lambda key, ks: np.array([rows[k][key] - rows[k]["exp0_eV_at"] for k in ks])
    ox = [k for k in rows if rows[k]["anion"] == "O"]
    raw_ox_perO = np.array([(rows[k]["raw_eV_at"] - rows[k]["exp0_eV_at"]) / rows[k]["x_anion"] for k in ox])
    e_loo = err("loocv_eV_at", loo_set); ofcn = [k for k in rows if rows[k]["anion"] in ("O", "F", "Cl", "N")]
    e_mp = err("mp2020_eV_at", ofcn)
    return rows, {
        "n_loocv": len(loo_set), "MAE_loocv_meV": float(np.abs(e_loo).mean() * 1e3), "maxabs_loocv_meV": float(np.abs(e_loo).max() * 1e3),
        "peor_loocv": loo_set[int(np.abs(e_loo).argmax())],
        "spearman_loocv": float(spearmanr([rows[k]["loocv_eV_at"] for k in loo_set], [rows[k]["exp0_eV_at"] for k in loo_set])[0]),
        "raw_oxidos_n_positivos": int((raw_ox_perO > 0).sum()), "raw_oxidos_media_eV_por_O": float(raw_ox_perO.mean()),
        "MAE_raw_OFClN_meV": float(np.abs(err("raw_eV_at", ofcn)).mean() * 1e3),
        "n_mp2020": len(ofcn), "MAE_mp2020_meV": float(np.abs(e_mp).mean() * 1e3), "maxabs_mp2020_meV": float(np.abs(e_mp).max() * 1e3),
        "MAE_mp2020_Br_I_desc_meV": float(np.abs(err("mp2020_eV_at", [k for k in rows if rows[k]["anion"] in ("Br", "I")])).mean() * 1e3),
        "delta_ajustado_eV": full, "delta_menos_mp2020_eV": {a: full[a] - MP2020[a] for a in full},
        "MAE_loocv_298_desc_meV": float(np.abs(np.array([rows[k]["loocv_eV_at"] - rows[k]["exp298_eV_at"] for k in loo_set])).mean() * 1e3)}

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "out"
    R = {}
    for run in ("run1", "run2"):
        for mdl in ("mattersim", "mace"):
            p = os.path.join(base, run, f"{mdl}.json")
            if os.path.exists(p): R[(run, mdl)] = json.load(open(p))
    res = {"meta": {"campana": "C-UMF-001", "prereg_sha256": open("prereg_C-UMF-001.sha256").read().split()[0]}, "modelos": {}}
    for mdl in ("mattersim", "mace"):
        rows, s = evaluate(R[("run1", mdl)]); r1 = R[("run1", mdl)]
        conv = all(v["convergio"] for g in ("compuestos", "elementos", "moleculas") for v in r1[g].values())
        dv = {m: v["V_A3"] / v["V0_A3"] - 1 for m, v in r1["compuestos"].items()}
        s["C1_convergencia"] = conv; s["C2_fuera_8pct"] = {m: round(x, 4) for m, x in dv.items() if abs(x) > 0.08}
        s["C3_Mg_hcp_menos_fcc_meV"] = (r1["elementos"]["Mg"]["E_por_atomo_eV"] - r1["control_C3"]["Mg_fcc_E_por_atomo_eV"]) * 1e3
        if ("run2", mdl) in R:
            r2 = R[("run2", mdl)]; rel = []
            for g in ("compuestos", "elementos", "moleculas"):
                for k, v in r1[g].items(): rel.append(abs(v["E_total_eV"] - r2[g][k]["E_total_eV"]) / abs(v["E_total_eV"]))
            s["rep_max_rel"] = float(max(rel))
        res["modelos"][mdl] = {"resumen": s, "filas": rows}
    ms, mc = res["modelos"]["mattersim"]["resumen"], res["modelos"]["mace"]["resumen"]
    v = {}
    v["H-F1"] = ms["raw_oxidos_n_positivos"] >= 12 and 0.40 <= ms["raw_oxidos_media_eV_por_O"] <= 1.00
    v["H-F2"] = ms["MAE_loocv_meV"] <= 60
    v["H-F3"] = ms["maxabs_loocv_meV"] <= 150
    v["H-F4"] = ms["MAE_loocv_meV"] <= mc["MAE_loocv_meV"]
    v["H-F5"] = all(abs(ms["delta_menos_mp2020_eV"][a]) <= 0.15 for a in ("O", "F", "Cl"))
    v["H-F6"] = ms["MAE_mp2020_meV"] <= 80
    v["H-F7"] = ms["spearman_loocv"] >= 0.95
    v["H-REP"] = ("rep_max_rel" in ms and "rep_max_rel" in mc and ms["rep_max_rel"] <= 1e-6 and mc["rep_max_rel"] <= 1e-6) if ("rep_max_rel" in ms and "rep_max_rel" in mc) else None
    v["C1"] = ms["C1_convergencia"] and mc["C1_convergencia"]; v["C3"] = ms["C3_Mg_hcp_menos_fcc_meV"] < 0
    res["veredictos"] = {k: ("PASA" if x else ("PENDIENTE" if x is None else "FALSADA")) for k, x in v.items()}
    json.dump(res, open("results.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res["veredictos"], indent=0)); print(json.dumps({"mattersim": ms, "mace": mc}, indent=1, ensure_ascii=False))
    for m, rw in res["modelos"]["mattersim"]["filas"].items():
        print(f'{m:8s} exp {rw["exp0_eV_at"]:7.3f} raw {rw["raw_eV_at"]:7.3f} mp {rw["mp2020_eV_at"]:7.3f} loo {rw.get("loocv_eV_at", float("nan")):7.3f}')

if __name__ == "__main__": main()
