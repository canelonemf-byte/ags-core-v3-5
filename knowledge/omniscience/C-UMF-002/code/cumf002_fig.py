"""Figura original C-UMF-002: ΔfH predicha vs JANAF (MatterSim). Autoría: Lázaro López Paz, con asistencia de IA (ORCID 0000-0001-8601-1963)."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
r = json.load(open("results.json"))["run1"]["mattersim"]["filas"]
fig, ax = plt.subplots(figsize=(5, 5))
for k, x in r.items():
    y = x.get("loocv_eV_at", x["pred_eV_at"]); c = "C3" if x["x_Ti"] > 0 else "C0"
    ax.scatter(x["exp_eV_at"], y, c=c, s=18); ax.scatter(x["exp_eV_at"], x["mp2020_eV_at"], c="0.7", s=8, marker="x")
ax.plot([-4, 0], [-4, 0], "k-", lw=.8); ax.set_xlabel("ΔfH JANAF (eV/átomo)"); ax.set_ylabel("ΔfH MatterSim (eV/átomo)")
ax.set_title("C-UMF-002: azul LOOCV, rojo Ti (δ_Ti), gris MP2020"); fig.tight_layout(); fig.savefig("figs/fig_cumf002_paridad.png", dpi=150)
