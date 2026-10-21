"""C-MAT-005: figura descriptiva (escrita tras la congelación; no afecta a ningún veredicto). Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np
r = json.load(open("results.json")); M = list(r["por_modelo"]["mattersim"])
fig, ax = plt.subplots(figsize=(9, 3.6)); x = np.arange(len(M)); w = 0.2
for i, (mod, k, lab) in enumerate([("mattersim", "err_S_Vexp", "MatterSim V_exp"), ("mattersim", "err_S_V0", "MatterSim V0"), ("mace", "err_S_Vexp", "MACE V_exp"), ("mace", "err_S_V0", "MACE V0")]):
    y = [100 * r["por_modelo"][mod][m][k][2] if k in r["por_modelo"][mod][m] else np.nan for m in M]
    hatch = [None if r["por_modelo"][mod][m].get("evaluable_Vexp" if "Vexp" in k else "evaluable_V0") else "//" for m in M]
    for j in range(len(M)): ax.bar(x[j] + (i - 1.5) * w, y[j], w, color=f"C{i}", hatch=hatch[j], label=lab if j == 0 else None)
ax.axhspan(-10, 10, color="0.92", zorder=0); ax.axhline(0, color="k", lw=0.6)
ax.set_xticks(x, M, rotation=45, ha="right"); ax.set_ylabel("error relativo S(298.15 K) [%]"); ax.legend(fontsize=7, ncol=4)
ax.set_title("C-MAT-005: S armónica frente a NIST-JANAF (rayado = no evaluable, f_min < −0.3 THz)", fontsize=9)
fig.tight_layout(); fig.savefig("fig_C-MAT-005_S298.png", dpi=150); print("ok")
