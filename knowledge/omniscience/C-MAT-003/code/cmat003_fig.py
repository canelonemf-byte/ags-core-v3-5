#!/usr/bin/env python3
"""Figura propia de C-MAT-003: error relativo de S frente a NIST-JANAF a 298.15 y 600 K (armónico y QHA, tres potenciales).
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = json.load(open("results.json")); M = ["Si", "MgO", "NaCl", "LiF", "NaF", "KCl", "KBr", "CaO", "CaF2", "Al2O3", "BeO"]
lab = {"mattersim": "MatterSim-v1-5M", "sevenn": "SevenNet-0", "mace": "MACE-MP-0 (base)"}; col = {"mattersim": "#1b7837", "sevenn": "#2166ac", "mace": "#b2182b"}
fig, axs = plt.subplots(1, 2, figsize=(11, 5.6), sharey=True); x = np.arange(len(M))
for ax, (T, i) in zip(axs, [("298.15 K", 2), ("600 K", 3)]):
    for k, mod in enumerate(["mace", "sevenn", "mattersim"]):
        P = R["por_modelo"][mod]; dx = (k - 1) * 0.25
        ya = [100 * P[m]["err_S_arm"][i] if "err_S_arm" in P[m] else np.nan for m in M]
        yq = [100 * P[m]["err_S_qha"][i] if P[m].get("err_S_qha") and P[m]["err_S_qha"][i] is not None else np.nan for m in M]
        ax.scatter(x + dx, ya, marker="o", facecolors="none", edgecolors=col[mod], s=30, label=f"{lab[mod]} armónico")
        yq = np.array(yq); big = yq > 40
        ax.scatter((x + dx)[~big], yq[~big], marker="s", color=col[mod], s=22, label=f"{lab[mod]} QHA")
        if big.any(): ax.scatter((x + dx)[big], np.full(big.sum(), 38.5), marker="^", color=col[mod], s=40, label=f"{lab[mod]} QHA fuera de escala (sin horquilla de volumen)")
    if i in (2, 3):
        E = json.load(open("results_exploratorio_vexp.json"))
        ye = [100 * E[f"mattersim:{m}"]["err_S%s_Vpartida" % ("298" if i == 2 else "600")] for m in M]
        ax.scatter(x + 0.25, ye, marker="D", facecolors="none", edgecolors="k", s=22, label="MatterSim armónico en celda de partida (exploratorio)")
    ax.set_ylim(-12, 40); ax.axhspan(-10, 10, color="0.9", zorder=0); ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(x); ax.set_xticklabels(M, rotation=45); ax.set_title(f"S a {T}"); ax.grid(axis="y", alpha=0.3)
axs[0].set_ylabel("(S calc − S JANAF) / S JANAF  [%]"); h, l = axs[1].get_legend_handles_labels(); fig.legend(h, l, fontsize=7, loc="lower center", ncol=3, frameon=False)
fig.suptitle("C-MAT-003 · entropía desde fonones frente a NIST-JANAF (banda gris: ±10 %)", fontsize=10)
fig.tight_layout(rect=(0, 0.17, 1, 1)); fig.savefig("figs/fig_S_err_JANAF.png", dpi=150)
