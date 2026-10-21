#!/usr/bin/env python3
"""C-UMF-002: evaluación con los criterios congelados (prereg sha256 be01fb96…).
Uso: python cumf002_eval.py out/run1 [out/run2]
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os, re, sys, glob, hashlib
import numpy as np
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDEntry
from pymatgen.core import Composition
sys.path.insert(0, "/workspace/omniscience_cumf001/code"); import cumf001_eval as e1
STORE = e1.STORE; KJ = e1.KJ; HERE = os.path.dirname(os.path.abspath(__file__)); REFS = os.path.join(HERE, "..", "refs")
JAN = {k: os.path.join(STORE, v) for k, v in e1.JANAF.items()}
NEW = {"NaI": "I-015", "SrCl2": "Cl-119", "BaO": "Ba-034", "TiN": "N-014", "Ti2O3": "O-059", "TiO2_anatasa": "O-042", "MgCl2": "Cl-093",
       "ZrN": "N-019", "CaI2": "Ca-023", "LiBr": "Br-019", "LiI": "I-008", "CsF": "Cs-008", "MgBr2": "Br-057"}
JAN.update({k: os.path.join(REFS, v + ".txt") for k, v in NEW.items()})
MP = e1.MP2020; ANION = set(MP); MOLREF = e1.MOLREF
TI_TRAIN = ["TiN", "Ti2O3"]; TI_TEST = ["TiO2", "TiO2_anatasa", "MgTiO3"]

def formula(m): return e1.comp("TiO2" if m == "TiO2_anatasa" else m)

def janaf(m):
    txt = open(JAN[m]).read(); h0 = h298 = None
    for ln in txt.splitlines():
        c = ln.split("\t")
        if c[0] == "0" and len(c) > 5 and c[5].strip(): h0 = float(c[5])
        if c[0] == "298.15": h298 = float(c[5])
    return (h0 if h0 is not None else h298), h0 is None, hashlib.sha256(txt.encode()).hexdigest()

def load(d):
    r = {"c": {}, "e": {}, "m": {}}
    for f in glob.glob(os.path.join(d, "*.json")):
        k, n = os.path.basename(f)[:-5].split("_", 1); r[k][n] = json.load(open(f))
    return r

def rows_of(r):
    rows = {}
    for m in JAN:
        f = formula(m); nat = sum(f.values()); c = r["c"][m]; e = c["E_total_eV"] / (c["n_atomos"] / nat)
        for el, n in f.items(): e -= n * (r["m"][MOLREF[el]]["E_por_atomo_eV"] if el in ANION else r["e"][el]["E_por_atomo_eV"])
        h, f298, sh = janaf(m); an = [el for el in f if el in ANION][0]
        rows[m] = {"anion": an, "x_anion": f[an] / nat, "x_Ti": f.get("Ti", 0) / nat, "exp_eV_at": h / KJ / nat, "ref_298": f298,
                   "raw_eV_at": e / nat, "mp2020_eV_at": e / nat + MP[an] * f[an] / nat, "sha256_janaf": sh, "n_at_formula": nat}
    return rows

def fit_anion(rows, keys):
    out = {}
    for an in {rows[k]["anion"] for k in keys}:
        ks = [k for k in keys if rows[k]["anion"] == an]
        x = np.array([rows[k]["x_anion"] for k in ks]); y = np.array([rows[k]["exp_eV_at"] - rows[k]["raw_eV_at"] for k in ks])
        out[an] = float((x * y).sum() / (x * x).sum())
    return out

def evaluate(r):
    rows = rows_of(r); noTi = [k for k in rows if rows[k]["x_Ti"] == 0]
    for k in noTi:
        d = fit_anion(rows, [j for j in noTi if j != k]); rows[k]["loocv_eV_at"] = rows[k]["raw_eV_at"] + d[rows[k]["anion"]] * rows[k]["x_anion"]
    dX = fit_anion(rows, noTi)
    for k in rows: rows[k]["anion_corr_eV_at"] = rows[k]["raw_eV_at"] + dX[rows[k]["anion"]] * rows[k]["x_anion"]
    xt = np.array([rows[k]["x_Ti"] for k in TI_TRAIN]); rt = np.array([rows[k]["exp_eV_at"] - rows[k]["anion_corr_eV_at"] for k in TI_TRAIN])
    dTi = float((xt * rt).sum() / (xt * xt).sum())
    for k in rows: rows[k]["pred_eV_at"] = rows[k]["anion_corr_eV_at"] + dTi * rows[k]["x_Ti"]
    err = lambda key, ks: np.array([rows[k][key] - rows[k]["exp_eV_at"] for k in ks])
    e_test = err("pred_eV_at", TI_TEST); e_test0 = err("anion_corr_eV_at", TI_TEST); e_loo = err("loocv_eV_at", noTi)
    ofcn = [k for k in rows if rows[k]["anion"] in ("O", "F", "Cl", "N")]; e_mp = err("mp2020_eV_at", ofcn)
    # reacciones (energías brutas: δ se cancela); JANAF con ΔfH
    def H(m, key): return rows[m][key] * rows[m]["n_at_formula"]
    RX = {"R1": ({"MgAl2O4": 1}, {"MgO": 1, "Al2O3": 1}), "R2": ({"BeAl2O4": 1}, {"BeO": 1, "Al2O3": 1}), "R3": ({"MgTiO3": 1}, {"MgO": 1, "TiO2": 1}),
          "R4": ({"ZrSiO4": 1}, {"ZrO2": 1, "SiO2": 1}), "R5": ({"TiO2": 1}, {"TiO2_anatasa": 1}), "R6": ({"Ti2O3": 2}, {"TiO2": 3})}
    rx = {}
    for k, (p, s) in RX.items():
        nat = sum(n * rows[m]["n_at_formula"] for m, n in p.items())
        mod = (sum(n * H(m, "raw_eV_at") for m, n in p.items()) - sum(n * H(m, "raw_eV_at") for m, n in s.items())) / nat
        exp = (sum(n * H(m, "exp_eV_at") for m, n in p.items()) - sum(n * H(m, "exp_eV_at") for m, n in s.items())) / nat
        rx[k] = {"model_eV_at": mod, "exp_eV_at": exp, "mismo_signo": bool(np.sign(mod) == np.sign(exp))}
    # E_hull con energías de formación corregidas (elementos a 0)
    ents = [PDEntry(Composition(el), 0.0) for el in set(r["e"]) | ANION] + \
           [PDEntry(Composition({k2: v for k2, v in formula(m).items()}), rows[m]["pred_eV_at"] * rows[m]["n_at_formula"], name=m) for m in rows]
    ehull = {}
    for m in rows:
        els = set(formula(m)); sub = [e for e in ents if set(e.composition.as_dict()) <= els]
        pd = PhaseDiagram(sub); ent = [e for e in sub if getattr(e, "name", None) == m][0]; ehull[m] = float(pd.get_e_above_hull(ent))
    stable = [m for m in rows if m != "TiO2_anatasa"]
    S = {"n_total": len(rows), "n_sin_Ti": len(noTi), "delta_X_eV": dX, "delta_Ti_eV": dTi,
         "test_Ti_err_meV": dict(zip(TI_TEST, (e_test * 1e3).tolist())), "test_Ti_err_sin_dTi_meV": dict(zip(TI_TEST, (e_test0 * 1e3).tolist())),
         "MAE_test_Ti_meV": float(np.abs(e_test).mean() * 1e3), "MAE_test_Ti_sin_dTi_meV": float(np.abs(e_test0).mean() * 1e3),
         "MAE_loocv_meV": float(np.abs(e_loo).mean() * 1e3), "maxabs_loocv_test_meV": float(np.abs(np.r_[e_loo, e_test]).max() * 1e3),
         "peor": (noTi + TI_TEST)[int(np.abs(np.r_[e_loo, e_test]).argmax())], "n_mp2020": len(ofcn), "MAE_mp2020_meV": float(np.abs(e_mp).mean() * 1e3),
         "reacciones": rx, "MAE_reacciones_meV": float(np.mean([abs(v["model_eV_at"] - v["exp_eV_at"]) for v in rx.values()]) * 1e3),
         "n_signo_ok": int(sum(v["mismo_signo"] for v in rx.values())), "E_hull_meV": {k: v * 1e3 for k, v in ehull.items()},
         "max_E_hull_estables_meV": float(max(ehull[m] for m in stable) * 1e3), "E_hull_anatasa_meV": ehull["TiO2_anatasa"] * 1e3,
         "ref_298": [k for k in rows if rows[k]["ref_298"]], "loocv_err_meV": dict(zip(noTi, (e_loo * 1e3).tolist()))}
    return rows, S

def veredictos(ms, mc):
    v = lambda c: "PASA" if c else "FALLA"
    return {"H-U1": v(all(abs(x) <= 100 for x in ms["test_Ti_err_meV"].values())), "H-U2": v(ms["MAE_test_Ti_meV"] <= 0.5 * ms["MAE_test_Ti_sin_dTi_meV"]),
            "H-U3": v(ms["MAE_loocv_meV"] <= 60), "H-U4": v(ms["maxabs_loocv_test_meV"] <= 150), "H-U5": v(ms["MAE_loocv_meV"] <= mc["MAE_loocv_meV"]),
            "H-U6": v(ms["MAE_mp2020_meV"] <= 80), "H-U7": v(ms["n_signo_ok"] >= 5), "H-U8": v(ms["MAE_reacciones_meV"] <= 25),
            "H-U9": v(ms["max_E_hull_estables_meV"] <= 25 and ms["E_hull_anatasa_meV"] <= 50)}

def controles(r, d):
    c1 = all(x["convergio"] for k in "cem" for x in r[k].values())
    c2 = {m: x["V_A3"] / x["V0_A3"] - 1 for m, x in r["c"].items() if abs(x["V_A3"] / x["V0_A3"] - 1) > 0.08}
    old = json.load(open(f"/workspace/omniscience_cumf001/out/run1/{os.path.basename(d)}.json"))
    c3 = max(abs(r["c"][m]["E_total_eV"] / v["E_total_eV"] - 1) for m, v in old["compuestos"].items())
    return {"C1_todas_convergen": c1, "C2_fuera_8pc": c2, "C3_max_rel_vs_CUMF001": c3}

def main():
    out = {}
    for run in sys.argv[1:]:
        res = {}
        for mdl in ("mattersim", "mace"):
            d = os.path.join(run, mdl); r = load(d); rows, S = evaluate(r); res[mdl] = {"resumen": S, "filas": rows, "controles": controles(r, d)}
        res["hipotesis"] = veredictos(res["mattersim"]["resumen"], res["mace"]["resumen"]); out[os.path.basename(run)] = res
    if len(sys.argv) > 2:
        a, b = [load(os.path.join(sys.argv[i], "mattersim")) for i in (1, 2)]; a2, b2 = [load(os.path.join(sys.argv[i], "mace")) for i in (1, 2)]
        dif = max(abs(x[k][n]["E_total_eV"] / y[k][n]["E_total_eV"] - 1) for x, y in ((a, b), (a2, b2)) for k in "cem" for n in x[k])
        out["H-REP"] = {"max_dif_rel": dif, "veredictos_iguales": out["run1"]["hipotesis"] == out["run2"]["hipotesis"],
                        "veredicto": "PASA" if dif <= 1e-6 and out["run1"]["hipotesis"] == out["run2"]["hipotesis"] else "FALLA"}
    json.dump(out, open(os.path.join(HERE, "..", "results.json"), "w"), indent=1)
    print(json.dumps({k: v.get("hipotesis", v) for k, v in out.items()}, indent=1))
    for mdl in ("mattersim", "mace"):
        S = out["run1"][mdl]["resumen"]; print(mdl, {k: S[k] for k in S if k not in ("loocv_err_meV", "E_hull_meV")})

if __name__ == "__main__": main()
