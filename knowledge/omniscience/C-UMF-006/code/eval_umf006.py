#!/usr/bin/env python3
"""C-UMF-006 evaluación tal cual. Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)) + "/.."; O = f"{H}/out"
def E(tag):
    f = f"{O}/{tag}.json"; return json.load(open(f))["E_por_atomo_eV"] if os.path.exists(f) else None
def delta(met, rc=""):
    a, r = E(f"{met}_anatasa_base_600{rc}"), E(f"{met}_rutilo_base_600{rc}"); return None if a is None or r is None else 1000 * (a - r)
R = {}
dP, dH = delta("PBE"), delta("PBE0TC"); dH3 = delta("PBE0TC", "_rc3")
R["dE_PBE_gamma"] = dP; R["dE_PBE0TC_gamma"] = dH
vm = json.load(open(f"{O}/vib_mattersim.json")) if os.path.exists(f"{O}/vib_mattersim.json") else None
vc = json.load(open(f"{O}/vib_mace.json")) if os.path.exists(f"{O}/vib_mace.json") else None
if dP is not None and dH is not None:
    d = dH - dP; Eh = -30.7 + d; R.update({"delta_hyb": d, "E_hyb": Eh, "HA1": "PASA" if d > 0 else "FALLA", "HA3": "PASA" if Eh > 0 else "FALLA"})
    if vm: tot = Eh + vm["delta_A_menos_R_meV_at"]["U_vib_eV_at"]; R.update({"E_hyb_mas_vib": tot, "HA2": "PASA" if -1.0 <= tot <= 19.0 else "FALLA"})
else: R.update({"HA1": "NO EVALUABLE", "HA2": "NO EVALUABLE", "HA3": "NO EVALUABLE"})
if vm:
    R["vib_mattersim"] = {f: {k: vm[f][k] for k in ("clase", "f_imag", "fmin_THz")} for f in ("rutilo", "anatasa")}; R["dvib_ms"] = vm["delta_A_menos_R_meV_at"]
    R["HB1"] = "PASA" if all(vm[f]["clase"] in ("normal", "evaluable_con_regla") for f in ("rutilo", "anatasa")) else "FALLA"
    R["HB2"] = "PASA" if abs(vm["delta_A_menos_R_meV_at"]["U_vib_eV_at"]) <= 5 else "FALLA"
rep_i = None
if vm and vc: R["dvib_mace"] = vc["delta_A_menos_R_meV_at"]; rep_i = abs(vc["delta_A_menos_R_meV_at"]["U_vib_eV_at"] - vm["delta_A_menos_R_meV_at"]["U_vib_eV_at"]) <= 3
rep_ii = None
if dH3 is not None and dP is not None and "delta_hyb" in R: R["delta_hyb_rc3"] = dH3 - dP; rep_ii = abs(R["delta_hyb_rc3"] - R["delta_hyb"]) <= 5
R["H_REP"] = {"i": rep_i, "ii": "NO EVALUABLE" if rep_ii is None else rep_ii, "veredicto": "PASA" if (rep_i and rep_ii is not False) else "FALLA"}
R["nivel_E"] = "E2" if (R["H_REP"]["veredicto"] == "PASA" and R["HA1"] != "NO EVALUABLE") else "E1"
json.dump(R, open(f"{H}/results.json", "w"), indent=1, ensure_ascii=False); print(json.dumps(R, indent=1, ensure_ascii=False))
