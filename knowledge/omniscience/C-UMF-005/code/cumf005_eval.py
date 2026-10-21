#!/usr/bin/env python3
"""C-UMF-005: evaluación literal de los criterios congelados (prereg sha256 9bcb51e0…6121), figura e informe.
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)) + "/.."; O = H + "/out"; EXP = 9.0
J = lambda p: json.load(open(p)) if os.path.exists(p) else None
def dE(d, met, c):
    r, a = J(f"{d}/{met}_rutilo_normal_{c}.json"), J(f"{d}/{met}_anatasa_normal_{c}.json")
    return None if r is None or a is None else (a["E_por_atomo_eV"] - r["E_por_atomo_eV"]) * 1e3
v = lambda c: "NO EVALUABLE" if c is None else ("PASA" if c else "FALLA")
A = {"dE_R2SCAN": dE(O + "/a_run1", "R2SCAN", 1000), "dE_R2SCAN_run2": dE(O + "/a_run2", "R2SCAN", 1000), "dE_R2SCAN_1200": dE(O + "/a_run1", "R2SCAN", 1200),
     "dE_PBE": dE(O + "/a_run1", "PBE", 1000), "ref_GPAW_PBE": -30.51277029161703, "ref_GPAW_R2SCAN": -11.755556168644432, "exp": EXP}
B1, B2 = J(O + "/b_run1.json"), J(O + "/b_run2.json"); h = {}; x = A["dE_R2SCAN"]
CA1 = None if A["dE_PBE"] is None else abs(A["dE_PBE"] - A["ref_GPAW_PBE"]) <= 10
CA2 = None if x is None or A["dE_R2SCAN_1200"] is None else abs(A["dE_R2SCAN_1200"] - x) <= 2
h["H-A1"] = v(None if x is None else x > 0); h["H-A2"] = v(None if x is None else abs(x - EXP) <= 10)
h["H-A3"] = v(None if x is None or not CA1 else x - A["ref_GPAW_R2SCAN"] >= 5)
if B1:
    h["H-B1"] = v(B1["MAE_loocv_sel"] <= 32.63); h["H-B2"] = v(B1["MAE_capas_sel"] <= 36.3); h["H-B3"] = v(B1["max_abs_sel"] <= 150); h["H-B4"] = v(B1["MAE_loocv_sel"] <= 36.01)
else: h["H-B1"] = h["H-B2"] = h["H-B3"] = h["H-B4"] = "NO EVALUABLE"
rep = []
if x is not None and A["dE_R2SCAN_run2"] is not None: rep.append(abs(x - A["dE_R2SCAN_run2"]) <= 0.01)
if B1 and B2: rep.append(abs(B1["MAE_loocv_sel"] / B2["MAE_loocv_sel"] - 1) <= 1e-6 and B1["marcados"] == B2["marcados"])
h["H-REP"] = v(None if len(rep) < 2 else all(rep))
P = lambda *k: all(h[q] == "PASA" for q in k)
nivel = "E3" if P("H-A1", "H-A2", "H-B1", "H-B2", "H-REP") and CA1 and CA2 else ("E2" if (P("H-A1", "H-A2") and CA1) or P("H-B1", "H-B2", "H-REP") else "E1")
R = {"A": A, "B": B1, "B_run2": B2, "hipotesis": h, "controles": {"C-A1": CA1, "C-A2": CA2, "C-R_marcados": B1 and B1["marcados"], "C-R_capas": B1 and B1["capas_marcadas"]}, "rep_checks": rep, "nivel_E": nivel}
json.dump(R, open(H + "/results.json", "w"), indent=1, default=float); print(json.dumps(h), nivel); print(json.dumps(A))
# figura
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
lab = ["exp", "GPAW PBE", "GPAW r2SCAN\n(PAW-PBE)", "CP2K PBE", "CP2K r2SCAN\n(GTH-SCAN)"]; val = [EXP, A["ref_GPAW_PBE"], A["ref_GPAW_R2SCAN"], A["dE_PBE"], x]
ax[0].bar(lab, [0 if q is None else q for q in val], color=["k", "C0", "C1", "C2", "C3"]); ax[0].axhline(0, color="gray", lw=0.8); ax[0].axhspan(EXP - 10, EXP + 10, color="k", alpha=0.08)
ax[0].set_ylabel("ΔE(anatasa − rutilo) meV/át"); ax[0].set_title("A: orden TiO2"); ax[0].tick_params(axis="x", labelsize=7)
if B1:
    ax[1].bar(["base\nC-UMF-002", "D3 global\nC-UMF-004", "D3 selectivo\nC-UMF-005"], [32.63, 38.01, B1["MAE_loocv_sel"]], color=["C0", "C1", "C3"], label="MAE LOOCV (n=37)")
    ax[1].plot([0, 1, 2], [51.8, 5.35, B1["MAE_capas_sel"]], "ko-", label="MAE haluros en capas"); ax[1].legend(fontsize=7)
ax[1].set_ylabel("meV/át"); ax[1].set_title("B: ΔfH MatterSim"); fig.suptitle(f"C-UMF-005 · nivel {nivel} · Lázaro López Paz (ORCID 0000-0001-8601-1963), con asistencia de IA", fontsize=8)
fig.tight_layout(); fig.savefig(H + "/figs/C-UMF-005_resumen.png", dpi=130)
f = lambda q: "—" if q is None else f"{q:.1f}"
md = f"""# Resultados C-UMF-005 (prereg sha256 9bcb51e0…6121, congelado 20-oct-2026 20:40:14 UTC+2)
autoria: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963
## A. ΔE(anatasa−rutilo) meV/át, CP2K GTH-SCAN + TZV2P-MOLOPT-SCAN (experimento +9.0±1.4)
r2SCAN 1000 Ry {f(x)} (réplica {f(A['dE_R2SCAN_run2'])}; 1200 Ry {f(A['dE_R2SCAN_1200'])}) · PBE CP2K {f(A['dE_PBE'])} (GPAW −30.5) · GPAW r2SCAN con PAW-PBE −11.8
## B. D3 selectivo (regla R-dim)
marcados: {B1 and B1['marcados']} · MAE LOOCV {f(B1 and B1['MAE_loocv_sel'])} (base 32.6, D3 global 38.0) · capas {f(B1 and B1['MAE_capas_sel'])} (base 51.8) · máx {f(B1 and B1['max_abs_sel'])} ({B1 and B1['peor']}) · test Ti {f(B1 and B1['MAE_test_Ti_sel'])}
## Hipótesis
{json.dumps(h, ensure_ascii=False)}
controles: C-A1 {CA1} · C-A2 {CA2}
nivel: **{nivel}**
## Desviaciones y notas
- Antes de congelar el código, el smoke F-A1 falló dos veces por sintaxis del input (anidado &XC; en CP2K 2026 los funcionales libxc van como subsecciones MGGA_X_R2SCAN/MGGA_C_R2SCAN); corregido, el smoke convergió en 22 pasos (20:45 UTC+2).
- El fichero BASIS_MOLOPT_UZH_2026.2 instalado (sha256 8ca61714…) difiere del descargado (dd2a387f…), pero las entradas Ti y O TZV2P-MOLOPT-SCAN/PBE son idénticas; se usa el instalado.
- R-dim usa el atributo dimtype del intervalo de mayor puntuación de ASE (marca si dimtype ≠ "3D").
figura: figs/C-UMF-005_resumen.png · referencias: ver prereg (DOI)
"""
open(H + "/resultados_C-UMF-005.md", "w").write(md); print("informe ok")
