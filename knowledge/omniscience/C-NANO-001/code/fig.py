"""Figura C-NANO-001 (original). Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = json.load(open("results.json")); fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
for k, c in (("run1_mattersim", "tab:blue"), ("run1_mace", "tab:orange")):
    mt = R[k]["metales"]; ax[0].scatter([v["ref"] for v in mt.values()], [v["gamma_w"] for v in mt.values()], c=c, s=22, label=k.replace("run1_", ""))
    for m, v in mt.items():
        if k == "run1_mattersim": ax[0].annotate(m, (v["ref"], v["gamma_w"]), fontsize=7)
ax[0].plot([0, 3.6], [0, 3.6], "k-", lw=.8); ax[0].set_xlabel("γ̄ PBE Tran et al. 2016 [J/m²]"); ax[0].set_ylabel("γ̄ potencial universal (3 facetas) [J/m²]"); ax[0].legend()
t = R["run1_mattersim"]["tio2"]; labs, vals, cols = [], [], []
for f, c in (("rutilo", "tab:green"), ("anatasa", "tab:purple")):
    for h, g in t[f]["facetas"].items(): labs.append(f"{f[:3]}({h})"); vals.append(g); cols.append(c)
ax[1].bar(labs, vals, color=cols); ax[1].axhline(0.44, ls=":", c="tab:purple"); ax[1].axhline(0.31, ls=":", c="tab:green")
ax[1].set_ylabel("γ MatterSim [J/m²]"); ax[1].set_title(f"d* = {t['d_estrella_nm']:.1f} nm · Δγ̄(R−A) = {t['delta_gamma']:.3f} J/m²", fontsize=9); ax[1].tick_params(axis="x", rotation=45)
fig.suptitle("C-NANO-001 · líneas punteadas: PBE Lazzeri 2002 · L. López Paz con asistencia de IA · CC BY 4.0", fontsize=9); fig.tight_layout(); fig.savefig("figs/C-NANO-001_resumen.png", dpi=130)
