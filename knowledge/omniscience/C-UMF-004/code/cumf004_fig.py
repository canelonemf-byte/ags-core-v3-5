#!/usr/bin/env python3
"""C-UMF-004: figura propia (A: ΔE anatasa−rutilo por método; B: error LOOCV sin/con D3).
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os, sys
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__)) + "/.."; R = json.load(open(H + "/results.json")); A = R["A"]
b0 = json.load(open("/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-UMF-002/results.json"))["run1"]["mattersim"]["resumen"]["loocv_err_meV"]
sys.path.insert(0, "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-UMF-002/code"); import cumf002_eval as e2
f, ax = plt.subplots(1, 2, figsize=(11, 4.4))
lab = [("PBE geom. exp.", -29.72), ("r2SCAN geom. exp.", -11.67), ("PBE relajada", A["dE_PBE_relaj"]), ("r2SCAN relajada", A["dE_R2SCAN_relaj"]),
       ("r2SCAN relaj. + vib", A["dH_R2SCAN_vib"]), ("HSE06 (k reducido)", A["dE_HSE06_reducido"])]
lab = [(l, x) for l, x in lab if x is not None]
ax[0].barh([l for l, _ in lab], [x for _, x in lab], color="#4a7bb7"); ax[0].axvspan(7.6, 10.4, color="orange", alpha=.45, label="experimento +9.0±1.4")
ax[0].axvline(0, color="k", lw=.8); ax[0].set_xlabel("ΔE(anatasa − rutilo) [meV/át]"); ax[0].legend(fontsize=8); ax[0].set_title("A. Orden de polimorfos TiO2")
try:
    d3 = e2.evaluate(e2.load(H + "/out/b_run1/mattersim"))[1]["loocv_err_meV"]; ks = sorted(d3)
    ax[1].scatter([b0[k] for k in ks], [d3[k] for k in ks], s=18, color="#888")
    for k in ("MgCl2", "CaI2", "MgBr2"): ax[1].scatter(b0[k], d3[k], color="red", s=30); ax[1].annotate(k, (b0[k], d3[k]), fontsize=8)
    lim = max(abs(x) for x in list(b0.values()) + list(d3.values())) * 1.1; ax[1].plot([-lim, lim], [-lim, lim], "k--", lw=.7); ax[1].set_xlim(-lim, lim); ax[1].set_ylim(-lim, lim)
except Exception as ex: ax[1].text(.1, .5, "B pendiente: " + repr(ex)[:40], transform=ax[1].transAxes)
ax[1].set_xlabel("error LOOCV MatterSim [meV/át]"); ax[1].set_ylabel("error LOOCV MatterSim+D3 [meV/át]"); ax[1].set_title("B. ΔfH sin Ti (n=37)")
f.text(.01, .005, "Lázaro López Paz, El Prat de Llobregat, con asistencia de IA · ORCID 0000-0001-8601-1963 · C-UMF-004", fontsize=7)
f.tight_layout(); os.makedirs(H + "/figs", exist_ok=True); f.savefig(H + "/figs/C-UMF-004_resumen.png", dpi=150); print("fig ok")
