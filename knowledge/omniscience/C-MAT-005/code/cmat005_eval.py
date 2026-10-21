#!/usr/bin/env python3
"""Evalúa C-MAT-005 con los criterios congelados del prereg. Uso: python code/cmat005_eval.py [run1|run2]
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os, sys, hashlib, statistics
RUN = sys.argv[1] if len(sys.argv) > 1 else "run1"; OTHER = "run2" if RUN == "run1" else "run1"
M = ["AlN", "SiC", "KF", "NaBr", "KI", "LiCl", "CsCl", "SrF2", "BaF2", "Na2O", "ZrO2", "BeAl2O4", "MgTiO3", "ZrSiO4"]
CTRL = ["Si", "MgO"]; MODELS = ["mattersim", "mace"]; STAB = -0.3; NMIN = 12; TOL_REP = 1e-6
REF = json.load(open("refs/refs_termo_C-MAT-005.json"))["materiales"]
C4P = "/workspace/omniscience_cmat004/C-MAT-004/out/run1"
rel = lambda a, b: (a - b) / b
def mare(v): v = [abs(x) for x in v]; return sum(v) / len(v) if v else None
def load(run, mod): return {m: json.load(open(f"out/{run}/{mod}/{m}.json")) for m in M + CTRL if os.path.exists(f"out/{run}/{mod}/{m}.json")}
def core_hash(run, mod):
    s = json.dumps(load(run, mod), indent=1, sort_keys=True); open(f"out/{run}/results_core_{mod}.json", "w").write(s); return hashlib.sha256(s.encode()).hexdigest()
res = {"run_principal": RUN, "por_modelo": {}, "hipotesis": {}, "controles": {}, "replica": {}}
D = {mod: load(RUN, mod) for mod in MODELS}; D2 = {mod: load(OTHER, mod) for mod in MODELS}
for mod in MODELS:
    P = {}
    for m in M:
        if m not in D[mod]: P[m] = {"estado": "FALTA", "ok": False}; continue
        r = D[mod][m]; J = REF[m]; v0, ve, vg = r["arm_V0"], r["arm_Vexp"], r["arm_Vexp_grande"]
        conv = abs(vg["S"][2] - ve["S"][2]) / ve["S"][2]
        e = {"V0_sobre_Vexp": r["V0_sobre_Vexp"], "fmin_V0": v0["fmin_THz"], "fmin_Vexp": ve["fmin_THz"], "evaluable_V0": v0["fmin_THz"] >= STAB,
             "evaluable_Vexp": ve["fmin_THz"] >= STAB, "conv_C4": conv, "inconcluso_C4": conv > 0.02, "c3_norm_Vexp": ve["c3_norm"],
             "err_S_V0": [rel(a, b) for a, b in zip(v0["S"], J["S"])], "err_S_Vexp": [rel(a, b) for a, b in zip(ve["S"], J["S"])],
             "err_CvVexp_vs_Cp": [rel(a, b) for a, b in zip(ve["Cv"], J["Cp"])], "S_Vexp": ve["S"], "Cv_Vexp": ve["Cv"]}
        e["ok"] = e["evaluable_Vexp"] and not e["inconcluso_C4"]; P[m] = e
    res["por_modelo"][mod] = P
PM = res["por_modelo"]["mattersim"]; PX = res["por_modelo"]["mace"]; H = res["hipotesis"]
okm = [m for m in M if PM[m]["ok"]]
n1 = sum(1 for m in okm if abs(PM[m]["err_S_Vexp"][2]) <= 0.10)
H["H1"] = {"n_dentro_10pc": n1, "de": len(M), "umbral": 12, "veredicto": "PASA" if n1 >= 12 else "FALSADA"}
def mare_h(vals, n, thr): return {"MARE": mare(vals), "n": n, "veredicto": "INCONCLUSA" if n < NMIN else ("PASA" if mare(vals) <= thr else "FALSADA")}
H["H2"] = mare_h([PM[m]["err_S_Vexp"][2] for m in okm], len(okm), 0.05)
c3 = [m for m in okm if PM[m]["evaluable_V0"]]; a3, b3 = mare([PM[m]["err_S_Vexp"][2] for m in c3]), mare([PM[m]["err_S_V0"][2] for m in c3])
H["H3"] = {"MARE_Vexp": a3, "MARE_V0": b3, "n": len(c3), "veredicto": "INCONCLUSA" if len(c3) < NMIN else ("PASA" if a3 < b3 else "FALSADA")}
c4 = [m for m in okm if PX[m]["ok"]]; a4, b4 = mare([PM[m]["err_S_Vexp"][2] for m in c4]), mare([PX[m]["err_S_Vexp"][2] for m in c4])
H["H4"] = {"MARE_mattersim": a4, "MARE_mace": b4, "cociente": (a4 / b4) if b4 else None, "n": len(c4), "veredicto": "INCONCLUSA" if len(c4) < NMIN else ("PASA" if a4 <= 0.6 * b4 else "FALSADA")}
H["H5"] = mare_h([PM[m]["err_CvVexp_vs_Cp"][2] for m in okm], len(okm), 0.05)
H["H6"] = mare_h([PM[m]["err_S_Vexp"][3] for m in okm], len(okm), 0.05)
med = statistics.median([PM[m]["err_S_Vexp"][2] for m in okm]) if okm else None
H["H7"] = {"mediana_err_S298": med, "n": len(okm), "veredicto": "INCONCLUSA" if len(okm) < NMIN else ("PASA" if abs(med) <= 0.03 else "FALSADA")}
# Réplica con tolerancia numérica fijada a priori
rep = {}
for mod in MODELS:
    bad = []; maxrel = 0.0; same_class = True
    for m in M + CTRL:
        if m not in D[mod] or m not in D2[mod]: bad.append((m, "FALTA")); continue
        for blk in ("arm_V0", "arm_Vexp", "arm_Vexp_grande"):
            if blk not in D[mod][m]: continue
            for q in ("S", "Cv"):
                for x, y in zip(D[mod][m][blk][q], D2[mod][m][blk][q]):
                    rr = abs(x - y) / abs(x) if x else abs(y); maxrel = max(maxrel, rr)
                    if rr > TOL_REP: bad.append((m, blk, q))
            if (D[mod][m][blk]["fmin_THz"] >= STAB) != (D2[mod][m][blk]["fmin_THz"] >= STAB): same_class = False
    rep[mod] = {"max_rel": maxrel, "fuera_tolerancia": bad[:20], "n_fuera": len(bad), "clase_estabilidad_igual": same_class,
                "sha256_" + RUN: core_hash(RUN, mod), "sha256_" + OTHER: core_hash(OTHER, mod)}
    rep[mod]["byte_identico"] = rep[mod]["sha256_" + RUN] == rep[mod]["sha256_" + OTHER]
res["replica"] = rep
H["H-REP"] = {"veredicto": "PASA" if all(rep[m]["n_fuera"] == 0 and rep[m]["clase_estabilidad_igual"] for m in MODELS) else "FALSADA",
              "nota": "veredictos iguales entre run1 y run2: se comprueba comparando results.json y results_replica_run2.json"}
# Controles
C = res["controles"]; c1 = {}
for mod in MODELS:
    for m in CTRL:
        p = f"{C4P}/{mod}/{m}.json"
        if os.path.exists(p) and m in D[mod]: c1[f"{mod}_{m}"] = rel(D[mod][m]["arm_Vexp"]["S"][2], json.load(open(p))["arm_Vexp"]["S"][2])
C["C1"] = {"desv": c1, "pasa": len(c1) == 4 and all(abs(x) <= 1e-4 for x in c1.values())}
C["C2"] = {"fallos": {mod: [m for m in M if res["por_modelo"][mod][m].get("evaluable_Vexp") and not (0.99 <= res["por_modelo"][mod][m]["c3_norm_Vexp"] <= 1.000001)] for mod in MODELS}}
C["C2"]["pasa"] = not any(C["C2"]["fallos"].values())
C["C3_convergencia"] = {mod: {m: res["por_modelo"][mod][m].get("conv_C4") for m in M} for mod in MODELS}
C["no_evaluables_Vexp"] = {mod: [m for m in M if not res["por_modelo"][mod][m].get("evaluable_Vexp", False)] for mod in MODELS}
C["inconclusos_C4"] = {mod: [m for m in M if res["por_modelo"][mod][m].get("inconcluso_C4")] for mod in MODELS}
# Prueba de artefacto (rutilo y cuarzo-α)
def jl(p): return json.load(open(p)) if os.path.exists(p) else None
art = {}
g5, g6 = jl("out/dft/TiO2_PBE/g500_result.json"), jl("out/dft/TiO2_PBE/g650_result.json")
q5, q6 = jl("out/dft/SiO2_PBE/g500_result.json"), jl("out/dft/SiO2_PBE/g650_result.json")
def dmax(a, b): return None if not (a and b) else max(abs(x - y) for x, y in zip(a["freq_commensurate_THz"]["0.000,0.000,0.000"], b["freq_commensurate_THz"]["0.000,0.000,0.000"]))
cdft = {"TiO2": dmax(g5, g6), "SiO2": dmax(q5, q6)}; C["C_DFT_ecut"] = {k: {"max_dif_Gamma_THz": v, "pasa": v is not None and v <= 0.15} for k, v in cdft.items()}
for mat, hid in (("TiO2", "H-D1"), ("SiO2", "H-D2")):
    pbe, lda = jl(f"out/dft/{mat}_PBE/sc_result.json"), jl(f"out/dft/{mat}_LDA/sc_result.json")
    e = {"PBE_fmin_comm": pbe and pbe["fmin_commensurate_THz"], "LDA_fmin_comm": lda and lda["fmin_commensurate_THz"],
         "PBE_relax_ok": bool(pbe and pbe["relax"]["converged"]), "C_DFT_ecut_pasa": C["C_DFT_ecut"][mat]["pasa"]}
    for mod in MODELS:
        a = jl(f"out/{RUN}/artefacto/{mod}/{mat}.json"); e[mod] = None if a is None else {"fmin_comm": a["sc_dft"]["fmin_commensurate_THz"], "fmin_mesh_misma_sc": a["sc_dft"]["fmin_mesh_interp_THz"],
              "fmin_mesh_sc_C4": a["sc_c4"]["fmin_mesh_interp_THz"], "q_fmin_sc_C4": a["sc_c4"]["q_fmin_mesh"]}
    def clase(mod):
        a = e[mod]
        if a is None or pbe is None or not e["PBE_relax_ok"] or not e["C_DFT_ecut_pasa"]: return "INCONCLUSA_DFT"
        if a["fmin_comm"] >= STAB: return "C_no_reproducida_en_q_conmensurados"
        if pbe["fmin_commensurate_THz"] >= STAB: return "A_artefacto_del_potencial"
        if lda is not None and lda["fmin_commensurate_THz"] >= STAB: return "B1_heredada_de_PBE_(LDA_estable)"
        return "B2_heredada_de_PBE_(LDA_inestable_o_sin_dato)"
    e["clase_mattersim"] = clase("mattersim"); e["clase_mace"] = clase("mace")
    cm = e["clase_mattersim"]
    e["veredicto"] = "CONFIRMADA" if cm.startswith("A_") else ("REFUTADA" if cm.startswith("B") else "INCONCLUSA")
    H[hid] = e
json.dump(res, open("results.json" if RUN == "run1" else "results_replica_run2.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: v["veredicto"] for k, v in H.items()}, indent=0))
for k, v in H.items(): print(k, {a: b for a, b in v.items() if a != "veredicto"})
print("C1", C["C1"], "\nC2", C["C2"], "\nno_eval", C["no_evaluables_Vexp"], "inconc", C["inconclusos_C4"], "\nC_DFT", C["C_DFT_ecut"])
for mod in MODELS:
    for m in M:
        e = res["por_modelo"][mod][m]
        if "err_S_Vexp" in e: print(mod, m, "V0/Vexp %.3f fmin V0 %.2f Vexp %.2f | S298 V0 %+.3f Vexp %+.3f | S600 %+.3f | Cv/Cp298 %+.3f | conv %.4f" % (e["V0_sobre_Vexp"], e["fmin_V0"], e["fmin_Vexp"], e["err_S_V0"][2], e["err_S_Vexp"][2], e["err_S_Vexp"][3], e["err_CvVexp_vs_Cp"][2], e["conv_C4"]))
