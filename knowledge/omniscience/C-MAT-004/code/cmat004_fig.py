#!/usr/bin/env python3
"""C-MAT-004: figura propia del error de S(298.15 K) frente a NIST-JANAF. Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np
r = json.load(open("results.json")); M = list(r["por_modelo"]["mattersim"]); x = np.arange(len(M))
fig, ax = plt.subplots(2, 1, figsize=(10, 6.5), sharex=True)
for a, mod, tit in zip(ax, ["mattersim", "mace"], ["MatterSim v1.0.0-5M (float64)", "MACE-MP-0 medium (float64)"]):
    P = r["por_modelo"][mod]
    for k, lab, dx, mk in [("err_S_armV0", "armónico en V0", -0.25, "o"), ("err_S_armVexp", "armónico en V_exp", 0.0, "s"), ("err_S_corr", "QHA corregida (P_corr)", 0.25, "^")]:
        y = [100 * P[m][k][2] if k in P[m] and (k != "err_S_armVexp" or P[m]["arm_Vexp_ok"]) and (k != "err_S_armV0" or P[m]["arm_V0_ok"]) else np.nan for m in M]
        a.plot(x + dx, y, mk, label=lab, ms=6)
    for i, m in enumerate(M):
        if P[m]["patologico"]: a.text(i + 0.25, 0, "P", ha="center", va="center", fontsize=8, color="red")
    a.axhspan(-10, 10, color="0.9", zorder=0); a.axhline(0, color="k", lw=0.6); a.axvline(10.5, color="0.5", ls="--", lw=0.8)
    a.set_ylabel("error S298 (%)"); a.set_title(tit, fontsize=10); a.legend(fontsize=8, ncol=3, loc="upper right")
ax[1].set_xticks(x, M, rotation=45); ax[0].text(13.5, -8.5, "validación nueva (6)", ha="center", fontsize=8)
fig.text(0.01, 0.005, "C-MAT-004 · P = QHA patológica (excluida) · banda gris ±10 % · Lázaro López Paz, con asistencia de IA", fontsize=7)
fig.tight_layout(); fig.savefig("figs/fig_S298_err_JANAF.png", dpi=130)
