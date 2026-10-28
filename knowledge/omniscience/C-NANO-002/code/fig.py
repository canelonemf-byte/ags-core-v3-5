#!/usr/bin/env python3
"""C-NANO-002 figura resumen desde results.json. Autoría: Lázaro López Paz (El Prat de Llobregat, Barcelona, España) con asistencia de IA."""
import json, os, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__)) + "/.."; R = json.load(open(f"{H}/results.json")); r = R["run1"]
fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))
for a, k, t in [(ax[0], "H1_tabla", "Γ ópticos vs DFT"), (ax[1], "H2_tabla", "Grafeno M/K vs Mounet GGA")]:
    lab = list(r[k]); v = [100 * r[k][x]["err_rel"] for x in lab]
    a.bar(range(len(v)), v, color=["tab:green" if abs(x) <= 5 else "tab:red" for x in v]); a.axhspan(-5, 5, alpha=.15)
    if "C2_mace" in R: a.plot(range(len(v)), [100 * R["C2_mace"][k][x]["err_rel"] for x in lab], "kx", label="MACE-MP-0")
    a.set_xticks(range(len(v))); a.set_xticklabels(lab, rotation=60, ha="right", fontsize=7); a.set_ylabel("error relativo MatterSim (%)"); a.set_title(t); a.legend(fontsize=7)
S = r["S"]; m = list(S); x = range(len(m))
ax[2].bar([i - .2 for i in x], [S[k]["dS"] for k in m], .4, label="ΔS (masivo MS+D3)"); ax[2].bar([i + .2 for i in x], [S[k]["dS_sinD3"] for k in m], .4, label="ΔS (masivo MS)")
ax[2].axhspan(0.05, 0.6, alpha=.15, label="banda H5"); ax[2].set_xticks(list(x)); ax[2].set_xticklabels(m); ax[2].set_ylabel("S_mono − S_masivo (k_B/át)"); ax[2].legend(fontsize=7); ax[2].set_title("S_vib(298) monocapa − masivo")
fig.suptitle("C-NANO-002 · MatterSim run1"); fig.tight_layout(); fig.savefig(f"{H}/figs/C-NANO-002_resumen.png", dpi=130); print("ok")
